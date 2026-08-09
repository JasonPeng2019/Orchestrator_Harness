# Worker Task Card and Context Budget

Status: authoritative task-card contract. S4 implements semantic acceptance and report-only recovery;
the immediately following S5 stage enforces terminal thread lifetime before fresh C0/C1/C2 and C3.

## Purpose

A focused worker should receive a compact, sufficient task instead of being told to reconstruct the
project from every governing document, handoff, and historical artifact. The orchestrator writes one
JSON task card. The harness publishes the scoring scale up front. The orchestrator records the file
count, corresponding score, and justification in the card. The harness then validates those values,
binds the card to the worker invocation, and supplies it to the worker as the primary prompt.

This feature is intended to reduce repeated context reading. It must not prevent a worker from reading
source code or obtaining information genuinely necessary to do the task correctly.

## Responsibility boundary

- The **harness** publishes the fixed initial-entrypoint scoring scale before card creation.
- The **orchestrator** decides what the task is and which files are the smallest useful starting
  point. It writes the task-card JSON, counts those initial entrypoints, records the score required by
  the published scale, and explains why that initial context cost is necessary.
- The **harness** validates identity, paths, hashes, required fields, the reported count, and the
  reported score. It rejects arithmetic or counting mistakes but does not reject an honestly
  reported low score.
- The **worker** begins with the card and its initial entrypoints. It then determines additional files
  to inspect as needed, without casually reconstructing project history.

The harness does not attempt to understand the project well enough to choose entrypoints itself. That
would turn a small validation feature into another planning agent. Its job is to make the
orchestrator's context decision explicit, measurable, and auditable.

## Normal flow

1. The orchestrator writes `.agent-workspace/TASK_CARD.json` before dispatch.
2. The invocation binds the task card by path and SHA-256.
3. The harness validates the card and every declared initial entrypoint before launching the worker.
4. The harness recounts the initial entrypoints, verifies the reported score against its published scale,
   and records the verified assessment in controller status.
5. For a focused lane, the task card replaces a long historical startup prompt. It must not merely be
   prepended to the same long prompt.
6. The worker reads the card's explicit `context` section first, then opens only the declared initial
   entrypoints initially.
7. Normal source discovery inside the declared working scope is allowed. Additional planning,
   history, handoff, or evidence files are read only when necessary.

## JSON contract

The proposed schema name is `orchestrator-task-card/v1`.

### Required root fields

| Field | Type | Meaning |
|---|---|---|
| `schema` | string | Exactly `orchestrator-task-card/v1`. |
| `card_id` | string | Unique immutable identity for this card. |
| `lane_id` | string | Lane that receives the card. Must match the invocation. |
| `worker_invocation_id` | string | Worker identity. Must match the invocation. |
| `authored_by` | string | Orchestrator role or identity that selected the context. |
| `task_kind` | string | One of `focused_implementation`, `focused_review`, `focused_test`, or `broad_review`. |
| `objective` | string | One short statement of the result the worker must produce. |
| `working_scope` | object | Where the worker may work and the explicit in/out boundaries. |
| `starting_state` | object | Exact candidate or repository state on which the task is based. |
| `context` | object | The relevant current situation, prior work, known facts, remaining uncertainty, and no-redo boundary. |
| `initial_entrypoints` | array | Exact files the worker opens first, with path, hash, reason, and first action. |
| `task_actions` | array | Concrete assigned work sequence and the conditions that require escalation. |
| `deliverables` | array | Files or results the worker must produce. |
| `acceptance_criteria` | array | Observable conditions for accepting the lane. |
| `constraints` | array | Safety, ownership, read/write, model, or process restrictions. |
| `verification` | array | Required or suggested checks relevant to this task. |
| `entrypoint_budget` | object | The reported initial-entrypoint count, published score, and explanation of why that cost is needed. |

### `working_scope`

Required fields:

- `roots`: directories in which ordinary task-related source discovery is allowed;
- `in_scope`: concise list of components or behaviors the worker owns;
- `out_of_scope`: concise list of nearby work the worker must not take over;
- `write_scope`: explicit files/directories the worker may edit, or an empty array for read-only work.

