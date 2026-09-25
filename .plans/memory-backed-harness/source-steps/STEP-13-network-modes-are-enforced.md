# STEP-13 - Network modes match actual enforcement

## Outcome

Requested and effective network profiles truthfully describe the actual launched worker and product service path, including a restricted-local path with no Atlas task call. This closes [BEHAVIOR-07](../specification/behaviors/BEHAVIOR-07-network-mode-claims-match-enforcement.md).

## Scope and touchpoints

Use `src/memory_harness/config.py` resolved configuration, Atlas/telemetry/publication service entrypoints, and provider/tool configuration in the STEP-12 installed payload. Do not describe a same-user process as a hardened sandbox.

## Implementation

Resolve `soft_guardrail_network`, `atlas_memory_only`, or `restricted_local` before an objective and retain requested/effective/enforcement-source state. Suppress supported provider-native general web/fetch/search tools in soft mode, while disclosing unsuppressed shell egress. Report Atlas-only only with independent unrelated-destination blocking and actual launched-payload verification; otherwise downgrade the claim. Restricted-local prevents Atlas retrieval, optional telemetry, publication retries, and other optional Atlas task-path work at service entry; safety administration that cannot run remains pending for an authorized environment. Distinguish outage from permission and enforce the Feature Section 15 off table independently.

## Dependencies and integration

Consumes STEP-12's installed payload and STEP-10's external-effect entrypoints. Produces effective mode/readiness facts for STEP-15 and a verified profile for STEP-17/18 fixtures.

## Requirement-fit validation

Show actual tool suppression and disclosed limits, Atlas-only downgrade without egress proof, zero restricted-local Atlas task calls including retries, and outage reporting without permission relabeling.

### Fast test suite

Extend `tests/local/contracts/test_config.py` with mode-resolution cases and add adapter/launch-payload tests that count actual forbidden calls and inspect installed tool settings. A local test can establish suppression logic; only measured egress enforcement permits an Atlas-only claim.

## Failure scope and recovery

Unverified egress limits the Atlas-only claim or affected task, not unrelated local work. An unsafe external retry remains pending; do not grant a task-path exception.

### Fast lane for revisiting old work

Repair the specific mode resolver, service gate, or installed tool setting; rerun its direct fast tests and STEP-15/17/18 only where the profile was consumed.
