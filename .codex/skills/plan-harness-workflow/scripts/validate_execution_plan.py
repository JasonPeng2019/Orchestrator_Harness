from __future__ import annotations

import argparse
import re
import sys
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
    "evaluator_enabled",
]


def section(text: str, heading: str, next_heading: str | None) -> str:
    start = text.index(heading) + len(heading)
    end = text.index(next_heading, start) if next_heading else len(text)
    return text[start:end]


def table_ids(value: str) -> set[str]:
    return set(re.findall(r"(?m)^\|\s*(C\d+)\s*\|", value))


def validate(text: str) -> list[str]:
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
        checklist = table_ids(section(text, HEADINGS[2], HEADINGS[3]))
        coverage = table_ids(section(text, HEADINGS[4], HEADINGS[5]))
        if not checklist:
            errors.append("coverage checklist contains no C<number> rows")
        missing = sorted(checklist - coverage)
        extra = sorted(coverage - checklist)
        if missing:
            errors.append(f"coverage map is missing: {', '.join(missing)}")
        if extra:
            errors.append(f"coverage map has unknown IDs: {', '.join(extra)}")

    gap_match = re.search(r"Gaps\s*/\s*surfaced issues[^:]*:\s*([^\n]+)", text, re.IGNORECASE)
    if not gap_match or gap_match.group(1).strip().lower() not in {"none", "none."}:
        errors.append("gaps/surfaced issues must be present and equal to none")

    for marker in HARNESS_MARKERS:
        if marker not in text:
            errors.append(f"missing current Portable Harness binding: {marker}")

    for role in ("reviewer-main", "doer-main", "final-reviewer"):
        match = re.search(rf"(?mi)^\|\s*{re.escape(role)}\s*\|[^|]*\|\s*(\d+)\s*\|", text)
        if not match:
            errors.append(f"cannot read numeric pool size for {role}")
            continue
        size = int(match.group(1))
        if not 1 <= size <= 3:
            errors.append(f"{role} pool size {size} exceeds manager-plus-three cap")

    required_rules = [
        "stall_threshold",
        "scope_policy",
        "gap_scope",
        "final_full_verification",
        "passed registry",
        "merge-then-triage",
    ]
    lowered = text.lower()
    for rule in required_rules:
        if rule.lower() not in lowered:
            errors.append(f"missing required execution rule: {rule}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a generated harness execution plan.")
    parser.add_argument("plan", help="Plan path, or - for stdin")
    args = parser.parse_args()
    try:
        text = sys.stdin.read() if args.plan == "-" else Path(args.plan).read_text(encoding="utf-8")
    except OSError as exc:
        parser.exit(2, f"cannot read plan: {exc}\n")

    errors = validate(text)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("execution plan validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
