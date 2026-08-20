# Root repair plan after M5 S1 reset

## Disposition-driving defects

The root accepts all three post-sprint findings because they invalidate required M5 evidence. The
epoch is preserved unchanged and does not count.

1. `validate_sprint_finalize` treats every harness acknowledgement telemetry baseline as a required
   complete manager baseline. Require complete invocation boundaries, require at least one complete
   formal baseline, and require complete formal baselines after activation and each formal review.
   Incomplete harness telemetry must neither poison nor satisfy these manager-owned gates.
2. Diagnostic analysis still requires the forbidden legacy watcher-to-manager collaboration relay.
   Treat a complete, identity-consistent production blocking wake chain as the manager-availability
   and healthy-response path. Retain the legacy relay path only for historical/evaluator-enabled
   runs; do not fabricate availability when either path is incomplete.
3. Render `deadline_lateness_seconds` from the correlated manager response and response deadline:
   `max(0, response_timestamp - deadline)`. Preserve positive causal lateness from earlier failed
   stages when that is the classification-driving value.

## Implementation and verification

The persistent Terra-medium coder will make the smallest code and focused-test changes. The
independent Terra-medium reviewer will review the resulting diff and tests. The root will adjudicate
all findings. Luna-high will then run a real host-only practical smoke covering the combined durable
timeline, diagnostic-only production wake classification, deadline rendering, and exact process
cleanup. Finally run the full harness/watcher suites, Pyright, compileall, and M4 readiness. Any
accepted change to the counted surface resets the sequence to 0/3 before a fresh sprint.

## Explicit exclusions

- Do not rewrite or repair this epoch's historical evidence.
- Do not rename schemas or remove legacy relay support.
- Do not infer idle/busy state without explicit interval evidence.
- Do not change firmware, server, hardware, worker, lease, or suite policy behavior.
