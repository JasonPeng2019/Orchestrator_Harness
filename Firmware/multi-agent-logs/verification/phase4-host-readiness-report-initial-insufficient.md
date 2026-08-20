# Phase 4 host-only wake readiness report

Date: 2026-08-01  
Scope: validation only; no production or test files changed.

## Advisory recommendation

**INSUFFICIENT_EVIDENCE.** The unchanged practical runner passed its internal complete-chain and quiet-control assertions, and all required suites/static checks passed. However, it does not print the generated UUID wake_id or action timestamps, and its temporary raw harness/watcher records are deleted on exit. Therefore the exact six-stage row cannot be independently reconstructed from the durable artifacts retained by this run. The root should decide whether the existing Phase 3 smoke evidence is sufficient or require a corrected validation run that preserves those records; this run did not modify the runner.

## Preflight

Repository root: C:/Users/Jason/Documents/Jason/FirmCLI_Tester/Firmware-Test-Manual/MCP-Trial-3

Commands/results:

    Get-CimInstance Win32_Process excluding current probe process
    RESULT: no matching repository practical/watch process outside probe

    Test-Path orchestrator_harness/.state
    RESULT: False

    stale runtime directory check
    RESULT: no stale relevant runtime directories

    python -c "import sys; print(sys.executable); print(sys.version)"
    C:/Users/Jason/Documents/Jason/FirmCLI_Tester/Firmware-Test-Manual/MCP-Trial-3/BYO-Firmware-MCP/.venv/Scripts/python.exe
    3.12.13 (main, Jun  2 2026, 22:47:20) [MSC v.1944 64 bit (AMD64)]

Implementation SHA-256 hashes (before and after validation; identical):

    orchestrator_harness/cli.py
    6E77F42870B7564A8F30BD2AB108112BB2E745882C69E005E899AFFA738D0CEE
    harness_watcher_implementation/attention.py
    D877ED285A522EA3E8ED7E460EB28C657E2668608C598C65D67FBDC1F38F1BF5
    harness_watcher_implementation/tests/run_attention_practical.py
    BDD6DFA90F80C2ED309E9B638BD8266D4E84EBBDF752911FBE0DC0598339CFFB

## Exact commands and results

### Practical host-only wake and quiet control

Command, from repository root:

    python harness_watcher_implementation/tests/run_attention_practical.py

Exit code: 0. Stdout:

    {"disabled": true}
    attention practical host-only check: PASS (R10 deadline-origin + healthy blocking path, R9 continuity precedence, CLI disabled gate)

Stderr: empty.

Durable captures:

- multi-agent-logs/verification/phase4-practical-stdout.txt
- multi-agent-logs/verification/phase4-practical-stderr.txt

The practical assertions at harness_watcher_implementation/tests/run_attention_practical.py:68-112 create the external request, run the real python -m orchestrator_harness ... watch --until-actionable subprocess, assert returned event/wake/transport, ingest producer and harness logs, require wake_evidence.status == COMPLETE, and require manager order MANAGER_WAIT_STARTED -> MANAGER_WAKE_RECEIVED -> MANAGER_WAIT_FINISHED -> MANAGER_EVENT_CLAIMED.

### Full suites

    python -m unittest discover -s orchestrator_harness/tests -t . -q

Exit code: 0; stdout empty. Raw stderr ended with:

    ----------------------------------------------------------------------
    Ran 191 tests in 28.274s

    OK (skipped=1)

The preceding stderr diagnostics are expected negative-path lane-controller test output; they did not affect the zero exit status. Full capture is retained in multi-agent-logs/verification/phase4-harness-suite-{stdout,stderr}.txt.

    python -m unittest discover -s harness_watcher_implementation/tests -t . -q

Exit code: 0; Ran 85 tests in 2.464s; OK. The suite emitted expected negative-path CLI diagnostics, retained in multi-agent-logs/verification/phase4-watcher-suite-{stdout,stderr}.txt.

### Static checks

    python -m pyright orchestrator_harness/cli.py harness_watcher_implementation/attention.py

Exit code: 0; output: 0 errors, 0 warnings, 0 informations.

    python -m compileall -q orchestrator_harness harness_watcher_implementation harness_common scripts/orchestration

Exit code: 0; stdout/stderr empty.

## Six-stage evidence reconstructed by the practical

The practical uses epoch_id=A00_test, event_id=wake, lane A00_test:Atlas:A00, manager session practical-session, invocation practical-invocation, activity blocking-wait, and transport blocking_harness_wait_stdout. The exact generated UUID and timestamps are not present in the retained output; each was asserted in-process.

