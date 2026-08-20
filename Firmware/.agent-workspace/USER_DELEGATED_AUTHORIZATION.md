# Current delegated hardware authorization

## Current interpretation for the next Plan 2 invocation

Status: `USER_DELEGATION_RECORDED_EPOCH_AUTHORITY_STOPPED`

Recorded: `2026-08-20`

The user's four-board delegation remains the scope available to ROOT after Plan 2 exposes
`EDGE-011`. Suite-008 and every earlier epoch are stopped: none of their manager/provider sessions,
plans, permissions, leases, claims, validation stamps, or hardware authority is current or
reusable. A later manager invocation must be separately dispatched by ROOT and must create fresh
runtime identities and obtain the server's actual plan, ordinary permission, exact lease, and live
electronic identity before each action. This interpretation preserves the authorization below but
does not authorize work before `CHECK-SPRINT-CONTINUATION` and affected exact-target M08 pass.

## Suite-008 fresh authority

Status: `AUTHORIZED_FOR_20260816_PLAN2_SUITE_008`

Recorded: `2026-08-16T13:06:45Z`

The controlling user instruction for epoch `20260816-plan2-suite-008` explicitly authorizes all
four connected declared boards for this fresh parallel hardware continuation. Suite-007 is
terminal and supplies no live process, provider/reviewer session, MCP lifetime, server plan,
permission, lease, validation stamp, resource claim, or hardware authority. Suite-006's 22
fail-closed claim records remain historical evidence only.

Every hardware action remains limited to a newly populated BYO-Firmware-MCP plan, ordinary
permission, a fresh exact-resource lease acquired by the Suite-008 controller before provider
start, and reverified live electronic identity. The authorized fixture is STM-A/STM-B on the fixed
PB13/PB14 100 kHz I2C link and NRF-A/NRF-B on their fixed 915 MHz CoreSX1262 links. NRF-A is the
BLE-peripheral ingress plus LoRa bridge/transmitter; NRF-B serializes BLE-central stimulus and
LoRa-peer/response duties. Planned MCP debug-memory writes may be used as bounded I2C stimulus but
do not prove the separate UART parser.

Flashing may replace the current observational images only through the ordinary plan/permission
surface when fresh identity cannot establish the required artifact/role state. Rewiring, cable or
power changes, mass erase, unlock, protection changes, bootloader replacement, destructive
recovery, remote pushes, and reading or acting on ROOT's separate harness-evidence review remain
excluded. The target-clean streak starts this epoch at `0/3`.

## Suite-007 fresh authority

Status: `AUTHORIZED_FOR_20260816_PLAN2_SUITE_007`

Recorded: `2026-08-16T11:54:39Z`

The controlling user instruction for epoch `20260816-plan2-suite-007` explicitly authorizes all
four connected declared boards for this fresh parallel hardware continuation. Suite-006 is
terminal and supplies no live process, provider session, MCP lifetime, server plan, permission,
lease, validation stamp, resource claim, or hardware authority. Its 22 fail-closed A25 claim files
remain untouched in the Suite-006 runtime as historical evidence. Suite-007 uses a fresh canonical
resource-lock root authorized by ROOT.

Every live action remains limited to a newly populated server plan, ordinary permission, a fresh
exact-resource lease held before provider start, and reverified live electronic identity. The
authorized fixture is STM-A/STM-B on their fixed PB13/PB14 I2C link and NRF-A/NRF-B on their fixed
915 MHz CoreSX1262 links. NRF-A is the BLE-peripheral ingress plus LoRa bridge/transmitter; NRF-B
provides serialized BLE-central stimulus and LoRa peer/response duties. Host Bluetooth is excluded.
Flashing may overwrite the currently installed incomplete A21 images and the assigned Nordic test
images only through the ordinary plan/permission surface. Rewiring, cable or power changes, mass
erase, unlock, protection changes, bootloader replacement, destructive recovery, and reading or
acting on ROOT's separate harness-evidence review remain excluded.

## Suite-006 fresh authority

Status: `AUTHORIZED_FOR_20260816_PLAN2_SUITE_006`

Recorded: `2026-08-16T10:11:03Z`

The controlling user instruction for epoch `20260816-plan2-suite-006` explicitly authorizes all
four connected declared boards for this fresh fully claimed Plan 2 continuation. No suite-005
process, watcher, provider session, MCP lifetime, server plan, ordinary permission, validation
stamp, lease, resource claim, or live hardware authority is continued. Only validated sealed
specifications, firmware/source/build artifacts, reviewer continuity records, and board-free proof
whose inputs still match may be adopted.

Every live action remains limited to a newly populated server plan, ordinary permission, a fresh
exact-resource lease held by the fresh HIL controller before provider start, and reverified live
electronic identity. The authorized fixture is STM-A/STM-B on their fixed I2C link and NRF-A/NRF-B
on their fixed 915 MHz CoreSX1262 links, with NRF-B providing serialized BLE-central stimulus and
LoRa peer/response duties for A25. Host Bluetooth is excluded. Rewiring, cable or power changes,
mass erase, unlock, protection changes, bootloader replacement, and destructive recovery remain
excluded. This grant does not authorize reading ROOT's separate harness-evidence review or making
ROOT's target-clean streak classification.

