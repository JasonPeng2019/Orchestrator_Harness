# Phase 3 — Live Claude‑lane behavior & cross‑provider coordination

**Depends on Phase 0.** Everything here needs a Claude lane that actually launches and
produces real events — impossible until findings #1–#4 are fixed. Uses the Ollama backend
from the [README setup](README-claude-code.md#3-environment--setup). These are the **TB‑SC** rows whose
*authentic wiring* (not just their logic, which Phase 1 covered) needs a real lane, plus the
cross‑provider round the findings doc's "planned scope" section calls for.

**Method:** launch real lanes via the Phase‑0 Claude fixture (`disposable_claude_coding_fixture.py`)
and the existing Codex fixture, observe `LANE_EVENTS.jsonl` + `watch` output. Capture all
evidence to `evidence/3.x/`.

---

## Status & remaining work (as of 2026‑08‑20)

**PHASE 3 FULLY EXECUTED (2026‑08‑20).** All areas closed; see `evidence/PHASE3-LOG.md` for the row table.

**Done / PASS (quota‑frugal, authentic):**
- ✅ **3.E** — six originally‑passing live behaviors re‑confirmed post‑fix. Evidence `evidence/3.E/`.
- ✅ **3.B** — `watch --until-actionable` real actionable wake + non‑wake (V7). Evidence `evidence/3.B/`.
- ✅ **3.A · G21 (all three launch‑failure event types, live)** — `CONTROLLER_FAILED`
  (`PROVIDER_STARTED`→`CONTROLLER_FAILED`, session null); **`LAUNCH_FAILED`** (live stub inventoried then
  clean exit 0 with no session‑init line → :3117, `PROVIDER_STARTED`(pid 27080)→`LAUNCH_FAILED`, session
  null); **`CONTROLLER_INTERRUPTED`** (KeyboardInterrupt injected at the provider‑spawn boundary via an
  argv‑scoped Popen gate → handler :3247 with `process is None` → clean else :3281, rc 130, no spawn). The
  G21 family is now fully observed live. Evidence `evidence/3.A/` (CONTROLLER_FAILED) and
  `evidence/3.A/g21-siblings/` (LAUNCH_FAILED + CONTROLLER_INTERRUPTED).
- ✅ **3.A · F15 + G32** — committed `RESULT.json` → terminal acceptance, driven authentically by the
  **orchestrator coaching loop**: turn‑1 controller run produced a schema‑valid RESULT.json missing the
  prompt shas; a corrective `claude --resume` rewrote it with the exact shas; `scan` →
  `RESULT_ACCEPTANCE_PENDING`; ROOT authored review + acceptance → `scan` `TERMINAL_RESULT` / `ACCEPTED`.
  Evidence `evidence/3.A/coach/`.
- ✅ **3.C** — cross‑provider concurrency (claude‑code+Ollama ⋈ codex+Ollama) on one shared runtime; both
  COMPLETED, distinct sessions, single `scan` reconciles both provider‑neutrally. Finding **P3‑OBS‑2**
  (codex `CODEX_*` vs claude `PROVIDER_*` in the shared log). Evidence `evidence/3.C/`.
- ✅ **3.D** — MCP under claude+Ollama: `--mcp-config` threaded into the argv AND a live round‑trip
  (model called `mcp__marker__record_marker`, only tool_use, marker file written). Evidence `evidence/3.D/`.

**Honestly NOT laundered into PASS:**
- **3.A · G8–G16 byproducts** — **GAP.** A single controller turn + an out‑of‑controller `--resume`
  coaching turn emit only `PROVIDER_STARTED`/`PROVIDER_EXITED`; helper/relay/lifecycle/ack events did
  **not** materialize. Classifiers stay covered in‑process by Phase 1.
- **3.A · G10 stall** — **synthetic FAKE (accepted).** Live producers removed in S4 (P3‑OBS‑4); only the
  classifier survives, proven against fabricated conditions. Explicitly labeled fake.

---

## 3.A — Live single‑Claude‑lane event authenticity — F15, G8–G13, G15, G16, G21, G32(live)

Run one real Claude lane to a real terminal state and assert each event fires authentically
(Phase 1 proved the classifier; this proves it's wired to a live lane).

1. **G21** launch‑failure events (LAUNCH_FAILED, CONTROLLER_FAILED, CONTROLLER_INTERRUPTED):
   force a launch failure (bad model name / kill the controller mid‑launch) → the matching
   failure event appears in `LANE_EVENTS.jsonl`. *(Also re‑confirms Phase 0's argv fix by
   showing a real launch no longer fails on the flag error.)*
2. **G8** subordinate‑process events (HELPER_EXITED/_STATE_UNKNOWN): run a lane that spawns a
   helper, let the helper exit → `HELPER_EXITED`; kill ‑9 it → `HELPER_STATE_UNKNOWN`.
   *(MCP portion is OOS → see 3.D.)*
3. **G9** `PROVIDER_WAIT` / `LANE_STATE_UNKNOWN`: pause the lane on a resource wait →
   `PROVIDER_WAIT`; sever its status file mid‑run → `LANE_STATE_UNKNOWN`.
4. **G10** stall‑detection (MANAGER_REVIEW_DUE, LANE_NO_PROGRESS, LANE_STAGE_REPEAT): drive a
   lane past the no‑progress / stage‑repeat thresholds → each stall event.
5. **G11** non‑actionable observed‑state events (CONTROLLER_ACTIVE, LANE_WAITING_RESOURCE,
   LANE_WAITING_RELAY, RESULT_ACCEPTANCE_PENDING, RESOURCE_RELEASE_POSSIBLE, REQUEST_STALE):
   observe a live lane in each state → each event present, none marked actionable.
6. **G12** relay‑observation events (RELAYED, RELAYED_INACTIVE, RELAYED_AMBIGUOUS): relay a
   live lane's request in each condition → each event.
7. **G13** steady‑state events (HELPER_ACTIVE, MCP_ACTIVE, CONDITION_CLEARED): live helper
   active → `HELPER_ACTIVE`; clear a prior condition → `CONDITION_CLEARED`. (MCP_ACTIVE → 3.D.)
8. **G15** harness event‑lifecycle tracking (HARNESS_SIGNAL_OBSERVED, HARNESS_EVENT_INELIGIBLE/
   _ACTIONABLE/_PENDING/_DEFERRED): drive a signal through the lifecycle on a live lane →
   each internal tracking event recorded in order.
9. **G16** harness ack tracking (HARNESS_ACK_ATTEMPTED/_SUCCEEDED): manager acks a live event →
   both ack‑tracking events recorded.
10. **F15 / G32** `RESULT_ACCEPTANCE_PENDING` → `TERMINAL_RESULT` / `RESULT_AVAILABLE`: let a
    Claude lane write a valid `RESULT.json` and reach a terminal, accepted state → the state
    transitions from acceptance‑pending to terminal and `RESULT_AVAILABLE` fires. *(This is
    the end‑to‑end completion the original round never reached because no lane produced a
    valid committed result — the single most important live gap to close.)*

### 3.A method — orchestrator coaching loop (REQUIRED continuation behavior)

**Intended behavior (binding for finishing this phase):** a weak backend model
(`deepseek-v4-flash:0731-cloud`) will usually **not** reach the desired outcome on a
single cold turn — the first turn typically yields a `MISSING`/invalid result. That is
**not** the end of the test. Acting **as the orchestrator**, you must:

1. **Read the model's prompt response** (`worker_last_message.txt` / the stream‑json
   `assistant` lines / the transcript) and diagnose exactly where it fell short of the
   desired outcome (e.g. wrote the artifact but did not commit; produced no `RESULT.json`;
   emitted a malformed `RESULT.json`; stopped early).
2. **Inject a corrective prompt as the orchestrator and let the same session keep going**
   via **provider‑session continuation**:
   `claude --resume <provider_session_id> "<specific correction>"` (same
   `--output-format stream-json --verbose --permission-mode bypassPermissions --model …`
   flags; same Ollama redirect). This continues the *same* Claude transcript and needs
   **no** committed `RESULT.json` precondition — it is the "tell it what it got wrong and
   let it continue" lever. (Do **not** confuse this with harness *task*-resume in
   `resume.py` / `_canonical_prior_task_preflight`, which is a strict identity re‑admission
   that *does* require a prior valid committed result — that is a different mechanism and is
   not what coaching uses.)
