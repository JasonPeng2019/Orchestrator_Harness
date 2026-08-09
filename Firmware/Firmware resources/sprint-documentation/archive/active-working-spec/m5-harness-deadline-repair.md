# M5 Harness Delivery-Deadline Repair Plan

## Verified defect

M5 sprint `20260802-m5-s3-101953Z` proved that a blocked HELP signal can be observed before its
declared delivery deadline yet be delivered late while a native blocking wait is active.

The source signal carried `delivery_deadline_utc`, `agent_blocked`, and `attention_epoch_id`.
Discovery read the record, but reconciliation omitted those fields. Selection therefore saw only
the later response deadline and ranked routine `STALE_STATUS` work ahead of the blocked HELP signal.
The diagnostic watcher correctly reported the resulting 44.100780-second delivery breach.

## Intended behavior

1. Optional manager-signal delivery metadata is validated at discovery instead of silently
   accepting malformed values.
2. Valid `delivery_deadline_utc`, `agent_blocked`, and `attention_epoch_id` survive reconciliation
   and appear in the native manager event.
3. Harness attention records preserve the delivery deadline separately from the response deadline.
4. Pending-work snapshots use the delivery deadline as the response-by time for manager delivery
   when it exists, without inventing missing data.
5. A genuinely blocked HELP signal with a valid delivery deadline is selected ahead of routine
   stale-status work. This must not make non-blocking checkpoints or ordinary handoffs urgent.
6. Deferred-handoff admission retains the same fixed ordering facts, and exact acknowledgement and
   lifecycle behavior remain unchanged.

## Implementation slices

1. **Schema boundary:** extend manager-signal validation for optional `delivery_deadline_utc`
   (valid UTC and not before `created_utc`), `agent_blocked` (boolean), and `attention_epoch_id`
   (non-empty string). Preserve backward compatibility when the fields are absent.
2. **Propagation:** copy those valid fields into reconciled `manager_signals`; emit
   `delivery_deadline_utc` from `_attention_identity`; use it in pending metadata where applicable.
3. **Selection:** give only blocked HELP signals with a real delivery deadline the urgent manager
   attention rank needed to precede `STALE_STATUS`; retain deadline/identity ordering among equal
   ranks. Do not globally reorder unrelated event classes.
4. **Regression tests:** reproduce a pre-deadline blocked HELP signal competing with stale status
   and prove HELP is selected. Cover invalid optional metadata, field propagation, attention
   correlation, deferred selection, and backward-compatible signals without the new fields.
5. **Verification:** run focused harness tests, then the full harness suite. Do not change the
   deterministic watcher unless a separately verified defect appears.

## Constraints

- Modify only the native harness and its tests unless raw evidence proves another owner.
- Add no runner, wrapper, relay, retry controller, scheduler, notification subagent, or other
  assistance layer.
- Do not weaken process identity, exact acknowledgement, path safety, or fail-closed validation.
- Prefer the smallest explicit rule over a global priority-policy redesign.
- No hardware, provider, MCP, deploy, flash, commit, or push action is authorized.

## Review and completion

A persistent GPT-5.6-terra medium coder implements this plan. An independent GPT-5.6-terra medium
reviewer critiques the diff; root accepts or rejects each finding and returns only accepted issues
to the same coder. GPT-5.6-luna high then writes/runs the smallest practical smoke. Root runs full
affected checks and M4 readiness. Completion requires green checks, archived repair plan, a new
tested-surface fingerprint/policy baseline, a reset comparable count of `0/3`, and a handoff that
starts at the next fresh M5 sprint.
