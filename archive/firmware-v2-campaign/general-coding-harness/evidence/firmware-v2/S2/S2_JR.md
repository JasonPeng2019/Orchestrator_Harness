# S2.JR review join and triage

- Reviewed candidate: `c998e41ad30b7a20ab36ed8f659483a29b376e7f`
- R1 safety/provenance review SHA-256:
  `4680474716a5f73b3ba9a6e2102ef42808271b494177902b93d68ddb8c3a7773`
- R2 target/evidence review SHA-256:
  `6e6174dde9e1c73f3edb19ca432d33d5da43f0e47b7128db5c0f9c15dcfbfbb5`
- Decision: both reviewer FAIL results are schema-valid and all ten findings collapse into seven
  accepted product-gap groups below. No reviewer requested hardware access or server mutation.

## Accepted product gaps

1. Replace invented/removed MCP method and parameter names with the exact guarded registered surface
   of pinned server `f003f84`; bind method version/schema and normalized parameters.
2. Make the evidence chain exact and non-skippable across same-call identities and every immediately
   preceding hash; validate decision/authorization/C1/governing/plan/permission/claim/route/server
   bindings instead of accepting caller assertions.
3. Make controller-only physical capability enforceable: absolute pinned command and working root,
   isolated `.firm`/artifact/log roots, comprehensive inherited-capability clearing, separate stderr,
   exact process/lifetime/cleanup ownership, and no O/target endpoint or launch handle.
4. Bind and validate the full verified resource provenance: all four datasheets, toolchain file hashes,
   fixture declaration path/hash, server cleanliness/pin, and build provenance.
5. Enforce P.05, legal-RF, authorization/expiry/timeout, path confinement, symlink/reparse rejection,
   create-new writes, and cleanup from authoritative bound evidence rather than booleans supplied by
   the caller.
6. Turn the five-file seed into an exact fresh disposable Git target with immutable/read-only seed
   proof. Expand the charter, per-ID test contract, typed closed evidence/result schemas, dependency
   fingerprints, and three-way failure routing enough to execute/adjudicate the bounded campaign.
7. Add focused hostile-path coverage for rewrite/tamper/tree injection, cross-call/skipped-stage
   ordering, identity/hash mismatch, expiry/timeout/cleanup, contention/resume/selective-rerun,
   actual worker environment isolation, and fresh-target materialization.

## Rejected criticisms

ROOT-IM agrees with the reviewers that live hardware work, a DIO2 mapping, exhaustive catalogs,
destructive cases, extra boards, UI/database/endurance work, a scheduler, or a general hardware
framework are invalid requirements for S2. The clean pinned server is not edited unless a focused
test reproduces a source defect.

Both R1 and R2 risk areas require production changes, so both exact reviewer threads must be revived
after S2.P repairs this joined finding set. Only the focused dependency-invalidated product tests run
before rereview.

## Gated repaired-tip rereview and cost-benefit triage

- Repaired candidate reviewed: `d08b6ccf3d2e0eacd3686b01658645249dfcc0a0`.
- R1 rereview SHA-256: `2c41f316299800e8cef6ae9d76b3f64e805952d8308cdef43455c83e65adaa04`.
- R1 findings SHA-256: `c96c45130e7bdbbbf8d3e5cf40ff14a49602f72a27904316843d93b0bf93e4fb`.
- R1 executable triage SHA-256: `6c3b55fe98c622ba38eccb2edc2029e5b55ffcf4cfa654808de9c282a329af58`.
- R2 rereview SHA-256: `307641d9162768d8a809a6fa6b5ccff9dd27397c400b4e6d3f169adad6dc11e4`.
- R2 findings SHA-256: `32a154902e6332b3cee4a809812eca4cf2cd1eddc854a1e42e0ae02a7d26aa5a`.
- R2 executable triage SHA-256: `9f54ec05f59c06906ba9dd6426b8b6ebc1963e9bf5cc293b012d5ae577e876c7`.
- Both triage artifacts passed the candidate's `validate_finding_triage` against the actual findings
  paths, hashes, and exact ID sets.