3. **Repeat** the read → diagnose → corrective‑continue loop until the lane reaches the
   desired outcome. For **F15/G32** the desired outcome is a **schema‑valid committed
   `RESULT.json`**: `schema="orchestrator-task-result/v1"`, with `lane_id` +
   `worker_invocation_id` matching the owning controller status (discovery.py ~826/873),
   written to `<workspace>/RESULT.json`. `_validate_task_result_cached` then yields
   `ACCEPTED` and reconcile fires the authentic terminal‑acceptance path. The multi‑turn
   coached run also naturally exercises the steady‑state / relay / lifecycle / ack events
   (G11–G16) as byproducts — capture them from `LANE_EVENTS.jsonl` during the loop.

Coaching turns spend real Ollama quota → **STOP‑on‑429** (do not retry a 429). Record each
corrective turn (the injected prompt + the resulting response/events) under `evidence/3.A/`
so the coached path is auditable.

> **Model‑dependent caveat (narrowed):** only a realistic **stall** (G10 — a genuinely
> long‑running lane state a fast/weak model never sits in) cannot be provoked authentically
> by coaching. For that **single** item a **synthetic/fake stall state** is acceptable
> (user decision, 2026‑08‑20); mark it explicitly as a fabricated‑state proof of the
> classifier wiring, not a live emergent stall. Everything else in 3.A (F15, G8–G9, G11–G13,
> G15, G16, G32‑live) is reachable via the coaching loop above and must **not** be written
> off as "not reproducible" without first attempting the corrective‑continuation loop.

