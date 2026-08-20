# Logging Repair 010 — impossible deadlines and healthy blocking paths

## Goal

Reject impossible deadline evidence and give a complete, deterministic result for a healthy
on-time blocking manager-response path.

## Required changes

1. **Deadline-origin validation**
   - For `AGENT_SIGNAL_CREATED`, reject each declared `delivery_deadline_utc` or
     `response_deadline_utc` that is earlier than the signal's `source_timestamp_utc`.
   - Preserve UTC parsing and equality behavior.
   - Do not apply this rule to later records that merely carry the original deadline, including
     watcher notifications, manager records, agent receipt/resume, or formal-review records.
   - Canonical ingestion of a historically impossible signal must yield contradiction/
     `INSUFFICIENT_EVIDENCE`, never harness, busy, or idle attribution. It must not crash polling.

2. **On-time blocking completion**
   - When a blocking signal has a canonical successful watcher notification at or before the
     response deadline, a matching manager claim at or before the deadline, and a matching manager
     response at or before the deadline, classify `NO_BLOCKING_IMPACT`.
   - Require exact event correlation and valid manager session/invocation identity.
   - Do not require agent receipt/resume to be before the manager response deadline; retain those
     metrics separately.
   - A late notification keeps harness-delivery precedence. A late/missing claim continues through
     Repair 009 busy/idle/insufficient analysis. Contradictory/impossible source evidence always
     forces insufficient.

3. **Tests**
   - Reproduce the R10 Atlas signal with deadline before creation; source validation rejects it.
   - Feed an equivalent historically canonical impossible signal to analysis; result is
     insufficient with explicit contradiction, not harness delay.
   - R10 Boreal/Delta shape with timely notification/claim/response returns
     `NO_BLOCKING_IMPACT`, even when agent receipt/resume is later.
   - Missing or late notification cannot use the healthy branch.
   - Late claim still follows causal-chain attribution.
   - Watcher-disabled recorder remains a no-op.

4. **Docs/practical**
   - Document deadline-origin rules and healthy blocking precedence.
   - Add both cases to the host practical check.

## Verification

- Full watcher unittest discovery.
- Host practical.
- Compileall.
- Focused Ruff F.
- Focused Pyright.
- Fresh metadata-file readiness with drained cursor proving one healthy blocking event is
  `NO_BLOCKING_IMPACT` and one late formal review remains `BUSY_MANAGER_DELAY`.

## Non-goals

- No bridge implementation.
- No firmware/server changes.
- No silence inference or tolerance/fuzz window.

