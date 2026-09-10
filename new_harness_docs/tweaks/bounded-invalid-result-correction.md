# Bounded controller correction for invalid worker results

## Status

Requested product behavior change. The current controller validates one result
after its provider exits and immediately records `result_invalid` when the
result is absent or invalid. This tweak replaces that immediate escalation with
bounded corrective retry.

## Goal

A provider's ordinary prose response is not a valid harness result. The
controller should not immediately hand that failure to ROOT when it can give
the provider a clear, structured correction request and let it repair its own
result.

## Required behavior

After each provider exit, the controller validates the lane's `RESULT.json`.

- If the result is valid, continue with the normal `review_pending` flow.
- If the result is missing or invalid, do **not** immediately publish
  `result_invalid` or release the lane to ROOT.
- Instead, start a corrective provider continuation in the same lane/worktree
  through the selected provider adapter's **native resume command**. The
  controller must pass the saved provider session ID to the adapter and request
  `resume=True`; the adapter, not generic controller code, builds that CLI's
  correct resume argument vector.
- Never replace a failed result with a fresh, context-less provider invocation.
  The corrective provider turn must retain the original conversation/session
  context through the CLI's native resume capability.
- Send a corrective prompt that says, in direct terms, that the prior response
  was not a valid proposed `result/v1` record and that the provider must write
  a valid `RESULT.json` matching the lane's current `lane_id` and `run_id`.
- The correction must include the required result shape and explicitly require
  a nonempty `summary`, a valid `PASS`/`FAIL`/`BLOCKED` outcome, an evidence
  list, completion timestamp, and correct content hash.
- Keep the controller and its existing exclusive lane leases alive across the
  correction attempts. Clean up each exited provider process boundary before
  starting the next provider attempt.

## Adapter-owned native resume requirement

The controller must stay provider-neutral. Each launcher binding already owns
the provider-specific command construction through
`build_argv(model, worktree, prompt_path, session_id, resume)`. Corrective
retry must call that binding with the saved `session_id` and `resume=True`.

The shipped Codex, Claude Code, and Qwen Code bindings must each generate their
own CLI-native resume form. A future/custom provider is supportable only when
its custom adapter implements and tests its CLI-native resume route and parser
for the returned session ID. The controller must never hard-code provider
resume flags or guess a provider's session format.

## Retry limit

Maintain a durable correction-attempt counter for the current lane run.

- The controller may send at most **five** corrective prompts after invalid or
  missing results.
- If another invalid/missing result would require a sixth correction prompt,
  stop retrying.
- At that point, prove cleanup of the final provider boundary, release leases
  only after cleanup is proven, and publish the lane state that causes the
  monitor to raise `provider_exited_no_result`.

In other words: the first five invalid exits are self-correction attempts; the
sixth invalid exit is treated as a non-progress/hang escalation for ROOT.

## Evidence and safety requirements

- Preserve a durable record of every attempt: provider command provenance,
  session ID if available, transcript/stderr paths, result-validation failure,
  corrective prompt, exit code, timestamps, and process-boundary cleanup.
- Never overwrite the original provider transcript. Use attempt-specific
  transcript/stderr records or an append-only attempt ledger.
- Never loop indefinitely.
- Do not use a different provider/model as an automatic fallback.
- If the provider did not emit a usable native session ID, or its selected
  adapter has no native resume implementation, the controller cannot perform a
  corrective retry. It must retain the evidence and take the terminal
  `provider_exited_no_result` escalation path rather than inventing a fresh
  conversation.
- Do not retry an actual provider-launch/authentication/process failure under
  this policy; those remain provider-start failures and must be reported
  honestly.
- Do not accept prose, a chat final answer, or an almost-correct file as a
  valid result.

## ROOT behavior after exhaustion

ROOT receives the ordinary managed `provider_exited_no_result` notification.
ROOT reads the durable attempt ledger and transcripts, acknowledges the event,
decides whether to retry through a new lane/resume path or change the task,
and closes the event only after handling it. The controller must not silently
continue after the limit.

## Required tests

1. Missing/invalid result on attempts one through five produces a corrective
   prompt and does not create `result_invalid` or `provider_exited_no_result`.
2. The corrective prompt contains the lane/run identity and the exact required
   `result/v1` fields.
3. A valid result on any corrective attempt enters the normal
   `review_pending` lifecycle.
4. The sixth invalid/missing result stops retries and produces exactly one
   `provider_exited_no_result` monitor event.
5. Every exited provider process boundary is proven gone before the next
   attempt, and the lane lease remains held until the final outcome.
6. Codex, Claude Code, and Qwen Code corrective attempts use their own
   adapter-built native resume commands with the saved session ID, and retain
   the original provider context.
7. A custom provider adapter is rejected or terminally escalated when it lacks
   a tested native resume implementation; generic controller fallback is not
   permitted.
8. A real provider integration test proves this behavior with a supported CLI
   in a disposable Git worktree.
9. Provider startup/authentication failures do not enter the correction loop.
