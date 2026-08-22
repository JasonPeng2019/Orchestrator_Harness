# Phase 5 — Residual live event emission (the 7 rows phases 0–4 missed)

> **STATUS: COMPLETE (2026-08-20) via the 5.B producer-seam path.** All 7 rows
> (G8, G9, G11, G12, G13, G15, G16) are now `TESTED-PASSED (5.B, producer-seam)`.
> The decision gate below resolved to 5.B: the Ollama backend cannot sustain the
> multi-lane/relay/subordinate-process/harness-lifecycle states a live 5.A pass
> needs within the time box, so each producer call site was driven in-process and
> asserted to emit. Test: `orchestrator_harness/tests/test_compat_live_emission.py`
> (7 passed). Evidence + caveats: [`evidence/5.B/`](evidence/5.B/README.md).
> These passes are explicitly weaker than a live 5.A pass and are never presented
> as live; a future live run may upgrade them. 5.C bookkeeping (inventory cells,
> coverage-matrix Result cells, the "Live-not-materialized" count → 0) is done.

> **Scope.** After phases 0–4, exactly **7** feature rows remain NOT-TESTED for a reason that
> is *neither* provider-agnostic (PA, deliberately not re-run) *nor* out-of-scope (OOS,
> excluded by instruction). They **should** be tested — the classifier logic exists in
> `notifications.py`/`events.py`, but no phase produced a **live lane** that emitted these
> events, and they were not in the phase-1 in-process batch either. Phase 5 exists to close
> that gap honestly.

The 7 rows (from `active_docs/claude_listed_Features.md` §G):

| Row | Event class | Why it didn't materialize in 3.A |
|---|---|---|
| **G8** | Subordinate-process events (HELPER_EXITED/_STATE_UNKNOWN, MCP_EXITED/_STATE_UNKNOWN) | A single controller turn spawned no subordinate helper process. MCP portion stays OOS. |
| **G9** | `PROVIDER_WAIT` / `LANE_STATE_UNKNOWN` | Single-turn run never entered a provider-wait / unknown-lane state. |
| **G11** | Non-actionable observed-state events (CONTROLLER_ACTIVE, LANE_WAITING_RESOURCE, LANE_WAITING_RELAY, RESULT_ACCEPTANCE_PENDING, RESOURCE_RELEASE_POSSIBLE, REQUEST_STALE) | No second lane / resource contention to produce observed-state events. |
| **G12** | Relay-observation events (RELAYED, RELAYED_INACTIVE, RELAYED_AMBIGUOUS) | No relay binding was exercised on a live lane. |
| **G13** | Steady-state events (HELPER_ACTIVE, MCP_ACTIVE, CONDITION_CLEARED) | No steady-state helper ran long enough to emit. |
| **G15** | Harness-internal event-lifecycle tracking (HARNESS_SIGNAL_OBSERVED, HARNESS_EVENT_INELIGIBLE/_ACTIONABLE/_PENDING/_DEFERRED) | The single turn produced no harness signal-observation lifecycle. |
| **G16** | Harness ack tracking (HARNESS_ACK_ATTEMPTED/_SUCCEEDED) | No ack round-trip occurred on the live lane. |

> **Root cause (one sentence).** Phase 3 proved the *launch + result* path live (a lane
> starts, runs, and its RESULT.json reconciles), but a one-turn Ollama lane never reaches the
> multi-lane / subordinate-process / relay / steady-state conditions that make these seven
> event families fire — so their **classifiers** are correct (they select/prioritize correctly
> when fed a record) yet their **producers** were never driven end-to-end.

---

## 5.0 — Decision gate: live producer vs. in-process producer-seam

Two honest ways to close these, in preference order:

1. **5.A (preferred) — drive real producers on live lanes.** Construct lane scenarios that
   *actually* reach each state, and assert the event lands in the shared `LANE_EVENTS.jsonl`.
   This is the authentic analog of the phase-3 `CONTROLLER_FAILED` / `PROVIDER_STARTED`
   evidence (G7/G21) and is the only way to earn a plain TESTED-PASSED.