---

## 3.B — `watch --until-actionable` real actionable firing — V7

11. **V7** actionable‑event allowlist gating (`cli._is_actionable`): the original round only
    saw the *timeout* path (`WATCH_TIMEOUT`). Now fire a genuinely actionable event
    (MANAGER_SIGNAL / RESOURCE_CONFLICT) while `watch --until-actionable` is blocked → it
    **returns that event before timeout**, and confirm a *non*‑actionable event does **not**
    wake it (still `WATCH_TIMEOUT`). Pass = both the positive wake and the negative
    non‑wake observed. Complements A23/B5 (only the timeout path passed before).

---

## 3.C — Cross‑provider multi‑lane coordination (the findings doc's planned next round)

The prior rounds tested one provider at a time. This tests the harness's central claim —
coordinating genuinely different provider CLIs in one run.

12. **Cross‑provider concurrency:** launch, in one run, a set of parallel **Claude Code +
    Ollama** subagent lanes together with one or two **Codex + Ollama/DeepSeek** lanes.
    Assert:
    - **Shared event log:** `LANE_EVENTS.jsonl` interleaves both providers' events with
      correct per‑lane `provider_id` and no lost/overwritten rows (append‑lock integrity).
    - **Resource locks across CLIs:** two lanes of *different* providers contending for one
      named lock → exactly one holds, the other publishes `WAITING_RESOURCE` (re‑exercises
      H‑section across a provider boundary).
    - **`watch --until-actionable` across CLIs:** a manager watching the mixed run wakes on
      an actionable event regardless of which provider produced it.
    - **Result validation across CLIs:** each provider's committed result validates through
      the same provider‑neutral `validate_coding_result` path (ties E14–E19 to real,
      differently‑authored commits).
    - **Isolation:** no cross‑lane / cross‑provider file or branch contamination (extends
      A10/V2/V8 across a provider boundary).
    Pass = all five hold; any coordination defect that only appears cross‑CLI is a new
    finding (record in `evidence/FINDINGS.md`).

---

## 3.D — MCP under Claude+Ollama — one attempt (bounded, per findings doc)

MCP is OOS generally, but the findings doc explicitly asks to **attempt it once** under
Claude+Ollama (Codex‑on‑Ollama can't do MCP, so it's excluded by construction).

13. **MCP attempt:** launch a Claude+Ollama lane with a minimal `--mcp-config` and one
    trivial MCP tool; observe whether the tool is callable. Three legitimate outcomes, all
    recorded — none is a "failure to chase":
    - MCP works → note it and, if so, `MCP_ACTIVE`/MCP‑proof states (F13/S2) become live‑
      testable; capture them.
    - Claude+Ollama can't do MCP (like Codex) → record it as a **documented backend
      boundary**: MCP simply can't be exercised under backend substitution.
    - Ambiguous → record exactly what was observed.
    Pass = the attempt was made once and its outcome documented (not assumed).

---

## 3.E — Re‑confirm the originally‑passing live set with the fixes in place

14. Re‑run the six originally‑passing live behaviors (2‑lane concurrency, provider event
    logging, transcript STARTED/COMPLETED, `MISSING` result detection, `--resume`,
    `watch`→`WATCH_TIMEOUT`) **after** Phase 0's fixes to prove no regression and that they
    now sit on a genuinely‑launching lane. Pass = all six still pass.
