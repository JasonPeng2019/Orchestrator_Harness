from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SKILL_ROOT = ROOT / ".codex" / "skills" / "run-firmware-test-suite"
POLICY_SHA256 = "be10f776c27fa8ffb46b8d395ac791ee0d73c235cf8a0d079fc960612a00f126"
APPENDIX_IDS = {"D35", "R37", "R38"}
ALLOWED_RESULT_STATUSES = {"PASS", "SERVER_FAILURE"}
BLOCKER_STATUS_RE = re.compile(
    r"\b(return|report|write|set)\b.*\b(NEEDS_USER|INFRA_BLOCKED)\b",
    re.IGNORECASE,
)
BLOCKER_NEGATION_RE = re.compile(r"\b(never|do not|invalid|prohibit)\b", re.IGNORECASE)
OPERATOR_ACTION_RE = re.compile(
    r"\b(operator|user)\s+(must|should|needs? to)\b",
    re.IGNORECASE,
)
SHA256_RE = re.compile(r"[0-9a-f]{64}")
RESULT_AUDIT_CORRECTION_SCHEMA = "firmware-result-audit-correction/v1"
RESULT_AUDIT_CORRECTION_DISPOSITION = "OUT_OF_AUTHORITY_FINDING"
MATRIX_IDS = {
    "S13",
    "A20",
    "A21",
    "A22",
    "A23",
    "A24",
    "A25",
    "A26",
    "D30",
    "D31",
    "D32",
    "D33",
    "D34",
    "D36",
    "Q40",
    "Q41",
}
ROSTER_OWNED_IDS = {
    "S10",
    "S11",
    "S12",
    "S13",
    "A20",
    "A21",
    "A22",
    "A23",
    "A24",
    "A25",
    "A26",
    "D30",
    "D31",
    "D32",
    "D33",
    "D34",
    "D36",
    "Q41",
}
SERVER_DOCUMENTS = (
    "README.md",
    "SERVER_GUIDE.md",
    "docs/architecture.md",
    "docs/client-contract.md",
    "docs/plan-tool-contract.md",
    "docs/Live_Edit_Docs/trusted-cmsis-pack-admission-spec.md",
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="strict")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def check_package_boundary(errors: list[str]) -> None:
    required = (
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "PROVIDER_ADAPTER.md",
        ROOT / "BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md",
        ROOT / "BYO-Firmware-MCP",
        ROOT / "Firmware resources" / "datasheets" / "stm32L476rgt.pdf",
        ROOT / "Firmware resources" / "datasheets" / "Nano_BLE_MCU-nRF52840_PS_v1.1.pdf",
        SKILL_ROOT / "SKILL.md",
        ROOT / ".codex" / "skills" / "plan-changes" / "SKILL.md",
        ROOT / ".codex" / "skills" / "change-loop" / "SKILL.md",
        ROOT / "scripts" / "orchestration" / "prompt_policy.py",
        ROOT / "scripts" / "orchestration" / "build_server_snapshot.py",
        ROOT / "multi-agent-logs" / "HANDOFF.md",
        ROOT / "multi-agent-logs" / "PROGRESS_REMAINING.md",
        ROOT / "multi-agent-logs" / "current-state" / "CURRENT_SUITE_STATE.json",
        ROOT / "multi-agent-logs" / "current-state" / "CURRENT_RELEVANT_PROCESS_INVENTORY.json",
        ROOT / "Firmware resources" / "test-program" / "design_charter.md",
        SKILL_ROOT / "references" / "execution-contract.md",
    )
    for path in required:
        if not path.exists():
            fail(errors, f"missing package-local dependency: {path.relative_to(ROOT)}")

    live_docs = (
        ROOT / "BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md",
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        SKILL_ROOT / "SKILL.md",
        SKILL_ROOT / "references" / "execution-contract.md",
        SKILL_ROOT / "references" / "model-continuity-contract.md",
    )
    forbidden = (
        "MCP-Trial-3",
        "../.codex",
        "stable-general-harness-runner",
    )
    for path in live_docs:
        text = read_text(path)
        for value in forbidden:
            if value in text:
                fail(
                    errors,
                    f"{path.relative_to(ROOT)}: parent-repository dependency: {value}",
                )


