from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_autonomy.py"
SPEC = importlib.util.spec_from_file_location("firmware_audit_autonomy", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {SCRIPT}")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class AuditRunDiscoveryTests(unittest.TestCase):
    def discover(self, root: Path) -> tuple[list[str], list[tuple[Path, str, str]]]:
        original_root = MODULE.ROOT
        MODULE.ROOT = root
        errors: list[str] = []
        try:
            runs = MODULE.unfinished_main_runs(errors)
        finally:
            MODULE.ROOT = original_root
        return errors, runs

    def write_run_state(self, root: Path, name: str, status: str) -> Path:
        run = root / "fresh-experiments" / name
        workspace = run / ".agent-workspace"
        workspace.mkdir(parents=True)
        (workspace / "RUN_STATE.json").write_text(
            json.dumps({"status": status}) + "\n", encoding="utf-8"
        )
        return run

    def test_current_run_state_is_the_primary_status_source(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            run = self.write_run_state(root, "H00_smoke", "CREATED")
            errors, runs = self.discover(root)
            self.assertEqual([], errors)
            self.assertEqual([(run, "H00", "CREATED")], runs)

    def test_green_current_run_is_not_returned(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.write_run_state(root, "H00_green", "GREEN")
            errors, runs = self.discover(root)
            self.assertEqual([], errors)
            self.assertEqual([], runs)

    def test_historical_status_remains_supported(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            run = root / "fresh-experiments" / "H00_legacy"
            run.mkdir(parents=True)
            (run / "STATUS.md").write_text(
                "# Status\n\n**State:** `CHECKPOINTED`\n", encoding="utf-8"
            )
            errors, runs = self.discover(root)
            self.assertEqual([], errors)
            self.assertEqual([(run, "H00", "CHECKPOINTED")], runs)


class AuditDocumentationTests(unittest.TestCase):
    def write_documentation_fixture(self, root: Path) -> None:
        server = root / "BYO-Firmware-MCP"
        mirror = root / "Firmware resources" / "server-guides"
        document_text = {
            "README.md": (
                '"<absolute-path-to-BYO-Firmware-MCP>" pyocd-debug-mcp\n'
                "# Firmware-suite repair path\n$plan-changes\n$change-loop\n"
            ),
            "SERVER_GUIDE.md": "initialization_handshake\ntools/list\n",
        }
        for relative in MODULE.SERVER_DOCUMENTS:
            text = document_text.get(relative, f"# {relative}\n")
            for base in (server, mirror):
                path = base / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
        documents = {
            "README.md": (
                "BYO-Firmware-MCP/README.md\nBYO-Firmware-MCP/SERVER_GUIDE.md\n"
                "$plan-changes\n$change-loop\n.agent-workspace/SUITE_COORDINATION.md\n"
            ),
            "AGENTS.md": "$plan-changes\n$change-loop\nNever launch Q11\n",
            "Firmware resources/README.md": (
                "not a second authority\n../BYO-Firmware-MCP/README.md\nmirror identical\n"
            ),
            ".codex/skills/run-firmware-test-suite/SKILL.md": (
                "BYO-Firmware-MCP/README.md\nBYO-Firmware-MCP/SERVER_GUIDE.md\n"
                "manager-verified production-code defect\n"
            ),
            ".codex/skills/plan-changes/SKILL.md": (
                "BYO-Firmware-MCP/README.md\n"
                "Firmware resources/test-program/design_charter.md\n"
            ),
            ".codex/skills/change-loop/SKILL.md": (
                "BYO-Firmware-MCP/README.md\n"
                "historical copies under `Firmware resources/test-program/`\n"
            ),
            "multi-agent-logs/PROGRESS_REMAINING.md": (
                "current package-local coordination ledger\nDo not start Q11\n2026-08-14\n"
            ),
        }
        for relative, text in documents.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")

    def check_documentation(self, root: Path) -> list[str]:
        original_root = MODULE.ROOT
        MODULE.ROOT = root
        errors: list[str] = []
        try:
            MODULE.check_documentation_navigation(errors)
        finally:
            MODULE.ROOT = original_root
        return errors

    def test_documentation_navigation_accepts_one_matching_mirror(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.write_documentation_fixture(root)
            self.assertEqual([], self.check_documentation(root))

    def test_documentation_navigation_rejects_a_stale_mirror(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.write_documentation_fixture(root)
            mirror = root / "Firmware resources" / "server-guides" / "SERVER_GUIDE.md"
            mirror.write_text("stale\n", encoding="utf-8")
            errors = self.check_documentation(root)
            self.assertIn(
                "server-document mirror differs from live source: BYO-Firmware-MCP/SERVER_GUIDE.md",
                errors,
            )


class AuditResultCorrectionTests(unittest.TestCase):
    def run_audit(
        self,
        result: dict[str, object],
        sidecar: dict[str, object] | None = None,
        result_bytes: bytes | None = None,
    ) -> list[str]:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            run = root / "fresh-experiments" / "A21_sidecar"
            workspace = run / ".agent-workspace"
            workspace.mkdir(parents=True)
            (workspace / "RESULT.schema.json").write_text(
                json.dumps({"properties": {"status": {"enum": ["PASS", "SERVER_FAILURE"]}}}),
                encoding="utf-8",
            )
            source_bytes = (
                result_bytes
                if result_bytes is not None
                else json.dumps(result, indent=2).encode("utf-8")
            )
            (workspace / "RESULT.json").write_bytes(source_bytes)
            if sidecar is not None:
                (workspace / "RESULT_AUDIT_CORRECTION.json").write_text(
                    json.dumps(sidecar, indent=2),
                    encoding="utf-8",
                )
            errors: list[str] = []
            MODULE.check_run(errors, run, "A21", "CHECKPOINTED")
            return errors

    def sidecar_for(
        self,
        result: dict[str, object],
        *,
        pointer: str = "/finding",
        original_value: str = "operator must connect the board",
        corrected_text: str = "Historical out-of-authority wording recorded.",
    ) -> dict[str, object]:
        result_bytes = json.dumps(result, indent=2).encode("utf-8")
        return {
            "schema": MODULE.RESULT_AUDIT_CORRECTION_SCHEMA,
            "source_result_sha256": hashlib.sha256(result_bytes).hexdigest(),
            "created_by_epoch": "suite011",
            "entries": [
                {
                    "json_pointer": pointer,
                    "original_value_sha256": hashlib.sha256(
                        original_value.encode("utf-8")
                    ).hexdigest(),
                    "disposition": MODULE.RESULT_AUDIT_CORRECTION_DISPOSITION,
                    "corrected_text": corrected_text,
                }
            ],
        }

    def test_result_action_is_rejected_without_sidecar(self) -> None:
        errors = self.run_audit(
            {"status": "PASS", "finding": "operator must connect the board"}
        )
        self.assertTrue(any("operator action" in error for error in errors))

    def test_valid_hash_bound_sidecar_accepts_historical_result(self) -> None:
        result = {"status": "PASS", "finding": "operator must connect the board"}
        self.assertEqual([], self.run_audit(result, self.sidecar_for(result)))

    def test_sidecar_rejects_stale_result_hash(self) -> None:
        result = {"status": "PASS", "finding": "operator must connect the board"}
        sidecar = self.sidecar_for(result)
        sidecar["source_result_sha256"] = "0" * 64
        errors = self.run_audit(result, sidecar)
        self.assertTrue(any("source hash does not match" in error for error in errors))

    def test_sidecar_rejects_wrong_value_hash_and_pointer(self) -> None:
        result = {"status": "PASS", "finding": "operator must connect the board"}
        wrong_hash = self.sidecar_for(result, original_value="wrong")
        errors = self.run_audit(result, wrong_hash)
        self.assertTrue(any("original value hash does not match" in error for error in errors))

        bad_pointer = self.sidecar_for(result, pointer="/missing")
        errors = self.run_audit(result, bad_pointer)
        self.assertTrue(any("JSON pointer is invalid" in error for error in errors))
        self.assertTrue(any("no correction entry" in error for error in errors))

    def test_sidecar_rejects_unsafe_corrected_text(self) -> None:
        result = {"status": "PASS", "finding": "operator must connect the board"}
        sidecar = self.sidecar_for(
            result,
            corrected_text="Do not defer; set NEEDS_USER.",
        )
        errors = self.run_audit(result, sidecar)
        self.assertTrue(any("unsafe corrected_text" in error for error in errors))

    def test_sidecar_rejects_duplicate_result_object_keys(self) -> None:
        result_bytes = (
            b'{"status":"PASS","finding":"operator must connect the board",'
            b'"finding":"user should attach the cable"}\n'
        )
        sidecar = {
            "schema": MODULE.RESULT_AUDIT_CORRECTION_SCHEMA,
            "source_result_sha256": hashlib.sha256(result_bytes).hexdigest(),
            "created_by_epoch": "suite011",
            "entries": [
                {
                    "json_pointer": "/finding",
                    "original_value_sha256": hashlib.sha256(
                        b"user should attach the cable"
                    ).hexdigest(),
                    "disposition": MODULE.RESULT_AUDIT_CORRECTION_DISPOSITION,
                    "corrected_text": "Historical wording recorded.",
                }
            ],
        }
        errors = self.run_audit({}, sidecar, result_bytes=result_bytes)
        self.assertTrue(
            any(
                "cannot read RESULT.json" in error
                and "duplicate JSON object key" in error
                for error in errors
            )
        )

    def test_sidecar_rejects_unaccounted_second_offending_string(self) -> None:
        result = {
            "status": "PASS",
            "finding": "operator must connect the board",
            "second_finding": "user should attach the cable",
        }
        sidecar = self.sidecar_for(result)
        errors = self.run_audit(result, sidecar)
        self.assertTrue(any("/second_finding has no correction entry" in error for error in errors))

    def test_sidecar_rejects_open_shape_and_duplicate_entries(self) -> None:
        result = {"status": "PASS", "finding": "operator must connect the board"}
        open_sidecar = self.sidecar_for(result)
        open_sidecar["unexpected"] = True
        errors = self.run_audit(result, open_sidecar)
        self.assertTrue(any("open or invalid shape" in error for error in errors))

        duplicate_sidecar = self.sidecar_for(result)
        duplicate_sidecar["entries"] = [
            duplicate_sidecar["entries"][0],
            duplicate_sidecar["entries"][0],
        ]
        errors = self.run_audit(result, duplicate_sidecar)
        self.assertTrue(any("duplicates JSON pointer" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
