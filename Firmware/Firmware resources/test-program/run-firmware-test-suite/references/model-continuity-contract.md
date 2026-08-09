# Test-agent model and continuity contract

## Default for named lanes

- Create Atlas, Boreal, Cygnus, or Delta only when its first assigned task becomes eligible, using
  `gpt-5.6-luna` at high reasoning and `service_tier="default"` (regular tier). Resume that same
  named session for its later roster tasks.
- Start A23 once with a persistent Claude Sonnet 5 doer. Record the provider's exact model
  identifier, launcher, session identity, and supported settings; do not translate Codex
  reasoning/service-tier labels onto Claude. If Claude remains unavailable after one bounded retry
  window, record a necessary model change and continue A23 with one persistent `gpt-5.6-luna`
  high-reasoning regular/default fallback; do not let provider availability block the suite. Q40 is
  manager-owned corpus aggregation, not another base-application doer.
- A doer runs one task at a time. Resume its recorded thread for routine firmware iteration,
  evidence repair, harness-assisted parallel checkpoint/resume, server-repair retest, and then its
  next roster task after the current task is terminal or at a manager-recorded handoff. Preserve
  the regular/default service tier on every Luna resume. Terra reviewer and repair roles use high
  reasoning and the priority/Fast tier on every resume.
- At a task switch, give the new isolated run path and prompt explicitly. The doer must not read
  the previous task directory or carry firmware files, leases, permission, or unevidenced
  conclusions into the new task.
- Do not open disposable `gpt-5.6-luna` sessions for successive turns or later roster tasks of a healthy
  named lane doer.
- A test already in progress on another model is grandfathered. Continue its recorded session;
  do not restart or repeat verified work merely to conform to the new default.

## When replacement is allowed

Agent identity persistence is the default, not an end in itself. A replacement is allowed only
when one of these conditions is recorded:

1. **Necessary model change:** the current model is unavailable, unsupported by the active
   launcher, or demonstrably lacks a capability required to continue the sealed test.
2. **Irrecoverable session:** the recorded thread cannot be resumed after bounded recovery, so a
   new session is necessary. Prefer the same model when it remains usable.

A red test, slow progress, a manager-requested parallel pause, a repair barrier, a desire for a
fresh perspective, or ordinary context growth does not justify replacement or a model change.

## Handoff rules

Before replacement, persist:

- old agent ID, task name, and model;
- new agent ID, task name, and model;
- the concrete necessity;
- the last structurally verified result/state;
- the durable evidence and remaining-work boundary the new agent must resume.

The new agent reads the sealed spec and durable run state, preserves prior raw evidence, and resumes
only the remaining work. It does not redo already verified requirements solely because the model
or session changed. Requirements affected by a server repair, missing proof, or the reason for the
handoff still receive the targeted rerun required by the normal test gate.

After a handoff, persist the new session exactly as before. Do not switch away from the lane/test's
designated model (`gpt-5.6-luna`, or Claude Sonnet 5 for A23), or create another same-model session,
unless another recorded necessity satisfies this contract.

Record a necessary model handoff with:

```powershell
python .codex/skills/run-firmware-test-suite/scripts/fresh_test.py bind-agent <run-dir> `
  --agent-id <new-agent-id> --task-name <new-task-name> --model <new-model> `
  --necessary-model-change --replacement-reason "<concrete necessity>" `
  --continuity-note "<last verified state; evidence paths; exact remaining work>"
```

For an irrecoverable session where the model remains unchanged, use the same command without
`--necessary-model-change` and with `--session-unrecoverable`. Apart from the catalog-designated
A23 Claude Sonnet 5 assignment, a new test may start on a non-designated model only when
`--necessary-model-change` and `--replacement-reason` record why the designated model is
unavailable or incapable; there is no prior evidence boundary in that case.