def check_documentation_navigation(errors: list[str]) -> None:
    """Keep one current server-document source and a checked package-local mirror."""

    server_root = ROOT / "BYO-Firmware-MCP"
    mirror_root = ROOT / "Firmware resources" / "server-guides"
    for relative in SERVER_DOCUMENTS:
        source = server_root / relative
        mirror = mirror_root / relative
        if not source.is_file():
            fail(errors, f"missing live server document: BYO-Firmware-MCP/{relative}")
            continue
        if not mirror.is_file():
            fail(errors, f"missing server-document mirror: server-guides/{relative}")
            continue
        if source.read_bytes() != mirror.read_bytes():
            fail(
                errors,
                f"server-document mirror differs from live source: BYO-Firmware-MCP/{relative}",
            )

    server_readme = server_root / "README.md"
    server_guide = server_root / "SERVER_GUIDE.md"
    if server_readme.is_file():
        readme = read_text(server_readme)
        for forbidden in ("FirmCLI_Tester", "C:\\Users\\Jason"):
            if forbidden in readme:
                fail(errors, f"BYO-Firmware-MCP/README.md: stale local path: {forbidden}")
        for required in (
            '"<absolute-path-to-BYO-Firmware-MCP>"',
            "pyocd-debug-mcp",
            "Firmware-suite repair path",
            "$plan-changes",
            "$change-loop",
        ):
            if required not in readme:
                fail(errors, f"BYO-Firmware-MCP/README.md: missing guidance: {required}")
    if server_guide.is_file():
        guide = read_text(server_guide)
        for required in ("initialization_handshake", "tools/list"):
            if required not in guide:
                fail(errors, f"BYO-Firmware-MCP/SERVER_GUIDE.md: missing live-tool rule: {required}")

    navigation_requirements = {
        "README.md": (
            "BYO-Firmware-MCP/README.md",
            "BYO-Firmware-MCP/SERVER_GUIDE.md",
            "$plan-changes",
            "$change-loop",
            ".agent-workspace/SUITE_COORDINATION.md",
        ),
        "AGENTS.md": ("$plan-changes", "$change-loop", "Never launch Q11"),
        "Firmware resources/README.md": (
            "not a second authority",
            "../BYO-Firmware-MCP/README.md",
            "mirror identical",
        ),
        ".codex/skills/run-firmware-test-suite/SKILL.md": (
            "BYO-Firmware-MCP/README.md",
            "BYO-Firmware-MCP/SERVER_GUIDE.md",
            "manager-verified production-code defect",
        ),
        ".codex/skills/plan-changes/SKILL.md": (
            "BYO-Firmware-MCP/README.md",
            "Firmware resources/test-program/design_charter.md",
        ),
        ".codex/skills/change-loop/SKILL.md": (
            "BYO-Firmware-MCP/README.md",
            "historical copies under `Firmware resources/test-program/`",
        ),
        "multi-agent-logs/PROGRESS_REMAINING.md": (
            "current package-local coordination ledger",
            "Do not start Q11",
            "2026-08-14",
        ),
    }
    for relative, required_phrases in navigation_requirements.items():
        path = ROOT / relative
        if not path.is_file():
            fail(errors, f"missing documentation-navigation file: {relative}")
            continue
        text = read_text(path)
        for required in required_phrases:
            if required not in text:
                fail(errors, f"{relative}: missing documentation-navigation clause: {required}")
    progress_path = ROOT / "multi-agent-logs" / "PROGRESS_REMAINING.md"
    if progress_path.is_file() and "historical coordination evidence" in read_text(progress_path):
        fail(errors, "PROGRESS_REMAINING.md: stale coordination-ledger classification")


def check_target_harness(errors: list[str], *, required: bool) -> None:
    target = ROOT / "target-harness"
    if not target.exists():
        if required:
            fail(errors, "missing package-local WIP product worktree: target-harness")
        return
    required_paths = (
        target / ".git",
        target / "orchestrator_harness" / "cli.py",
        target / "orchestrator_harness" / "lane_controller.py",
        target / "harness_watcher_implementation" / "__main__.py",
        target / "harness_watcher_implementation" / "settings.py",
        target / "docs" / "HARNESS_WATCHER_GUIDE.md",
    )
    for path in required_paths:
        if not path.exists():
            fail(
                errors,
                f"target-harness missing WIP runtime file: {path.relative_to(target)}",
            )
    if any(not path.exists() for path in required_paths):
        return
    cli = read_text(target / "orchestrator_harness" / "cli.py")
    watcher = read_text(target / "harness_watcher_implementation" / "__main__.py")
    settings = read_text(target / "harness_watcher_implementation" / "settings.py")
    for phrase in ("watch_until_actionable", "--until-actionable", "EXIT_TIMEOUT"):
        if phrase not in cli:
            fail(errors, f"target-harness bounded watch is missing: {phrase}")
    for phrase in ('"start"', '"status"', '"stop"', "--owner-pid"):
        if phrase not in watcher:
            fail(errors, f"target-harness deterministic watcher is missing: {phrase}")
    if "harness_watcher_active = True" not in settings:
        fail(errors, "target-harness deterministic watcher feature gate is not active")


def unfinished_main_runs(errors: list[str]) -> list[tuple[Path, str, str]]:
    runs: list[tuple[Path, str, str]] = []
    fresh_root = ROOT / "fresh-experiments"
    if not fresh_root.exists():
        return runs
    for run in sorted(fresh_root.iterdir()):
        if not run.is_dir():
            continue
        test_id = run.name.split("_", 1)[0]
        if test_id in APPENDIX_IDS or test_id == "Q40":
            continue
        state_path = run / ".agent-workspace" / "RUN_STATE.json"
        if state_path.exists():
            try:
                status = json.loads(read_text(state_path)).get("status")
            except (OSError, UnicodeError, json.JSONDecodeError, TypeError) as exc:
                fail(errors, f"{run.name}: unreadable RUN_STATE.json: {exc}")
                continue
            if not isinstance(status, str) or not status:
                fail(errors, f"{run.name}: RUN_STATE.json lacks a status")
                continue
            if status == "GREEN":
                continue
            runs.append((run, test_id, status))
            continue

        # Retained historical runs may predate RUN_STATE.json.
        status_path = run / "STATUS.md"
        if not status_path.exists():
            fail(errors, f"{run.name}: missing RUN_STATE.json and historical STATUS.md")
            continue
        status_text = read_text(status_path)
        if "`TERMINAL_GREEN`" in status_text:
            continue
        match = re.search(r"\*\*State:\*\*\s+`([^`]+)`", status_text)
        if match is None:
            fail(errors, f"{run.name}: STATUS.md lacks a machine-readable State field")
            continue
        runs.append((run, test_id, match.group(1)))
    return runs


