from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

HEADINGS = [
    "## 0. Metadata",
    "## 1. Agent-per-role mapping",
    "## 2. Coverage checklist",
    "## 3. Decomposition and disposition",
    "## 4. Coverage map",
    "## 5. Serial step flow",
    "## 6. Per-step execution spec",
    "## 7. Final phase",
    "## 8. Safeguard",
    "## 9. Rules the runner applies",
    "## 10. File handoffs",
    "## 11. Config block",
]

HARNESS_MARKERS = [
    "scan --no-write",
    "watch --until-actionable",
    "ack --event-id",
    ".agent-workspace",
    "PARALLEL_CHECKPOINT.md",
    "RESULT.json",
    "manager-signals",
    "evaluator_enabled",
    "stable-general-harness-runner",
    "pre-conversion-rollback",
]

SECTION_MARKERS = {
    "## 3. Decomposition and disposition": [
        "atomic changes and individual modules are not execution steps",
        "preflight gates (no full cycle)",
        "assigned large step",
        "included modules",
        "coherent feature or deliverable",
        "why one full qa cycle",
    ],
    "## 5. Serial step flow": [
        "large steps only",
        "modules and small changes do not receive their own cycle",
        "included modules and serial tasks",
        "global lane topology",
        "product lane and bundled modules",
        "review lane(s) -> triage",
        "author lane(s) -> integration",
        "test lane(s) -> triage",
        "failure route",
        "unlocks",
        "shortest affected smoke",
        "remaining focused",
    ],
    "## 6. Per-step execution spec": [
        "loop 1",
        "checkpoint a",
        "fixed conceptual",
        "explicit lane topology",
        "starts after / base",
        "join / merge target and order",
        "failure route",
        "loop 2",
        "no ordinary static review",
        "passed registry",
        "current portable harness binding",
        "smallest useful pool",
    ],
    "## 7. Final phase": [
        "final and acceptance lane topology",
        "f.c3.o",
        "f.c3.w",
        "f.c3.p1",
        "f.c3.m",
        "fresh final-reviewer",
        "final/acceptance spec",
        "c2 - final test loop",
        "recordability preflight",
        "fixture",
        "c3 - practical test",
        "c4 - nested static-audit loop",
        "only post-checkpoint-a static-review revival",
    ],
    "## 8. Safeguard": [
        "complete accumulated suite exactly once",
        "completion summary",
        "out-of-scope ledger",
    ],
    "## 9. Rules the runner applies": [
        "working product efficiently",
        "roughly 99.9%",
        "reviewer recommends; orchestrator decides",
        "targeted stable test ids",
        "no iteration cap",
        "same-signature failure",
        "oscillation",
        "only-extraneous scope churn",
        "unrecoverable error",
        "runtime never re-partitions",
        "merge-then-triage",
        "singleton direct handoff",
        "production/material",
        "strict test-only fast lane",
        "deterministic diff/eligibility checklist",
        "exactly those failed ids",
        "no fresh c0",
        "no unrelated smoke",
        "administrative",
        "recordability preflight",
        "fixture",
    ],
}


def section(text: str, heading: str, next_heading: str | None) -> str:
    start = text.index(heading) + len(heading)
    end = text.index(next_heading, start) if next_heading else len(text)
    return text[start:end]


def table_id_list(value: str) -> list[str]:
    return re.findall(r"(?m)^\|\s*(C\d+)\s*\|", value)


def duplicate_ids(values: list[str]) -> list[str]:
    return sorted(value for value, count in Counter(values).items() if count > 1)


def role_pool_size(text: str, role_pattern: str) -> int | None:
    match = re.search(rf"(?mi)^\|\s*{role_pattern}\s*\|[^|]*\|\s*(\d+)\b", text)
    return int(match.group(1)) if match else None


