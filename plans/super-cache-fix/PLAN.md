# Neutral Optional Super-Cache Fix

## Working location and destination

Work in `harness-single-worktrees/super-cache-fix` on a dedicated branch created from
`9f383712438d57cfcd8aea6b85c7fb284c7ecf3a` in the shared `harness-single` repository.

The dirty `firmware-v1.5-harness-runner` checkout and its historical branch must remain unchanged.
After ROOT accepts the result, publish the accepted commit to
`working/firmware/v2-candidate` and update the root repository's
`harness-v2-firmware-runner` submodule to that exact commit.

## Goal

Keep the super-cache provider-neutral, content-neutral, and optional. The harness may ingest a
user-selected folder, prepare either an orchestrator or subagent worktree from those contents,
verify a supplied receipt, and restore the overlay. It must not ship or require its own cached
hooks, verifier, rules, or other payload.

## Step 1 — Restore the clean implementation base

- Start from `9f38371`, before the payload-specific `4ed577c` changes.
- Confirm the generic ingest, prepare, receipt, collision, and restoration implementation remains
  present.
- Do not import the bundled super-cache payload or controller Stop-verifier coupling from
  `4ed577c`.

Acceptance: the implementation base contains the generic overlay machinery and no checked-in
super-cache content.

## Step 2 — Keep only generic receipt improvements

- Keep `overlay_receipt` optional for coding and canonical invocations.
- When no receipt is supplied, launch normally and record that no overlay was verified.
- When a receipt is supplied, verify it before provider construction or launch.
- Derive the expected receipt role from the invocation's `orchestrator` or `subagent` role instead
  of hard-coding `subagent`.
- Reject a missing, incomplete, wrong-worktree, or wrong-role supplied receipt before provider
  launch.
- Do not require `.agent/stop-verify.ps1`, call a cached verifier, add `prepared_stop` state, or infer
  hook trust merely from the existence of a cache receipt.

Acceptance: optional use works for both roles, and receipt validation remains fail-closed only when
the caller elects to use the cache.

## Step 3 — Selectively restore valid setup functionality

- Retain the separately packaged `workspace rules install` command that appends the managed
  `QUICK_RULES.md` block to the ROOT workspace's `AGENTS.md` idempotently.
- Keep Codex, Claude, and Qwen adapter installation and manager-event binding separate from the
  super-cache.
- Rewrite README setup instructions to require an explicit user-selected source folder and
  `workspace super-cache ingest` before `workspace prepare`.
- State clearly that the repository ships no cache payload and that adapter hooks are installed by
  the provider adapters, not supplied by the cache.
- Do not add `super-cache/AGENTS.md`, `super-cache/.super-cache.json`, `.codex/hooks.json`, or
  `.agent/stop-verify.ps1`.

Acceptance: the documented commands match the implemented neutral workflow, while ROOT workspace
rules and provider-adapter hooks remain explicit independent features.

## Step 4 — Verify and publish

ROOT must run:

- the changed-file Ruff, BasedPyright, compilation, and focused test gate;
- focused overlay tests for empty/user-supplied ingest, both roles, optional launch, supplied-receipt
  rejection, collision handling, and restoration;
- focused Codex, Claude, and Qwen provider/controller tests affected by the receipt seam; and
- one real Codex subagent lane through the actual controller using a fresh disposable Git worktree
  and a user-created cache source.

The real Codex proof must show:

1. The repository's cache starts without a bundled payload.
2. Ingest copies only the disposable source contents.
3. Prepare copies those contents into the subagent worktree and publishes a matching receipt.
4. The controller verifies the supplied receipt before launching Codex.
5. The Codex worker completes a small deterministic file task without relying on a cached harness
   hook or verifier.
6. Retirement/restoration removes or restores the overlay according to the receipt without losing
   the worker's unrelated change.
7. The provider process and resource claims are clean afterward.

All covered commands follow `BOUNDED-TEST-v1` with unique result paths. A failed or timed-out live
provider attempt is classified before any retry and does not erase deterministic passing evidence.

After all required evidence passes, ROOT commits the exact result, pushes it without force to
`working/firmware/v2-candidate`, updates the `harness-v2-firmware-runner` submodule to that commit,
and reads back local and remote equality.

## Done when

- Super-cache is optional and contains no repository-owned payload.
- Supplied receipts are verified early and correctly for orchestrator and subagent roles.
- Generic ingest, prepare, collision, receipt, and restoration behavior remains green.
- ROOT workspace rules and provider adapter hooks remain separate explicit installation features.
- The real Codex subagent proof passes.
- The accepted commit is pushed to the v2 branch and the root submodule points to it.
- `firmware-v1.5-harness-runner` remains untouched.
