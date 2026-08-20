# Coverage matrix — every inventory row → plan disposition

Every feature ID from `active_docs/claude_listed_Features.md` (A1–V8) mapped to exactly one
disposition, so nothing is silently dropped. Update the **Result** column as steps run.

**Legend for "Plan location":**
- `0.x` / `1.x` / `2.x` / `3.x` / `4.x` = the step in that phase file.
- `Done` = already TESTED‑PASSED in a prior session (re‑asserted only as a guard).
- `Appendix A` = PA (provider‑agnostic, already verified) — optional regression, not re‑run.
- `4.D` = OOS (firmware / MCP / legacy watcher) — excluded by instruction.
- `NOTED` = observed, not counted as pass/fail (U15).

**Result values:** ` ` (todo) · `PASS` · `FAIL` (→ record in `evidence/FINDINGS.md`) ·
`BLOCKED` · `SKIPPED` · `N/A` (by decision, e.g. accepted CX‑GAP).

---

## A. High‑level / workflow (A1–A41)
| ID | Prior tag | Plan location | Result |
|---|---|---|---|
| A1 | TESTED‑FAILED | 0.1 | PASS |
| A2 | PASSED | Done | PASS |
| A3 | PASSED | Done | PASS |
| A4 | PA | Appendix A | |
| A5 | OOS | 4.D | N/A |
| A6 | PASSED | Done | PASS |
| A7 | PASSED | Done | PASS |
| A8 | PASSED | Done | PASS |
| A9 | TB‑NS‑V | 2.A (I4/A9) | PASS (independent receipt verification; see F2A-I4-1) |
| A10 | PASSED | Done; extended 3.C | PASS |
| A11 | PASSED | Done | PASS |
| A12 | TB‑NS | 1.D (E7) | |
| A13 | TB‑SC | 1.D (E14–E19) | |
| A14 | PA | 1.D (E18) / Appendix A | |
| A15 | PA | Appendix A | |
| A16 | PA | Appendix A | |
| A17 | TESTED‑FAILED | 0.4 | PASS |
| A18 | PA | Appendix A | |
| A19 | PA | Appendix A | |
| A20 | PA | Appendix A | |
| A21 | TB‑NS | 1.F (G29) | |
| A22 | TB‑NS | 1.F (G30) | |
| A23 | PASSED | Done | PASS |
| A24 | CX‑GAP | 4.A | ✅ PASS (test_compat_claude_adapter::test_A24) |
| A25 | TB‑NS‑V | 2.B (L6) | PASS (full broker orchestration end-to-end, no authority leak into public record) |
| A26 | PASSED (partial) | 1.G (K2) completes | PASS* |
| A27 | TB‑NS | 1.G (K4) | |
| A28 | TB‑NS | 1.G (K10) | |
| A29 | TB‑SC | 1.C (D3–D20) | |
| A30 | TB‑NS‑V | 2.F | PASS (22 tests; inert decoder, fail-closed, never actionable) |
| A31 | TB‑NS‑V | 2.G | PASS (19 tests; condition merging dedup/last-write-wins + recovery projection) |
| A32 | PA | Appendix A | |
| A33 | PA | Appendix A | |
| A34 | TB‑NS‑V | 2.E | GAP — F2E-A34-1 (read-only accessors only; no packaging/digest engine) (10 tests) |
| A35 | TB‑NS‑V | 2.D (O7) | PASS @2.D |
| A36 | PASSED | Done | PASS |
| A37 | OOS | 4.D | N/A |
| A38 | OOS | 4.D | N/A |
| A39 | TB‑NS‑V | 2.G | GAP — F2G-A39-1 (no ordered STOP_ASSIGNING→…→RESOLVED ledger) |
| A40 | OOS | 4.D | N/A |
| A41 | OOS | 4.D | N/A |

