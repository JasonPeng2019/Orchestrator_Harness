# Task: Phase 2, Area 2.B — Capability broker pipeline (detection-only)

You are a **test-authoring subagent** for the `orchestrator_harness` compatibility-testing plan.
You write and run **pure-Python `unittest` tests** that drive the real
`orchestrator_harness.capability_broker` seams over fabricated in-memory requests / approvals /
snapshots / adapters. You do NOT launch any `claude`/provider subprocess, you do NOT modify any
harness source module, and you do NOT "fix to green" — a test that reveals a real gap is a valid,
recorded outcome. Two items (L4, L7) have KNOWN plan-vs-reality divergences (below): pin ACTUAL
behavior in a green test and flag the FINDING in your report.

## Where you are

- Working dir (disposable clone, carries phase-0 fixes):
  `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test`
- Run your new tests:
  ```bash
  cd "C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test"
  PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_compat_capability_broker -v
  ```
- **Model fixture — read FIRST and copy its idioms EXACTLY:**
  `orchestrator_harness/tests/test_s5_capability_broker.py`. It gives you ready-made helpers you
  should replicate (do not import from it — copy the small ones you need into your module):
  - `OWNER` — a fixed controller identity dict `{"pid","created_utc","creation_identity"}`.
  - `_request(...)` — builds a valid capability-request record (schema
    `orchestrator-capability-request/v1`, `route="capability"`).
  - `_approval(request, snapshot, ...)` — builds a valid approval record bound to a parsed
    request + snapshot (fills `request_sha256`, `snapshot_sha256`, `decision="approve"`, fake
    `public_key`/`signature`).
  - `_Verifier` — a trivial approval-signature verifier whose `.verify(payload, sig, key)` returns
    truthy for any non-empty inputs.
  - `_Claims` — an in-memory resource-claims double implementing
    `acquire_all/arm_boundary/retain_boundary/release_all/held`.
  - `_broker(adapter, claims, ...)` — wires a `CapabilityBroker` with `_Verifier`, a
    permissive `policy_verifier`, `identity_provider=lambda: dict(OWNER)`, and
    `claims_factory=lambda lane, request_id: claims`.
  - The `self._approval_for(request_value, adapter)` helper on the test class.
  The **canonical happy path** is `test_S5_F1_generic_success_binds_exact_facts_and_releases_after_cleanup`
  — read it to see how a PASS run is asserted (`outcome=="PASS"`, `state=="TERMINAL"`,
  `dispatch_calls==1`, `cleanup_calls==1`, `claims_released` true, `cleanup`/`cleanup_validation`
  present).

## Code under test — `orchestrator_harness/capability_broker.py` (grep bodies before asserting)

Schemas: `REQUEST_SCHEMA`, `SNAPSHOT_SCHEMA`, `APPROVAL_SCHEMA`, `PERMIT_SCHEMA`, `RESULT_SCHEMA`,
`CLEANUP_SCHEMA`, `STATE_SCHEMA` (all `.../vN`). Errors: `CapabilityError(ValueError)` →
`CapabilityDenied` (typed, carries `reason_code`/`stage`/`details`, `to_record()`),
`CapabilityAdapterError` → `CapabilityAdapterUnavailable`.

Dataclasses (all `@dataclass(frozen=True)`; nested mappings frozen via `MappingProxyType`):
`CapabilityRequest` (`from_record(value, *, now_monotonic)` — closed 10-key shape; rejects mixed
route, non-identifier fields, empty/duplicate resources, already-expired via `CapabilityDenied`),
`CapabilitySnapshot` (`from_record`), `CapabilityApproval` (`from_record` — rejects non-`approve`
decision with reason `APPROVAL_DENIED`, bad digests, inverted window), `CapabilityPermit`,
`AdapterResult` (validates `succeeded` is bool + public-json raw/interpreted + adapter identity in
`__post_init__`), `CleanupEvidence`, `CapabilityResult` (`.outcome`, `.state`, `.record`).

