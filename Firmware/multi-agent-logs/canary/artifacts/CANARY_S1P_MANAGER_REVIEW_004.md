# Clean-P manager formal review 004

- written_utc: `2026-08-01T00:19:23.798804+00:00`
- review_baseline_before: `2026-08-01T00:14:34.988065Z`
- due basis: Atlas is finalizing its failed one-lifetime checkpoint while Boreal is the only live provider-enumeration window
- higher-priority preemption: Boreal published a fresh lifetime plus an exact setup-plan request; the request was reviewed before any relay
- authority decision: Boreal retains the only live provider/hardware authority; Cygnus and Delta releases remain absent

## Whole-suite inspection

- Atlas/A22's one P lifetime ended before setup because its run-local parser rejected plain-text `initialization_handshake` guidance. Exact P-owned provider/helper processes are absent; no setup, manager relay, board action, B14, or B34 action occurred. Its Luna session is writing the truthful checkpoint and must not retry in P.
- Boreal/D31 has one live P controller/session and one exact P provider lifetime on STM-B. Its first public artifact and provider identities are fresh and exact. No Cygnus or Delta provider release has been issued.
- Boreal's request is not approvable: its copied Clean-M helper emits Clean-M phase/launcher/artifact labels inside the P runtime, and its populated `board_setup-plan` arguments omit the currently required `expected_fail_return` and `expected_success_return` fields while also supplying NULL setup facts. The manager therefore rejects the request without a hardware call. This is a run-local controller defect, not a production-server defect.
- The primary harness truthfully surfaced the Atlas/Boreal transitions, Boreal's lifetime, the request-associated signals, and the formal review due event. No harness or watcher repair decision is made inside this sprint.

## Manager judgment

- Reject Boreal's exact request and let its single P lifetime checkpoint without retry. Do not manufacture a corrected live plan inside this already-invalid lifetime.
- Once Boreal's exact provider descendants are absent, release the next serialized provider enumeration window. Unrelated disjoint-board work may overlap only after that serialization gate.
- Preserve all P evidence for independent audit. Clean-P is already a noncounting candidate because of run-local execution faults; only the independent sprint auditor decides the final classification.
