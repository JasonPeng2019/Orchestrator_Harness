---
name: plan-changes
description: Have the current main/orchestrating model directly author the one implementation plan for a verified BYO-Firmware-MCP production-code repair, then deterministically validate it for change-loop. Do not delegate planning to a subagent, provider-side planner, doer, or tester. Do not use for fresh experiments, firmware/fixture/SDK/spec work, documentation-only changes, or arbitrary repositories.
---

# Plan Changes — main-model server-repair planning only

Use this only after the current main/orchestrating model independently verifies that a
BYO-Firmware-MCP production-code defect requires repair.

## Non-negotiable authorship

The **current main/orchestrating model** that accepted the user request and verified the defect
must inspect the repository and author `$CL_RUN_DIR/plan.md` itself. Repair-control state stays
outside the production server tree.

Do not:

- launch or resume a planner subagent or provider-side planner;
- delegate plan authorship to the implementation doer or either tester;
- use a lower-level role's proposed plan as a substitute for main-model reasoning; or
- let the preparation script fill behavioral decisions.

The doer and testers may later expose a genuine mistake. The main model may then author the narrow
evidence-backed amendment allowed by `$change-loop`; they still do not replan.

Planning is for a working, maintainable product, not theoretical perfection. Include explicit
requirements, credible production/safety risks, and the actual diff blast radius. Record optional
hardening, speculative edge cases, style preferences, and unrelated improvements as out of scope
unless evidence shows they can realistically violate an accepted requirement.

## Delegated-role execution configuration

This skill never deploys a planner subagent. The Firmware provider adapter is intentionally pending,
so this skill must not start, configure, or infer a provider launcher. When the user later chooses
and implements that adapter, it must require explicit unrestricted/no-command-approval settings,
must not rely on parent configuration inheritance, and must not enable automatic approval review.
That future command-execution setting does
not weaken the server's live plan, disclosure, or hardware-permission gates.

## Workflow

1. Save the exact verified server-change request inside `Firmware/`, then run the commands below
   from the `Firmware/` suite root with `CL_REPO_ROOT=BYO-Firmware-MCP`.
2. Prepare deterministic runtime files:

   ```bash
   CL_REPO_ROOT=BYO-Firmware-MCP bash .codex/skills/plan-changes/scripts/plan.sh --prepare changes.md
   ```

   For inline text:

   ```bash
   CL_REPO_ROOT=BYO-Firmware-MCP bash .codex/skills/plan-changes/scripts/plan.sh --prepare --text \
     "Add JSON output while preserving text output."
   ```

   Preparation only copies the request, resets stale plan-review state, and scaffolds
   `$CL_RUN_DIR/plan.md`. It never calls a model.
3. As the current main model, inspect the repository directly before assuming wiring, callers,
   interfaces, tests, or reachability. Read:
   - `$CL_RUN_DIR/changes.md`;
   - `BYO-Firmware-MCP/README.md`, `BYO-Firmware-MCP/SERVER_GUIDE.md`, and the applicable linked
     client/plan contract;
   - `Firmware resources/test-program/design_charter.md` in full;
   - `templates/plan_prompt.md` for the authoring contract; and
   - `templates/plan.md` for the required shape.
4. Write `$CL_RUN_DIR/plan.md` directly. Each `CL-NNN` item must state:
   - the concrete change;
   - verified file/module/area;
   - exact observable behavior, including errors and edge cases;
   - preserved compatibility contracts and adjacent behavior; and
   - objective automated verification, split into the smallest targeted check, affected regression
     surface, and any genuinely necessary expensive acceptance check.
   Also state which existing passing checks would be invalidated by the planned source/contract
   change. Never default to rerunning the full suite or restarting experiments from scratch.
5. Ask the user when a material ambiguity remains. Record accepted minor interpretations beside
   the affected item as `<!-- Assumption: ... -->`.
6. Validate the authored file:

   ```bash
   CL_REPO_ROOT=BYO-Firmware-MCP bash .codex/skills/plan-changes/scripts/plan.sh --validate
   ```

   Validation rejects missing headings, missing `CL-NNN` items, and template placeholders. It
   prints the SHA-256 used by the one-time adversarial plan review.
7. Obtain the one read-only adversarial review required by `$change-loop` and classify its findings
   as actionable or advisory. The live loop remains unavailable until the user implements the
   adapter described in `PROVIDER_ADAPTER.md`. Do not seek repeated review verdicts. Advisory
   perfection work is recorded and declined; only evidenced requirement, safety/data-loss, or
   credible production/orchestration failures amend the plan.

## Script contract

### `scripts/plan.sh`

```bash
CL_REPO_ROOT=BYO-Firmware-MCP bash .codex/skills/plan-changes/scripts/plan.sh --prepare CHANGE_LIST_FILE
CL_REPO_ROOT=BYO-Firmware-MCP bash .codex/skills/plan-changes/scripts/plan.sh --prepare --text "free-form changes"
CL_REPO_ROOT=BYO-Firmware-MCP bash .codex/skills/plan-changes/scripts/plan.sh --validate
CL_REPO_ROOT=BYO-Firmware-MCP bash .codex/skills/plan-changes/scripts/plan.sh --dry-run CHANGE_LIST_FILE
bash .codex/skills/plan-changes/scripts/plan.sh --self-check
```

- `--prepare` writes `$CL_RUN_DIR/changes.md` and a fresh plan scaffold.
- `--validate` reads the main-authored plan and performs structural/placeholder validation.
- `--dry-run` prints paths without changing state.
- `--self-check` validates skill/template wiring.
- No mode starts a model, creates a planner thread, or writes planner JSONL.

## Scope boundary

Do not use this skill for fresh firmware experiments, application/fixture/SDK failures,
documentation-only or metadata-only work, evidence repair, or an unverified server suspicion.
Fresh-experiment agents must not invoke or read it.
