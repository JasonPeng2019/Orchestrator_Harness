# M5 native harness delivery-deadline repair

Date: `2026-08-02`  
Root verdict: **REPAIRED AND READY FOR A NEW M5 COMPARABLE SET**

## Verified defect and repair

Sprint `20260802-m5-s3-101953Z` proved that the native harness could observe a blocked HELP signal
before its delivery deadline yet deliver it late while root was already waiting. Reconciliation
discarded the source signal's `delivery_deadline_utc`, `agent_blocked`, and `attention_epoch_id`, so
routine `STALE_STATUS` work outranked it.

The focused repair now:

- validates those optional fields fail-closed at signal discovery;
- preserves them through reconciliation;
- retains delivery and response deadlines separately in attention evidence;
- uses delivery time for pending delivery-by metadata and deferred ordering; and
- ranks only a blocked HELP signal with a valid delivery deadline ahead of routine stale status.

No wrapper, runner, relay, retry controller, scheduler, watcher change, or assistance layer was
added.

## Required repair loop

- Persistent Terra-medium coder: `/root/m5_deadline_coder`.
- Independent Terra-medium reviewer: `/root/m5_deadline_review`.
- Reviewer found no code defect. Root found one stale README contract statement; the same coder
  corrected it. The reviewer then found one inaccurate phrase about ordinary `deadline_utc`; root
  accepted it, the coder corrected it, and the reviewer confirmed resolution.
- No accepted finding remains.

Focused coder checks: 44 tests passed; compileall passed. Independent reviewer checks: focused 117
tests plus 13 subtests passed; full harness 200 tests, 1 skipped, plus 13 subtests passed. Root's
full harness discovery ran 201 tests, 1 skipped, and passed.

## Luna practical smoke

External GPT-5.6-luna, high reasoning, default tier exercised the real native managed harness and
native blocking wait. A blocked HELP with a delivery deadline competed with routine stale status
and was returned first with delivery metadata present in every captured attention stage. The
nonblocking control correctly did not outrank stale status. Result: **PASS, 5/5 controls**.

Evidence: `m5-deadline-repair-luna-smoke.md`, `m5-deadline-repair-luna.jsonl`, and
`m5-deadline-repair-luna-last-message.md`.

## Root disposition

The repair is accepted. S3 remains `HARNESS_BUG`, `WATCHER_PASS`, and
`MANAGER_EVIDENCE_SUFFICIENT`; it does not count. Because native harness behavior changed, S1a is
historical pre-repair evidence and the comparable count resets to `0/3`.

The completed repair plan is archived at
`archive docs/active-working-spec/m5-harness-deadline-repair.md`.
