## Diagnosis

  The experiment was invalid for the main question because the watcher subagent woke the manager. Production will not have that relay.

  ## Confirmed problems

  - Some requests took a long time to reach the manager.
  - The manager was sometimes busy and responded late.
  - Wake-source timestamps are inconsistent, so we cannot reliably identify what woke the manager.

  ## Potential problems

  - The harness may be unable to wake an idle orchestrator.
  - Workers may wait indefinitely until the orchestrator receives another turn.
  - A busy orchestrator may respond too slowly as the agent count increases.

  ## Implementation gaps

  - No confirmed production wake mechanism.

  ## What to test

  Run new sprints where:

  1. The watcher subagent only observes.
  2. The orchestrator enters a real idle/wait state.
  3. A worker raises a blocking request through the production harness.
  4. Measure whether the orchestrator wakes, how it wakes, and how long it takes.
  5. Repeat while the orchestrator is busy.

  ## How to fix it

  - If the harness wakes the manager reliably: keep the persistent manager.
  - If it cannot: add a host-side wake bridge, likely using codex exec.