`FakeCapabilityAdapter(capabilities, *, snapshot_identity=None, adapter_identity=None,
result_factory=None, fail_dispatch=False, cleanup_proved=True)` — the L10 reference adapter:
counts `support_calls/observe_calls/dispatch_calls/cleanup_calls`, records `permits`, and
`supports` returns `request.action in capabilities.get(request.capability, ())`.

`CapabilityBroker(adapter, *, approval_verifier, policy_verifier, identity_provider=None,
claims_factory=None, claims_root=None, state_root=None, clock=time.monotonic, ...)`. Entry point
`execute(request_value, approval_value)` (alias `run`); `execute_or_raise` raises `CapabilityDenied`
on a DENIED outcome. Terminal outcomes on `CapabilityResult.outcome`: `"PASS"`, `"FAIL"`,
`"UNCERTAIN"`, `"DENIED"`. A DENIED record carries `record["denial"]["reason_code"]`. A permit is
only ever constructed internally on the admitted path; a denied/failed admission NEVER constructs
or dispatches a permit (`adapter.dispatch_calls==0`, `len(adapter.permits)==0`).

## What to build

Create ONE new test module: `orchestrator_harness/tests/test_compat_capability_broker.py`. Aim for
one focused test per feature ID (subtests are fine). **Do not re-derive the whole S5 suite** — write
targeted checks for L1–L7 + L10 + A25:

1. **L1 — `CapabilityRequest` construction.** A valid `_request()` parses via
   `CapabilityRequest.from_record(value, now_monotonic=0.0)` and round-trips `to_record()`. Malformed
   inputs each raise `CapabilityDenied` (assert the `reason_code`): a non-closed key set
   (`REQUEST_NOT_CLOSED`), a wrong `route` (`MIXED_ROUTE`), an empty/duplicate `resources`
   (`INVALID_RESOURCES`/`DUPLICATE_RESOURCE`), an already-expired `expires_monotonic`
   (`EXPIRED_REQUEST`), a non-identifier `request_id`/`capability` (`INVALID_IDENTITY`).
