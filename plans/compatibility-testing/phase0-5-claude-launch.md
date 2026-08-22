# Launching Claude Code subagents against the local Ollama backend

How the phase-0–5 subagents are launched as `claude` CLI sessions pointed at a **local
Ollama** backend (model `deepseek-v4-flash:0731-cloud`), and — critically — how that launch is
**fully session-local**: it never touches `~/.claude`, never runs `claude config set`, never
edits any global Claude Code settings, and never contacts the Anthropic API.

This is the mechanism used for every phase-0 step (0.1–0.5) and the intended mechanism for
phases 1–5 (Phase 5 = live emission of the 7 residual notification/event rows). It is the same launcher documented in the plan README
(`plans/compatibility-testing/README.md` §3) and in the memory note
`subagent-launch-local-only`.

---

## 1. The launcher (one command, one subprocess)

Git-Bash form (what the coordinator uses):

```bash
cd "C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test" \
  && mkdir -p .subagent-scratch-XX \
  && ANTHROPIC_BASE_URL=http://localhost:11434 \
     ANTHROPIC_AUTH_TOKEN=ollama \
     ANTHROPIC_API_KEY= \
     CLAUDE_CONFIG_DIR="C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test/.subagent-scratch-XX" \
     CLAUDE_CODE_AUTO_COMPACT_WINDOW=180000 \
     CLAUDE_CODE_MAX_CONTEXT_TOKENS=200000 \
     claude --print --output-format stream-json --verbose \
       --model deepseek-v4-flash:0731-cloud --permission-mode bypassPermissions \
       --effort high \
       < "C:/Users/Jason/Documents/Jason/Orchestrator_Harness/plans/compatibility-testing/evidence/0.X/subagent.prompt.md" \
       > "C:/Users/Jason/Documents/Jason/Orchestrator_Harness/plans/compatibility-testing/evidence/0.X/subagent.stdout.jsonl" \
       2> "C:/Users/Jason/Documents/Jason/Orchestrator_Harness/plans/compatibility-testing/evidence/0.X/subagent.stderr.log"
```

PowerShell form (same effect; env vars are process-scoped and removed after):

```powershell
$env:ANTHROPIC_BASE_URL = "http://localhost:11434"
$env:ANTHROPIC_AUTH_TOKEN = "ollama"
$env:ANTHROPIC_API_KEY = ""
$env:CLAUDE_CONFIG_DIR = "C:\Users\Jason\Documents\Jason\Orchestrator_Harness\harness-single-worktrees\compat-test\.subagent-scratch-XX"
$env:CLAUDE_CODE_AUTO_COMPACT_WINDOW = "180000"
$env:CLAUDE_CODE_MAX_CONTEXT_TOKENS = "200000"
claude --print --output-format stream-json --verbose --model deepseek-v4-flash:0731-cloud --permission-mode bypassPermissions --effort high < prompt.md > stdout.jsonl 2> stderr.log
Remove-Item Env:ANTHROPIC_BASE_URL, Env:ANTHROPIC_AUTH_TOKEN, Env:ANTHROPIC_API_KEY, Env:CLAUDE_CONFIG_DIR, Env:CLAUDE_CODE_AUTO_COMPACT_WINDOW, Env:CLAUDE_CODE_MAX_CONTEXT_TOKENS
```

Alternative launcher (equivalent, from the findings doc):

```bash
ollama launch claude --model deepseek-v4-flash:0731-cloud -- --dangerously-skip-permissions
```

**Requirements:** Ollama v0.14.0+ running locally with the model pulled
(`ollama pull deepseek-v4-flash:0731-cloud`). The `claude` binary is the real CLI
(`C:\Users\Jason\.local\bin\claude.exe`).

---

## 2. Why it does not interfere with Claude outside this session

Four independent layers keep everything local:

### 2.1 Process-scoped env vars (the Ollama redirect)

`ANTHROPIC_BASE_URL=http://localhost:11434`, `ANTHROPIC_AUTH_TOKEN=ollama`,
`ANTHROPIC_API_KEY=` (empty) are set **only for that one subprocess and its children**. They
are not exported to the parent shell, not persisted to any file, and die with the process.

- The redirect means the subagent talks to **local Ollama**, never to the Anthropic API — no
  Anthropic account, no cloud quota, no real-model billing.
- The only quota that can be consumed is the **Ollama account's own session usage limit**
  (this is what blocked step 0.5 on 2026-08-18 — a 429 from Ollama, not from Anthropic).

### 2.2 `CLAUDE_CONFIG_DIR` → scratch dir inside the disposable clone

