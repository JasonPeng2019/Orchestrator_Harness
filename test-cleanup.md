# Test-cleanup specification

Status: **READY FOR NEXT RUN**. The reusable support/helper implementation, 16 focused tests,
eight-scenario practical smoke, independent Luna-high practical retry, plan validator, and full
repository verification are green as of 2026-08-06. The first Luna dispatch was a no-test sandbox-
helper failure; the one corrected retry passed and produced an empty finding set.

## Purpose

Simplify the external C3 acceptance controller so outer-test procedure errors do not create
candidate-harness reruns, relocks, or false product findings. This specification concerns only the
outside C3 setup/launch/monitor/validation scripts. It does not change candidate product behavior,
the stable runner, the MCP fixture, or hardware authority.

## Required behavior

### Candidate-rerun boundary

Only an evidence-backed **candidate-harness behavior defect** may invalidate an already-green
candidate test or reopen candidate implementation/C0/C1/C2. Every other failure—including any
external controller, watcher helper, prompt, launch, report, schema, evidence-writer, process
supervision, fixture, or test-support failure—must remain in the supporting-test route.

Supporting-test failures are corrected in place when the current attempt can still close honestly.
When they make a physical attempt uncloseable, mark only the incomplete physical work incomplete and
create a fresh attempt namespace if needed; retain all valid prior candidate and test credit by
immutable evidence and unchanged dependency fingerprint. Never convert a supporting-test failure
into a candidate rerun, relock, or broad candidate-test repeat merely because the support layer
could not complete its paperwork or shutdown.

### 1. ROOT starts the mechanical observer

ROOT starts `.codex/scripts/c3_watcher_helper.py` directly, records its exact PID-plus-creation
identity, and waits for its helper-authored ready record before target work starts. The helper must
not depend on an AI watcher subagent to be launched or kept alive.

The AI watcher role is removed from the acceptance-critical path. It may be retained as optional,
read-only review only when explicitly useful; its launch, report, exit, or absence must not block a
physical attempt, manifest closure, or result acceptance.

### 2. Observer outcomes are pooled by default

The loop continuously writes its existing ready, heartbeat/cursor, defined finding, and terminal
service records. A non-critical observation is recorded as a finding for the attempt's one post-gate
triage; it must not stop target work, restart a review, or trigger repair during the same gate.

The only loop outcome that may request immediate ROOT stop is exact evidence that continued work
would cause one of these:

- an unauthorized or wrong-resource operation;
- loss of containment or cleanup of a live registered process; or
- irreversible corruption of evidence needed to judge later work.

The abort record must name which condition applies and reference supporting evidence. No inferred,
speculative, cosmetic, target-test, safely contained candidate behavior, or incomplete non-critical
evidence condition may be promoted to an immediate abort.

### 3. ROOT closes observer evidence mechanically

After candidate-managed shutdown, ROOT requests the helper stop, verifies its terminal-service
record and exact process exit/reap, then creates one immutable
`topology/WATCHER_OBSERVATION_CLOSE.json` before the manifest begins.

That record binds:

- helper launch path/hash and exact identity;
- ready path/hash;
- heartbeat path/hash and final sequence/cursor;
- service-terminal path/hash;
- abort path/hash or explicit absence;
- exact exit/reap result; and
- any optional AI-watcher report/exit reference, marked supplemental.

The candidate orchestrator may close the manifest only after this required record is valid, or after
the fallback-evidence rule below proves every fact the unavailable helper record was meant to prove.
A missing optional AI-watcher report never blocks closure. A missing helper record is uncloseable only
when one of its required facts cannot be reconstructed honestly from approved backup evidence.

### 4. Isolate outer procedure failures

ROOT must classify failures from outer attempt allocation, launch, monitoring, report handling,
evidence validation, or emergency cleanup as `OUTER_ATTEMPT_PROCEDURE_FAILURE` unless exact evidence
shows a candidate defect, changed C1-locked candidate input, or untrustworthy candidate result.

