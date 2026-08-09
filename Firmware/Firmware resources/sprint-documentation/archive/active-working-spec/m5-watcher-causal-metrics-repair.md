# M5 focused repair plan — watcher causal metrics

## Verified defect

M5 attempt `20260802-m5-s1-052110Z` preserved complete raw wake chains, but the diagnostic
watcher's final report calculated several causal durations from watcher ingestion time. Records
from different sources can be ingested in a different order from the events they describe. The
report therefore emitted impossible negative values, including Cygnus
`signal_to_observation_seconds = -14.808474`, while reporting no contradiction.

This is a diagnostic-reporting defect. It invalidates the sprint under the M5 rules, but it is not
evidence that the production harness failed to deliver a wake.

## Smallest implementation

1. In `harness_watcher_implementation/attention.py`, calculate reported causal stage durations
   from each canonical record's `source_timestamp_utc`, not `observed_timestamp_utc`.
   Host-observed timestamps remain unchanged for ingestion coverage and existing deadline/
   availability decisions; this repair must not broaden into a correlation redesign.
2. Treat any negative causal duration as contradictory evidence. Name the affected metric in the
   contradiction and leave the event `INSUFFICIENT_EVIDENCE`; never silently clamp, take an
   absolute value, or call an impossible ordering complete.
3. Add focused regression tests proving:
   - records ingested out of order but carrying correctly ordered source timestamps produce the
     correct non-negative causal metrics; and
   - genuinely inverted source timestamps produce a named contradiction and an
     `INSUFFICIENT_EVIDENCE` classification.
4. Do not change wake selection, transport, acknowledgements, evaluator behavior, manager
   classification policy, or any runtime topology.

## Root procedure corrections for the next sprint (no production-code change)

- Require every worker request to use the schema's exact populated `deadline_utc` field, in
  addition to the worker attention record's `response_deadline_utc`.
- Record `MANAGER_WAIT_FINISHED` for every wait outcome, including `WATCH_TIMEOUT`.
- Emit `MANAGER_INVOCATION_FINISHED` before final drain and watcher shutdown.
- Complete the last native watcher poll/drain and exact cleanup before launching the reviewer.

## Verification and authority

The persistent Terra coder implements only the accepted change. An independent Terra reviewer
advises after implementation; the root accepts or rejects every finding. Luna performs the
smallest host-only practical smoke. Then run the affected watcher suite, harness suite, compile/
type checks, and M4 readiness required by the active M5 spec. A green repair refreezes the tested
surface and restarts the M5 accepted count at 0/3. No commit, push, runner, wrapper, relay, or
mid-sprint repair is authorized.
