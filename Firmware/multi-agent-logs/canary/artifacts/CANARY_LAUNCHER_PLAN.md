# Canary lane-controller repair plan

Status: accepted for implementation

## Problem

The cleaned repository correctly contains no stale launcher wrapper, but a real canary epoch still
needs a small, auditable process controller so the required read-only `orchestrator_harness` can
observe externally launched persistent Luna doers. Direct shell launches do not provide the
controller PID/child PID/thread identity and durable state transitions required by the harness.

## Scope

Implement one reusable controller inside `orchestrator_harness/`, not in root `.agent-workspace`
or an experiment run. It launches exactly one Codex turn and writes only its assigned run's
`.agent-workspace/<label>_*` controller/output files plus the manager-selected aggregate lane log.
It does not schedule, assign leases, approve hardware, start the MCP server itself, or edit suite
state.

## Required behavior

1. Accept a UTF-8 JSON invocation file containing action (`start` or `resume`), run root, prompt
   path, label, task/doer/lane/phase, leases/resources, immutable server snapshot, model settings,
   optional resume thread ID, optional repeated Codex `-c` overrides, and output paths.
2. Verify all resolved writable paths remain within the assigned run workspace except the explicit
   aggregate lane-event log under root `.agent-workspace/ORCHESTRATOR_HARNESS/`.
3. Invoke `codex exec` (or `codex exec resume`) with the policy-bound prompt on stdin, never on the
   Windows command line. Require:
   `--dangerously-bypass-approvals-and-sandbox`, `--ignore-user-config`,
   `--skip-git-repo-check`, `approval_policy="never"`, `approvals_reviewer="user"`, JSONL,
   the requested model/reasoning/tier, and no ephemeral session.
4. Atomically publish `RUNNING_CODEX` only after obtaining distinct controller and child process
   identities/creation times. Stream exact JSONL without buffering, parse `thread.started`, and
   atomically add the thread ID to status.
5. End in `CODEX_EXITED` with exit code and timestamps. Use `LAUNCH_FAILED`,
   `CONTROLLER_INTERRUPTED`, or `CONTROLLER_FAILED` truthfully. Exit zero from Codex without a
   thread ID is a launch failure.
6. Preserve one thread ID across later `resume` turns; reject a resume without one.
7. Append compact lifecycle events to the explicit aggregate lane log without copying full model
   output into root state.
8. Provide focused host tests using a fake Codex executable for start, resume, required flags,
   stdin, thread parsing, terminal states, malformed invocation, path escape, and missing-thread
   failure. Tests must not call a model, MCP server, or hardware.

## Acceptance

- Focused controller tests are green.
- Existing `orchestrator_harness` host tests remain green.
- A manager-owned fake smoke launch proves the harness discovers the controller and the controller
  reaches a truthful terminal state.
- No production server, experiment evidence, or hardware is mutated by implementation testing.

## Pre-live review amendment 001

The first implementation passed its focused and full host suites, but main review found that it
only required a non-empty prompt. Before any real model launch it must enforce the suite's actual
policy-binding contract rather than trusting the invocation writer:

1. require `policy_sha256` and `prompt_sha256` in the invocation;
2. verify the canonical root policy file and sidecar both equal the required policy SHA;
3. verify the exact prompt bytes equal `prompt_sha256` and contain the policy helper's authoritative
   banner, matching SHA, end marker, and final precedence reminder;
4. record prompt path/hash, policy path/hash, action, board tokens, and MCP server names in status;
5. add focused negative tests for raw/unbound prompt, changed prompt, and policy/hash mismatch.

This is a functional launch-integrity gap, not gold-plating: without it, a controller can mark an
unbound prompt as an unrestricted suite role even though the skill expressly forbids that launch.
