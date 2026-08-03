# Simple Harness Development Flow

There are two copies of the harness:

- The **frozen harness** is the current version that already works.
- The **candidate harness** is the version being changed.

Only one of them should control agents at a time.

## While Writing the Changes

Use the frozen harness.

```text
frozen harness
  -> coding agent
  -> review agents
  -> test agents
```

The agents edit the candidate harness and test individual pieces of its code.

The candidate harness is only code being worked on. It does not control the agents developing it.

Examples of allowed tests:

- Test its lock code using a temporary directory.
- Test its Git checks using a temporary repository.
- Test its result validator using sample JSON files.
- Test its controller using a fake program instead of a real Codex worker.

Small tests can run in parallel as long as each test uses separate temporary files and repositories.

## Firmware Tests

Firmware remains supported, so keep its synthetic tests in the normal required test suite.

- The complete orchestrator suite currently runs 208 tests in about 28 seconds.
- These tests use fake records and subprocesses, not real hardware.
- Keeping the firmware path while adding coding support should cost roughly 1–3 extra agent-hours.
- Run physical hardware tests only for releases or hardware-specific changes.

While the frozen harness is running, do **not** start the candidate as a real harness. The candidate must not start Codex agents, run a live manager loop, watch the frozen harness's lanes, acknowledge real events, or use the frozen harness's runtime files.

```text
allowed:
frozen harness -> test agent -> candidate unit test

not allowed:
frozen harness -> candidate harness -> real Codex agents
```

Testing candidate code is not the same as giving the candidate control of agents.

## When Running the Full Test

Pause development and checkpoint the agents.

This is the first time the candidate is allowed to operate as a real harness.

Then:

1. Stop the frozen harness.
2. Confirm it is no longer running.
3. Start an outside test supervisor.
4. Start the candidate harness by itself.
5. Give it a temporary Python application to build from beginning to end.
6. Let it plan serially, run one production-code or merge lane at a time, and parallelize disjoint test and documentation authors plus isolated test execution.
7. Use the normal watcher to record what happens.
8. Use a read-only watcher subagent to look for critical harness failures.
9. Check that the merged application passes its tests.
10. Stop the candidate harness.

```text
outside test supervisor
  |-- candidate harness
  |     |-- one coding lane at a time
  |     |-- disjoint test lane A
  |     |-- disjoint test lane B
  |     `-- one merge lane at a time
  |-- watcher logs
  `-- read-only watcher subagent
```

Run only one full candidate test at a time.

The candidate harness writes the application. The outside supervisor and watcher judge whether the harness behaved correctly. The candidate does not test its own orchestration.

## What the Test Program Should Be

Use a small but meaningful local Python program, such as a task tracker with:

- Data validation.
- SQLite storage.
- A command-line interface.
- JSON import and export.
- Tests and documentation.

It should require several coding lanes and a merge, but no network, secrets, hardware, or production services.

## What the Watcher Subagent Can Do

The watcher subagent can only read logs and report a critical problem. It cannot edit code, direct agents, acknowledge events, stop processes, or fix anything.

If it reports a critical problem, the outside supervisor:

1. Stops new work.
2. Shuts down the candidate harness.
3. Stops only its exact remaining processes if needed.
4. Saves all evidence.
5. Confirms the entire candidate test has ended.

Abort for serious harness failures, such as workers using the wrong worktree, duplicate locks, invalid results being accepted, corrupted events, lost processes, or unsafe shutdown.

Do not abort just because the application has a bug or a test fails. The candidate harness should be allowed to handle normal coding problems.

## If the Full Test Fails

Stop the candidate harness completely and save its evidence. Then restart the frozen harness and spawn a separate repair agent. The repair agent may use its own subagents, but that repair work is a new run and is never part of the failed candidate test.

## If the Full Test Passes

Promote the candidate harness and use it for future work. Keep the frozen harness turned off but available as a backup.

## The Main Rule

```text
development: frozen harness controls agents
full test:   candidate harness controls test agents
after pass:  promoted candidate controls real agents
```

Never let the frozen and candidate harnesses control agents at the same time.
