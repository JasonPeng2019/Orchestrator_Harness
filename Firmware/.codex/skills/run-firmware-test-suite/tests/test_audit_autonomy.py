from __future__ import annotations

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


if __name__ == "__main__":
    unittest.main()
