# Handoff

## Objective

Finish the unaccepted fixed-strategy work governed by `goal.md` and
`.plans/memory-backed-harness/`, using one native lane-ROOT and one repaired,
frozen `harness-single` per lane. Master-ROOT alone integrates reviewed pins.
First prove the minimal MVP through STEP-16–18; then keep the run open and
repair every actionable deferred item in `KNOWN_ISSUES.md`.

Do not reopen accepted STEP-04 or the accepted first STEP-05 Level 0 slice,
implement the learned selector, run benchmarks, push, or broaden the harness.
The time-crunch acceptance rule in `NORMAL_OPERATION_ACCEPTANCE.md` controls:
only genuine normal supported behavior, credible regular recovery/
compatibility, and critical-invariant defects gate the MVP.

## Status

Current Windows checkpoint: 2026-09-26.

**Run state: PAUSED by explicit user request at 2026-09-26 08:56 -04:00.**
All native lane-ROOTs are stopped. Lane 1 and Lane 3 explicitly quiesced their
frozen harnesses and confirmed that no writer, reviewer, child process, active
epoch, or orphaned lease remains. Lanes 2 and 4 were already parked/completed.
Preserve all retained branches, worktrees, results, and historical evidence.

Master integration worktree
`development/product/integration/checkpoint-20260925` is clean at
`4263abf970d34c2b96957857eb38787b25775c09`, branch
`integration/checkpoint-20260925`, synchronized with its remote tracking ref.
After explicit user authorization on 2026-09-26, Master pushed that exact
integration pin and one latest accepted writer branch per lane to the existing
`Harness-Memory-Base` remote. The four frozen harness refs already matched their
configured remote branches, so no redundant or historical harness ref was
pushed. This HANDOFF belongs to the separately requested top-level `memory`
checkpoint push.

| Lane | Authoritative accepted pin | Current work |
| --- | --- | --- |
| 1 | `4f4d4e2e6a31c878b26a96c9966903c7e61476e5` | Paused before STEP-15-1. Manager root is clean at joined base `4263abf`; no STEP-15 task card, assignment, candidate, RESULT, or product edit exists. Frozen harness `9936c7f` has no running lane or orphaned lease. |
| 2 | `97dda4f97a55101f63b2d2c0fa0f4a2d04c416c4` | STEP-13-2 accepted/integrated. Parked until Lane 1 publishes the STEP-15 domain/recovery facade; then complete STEP-15-2. |
| 3 | `e64fda9cf54114f7321ea582f854c181805cccd1` | Paused before STEP-13-3. No STEP-13 card, assignment, candidate, RESULT, or lane-owned edit exists. Frozen harness `1fe069d` reports no active epoch/process; prior STEP-10 evidence is retained. |
| 4 | `7583549911d8f15bbea0a9e1d4daf776d35e69bf` | STEP-13-4 accepted/integrated. Lane 4 is implementation-complete until joined STEP-16, live Atlas STEP-17, and native STEP-18 evidence. |

## Completed

- The checkout and submodules were synchronized to their configured remotes;
  the four repaired lane harnesses remain isolated and frozen.
- The accelerated MVP policy is referenced by all 25 executable STEP files and
  acknowledged by all lane-ROOTs.
- Accepted/integrated through Lane 1 STEP-09, STEP-10, STEP-11, claimant/fence
  recovery, STEP-13, and STEP-14; Lane 2 KI-007 and STEP-13; Lane 3 STEP-09;
  Lane 4 privacy and STEP-10.
- Lane 1 STEP-14 pin `c4504d1` adds an authorized whole-store SQLite snapshot
  service, truthful capture/restore dependency readiness, preflight before
  mutation, local-only restore, and no replay of pending/uncertain work.
- Lane 2 STEP-13 pin `97dda4f` applies the captured effective network profile
  to real provider launches, records requested/effective attribution and
  installed payload limits, and never grants unproven Atlas-only isolation.
- Lane 4 STEP-13 pin `7583549` gates new/pending Atlas task calls by captured
  effective mode while permitting only exact one-write recovery of already
  submitted unresolved work; confirmed-complete work remains zero-call denied.
- Lane 3 churn audit showed the repeated STEP-10 failures share one cause:
  effect operation, ingestion, and case receipts settle in separate commits.
  Adapter-level rereads only move the race window. Lane 1 pin `773ddcf` now
  supplies one `BEGIN IMMEDIATE` settlement for effect, ingestion, case receipts,
  and the STEP-09 bridge. Lane 3 STEP-10-3 pin `e64fda9` consumes that provider
  for one claimed public EverOS submission, exact readback, authentic usage,
  and atomic effect/ingestion/receipt/bridge settlement; Master integrated it at
  `87afcab`.
- Lane 1 policy-context pin `4f4d4e2` sends only the closed opaque preparation
  ID/digest/schema pointer on both initial and final SearchStore callbacks,
  validates its exact durable record and route, preserves direct legacy calls,
  and fails custom nonhex durable IDs closed for network callbacks while local
  search continues. Master integrated it at `4263abf`.

## Verification

