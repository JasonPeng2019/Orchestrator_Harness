# Subagent CLI hooks: completed compatibility repair

> **Status: historical compatibility evidence, not the v2 queue protocol.**
> This file proves the three native CLIs execute PostToolUse hooks. Its candidate
> binding, coordinator, and multi-file router details do not carry into v2.

## Firmware v2 candidate readiness

The new firmware v2 candidate (`harness-single`) now supports real
project-local subagent hooks on all three shipped CLI hosts: Codex, Claude
Code, and Qwen Code. This is no longer a proposed or synthetic capability: a
native headless launch of each CLI executed a tool and produced the harness's
durable PostToolUse delivery record.

That closes the hook-feasibility question for the new-harness design. We can
now specify the revamp on the assumption that a fresh, explicitly bound
subagent lane can notify its registered manager at PostToolUse. The remaining
specification work is the harness's control-plane and recovery design, not
whether these shipped CLIs can run the required hook.

This conclusion is intentionally narrow. It proves the notification premise,
not every lifecycle hook in every provider mode, and it does not make hook
delivery an acknowledgement, a scheduler, or a replacement for manager-owned
state.

## Revamp compatibility decision

The new harness starts fresh v2 runtime roots. It does not open, migrate, or
preserve an existing candidate queue, binding, coordinator, or in-flight lane
record. Those existing records remain only archival/forensic evidence. The
proven candidate supplies one native-provider fact to retain: a lane can use its
own provider-local binding and hook configuration. V2 keeps that lane-specific
binding, but ROOT does not inherit the candidate's queue bind/fresh-session
lifecycle: its static hook wrapper uses the fixed runtime manager queue and the
generic current-epoch marker. V2 therefore carries no compatibility code for the
candidate's multi-file `ManagerEventRouter` records.

## Scope and decision

This record covers the shipped subagent CLI resources in the current
`harness-single` candidate:

- Codex CLI (`--host codex`)
- Claude Code CLI (`--host claude`)
- Qwen Code CLI (`--host qwen` or `--host qwen-code`)

All three now use the same setup contract. Installing a project adapter only
writes that provider's project-local hook configuration. It does **not** guess
a manager, create a queue, or bind the project automatically. The manager must
create the real `ManagerEventRouter`, then explicitly bind the prepared project
to that registered queue before a fresh provider session starts.

```text
install provider project files
    -> manager creates/registers its queue
    -> adapter bind records that exact queue identity
    -> fresh CLI subagent session executes a tool
    -> PostToolUse hook delivers a sparse manager notice
    -> manager retains the original event until explicit acknowledgement
```

This is deliberately small. A hook is not a scheduler, a second queue, an
automatic repair service, or an acknowledgement path.

## Public setup surface

The caller uses the provider that matches the launched CLI:

```shell
python -m orchestrator_harness adapter install --host <codex|claude|qwen> --project-root $lane
python -m orchestrator_harness adapter bind --host <codex|claude|qwen> --project-root $lane --queue-root $managerQueue
```

`--coordinator-root` remains optional. If it is omitted, the binding creates
only the provider-specific coordinator directory beneath the already-existing
manager queue. It never creates a manager queue.

`adapter bind` is safely repeatable only when the existing record is byte-for-
byte the same binding. It rejects a missing manager registration, a stale or
cross-bound record, a changed project/queue/coordinator directory identity, an
adapter revision mismatch, or a changed manager registration. The recovery is
to use the actual current manager queue and start a fresh provider session.
The one exception is the exact pre-v1 Claude record for those same binding
facts: an explicit Claude `adapter bind` migrates it to the closed v1 record.
It does not migrate malformed, changed, or cross-bound legacy records.

## Binding contents and hook semantics

Each provider writes one closed binding record inside its project directory:

| Provider | Binding file | Default coordinator folder |
| --- | --- | --- |
| Codex | `.codex/orchestrator-harness-binding.json` | `codex-coordinator` |
| Claude Code | `.claude/orchestrator-harness-binding.json` | `claude-coordinator` |
| Qwen Code | `.qwen/orchestrator-harness-binding.json` | `qwen-coordinator` |

Every record includes the adapter schema/version/package revision; project,
queue, and coordinator paths plus filesystem identities; and the exact
`run_id`, `queue_id`, manager session/thread/invocation IDs, registration ID,
and registration generation. The hook re-checks those facts against
`REGISTRATION.json` before it sends anything.

