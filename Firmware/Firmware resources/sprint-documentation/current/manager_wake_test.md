# Manager-Wake Test - Evidence Standard

## Purpose

Determine whether real worker delays are caused by the native harness, an idle/inattentive
persistent manager, or a manager that is genuinely busy. The active procedure is
`active-working-spec/m5-three-sprint-wake-test.md`; this document is the compact rationale and
acceptance reference.

## What success means

Success is **3/3 clean comparable E2E orchestration sprints that each pass three independent
gates**. It is not three perfectly executed sprints.

The 90-second request window is a target, not an automatic failure. A longer request remains valid
when complete records show the persistent manager was genuinely busy or handling an earlier real
request. Late harness observation, native-wait delay, idle-manager delay, and unknown or incomplete
activity are not excused.

### Gate 1 — harness

Record `HARNESS_PASS` only when the native harness correctly observes, selects, wakes, returns,
correlates, and acknowledges genuine work without a verified in-scope functional defect.

### Gate 2 — deterministic watcher

Record `WATCHER_PASS` only when the watcher provides uninterrupted diagnostic-only coverage and
correct correlation, timing, and reporting without a verified in-scope defect.

### Gate 3 — manager architecture evidence

Record `MANAGER_EVIDENCE_SUFFICIENT` only when the run can distinguish healthy operation, harness
delay, otherwise-idle manager inattention, busy-manager contention, and downstream response
failure.

A sprint counts only when all three results are present. “Bug-free” means no observed or verified
in-scope harness/watcher defect during the sprint, not a claim of absolute software perfection.

Each sufficient sprint must provide at least three classifiable genuine requests from at least
three external worker lanes. Across the three-run set, the evidence must cover both a manager that
is blocked/waiting and a manager doing genuine bounded work.

## Minimum causal chain

For each counted request, reconstruct:

1. worker created the request;
2. worker atomically published the final request, with exact captured publication time;
3. harness detected it;
4. wake was attempted;
5. wake was delivered or explicitly failed;
6. manager noticed/resumed;
7. manager claimed/began handling;
8. manager busy/wait state covered the relevant interval; and
9. worker received the response and resumed useful work, or recorded a truthful terminal reason.

The worker records `AGENT_SIGNAL_CREATED`, captures UTC immediately before the atomic final rename,
records passive `AGENT_SIGNAL_PUBLISHED` with that exact source time, then records
`AGENT_WAIT_STARTED`. When harness-delay attribution depends on publication, missing or
contradictory publication evidence is unclassifiable; creation time must not be substituted for the
time the harness could first observe the request.

An incomplete request is unclassifiable. It does not invalidate other complete requests.

## Diagnosis

- **Harness delay/failure:** observation is late, delivery fails, or delivery is late without a
  complete valid manager-work explanation.
- **Idle-manager inattention:** delivery succeeds, no genuine busy interval explains the gap, and
  receipt/claim is late.
- **Busy-manager contention:** a genuine manager-work interval covers the delay.
- **Healthy:** request reaches the manager and worker in time without unexplained delay.
- **Downstream failure:** manager handles it, but response delivery or worker resume fails.
- **Unclassifiable:** logging cannot establish the causal boundary.

## Imperfect operation is data

The orchestrator performs much of the real management work and is fallible. Its mistakes must be
recorded rather than automatically invalidating a sprint. A late response from an otherwise-idle
orchestrator may be the evidence this experiment exists to find.

Worker mistakes, firmware failures, provider failures, and operator cleanup corrections are also
recorded separately. They invalidate the sprint only when they prevent enough causal samples,
introduce forbidden assistance, or leave process/resource safety unknown.

The E2E work must remain real and must make truthful, durable progress. Firmware success alone does
not prove wake reliability, and firmware failure alone does not disprove it.

## Runtime isolation

During counted request discovery, use only the persistent root, real external E2E workers, the
native harness blocking wait, and the diagnostic-only deterministic watcher. No watcher/reviewer
subagent, collaboration notification, transcript inspection, user-message wake, runner, relay,
wrapper, or automated support layer may help.

## Dispositions

- `QUALIFYING`: `HARNESS_PASS`, `WATCHER_PASS`, and `MANAGER_EVIDENCE_SUFFICIENT`; add it to the
  comparable set.
- `EVIDENCE_INSUFFICIENT`: real sprint, insufficient sample; preserve it and identify the exact
  cause before retrying. Correct sample/setup mistakes without code changes. If a verified
  harness/watcher/logging diagnostic gap caused the insufficiency, implement the smallest logging
  change and smoke test it before the next sprint.
- `SETUP_RETRY`: failed before a genuine sample began; correct and retry.
- `HARNESS_BUG`: verified in-scope native harness defect.
- `WATCHER_BUG`: verified in-scope deterministic-watcher defect.
- `SYSTEM_DEFECT`: verified required-logging defect that prevents trustworthy classification.

Any verified in-scope component/logging repair, including evidence-critical diagnostic
instrumentation, happens between sprints and requires rebaselining and three new comparable
qualifying runs on the repaired surface.

Comparable runs need not be consecutive in wall-clock history. Only a relevant tested-surface
change makes older runs ineligible for the final three-run comparison.

Count every live sprint launched under the active goal. The active-goal budget was 10 attempts.
Q1-Q10 used all 10. Q9 verified and repaired a passive ineligibility-attribution watcher defect,
which reset the comparable count to `0/3`. Q10 then recorded `HARNESS_PASS`, `WATCHER_PASS`, and
`MANAGER_EVIDENCE_INSUFFICIENT`: reversed manager receipt/wait-finish records and empty response
lane IDs severed all four worker chains. The final comparable count is `0/3`; never launch attempt
11. Historical pre-goal runs do not consume this budget.

## Review and repair

After every sprint, a fresh Terra-medium result reviewer reports evidence sufficiency and possible
defects. Root independently audits every criticism and has final say. Reviewers never block.

For a verified native defect only: root writes the repair plan, a persistent Terra-medium coder
changes the code, an independent Terra-medium reviewer critiques it, and Luna-high performs
focused practical smoke testing. Root accepts or rejects findings and repeats only until accepted
issues are resolved.

## Verdict

After three clean comparable qualifying sprints (3/3), choose:

- persistent manager sufficient;
- `codex exec` bridge justified by repeated idle-manager inattention;
- busy-manager contention; or
- focused implementation repair still required.

The bounded M5 execution ended before 3/3. Its exact final category is **focused implementation
repair still required because evidence remains inadequate**, with no new verified native harness or
watcher code defect. Further live work requires explicit new user authority and a new budget.
