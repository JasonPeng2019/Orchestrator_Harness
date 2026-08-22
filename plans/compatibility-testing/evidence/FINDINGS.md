# Findings — compatibility testing (phases 1–4)

New gaps or defects discovered while running the detection-only test suite. A finding here
is a **valid, recorded outcome** — the plan convention is to record, not "fix to green"
(only phase 0 changed code). Each row links to the evidence dir for the step that found it.

Format: one row per finding. `Severity`: blocker / defect / gap / note.

> **RESOLVED-PARITY (2026-08-20).** Six findings — **F1D-E19-1, F1G-K8-1, F2B-L4-1, F2B-L7-1,
> F1K-Q1-1, F1K-Q17-1** — were re-dispositioned from GAP to `TESTED-PASSED (parity)` in
> `active_docs/claude_listed_Features.md`. Rationale: each was tested against a **shared**
> `orchestrator_harness` module (there is no `claude_adapter`/`codex_adapter` split for config
> loading, invocation validation, the capability broker, or prompt composition), so the Claude
> provider already runs Codex's exact mechanism. The recorded "divergence" was between the plan
> **text** and the shared implementation — not between the two providers. Per the operator decision
> that the Claude code must mirror Codex's exact mechanism, that condition is already satisfied here.
> The detail sections below are retained as-is for the historical record; they remain accurate about
> *what the code does* — only the disposition (GAP → parity pass) changed. **U15-CANCELLED** remains
> the sole genuine Codex-vs-Claude provider divergence and is unclosable (upstream CLI emits no
> cancel event). **F2G-A39-1** is flagged **stale** — the ordered recovery ledger it reports missing
> exists in `harness_watcher_implementation/state.py` (`ORDER`/`transition`/out-of-order guard); the
> test observed `watcher_integration.watcher_recovery_projection` instead. Re-test pending.