2. **5.B (fallback) — producer-seam in-process test.** If a producer cannot be reached with
   the weak Ollama backend within the time box (e.g. HELPER_* requires a subordinate helper
   the harness only spawns under conditions Ollama can't sustain), test the **producer call
   site** in-process: invoke the code path that *should* emit, capturing the emit, so the
   producer→event wiring (not just the classifier) is proven. Mark such rows
   `TESTED-PASSED (5.B, producer-seam)` — explicitly weaker than a live 5.A pass, never
   presented as live.

**Any row that 5.A and 5.B both fail to reach stays NOT-TESTED with the honest reason** — do
not fabricate, do not flip to PASS. Record the blocker in `evidence/5.x/`.

> **Subagent launch envelope (identical to phases 0–4).** Every phase-5 build/test subagent is
> a `deepseek-v4-flash:0731-cloud` session launched **session-local** with the pinned envelope in
> [`../phase0-5-claude-launch.md`](../phase0-5-claude-launch.md):
> - `--effort high` (explicit on the command line — never `max`/`xhigh`, never inherited)
> - **`CLAUDE_CODE_AUTO_COMPACT_WINDOW=180000`** (fixed 180k-token auto-compact pin)
> - **`CLAUDE_CODE_MAX_CONTEXT_TOKENS=200000`** (context ceiling)
> - `CLAUDE_CONFIG_DIR` into the disposable clone — never `~/.claude`, never `claude config set`,
>   never global settings
>
> Rationale in memory `subagent-launch-local-only`.

---

## 5.A — Live producer scenarios

Run in the compat-test clone against local Ollama. Each step ends by grepping the shared
`LANE_EVENTS.jsonl` for the named event and capturing the matching line to `evidence/5.x/`.

1. **G8 — subordinate-process events.** Drive a lane whose controller spawns a subordinate
   helper process, then force that helper to exit (clean and killed) → assert
   `HELPER_EXITED` and, on an unobservable exit, `HELPER_STATE_UNKNOWN`. *(MCP_* variants stay
   OOS.)* Pass = both HELPER_* events observed in `LANE_EVENTS.jsonl`.
2. **G9 — `PROVIDER_WAIT` / `LANE_STATE_UNKNOWN`.** Start a lane and induce a provider stall
   (provider process alive but producing no turn within the liveness bound) → `PROVIDER_WAIT`;
   then remove/scramble the lane status file mid-run → `LANE_STATE_UNKNOWN`.
3. **G11 — non-actionable observed-state events.** Run **two** lanes contending for one named
   resource (reuse the H9 `exclusive_resources` machinery) so the blocked lane publishes
   `LANE_WAITING_RESOURCE`; keep the winner active for `CONTROLLER_ACTIVE`; commit a RESULT.json
   awaiting acceptance for `RESULT_ACCEPTANCE_PENDING`. Pass = each observed-state event
   present.
4. **G12 — relay-observation events.** Exercise a relay binding on a live lane (bind → observe
   `RELAYED`; let it go inactive → `RELAYED_INACTIVE`; create a two-candidate ambiguity →
   `RELAYED_AMBIGUOUS`).
5. **G13 — steady-state events.** Keep a subordinate helper alive across a scan interval →
   `HELPER_ACTIVE`; clear a previously-raised condition → `CONDITION_CLEARED`. *(MCP_ACTIVE
   stays OOS.)*
6. **G15 — harness event-lifecycle tracking.** Feed the harness a manager signal and walk it
   through the lifecycle → `HARNESS_SIGNAL_OBSERVED`, then the eligibility transitions
   (`HARNESS_EVENT_INELIGIBLE` for a not-yet-actionable signal, `_ACTIONABLE`, `_PENDING`,
   `_DEFERRED` under preemption).
7. **G16 — harness ack tracking.** Drive an actionable event through an ack round-trip →
   `HARNESS_ACK_ATTEMPTED` then `HARNESS_ACK_SUCCEEDED`.

---

## 5.B — Producer-seam fallback (only for rows 5.A cannot reach)

For any row above whose live producer the Ollama backend cannot sustain within the time box,
add a focused test in `orchestrator_harness/tests/test_compat_live_emission.py` that invokes
the **producer** code path directly (not the classifier) and asserts the event record is
emitted with the correct kind/fields. This proves the emit wiring; it does **not** count as
live evidence. Tag the row `TESTED-PASSED (5.B, producer-seam)` and note in the Status cell
that live emission on Ollama was not reached.

---

## 5.C — Bookkeeping on completion

For each of the 7 rows, update **in lockstep**:

- `active_docs/claude_listed_Features.md` §G Status cell → `TESTED-PASSED (5.A)` /
  `TESTED-PASSED (5.B, producer-seam)` / unchanged NOT-TESTED (with blocker note).
- `plans/compatibility-testing/coverage-matrix.md` §G Result cells (currently empty for
  G8–G13/G15/G16) → the phase-5 outcome.
- The summary counts and the "Live-not-materialized — 7" breakdown row in
  `claude_listed_Features.md` (decrement by whatever 5.A/5.B closes).
- `evidence/5.x/` holds the `LANE_EVENTS.jsonl` excerpt (5.A) or the pytest transcript (5.B)
  behind every changed cell.

> **Honesty rule (unchanged from phases 1–4).** A row moves off NOT-TESTED only with evidence
> in `evidence/5.x/`. Live (5.A) and producer-seam (5.B) passes are labeled distinctly. Rows
> neither path can reach stay NOT-TESTED with a one-line blocker — never fabricated.

---

## Out of scope for Phase 5 (unchanged)

- **MCP_* variants** of G8/G13 (MCP_EXITED/_STATE_UNKNOWN, MCP_ACTIVE) remain **OOS** per the
  standing MCP exclusion — Phase 5 covers only the HELPER_* / non-MCP halves of those rows.
- The **72 PA rows** stay optional-regression (Appendix A); Phase 5 does **not** re-run them.
- The **23 OOS rows** (firmware / MCP / legacy-watcher) stay excluded by instruction.