- If the error is administrative and the existing attempt can still close honestly, correct it in
  place and continue without rerunning any test.
- If the error makes the immutable attempt uncloseable, close it as non-acceptable and allocate a
  fresh attempt namespace.
- Re-credit every prior candidate/test result only by immutable evidence reference and unchanged
  dependency fingerprint.
- Do not reopen candidate implementation, C0, C1, C2, or a green candidate test solely because of
  an outer procedure failure.

### 5. Cleanup must continue safely

During outer emergency cleanup, ROOT must never signal a PID whose exact creation identity is not
verified. If a registered child is already gone or its identity cannot safely be verified, ROOT
records `already_gone_or_identity_unverified`, does not signal that PID, and continues orderly
shutdown/reaping of every other registered identity. The attempt remains failed/non-acceptable; this
is not a clean-success claim.

## Topology/documentation changes

### Evidence fallback matrix

The C3 plan, governing specification, readiness document, and acceptance criteria must contain one
fact-by-fact evidence matrix. For every required C3 conclusion, it names:

- the conclusion being proved;
- the normal primary evidence source;
- the independent backup evidence sources that may replace it;
- the exact correlation fields, hashes, identities, and time bounds required for that replacement;
- who evaluates the fallback; and
- whether an unreconstructable absence makes only the current attempt incomplete or is a real
  immediate-stop condition.

The helper is independent corroboration, not the sole source of truth. If its record is missing,
ROOT and C4 may use only the named backups to prove the same fact. Typical backups may include
candidate immutable process/claim/event/result records, ROOT launch/identity/reap records and OS
snapshots, MCP session/request logs, and target build/behavioral evidence. Candidate-owned evidence
alone may not be treated as independent corroboration for a candidate behavior claim; use the
matrix's required external correlation as well.

If the matrix's approved sources completely prove the required fact, the attempt may continue or
close without the helper record. If a fact has no complete, correlated backup—for example, a required
live observation that left no durable trace—the attempt is incomplete and rolls only to a fresh
physical attempt. It does not trigger candidate relock, candidate repair, or broad candidate-test
repeat.

This is a topology/documentation requirement plus outer C3 validation behavior. It is not a
candidate-harness feature and must not add a generic harness framework.

## Explicit non-goals

- Do not add a generic AI-watcher resume framework.
- Do not change the candidate harness, MCP server, or physical hardware protocol.
- Do not make the external controller a second target-work orchestrator.
- Do not use broad process termination or kill a PID with uncertain identity.
- Do not replace C4's independent final evidence audit.

## Implementation location and ownership

The reusable lifecycle/classification source is `.codex/scripts/c3_outer_support.py`; the reusable
deterministic observer is `.codex/scripts/c3_watcher_helper.py`; the host-only practical smoke is
`.codex/scripts/run_c3_outer_support_smoke.py`; and focused units are in
`.codex/tests/test_c3_outer_support.py`. A future attempt-specific ROOT controller imports this source
and supplies its attempt paths/commands. It must not import an implementation from a closed
`attempt-NNNN` directory. Closed attempts remain immutable evidence, not production support code.

ROOT owns helper launch, immediate-stop classification, observation closure, outer-procedure
classification, and safe cleanup. `C3-HARNESS` remains the owner of target workers, MCP sessions,
claims, authorization, and ordinary candidate cleanup. The support module is deliberately not a
target-work orchestrator and does not edit the candidate, stable runner, MCP fixture, or hardware.

## Implemented outer-support behavior

The reusable layer now provides these bounded mechanics:

1. `MechanicalObserver.start()` launches the helper directly as a non-agent process, retains the
   process handle, records exact PID/creation identity and outputs, and waits for helper readiness.
2. `classify_observer_record()` returns an immediate safety stop only for the three exact conditions
   in this specification with valid evidence; every other observation is pooled and does not
   invalidate product credit.
