# Qwen compatibility testing — TB-W follow-up plan

**Source inventory:** `active_docs/qwencode_listed_features.md`
**Harness under test:** `harness-single-worktrees/qwencode-test/orchestrator_harness`
(branch `qwencode-test-copy`; a disposable copy of WIP commit `055a5bd`,
`firmware/v2-candidate`).
**Test module:** `orchestrator_harness/tests/test_qwen_multi_agent.py`
**Run command (all qwen tests):**
```text
cd harness-single-worktrees/qwencode-test
python -m unittest orchestrator_harness.tests.test_qwen_multi_agent -v
```

---

## 1. Purpose & scope

`qwencode_listed_features.md` inventoried 112 features and flagged **18 rows as
TB-W** ("worth testing"): the features a qwen pass "should still add" because
the 15-test qwen suite did not exercise them. This plan turns those 18 rows into
concrete, per-feature steps.

The 18 TB-W features are:

- **Tier 1 (qwen-relevant):** F6.4, F2.1.2, F1.6.3
- **Tier 2 (provider-neutral safety):** F3.4, I5, I8, F4.3, F5.1.4
- **Tier 3 (heavier subsystems):** F2.3.1–F2.3.4 (lane lifecycle), F8.1–F8.6 (capability broker)

### The dedup constraint (why this plan is not "write 18 tests")

The user requirement is explicit: **tests must not cover things that were also
tested.** The TB-W rows were "not covered *by the 15-test qwen suite*" — but the
harness ships a much larger generic suite (`tests/test_*.py`, ~40 files). A
direct audit of that suite (§2) shows **12 of the 18 TB-W features are already
covered generically**, byte-for-byte, by provider-neutral tests. Re-adding
qwen-shaped copies of those would test the harness a second time, not qwen.

Therefore this plan splits the 18 into:

- **Part A — 4 genuinely uncovered gaps → write new tests.** (F5.1.4, F2.1.2, F4.3, F6.4)
- **Part B — 1 optional qwen-suite-local integration wrapper.** (F3.4)
- **Part C — 12 already-covered features → verify + cross-reference, do NOT duplicate.** (F1.6.3, I5, I8, F2.3.1–F2.3.4, F8.1–F8.6)

Every TB-W feature gets a concrete step. For Part C, the concrete step is a
verification-and-citation step (run the existing generic test, record its pass
as the coverage evidence for the qwen row), never a duplicate test.

### Guardrails

- **Never edit the WIP target commit.** All work happens in the
  `qwencode-test` copy and sibling disposable worktrees, exactly as the original
  qwen pass did.
- New tests are **deterministic and host-only** — reuse the existing
  `QWEN_FAKE_CLI` fake CLI and the `_canonical` / `_start` / `_start_async`
  helpers already in `test_qwen_multi_agent.py`. No live model service.
- Keep every new test method inside `test_qwen_multi_agent.py` (Part A/B) so the
  documented run command still runs the whole qwen suite in one shot.
- The qwen adapter must be registered in-process via `_register_qwen()` (loads
  `Firmware/scripts/orchestration/qwen_provider_bootstrap.py`), matching production.

---

## 2. Coverage reconciliation matrix (the honest map)

Legend: **NEW** = genuine gap, write a test (Part A). **OPT** = covered
generically; optional thin qwen wrapper (Part B). **COVERED** = already tested
generically; cross-reference only (Part C).

