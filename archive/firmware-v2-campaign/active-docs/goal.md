# Fast_Lane_V2 rule:

> **Closed 2026-08-21.** The firmware-enabled WIP harness has been published and the Plan 2
> campaign is over. This document is historical context only and must not authorize another lane,
> sprint, repair, or promotion. See [`HANDOFF.md`](../HANDOFF.md) and
> [`final_v2-firmware_harness_overview.md`](../firmware-v2-harness-runner/final_v2-firmware_harness_overview.md).

  Specifically use fast-lane-v2 for small scoped edits. Never use
  the full heavy edit loop unless you deem it absolutely necessary. Always re-evaluate whether every change batch belongs to fast-lane-v2 or the heavy fix + gate set. Most things will belong to fast_lane_v2. Do not
  reuse prior rules (this other edit needed the full gate, so this one does too) for current edits - always re-evaluate whether the current edit can use fast-lane-v2 or the heavyweight fix loop.

# Current ROOT-IM Execution Directive

## Current status (operative)

`plans/general-coding-harness/FULL-EXECUTION-SPEC_PLAN_2.md` v3.9.25 is the sole
current execution contract. Generic release plus M08 connection-readiness credit is retained from
the accepted `055a5bd137039eaa1917e4a859a3d5bf30eb6444` boundary. ROOT-IM reconciled its accepted
descendant through the empty final review 062, proof 063, and integration/readback 064. The clean
detached target and `firmware/v2-candidate` now point at the bound repair base
`dd673cb304501bfc2228b8c44f41df45a0c8608f`, tree
`c18ccd0bc88de9c8fae1f98652a12fb5c1a951ae`. The checkpointed safeguard finished
with all 16 units at PASS while preserving unaffected credit, its cleanup passed,
and the fresh Terra final review returned PASS with no findings.

The run is authorized to resume at the Firmware sprint with a fresh live manager. The accepted
target launched the then-mapped acceptance orchestrator and cleaned it up,
and an independent raw MCP initialization/list exchange exactly matched the 39-name
production registration without hardware or tool side effects. The provider itself
returned an empty catalog because Codex 0.147.0 forcibly defers custom MCP definitions
from initial model context. Plan v3.9.25 preserves the prohibition on every provider
tool invocation and used target/server protocol evidence instead. Attempt 053 passed:
the accepted static/raw 39-name comparison remained the catalog oracle, the accepted
target recorded `ListToolsRequest`, the provider returned only the exact alias plus
`connection_ready`, finite watch and the passive owner-bound watcher completed, and all
identified processes and disposable roots cleaned up. Preserve all M07 and M08 credit. No
continuation product repair, verification asset, or affected M07/M08 repetition is required before
live work; the accepted target is the Firmware sprint input.

The user authorized the declared fixture and requires three consecutive completed, accepted,
predeclared catalog logical sprints with no WIP target-v2 harness error before promotion. Logical
sprints are stable across replaceable manager epochs and provider invocations. The test orchestrator
owns every logical lane and sprint through completion, recovers or replaces affected provider
invocations without terminating the logical lane, and keeps every feasible lane
continues until the sprint publishes `COMPLETED_CLEAN` or `COMPLETED_WITH_FINDINGS`. A sprint in
which a harness error occurred completes and pools all findings before ROOT review/repair; it earns
no clean credit and resets the indexed clean streak. Confirmed harness repairs occur between
completed sprints, never during one. The project-local Qwen Code/Ollama
provider route in `Firmware/.qwen/settings.json` passed its no-hardware smokes for DeepSeek and
Qwen 397B; its Firmware-owned external target-provider bridge passed its target-lane MCP smoke.
Codex is not an admitted Firmware route. A Firmware MCP-server
defect and firmware/specification/fixture/doer errors are suite-owned: they are repaired/retested
inside the same logical sprint and do not reset confirmed clean credit, but that sprint does not
count until it reaches an accepted completed result.

