# Phase 4 Spec - Host-Only Wake Readiness

## Plain goal

Prove that the real blocking harness wait can receive one external request and return it to a live
manager without an internal watcher/relay subagent. Confirm that the durable records reconstruct
the exact wake path and that a quiet wait does not fabricate a wake.

This is a validation task, not a redesign or implementation phase.

## Scope and authority

- The root orchestrator owns this plan, audits the evidence, and makes the final pass/fail decision.
- One **GPT-5.6-luna high** doer executes the procedure and reports facts. It does not decide that
  Phase 4 is complete and cannot block later work.
- No firmware, hardware, provider, MCP-server, deployment, commit, push, or flash operation is in
  scope.
- No AI watcher/observer/relay subagent may participate in the tested wake path.
- Do not edit production code or tests merely to make the run pass. If a defect appears, stop the
  affected run, preserve the evidence, and report the smallest diagnosed boundary to the root.
- The doer may create only the verification report and ordinary runtime evidence in the locations
  allowed by `REPOSITORY_LAYOUT.md`.

## Existing implementation under test

Use the completed Phase 3 implementation and its existing host-only practical runner:

- `orchestrator_harness/cli.py`
- `harness_watcher_implementation/attention.py`
- `harness_watcher_implementation/tests/run_attention_practical.py`

Do not introduce another runner, wake transport, queue, polling loop, or notification path.

## Procedure

### 1. Preflight

1. Read `AGENTS.md`, `REPOSITORY_LAYOUT.md`, `$always-keep-in-mind`,
   `logging_additions_spec_2.md`, this spec, and the Phase 3 completion evidence in `PLAN.md`.
2. Confirm no process in this repository is already running
   `run_attention_practical.py` or `orchestrator_harness ... watch`.
3. Confirm `orchestrator_harness/.state` does not exist and no stale
   `multi-agent-logs/attention-runtime-*` or `multi-agent-logs/practical-wake-*` directory exists.
4. Record the Python executable/version and SHA-256 hashes of the three implementation files
   listed above.

Any stale relevant process or ambiguous source-tree runtime state makes the preflight
`INSUFFICIENT_EVIDENCE`; do not kill an unrelated process or guess ownership.

### 2. Run the real host-only wake smoke

From the repository root, run:

```powershell
python harness_watcher_implementation/tests/run_attention_practical.py
```

The existing practical must, without modification:

1. create the external `AGENT_SIGNAL_CREATED` record;
2. record the manager wait boundary;
3. launch a real `python -m orchestrator_harness ... watch --until-actionable` subprocess;
4. publish the matching external manager signal while that process is blocked;
5. receive the returned `event_id`, `wake_id`, component, and transport from stdout;
6. record manager receipt first, then matching wait finish and claim through the real recorder CLI;
7. ingest both producer logs and the harness attention log through the deterministic watcher
   implementation; and
8. assert `wake_evidence.status == COMPLETE`, exact wake-ID correlation, and ordered manager
   actions.

The same practical must run a separate fresh quiet epoch/output and prove exit code 3, no returned
`wake_id`, and no `MANAGER_WAKE_*` records.

Capture the complete command, exit code, stdout, and stderr in the final report. A printed `PASS`
without exit code 0 is not a pass.

### 3. Verify failed-wake and fail-closed controls

Run the complete harness and deterministic-watcher suites:

```powershell
python -m unittest discover -s orchestrator_harness/tests -t . -q
python -m unittest discover -s harness_watcher_implementation/tests -t . -q
```

Inspect the relevant focused test matrix and report the exact tests that prove:

- an explicit failed wake is distinguishable from missing evidence;
- a failed-only chain still requires request creation and harness observation;
- missing, duplicate, mismatched, reused, or out-of-order wake evidence is
  `INSUFFICIENT_EVIDENCE`;
- every attempt has exactly one delivered or failed outcome; and
- watcher-disabled recording is a clean no-op.