def check_policy(errors: list[str]) -> None:
    policy = ROOT / ".agent-workspace" / "AUTONOMOUS_EXECUTION_POLICY.md"
    sidecar = ROOT / ".agent-workspace" / "AUTONOMOUS_EXECUTION_POLICY.sha256"
    actual = hashlib.sha256(policy.read_bytes()).hexdigest()
    recorded = read_text(sidecar).split()[0].lower()
    if actual != POLICY_SHA256 or recorded != POLICY_SHA256:
        fail(
            errors,
            f"autonomy policy hash mismatch: expected={POLICY_SHA256} actual={actual} sidecar={recorded}",
        )


def check_imported_progress(errors: list[str]) -> None:
    state_path = ROOT / "multi-agent-logs" / "current-state" / "CURRENT_SUITE_STATE.json"
    inventory_path = ROOT / "multi-agent-logs" / "current-state" / "CURRENT_RELEVANT_PROCESS_INVENTORY.json"
    try:
        state = json.loads(read_text(state_path))
        inventory = json.loads(read_text(inventory_path))
    except (OSError, ValueError) as exc:
        fail(errors, f"imported progress is unreadable: {exc}")
        return

    validation = state.get("m5_validation", {})
    if (
        state.get("active_epoch") is not None
        or validation.get("active_goal_attempt_count") != 10
        or validation.get("active_goal_attempt_limit") != 10
        or validation.get("next_active_goal_attempt") is not None
        or validation.get("status") != "CLOSED_ATTEMPT_LIMIT_EVIDENCE_INSUFFICIENT"
    ):
        fail(errors, "imported M5 progress does not describe the closed Q10 boundary")
    if inventory.get("disposition") != "SAFE_BOUNDARY" or inventory.get("live_relevant") != []:
        fail(errors, "imported process inventory is not an empty safe boundary")

    for path in (
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md",
        SKILL_ROOT / "SKILL.md",
        ROOT / ".agent-workspace" / "SUITE_COORDINATION.md",
    ):
        normalized = " ".join(read_text(path).lower().split())
        if "never launch q11" not in normalized:
            fail(
                errors,
                f"{path.relative_to(ROOT)}: missing resume-boundary clause: never launch Q11",
            )

    for path in (
        ROOT / "README.md",
        ROOT / "BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md",
        SKILL_ROOT / "SKILL.md",
        ROOT / ".agent-workspace" / "SUITE_COORDINATION.md",
    ):
        if "manager evidence" not in " ".join(read_text(path).lower().split()):
            fail(
                errors,
                f"{path.relative_to(ROOT)}: Q10 manager-evidence cause is missing",
            )


def check_catalog_skill_and_matrix(errors: list[str]) -> None:
    catalog_path = ROOT / "BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md"
    catalog = read_text(catalog_path)
    main_catalog = catalog.split("## Appendix A", 1)[0]
    required_catalog_text = (
        "Zero-operator, no-external-blocker contract",
        "`NEEDS_USER` and `INFRA_BLOCKED` are invalid terminal outcomes",
        "another chat pause",
    )
    for required in required_catalog_text:
        if required not in main_catalog:
            fail(errors, f"{catalog_path.name}: missing autonomy clause: {required}")
    forbidden_catalog_text = (
        "perform the human-approved",
        "user/operator must provide",
        "until the user corrects",
        "ask the user to inspect",
        "ask the user to move",
    )
    for forbidden in forbidden_catalog_text:
        if forbidden.lower() in main_catalog.lower():
            fail(errors, f"{catalog_path.name}: main catalog contains: {forbidden}")

    matrix_path = ROOT / ".agent-workspace" / "AUTONOMY_REQUIREMENT_MATRIX.md"
    if not matrix_path.exists():
        fail(errors, "missing AUTONOMY_REQUIREMENT_MATRIX.md")
    else:
        matrix = read_text(matrix_path)
        if POLICY_SHA256 not in matrix:
            fail(errors, "autonomy matrix lacks policy hash")
        for test_id in sorted(MATRIX_IDS):
            if f"| {test_id} |" not in matrix:
                fail(errors, f"autonomy matrix lacks {test_id}")

    skill = read_text(SKILL_ROOT / "SKILL.md")
    if "AUTONOMY_REQUIREMENT_MATRIX.md" not in skill:
        fail(errors, "skill does not require autonomy matrix")
    if "audit_autonomy.py" not in skill:
        fail(errors, "skill does not require deterministic autonomy audit")


