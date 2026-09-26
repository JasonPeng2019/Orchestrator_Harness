# STEP-12-2 — Compose the installed worker workspace

> **Time-crunch MVP acceptance:** Execute this step with [NORMAL_OPERATION_ACCEPTANCE.md](../../NORMAL_OPERATION_ACCEPTANCE.md). Return work for repair only for a reproduced defect in desired normal supported behavior, credible regular recovery or compatibility, or a critical invariant. Record every other confirmed edge, theoretical, unsupported, or non-normal issue in [KNOWN_ISSUES.md](../../KNOWN_ISSUES.md) without a correction or re-review gate.

This step is a derivative of [original STEP-12](../../source-steps/STEP-12-workspace-composition-is-ready.md).

Owner: lane 2. This is the complete installed-workspace composition assignment.

Extend the existing `harness/orchestrator_harness/setup.py` `run_setup` entrypoint and its planning, preflight, staged replacement, and installed-binding validation; do not create a second installer.

Extend the existing setup.py planning, preflight, staged replacement, and installed binding validation. Compose product-harness lifecycle files, ROOT-suite tools, and repository instructions in the same installed payload that the launcher actually consumes. Detect command/provider collisions and later overwrite before enhanced dispatch. Repeat setup idempotently and repair interrupted owned stages without erasing unrelated workspace content. Preserve the two pre-existing setup-installed hook edits on product main.

Evidence: focused setup-monitor and installed-payload tests for ownership collision, both behavior families, repeat, overwrite, and interrupted repair. The checkpoint verifies the STEP-07 launched payload after lane 1/2 combination.

Resolve exact source and destination ownership before mutation and reject unknown command/provider collisions. Compose the harness lifecycle, ROOT-suite tools, and repository instructions deterministically in staging; validate the same installed payload path the launcher consumes, not only source templates. Commit through a recoverable boundary that preserves the previous valid installation on failure. A repeat of the correct payload is idempotent; an interrupted compose or later upstream overwrite must be detectable and repairable before enhanced dispatch. Never erase unrelated workspace files or the pre-existing setup-installed hook edits. Run affected `harness/orchestrator_harness/tests/test_setup_monitor.py` cases and focused installed-payload collision/overwrite/interruption tests. Unknown ownership or incomplete compose blocks only enhanced dispatch; repair the exact owned target.

After a preflight or staged-commit repair, rerun its direct setup checks. Rerun STEP-13 network enforcement and STEP-15 readiness consumers only if the installed payload changed; otherwise preserve their valid evidence.
