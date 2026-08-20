from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

HEADINGS = [
    "## 0. Plan contract and status",
    "## 1. Inputs, authority, and directive hierarchy",
    "## 2. Goal, exclusions, and acceptance outcomes",
    "## 3. Requirement coverage map",
    "## 4. Runtime and repository truth",
    "## 5. Deliverable, dependency, risk, and cost model",
    "## 6. Workflow module selection manifest",
    "## 7. Roles and role-model mapping boundary",
    "## 8. Composed execution graph and critical path",
    "## 9. Global workflow policies and exceptions",
    "## 10. Lane, resource, result, and handoff manifest",
    "## 11. Module instances",
    "## 12. External and practical validation",
    "## 13. Integration, safeguard, promotion, rollback, and retirement",
    "## 14. Tolerances, unresolved decisions, and out-of-scope ledger",
    "## 15. Rule application matrix",
    "## 16. Structural validation result",
]

POLICY_HEADINGS = [
    "### P01 Ownership and decisions",
    "### P02 Context and thread lifetime",
    "### P03 Failure-case selection",
    "### P04 Check selection and green credit",
    "### P05 Review classes and invalidation",
    "### P06 Parallel checks and results",
    "### P07 Finding pooling and material repair",
    "### P08 Test-only correction",
    "### P09 Administrative recovery",
    "### P10 Semantic acceptance",
    "### P11 Full-safeguard scope",
    "### P12 External authorization and rehearsal",
    "### P13 Gate/loop sizing, health, and topology reassessment",
    "### P14 Exception classes",
    "### P15 Stop and live-harm containment",
]

INSTANCE_FIELDS = [
    "Purpose",
    "Coverage",
    "Selection basis",
    "Owner and roles",
    "Preconditions",
    "Inputs",
    "Local instructions",
    "Outputs and results",
    "Concurrency and isolation",
    "Resources and side effects",
    "Checks and acceptance",
    "Failure and exception routes",
    "Prior results and change effects",
    "Repeat, join, and terminal behavior",
    "Cost and critical-path effect",
]

TASK_FIELDS = [
    "schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id",
    "workflow_role",
    "objective",
    "why_now",
    "starting_state",
    "dependencies_and_predecessor_outputs",
    "working_scope",
    "required_behavior",
    "initial_entrypoints",
    "failure_case_brief",
    "ordered_actions",
    "allowed_tools_capabilities_resources",
    "forbidden_actions_and_boundaries",
    "verification",
    "deliverables_and_result_paths",
    "acceptance_criteria_and_tolerances",
    "completion_review_owner_and_handoff",
    "failure_classification_and_routes",
    "thread_resume_and_terminal_rule",
    "cited_global_policy_ids_and_exception_ids",
]

UNDISPATCHABLE_BARE_TASK_VALUES = {"", "N/A", "TBD", "TODO", "UNKNOWN"}

MODULE_IDS = [f"M{number:02d}" for number in range(1, 11)]
MODULE_ACTION_COUNTS = {
    "M01": 7,
    "M02": 8,
    "M03": 7,
    "M04": 8,
    "M05": 10,
    "M06": 8,
    "M07": 7,
    "M08": 6,
    "M09": 9,
    "M10": 5,
}
MODULE_ACTIONS = {
    module_id: [f"{module_id}-A{number}" for number in range(1, count + 1)]
    for module_id, count in MODULE_ACTION_COUNTS.items()
}
RULE_IDS = [f"R{number}" for number in range(1, 31)] + [f"S{number}" for number in range(1, 17)]
CHECK_IDS = [f"V{number:02d}" for number in range(1, 30)]
ALLOWED_CAPABILITY_STATES = {
    "RUNTIME_ENFORCED",
    "ORCHESTRATOR_ENFORCED",
    "TARGET_TOOL_INVOKED",
    "UNAVAILABLE",
}
ALLOWED_MODULE_DECISIONS = {"SELECTED", "OMITTED", "DEFERRED"}
ALLOWED_GATE_CLASSES = {"PRODUCT", "OPERATION_BOUNDARY"}

