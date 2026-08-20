# M5 Q8 sprint checkpoint

Q8 is fully stopped, drained, reviewed, and non-qualifying.

- Gates: `HARNESS_PASS`; `WATCHER_BUG`; `MANAGER_EVIDENCE_INSUFFICIENT`.
- Attempt budget: 8/10 used; attempts 9-10 remain; attempt 11 is forbidden.
- Comparable count: 0/3.
- Four genuine requests completed with native wake, response, acknowledgement, receipt, and resume.
- No observable idle-manager inattention: delivery-to-receipt about 2.4-2.7 s; receipt-to-claim
  about 0.6 s.
- Verified gap: no durable final-signal-publication timestamp, so watcher could not distinguish
  worker publication delay from harness detection delay for Atlas/Boreal.
- Finalizer PASS (183 records); exact 10/10 cleanup; resources empty.
- Repair plan: `REPAIR_PLAN.md`; implement/review/smoke/M4/refreeze before attempt 9.

The relevant repair leaves only two attempts, so 3/3 cannot be reached inside the current hard
budget. Continue through attempt 10 only as authorized and report the bounded result.