## Suite-005 fresh authority

Status: `AUTHORIZED_FOR_20260816_PLAN2_SUITE_005`

Recorded: `2026-08-16T09:28:09Z`

The controlling user instruction for epoch `20260816-plan2-suite-005` explicitly authorizes all
four connected declared boards for the selected Plan 2 catalog work. This is fresh authority only:
no suite-004 controller, watcher, provider session, MCP lifetime, server plan, permission, lease,
validation stamp, resource claim, or process authority is continued. Suite-004's retained STM-A
claim remains untouched beneath its historical resource-lock root and is not current authority.

The accepted target is the clean detached `target-harness/` at commit
`dd673cb304501bfc2228b8c44f41df45a0c8608f`, tree
`c18ccd0bc88de9c8fae1f98652a12fb5c1a951ae`. Each live action remains limited to the selected
catalog case's fresh server-populated plan, ordinary permission, current exact-resource lease,
verified electronic identity, disclosed loss, and declared final state. Rewiring, power/cable
changes, mass erase, unlock, protection changes, bootloader replacement, and destructive recovery
are excluded. The grant does not authorize ROOT's separate Terra harness-evidence review or a
target-clean streak classification.

## Suite-004 fresh authority

Status: `AUTHORIZED_FOR_20260816_PLAN2_SUITE_004`

Recorded: `2026-08-16T07:18:26Z`

The controlling user instruction for epoch `20260816-plan2-suite-004` explicitly authorizes the declared connected four-board fixture and real hardware work within the package safety contract. It supplies fresh authority only: no suite-003 provider session, controller, lease, permission, MCP lifetime, watcher, process, or hardware authority is continued.

The accepted product target is the clean detached `target-harness/` at commit `dd673cb304501bfc2228b8c44f41df45a0c8608f`, tree `c18ccd0bc88de9c8fae1f98652a12fb5c1a951ae`. Authorized live actions remain limited to each selected catalog case's fresh server-populated plan, ordinary permission, exact fresh lease, reverified board identity, disclosed loss, and declared final state. Rewiring, cable or power changes, mass erase, unlock, protection changes, bootloader replacement, and destructive recovery are excluded.

This suite may run STM and Nordic HIL concurrently only under disjoint exact leases and may use all four boards for D34 only after its declared A21/nRF edges are green. This grant does not authorize ROOT's separate Terra harness-evidence review or target-clean streak classification.

Status: `AUTHORIZED_FOR_FRESH_PLAN_2_HARDWARE_SEQUENCE`

Recorded: `2026-08-15T15:48:27-07:00`

Authoritative user instruction:

> “you should have everything needed to set up the run to continue. ... instead of one
> successful sprint as the passing criteria, i want 3 passing sprints in a row with no
> WIP product target v2 product errors to pass. MCP server errors are fine ... you have
> explicit permission to continue the run on hardware”

The later instruction is also controlling: finish Plan 2 end-to-end and do not report completion
until three successful sprints reveal no WIP target-harness errors.

## Scope

- External run owner: `ROOT-IM`; the fresh epoch must record the exact Sol manager/provider-session
  identity before its first hardware action.
- Product under test: a fresh package-local `target-harness/` worktree at accepted WIP target-v2
  coordinate `1302d90b2e1439c6f7f66031821a8f452a159f78`.
- Fixture: the four user-owned boards named in `assigned_hardware_fixture.md`, with live stable
  electronic identity confirmed by the server before use: `STM-A`, `STM-B`, `NRF-A`, and `NRF-B`.
- Goal: three consecutive manager-selected, dependency-ready main-catalog sprints that each reach
  a terminal accepted, target-clean result. The first selection is `A21` (dual-STM I2C); later
  selections occur only after ROOT's terminal classification under Plan 2.

## Permitted operations and disclosed effects

The suite may perform only the selected catalog case's server-planned, permission-gated operations:
live discovery/setup/validation, build, flash, reset, halt/run, bounded serial/debug observation,
I2C traffic, and—only when a later selected case requires it—bounded nRF radio actions. Flashing
replaces the test firmware on an assigned board; reset/halt interrupts its current firmware; and
the suite creates disposable logs, artifacts, run roots, and server state under its declared paths.
Every actual action still requires the server's populated plan, ordinary permission, fresh lease,
and exact board identity. This authorization does not bypass any of those controls.

## Exclusions

- No physical rewiring, power changes, antenna changes, cable moves, board swaps, metering,
  photography, external instruments, or manual fixture manipulation.
- No operation on an unassigned or identity-mismatched target.
- No historical process, lease, provider session, checkpoint, or Q11 continuation.
- No promotion from one or two target-clean sprints; a verified WIP target-v2 product defect resets
  the target-clean streak to `0/3`. A BYO-Firmware-MCP defect follows the suite repair/retest route
  and does not itself count as a target-harness error.
