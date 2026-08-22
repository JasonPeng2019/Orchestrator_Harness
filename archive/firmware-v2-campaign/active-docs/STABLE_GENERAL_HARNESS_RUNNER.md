# Stable General Harness Runner

> **Archived at closure (2026-08-21).** This reference does not authorize a new Firmware or Plan 2
> run. The published WIP handoff is [`HANDOFF.md`](../HANDOFF.md).

Status: reference documentation for the current ROOT-side launch bridge. This page
describes `.codex/scripts/stable_runner.py`; it does not replace the current run
authority in `goal.md`, `HANDOFF.md`, or
`plans/general-coding-harness/FULL-EXECUTION-SPEC_PLAN_2.md`.

## Purpose

The stable general harness runner is a small, fail-closed boundary between the
mutable repository and the pinned `stable-general-harness-runner` checkout. It
lets ROOT use selected, known-good harness entry points without importing code
from a candidate or from the caller's Python environment.

It also provides the current runtime bridge for:

- proving that the stable checkout is exactly the approved immutable revision;
- resolving a workflow role through the single editable role-model mapping;
- projecting a candidate coding invocation into the schema understood by the
  stable checkout;
- dispatching an approved stable module; and
- temporarily installing bounded-test enforcement in a real Codex worker's
  worktree, then restoring the worktree exactly.

It is deliberately a launch bridge, not a scheduler, a workflow engine, a
replacement supervisor, or a product implementation. The lane controller owns
the launched provider session; that session is lane-managed rather than placed
under a bounded-test lifetime.

## Stable-checkout and import protection

Before projection or module dispatch, the runner reads the stable-runner lock
and rejects anything except the expected lock schema, checkout name, and
detached commit. It then proves that the checkout:

- is a real directory rather than a symlink;
- is a Git top-level directory;
- is at the locked commit;
- has no tracked or untracked changes; and
- has detached `HEAD`.

After that proof, it accepts only these stable modules:

| Module | Function |
| --- | --- |
| `orchestrator_harness.cli` | Stable command-line entry point. |
| `orchestrator_harness.operator_launch` | Stable operator launch entry point. |
| `orchestrator_harness.lane_controller` | Stable lane-controller entry point. |

All other module names are refused. Before importing an allowed module, the
runner removes ambient Python import variables, limits `sys.path` to the
stable checkout and standard-library locations, and rejects a conflicting
preloaded `orchestrator_harness` module. It also proves that both the package
and selected module were imported from the stable checkout.

The runner emits a `STABLE_RUNNER_PROOF` record to standard error for each
validated projection or module dispatch. An optional proof file is allowed only
outside the stable checkout and is create-only: existing evidence is never
overwritten.

## Invocation projection

The `--project-invocation` mode converts an input invocation into a
stable-compatible invocation. It first resolves the requested workflow role
from `plans/general-coding-harness/SUBAGENT_ROLE_MODEL_MAPPING.json`, then
applies the selected profile's model, reasoning effort, service tier, Codex
flags, and safe context/compaction overrides.

Every outer workflow role has one enforced local launch policy, independent of
its model profile: the input must declare `sandbox: "danger-full-access"` and
`approval_policy: "never"`, or projection refuses it. For a real Codex command,
the bridge also adds `--dangerously-bypass-approvals-and-sandbox` and
`--ignore-user-config`, then writes the matching `approval_policy="never"` and
`approvals_reviewer="user"` overrides. Thus a DeepSeek, Luna fallback, Terra,
or Sol role cannot silently inherit a restricted sandbox or interactive command
approval setting. This local execution policy does not authorize hardware or
override any Plan, resource, or user-approval gate.

The input must be either a schema-less firmware invocation or an
`orchestrator-coding-invocation/v1` object with only the fields the stable
checkout can consume. Unknown fields are refused. For coding invocations, the
candidate-only `finding_gate` and `child_environment_isolation` fields may be
removed from the projected input only after their shape is validated. The
projection record preserves their field names and value hashes, records the
source and projected-file hashes, role, chosen profile, and the stable commit.
It explicitly says that ROOT must validate the retained candidate artifacts and
triage before accepting a lane result.