- Lane 2 writer and fresh reviewer each passed 191 focused tests. After merge
  to Master, the same command passed 191/191 in 64.274 seconds:
  `PYTHONPATH=src;harness python -m unittest orchestrator_harness.tests.test_provider_network_payload orchestrator_harness.tests.test_step04_launch_boundary orchestrator_harness.tests.test_memory_handoff orchestrator_harness.tests.test_setup_cache_recovery tests.local.contracts.test_config tests.local.preparation.test_step05_captured_configuration`.
- Lane 1 writer/reviewer passed 64 snapshot and adjacent checks. After merge to
  Master, the same five-module selection passed 64/64 in 3.319 seconds:
  `PYTHONPATH=src;harness python -B -m unittest tests.local.recovery.test_snapshot_restore tests.local.effects.test_local_effect_state tests.local.effects.test_external_reconciliation tests.local.usage.test_native_usage tests.local.procedures.test_procedure_contracts`.
- Both merges were conflict-free. Master `git diff --check` passes and the
  integration worktree is clean.
- Lane 4 fresh review returned SHIP on `7583549`. After merge, Master passed
  82/82 Atlas/procedure tests, 7/7 config tests, the focused local-delivery/
  zero-Atlas-call preservation test, and `git diff --check`.
- Lane 1 fresh review returned SHIP on `773ddcf`. After merge, Master passed
  53/53 atomic effect/ingestion/usage tests, 10/10 neighboring trust/outcome
  tests, and `git diff --check`.
- Reviewer-confirmed handle-local claim-token retention after voluntary
  uncertainty is document-only KI-011 and queued for the post-MVP repair pass;
  durable late/reopen mutation probes remained correctly fenced.
- Joined Lane-3 preflight reproduced KI-012: accepted provider `773ddcf`
  rejected the real adapter's deterministic transport IDs. Lane-1 correction
  `cb8407c` is reviewed/integrated and accepts only exact complete raw or mapped
  cohorts; no Lane-3 workaround was introduced.
- Lane 3's STEP-10-3 writer passed its exact 82-test experience/effect/usage
  selector. Fresh review returned SHIP and independently passed 31 atomic/
  reconciliation plus 23 gate/trust/retry tests. After merge, Master reran the
  literal seven-module writer selector: 82/82 passed in 4.961 seconds; the
  reviewed two-file delta also passed `git diff --check`.
- Lane 1's policy-context writer passed 204 focused and 24 neighboring tests;
  fresh exact-tip review returned SHIP. After merge, Master ran the literal
  focused selection with the joined tree: 206/206 passed in 18.248 seconds,
  then the neighboring selection passed 24/24 in 2.537 seconds. Integration
  `git diff --check` passed. The review's two unchanged missing-checkpoint
  fixture errors are document-only KI-013 and queued for post-MVP repair.

## Remaining

1. Lane 3 completes STEP-13-3 on exact joined base `4263abf` while Lane 1
   completes STEP-15-1 on the same base.
2. Lane 2 consumes the reviewed/integrated STEP-15-1 facade in STEP-15-2.
3. Master integrates reviewed pins and runs STEP-16 curated normal/critical
   checks, STEP-17 disposable live Atlas proof, and STEP-18 all-off plus
   enhanced native lifecycles.
4. After MVP proof, repair every actionable deferred code issue in
   `KNOWN_ISSUES.md`, review/integrate each owner pin, and update rows
   monotonically. Environment/non-product entries require honest disposition,
   not speculative product changes.
5. STEP-17 preflight found that the current live Atlas test revokes and drops
   its sole synthetic fixture in `finally`; by itself it cannot leave the owned
   eligible fixture STEP-18 requires. Resolve that verification seam before the
   live campaign, without weakening exact cleanup ownership.

## Important assumptions

- `goal.md`, the specification, plan, lane guide, and step cards are
  authoritative; stale top-level README scope is not.
- Lane workers never edit the Master integration worktree. Master does not use
  a repository harness.
- Harness changes are allowed only for reproduced run-blocking defects in
  already-implemented coordination behavior.
- Real Atlas-only, egress, claimant crash, and provider-native attribution
  claims remain for STEP-17/18; local doubles do not prove them.
- Preserve unrelated dirty/untracked artifacts and all historical evidence.

## Relevant files

- `goal.md`
- `.plans/memory-backed-harness/PLAN.md`
- `.plans/memory-backed-harness/NORMAL_OPERATION_ACCEPTANCE.md`
- `.plans/memory-backed-harness/KNOWN_ISSUES.md`
- `.plans/memory-backed-harness/specification/SPEC.md`
- `.plans/memory-backed-harness/steps/`
- `src/memory_harness/store.py`
- `src/memory_harness/snapshot.py`

## Next action

Remain paused until the user explicitly resumes. On resume, first re-read this
checkpoint, re-scan each frozen harness, and confirm Master still equals clean
joined pin `4263abf`. Then reuse the same native roots: launch one Lane-1
STEP-15-1 writer and one Lane-3 STEP-13-3 writer from that exact pin, each
followed by a fresh exact-tip review. Integrate their reviewed pins, then
reactivate Lane 2 for STEP-15-2. Do not perform any further push without new
user authorization.
