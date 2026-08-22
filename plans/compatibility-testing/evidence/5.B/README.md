# Evidence 5.B — Phase 5 residual event-emission (producer-seam)

**Date:** 2026-08-20 · **Disposition:** `TESTED-PASSED (5.B, producer-seam)` for G8, G9, G11, G12, G13, G15, G16.

## What this closes

The 7 rows phases 0–4 missed — the sole NOT-TESTED rows that were neither PA nor
OOS. Their classifiers passed in phase 1; their **producers** had never been
driven end-to-end. Phase 5's decision gate (see
`../../phase-5-residual-live-event-emission.md` §5.0) preferred a live **5.A**
pass, but the weak Ollama backend cannot sustain the multi-lane / relay /
subordinate-process / harness-lifecycle states those producers require within the
time box. So all 7 were closed via the **5.B producer-seam** path: the real
producer call sites are invoked in-process and asserted to emit the correct event
kinds. This is **explicitly weaker than a live 5.A pass** and is never presented
as live.

## Producers driven (not the classifier)

| Row | Producer exercised | Event kinds asserted |
|---|---|---|
| G8  | `orchestrator_harness.events.conditions_from_snapshot` | HELPER_EXITED, HELPER_STATE_UNKNOWN (MCP_* OOS) |
| G9  | `conditions_from_snapshot` | PROVIDER_WAIT, LANE_STATE_UNKNOWN |
| G11 | `conditions_from_snapshot` | CONTROLLER_ACTIVE, LANE_WAITING_RESOURCE, LANE_WAITING_RELAY, RESULT_ACCEPTANCE_PENDING, RESOURCE_RELEASE_POSSIBLE, REQUEST_STALE |
| G12 | `models.RequestFacts.operator_summary` → `conditions_from_snapshot` | RELAYED, RELAYED_INACTIVE, RELAYED_AMBIGUOUS |
| G13 | `conditions_from_snapshot` + `events.diff_conditions` | HELPER_ACTIVE, CONDITION_CLEARED (MCP_ACTIVE OOS) |
| G15 | `harness_watcher_implementation.attention.make_source_record` | HARNESS_SIGNAL_OBSERVED, HARNESS_EVENT_INELIGIBLE/_ACTIONABLE/_PENDING/_DEFERRED |
| G16 | `attention.make_source_record` | HARNESS_ACK_ATTEMPTED, HARNESS_ACK_SUCCEEDED |

## Test + transcript

- Test module: `orchestrator_harness/tests/test_compat_live_emission.py` (in the
  `harness-single-worktrees/compat-test` clone — uncommitted, like the phase-0
  fixes; the authoritative target does not yet carry this test).
- Transcript: `pytest-producer-seam.txt` (7 passed).

## Honesty caveats

- **Not live.** No `claude`/Ollama subprocess ran. These prove the
  producer→event wiring, not that a live lane reaches the state.
- **MCP_* variants** of G8/G13 remain OOS per the standing MCP exclusion.
- Any future live 5.A run may upgrade these rows from `(5.B, producer-seam)` to a
  plain live pass; until then they carry the weaker tag.