The first live A21 attempt (`A21_20260815-plan2-a21-001`) is terminal
`INCOMPLETE_NOT_PASSED`, with the streak still `0/3`. STM-A was electronically validated, but STM-B
was absent; the server refused the only attempted flash before writing because the firmware's
initial stack pointer was outside verified writable RAM. The doer corrected the linker RAM extent
and rebuilt before the attempt was stopped. No device mutation or `RESULT.json` occurred, and the
manager, watcher, provider tree, and lease were retired. Do not reuse that attempt's runtime
authority; its verified semantic checkpoints may continue under a correlated handoff and fresh
authority. STM-B is now
electronically present on COM17. Retry `A21_20260816-plan2-a21-002` reached a sealed,
Qwen-approved `SPEC_REVIEWED` checkpoint and stopped before doer launch or hardware because normal
watcher start exposed the unnecessary Windows Job Object breakaway flag. The mapped coder, reviewer,
test executor, and integration executor repaired and proved that path at `055a5bd`. Suites 003-008
then exposed the workflow defect: ROOT terminalized recoverable lane/runtime interruptions instead
of allowing the test orchestrator to finish the logical sprint. Launch the prepared fresh manager,
carry verified durable suite-008 checkpoints through its handoff, issue new authority for every live
action, and continue the current logical sprint. During execution the test orchestrator records each
possible harness error as a suspected finding with evidence, affected lane/unit, observed and
expected behavior, containment, continuation, and cleanup facts; ROOT does not intervene or diagnose
mid-sprint. After completion ROOT reviews the full pool, authorizes only justified repairs, resets
the streak only for a confirmed harness defect, and continues until three consecutive completed
accepted sprints receive a harness-clean ROOT verdict (`3/3`), then promotes.

`HANDOFF.md` is the concise resume record. The detailed notes below are historical
context only; they do not create a live edge, alter the pause, or override Plan 2.


# User Goal and Explicit Hardware Authority

## User Provided Instructions: Instructions, Passing Criteria, and Blocking Handling:

#### Instructions:

Use `HANDOFF.md` as guidance. `stable-general-harness-runner` is the fixed
lane/session launcher for the multi-agent coding workflow.
`C:\Users\Jason\Documents\Jason\Orchestrator_Harness\plans\general-coding-harness\FULL-EXECUTION-SPEC_PLAN_2.md`
is the authoritative workflow and plan; its current pause, successor edge, and
hardware boundary are defined by its current version.
Launch each implementation or review
provider session through the fixed stable runner using its exact adjustable
assignment from the operative role mapping. `MI-FIRMWARE-HOST-READINESS` is the
declared exception because the accepted WIP target launcher is the object being
tested: ROOT-IM resolves its `acceptance-orchestrator` role from the same mapping,
materializes the resolved settings into a canonical target invocation, then the
accepted target launches that disposable provider session. Concrete child
launch settings must not be duplicated or hardcoded elsewhere; changing one role
entry controls all later projections and dispatch checks for that role without code
changes. All subagent task
completions and returns must summarize their work and return to ROOT-IM for
review before a consuming edge advances. ROOT-IM is the authoritative master
orchestrator and does not substitute for delegated workflow roles. If the plan
selects a full-harness testing orchestrator, it only orchestrates its own test
subagents and does not perform ROOT-IM's coordination, adjudication, or
integration duties.

M08 and the current route's target-lane smoke are accepted. MI-FIRMWARE-SPRINT resumes directly at
the unfinished logical Firmware sprint. The test orchestrator owns lane recovery and sprint
completion across replaceable provider invocations; ROOT does not terminalize or repair the sprint
mid-run. Harness repair begins only after the sprint completes and seals its full pool, and the next
sprint uses the repaired harness. One manager invocation may host multiple predeclared indexed
logical sprints and launches every eligible nonconflicting lane. Each live action still requires the
server's plan, ordinary permission, fresh lease, and confirmed identity. ROOT reaches promotion only
after `3/3` consecutive indexed completed accepted no-harness-error passes.

#### Passing Critera:

Passing criteria is that the entire plan is successfully implemented and tested, and the product is finished with all features specified by the spec plan, nothing skipped.

#### Blocking:

For anything that blocks you or any subagents, you may do whatever possible to unblock them. This blanket statement is not just a blanket; it applies to every single blocking case. If you are currently blocked, it applies to this case too.

## User outcome

Build the active candidate into a small, general, cross-provider multi-agent coding harness. It
must make custom workflows easy to declare and enforce, improve multi-agent coordination and
correctness, and remove recurring runtime and process waste. Hardware support must remain an
optional capability adapter and campaign pack, not the shape of the core.