| ID | Phase/Step | Feature | Severity | Summary | Evidence |
|---|---|---|---|---|---|
| F1A-C24-1 | 1 / 1.A | C24 `_classify_provider_operations` | note | unknown-operation branch is dead code: it raises `ProviderAdapterError` instead of emitting the intended unsupported-operation record | evidence/1.A |
| F1D-E19-1 | 1 / 1.D | E19 `_trustworthy_live_status` state gate | note | **[RESOLVED-PARITY 2026-08-20 → TESTED-PASSED]** the RUNNING_CODEX/RUNNING_PROVIDER gate is scoped to conflict detection; discovery-level result acceptance does not reject a result offered under `EXITED`/`PROVIDER_EXITED` | evidence/1.D |
| F1D-E20-1 | 1 / 1.D | E20 result-candidate ambiguity | note | no "more than one candidate result JSON" ambiguity rejection exists; `RESULT.json` is the single canonical result path and a second result-shaped JSON is silently ignored (only the >256 bound in `active_declaration_conflicts` fires) | evidence/1.D |
| F1E-F3-1 | 1 / 1.E | F3 `WAITING_RELAY` elevation | note | lane elevates to `WAITING_RELAY` only when a matching request is `RELAY_READY`; a request that is `RELAY_UNBOUND` (relay file exists but cannot bind) leaves the lane in `RUNNING_CODEX`, not `WAITING_RELAY` | evidence/1.E |
| F1E-F24-1 | 1 / 1.E | F24 result-validation memo | note | the validation memo (`_RESULT_VALIDATION_CACHE`) covers only the coding-result path (`_validate_coding_result_cached`); the task-result path (`_validate_task_result_cached`) is not memoized and re-validates on every pass | evidence/1.E |
| F1F-G18-1 | 1 / 1.F | G18 `HARNESS_SCAN_COMMITTED` | note | the kind is declared in the taxonomy (`notifications.py:115`, OBSERVED) and in the watcher KINDS (`attention.py:37`) but no producer in this worktree emits it; "exactly once per scan commit" is observable only at the record-contract level (`make_source_record` → one record) | evidence/1.F |
| F1F-G1-1 | 1 / 1.F | G1 `REQUEST_EXPIRY_WARNING` selectability | note | an expiry request with `expiry_bucket:"EXPIRED"` is emitted (severity error) but never selectable — `_priority` returns 1 only for buckets WARNING/CRITICAL (`notifications.py:1697-1703`) | evidence/1.F |
| F1F-G5-1 | 1 / 1.F | G5 `OBSERVATION_ERROR` selectability | note | `OBSERVATION_ERROR` is emitted for any `observation_errors` entry but is actionable (priority 2) only when `_active_lanes(snapshot)` or a LIVE request exists (`notifications.py:1727-1735`); a lone malformed signal is emitted-but-unselected | evidence/1.F |
| F1B-B2-1 | 1 / 1.B | B2 `scan --no-write` flag | note | the `scan --no-write` flag is parsed (`cli.py:243`) but the scan dispatch calls `scan_command(config)` with no `no_write` argument (`cli.py:439`) and `scan_command` has no such parameter (`cli.py:82`); the flag is a pure no-op (the no-write guarantee holds only vacuously — one-shot scan never persists in any mode) | evidence/1.B |
| F1G-K8-1 | 1 / 1.G | K8 resume thread-ID precedence | note | **[RESOLVED-PARITY 2026-08-20 → TESTED-PASSED]** the plan describes "canonical `resume_identity.thread_id` wins per documented precedence"; the real coding-v1 adapter instead fails **closed** — when both `resume_thread_id` and `resume_identity.thread_id` are present and differ it raises `InvocationValidationError("conflicting requested resume thread IDs")` (`invocation.py:716-722`) rather than silently letting either win | evidence/1.G |
| F1K-Q1-1 | 1 / 1.K | Q1 `load_config` numeric bounds | note | **[RESOLVED-PARITY 2026-08-20 → TESTED-PASSED]** the plan describes out-of-range config numbers "clamp to bounds"; the real `_number`/`_integer` helpers (`config.py:62,74`) **reject** them — an out-of-range value raises `ConfigError("{key} must be >= {minimum}")` rather than being silently clamped (stricter/safer) | evidence/1.K |
| F1K-Q17-1 | 1 / 1.K | Q17 `prompt.py` template constants | note | **[RESOLVED-PARITY 2026-08-20 → TESTED-PASSED]** the plan describes asserting "documented template constants / templates" in `prompt.py`; the module contains **no** template constants — it is a pure compatibility re-export shim (7-name `__all__`, object-identity re-exports of `prompt_bundle`), and `compose_prompt_bundle` performs verbatim ordered concatenation with no placeholder substitution | evidence/1.K |
| F2A-I4-1 | 2 / 2.A | I4/A9 `verify_overlay_receipt` byte-integrity | note | the plan's I4 says "corrupt one materialized byte and re-verify [via `verify_overlay_receipt`] → verification fails"; reality: `verify_overlay_receipt` is a structural/identity prelaunch check (REQ-O41) that **never reads materialized worktree bytes** — byte-integrity is enforced at `restore_worktree` (exact `post_prepare_bytes` comparison, `workspace_overlay.py:789-795`). A corrupted worktree byte still verifies `True`; only `restore_worktree` reports `BLOCKED` "later edit detected" | evidence/2.A |
| F2B-L4-1 | 2 / 2.B | L4 bounded single-use grant | note | **[RESOLVED-PARITY 2026-08-20 → TESTED-PASSED]** the plan describes a per-permit bounded-use counter; reality: `CapabilityPermit` is an immutable value with **no** `use_count`/`uses_remaining` field — bounded use is broker-enforced via (a) idempotent terminal-result reuse for an exact retry (`dispatch_calls` stays 1) and (b) replay refusal — `REPLAY_MISMATCH` when the request identity is reused under changed semantics, durable `APPROVAL_REPLAY` when a consumed approval's provenance changes (`_used_approvals` seam) | evidence/2.B |
| F2B-L7-1 | 2 / 2.B | L7 missing-adapter fail-closed | note | **[RESOLVED-PARITY 2026-08-20 → TESTED-PASSED]** the plan says pointing at a missing adapter raises `CapabilityAdapterUnavailable` to the caller; reality: the broker **catches** an adapter's `CapabilityAdapterUnavailable` raised from `observe` and returns a `DENIED` result with reason `SNAPSHOT_UNAVAILABLE` (`capability_broker.py:1400-1406`) — the typed exception does not propagate out of `execute`. No permit is constructed and `dispatch_calls` stays 0 (fail-closed, safer than the plan text) | evidence/2.B |
| F2C-P7P11-1 | 2 / 2.C | P7/P11 retirement refusal shape | note | the plan phrases P7 (mismatched lane binding) and P11 (missing process proof) as "rejected", implying a raised exception; reality: `retire_terminal_lane` refuses **fail-closed by returning a blocked result** (`outcome == "VISIBLE"`, lane left present) rather than raising — P7 reason `ARCHIVE_EVIDENCE_INCOMPLETE:canonical lifecycle registry root is missing or unsafe` (and `_validate_lane_binding` itself returns `(None, "LANE_BINDING_FOREIGN_WORKTREE")` for a forged `lane_id`), P11 reason `PROCESS_SNAPSHOT_INCOMPLETE` when `process_snapshot` is unproved. Both are correct fail-closed behavior; the note only records that the refusal is an outcome field, not an exception | evidence/2.C |
| F4A-G17-1 | 4 / 4.A | G17 resume-wake failure path | note | the plan phrases the WAKE_FAILED path as the transport raising to the caller; reality: `DeliveryCoordinator.deliver_at_boundary` **converts** a transport exception into a `DELIVERY_FAILED` receipt (fail-closed, `host_adapters.py:1004`) rather than re-raising, and no `resume_invocation` is recorded. `test_G17` pins that safer provider-neutral contract — TESTED-PASSED, not a divergence | evidence/4.A |
| F4B-B9-1 | 4 / 4.B | B9 install rollback wrapping | note | the plan phrases an ambiguous owned-id install as raising `CodexInstallConflict`; reality: the bounded installer wraps it as `CodexInstallRollback` (`__cause__` = `CodexInstallConflict`) so the transaction is visibly atomic, and the manifest is absent afterward. `test_B9` asserts both layers — TESTED-PASSED, stricter/safer than the plan text | evidence/4.B |

---

## Detail

### F1A-C24-1 — `_classify_provider_operations` never returns an unsupported-operation record

**What was tested:** `_classify_provider_operations("claude-code", ["teleport"])` with an
operation outside `PROVIDER_OPERATION_NAMES`.

**Fabricated input:** `["teleport"]` (not in `PROVIDER_OPERATION_NAMES`).

**Expected:** the branch at `lane_controller.py:1692-1699` builds an explicit
unsupported-operation record via `unsupported_operation_result(...).as_record()` with
`supported=False` and reason `"operation is not part of the provider contract"`.

**Observed:** `unsupported_operation_result` itself raises
`ProviderAdapterError("unknown provider operation: teleport")` at `provider.py:909`, so the
record-producing branch in `_classify_provider_operations` is unreachable. The actual,
documented behavior is a raise (no silent acceptance of any mutation). Severity `note`: the
branch is latent — `_requested_provider_operations` only ever emits operations from
`PROVIDER_OPERATION_NAMES`, so the dead path cannot fire from a validated invocation today.

**Code under test:** `orchestrator_harness/lane_controller.py:1692-1699` and
`orchestrator_harness/provider.py:904-924` (`unsupported_operation_result`).

**Test:** `test_c24_provider_operation_classification_and_handoff_identity` documents the
actual raise behavior and stays green.

## Detail

### F1D-E19-1 — the operational-state gate does not gate discovery-level result acceptance

**What was tested:** `discover_run` with a coding status whose `state` is
`PROVIDER_EXITED` (i.e. not `RUNNING_CODEX`/`RUNNING_PROVIDER`) and a valid
`RESULT.json` offered under that status.