def check_parallel_contract(errors: list[str]) -> None:
    required_by_file = {
        "BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md": (
            "fill all five lanes concurrently where eligible",
            "including work from later rows that is already eligible",
            "not a serial schedule",
            "a blocked lane never holds an unrelated lane",
            "target-harness/",
            "harness_watcher_implementation",
            ".agent-workspace/epochs/<epoch>/",
            "this table is the authoritative catalog-level cross-test dependency graph",
            "an unlisted edge does not exist",
        ),
        ".codex/skills/run-firmware-test-suite/SKILL.md": (
            "launch or resume **all** eligible named doer lanes concurrently",
            "same scheduling batch",
            "continue unrelated lanes while another waits",
            "target-harness/",
            "harness_watcher_implementation",
            ".agent-workspace/epochs/<epoch>/",
            "catalog section 11.1 is the authoritative cross-test edge list",
        ),
        ".codex/skills/run-firmware-test-suite/references/execution-contract.md": (
            "launch or resume every eligible non-conflicting lane in the same batch",
            "never wait for a blocked lane",
            "catalog section 11.1 is the authoritative cross-test edge list",
            "package-local `target-harness/`",
            "bounded diagnostic wait",
        ),
        ".codex/skills/run-firmware-test-suite/references/doer-roster.md": (
            "every dependency-ready, resource-compatible doer lane concurrently",
            "a blocked lane never holds an unrelated lane",
        ),
        ".agent-workspace/SUITE_COORDINATION.md": (
            "every dependency-ready, resource-compatible named lane concurrently",
            "a waiting lane never stops unrelated work",
        ),
    }
    for relative, required_phrases in required_by_file.items():
        normalized = " ".join(read_text(ROOT / relative).lower().split())
        for required in required_phrases:
            if required not in normalized:
                fail(
                    errors,
                    f"{relative}: missing parallel-contract clause: {required}",
                )

    roster_path = SKILL_ROOT / "references" / "doer-roster.md"
    assigned: dict[str, str] = {}
    for line in read_text(roster_path).splitlines():
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) < 4 or cells[1] not in {
            "Atlas",
            "Boreal",
            "Cygnus",
            "Delta",
            "Nova",
        }:
            continue
        # Provider settings belong to PROVIDER_ADAPTER.md. This roster contains
        # only doer/task assignments, so the final cell is the task allocation.
        task_cell = next(
            (cell for cell in reversed(cells[2:]) if cell),
            "",
        )
        for test_id in re.findall(r"\b(?:S|A|D|Q)\d{2}\b", task_cell):
            if test_id in assigned:
                fail(
                    errors,
                    f"doer-roster.md: duplicate assignment for {test_id}",
                )
            assigned[test_id] = cells[1]
    if set(assigned) != ROSTER_OWNED_IDS:
        fail(
            errors,
            "doer-roster.md: coverage mismatch "
            f"missing={sorted(ROSTER_OWNED_IDS - set(assigned))} "
            f"extra={sorted(set(assigned) - ROSTER_OWNED_IDS)}",
        )
    if assigned.get("A23") != "Nova":
        fail(errors, "doer-roster.md: A23 must be assigned only to Nova")


