# Attention readiness failure 001

Counter: `0/3`; no provider, MCP, lane controller, or hardware action was started.

Host-only exact-path probes confirmed three logging integration gaps before Sprint R:

1. A real Clean-Q `MANAGER_SIGNAL` has a human-stable `signal_id` that differs from the harness's
   hashed `event_id`; an agent source record cannot join the harness attention records by guessing.
2. The normal sequence `WAIT_STARTED -> deadline -> WAIT_FINISHED -> EVENT_CLAIMED` currently
   produces `INSUFFICIENT_EVIDENCE` / `complete explicit manager interval` even when claim follows
   wake by one second.
3. Adding a harness `attention-events.jsonl` source to the optional watcher makes an attention-only
   append count as an ordinary changed evaluator input (`evaluator calls = 1`), which can create an
   unnecessary Terra-evaluation loop at the attention scan cadence.

Accepted minimal repair, owned by the main manager:

- map `MANAGER_SIGNAL` attention correlation to its stable `signal_id` while retaining the ordinary
  harness event ID as provenance and use the signal deadline as `response_deadline_utc`;
- recognize a paired wait that spans the response deadline and is followed by exact-event claim
  within the sealed 10-second wake-to-claim bound;
- ingest harness attention files through the attention path but exclude them from the ordinary
  evaluator-change stream;
- add focused regression/integration tests and retain all default-off behavior.
