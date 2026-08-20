# Named Persistent Doer Roster

A doer name identifies one persistent doing-subagent session, not a task. If the manager opens
`N` concurrent execution lanes, it uses exactly `N` named persistent doers. Each task is assigned
to exactly one doer, and each doer runs at most one task at a time. A doer may receive another task
only after its current task reaches a terminal or manager-checkpointed handoff.

Already completed/bootstrap tasks receive no retroactive doer name. The named pool applies to the
roster-owned catalog tasks; it is not conditioned on any eligibility-map row or every unrelated
H00–H05 case finishing first.

## Persistent lane doers

| Doer | Assigned catalog tasks |
|---|---|
| Atlas | S10, S13, A20, A22, D30, D32, Q41 |
| Boreal | S11, A21, D31, D36 |
| Cygnus | S12, A24, D33, D34 |
| Delta | A25, A26 |
| Nova | A23 only |

The [Firmware provider-adapter contract](../../../../PROVIDER_ADAPTER.md) is the sole authority
for model/effort/tier/route configuration and the pending-adapter rule. This roster owns only
named doer/task continuity and catalog coverage.

## Persistent sprint MCP reviewer

Each selected sprint/module has one persistent, read-only firmware-MCP reviewer. The contract
defines its allocation and the separate server-repair roles. This roster's local rule is that the
reviewer never operates hardware or edits firmware, the server, or the harness.

On every scheduling pass, the manager launches or resumes every dependency-ready,
resource-compatible doer lane concurrently. A blocked lane never holds an unrelated lane. Row
number, row membership, and row completion are never prerequisites. The table is a stable
ownership assignment, not permission to run conflicting tasks concurrently.

Appendix A is non-gating. If tried autonomously after main work cannot be delayed, D35/R38 retain
Delta and R37 retains Cygnus; they do not occupy or block a main-suite lane when they require
operator intervention. Record `SKIPPED_AUTONOMY_REQUIRED` without asking the user.

## Q40 branch tasks

Q40 is manager-owned aggregation rather than an executable catalog test. Each genuinely missing
Bxx branch is assigned in `SUITE_COORDINATION.md` to exactly one currently idle ordinary doer from
Atlas, Boreal, Cygnus, or Delta. A doer runs at most one branch at a time. Nova is not reused, and
no new branch-specific doer is created.

## Identity rules

1. Record doer name, provider agent/session ID, model, current task, run directory, and state in
   `SUITE_COORDINATION.md`.
2. Never have two live provider sessions under one doer name or two doers assigned to one task.
3. A task's internal board/family shards remain under its assigned doer. The doer may orchestrate
   disjoint processes but may not delegate a shard.
4. Reviewers and server-repair roles are not doers and do not use these names.
5. A necessary session/model replacement retains the doer name, records old/new provider
   identities, and proves the old identity is no longer active.