The entrypoint budget does not count ordinary source files discovered under these roots while coding,
reviewing, or testing. It measures only the files the orchestrator deliberately supplies as the
worker's initial starting point.

### `starting_state`

Required when the invocation is repository-backed:

- `repository_root`;
- `branch`;
- `commit`;
- `clean_required`.

The harness cross-checks these values with the invocation and observed repository state rather than
trusting the card alone.

### `context`

This is the direct, structured background for the worker. It must explain what is going on, not merely
point at historical files. Every field is required; use an empty array only when that category truly
has no relevant entries.

| Field | What the worker learns from it |
|---|---|
| `project_goal` | The relevant product outcome this lane is helping achieve. |
| `why_this_lane_now` | The exact trigger for launching this lane now. |
| `execution_position` | Current phase/gate, predecessor outputs, and who receives this result next. |
| `change_state` | Relevant components, the current change/behavior under study, and what must remain unchanged. |
| `relevant_history` | The short ordered chain of prior events that led to this task. |
| `evidence_credit` | Results already accepted as valid, what they prove, and the boundary for reusing them. |
| `known_problems` | Known failures or risks and their disposition: fixed, in scope, out of scope, or unresolved. |
| `governing_decisions` | Decisions that constrain this lane and the reason they were made. |
| `dependencies` | Inputs, locks, or prior outputs this task relies on and their current status. |
| `ownership_and_handoffs` | What this lane owns, what adjacent roles own, and the next recipient. |
| `do_not_repeat` | Tests, history reconstruction, or work that must not be redone. |
| `open_questions` | The only uncertainties this lane is expected to resolve. |

Required shapes:

- `execution_position`: `phase`, `current_gate`, `predecessor_outputs`, `next_recipient`;
- `change_state`: `relevant_components`, `behavior_under_study`, `must_preserve`;
- `ownership_and_handoffs`: `this_lane_owns`, `adjacent_owners`, `next_recipient`;
- every item in `relevant_history`, `evidence_credit`, `known_problems`, `governing_decisions`, and
  `dependencies`: `summary`, `evidence`; `known_problems` also has `disposition` and
  `evidence_credit` also has `reuse_boundary`.

Optional `continuity` records the immediately preceding lane, worker, or checkpoint when this is a
same-thread continuation. It contains `prior_lane_id`, `prior_worker_invocation_id`, and
`resume_boundary` as applicable.

The card must put the useful conclusion in these fields directly, for example “the affected smoke
passed at this exact commit” and “do not rerun it.” The attached proof pointer proves the summary; it
is not a substitute for the summary and does not instruct the worker to open the file.

Each `evidence` value is an object with `path` and `sha256`. The harness may validate it for evidence
integrity, but proof pointers are not initial entrypoints and never count toward the context score.

### `initial_entrypoints`

An initial entrypoint is a file the orchestrator deliberately tells the worker to open first. Each
item contains:

- `entrypoint_id`: unique ID inside the card;
- `path`: exact file path;
- `sha256`: exact expected file digest;
- `kind`: one of `task_input`, `source`, `test`, `interface_contract`, or `evidence`;
- `reason`: why this is the right file to open first;
- `first_action`: what the worker should learn, inspect, or change there.

It tells the worker where to begin without prescribing every later file it may need. A focused coding
lane normally names the relevant source file and test file; a focused test lane normally names the
exact selection and relevant test module. Directories and globs are not entrypoints because their
cost cannot be measured.

### `task_actions`

Each item contains:

- `order`: positive integer;
- `instruction`: concrete assigned action, not a request for hidden reasoning;
- `uses`: initial-entrypoint IDs needed for that action;
- `completion_signal`: observable condition that completes the action;
- `escalate_if`: array of conditions under which the worker must record the problem and return it to
  the orchestrator instead of expanding scope or inventing a decision.

These are the task's intended operational steps. They make the card immediately actionable, while
the worker retains discretion over ordinary implementation details within its declared scope.

### `deliverables`

Each item contains:

- `path`;
- `description`;
- `required` (boolean).

### `acceptance_criteria`

