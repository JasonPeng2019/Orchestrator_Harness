# Plain-English Explanation: Worker Task Cards

## What this does

Before starting a focused worker, the orchestrator writes a small JSON task card containing only the
information needed for that job. The harness publishes the scoring scale in advance. The orchestrator
writes the initial-entrypoint count, matching score, and justification into the card. The harness
verifies them and gives the card to the worker as the worker's main prompt.

The card now has a dedicated `context` section. The worker starts there instead of rereading the whole
plan and project history. It can still inspect relevant source code and obtain more background when
that is genuinely needed.

## Who does what

- **Harness:** publishes the fixed scoring scale, then checks identities, initial entrypoints, file
  count, and reported score.
- **Orchestrator:** describes the task, chooses the few files the worker should open first, records
  their count and published score, and explains why that starting set is needed.
- **Worker:** performs the task from the card and expands its background context only when necessary.

The harness does not decide which files are semantically relevant. That requires project judgment and
remains the orchestrator's job.

## Main JSON fields

| Field | Plain-English meaning | Why it is necessary |
|---|---|---|
| `schema` | Version of the task-card format. | Lets the harness validate the correct rules. |
| `card_id` | Unique name for this exact card. | Prevents evidence from different cards being confused. |
| `lane_id` | Lane receiving the task. | Prevents the card being sent to the wrong lane. |
| `worker_invocation_id` | Exact worker receiving it. | Prevents reuse by the wrong worker or retry. |
| `authored_by` | Orchestrator that selected the context. | Records who made the judgment. |
| `task_kind` | Focused coding, review, testing, or broad review. | Explains whether narrow or broad context is reasonable. |
| `objective` | One-sentence desired outcome. | Gives the worker a clear finish line. |
| `working_scope` | What the worker may inspect or change. | Stops unrelated work while allowing necessary source discovery. |
| `starting_state` | Exact repository, branch, and commit. | Ensures the worker operates on the intended code. |
| `context` | Plain-English situation, prior work, known facts, no-redo list, and remaining uncertainty. | Gives the worker the actual background needed to act without reconstructing history. |
| `initial_entrypoints` | Exact files to open first and what to do there. | Removes unnecessary codebase searching at the start. |
| `task_actions` | Concrete actions, completion signals, and escalation conditions. | Tells the worker exactly how to begin and when not to make an out-of-scope decision. |
| `deliverables` | Results or files the worker must produce. | Makes completion concrete. |
| `acceptance_criteria` | Numbered success conditions with strict/tolerable classification. | Lets the orchestrator make a precise acceptance decision rather than trust self-reported PASS. |
| `constraints` | Safety, ownership, and process limits. | Keeps the worker inside the assigned job and authority. |
| `verification` | Relevant tests or checks. | Tells the worker how to prove the work. |
| `entrypoint_budget` | Initial-entrypoint count, published score, and cost explanation. | Makes the prompt's starting-context expense visible and intentional. |

## Important nested fields

`context` is the most important part for compute efficiency. It is a required checklist, not a broad
paragraph. It directly supplies:

- `project_goal`: the relevant product outcome;
- `why_this_lane_now`: why this worker exists now;
- `execution_position`: current phase/gate, predecessor outputs, and next recipient;
- `change_state`: relevant code/behavior and what must remain unchanged;
- `relevant_history`: the short event chain that led here;
- `evidence_credit`: what is already proven and when that proof remains reusable;
- `known_problems`: known failures and whether they are fixed, in scope, out of scope, or unresolved;
- `governing_decisions`: rules/decisions that constrain the lane;
- `dependencies`: inputs and prior outputs the task relies on;
- `ownership_and_handoffs`: who owns this task, nearby work, and the next decision;
- `do_not_repeat`: specific work the worker must not redo; and
- `open_questions`: the narrow uncertainty this lane must resolve.

Every historical claim includes a proof pointer. The worker gets a full concise story first; proof
pointers support audit but are not a to-do list of files to open.

`working_scope` identifies allowed roots, in-scope work, out-of-scope work, and editable paths.
Ordinary source files discovered inside that scope do not count against the context budget.

Each `initial_entrypoint` supplies a unique ID, path, SHA-256 hash, kind, reason, and first action.
It is the only file the orchestrator actively tells the worker to open at the start. After that, the
worker chooses the smallest additional files needed to do the task correctly.

`task_actions` gives the short work sequence: what to do, which initial entrypoints it uses, what
proves the step is complete, and when to return an issue to the orchestrator rather than expanding
scope.

`entrypoint_budget` contains `entrypoint_count`, `score`, and `justification`. The orchestrator copies
the score from the harness's published scale and explains why that many initial files are necessary.
The harness recounts those entrypoints and verifies that the reported score is correct.

## How scoring works

The harness publishes this score table before the orchestrator writes the card. It applies only to
initial entrypoints:

- 0-5 files: score 100;
- 6-14 files: subtract 10 points per additional file;
- 15 or more files: score 0.

For example, 7 initial entrypoints score 80 and 10 score 50. The orchestrator writes both the count
and score into the card and always explains why that starting context is needed. It does not choose
the score. The harness verifies the count and arithmetic.

The score is only a warning about likely compute expense. It never blocks a legitimate task. A broad
final review may correctly score zero if all of those initial files are truly required.

## If the card is missing context

The worker may read the smallest additional set needed to understand or correctly finish the task.
It records what it added and why in `CONTEXT_EXPANSION.json`. It must not guess, fabricate missing
facts, or casually reconstruct unrelated history.

This exception protects correctness while keeping narrow tasks narrow in the normal case.

## When the worker says it is done

A valid-shaped `RESULT.json` is not final acceptance. The harness emits a durable
`LANE_RESULT_READY_FOR_SEMANTIC_ACCEPTANCE` event that says not to start dependent work yet and gives
the exact task-card and result paths/hashes.

The orchestrator reads the task card, result, and required evidence, then writes one verdict:

- `ACCEPTED`: every required condition passed.
- `ACCEPT-WITHIN-TOLERANCE`: only explicitly tolerable conditions missed, with a recorded reason the
  remaining gap does not matter to the product goal.
- `CONTINUE`: resume the same worker with exact missing or unproven items.
- `INCOMPLETE`: completion is not honest or possible within the lane's current scope.

The orchestrator writes the decision in `ORCHESTRATOR_ACCEPTANCE.json`. A next lane/test agent may
start only after `ACCEPTED` or `ACCEPT-WITHIN-TOLERANCE`.

## What this does not do

- It does not restrict necessary source-code inspection.
- It does not estimate exact token use.
- It does not automatically understand which project files matter.
- It does not replace result validation or testing.
- It does not modify the currently frozen stable runner.

The complete proposed contract is in `task-card-spec.md`.