REQUIRED_TABLES: dict[str, list[tuple[str, ...]]] = {
    HEADINGS[0]: [("Field", "Value")],
    HEADINGS[1]: [
        (
            "Source",
            "Authority",
            "Path/reference",
            "Supplies",
            "Conflict rule",
        ),
        ("Layer", "Authority", "May define", "Must not override"),
    ],
    HEADINGS[2]: [
        (
            "Outcome ID",
            "Required behavior",
            "Acceptance method",
            "Decision owner",
            "Status",
        ),
        (
            "Boundary ID",
            "Type",
            "Included/excluded/authorization condition",
            "Reason",
            "Owner",
        ),
    ],
    HEADINGS[3]: [
        (
            "Requirement ID",
            "Source",
            "Deliverable ID",
            "Implementation owner",
            "Verification",
            "Acceptance owner",
            "Status",
        )
    ],
    HEADINGS[4]: [
        (
            "Capability/action",
            "State",
            "Source of truth",
            "Invocation owner",
            "Preconditions",
            "How confirmed",
            "Fallback",
        )
    ],
    HEADINGS[5]: [
        (
            "Deliverable ID",
            "Behavioral output",
            "Requirement IDs",
            "Dependencies",
            "Shared seams",
            "Release unit",
        ),
        (
            "Deliverable ID",
            "Realistic failure",
            "Impact",
            "Coupling",
            "Expected range",
            "Expensive operations",
            "Cheapest adequate topology",
            "Why",
        ),
    ],
    HEADINGS[6]: [
        (
            "Module type",
            "Decision",
            "Instance IDs",
            "Reason",
            "Prerequisite/owner if deferred",
        )
    ],
    HEADINGS[7]: [
        (
            "Workflow role",
            "Responsibilities",
            "Pool",
            "Context class",
            "Write authority",
            "Resources",
            "Activation",
            "Lifetime",
        ),
        ("Resolution rule", "Unknown-role behavior", "Mapping-update behavior"),
    ],
    HEADINGS[8]: [
        (
            "Edge ID",
            "From/output",
            "To/input",
            "Condition",
            "Serial/parallel",
            "Join ID",
            "Failure branch",
        ),
        (
            "Parallel group",
            "Shared input",
            "Member instance IDs",
            "Writable-root isolation",
            "Launch rule",
            "Join ID",
            "Serial exception",
        ),
        (
            "Path ID",
            "Ordered instance/edge IDs",
            "Expected range",
            "Overlap",
            "Expensive operations",
            "Why critical",
        ),
        (
            "Gate/loop ID",
            "Gate class",
            "Shared input",
            "Decided behavioral outcome",
            "Checking module instances",
            "Shared failure family/invariants",
            "Blocking scope",
            "Continuation/loop eligibility",
            "Default-forward edge",
            "Failure return target",
            "Aggregation payoff",
            "Manageability proof",
            "Prior-result boundary",
            "Split/merge trigger",
        ),
    ],
    HEADINGS[10]: [
        (
            "Lane ID",
            "Module instance",
            "Role",
            "Activation",
            "Mutable root",
            "Consumer",
            "Completion condition",
            "Failure route",
        ),
        (
            "Claim/lock ID",
            "Resource",
            "Owner",
            "Activation",
            "Mutable root",
            "Consumer",
            "Completion condition",
            "Failure route",
        ),
        (
            "Check",
            "Proves",
            "Dependencies",
            "Result owner",
            "Reuse condition",
            "Rerun route",
            "Result path if needed",
            "Failure route",
        ),
        (
            "Result/handoff ID",
            "Producer",
            "Consumer",
            "Path if durable",
            "Correlation needed",
            "Publication rule",
            "Completion condition",
            "Failure route",
        ),
        (
            "Source allocation ID",
            "Mode",
            "Source/worktree",
            "Writer",
            "Mutable root",
            "Consumer",
            "Completion condition",
            "Failure route",
        ),
        (
            "Retirement ID",
            "Target",
            "Owner",
            "Activation",
            "What must be retained",
            "Completion condition",
            "Recovery visibility",
            "Failure route",
        ),
    ],
    HEADINGS[12]: [
        (
            "Decision ID",
            "Module type",
            "Decision",
            "Authority/resource",
            "Synthetic proof",
            "Real proof",
            "Owner",
            "Failure route",
        )
    ],
    HEADINGS[13]: [
        (
            "Decision ID",
            "Module type",
            "Decision",
            "Accepted input",
            "Action/order",
            "Checks",
            "Promotion/rollback/retirement",
            "Owner",
        )
    ],
    HEADINGS[14]: [
        (
            "Item ID",
            "Type",
            "Exact condition",
            "Consequence",
            "Owner",
            "Resolution boundary",
        )
    ],
    HEADINGS[15]: [("Rule ID", "Plan location", "Applied behavior or justified N/A")],
    HEADINGS[16]: [("Check ID", "Result", "Basis")],
}

POLICY_TABLE = (
    "Owner",
    "Trigger",
    "Required action",
    "Exit",
    "Result/record if needed",
    "Module IDs",
)
EXCEPTION_TABLE = (
    "Exception ID",
    "Affected policy",
    "Exact trigger",
    "Decision owner",
    "Allowed alternate action",
    "Required confirmation",
    "Preserved results",
    "Invalidated results",
    "Scope",
    "Expiry",
)
INSTANCE_RE = re.compile(r"(?m)^###\s+(MI-[A-Z0-9][A-Z0-9_-]*)\s+-\s+(M\d{2}):\s+(.+?)\s*$")
MI_RE = re.compile(r"\bMI-[A-Z0-9][A-Z0-9_-]*\b")


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().strip("`"))


def table_cells(line: str) -> list[str] | None:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    return [normalize(cell) for cell in stripped[1:-1].split("|")]


def is_separator(cells: list[str] | None) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def extract_table(body: str, header: tuple[str, ...]) -> list[list[str]] | None:
    lines = body.splitlines()
    expected = list(header)
    for index, line in enumerate(lines):
        if table_cells(line) != expected:
            continue
        if index + 1 >= len(lines) or not is_separator(table_cells(lines[index + 1])):
            return []
        rows: list[list[str]] = []
        for row_line in lines[index + 2 :]:
            cells = table_cells(row_line)
            if cells is None:
                if rows or row_line.strip():
                    break
                continue
            if len(cells) != len(expected):
                rows.append(cells)
                continue
            rows.append(cells)
        return rows
    return None