At PostToolUse, the installed hook reads only that bound queue and produces a
content-free delivery notice: pending count, highest class/severity, binding
identity, and timestamp. The durable delivery receipt has `outcome:
"DELIVERED"` when the provider hook boundary ran. It does **not** carry an
event payload, mark work complete, or acknowledge the manager event. The event
stays pending until the manager explicitly handles and acknowledges its
top-level event ID.

An installed but unbound project is a setup error. Codex, Claude, and Qwen now
all fail loudly with an `installed <provider> hook has no harness binding`
error instead of silently pretending delivery occurred.

## Provider-specific repairs

### Codex

Codex already had project hook assets but needed an explicit queue-binding
setup path. The completed repair binds the lane to the real manager queue,
stores a closed identity-checked record, and configures the native Codex
session to load the owned project hook fragment. It was live-proven through
`operator_launch -> lane_controller -> codex exec` with GPT-5.6 Luna at medium
reasoning: one `git status --short` tool call produced a durable PostToolUse
delivery receipt.

### Claude Code

Claude had an installer and hook scripts, but no public `adapter bind` command.
The repaired path adds `activate_claude_binding`,
`bind_claude_project_from_queue`, and `adapter bind --host claude`. It uses the
same closed binding validation as Codex and Qwen. The former unbound-hook
no-op has been removed: missing binding is visible and recoverable.

Claude Code 2.1.239 was live-proven through the native launcher with `claude
--print`, model `sonnet`, and `Bash` allowed. It ran `git status --short`,
returned `CLAUDE_HOOK_PROOF_COMPLETE`, and produced a durable `DELIVERED`
PostToolUse receipt for a real pending manager event.

### Qwen Code

Qwen now has the same explicit binding API and CLI path. Its actual headless
command is `qwen`, not the obsolete `qwen exec` shape. The controller resolves
the Qwen launcher before creating the isolated child process,
which prevents command-discovery failure. The safe base child environment also
retains the minimal non-secret platform environment variables the launcher needs; otherwise the CLI creates a
literal unresolved-environment-variable cache directory in the lane.

Qwen Code 0.21.10 was live-proven with the existing local
Ollama-compatible configuration selecting `deepseek-v4-flash:0731-cloud`. It
ran `git status --short`, returned `QWEN_HOOK_PROOF_COMPLETE`, and produced a
durable `DELIVERED` PostToolUse receipt. The harness neither read nor wrote
provider credentials.

## Live-proof conditions and limits

Each proof used a fresh ignored runtime root, a fresh Git lane, one real
registered manager queue containing one pending `MANAGER_SIGNAL`, and the
native `operator_launch -> lane_controller` route. The provider performed
exactly one harmless Git status command. The proof criterion was independent
of transcript wording: the manager's durable `DELIVERY.jsonl` and the bound
coordinator both recorded a `post_tool_use` receipt with `outcome:
"DELIVERED"`.

The source-checkout proofs granted only `PYTHONPATH` so the project-local hook
scripts could import the uninstalled harness package. A normal installed
harness does not need that temporary grant. The proofs establish the
PostToolUse path; they do not claim that every provider invokes every hook type
in every interactive, safe-mode, or disabled-customization configuration.

## Observable acceptance criteria

The repair is complete only when all of these remain true:

1. `adapter install`, `adapter check`, and `adapter bind` accept each shipped
   provider host and operate only inside the caller-selected project plus the
   already-existing manager queue/coordinator location.
2. Binding to an absent, stale, cross-bound, symbolic-link, or unregistered
   queue fails without redirecting the project to a synthetic queue.
3. A real headless tool call for each provider writes a durable
   `post_tool_use`/`DELIVERED` receipt for a real pending event.
4. The event remains pending after delivery; only the manager can acknowledge
   it.
5. A missing binding is an actionable error, not a success or a fake delivery.
6. The provider-specific launch form stays native: `codex exec`, `claude
   --print`, and `qwen`.

The provider-specific reproducible proof contracts live in
`harness-single/docs/codex-headless-hook-proof.md`,
`harness-single/docs/claude-headless-hook-proof.md`, and
`harness-single/docs/qwen-headless-hook-proof.md`.
