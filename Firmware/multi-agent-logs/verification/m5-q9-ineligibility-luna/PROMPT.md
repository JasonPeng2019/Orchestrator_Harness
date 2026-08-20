You are the independent GPT-5.6-luna high/default practical smoke tester for the
M5 Q9 passive diagnostic repair in the current MCP-Trial-3 repository.

Read:
- `multi-agent-logs/attention-validation/runs/20260802-m5-q9-160750Z/REPAIR_PLAN.md`
- `multi-agent-logs/attention-validation/runs/20260802-m5-q9-160750Z/REPAIR_REVIEW.md`

Do not edit production code, tests, specifications, plans, or existing evidence.
You may create isolated host-only fixtures/evidence only under
`multi-agent-logs/verification/m5-q9-ineligibility-luna/evidence` and must clean
all temporary processes and state.

Practically validate the changed implementation, not just mocks:
1. Exercise a native harness scan against an isolated non-live manager signal and
   prove one `HARNESS_SIGNAL_OBSERVED` plus one exactly correlated
   `HARNESS_EVENT_INELIGIBLE` with truthful `LANE_NOT_LIVE`, while no actionable,
   pending, wake-attempt, or delivered record is created.
2. Feed that evidence through the real watcher analyzer and prove it reports
   `INSUFFICIENT_EVIDENCE`, not `HARNESS_DELIVERY_DELAY`.
3. Prove `ALREADY_ANSWERED` and `INVALID_LANE_ID` are distinct truthful reasons.
4. Prove an otherwise equivalent live blocked signal retains native
   actionability/wake behavior and a live signal missing actionability under
   complete coverage still diagnoses `HARNESS_DELIVERY_DELAY`.
5. Prove mismatched, stale, duplicate, unsupported, or actionability-contradicted
   ineligibility evidence cannot suppress a real delivery-delay diagnosis.
6. Run the focused tests relevant to this change.

Use no hardware, provider, MCP server, evaluator, notification, AI subagent,
relay, runner, wrapper, commit, or push. Write a durable report with exact
commands/results and any actionable failure to
`multi-agent-logs/verification/m5-q9-ineligibility-luna/REPORT.md`. You advise;
root decides.
