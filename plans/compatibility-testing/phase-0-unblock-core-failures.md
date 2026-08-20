# Phase 0 — Unblock: fix + re‑test the 4 confirmed failures

These are the **TESTED‑FAILED** rows. They are already known‑broken, but they gate
every TB‑SC row (a lane that can't launch produces no results/events to validate). Each
step here: (a) reproduces the failure against the real CLI, (b) applies the minimal fix
in the disposable clone, (c) re‑tests to confirm the fix, (d) adds a regression test.

Covers inventory rows: **A1, U1, U2** (§1) · **U3** (§2) · **C17, U4** (§3) · **A17** (§4).
Also directly re‑exercises **B19** (exit‑code contract) and **U14/U15** (transcript parse).

Fix locations (from findings doc): `orchestrator_harness/provider.py`
(`ClaudeCodeProviderAdapter`) and `orchestrator_harness/invocation.py` (`_provider()`).

---

## Step 0.1 — Claude lane launch: missing `--verbose` (A1 / U1 / U2, §1)

**Reproduce (must fail first):**
```bash
echo "hi" | claude --print --output-format stream-json \
  --model deepseek-v4-flash:0731-cloud --permission-mode bypassPermissions
# Expect: "Error: When using --print, --output-format=stream-json requires --verbose" exit 1
```
Confirm the harness builds exactly this bad argv: call
`ClaudeCodeProviderAdapter().build_argv(spec)` (`provider.py:505`) with a `start`
spec and assert `"--verbose"` is **absent** — reproducing the defect.

**Fix:** in `build_argv`, emit `--verbose` whenever `--output-format stream-json` is
used in `--print` mode (i.e. append it right after `stream-json` on line 508).

**Re‑test / Pass:**
- `build_argv` now yields `[..., "--print", "--output-format", "stream-json", "--verbose", ...]`.
- Piping the newly‑built argv to the real CLI (Ollama backend) no longer exits 1 on the
  flag error; a `system/subtype=init` line appears.
- **Regression:** add `test_compat_provider_argv.py::test_claude_start_argv_has_verbose`.
**Evidence:** `evidence/0.1/argv.txt`, `evidence/0.1/cli-transcript.jsonl`.

---

## Step 0.2 — No automatic permission bypass → silent false‑COMPLETED (U3, §2)

**Reproduce (must produce the false positive first):**
```bash
echo "Create a file named default_perm_test.txt with content HI" | \
  claude --print --output-format stream-json --verbose --model deepseek-v4-flash:0731-cloud
# Observe: permission_denied for Write; final result is_error:false subtype:success; EXIT 0
ls default_perm_test.txt   # must NOT exist — work never happened
```
Confirm `parse_transcript_line` (`provider.py:535`) classifies that final `result`
line as **COMPLETED** — the false positive.

**Fix (two independent hardenings; do both):**
1. **Default‑safe bypass:** when the caller does not set `permission_mode`, default the
   Claude spec to `bypassPermissions` for a headless lane (mirroring Codex's
   unconditional `--dangerously-bypass-approvals-and-sandbox`) — OR make the missing
   field a hard validation error so a lane can never silently run un‑permissioned.
   (Pick one; document which in the fix note.)
2. **Detect permission denial:** in `parse_transcript_line`, treat a transcript
   containing a `system/subtype=permission_denied` as not‑clean — surface it as `FAILED`
   or a distinct `BLOCKED`, so a lane that was blocked is never reported COMPLETED.

**Re‑test / Pass:**
- With the default bypass, the same prompt now actually creates `default_perm_test.txt`
  and the lane reports COMPLETED **and** the file exists.
- With permission bypass *removed* (to force denial), the lane no longer maps to
  COMPLETED — it maps to FAILED/BLOCKED.
- **Regression:** `test_compat_transcript_parse.py` — feed a captured
  permission‑denied transcript, assert non‑COMPLETED.
**Evidence:** `evidence/0.2/denied-transcript.jsonl`, `evidence/0.2/bypass-success.jsonl`.

---

## Step 0.3 — `config_overrides`/`service_tier`/`approval_policy` accepted then dropped (C17 / U4, §3)

**Reproduce:** build a canonical invocation for `provider.id = "claude-code"` that sets
`config_overrides`, `service_tier`, and `approval_policy`. `_provider()`
(`invocation.py:380`) accepts them (same allow‑list for every provider). Then call
`ClaudeCodeProviderAdapter.build_argv` and assert **none** of those three appear in the
Claude argv — reproducing the silent drop. Compare to the Codex adapter, where all three
*do* appear.

**Fix (choose the intended contract):**
- **Option A — reject:** make `_provider()` per‑provider aware; for `claude-code`, raise
  `InvocationValidationError` on fields Claude cannot honor (fail loud, no silent drop).
- **Option B — honor:** add a generic override channel to `ClaudeCodeProviderAdapter`
  (e.g. map `config_overrides` entries like `model_provider="ollama"` / env redirects
  into the child environment or CLI flags Claude does support).
> Recommend **A** as the minimum (kills the silent‑success trap); **B** additionally
> restores the Ollama‑redirect mechanism the Codex/DeepSeek probe relied on. Confirm
> intended behavior before implementing — see [open question](#open-question).

**Re‑test / Pass:**
- Option A: the same invocation now raises a clear validation error naming the offending
  field(s). Option B: the values demonstrably reach the child (argv/env asserted).
- **Regression:** `test_compat_provider_allowlist.py` for the chosen contract.
**Evidence:** `evidence/0.3/claude-argv.txt`, `evidence/0.3/codex-argv.txt` (the diff).

---

## Step 0.4 — No working Claude example/fixture (A17, §4)

**Reproduce:** `grep -ri claude Firmware/target-harness/examples/` → no hits;
`disposable_coding_fixture.py` and `coding.invocation.example.json` are Codex‑only.

**Fix:** author, in the disposable clone's `examples/`:
- `coding.claude.invocation.example.json` — a valid canonical
  `orchestrator-worker-invocation/v1` for `provider.id="claude-code"` (model, and the
  now‑fixed permission handling from 0.2), cross‑checked against
  `tests/test_s2_contract.py` (the only existing claude‑code shape).
- a `disposable_claude_coding_fixture.py` (or a `--provider claude-code` switch on the
  existing fixture) that launches a real single Claude lane end‑to‑end on the Ollama
  backend.

**Re‑test / Pass:** running the new fixture with steps 0.1–0.3 applied launches a real
`claude` subprocess, produces `PROVIDER_STARTED`/`PROVIDER_EXITED` in
`LANE_EVENTS.jsonl`, and a real `session_id` — the copy‑paste path a new caller would
follow now works.
**Evidence:** `evidence/0.4/fixture-run.log`, `evidence/0.4/LANE_EVENTS.jsonl`.

---

## Step 0.5 — Confirm the unblock (gate for Phase 3)

Re‑run the original passing set to prove nothing regressed and the lane is now real:
2‑lane concurrency, provider event logging, transcript STARTED/COMPLETED, `MISSING`
result detection, `--resume <session_id>`, `watch --until-actionable` → `WATCH_TIMEOUT`.
**Pass:** all still pass **and** a Claude lane now launches without the flag error and
without the false‑COMPLETED. Only then start Phase 3.

---

## Open question

Steps 0.2 and 0.3 each have a legitimate "reject vs. honor" fork. The plan recommends
*default‑safe bypass* (0.2) and *reject‑loud* + optionally *honor* (0.3), but the intended
product contract is the user's call — resolve before implementing those two fixes. The
rest of Phase 0 (0.1, 0.4) has no such fork.
