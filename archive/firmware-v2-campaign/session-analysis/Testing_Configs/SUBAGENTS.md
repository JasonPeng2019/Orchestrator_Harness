# Superseded delegate prototype — do not use to launch the active workflow

This directory is retained only as design source material. Its launcher resolves the
wrong repository root and its profiles contain historical allocations. Do not run it
for this harness or treat its settings as active. The active workflow uses the
versioned role/profile registry at
`plans/general-coding-harness/SUBAGENT_ROLE_MODEL_MAPPING.json`, resolved only by
`.codex/scripts/stable_runner.py`; current settings, fallback admission, and the
current S6 P02 handoff are recorded there and in `HANDOFF.md`.

# Historical external Codex delegates

## Scope boundary

This is a historical development-only guide for an earlier external Codex delegate workaround. It does not
define the product harness's provider support or its role mapping. The future product requirement
is the post-S6 provider-adapter deliverable in
`plans/general-coding-harness/FULL-EXECUTION-SPEC_PLAN_2.md`: it must ship Codex and Claude Code
adapters and admit another CLI through a small truthful registered adapter. Until that deliverable
is implemented and accepted, this guide must not be read as evidence that the product supports a
provider or CLI.

This repository contains self-contained configurations and a launcher for two
persistent external Codex delegates:

| Delegate | Model | Context window | Automatic compaction |
| --- | --- | ---: | ---: |
| `luna` | `gpt-5.6-luna` | 272,000 | 150,000 |
| `deepseek` | `deepseek-v4-flash:0731-cloud` via Ollama | 1,048,576 | 230,000 |

The context window is the model capacity. The automatic-compaction threshold is
the smaller point at which Codex summarizes history. Both are explicit in the
delegate profile, so they do not use Codex's model defaults.

This external-delegate pattern is the intended local workaround for DeepSeek:
project-local native-agent configuration cannot route a native child to an
Ollama provider. A native child thread and an external Codex delegate are
therefore different things; the latter is the supported option here without
adding an MCP server.

## Run or continue a delegate

From the repository root in PowerShell. The `-ExecutionPolicy Bypass` here is
process-local: it does not change your Windows execution-policy setting.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Invoke-CodexDelegate.ps1 luna "Inspect this repository and report the most important risks."
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Invoke-CodexDelegate.ps1 deepseek "Implement the requested change and run the relevant tests."
```

The first invocation creates a delegate session and records its Codex thread ID
under `.codex/delegates/sessions/`. Every later invocation with the same agent
name resumes that same conversation, including its prior task context. To
discard that context and intentionally start a new conversation, pass `-New`:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Invoke-CodexDelegate.ps1 luna -New "Start a fresh investigation of the repository."
```

This launcher defaults to persistence; the workflow does not require it. When a
user changes the subagent/provider allocation or the prior session cannot resume,
start the selected replacement with a structured handoff containing the same
workflow role, bounded task card, accepted state, complete evidence, source
identity, and first unresolved action. Record the old/new session identities when
available. Do not use `-New` as a reason to restart completed work or create a
new product loop.

Add `-ReadOnly` for analysis tasks that must not edit the workspace:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Invoke-CodexDelegate.ps1 luna -ReadOnly "Review the current configuration."
```

The process runs in the repository root with workspace-write access by default.
Its response is printed in the terminal that launched it. These are persistent
external Codex sessions, not native child threads in the Codex Subagents UI.
That distinction is necessary because the native subagent launcher does not
admit Luna or this custom Ollama model as child models.

## Where the settings live

- `.codex/delegates/luna.toml` is Luna's complete launch profile.
- `.codex/delegates/deepseek.toml` is DeepSeek's complete launch profile.
- `.codex/delegates/deepseek-model-catalog.json` supplies DeepSeek's one-million-token model metadata to Codex.
- `scripts/Invoke-CodexDelegate.ps1` reads a profile and passes its settings to `codex exec`.
- `.codex/delegates/sessions/<agent>.json` is the repo-local pointer to that delegate's persistent Codex session.

Edit `model_auto_compact_token_limit` in the applicable TOML file to choose a
different compaction threshold. Keep it below the matching `model_context_window`.

## Isolation from global configuration

The launcher always passes `--ignore-user-config`, so it does not inherit model,
provider, or compaction settings from `C:\Users\Jason\.codex\config.toml`.
It still uses Codex's existing local sign-in for OpenAI authentication; this is
required for Luna and does not read or modify the global configuration file.

DeepSeek uses Codex's built-in Ollama provider (`--oss --local-provider ollama`)
and expects its server at the usual local endpoint, `http://127.0.0.1:11434`.
Start the Ollama service and make sure the `deepseek-v4-flash:0731-cloud` model
is available before launching that delegate.

## Verification

Run these two smoke tests after changing the launcher or profiles:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Invoke-CodexDelegate.ps1 luna "Reply exactly: LUNA_DELEGATE_OK"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Invoke-CodexDelegate.ps1 deepseek "Reply exactly: DEEPSEEK_DELEGATE_OK"
```

Each Codex startup banner should show the intended model and provider. The
launcher prints the requested compaction threshold before it starts Codex.

## Parallel DeepSeek capacity

On 2026-08-12, a four-way smoke test sent four independent, minimal requests to
`deepseek-v4-flash:0731-cloud` concurrently through this machine's Ollama
endpoint. All four succeeded, each in 6.3–6.8 seconds, with no `429` rate-limit
or `503` overload error. This confirms the account and endpoint accepted four
simultaneous small requests at that time.

It is not a promise that four long-running coding agents will have the same
latency or never be rate-limited: provider load, account limits, prompt size,
and the 230,000-token compaction threshold all affect capacity. Also, do not
run several tasks through the same named `deepseek` session concurrently. Each
parallel delegate needs its own session ID and state file so that their contexts
do not collide.
