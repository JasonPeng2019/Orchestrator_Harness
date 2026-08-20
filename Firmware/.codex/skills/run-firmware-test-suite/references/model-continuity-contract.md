# Test-agent model and continuity contract

The [Firmware provider-adapter contract](../../../../PROVIDER_ADAPTER.md) is the sole authority
for the logical provider/model/effort/tier/route allocation and current adapter status. This file
defines only session continuity and replacement rules.

## Default for named lanes

- Create each named doer only when its first assigned task becomes eligible. Resume that same
  named session for later roster tasks, including Nova/A23. Q40 is manager-owned corpus
  aggregation, not another base-application doer.
- Do not start a live sprint while the adapter remains pending. A later provider-route choice must
  preserve the named doer, model, evidence boundary, and task continuity.
- A doer runs one task at a time. Resume its recorded thread for routine firmware iteration,
  evidence repair, manager-controlled parallel checkpoint/resume, server-repair retest, and then its
  next roster task after the current task is terminal or at a manager-recorded handoff. Preserve
  the contract's named-doer and sprint-reviewer allocation on every resume.
- At a task switch, give the new isolated run path and prompt explicitly. The doer must not read
  the previous task directory or carry firmware files, leases, permission, or unevidenced
  conclusions into the new task.
- Do not open disposable DeepSeek sessions for successive turns or later roster tasks of a healthy
  named lane doer.
- A test already in progress on another model is grandfathered. Continue its recorded session;
  do not restart or repeat verified work merely to conform to the new default.

For a manager-verified production-server defect, the test orchestrator creates the contract's
separate server-implementer and repair-test roles and reuses the owning sprint reviewer for
read-only repair-plan and terminal-evidence review. These server-repair roles are not named
firmware-doer sessions.

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

After a handoff, persist the new session exactly as before. Do not switch away from the contract's
designated model or create another same-model session unless another recorded necessity satisfies
this contract. A provider-route change still requires the same recorded necessity and handoff.

Record a necessary model handoff with:

```powershell
python .codex/skills/run-firmware-test-suite/scripts/fresh_test.py bind-agent <run-dir> `
  --agent-id <new-agent-id> --task-name <new-task-name> --model <new-model> `
  --necessary-model-change --replacement-reason "<concrete necessity>" `
  --continuity-note "<last verified state; evidence paths; exact remaining work>"
```

For an irrecoverable session where the model remains unchanged, use the same command without
`--necessary-model-change` and with `--session-unrecoverable`. A new test may start on a
non-designated model only when `--necessary-model-change` and `--replacement-reason` record why
the designated model is unavailable or incapable; there is no prior evidence boundary in that case.