3. `write_observation_close()`, `validate_observation_close()`, and
   `MechanicalObserver.stop_and_close()` validate all six required
   facts—helper identity, ready, heartbeat, terminal service, abort disposition, and helper exit—and
   write create-once `WATCHER_OBSERVATION_CLOSE.json`. A normal primary source is enough; a fallback
   requires two independent source classes plus exact correlation. Missing unresolved facts raise
   `AttemptIncomplete`, not a candidate defect. The O-side sealer must call
   `validate_observation_close()` and must not reuse a closed-attempt sealer that requires an AI
   watcher report.
4. `classify_outer_failure()` routes support failures to in-place correction or outer-attempt-only
   rollover. It permits material product triage only when exact referenced evidence proves a
   candidate defect, changed locked input, or untrustworthy candidate result.
5. `cleanup_registered_children()` never signals an unverified PID and continues through the full
   registered child set after an already-exited child, identity race, or per-child cleanup error.
6. `.codex/scripts/c3_watcher_helper.py` is the reusable, attempt-configured deterministic loop. It
   records ready/heartbeat/claim/assignment/terminal evidence, pools ordinary findings, and creates
   an immediate-stop request only for the three explicit live-safety conditions. It never launches
   target work or uses MCP/hardware authority.

This is the complete authorized code slice. Do not copy the historical 1,000-line ROOT supervisor,
create a second orchestration framework, or modify closed attempt scripts merely for tidiness. The
next attempt's thin ROOT controller composes these mechanics with the already-defined O/signer/
governing-input/candidate lifecycle and binds the exact support-source hash in prelaunch evidence.

## Read-only supporting-architecture audit (2026-08-05)

The following observed paths require review and, where applicable, change. They are all outside the
candidate/general harness.

1. **AI watcher is treated as a required live process.**
   `acceptance-control/attempt-0004/root/root_launch.py` lines 781-812 and 836-845 monitor the
   AI-watcher's PID, wait for its exit, and fail if its report/terminal record is absent. This is the
   direct cause of the attempt-0010 “watcher exited without terminal report” failure. Replace that
   dependency with direct ROOT ownership of the mechanical helper and its closure record.
2. **Every observer abort is promoted immediately.**
   The same ROOT script lines 795-808 turns any `ABORT_REQUIRED.json` into a root abort. The helper
   script at `attempt-0004/watcher/watcher_loop.py` lines 169-178 and 270-299 emits that record for
   every classified oracle/immutability/singular-root condition. Split this into pooled findings and
   the three narrow immediate-stop conditions in this specification.
3. **ROOT's broad exception path aborts candidate work.**
   `root_launch.py` lines 995-1028 writes `ROOT_ABORT_NOTICE.json` for any outer exception and waits
   for candidate shutdown. Classify those exceptions first. Administrative/support failures must
   resume in place; uncloseable support failures must close only the outer attempt and preserve credit.
4. **One uncertain child interrupts remaining cleanup.**
   `root_launch.py` lines 1029-1042 call `terminate_exact` serially. Its lines 228-243 raise if PID
   creation identity cannot be confirmed, which stopped the intended cleanup order in attempt-0010.
   Replace this only in the outer supervisor with a non-signaling `already_gone_or_identity_unverified`
   outcome that lets cleanup continue for other registered children.
5. **Helper startup is delegated to an AI prompt.**
   `acceptance-control/attempt-0010/watcher/W_PROMPT.md` lines 20-25 makes the AI watcher execute
   `Start-Process watcher_loop.py`. Move that launch and identity binding into ROOT; update the
   generated external-control template rather than the already-closed attempt directory.
6. **Support-script exceptions are indistinguishable from candidate failure.**
   `watcher_loop.py` lines 194-208 raises on missing launch provenance or candidate/server setup;
   ROOT's generic liveness checks then classify the resulting helper/agent loss as fatal. Give these
   conditions explicit support-procedure records and the isolation route above, except a real changed
   candidate/locked input, which remains an honest invalid-input result rather than a candidate bug.