**Fabricated input:** status `orchestrator-lane-controller/v1` with
`invocation_schema="orchestrator-coding-invocation/v1"`, `state="PROVIDER_EXITED"`,
`declared_lane_id="coding:one"`, `worker_invocation_id="worker-1"`, and a self-consistent
`repository` declaration; a valid `orchestrator-lane-result/v1` `RESULT.json`.

**Expected (plan E19):** a result offered while the state is e.g. `EXITED` is rejected —
the operational-state gate accepts only `RUNNING_CODEX`/`RUNNING_PROVIDER`.

**Observed:** the gate `str(raw.get("state", "")).upper() not in {"RUNNING_CODEX",
"RUNNING_PROVIDER"}` (`git_safety.py:370-373`) exists but is scoped to
`_trustworthy_live_status`, which only feeds `active_declaration_conflicts`. Discovery-level
result acceptance (`discovery.py:844-895`) selects the coding lane by
`declared_lane_id`/`worker_invocation_id` matching and never consults controller state, so
the valid result is accepted (`result` set, `invalid_result` None) even under
`PROVIDER_EXITED`. Severity `note`: no mutation is silently accepted — a malformed result is
still rejected — but the gate does not mean what the plan text says it means.

**Code under test:** `orchestrator_harness/git_safety.py:370-373`
(`_trustworthy_live_status`) and `orchestrator_harness/discovery.py:844-895`
(`discover_run` result acceptance).

**Test:** `test_e19_result_offered_under_exited_state_is_still_accepted` documents the
actual behavior and stays green; `test_e19_operational_state_gate` documents the gate as it
exists (RUNNING_PROVIDER considered, EXITED not considered).

## Detail

### F1D-E20-1 — no "more than one candidate result JSON" ambiguity rejection

**What was tested:** dropping two result-shaped JSON files under the result workspace —
`RESULT.json` (valid) plus a second `SECOND-RESULT.json` — and running `discover_run`.

**Fabricated input:** workspace containing `coding-status.json` (live controller status),
`RESULT.json` (valid PASS result), and `SECOND-RESULT.json` (a valid-shaped FAIL result).

**Expected (plan E20):** the second candidate triggers an ambiguity rejection (the
`_MAX_JSON_CANDIDATES_PER_WORKTREE` bound is the too-many bound; the ">1 ambiguity path"
rejects).

**Observed:** discovery reads only `workspace / "RESULT.json"`
(`discovery.py:826`) as the result candidate; `SECOND-RESULT.json` is not a conventional
`*_controller.status.json` nor an `orchestrator-lane-controller/v1` schema, so it is skipped
as a status candidate and never considered. No ambiguity rejection fires. The only
too-many guard is `len(paths) > _MAX_JSON_CANDIDATES_PER_WORKTREE` (256) inside
`active_declaration_conflicts` (`git_safety.py:415-416`), which is about `.agent-workspace`
status candidates, not result candidates — and 2 files do not approach it. Severity `note`:
behavior is deterministic (the canonical result path wins), but the plan-described
ambiguity rejection does not exist.

**Code under test:** `orchestrator_harness/git_safety.py:415-416`
(`active_declaration_conflicts` bound) and `orchestrator_harness/discovery.py:826`
(single canonical `RESULT.json` path).

**Test:** `test_e20_two_result_candidates_select_resolved_result_json` documents the actual
deterministic selection; `test_e20_too_many_json_candidates_bound` documents the real
>256 bound in `active_declaration_conflicts`.

## Detail

### F1E-F3-1 — `WAITING_RELAY` elevation fires only on `RELAY_READY`, not `RELAY_UNBOUND`

**What was tested:** a coding lane with a matching run-request whose relay classification is
`RELAY_UNBOUND` (a relay file exists on disk but cannot bind — wrong hash / unproven identity),
versus the `RELAY_READY` control.

**Fabricated input:** live coding lane fixture + a run-request; in one case the request derives
`RELAY_READY` (live request, no bindable relay yet), in the other `RELAY_UNBOUND` (an
unbindable relay file present).

**Expected (plan F3):** an unbound relay + a pending request drives the lane's
`operational_state` to `WAITING_RELAY`.