Projection output and its record are create-only, so a later invocation cannot
silently replace earlier evidence. Neither may be placed inside the immutable
stable checkout.

## Role and launch-profile selection

The role-model mapping is data, not launch code. The runner validates the
mapping's closed schema, each profile, its optional context settings and model
catalog path, and each role's primary/fallback relationship before using it.
This permits a role allocation to be adjusted without modifying the runner.

By default, the role's primary profile is selected. A declared fallback profile
is accepted only when a supplied backend-failure history proves the configured
number of consecutive primary-profile backend failures, each in one of that
role's configured error classes. The history must name the same workflow role
and have the expected closed schema. A fallback coding invocation must use a
new `action: "start"` handoff; it cannot resume a prior provider session.

For safe, content-free failure handling, `--classify-backend-error-file` has a
separate mode that emits only a recognized backend-error class (HTTP 429, HTTP
303, rate-limit, or backend/upstream/service failure) and a SHA-256 of the
input. It does not dispatch a module or accept projection/profile options.

## Dispatch behavior

For ordinary stable module dispatch, the runner passes the remaining arguments
to the allowed stable module's `main` function. `None` means success and an
integer is returned as the process exit code; any other return type is refused.

Lane-controller dispatch has additional safeguards:

1. It requires `--workflow-role` and an invocation file.
2. It resolves the current role allocation immediately before dispatch, rather
   than trusting model settings materialized in an earlier artifact.
3. A real Codex invocation must point to a prompt containing both
   `BOUNDED-TEST-v1` and `Invoke-BoundedTest.ps1`.
4. It writes the resolved invocation only to a temporary directory and passes
   that temporary path to the stable controller. The source invocation remains
   unchanged.

The runner returns exit status 2 after printing `stable runner refused: ...`
for its own validation, I/O, or value errors. It does not claim that a provider
result is accepted; ROOT still validates the returned result, dependency map,
commit ancestry, checks, cleanup, and claim release.

## Temporary Codex bounded-test overlay

When the resolved lane invocation launches the real `codex` executable, the
runner requires its `run_root` and temporarily merges entries into
`<run_root>/.codex/hooks.json`:

- a `SessionStart` hook loads the bounded-test adapter; and
- a `PreToolUse` hook matches `Bash` and `shell_command` so covered nested
  commands are enforced.

The overlay is written atomically and read back. During the controller call,
the runner supplies a process-local Git exclude for `/.codex/hooks.json`; the
temporary injection therefore does not appear as a project change. On every
exit path it restores the original hook file byte-for-byte, or removes the hook
and newly created `.codex` directory when neither existed beforehand. It also
restores the prior `GIT_CONFIG_*` environment. Failure to establish or restore
the overlay is a refusal, not a best-effort warning.

The overlay governs covered commands *inside* the Codex session. It does not
wrap the stable-runner/lane-controller/provider session itself in
`Invoke-BoundedTest.ps1`, and it does not change the policy boundary for direct
executables, PowerShell command text, or MCP calls.

## Operational limits

- Use it only through its documented projection, classification, or
  allowlisted-module paths; it is not a general Python-module launcher.
- Do not put evidence outputs or generated projections in the stable checkout.
- Do not treat a successful runner exit as product acceptance or as permission
  to skip lane-result and integration checks.
- A terminal test/check invocation is not permission to integrate. ROOT must
  accept its handoff and dispatch a separate exact integration invocation; a
  later mapped doer may perform only that authorized mechanical operation.
- Do not rely on a prompt alone for bounded execution: real Codex dispatch
  requires the prompt markers and installs the temporary hook overlay.
- Treat a runner refusal as evidence that a required precondition is missing or
  unsafe. Correct the stated condition before trying again; do not bypass the
  stable or bounded-execution protections.

Source: `.codex/scripts/stable_runner.py`.
