# Adversarial review — Clean-O optional-watcher repair plan

**Verdict: PASS**

The proposed repair is a proportionate response to the validated Clean-O defect.

- A durable one-poll quarantine keyed by the exact primary condition identity covers the observed
  cross-poll stale → `CONTROLLER_EXITED` transition without blanket suppression. It preserves a
  genuinely sustained stale condition by releasing it after one configured interval, exactly once.
- Required recovery matching is exact: only the same identity's active/exited or stale-clearing
  record resolves quarantine. Unrelated records cannot hide a real defect.
- Persisting first-seen time, source evidence tuple, and raw stale record in the cursor is the
  minimum correct restart contract. Legacy cursor readability, one-time release, and strict
  path/SHA/offset evidence validation are explicitly tested.
- The plan leaves primary-harness fail-closed stale detection untouched and preserves alert
  deduplication, raw logs, recursive-input filtering, and all non-stale defect categories.
- The manager remedy is appropriately operational, not a speculative primary-harness change:
  an independent wall-clock review deadline requires a written whole-suite review before ordinary
  draining continues and blocks new authority until it is complete. Canonical acknowledgement and
  baseline verification still occur when the due event is pending.

Implementation review must verify release itself marks the packet evaluable even when no new log
bytes arrive; this is inherent in the specified “release exactly once” test and is not an open
design gap. No hardware/model/live endpoint work is warranted for this repair.