2. **L2 — `CapabilitySnapshot` point-in-time capture + immutability.** Build a snapshot (copy the
   fake adapter's `observe(...)` output, or `CapabilitySnapshot.from_record`). Assert the frozen
   dataclass rejects attribute assignment (`with self.assertRaises((dataclasses.FrozenInstanceError,
   AttributeError, TypeError)): snapshot.snapshot_id = "x"`) AND that a nested mapping is a read-only
   `MappingProxyType` (mutating `snapshot.identity["k"] = 1` raises `TypeError`). Confirm
   `from_record` rejects a non-closed shape / wrong schema with `CapabilityError`.
3. **L3 — mediated approval gate.** An `approve` approval bound to the exact request+snapshot lets
   the broker reach a PASS (permit issued → dispatch → cleanup). A **deny** path: an approval record
   with `decision != "approve"` is refused by `CapabilityApproval.from_record` with reason
   `APPROVAL_DENIED`; and a broker run given such an approval returns `DENIED` with NO permit issued
   (`adapter.dispatch_calls==0`, `adapter.permits==[]`).
4. **L4 — bounded/single-use grant.**
   > **PLAN-VS-REALITY DIVERGENCE — flag as FINDING F2B-L4-1 (note).** The plan says "the permit is
   > single/bounded-use — a second use beyond bound is refused." Reality: `CapabilityPermit` is an
   > immutable in-memory value with no self-contained use counter; bounded-use is enforced by the
   > **broker**, via (a) idempotent terminal-result reuse — an exact retry of the same
   > request+approval returns the cached terminal WITHOUT re-dispatching (`dispatch_calls` stays 1),
   > and (b) `self._used_approvals` — reusing one approval under changed semantics is refused. Pin
   > the ACTUAL mechanism: run once (PASS), run the exact same request+approval again → identical
   > `to_record()` and `dispatch_calls==1`; then run a **changed** request (mutated `arguments`) →
   > `DENIED` with reason `REPLAY_MISMATCH`. Do not assert a per-permit counter.
5. **L5 — `AdapterResult`/`CleanupEvidence`/`CapabilityResult` outcome+cleanup pipeline.** After a
   PASS run assert the terminal record is well-formed: `schema==RESULT_SCHEMA`, has `cleanup` (a
   `CLEANUP_SCHEMA` record with `proved` true), `cleanup_validation.valid` true, `raw_result_sha256`
   present and equal to `hashlib.sha256(canonical_json_bytes(raw_result)).hexdigest()`,
   `permit_sha256` echoed. Also directly assert the value objects fail closed on private material:
   `AdapterResult(...)` and `CleanupEvidence(...)` raise `CapabilityError` when a field carries a
   banned authority-alias key (e.g. `endpoint`, `token`) — mirror the S5_R1_006 style but keep it to
   2–3 aliases.
6. **L6 / A25 — full orchestration end-to-end.** Drive request→approval→permit→adapter→cleanup via
   `FakeCapabilityAdapter` and `_broker`: assert `outcome=="PASS"`, `state=="TERMINAL"`, cleanup
   evidence produced (`cleanup_calls==1`, `record["cleanup"]["proved"] is True`), claims released,
   and the ordering `["claim","arm","cleanup"]` then `"release"` (use the `_OrderedAdapter`/events
   idiom from S5_F1). Assert NO endpoint/authority material leaks into `str(result.to_record())`.
7. **L7 — fail-closed paths + no permit leak.**
   > **PLAN-VS-REALITY DIVERGENCE — flag as FINDING F2B-L7-1 (note).** The plan says "point at a
   > missing adapter → `CapabilityAdapterUnavailable`." Reality: the broker catches an adapter's
   > `CapabilityAdapterUnavailable` (raised from `observe`) and returns a **DENIED result** with
   > reason `SNAPSHOT_UNAVAILABLE` — it does NOT propagate the exception to the caller. Pin the
   > ACTUAL behavior. Cases (each `outcome=="DENIED"`, `dispatch_calls==0`, `permits==[]`): (a)
   > adapter whose `supports()` returns False for the requested action → `CAPABILITY_UNAVAILABLE`;
   > (b) adapter whose `observe()` raises `CapabilityAdapterUnavailable` → `SNAPSHOT_UNAVAILABLE`; (c)
   > a plainly denied request (e.g. an approval that fails binding) → `DENIED`. Confirm
   > `CapabilityAdapterUnavailable` is a real subclass of `CapabilityAdapterError`/`CapabilityError`.
8. **L10 — `FakeCapabilityAdapter` reference adapter honors its contract.** Directly assert:
   `supports(request)` is True only when `request.action` is advertised and False otherwise;
   `observe(request)` returns a `CapabilitySnapshot` whose `request_id/lane_id/capability/action/
   resources` echo the request and whose `capabilities` advertise the configured actions;
   `fail_dispatch=True` makes a broker run terminate `FAIL` (dispatch raised, cleanup still ran);
   `cleanup_proved=False` makes a run `UNCERTAIN` with `claims_released` False and the claim retained.

Never edit source. If any OTHER behavior differs from the plan (a denied path that STILL dispatches
or leaks a permit, a frozen dataclass that is actually mutable, private material surviving into a
result record, a bounded-use grant that re-dispatches on exact retry — any fail-open), that is
HIGHER severity — flag it clearly and prominently.

## Pass criterion

- New module green under the run command above.
- Re-run the model suite to prove you did not perturb it:
  `PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_s5_capability_broker -v`

## Evidence to leave behind

Into `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/plans/compatibility-testing/evidence/2.B/`:
- `test-run.log` — full `-v` output of your new module.
- `s5-regression.log` — `-v` output of `test_s5_capability_broker`.

## Final report (return as your last message)

A markdown table: one row per feature ID (L1, L2, L3, L4, L5, L6/A25, L7, L10), each `PASS` /
`FINDING` (one-line what-differed) / `BLOCKED`/`SKIPPED` (why) — L4 and L7 are EXPECTED to be
`FINDING` rows. Then the exact commands run, the test count, and the pass/fail tally. Do not modify
any file outside your new test module and the evidence dir (if you believe a finding should be
recorded in `evidence/FINDINGS.md`, describe it in your report — the coordinator files it).
