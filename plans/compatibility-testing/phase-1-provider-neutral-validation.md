# Phase 1 — Provider‑neutral validation & logic (testable now, no live lane)

Every feature here is **pure logic over fabricated inputs** — invocation JSON, task/result
records, synthetic process snapshots, synthetic event records. None needs a live `claude`
subprocess, so Phase 1 can start immediately, in parallel with Phase 2, before Phase 0's
fixes land. These are the plain‑**TB‑NS** validation rules plus the pure‑validation half of
**TB‑SC** (task/result/git‑safety logic that was short‑circuited only because no lane was
producing results — but the validators accept fabricated results directly).

**Method for all steps:** add/extend a unit module under
`orchestrator_harness/tests/` (`test_compat_<area>.py`), build the minimal fixture, assert
the concrete expectation. Model the fixtures on the existing suite
(`test_s2_contract.py`, `test_git_results.py`, `test_reconcile.py`,
`test_manager_notifications_adversarial.py`, `support.py`). Pass = new assertions green +
existing suite still green.

---

## 1.A — Invocation schema & validation rules (`invocation.py`) — C2–C24

Build one valid canonical `orchestrator-worker-invocation/v1` baseline (from
`test_s2_contract.py`), then mutate one field per step and assert the exact rejection.

1. **C2** `action` ∈ {`start`,`resume`}: set `action:"foo"` → `InvocationValidationError`. Valid `start`/`resume` accepted.
2. **C3** resume needs non‑empty session/thread id: `action:"resume"` with empty/missing id → error.
3. **C4** `start` cannot carry a `resume` block: add `resume:{...}` to a `start` → error.
4. **C5** `provider.notification` must be boolean (`invocation.py:416`): set `"notification":"yes"` → error; `true`/`false` accepted.
5. **C6** `profile.role` must match invocation role: mismatch role → error.
6. **C7** `profile.provider` must match `provider.id`: mismatch → error.
7. **C8** `profile.model` must match `provider.model`: mismatch → error.
8. **C9** `prompt_bundle` schema/version validation: wrong schema string / version → error (dovetails Q13/B15).
9. **C10** `resume_identity` must be an object: pass a string → error.
10. **C11** unknown invocation‑schema string: `schema:"bogus/v1"` → `load_invocation` rejects (`invocation.py:428`).
11. **C16** ambiguous coding‑alias rejection (`_reject_ambiguous_coding_aliases`): supply conflicting aliases → error.
12. **C18** canonical output‑path safety/uniqueness (`_validate_canonical_output_paths`): duplicate or traversal output path → error; unique safe paths accepted.
13. **C19** SHA‑256 hex‑digest format: 63‑char / non‑hex digest field → error; valid 64‑hex accepted.
14. **C20** string‑list no‑duplicates (`_string_list`): `allowed_tools:["Read","Read"]` → error.
15. **C21** isolated coding child‑environment (`isolated_coding_child_environment`): assert the returned env strips inherited secrets and sets the declared vars only. *(PA‑adjacent; include as a construction assertion.)*
16. **C22** prior canonical acceptance read/persist (`_read_canonical_prior_status`/`_persist_canonical_acceptance`): persist a status, read it back byte‑stable.
17. **C23** canonical resume‑admission path & amendment‑claims (`_canonical_resume_admission_path`/`_canonical_resume_claims_accepted`): valid claims accepted, tampered claims rejected.
18. **C24** provider‑operation classification & handoff‑identity (`_classify_provider_operations`/`_provider_handoff_identity`): assert start→launch / resume→resume classification and a stable handoff identity.
> C13/C14 (repo path + worktree_root==run_root) and C1 (closed‑shape) are already
> TESTED‑PASSED; re‑assert them here as guards only.

---

## 1.B — CLI subcommands (`cli.py`, `__main__.py`) — B1–B8, B15, B16

Drive `python -m orchestrator_harness ... <subcommand>` against a fabricated suite dir.

19. **B1** `scan` one‑shot snapshot compute + print: run against a fixture run‑root; assert snapshot printed and a snapshot/event written.
20. **B2** `scan --no-write` diagnostic‑only: assert **no** snapshot/event mutation on disk (diff run‑root before/after).
21. **B3** `watch --once` single reconcile pass: assert exactly one pass, then exit.
22. **B4** `watch --until-event` blocks until a new event: fabricate an event mid‑wait (touch a record) → returns promptly with that event.
23. **B7** `watch --no-write`: assert reconcile runs but persists nothing.
24. **B8** `handoff-preflight` subcommand: run with a valid preflight bundle → OK exit; with missing evidence → non‑zero + reason (ties K10/A28).
25. **B15** `view` / `source allocate` immutable source view: allocate a read‑only view of a fixture repo at a revision; assert the view exists and is read‑only (ties P1/P2).
26. **B16** `lane retire` archive‑first retirement: retire a fabricated terminal lane; assert archive written **before** worktree close (ties P6).
> B5/B6/B17/B18/B19 already TESTED‑PASSED; B9–B14 are CX‑GAP → Phase 4.

