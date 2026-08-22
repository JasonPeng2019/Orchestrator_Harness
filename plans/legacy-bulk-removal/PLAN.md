# Legacy Firmware Bulk Removal Plan

## Plan status and work location

Completed and accepted on 2026-08-22. The v2 result is commit
`09e5786e338d9ebcf71230c8ad327808b2ec229b`, published at
`origin/working/firmware/v2-candidate`. The rollback base is
`f6f6c86403515bed644f1e08cee5bc9740db313a`.

The implementation and affected-surface checks passed. Three unchanged baseline assertions were
recorded separately during the broader verification pool: a one-second Windows resource-lock
timing test, a pre-existing reconciliation expectation, and an older Claude argv expectation that
omits the adapter's existing `--verbose` flag. They do not arise from the removal diff; provider
implementations and `resource_locks.py` are unchanged from the rollback base.

All implementation work must occur in an isolated linked worktree under
`harness-single-worktrees/`, using:

- worktree: `harness-single-worktrees/legacy-bulk-removal`
- allocation ID: `WT-LEGACY-REMOVAL-001`
- source: the current accepted tip of `harness-v2-firmware-runner`

Do not edit `firmware-v1.5-harness-runner`. It remains the recoverable historical implementation.

## Goal

Remove both obsolete firmware-specific routes from the v2 runner so it has one general-purpose,
canonical lane-management path while retaining generic shared-resource leasing and normal firmware
capability through ordinary worker lanes and their tools.

The finished v2 runner must:

- contain no direct capability broker, firmware campaign pack, or firmware hardware adapter;
- contain no legacy schema-less firmware lane or compatibility dispatch;
- retain canonical Codex, Claude, and Qwen lane behavior;
- retain provider-neutral `exclusive_resources` acquisition, contention, release, and cleanup;
- retain hooks, super-cache, events, resume, packaging, and public imports not owned by the removed
  routes; and
- be integrated only after ROOT accepts the frozen implementation and verification evidence.

This is deletion and simplification, not a redesign. Do not add a replacement firmware schema,
canonical capability-binding system, backend policy service, special rejection path, or new hardware
API. Old schema-less inputs should simply fail ordinary canonical invocation validation.

Live provider sessions and physical-hardware tests are not required because the change removes
isolated routes and must not change canonical provider or resource-management behavior.

## Ownership

| Role | Responsibility |
|---|---|
| ROOT | Defines the task cards, creates and admits the worktree, reviews the diff after MI-01 and MI-02, runs MI-03, classifies failures, accepts or rejects the result, and performs any authorized integration. |
| `PARITY_IMPLEMENTER` | Persistent implementation lane. Performs all product edits for MI-01 and MI-02 in the isolated worktree, runs only producer-owned focused checks, and returns terminal evidence to ROOT after each step. |

Worker launch configuration is resolved from the repository's sole active role mapping at execution
time. ROOT is not part of that mapping and is whatever model/session the user chose to run as ROOT.

There is one product writer. The implementer must not self-dispatch another role, integrate its own
work, or decide acceptance. ROOT must issue a separate card before each implementation or repair
turn.

## Execution graph

```text
worktree admission
        |
        v
MI-01 direct capability removal
        |
        v
ROOT scope review
        |
        v
MI-02 legacy lane removal
        |
        v
ROOT scope review and frozen tip
        |
        v
MI-03 deterministic verification
        |
        v
ROOT acceptance decision
        |
        v
authorized fast-forward, push, and readback
```

The path is serial because MI-02 edits shared invocation/controller surfaces after MI-01 changes
exports, tests, and documentation, and MI-03 must evaluate their combined frozen result.

## Worktree admission and resource rules

Before MI-01, ROOT must:

1. Read back the current v2 source branch, revision, remote, and clean status.
2. Create `WT-LEGACY-REMOVAL-001` from that exact accepted v2 tip on a dedicated cleanup branch.
3. Verify the new worktree is clean, points at the recorded base, and is located beneath
   `harness-single-worktrees/`.
4. Establish one logical writer claim, `LOCK-RUNNER-WRITER-001`, covering the cleanup branch and
   worktree through final acceptance or preserved failure.
5. Resolve the `PARITY_IMPLEMENTER` launch configuration and issue the MI-01 task card.

No second writer may touch the cleanup worktree. A dirty, ambiguous, active, or unaccepted worktree
must be preserved rather than deleted. Worktree retirement is allowed only after its accepted commit
is integrated and read back, or after ROOT explicitly records a terminal preserved state.

