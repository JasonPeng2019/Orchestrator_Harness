# STEP-12 - Workspace composition preserves both owners

## Outcome

Setup installs an isolated product-harness/ROOT-suite payload that preserves both behavior families and repository instructions, detects collision or overwrite, and can recover without touching unrelated work. This is the composition part of [BEHAVIOR-06](../specification/behaviors/BEHAVIOR-06-setup-and-readiness-preserve-ownership.md).

## Scope and touchpoints

Extend existing `harness/orchestrator_harness/setup.py` planning, preflight, staged replacement, installed binding validation, and `run_setup`. Inspect the actual launched worker payload and current `tests/test_setup_monitor.py`; do not replace setup or create a second installer. Preserve the two existing setup-installed tracked hook edits on product `main`.

## Implementation

Resolve exact source and destination ownership before mutation, rejecting unknown command/provider collisions. Compose harness lifecycle, ROOT-suite tools, and repository instructions deterministically in staging; validate the installed and launched payload, not source files alone. Commit through a recoverable boundary. A repeat with the same correct payload is idempotent; an interrupted compose or later upstream overwrite becomes detectable and repairable before enhanced dispatch. Never erase unrelated files to manufacture a clean workspace.

## Dependencies and integration

Consumes existing setup and STEP-07's actual launch payload requirements. Produces composition state for STEP-13 network enforcement, STEP-15 readiness, and STEP-18 native launch. Domain preparation remains in `memory_harness`.

## Requirement-fit validation

Prove pre-mutation ownership collision, both behavior families in the launched payload, repeat idempotence, overwrite detection, and bounded repair of an interrupted stage.

### Fast test suite

Run affected `harness/orchestrator_harness/tests/test_setup_monitor.py` cases and add a focused installed-payload collision/overwrite test if needed. The test must inspect the same payload path the launcher consumes; source-template inspection alone is insufficient.

## Failure scope and recovery

Unknown ownership or incomplete compose blocks enhanced dispatch only. Preserve previous valid installed state and unrelated workspace files; repair the exact owned target.

### Fast lane for revisiting old work

Re-enter setup preflight or staged commit, rerun its direct tests and STEP-13/15 consumers only if the installed payload changed.