## B. CLI surface (B1–B19)
| ID | Prior tag | Plan location | Result |
|---|---|---|---|
| B1 | TB‑NS | 1.B | PASS (scan prints reconciled snapshot, EXIT_OK, no persistence) |
| B2 | TB‑NS | 1.B | PASS (finding F1B‑B2‑1: `--no-write` flag parsed but ignored, no-op, note) |
| B3 | TB‑NS | 1.B | PASS (watch --once = exactly one reconcile pass, cursor persisted) |
| B4 | TB‑NS | 1.B | PASS (watch --until-event returns on fabricated STALE_STATUS, not EXIT_TIMEOUT) |
| B5 | PASSED | Done; 3.B extends | PASS |
| B6 | PASSED | Done | PASS |
| B7 | TB‑NS | 1.B | PASS (watch --no-write: reconcile runs, store=None, tree unchanged) |
| B8 | TB‑NS | 1.B | PASS (valid bundle→exit 0; missing evidence→EXIT_INCOMPLETE + REQUIRED_EVIDENCE_EXISTS) |
| B9 | CX‑GAP | 4.B | ✅ PASS (test_compat_claude_adapter::test_B9) |
| B10 | CX‑GAP | 4.B | ✅ PASS (test_compat_claude_adapter::test_B10) |
| B11 | CX‑GAP | 4.B | ✅ PASS (test_compat_claude_adapter::test_B11) |
| B12 | CX‑GAP | 4.B | ✅ PASS (test_compat_claude_adapter::test_B12) |
| B13 | CX‑GAP | 4.B | ✅ PASS (test_compat_claude_adapter::test_B13) |
| B14 | CX‑GAP | 4.B | ✅ PASS (test_compat_claude_adapter::test_B14) |
| B15 | TB‑NS | 1.B; 2.C (P1/P2) | PASS @1.B + PASS @2.C (P1/P2: immutable view read-only enforced, write_source → ImmutableViewError) |
| B16 | TB‑NS | 1.B; 2.C (P6) | PASS @1.B + PASS @2.C (P6: archive written and hash-bound before git worktree close) |
| B17 | PASSED | Done | PASS |
| B18 | PASSED | Done | PASS |
| B19 | PASSED (partial) | Done; 0.1 re‑exercises | PASS |