def section(text: str, heading: str, next_heading: str | None) -> str:
    start = text.index(heading) + len(heading)
    end = text.index(next_heading, start) if next_heading else len(text)
    return text[start:end]


def sections(text: str) -> dict[str, str]:
    return {
        heading: section(text, heading, HEADINGS[index + 1] if index + 1 < len(HEADINGS) else None)
        for index, heading in enumerate(HEADINGS)
    }


def duplicates(values: list[str]) -> list[str]:
    return sorted(value for value, count in Counter(values).items() if count > 1)


def id_column(rows: list[list[str]], pattern: str) -> list[str]:
    return [row[0] for row in rows if row and re.fullmatch(pattern, row[0])]


def validate_required_tables(by_section: dict[str, str]) -> list[str]:
    errors: list[str] = []
    for heading, headers in REQUIRED_TABLES.items():
        body = by_section[heading]
        for header in headers:
            rows = extract_table(body, header)
            if rows is None:
                errors.append(f"{heading} is missing table: {' | '.join(header)}")
            elif not rows:
                errors.append(f"{heading} table has no data rows: {' | '.join(header)}")
            elif any(len(row) != len(header) for row in rows):
                errors.append(f"{heading} table has a row with the wrong column count: {' | '.join(header)}")
    return errors


def validate_module_manifest(body: str) -> tuple[list[str], dict[str, str]]:
    errors: list[str] = []
    header = REQUIRED_TABLES[HEADINGS[6]][0]
    rows = extract_table(body, header) or []
    seen_modules = [row[0] for row in rows if len(row) == len(header)]
    if duplicates(seen_modules):
        errors.append(f"module manifest contains duplicates: {', '.join(duplicates(seen_modules))}")
    missing = sorted(set(MODULE_IDS) - set(seen_modules))
    extra = sorted(set(seen_modules) - set(MODULE_IDS))
    if missing:
        errors.append(f"module manifest is missing: {', '.join(missing)}")
    if extra:
        errors.append(f"module manifest has unknown module IDs: {', '.join(extra)}")

    instance_types: dict[str, str] = {}
    for row in rows:
        if len(row) != len(header) or row[0] not in MODULE_IDS:
            continue
        module_id, decision, ids_cell = row[0], row[1].upper(), row[2]
        if decision not in ALLOWED_MODULE_DECISIONS:
            errors.append(f"{module_id} has invalid decision {row[1]!r}")
            continue
        instance_ids = MI_RE.findall(ids_cell)
        if decision == "SELECTED" and not instance_ids:
            errors.append(f"{module_id} is SELECTED but has no MI-* instance ID")
        if decision != "SELECTED" and instance_ids:
            errors.append(f"{module_id} is {decision} but declares instance IDs")
        for instance_id in instance_ids:
            if instance_id in instance_types:
                errors.append(f"module instance ID is declared more than once: {instance_id}")
            instance_types[instance_id] = module_id
    return errors, instance_types


def validate_instances(body: str, instance_types: dict[str, str]) -> list[str]:
    errors: list[str] = []
    matches = list(INSTANCE_RE.finditer(body))
    found_ids = [match.group(1) for match in matches]
    if duplicates(found_ids):
        errors.append(f"Section 11 contains duplicate module blocks: {', '.join(duplicates(found_ids))}")
    missing = sorted(set(instance_types) - set(found_ids))
    extra = sorted(set(found_ids) - set(instance_types))
    if missing:
        errors.append(f"selected module instances missing from Section 11: {', '.join(missing)}")
    if extra:
        errors.append(f"Section 11 has undeclared module instances: {', '.join(extra)}")

    for index, match in enumerate(matches):
        instance_id, module_type = match.group(1), match.group(2)
        block_end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        block = body[match.end() : block_end]
        if instance_types.get(instance_id) != module_type:
            errors.append(
                f"{instance_id} block type {module_type} does not match manifest type "
                f"{instance_types.get(instance_id, 'UNDECLARED')}"
            )
        fields = re.findall(r"(?m)^####\s+(.+?)\s*$", block)
        if fields != INSTANCE_FIELDS:
            errors.append(f"{instance_id} does not use the exact 15 subheadings in order")
        local_start = block.find("#### Local instructions")
        local_end = block.find("#### Outputs and results", local_start + 1)
        local_body = block[local_start:local_end] if local_start >= 0 and local_end >= 0 else ""
        task_rows = extract_table(local_body, ("Field", "Value"))
        if task_rows is None:
            errors.append(f"{instance_id} has no local task-card Field | Value table")
        else:
            valid_task_rows = [row for row in task_rows if len(row) == 2]
            if [row[0] for row in valid_task_rows] != TASK_FIELDS:
                errors.append(f"{instance_id} does not use all 20 local task-card fields in order")
            task_values = {row[0]: row[1] for row in valid_task_rows}
            for task_field in TASK_FIELDS:
                task_value = normalize(task_values.get(task_field, "")).upper()
                if task_value in UNDISPATCHABLE_BARE_TASK_VALUES:
                    errors.append(
                        f"{instance_id} task field {task_field} has a bare placeholder; "
                        "ROOT must supply a concrete dispatch-contract value or a reasoned N/A "
                        "explicitly permitted by the selected recipe"
                    )
            found_actions = re.findall(r"\bM\d{2}-A\d+\b", task_values.get("ordered_actions", ""))
            if found_actions != MODULE_ACTIONS.get(module_type, []):
                errors.append(
                    f"{instance_id} ordered_actions must contain "
                    f"{', '.join(MODULE_ACTIONS.get(module_type, []))} exactly once and in order"
                )
    return errors


