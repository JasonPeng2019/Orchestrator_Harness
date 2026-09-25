---
name: churn-watcher
description: Investigate repair churn and replace repeated symptom fixes with a verified root-cause correction. Call this skill whenever the same repair or acceptance target has taken 3 or more implementation, review, or correction tries, or when the user asks to investigate thrashing.
---

# Stop repair churn

Pause new correction launches for the affected target. Let useful in-flight
evidence collection finish, but do not accept, discard, or start another repair
until the investigation below is complete.

Use existing commits, diffs, test output, reviewer findings, and run state to
reconstruct the attempts. Keep the result in the agent's report; do not create a
new ledger or bespoke evidence artifact. For each attempt, identify:

- the behavior it tried to repair;
- the actual implementation mechanism it changed;
- the next reproduced failure and the path by which it escaped; and
- whether the criticism is a contract-required defect, reviewer overreach,
  administrative noise, or an unrelated failure.

Validate every material criticism against the governing specification and an
executable reproduction. Reject invalid or merely stylistic findings. Do not
turn a passing behavior into a failure because a report is imperfect.

Find the shared mechanism behind the valid failures. Inspect the complete but
bounded behavior space that matters to that mechanism, such as representation,
provenance or trust, state, ownership, and every real consumer or sink. Look for
duplicated predicates, inconsistent parsing, mismatched validation and
sanitation, or checks applied after irreversible work. Distinguish one root
cause from genuinely independent defects.

Choose the smallest architectural correction that closes the root cause across
the governed boundary. Prefer one shared policy or state transition over more
literal exceptions. Add a compact table-driven test matrix for the validated
failure classes and for behavior that must remain allowed. Do not broaden the
product policy, reopen accepted work, expand the harness, or add validation
unrelated to the reproduced failure chain.

Before resuming, report to the parent ROOT:

- the root cause and evidence;
- which prior findings were valid or invalid;
- why earlier repairs missed it;
- the consolidated correction and preservation boundary; and
- the focused and affected checks that will prove it.

Then run one correction and one fresh review. If the review finds another issue,
first determine whether the root-cause model was incomplete; do not immediately
add another one-off patch.