| Stage | Record/evidence | Practical proof |
|---|---|---|
| 1. Request created | AGENT_SIGNAL_CREATED | real recorder call at lines 62-68 |
| 2. Harness detected | HARNESS_SIGNAL_OBSERVED | watcher timeline required at lines 100-110 |
| 3. Wake attempted | MANAGER_WAKE_ATTEMPTED with shared generated wake_id | timeline required at lines 108-110 |
| 4. Wake delivered | MANAGER_WAKE_DELIVERED, successful blocking-wait transport | returned event assertion at lines 89-93 and timeline assertion at 110 |
| 5. Manager noticed | MANAGER_WAKE_RECEIVED first manager action after wait start | manager-order assertion at lines 95-112 |
| 6. Manager began handling | MANAGER_EVENT_CLAIMED | manager-order assertion at lines 111-112 |

The analyzer also asserted nonnegative attempted-to-delivered, delivered-to-received, and received-to-claim metrics at lines 103-107. This proves the runner's internal validation, but not an independently auditable durable row for this execution.

## Quiet-timeout control

The practical creates fresh quiet epoch/output A00_practical_quiet and asserts at run_attention_practical.py:117-140:

- blocking wait exit code 3;
- returned event_id == WATCH_TIMEOUT;
- no returned wake_id;
- no MANAGER_WAKE_* records in producer, harness, watcher timeline, or findings.

The practical overall exit code was 0.

## Failed-wake and fail-closed focused references

- harness_watcher_implementation/tests/test_attention.py:51-77 asserts a complete chain is COMPLETE; every removed stage, duplicate delivery, reused attempt, out-of-order delivery, and contradictory post-claim action is INSUFFICIENT_EVIDENCE; an attempt with MANAGER_WAKE_FAILED is FAILED only when request creation and harness observation exist; a failed-only chain missing observation is INSUFFICIENT_EVIDENCE; and a retry uses a new wake ID and can become COMPLETE.
- harness_watcher_implementation/tests/test_attention.py:30-48 validates wake record metadata, UUID/provenance, mutually exclusive delivered/failed outcomes, and exact wait-finish wake and transport linkage.
- orchestrator_harness/tests/test_manager_notifications.py:100-130 asserts two attempts each have one delivered outcome, retries receive distinct wake IDs, failed delivery records MANAGER_WAKE_FAILED with delivery_succeeded == false, and no delivered record exists for the failed wake ID.
- harness_watcher_implementation/tests/test_attention_ingestion.py:22-25 asserts disabled ingestion returns disabled and creates no watcher output; the practical disabled CLI gate is also at run_attention_practical.py:190-196.
- harness_watcher_implementation/tests/test_attention_ingestion.py:26-49 asserts malformed or impossible durable evidence is retained as event-level INSUFFICIENT_EVIDENCE.

## Isolation

No AI watcher, observer, relay, reviewer, collaboration API/message, user-message wake, hardware, firmware, provider, MCP-server, deploy, flash, commit, or push operation was used. The practical alone launched the production harness watch subprocess and published its synthetic external signal through the existing test fixture. No production code or tests were edited.

## Cleanup proof

The initial broad process probe accidentally matched its own probe command text; it was immediately rerun excluding the probe PID. The corrected preflight and final checks found no relevant process. A repository-wide temporary-directory probe timed out before producing a result; the required narrow owner-scoped probe then completed successfully.

Final results:

    no practical runner or blocking harness watch process
    no practical temporary directories in relevant owners
    orchestrator_harness/.state exists: False
    __pycache__ remaining in allowed trees: 0

The only deletion was the set of 13 resolved __pycache__ directories under orchestrator_harness, harness_watcher_implementation, harness_common, and scripts/orchestration; every target was verified to be named __pycache__ and inside the repository before removal. No repository-wide or unrelated-environment cleanup was performed.

## Evidence capture hashes

    phase4-compileall-stderr.txt E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855
    phase4-compileall-stdout.txt E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855
    phase4-harness-suite-stderr.txt 298927F4E919C8A09EB3F1A17258F7C4B4ABD9607E59ADC938005472695E2BBB
    phase4-harness-suite-stdout.txt E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855
    phase4-practical-stderr.txt E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855
    phase4-practical-stdout.txt ACABD0B2BE47ECA7A0CF520943BCAB7CF86EBB806AE57DD3DE28E67CADB8A09D
    phase4-pyright-stderr.txt E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855
    phase4-pyright-stdout.txt F7E36FCD53B8A6D457BCA02A7B7F3443B6848820463F4D938478CB07621952E8
    phase4-watcher-suite-stderr.txt 3BD364D323D4C0756921B9CEC73FF44EDA191733053B3F44958B0FFA165B6709
    phase4-watcher-suite-stdout.txt 700A7CAB9DE76E75697D776BC992E0416817AA6A0A7E87B33D0A408857D3A38E