def check_cross_document_contract(errors: list[str]) -> None:
    catalog_path = ROOT / "BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md"
    skill_path = SKILL_ROOT / "SKILL.md"
    execution_path = SKILL_ROOT / "references" / "execution-contract.md"
    roster_path = SKILL_ROOT / "references" / "doer-roster.md"
    provider_path = ROOT / "PROVIDER_ADAPTER.md"
    catalog = read_text(catalog_path)
    main_catalog = catalog.split("## Appendix A", 1)[0]
    skill = read_text(skill_path)
    execution = read_text(execution_path)

    required_by_file = {
        catalog_path.name: (
            "PROVIDER_ADAPTER.md",
            "fresh-experiments/<test-id>_<timestamp>/",
            "Treat setup/APP-1 repetitions, returning-state repetitions",
            "60852689.DS_SX1261_2 V2-2.pdf",
            "nrf-sx-pin-mappings.md",
            "Every production-server repair uses `Firmware resources/test-program/design_charter.md`",
        ),
        str(skill_path.relative_to(ROOT)): (
            "PROVIDER_ADAPTER.md",
            "The manager rereads `Firmware resources/test-program/design_charter.md`",
        ),
        str(execution_path.relative_to(ROOT)): (
            "PROVIDER_ADAPTER.md",
            "For A24/A25 only",
            "60852689.DS_SX1261_2 V2-2.pdf",
            ".agent-workspace/FIXTURE.md",
        ),
    }
    texts = {
        catalog_path.name: catalog,
        str(skill_path.relative_to(ROOT)): skill,
        str(execution_path.relative_to(ROOT)): execution,
    }
    for label, phrases in required_by_file.items():
        normalized = " ".join(texts[label].split())
        for phrase in phrases:
            if phrase not in normalized:
                fail(errors, f"{label}: missing cross-document clause: {phrase}")

    provider = " ".join(read_text(provider_path).split())
    for phrase in (
        "`deepseek-v4-flash:0731-cloud`",
        "`qwen3.5:397b-cloud`",
        "The implemented Firmware-local route is Qwen Code 0.21.10 through Ollama's OpenAI-compatible endpoint",
        "The admitted target-lane entry point, run from `Firmware/`",
        "Qwen Code is the active Firmware route",
        "Codex remains inadmissible until its own dedicated",
        "DeepSeek and Qwen do not receive a Fast/Priority service-tier setting",
        "max",
        "high",
        "Terra XHigh",
    ):
        if phrase not in provider:
            fail(errors, f"PROVIDER_ADAPTER.md: missing provider-contract clause: {phrase}")

    for stale in (
        "I2C waveform",
        "measured SCL",
        "| DIO trace,",
        "runs/<experiment>/<agent>-<timestamp>/",
        "MCP-Trial-3",
    ):
        if stale.lower() in main_catalog.lower():
            fail(errors, f"{catalog_path.name}: stale external/path contract: {stale}")
    if "the exact Codex settings above" in skill:
        fail(errors, f"{skill_path.relative_to(ROOT)}: ambiguous doer settings")
    if "S12 and S13 pass with all four boards" in catalog:
        fail(errors, f"{catalog_path.name}: S13 retains a blanket all-board barrier")
    if "independent passive logic/BLE/RF/serial oracle" in execution:
        fail(
            errors,
            f"{execution_path.relative_to(ROOT)}: stale external-oracle permission",
        )
    required_heading_levels = {
        "#### Q40 — Nonduplicative cross-agent bug-hunt corpus",
        "#### Future version-to-version regression policy",
        "### D35 — Autonomous lifecycle and endpoint-loss handling",
        "### R37 — Target lock and destructive recovery",
        "### R38 — Bootloader tool truthfulness",
    }
    missing_headings = sorted(required_heading_levels - set(catalog.splitlines()))
    if missing_headings:
        fail(
            errors,
            f"{catalog_path.name}: inconsistent heading levels: {missing_headings}",
        )

    def roster_assignments(text: str) -> dict[str, str]:
        result: dict[str, str] = {}
        for line in text.splitlines():
            cells = [cell.strip() for cell in line.split("|")]
            if len(cells) < 4 or cells[1] not in {
                "Atlas",
                "Boreal",
                "Cygnus",
                "Delta",
                "Nova",
            }:
                continue
            result[cells[1]] = cells[2]
        return result

    catalog_roster = roster_assignments(catalog)
    skill_roster = roster_assignments(read_text(roster_path))
    if catalog_roster != skill_roster:
        fail(
            errors,
            f"catalog/doer-roster mismatch: catalog={catalog_roster} skill={skill_roster}",
        )


def _operational_violations(text: str) -> set[str]:
    violations: set[str] = set()
    for line in text.splitlines():
        if BLOCKER_STATUS_RE.search(line) and not BLOCKER_NEGATION_RE.search(line):
            violations.add("blocker status")
        if OPERATOR_ACTION_RE.search(line):
            violations.add("operator action")
    return violations


def _scan_operational_text(errors: list[str], label: str, text: str) -> None:
    """Apply the existing line-based operational-file rules to one file."""

    for number, line in enumerate(text.splitlines(), 1):
        if BLOCKER_STATUS_RE.search(line) and not BLOCKER_NEGATION_RE.search(line):
            fail(errors, f"{label}:{number}: blocker status")
        if OPERATOR_ACTION_RE.search(line):
            fail(errors, f"{label}:{number}: operator action")


def _escape_json_pointer_token(token: str) -> str:
    return token.replace("~", "~0").replace("/", "~1")


def _decode_json_pointer_token(token: str) -> str:
    if re.search(r"~(?:[^01]|$)", token):
        raise ValueError("invalid escape in JSON pointer")
    return token.replace("~1", "/").replace("~0", "~")


def _resolve_json_pointer(document: object, pointer: str) -> object:
    if pointer == "":
        return document
    if not pointer.startswith("/"):
        raise ValueError("JSON pointer must be empty or start with '/'")

    current = document
    for raw_token in pointer[1:].split("/"):
        token = _decode_json_pointer_token(raw_token)
        if isinstance(current, dict):
            if token not in current:
                raise KeyError(token)
            current = current[token]
        elif isinstance(current, list):
            if token == "-" or not re.fullmatch(r"0|[1-9][0-9]*", token):
                raise KeyError(token)
            index = int(token)
            if index >= len(current):
                raise KeyError(token)
            current = current[index]
        else:
            raise KeyError(token)
    return current


