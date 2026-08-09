#!/usr/bin/env python3
"""Scaffold and validate isolated fresh-firmware experiment runs.

This utility never invokes a model, accesses hardware, flashes, or edits the server.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT = Path(__file__).resolve()
ROOT = SCRIPT.parents[4]
CATALOG = ROOT / "BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md"
FRESH_ROOT = ROOT / "fresh-experiments"
WORKSPACE_NAME = ".agent-workspace"
DEFAULT_TEST_MODEL = "gpt-5.6-luna"
DEFAULT_REVIEWER_MODEL = "gpt-5.6-terra"
DESIGNATED_TEST_MODELS = {"A23": "claude-sonnet-5"}
BOOTSTRAP_TESTS = {"H00", "H01", "H02", "H03", "H04", "H05"}
TASK_DOERS = {
    "S10": "Atlas",
    "S11": "Boreal",
    "S12": "Cygnus",
    "S13": "Atlas",
    "A20": "Atlas",
    "A21": "Boreal",
    "A22": "Atlas",
    "A23": "Nova",
    "A24": "Cygnus",
    "A25": "Delta",
    "A26": "Delta",
    "D30": "Atlas",
    "D31": "Boreal",
    "D32": "Atlas",
    "D33": "Cygnus",
    "D34": "Cygnus",
    "D36": "Boreal",
    "Q41": "Atlas",
}
DATASHEETS = {
    "stm32L476rgt.pdf": ROOT / "reference" / "datasheets" / "stm32l476rgt.pdf",
    "Nano_BLE_MCU-nRF52840_PS_v1.1.pdf": (
        ROOT / "reference" / "datasheets" / "nrf52840-product-spec-v1.1.pdf"
    ),
}
TEST_HEADING = re.compile(r"^####\s+([A-Z]\d{2})\s+[—-]\s+(.+?)\s*$")
MARKDOWN_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
NON_EXECUTABLE_CATALOG_TESTS = {"Q40"}
REQUIRED_RESULT_FIELDS = {
    "schema_version",
    "test_id",
    "status",
    "summary",
    "run_directory",
    "server_commit",
    "firmware_commit",
    "hardware",
    "requirements",
    "commands",
    "mcp_evidence",
    "oracle_evidence",
    "final_board_state",
    "server_failure",
    "blocking_request",
    "remaining_work",
}
TERMINAL_STATUSES = {"PASS", "SERVER_FAILURE"}
INITIAL_WORKSPACE_FILES = {
    "SPEC.md",
    "RUN_STATE.json",
    "INITIAL_MANIFEST.json",
    "RESULT.schema.json",
    "TEST_AGENT_PROMPT.md",
    "REVIEWER_PROMPT.md",
}


class FreshTestError(RuntimeError):
    """A deterministic scaffold or validation error."""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def designated_test_model(test_id: str) -> str:
    return DESIGNATED_TEST_MODELS.get(test_id, DEFAULT_TEST_MODEL)


def designated_doer_name(test_id: str) -> str | None:
    if test_id in BOOTSTRAP_TESTS:
        return None
    try:
        return TASK_DOERS[test_id]
    except KeyError as exc:
        raise FreshTestError(
            f"remaining catalog test has no lane doer: {test_id}"
        ) from exc


def doer_label(test_id: str) -> str:
    return designated_doer_name(test_id) or "none (bootstrap task)"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def load_json(path: Path) -> dict[str, Any]:
    try:
        # Accept a UTF-8 BOM because Windows PowerShell commonly adds one when
        # test agents create JSON with Set-Content.
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise FreshTestError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise FreshTestError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise FreshTestError(f"expected JSON object in {path}")
    return value


def catalog_sections() -> dict[str, tuple[str, str]]:
    if not CATALOG.is_file():
        raise FreshTestError(f"catalog is missing: {CATALOG}")
    lines = CATALOG.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str, str]] = []
    for index, line in enumerate(lines):
        match = TEST_HEADING.match(line)
        if match:
            starts.append((index, match.group(1), match.group(2)))
    sections: dict[str, tuple[str, str]] = {}
    seen_test_ids: set[str] = set()
    for start, test_id, title in starts:
        if test_id in seen_test_ids:
            raise FreshTestError(f"duplicate catalog test ID: {test_id}")
        seen_test_ids.add(test_id)
        if test_id in NON_EXECUTABLE_CATALOG_TESTS:
            continue
        end = len(lines)
        for index in range(start + 1, len(lines)):
            heading = MARKDOWN_HEADING.match(lines[index])
            if heading and len(heading.group(1)) <= 4:
                end = index
                break
        excerpt = "\n".join(lines[start:end]).rstrip() + "\n"
        sections[test_id] = (title, excerpt)
    if not sections:
        raise FreshTestError(f"no test headings found in {CATALOG}")
    expected_named = set(sections) - BOOTSTRAP_TESTS
    missing_doers = sorted(expected_named - set(TASK_DOERS))
    stale_doers = sorted(set(TASK_DOERS) - expected_named)
    if missing_doers or stale_doers:
        raise FreshTestError(
            "named-doer roster does not match executable catalog: "
            f"missing={missing_doers}, stale={stale_doers}"
        )
    return sections


def resolve_run(value: str) -> Path:
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = (ROOT / candidate).resolve()
    else:
        candidate = candidate.resolve()
    fresh = FRESH_ROOT.resolve()
    if candidate == fresh or fresh not in candidate.parents:
        raise FreshTestError(f"run directory must be a child of {fresh}: {candidate}")
    return candidate


def state_path(run: Path) -> Path:
    return run / WORKSPACE_NAME / "RUN_STATE.json"


def append_history(state: dict[str, Any], status: str, note: str) -> None:
    history = state.setdefault("history", [])
    if not isinstance(history, list):
        raise FreshTestError("RUN_STATE history must be an array")
    history.append({"at": utc_now(), "status": status, "note": note})
    state["status"] = status


def spec_text(test_id: str, title: str, excerpt: str) -> str:
    return f"""# Test Specification — {test_id}: {title}

