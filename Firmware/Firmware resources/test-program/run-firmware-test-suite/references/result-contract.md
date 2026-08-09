# Test Result Contract

The test agent writes both:

- `.agent-workspace/RESULT.json` for deterministic validation
- `.agent-workspace/TEST_REPORT.md` for human evidence review

## Main-run terminal statuses

### `PASS`

All spec requirements were executed and passed on the required hardware. Build/flash alone is not
PASS. The result includes raw evidence paths and final board state.

### `SERVER_FAILURE`

The agent has corrected or ruled out firmware, SDK, fixture, identity, and precondition mistakes
and has a minimal reproducible MCP server defect. It must not edit the server.

### Prohibited main-run blocker statuses

`NEEDS_USER` and `INFRA_BLOCKED` are invalid for this suite's main-catalog runs. A doer must not
create a terminal result or ask the user to touch/inspect hardware, supply another approval
utterance, install equipment, or resolve routine infrastructure.

The manager instead applies recorded delegated authorization, repairs ordinary infrastructure,
uses an autonomous electronic/software oracle, or appends a signed spec correction. A temporarily
unavailable resource is a nonterminal `WAITING_FOR_RESOURCE` or `WAITING_FOR_PROVIDER` ledger state:
checkpoint the persistent session and continue every unrelated lane. An intrinsically
manual/special-equipment branch belongs only in non-gating Appendix A, where it receives
`SKIPPED_AUTONOMY_REQUIRED`.

There is intentionally no terminal `FIRMWARE_FAILURE`. Resume the recorded persistent test agent
while it remains usable. If a necessary model change or irrecoverable session requires replacement,
record the continuity handoff defined in `model-continuity-contract.md`; the replacement continues
from the verified evidence boundary rather than restarting the test.

A manager-requested harness-assisted parallel pause is also not a terminal result. At a sealed safe
boundary, write `PARALLEL_CHECKPOINT.md` and return without creating or changing `RESULT.json`.
Resume the same persistent agent after the repair barrier. Never encode a coordination pause as a
terminal result.

`SKIPPED_AUTONOMY_REQUIRED` is a suite-ledger disposition for non-gating Appendix A only. It is not
a main-run `RESULT.json` terminal status and never satisfies or blocks a main catalog gate.

## Required JSON fields

```json
{
  "schema_version": 1,
  "test_id": "A20",
  "status": "PASS",
  "summary": "One-sentence evidence-based outcome.",
  "run_directory": "absolute path",
  "server_commit": "git commit under test",
  "firmware_commit": "fresh repo commit or null with explanation",
  "hardware": [
    {
      "friendly_name": "name used through setup",
      "board": "NUCLEO-L476RG",
      "mcu": "STM32L476RGT6",
      "role": "controller",
      "identity_evidence": "relative evidence path"
    }
  ],
  "requirements": [
    {
      "id": "REQ-001",
      "status": "PASS",
      "evidence": ["relative/path.txt"]
    }
  ],
  "commands": [
    {
      "command": "exact argv or command",
      "cwd": "absolute or run-relative cwd",
      "exit_code": 0,
      "evidence": "relative/path.log"
    }
  ],
  "mcp_evidence": ["relative/path.json"],
  "oracle_evidence": ["relative/path.txt"],
  "final_board_state": "observed state and how it was observed",
  "server_failure": null,
  "blocking_request": null,
  "remaining_work": []
}
```

For `SERVER_FAILURE`, replace `server_failure: null` with:

```json
{
  "observed": "exact observed behavior",
  "expected": "contract/spec behavior",
  "minimal_reproducer": ["ordered exact calls"],
  "reproduced_count": 2,
  "evidence": ["relative/raw-output.json"],
  "ruled_out": ["firmware", "artifact", "board identity", "wiring", "SDK"],
  "suspected_server_scope": ["module or tool name if known"]
}
```

For every main-run result, `blocking_request` is `null`. Waiting work is recorded in
`SUITE_COORDINATION.md`, not `RESULT.json`.

## Report requirements

`TEST_REPORT.md` maps each spec requirement to:

1. action performed;
2. raw evidence path;
3. independent oracle, if required;
4. observed result;
5. verdict;
6. cleanup/final state.

Do not paste only summaries. Preserve exact commands, MCP outputs, artifact hashes, UART/peer
counters, and timestamps in evidence files.