**Observed:** elevation to `WAITING_RELAY` happens only when a matching request is
`RELAY_READY` (`reconcile.py:1355-1358`: `if any(item["operational_state"] == "RELAY_READY" ...)`).
A `RELAY_UNBOUND` request does not elevate — the lane stays `RUNNING_CODEX`. Severity `note`:
this is a defensible distinction (an unbindable relay is a different condition than "waiting
for a relay to arrive"), and the request itself is still classified `RELAY_UNBOUND`, so no
state is lost — but the lane-level elevation is narrower than the plan text implies.

**Code under test:** `orchestrator_harness/reconcile.py:1352-1358`.

**Test:** the F3 test documents both the `RELAY_READY`→`WAITING_RELAY` elevation and the
`RELAY_UNBOUND`→(lane stays `RUNNING_CODEX`) behavior, and stays green.

## Detail

### F1E-F24-1 — result-validation memo covers coding results but not task results

**What was tested:** validating the same result twice through each cached entry point and
observing `_RESULT_VALIDATION_CACHE`; then changing the record signature.

**Fabricated input:** a valid coding result and a valid task result (real disposable
`git init` worktree, the `test_compat_git_safety` idiom), each validated twice, then re-validated
after a field change.

**Expected (plan F24):** a memoized coding/task-result validation cache — second validation of
an unchanged record hits the cache; a signature change invalidates it.

**Observed:** the coding-result path is memoized (`_validate_coding_result_cached`,
`discovery.py:566-608`): repeat validation hits the cache (size unchanged), a signature change
adds a new key (cache grows), and a cached invalid `(False, detail)` is re-raised on repeat.
The task-result path (`_validate_task_result_cached`, `discovery.py:611`) does **not** touch
`_RESULT_VALIDATION_CACHE` at all — it re-runs validation every time and never populates the
cache. Severity `note`: a missing optimization, not a correctness gap — task-result validation
is still correct, just not memoized.

**Code under test:** `orchestrator_harness/discovery.py:88` (`_RESULT_VALIDATION_CACHE`),
`:566-608` (coding-result cached path), `:611+` (task-result path, uncached).

**Test:** the F24 test asserts the coding-result cache hit / invalidation / cached-invalid
re-raise, and documents the task-result non-memoization, staying green.

## Detail

### F1F-G18-1 — `HARNESS_SCAN_COMMITTED` is declared but has no in-repo emitter

**What was tested:** membership of `HARNESS_SCAN_COMMITTED` in the notification taxonomy and
the watcher KINDS, and `make_source_record(kind="HARNESS_SCAN_COMMITTED")` producing exactly one
record; plus a grep for any producer that emits it.

**Expected (plan G18):** run a scan → the atomic scan-commit marker is present exactly once.

**Observed:** the kind is a valid, OBSERVED-disposition taxonomy member
(`notifications.py:115`) and a valid watcher record kind (`attention.py:37`), and
`make_source_record` yields exactly one record per call — but no code path in this worktree
emits the marker as part of a scan commit, so the "once per scan commit" guarantee can only be
demonstrated at the record-contract level, not driven end-to-end. Severity `note`: the taxonomy
declaration is correct and single-valued; the emission path is simply absent here (likely lives
in the watcher-side runtime, out of this worktree).

**Code under test:** `orchestrator_harness/notifications.py:115`,
`harness_watcher_implementation/attention.py:37`.

**Test:** `test_g18_scan_committed_marker_exactly_once` documents the record-contract behavior
and stays green.

## Detail

### F1F-G1-1 — `REQUEST_EXPIRY_WARNING` is selectable only for WARNING/CRITICAL buckets

**What was tested:** priority/selection of a `REQUEST_EXPIRY_WARNING` event across
`expiry_bucket` values WARNING, CRITICAL, and EXPIRED.

**Fabricated input:** expiry events with each bucket value, fed through `_priority` /
`select_actionable`.

**Expected (plan G1):** `REQUEST_EXPIRY_WARNING` is in the actionable class.

**Observed:** it is actionable at priority 1 for buckets `WARNING`/`CRITICAL` only. An
`EXPIRED`-bucket request is still emitted by `conditions_from_snapshot` (as severity `error`,
`events.py:287-303`) but `_priority` returns `None` for it (`notifications.py:1697-1703`), so it
is never selected. Severity `note`: no manager-actionable signal is silently dropped in a way
that hides a live condition — an EXPIRED request has already passed its warning window — but the
selectability boundary is narrower than the plan's blanket "actionable" implies.

**Code under test:** `orchestrator_harness/notifications.py:1697-1703`,
`orchestrator_harness/events.py:287-303`.

**Test:** the G1 test asserts WARNING/CRITICAL selected at priority 1 and EXPIRED → not
selected, staying green.

## Detail

### F1F-G5-1 — `OBSERVATION_ERROR` is selectable only when a lane/request is live

**What was tested:** selection of an `OBSERVATION_ERROR` event with and without an active lane /
LIVE request in the snapshot.

**Fabricated input:** a snapshot carrying an `observation_errors` entry (a) alongside an active
lane / LIVE request, and (b) with only a lone malformed manager signal and no live lane.

**Expected (plan G5):** `OBSERVATION_ERROR` is one of the process-health events surfaced.

**Observed:** it is emitted for any `observation_errors` entry, but `_priority` returns 2
(actionable) only when `_active_lanes(snapshot)` is true or a request has
`lifetime_state == "LIVE"` (`notifications.py:1727-1735`); otherwise it returns `None` and the
event is emitted-but-unselected. Severity `note`: consistent with the harness only paging a
manager when there is live work to act on, but the emission-vs-selection split is worth
recording.

**Code under test:** `orchestrator_harness/notifications.py:1727-1735`.

**Test:** the G5 test asserts emission in both cases and selection only in the live-lane case,
staying green.

## Detail

### F1B-B2-1 — `scan --no-write` is a parsed-but-ignored no-op flag

**What was tested:** the `scan` subcommand's `--no-write` flag: a full digest of the run-root
directory tree before and after a scan, and inspection of how the flag is dispatched.

**Fabricated input:** a `SuiteFixture` run-root; `scan_command(config, stream=...)` invoked (the
CLI dispatch for `scan`), with and without `--no-write`.

**Expected (plan B2):** `scan --no-write` is diagnostic-only — no snapshot/event mutation on disk.

**Observed:** the guarantee holds, but **vacuously**: `scan_command` (`cli.py:82`) has no
`no_write` parameter and never persists anything in any mode (it calls `observe(...)` and prints,
with no store). The `--no-write` flag is registered on the parser (`cli.py:243`) but the scan
dispatch is `if args.command == "scan": return scan_command(config)` (`cli.py:438-439`) — the
flag is never read. Severity `note`: no data is ever written by scan, so the ignored flag is
harmless, but it is misleading (a user could believe `--no-write` is what makes scan safe).

**Code under test:** `orchestrator_harness/cli.py:82` (`scan_command`, no `no_write` param),
`:243` (flag registered), `:438-439` (dispatch ignores it).

**Test:** `test_b2_scan_no_write_diagnostic_only` asserts the run-root tree is byte-identical
before/after and documents the flag as a no-op, staying green.

## Detail

### F1G-K8-1 — conflicting resume thread IDs fail closed rather than "canonical wins"

**What was tested:** the coding-v1 → canonical adaptation of the resume thread identity when
both the legacy `resume_thread_id` field and the canonical `resume_identity.thread_id` field
are supplied.

**Fabricated input:** a valid `orchestrator-coding-invocation/v1` record with (a) both fields
present and equal (`"thread-1"`); (b) each field present alone; and (c) both present but
differing (`resume_thread_id="thread-legacy"`, `resume_identity.thread_id="thread-canonical"`).

**Expected (plan §1.G K8):** the canonical `resume_identity.thread_id` wins per a documented
precedence order — a conflicting legacy value is dropped in favor of the canonical one.

**Observed:** equal values resolve to the shared value and each single-field spelling resolves
to its own value, but a **conflict** does not resolve by precedence — `adapt_coding_v1` raises
`InvocationValidationError("conflicting requested resume thread IDs")`
(`invocation.py:716-722`). The adapter fails closed, so a conflicting legacy thread ID can
never be silently dropped without detection. Severity `note`: this is *safer* than the plan
text (fail-closed beats silent precedence), and matches the sibling worker-invocation-id
conflict guard at `invocation.py:709-712`; the divergence is only that the behavior is a
rejection, not a documented winner.

**Code under test:** `orchestrator_harness/invocation.py:698-723` (resume thread
canonicalization; conflict raise at `:716-722`).

**Test:** `test_k8_thread_id_precedence_is_conflict_rejection` pins the equal / single-field /
conflict-rejection behaviors and stays green.

### F1K-Q1-1 — out-of-range config numbers are rejected, not clamped

**What was tested:** `load_config` on a fabricated config JSON carrying numeric values below
their documented minimum (`poll_interval_seconds: 0.0` vs. minimum `0.05`;
`stable_read_retries: 0` vs. minimum `1`).

**Fabricated input:** temp config file with `poll_interval_seconds: 0.0` (and, separately,
`stable_read_retries: 0`), plus valid `suite_root`/`run_globs`.

**Expected (plan text):** Q1 says out-of-range numbers "clamp to bounds" — i.e. the loaded
config would carry the clamped minimum.

**Observed:** `_number` (`config.py:69-70`) and `_integer` (`config.py:78-79`) raise
`ConfigError("{key} must be >= {minimum}")` — the config is **rejected**, never silently
clamped. Non-numeric/bool → `"must be numeric"`/`"must be an integer"`; non-finite (`1e999`
→ `inf`) → `"must be finite"`. A valid in-range config carries the exact value unchanged.
Severity `note`: the actual behavior is *stricter and safer* than the plan (fail-closed
rejection beats silent clamping, which could mask an operator misconfiguration).

**Code under test:** `orchestrator_harness/config.py:62-80` (`_number`, `_integer`).

**Test:** `test_q1_load_config_numeric_bounds_reject_instead_of_clamp` (plus
`_non_numeric_and_non_integer_reject` and `_valid_in_range_numeric_config_carries_exact_value`)
pins the reject-not-clamp behavior and stays green.

### F1K-Q17-1 — `prompt.py` is a re-export shim with no template constants

**What was tested:** the public surface of `orchestrator_harness/prompt.py` and whether
`compose_prompt_bundle` performs any placeholder/template substitution.

**Fabricated input:** a bundle composed from components whose bytes contain placeholder-looking
literals `{{instructions}}` and `{bundle_sha256}`.

**Expected (plan text):** Q17 says to assert "documented template constants / templates exist
and compose without unresolved placeholders."

**Observed:** `prompt.py` contains **no** template constants — it is a pure compatibility
re-export shim whose entire non-dunder namespace is exactly its 7-name `__all__`
(`PROMPT_BUNDLE_SCHEMA`, `PromptBundle`, `PromptBundleError`, `PromptComponent`,
`bundle_from_record`, `compose_prompt_bundle`, `prompt_bundle_record_from_paths`), each name
being the *same object* as in `prompt_bundle`. The real "composes without unresolved
placeholders" contract is that `compose_prompt_bundle` concatenates component bytes verbatim in
order — the placeholder-looking literals survive byte-for-byte, because no substitution step
exists anywhere in the pipeline. Severity `note`: the plan's "template constants" premise does
not match the module; the actual re-export + verbatim-concatenation contract is pinned instead.

**Code under test:** `orchestrator_harness/prompt.py:1-22` (re-export surface);
`orchestrator_harness/prompt_bundle.py:176-208` (`compose_prompt_bundle`).

**Test:** `test_q17_prompt_module_reexports_exactly_its_documented_all` and
`test_q17_compose_is_ordered_concatenation_no_substitution` pin the surface and stay green.

<!-- Append a `### <finding-id>` section per finding with: what was tested, the fabricated
input, the expected vs. observed behavior, and the file:line of the code under test. -->

### F2A-I4-1 — `verify_overlay_receipt` never reads materialized worktree bytes

**What was tested:** after a real `prepare_worktree` (cache with one created file +
one declared-append file), (a) `verify_overlay_receipt(receipt_path=…,
expected_target_worktree_id=<target>, role="subagent")` on the untouched worktree;
(b) corrupting **one materialized worktree byte** (`created.txt` gains one extra
byte) and then re-running `verify_overlay_receipt`; (c) the same corrupted byte fed
to `restore_worktree`.

**Fabricated input:** disposable temp-dir cache `{created.txt, notes.txt,
.super-cache.json(append_text:["notes.txt"])}`, target pre-seeded with `notes.txt`
= `b"original-notes\n"`, receipt under `temp/receipts/overlay-receipt.json`.

**Expected (plan I4):** "corrupt one materialized byte and re-verify → verification
fails."

**Observed:** `verify_overlay_receipt` is a structural/identity prelaunch check
(REQ-O41): it validates the receipt's closed shape, `completed:true`, role, and
target-worktree-ID — then returns `verified:True` even when the materialized
worktree byte differs from the receipt's `post_prepare_bytes`. It literally "never
compared with the current cache … no cache work is performed here"
(`workspace_overlay.py:854-865`). Byte-integrity is enforced only at
`restore_worktree`, which compares current bytes with the receipt's exact
`post_prepare_bytes` (`workspace_overlay.py:789-795`) and reports
`outcome:"BLOCKED"` with reason `"later edit detected …"`, preserving the edited
file. Severity `note`: both behaviors are correct and safe — verify is a cheap
prelaunch gate and byte enforcement happens at the destructive-action boundary
(restore) where it is most needed; only the plan text overpromised the verify
seam.

**Code under test:** `orchestrator_harness/workspace_overlay.py:854-901`
(`verify_overlay_receipt`) and `:789-795` (`restore_worktree` post-prepare-byte
comparison).

**Test:** `test_i4_byte_corruption_blocks_restore_not_verify` pins both actual
behaviors (verify → `verified:True`; restore → `BLOCKED`/"later edit detected")
and stays green.

### F2B-L4-1 — bounded single-use is broker-enforced, not a per-permit counter

**What was tested:** the shape of `CapabilityPermit`, then a full `execute` PASS
followed by (a) an exact retry (same request + approval, deep-copied) and (b) a
reuse of the same request identity under changed `arguments`; and separately (c) a
durable-state retry across two brokers sharing a `state_root`, replaying a consumed
approval whose `signature` changed.

**Fabricated input:** a `FakeCapabilityAdapter({"synthetic": ("read",)})`, an
in-memory `_Claims`, and `_request()` / `_approval_for(...)` bindings; the durable
case uses two `_broker(..., state_root=<temp>/state)` instances.

**Expected (plan L4):** a single/bounded-use permit carrying a self-contained use
counter that decrements per use.

**Observed:** `CapabilityPermit` is an immutable dataclass with **no** `use_count`
or `uses_remaining` field. Bounded use is enforced by the broker: an exact retry
reuses the cached terminal result byte-for-byte (`first.to_record() ==
second.to_record()`, `dispatch_calls` stays 1); reusing the request identity under
changed semantics is refused with `REPLAY_MISMATCH`; and a durable consumed approval
whose provenance changed is refused with `APPROVAL_REPLAY` (the `_used_approvals` /
approval-state seam). Severity `note`: the invariant the plan wanted (a grant cannot
be silently re-spent) holds — it is realized as terminal-result caching + replay
refusal rather than a mutable counter, which is safer (no mutable per-permit state to
corrupt).

**Code under test:** `orchestrator_harness/capability_broker.py` —
`CapabilityPermit` dataclass; the terminal-result cache and `_used_approvals`
replay-refusal paths in `CapabilityBroker.execute`.

**Test:** `test_L4_bounded_single_use_grant_actual_broker_mechanism` pins the
absence of a counter and both refusal paths (`REPLAY_MISMATCH`, `APPROVAL_REPLAY`)
and stays green.

### F2B-L7-1 — `CapabilityAdapterUnavailable` from `observe` is swallowed into a DENIED result

**What was tested:** three fail-closed paths through `execute`: (a) an adapter that
does not advertise the requested action; (b) an adapter whose `observe` raises
`CapabilityAdapterUnavailable`; (c) an approval that fails snapshot binding.

**Fabricated input:** `FakeCapabilityAdapter` variants (one subclassed to raise
`CapabilityAdapterUnavailable` from `observe`, one with a mismatched
`snapshot_sha256`), each driven through `_broker(...).execute(...)`.

**Expected (plan L7):** pointing the broker at a missing/unavailable adapter raises
`CapabilityAdapterUnavailable` to the caller.

**Observed:** the broker **catches** the adapter's `CapabilityAdapterUnavailable`
from `observe` and returns `outcome:"DENIED"` with
`record["denial"]["reason_code"] == "SNAPSHOT_UNAVAILABLE"`
(`capability_broker.py:1400-1406`); the typed exception does not propagate out of
`execute`. In every fail-closed path no permit is constructed (`adapter.permits ==
[]`) and `dispatch_calls` stays 0. The unadvertised-action path denies with
`CAPABILITY_UNAVAILABLE`; the binding-failure path denies with `APPROVAL_MISMATCH`.
`CapabilityAdapterUnavailable` remains a real `CapabilityAdapterError` /
`CapabilityError` subclass (the part of the plan that does hold). Severity `note`:
fail-closed-as-DENIED is safer than propagating an exception the caller might not
handle.

**Code under test:** `orchestrator_harness/capability_broker.py:1400-1406`
(`observe` `CapabilityAdapterUnavailable` → DENIED `SNAPSHOT_UNAVAILABLE`) and the
`CAPABILITY_UNAVAILABLE` / `APPROVAL_MISMATCH` denial paths.

**Test:** `test_L7_fail_closed_paths_and_no_permit_leak` pins all three DENIED
outcomes with zero dispatch and no permit leak, and stays green.

### F2E-A34-1 — `release_assets.py` is read-only manifest accessors only, no packaging/digest engine

**What was tested:** the full public surface of `orchestrator_harness.release_assets`
against plan item A34 ("release-manifest asset packaging"): the three accessors
`release_manifest`, `manifest_asset_paths`, `read_package_asset`, plus a negative
probe for any packaging/digest machinery.

**Fabricated input:** direct calls to the accessors over the module's shipped
manifest; `dir(release_assets)` / `__all__` introspection; malformed-schema and
path-traversal probes through `read_package_asset`.

**Expected (plan A34):** a release surface that *packages* assets — builds an
archive and/or emits a content digest (sha/hash) over the declared asset set.

**Observed:** the module exposes exactly three **read-only** accessors
(`__all__ == ["manifest_asset_paths", "read_package_asset", "release_manifest"]`);
there is no `package`/`build_package` entry point and no digest/hash/archive name
anywhere on the module surface or in the shipped manifest keys. The accessors are
well-behaved and fail-closed (schema guard rejects malformed manifests; traversal
and bogus-relative/directory paths are refused), but the packaging/digest half of
A34 is simply absent. Severity `note`: the shipped behavior is safe and correct for
what it does; it is narrower than the intended deliverable. Reclassified
2026-08-20: this is a **DESIGN-REC** (design recommendation for shared code), **not a
GAP** — it is a shared-code shortfall relative to an old plan doc, behaves identically
for Codex and Claude, and is not a Codex-vs-Claude provider divergence. The only genuine
provider gap in the inventory is U15.

**Code under test:** `orchestrator_harness/release_assets.py` (`release_manifest`,
`manifest_asset_paths`, `read_package_asset`; `__all__`).

**Test:** `test_f2e_a34_1_no_packaging_or_digest_surface` pins the absence of the
packaging/digest surface; the nine sibling tests pin the accessors' fail-closed
read-only contract. All 10 green.

### F2G-A39-1 — no ordered `STOP_ASSIGNING → … → RESOLVED` recovery ledger

**What was tested:** `orchestrator_harness.watcher_integration.watcher_recovery_projection`
against plan item A39 / T3, which describes a "watcher alert / recovery **ledger**
(`STOP_ASSIGNING → … → RESOLVED`)" with "each transition admitted only in order".

**Fabricated input:** recovery-record lists driven through
`watcher_recovery_projection`, including out-of-order and lone records
(`{alert_id:"A9", state:"resolved"}` with no prior `open`), a `STOP_ASSIGNING`
state, and invalid/blank/non-Mapping records.

**Expected (plan A39/T3):** an ordered state-machine ledger admitting each
transition only in `STOP_ASSIGNING → … → RESOLVED` order.

**Observed:** no such ledger exists. The module docstring states recovery is "a small
open/acknowledged/resolved projection only" and watcher alerts "do not become harness
queue events." `watcher_recovery_projection` is a **stateless filter+label pass with
no ordering guard**: `schema == "orchestrator-watcher-recovery/v1"`; records are
labeled `open`/`acknowledged`/`resolved` in input order; `actionable` = only `open`
ids; a lone `resolved` record (never previously `open`) is admitted unchanged;
`STOP_ASSIGNING` is not in `WATCHER_RECOVERY_STATES` so those records are silently
dropped. Output is exactly `{schema, states, actionable}` — no queue events. Severity
`note`: the shipped projection is safe and internally consistent. Reclassified
2026-08-20: **DESIGN-REC**, **not a GAP** — a shared-code recommendation, identical for
both providers, not a Codex-vs-Claude provider divergence (the only provider gap is U15).
**STALE FINDING:** this tested only the stateless `watcher_recovery_projection`; an
ordered `STOP_ASSIGNING → … → RESOLVED` ledger with an out-of-order guard **does** exist
in `harness_watcher_implementation/state.py` (`ORDER`, `transition()` raising
`ValueError("recovery transition out of order")`, `recovery_history`) — re-test pending.
(A31 condition merging in the same module is a genuine PASS.)

**Code under test:** `orchestrator_harness/watcher_integration.py`
(`watcher_recovery_projection`, `WATCHER_RECOVERY_STATES`).

**Test:** `test_lone_resolved_record_accepted_no_order_guard` and
`test_projection_schema_states_and_order` pin the absence of ordered admission; all
19 tests green.

---

## Phase 3 — live-lane observations (not GAPs; test-methodology / behavioral notes)

### P3-OBS-1 — the real `claude` binary emits a client-side `session_id` *before* any network call

**Context:** while building the 3.A/G21 authentic launch-failure probe, an initial
attempt pointed the real `claude` binary at a dead endpoint (`127.0.0.1:9`) expecting
`LAUNCH_FAILED`. It did **not** fail-to-launch: `claude` prints a client-side
`system/init` line carrying a locally-generated `session_id` *before* it makes any
network request, so the harness records a `provider_session_id` and classifies the
lane as `RUNNING_PROVIDER` (then the binary hangs on retries against the dead host).

**Consequence for testing:** `LAUNCH_FAILED` (lane_controller.py ~3117) requires
`action=="start" and not state.get("provider_session_id")`. A dead-endpoint claude
therefore cannot be used to authentically trigger the launch-failure family — the
session id is already set. The authentic trigger is a provider process that exits
**before** emitting any session line. The 3.A probe uses an immediate-exit stub
(`[python, -c, "import sys; sys.exit(3)"]`) as the provider command; the harness then
emits `PROVIDER_STARTED` → `CONTROLLER_FAILED` with `provider_session_id: null`,
which is the genuine G21 wiring (see PHASE3-LOG 3.A and `evidence/3.A/`).

**Not a GAP:** this is authentic `claude` behavior and correct harness classification;
it only changes *how* a launch failure must be provoked. Recorded so future live-lane
agents don't mistake a hung dead-endpoint run for a launch failure, and don't return
on the transient initial-default `LAUNCH_FAILED` status (poll `LANE_EVENTS.jsonl` for
a real failure *event* instead, keyed on `"event"` not `"type"`).

---

### P3-INT-1 — intended behavior: the orchestrator coaches the subagent to the desired outcome via provider-session continuation

**Intended behavior (user, 2026-08-20):** when a live subagent lane does not reach the
desired outcome on its first turn (e.g. a weak backend model produces `MISSING` result
or a malformed/incomplete artifact), the orchestrator is expected to **use the model's
prompt response to determine where it went wrong and inject a corrective prompt — as the
orchestrator — to let the same session keep going** toward the desired outcome. This is
authentic orchestrator relay/coaching, not a workaround, and it is the intended path to
drive a lane into runtime states a single cold turn does not reach.

**Mechanism (two distinct "resume" notions — only one has a RESULT precondition):**
- *Provider-session continuation* — `claude --resume <session_id> "<corrective prompt>"`
  continues the same Claude CLI transcript/conversation. It needs **no** committed
  RESULT.json; it is the actual "tell it what it got wrong and let it keep going" lever.
- *Harness task-resume* — `resume.py` / `_canonical_prior_task_preflight` re-admits a
  whole lane as a continuation under strict identity checks and **does** require a prior
  valid committed result. This is a different concern and is **not** what the coaching
  loop uses.

**Authentic target for the coached outcome (F15/G32 terminal acceptance):** the worker
must write `<workspace>/RESULT.json` with `schema="orchestrator-task-result/v1"` whose
`lane_id` + `worker_invocation_id` match the owning controller status
(discovery.py ~826/873); `_validate_task_result_cached` then yields the acceptance state
(`ACCEPTED`). Reconcile over that real committed result fires the terminal-acceptance
path for real. The disposable-claude fixture's own success check (committed HELLO.txt +
`PROVIDER_EXITED`/`COMPLETED`) is a *separate, weaker* gate than this RESULT.json contract.