---

## 1.C — Task & result lifecycle validation (`task.py`) — D3–D20 (TB‑SC, now unblocked via fixtures)

Fabricate a valid task card (D1/D2 already pass), then a task result / completion review /
acceptance record, mutate one field per step, assert the validator's behavior. No live
lane needed — the validators take records directly.

27. **D3** task‑result schema validation: malformed root shape → error; valid accepted.
28. **D4** result↔card identity cross‑match: result referencing a different card id → error.
29. **D5** `.outcome` enum ∈ {PASS,FAIL,BLOCKED}: `"outcome":"DONE"` → error.
30. **D6** `.checks[]` shape + per‑check outcome enum {PASS,FAIL,SKIP,NOT_RUN}: bad check outcome → error.
31. **D7** `.acceptance_state` enum {PENDING,ACCEPTED,REJECTED}: bad value → error.
32. **D8** completion‑review schema validation: malformed → error.
33. **D9** completion‑review result‑identity cross‑match: mismatched result id → error.
34. **D10** completion‑review owner‑must‑own‑task‑card: foreign owner → error.
35. **D11** completion‑review `.verdict` enum {PASS,FAIL,BLOCKED}: bad verdict → error.
36. **D12** orchestrator‑acceptance schema validation: malformed → error.
37. **D13** orchestrator‑acceptance identity cross‑match: mismatch → error.
38. **D14** orchestrator‑acceptance `.verdict` enum {ACCEPTED,REJECTED}: bad verdict → error.
39. **D15** `advance_task` state machine (`ACCEPTANCE_PENDING`→`ACCEPTED`/`REJECTED`): drive both transitions; assert the resulting state.
40. **D16** advancement result‑must‑match‑supplied‑card: mismatched card → error.
41. **D17** advancement review/acceptance‑identity cross‑match: mismatch → error.
42. **D18** advancement acceptance‑commit‑must‑match‑result: mismatched commit → error.
43. **D20** schema‑string constant surface: assert the 4 schema constants equal their documented `orchestrator-*/v1` strings.
> D19 already TESTED‑PASSED (canonical_record).

---

## 1.D — Git safety & result‑merge validation (`git_safety.py`) — E4–E7, E14–E20 (E14–E19 are TB‑SC)

Use a real disposable `git init` worktree (as `test_git_results.py` does) + fabricated
result records.

44. **E4** repository‑identity‑must‑be‑reported: omit reported identity → error.
45. **E5** detached‑HEAD rejection: put the worktree on a detached HEAD → coding‑worktree validation error.
46. **E6** commit‑identity format validation: malformed commit id → error.
47. **E7** duplicate active worktree/branch (`active_declaration_conflicts`) (also A12/F16): two declarations, same branch/worktree → conflict reported.
48. **E14** coding‑result root‑shape + `orchestrator-lane-result/v1` schema: malformed → error.
49. **E15** lane_id / branch / outcome‑enum cross‑match vs. current lane: mismatched lane_id → error.
50. **E16** per‑check shape (name‑or‑command required, outcome enum): check missing both name and command → error.
51. **E17** commit‑must‑equal‑branch‑tip (dirty/stale‑tree rejection): make the tree dirty / point at a non‑tip commit → error.
52. **E18** `CODING_RESULT_INVALID` durable evidence + clearing (also A14, PA): invalid result writes evidence; a corrected result clears it. Assert both.
53. **E19** operational‑state gate (accept only in `RUNNING_CODEX`/`RUNNING_PROVIDER`): offer a result while state is e.g. `EXITED` → rejected; while `RUNNING_PROVIDER` → considered.
54. **E20** too‑many‑JSON‑candidates ambiguity: drop 2 candidate result JSONs under the result workspace → ambiguity rejection.

---

## 1.E — Reconcile state classification (`reconcile.py`, `discovery.py`) — F3, F4, F7–F14, F16, F19, F22, F24

Fabricate `ProcessSnapshot`/status/record inputs (as `test_reconcile.py` does) and assert
the derived classification. No live process needed.

