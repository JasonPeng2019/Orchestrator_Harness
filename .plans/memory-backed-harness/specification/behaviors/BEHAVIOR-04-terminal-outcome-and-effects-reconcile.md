# BEHAVIOR-04 - Terminal truth and enabled effects reconcile durably

## Dictated outcome and source

The product fixes at most one terminal outcome from exact linked execution and
review evidence. Enabled reviewed-memory and other current-phase effects remain
durable, separately recoverable work; their failure cannot rewrite a valid
harness acceptance. Feature Section 11 and binding Implementation Sections 2.6
and 12 govern this outcome. Usage has its separate lifecycle in BEHAVIOR-05.

## Actors, triggers, and preconditions

ROOT or an authorized completion bridge submits terminal evidence for an
observed product-harness invocation. Task, objective, decision, accepted plan,
dispatch/run, review/acceptance, and resolved feature configuration are durable
or exactly resolvable. APC draft completion alone is never parent terminal
evidence.

## Behavioral flow and decision rules

1. Join the exact task, objective, decision, accepted plan, observed execution,
   result, review, and acceptance. Distinguish PASS, FAIL, BLOCKED, genuine
   terminal unknown, forced/exceptional acceptance, and absent evidence.
2. Fix one immutable local outcome. Identical replay returns it; contradictory
   replay reports an integrity conflict. A legitimate correction needs linked
   correction or supersession evidence rather than overwriting history.
3. At the recoverable local boundary, retain deterministic intent for every
   enabled current-phase follow-on effect. Reviewed receipts/recent evidence,
   EverOS ingestion, and optional telemetry execute and acknowledge separately.
   Learned-policy updates never enter this phase.
4. After restart, discover pending or uncertain effects from exact durable
   identities. Repeat effectful work only with source-backed idempotency or
   exact external reconciliation; otherwise leave an actionable uncertainty.
   Coordinate conflicting retries so concurrent processes cannot duplicate or
   overwrite an accepted authoritative effect.
5. A feature transition to off prevents new non-safety submissions and pauses,
   reconciles, drains, or isolates in-flight work before claiming fully effective
   off. Late acknowledgements retain the original configuration attribution.

## State, data, and observable effects

The outcome carries exact execution and acceptance joins, status, exception
facts, evidence identity, and observation time. Each effect retains stable
intent/payload identity, phase, acknowledgement, uncertainty/error, and
supersession as applicable. A local fixed outcome, external completion, and
operator recovery are distinct observable facts.

## Edge, failure, and recovery behavior

Wrong-task/run/decision/plan evidence or missing review cannot create an
outcome. Crash before fixation permits evaluation from exact evidence; crash
after fixation resumes only missing effects. A lost external acknowledgement
does not justify blind replay under a fresh ID. An outage leaves valid harness
acceptance and recent reviewed evidence intact. Successfully superseded failures
remain historical, not live blockers.

## Constraints and preserved behavior

Accepted STEP-01 through STEP-03 outcome, reviewed-experience, and procedure
contracts remain compatible. Original evidence or protected references remain
available for provenance. Recovery never starts learner work or treats an APC
draft as parent execution success.

## Acceptance scenarios

- Exact linked PASS, FAIL, and BLOCKED evidence fixes one outcome; unrelated or
  missing evidence does not. Genuine terminal unknown is not fabricated.
- Identical replay returns the original outcome; contradictory replay preserves
  it and exposes the conflict.
- A crash immediately before or after fixation respectively leaves no invented
  outcome or one fixed outcome with only missing effects resumed.
- Lost EverOS/remote acknowledgement is exactly reconciled or remains uncertain;
  two concurrent retries cannot duplicate the effect.
- A side-effect outage does not reverse harness acceptance, and recent reviewed
  evidence remains available for recovery.
- Disabling a write feature stops new submissions and reports in-flight work
  truthfully rather than claiming it never happened.

## Implementation freedom and unresolved decisions

Transaction, outbox, and locking mechanisms are implementation choices provided
they preserve exact joins, truthful uncertainty, and safe retry. No product
decision remains unresolved.
