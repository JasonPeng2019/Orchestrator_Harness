# Normal-operation acceptance policy

## Authority and purpose

This policy is the user-authorized acceptance rule for the remaining
fixed-strategy implementation run. It changes review and verification breadth;
it does not change the product's intended normal behavior, lane ownership, or
the prohibition on benchmarks and the learned selector.

The run should finish the ideal supported product path within the available
time. A reviewer requests repair only for a defect that affects normal use, a
credible regular recovery, or a non-negotiable correctness boundary. Every
other confirmed issue is recorded in [KNOWN_ISSUES.md](KNOWN_ISSUES.md) with its
evidence and disposition, then work continues without a correction/re-review
loop.

## What counts as normal operation

Normal operation includes:

- documented supported platforms, providers, configurations, and schemas;
- valid task cards, accepted plans, ordinary legacy cards, and all-off mode;
- enabled fixed-strategy preparation, final context, launch, review, outcome,
  effects, usage, setup, network, snapshot, and operator flows;
- ordinary bootstrap, resume, restart, retry, optional-service outage, and
  interrupted-operation recovery that the product explicitly supports; and
- the scoped local, live Atlas, and nested native proof paths in STEP-16–18.

Normal operation does not include manually corrupted internal records,
contrived impossible combinations, unsupported providers/platforms, unreachable
private helpers, or synthetic timing windows that require test-only mutation,
unless the same condition is credible in a supported deployment.

## Findings that require repair

Repair is required when evidence shows any of the following:

1. The ideal normal path fails, lies, silently falls back to different meaning,
   or regularly produces the wrong result.
2. A supported bootstrap, resume, retry, restart, or ordinary outage path loses
   work, duplicates work, wedges the product, or cannot recover as promised.
3. A changed public or persisted contract breaks a supported caller or existing
   supported state without an explicit compatibility path.
4. A critical invariant is violated, even if the triggering case is uncommon:
   credential/privacy leakage; wrong task/plan/base/recipient execution;
   fabricated success or missing evidence treated as success; duplicate or
   unsafe external mutation; durable corruption/data loss; or uncontrolled
   cleanup of resources outside the exact owned scope.
5. With the proof's declared service, authority, binding, and environment
   prerequisites ready, the required local, live Atlas, or nested native
   normal-path proof cannot be produced for the pinned candidate. An unavailable
   prerequisite instead leaves only the dependent claim blocked/open; it is not
   evidence of a candidate defect or a pass.

## Findings that are documented without repair

A confirmed issue may ship as a known issue when all of the following are true:

- it is outside normal supported use and outside the critical invariants above;
- the normal path and directly affected preservation path still pass;
- failure is contained and reported honestly rather than converted to success;
- it does not make a supported public/persisted contract misleading; and
- [KNOWN_ISSUES.md](KNOWN_ISSUES.md) records reproduction evidence, impact,
  scope, workaround or containment, and why repair was deferred.

Examples include cosmetic diagnostics, administrative/reporting imperfections,
unsupported malformed input, an unreachable internal helper, a test-only race
with no credible product path, or a platform/provider outside the declared
support set. Uncertainty is not automatically non-blocking: classify it with
evidence or leave only its dependent claim unaccepted.

## Reviewer contract

Reviewers inspect the exact candidate and return the existing `SHIP`, `REVISE`,
or `BLOCK` verdict:

- `SHIP`: normal operation and affected critical invariants are correct. The
  reviewer may report documented-only findings; they do not change the verdict.
- `REVISE`: at least one reproduced repair-required defect exists. Each finding
  states the normal operation or critical invariant it breaks and the smallest
  correction.
- `BLOCK`: required authority, dependency, or normal-path evidence is absent, so
  the candidate cannot yet be judged or accepted.

Reviewers do not request repair for style, theoretical hardening, exhaustive
malformed-input behavior, dead code, or a test-only edge unless they demonstrate
normal-use or critical-invariant impact. One fresh review is sufficient after a
candidate's focused evidence passes. A documented-only finding does not trigger
a correction worker or another review.

## Proportionate verification

Each lane and integration candidate must prove the smallest representative set
that supports its claim:

1. one direct ideal normal path for the changed behavior;
2. legacy/all-off preservation when the changed seam can affect it;
3. one credible regular failure/recovery path when recovery is central; and
4. focused checks for each critical invariant the diff touches.

Run broader selectors only when they decide a required claim, when focused
evidence is ambiguous, or once at final integration as specified by STEP-16.
Classify every observed failure. Repair-required failures return to their owner;
documented-only failures enter the known-issues register and do not trigger a
serial repair loop. Skipped or unavailable evidence is never called passing.

## Time-priority order

Use the remaining run time in this order:

1. close the joined checkpoint/context/dispatch normal path;
2. finish lane 1's outcome, effects, usage, network, snapshot, and operator
   contracts, publishing consumer interfaces as soon as each is stable;
3. finish the lane 2–4 normal-path consumers in parallel;
4. integrate one pinned candidate and run the focused STEP-16 gate;
5. run the scoped STEP-17 live Atlas proof and STEP-18 all-off/enhanced native
   lifecycles; and
6. spend remaining time only on repair-required findings.

## Post-MVP deferred repair

The rules above govern the shortest path to the minimal MVP. A documented-only
finding never delays or invalidates that MVP proof. After STEP-16 through STEP-18
pin and prove the MVP, the active run continues with the user's deferred-repair
phase: Master-ROOT assigns every actionable code finding in `KNOWN_ISSUES.md` to
its owning lane for one bounded correction, focused preservation evidence, and
one fresh review. Update each row monotonically with its fixing pin and evidence.
Resolve environment/access/tooling entries with direct evidence instead of
inventing product changes. This later phase does not broaden product meaning or
the frozen-harness exception.