def validate_policies(body: str) -> list[str]:
    errors: list[str] = []
    found = re.findall(r"(?m)^###\s+P\d{2}.+?$", body)
    if found != POLICY_HEADINGS:
        errors.append("Section 9 does not contain exact P01-P15 policy headings in order")
        return errors
    for index, heading in enumerate(POLICY_HEADINGS):
        start = body.index(heading) + len(heading)
        end = body.index(POLICY_HEADINGS[index + 1], start) if index + 1 < len(POLICY_HEADINGS) else len(body)
        policy_body = body[start:end]
        rows = extract_table(policy_body, POLICY_TABLE)
        if rows is None or not rows:
            errors.append(f"{heading} has no populated policy table")
        if heading.startswith("### P14"):
            exception_rows = extract_table(policy_body, EXCEPTION_TABLE)
            if exception_rows is None or not exception_rows:
                errors.append("P14 has no exception-class table or reasoned N/A row")
    return errors


def validate_verification_economy(by_section: dict[str, str], text: str) -> list[str]:
    """Validate the optional checkpointed-gate protocol for newly amended plans."""

    checkpointed = "checkpointed_verification_v1" in text.lower()
    fast_lane_v2 = "fast_lane_v2" in text.lower()
    if fast_lane_v2 and not checkpointed:
        return ["FAST_LANE_V2 requires CHECKPOINTED_VERIFICATION_V1"]
    if not checkpointed:
        return []

    errors: list[str] = []
    if "checkpointed_verification_v1" not in by_section[HEADINGS[0]].lower():
        errors.append("CHECKPOINTED_VERIFICATION_V1 must appear in Section 0")
    policy_text = "\n".join(
        by_section[heading]
        for heading in (
            "## 9. Global workflow policies and exceptions",
            "## 10. Lane, resource, result, and handoff manifest",
            "## 13. Integration, safeguard, promotion, rollback, and retirement",
        )
    ).lower()
    for term in ("checkpoint", "input map", "first unresolved", "earliest required", "ordinary failure"):
        if term not in policy_text:
            errors.append(f"CHECKPOINTED_VERIFICATION_V1 requires policy text for {term!r}")
    if fast_lane_v2:
        for term in (
            "complete pool",
            "motivating test",
            "compile",
            "review",
            "integration",
            "smoke credit",
        ):
            if term not in policy_text:
                errors.append(f"FAST_LANE_V2 requires policy text for {term!r}")
    return errors


def validate_gates(body: str) -> list[str]:
    errors: list[str] = []
    header = REQUIRED_TABLES[HEADINGS[8]][3]
    rows = extract_table(body, header) or []
    gate_ids = [row[0] for row in rows if len(row) == len(header) and row[0] != "N/A"]
    if duplicates(gate_ids):
        errors.append(f"gate manifest contains duplicates: {', '.join(duplicates(gate_ids))}")

    for row in rows:
        if len(row) != len(header) or row[0] == "N/A":
            continue
        gate_id, gate_class = row[0], row[1]
        if not gate_id.startswith("GATE-"):
            errors.append(f"gate row has invalid ID {gate_id!r}")
        if gate_class not in ALLOWED_GATE_CLASSES:
            errors.append(f"{gate_id} has invalid gate class {gate_class!r}")
        required_fields = (
            (6, "blocking scope"),
            (7, "continuation/loop eligibility"),
            (8, "default-forward edge"),
            (9, "failure return target"),
        )
        for index, label in required_fields:
            if row[index].lower() in {"", "n/a", "none", "not applicable"}:
                errors.append(f"{gate_id} has no {label}")
        blocking_scope = row[6].lower()
        continuation = row[7].lower()
        default_forward = row[8].lower()
        failure_target = row[9].lower()

        if not any(
            token in default_forward
            for token in (
                "edge",
                "advance",
                "continue",
                "accept",
                "success",
                "terminal",
            )
        ):
            errors.append(f"{gate_id} default-forward edge must name an advancing successor or terminal action")

        if gate_class == "PRODUCT":
            decided_outcome = row[3].lower()
            strong_product_terms = (
                "behavior",
                "contract",
                "satisf",
                "capability",
                "agree",
                "prove",
            )
            operation_terms = (
                "allocat",
                "integrat",
                "join",
                "deploy",
                "promot",
                "read back",
                "readback",
                "cleanup",
                "retire",
            )
            names_product_outcome = any(token in decided_outcome for token in strong_product_terms) or (
                "correct" in decided_outcome and not any(token in decided_outcome for token in operation_terms)
            )
            if not names_product_outcome:
                errors.append(
                    f"{gate_id} PRODUCT decided outcome must name observable behavior, "
                    "contract, capability, correctness, satisfaction, agreement, or proof; "
                    "a pure required operation belongs to OPERATION_BOUNDARY"
                )
            required_terms = ("only", "required", "product")
            if not all(term in continuation for term in required_terms) or not any(
                term in continuation for term in ("fail", "undecidable")
            ):
                errors.append(
                    f"{gate_id} PRODUCT continuation eligibility must say that only a failed/"
                    "undecidable required product criterion permits continuation"
                )
            if "only" not in blocking_scope:
                errors.append(f"{gate_id} PRODUCT blocking scope must be explicitly limited with 'only'")

        if gate_class == "OPERATION_BOUNDARY":
            if "only" not in blocking_scope or "never product" not in blocking_scope:
                errors.append(
                    f"{gate_id} OPERATION_BOUNDARY blocking scope must say it holds only the "
                    "exact operation and never product work/credit"
                )
            if "no product loop" not in continuation:
                errors.append(f"{gate_id} OPERATION_BOUNDARY continuation must explicitly say 'No product loop'")
            if any(
                token in failure_target
                for token in (
                    "m02",
                    "material repair",
                    "material return",
                    "product repair",
                )
            ):
                errors.append(f"{gate_id} OPERATION_BOUNDARY failure target must not enter product repair")
    return errors