7. **Manifest sealing still requires AI-watcher exit.**
   `acceptance-control/attempt-0004/orchestrator/seal_attempt.py` lines 120-135 rejects closure when
   `WATCHER_EXIT.json` is not exact normal/reaped, and lines 183-204 use watcher abort/exit as PASS
   preconditions. Replace these checks with required helper-backed
   `WATCHER_OBSERVATION_CLOSE.json`; retain any AI-watcher reference only as optional provenance.
8. **Outer O/signer launch and result failures collapse into a candidate-abort path.**
   `root_launch.py` has generic launch/pipe/identity failures (lines 77-125 and 663), O-result
   deadline/manifest failures (lines 866-883), and signer/governing-helper closure failures
   (lines 881-925). These are support-layer failures unless the preserved evidence demonstrates
   incorrect candidate behavior. They need in-place correction or outer-attempt-only rollover, never
   automatic candidate rerun/relock.
9. **The governing-input helper needs a split classification.**
   `root_launch.py` lines 813-816 and 923-925 treat helper loss as generic fatal failure. A real
   detected governing/C1 change remains an invalid-input safety stop; helper process, report, or
   shutdown failure without such a change is supporting infrastructure and must use the isolated
   outer-attempt route.
10. **C3 service-launch failures need explicit attribution.**
    `acceptance-control/attempt-0006/orchestrator/launch_c3_service.py` has support-launch,
    process-snapshot, readiness-record, and wrapper-identity failure branches (for example lines
    144 and 188-251). Classify them as support failures unless their captured candidate output proves
    a candidate-harness behavior defect. A service that never became ready leaves physical work
    incomplete; it does not invalidate prior green candidate gates.
11. **The control code is chained through historical attempt directories.**
    The current attempt-0010 root and watcher wrappers import implementations from attempts 0004/0006
    rather than from one named reusable external-control source. Move the future implementation to a
    dedicated external-control source location and generate wrappers from it. Do not edit closed
    attempt directories or let a historical attempt become mutable production support code.

## Mandatory implementation-agent audit

Before changing code, the implementing agent must perform a second, broader read-only audit of every
reusable external C3 control-script source and generated attempt wrapper, including ROOT launch,
observer/helper, C3 orchestrator launch, signer/governing-input helper, result/manifest validation,
failure classification, and cleanup paths. It must identify every branch where supporting-test code
can currently:

- abort candidate work;
- invalidate a green candidate/test result;
- request a candidate relock or rerun; or
- prevent cleanup/closure solely through support-code failure.

For each branch, the agent must state whether it is a real immediate-stop condition under this spec.
If not, it must route it to in-place correction or outer-attempt-only rollover with preserved credit.
The agent must not edit candidate/general-harness code to solve any audited support-layer issue.

## Required proof before use

Run a host-only disposable-fake rehearsal that proves all of the following without MCP, hardware, or
candidate source edits:

1. ROOT launches the helper directly and accepts its ready record.
2. A non-critical injected observer finding is retained and the selected test set completes.
3. A defined immediate-stop condition halts only registered topology and preserves evidence.
4. An early or absent optional AI watcher does not block closure.
5. Helper terminal evidence produces a valid `WATCHER_OBSERVATION_CLOSE.json`.
6. A simulated already-exited registered child is recorded without signaling an uncertain PID, while
   other registered children still shut down.
7. An injected outer report/schema failure is corrected in place when closure remains possible.
8. An injected uncloseable outer failure rolls only to a new attempt namespace and preserves valid
   candidate/test credit without a candidate relock.

Then run targeted external-controller tests for the changed paths. Do not run a physical C3 attempt
until the rehearsal is green. The subsequent physical attempt remains a fresh attempt and is the only
evidence of physical behavior.

## Acceptance criteria

The change is complete only when the rehearsal and targeted controller tests pass, the governing
documents and execution plan remain aligned, and a review confirms that no candidate-harness files,
MCP fixture files, or hardware authority changed.