## Immutable identity

- Test ID: `{test_id}`
- Catalog title: {title}
- Assigned lane doer: `{doer_label(test_id)}`
- Server repository: `BYO-Firmware-MCP`
- Server commit under test: [REQUIRED]
- Spec author/time: [REQUIRED]

## Objective

[REQUIRED: one concrete end-to-end objective]

## Exclusions

[REQUIRED: behavior this test must not change or claim]

## Hardware and roles

- Required physical boards and friendly names: [REQUIRED; may be `none` for board-free cases]
- MCU/package identifiers:
  - NUCLEO-L476RG: `STM32L476RGT6`
  - nRF52840 DK: `nRF52840-QIAA`
- Physical identity and MCU/package evidence material to this case: [REQUIRED or `not applicable`;
  stable electronic identity or a manager-supplied correlated official/fixture record is
  sufficient; no PCA, PCB revision, photo, visual-inspection, or new-operator gate]
- Wiring, power, antenna, and independent oracle material to this case: [REQUIRED or `not
  applicable`; external lab instruments are outside the main-suite contract]
- Firmware execution model and queue/thread requirements: [REQUIRED or `not applicable`]

## Initial-information boundary

The test agent receives only the manager-sealed root inputs declared in
`.agent-workspace/INITIAL_MANIFEST.json`, this `.agent-workspace`, official internet sources it
locates, ordinary SDK/toolchain acquisition, the live MCP surface, and the physical fixture. It
must not inspect the master catalog, another run, or BYO-Firmware-MCP source.

## Risk and permission

- Risk class (non-destructive / flash / destructive / RF): [REQUIRED]
- Applicable recorded delegated authorization: [REQUIRED; may be `none`; never request a new user
  response for a main-suite phase]
- Safe abort/final state: [REQUIRED]

## Parallel execution

- Catalog ID and assigned lane doer: `{test_id}` / `{doer_label(test_id)}`
- Internal shard map owned by this same doer: [REQUIRED; may be `none`]
- Build prerequisites that must already be GREEN: [REQUIRED; only dependencies actually consumed,
  may be `none`]
- HIL prerequisites that must already be GREEN: [REQUIRED; only dependencies actually consumed,
  may be `none`]
- Planned phases (SPEC_READY / BUILDING / BUILT_WAITING_FOR_LEASE / HIL_RUNNING): [REQUIRED]
- Phase-specific exclusive/shared resource requests (STM-A, STM-B, NRF-A, NRF-B, probes, serial,
  peer/radio, autonomous electronic controls actually used, USB/power scope actually affected,
  server lifecycle, mutable cache/artifact/state roots):
  [REQUIRED; may be `none`]
- Immutable build-to-HIL artifact/configuration handoff: [REQUIRED or `not applicable`]
- Disruptive or host-global scope: [REQUIRED or `none`]
- Safe checkpoint boundaries: [REQUIRED]
- Maximum pause latency and bounded soak/repetition epoch: [REQUIRED]

## Numbered requirements

### REQ-001

- Action: [REQUIRED]
- Observable pass condition: [REQUIRED]
- Observable failure condition: [REQUIRED]
- Required raw evidence/oracle: [REQUIRED; any adequate catalog-permitted modality]

### REQ-002

- Action: [REQUIRED]
- Observable pass condition: [REQUIRED]
- Observable failure condition: [REQUIRED]
- Required raw evidence/oracle: [REQUIRED; any adequate catalog-permitted modality]

## Seeded-fault boundary

- Symptom visible to test agent: [REQUIRED or `none`]
- Hidden answer-key location outside this run: [REQUIRED or `none`]
- Disclosure rule: Do not reveal the seeded root cause before the agent's evidence-based diagnosis.

## Retry, timing, and cleanup

- Protocol/hardware-derived bounds: [REQUIRED]
- Required regression path: [REQUIRED]
- Required final board state and cleanup: [REQUIRED]

## Terminal evidence

Require `.agent-workspace/RESULT.json`, `.agent-workspace/TEST_REPORT.md`, and the evidence types
applicable to the selected requirements: exact commands, artifact hashes, raw MCP outputs,
UART/peer counters, independent oracle where specified, firmware diff/commit, and final observed
target state. Irrelevant evidence arrays may be empty and do not block the result.

## Catalog source excerpt

The excerpt is context, not permission to weaken the numbered requirements above.

{excerpt}
"""


def result_schema(test_id: str) -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": f"Fresh firmware result for {test_id}",
        "type": "object",
        "required": sorted(REQUIRED_RESULT_FIELDS),
        "properties": {
            "schema_version": {"const": 1},
            "test_id": {"const": test_id},
            "status": {"enum": sorted(TERMINAL_STATUSES)},
            "summary": {"type": "string", "minLength": 1},
            "run_directory": {"type": "string", "minLength": 1},
            "server_commit": {"type": "string", "minLength": 1},
            "firmware_commit": {"type": ["string", "null"]},
            "hardware": {"type": "array"},
            "requirements": {"type": "array"},
            "commands": {"type": "array"},
            "mcp_evidence": {"type": "array"},
            "oracle_evidence": {"type": "array"},
            "final_board_state": {"type": "string"},
            "server_failure": {"type": ["object", "null"]},
            "blocking_request": {"type": ["string", "null"]},
            "remaining_work": {"type": "array"},
        },
        "additionalProperties": False,
    }


def agent_prompt(test_id: str, title: str, run: Path) -> str:
    model = designated_test_model(test_id)
    doer_name = designated_doer_name(test_id)
    doer_assignment = (
        f"Your stable suite lane-doer name is `{doer_name}`."
        if doer_name
        else "This is a bootstrap task and has no retroactive lane-doer name."
    )
    return f"""# Persistent test-agent assignment

