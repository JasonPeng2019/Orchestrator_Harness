# Logging Repair Plan 008 — Preserve Response-Deadline Causality

## Problem

The v1 analyzer evaluates a late delivery branch before a late response/claim branch. When both stages are late, the earlier delivery branch masks the manager-attention deadline. If no `HARNESS_EVENT_ACTIONABLE` exists, it also reports zero lateness by subtracting the deadline from itself. In R8 this hid a known 14.6-second late Cygnus claim.

## Accepted design decision

Keep the public `manager-attention-report/v1` shape and existing classification vocabulary. This is a compatible semantic correction, not a new schema. For a blocked signal with an explicit response deadline, diagnose the response/claim stage first **when the canonical watcher timeline proves the signal was available to the manager by that deadline**. If delivery made the signal unavailable until after the response deadline, attribute the miss to `HARNESS_DELIVERY_DELAY`. Never let an earlier-stage delay hide a later manager-attention deadline that can be causally evaluated.

## Implementation

1. Refactor `analyze_event` into small stage helpers or equally clear flat logic so deadline precedence is explicit:
   - nonblocking/no-deadline remains `NO_BLOCKING_IMPACT`;
   - blocked response deadline is evaluated before delivery-only attribution;
   - acknowledgement and formal-review behavior remains intact;
   - delivery-only misses remain `HARNESS_DELIVERY_DELAY`.
2. For a blocked response deadline, use the earliest trusted canonical manager-availability evidence for the exact event (watcher-observed agent signal, harness signal/actionable/pending as applicable).
   - availability after the response deadline => `HARNESS_DELIVERY_DELAY`;
   - availability on time plus late/absent exact claim => classify from complete explicit manager intervals as `BUSY_MANAGER_DELAY`, `IDLE_OR_ABSENT_MANAGER_DELAY`, or `INSUFFICIENT_EVIDENCE`.
   - Do not infer manager state from silence or point events.
3. Compute `deadline_lateness_seconds` from the actual late endpoint used for the classification. It must never be fabricated as `0.0` merely because the eventual actionable endpoint is absent.
4. Preserve the existing host-observed timestamp authority and contradiction checks. Do not substitute producer timestamps for causal ordering. Two-second race tolerance does not extend deadlines.
5. Add focused regression tests for:
   - R8-shaped late delivery plus on-time watcher availability plus late claim and complete busy interval => `BUSY_MANAGER_DELAY` with positive claim lateness;
   - same shape with explicit wait/absence => `IDLE_OR_ABSENT_MANAGER_DELAY`;
   - watcher availability itself after the response deadline => `HARNESS_DELIVERY_DELAY` with positive actual lateness;
   - delivery-only late event retains `HARNESS_DELIVERY_DELAY` and a truthful positive metric;
   - on-time blocked signal does not become a false delay;
   - incomplete manager interval remains `INSUFFICIENT_EVIDENCE`.
6. Update `ATTENTION_LOGGING.md` to require paired wait/tool intervals, or exact `HANDLING_OTHER_EVENT` state with `related_event_id`, for the entire time a known pending event is deferred. State that point records alone do not prove continuous busyness.
7. Add/run a host-only practical fixture reproducing R8's composite late-stage case. No provider, MCP, board, server edits, commit, push, deploy, or flash.

## Verification

- focused unit/regression tests;
- full `harness_watcher_implementation/tests` discovery;
- `compileall`;
- Ruff F checks;
- focused Pyright;
- practical analyzer fixture confirming nonzero lateness and correct causal precedence;
- independent read-only review before accepting the repair.

## Sprint consequence

R8 is rejected and the counter is `0/3`. After Repair 008 passes readiness, begin a fresh epoch with a fresh manager invocation. Do not reuse R8 authority, PIDs, or counted evidence.

## Amendment 008-A — Prove notification, not mere observation

Independent review found that canonical source/harness observation does not prove the persistent root could see the event. This finding is accepted as code-breaking for the experiment's causal verdict.

- Add a validated exact-event durable successful-notification boundary for `collaboration.send_message` (additive within v1), with enforced producer-role provenance, `wake_transport`, and success metadata.
- Exact-event `MANAGER_WAIT_FINISHED` with the matching source record and wake transport may corroborate receipt for the required wait challenge.
- Manager availability must not derive from `AGENT_SIGNAL_CREATED`, `HARNESS_SIGNAL_OBSERVED`, actionable, or pending observation alone.
- Timely observation but late successful notification is delivery delay; missing/failed notification is insufficient; only timely proven notification/receipt may lead to busy/idle manager attribution.
- Add focused regressions and update the watcher operating documentation so every successful mailbox forward is durably recorded after the send returns.

- Amendment audit clarification: every response-deadline path, including the legacy HARNESS_EVENT_PENDING fallback, requires timely proven WATCHER_NOTIFICATION_SENT availability before BUSY/IDLE attribution; otherwise it is INSUFFICIENT_EVIDENCE.

