# Candidate Harness Practical Acceptance V2

## Outcome

PASS. The candidate harness at `4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f` orchestrated a completely fresh typed Python taskboard from a minimal skeleton through production, audit, validation, integration, promotion, and exact shutdown. The candidate checkout remained clean and unchanged.

The final target `main` and `lane/m` both resolve to `86daa9901f46b41c14e26b45135fa553503021ef`. Promotion was `git merge --ff-only lane/m` after the candidate validated M's clean-tip result.

## Accepted Chain

| Lane | Accepted commit |
| --- | --- |
| P1 | `71b9939be10ea8de17775624e89f6b704af1b5f2` |
| P2 | `e6599ed3ce92f960795a5e92b11b855f38da5e68` |
| P3 | `1037577df29f1d54b7590ad3f3ee77a0d9123122` |
| P4 | `b1247c830ca8479f6b5e2607e4aa0d88b03456b8` |
| P5 | `cfd109f3db2960ee140b79863a23f62ff32167a1` |
| A1 | `8b562af2f247d880eed40bdabb2600ba28799c0a` |
| A2 | `2d1b94d00fd843273318561664bdd4e901dfe4a0` |
| D1 | `92a0f8dd472be8d2f11c63d238f6b0c7d1c9d258` |
| D2 | `7be84b13754bb9e4a65eff32533d04a9c49ebff0` |
| M | `86daa9901f46b41c14e26b45135fa553503021ef` |

Every adjacent pair passed `git merge-base --is-ancestor`. M also verified the common Git directory, distinct worktrees, and every accepted branch as an ancestor of its final tip.

## Target Validation

- Final manager validation on promoted `main`: 77 tests passed in 14.459 seconds.
- M validation: 77 full-suite tests, 58 focused core tests, 16 focused CLI/JSON tests, and 3 subprocess E2E tests passed.
- `compileall` passed on the final target.
- The implementation is standard-library-only and includes typed domain, SQLite storage, service, CLI, deterministic JSON interchange, atomic import validation, isolated tests, subprocess E2E coverage, and README documentation.
- A1 found ordinary domain validation issues, repaired them, and added regression coverage within the candidate coding flow.

## Harness Evidence

- All target workers used `orchestrator-coding-invocation/v1`, `gpt-5.6-sol` at medium reasoning as the recorded Luna-medium substitute, priority service, approval `never`, sandbox `danger-full-access`, and the candidate-supplied `--dangerously-bypass-approvals-and-sandbox` argv flag.
- P1 deliberately published base commit `e39b1031085ca2ca640494d4635073e287206beb` after advancing its branch. The candidate emitted `CODING_RESULT_INVALID` event `d4ee31189d90b906425e6dd9e7a65d53e675144afee7234933c31735a11fe843`; the result was handled, exactly acknowledged, and repaired by `p1-retry-002`.
- D2 later published a result with an overlong check name. The candidate rejected it with event `94de78ab092d9403f6ea2ded6c094439471faafc69c06d35fdefcdf9a932717b`; `d2-retry-002` revalidated and published the accepted result.
- P3 checkpointed at `5bd2a441b922ed484a0798d1857c2e6d31b3adca` without a result, then resumed worker `p3-001` on the exact persisted thread `019fc7b4-d325-75e1-a728-5b0fc3eab7a5`, repository identity, status path, and output paths.
- The retained candidate disposable fixture observed bounded named-resource contention, rejected a stale result, delivered and exactly acknowledged event `2aa468c513ece7a47771b8a950ea1fe601d8865d01c2567642567b07aa673c3c`, passed its tests, and ended with zero claims.
- The V2 observer recorded 19 exact acknowledgements with no pending or deferred notification. The final bounded native wait timed out quietly.
- Candidate controller native evidence contains 13 `CODEX_STARTED` and 13 `CODEX_EXITED` records.

## Shutdown

The final complete process snapshot found all 26 recorded controller/worker PIDs absent. Every retained controller status is terminal, every status matches native start/exit evidence, all worktrees are clean, and both target and candidate are clean. No coding-resource claim remains. No managed watcher or poller was launched. The isolated watcher was never contacted, inspected, or used; all control used candidate native `scan`, `watch --until-actionable`, and exact `ack --event-id`.

The required P3 same-path resume overwrote its start status before the auxiliary manifest was materialized. This auxiliary bookkeeping issue was corrected from the exact operator receipt and immutable native P3 start/exit records; authoritative candidate evidence remained consistent.

## Evidence Paths

- Runtime completion record: `plans/general-coding-harness/runtime/candidate-acceptance-v2/ACCEPTANCE_COMPLETE.json`
- Exact shutdown and process manifest: `plans/general-coding-harness/runtime/candidate-acceptance-v2/evidence/exact-shutdown.json`
- Final native scan: `plans/general-coding-harness/runtime/candidate-acceptance-v2/evidence/final-scan.json`
- Final test output: `plans/general-coding-harness/runtime/candidate-acceptance-v2/evidence/final-main-tests.txt`
- Retained contention fixture result: `plans/general-coding-harness/runtime/candidate-acceptance-v2/evidence/lock-fixture-result.json`
- Native controller events: `plans/general-coding-harness/runtime/candidate-acceptance-v2/controller-runtime/LANE_EVENTS.jsonl`
- Native observer events and acknowledgement state: `plans/general-coding-harness/runtime/candidate-acceptance-v2/runtime/observer/`

No candidate-harness defect was observed. V1 and the frozen harness were not used.