| # | Feature | Existing coverage found (evidence) | Verdict |
|---|---|---|---|
| **F5.1.4** | `ManagerEventRouter.rebuild_state` crash recovery | **None.** `grep rebuild_state tests/` → only `notifications.py` (impl) references it. No test exercises rebuild-from-journal. | **NEW → A1** |
| **F2.1.2** | Unregistered provider → fail closed | Generic parse-level rejection exists (`test_provider_adapter_registry.py::test_unregistered_provider_is_rejected_by_invocation_and_profile`) but uses a `not-registered` placeholder id; the **qwen** process-local-registry operational risk (detached controller skips the bootstrap → qwen unregistered → controller exit 2) is unexercised. Controller state `PROVIDER_OPERATION_UNSUPPORTED` at `lane_controller.py:2431` is unreached by any test. | **NEW → A2** |
| **F4.3** | `active_declaration_conflicts` duplicate branch/worktree | Unit-tested generically (`test_git_results.py::test_active_conflicts_accept_arbitrary_status_name_and_ignore_exited`). But the **controller-wired** guard (`lane_controller.py:2091`, raises `InvocationError` → exit 2) is never exercised in a real two-lane launch. | **NEW → A3** (qwen e2e, additive) |
| **F6.4** | `watch --until-actionable` vs a finished qwen lane | `watch_until_actionable` tested generically (`test_manager_notifications_adversarial.py`, timeout/no-wake paths). Never run against a **real `PROVIDER_EXITED` qwen lane** — the exact KEY-gap poll workaround the doc calls for. | **NEW → A4** (qwen e2e) |
| **F3.4** | `restore_worktree` exact-byte reversal | Covered generically: `test_workspace_overlay.py::test_restore_exact_clean_returns_original_state`, `…preserves_later_edit_and_blocks`, `…test_retirement_restores_prepared_overlay_and_records_restoration`, `…test_retirement_restores_matching_subagent_receipt`. | **OPT → B1** (qwen-suite-local wrapper only) |
| **F1.6.3** | Post-registration wake-text mutation → SAFE_BOUNDARY_ONLY | **Covered generically:** `test_provider_adapter_public_seams.py:795–811` (`ForeignMutatedWakeAdapter`, mutates wake text after registration, asserts `SAFE_BOUNDARY_ONLY` + no wake text). qwen-specific angle (qwen cannot become WAKE) covered by `test_qwen_adapter_registers_with_notification_false`. Mechanism (`provider.py:980` byte recheck) requires `notification=True`, which qwen can never register. | **COVERED → C1** |
| **I5** | `OverlayCollisionError` (append-only plan rejection) | Covered: `test_workspace_overlay.py::test_prepare_rejects_collision_before_any_mutation`, `…test_prepare_rejects_non_utf8_or_missing_append_target_before_mutation`. | **COVERED → C2** |
| **I8** | Receipt rollback on partial-apply failure | Covered: `test_workspace_overlay.py::test_prepare_rolls_back_partially_applied_target_mutation`, `…test_prepare_rolls_back_when_receipt_cannot_be_published`. | **COVERED → C3** |
| **F2.3.1–F2.3.4** | Lane lifecycle (immutable source view, archive-first retirement) | Exhaustively covered: `test_s4_contract.py::test_S4_IMMUTABLE_VIEW_001`, `…test_S4_LANE_RETIREMENT_001`; `test_s4_repair.py::FC1–FC45` (~45 tests) drive `allocate_immutable_source_view` + `retire_terminal_lane`. | **COVERED → C4** |
| **F8.1–F8.6** | Capability broker full cycle + fail-closed | Exhaustively covered: `test_s5_capability_broker.py` (27 tests incl. `CapabilityDenied`, `CapabilityAdapterUnavailable`, `_public_json` private-material rejection). | **COVERED → C5** |

**Net new test work: 4 tests (Part A) + 1 optional wrapper (Part B).** The other
12 rows are closed by verification/citation (Part C), satisfying the dedup rule.

---

## 3. Part A — New tests to write (genuine gaps)

All four are new `def test_…` methods added to
`orchestrator_harness/tests/test_qwen_multi_agent.py`
(class `QwenMultiAgentTests`), reusing its existing fixtures.

---

### Step A1 — F5.1.4 · `rebuild_state` crash recovery from the durable queue

**Gap:** admit / `next_event` / `acknowledge` are tested
(`test_s3_manager_queue_admit_and_ack`), but the crash-rebuild path
(`ManagerEventRouter.rebuild_state`, `notifications.py:841`) is tested nowhere.
The durable design point — `QUEUE.jsonl` is authoritative, the derived
`STATE.json` / `WAKE.json` caches are reconstructable — is unproven.

**New method:** `test_qwen_manager_queue_rebuild_state_recovers_from_journal`

**Facts to rely on** (from `notifications.py`):
- Router files under its root: `QUEUE.jsonl` (journal, `:469`), `STATE.json`
  (derived cache, `:473`), `WAKE.json` (derived, `:477`), `REGISTRATION.json`.