- The reviewed findings/results/rereviews were then moved intact to immutable S2 evidence names
  `S2_R{1,2}_{FINDINGS,RESULT,REREVIEW}_d08.*`; triage paths were updated and revalidated before the
  final same-thread rereview.

ROOT-IM accepts four joined, reproducible, net-positive repair groups:

1. Correct the pinned `read_memory_address` policy from invented `size` to bounded `width` and
   `length`, with exact signature coverage.
2. Bind exact clean server revision and one canonical operation-authority object/hash--method,
   normalized arguments, policy, plan, permission, authorization, claim, deadline, route, and seed
   identity--through every immutable call stage.
3. Make every selected acceptance ID a compact executable contract with deterministic input/action/
   oracle, failure injection, evidence type, dependency fingerprint inputs, registry/selective-rerun
   semantics, cleanup, and allowed failure route; close and consume its evidence schema.
4. Add an opt-in coding-child environment isolation policy used by project target-worker templates,
   plus defined pre/post seed/tree validation boundaries and focused synthetic hostile proofs. This
   does not make target-created application files immutable and does not add a scheduler/framework.

ROOT-IM rejects R1 `S2R1-TRIAGE-003` and R2 `S2R2-F03`. A manager cannot triage a finding before the
controller safely validates and publishes that finding's lane result; making result validation wait
on future manager evidence is circular and adds net-negative lifecycle complexity. The correct
enforced order is gated lane result, exact manager join/triage validation, then repair or acceptance,
which these artifacts demonstrate. No source edit is authorized for the rejected findings.

## Final targeted rereview at `66e053a`

- R2 returned schema-valid `PASS` with an empty gated finding set. Its reviewed risk area is green
  and is not rerun unless a later change invalidates it.
- R2 result SHA-256: `b2dc08992c6cca0de74018119a375d5b7d68fd958e313a9460ab523e859f115d`.
- R2 findings SHA-256: `f58b669a443a03c37762f917f950890da7fb242ab13e60be32117b3afa567f1b`.
- R1 returned schema-valid `FAIL` with exactly one admissible finding,
  `S2R1-RAW-RESULT-001`: the bound operation asserts `raw_result_sha256`, but admission does not hash
  retained raw-result bytes or compare their digest with that assertion.
- R1 result SHA-256: `2720de3964224a1c9b95d796cd8dedd9d36b8b76b28edcccb69b5640ceebca8a`.
- R1 findings SHA-256: `1001b1c2520d5adcf82ec05c54d270624c09fff5dc4ac43c0627c6cb88867e45`.
- ROOT-IM accepted only that bounded provenance defect in `S2_R1_FINAL_TRIAGE.json`: the problem is
  codebase-breaking at the physical evidence boundary, the smallest correction is localized, and
  its benefit outweighs its low complexity, regression risk, and verification cost.
- The earlier request for pre-result manager triage remains rejected as causally circular and
  net-negative. R2 remains green; only the exact R1 dependency path may be repaired and rerun.

## Product-review closure at `196d686`

- S2.P repaired only accepted `S2R1-RAW-RESULT-001` in commit
  `196d68660f934154248c9400f03a937a792fcb68`; its two directly invalidated raw-result identity
  tests passed. The pinned MCP server remained clean at `f003f84...`, and no hardware was accessed.
- R1's failed `66e053a` artifacts were preserved immutably as `S2_R1_{FINDINGS,RESULT,REREVIEW}_66.*`.
  `S2_R1_FINAL_TRIAGE.json` was rebound to that immutable findings path and passed the candidate's
  exact-file/hash/ID triage validator again.
- The same R1 thread reviewed only `66e053a..196d686` and returned gated `PASS` with no findings.
  Result SHA-256: `5077445d11af8226906f6788f086443891e3a6eb95ea4206b1c88489f8985544`;
  findings SHA-256: `45980d0e6c3144e9308ec068370867a42fc85347fb7b21d4a36ada073bbc3212`.
- R2 remained credited and was not rerun because the final repair did not touch its target/evidence
  risk area. Its result and empty-findings hashes remain `b2dc0899...` and `f58b669a...`.
- S2.JR is closed. There is no remaining admissible product finding; suggestions that are merely
  nicer, speculative, stylistic, or not worth their repair risk remain non-authorizing.
