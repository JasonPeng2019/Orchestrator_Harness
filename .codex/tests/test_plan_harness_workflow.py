from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / ".codex" / "skills" / "plan-harness-workflow" / "scripts" / "validate_execution_plan.py"
SPEC = importlib.util.spec_from_file_location("validate_execution_plan", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def valid_plan() -> str:
    return """# Execution Plan

## 0. Metadata
- Plan title: Example
- Product spec: spec.md
- Reference plan: plan.md

## 1. Agent-per-role mapping
| Role | Agent chosen | Pool size | Authority |
|---|---|---:|---|
| orchestrator / planner-executor | agent-o | 1 | fixed |
| coder-main | agent-c | 1 | fixed |
| reviewer-main | agent-r | 1 | skill |
| doer-main | agent-d | 1 | skill |
| final-reviewer | agent-f | 1 | skill |

## 2. Coverage checklist
| ID | Required outcome | Source |
|---|---|---|
| C1 | Deliver behavior | Plan section 1 |
| C2 | Persist behavior | Plan section 2 |

## 3. Decomposition and disposition
Atomic changes and individual modules are not execution steps.
Preflight gates (no full cycle): record baseline evidence.
| Module | Included atomic changes | Functional area | Assigned large step |
|---|---|---|---|
| parser | C1 | behavior | S1 |
| storage | C2 | behavior | S1 |
| Large step | Disposition | Included modules | Coherent feature or deliverable | Why one full QA cycle | Covers |
|---|---|---|---|---|---|
| S1 | reused as-is | parser, storage | complete behavior | one integrated deliverable | C1, C2 |

## 4. Coverage map
| Checklist ID | Built in module | Containing large step | Tested by |
|---|---|---|---|
| C1 | parser | S1 | unit and practical tests |
| C2 | storage | S1 | unit and practical tests |

Gaps / surfaced issues (must be empty to finalize): none

## 5. Serial step flow
Large steps only appear here. Modules and small changes do not receive their own cycle.
Step 1 completes before any later step.
Run the shortest affected smoke before complete review and remaining focused execution.

### Global lane topology
S1.P -> S1.R1 -> S1.JR -> S1.CA -> S1.A1 -> S1.JA -> S1.D1 -> S1.JT -> S1.DONE

| Large step | Included modules and serial tasks | Product lane and bundled modules | Review lane(s) -> triage | Author lane(s) -> integration | Test lane(s) -> triage | Failure route | Unlocks |
|---|---|---|---|---|---|---|---|
| S1 | parser and storage | S1.P: build parser and storage | S1.R1 -> S1.JR | S1.A1 -> S1.JA | S1.D1 -> S1.JT | S1.JT -> S1.P | final phase |

## 6. Per-step execution spec
### Step S1: Build
The skill-defined fixed conceptual slices cannot be changed by the runtime.
- Step class: large step
- Coherent feature or deliverable: deliver the complete example behavior
- Included modules: parser, storage
- Included serial tasks: implement parser, storage, and ordinary tests
- Why grouped by coherence: parsing and persistence form one usable behavior
- Why full QA is justified: their integration is the independently testable delivery boundary
- Granularity boundary: modules and small changes remain here; an unrelated feature becomes another large step
- Smallest useful pool: one reviewer, one author, and one doer cover the only independent slice

| Function | Pool size | Why this exact size | Topology |
|---|---:|---|---|
| Review | 1 | one coherent review | direct R1 |
| Test/document authoring | 1 | one coherent test file | direct A1 |
| Test execution | 1 | one isolated test run | direct D1 |

**Explicit lane topology**

S1.P -> S1.R1 -> S1.JR -> S1.CA -> S1.A1 -> S1.JA -> S1.D1 -> S1.JT

| Lane ID | Agent role / wave | Concrete task | Starts after / base | Branch / worktree or run root | Ownership | Output / handoff | Join / merge target and order | Failure route |
|---|---|---|---|---|---|---|---|---|
| S1.P | coder-main | build product | baseline | branch/worktree | production | commit | S1.R1 | fix and repeat S1.R1 |
| S1.R1 | reviewer-main | review behavior | product tip | read-only tip | no writes | review | S1.JR | finding to S1.P |
| S1.A1 | reviewer-main | write tests | Checkpoint A | author branch/worktree | tests | commit | S1.JA, only merge | conflict to S1.A1 |
| S1.D1 | doer-main | run tests | integrated tip | validation worktree/run root | test IDs | evidence | S1.JT | failures to S1.P |

Loop 1 performs static review and merge-then-triage until permanent Checkpoint A.
Test authoring follows Checkpoint A.
Loop 2 runs tests with no ordinary static review and updates the passed registry.

Current Portable Harness binding:
- Run through stable-general-harness-runner and keep pre-conversion-rollback available.
- Run `scan --no-write` before launch.
- Wait with `watch --until-actionable`.
- Acknowledge with `ack --event-id` after handling.
- Use a fresh `.agent-workspace` with `PARALLEL_CHECKPOINT.md`, `RESULT.json`, and manager-signals.
- Keep `evaluator_enabled: false`.

## 7. Final phase
### Final and acceptance lane topology
F.C0.FR1 -> F.C0.JR -> F.C1.A1 -> F.C1.JA -> F.C2.D1 -> F.C2.JT -> F.C3.O -> F.C3.P1 -> F.C3.M

| Lane ID | Agent | Concrete task | Starts after / base | Branch / worktree or run root | Output | Join / merge target | Failure route |
|---|---|---|---|---|---|---|---|
| F.C3.O | candidate orchestrator | run predefined acceptance | final gate | candidate root | evidence | shutdown | repair |
| F.C3.W | watcher | observe only | process manifest | outside root | report | outside supervisor | abort |
| F.C3.P1 | target worker | target production | target base | target branch/worktree | result | F.C3.M | retry |
| F.C3.M | merge worker | merge target | F.C3.P1 | merge branch/worktree | commit | shutdown | merge repair |

- C0: spawn a fresh final-reviewer invocation.
- C1: use the final/acceptance spec for complete unit and smoke tests.
- C2 - final test loop: run gap-only tests with no static review.
- Executor self-check decision: recordability preflight uses a disposable local fake, verifies the complete process record, and performs no real product or external action.
- Pooled process-environment decision: fixture, mock, runner, and executor-environment-only defects are batched before one selection rerun; candidate, contract, oracle, expected-behavior, and coverage defects use the material route.
- C3 - practical test: run the real end-to-end scenario.
- External-operation readiness decision: a disposable local rehearsal verifies control-plane admission before external allocation; green unlocks the attempt but is not external-pass evidence.
- C4 - nested static-audit loop: repair repeated practical failure.
  This is the only post-Checkpoint-A static-review revival.

## 8. Safeguard
Run the complete accumulated suite exactly once after practical success.
Write a completion summary with the out-of-scope ledger.

## 9. Rules the runner applies
- Goal: ship a working product efficiently.
- Triage: realistic functional defect is valid; roughly 99.9% adequate edge behavior is extraneous.
- Reviewer recommends; orchestrator decides.
- Each fix records targeted stable test IDs in the passed registry.
- Termination has no iteration cap and stops on stall_threshold: 2, same-signature failure,
  oscillation, only-extraneous scope churn, or unrecoverable error.
- The runtime never re-partitions conceptual slices.
- Every pool follows merge-then-triage.
- A singleton direct handoff has no split or fake merge.
- production/material changes use the bounded batch route after the shortest affected smoke.
- strict test-only fast lane: a deterministic diff/eligibility checklist proves fixture-only scope; rerun exactly those failed IDs, with no fresh C0 and no unrelated smoke.
- administrative corrections stay in the same lane and do not reopen product review.
- executor self-check: recordability preflight uses local fakes and no real product, MCP, hardware, or external side effect; correct procedure defects in the same lane.
- pooled process-environment correction: batch classified fixture/mock/runner/executor-environment defects and rerun the selection once.
- external-operation readiness: a proportionate local rehearsal is required before scarce external allocation and does not substitute for external-pass evidence.
- scoped lock-input domains: candidate behavior and test procedure are independently tracked.
- gate dependency matrix: each gate lists the domains it consumes.
- governing-change classification: record changed domains and invalidated gates.
- conservative fallback: use the broad route when classification is uncertain.
- scope_policy: ship-realistic
- gap_scope: change
- final_full_verification: true
- Executor self-check decision: required recordability preflight
- Pooled process-environment correction policy: one batch then one selection rerun
- External-operation readiness decision: required local rehearsal
- Scoped lock-input domains: candidate behavior, test procedure
- Gate dependency matrix: C0 -> candidate behavior
- Governing-change classification: runtime/change-classification.json
- Conservative fallback: broad revalidation
- Test-ID scheme: path::class::test
- Pass criteria: all admitted behavior passes

## 10. File handoffs
- Out-of-scope ledger: runtime/out-of-scope.jsonl
- Passed registry: runtime/passed.json

## 11. Config block
- stall_threshold: 2
- scope_policy: ship-realistic
- gap_scope: change
- final_full_verification: true
- Executor self-check decision: required recordability preflight
- Pooled process-environment correction policy: one batch then one selection rerun
- External-operation readiness decision: required local rehearsal
- Scoped lock-input domains: candidate behavior, test procedure
- Gate dependency matrix: C0 -> candidate behavior
- Governing-change classification: runtime/change-classification.json
- Conservative fallback: broad revalidation
- Test-ID scheme: path::class::test
- Pass criteria: all admitted behavior passes
"""


def plan_with_review_pool(size: int) -> str:
    if size == 1:
        return valid_plan()
    if size not in {2, 3}:
        raise ValueError("review pool fixture supports sizes 1-3")

    plan = valid_plan()
    lane_ids = [f"S1.R{index}" for index in range(1, size + 1)]
    lane_set = ", ".join(lane_ids)
    plan = plan.replace("| reviewer-main | agent-r | 1 |", f"| reviewer-main | agent-r | {size} |")
    plan = plan.replace("| Review | 1 |", f"| Review | {size} |", 1)
    plan = plan.replace(
        "S1.P -> S1.R1 -> S1.JR -> S1.CA",
        f"S1.P -> S1.SR -> {{{lane_set}}} -> S1.JR -> S1.CA",
    )
    plan = plan.replace(
        "S1.R1 -> S1.JR | S1.A1",
        f"S1.SR -> {{{lane_set}}} -> S1.JR | S1.A1",
    )
    anchor = "| S1.R1 | reviewer-main | review behavior | product tip | read-only tip | no writes | review | S1.JR | finding to S1.P |"
    extra_rows = "\n".join(
        f"| {lane_id} | reviewer-main | review slice {index} | S1.SR | read-only tip | no writes | review | S1.JR | finding to S1.P |"
        for index, lane_id in enumerate(lane_ids[1:], start=2)
    )
    return plan.replace(anchor, f"{anchor}\n{extra_rows}")


def test_complete_prompt_contract_passes() -> None:
    assert VALIDATOR.validate(valid_plan(), require_scoped_locks=True) == []


@pytest.mark.parametrize("size", [2, 3])
def test_real_review_fanout_sizes_pass(size: int) -> None:
    assert VALIDATOR.validate(plan_with_review_pool(size), require_scoped_locks=True) == []


@pytest.mark.parametrize(
    ("required_text", "expected_error"),
    [
        ("fresh final-reviewer", "fresh final-reviewer"),
        ("c3 - practical test", "c3 - practical test"),
        ("c4 - nested static-audit loop", "c4 - nested static-audit loop"),
        (
            "complete accumulated suite exactly once",
            "complete accumulated suite exactly once",
        ),
        ("targeted stable test IDs", "targeted stable test ids"),
        ("runtime never re-partitions", "runtime never re-partitions"),
        ("explicit lane topology", "explicit lane topology"),
        ("final and acceptance lane topology", "final and acceptance lane topology"),
        (
            "atomic changes and individual modules are not execution steps",
            "atomic changes and individual modules are not execution steps",
        ),
        ("preflight gates (no full cycle)", "preflight gates (no full cycle)"),
        ("large steps only", "large steps only"),
        (
            "modules and small changes do not receive their own cycle",
            "modules and small changes do not receive their own cycle",
        ),
        ("singleton direct handoff", "singleton direct handoff"),
        ("strict test-only fast lane", "strict test-only fast lane"),
        ("executor self-check", "executor self-check"),
        ("recordability preflight", "recordability preflight"),
        (
            "pooled process-environment correction",
            "pooled process-environment correction",
        ),
        ("external-operation readiness", "external-operation readiness"),
        ("executor self-check decision", "executor self-check decision"),
        (
            "deterministic diff/eligibility checklist",
            "deterministic diff/eligibility checklist",
        ),
    ],
)
def test_missing_prompt_decision_is_rejected(required_text: str, expected_error: str) -> None:
    plan = re.sub(
        re.escape(required_text),
        "removed decision",
        valid_plan(),
        count=0,
        flags=re.IGNORECASE,
    )

    errors = VALIDATOR.validate(plan, require_scoped_locks=True)

    assert any(expected_error in error.lower() for error in errors)


def test_duplicate_coverage_id_is_rejected() -> None:
    plan = valid_plan().replace(
        "| C1 | Deliver behavior | Plan section 1 |",
        "| C1 | Deliver behavior | Plan section 1 |\n| C1 | Duplicate | Plan section 2 |",
    )

    assert any("duplicate ids: c1" in error.lower() for error in VALIDATOR.validate(plan))


def test_coder_pool_must_be_singular() -> None:
    plan = valid_plan().replace("| coder-main | agent-c | 1 |", "| coder-main | agent-c | 2 |")

    assert any("coder-main must have pool size 1" in error for error in VALIDATOR.validate(plan))


def test_missing_required_lane_row_is_rejected() -> None:
    plan = valid_plan().replace("| S1.A1 | reviewer-main", "| S1.AX | reviewer-main")

    assert any("no row for S1.A1" in error for error in VALIDATOR.validate(plan))


@pytest.mark.parametrize(
    "field",
    [
        "coherent feature or deliverable",
        "included modules",
        "included serial tasks",
        "why grouped by coherence",
        "why full qa is justified",
        "granularity boundary",
        "smallest useful pool",
    ],
)
def test_missing_large_step_definition_is_rejected(field: str) -> None:
    plan = re.sub(
        rf"(?mi)^- {re.escape(field)}:.*$",
        f"- removed {field}: value",
        valid_plan(),
        count=1,
    )

    assert any(f"large-step definition is missing: {field}" in error for error in VALIDATOR.validate(plan))


def test_non_large_step_class_is_rejected() -> None:
    plan = valid_plan().replace("- Step class: large step", "- Step class: module")

    assert any("step class must be large step" in error for error in VALIDATOR.validate(plan))


def test_large_step_must_bundle_multiple_modules() -> None:
    plan = valid_plan().replace("- Included modules: parser, storage", "- Included modules: parser")

    assert any("must bundle multiple modules" in error for error in VALIDATOR.validate(plan))


def test_singleton_pool_rejects_fake_split_gate() -> None:
    plan = valid_plan().replace(
        "S1.P -> S1.R1 -> S1.JR -> S1.CA",
        "S1.P -> S1.SR -> S1.R1 -> S1.JR -> S1.CA",
    )

    assert any("singleton Review pool must not use split gate S1.SR" in error for error in VALIDATOR.validate(plan))


def test_multi_lane_pool_requires_real_split_gate() -> None:
    plan = plan_with_review_pool(2).replace(
        "S1.SR -> {S1.R1, S1.R2} -> S1.JR",
        "S1.R1 -> S1.R2 -> S1.JR",
    )

    assert any("multi-lane Review pool requires split gate S1.SR" in error for error in VALIDATOR.validate(plan))


def test_step_pool_cannot_exceed_configured_role_pool() -> None:
    plan = plan_with_review_pool(2).replace("| reviewer-main | agent-r | 2 |", "| reviewer-main | agent-r | 1 |")

    assert any("exceeds its configured role pool 1" in error for error in VALIDATOR.validate(plan))


def test_missing_required_join_gate_is_rejected() -> None:
    plan = valid_plan().replace("S1.JA", "S1.JX")

    assert any("missing lane/gate S1.JA" in error for error in VALIDATOR.validate(plan))


def test_missing_final_acceptance_lane_is_rejected() -> None:
    plan = valid_plan().replace("| F.C3.W | watcher", "| F.C3.WX | watcher")

    assert any("no row for F.C3.W" in error for error in VALIDATOR.validate(plan))


@pytest.mark.parametrize(
    "config_line",
    [
        "- stall_threshold: 0",
        "- gap_scope: everything",
        "- final_full_verification: sometimes",
    ],
)
def test_invalid_config_value_is_rejected(config_line: str) -> None:
    plan = valid_plan()
    key = config_line.split(":", 1)[0]
    plan = "\n".join(config_line if line.startswith(key) else line for line in plan.splitlines())

    assert VALIDATOR.validate(plan)
