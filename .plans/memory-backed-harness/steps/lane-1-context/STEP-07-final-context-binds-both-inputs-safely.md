# STEP-07 - Final context binds both inputs safely

## Outcome

Lane 1 finalizes STEP-06's accepted Standard preparation into one durable
context/envelope bound to the exact task, plan, decision, base, checkpoint,
execution role, invocation target, and recipient. Both trusted source IDs,
digests, and unique markers reach worker-bound optional content; secrets and raw
approval/control records do not.

## Scope and touchpoints

Continue in `tests/local/mvp/test_coherent_memory_path.py`. Own
`src/memory_harness/context.py`, `runtime.py`, `contracts.py`, or `store.py` only
if the focused test reproduces a normal-path provider defect. Do not edit the
product harness; STEP-09 consumes this exact envelope contract.

## Implementation

Construct an accepted plan that explicitly depends on both selected revisions,
then call the existing finalization path with all actual destination fields.
Exercise the final live/source recheck for both inputs before persistence.
Read the context back by product API and validate the envelope against the exact
dispatch target. Assert optional content and delivery trace carry both source
identities/digests/markers and `plan_affecting` provenance. Inspect the complete
serialized context/envelope and require credentials, raw approval evidence, and
control-plane fields to be absent. A revoked or changed source at final recheck
must block rather than silently omit plan-dependent guidance.

## Dependencies and integration

Consumes STEP-06. Produces the canonical enhanced envelope/context shape that
STEP-09 must hand to the product worker and STEP-12 must test after integration.
Lane 2 must not invent a second representation of selected memory.

## Requirement-fit validation

The context must be durable, exact-target-valid, privacy-safe, and contain both
material-use markers. Any copied base/task/recipient or stale plan-dependent
source must fail before dispatch/persistence claims success.

**Time-crunch repair gate:** repair only a reproduced defect in this normal safe
finalization/dispatch contract or a critical privacy, identity, trust, or
durability invariant. Document edge malformed records, unsupported targets, and
theoretical races without correction, blocking, or re-review.

### Fast test suite

Run `CoherentFinalContextTests` from
`tests/local/mvp/test_coherent_memory_path.py`. If product context/runtime code
changes, also run `tests.local.preparation.test_final_context_dispatch`; select
the directly affected class/methods first and run the module only when shared
logic changed. The decisive assertions are durable exact binding, two markers,
and absence of prohibited fields.

## Failure scope and recovery

A final recheck failure invalidates only the changed source and the combined
context/native consumers. Return to its provider step if the candidate changed;
return here if binding/packing is wrong. Do not accept a one-source fallback for
this enhanced campaign.

### Fast lane for revisiting old work

Preserve STEP-06 and the unaffected source evidence, repair the exact
finalization/privacy seam, rerun this focused class, then STEP-09/12 consumers.