The finished product must use a small, truthful, registered provider-adapter layer: it ships Codex
and Claude Code adapters, and an operator can add and select another agent CLI by supplying its
adapter rather than editing the generic workflow, task, event, supervision, or cleanup core. An
adapter must report its real capabilities and provenance. Keep coder-main's provider session by
default through every correction in one unaccepted candidate gate, then retire it when that gate
accepts or the logical task otherwise terminates. Keep each named Firmware doer session available
across completed sprints when possible. These are reuse preferences, never prerequisites: if a
provider cannot resume or the user changes the subagent/provider allocation, use a structured
handoff for the same logical workflow role without blocking a ready edge, terminating a sprint,
fabricating continuity, or reopening accepted work.

For Plan 2 `doer-main` and the named Firmware doers Atlas through Nova, retain the unchanged
DeepSeek route through the first two consecutive eligible backend-connection failures. After the
third consecutive `HTTP_429`, `HTTP_303`, `RATE_LIMIT`, or `BACKEND_ERROR`, use a structured handoff
to a fresh `luna-high` replacement while preserving the same logical role, task card, verified
checkpoints, evidence, and first unresolved action. The provider replacement must not block a ready
edge or terminalize a sprint.

Keep the existing general coding harness working and preserve schema-less, policy-bound firmware
compatibility. Do not add a scheduler, shared-memory database, second workflow engine, dashboard,
or universal hardware framework for this phase.

## Authority rule

`plans/general-coding-harness/FULL-EXECUTION-SPEC_PLAN_2.md` is the sole operative product,
execution, readiness, and acceptance specification. It defines roles and the model-mapping
boundary, workflow, gates, tests, hardware-authority enforcement, physical acceptance, and
promotion rules; concrete launch settings remain in the sole role-model mapping.

This file supplies only this user outcome and the explicit hardware scope below. A later direct user
instruction prevails, but ROOT must record it in the full execution plan and classify affected work
before execution continues. `HANDOFF.md` supplies current status and the next safe action.

## 11. Hardware authorization and safety

I authorize ordinary setup, application flashing, reset, debug, memory/register inspection, UART,
BLE, and bounded legal-band low-power 915 MHz LoRa work on the four named fixtures—STM-A, STM-B,
NRF-A, and NRF-B—only within the following complete user-issued scope. The canonical hash is the
SHA-256 of UTF-8 JSON serialized with keys sorted, no insignificant whitespace, and no ASCII
escaping. The selected `MI-FIRMWARE-SPRINT` suite workflow may use the parsed object only after its
current-plan admission conditions and fresh fixture confirmation are satisfied; no agent may infer
another action or widen a bound.

`USER_HARDWARE_AUTHORIZATION_V1`:

```json
{
  "allowed_action_classes": [
    "probe_discovery_read",
    "connect_setup",
    "application_flash",
    "reset",
    "debug_halt_resume",
    "memory_register_read",
    "uart_session_io",
    "ble_gatt_test",
    "lora_ping_pong_test"
  ],
  "expires_at_utc": null,
  "fixtures": ["STM-A", "STM-B", "NRF-A", "NRF-B"],
  "limits": {
    "application_flash": {
      "application_regions_only": true,
      "allow_bootloader_replace": false,
      "allow_mass_erase": false,
      "allow_protection_change": false,
      "allow_target_unlock": false
    },
    "ble": {"max_tx_power_dbm": 0},
    "lora": {
      "bandwidth_hz": 125000,
      "center_frequency_hz": 915000000,
      "coding_rate_denominator": 5,
      "max_campaign_minutes": 30,
      "max_payload_bytes": 64,
      "max_tx_airtime_ms_per_60s": 6000,
      "max_tx_power_dbm": 10,
      "spreading_factor_max": 10,
      "spreading_factor_min": 7
    },
    "uart": {"max_write_bytes_per_call": 256}
  },
  "prohibited_action_classes": [
    "bootloader_replace",
    "mass_erase",
    "protection_change",
    "target_unlock",
    "destructive_recovery"
  ],
  "schema_version": "user-hardware-authorization-v1"
}
```

These are maxima, not entitlements: the full plan's locked policy, live fixture evidence, and MCP
permissions may narrow or deny them. I do not authorize bootloader replacement, target unlock, mass
erase, protection changes, or destructive recovery. If any becomes necessary, preserve evidence and
request separate user authority.

The user is the sole issuer of hardware authority through this Section 11 or a later explicit user
directive. No agent may create, expand, or extend this authority.