**Consequence for the model-dependent 3.A items:** F15, G8–G13, G15, G16, G32-live are
therefore **not** permanently "not reproducible on this backend" — they are reachable by
coaching deepseek-v4-flash across multiple corrective turns until it emits the valid
committed RESULT.json (and the multi-turn run exercises the steady-state/relay/lifecycle/
ack events as byproducts). The single exception is a realistic **stall** (a genuinely
long-running lane state the weak/fast model never sits in): per user decision 2026-08-20
a **synthetic/fake stall state** is acceptable for that one item, since it cannot be
provoked authentically without a slower long-running turn. Coaching turns spend live
Ollama quota — STOP-on-429 still applies.

---

### P3-OBS-2 — cross-provider event-name divergence in one shared LANE_EVENTS.jsonl

Observed live in 3.C: a claude-code lane and a codex lane run concurrently against the
same shared `LANE_EVENTS.jsonl`. The **claude** worker-invocation path emits
`PROVIDER_STARTED`/`PROVIDER_EXITED`; the **codex** coding-invocation path emits the
**legacy** `CODEX_STARTED`/`CODEX_EXITED` — both into the same log, interleaved. The
reconciler (`scan`) is provider-neutral and groups both lanes correctly (`claude-code`
EXITED + `codex` EXITED) despite the divergent terminal event names. Impact: cosmetic /
naming only; downstream consumers keying on the string `PROVIDER_EXITED` would miss a
codex lane's terminal row. Evidence: `evidence/3.C/LANE_EVENTS.jsonl`, `xprovider-report.json`.