{doer_assignment} You alone own fresh test `{test_id}` ({title}) in:

`{run}`

The catalog-designated doer model for this test is `{model}`. Preserve this provider/model and
session across ordinary continuation, checkpoint/resume, and server-repair retest.
You own every internal board/family shard of this task. You may orchestrate concurrent processes
under disjoint manager-assigned leases, but must not delegate a shard to another doing subagent.
After this task is terminal or manager-checkpointed, the manager may resume this same named doer
for its next roster task in a different isolated run. Do not carry firmware files, hidden context,
leases, permission, or unevidenced conclusions from one task into another.

First, print and verify the current working directory. Scope every filesystem/command tool call to
that exact directory. Read `.agent-workspace/SPEC.md` and
`.agent-workspace/RESULT.schema.json`.
    Read `.agent-workspace/SPEC_AMENDMENTS.md` too when it exists; its last signed amendment has
    precedence over older clauses. Read and hash-check the suite-root
    `.agent-workspace/AUTONOMOUS_EXECUTION_POLICY.md`.

    This main-suite run is zero-operator after launch. Never request another user response or a
    physical inspection, label/marking, cable move, button press, repositioning, rewiring,
    jumper/solder change, external instrument, or operator-timed event. Use the fixed declared
    fixture, stable electronic identity, existing correlated evidence, and autonomous
    software/server controls. If older text conflicts, the autonomy policy and last signed amendment
    win.

Implement all firmware and test code yourself inside this fresh run. Use only the manager-sealed
root inputs declared in `.agent-workspace/INITIAL_MANIFEST.json`, official internet sources you
find, ordinary SDK/toolchain acquisition, the live BYO firmware MCP, and the specified physical
fixture. Do not read the parent experiment catalog,
another run, or any BYO-Firmware-MCP source/test/doc file. Do not edit the MCP server. Do not use a
direct hardware utility to bypass the MCP. Do not invoke, read, or use `$change-loop` or
`$plan-changes`; those workflows are unavailable to fresh-experiment test agents and reserved for
the main model's verified production-server repairs.

Iterate autonomously through implementation, build, live setup/plan/permission gates, flash,
observation, debugging, firmware repair, and regression testing. Routine firmware failures are
yours to fix; do not return merely to report progress. Preserve exact commands and raw evidence
under `.agent-workspace/evidence/`.

The main manager, not you, assigns phase and resources. Never self-acquire a board, probe, serial
    endpoint, peer/radio, autonomous electronic control, or server lifecycle scope. Before entering HIL, require a current
manager-written assignment in `.agent-workspace/RESOURCE_ASSIGNMENT.md` that names this
test/shard, `HIL_RUNNING`, every lease, and the server snapshot. If the build finishes before such
an assignment is valid, preserve an immutable artifact/configuration handoff, write
`.agent-workspace/BUILT_WAITING_FOR_LEASE.md`, and return without creating or changing
`RESULT.json`. On resume, verify the handoff before using it. Board-free build work must not invoke
the MCP server or touch hardware.

Between the safe boundaries declared in `SPEC.md`, check whether
`.agent-workspace/PAUSE_REQUESTED.md` exists. Never interrupt flash, erase, or another atomic
hardware mutation mid-operation. Let the current operation reach its declared finite completion
or timeout, flush evidence, record live board/session/serial state and cleanup, and write
`.agent-workspace/PARALLEL_CHECKPOINT.md` containing the wave/server snapshot, last completed
requirement, evidence paths, `in-flight operation: none`, remaining work, and exact first resume
action. Then return without creating or changing `RESULT.json`; this manager-requested pause is not
a terminal result. Long soaks/repetition loops must use the bounded epochs declared in the spec.
During a server repair, an explicitly assigned board-free build phase may continue only while it
does not invoke or depend on the live server and does not advance into HIL.

Otherwise, return only after writing `.agent-workspace/RESULT.json` and
`.agent-workspace/TEST_REPORT.md` with one terminal status:

- PASS
- SERVER_FAILURE
    There is no terminal blocker or firmware-failure status. For SERVER_FAILURE, first rule out firmware,
artifact, identity, wiring, SDK, and precondition mistakes and provide a minimal reproducer. For
hardware-changing or destructive actions, obey every live MCP plan and permission gate. Use only
a manager-recorded delegated authorization artifact/hash named by the current resource assignment;
never invent or broaden permission. When the exact populated plan is within that recorded scope,
    the manager may relay permission without another conversational pause. Never write
    `NEEDS_USER` or `INFRA_BLOCKED`. If a temporary resource/provider condition prevents this phase,
    write a safe nonterminal checkpoint without `RESULT.json`; the manager records the wait in the
    suite ledger and continues unrelated lanes. An intrinsically manual/special-equipment branch is
    Appendix A only and cannot remain a main-run gate.
"""


def reviewer_prompt(test_id: str, title: str, run: Path) -> str:
    return f"""# Persistent adversarial reviewer assignment

You are the read-only reviewer for fresh test `{test_id}` ({title}) in:

`{run}`

First, print and verify the current working directory. Scope every filesystem/command tool call to
that directory. You must never inspect `BYO-Firmware-MCP`, invoke `$change-loop` or
`$plan-changes`, operate hardware, invoke destructive tools, or edit firmware/server files.

## First turn: sealed-spec review

    Read `.agent-workspace/SPEC.md`, the supplied-input manifest, any existing
    `.agent-workspace/SPEC_AMENDMENTS.md`, and the hash-verified suite-root
    `.agent-workspace/AUTONOMOUS_EXECUTION_POLICY.md`. The policy and last signed amendment
    supersede older contrary clauses. Adversarially assess whether the test is executable and