55. **F3** `WAITING_RELAY` (blocked on manager relay): fixture with an unbound relay + pending request → `WAITING_RELAY`.
56. **F4** helper tri‑state `HELPER_RUNNING`/`_EXITED`/`_STATE_UNKNOWN`: three fixtures → three classifications.
57. **F7** `PROCESS_STATE_UNKNOWN` fail‑closed on incomplete evidence: omit process evidence → `PROCESS_STATE_UNKNOWN` (never a false "running").
58. **F8** `EXITED`/`UNKNOWN` terminal states: dead‑PID / no‑evidence fixtures → each.
59. **F10** relay‑binding `BOUND`/`BOUND_EXPIRED`/`UNBOUND`/`ABSENT`: four relay fixtures → four states.
60. **F11** request‑lifetime `LIVE`/`ABSENT`/`UNKNOWN`: three request fixtures.
61. **F12** expiry‑bucket `WARNING`/`CRITICAL`/`EXPIRED`/`UNKNOWN`: vary timestamps across the bounds → each bucket.
62. **F14** `RELAY_READY`/`RELAY_UNBOUND`/`REQUEST_AMBIGUOUS`: ready / unbound / two‑request fixtures.
63. **F16** duplicate coding worktree/branch at reconcile layer (dup of E7): assert `DUPLICATE_CODING_WORKTREE`/`_BRANCH`.
64. **F19** record‑kind classification from declared manifest (`_record_kind`): each declared kind → correct classification.
65. **F22** UTC‑timestamp format validation (`_is_utc_timestamp`): non‑UTC / malformed timestamp on a discovered record → rejected.
66. **F24** memoized coding/task‑result validation cache: validate twice; assert cached path taken and that a signature change invalidates it.
> F1/F2/F6/F9/F17/F18/F20/F21/F23/F25/F26 are PA (Appendix A); F5/F13 are OOS (MCP).

---

## 1.F — Notification & event taxonomy, pure logic (`notifications.py`, `events.py`) — G1, G2, G3, G5, G6, G18, G23–G30, G32

Fabricate event records and assert selection/priority/coalescing logic directly (as
`test_manager_notifications_adversarial.py` does). The *live‑lane‑fired* angle of these
events is Phase 3.

67. **G1** actionable manager‑facing class membership (RELAY_READY, REQUEST_AMBIGUOUS, RELAY_UNBOUND, REQUEST_EXPIRY_WARNING): assert each is in the actionable allowlist and non‑actionable ones are not.
68. **G2** duplicate‑controller/coding‑branch/coding‑worktree conflict events: fabricate the conflict → correct event kinds emitted.
69. **G3** `CODING_RESULT_INVALID`/`COORDINATION_FAILED` (TB‑SC): feed an invalid result (from 1.D E18) → these failure events emitted.
70. **G5** process‑health events (STALE_STATUS, PROCESS_STATE_UNKNOWN, PROCESS_INVENTORY_INCOMPLETE, OBSERVATION_ERROR): drive each from the matching reconcile fixture (1.E).
71. **G6** `MANAGER_SIGNAL` actionable event: fabricate a manager signal record → surfaced as actionable (the allowlist itself was already exercised via B5).
72. **G18** `HARNESS_SCAN_COMMITTED` atomic scan‑commit marker: run a scan → marker present exactly once.
73. **G23** `HARNESS_WATCHER_ALERT` top‑priority: with a watcher alert + a lower‑priority event pending, alert is selected first.
74. **G24** numeric preemption priority table (0 alert … 5 RESULT_AVAILABLE): assert the constant ordering and that `preempt_pending_with_higher_priority` respects it.
75. **G25** disposition tri‑state EVENT_DISPOSITION_WAKING/_OBSERVED/_SUPERSEDED: drive a supersession → transitions asserted.
76. **G26** record kinds EVENT/ACK/SUPERSESSION: construct one of each → classified correctly.
77. **G27** lane‑notification outcome codes ALREADY_ANSWERED/INVALID_LANE_ID/LANE_NOT_LIVE (TB‑SC): notify an answered / bad / dead lane → each code.
78. **G28** `notification:"MANAGER_ACTION_REQUIRED"` field convention: assert actionable events carry this field.
79. **G29** deferred/durable notification + priority preemption (`select_actionable_with_deferred`, also A21): higher‑priority arrival preempts a deferred pending one.
80. **G30** coalescing of mutable handoffs (`coalesce_mutable_handoffs`, also A22): two mutable handoffs for the same target → coalesced to one.
81. **G32** `RESULT_AVAILABLE` terminal‑result event (TB‑SC): a terminal valid result fixture → `RESULT_AVAILABLE` emitted at lowest priority.
> G7/G14/G20 already TESTED‑PASSED; G4/G22/G31/G33 are PA; G8–G13/G15/G16/G21 need a
> live lane → Phase 3; G17/G19 are CX‑GAP → Phase 4.