### P3-OBS-3 — controller status embeds a turn-1 result snapshot that goes stale after coaching

The lane controller writes a `result_validation` snapshot into its status file at the
turn-1 exit time. When the orchestrator subsequently coaches the lane via post-exit
`claude --resume` (P3-INT-1) and the worker rewrites `RESULT.json`, that embedded snapshot
is **not** refreshed and is stale. The authoritative view is a live `scan`, which re-reads
`RESULT.json` fresh and reflects the coached state (`RESULT_ACCEPTANCE_PENDING` →, after
review+acceptance, `ACCEPTED`). Lesson: never trust the status-embedded snapshot after
coaching; reconcile. Evidence: `evidence/3.A/coach/scan-before/after-acceptance.json`.

### P3-OBS-4 — S4 removed the live stall producers; G10 has no authentic route

`manager_review_interval_seconds` / `lane_no_progress_seconds` are listed in
`config.py` (~168-184) as removed/legacy keys with "no S4 runtime effect". No live lane
emits `MANAGER_REVIEW_DUE` / `LANE_NO_PROGRESS` / `LANE_STAGE_REPEAT` — only the
**classifier** wiring (disposition table + `_priority` + `select_actionable`) survives.
An emergent stall is therefore unreachable on this harness; per user acceptance G10 is
proven only synthetically (fabricated conditions driven through the surviving classifier),
explicitly labeled fake. Evidence: `evidence/3.A/coach/g10-stall-classifier.json`.

