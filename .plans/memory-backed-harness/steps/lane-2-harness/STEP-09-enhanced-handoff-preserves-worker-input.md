# STEP-09 - Enhanced handoff preserves worker input

## Outcome

Lane 2 proves the product harness's existing handoff, worker-input construction,
and result-capture seam preserves an enhanced context containing both memory
inputs. It uses a locally constructed fixture conforming to the frozen `4263abf`
schema and a deterministic in-process worker boundary; STEP-14 alone performs
the actual native launch and proves real material use.

## Scope and touchpoints

Own `harness/orchestrator_harness/memory_handoff.py`, `bootstrap.py`,
`launch.py`, `controller.py`, their focused tests, and
`src/memory_harness/harness_child.py`/`harness_bridge.py` only if those accepted
bridges are actually involved. Lane 1 owns context shape; Lane 2 owns its native
consumption. Do not wire provider search into the worker process or invent a
second context format.

## Implementation

Build the focused handoff test against the accepted final-context/envelope schema
already frozen at `4263abf`, using the same two-source fixture shape STEP-07 is
required to preserve. Exercise the real product functions that validate the
handoff, construct the worker prompt/structured input, and capture a result, but
inject the repository's focused deterministic worker boundary instead of starting
a native process. Ensure the resulting worker input includes the safe
optional contents/delivery trace already persisted in the final context,
including both IDs/digests/markers, while keeping control credentials absent.
Validate exact task/plan/decision/base/run/recipient before spawn and retain the
existing one-intent/one-observation dispatch fencing. Have the deterministic
worker return marker-derived structured fields and assert result capture preserves
them. Define the later STEP-14 campaign task separately so the real worker must
echo or act on both markers. Do not add a generic campaign runner, launch a native
worker in this step, or use outer-worker narrative as proof.

## Dependencies and integration

Consumes the frozen canonical envelope contract at `4263abf`; Lane 2 may finish
and review independently of Lane 1. STEP-12 compares its fixture with STEP-07's
actual output and reruns this focused selector only if STEP-07 repaired the shared
shape for a reproduced defect. Produces the enhanced launch/material-use seam
consumed by STEP-10, STEP-12, and the actual STEP-14 campaign.

## Requirement-fit validation

The focused test must fail if either selected item is omitted, identities change,
the context is copied to another target, prohibited data reaches the worker, or
the deterministic result-capture seam drops either marker. It proves transport
and validation only; STEP-14 must still establish actual native material use.

**Time-crunch repair gate:** repair only a reproduced defect in this normal
enhanced launch/material-use path or a critical privacy, identity, duplicate
dispatch, or trust invariant. Document non-normal prompt formatting, unsupported
worker tiers, and theoretical recovery edges without correction or re-review.

### Fast test suite

Add the focused enhanced-memory worker handoff test beside
`orchestrator_harness.tests.test_memory_handoff`. Run that test plus the directly
affected existing exact-target and duplicate-dispatch tests. If controller/launch
prompt code changes, run its narrow existing test module. No native process is
started here; STEP-14 remains the decisive real native proof.

## Failure scope and recovery

If STEP-07 actually changes the frozen shape, hold only STEP-09–11 integration
and redo the focused handoff test. A deterministic boundary failure holds the
handoff/result contract only; native launch ownership does not exist in this step.

### Fast lane for revisiting old work

Keep the accepted final context and any passing pre-spawn validation, repair the
first native-consumption boundary, rerun the focused handoff/dispatch tests, then
STEP-10 and the invalidated STEP-14 observation.
