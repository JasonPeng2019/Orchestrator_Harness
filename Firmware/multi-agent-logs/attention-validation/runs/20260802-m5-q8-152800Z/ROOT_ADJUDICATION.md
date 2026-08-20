# Q8 root adjudication

- Attempt 8/10
- `HARNESS_PASS`
- `WATCHER_BUG`
- `MANAGER_EVIDENCE_INSUFFICIENT`
- Non-qualifying; comparable count remains 0/3.

Root accepts the reviewer's narrow diagnostic finding. All four real signals completed native
wake, root receipt/claim, response, acknowledgement, worker receipt, and resume. No request shows
otherwise-idle manager inattention: native delivery to root receipt was about 2.4-2.7 seconds and
receipt to claim about 0.6 seconds. The harness had no crash, loss, stale identity, queue corruption,
or transport failure.

However, the new safe publisher order records `AGENT_SIGNAL_CREATED` before final JSON exposure.
Atlas and Boreal then spent material unmeasured time before the final rename. The watcher labeled
the resulting deadline misses `HARNESS_DELIVERY_DELAY`, even though it has no timestamp proving
when the harness could first see the final signal. This is a verified watcher/logging causal gap,
not proof of a harness defect or manager inattention.

The overwritten Boreal convenience files were moved to unique checkpoint names and reconstructed
from immutable canonical producer record IDs. Canonical producer/timeline evidence was never
changed. This operator file-naming mistake does not own the accepted diagnostic gap.
