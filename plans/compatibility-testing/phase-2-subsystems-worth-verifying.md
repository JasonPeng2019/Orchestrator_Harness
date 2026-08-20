# Phase 2 — Subsystems worth verifying (TB‑NS‑V)

These are the **TB‑NS‑V** rows: provider‑neutral subsystems the inventory explicitly flags
as "worth verifying" because they were *never exercised in either session* — complex
enough that the Codex/DeepSeek evidence does not trivially cover them. All are testable
now with fixtures (real disposable git worktrees + filesystem), no live `claude`
subprocess. Runs in parallel with Phase 1.

**Method:** extend the existing subsystem tests where present
(`test_workspace_overlay.py`, `test_s5_capability_broker.py`, `test_operator_launch.py`,
`test_s6_public_release.py`, `test_attention_sprint.py` in the stable tree) or add
`test_compat_<area>.py`. Pass = new assertions green + existing suite still green.

---

## 2.A — Workspace overlay edge cases (`workspace_overlay.py`) — A9/I4, I5, I7, I8, I9, I10

The happy‑path round trip (I1/I2/I3/I6) already passed. These are the *failure/edge* paths
that round trip never touched.

1. **I4 / A9** `verify_overlay_receipt` independent verification: after `prepare_worktree`,
   verify the receipt **independently** (not via restore). Then corrupt one materialized
   byte and re‑verify → verification fails. Pass = clean verifies, corrupted rejects.
2. **I5** append‑only copy plan + collision detection (`_build_plan`/`_validate_append_targets`):
   materialize into a worktree that already contains a file at a target path →
   `OverlayCollisionError`. Pass = collision raised, no partial write left behind.
3. **I7** reparse‑point / regular‑directory‑only enforcement (`_is_reparse`/`_regular_directory`):
   point the overlay source/target through a symlink/junction → rejected before any copy.
4. **I8** receipt rollback on partial‑apply failure (`_rollback_applied`): inject a failure
   mid‑apply (e.g. make the Nth target unwritable) → **every** already‑applied file is
   rolled back to exact prior bytes; receipt reflects the abort. Pass = worktree
   byte‑identical to pre‑apply state.
5. **I9** declaration‑file read/validate (`_read_declaration`): malformed / missing
   super‑cache declaration → clear validation error; valid declaration parses.
6. **I10** byte‑encode/decode helpers (`_encode_bytes`/`_decode_bytes`): round‑trip
   arbitrary bytes (incl. non‑UTF‑8, embedded NULs) through the receipt encoding →
   decode returns identical bytes.

---

## 2.B — Capability broker (`capability_broker.py`) — A25, L1–L7, L10

The broker mediates request → approval → permit → adapter → cleanup. Only L8 (hashing) was
indirectly touched. Drive the full pipeline with the `FakeCapabilityAdapter` reference
adapter (L10).

7. **L1** `CapabilityRequest` construction: build a valid request; malformed request → error.
8. **L2** `CapabilitySnapshot` point‑in‑time capture: snapshot capability state; assert immutability of the snapshot.
9. **L3** `CapabilityApproval` mediated approval gate: approve a request → permit issuable; deny → no permit.
10. **L4** `CapabilityPermit` bounded‑use grant: assert the permit is single/bounded‑use — a second use beyond bound is refused.
11. **L5** `AdapterResult`/`CleanupEvidence`/`CapabilityResult` outcome+cleanup pipeline: run the fake adapter → assert cleanup evidence produced and result well‑formed.
12. **L6** `CapabilityBroker` full orchestration (A25): drive request→approval→permit→adapter→cleanup end‑to‑end via `FakeCapabilityAdapter` → success result + cleanup evidence.
13. **L7** fail‑closed paths `CapabilityDenied`/`CapabilityAdapterUnavailable`: deny a request → `CapabilityDenied`; point at a missing adapter → `CapabilityAdapterUnavailable`. Neither leaks a permit.
14. **L10** `FakeCapabilityAdapter` reference adapter itself: assert it honors the contract (used as the vehicle for L1–L7).
> L8 already TESTED‑PASSED; L9 is PA.

---

## 2.C — Lane lifecycle: immutable views & archive‑first retirement (`lane_lifecycle.py`) — P1–P12

Use a real disposable git repo + linked worktree.