## MI-01 — Remove the direct firmware capability route

### Objective

Delete the unused direct-capability implementation and every surface that exists only to expose,
package, test, or document it.

### Required changes

The implementer must:

1. Delete:
   - `capability_broker.py`
   - `firmware_campaign.py`
   - `firmware_adapter.py`
2. Remove their public imports and exports.
3. Remove packaging, release-check, example, and documentation references that depend on them.
4. Delete focused tests whose only purpose is the direct-capability route.
5. In mixed tests, remove only the firmware-capability cases and retain every assertion covering
   canonical lanes, provider-neutral behavior, generic resource leasing, or shared cleanup.
6. Remove all runtime and public-API references to:
   - `CapabilityBroker`
   - `FirmwareCampaignPack`
   - `FirmwareHardwareAdapter`
   - their associated request, approval, and permit types.
7. Make no replacement implementation and do not move this behavior into canonical lanes.

### Producer proof

Before returning, the implementer must inspect the complete MI-01 diff and run the smallest focused
checks covering changed imports, exports, packaging, and retained mixed-test behavior. The handoff
must identify:

- the exact files deleted and edited;
- the exact focused checks and their outcomes;
- any remaining matching symbol and why it is not a v2 runtime/public reference; and
- the current worktree revision and status.

### ROOT checkpoint

ROOT reviews MI-01 before MI-02 starts. Acceptance requires:

- no direct-capability runtime or public API remains;
- retained mixed-test assertions were not accidentally deleted;
- generic `exclusive_resources` behavior was not coupled to or removed with the adapter; and
- the diff contains no redesign or unrelated cleanup.

A material issue returns to MI-01 under one complete correction card. A malformed or missing
handoff blocks only the next dispatch and does not by itself prove a product defect.

## MI-02 — Remove the legacy schema-less firmware lane

### Objective

Remove the compatibility route that allows a lane to use the old schema-less firmware format, so
the canonical coding invocation is the runner's only supported lane contract.

### Required changes

The implementer must:

1. Remove `adapt_legacy_firmware` and the schema-less dispatch branch from invocation adaptation.
2. Remove the legacy firmware loader and its route selection from the lane controller.
3. Remove legacy-only discovery, status, safeguard, and release-check behavior.
4. Delete the legacy invocation example and the dual-path example.
5. Rewrite README, quick-start, specification, overview, and relevant test language so they describe
   the canonical coding invocation as the sole supported route.
6. Delete obsolete legacy-only tests and fixtures.
7. Preserve or relocate provider-neutral assertions from mixed legacy tests when they still protect
   canonical parsing, controller lifecycle, provider construction, resource leasing, or cleanup.
8. Do not add a special `legacy firmware input rejected` compatibility branch. With the adapter
   gone, old-shaped input must fail through ordinary canonical validation like any other invalid
   invocation.

### Producer proof

Before returning, the implementer must inspect the combined MI-01/MI-02 diff and run the smallest
focused checks covering invocation parsing, controller route selection, documentation/examples, and
preserved mixed-test behavior. The handoff must identify:

- the exact legacy branches, examples, tests, and documentation removed;
- every provider-neutral assertion preserved or relocated;
- the ordinary canonical-validation result for representative old-shaped input;
- the exact focused checks and their outcomes; and
- the frozen candidate revision and worktree status.

### ROOT checkpoint

ROOT reviews MI-02 and the combined diff before freezing the candidate for MI-03. Acceptance
requires:

- one canonical lane-management route remains;
- no loader or controller branch can select the legacy format;
- no compatibility promise, example, fixture, dead import, or release rule remains;
- invalid old-shaped input is handled by normal canonical validation; and
- canonical providers, generic resource leasing, and shared lifecycle code were not semantically
  changed beyond what removal requires.

A material issue returns to MI-02 under one complete correction card. If review exposes a direct-
capability omission owned by MI-01, ROOT routes it back to MI-01 instead.

## MI-03 — Verify the remaining general-purpose harness

### Frozen input

ROOT records the candidate revision and runs verification against those exact bytes. Product edits
invalidate the affected checks and require a newly recorded frozen revision. Unchanged passing units
may be reused when their source, tests, configuration, and environment are unchanged.

### Required review and checks

ROOT must:

1. Review the complete diff for accidental changes to provider construction, canonical invocation
   semantics, resource claims, worker lifecycle, or cleanup.
