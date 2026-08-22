# Candidate Acceptance Contract

## Isolation

- The outside writer-manager supervises this acceptance but does not orchestrate the target project.
- The candidate orchestrator uses only `harness-in-progress` and fresh acceptance/target roots.
- The frozen checkout is inactive and forbidden to the candidate orchestrator, target workers, and watcher.
- Target workers launch from their assigned target worktrees with the actual Codex bypass flag, full filesystem access, and approval policy `never`.
- Requested Luna models are unavailable in this environment. Sol-medium is the recorded target-worker and watcher substitute. The candidate orchestrator remains Sol.

## Target project

Build a local typed Python taskboard with:

- projects and tasks with stable identifiers and statuses;
- validated status transitions, dependency rules, unfinished-dependency guards, and cycle rejection;
- transactional SQLite storage and isolated tests;
- a service API for project/task CRUD, status changes, dependencies, filters, and summaries;
- a CLI with clear nonzero failures;
- deterministic JSON import/export with atomic validation of malformed, duplicate, invalid-status, invalid-dependency, and cyclic input;
- domain, storage, service, CLI, import/export, and subprocess end-to-end tests;
- a concise README.

Production and authoring lanes are serialized as `P1 -> P2 -> P3 -> P4 -> P5 -> A1 -> A2`. Validation is `D1 -> D2`, followed by merge verification and exact shutdown. Each branch descends from the accepted predecessor.

## Harness invariants

Acceptance must demonstrate declared branch/worktree identity, a valid current clean-tip result, rejection of one deliberately stale result, bounded named-resource ownership, checkpoint/resume with the same thread, durable event delivery, exact acknowledgement, and clean controller/worker/claim shutdown. An ordinary target-code bug stays inside the candidate coding flow and must not trigger the watcher.

## Watcher boundary

The watcher is read-only and isolated. It may inspect acceptance evidence and exact process metadata, but may not message, advise, edit, acknowledge, repair, or stop the candidate orchestrator or target workers. It ignores ordinary application bugs and orchestrator mistakes, including bad prompts, malformed results, test failures, retries, merge conflicts, and incorrect auxiliary bookkeeping, whenever the harness rejects or records them safely.

A whole-test abort is limited to an actual candidate-harness or watcher defect: unsafe execution outside a declared worktree, simultaneous ownership of one exclusive resource, unsafe claim stealing, harness acceptance of a stale/invalid result, loss or false acknowledgement of authoritative actionable evidence, corruption within authoritative controller/native-event evidence, an uncontained controller/worker process, or watcher interference/misclassification. An orchestrator-maintained manifest mismatch is not an abort condition when native controller status and events remain correct. On a demonstrated harness/watcher defect the watcher reports only to the outside writer-manager; the outside writer-manager terminates the complete exact candidate topology and preserves evidence before any repair.
