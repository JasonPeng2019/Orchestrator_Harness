# Attention readiness failure 004

Counter reset: `0/3`. R3 is noncounting. No provider, MCP server, board lease, or hardware action
started; all four host-prep controllers eventually exited and all exact service/controller/Codex
PIDs are absent.

Two independent logging failures occurred during the host-only counted candidate:

1. Atlas created a real blocking manager-signal, but its producer records used generated
   `event_id` values and only carried the stable `signal_id` as metadata. The producer and harness
   records therefore could not join. The fail-closed contract now rejects any supplied
   `signal_id` unless it exactly equals `event_id`; independent review returned CLEAR.
2. The primary managed harness exited with `attention record ID collision` while four controllers
   were active. Its owner recorded `watcher-exited`, but its runtime file remained stale-looking;
   optional/watcher-subagent reporting did not promptly prove the primary death. This destroyed
   continuous primary coverage and requires another Terra-medium collision/liveness repair plus
   independent review.

The collaboration challenge also failed procedurally: a nonblocking Boreal watcher message ended
the root's active wait before the exact Atlas blocking wake arrived. Future watcher-subagent
procedure now permits only the exact blocking wake or a critical service failure while that wait
is open.

R3 evidence is retained as falsification evidence only. The next candidate must use a fresh epoch,
correct producer correlation, exact primary liveness proof, and no manager write-scan against the
managed output root.