Each item contains:

- `criterion_id`: stable unique ID inside the card;
- `requirement`: observable condition that normally must be true for the task to pass;
- `evidence_required`: what result or raw evidence must establish it;
- `tolerance`: either `strict` or `orchestrator_judgment`.

`strict` means the criterion must be satisfied for `ACCEPTED`; it cannot be bypassed with
`ACCEPT-WITHIN-TOLERANCE`. Use it for explicit user requirements, safety boundaries, security,
required product behavior, identity, authority, or evidence integrity. `orchestrator_judgment` means
the orchestrator may accept an unmet criterion only through the fully recorded tolerance verdict
defined below. The default is `strict` when the card does not explicitly say otherwise.

### `verification`

Each item contains:

- `name`;
- `command` or `procedure`;
- `required` (boolean);
- `success_condition`.

Only checks relevant to the assigned surface belong here. Broad repository gates remain owned by the
orchestrator unless this lane is explicitly the broad gate.

### `entrypoint_budget`

The orchestrator writes:

- `entrypoint_count`: number of unique files in `initial_entrypoints`;
- `score`: score dictated by the harness's published scale;
- `justification`: why this many initial files are necessary for this task and why a smaller initial
  starting set would be insufficient.

The harness independently recounts the initial entrypoints and recomputes the score. The card is malformed if
the reported count or score is wrong. This check catches mistakes; it does not let the orchestrator
choose a more favorable score.

## Soft-budget score

Before any card is written, the harness publishes this transparent version 1 scale for initial
entrypoints:

- **Maximum score:** 100 when the card contains 0 through 5 unique initial entrypoints.
- **Minimum score:** 0 when the card contains 15 or more unique initial entrypoints.
- Between 5 and 15 entrypoints, subtract 10 points for every additional entrypoint.

Equivalent formula, where `N` is the normalized unique initial-entrypoint count:

```text
score = clamp(0, 100, 150 - (10 * N))
```

Examples:

| Unique initial entrypoints | Score | Interpretation |
|---:|---:|---|
| 4 | 100 | Compact/optimal |
| 5 | 100 | Compact/optimal |
| 7 | 80 | Reasonable |
| 10 | 50 | Expensive; justify the breadth |
| 15 | 0 | Most-expensive band; likely a broad gate |
| 22 | 0 | Still allowed, but explicitly expensive |

The score measures likely context expense only. It is not a correctness score and does not reject a
task. A genuine whole-product or final broad review may correctly score zero.

The harness requires:

- the orchestrator to report the exact `entrypoint_count` and matching `score` in every card;
- a `justification` for every score, explaining why that many initial files are necessary;
- a path, hash, reason, and first action for every initial entrypoint.

A low score with a valid reason proceeds normally. This is a soft budget: it makes expensive context
visible without pressuring the orchestrator to omit information necessary for correctness.

The normalized count deduplicates identical canonical paths. Output paths, the task card itself,
proof pointers, and ordinary files discovered after launch do not count. Byte size may be recorded
for later measurement, but it does not affect the v1 score.

## Worker instruction injected by the harness

For focused lanes, the harness supplies this instruction with the validated card:

> Start from this task card's `context` section. Treat its evidence-backed facts, completed-work
> boundary, and no-redo list as your starting state. Open the initial entrypoints first. Then use your
> judgment to inspect the smallest additional files needed to understand or correctly complete the
> task. Do not read planning, handoff, history, or evidence files merely to reconstruct earlier work
> when the card already states the needed conclusion. Normal inspection of relevant source code inside
> the declared working scope is allowed. If additional project context is necessary, record what you
> added and why. Never guess or fabricate missing context.

For `broad_review`, the harness keeps the same instruction but permits a deliberately broader initial
entrypoint set. Full governing-document reading is required only when the orchestrator has classified
the lane as a genuinely broad gate and explained why.

## Orchestrator semantic acceptance gate

After a worker exits with a structurally valid `RESULT.json`, the harness emits this durable event;
it does **not** call the worker's self-reported outcome final acceptance:

