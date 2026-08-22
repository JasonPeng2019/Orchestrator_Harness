# HANDOFF

## Firmware target — closed

Closed by direct user decision on 2026-08-21. The working firmware-enabled WIP harness is
published at [`harness-single` / `working/firmware/v2-candidate`](https://github.com/JasonPeng2019/harness-single/tree/working/firmware/v2-candidate),
commit `cb5b568d5fc3f63a1fe037312894e9736a2f2db1`. The code baseline is
`5ab4b1f2f9170c3e57c35883bcb1ad22a2d04815`, tree
`17e67a7affd2d16e1b1104e1df3dec22bfa198eb`; `cb5b568` adds only the final closure docs.

The retained WIP checkout is a real submodule at that exact published commit:

- `firmware-v2-harness-runner`

The source overview is
[`firmware-v2-harness-runner/final_v2-firmware_harness_overview.md`](firmware-v2-harness-runner/final_v2-firmware_harness_overview.md).
It states the supported harness surface, firmware compatibility route, responsibilities that remain
with a manager/caller, and the limits of the closure.

## Truthful completion boundary

The harness source is delivered and no Firmware manager, provider, watcher, MCP, controller, or
hardware action remains live. Suite 14 was stopped for project closure and is not a clean result.
The historical three-clean-sprint tally ended at `0/3`; closure is a user delivery decision, not
fabricated test credit. Suite 8’s two target-harness defects were repaired; suites 9–13 found no
further confirmed target-harness defect.

All Plan 2 campaign material is preserved under
`archive/firmware-v2-campaign/general-coding-harness/`. It is completed/historical and must not be
used to restart Plan 2, a Firmware sprint, a repair, or promotion.

## Active compatibility follow-through

The compatibility testing plans, the restored `harness-single-worktrees/{compat-test,qwencode-test}`
worktrees, and the related Claude/Qwen feature documents under `active_docs/` remain active. Their
source changes have not yet been merged into `firmware-v2-harness-runner`. This is compatibility
integration work only; it does not reopen the closed Firmware hardware campaign.

## Cleanup and preserved history

Removed 79 inactive Git worktrees after confirming they were clean. At the user's subsequent
request, the three historical source worktrees `Firmware/target-harness` and
`harness-single-worktrees/{compat-test,qwencode-test}` were restored. The disposable
`claude-test` and `claude-probe-lanes/{lane-a,lane-b}` copies were also briefly restored for audit,
then removed as unnecessary historical-only scratch copies. A Windows path-length cleanup issue
was resolved with repository-local Git `core.longpaths=true`; no product source was changed.
Generated runtime/evidence directories remain as historical files. The retained
`.git/modules/harness-in-progress` directory keeps the local archive refs and display-checkout
stash recoverable and backs the three restored historical source worktrees.

`compat-test` and `qwencode-test` are restored from their local archive commits. The removed
Claude scratch copies are not a valid checkout or launch route; their historical evidence remains
under `plans/compatibility-testing/evidence/`.

Meaningful dirty material was retained locally before removal:

- `archive/compat-test-preclose-20260821` at `7a37c0a`
- `archive/qwencode-test-preclose-20260821` at `9e91618`
- `archive/pac-evidence-preclose-20260821` at `7adb3d0`
- the prior duplicate checkout is in the named local stash `archive user-display before firmware v2 closure 2026-08-21`

These archives are deliberately local and were not promoted into the delivered WIP branch.

## Current files and next action

This root repository retains pre-existing dirty state outside the closure documentation. The
closure edits and their supporting evidence are retained under `archive/firmware-v2-campaign/`.
No further Firmware command is authorized. Compatibility work remains authorized only within its
active plans and restored worktrees; any other future work should begin as a separately directed
project from the published WIP branch.

On 2026-08-21, the active submodule checkout was renamed from
`current-wip-harness-runner` to `firmware-v2-harness-runner`; its published commit remains
`cb5b568d5fc3f63a1fe037312894e9736a2f2db1`. The closed campaign plans, campaign-only Firmware
documents, session analysis, and V1 topology prompts were moved beneath `archive/`. The changed-code
gate then passed (Ruff, format, BasedPyright, compilation, and 58 targeted tests); its receipt is
`.codex/runtime/bounded-tests/archive-cleanup-verify-changed-002.json`. No full product test sweep
was run for this documentation/submodule/archive operation, and the WIP source code was not changed.

## Active Claude/Qwen runner integration

The authorized Claude/Qwen compatibility integration is in progress only in the isolated worktree
`.firmware-v2-harness-runner-worktrees/claude-qwen-parity-implementation`, branch
`compat/claude-qwen-runner-parity`, based on published commit `cb5b568`. The top-level
`firmware-v2-harness-runner` checkout remains untouched.

CP-01 (the selected Claude parity port) is currently assigned to the persistent
`PARITY_IMPLEMENTER` lane. Its task card, lane state, and output are contained beneath that
worktree's untracked `.agent-workspace/`; ROOT must inspect the terminal handoff and independently
validate its exact scoped changes before dispatching CP-02. The live integration plan is
`active_docs/claude_qwen_runner_integration_plan.md` and its role mapping is
`active_docs/SUBAGENT_ROLE_MODEL_MAPPING.json`.

At the current CP-01 checkpoint, the worker has staged the Claude runner port (provider behavior,
adapter/installer assets, examples, and focused tests) in that isolated worktree and is executing
its producer-owned bounded checks. This is implementation progress only: ROOT has not yet reviewed
or accepted the diff, and no Qwen checkpoint has been dispatched.

CP-01's producer proof then found one reproducible packaging defect: the imported Claude hook files
contain two extra trailing blank lines, so their canonical bytes no longer match the unchanged
manifest SHA-256 values; four installer tests fail closed as designed. ROOT independently confirmed
that the only difference from the reconciled Claude reference is those trailing lines. A repair turn
may remove only those lines, must prove the two canonical asset hashes equal the manifest entries,
then rerun the failed adapter/installer module before ROOT revalidates CP-01. No Qwen work is
authorized during this repair.

The exact CP-01 repair turn has been resumed in the same persistent `PARITY_IMPLEMENTER` thread
after its invocation identity/configuration was independently parsed. Its separate task card is
`parity-implementer-cp01-repair.md` under the isolated worktree's `.agent-workspace/`; its source
write contract is limited to removing those trailing blank lines. ROOT still owns review and the
decision to dispatch any subsequent checkpoint.

The hash repair and ROOT's four-module focused suite then passed (32 tests), but ROOT's changed-file
Ruff check found 24 mechanical violations in the ported/touched CP-01 Python files. The next and
final CP-01 repair is limited to resolving those named lint findings with no behavior change, then
proving the same static check and focused suite. Qwen work remains blocked until ROOT accepts that
evidence.

That final mechanical CP-01 lint repair is now running in the same persistent implementer thread,
after ROOT parsed its resume invocation. It has a disjoint task card
`parity-implementer-cp01-lint.md` and may edit only the explicitly listed CP-01 Python files to
remove the recorded Ruff violations; its required proof is a fresh Ruff result and focused-suite
result. ROOT has not accepted CP-01 or authorized CP-02.

The lint turn stopped on a single remaining exact Ruff finding:
`orchestrator_harness/lane_controller.py:1764` shadows the imported `dataclasses.field` with a
loop variable. Its bounded Ruff receipt is
`runtime/cp01-lint-results/20260822-cp01-ruff-01.json`. The next repair must rename only that loop
variable and its local uses, rerun the 14-path Ruff proof and the focused CP-01 suite, then return
to ROOT. No Qwen work is authorized.

That exact final one-variable correction has been launched in the same persistent implementer
thread after ROOT parsed its resume invocation. Its task card is
`parity-implementer-cp01-lint-final.md`; ROOT awaits its fresh Ruff and focused-suite receipts
before CP-01 acceptance or any Qwen dispatch.

The final lint turn then passed its 14-path Ruff proof and the 32-test CP-01 focused suite. ROOT's
next type/compile gate stopped before compilation with 77 BasedPyright diagnostics across the
ported Claude implementation and its focused tests; receipt:
`.codex/runtime/bounded-tests/claude-qwen-root-cp01-types-compile-001.json`. A same-scope
read-only classification run on the reconciled Claude reference reproduced the same 77 diagnostics
(`claude-qwen-root-cp01-reference-types-001.json`), so this is an inherited source-quality gap,
not a target-only regression. It remains blocking under the active rules: ROOT must give the
implementer an exact type-repair/no-behavior-change contract, then rerun the target type/compile
gate and focused suite before accepting CP-01. No Qwen checkpoint is authorized.

ROOT has now parsed and launched that exact type-only repair in the same persistent
`PARITY_IMPLEMENTER` thread. The task card is `parity-implementer-cp01-types.md`; it permits only
six named Claude source/test files, forbids baseline/config/suppression changes, and explicitly
preserves the already-correct installer loops. Invocation validation passed at
`.codex/runtime/bounded-tests/claude-qwen-root-cp01-type-invocation-001.json`; the lane-launch
receipt is `claude-qwen-root-cp01-type-launch-001.json`. ROOT awaits its bounded Ruff,
BasedPyright/compile, and focused-suite receipts before CP-01 acceptance or CP-02 dispatch.

That type-only turn passed its producer Ruff, type/compile, and focused-suite receipts, but ROOT's
post-turn semantic comparison found one remaining functional parity defect in
`claude_installer.py`: the source checks the three visible mojibake code points `ï»¿`, whereas the
reconciled Claude implementation checks one actual UTF-8 BOM character. The target would therefore
fail to reject a BOM-bearing packaged asset. CP-01 is still unaccepted. ROOT must dispatch one
line-only correction in the persistent implementer lane, prove that exact sentinel and rerun the
affected static/focused checks; CP-02 remains unauthorized.

ROOT has parsed and launched that final one-line BOM repair in the same persistent
`PARITY_IMPLEMENTER` thread. The only permitted source edit is the installer sentinel, expressed as
the unambiguous Python escape `"\ufeff"`; its separate task card forbids all other source, test,
asset, baseline, and Qwen changes. Invocation validation passed at
`claude-qwen-root-cp01-bom-invocation-001.json` and the lane launch at
`claude-qwen-root-cp01-bom-launch-001.json`. ROOT must independently inspect the corrected code
point and validate the resulting receipts before CP-01 acceptance or CP-02 dispatch.

CP-01 is accepted. ROOT verified the escaped sentinel evaluates to exactly U+FEFF, inspected the
worker's constrained six-file type repair and one-line BOM repair, and ran a fresh full 14-path
acceptance command: Ruff, BasedPyright, `py_compile`, and all four focused Claude modules passed
(32 tests), cleanup verified. The ROOT receipt is
`.codex/runtime/bounded-tests/claude-qwen-root-cp01-final-acceptance-001.json`. No Qwen source has
yet been changed; CP-02 may now be dispatched as the next separate, ROOT-owned checkpoint.

CP-02 is now running in the same persistent `PARITY_IMPLEMENTER` lane on the isolated runner
worktree. Its scope is native Qwen registration/argv/resume/transcript/cancellation behavior and
reject-loud invocation validation with deterministic focused tests only; Firmware bootstrap,
MCP/settings imports, and all Qwen host/installer/example/documentation surfaces remain expressly
deferred to CP-03. ROOT has not accepted any CP-02 source change or authorized CP-03.

CP-02 is accepted. The native built-in `qwen-code` provider now owns its `qwen exec` default,
stream-JSON start/resume argv, native transcript parsing, interrupt/exit-130 `CANCELLED` identity,
and reject-loud validation for unrepresentable fields. ROOT verified the scope contains no Firmware
bootstrap, MCP/settings import, or CP-03 host/installer surface and ran a fresh Ruff, BasedPyright,
compile, focused Qwen, and provider-registry acceptance gate; it passed with cleanup verified at
`.codex/runtime/bounded-tests/claude-qwen-root-cp02-final-acceptance-001.json`. CP-03 may now be
separately dispatched; no source has been integrated into the top-level runner checkout.

CP-03 has been dispatched to the same persistent implementer lane under a separate task card. It
may add only the Qwen runner-owned host adapter, owned project-local installer/assets, fixture,
example, public documentation, and deterministic sparse delivery/installer tests; it may not
import Firmware/MCP/settings material or run a real provider. The launch receipt is
`.codex/runtime/bounded-tests/claude-qwen-root-cp03-launch-001.json`. ROOT awaits the terminal
checkpoint evidence before final frozen-tip verification and integration.

ROOT review found one CP-03 Qwen configuration defect before acceptance: Qwen's `Stop` hook group
must be matcherless. The prior attempted repair dispatch used a new worker identity and was rejected
before a worker turn started; its temporary launcher/diagnostic artifacts were removed. The same
persistent implementer lane is now being resumed with its original `claude-qwen-parity-cp01-001`
identity for this one Qwen fragment/installer/test correction only. The top-level runner remains
untouched; ROOT must review the terminal receipt and rerun the scoped acceptance gate before CP-03
can be accepted.

CP-03 is accepted. ROOT inspected the three-file matcherless-Stop correction against Qwen's
documented event shape, verified no Qwen Firmware/MCP imports, and ran a fresh independent scoped
gate: Ruff, BasedPyright, compilation, and the Qwen adapter/provider/registry tests all passed with
cleanup verified at `.codex/runtime/bounded-tests/claude-qwen-root-cp03-final-acceptance-001.json`.
All CP-01 through CP-03 source remains only in the isolated compatibility worktree; ROOT may now
run final frozen-tip parity verification before deciding any integration action.

Final frozen-tip static parity verification passed after correcting one nonexistent asset path in
the check command (the first combined command did not run a product check). The fresh full scoped
Claude/Qwen/provider-registry Ruff, BasedPyright, compilation, and focused test gate passed with
cleanup verified at `.codex/runtime/bounded-tests/claude-qwen-root-final-frozen-tip-static-002.json`.
The repository-wide change-aware script cannot target this isolated runner worktree because it is
hard-wired to `stable-general-harness-runner`; no `VERIFY_CHANGED: PASS` claim is made. The next
authorized step is only the plan's disposable-provider readiness check.

The accepted frozen parity bytes were snapshotted locally as commit `2b9e9ec` on
`compat/claude-qwen-runner-parity` in the isolated runner worktree. This is not an integration into
the top-level runner checkout. The commit is the exact source coordinate for the two disposable
provider-lane readiness checks.

MI-READINESS created two disjoint disposable runner worktrees at commit `2b9e9ec` and recorded
no-prompt CLI readiness receipts for Claude and Qwen under
`.codex/runtime/bounded-tests/claude-qwen-parity/readiness-{claude,qwen}.json`; both passed with
cleanup verified. The first serial MI-LIVE attempt, Claude, also passed at
`.codex/runtime/bounded-tests/claude-qwen-parity/live-claude.json`: the integrated controller
started the real Claude CLI, observed a session and `COMPLETED` terminal outcome, and its disposable
doer created and committed the exact required `HELLO.txt`. The Qwen live lane is the one remaining
required live provider attempt; do not change runner source before it.

The first Qwen live attempt was interrupted by the outer execution timeout before its bounded
supervisor could emit a terminal receipt or controller status. No Qwen provider process remains and
no runner source changed. It is a provider-test support interruption, not a product result; a fresh
Qwen readiness record, unique disposable fixture root, lane/result identifiers, and one new
authorized attempt are required before any Qwen live claim.

The fresh Qwen live card was then corrected to remove the intentionally unsupported
`provider.allowed_tools` field; a read-only canonical parse accepted that corrected card. Its
subsequent detached controller attempt again produced neither controller status nor transcript and
timed out at the fixture's 240-second observation limit, while the bounded supervisor cleaned up.
This is a Qwen live-lane launch/support gap, not a static/provider-contract product finding: the
frozen branch's native-Qwen provider, installer, and focused tests remain accepted. Do not retry
this live lane without a separately repaired/observable stable launch path. Claude live integration
is complete; Qwen live proof is explicitly unfinished.

The accepted runner copy required by the direct request now exists at
`harness-single-worktrees/firmware-v2-harness-runner-parity`, on local branch
`integration/claude-qwen-runner-parity` at commit `2b9e9ec`. Its clean readback matches the
accepted isolated parity source. The top-level `firmware-v2-harness-runner` checkout remains
untouched at `cb5b568`.

ROOT subsequently diagnosed the apparent Qwen live-lane “support gap” as a deterministic
canonical-provider normalization defect, not an Ollama timeout: the canonical invocation's
mandatory `provider.id` and `provider.model` were retained in adapter-only `provider_options`.
The Qwen adapter then correctly rejected those generic keys before lifecycle admission or first
status publication. A read-only prelaunch diagnostic recorded the exact failure at
`.codex/runtime/bounded-tests/claude-qwen-parity/live-qwen-003-prelaunch-diagnostic-002.json`.
The persistent `PARITY_IMPLEMENTER` Luna lane is dispatched for only the parser-boundary
normalization and one deterministic regression test in the isolated implementation worktree;
ROOT will independently inspect, test, and accept or reject that repair before copying a revised
tip or authorizing another Qwen provider attempt. The top-level target and accepted durable copy
remain untouched.

ROOT accepted the resulting two-file repair at commit `9f38371` after a fresh scoped Ruff,
BasedPyright, compilation, and 31-test Qwen/provider/parser gate passed with cleanup verified at
`.codex/runtime/bounded-tests/claude-qwen-parity/qwen-provider-normalization-root-acceptance-001.json`.
The dedicated `harness-single-worktrees/firmware-v2-harness-runner-parity` copy was then
fast-forwarded to that same accepted commit; the top-level target was not changed. A read-only
replay of the formerly failing Qwen canonical card passed its parser/prelaunch/argv construction
at `.codex/runtime/bounded-tests/claude-qwen-parity/live-qwen-003-prelaunch-after-repair-001.json`.
The fresh real-Qwen fixture then passed at
`.codex/runtime/bounded-tests/claude-qwen-parity/live-qwen-004.json`: native `qwen exec` started,
reported a real provider session, exited `COMPLETED` with code 0, created and committed the exact
`HELLO_QWEN.txt` content, and the bounded supervisor verified cleanup. A final fresh Claude live
proof remains necessary on this new shared-parser commit before terminal acceptance.

Final terminal verification is complete. The fresh Claude proof at
`.codex/runtime/bounded-tests/claude-qwen-parity/live-claude-002.json` also passed on commit
`9f38371`: the real Claude CLI through its Ollama configuration reported a provider session,
`COMPLETED`/exit 0, and committed the exact `HELLO.txt` content. The equivalent Qwen proof is
`live-qwen-004.json` and records native `qwen exec`, a real session, `COMPLETED`/exit 0, and the
committed exact Qwen artifact. The dedicated durable copy is clean on
`integration/claude-qwen-runner-parity` at `9f383712438d57cfcd8aea6b85c7fb284c7ecf3a`; the isolated
implementation branch is at that same accepted commit. The top-level
`firmware-v2-harness-runner` checkout remains clean, detached, and exactly at the original
`cb5b568d5fc3f63a1fe037312894e9736a2f2db1`. The requested compatibility integration is therefore
complete without modifying the top-level target.

## Active super-cache repair

The current compatibility candidate at
`harness-single-worktrees/firmware-v2-harness-runner-parity` has a scoped super-cache repair in
progress, separate from the closed Firmware campaign.  It makes a completed prepared-worktree
receipt mandatory before provider launch; applies Codex hook trust only to prepared worktrees;
and runs the deployed cache Stop verifier at baseline and after provider cleanup, treating its
`{"continue":false}` response as a lane failure.  The checked-in `super-cache/` supplies the
15-second SessionStart/PreToolUse settings, the `^(Bash|shell_command)$` matcher, the 300-second
Stop setting, and a Stop script that discovers sibling-worktree virtual environments while
excluding harness output from its snapshot.

Focused static/controller/provider verification passed with cleanup verified at
`.codex/runtime/bounded-tests/super-cache/super-cache-focused-007.json` (55 tests).  A separate
fresh disposable prepared-lane proof passed at
`.codex/runtime/bounded-tests/super-cache/super-cache-real-stop-004.json`: a lane without a local
`.venv` discovered its sibling worktree tools and the deployed verifier passed both Ruff and
Pyright after a one-file Python change.  The deterministic controller tests cover the Codex,
Claude Code, and Qwen Code adapter paths for both orchestrator and subagent overlay roles.  The
verified source change is committed as `4ed577cb39bdb7330290496e5c0f6b29595a7210` (`Fix prepared
super-cache provider gates`).  On 2026-08-22, ROOT fast-forwarded the checked-out
`firmware-v2-harness-runner` to that commit and pushed it to
`origin/working/firmware/v2-candidate`; a post-push fetch confirmed local HEAD and the remote ref
match exactly.
