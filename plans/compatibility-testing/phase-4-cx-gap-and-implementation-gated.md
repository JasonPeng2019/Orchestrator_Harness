# Phase 4 — CX‑GAP (implementation‑gated) & out‑of‑scope disposition

> **⚠️ Build & test are delegated to Claude‑Code deepseek subagents — pinned autocompact.**
> Both the `ClaudeHostAdapter` build (4.A/4.B) and its test runs are executed by
> `deepseek-v4-flash:0731-cloud` subagents launched **session-local** with a pinned
> **`CLAUDE_CODE_AUTO_COMPACT_WINDOW=180000`** (fixed 180k-token limit) under a
> `CLAUDE_CODE_MAX_CONTEXT_TOKENS=200000` ceiling, `--effort high`, `CLAUDE_CONFIG_DIR`
> inside the disposable clone — never `claude config set` / `~/.claude` / global settings.
> Full envelope: [README-claude-code.md §3 "MANDATORY subagent launch envelope"](README-claude-code.md#3-environment--setup);
> rationale in memory `subagent-launch-local-only`.


The **30 CX‑GAP** rows are provider‑neutral *concepts* — a "product that works for every
provider CLI" would have them for Claude — but the harness only built the **Codex** side and
left Claude with `FutureHostFixture` (a stub). They **cannot be exercised for Claude until a
Claude host adapter exists.** So Phase 4 is two things:

1. A **build decision** the user must make (implement the Claude host adapter, or accept the
   gap and mark these permanently N/A for Claude).
2. The **test plan to run once built** — concrete per‑feature steps, ready to execute the
   moment an adapter lands.

Rows: **A24, N1, N2, N3, N6, N8, G17, G19, B9–B14, M1–M16.**

---

> **✅ STATUS — COMPLETE (2026-08-20).** Build decision: *implement the Claude host adapter*.
> All 30 CX‑GAP rows are now built-and-tested for the Claude Code track:
> 4.A (A24, N1, N2, N3, N6, N8, G17, G19) + 4.B (B9–B14) via
> `orchestrator_harness/tests/test_compat_claude_adapter.py` (14 passed, 3 subtests);
> 4.C (M1–M16) held as green Codex regression reference (45 passed). ROOT independently
> re-ran and read every result. Acceptance: `evidence/PHASE4-ORCHESTRATOR_ACCEPTANCE.json`
> (ACCEPTED); disposition detail in `evidence/PHASE4-COMPLETION_REVIEW.json`;
> matrix cells updated in `coverage-matrix.md`. 4.D remains out-of-scope by instruction.

## 4.0 — Decision gate (do this first)

The CX‑GAP root cause (inventory taxonomy note): the harness built the full Codex
hook‑adapter + delivery‑coordinator stack (install into `.codex/hooks.json`, wake idle
sessions via `PostToolUse`/`Stop` hooks + App Server fixtures) and gave Claude
`FutureHostFixture`. The one genuine caveat is the *wake‑the‑idle‑agent* half of A24: Codex
injects in‑process (`thread/inject_items`/`Stop.continue`); Claude Code has no in‑session
injection API, but `claude --resume <session_id>` (already tested live, K1/A26) is a
cross‑process re‑entry that serves the same purpose. So the gap is "no delivery coordinator
wires resume‑as‑wake together for Claude," not "impossible."

**Ask the user (see [open question](#open-question)):** build a Claude host adapter
(`ClaudeHostAdapter` + a resume‑based delivery coordinator) so these become testable, or
accept the gap? Nothing below runs until this is answered.

> **DECISION (user, 2026‑08‑20): BUILD.** Build permission granted for the Claude host
> adapter + resume‑based delivery coordinator. The build is delegated to Claude‑Code
> `deepseek-v4-flash` subagents (see banner at top), coordinator‑verified by ROOT; the
> test plan in 4.A/4.B is then executed the same way. 4.C Codex regression is run first as
> the known‑good reference contract.

---

## 4.A — Claude host adapter & S4 delivery (once `ClaudeHostAdapter` exists) — A24, N1, N2, N3, N6, N8, G17, G19

Mirror the Codex host‑adapter tests (`test_s4_contract.py`, `test_s4_repair.py`) for the new
Claude adapter.

1. **N1** real Claude host adapter replaces `FutureHostFixture`: `select_host_adapter` for a
   Claude host returns the real adapter, not the stub. Pass = fixture no longer selected.
2. **N8** `select_host_adapter` capability‑based selection: a Claude host with delivery
   capability routes to `ClaudeHostAdapter`; a host without it still routes to
   `FutureHostFixture`.
3. **N2** `DeliveryNotice` bounded wake payload: build a notice for a Claude lane → carries
   identity/revision/pending‑count/severity and **no** event payload (sparse‑notice rule).
4. **N3** `DeliveryReceipt` transport‑evidence‑only: deliver via the Claude adapter → receipt
   holds transport evidence only, never an acknowledgement.
5. **N6** `DeliveryCoordinator` registration/replay‑state persistence beside the S3 queue:
   register a Claude binding → replay state persists and survives a coordinator restart.
6. **A24** S4 delivery for Claude via **resume‑as‑wake**: with an idle Claude session, the
   coordinator wakes it by spawning `claude --resume <session_id>` (the K1/A26 machinery)
   and the resumed process observes the pending notice. Pass = an idle Claude lane is
   demonstrably re‑entered and picks up the notice (the cross‑process analog of Codex's
   in‑process injection).
7. **G17** wake‑delivery tracking (HARNESS_WAKE_ATTEMPTED/_DELIVERED/_FAILED) for Claude:
   drive a successful and a failed resume‑wake → both tracking events recorded.
8. **G19** manager‑wake events (MANAGER_WAKE_RECEIVED, MANAGER_WAIT_FINISHED,
   MANAGER_WAKE_ATTEMPTED/_DELIVERED/_FAILED) for Claude: manager‑side wake round trip →
   each event recorded.

---

## 4.B — `adapter` CLI subcommands for a Claude host (once supported) — B9–B14

Today these are Codex‑only (`--host codex`). Once a Claude host adapter exists, re‑run each
with `--host claude` against a disposable project.

9. **B9** `adapter install --host claude`: installs the Claude‑side hook/binding into the
   project's Claude config (`.claude/settings.json` hooks) with atomic rollback‑on‑failure.
10. **B10** `adapter check --host claude`: reports ownership/currency of the installed Claude binding.
11. **B11** `adapter upgrade --host claude`: migrates a legacy Claude binding revision.
12. **B12** `adapter uninstall --host claude`: removes owned files, preserves user‑modified ones, rolls back cleanly.
13. **B13** `adapter self-test --host claude`: synthetic wake self‑test succeeds against the Claude adapter.
14. **B14** `adapter hook --boundary post_tool_use|turn_completed|finalization --host claude`:
    each boundary dispatch delivers a bounded notice via the Claude transport.

---

## 4.C — Codex host‑adapter internals (optional regression) — M1–M16

These are the **existing Codex implementation** (`codex_adapter.py`,
`codex_bounded_policy.py`). They are CX‑GAP only in the sense that Claude lacks the
equivalent — the Codex side itself is real and already has `test_codex_bounded_policy.py`.
**Optional:** if the Claude adapter (4.A/4.B) is built by mirroring the Codex one, run
M1–M16 as a regression baseline first so the Claude adapter has a known‑good reference:
installer transaction + rollback (M1), ownership probe (M2), legacy upgrade (M3), uninstall
with preserved‑modified detection (M4), packaged‑asset integrity incl. BOM/lone‑CR/UTF‑8
strictness (M5), project‑mutation guard / symlink‑chain rejection (M6), hook‑fragment merge
with ambiguous‑owned‑hook conflict detection (M7), hook‑fragment subtraction (M8),
manifest identity validation (M9), `deliver_notice` boundary dispatch (M10), safe‑boundary
hook methods (M11), synthetic wake self‑test (M12), sparse‑notice‑only transport enforcement
(M13), binding‑record read/validate (M14), bounded‑policy launcher/exclusion enforcement
(M15), bounded‑policy status (M16).
Pass (if run) = Codex adapter internals green, establishing the contract the Claude adapter
must match.

---

## 4.D — Out‑of‑scope disposition (not tested; recorded for completeness)

Per explicit instruction these stay **excluded**; listed so the coverage matrix is complete
and nobody re‑discovers them as "missing":

- **Firmware / hardware** (A5, A40, R1–R8, C15): `firmware_adapter.py`,
  `firmware_campaign.py`, firmware capability adapters, legacy policy‑bound firmware
  invocation, firmware‑as‑coding rejection. **Not tested.**
- **MCP** generally (A41, S1–S3, F5, F13): `--mcp-config` provider wiring, MCP process
  tri‑state, MCP‑proof states, broker MCP traffic. **Not tested** — *except* the single
  bounded Claude+Ollama attempt in [Phase 3.D](phase-3-live-claude-and-cross-provider.md#3d--mcp-under-claudeollama--one-attempt-bounded-per-findings-doc).
- **Legacy / parallel watcher generation** (A37, A38, T1, T2, T4, T5):
  `Portable_Watcher_Repo/*` superseded design, AI‑judge evaluator, WSL2/bubblewrap dry‑run
  spec, older host‑only test list. **Not tested** (superseded by `discovery.py` /
  `watcher_integration.py`, whose in‑scope parts are covered in Phase 2.G).

---

## Open question

Phase 4 is entirely gated on the **build‑or‑accept** decision in
[4.0](#40--decision-gate-do-this-first). If the answer is "accept the gap," mark A24 /
N1–N3 / N6 / N8 / G17 / G19 / B9–B14 as **N/A‑for‑Claude (by decision)** in the coverage
matrix and skip 4.A/4.B; 4.C/4.D need no decision.