## C. Invocation validation (C1–C24)
| ID | Prior tag | Plan location | Result |
|---|---|---|---|
| C1 | PASSED | Done | PASS |
| C2–C8 | TB‑NS | 1.A | PASS |
| C9 | PASSED | Done; 1.A re‑asserts | PASS |
| C10 | TB‑NS | 1.A | PASS |
| C11 | TB‑NS | 1.A | PASS |
| C12 | PA | Appendix A | |
| C13 | PASSED | Done | PASS |
| C14 | PASSED | Done | PASS |
| C15 | OOS | 4.D | N/A |
| C16 | TB‑NS | 1.A | PASS |
| C17 | TESTED‑FAILED | 0.3 | PASS |
| C18–C20 | TB‑NS | 1.A | PASS |
| C21 | PA | 1.A (#15) | PASS |
| C22–C23 | TB‑NS | 1.A | PASS |
| C24 | TB‑NS | 1.A | PASS (finding F1A‑C24‑1: dead unsupported‑op branch, note) |

## D. Task & result lifecycle (D1–D20)
| ID | Prior tag | Plan location | Result |
|---|---|---|---|
| D1 | PASSED | Done | PASS |
| D2 | PASSED | Done | PASS |
| D3–D18 | TB‑SC | 1.C | PASS |
| D19 | PASSED | Done | PASS |
| D20 | TB‑SC | 1.C | PASS |

## E. Git safety (E1–E20)
| ID | Prior tag | Plan location | Result |
|---|---|---|---|
| E1 | PASSED | Done | PASS |
| E2 | PASSED | Done | PASS |
| E3 | PASSED | Done | PASS |
| E4–E7 | TB‑NS | 1.D | PASS |
| E8–E13 | PA | Appendix A | |
| E14–E17 | TB‑SC | 1.D | PASS |
| E18 | PA | 1.D / Appendix A | PASS |
| E19 | TB‑SC | 1.D | PASS (finding F1D‑E19‑1: state gate not applied to result acceptance, note) |
| E20 | TB‑NS | 1.D | PASS (finding F1D‑E20‑1: no >1‑candidate ambiguity rejection, note) |

## F. Reconcile / discovery classification (F1–F26)
| ID | Prior tag | Plan location | Result |
|---|---|---|---|
| F1, F2 | PA | Appendix A | |
| F3, F4 | TB‑NS | 1.E | PASS (F3 finding F1E‑F3‑1: elevation only on RELAY_READY, note; F4 helper tri‑state OK) |
| F5 | OOS | 4.D | N/A |
| F6 | PA | Appendix A | |
| F7, F8 | TB‑NS | 1.E | PASS (F7 PROCESS_STATE_UNKNOWN fail‑closed OK; F8 EXITED/UNKNOWN OK) |
| F9 | PA | Appendix A | |
| F10–F12 | TB‑NS | 1.E | PASS (F10 BOUND/BOUND_EXPIRED/UNBOUND/ABSENT; F11 LIVE/ABSENT/UNKNOWN; F12 WARNING/CRITICAL/EXPIRED/UNKNOWN) |
| F13 | OOS | 4.D | N/A |
| F14 | TB‑NS | 1.E | PASS (RELAY_READY/RELAY_UNBOUND/REQUEST_AMBIGUOUS) |
| F15 | TB‑SC | 3.A (#10) | |
| F16 | TB‑NS | 1.E | PASS (DUPLICATE_CODING_WORKTREE + DUPLICATE_CODING_BRANCH; distinct‑repo negative control) |
| F17, F18 | PA | Appendix A | |
| F19 | TB‑NS | 1.E | PASS (`_record_kind` helper/mcp/filename/field/schema/default) |
| F20, F21 | PA | Appendix A | |
| F22 | TB‑NS | 1.E | PASS (`_is_utc_timestamp` Z/+00:00 accepted; naive/offset/garbage rejected) |
| F23 | PA | Appendix A | |
| F24 | TB‑NS | 1.E | PASS (finding F1E‑F24‑1: coding‑result memoized, task‑result path not memoized, note) |
| F25, F26 | PA | Appendix A | |

## G. Notification / event taxonomy (G1–G33)
| ID | Prior tag | Plan location | Result |
|---|---|---|---|
| G1, G2 | TB‑NS | 1.F | PASS (G1 finding F1F‑G1‑1: EXPIRED bucket not selectable, note; G2 DUPLICATE_*/RESOURCE_CONFLICT emitted) |
| G3 | TB‑SC | 1.F (#69) | PASS (CODING_RESULT_INVALID + COORDINATION_FAILED emitted) |
| G4 | PA | Appendix A | |
| G5, G6 | TB‑NS | 1.F | PASS (G5 finding F1F‑G5‑1: OBSERVATION_ERROR selectable only when lane/request live, note; G6 MANAGER_SIGNAL actionable) |
| G7 | PASSED | Done | PASS |
| G8–G13 | TB‑SC | 3.A | |
| G14 | PASSED | Done | PASS |
| G15, G16 | TB‑SC | 3.A | |
| G17 | CX‑GAP | 4.A | ✅ PASS (test_compat_claude_adapter::test_G17) |
| G18 | TB‑NS | 1.F | PASS (finding F1F‑G18‑1: kind declared, no in‑repo emitter; single record at contract level, note) |
| G19 | CX‑GAP | 4.A | ✅ PASS (test_compat_claude_adapter::test_G19) |
| G20 | PASSED | Done | PASS |
| G21 | TB‑SC | 3.A | |
| G22 | PA | Appendix A | |
| G23–G26 | TB‑NS | 1.F | PASS (G23 alert top‑priority; G24 numeric 0–5 preemption via behavior; G25 WAKING/OBSERVED/SUPERSEDED; G26 EVENT/ACK/SUPERSESSION + BOGUS rejected) |
| G27 | TB‑SC | 1.F (#77) | PASS (ALREADY_ANSWERED/INVALID_LANE_ID/LANE_NOT_LIVE; live→None) |
| G28–G30 | TB‑NS | 1.F | PASS (G28 MANAGER_ACTION_REQUIRED field; G29 deferred preemption; G30 mutable‑handoff coalescing) |
| G31 | PA | Appendix A | |
| G32 | TB‑SC | 1.F (#81) logic; 3.A (#10) live | PASS (logic: RESULT_AVAILABLE emitted at priority 5; live angle → 3.A) |
| G33 | PA | Appendix A | |

## H. Resource locks (H1–H10)
| ID | Prior tag | Plan location | Result |
|---|---|---|---|
| H1–H8 | PA | Appendix A | |
| H9, H10 | TB‑NS | 1.H | PASS (exclusive canonicalization + conflict raise; second claimant blocks CONTENDED; release-possible on owner exit, fail-closed while live) |

## I. Workspace overlay (I1–I10)
| ID | Prior tag | Plan location | Result |
|---|---|---|---|
| I1 | PASSED | Done | PASS |
| I2 | PASSED | Done | PASS |
| I3 | PASSED | Done | PASS |
| I4 | TB‑NS‑V | 2.A | FINDING (F2A-I4-1) — verify is structural/identity-only; byte-integrity enforced at restore |
| I5 | TB‑NS‑V | 2.A | PASS |
| I6 | PASSED | Done | PASS |
| I7 | TB‑NS‑V | 2.A | PASS (junctions available on host; not skipped) |
| I8 | TB‑NS‑V | 2.A | PASS |
| I9 | TB‑NS‑V | 2.A | PASS |
| I10 | TB‑NS‑V | 2.A | PASS |

## J. Release checks & checkpoint/credit (J1–J16)
| ID | Prior tag | Plan location | Result |
|---|---|---|---|
| J1–J16 | PA | Appendix A | |

## K. Resume & handoff (K1–K10)
| ID | Prior tag | Plan location | Result |
|---|---|---|---|
| K1 | PASSED | Done | PASS |
| K2–K8 | TB‑NS | 1.G | PASS (K8 → F1G-K8-1: conflict fails closed, not "canonical wins") |
| K9 | PASSED | Done | PASS |
| K10 | TB‑NS | 1.G | PASS (handoff preflight blocks each missing piece distinctly) |

## L. Capability broker (L1–L10)
| ID | Prior tag | Plan location | Result |
|---|---|---|---|
| L1 | TB‑NS‑V | 2.B | PASS (closed-shape request + reason codes) |
| L2 | TB‑NS‑V | 2.B | PASS (frozen snapshot, MappingProxy nesting, byte-stable round trip) |
| L3 | TB‑NS‑V | 2.B | PASS (approval gate admits bound / denies non-approve, no permit on deny) |
| L4 | TB‑NS‑V | 2.B | FINDING F2B-L4-1 (bounded use is broker-enforced replay refusal, not a per-permit counter) |
| L5 | TB‑NS‑V | 2.B | PASS (result/cleanup pipeline; value objects fail closed on authority-alias material) |
| L6 | TB‑NS‑V | 2.B | PASS (end-to-end orchestration, claim→arm→cleanup→release ordering, no authority leak) |
| L7 | TB‑NS‑V | 2.B | FINDING F2B-L7-1 (missing adapter → DENIED SNAPSHOT_UNAVAILABLE, not raised) |
| L8 | PASSED | Done | PASS |
| L9 | PA | Appendix A | |
| L10 | TB‑NS‑V | 2.B | PASS (FakeCapabilityAdapter contract: supports/observe, fail_dispatch→FAIL+release, cleanup_proved=False→UNCERTAIN+retain) |

## M. Codex host adapter internals (M1–M16)
| ID | Prior tag | Plan location | Result |
|---|---|---|---|
| M1–M16 | CX‑GAP | 4.C (optional regression) | ✅ REGRESSION‑GREEN (Codex reference; 45 passed, evidence/4.C) |

## N. Host adapter framework / S4 delivery (N1–N8)
| ID | Prior tag | Plan location | Result |
|---|---|---|---|
| N1 | CX‑GAP | 4.A | ✅ PASS (test_compat_claude_adapter::test_N1) |
| N2, N3 | CX‑GAP | 4.A | ✅ PASS (test_compat_claude_adapter::test_N2/test_N3) |
| N4, N5 | TB‑NS | 1.J | ✅ PASS (test_compat_host_adapters) |
| N6 | CX‑GAP | 4.A | ✅ PASS (test_compat_claude_adapter::test_N6) |
| N7 | TB‑NS | 1.J | ✅ PASS (test_compat_host_adapters) |

| N8 | CX‑GAP | 4.A | ✅ PASS (test_compat_claude_adapter::test_N8) |

## O. Process supervision & identity (O1–O10)
| ID | Prior tag | Plan location | Result |
|---|---|---|---|
| O1–O6 | PA | Appendix A | |
| O7–O9 | TB‑NS‑V | 2.D | PASS (5 tests, 2 host-capability skips) |
| O10 | PASSED | Done | PASS |

## P. Lane lifecycle (P1–P12)
| ID | Prior tag | Plan location | Result |
|---|---|---|---|
| P1 | TB‑NS‑V | 2.C | PASS (immutable view at retained commit; VIEW_READY.json present) |
| P2 | TB‑NS‑V | 2.C | PASS (view.assert_read_only True; write_source → ImmutableViewError; B15) |
| P3 | TB‑NS‑V | 2.C | PASS (lifecycle registry admission with process-boundary record) |
| P4 | TB‑NS‑V | 2.C | PASS (registry updated atomically on transition) |
| P5 | TB‑NS‑V | 2.C | PASS (non-retained commit rejected; same-root view/result/cache rejected) |
| P6 | TB‑NS‑V | 2.C | PASS (retire archive-first: archive present + hash-bound before worktree close; B16) |
| P7 | TB‑NS‑V | 2.C | PASS — mismatched lane binding refused fail-closed as `outcome==VISIBLE` (not a raised exc); `_validate_lane_binding` → `LANE_BINDING_FOREIGN_WORKTREE`. See note F2C-P7P11-1 |
| P8 | TB‑NS‑V | 2.C | PASS (independent re-derivation of archive_content_sha256 == _archive_digest; per-member sha256/size match) |
| P9 | TB‑NS‑V | 2.C | PASS (good archive → orchestrator-lane-archive/v1; corrupted member → ArchiveFailed) |
| P10 | TB‑NS‑V | 2.C | PASS (three path spellings collapse to one canonical registry identity) |
| P11 | TB‑NS‑V | 2.C | PASS — retire without valid process proof (ProcessSnapshot(False)) refused fail-closed as `outcome==VISIBLE`, reason PROCESS_SNAPSHOT_INCOMPLETE. See note F2C-P7P11-1 |
| P12 | TB‑NS‑V | 2.C | PASS (_safe_member rejects ../, a/../b, absolute; crafted ../ archive member → ArchiveFailed; no fail-open traversal vector) |

## Q. Config / profile / prompt / stable I/O (Q1–Q20)
| ID | Prior tag | Plan location | Result |
|---|---|---|---|
| Q1, Q2 | TB‑NS | 1.K | ⚠️ Q1 FINDING F1K-Q1-1 (rejects, not clamps); Q2 ✅ PASS (test_compat_config_bundle) |
| Q3 | PASSED | Done | PASS |
| Q4 | TB‑NS‑V | 2.H | PASS (5 tests; declared kept, secrets/undeclared cleared, construction fail-closed, no fail-open) |
| Q5–Q11 | PA | Appendix A | |
| Q12, Q13 | PASSED | Done | PASS |
| Q14, Q15 | TB‑NS | 1.K | ✅ PASS (test_compat_config_bundle; Q14 symlink sub-case skipped on Windows) |
| Q16 | PASSED | Done | PASS |
| Q17 | TB‑NS | 1.K | ⚠️ FINDING F1K-Q17-1 (re-export shim, no template constants) |
| Q18–Q20 | PA | Appendix A | |

## R. Firmware/hardware (R1–R8) · S. MCP (S1–S3)
| ID | Prior tag | Plan location | Result |
|---|---|---|---|
| R1–R8 | OOS | 4.D | N/A |
| S1 | OOS | 4.D | N/A |
| S2 | OOS | 4.D; 3.D if MCP works | N/A |
| S3 | OOS | 4.D | N/A |

## T. Legacy/parallel watcher generation (T1–T6)
| ID | Prior tag | Plan location | Result |
|---|---|---|---|
| T1 | OOS | 4.D | N/A |
| T2 | OOS | 4.D | N/A |
| T3 | TB‑NS‑V | 2.G | GAP — F2G-A39-1 (see A39) |
| T4, T5 | OOS | 4.D | N/A |
| T6 | TB‑NS‑V | 2.F | PASS @2.F (A30) |

## U. Provider adapter contract & argv (U1–U16)
| ID | Prior tag | Plan location | Result |
|---|---|---|---|
| U1, U2 | TESTED‑FAILED | 0.1 | PASS |
| U3 | TESTED‑FAILED | 0.2 | PASS |
| U4 | TESTED‑FAILED | 0.3 | PASS |
| U5 | TB‑NS | 1.I | PASS (both built-ins share versioned contract shape + ProviderOperationResult fields) |
| U6 | PASSED | Done | PASS |
| U7–U11 | TB‑NS | 1.I | PASS (U7 incomplete/id-mismatch adapter rejected; U8 graceful unsupported + F1A-C24-1 raise; U9 digest stable/field-sensitive; U10/U11 no secret survives redaction into any token or evidence/handoff byte) |
| U12, U13 | PASSED | Done | PASS |
| U14 | PASSED | Done; 0.1/0.2 re‑exercise | PASS |
| U15 | NOTED | NOTED (0.2 note) | N/A |
| U16 | PASSED | Done | PASS |

## V. Lane controller (V1–V8)
| ID | Prior tag | Plan location | Result |
|---|---|---|---|
| V1 | PASSED | Done | PASS |
| V2 | PASSED | Done; 3.C extends | PASS |
| V3 | PASSED | Done | PASS |
| V4 | PASSED | Done | PASS |
| V5 | PASSED | Done | PASS |
| V6 | PASSED | Done | PASS |
| V7 | TB‑SC | 3.B | |
| V8 | PASSED | Done; 3.C extends | PASS |

---

## Appendix A — PA regression set (optional, not re‑run by this plan)

74 provider‑agnostic rows already verified end‑to‑end in the earlier Codex/DeepSeek session
(A4, A14–A16, A18–A20, A32, A33; C12, C21; E8–E13, E18; F1, F2, F6, F9, F17, F18, F20, F21,
F23, F25, F26; G4, G22, G31, G33; H1–H8; J1–J16; L9; O1–O6; Q5–Q11, Q18–Q20). Re‑run **only**
if a change touches the underlying module; otherwise they carry their prior PASS. They are
provider‑neutral by construction, so a Claude lane does not exercise them differently — which
is exactly why they are regression‑only, not primary compatibility targets.
