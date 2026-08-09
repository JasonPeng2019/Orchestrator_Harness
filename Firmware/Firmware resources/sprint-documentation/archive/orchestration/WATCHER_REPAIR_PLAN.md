# Optional watcher feedback-loop repair plan

Created: `2026-07-31T14:26Z`  
Owner: main orchestrator  
Sprint: `20260731-long-canary-sprint-1`

## Verified defect

The optional Harness Watcher observes the primary harness event stream. Its own unresolved
`HARNESS_WATCHER_ALERT` is mirrored into that same stream. The poller then sends the mirrored alert
back to the Terra evaluator as if it were a new primary observation. Model paraphrase and a new
wrapper offset evade exact `{kind, summary, evidence}` deduplication, producing a self-amplifying
series of alerts.

The persistent Terra-medium auditor mapped:

- `hwa-37b43d38527940c01c4ae68b` to the original transient `STALE_STATUS`;
- `hwa-7d76455d39d6da942a78a1c6` to the first mirrored watcher alert;
- `hwa-5b135c0240a6df0efc5d7a1b` to the second mirrored watcher alert; and
- `hwa-e6...` to the third mirrored watcher alert.

The primary harness transition itself is correct and requires no repair. The optional watcher
feedback loop is a functional defect and Sprint 1 cannot count.

## Accepted design decision

Filter watcher-derived records from evaluator-visible harness deltas when either:

1. `type == "HARNESS_WATCHER_ALERT"`; or
2. `identity` begins with `"harness-watcher:"`.

The source reader must still advance and persist its raw byte cursor over filtered records. If a
changed delta contains only watcher-derived records, do not invoke the evaluator. If the delta mixes
derived and genuine records, pass only the genuine records to the evaluator.

Keep raw logging, primary-harness integration, manager delivery, alert durability, and cursor
semantics unchanged. Do not modify primary reconciliation, controller behavior, lane state, hardware
work, evaluator scope policy, or broad alert signature semantics.

## Implementation slices

1. Add a small provenance predicate/filter at the packet-construction boundary in
   `harness_watcher_implementation`.
2. Apply it only to evaluator-visible records while preserving raw cursor advancement.
3. Add focused regressions:
   - a mirrored watcher alert alone does not call the evaluator and does not create another alert;
   - a mixed delta removes the derived alert but retains and evaluates the neighboring genuine
     harness record.
4. Run the focused watcher tests, compile check, then the ordinary watcher/harness host suites.
5. Main orchestrator reviews the diff and evidence. Restart one optional watcher against the same
   active epoch, resolve/acknowledge the false historical alerts through the manager path, and verify
   at least one real poll remains silent for healthy work.

## Completion

The repair is accepted only if focused regressions and ordinary host suites pass, the active watcher
does not re-alert on its own mirrored records, current HIL lanes remain preserved, and no unrelated
experiment or passed test is restarted.