falsifiable: numbered pass/fail oracles, hardware/fixture identity, destructive scope, evidence,
time/retry bounds, dependency correctness, complete/non-overlapping requested leases, safe
checkpoint boundaries, bounded pause latency, and ambiguities that would force the test agent to
    invent the contract. Reject every main-run requirement for another user response,
    physical/operator intervention, external lab equipment, or terminal
    `NEEDS_USER`/`INFRA_BLOCKED`. Require autonomous software/electronic substitutes and one
    truthful correlated oracle. Do not reveal a seeded-bug answer.

Write `.agent-workspace/SPEC_ADVERSARIAL_REVIEW.md` with either `SPEC_APPROVED` or numbered
criticisms labeled `ACTIONABLE` or `ADVISORY`. Actionable means an evidenced requirement
violation, credible safety/data-loss/identity risk, reproducible failure, or likely
hang/orchestration collapse. Style, speculative hardening, vanishingly unlikely cases without
evidence, unrelated features, and disproportionate complexity are advisory. You may write only
this review file. The main model decides whether a narrow signed spec amendment is needed; do not
request a review loop or make advisory perfection work a release gate.

## Later turn: PASS-evidence review

When resumed after a PASS claim, independently reassess the sealed spec and any amendment against
`RESULT.json`, `TEST_REPORT.md`, and raw evidence. Do not defer to your earlier spec approval.
Write `.agent-workspace/ADVERSARIAL_REVIEW.md` with either `NO_ACTIONABLE_SERVER_ISSUES` or
numbered evidence-backed criticisms labeled `ACTIONABLE` or `ADVISORY` under the same standard.
Assess only evidence invalidated by the current failure/change plus any explicitly missing proof;
do not reopen already accepted requirements whose inputs are unchanged. One targeted follow-up is
the review budget after rejected evidence. When actionable findings are resolved and objective
gates pass, stop; do not pursue a perfect product. You may write only that review file.
"""


def command_list(args: argparse.Namespace) -> int:
    sections = catalog_sections()
    if args.json:
        print(
            json.dumps(
                [
                    {
                        "test_id": key,
                        "title": value[0],
                        "doer_name": designated_doer_name(key),
                    }
                    for key, value in sections.items()
                ],
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        for test_id, (title, _) in sections.items():
            print(f"{test_id}\t{doer_label(test_id)}\t{title}")
    return 0


def command_create(args: argparse.Namespace) -> int:
    sections = catalog_sections()
    test_id = args.test_id.upper()
    try:
        title, excerpt = sections[test_id]
    except KeyError as exc:
        raise FreshTestError(f"unknown catalog test ID: {test_id}") from exc
    stamp = args.label or datetime.now().strftime("%Y%m%d-%H%M%S")
    if not re.fullmatch(r"[A-Za-z0-9._-]+", stamp):
        raise FreshTestError(
            "label may contain only letters, digits, dot, underscore, and hyphen"
        )
    FRESH_ROOT.mkdir(parents=True, exist_ok=True)
    run = (FRESH_ROOT / f"{test_id}_{stamp}").resolve()
    if run.exists():
        raise FreshTestError(f"run directory already exists: {run}")
    sources = list(DATASHEETS.values())
    missing = [str(path) for path in sources if not path.is_file()]
    if missing:
        raise FreshTestError(
            "missing required supplied datasheet(s): " + ", ".join(missing)
        )

    run.mkdir()
    workspace = run / WORKSPACE_NAME
    evidence = workspace / "evidence"
    evidence.mkdir(parents=True)
    for source in sources:
        copied_name = next(name for name, path in DATASHEETS.items() if path == source)
        shutil.copy2(source, run / copied_name)
    (workspace / "SPEC.md").write_text(
        spec_text(test_id, title, excerpt), encoding="utf-8"
    )
    atomic_json(workspace / "RESULT.schema.json", result_schema(test_id))
    (workspace / "TEST_AGENT_PROMPT.md").write_text(
        agent_prompt(test_id, title, run), encoding="utf-8"
    )
    (workspace / "REVIEWER_PROMPT.md").write_text(
        reviewer_prompt(test_id, title, run), encoding="utf-8"
    )
    state = {
        "schema_version": 1,
        "test_id": test_id,
        "title": title,
        "doer_name": designated_doer_name(test_id),
        "run_directory": str(run),
        "status": "CREATED",
        "created_at": utc_now(),
        "sealed_at": None,
        "spec_sha256": None,
        "reviewer_id": None,
        "reviewer_task_name": None,
        "reviewer_model": None,
        "spec_review": None,
        "agent_id": None,
        "agent_task_name": None,
        "agent_model": None,
        "agent_assignments": [],
        "main_review": None,
        "history": [],
    }
    append_history(state, "CREATED", "Fresh run scaffolded; spec requires completion.")
    atomic_json(state_path(run), state)
    manifest = {
        "schema_version": 1,
        "created_at": utc_now(),
        "sealed_at": None,
        "test_id": test_id,
        "doer_name": designated_doer_name(test_id),
        "allowed_initial_root_entries": sorted((*DATASHEETS, WORKSPACE_NAME)),
        "datasheets": {
            next(name for name, path in DATASHEETS.items() if path == source): {
                "source": str(source),
                "copied_sha256": sha256_file(
                    run / next(name for name, path in DATASHEETS.items() if path == source)
                ),
            }
            for source in sources
        },
        "spec_sha256": None,
    }
    atomic_json(workspace / "INITIAL_MANIFEST.json", manifest)
    print(run)
    return 0


def validate_initial_layout(run: Path) -> None:
    if not run.is_dir():
        raise FreshTestError(f"run directory is missing: {run}")
    workspace = run / WORKSPACE_NAME
    manifest = load_json(workspace / "INITIAL_MANIFEST.json")
    declared_root = manifest.get("allowed_initial_root_entries")
    if (
        not isinstance(declared_root, list)
        or not declared_root
        or any(not isinstance(name, str) or not name for name in declared_root)
        or len(set(declared_root)) != len(declared_root)
        or WORKSPACE_NAME not in declared_root
    ):
        raise FreshTestError(
            "INITIAL_MANIFEST allowed_initial_root_entries must be a unique nonempty "
            f"string list containing {WORKSPACE_NAME}"
        )
    actual_root = {item.name for item in run.iterdir()}
    expected_root = set(declared_root)
    if actual_root != expected_root:
        raise FreshTestError(
            "unsealed run root is contaminated; "
            f"expected {sorted(expected_root)}, found {sorted(actual_root)}"
        )
    actual_workspace_files = {
        item.name for item in workspace.iterdir() if item.is_file()
    }
    unexpected = actual_workspace_files - INITIAL_WORKSPACE_FILES
    missing = INITIAL_WORKSPACE_FILES - actual_workspace_files
    subdirs = {item.name for item in workspace.iterdir() if item.is_dir()}
    if unexpected or missing or subdirs != {"evidence"}:
        raise FreshTestError(
            "unexpected initial agent workspace layout: "
            f"missing={sorted(missing)}, unexpected={sorted(unexpected)}, "
            f"subdirs={sorted(subdirs)}"
        )
    if any((workspace / "evidence").iterdir()):
        raise FreshTestError("initial evidence directory must be empty")
    declared_inputs = manifest.get("datasheets")
    if not isinstance(declared_inputs, dict) or not declared_inputs:
        raise FreshTestError("INITIAL_MANIFEST datasheets/input mapping must be a nonempty object")
    for name in declared_inputs:
        if not (run / name).is_file():
            raise FreshTestError(f"missing copied initial input: {name}")


def command_seal(args: argparse.Namespace) -> int:
    run = resolve_run(args.run_dir)
    validate_initial_layout(run)
    workspace = run / WORKSPACE_NAME
    spec = workspace / "SPEC.md"
    text = spec.read_text(encoding="utf-8")
    if "[REQUIRED" in text:
        raise FreshTestError(f"spec still contains [REQUIRED] placeholders: {spec}")
    state = load_json(state_path(run))
    if state.get("status") != "CREATED":
        raise FreshTestError(
            f"only CREATED runs can be sealed; status={state.get('status')}"
        )
    manifest = load_json(workspace / "INITIAL_MANIFEST.json")
    declared_inputs = manifest.get("datasheets")
    if not isinstance(declared_inputs, dict) or not declared_inputs:
        raise FreshTestError("INITIAL_MANIFEST datasheets/input mapping must be a nonempty object")
    for name, input_record in declared_inputs.items():
        if not isinstance(input_record, dict) or not isinstance(
            input_record.get("copied_sha256"), str
        ):
            raise FreshTestError(f"invalid initial-input hash record: {name}")
        expected = input_record["copied_sha256"]
        actual = sha256_file(run / name)
        if actual != expected:
            raise FreshTestError(f"initial input changed before seal: {name}")
    digest = sha256_file(spec)
    sealed = utc_now()
    manifest["sealed_at"] = sealed
    manifest["spec_sha256"] = digest
    atomic_json(workspace / "INITIAL_MANIFEST.json", manifest)
    state["sealed_at"] = sealed
    state["spec_sha256"] = digest
    append_history(state, "SPEC_READY", "Spec and initial inputs sealed.")
    atomic_json(state_path(run), state)
    print(f"SEALED {run}")
    return 0


def command_bind_reviewer(args: argparse.Namespace) -> int:
    run = resolve_run(args.run_dir)
    state = load_json(state_path(run))
    if state.get("status") != "SPEC_READY":
        raise FreshTestError(
            f"reviewer can be initially bound only from SPEC_READY; status={state.get('status')}"
        )
    if state.get("agent_id") is not None:
        raise FreshTestError("reviewer must be bound before the test agent")
    if any(
        state.get(field) is not None
        for field in ("reviewer_id", "reviewer_task_name", "reviewer_model")
    ):
        raise FreshTestError("persistent reviewer is already bound")
    for field, value in (
        ("reviewer ID", args.reviewer_id),
        ("reviewer task name", args.task_name),
        ("reviewer model", args.model),
    ):
        if not value.strip():
            raise FreshTestError(f"{field} must be non-empty")
    if not re.fullmatch(r"[A-Za-z0-9._-]+", args.model):
        raise FreshTestError(
            "reviewer model may contain only letters, digits, dot, underscore, and hyphen"
        )

    state["reviewer_id"] = args.reviewer_id
    state["reviewer_task_name"] = args.task_name
    state["reviewer_model"] = args.model
    append_history(
        state,
        "SPEC_READY",
        "Persistent adversarial reviewer bound for spec and evidence review.",
    )
    atomic_json(state_path(run), state)
    print(f"REVIEWER_BOUND {args.reviewer_id} {args.task_name} {args.model}")
    return 0


def command_approve_spec(args: argparse.Namespace) -> int:
    run = resolve_run(args.run_dir)
    state = load_json(state_path(run))
    if state.get("status") != "SPEC_READY":
        raise FreshTestError(
            f"spec approval requires SPEC_READY; status={state.get('status')}"
        )
    if not all(
        state.get(field)
        for field in ("reviewer_id", "reviewer_task_name", "reviewer_model")
    ):
        raise FreshTestError("spec approval requires a bound persistent reviewer")
    review_path = run / WORKSPACE_NAME / "SPEC_ADVERSARIAL_REVIEW.md"
    if not review_path.is_file() or not review_path.read_text(encoding="utf-8").strip():
        raise FreshTestError(f"missing or empty sealed-spec review: {review_path}")
    state["spec_review"] = {
        "reviewer_id": state["reviewer_id"],
        "reviewer_task_name": state["reviewer_task_name"],
        "reviewer_model": state["reviewer_model"],
        "at": utc_now(),
        "note": args.note,
    }
    append_history(
        state, "SPEC_REVIEWED", f"Main accepted sealed-spec review: {args.note}"
    )
    atomic_json(state_path(run), state)
    print(f"SPEC_APPROVED {run}")
    return 0


def command_bind_agent(args: argparse.Namespace) -> int:
    run = resolve_run(args.run_dir)
    state = load_json(state_path(run))
    if state.get("status") not in {
        "SPEC_REVIEWED",
        "AGENT_RUNNING",
        "SERVER_FIXED",
    }:
        raise FreshTestError(
            "agent can be bound or resumed only from a resumable run state; "
            f"status={state.get('status')}"
        )
    for field, value in (
        ("agent ID", args.agent_id),
        ("task name", args.task_name),
        ("model", args.model),
    ):
        if not value.strip():
            raise FreshTestError(f"{field} must be non-empty")
    if not re.fullmatch(r"[A-Za-z0-9._-]+", args.model):
        raise FreshTestError(
            "model may contain only letters, digits, dot, underscore, and hyphen"
        )
    if args.previous_model and not re.fullmatch(
        r"[A-Za-z0-9._-]+", args.previous_model
    ):
        raise FreshTestError(
            "previous model may contain only letters, digits, dot, underscore, and hyphen"
        )

    existing_id = state.get("agent_id")
    existing_task = state.get("agent_task_name")
    existing_model = state.get("agent_model")
    if (existing_id is None) != (existing_task is None):
        raise FreshTestError("RUN_STATE has an incomplete persistent agent identity")
    if existing_model is not None and not isinstance(existing_model, str):
        raise FreshTestError("RUN_STATE agent_model must be a string or null")

    assignments = state.setdefault("agent_assignments", [])
    if not isinstance(assignments, list):
        raise FreshTestError("RUN_STATE agent_assignments must be an array")

    initial_binding = existing_id is None
    identity_changed = not initial_binding and (
        existing_id != args.agent_id or existing_task != args.task_name
    )

    # Runs created before model tracking may safely record the model of their
    # already-bound agent without restarting it or invalidating verified work.
    legacy_model_record = (
        not initial_binding and existing_model is None and not identity_changed
    )
    if legacy_model_record:
        existing_model = args.model

    if not initial_binding and existing_model is None:
        if not args.previous_model:
            raise FreshTestError(
                "legacy run is changing agent identity; first provide --previous-model "
                "so the handoff records the old model"
            )
        existing_model = args.previous_model
    elif (
        args.previous_model
        and existing_model is not None
        and args.previous_model != existing_model
    ):
        raise FreshTestError(
            "--previous-model does not match the model already recorded in RUN_STATE"
        )

    model_changed = not initial_binding and existing_model != args.model
    replacement = identity_changed or model_changed
    expected_model = designated_test_model(state["test_id"])
    initial_model_exception = initial_binding and args.model != expected_model
    if initial_model_exception:
        if args.previous_model:
            raise FreshTestError(
                "--previous-model is not valid for an initial assignment"
            )
        if not args.necessary_model_change:
            raise FreshTestError(
                f"new {state['test_id']} tests must start on {expected_model}; a necessary exception "
                "requires --necessary-model-change"
            )
        if not args.replacement_reason or not args.replacement_reason.strip():
            raise FreshTestError(
                "a necessary non-default initial model requires --replacement-reason"
            )
        if args.session_unrecoverable:
            raise FreshTestError(
                "--session-unrecoverable is not valid for an initial assignment"
            )
        if args.continuity_note:
            raise FreshTestError(
                "--continuity-note is not valid before a test has prior evidence"
            )
    elif replacement:
        if not args.replacement_reason or not args.replacement_reason.strip():
            raise FreshTestError(
                "agent/model replacement requires --replacement-reason"
            )
        if not args.continuity_note or not args.continuity_note.strip():
            raise FreshTestError(
                "agent/model replacement requires --continuity-note with the "
                "last verified state, durable evidence, and remaining-work boundary"
            )
        if model_changed and not args.necessary_model_change:
            raise FreshTestError("changing models requires --necessary-model-change")
        if model_changed and args.session_unrecoverable:
            raise FreshTestError(
                "do not combine --session-unrecoverable with a model change; "
                "record the necessary model change as the handoff cause"
            )
        if identity_changed and not model_changed and not args.session_unrecoverable:
            raise FreshTestError(
                "a same-model agent replacement requires --session-unrecoverable; "
                "resume the recorded persistent session otherwise"
            )
        if not model_changed and args.necessary_model_change:
            raise FreshTestError(
                "--necessary-model-change requires the new model to differ"
            )
    else:
        if args.necessary_model_change or args.session_unrecoverable:
            raise FreshTestError(
                "replacement acknowledgement supplied, but agent and model did not change"
            )
        if args.replacement_reason or args.continuity_note:
            raise FreshTestError(
                "replacement handoff fields are allowed only when agent or model changes"
            )
        if args.previous_model and initial_binding:
            raise FreshTestError(
                "--previous-model is not valid for an initial assignment"
            )

    previous = (
        None
        if initial_binding
        else {
            "agent_id": existing_id,
            "task_name": existing_task,
            "model": existing_model,
        }
    )
    state["agent_id"] = args.agent_id
    state["agent_task_name"] = args.task_name
    state["agent_model"] = args.model
    current = {
        "agent_id": args.agent_id,
        "task_name": args.task_name,
        "model": args.model,
    }
    if initial_binding or legacy_model_record or replacement:
        assignments.append(
            {
                "at": utc_now(),
                "kind": (
                    "initial_model_exception"
                    if initial_model_exception
                    else "initial"
                    if initial_binding
                    else "legacy_model_record"
                    if legacy_model_record
                    else "replacement"
                ),
                "previous": previous,
                "current": current,
                "necessity": (
                    args.replacement_reason.strip()
                    if replacement or initial_model_exception
                    else "initial assignment"
                    if initial_binding
                    else "recorded model for pre-contract assignment"
                ),
                "continuity_note": (
                    args.continuity_note.strip() if replacement else None
                ),
            }
        )
    note = (
        "Necessary non-default initial model recorded."
        if initial_model_exception
        else "Persistent test agent bound."
        if initial_binding
        else "Legacy test-agent model recorded; existing session and evidence preserved."
        if legacy_model_record
        else "Necessary agent/model replacement recorded with continuity handoff."
        if replacement
        else "Persistent test agent resumed."
    )
    append_history(state, "AGENT_RUNNING", note)
    atomic_json(state_path(run), state)
    print(f"BOUND {args.agent_id} {args.task_name} {args.model}")
    return 0


def safe_evidence_path(run: Path, value: object, field: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise FreshTestError(f"{field} evidence path must be a non-empty string")
    candidate = Path(value)
    if candidate.is_absolute():
        path = candidate.resolve()
    else:
        path = (run / candidate).resolve()
    if run != path and run not in path.parents:
        raise FreshTestError(f"{field} evidence escapes the run directory: {value}")
    if not path.is_file():
        raise FreshTestError(f"{field} evidence file is missing: {value}")
    return path


def validate_result(run: Path, result: dict[str, Any]) -> None:
    missing = REQUIRED_RESULT_FIELDS - set(result)
    extra = set(result) - REQUIRED_RESULT_FIELDS
    if missing or extra:
        raise FreshTestError(
            f"RESULT fields mismatch: missing={sorted(missing)}, extra={sorted(extra)}"
        )
    if result["schema_version"] != 1:
        raise FreshTestError("RESULT schema_version must be 1")
    state = load_json(state_path(run))
    if result["test_id"] != state.get("test_id"):
        raise FreshTestError("RESULT test_id does not match RUN_STATE")
    status = result["status"]
    if status not in TERMINAL_STATUSES:
        raise FreshTestError(f"invalid terminal status: {status}")
    for field in ("summary", "server_commit", "final_board_state"):
        if not isinstance(result[field], str) or not result[field].strip():
            raise FreshTestError(f"RESULT {field} must be non-empty")
    if Path(result["run_directory"]).resolve() != run:
        raise FreshTestError(
            "RESULT run_directory does not match the run being verified"
        )
    for field in (
        "hardware",
        "requirements",
        "commands",
        "mcp_evidence",
        "oracle_evidence",
        "remaining_work",
    ):
        if not isinstance(result[field], list):
            raise FreshTestError(f"RESULT {field} must be an array")
    if not result["requirements"]:
        raise FreshTestError("RESULT requirements must not be empty")

    for index, requirement in enumerate(result["requirements"]):
        if not isinstance(requirement, dict):
            raise FreshTestError(f"requirements[{index}] must be an object")
        if not isinstance(requirement.get("id"), str):
            raise FreshTestError(f"requirements[{index}].id is required")
        evidence = requirement.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            raise FreshTestError(f"requirements[{index}].evidence must be non-empty")
        for item in evidence:
            safe_evidence_path(run, item, f"requirements[{index}]")

    for index, command in enumerate(result["commands"]):
        if not isinstance(command, dict):
            raise FreshTestError(f"commands[{index}] must be an object")
        for key in ("command", "cwd", "exit_code", "evidence"):
            if key not in command:
                raise FreshTestError(f"commands[{index}].{key} is required")
        if not isinstance(command["exit_code"], int):
            raise FreshTestError(f"commands[{index}].exit_code must be an integer")
        safe_evidence_path(run, command["evidence"], f"commands[{index}]")

    for field in ("mcp_evidence", "oracle_evidence"):
        for index, item in enumerate(result[field]):
            safe_evidence_path(run, item, f"{field}[{index}]")

    if status == "PASS":
        failed = [
            req.get("id")
            for req in result["requirements"]
            if req.get("status") != "PASS"
        ]
        if failed:
            raise FreshTestError(f"PASS contains non-passing requirements: {failed}")
        if result["server_failure"] is not None:
            raise FreshTestError("PASS must have server_failure=null")
        if result["blocking_request"] is not None:
            raise FreshTestError("PASS must have blocking_request=null")
        if result["remaining_work"]:
            raise FreshTestError("PASS must have no remaining_work")
    elif status == "SERVER_FAILURE":
        if result["blocking_request"] is not None:
            raise FreshTestError("SERVER_FAILURE must have blocking_request=null")
        failure = result["server_failure"]
        if not isinstance(failure, dict):
            raise FreshTestError("SERVER_FAILURE requires server_failure object")
        needed = {
            "observed",
            "expected",
            "minimal_reproducer",
            "reproduced_count",
            "evidence",
            "ruled_out",
            "suspected_server_scope",
        }
        if needed - set(failure):
            raise FreshTestError(
                "server_failure missing fields: "
                + ", ".join(sorted(needed - set(failure)))
            )
        if (
            not isinstance(failure["reproduced_count"], int)
            or failure["reproduced_count"] < 2
        ):
            raise FreshTestError("server_failure.reproduced_count must be >=2")
        if not isinstance(failure["evidence"], list) or not failure["evidence"]:
            raise FreshTestError("server_failure.evidence must be non-empty")
        for index, item in enumerate(failure["evidence"]):
            safe_evidence_path(run, item, f"server_failure.evidence[{index}]")
    else:
        raise FreshTestError(f"invalid terminal status: {status}")


def command_verify(args: argparse.Namespace) -> int:
    run = resolve_run(args.run_dir)
    workspace = run / WORKSPACE_NAME
    state = load_json(state_path(run))
    manifest = load_json(workspace / "INITIAL_MANIFEST.json")
    spec = workspace / "SPEC.md"
    if not state.get("sealed_at") or not manifest.get("sealed_at"):
        raise FreshTestError("run was not sealed before execution")
    digest = sha256_file(spec)
    if digest != state.get("spec_sha256") or digest != manifest.get("spec_sha256"):
        raise FreshTestError(
            "sealed SPEC.md changed; record a separate SPEC_AMENDMENTS.md instead"
        )
    declared_inputs = manifest.get("datasheets")
    if not isinstance(declared_inputs, dict) or not declared_inputs:
        raise FreshTestError("INITIAL_MANIFEST datasheets/input mapping must be a nonempty object")
    for name, input_record in declared_inputs.items():
        if not isinstance(input_record, dict) or not isinstance(
            input_record.get("copied_sha256"), str
        ):
            raise FreshTestError(f"invalid initial-input hash record: {name}")
        expected = input_record["copied_sha256"]
        if sha256_file(run / name) != expected:
            raise FreshTestError(f"supplied initial input changed after seal: {name}")
    result_path = workspace / "RESULT.json"
    report_path = workspace / "TEST_REPORT.md"
    if not report_path.is_file() or not report_path.read_text(encoding="utf-8").strip():
        raise FreshTestError(f"missing or empty test report: {report_path}")
    result = load_json(result_path)
    validate_result(run, result)
    status = result["status"]
    append_history(
        state,
        "PASS_CLAIMED" if status == "PASS" else status,
        "Agent result validated structurally.",
    )
    atomic_json(state_path(run), state)
    print(f"VALID {status} {run}")
    return 0


def command_review(args: argparse.Namespace) -> int:
    run = resolve_run(args.run_dir)
    state = load_json(state_path(run))
    if args.verdict == "GREEN" and state.get("status") != "PASS_CLAIMED":
        raise FreshTestError(
            f"GREEN requires PASS_CLAIMED after verify; status={state.get('status')}"
        )
    if args.verdict == "GREEN":
        if not state.get("reviewer_id"):
            raise FreshTestError(
                "GREEN requires the persistent reviewer recorded before test execution"
            )
        evidence_review = run / WORKSPACE_NAME / "ADVERSARIAL_REVIEW.md"
        if (
            not evidence_review.is_file()
            or not evidence_review.read_text(encoding="utf-8").strip()
        ):
            raise FreshTestError(
                f"GREEN requires a non-empty adversarial evidence review: {evidence_review}"
            )
    state["main_review"] = {
        "verdict": args.verdict,
        "at": utc_now(),
        "note": args.note,
    }
    status = "GREEN" if args.verdict == "GREEN" else "AGENT_RUNNING"
    append_history(state, status, f"Main review: {args.note}")
    atomic_json(state_path(run), state)
    print(f"REVIEW {args.verdict} {run}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scaffold and validate isolated fresh firmware MCP tests."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser(
        "list", help="List test IDs parsed from the catalog."
    )
    list_parser.add_argument("--json", action="store_true")
    list_parser.set_defaults(handler=command_list)

    create_parser = subparsers.add_parser("create", help="Create a fresh run scaffold.")
    create_parser.add_argument("test_id")
    create_parser.add_argument(
        "--label", help="Unique safe suffix; defaults to local timestamp."
    )
    create_parser.set_defaults(handler=command_create)

    seal_parser = subparsers.add_parser(
        "seal", help="Seal a completed fresh test spec."
    )
    seal_parser.add_argument("run_dir")
    seal_parser.set_defaults(handler=command_seal)

    reviewer_parser = subparsers.add_parser(
        "bind-reviewer",
        help="Persist the one read-only reviewer reused for sealed-spec and PASS-evidence review.",
    )
    reviewer_parser.add_argument("run_dir")
    reviewer_parser.add_argument("--reviewer-id", required=True)
    reviewer_parser.add_argument("--task-name", required=True)
    reviewer_parser.add_argument("--model", default=DEFAULT_REVIEWER_MODEL)
    reviewer_parser.set_defaults(handler=command_bind_reviewer)

    approve_spec_parser = subparsers.add_parser(
        "approve-spec",
        help="Record main-model acceptance of the one sealed-spec adversarial review.",
    )
    approve_spec_parser.add_argument("run_dir")
    approve_spec_parser.add_argument("--note", required=True)
    approve_spec_parser.set_defaults(handler=command_approve_spec)

    bind_parser = subparsers.add_parser(
        "bind-agent",
        help=(
            "Persist the test-agent identity/model; replacement requires a "
            "recorded necessity and continuity handoff."
        ),
    )
    bind_parser.add_argument("run_dir")
    bind_parser.add_argument("--agent-id", required=True)
    bind_parser.add_argument("--task-name", required=True)
    bind_parser.add_argument("--model", required=True)
    bind_parser.add_argument(
        "--previous-model",
        help="Old model for a pre-contract run whose RUN_STATE does not record one.",
    )
    bind_parser.add_argument(
        "--replacement-reason",
        help="Concrete necessity for changing agent or model.",
    )
    bind_parser.add_argument(
        "--continuity-note",
        help=(
            "Last verified state, durable evidence, and exact remaining-work "
            "boundary handed to the replacement."
        ),
    )
    bind_parser.add_argument(
        "--necessary-model-change",
        action="store_true",
        help=(
            "Acknowledge that a model change, or a non-default model for a new test, "
            "is necessary under the continuity contract."
        ),
    )
    bind_parser.add_argument(
        "--session-unrecoverable",
        action="store_true",
        help="Acknowledge that a same-model replacement is necessary because the old session cannot resume.",
    )
    bind_parser.set_defaults(handler=command_bind_agent)

    verify_parser = subparsers.add_parser(
        "verify", help="Validate a terminal result and all named evidence."
    )
    verify_parser.add_argument("run_dir")
    verify_parser.set_defaults(handler=command_verify)

    review_parser = subparsers.add_parser(
        "review", help="Persist main-model evidence review."
    )
    review_parser.add_argument("run_dir")
    review_parser.add_argument(
        "--verdict", choices=("GREEN", "REJECTED"), required=True
    )
    review_parser.add_argument("--note", required=True)
    review_parser.set_defaults(handler=command_review)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.handler(args))
    except FreshTestError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