```json
{
  "schema": "orchestrator-semantic-acceptance-required/v1",
  "kind": "LANE_RESULT_READY_FOR_SEMANTIC_ACCEPTANCE",
  "instruction": "Do not dispatch a dependent test or next lane yet. Read the task card, result, and required evidence. Write exactly one verdict: ACCEPTED, ACCEPT-WITHIN-TOLERANCE, CONTINUE, or INCOMPLETE.",
  "task_card": {
    "path": ".agent-workspace/TASK_CARD.json",
    "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
  },
  "result": {
    "path": ".agent-workspace/RESULT.json",
    "sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
  },
  "state": "ACCEPTANCE_PENDING"
}
```

The harness emits the event through the same durable status/event channel the orchestrator already
watches. It supplies the instruction and exact artifacts; the orchestrator makes the semantic
judgment. A malformed or missing result instead produces a structural-result repair event and must
be corrected or honestly marked incomplete before semantic acceptance begins.

### Required orchestrator check

Before writing a verdict or dispatching a dependent lane, the orchestrator compares the entry task
card against the result and the applicable raw evidence. It must determine whether:

1. every required deliverable exists and is valid;
2. every `task_action` has its stated completion signal;
3. every acceptance criterion has the required evidence;
4. every required verification actually ran and passed;
5. the exact expected final state, commit, cleanliness, and constraints hold; and
6. no escalation condition remains unresolved.

The orchestrator writes `.agent-workspace/ORCHESTRATOR_ACCEPTANCE.json`, bound to the exact task-card
and result hashes. It records the verdict, concise reason, and one disposition for each criterion:
`SATISFIED`, `TOLERATED`, `MISSING`, or `NOT_APPLICABLE`.

### Verdicts

- `ACCEPTED`: every required task-card condition is satisfied. A dependent lane may start.
- `ACCEPT-WITHIN-TOLERANCE`: one or more `orchestrator_judgment` criteria are not literally met, but
  the orchestrator has determined from the evidence that the stated product goal is met and the
  remaining gap has no meaningful deployment, correctness, safety, security, recovery, or required
  behavior consequence. The acceptance record must name every tolerated criterion, the observed
  evidence, why the criterion was disproportionate or immaterial here, and why further work is not
  worth its regression/verification cost. A `strict` criterion can never be tolerated.
- `CONTINUE`: the task can still be completed within its current scope. The acceptance record lists
  the exact missing or unproven items. The orchestrator resumes the same worker thread with only
  those items; it retains all still-valid prior work and evidence.
- `INCOMPLETE`: honest completion is not currently possible within the task's scope or available
  evidence. No dependent lane starts on the claimed result. The orchestrator records the blocker and
  routes only the affected work according to the plan.

No later lane may treat a worker's `RESULT.json` outcome as final acceptance without the matching
orchestrator acceptance record.

### Logical task and thread lifetime

One worker thread belongs to one task-card objective. `CONTINUE` may resume it only for the exact
missing criteria in that card. The same thread is also allowed for the one report-only structural
recovery and the strict test-only fast lane while that logical task remains unaccepted. The
orchestrator must send the complete currently known same-task gap set in that continuation.

`ACCEPTED` or `ACCEPT-WITHIN-TOLERANCE` makes the logical task and its thread terminal. The harness
rejects a later resume that tries to use that accepted thread for unrelated work. A later task starts
a new worker invocation and bounded task card referencing only the accepted evidence it needs. This
does not disable Codex's own automatic context management or split one unfinished task merely because
it is long.

## Context expansion

If the worker needs additional planning, history, handoff, or evidence context, it writes
`.agent-workspace/CONTEXT_EXPANSION.json` containing:

```json
{
  "schema": "orchestrator-context-expansion/v1",
  "card_id": "S12.D1-task-card-001",
  "reason": "The prior result summary did not identify which assertion owns the failing behavior.",
  "added_files": [
    {
      "path": "evidence/S12/TEST_REPORT.json",
      "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "purpose": "Locate the exact failing assertion and its evidence binding."
    }
  ]
}
```

