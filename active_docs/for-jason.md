# Personal historical notes

Status: non-operative scratchpad. Current product and workflow authority lives only in `goal.md`,
`plans/general-coding-harness/FULL-EXECUTION-SPEC_PLAN_2.md`, and `HANDOFF.md`. Items phrased as
future work or “need to” below may already be implemented or superseded and must not create a live
task, gate, loop, or product requirement.

> For future, when we move back to MCP server, move the .codex setup. Add rules: (1) No overengineering (2) No blocking from reviewers/testers. Orchestrators make final decision based on "worth-it" scale. (3) all changes must follow design principles.

> Add to a requirements plan: ALL changes to the harness must be backwards compatible with the stable general harness- meaning any changes made for the sake of the E2E tests on the agent need to also work on a general python experiment.

> Move same general python experiment back to test the multi agent harness after all the codex exec changes, then after all firmware changes.

> Move the skill + prompt to a general skill that reflects the changes we made (for the loop too - fast lane, aggregate / pool tests, finish full tests and full review before changing rather than looping, stopping every premature review/test -> single contained change -> review/test premature stop -> contained change, amongst the other modification principles made in the plan harness workflow

> Make sure the E2E tests for the MCP server aren't because the multi-agent process keeps having bugs, or the tests themselves keep having bugs, but the MCP server pretty much passes tests or demonstrates capability/validity. We need to fix any looping cuased because the process has an issue and causes rejection, despite the test having demonstrably showed that the MCP server worked.


************
************
***********

>Tell codex to read the harness summary plain, audit and determine which "overengineered" criticisims are valid, and fix them in the codebase. Never do any fix that may remove general multi agent/hardware multi agent functionality and safety (safety as in safeguards that keep it efficient or operational) in all major cases. However, it may remove safeguards that are excessive and dont meaningfully improve safety, but only add complexity.
-------------
--------------
------------

> Make the multi agent harness work on Mac!

> Need to edit the workflow itself for inefficiencies
> Need codex to review claude criticisms in harness summary plain
> Need claude edit execution_plan_2 to make it (1) more efficient and quick and (2) include all the changes we made in the harness summary plain


> Need to edit/change locking mechanism - scoped locking. (is in the skill now)

Current topology (skill changes)
 (1) what Plan should determine:
  - Which project role owns the attempt folder, abort notice, watcher report, and cleanup.
  - Which exact project flow is rehearsed with fakes before real resources are used.

  (2)
 - • Before a costly test, do one tiny fake run to make sure the test runner is set up correctly.
  Check that it has the right files, IDs, folders, arguments, and can start and record its result.
  Do that again only if the runner, its settings, or its environment changed. If nothing changed, reuse the earlier successful check instead of repeating it.

  - (3) Scoped dependency locks.
  - (4) Clear ownership mapping.
  - (5) Fake rehearsal planning.
  - (6) Runner preflight/reuse rules.
  - (7) Pooling and narrow reruns.


Harness changes:

>   1. Make one harness change: narrow worker prompts.
     Give focused workers a compact task card plus verified prior-result references; require full governing-document reading only for genuinely broad review gates. This
     is a real change and should reduce agent compute. -> Make the harness determine it for the orchestrator agent. Let the orchestrator agent fill it out in a json and send it. Put in reference files, but have a soft budget - agent should have a score on the reference file count. The more the count, the lower the score, and agent has to justify the score; we give it the max and min (most optimal vs most expensive) and explain why this amount of expense is necessary. In this prompt, also add: the instruction to not read other files or spend extra compute reconstructing history unless it determines it doesnt have enough context to understand the task or implement it properly

> Lane acceptance mechanism:
     - A report/result artifact fails validation.
  - Freeze the lane; inject the exact validation failure into the same Codex worker.
  - Allow one report-only retry, with “do not invent evidence; use only files already present. If missing, report lane as failed/incomplete”
  - Validate the new artifact normally.
  - If it still fails, reject the lane or narrowly rerun the affected check.

Process changes - get rid of the process bugs blocking things:
test-cleanup.md covers these:

  1. Watcher lifecycle enforcement
     Keep/resume the watcher agent until delayed failure and shutdown, so it writes its own final report.

  2. Already-exited-child cleanup
     Make the ROOT supervisor continue cleanup when a registered child has already exited, instead of raising on an identity race.


