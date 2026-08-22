# Super-cache problems and findings

Updated: 2026-08-22

This is the factual record for the bounded-script and Stop-verification cache
work. The final proof used a disposable BYO-Firmware-MCP Git worktree only; it
did not start an MCP server, use hardware, claim a board, or change the primary
repository.

## Final result

The documented workflow is now enforced and verified for harness-launched
coding/subagent lanes:

- The controller rejects a coding/canonical launch before `Popen` when its
  identified worktree has no completed subagent overlay receipt.
- A prepared receipt enables the Codex trust override required with
  `--ignore-user-config`.
- The controller invokes the cached Stop verifier before the provider starts
  and after the provider has been reaped. A failed or blocking check fails the
  lane.
- A fresh prepared worktree receives SessionStart and PreToolUse timeouts of
  15 seconds and a Stop timeout of 300 seconds. There are no remaining
  3-second settings in the cache source or cache copy.
- The Stop verifier can find a `.venv` owned by the primary worktree of the
  same Git repository when the prepared worktree has no local `.venv`.

A clean final public-harness lane used a newly prepared disposable BYO
worktree (`byo-final-proof-v3`). It had no `.venv` and no existing Stop
snapshot. Its receipt was verified; both the baseline and final Stop calls
passed; Codex exited `0`; the direct child was reaped; the owned process
boundary was empty; and no owned PID remained live.

The agent changed only `super_cache_probe.py` from `VALUE = 0` to `VALUE = 1`.
The final Stop evidence shows both real checks passed against that file:

- `ruff check super_cache_probe.py`: exit `0` (1.515 seconds)
- `pyright super_cache_probe.py`: exit `0` (5.155 seconds)

## Problems found and fixed

### Receipt enforcement was optional

Previously, the controller verified a supplied overlay receipt but allowed a
coding/subagent launch without one. The controller now requires a completed
receipt for the exact subagent worktree before a provider process can start.
Focused tests cover rejection without a receipt and acceptance with a matching
completed receipt.

This enforcement applies at the harness-controller boundary. A direct
`codex exec` launched outside the harness remains outside that boundary.

### Codex project trust was absent

The provider uses `--ignore-user-config`, which omits normal user-level trust
entries. As a result, a prepared worktree could contain `.codex/hooks.json`
without Codex loading it.

For a receipt-backed worktree, the provider now adds
`--dangerously-bypass-hook-trust` and a trusted-project override for that exact
worktree. The final lane's recorded provider argv contains both values.

### The PreToolUse matcher and timeout were wrong

The cache originally matched only `Bash`, while the harnessed Codex command
surface is `shell_command`. The matcher is now:

```json
"matcher": "^(Bash|shell_command)$"
```

The original three-second budget was too low for the Windows hook wrapper.
PreToolUse is now 15 seconds. A separate SessionStart context hook still had a
three-second timeout, so it was also changed to 15 seconds. The clean final
prepared worktree reports `[15, 15]` for SessionStart, `15` for PreToolUse,
and `300` for Stop.

An already-open Codex session can retain the old hook configuration. Exit and
reopen Codex once after the cache change; fresh prepared subagent worktrees
receive the new configuration.

### Prepared worktrees could not find Ruff or Pyright

Git worktrees normally do not contain the ignored primary-worktree `.venv`.
The Stop verifier initially searched only its own worktree, so it could not
find `ruff` or `pyright`.

It now reads `git worktree list --porcelain` and prepends available repository
worktree `.venv/bin` and `.venv/Scripts` directories to its child-process
`PATH`. The real proof deliberately used a worktree without `.venv` and the
primary BYO worktree's existing `.venv\Scripts\ruff.exe` and `pyright.exe`.

### Codex `exec` did not deliver lifecycle hooks

Real `codex exec` lanes did not create the expected project-hook lifecycle
artifacts, even with hook trust enabled. The cache-only Stop hook therefore
could not ensure Ruff/Pyright ran at the end of a harness provider run.

The controller now runs the cache's existing Stop verifier as a fallback at
the session-start baseline and after provider cleanup. This is the mechanism
used by the clean final proof above. It does not bound agent/subagent sessions;
it runs only the finite verifier commands selected by the cache configuration.

### The controller did not enable the Stop verifier

The cached script intentionally exits unless `AGENT_STOP_GATE_ENABLED=1`.
The new controller fallback initially omitted that environment variable, so
the script exited successfully without publishing a baseline snapshot.