This record is informational. It does not fail the lane merely because context expansion was needed.
The final status records the original initial-entrypoint score and added-file count so future plans can
improve their cards using actual evidence rather than guesses. Added files do not retroactively alter
the score: it measures the orchestrator's initial prompt efficiency.

Source-code discovery inside the declared working scope does not require this record.

## Complete example

```json
{
  "schema": "orchestrator-task-card/v1",
  "card_id": "S12.D1-task-card-001",
  "lane_id": "S12.D1",
  "worker_invocation_id": "s12-d1-001",
  "authored_by": "ROOT-IM",
  "task_kind": "focused_test",
  "objective": "Run the two tests invalidated by the accepted parser repair and report their exact outcomes.",
  "working_scope": {
    "roots": ["orchestrator_harness/tests", ".agent-workspace"],
    "in_scope": ["The two named parser regression IDs", "Their result evidence"],
    "out_of_scope": ["Production edits", "Unrelated tests", "Full-suite reruns"],
    "write_scope": [".agent-workspace"]
  },
  "starting_state": {
    "repository_root": ".",
    "branch": "repair/parser-validation",
    "commit": "0123456789abcdef0123456789abcdef01234567",
    "clean_required": true
  },
  "context": {
    "project_goal": "Retain the accepted parser repair and prove only its dependency-invalidated regression coverage.",
    "why_this_lane_now": "The accepted repair invalidated these two tests and no other test coverage.",
    "execution_position": {
      "phase": "focused post-repair test lane",
      "current_gate": "S12 selected regression validation",
      "predecessor_outputs": ["Accepted parser repair", "Affected-test selection"],
      "next_recipient": "ROOT triage"
    },
    "change_state": {
      "relevant_components": ["Parser validation", "The two named parser regression tests"],
      "behavior_under_study": "The accepted parser behavior at the exact starting commit.",
      "must_preserve": ["Accepted production repair", "Existing green unrelated coverage"]
    },
    "relevant_history": [
      {
        "summary": "ROOT accepted the parser repair at the exact starting commit.",
        "evidence": {
          "path": "evidence/S12/ROOT_ADMISSION.json",
          "sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
        }
      }
    ],
    "evidence_credit": [
      {
        "summary": "The production repair and its review are complete and must not be edited by this lane.",
        "evidence": {
          "path": "evidence/S12/ROOT_ADMISSION.json",
          "sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
        },
        "reuse_boundary": "Reusable while the starting commit and two selected test IDs remain unchanged."
      }
    ],
    "known_problems": [],
    "governing_decisions": [
      {
        "summary": "Run only the two dependency-invalidated IDs; do not reopen production review.",
        "evidence": {
          "path": "evidence/S12/AFFECTED_TEST_SELECTION.json",
          "sha256": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
        }
      }
    ],
    "dependencies": [
      {
        "summary": "The selected test IDs and commands are fixed by the affected-test selection artifact.",
        "evidence": {
          "path": "evidence/S12/AFFECTED_TEST_SELECTION.json",
          "sha256": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
        }
      }
    ],
    "ownership_and_handoffs": {
      "this_lane_owns": ["Executing the two selected tests", "Writing exact result evidence"],
      "adjacent_owners": ["ROOT owns acceptance/triage", "Repair lane owns production source"],
      "next_recipient": "ROOT triage"
    },
    "do_not_repeat": ["Production review", "Unrelated parser tests", "Full-suite execution"],
    "open_questions": ["Do both exact affected regression IDs pass at this commit?"]
  },
  "initial_entrypoints": [
    {
      "entrypoint_id": "selection",
      "path": "evidence/S12/AFFECTED_TEST_SELECTION.json",
      "sha256": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
      "kind": "task_input",
      "reason": "It supplies the exact two stable test IDs and commands.",
      "first_action": "Confirm the two selected IDs and their required commands."
    },
    {
      "entrypoint_id": "parser-test-module",
      "path": "orchestrator_harness/tests/test_parser.py",
      "sha256": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
      "kind": "test",
      "reason": "It is the direct test source for the selected IDs.",
      "first_action": "Inspect the two selected tests and directly used helpers."
    }
  ],
  "task_actions": [
    {
      "order": 1,
      "instruction": "Confirm that the starting commit and selected IDs match the card.",
      "uses": ["selection"],
      "completion_signal": "The selection and starting state match exactly.",
      "escalate_if": ["The commit or selected IDs do not match the card."]
    },
    {
      "order": 2,
      "instruction": "Run each selected regression exactly once using the declared commands.",
      "uses": ["selection", "parser-test-module"],
      "completion_signal": "Both named IDs have an exact command and outcome.",
      "escalate_if": ["A required command or fixture is missing.", "The task would require a production or unrelated test edit."]
    },
    {
      "order": 3,
      "instruction": "Write the lane result using the observed outcomes and preserve the clean worktree.",
      "uses": ["selection"],
      "completion_signal": "A valid result exists with both outcomes and the tracked worktree is clean.",
      "escalate_if": ["The result cannot be written truthfully from available evidence."]
    }
  ],
  "deliverables": [
    {
      "path": ".agent-workspace/RESULT.json",
      "description": "Lane result bound to both stable IDs and exact commit.",
      "required": true
    }
  ],
  "acceptance_criteria": [
    {
      "criterion_id": "selected-ids-ran-once",
      "requirement": "Both selected stable IDs ran exactly once.",
      "evidence_required": "Exact commands and outcomes for both named IDs.",
      "tolerance": "strict"
    },
    {
      "criterion_id": "result-is-complete",
      "requirement": "The result reports exact commands and outcomes.",
      "evidence_required": "Valid RESULT.json with both command/outcome records.",
      "tolerance": "strict"
    },
    {
      "criterion_id": "clean-worktree",
      "requirement": "The tracked worktree remains clean.",
      "evidence_required": "Final clean Git status record.",
      "tolerance": "strict"
    }
  ],
  "constraints": [
    "Do not edit production or test source.",
    "Do not run unrelated tests.",
    "Do not access hardware or MCP."
  ],
  "verification": [
    {
      "name": "selected parser regressions",
      "command": "python -m unittest test_one test_two",
      "required": true,
      "success_condition": "Exit code 0 and both named tests reported passing."
    }
  ],
  "entrypoint_budget": {
    "entrypoint_count": 2,
    "score": 100,
    "justification": "Two initial files are necessary and sufficient: the exact test selection and directly affected test source. The accepted-repair history is summarized in context."
  }
}
```