Do not treat test names alone as evidence: cite the test file/line range and the asserted result.

### 4. Static validation

Run:

```powershell
python -m pyright orchestrator_harness/cli.py harness_watcher_implementation/attention.py
python -m compileall -q orchestrator_harness harness_watcher_implementation harness_common scripts/orchestration
```

Report exact results. Do not broaden into unrelated lint cleanup.

### 5. Cleanup proof

After all commands finish:

1. confirm no repository process remains for the practical runner or blocking harness watch;
2. confirm no practical temporary directory remains;
3. confirm `orchestrator_harness/.state` was not recreated; and
4. remove only generated `__pycache__` directories under the changed harness/watcher/common and
   orchestration-helper trees after resolving every deletion target inside this repository.

Never recursively delete across the whole repository or inside unrelated environments.

### 6. Durable report

Write:

`multi-agent-logs/verification/phase4-host-readiness-report.md`

Include:

- preflight identities and hashes;
- exact commands, exit codes, and concise outputs;
- a six-stage evidence table showing what the practical verified;
- quiet-timeout result;
- failed-wake/fail-closed test references;
- full-suite and static-check totals;
- isolation statement confirming no AI relay or collaboration notification was used;
- cleanup proof;
- every observed failure or ambiguity; and
- a recommendation of `READY`, `NOT_READY`, or `INSUFFICIENT_EVIDENCE`.

The recommendation is advisory. The root independently audits it and determines Phase 4 status.

## Acceptance checklist for the root

The root may mark Phase 4 complete only when all of these are verified:

- the real blocking wait returned the exact external event without an AI relay;
- the practical reconstructed the complete ordered six-stage chain with one shared wake ID;
- manager receipt was the first manager action after delivery;
- the separate quiet wait timed out without any wake record or ID;
- explicit failure is distinguishable from absent/incomplete evidence;
- the deterministic watcher ingestion path reported complete, internally consistent evidence;
- full harness and watcher suites and targeted static checks passed, apart from documented
  intentional skips;
- no contradictory or missing evidence remains; and
- all relevant processes and temporary runtime state were cleaned up exactly.

If any requirement is false or unknowable, Phase 4 does not pass. The root decides whether the
result identifies a small Phase 3 repair or merely requires a corrected rerun.

## Accepted repair after the first readiness run

The 2026-08-01 run returned `INSUFFICIENT_EVIDENCE`: all functional assertions passed, but the
practical deleted its generated raw wake records and did not retain the exact wake ID/timestamps.
The root accepts this as a narrow test-evidence retention defect, not a production wake defect.

Implement only this repair in
`harness_watcher_implementation/tests/run_attention_practical.py`:

1. Add an optional `--evidence-dir <path>` argument. With no argument, preserve the current
   temporary-directory behavior and exact cleanup.
2. When the argument is supplied, require a fresh empty destination and retain these separate
   subtrees beneath it:
   - successful wake harness records;
   - successful wake producer/watcher records;
   - quiet-control harness records; and
   - quiet-control producer/watcher records.
3. Retain a machine-readable successful-wake result containing the returned event, exact
   `wake_id`, analyzer `wake_evidence`, and the ordered six matching canonical records with source
   timestamps. Retain a quiet result containing the timeout event and proof that no wake record
   exists.
4. Do not retain fixture clutter unrelated to reconstructing the wake or quiet control.
5. Add focused automated coverage that invokes the real practical with `--evidence-dir` and proves
   the retained bundle independently reconstructs one shared wake ID and the required timestamp
   order. Also prove the quiet bundle has no wake ID or `MANAGER_WAKE_*` record.
6. Do not change production harness/analyzer behavior, add a new wake mechanism, or weaken any
   assertion.

After the repair passes independent code review, rerun the Luna-high procedure with a fresh
evidence directory under `multi-agent-logs/verification/phase4-wake-evidence/`. The final report
must cite the retained files and reproduce their exact IDs/timestamps rather than relying only on
in-process assertions.