---

## 1.G — Resume & handoff admission (`resume.py`, `resume_admission.py`, `handoff_preflight.py`) — K2–K8, K10

82. **K2** `ResumeAdmission` identity‑matching gate (`make_resume_admission`/`require_resume_admission`, also A26): matching identity admits; call it.
83. **K3** resume‑identity mismatch rejection (`_compare_identity`): mismatched manager/session identity → rejected.
84. **K4** resume amendment diff‑based review validation (`validate_resume_amendment_review`, also A27): valid diff‑review accepted; missing/altered review → rejected.
85. **K5** amendment review‑card payload load + digest (`_review_card_payload`/`_review_path_digest`): tampered digest → rejected.
86. **K6** amendment diff‑command safety (`_validate_review_diff_command`): unsafe diff command (shell metachars / non‑git) → rejected.
87. **K7** amendment job‑identity derivation (`_review_job_identity`): assert stable, matches the amendment.
88. **K8** `resume_thread_id` (legacy) vs `resume_identity.thread_id` (canonical) precedence: set both conflicting → canonical wins per documented precedence.
89. **K10** handoff preflight gate (`preflight_handoff`, also A28/B8): missing invocation file / amendment identity / required evidence → each blocks with a distinct reason; complete bundle passes.
> K1/K9 already TESTED‑PASSED.

---

## 1.H — Resource‑lock invocation semantics (`resource_locks.py`, `invocation.py`) — H9, H10

90. **H9** `exclusive_resources` field semantics: invocation declaring exclusive resources → claims attempted for exactly those; two lanes wanting the same one → second blocks (drive via `ResourceClaims`, filesystem‑only).
91. **H10** resource‑release‑possible on owner exit: owner claim + simulated owner exit → `RESOURCE_RELEASE_POSSIBLE`/release‑detection fires.
> H1–H8 are PA (Appendix A).

---

## 1.I — Provider adapter contract, non‑argv (`provider.py`, `providers.py`) — U5, U7–U11

92. **U5** `BaseProviderAdapter` shared contract: assert `ProviderCapabilities`/`ProviderOperationResult` shape for both registered adapters.
93. **U7** `_validate_adapter_contract` on a registered adapter: register a structurally‑incomplete adapter → contract check rejects it.
94. **U8** `classify_operation`/`unsupported_operation_result`: ask an adapter for an unsupported op → `unsupported_operation_result`, not a crash.
95. **U9** `provider_config_digest` config‑identity hashing: same config → same digest; one field changed → different digest.
96. **U10** `redact_command` secret redaction (also `redact_argv`): argv containing a secret‑looking value → redacted before logging/persist.
97. **U11** `build_provider_evidence`/`structured_handoff` evidence record: assert the evidence record shape + that it omits secrets.
> U6/U12/U13/U14/U16 already TESTED‑PASSED; U1–U4 are Phase 0; U15 is NOTED.

---

## 1.J — Host adapter records, non‑delivery (`host_adapters.py`) — N4, N5, N7

98. **N4** `ManagerEventAck` created only by a separate manager action: construct via the manager path → valid; assert a lane/coordinator path cannot fabricate one.
99. **N5** `NotificationStopDecision`: construct and assert the stop/continue decision shape.
100. **N7** severity / highest‑pending computation (`_severity_for`/`_highest_pending`): feed a mixed‑severity pending set → correct severity + highest‑pending.
> N1–N3/N6/N8 are CX‑GAP → Phase 4.

---

## 1.K — Config, profile, prompt bundle (`config.py`, `profile.py`, `prompt_bundle.py`, `prompt.py`) — Q1, Q2, Q4→(Phase 2), Q14, Q15, Q17

101. **Q1** `HarnessConfig` load with numeric‑bound clamping (`load_config`/`_number`/`_integer`): out‑of‑range numbers clamp to bounds; non‑numeric → error.
102. **Q2** declared‑relative‑path validation (`_declared_relative_paths`): absolute / traversal path in config → error.
103. **Q14** prompt‑bundle safe‑component‑path enforcement (`_safe_component_path`): component path escaping the bundle root → error.
104. **Q15** `bundle_from_record` reconstruction: persist a bundle, reconstruct from record, assert byte‑identical components + digests.
105. **Q17** `prompt.py` constants/templates: assert the documented template constants exist and compose without unresolved placeholders.
> Q3/Q12/Q13/Q16 already TESTED‑PASSED; Q5–Q11/Q18–Q20 are PA; Q4 → Phase 2 (child env).
