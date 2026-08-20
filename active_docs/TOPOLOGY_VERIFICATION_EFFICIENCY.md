# Verification efficiency changes

## Why this exists

The paused candidate safeguard confirms a real workflow defect: its PowerShell loop throws on the
first failed check. It therefore never collects the later check results, and a later attempt starts
the selected list over from the beginning. The current script already accepts changed paths and a
credit-file input, but it does not yet use either to run incrementally.

This document changes the topology compiler. It does **not** claim that the currently paused WIP
safeguard is resumable today, and it does not change Plan 2 by implication. Before Plan 2 resumes,
ROOT must explicitly amend it and authorize the smallest target-harness implementation needed for
the new runner behavior.

## 1. Scoped product fast lane v2

The existing fast lane remains for strict test-only corrections. `FAST_LANE_V2` is a second, narrow
route for a ROOT-confirmed scoped production repair.

It is available only after the originating checking tranche finishes every feasible unit and returns
one complete pool containing one scoped compatible material correction objective. ROOT then supplies
all of these facts in the repair card:

- The exact observed failure and the one deterministic motivating test that proves it.
- The bounded production surface and protected behavior.
- A minimal smoke: compile every changed production source and run the motivating test.
- A frozen-tip independent review and a normal separate integration decision.

That route skips the normal broad affected-check campaign. It does not waive behavior proof: the
minimal smoke proves the repaired defect, review checks the change, and the incremental gate retains
or runs every remaining required check according to its input map. The compile and motivating-test
PASS from the smoke become reusable checkpoint credit; byte-identical integration does not rerun them.
It is unavailable when no deterministic motivating test exists, the change alters
test/runner/configuration selection, the impact is uncertain, the work involves an external/hardware
stateful action, or the complete pool requires a broader compatible repair batch.

## 2. Checkpointed, non-redundant gates

Every expensive multi-check gate is a sequence of independently runnable check units, not an opaque
all-or-nothing script. The gate records the first unresolved unit and the outcome of each completed
unit. It continues with every unit that is still runnable after an ordinary failure; only a real
dependency or live-harm containment can skip a unit, and the reason is recorded.

Each unit declares a conservative input set: source paths plus the configuration, runner, environment,
fixture, and external-state facts that can change its result. After a repair, ROOT compares the change
with those declared inputs:

- Reuse a previous PASS only when all declared inputs are unchanged.
- Form the rerun set from every failed, unresolved, change-affected, or uncertain unit.
- Execute that set in declared order from its earliest member. When no earlier unit was invalidated,
  this is the checkpoint's first unresolved unit.
- A cold start, or a change to a global input, is the only honest reason to run the complete sequence.

The record uses a repository revision or external attempt state only because check reuse must target a
specific source or real-world state. It does not add hashes, IDs, or immutable snapshots to ordinary
features or files.

For hardware/practical gates, a completed unit is reusable only when the target/fixture/resource state
it consumed has been verified unchanged. A firmware image, fixture allocation, lease, server behavior,
or target state change invalidates the consuming unit and its dependents; an unrelated source edit does
not.

## 3. Batch the complete finding pool

A deterministic campaign and final safeguard must collect every feasible selected result before ROOT
classifies repairs. ROOT then deduplicates and partitions the result pool by coherent repair objective.
One writer receives every compatible admitted finding in its tranche, produces one reviewable tip, and
is reviewed/integrated once. Independent findings use separate tranches only when they require
different owners, source contexts, or acceptance decisions.

Final assurance is not rerun after each individual fix. After the batch reaches an accepted integrated
coordinate, it runs the failed, unresolved, change-affected, or uncertain set from that set's earliest
unit. Passing, unaffected units remain creditable.

## Audit correction

The prior M04 recipe allowed a cheap failure to cancel later expensive paths. That contradicted the
complete-pool rule, so an independent cheap check now belongs in the same parallel group as every
other feasible path; only a named failed prerequisite or live-harm containment may skip one. The
second audit also removed a duplicate motivating-test rerun from `FAST_LANE_V2` and clarified that an
invalidated unit before the first unresolved unit must run first. M08 likewise reruns a failed or
input-affected readiness profile rather than assuming that only the original failed profile can
matter. The template now gives
`CHECKPOINTED_VERIFICATION_V1` its own Section 0 field and explicitly carries stateful practical or
hardware checks through the same reuse and continuation policy.

## Compiler changes made

- `design-project-topology/SKILL.md` now requires `FAST_LANE_V2`, checkpointed check units,
  conservative input maps, continuation after ordinary failures, and batch-first final assurance.
- `references/incremental-verification.md` holds the concrete compiler contract so the main skill
  remains readable.
- The plan template, compiler recipes, project-truth audit, and structural validator recognise the
  explicit `CHECKPOINTED_VERIFICATION_V1` / `FAST_LANE_V2` protocol for newly compiled plans.

## Amendment status and next runtime step

Plan 2 v3.9.20 now authorizes the small WIP-harness correction before another safeguard:
`MI-SAFEGUARD-CHECKPOINT-CORRECT` changes the current fail-fast executor into checkpointed,
continue-on-failure coarse units with conservative input maps. The correction must still complete its
ordinary candidate evidence, ROOT decision, and integration path before any release assurance claims
incremental behavior.

The run remains paused. On a future explicit resume, ROOT first classifies the known canonical-worktree
environment-only verification condition, then dispatches that correction. Until its accepted
integration, the actual safeguard remains the old monolithic behavior and must not be described as
incremental.