`CLAUDE_CONFIG_DIR` points at `.subagent-scratch-XX/` **inside the clone**. This redirects
every internal write Claude Code makes — `backups/`, `projects/`, `sessions/`,
`shell-snapshots/`, `tasks/`, `session-env/` — into that scratch dir instead of the default
`~/.claude`. Verified: the scratch dirs contain exactly those subdirectories, and `~/.claude`
mtimes were unchanged across all phase-0 runs.

The scratch dirs are git-ignored (`.subagent-scratch*/` appended to the clone's `.gitignore`),
so they never pollute the repo.

### 2.3 Per-invocation CLI flags only

Everything the subagent needs is passed as flags on the one command line (`--model`,
`--permission-mode`, `--print`, `--output-format`, `--verbose`). **No `claude config set`, no
`settings.json` edits, no `~/.claude` writes, no global config mutation of any kind.**

**Effort is pinned per launch with `--effort high`.** Every subagent runs at `high` — never
`max`/`xhigh`, and never inherited from the parent session's effort level (the flag is set
explicitly on the command line, so the subagent's effort is identical no matter how the
launcher session itself was configured). If a step ever needs a different level, the change is
made on that one launch line only — never stored, never applied globally.

**Auto-compaction is pinned per launch too**, alongside the effort flag, as process-scoped env
vars (same isolation guarantees as §2.1):

- **`CLAUDE_CODE_AUTO_COMPACT_WINDOW=180000`** — fixed 180k-token auto-compact pin (fires during
  `--print` runs so a long test/build subagent compacts deterministically rather than at an
  ambient default).
- **`CLAUDE_CODE_MAX_CONTEXT_TOKENS=200000`** — context ceiling under which the 180k pin sits.

Both are set only for the one subprocess, are never written to `~/.claude` or any settings
file, and die with the process. This is the identical envelope used for phases 0–4 and 5.

### 2.4 Nested claude spawns are isolated too

When a subagent drives the harness (e.g. `disposable_claude_coding_fixture.py`), the lane
controller spawns its own `claude` subprocesses. Those are also sandboxed:

- The controller builds an **isolated child environment** (allow-list filtering) and the
  phase-0.3 fix merges the declared `ANTHROPIC_*` overrides **after** that isolation — so only
  the explicitly declared redirect reaches the child, never inherited ambient secrets.
- The lane profile declares `provider_needs: ["CLAUDE_CONFIG_DIR", "HOME"]`, keeping Claude's
  config/home under caller control (the scratch dir survives the scrub).

---

## 3. What the launcher does NOT do

| Concern | Guarantee |
|---|---|
| Touches `~/.claude` | Never — `CLAUDE_CONFIG_DIR` redirects all writes into the clone's scratch dir |
| Runs `claude config set` / edits global `settings.json` | Never |
| Contacts the Anthropic API | Never — `ANTHROPIC_BASE_URL` points at `localhost:11434` |
| Persists env vars beyond the subprocess | Never — process-scoped (incl. `CLAUDE_CODE_AUTO_COMPACT_WINDOW=180000` / `CLAUDE_CODE_MAX_CONTEXT_TOKENS=200000`), gone on exit |
| Inherits parent effort / auto-compact settings | Never — `--effort high` and the 180k/200k pins are set explicitly per launch, identical regardless of the launcher session's own config |
| Writes outside the clone + evidence dir | Never — subagents are instructed to work only in the clone and `plans/compatibility-testing/evidence/` |
| Modifies `Firmware/target-harness` | Never — the clone is a separate worktree; the source tree stays read-only |

---

## 4. How to verify isolation after a run

- `~/.claude` mtimes unchanged (no new files/dirs under it).
- The scratch dir `.subagent-scratch-XX/` contains the session's `backups/projects/sessions/…`.
- `git -C <clone> status` shows only the intended uncommitted changes; `.subagent-scratch*/`
  is ignored.
- The subagent's stdout is a `stream-json` transcript ending in a `result` envelope (the final
  report lives in that envelope's `result` field); stderr is captured separately.

---

## 5. Output capture pattern (coordinator)

- **Prompt** → stdin (from `evidence/<step>/subagent.prompt.md`).
- **stdout** → `evidence/<step>/subagent.stdout.jsonl` (stream-json; the last `result` line
  carries the subagent's final report).
- **stderr** → `evidence/<step>/subagent.stderr.log`.
- The coordinator extracts the report with
  `PYTHONIOENCODING=utf-8 python -c "…"` over the `result` lines, then independently verifies
  the diff + evidence before accepting the step.