def validate_cross_references(by_section: dict[str, str], instance_types: dict[str, str]) -> list[str]:
    errors: list[str] = []
    req_header = REQUIRED_TABLES[HEADINGS[3]][0]
    deliverable_header = REQUIRED_TABLES[HEADINGS[5]][0]
    req_rows = extract_table(by_section[HEADINGS[3]], req_header) or []
    deliverable_rows = extract_table(by_section[HEADINGS[5]], deliverable_header) or []
    req_ids = id_column(req_rows, r"REQ-[A-Z0-9][A-Z0-9._-]*")
    deliverable_ids = id_column(deliverable_rows, r"DEL-[A-Z0-9][A-Z0-9._-]*")
    if not req_ids:
        errors.append("requirement coverage map has no REQ-* rows")
    if not deliverable_ids:
        errors.append("deliverable model has no DEL-* rows")
    if duplicates(req_ids):
        errors.append(f"duplicate requirement IDs: {', '.join(duplicates(req_ids))}")
    if duplicates(deliverable_ids):
        errors.append(f"duplicate deliverable IDs: {', '.join(duplicates(deliverable_ids))}")
    known_deliverables = set(deliverable_ids)
    for row in req_rows:
        if len(row) == len(req_header) and row[0].startswith("REQ-") and row[2] not in known_deliverables:
            errors.append(f"{row[0]} references unknown deliverable {row[2]}")

    capability_rows = extract_table(by_section[HEADINGS[4]], REQUIRED_TABLES[HEADINGS[4]][0]) or []
    for row in capability_rows:
        if len(row) == 7 and row[0] != "N/A" and row[1] not in ALLOWED_CAPABILITY_STATES:
            errors.append(f"capability {row[0]!r} has invalid state {row[1]!r}")

    selected_ids = set(instance_types)
    for header in REQUIRED_TABLES[HEADINGS[8]]:
        rows = extract_table(by_section[HEADINGS[8]], header) or []
        for row in rows:
            for instance_id in MI_RE.findall(" ".join(row)):
                if instance_id not in selected_ids:
                    errors.append(f"Section 8 references undeclared module instance {instance_id}")
    return errors


def validate_roles(body: str, mapping_roles: set[str], mapping_name: str, text: str) -> list[str]:
    errors: list[str] = []
    role_rows = extract_table(body, REQUIRED_TABLES[HEADINGS[7]][0]) or []
    plan_roles = [row[0] for row in role_rows if len(row) == 8 and row[0] != "N/A"]
    if not plan_roles:
        errors.append("role table contains no workflow roles")
    if duplicates(plan_roles):
        errors.append(f"role table contains duplicate roles: {', '.join(duplicates(plan_roles))}")
    if set(plan_roles) != mapping_roles:
        missing = sorted(set(plan_roles) - mapping_roles)
        extra = sorted(mapping_roles - set(plan_roles))
        if missing:
            errors.append(f"mapping is missing plan roles: {', '.join(missing)}")
        if extra:
            errors.append(f"mapping has roles absent from the plan: {', '.join(extra)}")
    for row in role_rows:
        if len(row) != 8 or row[0] == "N/A":
            continue
        pool_match = re.search(r"\b(\d+)\b", row[2])
        if pool_match is None or int(pool_match.group(1)) < 1:
            errors.append(f"role {row[0]} has no positive pool size")
    if text.lower().count(mapping_name.lower()) != 1:
        errors.append(f"plan must mention mapping filename {mapping_name!r} exactly once")
    return errors


def validate_rule_and_check_matrices(by_section: dict[str, str]) -> list[str]:
    errors: list[str] = []
    rule_rows = extract_table(by_section[HEADINGS[15]], REQUIRED_TABLES[HEADINGS[15]][0]) or []
    rule_ids = [row[0] for row in rule_rows if len(row) == 3]
    if rule_ids != RULE_IDS:
        errors.append("Section 15 must map R1-R30 then S1-S16 exactly once and in order")

    check_rows = extract_table(by_section[HEADINGS[16]], REQUIRED_TABLES[HEADINGS[16]][0]) or []
    check_ids = [row[0] for row in check_rows if len(row) == 3]
    if check_ids != CHECK_IDS:
        errors.append("Section 16 must contain V01-V29 exactly once and in order")
    for row in check_rows:
        if len(row) == 3 and row[1] != "PASS":
            errors.append(f"{row[0]} is not PASS")
        if len(row) == 3 and not row[2].strip():
            errors.append(f"{row[0]} has no basis")
    marker_count = by_section[HEADINGS[16]].count("PLAN_STRUCTURE=VALID")
    if marker_count != 1:
        errors.append(f"expected one PLAN_STRUCTURE=VALID marker, found {marker_count}")
    if "PLAN_STRUCTURE=INVALID" in by_section[HEADINGS[16]]:
        errors.append("Section 16 still contains PLAN_STRUCTURE=INVALID")
    return errors


