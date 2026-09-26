# Memory-backed Orchestrator Harness MVP

This repository is the assembly and planning workspace for a coding harness
that can use reviewed EverOS experience and trusted MongoDB Atlas procedures
while preserving the ordinary all-enhancements-off harness path.

## Canonical product

The completed product is a tracked submodule:

| Field | Value |
| --- | --- |
| Path | `product` |
| Repository | `https://github.com/JasonPeng2019/Harness-Memory-Base.git` |
| Branch | `integration/checkpoint-20260925` |
| Pinned commit | `2544045a4ddf38622948dd3da8a9e6051c92a802` |

The Gitlink commit is authoritative. The branch name records where that commit
is published, but a normal submodule checkout uses the exact pinned commit.
The shorter path avoids Windows checkout failures from the product's deeply
nested skill and vendor files. `development/product/worktree_example` is an
older development example, and `development/product/integration/` is reserved
for ignored local checkpoints; neither is the completed cloned baseline.

## Get the working product

Clone the top-level `memory` branch, then initialize only the canonical product
submodule:

```powershell
git clone --branch memory https://github.com/JasonPeng2019/Orchestrator_Harness.git
Set-Location Orchestrator_Harness
git -c core.longpaths=true submodule update --init -- product
git -C product rev-parse HEAD
```

The final command must print:

```text
2544045a4ddf38622948dd3da8a9e6051c92a802
```

To initialize every reference, lane, and historical test submodule instead, use
`git -c core.longpaths=true submodule update --init --recursive`. That is not
required to run or inspect the completed product.

## What the MVP does

One supported Standard-strategy task can now:

1. Retrieve a scoped, reviewed EverOS case or generated stored skill.
2. Retrieve an eligible trusted procedure through real Atlas Vector Search.
3. Recheck both sources for trust, revision, recipient, and scope.
4. Bind their sanitized guidance and exact identities into an accepted plan and
   privacy-safe final context.
5. Run the actual native harness worker.
6. Run a separate consequential review.
7. Record one durable terminal outcome.
8. Retire the lane and clean only the resources owned by that campaign.

The completed native proof materially used both an `EVEROS_MVP_MARKER` and an
`ATLAS_MVP_MARKER`; Atlas and EverOS were inputs to the real worker rather than
side demonstrations. The focused all-off path also passed with zero optional
EverOS, Atlas, or APC calls.

This is an MVP, not full production qualification. Deferred work includes the
complete operator surface, snapshot qualification, all strategies/profiles,
the full EverOS service-gating matrix, exhaustive recovery and usage accounting,
packaging, broad regression, benchmarks, and learned selection.

## Repository map

```text
Orchestrator-Harness-3/
|-- README.md
|-- HANDOFF.md                         Completed-run status and evidence summary
|-- goal.md                            MVP outcome and completion decision
|-- .plans/memory-backed-harness/      Active plan, step cards, and known issues
|-- new_harness_memory_docs/           Original product intent and contracts
|-- references/                        Pinned upstream/reference repositories
|-- product/                           Canonical product submodule
`-- development/
    |-- product/lane-roots/                         Development lane checkouts
    |-- product/worktree_example/                  Older example checkout
    `-- dogfood/lane-harnesses/                    Frozen implementation harnesses
```

Read current project state in this order:

1. [`HANDOFF.md`](HANDOFF.md) for the completed run and exact product identity.
2. [`goal.md`](goal.md) for the promised MVP outcome.
3. [`.plans/memory-backed-harness/PLAN.md`](.plans/memory-backed-harness/PLAN.md)
   for architecture, execution topology, and the completion gate.
4. [`.plans/memory-backed-harness/KNOWN_ISSUES.md`](.plans/memory-backed-harness/KNOWN_ISSUES.md)
   for deliberately deferred work and non-gating findings.

The older broad specification and plan were intentionally removed from the
active tree during the time-boxed MVP cut. Git history retains their published
versions. Local `.plans/archive/` content is historical and is not required to
obtain the product.

## Focused local check

From the canonical product root, create an ordinary development environment and
run the focused coherent-path test:

```powershell
Set-Location product
python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -e .
& .\.venv\Scripts\python.exe -m unittest tests.local.mvp.test_coherent_memory_path
```

The completed candidate passed this module 4/4. The broader accepted evidence
also includes 29/29 focused Atlas tests, one successful real Atlas live test,
and one accepted priority-tier native worker/reviewer/outcome lifecycle.

Read `harness/QUICK_RULES.md` and `harness/QUICK_START.md` before activating a
new harness runtime. Harness setup binds absolute workspace paths and must be run
for the actual checkout; never copy a virtual environment or runtime directory
from another worktree.

## Credentials and run evidence

Credentials, Atlas connection strings, `.venv` directories, EverOS mutable
roots, `.harness-runtime`, `.agent-runtime`, and live campaign resources are not
part of the repository. Provide secrets only through ignored configuration or
the process environment.

The detailed terminal JSON from the completed native campaign was intentionally
kept as ignored local evidence and is not needed to build or run the pinned
product. The nonsecret durable summary—candidate, run identity, result/review/
acceptance hashes, checks, and cleanup readbacks—is recorded in `HANDOFF.md`.

Do not rerun the completed live campaign against its old UUID resources. Any new
live Atlas proof must allocate a fresh isolated namespace and exact cleanup
owner.