The controller now copies its environment and sets that one variable before
invoking the verifier. Regression test:

```text
OverlayLaneSeamTests.test_prepared_stop_hook_enables_the_stop_gate: PASS
```

### The controller initially read the Stop-block result backwards

The cache's `Write-StopBlock` contract emits JSON with `"continue": false`
and exits successfully so the hook host can show the reason. The first
controller fallback checked for `"continue": true`, which would have treated
a real cache block as a pass.

`_run_prepared_stop_hook` now treats `continue is False` as `BLOCKED`; the
controller then records `CONTROLLER_FAILED` after provider cleanup. The
regression test feeds the exact `{"continue":false}` shape and now passes.

### Baseline snapshotting tried to hash a live harness output file

The first real fallback attempt found `.agent-workspace/*.codex.jsonl` while
it was locked by the provider. The script warned that it could not create its
baseline. A manually created prior snapshot could have hidden this, so that
attempt was not accepted as proof.

The snapshot logic now excludes `.agent-workspace/`, just as it already
excluded its own `.agent-runtime/stop-verify/` records. The final v3 proof
started with no snapshot and passed both boundaries with no warning.

### Disposable-proof setup failures

- The first detached proof launch named a runtime directory that did not yet
  exist. The controller rejected the invocation before creating a status file.
  The runtime root was created and the invocation was preflighted before the
  next launch.
- One disposable `v2` worktree was accidentally created from the harness
  repository rather than BYO. It was detected before any agent launch, then
  that exact disposable worktree and its branch were removed.
- An earlier broad focused-test command exceeded the tool's 64-second limit.
  Its exact test process was checked afterward and was gone. It is not counted
  as a passing test.

## Files changed and code fixes

| File | Change |
| --- | --- |
| `fresh-experiments/firmware-v2-20260821-active/subagent-hook-cache-source/.codex/hooks.json` | Matched both `Bash` and `shell_command`; raised PreToolUse and the remaining SessionStart timeout to 15 seconds; retained the 300-second Stop timeout. |
| `fresh-experiments/firmware-v2-20260821-active/subagent-hook-cache-source/.agent/stop-verify.ps1` | Finds repository worktree virtual environments; excludes harness-owned `.agent-workspace/` output from snapshots so an open JSONL cannot break the baseline. |
| `firmware-v2-harness-runner/super-cache/` | Regenerated from that source after every cache change; final ingest reports 21 entries and the staged/cached Stop-script hashes match. |
| `firmware-v2-harness-runner/orchestrator_harness/lane_controller.py` | Requires a receipt; verifies it before provider creation; supplies prepared-worktree trust data; runs the cached Stop verifier at baseline and post-cleanup; enables its gate; requires a baseline snapshot; and maps `continue: false` to a blocking lane result. |
| `firmware-v2-harness-runner/orchestrator_harness/provider.py` | Adds the receipt-backed prepared worktree trust override and hook-trust bypass to the Codex argv only for prepared lanes. |
| `firmware-v2-harness-runner/orchestrator_harness/tests/test_workspace_overlay.py` | Adds receipt-rejection, baseline/final Stop ordering, blocking Stop, gate-environment, and `continue: false` regression coverage. |
| `firmware-v2-harness-runner/orchestrator_harness/tests/test_provider_adapter_registry.py` | Checks the prepared-worktree Codex trust argv. |
| `firmware-v2-harness-runner/orchestrator_harness/tests/test_coding_lane_controller.py` | Prepares a genuine overlay receipt for its coding-lane fixture, matching the new launch requirement. |
| `super-cache-problems.md` | This problem/fix/evidence record. |

## Cache and code verification

- `workspace super-cache ingest`: completed with 21 entries after every source
  change; the final source and cached `stop-verify.ps1` SHA-256 values match.
- Final clean real lane: receipt verified; Stop baseline `PASSED`; Stop
  `PASSED`; Codex exit `0`; direct child reaped; helpers complete; owned
  boundary empty; no owned PIDs live.
- Focused gate-environment regression test: `PASS`.
- Focused Stop-block-polarity regression test: `PASS`.
- Focused receipt/Stop-order/Stop-block/provider-trust tests: `PASS` (4 tests,
  35.258 seconds).
- `python -m py_compile orchestrator_harness/lane_controller.py
  orchestrator_harness/provider.py`: `PASS`.
- `git diff --check` in `firmware-v2-harness-runner`: `PASS` (Git emitted only
  line-ending warnings).

The failed broad test command is intentionally not represented as a pass.