def validate(text: str, mapping_roles: set[str], mapping_name: str) -> list[str]:
    errors: list[str] = []
    title_matches = re.findall(r"(?m)^#\s+.+\s+-\s+Modular Execution Plan\s*$", text)
    if len(title_matches) != 1:
        errors.append(f"expected one modular execution plan title, found {len(title_matches)}")

    positions: list[int] = []
    for heading in HEADINGS:
        count = text.count(heading)
        if count != 1:
            errors.append(f"expected one {heading!r}, found {count}")
        else:
            positions.append(text.index(heading))
    if len(positions) == len(HEADINGS) and positions != sorted(positions):
        errors.append("Sections 0-16 are out of order")
    if errors:
        return errors

    unresolved = sorted(set(re.findall(r"\{\{[^}\n]+\}\}", text)))
    if unresolved:
        errors.append(f"unresolved template tokens remain: {', '.join(unresolved[:5])}")
    if "TEMPLATE NOTE:" in text:
        errors.append("TEMPLATE NOTE lines remain in the generated plan")
    angle_placeholders = sorted(set(re.findall(r"<[^>\n]+>", text)))
    if angle_placeholders:
        errors.append(f"angle-bracket placeholders remain: {', '.join(angle_placeholders[:5])}")

    by_section = sections(text)
    errors.extend(validate_required_tables(by_section))
    manifest_errors, instance_types = validate_module_manifest(by_section[HEADINGS[6]])
    errors.extend(manifest_errors)
    errors.extend(validate_instances(by_section[HEADINGS[11]], instance_types))
    errors.extend(validate_policies(by_section[HEADINGS[9]]))
    errors.extend(validate_verification_economy(by_section, text))
    errors.extend(validate_gates(by_section[HEADINGS[8]]))
    errors.extend(validate_cross_references(by_section, instance_types))
    errors.extend(validate_roles(by_section[HEADINGS[7]], mapping_roles, mapping_name, text))
    errors.extend(validate_rule_and_check_matrices(by_section))

    local_instructions = by_section[HEADINGS[11]].lower()
    for phrase in ("as needed", "if useful", "best practice"):
        if phrase in local_instructions:
            errors.append(f"module local instructions contain banned vague phrase: {phrase!r}")
    return errors


