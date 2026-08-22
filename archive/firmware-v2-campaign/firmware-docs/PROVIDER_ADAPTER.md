# Firmware provider-adapter contract

> **Historical at closure (2026-08-21).** This records the final Firmware adapter configuration;
> it is not a live launch authority after the campaign closure.

This is the sole current authority for Firmware provider selection, model allocation, service-tier
rules, and adapter status. Other Firmware documents link here instead of duplicating launcher
configuration.

## Current status

The implemented Firmware-local route is Qwen Code 0.21.10 through Ollama's OpenAI-compatible
endpoint. Its project-only MCP and model configuration is
[`Firmware/.qwen/settings.json`](../../../Firmware/.qwen/settings.json); it contains no credential and registers the local
stdio server relative to this package. Each launch supplies `OLLAMA_API_KEY=ollama` only in its
process environment. It does not read or write a user-wide Codex or Qwen configuration.

The admitted target-lane entry point, run from `Firmware/`, is:

```powershell
$env:OLLAMA_API_KEY = 'ollama'
python scripts/orchestration/qwen_provider_bootstrap.py <canonical-invocation.json>
```

The bridge defaults to `Firmware/target-harness/`. A disposable target may be selected only by
setting `FIRMWARE_TARGET_HARNESS` to its package-local path before the bridge starts; the invocation
still declares and validates the exact target worktree. This is for isolated lanes, not a global
configuration setting.

`scripts/orchestration/qwen_provider_bootstrap.py` is a Firmware-owned external adapter, not WIP
product code. It registers `qwen-code` with the target's existing provider registry in the same
controller process, then delegates the lane lifecycle to the target. It uses Qwen's stream-JSON
protocol, sends the task card on standard input, and launches Qwen with `--approval-mode=yolo`.
It reads the package-local model/MCP settings, passes the selected Ollama endpoint and local
non-secret `ollama` API-key placeholder explicitly, and passes an inline MCP configuration with
the BYO server's working directory pinned to `Firmware/`. This avoids dependence on a user-wide
Qwen settings file while letting the target worktree remain the agent's working directory.
The configured models are `deepseek-v4-flash:0731-cloud` and `qwen3.5:397b-cloud`.

Disposable no-hardware direct Qwen smokes passed for both models. The bridge's focused unit test
and a disposable no-tool **target-lane** smoke then passed: the target launched DeepSeek through
Qwen, Qwen registered/listed the local BYO MCP server, returned the exact response without a tool
call, and the target reaped the complete process boundary. No connection, setup, validation, action,
flash, reset, serial, write, discovery, lease, or other hardware operation occurred.

Codex 0.147.0 is not an admitted primary Firmware route. Its DeepSeek/Ollama probe exposed the server
only as an opaque namespace and repeated unsupported MCP calls; its Qwen/Ollama probe exhausted
provider connection retries before reaching MCP. The one narrow exception is the named-doer
backend-failure fallback declared below: it uses direct `luna-high`, not either failed Ollama
projection, and must pass its dedicated no-hardware target-lane smoke before first use. Historical imported launcher copies under
`Firmware resources/test-program/` are not configuration or a live route.

This is a provider route, not hardware authority. Current hardware authority is recorded in
`.agent-workspace/USER_DELEGATED_AUTHORIZATION.md`; the suite still must create its fresh epoch,
verify the package-local target, obtain exact leases, and pass the server's normal plan/permission
checks before it operates a board.

## Context-compaction settings

The selected provider route must set and record the effective automatic-compaction threshold for
each launch when its CLI exposes that setting:

| Firmware role | Automatic-compaction threshold |
|---|---:|
| Acceptance/test orchestrator (Sol) | 280,000 tokens |
| Named application/test doer (Atlas, Boreal, Cygnus, Delta, Nova) | 180,000 tokens |
| Named-doer `luna-high` backend-failure replacement | 150,000 tokens |
| Any Firmware Terra role, including the ROOT sprint-evidence reviewer | 230,000 tokens |

The five named DeepSeek doers use the package-local Qwen home in `.qwen/`. Its declared
1,048,576-token context window and `context.autoCompactThreshold` fraction produce the exact
180,000-token automatic-compaction trigger. The bootstrap sets `QWEN_HOME` only in its own process
environment before launching Qwen, so neither reasoning effort nor compaction changes user-wide
Qwen configuration. The target-lane smoke must record whether the selected route exposes and
applies this setting. It must not claim a threshold the provider did not actually accept.

## Logical role allocation

| Firmware role | Primary model | Reasoning | Backend fallback | Service tier | Scope |
|---|---|---|---|---|---|
| Acceptance/test orchestrator | Sol | low | none | product-owned | Schedules the suite; never reads ROOT's harness-evidence review. |
| Named application/test doer | `deepseek-v4-flash:0731-cloud` | high | `luna-high` after three consecutive eligible failures | none primary; Fast (priority) fallback | Implements substantial catalog firmware/test code; its provider session is replaceable through a structured handoff. |
| Firmware-MCP reviewer | `qwen3.5:397b-cloud` | provider-selected | none | none | One persistent, read-only reviewer per sprint/module; replace it with recorded continuity when required. |
| BYO-Firmware-MCP server implementer | `deepseek-v4-flash:0731-cloud` | max | none | none | Separate source writer, admitted only after the test orchestrator verifies a production-server defect. |
| Server-repair test/scaffolding role | `deepseek-v4-flash:0731-cloud` | high | none | none | Tests/scaffolding only; never replaces the server implementer. |
| ROOT sprint-evidence reviewer | Terra XHigh | xhigh | none | Fast (priority) | ROOT-only review after the terminal suite handoff; it is outside Firmware suite state. |