### P3-OBS-5 — MCP wiring and live round-trip both authentic (3.D)

The harness `provider.mcp_config` channel threads a well-formed `--mcp-config` JSON
(`mcpServers`) into the claude argv (verified by rebuilding the `ProviderLaunchSpec` →
`build_argv`), and a live claude+Ollama lane completed a full MCP round-trip against a
local hand-rolled stdio server: the model issued exactly one tool_use,
`mcp__marker__record_marker`, with no Bash/Write fallback, and the server wrote the
marker file. Session-local isolation via a fresh `CLAUDE_CONFIG_DIR` (no other MCP
servers) makes `--mcp-config` alone the sole server source. Evidence: `evidence/3.D/`.

### P3-OBS-6 — G21 launch-failure family fully observed live; two probe subtleties

All three G21 launch-failure event types now drive live through the real controller
(`evidence/3.A/g21-siblings/`), not only in-process:

- **LAUNCH_FAILED requires an observed-then-cleanly-reaped child.** A too-fast stub
  (`sys.exit(3)` immediately) exits before the supervisor can inventory it as a live
  member and prove a clean reap, so `release_safe` is false and the run diverts to
  `CONTROLLER_FAILED` with `[Errno 22] Invalid argument`. A stub that sleeps ~2.5s
  (inventoried as a live child), prints no stream-json session line, then exits 0
  cleanly passes the reap/`release_safe` gate and reaches `lane_controller.py:3117` →
  `LAUNCH_FAILED` (session null). The distinction is the reap-proof boundary, not the
  exit code.
- **CONTROLLER_INTERRUPTED needs an argv-scoped interrupt injection.** Patching
  `subprocess.Popen` blanket to raise `KeyboardInterrupt` fails: `git_safety.inspect_repository`
  runs `subprocess.run(["git", ...])` (same module) at `run()` line ~1842, BEFORE the
  main try-block, so the interrupt escapes the handler under test. Gating the patch to
  raise only when the provider argv is spawned (identified by the `stream-json` flag the
  adapter always emits) and delegating the real Popen for git fires the interrupt inside
  `run()`'s try at the spawn boundary; the handler at :3247 sees `process is None`
  (spawn never assigned) → clean else at :3281 → `CONTROLLER_INTERRUPTED`, rc 130.
