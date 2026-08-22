# Multi-Agent Topology Audit

## Verdict

`PASS`. Product creation, candidate acceptance, independent observation, and final review used distinct roles. The outside writer-manager coordinated the work but did not impersonate the candidate harness orchestrator.

## Product-Creation Topology

The outside writer-manager serialized product ownership and integration. S1-S4 were created by a coordinated multi-agent system with bounded, disjoint review, test-authoring, and isolated-validation slices; they were not the practical-acceptance topology.

| Step | Product agent | Review agent(s) | Test agent(s) |
|---|---|---|---|
| S1 | `019fc6f6...` | `019fc6fe...` | `019fc704...` |
| S2 | `019fc70b...` | `019fc715...` | `019fc71d...` |
| S3 | `019fc726...` | `019fc72e-bf96...`, `019fc72e-dd8e...` | `019fc737-6726...`, `019fc737-8825...` |
| S4 | `019fc73f...` | `019fc748...` | `019fc74b-dbbc...`, `019fc74b-f036...` |

The authoritative per-step ownership and results are preserved under `../S1/` through `../S4/`. The parent outside writer-manager thread for this production and acceptance epoch was `019fc449-db7c-7a80-a5f8-8609f7af7156`.

## Practical-Acceptance Topology

Fresh V2 used a different system under test:

- Outside writer-manager/supervisor: thread `019fc449-db7c-7a80-a5f8-8609f7af7156`; it supervised boundaries and preserved evidence but did not perform F.C3.O work.
- Candidate orchestrator F.C3.O: `/root/acceptance_v2_orchestrator`, thread `019fc7a7-0475-7de2-a682-608ed5b4a2ae`.
- Independent watcher F.C3.W: `/root/acceptance_v2_watcher`, thread `019fc7a6-b0ce-7081-a8de-1dd08d45128f`.
- Target workers: candidate-launched Codex workers with separate rollout threads, invocations, branches, and worktrees for P1-P5, A1-A2, D1-D2, and M.

F.C3.O coordinated the serialized target chain and bounded author/validation waves through the candidate harness. F.C3.W remained read-only and isolated: no messages, acknowledgements, repairs, file edits, or control actions. This acceptance test used an orchestrator subagent; it did not reuse the outside writer-manager or the S1-S4 product-creation agents as that orchestrator.

## Final Review Topology

Exactly one final reviewer was used:

- Lane: F.C0.FR1
- Agent: `/root/f_c0_fr1_final_review`
- Model/effort: GPT-5.6 Terra-medium
- Thread: `019fc935-256b-78b2-929a-8e4eff882626`
- Parent outside writer-manager thread: `019fc889-3bb9-79c2-ad14-26494f6f1fe3`

The same reviewer performed the strict addendum; no second final reviewer was created. It was read-only, did not inspect the frozen checkout, and did not rerun candidate gates or practical acceptance.

## Model Substitution

C106 requested Luna-medium target workers and watcher. `../acceptance/CONTRACT.md` records that Luna was unavailable in the environment and explicitly authorizes Sol-medium for those roles. V2 used that substitution while preserving role isolation. The audit therefore records C106 as `AUTHORIZED_SUBSTITUTION`, not a literal Luna pass.
