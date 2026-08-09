# M5 Q1 harness scan-latency repair plan

## Verified defect

In epoch `20260802-m5-q1-115933Z`, Delta created a genuine blocked HELP request before root entered the native blocking wait. The harness did not observe it until after its 90-second delivery deadline. A post-sprint `scan --no-write` took 43.2 seconds. `cProfile` attributed 35.7 seconds to two separate recursive `workspace.rglob("*.json")` traversals per run in `discover_run`, producing 217,585 directory scans across the four real workspaces.

The Q1 sprint is `HARNESS_BUG` and does not count. The deterministic watcher correctly failed the four causal rows because root recorded each wake-bearing `MANAGER_WAIT_FINISHED` under `native-wait-*` instead of the returned signal ID and linked claims to the wake record instead of the wait-finish record. Reject the post-sprint reviewer's watcher-bug recommendation: this is a root procedure error, not a watcher correlation defect.

## Smallest repair

1. In `orchestrator_harness/discovery.py`, enumerate recursive JSON candidates once per workspace and classify the same candidates into helper-process and MCP-process record sets. Preserve current path ordering, stable-read behavior, error codes, and arbitrary nesting support.
2. Add focused unit coverage proving one recursive traversal supplies both record classes and preserves independent helper/MCP parse errors.
3. Do not add caching, a background index, a runner, a wrapper, a relay, a new config knob, or any M5-specific path shortcut.
4. Run the focused discovery tests, full harness suite, compile/type checks, and a practical scan against the same four retained real run roots. Compare the practical elapsed time to the 43.2-second reproducer and require a material reduction adequate for the 90-second delivery target.
5. Independently review, adjudicate findings, then have Luna run the practical smoke. Rebaseline the Python surface and restart the comparable sprint count at 0/3.

## Next-sprint procedure correction (no code change)

For a successful native wake, record `MANAGER_WAIT_FINISHED` with the returned **signal ID** as `event_id`, the original wait `activity_id`, and the returned wake ID/transport. Link `MANAGER_EVENT_CLAIMED.continuous_from_record_id` to the successful wait-finish record ID. Only a timeout retains the synthetic `native-wait-*` event ID.

## Practical smoke result and accepted follow-up

The first one-`Path.rglob` implementation passed 74 focused tests and independent review, but the real four-root practical scan was not robust: one run took 80.111 seconds and a profiled run took 34.314 seconds, with 25.568 seconds still spent in the single pathlib recursive traversal across about 54,000 directories. Root accepts this smoke failure because it leaves too little margin under the 90-second delivery target. The same coder must replace that traversal with the smallest faster single recursive walk that preserves arbitrary nesting and semantics, without caching, indexing, configuration, wrappers, or run-specific pruning.
