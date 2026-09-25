# Archived Tier 4 memory-backed harness plan

> Retired on 2026-09-21. This package is historical evidence only and is not
> execution authority. The active plan is
> [../../memory-backed-harness/PLAN.md](../../memory-backed-harness/PLAN.md).

Current plan: [formal Tier 4 composition root](memory-backed-harness-formal/plan-workflow.md).

Status: **VALIDATED**. Accepted compilation, freshness check and canonical
validation all pass. Four independent native reviewers approved F5 and explicitly
carried approval forward through line-ending-only normalization. Findings and
ROOT's vetted dispositions are recorded in the generated validation file.

There is one active plan in two required forms: `memory-backed-harness-source/`
is the editable compiler source; `memory-backed-harness-formal/` is its generated
execution view. Keep both. The superseded non-formal directory was removed to the
Recycle Bin at the user's request; its approvals were not reused.

## Read and edit

- [Composition root](memory-backed-harness-formal/plan-workflow.md): scope,
  authority, requirement coverage, graph, resources and stopping point.
- [Global rules](memory-backed-harness-formal/global-rules.md): shared policies.
- [Steps](memory-backed-harness-formal/steps/): STEP-001 through STEP-010, each
  with a gate and distinct normal/Series1/Series2 paths.
- [Module library](memory-backed-harness-formal/modules/): M01 through M10;
  M01–M09 selected, M10 omitted because no additional recipe is necessary.
- [Validation and reviews](memory-backed-harness-formal/validation.md): actual
  reviewer identities, findings, ROOT dispositions and per-step necessity/cost.
- [Normalized source](memory-backed-harness-source/): sole editable workflow
  source; generated Markdown is not hand-edited.
- [Role mapping](SUBAGENT_ROLE_MODEL_MAPPING.json): sole concrete launch binding
  owner; all 14 roles are populated.

Orchestrating ROOT is the existing assistant session, not a launched subagent.
The separate candidate `test_root` is launchable. Implementation `test_author`
and outer `reviewer` remain distinct from candidate-testing workers and the
internal `test_reviewer`. The latest explicit user allocations govern.
All 12 Codex-launched roles use the normal service tier; ROOT has no launch tier
and the Claude compatibility role retains its non-Codex effort configuration.
Exact installed support and capacity remain STEP-001 runtime admission checks.

APC A and B deliberately use the same selected live binding. Actual native
adaptation evidence proves that tuple; B supplies integrated-context evidence,
not model diversity. Separate deterministic fixtures exercise two selectable
configurations through real candidate validation, persistence and argv code.
Fixture support is not claimed as live provider support. The older plan's
stronger demand for two distinct live tuples was unnecessary; product
configurability and real native-adaptation requirements remain intact.

Ten steps cover the complete current fixed-strategy product:
builder qualification → contracts → real thin slice → disjoint experience and
procedure adapters → search/templates/APC → composition/context/security →
recovery/accounting/snapshots → integrated native demonstration → release audit.

Sources: direct user instructions, repository guidance,
`new_harness_memory_docs` Feature v65 and binding Implementation v67,
Concepts for intent, and Detailed v72 as source hypotheses.
Development stays under `development/`. The frozen dogfooding builder is
`references/harness-single` at
`d679c1f792bd46e78a0bfcefc0e4991e43dfb409`; only a genuine demonstrated bug
can justify a narrow repair. No feature/capability expansion, benchmarks or
learned-selector implementation.

## Verification and next action

Final F5-LF source:
`b81317479f7c2f9bc7f00555fecb8e96f015bd662d9a4558b79987c637ea9fc4`.

VERIFY: PASS — relevant plan-package checks, each exit 0:

```powershell
python -B .agents/skills/project-topology/references/level-4-design-project-topology/scripts/compile_topology.py build .plans/memory-backed-harness-source --output .plans/memory-backed-harness-formal --mapping .plans/SUBAGENT_ROLE_MODEL_MAPPING.json
python -B .agents/skills/project-topology/references/level-4-design-project-topology/scripts/compile_topology.py check .plans/memory-backed-harness-source --output .plans/memory-backed-harness-formal --mapping .plans/SUBAGENT_ROLE_MODEL_MAPPING.json
python -B .agents/skills/project-topology/references/level-4-design-project-topology/scripts/validate_execution_plan.py .plans/memory-backed-harness-formal --mapping .plans/SUBAGENT_ROLE_MODEL_MAPPING.json
```

Build reports VALID with no errors; freshness reports no changed units or review
candidates; canonical validation reports PASS. The accepted package contains
23 files, 135 configured instances and 302 executable cards. Embedded CRLF and
standalone CR source strings were normalized to LF; the compiler and validator
were not modified.

Next, upon an execution request, begin STEP-001's prerequisite/admission closure.
Exact installed CLI/model/effort support, capacity, current service state and
launch permissions remain runtime checks, not claims established by plan
validation. No implementation, product tests or live worker trials were run
during this plan repair.