def markdown_table(header: tuple[str, ...], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(header) + " |",
        "|" + "|".join("---" for _ in header) + "|",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def build_self_test_plan() -> str:
    parts = ["# Validator Self Test - Modular Execution Plan"]
    parts += [
        HEADINGS[0],
        markdown_table(
            ("Field", "Value"),
            [["Plan ID", "SELF-TEST"], ["Verification protocol", "N/A"]],
        ),
    ]
    parts += [
        HEADINGS[1],
        markdown_table(
            REQUIRED_TABLES[HEADINGS[1]][0],
            [["SRC-001", "goal", "mapping.json", "mapping", "user wins"]],
        ),
        markdown_table(REQUIRED_TABLES[HEADINGS[1]][1], [["1", "user", "goal", "N/A"]]),
    ]
    parts += [
        HEADINGS[2],
        "Goal: validate the validator.",
        markdown_table(
            REQUIRED_TABLES[HEADINGS[2]][0],
            [["OUT-001", "valid plan", "validator pass", "orchestrator", "covered"]],
        ),
        markdown_table(
            REQUIRED_TABLES[HEADINGS[2]][1],
            [["BOUND-001", "in scope", "validation", "self test", "orchestrator"]],
        ),
    ]
    parts += [
        HEADINGS[3],
        markdown_table(
            REQUIRED_TABLES[HEADINGS[3]][0],
            [
                [
                    "REQ-001",
                    "SRC-001",
                    "DEL-001",
                    "orchestrator",
                    "CHECK-001",
                    "orchestrator",
                    "covered",
                ]
            ],
        ),
        HEADINGS[4],
        markdown_table(
            REQUIRED_TABLES[HEADINGS[4]][0],
            [
                [
                    "validation",
                    "ORCHESTRATOR_ENFORCED",
                    "script",
                    "orchestrator",
                    "plan",
                    "exit 0",
                    "fix",
                ]
            ],
        ),
        HEADINGS[5],
        markdown_table(
            REQUIRED_TABLES[HEADINGS[5]][0],
            [["DEL-001", "valid plan", "REQ-001", "none", "schema", "plan"]],
        ),
        markdown_table(
            REQUIRED_TABLES[HEADINGS[5]][1],
            [
                [
                    "DEL-001",
                    "shape error",
                    "invalid",
                    "low",
                    "short",
                    "none",
                    "M05",
                    "accept",
                ]
            ],
        ),
    ]
    module_rows = [[module_id, "OMITTED", "N/A", "not required", "N/A"] for module_id in MODULE_IDS]
    module_rows[4] = ["M05", "SELECTED", "MI-001", "semantic acceptance", "N/A"]
    parts += [HEADINGS[6], markdown_table(REQUIRED_TABLES[HEADINGS[6]][0], module_rows)]
    parts += [
        HEADINGS[7],
        markdown_table(
            REQUIRED_TABLES[HEADINGS[7]][0],
            [
                [
                    "orchestrator",
                    "accept",
                    "1",
                    "bounded",
                    "none",
                    "none",
                    "plan ready",
                    "plan",
                ]
            ],
        ),
        markdown_table(
            REQUIRED_TABLES[HEADINGS[7]][1],
            [["resolve at launch", "reject", "no plan edit"]],
        ),
    ]
    parts += [HEADINGS[8]]
    parts.append(
        markdown_table(
            REQUIRED_TABLES[HEADINGS[8]][0],
            [
                [
                    "EDGE-001",
                    "MI-001.output",
                    "terminal",
                    "accepted",
                    "serial",
                    "N/A",
                    "incomplete",
                ]
            ],
        )
    )
    parts.append(
        markdown_table(
            REQUIRED_TABLES[HEADINGS[8]][1],
            [["N/A", "N/A", "N/A", "no parallel work", "N/A", "N/A", "N/A"]],
        )
    )
    parts.append(
        markdown_table(
            REQUIRED_TABLES[HEADINGS[8]][2],
            [["PATH-001", "MI-001", "short", "none", "none", "only path"]],
        )
    )
    parts.append(
        markdown_table(
            REQUIRED_TABLES[HEADINGS[8]][3],
            [
                [
                    "GATE-001 / LOOP-001",
                    "PRODUCT",
                    "revision",
                    "Does the required product plan behavior satisfy its acceptance contract?",
                    "MI-001",
                    "plan semantics",
                    "DEL-001 product acceptance only",
                    "only when a required product criterion fails or is genuinely undecidable",
                    "accepted -> terminal",
                    "same MI-001 task",
                    "one decision",
                    "one owner",
                    "unrelated credit preserved",
                    "split on independent criterion",
                ],
                [
                    "GATE-002",
                    "OPERATION_BOUNDARY",
                    "deployment target state",
                    "May the exact deployment operation start?",
                    "MI-001",
                    "authorization and destination state",
                    "only deployment allocation; never product acceptance or credit",
                    "No product loop; retry only the unresolved deployment admission action",
                    "accepted product work continues to terminal",
                    "same deployment admission action or stop allocation",
                    "one admission check",
                    "one operation owner",
                    "product credit preserved",
                    "split on independent resource",
                ],
            ],
        )
    )
    parts += [HEADINGS[9]]
    for policy in POLICY_HEADINGS:
        parts += [
            policy,
            markdown_table(
                POLICY_TABLE,
                [["orchestrator", "plan", "decide", "recorded", "plan", "MI-001"]],
            ),
        ]
        if policy.startswith("### P14"):
            parts.append(markdown_table(EXCEPTION_TABLE, [["N/A"] * len(EXCEPTION_TABLE)]))
    parts += [HEADINGS[10]]
    for header in REQUIRED_TABLES[HEADINGS[10]]:
        parts.append(markdown_table(header, [["N/A"] * len(header)]))
    parts += [HEADINGS[11], "### MI-001 - M05: Acceptance"]
    for field in INSTANCE_FIELDS:
        parts += [f"#### {field}"]
        if field == "Local instructions":
            task_rows = [[task_field, f"self-test concrete {task_field}"] for task_field in TASK_FIELDS]
            task_rows[TASK_FIELDS.index("workflow_role")][1] = "orchestrator"
            task_rows[TASK_FIELDS.index("ordered_actions")][1] = "; ".join(MODULE_ACTIONS["M05"])
            parts.append(markdown_table(("Field", "Value"), task_rows))
        else:
            parts.append("Self-test value.")
    parts += [
        HEADINGS[12],
        markdown_table(REQUIRED_TABLES[HEADINGS[12]][0], [["N/A"] * 8]),
        HEADINGS[13],
        markdown_table(REQUIRED_TABLES[HEADINGS[13]][0], [["N/A"] * 8]),
        HEADINGS[14],
        markdown_table(
            REQUIRED_TABLES[HEADINGS[14]][0],
            [["N/A", "OUT_OF_SCOPE", "none", "none", "orchestrator", "terminal"]],
        ),
        HEADINGS[15],
        markdown_table(
            REQUIRED_TABLES[HEADINGS[15]][0],
            [[rule_id, "self test", "applied"] for rule_id in RULE_IDS],
        ),
        HEADINGS[16],
        markdown_table(
            REQUIRED_TABLES[HEADINGS[16]][0],
            [[check_id, "PASS", "self test"] for check_id in CHECK_IDS],
        ),
        "PLAN_STRUCTURE=VALID",
    ]
    return "\n\n".join(parts) + "\n"


def run_self_test() -> list[str]:
    plan = build_self_test_plan()
    failures: list[str] = []
    if errors := validate(plan, {"orchestrator"}, "mapping.json"):
        failures.append("valid fixture failed: " + "; ".join(errors))

    checkpointed = plan.replace(
        "| Verification protocol | N/A |",
        "| Verification protocol | CHECKPOINTED_VERIFICATION_V1 |",
        1,
    ).replace(
        "| orchestrator | plan | decide | recorded | plan | MI-001 |",
        "| orchestrator | checkpoint | input map; first unresolved; earliest required; "
        "ordinary failure continuation | "
        "recorded | plan | MI-001 |",
        1,
    )
    if errors := validate(checkpointed, {"orchestrator"}, "mapping.json"):
        failures.append("checkpointed fixture failed: " + "; ".join(errors))

    fast_lane = checkpointed.replace(
        "input map; first unresolved; earliest required; ordinary failure continuation",
        "input map; first unresolved; earliest required; ordinary failure continuation; "
        "FAST_LANE_V2 complete pool motivating test compile review integration smoke credit",
        1,
    )
    if errors := validate(fast_lane, {"orchestrator"}, "mapping.json"):
        failures.append("FAST_LANE_V2 fixture failed: " + "; ".join(errors))

    corruptions = {
        "placeholder": plan + "\n{{UNFILLED}}\n",
        "module manifest": plan.replace("| M10 | OMITTED |", "| M09 | OMITTED |", 1),
        "instance schema": plan.replace("#### Cost and critical-path effect\n\nSelf-test value.\n", "", 1),
        "bare ROOT dispatch field": plan.replace(
            "| objective | self-test concrete objective |",
            "| objective | N/A |",
            1,
        ),
        "gate class": plan.replace("| GATE-001 / LOOP-001 | PRODUCT |", "| GATE-001 / LOOP-001 | ADVISORY |", 1),
        "product gate eligibility": plan.replace(
            "only when a required product criterion fails or is genuinely undecidable",
            "after any gate failure",
            1,
        ),
        "pure operation mislabeled product": plan.replace(
            "Does the required product plan behavior satisfy its acceptance contract?",
            "Was the exact accepted coordinate promoted and read back?",
            1,
        ),
        "operation with correctness word mislabeled product": plan.replace(
            "Does the required product plan behavior satisfy its acceptance contract?",
            "Was the required product promotion correct?",
            1,
        ),
        "operation boundary scope": plan.replace(
            "only deployment allocation; never product acceptance or credit",
            "the entire deployment and product",
            1,
        ),
        "operation boundary product repair": plan.replace(
            "same deployment admission action or stop allocation",
            "M02 material repair",
            1,
        ),
        "checkpoint marker without protocol": plan.replace(
            "| Verification protocol | N/A |",
            "| Verification protocol | CHECKPOINTED_VERIFICATION_V1 |",
            1,
        ),
        "checkpoint marker outside Section 0": plan + "\nCHECKPOINTED_VERIFICATION_V1\n",
        "FAST_LANE_V2 without checkpoint protocol": plan.replace(
            "| Verification protocol | N/A |",
            "| Verification protocol | FAST_LANE_V2 |",
            1,
        ),
        "checkpoint protocol without earliest required route": checkpointed.replace(
            "earliest required",
            "resume point",
            1,
        ),
        "FAST_LANE_V2 without complete pool": fast_lane.replace(
            "complete pool",
            "partial pool",
            1,
        ),
        "FAST_LANE_V2 without smoke credit": fast_lane.replace(
            "smoke credit",
            "smoke result",
            1,
        ),
    }
    for label, corrupted in corruptions.items():
        if not validate(corrupted, {"orchestrator"}, "mapping.json"):
            failures.append(f"{label} corruption was not detected")
    if not validate(plan, {"different-role"}, "mapping.json"):
        failures.append("mapping-role mismatch was not detected")
    return failures


def load_mapping(path: Path) -> tuple[set[str], list[str]]:
    try:
        data: Any = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return set(), [f"cannot read role-model mapping {path}: {exc}"]
    if not isinstance(data, dict) or not isinstance(data.get("roles"), dict):
        return set(), ["role-model mapping must be a JSON object containing a roles object"]
    roles = data["roles"]
    errors = [
        f"mapping role {role!r} must contain an object" for role, value in roles.items() if not isinstance(value, dict)
    ]
    if not roles:
        errors.append("role-model mapping contains no roles")
    return set(roles), errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a modular execution plan's deterministic structure.")
    parser.add_argument("plan", nargs="?", help="generated execution plan path, or - for stdin")
    parser.add_argument("--mapping", help="canonical role-model mapping JSON path")
    parser.add_argument("--self-test", action="store_true", help="run validator contract tests")
    args = parser.parse_args()

    if args.self_test:
        failures = run_self_test()
        if failures:
            for failure in failures:
                print(f"SELF-TEST ERROR: {failure}", file=sys.stderr)
            return 1
        print("execution plan validator self-test: PASS")
        return 0

    if args.plan is None or args.mapping is None:
        parser.error("plan and --mapping are required unless --self-test is used")
    mapping_path = Path(args.mapping)
    mapping_roles, mapping_errors = load_mapping(mapping_path)
    if mapping_errors:
        for error in mapping_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    try:
        text = sys.stdin.read() if args.plan == "-" else Path(args.plan).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        parser.exit(2, f"cannot read plan: {exc}\n")

    errors = validate(text, mapping_roles, mapping_path.name)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("execution plan validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
