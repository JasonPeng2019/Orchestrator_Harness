from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
POLICY_SHA256 = "fcb25396d58af7ee6e7ffc931142b830e8a1b28ea3e5c197a1ca1e3d6248aa68"
APPENDIX_IDS = {"D35", "R37", "R38"}
ALLOWED_RESULT_STATUSES = {"PASS", "SERVER_FAILURE"}
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


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="strict")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def unfinished_main_runs(errors: list[str]) -> list[tuple[Path, str, str]]:
    runs: list[tuple[Path, str, str]] = []
    for run in sorted((ROOT / "fresh-experiments").iterdir()):
        if not run.is_dir():
            continue
        test_id = run.name.split("_", 1)[0]
        if test_id in APPENDIX_IDS or test_id == "Q40":
            continue
        status_path = run / "STATUS.md"
        if not status_path.exists():
            fail(errors, f"{run.name}: missing current STATUS.md")
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
            "autonomy policy hash mismatch: "
            f"expected={POLICY_SHA256} actual={actual} sidecar={recorded}",
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

    skill = read_text(
        ROOT / ".codex" / "skills" / "run-firmware-test-suite" / "SKILL.md"
    )
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
            "the validated `orchestrator_harness` is required",
            "the same watcher reconciles and self-arms after exact acknowledgement",
            "this table is the authoritative catalog-level cross-test dependency graph",
            "an unlisted edge does not exist",
        ),
        ".codex/skills/run-firmware-test-suite/SKILL.md": (
            "launch or resume **all** eligible named doer lanes concurrently",
            "same scheduling batch",
            "continue unrelated lanes while another waits",
            "the validated `orchestrator_harness` is required",
            "the same watcher self-arms after exact acknowledgement",
            "use catalog section 11.1 as the authoritative cross-test edge list",
        ),
        ".codex/skills/run-firmware-test-suite/references/execution-contract.md": (
            "launch or resume every eligible non-conflicting lane in the same batch",
            "never wait for a blocked lane",
            "catalog section 11.1 is the authoritative cross-test edge list",
            "start exactly one `orchestrator_harness` managed watcher",
        ),
        ".codex/skills/run-firmware-test-suite/references/doer-roster.md": (
            "every dependency-ready, resource-compatible doer lane concurrently",
            "a blocked lane never holds an unrelated lane",
        ),
        "PLAN.md": (
            "every dependency-ready, resource-compatible lane concurrently",
            "prepare later board-free work early",
        ),
        ".agent-workspace/SUITE_COORDINATION.md": (
            "every dependency-ready, resource-compatible lane in parallel",
            "a waiting lane never stops unrelated work",
        ),
        "HANDOFF.md": (
            "every dependency-ready, resource-compatible named doer lane in the same batch",
            "never serializes unrelated work",
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

    roster_path = (
        ROOT
        / ".codex"
        / "skills"
        / "run-firmware-test-suite"
        / "references"
        / "doer-roster.md"
    )
    assigned: dict[str, str] = {}
    for line in read_text(roster_path).splitlines():
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) < 5 or cells[1] not in {
            "Atlas",
            "Boreal",
            "Cygnus",
            "Delta",
            "Nova",
        }:
            continue
        # The roster is a five-column contract (model/reasoning/tier/tasks).
        # Use the final non-empty cell so older three-column evidence remains
        # readable without confusing the reasoning column for assignments.
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
    skill_path = (
        ROOT / ".codex" / "skills" / "run-firmware-test-suite" / "SKILL.md"
    )
    execution_path = (
        ROOT
        / ".codex"
        / "skills"
        / "run-firmware-test-suite"
        / "references"
        / "execution-contract.md"
    )
    roster_path = (
        ROOT
        / ".codex"
        / "skills"
        / "run-firmware-test-suite"
        / "references"
        / "doer-roster.md"
    )
    catalog = read_text(catalog_path)
    main_catalog = catalog.split("## Appendix A", 1)[0]
    skill = read_text(skill_path)
    execution = read_text(execution_path)

    required_by_file = {
        catalog_path.name: (
            "`gpt-5.6-luna`",
            '`reasoning_effort="high"`',
            '`service_tier="default"`',
            "`gpt-5.6-terra`",
            '`service_tier="priority"`',
            "fresh-experiments/<test-id>_<timestamp>/",
            "Treat setup/APP-1 repetitions, returning-state repetitions",
            "60852689.DS_SX1261_2 V2-2.pdf",
            "nrf-sx-pin-mappings.md",
            "Every production-server repair uses `.codex/design_charter.md` as a live constraint",
        ),
        str(skill_path.relative_to(ROOT)): (
            '`model="gpt-5.6-luna"`',
            '`reasoning_effort="high"`',
            '`service_tier="default"`',
            "D35/R38 with",
            "R37 with Cygnus",
            "Treat `.codex/design_charter.md` as a live repair constraint",
        ),
        str(execution_path.relative_to(ROOT)): (
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

    for stale in (
        "I2C waveform",
        "measured SCL",
        "| DIO trace,",
        "runs/<experiment>/<agent>-<timestamp>/",
    ):
        if stale.lower() in main_catalog.lower():
            fail(errors, f"{catalog_path.name}: stale external/path contract: {stale}")
    if "the exact Codex settings above" in skill:
        fail(errors, f"{skill_path.relative_to(ROOT)}: ambiguous doer settings")
    if "S12 and S13 pass with all four boards" in catalog:
        fail(errors, f"{catalog_path.name}: S13 retains a blanket all-board barrier")
    if "independent passive logic/BLE/RF/serial oracle" in execution:
        fail(errors, f"{execution_path.relative_to(ROOT)}: stale external-oracle permission")
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

    def roster_assignments(text: str) -> dict[str, tuple[str, str, str]]:
        result: dict[str, tuple[str, str, str]] = {}
        for line in text.splitlines():
            cells = [cell.strip() for cell in line.split("|")]
            if len(cells) < 5 or cells[1] not in {
                "Atlas",
                "Boreal",
                "Cygnus",
                "Delta",
                "Nova",
            }:
                continue
            if len(cells) < 7:
                continue
            result[cells[1]] = (cells[2], cells[3], cells[4])
        return result

    catalog_roster = roster_assignments(catalog)
    skill_roster = roster_assignments(read_text(roster_path))
    if catalog_roster != skill_roster:
        fail(
            errors,
            "catalog/doer-roster mismatch: "
            f"catalog={catalog_roster} skill={skill_roster}",
        )


def check_run(
    errors: list[str],
    run: Path,
    test_id: str,
    status: str,
) -> None:
    workspace = run / ".agent-workspace"
    amendments = workspace / "SPEC_AMENDMENTS.md"
    if not amendments.exists():
        fail(errors, f"{run.name}: missing SPEC_AMENDMENTS.md")
    else:
        text = read_text(amendments)
        notice_index = text.find("**Effective interpretation notice**")
        first_amendment_index = text.find("## Amendment ")
        if notice_index < 0 or (
            first_amendment_index >= 0 and notice_index > first_amendment_index
        ):
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
    except Exception as exc:
        fail(errors, f"{run.name}: invalid RESULT schema: {exc}")

    result_path = workspace / "RESULT.json"
    if result_path.exists():
        try:
            result_status = json.loads(read_text(result_path)).get("status")
            if result_status in {"NEEDS_USER", "INFRA_BLOCKED"}:
                fail(errors, f"{run.name}: stale blocker RESULT={result_status}")
        except Exception as exc:
            fail(errors, f"{run.name}: unreadable RESULT: {exc}")

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
        text = read_text(prompt)
        for number, line in enumerate(text.splitlines(), 1):
            if re.search(
                r"\b(return|report|write|set)\b.*\b(NEEDS_USER|INFRA_BLOCKED)\b",
                line,
                re.IGNORECASE,
            ) and not re.search(
                r"\b(never|do not|invalid|prohibit)\b",
                line,
                re.IGNORECASE,
            ):
                fail(errors, f"{run.name}/{prompt.name}:{number}: blocker status")
            if re.search(
                r"\b(operator|user)\s+(must|should|needs? to)\b",
                line,
                re.IGNORECASE,
            ):
                fail(errors, f"{run.name}/{prompt.name}:{number}: operator action")

    print(f"RUN_OK {run.name} state={status}")


def check_launchers(errors: list[str]) -> None:
    # Legacy direct Python/PowerShell launcher wrappers were removed during the
    # clean-restart refactor. Validate the current subagent-exec contract instead.
    skill = read_text(ROOT / ".codex" / "skills" / "run-firmware-test-suite" / "SKILL.md")
    for required in (
        "subagent exec",
        'model="gpt-5.6-luna"',
        'reasoning_effort="high"',
        'service_tier="default"',
        "--dangerously-bypass-approvals-and-sandbox",
        'approval_policy="never"',
        'approvals_reviewer="user"',
        'model="gpt-5.6-terra"',
        'service_tier="priority"',
    ):
        if required not in skill:
            fail(errors, f"subagent launch contract missing: {required}")
    binder = read_text(ROOT / "scripts" / "orchestration" / "prompt_policy.py")
    for required in (
        "load_verified_policy",
        "last signed specification amendment",
        "FINAL PRECEDENCE REMINDER",
    ):
        if required not in binder:
            fail(errors, f"prompt_policy.py: missing enforcement: {required}")


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
        except Exception as exc:
            fail(errors, f"{status_path}: unreadable controller status: {exc}")
            continue
        # Old controller records are durable evidence and may truthfully retain "running" after a
        # terminated host process. Treat a role as active only while its controller and Codex child
        # are both live; do not rewrite archival status just to satisfy a new launch policy.
        if (
            status.get("state") != "running"
            or not alive(status.get("controller_pid"))
            or not alive(status.get("codex_pid"))
        ):
            continue
        if (
            status.get("sandbox") != "danger-full-access"
            or status.get("approval_policy") != "never"
            or status.get("approvals_reviewer") != "disabled"
        ):
            fail(errors, f"{status_path}: active role lacks mandatory unrestricted execution")


def check_generator(errors: list[str]) -> None:
    generator = read_text(
        ROOT
        / ".codex"
        / "skills"
        / "run-firmware-test-suite"
        / "scripts"
        / "fresh_test.py"
    )
    terminal_match = re.search(r"^TERMINAL_STATUSES\s*=\s*(.+)$", generator, re.MULTILINE)
    if not terminal_match or "NEEDS_USER" in terminal_match.group(1) or "INFRA_BLOCKED" in terminal_match.group(1):
        fail(errors, "fresh_test.py: blocker status remains terminal")
    if '- NEEDS_USER' in generator or '- INFRA_BLOCKED' in generator:
        fail(errors, "fresh_test.py: generated prompt advertises blocker status")
    if 'NON_EXECUTABLE_CATALOG_TESTS = {"Q40"}' not in generator:
        fail(errors, "fresh_test.py: manager-owned Q40 is not explicitly excluded")
    if "len(heading.group(1)) <= 4" not in generator:
        fail(errors, "fresh_test.py: catalog excerpts are not bounded by peer/parent headings")


def main() -> int:
    errors: list[str] = []
    check_policy(errors)
    check_catalog_skill_and_matrix(errors)
    check_parallel_contract(errors)
    check_cross_document_contract(errors)
    check_launchers(errors)
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
    print(
        f"AUTONOMY_AUDIT_PASS runs={len(runs)} "
        f"policy_sha256={POLICY_SHA256}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
