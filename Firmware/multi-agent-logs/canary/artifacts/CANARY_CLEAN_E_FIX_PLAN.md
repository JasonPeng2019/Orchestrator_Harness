# Clean-E canary repair plan

Authority: root manager  
Audit: `.agent-workspace/CANARY_AUDIT_20260731_S1_CLEAN_E.md`  
Verdict: `ACCEPTED_NONCOUNTING`; counter remains `0/3`

## Objective

Remove only the functional defects validated by the clean-E audit and prepare the three affected
run-local boundaries for a fresh epoch. Preserve every accepted experiment result and all closed
clean-E evidence. Do not edit production server code, broaden scheduler authority, invent a new
coordinator, or rerun hardware.

## Slice 1 — historical manager signals are retained but not actionable

Change `orchestrator_harness/notifications.py`, with focused tests under
`orchestrator_harness/tests/`.

- Keep historical manager-signal records in discovery, snapshots, and event history.
- A `MANAGER_SIGNAL` may enter active notification ordering only when its exact `lane_id` still has
  a live/unknown controller, helper, or MCP ownership domain, or when an exact matching live request
  still requires review.
- A signal for an exited/checkpointed historical lane must not become the pending notification of a
  fresh watcher epoch.
- Preserve notification of current live-lane HELP/FEEDBACK/INSTRUCTION signals and all higher
  priority request/safety conditions.
- Add regressions proving both sides. Do not add an epoch/config API merely to solve this case.

## Slice 2 — resolved transient STALE_STATUS does not reach Terra

Change `harness_watcher_implementation/poller.py` and its focused smoke tests.

- Before constructing evaluator-visible text, parse a changed JSONL delta by event identity.
- Suppress a `STALE_STATUS` record only when a later record in the same bounded observed delta
  proves that exact identity recovered (`CONTROLLER_ACTIVE` or a matching `CONDITION_CLEARED`).
- Retain the raw cursor/context and normal routing logs unchanged.
- Keep an unresolved/persistent `STALE_STATUS` visible and alertable.
- Add one resolved-transient regression and one persistent-stale control. Do not suppress other
  resource, request, lifetime, or process-identity defects.

## Slice 3 — D31 records each process role's actual creation time

Change only the run-local helper
`fresh-experiments/D31_20260726-062325/.agent-workspace/tools/d31_s1_rst01_request_helper.py`
and its focused routing tests.

- Populate `mcp_creation_time_utc` from the selected MCP/provider identity's existing
  `creation_time_utc` field, never the launcher start time and never a misspelled key.
- Preserve launcher identity separately.
- Add a focused regression with distinct launcher/provider times; no process or hardware launch.

## Slice 4 — A22 follows the live setup route before B14

Change only the current run-local adapter source
`fresh-experiments/A22_20260726-062324/.agent-workspace/tools/a22_stm_a_b14_s1_canary.py`
and focused host checks.

- Generate code that consumes the accepted live `setup_overview` route: copy its `load_call`, call
  the returned `board_setup-plan` initialization, populate only the server-requested setup facts
  from the recorded fixture/datasheet/authorization, and request the exact setup action. Keep the
  same helper/MCP lifetime alive while waiting boundedly for a hash/lane/lifetime-bound manager
  relay; execute only that returned setup action when relayed, then continue into B14. On timeout,
  checkpoint and cleanly close. Never publish a request and immediately return with a dead lifetime.
- Give the setup action and later B14 read plan distinct immutable request, sidecar, relay, and
  evidence paths. Never overwrite or reuse a consumed setup request/relay for the read boundary.
- Remove the obsolete unconditional `board_validate` / `connect` path for an unknown profile.
- Preserve live returned connection-ID selection, isolated roots, exact request binding, and all
  accepted B12/B15/B35/B36 evidence.
- Focused tests inspect/generated-code routing only; no MCP or hardware launch.

## Slice 5 — A24 validates and uses a real UV executable before lifetime creation

Add a small reusable run-local launcher preflight under
`fresh-experiments/A24_20260726-052146/.agent-workspace/tools/` with focused tests.

- Resolve UV from an explicit supplied path or `shutil.which("uv")`; require an existing regular
  executable before writing/starting a paired launcher.
- Render the resolved absolute executable into each fresh launcher.
- Fail during board-free preparation, before lifetime/registry creation, if resolution fails.
- Do not rewrite closed clean-E launcher/evidence files. The next epoch must generate new launchers
  using this preflight.

## Manager-procedure corrections (no harness code)

- Start the independent cadence alarm and confirm one successful scan before lane launch.
- Service or explicitly reject every exact request before its deadline.
- Stop a doer/controller promptly after its durable lease-gated checkpoint instead of waiting for
  `LANE_NO_PROGRESS`.
- Continue unrelated eligible lanes and preserve all passing evidence.

## Verification gate

Run only focused checks for the changed surfaces first:

1. primary notification tests covering historical-vs-live manager signals;
2. watcher smoke tests covering resolved-vs-persistent `STALE_STATUS`;
3. D31 routing/lifetime tests;
4. A22 generated-source/self tests;
5. A24 launcher-preflight tests.

Then run the complete existing primary-harness and optional-watcher host suites once because the
two core monitor surfaces changed. Do not run firmware, MCP, provider, or hardware tests. The next
fresh epoch is the practical validation.