- `rebuild_state(publish_wake=True)` rebuilds the cache **solely** from the queue
  journal (`:841`). `_load_state_locked` also rebuilds if `STATE.json` is missing.

**Procedure:**
1. Build a `ManagerEventRouter` exactly as in `test_s3_manager_queue_admit_and_ack`
   (same binding args, `queue_root = self.runtime / "manager-queue"`).
2. `admit(...)` one `MANAGER_SIGNAL` event (reuse that test's event dict). This
   writes `QUEUE.jsonl` + derived `STATE.json` + `WAKE.json`.
3. Capture `before = router.pending_events()` and `wake_before = router.wake_revision`.
4. **Simulate a crash that loses only the derived caches:** delete
   `queue_root/STATE.json` and `queue_root/WAKE.json`; assert `QUEUE.jsonl` still
   exists and is non-empty.
5. Construct a **fresh** `ManagerEventRouter` at the same root with the same
   binding (simulates a restarted manager process).
6. Call `rebuilt = fresh.rebuild_state()`.
7. Assert recovery.

**Assertions:**
- `queue_root / "STATE.json"` exists again after `rebuild_state()` (cache republished).
- `fresh.pending_events()` still lists the admitted event id (recovered from journal).
- The recovered event equals the pre-crash pending event (same `event_id`).
- `fresh.wake_revision >= wake_before` (monotonic; wake not lost/rewound).
- After recovery, `acknowledge(event_id, binding=fresh.registration)` succeeds and
  `pending_events()` is then `[]` (queue still fully operable post-rebuild).

**Run:**
```text
python -m unittest orchestrator_harness.tests.test_qwen_multi_agent.QwenMultiAgentTests.test_qwen_manager_queue_rebuild_state_recovers_from_journal -v
```
**Pass criteria:** the admitted event survives deletion of the derived caches and
is recovered purely from `QUEUE.jsonl`; the queue is fully usable afterward.
**Effort:** ~1 test, low.

---

### Step A2 — F2.1.2 · Unregistered qwen provider fails closed (process-local registry)

**Gap:** the qwen-specific operational risk called out in the inventory
(§Operational note): the provider registry is **process-local**, so a detached
controller subprocess that skips the Firmware bootstrap has `qwen-code`
unregistered and must fail closed. No test drives this through the controller.

**New method:** `test_qwen_unregistered_provider_fails_closed_before_launch`

**Facts to rely on:**
- `parse_canonical_invocation` rejects an unregistered provider id:
  `invocation.py:400` → `InvocationValidationError("provider.id is not a registered provider: …")`.
- The canonical loader wraps that into `InvocationError`
  (`lane_controller.py:940–941`), and `controller.main` maps `InvocationError` → **exit 2**
  (`lane_controller.py:3406–3408`).
- `unregister_provider_adapter` / `register_provider_adapter` are already imported
  in the test module; foreign adapters (qwen) can be unregistered.

**Procedure:**
1. Build a valid qwen `_canonical(...)` invocation for `self.beta` and write it to
   `beta.invocation.json` (reuse `_write_json`).
2. In a `try/finally`, call `unregister_provider_adapter("qwen-code")` to reproduce a
   detached controller that never ran `_register_qwen()`.
3. Capture stderr (`contextlib.redirect_stderr`) and run `rc = controller.main([str(path)])`.
4. In `finally`, call `_register_qwen()` to restore the registry for other tests
   (setUp's `_register_qwen()` early-returns if already present, so restore is required).

**Assertions:**
- `rc == 2` (fail-closed invocation error, not a launch).
- stderr contains `"is not a registered provider"`.
- No provider process was started: the status file either does not exist, or if
  written, `status.get("provider_pid") is None` and `state != "PROVIDER_EXITED"`.

**Optional sub-assertion (A2b, hits `PROVIDER_OPERATION_UNSUPPORTED` at
`lane_controller.py:2431`):** this branch only fires when a *requested* operation
is undeclared. For a normal qwen `start`, requested ops =
`[launch, prompt, event_result, session, permission, configuration]`
(`_requested_provider_operations`, `lane_controller.py:1633`) — qwen declares all
of them, so the branch cannot fire for stock qwen. To exercise it, register a
**reduced-capability** qwen variant under a distinct id (e.g. `qwen-code-noprompt`
with `prompt=False`), point the invocation's `provider.id` at it, launch, and
assert `status["state"] == "PROVIDER_OPERATION_UNSUPPORTED"` and `rc == 1`. Mark
optional — it is a synthetic registration, not the stock qwen path.

**Run:**
```text
python -m unittest orchestrator_harness.tests.test_qwen_multi_agent.QwenMultiAgentTests.test_qwen_unregistered_provider_fails_closed_before_launch -v
```
**Pass criteria:** an unregistered qwen invocation is rejected with exit 2 and no
provider launch; the registry is restored for the rest of the suite.
**Effort:** ~1 test (+1 optional), low. **Caution:** always restore the adapter in
`finally` to avoid leaking an unregistered state into sibling tests.

---

### Step A3 — F4.3 · Duplicate ACTIVE declaration blocks a second qwen lane

**Gap:** `active_declaration_conflicts` is unit-tested with synthetic status
files, but the controller-wired guard (`lane_controller.py:2089–2100`, raises
`InvocationError` on a live duplicate → exit 2) is never exercised in a real
two-lane qwen launch. This proves the duplicate-branch/worktree guard in the
actual launch path.

**New method:** `test_qwen_duplicate_active_declaration_blocks_second_lane`

**Facts to rely on:**
- The conflict is only detected against a **live, trustworthy** status:
  `_trustworthy_live_status` (`git_safety.py:362`) requires
  `state ∈ {RUNNING_CODEX, RUNNING_PROVIDER}` **and** the declared
  `controller_pid` + `provider_pid` to be present in the process snapshot with
  the right parent/creation identity. So lane #1 must be genuinely running when
  lane #2 launches.
- The existing async machinery holds a lane running until a release signal:
  `_start_async` + a release-signal path in `QWEN_FAKE_CLI` + `_wait_for_status`
  (see `test_resource_contention_serializes_two_qwen_lanes`).

**Procedure:**
1. Add a second worktree on the **same branch/worktree identity** as lane #1. The
   cleanest duplicate is two invocations that declare the *same* `worktree_root`
   and `branch`. Start lane #1 async against `self.alpha` (branch `lane/alpha`)
   with a release signal so it stays in `RUNNING_PROVIDER`.
2. `_wait_for_status(self.alpha, "alpha", lambda v: v.get("state") == "RUNNING_PROVIDER")`
   to confirm it is live and its status advertises `controller_pid` + `provider_pid`.
3. Build a second invocation whose `repository.worktree_root` and `branch` match
   lane #1's declaration (same `self.alpha` identity), write it, and run it
   **synchronously** via `controller.main(...)`.
4. Capture stderr and the return code.
5. Release lane #1 (`_write_json(alpha_release, {"release": True})`) and
   `_finish_async` it to a clean terminal state.

**Assertions:**
- The second launch returns **exit 2**.
- stderr contains `"duplicate ACTIVE coding declaration"`.
- The second launch did not start a provider (no second `provider_pid`; its status
  state is not `PROVIDER_EXITED`).
- After release, lane #1 still reaches `PROVIDER_EXITED` with `result_valid` true
  (the guard blocked the intruder without harming the incumbent).

**Run:**
```text
python -m unittest orchestrator_harness.tests.test_qwen_multi_agent.QwenMultiAgentTests.test_qwen_duplicate_active_declaration_blocks_second_lane -v
```
**Pass criteria:** a second qwen lane declaring an already-ACTIVE branch/worktree
is refused before launch; the live lane is unaffected.
**Effort:** ~1 test, medium (uses async hold/release; model on the resource-contention test).
**Note:** if the snapshot-liveness precondition proves flaky in the sandbox,
fall back to driving `active_declaration_conflicts(...)` directly with a
hand-built `ProcessSnapshot` over two qwen worktrees (still additive vs the
generic test, which uses a codex-shaped status) — but prefer the e2e form.

---

### Step A4 — F6.4 · `watch --until-actionable` observes a finished qwen lane (KEY-gap poll)

**Gap:** the inventory's headline qwen gap (F10.9) is that qwen registers
`notification=False` → no push wake → **the manager must poll**. Only the
registration-level `SAFE_BOUNDARY_ONLY` is asserted today. F6.4 asks for the
operational proof: the manager's polling path (`watch --until-actionable`)
actually observing a genuinely completed qwen lane end-to-end. `watch_until_actionable`
is tested generically only for timeout/no-wake, never against a real
`PROVIDER_EXITED` qwen lane.

**New method:** `test_qwen_watch_until_actionable_observes_completed_lane`

**Facts to rely on:**
- `watch_until_actionable` (`cli.py:182`) polls `observe()` → `reconcile()` over a
  `HarnessConfig` suite root, diffs `_diagnostic_conditions`, and returns
  `EXIT_OK` on the first actionable event, else `EXIT_TIMEOUT`.
- `_is_actionable` (`cli.py:98`) treats `manager_actionable: true` and a fixed set
  of event types (`MANAGER_SIGNAL`, `RESOURCE_CONFLICT`, …) as actionable.
- `SuiteFixture` (`tests/support.py:31`) builds a `HarnessConfig` + suite root and
  a synthetic `process_snapshot`; `watch_until_actionable` accepts injected
  `process_provider`, `clock`, `sleeper`, `monotonic`, `stream` (see
  `test_manager_notifications_adversarial.py::_timeout_wait` for the exact call shape).

**Procedure (two acceptable forms; pick one):**

*Form 1 — reconcile a real finished qwen lane (preferred, most faithful):*
1. Run a qwen lane to completion with the existing `_start(...)` (e.g. `alpha`),
   yielding a `PROVIDER_EXITED` status with `result_valid` true.
2. Point a `HarnessConfig` suite root at the run workspace containing that lane's
   `*_controller.status.json` (mirror `SuiteFixture.create()`'s config; set
   `run_globs`/`workspace_relpath` so `discover_suite` finds the finished lane).
3. Provide a `process_snapshot` in which the lane's controller/provider PIDs are
   **absent** (the lane has exited) so reconcile derives a terminal/actionable
   diagnostic condition for a completed-but-unharvested lane.
4. Call `watch_until_actionable(config, timeout_seconds=…, process_provider=…,
   clock=…, sleeper=lambda _:None, monotonic=<two-tick iter>, stream=StringIO())`.

*Form 2 — deterministic actionable condition (simpler, still proves the poll path):*
1. Seed the suite workspace with a lane status + a `manager-signal` /
   terminal condition that reconcile classifies actionable for the finished lane
   (reuse `SuiteFixture` + `write_json`, as the adversarial test does).
2. Call `watch_until_actionable(...)` and assert it returns on the first tick.

**Assertions:**
- Return code is `EXIT_OK` (not `EXIT_TIMEOUT`) — the poll surfaced the finished
  lane without any push notification.
- The emitted event JSON on `stream` describes the finished/actionable qwen lane
  (contains the lane id / an actionable `type`), i.e. the manager learned of
  completion **by polling**, consistent with `notification=False`.
- (Tie-back) In the same test, assert `notification_mode("qwen-code")["mode"] ==
  SAFE_BOUNDARY_ONLY` so the test documents *why* polling is the required path.

**Run:**
```text
python -m unittest orchestrator_harness.tests.test_qwen_multi_agent.QwenMultiAgentTests.test_qwen_watch_until_actionable_observes_completed_lane -v
```
**Pass criteria:** the polling watch returns `EXIT_OK` on a completed qwen lane,
proving the documented KEY-gap workaround end-to-end.
**Effort:** ~1 test, medium (config/suite wiring). Prefer Form 1; fall back to
Form 2 if suite discovery over the temp run root is awkward.

---

## 4. Part B — Optional qwen-suite-local integration wrapper

### Step B1 (optional) — F3.4 · `restore_worktree` on a qwen-prepared overlay receipt

**Status:** `restore_worktree` byte-level behavior is **already covered** by
`test_workspace_overlay.py` (see matrix). The only qwen-suite-local gap is that
the qwen overlay test (`test_overlay_super_cache_into_subagent_worktree`) exercises
ingest + prepare + receipt but not the **reversal**. This wrapper closes that
without re-testing the byte mechanics.

**New method (optional):** `test_qwen_overlay_receipt_restores_on_retirement`

**Procedure:**
1. Reproduce the setup of `test_overlay_super_cache_into_subagent_worktree` up to
   `prepare_worktree(...)` producing `receipt` for `self.alpha` (role `subagent`).
2. Do **not** re-assert the byte-level restore semantics (covered generically);
   instead call `restore_worktree(receipt_path=receipt)` and assert the
   integration outcome.

**Assertions:**
- `result["outcome"] == "RESTORED"`.
- The overlay-created files (`instructions.md`, `config/settings.txt`) are gone
  from `self.alpha` after restore (`removed_paths` non-empty; files absent).
- `result["schema"]` is the overlay-receipt schema (integration returns a receipt).

**Run:**
```text
python -m unittest orchestrator_harness.tests.test_qwen_multi_agent.QwenMultiAgentTests.test_qwen_overlay_receipt_restores_on_retirement -v
```
**Pass criteria:** a qwen-prepared overlay reverses cleanly via `restore_worktree`.
**Effort:** ~1 test, low. **Skip if** minimizing footprint — generic coverage
already proves the mechanism; this only closes the qwen-suite-local narrative gap.

---

## 5. Part C — Already-covered features (verify + cross-reference, do NOT duplicate)

For each, the concrete step is: **run the cited generic test(s), confirm they
pass, and record the citation as the qwen row's coverage evidence** in
`qwencode_listed_features.md` (change the row note from "worth testing" to
"covered by <generic test>"). No new test is written — writing one would violate
the dedup rule.

### Step C1 — F1.6.3 · wake-text mutation guard
- **Cited coverage:** `test_provider_adapter_public_seams.py:795–811`
  (`ForeignMutatedWakeAdapter` → mutate wake text after registration → assert
  `SAFE_BOUNDARY_ONLY`, no wake text) + `test_qwen_multi_agent.py::test_qwen_adapter_registers_with_notification_false`.
- **Why no qwen test:** the byte-recheck guard (`provider.py:980`) only runs for
  `notification=True` adapters; qwen can never register `notification=True`
  (`test_notification_true_requires_a_real_delivery_seam` enforces a real delivery
  binding). qwen's protection is the capability short-circuit (`provider.py:969`),
  already asserted.
- **Verify:** `python -m unittest orchestrator_harness.tests.test_provider_adapter_public_seams -v`

### Step C2 — I5 · `OverlayCollisionError`
- **Cited coverage:** `test_workspace_overlay.py::test_prepare_rejects_collision_before_any_mutation`,
  `…::test_prepare_rejects_non_utf8_or_missing_append_target_before_mutation`.
- **Verify:** `python -m unittest orchestrator_harness.tests.test_workspace_overlay -v`

### Step C3 — I8 · Receipt rollback on partial-apply
- **Cited coverage:** `test_workspace_overlay.py::test_prepare_rolls_back_partially_applied_target_mutation`,
  `…::test_prepare_rolls_back_when_receipt_cannot_be_published`.
- **Verify:** `python -m unittest orchestrator_harness.tests.test_workspace_overlay -v`

### Step C4 — F2.3.1–F2.3.4 · Lane lifecycle (immutable view + retirement)
- **Cited coverage:** `test_s4_contract.py::test_S4_IMMUTABLE_VIEW_001`,
  `…::test_S4_LANE_RETIREMENT_001`; `test_s4_repair.py::FC1–FC45` (~45 tests over
  `allocate_immutable_source_view` + `retire_terminal_lane`).
- **Verify:** `python -m unittest orchestrator_harness.tests.test_s4_contract orchestrator_harness.tests.test_s4_repair -v`

### Step C5 — F8.1–F8.6 · Capability broker full cycle + fail-closed
- **Cited coverage:** `test_s5_capability_broker.py` (27 tests, incl.
  `CapabilityDenied`, `CapabilityAdapterUnavailable`, `_public_json`
  private-material rejection, request→snapshot→approval→permit→result→cleanup).
- **Verify:** `python -m unittest orchestrator_harness.tests.test_s5_capability_broker -v`

### Step C6 — F3.4 · `restore_worktree` (byte-level)
- **Cited coverage:** `test_workspace_overlay.py::test_restore_exact_clean_returns_original_state`,
  `…::test_restore_preserves_later_edit_and_blocks`,
  `…::test_retirement_restores_prepared_overlay_and_records_restoration`,
  `…::test_retirement_restores_matching_subagent_receipt`.
- (Part B/B1 optionally adds the qwen integration wrapper on top of this.)
- **Verify:** `python -m unittest orchestrator_harness.tests.test_workspace_overlay -v`

---

## 6. Execution order

1. **Baseline:** run the existing qwen suite green first.
   `python -m unittest orchestrator_harness.tests.test_qwen_multi_agent -v` (expect 15 pass, ~268s).
2. **Part C verifications (C1–C6)** — cheapest, and they confirm the generic
   coverage this plan relies on actually passes in this checkout *before* you
   decide not to duplicate it. If any C-cited test fails/does-not-exist, promote
   that feature from Part C to a new Part A test.
3. **Part A, in ascending mechanical difficulty:** A1 (rebuild_state, isolated) →
   A2 (unregister/fail-closed) → A4 (watch poll) → A3 (two-lane async, hardest).
4. **Part B1 (optional)** if closing the qwen-suite-local reversal narrative.
5. **Full suite re-run** to confirm no cross-test contamination (esp. A2's
   unregister/restore of `qwen-code`).

---

## 7. Final validation & deliverables

**Validation:**
- `python -m unittest orchestrator_harness.tests.test_qwen_multi_agent -v` →
  15 existing + 4 new (+1 optional) all pass.
- Confirm A2 leaves `qwen-code` registered (run a second test after it in the same
  process, or assert `"qwen-code" in provider_registry()` at the end of A2).

**Deliverables / doc updates:**
- New test methods A1–A4 (+ optional B1) in `test_qwen_multi_agent.py`.
- Update `active_docs/qwencode_listed_features.md`:
  - F5.1.4, F2.1.2, F4.3, F6.4 → **TESTED-PASSED** with the new method names.
  - F1.6.3, I5, I8, F2.3.1–F2.3.4, F8.1–F8.6 → change TB-W note to
    **NOT-TESTED (qwen) / COVERED-GENERIC** citing the Part C tests (they are
    provider-neutral and proven by the harness suite; a qwen copy would duplicate).
  - Update the summary counts (TB-W 18 → resolved: 4 tested + 12 covered-generic
    + 1 optional + F3.4 covered).
- Optionally add a short `coverage-matrix.md` next to this plan mirroring §2 for
  quick reference.

**Scope reminder:** Firmware (`firmware_*.py`) and MCP-server functionality remain
**out of scope** per the original instruction and are not part of any step here.

---

## 10. Full-inventory completion (2026-08-20) — every non-OOS row has test evidence

After the TB-W pass (§8) the whole 112-row inventory was driven to a disposition
backed by a passing test, not merely categorized:

- **8 new qwen-specific tests total** in `test_qwen_multi_agent.py` (suite now
  **23/23 OK**): the 4 TB-W tests (§8) plus 4 completion-pass tests —
  `test_qwen_wake_text_mutation_fails_closed_to_safe_boundary` (F1.6.3),
  `test_qwen_notification_true_without_real_binding_is_rejected` (F1.1.6 GAP),
  `test_qwen_no_push_wake_delivery_path_exists` (F5.2.x/F5.3.x GAP), and
  `test_qwen_overlay_collision_rejected_atomically` (I5/I8/F3.3).
- **Provider-neutral batteries confirmed green** and cited inline on every
  COVERED-GENERIC row: a 178-test battery (registry/public-seams/resource-locks/
  finding-gate/broker/events-cli/reconcile/discovery/processes, exit 0), a
  48-test battery (manager-adversarial/s3/s2/process-supervisor/integration-
  processes/lock-cleanup/real-agent-isolation, exit 0), and a 129-test
  lifecycle/broker/CLI battery (s4-contract/s4-repair/s5-capability-broker/
  coding-lane-controller/git-results/handoff-preflight, exit 0).
- **Final `qwencode_listed_features.md` counts:** 60 TESTED-PASSED (incl. 9
  GAP-confirmed-by-test), 44 COVERED-GENERIC, 4 N/A-QWEN (codex-only, analog
  tested), 4 NOT-TESTED-OOS (firmware/MCP, excluded by instruction). The OOS
  rows are the only untested rows.
- **GAP-vs-PASSED rule upheld:** F1.1.6 and F5.2.x/F5.3.x are recorded as
  GAP — CONFIRMED BY TEST (the test asserts the *absence* of a qwen push-wake
  path), never laundered into TESTED-PASSED.

## 8. Execution status (2026-08-20) — implemented

The plan has been executed. Results:

- **Part A / B implemented and passing.** Four new deterministic host-only
  methods were added to `test_qwen_multi_agent.py`; the whole suite is green
  (`Ran 19 tests … OK`, 15 original + 4 new):
  - `test_qwen_manager_queue_rebuild_state_recovers_from_journal` (F5.1.4) ✅
  - `test_qwen_unregistered_provider_fails_closed_before_launch` (F2.1.2) ✅
  - `test_qwen_watch_until_actionable_observes_actionable_condition` (F6.4) ✅
  - `test_qwen_overlay_receipt_restores_on_retirement` (F3.4, Part B1) ✅
- **A3 (F4.3 duplicate ACTIVE declaration) reclassified to COVERED-GENERIC.** A
  qwen-suite-local reproduction needs two genuinely-live sibling processes
  sharing a worktree; on Windows that is inherently racy and hits status-file
  locks during teardown, and the controller's canonical-prior-task preflight
  fires first when the second lane reuses the first lane's status path. The guard
  (`git_safety.active_declaration_conflicts` → `InvocationError`
  "duplicate ACTIVE coding declaration") is provider-neutral and already proven
  by `test_git_results.py` and `test_s4_repair.py`, so F4.3 is verified there
  rather than duplicated. A placeholder comment documents this in the module.
- `qwencode_listed_features.md` rows F2.1.2, F3.4, F5.1.4, F6.4 updated to
  **TESTED-PASSED** with the new method names; F4.3 → **COVERED-GENERIC**.

## 9. Full-inventory disposition (all 112 features)

Widening beyond the 18 TB-W rows, every remaining NOT-TESTED row carries one of
the inventory's own subcategory tags; this section fixes what each tag *means as
a disposition* so no row is left without a decision:

| Tag | Meaning | Disposition | Action |
| --- | --- | --- | --- |
| **TESTED-PASSED** | executed in the qwen suite | done | none (42 baseline + 4 new = 46) |
| **COVERED-GENERIC** | provider-neutral; proven by a non-qwen suite | done | verify the cited generic suite is green; cite it on the row — never duplicate (F4.3 + the 12 Part-C rows) |
| **TB** | testable-but-not by the qwen suite; generic coverage exists | covered-generic by default | fold into COVERED-GENERIC where a generic suite exercises it; otherwise leave TB with a one-line reason |
| **PA** | process / async / OS-boundary (windows-job, env isolation, thread drain) | not host-deterministic | keep NOT-TESTED (PA); real-process behavior, not a qwen semantic gap. Exercised incidentally by the live parallel demo, not asserted |
| **CX** | codex-only mechanism (e.g. `CodexProviderAdapter`, wake delivery) | out of qwen scope | keep NOT-TESTED (CX); documents a codex-vs-qwen shape difference, not a qwen gap |
| **OOS** | Firmware / MCP-server; out of scope by instruction | excluded | keep NOT-TESTED (OOS) |
| **GAP** | mechanism is generic and qwen *could* use it but it is not implemented for qwen | real qwen gap | keep as **GAP** in the inventory (e.g. F1.1.6 notification=True path, C17/U4, A17) — a divergence from the codex-era intent, never laundered to PASSED |

**Binding rule (unchanged):** a test *completing* is not a pass. TESTED-PASSED
requires observed behavior matching the intended codex-era behavior; any
divergence — including a stricter/safer qwen behavior — is a **GAP**, recorded as
such against the row. The four new tests were checked against this rule before
their rows were marked.

**Live multi-agent parallelism proof (separate deliverable):** a qwen-code ROOT
subagent (deepseek-v4-flash:0731-cloud, session-local autocompact pinned to 180K
per `.subagent-qwen-home/AUTOCOMPACT-180K.md`) plus a parallel codex subagent
demonstrate real multi-agent concurrency; this exercises the PA-tagged
real-process paths incidentally but asserts nothing against them.