def _iter_json_strings(
    value: object,
    pointer: str = "",
    *,
    include_object_keys: bool = True,
) -> list[tuple[str, str, str]]:
    """Return ``(kind, pointer, text)`` for JSON strings and object keys."""

    strings: list[tuple[str, str, str]] = []
    if isinstance(value, str):
        strings.append(("value", pointer, value))
    elif isinstance(value, dict):
        for key, child in value.items():
            child_pointer = f"{pointer}/{_escape_json_pointer_token(key)}"
            if include_object_keys:
                strings.append(("key", pointer, key))
            strings.extend(
                _iter_json_strings(
                    child,
                    child_pointer,
                    include_object_keys=include_object_keys,
                )
            )
    elif isinstance(value, list):
        for index, child in enumerate(value):
            strings.extend(
                _iter_json_strings(
                    child,
                    f"{pointer}/{index}",
                    include_object_keys=include_object_keys,
                )
            )
    return strings


def _load_json_without_duplicate_keys(text: str) -> object:
    def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON object key: {key}")
            result[key] = value
        return result

    return json.loads(text, object_pairs_hook=reject_duplicate_keys)


def _result_string_violations(
    errors: list[str],
    run_name: str,
    result: object,
    *,
    emit: bool,
) -> dict[str, tuple[str, set[str]]]:
    offending: dict[str, tuple[str, set[str]]] = {}
    for kind, pointer, text in _iter_json_strings(result):
        violations = _operational_violations(text)
        if not violations:
            continue
        if kind != "value":
            for violation in sorted(violations):
                fail(
                    errors,
                    f"{run_name}/RESULT.json object key {text!r}: {violation}",
                )
            continue
        offending[pointer] = (text, violations)
        if emit:
            for violation in sorted(violations):
                fail(errors, f"{run_name}/RESULT.json{pointer}: {violation}")
    return offending


def _scan_sidecar_strings(errors: list[str], run_name: str, sidecar: object) -> None:
    for kind, pointer, text in _iter_json_strings(sidecar):
        # corrected_text is checked below with a dedicated message so it is not
        # reported twice; all other sidecar strings remain operational files.
        if kind == "value" and pointer.startswith("/entries/") and pointer.endswith("/corrected_text"):
            continue
        for violation in sorted(_operational_violations(text)):
            fail(errors, f"{run_name}/RESULT_AUDIT_CORRECTION.json{pointer}: {violation}")


