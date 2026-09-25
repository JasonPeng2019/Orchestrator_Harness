# STEP-01 - Existing foundation is reviewed and integrated

> Completed and accepted. This is a historical plan record, not active work.

## Outcome

The already-completed Stage-A candidate is either integrated unchanged or with
only material corrections found during review. Its contracts, SQLite foundation,
privacy/configuration guards, local templates, APC data contract, and optional
product-harness handoff become the base for all remaining work. Nothing in this
step reimplements that slice or attempts to prove the unfinished full product.

## Scope and touchpoints

Review the candidate named in `PLAN.md` against product `main`, its `RESULT.json`,
and the relevant Feature/Implementation contract sections. The owned source is
`pyproject.toml`, `src/memory_harness/`, the memory-handoff changes under
`harness/orchestrator_harness/`, and their focused tests. The current native lane,
pending manager event, and exact worktree are resume facts kept in `HANDOFF.md`.

## Implementation

1. Inspect the actual candidate diff and confirm that it supplies the advertised
   Stage-A behavior without a second launcher, review system, learner, benchmark
   code, or unrelated harness expansion.
2. Use the worker's already-recorded checks. Independently rerun only the focused
   local and affected harness checks needed to decide any uncertain behavior; do
   not repeat the wheel build or create a new smoke wave merely to duplicate valid
   evidence.
3. If review finds a behavior-impacting defect, correct it in the existing lane
   or a narrowly scoped continuation and rerun only checks that consume the changed
   code. Report wording, line-ending warnings, or expected harness overlays are not
   product defects.
4. Record the required native completion review, handle the pending event, retire
   the accepted lane, and integrate the candidate into product `main`. Preserve the
   candidate if review finds a material defect that cannot yet be corrected.

Do not run the old Stage-A nested APC smoke. The current source implements an APC
request/result contract, not the real child launcher; the decisive native APC path
belongs to Steps 04 and 06.

## Dependencies and integration

This step consumes only the existing pending candidate and its native lifecycle
state. The integrated commit becomes the sole base for Step 02. No new worker or
parallel worktree is needed unless a material code correction cannot safely be
made in the current lane.

## Requirement-fit validation

- Inspect exact task/plan/base binding, candidate-plan non-authority, envelope
  mutation rejection, dispatch intent/ambiguity, and optional-content omission
  for T02-T03.
- Confirm fixed Standard/Problem-focused/Deeper configuration, all-off bypass,
  deferred learned-mode rejection, and worker credential scrubbing for T17, T18,
  and T21 at the surfaces that exist in this foundation.
- When an independent rerun is needed, use the confirmed commands from the
  candidate result: `python -m unittest discover -s tests/local -q`, then from
  `harness/` run the focused `test_memory_handoff`, `test_addendum3_product`,
  `test_launch_lifecycle`, `test_cleanup_exit_races`, and `test_processes` modules.
  A rerun is not required solely because the native result summarized them.
- Ensure the integrated tree contains the reviewed candidate bytes. A Git identity
  mismatch or merge conflict requires inspecting the resulting bytes, not blindly
  repeating all tests.

## Failure scope and recovery

A material contract, persistence, or harness-seam defect blocks Step 02 because
later code imports that foundation. Repair the defect and rerun its focused tests.
An invalid administrative field or unhandled event blocks only the corresponding
harness lifecycle action; correct it without discarding source or behavioral
evidence. If integration changes code, rerun the affected checks on the integrated
tree; a byte-identical integration reuses the candidate evidence.