15. **P1** `allocate_immutable_source_view` read‑only snapshot: allocate at a revision → view exists at that commit.
16. **P2** immutable‑view read‑only enforcement (`_set_read_only`): attempt to write into the view → denied by filesystem perms (also validates B15).
17. **P3** lifecycle‑registry admission with process‑boundary (`_admit_lifecycle_registry`): admit a lane → registry row with process‑boundary record.
18. **P4** lifecycle‑registry update on transition (`_update_lifecycle_registry`): transition state → registry updated atomically.
19. **P5** retained‑commit / separate‑root safety (`_retained_commit`/`_assert_retained`/`_separate_root`): allocate against a non‑retained commit / same‑root → rejected.
20. **P6** `retire_terminal_lane` archive‑first (also B16): retire → archive is written and hash‑bound **before** the git worktree is closed (assert ordering).
21. **P7** lane‑binding validation before retirement (`_validate_lane_binding`): retire with a mismatched lane binding → rejected.
22. **P8** archive digest / member‑copy integrity (`_archive_digest`/`_copy_member`): assert the archive digest matches recomputed content.
23. **P9** `validate_lane_archive` independent post‑hoc verification: verify a good archive → OK; corrupt a member → verification fails.
24. **P10** registry‑identity canonicalization (`_canonical_registry_identity`): two path spellings of one lane → one canonical identity.
25. **P11** process‑proof requirement before retirement (`_process_proof`): retire without process proof → rejected.
26. **P12** safe tar‑member‑name validation on extraction (`_safe_member`): craft an archive with a `../` member name → extraction refuses it (path‑traversal guard).

---

## 2.D — Operator launch & process supervision (`operator_launch.py`, `process_supervisor.py`) — A35, O7, O8, O9

Launch a short‑lived detached child (a `python -c "import time; time.sleep(...)"` stand‑in)
so no real lane is required.

27. **O7 / A35** detached long‑lived owner launch with exact creation‑identity (`launch_process`): launch → capture exact PID + creation time; assert identity recorded.
28. **O8** detached‑owner snapshot for external supervision (`detached_owner_snapshot`): snapshot the running owner → snapshot matches the launched identity.
29. **O9** cooperative exact‑identity termination (`_cleanup_exact_posix`/`_terminate_windows_exact`): terminate **by exact identity**; assert only that PID+creation‑time is signaled (never a broad kill), and a PID‑reuse decoy is *not* touched.
> O1–O6/O10 are PA / already‑passed.

---

## 2.E — Release‑manifest asset packaging (`release_assets.py`) — A34

30. **A34** public release surface / release‑manifest asset packaging: build a release
    manifest + package the declared assets from a fixture → assert manifest lists exactly
    the declared assets, each with a matching content digest, and packaging is
    deterministic (re‑run → identical bytes/digests).
> A32/A33 (selection engine, checkpoint/credit) are PA (Appendix A).

---

## 2.F — Attention sprint (`attention_sprint.py`) — A30 / T6

31. **A30 / T6** attention‑sprint historical record decoding
    (`decode_historical_attention_record`): feed a fabricated historical attention record
    (valid) → decodes to the expected structured sprint; feed a truncated/corrupt record →
    clear decode error (no silent partial). Model on `test_attention_sprint.py`.

---

## 2.G — Watcher recovery projection (`watcher_integration.py`) — A31, A39 / T3

32. **A31** watcher recovery projection / condition merging: feed a set of overlapping
    diagnostic conditions → assert they merge into the expected recovery projection
    (dedup + precedence), and a cleared condition drops out of the projection.
33. **A39 / T3** watcher alert / recovery ledger (`STOP_ASSIGNING → … → RESOLVED`): drive
    the ledger through the full state sequence with fabricated alerts → assert each
    transition is admitted only in order and `RESOLVED` clears the alert. *(This is the
    harness‑owned diagnostic observer, not the OOS legacy watcher generation.)*

---

## 2.H — Profile‑scoped child environment (`profile.py`) — Q4

34. **Q4** `build_child_environment` profile‑scoped subprocess env: build from a profile
    with denied names + declared capability/env names → assert the child env contains
    exactly the declared vars, excludes denied names, and strips inherited secrets.
    (Complements C21's invocation‑level isolation with the profile‑level construction.)