def _check_result_audit_correction(
    errors: list[str],
    run: Path,
    result_path: Path,
) -> tuple[bool, bool]:
    """Validate a hash-bound result correction and return checked-file flags."""

    workspace = result_path.parent
    sidecar_path = workspace / "RESULT_AUDIT_CORRECTION.json"
    if not sidecar_path.exists():
        return False, False

    run_name = run.name
    if not result_path.is_file():
        fail(
            errors,
            f"{run_name}: RESULT_AUDIT_CORRECTION.json requires readable RESULT.json",
        )
        return False, False

    result_bytes: bytes | None = None
    try:
        result_bytes = result_path.read_bytes()
        result = json.loads(result_bytes.decode("utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError) as exc:
        fail(errors, f"{run_name}: RESULT_AUDIT_CORRECTION.json cannot read RESULT.json: {exc}")
        result_checked = False
    else:
        result_checked = True
        result_offenses = _result_string_violations(errors, run_name, result, emit=False)

    try:
        sidecar_text = read_text(sidecar_path)
        sidecar = _load_json_without_duplicate_keys(sidecar_text)
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        fail(errors, f"{run_name}: invalid RESULT_AUDIT_CORRECTION.json: {exc}")
        return result_checked, False

    sidecar_checked = True
    _scan_sidecar_strings(errors, run_name, sidecar)
    expected_keys = {
        "schema",
        "source_result_sha256",
        "created_by_epoch",
        "entries",
    }
    if not isinstance(sidecar, dict) or set(sidecar) != expected_keys:
        fail(errors, f"{run_name}: RESULT_AUDIT_CORRECTION.json has an open or invalid shape")
        return result_checked, sidecar_checked

    if sidecar["schema"] != RESULT_AUDIT_CORRECTION_SCHEMA:
        fail(errors, f"{run_name}: RESULT_AUDIT_CORRECTION.json schema is invalid")
    source_hash = sidecar["source_result_sha256"]
    if not isinstance(source_hash, str) or SHA256_RE.fullmatch(source_hash) is None:
        fail(errors, f"{run_name}: RESULT_AUDIT_CORRECTION.json source hash is not lowercase SHA-256")
    elif result_checked and result_bytes is not None:
        actual_hash = hashlib.sha256(result_bytes).hexdigest()
        if source_hash != actual_hash:
            fail(
                errors,
                f"{run_name}: RESULT_AUDIT_CORRECTION.json source hash does not match RESULT.json",
            )

    created_by_epoch = sidecar["created_by_epoch"]
    if not isinstance(created_by_epoch, str) or not created_by_epoch.strip():
        fail(errors, f"{run_name}: RESULT_AUDIT_CORRECTION.json created_by_epoch is empty")

    entries = sidecar["entries"]
    if not isinstance(entries, list) or not entries:
        fail(errors, f"{run_name}: RESULT_AUDIT_CORRECTION.json entries must be non-empty")
        return result_checked, sidecar_checked

    entry_keys = {
        "json_pointer",
        "original_value_sha256",
        "disposition",
        "corrected_text",
    }
    pointers: dict[str, tuple[int, dict[str, object]]] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or set(entry) != entry_keys:
            fail(errors, f"{run_name}: correction entry {index} has an open or invalid shape")
            continue
        pointer = entry["json_pointer"]
        if not isinstance(pointer, str):
            fail(errors, f"{run_name}: correction entry {index} has an invalid JSON pointer")
        elif pointer in pointers:
            fail(errors, f"{run_name}: correction entry {index} duplicates JSON pointer {pointer!r}")
        else:
            pointers[pointer] = (index, entry)

        original_hash = entry["original_value_sha256"]
        if not isinstance(original_hash, str) or SHA256_RE.fullmatch(original_hash) is None:
            fail(errors, f"{run_name}: correction entry {index} has an invalid value hash")
        if entry["disposition"] != RESULT_AUDIT_CORRECTION_DISPOSITION:
            fail(errors, f"{run_name}: correction entry {index} has an invalid disposition")
        corrected_text = entry["corrected_text"]
        if not isinstance(corrected_text, str) or not corrected_text.strip():
            fail(errors, f"{run_name}: correction entry {index} has empty corrected_text")
        elif _operational_violations(corrected_text):
            fail(errors, f"{run_name}: correction entry {index} has unsafe corrected_text")

    if not result_checked:
        return result_checked, sidecar_checked

    for pointer, (index, entry) in pointers.items():
        try:
            value = _resolve_json_pointer(result, pointer)
        except (KeyError, TypeError, ValueError) as exc:
            fail(errors, f"{run_name}: correction entry {index} JSON pointer is invalid: {exc}")
            continue
        if not isinstance(value, str):
            fail(errors, f"{run_name}: correction entry {index} JSON pointer does not resolve to a string")
            continue
        value_hash = hashlib.sha256(value.encode("utf-8")).hexdigest()
        if entry["original_value_sha256"] != value_hash:
            fail(errors, f"{run_name}: correction entry {index} original value hash does not match")
        if pointer not in result_offenses:
            fail(errors, f"{run_name}: correction entry {index} points to a non-offending result string")

    for pointer, (text, violations) in result_offenses.items():
        if pointer not in pointers:
            fail(errors, f"{run_name}: RESULT.json{pointer} has no correction entry")

    return result_checked, sidecar_checked


def check_run(
    errors: list[str],
    run: Path,
    test_id: str,
    status: str,
) -> None:
    workspace = run / ".agent-workspace"
    amendments = workspace / "SPEC_AMENDMENTS.md"
    if amendments.exists():
        text = read_text(amendments)
        notice_index = text.find("**Effective interpretation notice**")
        first_amendment_index = text.find("## Amendment ")
        if notice_index < 0 or (first_amendment_index >= 0 and notice_index > first_amendment_index):
            fail(
                errors,
                f"{run.name}: effective-interpretation notice is missing or not before history",
            )
        headings = list(
            re.finditer(
                rf"^## Amendment {re.escape(test_id)}-(\d+).*$",
                text,
                re.MULTILINE,
            )
        )
        if not headings:
            fail(errors, f"{run.name}: no numbered amendment")
        else:
            tail = text[headings[-1].start() :]
            retired_duplicate = test_id == "H05" and "must not be launched" in tail
            if POLICY_SHA256 not in tail and not retired_duplicate:
                fail(
                    errors,
                    f"{run.name}: latest amendment lacks autonomy-policy hash",
                )

    schema_path = workspace / "RESULT.schema.json"
    try:
        schema = json.loads(read_text(schema_path))
        statuses = set(schema["properties"]["status"]["enum"])
        if statuses != ALLOWED_RESULT_STATUSES:
            fail(
                errors,
                f"{run.name}: RESULT schema statuses={sorted(statuses)}",
            )
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
        fail(errors, f"{run.name}: invalid RESULT schema: {exc}")

    result_path = workspace / "RESULT.json"
    if result_path.exists():
        try:
            result_status = json.loads(read_text(result_path)).get("status")
            if result_status in {"NEEDS_USER", "INFRA_BLOCKED"}:
                fail(errors, f"{run.name}: stale blocker RESULT={result_status}")
        except (OSError, UnicodeError, json.JSONDecodeError, TypeError) as exc:
            fail(errors, f"{run.name}: unreadable RESULT: {exc}")

    result_checked, sidecar_checked = _check_result_audit_correction(errors, run, result_path)
    operational_name = re.compile(
        r"(PROMPT|CHECKPOINT|WAITING|RESOURCE_ASSIGNMENT|RUN_STATE|RESULT)",
        re.IGNORECASE,
    )
    for prompt in workspace.iterdir():
        if (
            not prompt.is_file()
            or not operational_name.search(prompt.name)
            or prompt.suffix.lower() in {".jsonl", ".log"}
        ):
            continue
        if prompt == result_path and result_checked:
            continue
        if prompt == workspace / "RESULT_AUDIT_CORRECTION.json" and sidecar_checked:
            continue
        text = read_text(prompt)
        _scan_operational_text(errors, f"{run.name}/{prompt.name}", text)

    print(f"RUN_OK {run.name} state={status}")


def check_launchers(errors: list[str]) -> None:
    skill = " ".join(read_text(SKILL_ROOT / "SKILL.md").split())
    provider = " ".join(read_text(ROOT / "PROVIDER_ADAPTER.md").split())
    for required in (
        "target-harness/",
        "harness_watcher_implementation",
        "watch --until-actionable",
        "PROVIDER_ADAPTER.md",
        "current user instruction authorizing hardware testing",
        "Never substitute the stable development harness",
    ):
        if required not in skill:
            fail(errors, f"agent launch contract missing: {required}")
    if "The implemented Firmware-local route is Qwen Code 0.21.10" not in provider:
        fail(errors, "PROVIDER_ADAPTER.md: implemented local-route status is missing")


def check_no_duplicate_provider_launcher(errors: list[str]) -> None:
    """Keep legacy change-loop scripts from becoming a competing provider route."""

    scripts = (
        ROOT / ".codex" / "skills" / "change-loop" / "scripts" / "agent.sh",
        ROOT / ".codex" / "skills" / "change-loop" / "scripts" / "lib.sh",
    )
    prohibited = re.compile(
        r"\bcodex\s+exec\b|\bqwen\s+code\b|CL_CODEX_(?:BIN|FLAGS)",
        re.IGNORECASE,
    )
    for path in scripts:
        if not path.is_file():
            fail(errors, f"provider-boundary script is missing: {path.relative_to(ROOT)}")
            continue
        if prohibited.search(read_text(path)):
            fail(errors, f"{path.relative_to(ROOT)}: duplicate provider launcher is not allowed")


def check_active_controller_permissions(errors: list[str]) -> None:
    """Reject an active restricted role without rewriting historical evidence."""

    def alive(pid: object) -> bool:
        if not isinstance(pid, int) or pid <= 0:
            return False
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        return True

    for status_path in ROOT.glob("fresh-experiments/*/.agent-workspace/*_controller.status.json"):
        try:
            status = json.loads(read_text(status_path))
        except (OSError, UnicodeError, json.JSONDecodeError, TypeError) as exc:
            fail(errors, f"{status_path}: unreadable controller status: {exc}")
            continue
        # Old controller records are durable evidence and may truthfully retain "running" after a
        # terminated host process. Treat a role as active only while its controller and provider child
        # are both live; do not rewrite archival status just to satisfy a new launch policy.
        state = status.get("state")
        provider_pid = status.get("provider_pid", status.get("codex_pid"))
        if state not in {"running", "RUNNING_CODEX", "RUNNING_PROVIDER"}:
            continue
        if not alive(status.get("controller_pid")) or not alive(provider_pid):
            continue
        settings = status.get("launcher_settings", status)
        if (
            settings.get("sandbox") != "danger-full-access"
            or settings.get("approval_policy") != "never"
            or (state in {"running", "RUNNING_CODEX"} and settings.get("approvals_reviewer") != "user")
        ):
            fail(
                errors,
                f"{status_path}: active role lacks mandatory unrestricted execution",
            )


def check_generator(errors: list[str]) -> None:
    generator = read_text(SKILL_ROOT / "scripts" / "fresh_test.py")
    terminal_match = re.search(r"^TERMINAL_STATUSES\s*=\s*(.+)$", generator, re.MULTILINE)
    if not terminal_match or "NEEDS_USER" in terminal_match.group(1) or "INFRA_BLOCKED" in terminal_match.group(1):
        fail(errors, "fresh_test.py: blocker status remains terminal")
    if "- NEEDS_USER" in generator or "- INFRA_BLOCKED" in generator:
        fail(errors, "fresh_test.py: generated prompt advertises blocker status")
    if 'NON_EXECUTABLE_CATALOG_TESTS = {"Q40"}' not in generator:
        fail(errors, "fresh_test.py: manager-owned Q40 is not explicitly excluded")
    if "len(heading.group(1)) <= 4" not in generator:
        fail(
            errors,
            "fresh_test.py: catalog excerpts are not bounded by peer/parent headings",
        )


def main() -> int:
    arguments = sys.argv[1:]
    if arguments not in ([], ["--require-target"]):
        print("usage: audit_autonomy.py [--require-target]", file=sys.stderr)
        return 2
    errors: list[str] = []
    check_package_boundary(errors)
    check_documentation_navigation(errors)
    check_target_harness(errors, required=bool(arguments))
    check_policy(errors)
    check_imported_progress(errors)
    check_catalog_skill_and_matrix(errors)
    check_parallel_contract(errors)
    check_cross_document_contract(errors)
    check_launchers(errors)
    check_no_duplicate_provider_launcher(errors)
    check_active_controller_permissions(errors)
    check_generator(errors)
    runs = unfinished_main_runs(errors)
    for run, test_id, status in runs:
        check_run(errors, run, test_id, status)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        print(f"AUTONOMY_AUDIT_FAIL errors={len(errors)}", file=sys.stderr)
        return 1
    print(f"AUTONOMY_AUDIT_PASS runs={len(runs)} policy_sha256={POLICY_SHA256}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