def validate_step_lane_topologies(body: str, reviewer_pool_limit: int | None, doer_pool_limit: int | None) -> list[str]:
    errors: list[str] = []
    matches = list(re.finditer(r"(?mi)^### Step\s+(S\d+)\s*:", body))
    if not matches:
        return ["per-step execution spec contains no Step S<number> blocks"]

    for index, match in enumerate(matches):
        step_id = match.group(1).upper()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        step = body[match.end() : end]
        lowered = step.lower()
        required_text = [
            "explicit lane topology",
            "starts after / base",
            "branch / worktree or run root",
            "join / merge target and order",
            "failure route",
        ]
        for required in required_text:
            if required not in lowered:
                errors.append(f"{step_id} lane topology is missing: {required}")

        required_fields = (
            "step class",
            "coherent feature or deliverable",
            "included modules",
            "included serial tasks",
            "why grouped by coherence",
            "why full qa is justified",
            "granularity boundary",
            "smallest useful pool",
        )
        for field in required_fields:
            if not re.search(rf"(?mi)^\s*-\s*{field}\s*:\s*\S", step):
                errors.append(f"{step_id} large-step definition is missing: {field}")

        if not re.search(r"(?mi)^\s*-\s*step class\s*:\s*`?large step`?\s*$", step):
            errors.append(f"{step_id} step class must be large step")

        modules_match = re.search(r"(?mi)^\s*-\s*included modules\s*:\s*(\S.*)$", step)
        if modules_match and not re.search(r",|;|\band\b", modules_match.group(1), re.IGNORECASE):
            errors.append(f"{step_id} must bundle multiple modules")

        topology_match = re.search(
            r"(?ims)\*\*Explicit lane topology\*\*\s*(.*?)(?=^\|\s*Lane ID\s*\|)",
            step,
        )
        topology = topology_match.group(1) if topology_match else ""
        if not topology:
            errors.append(f"{step_id} has no parseable explicit lane topology graph")

        manifest_ids = {
            lane.upper()
            for lane in re.findall(
                rf"(?mi)^\|\s*`?({re.escape(step_id)}\.(?:P|R\d+|A\d+|D\d+))`?\s*\|",
                step,
            )
        }
        topology_ids = {
            lane.upper()
            for lane in re.findall(
                rf"(?i)\b({re.escape(step_id)}\.(?:P|R\d+|A\d+|D\d+))\b",
                topology,
            )
        }

        for suffix in ("P", "R1", "A1", "D1"):
            lane_or_gate = f"{step_id}.{suffix}"
            if lane_or_gate not in manifest_ids:
                errors.append(f"{step_id} lane manifest has no row for {lane_or_gate}")
            if lane_or_gate not in topology_ids:
                errors.append(f"{step_id} lane topology is missing lane/gate {lane_or_gate}")

        missing_manifest = sorted(topology_ids - manifest_ids)
        extra_manifest = sorted(manifest_ids - topology_ids)
        if missing_manifest:
            errors.append(f"{step_id} topology lanes missing from manifest: {', '.join(missing_manifest)}")
        if extra_manifest:
            errors.append(f"{step_id} manifest lanes missing from topology: {', '.join(extra_manifest)}")

        for gate in ("JR", "CA", "JA", "JT"):
            gate_id = f"{step_id}.{gate}"
            if gate_id.lower() not in topology.lower():
                errors.append(f"{step_id} lane topology is missing lane/gate {gate_id}")

        pools = (
            ("R", "SR", "Review", reviewer_pool_limit),
            ("A", "SA", "Test/document authoring", reviewer_pool_limit),
            ("D", "ST", "Test execution", doer_pool_limit),
        )
        for lane_prefix, split_suffix, label, role_limit in pools:
            pool_match = re.search(rf"(?mi)^\|\s*{re.escape(label)}\s*\|\s*(\d+)\s*\|", step)
            if not pool_match:
                errors.append(f"{step_id} cannot read {label} pool size")
                continue
            pool_size = int(pool_match.group(1))
            if not 1 <= pool_size <= 3:
                errors.append(f"{step_id} {label} pool size must be 1-3, found {pool_size}")
            if role_limit is not None and pool_size > role_limit:
                errors.append(f"{step_id} {label} pool size {pool_size} exceeds its configured role pool {role_limit}")

            lane_count = sum(lane.startswith(f"{step_id}.{lane_prefix}") for lane in manifest_ids)
            if lane_count != pool_size:
                errors.append(f"{step_id} {label} pool size {pool_size} does not match {lane_count} manifest lanes")

            split_id = f"{step_id}.{split_suffix}"
            has_split = split_id.lower() in topology.lower()
            if pool_size == 1 and has_split:
                errors.append(f"{step_id} singleton {label} pool must not use split gate {split_id}")
            if pool_size > 1 and not has_split:
                errors.append(f"{step_id} multi-lane {label} pool requires split gate {split_id}")

        if "->" not in topology:
            errors.append(f"{step_id} lane topology has no arrow graph")

    return errors