This example receives a score of 100 because it declares two unique initial entrypoints.

## Validation and failure behavior

Before worker launch, the harness rejects the card when:

- its lane or worker identity does not match the invocation;
- a declared path is missing, unsafe, or outside the invocation's allowed readable boundaries;
- an initial-entrypoint hash does not match;
- a required field is absent or malformed;
- the reported initial-entrypoint count or score does not match the published scale;
- a required justification is missing.

The harness does **not** reject a card because its score is low. It records the score and explanation.
It also does not claim that the entrypoints are semantically complete; that judgment belongs to the
orchestrator, with the worker's bounded expansion as the recovery path.

## Non-goals

- Automatically deciding which project files are relevant.
- Preventing necessary source inspection.
- Estimating exact token consumption from file count.
- Replacing structural result validation, review, or test selection.
- Forcing every project into the same number of initial entrypoints.
- Requiring this feature in the currently frozen stable runner.

## Minimum implementation slice

The bounded S4/S5 implementation needs only:

1. optional `task_card` path/SHA binding in a coding invocation;
2. one task-card validator and deterministic verifier for the published score;
3. prompt rendering from the validated card for focused lanes;
4. durable `LANE_RESULT_READY_FOR_SEMANTIC_ACCEPTANCE` events and hash-bound orchestrator acceptance
   records;
5. controller-status fields for card identity, initial-entrypoint count, score, and justification; and
6. focused tests for identity mismatch, hash mismatch, scoring boundaries, low-score allowance,
   required context/action/entrypoint fields, semantic verdicts, and context-expansion recording; and
7. S5 resume admission that preserves valid unfinished same-task routes but rejects unrelated reuse
   after semantic acceptance.

No scheduler, semantic file selector, token estimator, or automatic context-retrieval system is
needed.