2. Search source, tests, examples, package exports, and documentation for every removed symbol and
   legacy-route phrase. A remaining reference must be removed or explicitly shown to be historical
   material outside the v2 runner.
3. Run the repository's change-aware Ruff, BasedPyright, compilation, and focused test gate under
   `BOUNDED-TEST-v1` where applicable.
4. Run focused deterministic tests covering:
   - canonical invocation parsing and controller lifecycle;
   - Codex, Claude, and Qwen provider construction and result handling;
   - `exclusive_resources` acquisition, contention, release, and cleanup;
   - hooks, super-cache, events, resume, and controller cleanup affected by the removal; and
   - packaging, release checks, documentation/examples, and public imports affected by the removal.
5. Confirm `firmware-v1.5-harness-runner` remains unchanged and recoverable.

### Bounded execution

Every covered command must run through `.codex/scripts/Invoke-BoundedTest.ps1` as required by
`BOUNDED-TEST-v1`. Each invocation must have a unique task-specific result path, a heartbeat no
longer than 60 seconds, and a maximum lifetime based on measured history or a stated protocol bound
plus policy-capped cleanup.

Do not retry an unchanged supervisor failure. First classify whether the fault is:

- a product failure that invalidates a required criterion;
- a strict test-only defect whose correction preserves the scenario and oracle; or
- a supervisor, environment, reporting, or other support failure that blocks only the evidence it
  prevented.

Continue independent feasible check units after a failure so ROOT receives the complete useful
result pool. Store receipts beneath a unique root under
`.codex/runtime/bounded-tests/legacy-bulk-removal/`.

### Acceptance gate

ROOT issues exactly one result for the frozen candidate:

- `ACCEPTED`: every required criterion is decided and satisfied;
- `CONTINUE`: a required criterion failed or is genuinely undecidable, with one complete repair
  contract routed to MI-01 or MI-02; or
- `INCOMPLETE`: safe evidence cannot decide a required criterion and no bounded repair or changed-
  condition continuation is available.

Test or support failures do not automatically become product defects. They invalidate only the
claims that depend on their missing or unsound evidence. No product tolerance is preauthorized.

## Integration and retirement

Only after `ACCEPTED` and separate ROOT authorization may ROOT integrate the candidate. Integration
must:

1. Reconfirm the accepted revision, clean destination, current destination tip, and remote state.
2. Record the rollback base.
3. Advance the v2 destination only by conflict-free fast-forward to the accepted revision.
4. Stop without resolving content if the destination changed or the operation is not a clean
   fast-forward.
5. Push without force and read back exact local/remote revision equality.
6. Confirm v1.5 remains unchanged.
7. Retain the accepted revision and verification receipts, then retire only the clean, terminal,
   unclaimed cleanup worktree.

A push, readback, or retirement failure blocks only that operation. It does not invalidate accepted
product evidence unless source bytes changed.

## Done when

- MI-01 through MI-03 pass and ROOT records `ACCEPTED`.
- V2 contains neither the legacy schema-less firmware lane nor the direct capability/adapter stack.
- Repository search finds no v2 runtime, public API, packaging, example, test, or documentation
  reference to the removed routes.
- Generic `exclusive_resources` remains fully tested and provider-neutral.
- Canonical Codex, Claude, and Qwen lanes remain green.
- Hooks, super-cache, events, resume, packaging, public imports, and cleanup affected by the removal
  remain green.
- The accepted revision is fast-forwarded, pushed, and read back exactly.
- V1.5 remains unchanged and recoverable as the historical implementation.

## Completion record

- MI-01 removed the direct capability broker, campaign pack, adapter, exports, packaging entries,
  dedicated tests, and documentation.
- MI-02 removed the schema-less firmware adapter/controller route and its examples while retaining
  the canonical schema, the coding-v1 input adapter, generic resource claims, and external firmware
  MCP isolation boundaries.
- MI-03 passed changed-file Ruff, BasedPyright, and compilation at
  `.codex/runtime/bounded-tests/legacy-bulk-removal/mi03/root-static-004.json`. The focused surface
  pool passed 120 tests plus 75 subtests; the core pool passed 149 tests plus 28 subtests. The three
  unchanged baseline assertions described above remain classified outside this removal.
- Final search found no removed symbol, module, adapter, legacy example, or public export.
- ROOT fast-forwarded and read back `origin/working/firmware/v2-candidate` at `09e5786` without
  changing the v1.5 branch.