def validate_final_lane_topology(body: str) -> list[str]:
    errors: list[str] = []
    required_rows = ("F.C3.O", "F.C3.W", "F.C3.P1", "F.C3.M")
    for lane_id in required_rows:
        if not re.search(rf"(?mi)^\|\s*`?{re.escape(lane_id)}`?\s*\|", body):
            errors.append(f"final acceptance lane manifest has no row for {lane_id}")
    if "->" not in body:
        errors.append("final acceptance lane topology has no arrow graph")
    return errors


def validate(text: str, require_scoped_locks: bool = False) -> list[str]:
    errors: list[str] = []
    positions = []
    for heading in HEADINGS:
        count = text.count(heading)
        if count != 1:
            errors.append(f"expected one {heading!r}, found {count}")
            continue
        positions.append(text.index(heading))
    if len(positions) == len(HEADINGS) and positions != sorted(positions):
        errors.append("required sections are out of order")

    placeholders = sorted(set(re.findall(r"<[^>\n]+>", text)))
    if placeholders:
        preview = ", ".join(placeholders[:5])
        errors.append(f"unfilled angle-bracket placeholders remain: {preview}")

    if all(heading in text for heading in HEADINGS):
        checklist_values = table_id_list(section(text, HEADINGS[2], HEADINGS[3]))
        coverage_values = table_id_list(section(text, HEADINGS[4], HEADINGS[5]))
        checklist = set(checklist_values)
        coverage = set(coverage_values)
        if not checklist_values:
            errors.append("coverage checklist contains no C<number> rows")
        for label, values in (
            ("coverage checklist", checklist_values),
            ("coverage map", coverage_values),
        ):
            duplicates = duplicate_ids(values)
            if duplicates:
                errors.append(f"{label} contains duplicate IDs: {', '.join(duplicates)}")
        missing = sorted(checklist - coverage)
        extra = sorted(coverage - checklist)
        if missing:
            errors.append(f"coverage map is missing: {', '.join(missing)}")
        if extra:
            errors.append(f"coverage map has unknown IDs: {', '.join(extra)}")

        disposition = section(text, HEADINGS[3], HEADINGS[4]).lower()
        if not any(
            value in disposition
            for value in (
                "reused as-is",
                "reused with minor adjustment",
                "re-decomposed",
            )
        ):
            errors.append("decomposition has no allowed disposition")

        for heading, markers in SECTION_MARKERS.items():
            index = HEADINGS.index(heading)
            body = section(
                text,
                heading,
                HEADINGS[index + 1] if index + 1 < len(HEADINGS) else None,
            ).lower()
            for marker in markers:
                if marker not in body:
                    errors.append(f"{heading} is missing required decision: {marker}")

        step_body = section(text, HEADINGS[6], HEADINGS[7])
        errors.extend(
            validate_step_lane_topologies(
                step_body,
                role_pool_size(text, r"reviewer-main"),
                role_pool_size(text, r"doer-main"),
            )
        )
        final_body = section(text, HEADINGS[7], HEADINGS[8])
        errors.extend(validate_final_lane_topology(final_body))

        if require_scoped_locks:
            rules_body = section(text, HEADINGS[9], HEADINGS[10]).lower()
            for marker in (
                "external-operation readiness",
                "scoped lock-input domains",
                "gate dependency matrix",
                "governing-change classification",
                "conservative fallback",
            ):
                if marker not in rules_body:
                    errors.append(f"scoped-lock plan is missing required decision: {marker}")

    gap_match = re.search(r"Gaps\s*/\s*surfaced issues[^:]*:\s*([^\n]+)", text, re.IGNORECASE)
    if not gap_match or gap_match.group(1).strip().lower() not in {"none", "none."}:
        errors.append("gaps/surfaced issues must be present and equal to none")

    for marker in HARNESS_MARKERS:
        if marker not in text:
            errors.append(f"missing current Portable Harness binding: {marker}")

    singular_roles = {
        "orchestrator/planner-executor": r"orchestrator\s*/\s*planner-executor",
        "coder-main": r"coder-main",
    }
    for label, pattern in singular_roles.items():
        size = role_pool_size(text, pattern)
        if size is None:
            errors.append(f"cannot read numeric pool size for {label}")
        elif size != 1:
            errors.append(f"{label} must have pool size 1, found {size}")

    for role in ("reviewer-main", "doer-main", "final-reviewer"):
        size = role_pool_size(text, re.escape(role))
        if size is None:
            errors.append(f"cannot read numeric pool size for {role}")
            continue
        if not 1 <= size <= 3:
            errors.append(f"{role} pool size {size} exceeds manager-plus-three cap")

    required_rules = [
        "stall_threshold",
        "scope_policy",
        "gap_scope",
        "final_full_verification",
        "passed registry",
        "merge-then-triage",
        "test-id scheme",
        "pass criteria",
    ]
    lowered = text.lower()
    for rule in required_rules:
        if rule.lower() not in lowered:
            errors.append(f"missing required execution rule: {rule}")

    config_text = section(text, HEADINGS[-1], None) if HEADINGS[-1] in text else text
    thresholds = [int(value) for value in re.findall(r"(?i)`?stall_threshold`?[^\d\n]*(\d+)", config_text)]
    if not thresholds or not any(value > 0 for value in thresholds):
        errors.append("stall_threshold must have a positive integer value")

    if not re.search(r"(?i)`?gap_scope`?\s*:\s*`?(change|all-failing)`?", config_text):
        errors.append("gap_scope must be change or all-failing")
    if not re.search(r"(?i)`?final_full_verification`?\s*:\s*`?(true|false)`?", config_text):
        errors.append("final_full_verification must be true or false")

    config_decisions = (
        (r"executor[ _-](?:self-check decision|recordability_policy)", "executor self-check decision"),
        (r"(?:pooled process-environment correction policy|fixture_batch_policy)", "pooled process-environment correction policy"),
        (r"(?:external-operation readiness decision|[a-z0-9_]*rehearsal_policy)", "external-operation readiness decision"),
    )
    for pattern, label in config_decisions:
        if not re.search(pattern, config_text, re.IGNORECASE):
            errors.append(f"config block is missing required decision: {label}")

    if require_scoped_locks:
        for decision in (
            "scoped lock-input domains",
            "gate dependency matrix",
            "governing-change classification",
            "conservative fallback",
        ):
            if decision not in config_text.lower():
                errors.append(f"config block is missing required scoped-lock decision: {decision}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a generated harness execution plan.")
    parser.add_argument("plan", help="Plan path, or - for stdin")
    parser.add_argument(
        "--require-scoped-locks",
        action="store_true",
        help="Require the current scoped-lock planning contract; use for newly generated plans.",
    )
    args = parser.parse_args()
    try:
        text = sys.stdin.read() if args.plan == "-" else Path(args.plan).read_text(encoding="utf-8")
    except OSError as exc:
        parser.exit(2, f"cannot read plan: {exc}\n")

    errors = validate(text, require_scoped_locks=args.require_scoped_locks)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("execution plan validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