For Atlas, Boreal, Cygnus, Delta, and Nova, `luna-high` resolves to `gpt-5.6-luna` with high
reasoning, a 272,000-token context window, and a 150,000-token total automatic-compaction trigger.
`HTTP_429`, `HTTP_303`, `RATE_LIMIT`, and `BACKEND_ERROR` are eligible backend-connection classes.
The first and second consecutive eligible failures retry the unchanged DeepSeek route. After the
third, the terminal DeepSeek attempt publishes a structured handoff and a fresh Codex invocation
continues the same named logical role, task card, verified checkpoints, evidence, and first
unresolved action on `luna-high`. A successful or ordinary non-backend terminal attempt breaks the
consecutive-failure streak. No other error class selects this fallback.

DeepSeek and Qwen do not receive a Fast/Priority service-tier setting. The product-harness
implementer/reviewer configuration is separate and unchanged; this contract does not modify it.

## Active adapter and launch requirements

Qwen Code is the active primary Firmware route. Codex is admitted only for the exact named-doer
`luna-high` backend-failure fallback after its dedicated no-hardware target-lane smoke passes. This
does not permit any other substitution of a model, effort, role, or suite ownership.

The Qwen adapter must, before any provider session starts:

1. record the chosen route, model, reasoning level, logical role, provider-session identity, target
   worktree/run root, and parent/controller identity;
2. use the existing WIP `target-harness/` provider/lane lifecycle for Firmware sprint roles rather
   than a second Firmware scheduler or controller;
3. make its approval/sandbox policy explicit, rather than inheriting unrelated user configuration;
4. preserve the named logical role and durable task checkpoint; for Atlas, Boreal, Cygnus, Delta,
   and Nova, reuse the same valid session by default across task and completed-sprint boundaries
   when the role/model selection is unchanged. Keep it idle at manager/ROOT decision boundaries
   until a new card explicitly resumes it. If it is unavailable or remapped, record the old-session
   absence/terminal state and use a structured
   handoff to a fresh session—session continuity is never required for logical-sprint continuity;
   and
5. complete a host-only smoke test before any MCP, hardware, or production-server action.

Before each provider invocation, resolve and record its role, route, command shape, target, and
provider registration. Keep those inputs fixed for that invocation. If one must change, publish a
continuity handoff and use a fresh invocation for the same logical sprint; do not discard verified
work. A malformed non-mutating call may be corrected to the recorded shape. Never retry an unchanged
supervisor failure.

Qwen profiles must include the safe `SYSTEMDRIVE` provider environment need on Windows. It is not a
credential or hardware grant; it prevents Qwen from treating the literal `%SystemDrive%` string as
a relative directory inside an isolated target worktree.

For every Firmware role, that explicit policy must require full local worktree/command access and
no interactive command approval. A Codex route must use
`--dangerously-bypass-approvals-and-sandbox`, `--ignore-user-config`,
`approval_policy="never"`, and `approvals_reviewer="user"`; another provider route must record and
prove its equivalent unrestricted/no-approval settings, or fail closed before launch. The required
host-only smoke must show the effective settings for the selected route. This is not hardware
authority: the server's hardware plan, user permission, resource lease, and safety controls remain
independent and mandatory.

## Full-access invocation reference

This section is the launch-policy reference. It describes process access only; it does not
authorize hardware, expand a role's task card, or permit an adapter to bypass the required
target-lane smoke.

| Route | Required full-access form | Notes |
|---|---|---|
| Qwen Code fallback | `qwen --approval-mode=yolo ...` | `--yolo` is an equivalent compatibility form; use one form, not both. Do not add Qwen's `--sandbox` mode for a full-host-access lane. Record the effective approval mode and executable arguments. |
| Codex CLI | `codex exec --dangerously-bypass-approvals-and-sandbox --ignore-user-config -c approval_policy="never" -c approvals_reviewer="user" ...` | This is the explicit unattended full-access route. Keep model, reasoning, session/resume, output, working-directory, and bounded-card arguments outside this policy fragment. |
| Codex controller/configuration route | `sandbox_mode = "danger-full-access"` and `approval_policy = "never"` | Use only when the adapter passes these settings directly to Codex and the smoke proves they are effective. Record the final resolved settings; no inherited user configuration may weaken or replace them. |

For Codex, the adapter may use either listed Codex form, but it must not treat Qwen's `--yolo` spelling
as a Codex flag: the current Codex CLI's full-access/no-approval switch is
`--dangerously-bypass-approvals-and-sandbox`. For Qwen, YOLO auto-approves tool calls and, without
Qwen sandbox mode, tools run at the host process's privilege level. The adapter must record the
selected form verbatim and have its host-only smoke reject a missing, contradictory, or weaker
setting before any provider, MCP, production-server, or hardware action.

The adapter must not let the Firmware test orchestrator read or act on ROOT's
sprint-evidence-review report. It also must not bypass the server's hardware plan, permission, or
safety controls.
