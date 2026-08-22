# F.C3.W final report — attempt-0001

## Result

No reproducible candidate-harness or watcher contract failure was observed. `ABORT_REQUIRED.json` was not created.

ROOT requested normal watcher shutdown after `ORCHESTRATOR_LOST` before candidate work. The loss record attributes this to the released signing helper's incorrect liveness classification; it records no candidate harness start, signed C3 request, target materialization or worker launch, MCP process, claim, or hardware access. This is not a candidate/watcher abort condition.

## Watcher lifecycle

- Launch provenance: `topology/WATCHER_LAUNCH.json`, SHA-256 `2bbe866adc0bf25df3adf8a8f38909c8e19ef2243a692c18e94db285849cb709`.
- Codex watcher identity: PID `196176`, created `2026-08-05T06:25:39.745243Z`, thread `019fd099-5f0e-70b2-b935-a326afa1c16c`.
- Hidden watcher-loop process: PID `14444`, started `2026-08-05T06:26:05.1871181Z`; loop SHA-256 `6e9c83868a56389f03c5390221fc85899f0fd101fa4d1834cc5d56273024eb7c`.
- Ready evidence: `WATCHER_READY.json`, SHA-256 `eb6e2e005080b85bcab28fe3f919900cc229c5f09fb5f83f584b8346745f58f0`.
- Stop request: `topology/WATCHER_STOP_REQUEST.json`, SHA-256 `8e6cad8f6110cb34c8c6522c7ed4ad9ba827d76983d0a9437e40f7a185892193`.
- Service terminal: `WATCHER_SERVICE_TERMINAL.json`, SHA-256 `ae97e02a2348ac1c1d295be80e75f89bfd27650c462479f75d877f486af74f9c`.

The loop emitted six monotonically increasing heartbeats. Final sequence was `6`; final cursor was `a94523b7af098ddb90960d53b63dbd5ea2af924c17ea64b4387f739fdf5d36aa` over 34 regular files. The helper has exited and is reaped.

## Invariant audit

- Candidate remained clean at `2877ec1385b947a6ed72bbd7c95ac7a28d169782`.
- Pinned server remained clean at `f003f84a7df51cd8595a3203c62e225b21da2a22`.
- C1 lock SHA-256 was `a72d30f6f6788edbc639fd90f8174ee78a84d006ab70f9a5712bf64ec3302eb1`; C2 ROOT acceptance SHA-256 was `9b5ec6dac5391f7c3b8045903cf9c43a5f56121df61586c44907554658ae77a3`.
- All five governing hashes matched the allocated C1 values.
- Attempt roots contained no claims, events, HIL files, target files, target-worker launches, MCP processes, or hardware operations.
- The candidate/server identities, empty capability environment declaration, watcher launch identity, ready/heartbeat/terminal provenance, and ROOT stop reason were consistent. No cross-lane mutation, duplicate ownership, premature release, malformed acknowledgement, false completion, missing actionable candidate event, or leaked candidate-managed process was observed.

## Exit readiness

`WATCHER_SERVICE_TERMINAL.json` is present; helper PID `14444` is absent; `ABORT_REQUIRED.json` is absent. This watcher is ready for normal agent exit. ROOT may write `topology/WATCHER_EXIT.json` only after this agent has exited and been reaped.
