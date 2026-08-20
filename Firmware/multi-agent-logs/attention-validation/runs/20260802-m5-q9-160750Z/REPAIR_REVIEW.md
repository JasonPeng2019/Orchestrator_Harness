# Q9 Independent Repair Review

**Verdict: CHANGES ADVISED** (advisory; root adjudicates)

## Scope reviewed

- `REPAIR_PLAN.md`
- `orchestrator_harness/notifications.py` and `cli.py`
- `harness_watcher_implementation/attention.py`
- Q9-focused harness and watcher tests
- Design charter (`always-keep-in-mind`), especially honest reporting / no fabrication.

## Finding 1 — already-answered is falsely reported as `LANE_NOT_LIVE` (changes advised)

`_manager_signal_ineligibility_reason()` returns `LANE_NOT_LIVE` immediately when
`correlated_request_answered is True` (`orchestrator_harness/notifications.py:73-74`).
That fact means the correlated request was answered; it neither establishes that
the lane is non-live nor says that no helper/request is live.  The existing test
already constructs this exact shape with a `RUNNING_CODEX` lane
(`test_manager_notifications.py:654-676`).

The watcher then repeats the false attribution in its missing-evidence text
(`attention.py:667`), and accepts only `LANE_NOT_LIVE` (`attention.py:631`).
Thus an already-answered signal becomes "lane not live" in canonical evidence
and in the diagnosis. This conflicts with the required truthful attribution and
the charter's no-fabrication rule.

**Recommended repair:** add a distinct bounded canonical reason such as
`CORRELATED_REQUEST_ANSWERED`; emit it for this branch; accept it under the
same exact-correlated, ordered, single-record, no-actionable guard; and report
that exact reason. Preserve the native no-wake decision.

## Finding 2 — absent/malformed lane ID is also named `LANE_NOT_LIVE` (changes advised)

The next branch (`notifications.py:75-77`) maps a missing or non-string `lane_id`
to `LANE_NOT_LIVE`. A lane identity that cannot be determined is not proof that
a lane was checked and found non-live. This is another false attribution,
though separate from the already-answered case.

**Recommended repair:** either use a truthful bounded reason such as
`LANE_ID_MISSING` / `SIGNAL_UNCORRELATABLE`, or do not issue ineligibility
explanation for that malformed signal. If such a reason is accepted by the
watcher, retain the plan's exact-correlation/order/uniqueness/actionability
conditions and classify it `INSUFFICIENT_EVIDENCE`, never a harness defect.

## Correlation, ordering, duplication, and behavioral review

- The new record is emitted after `HARNESS_SIGNAL_OBSERVED` in the same native
  scan loop and is passive; it does not alter selection, deferred work, or wake
  delivery.
- Watcher acceptance requires exactly one ineligibility record, exact
  `harness_event_id`, harness provenance, timestamp no earlier than observation,
  and no actionable record. Unsupported, mismatched, stale, duplicate, or
  contradicted evidence therefore does **not** suppress a delivery-delay result.
- The ineligibility branch currently only covers `LANE_NOT_LIVE`; this is why
  the truthful additional reasons above need corresponding analyzer support and
  adversarial tests.
- A `HARNESS_EVENT_ACTIONABLE` rejection is event-id scoped rather than also
  `harness_event_id` scoped. This is conservative (it prevents suppression),
  not a false harness attribution, but an exact-ID regression test would make
  the intended correlation boundary explicit.

## Test sufficiency

Focused test run:

```text
python -m pytest orchestrator_harness/tests/test_manager_notifications.py \
  harness_watcher_implementation/tests/test_attention.py -q
63 passed, 11 subtests passed
```

The tests cover non-live, wrong ID/reason/order, duplicate evidence, and later
actionability. They do **not** test the already-answered branch's emitted reason
or watcher analysis, despite an existing selection test exercising the input.
Before treating Q9 as ready, add tests for:

1. answered + live lane emits and reports `CORRELATED_REQUEST_ANSWERED`, and
   reaches `INSUFFICIENT_EVIDENCE` rather than `HARNESS_DELIVERY_DELAY`;
2. missing/invalid lane ID is truthfully represented or remains un-explained;
3. wrong, stale, duplicate, contradictory, and post-ineligibility actionable
   evidence for each newly accepted reason still leaves the delivery-delay
   classification unsuppressed.

## Re-review

**Final verdict: PASS** (advisory; root adjudicates)

The accepted correction resolves the prior false attribution without changing the
native selection outcome:

- `ALREADY_ANSWERED` is emitted solely from the verified
  `correlated_request_answered is True` fact; it no longer claims the lane is
  dead, including when the lane is live.
- `INVALID_LANE_ID` is emitted solely when `lane_id` is missing, empty, or not a
  string; it honestly reports an uncorrelatable lane rather than inventing a
  liveness result.
- `LANE_NOT_LIVE` remains the residual result only after the supplied valid lane
  has no current active lane, actionable request, running helper, or running
  MCP under the unchanged native liveness decision.

The three values are bounded by `INELIGIBILITY_REASONS`. The analyzer accepts
one only when it is canonical harness evidence for the same attention event,
with the exact observed `harness_event_id`, at-or-after observation, with no
`HARNESS_EVENT_ACTIONABLE` evidence. Unsupported, mismatched, stale, duplicate,
or contradicted records are not accepted and therefore cannot suppress a
`HARNESS_DELIVERY_DELAY`. The implementation only changed reason text returned
for existing non-live/invalid/answered outcomes; selection still treats every
non-`None` result as ineligible.

Focused verification passed:

```text
python -m pytest orchestrator_harness/tests/test_manager_notifications.py \
  harness_watcher_implementation/tests/test_attention.py -q
64 passed, 11 subtests passed
```

The added focused tests cover each reason's truthful source condition and each
reason's exact-evidence fail-closed watcher result, alongside wrong-ID, stale,
unsupported, duplicate, and actionable counterexamples. No remaining changes
advised for this Q9 correction.
