# Memory-enabled harness development workspace

This repository is the assembly workspace for a ROOT-led coding harness with
durable experience memory, shared Atlas-backed procedures, and reusable plan
templates. The active product seed is
`development/product/worktree_example`; the other top-level trees are source
material and governing specifications.

## Repository map

```text
Orchestrator-Harness-3/
|-- .plans/                        Active remaining-work spec/plan and finished history
|-- new_harness_memory_docs/        Product intent and normative contracts
|-- references/                     Pinned upstream/reference working trees
|   |-- harness-single/             Base Orchestrator Harness v2
|   |-- Codex_Claude_Setup/         ROOT workflow and skill suite
|   |-- Harness-Memory-Base/        EverOS fork
|   `-- Harness-Memory-Planning/    langchain-mongodb fork/monorepo
`-- development/
    |-- dogfood/harness/             Outer implementation harness source
    `-- product/worktree_example/   Active product repository and candidate harness
        |-- .agent/ .agents/ ...    ROOT suite at workspace scope
        |-- .harness-runtime/
        |   `-- worktrees/          Native implementation/test worktrees only
        `-- harness/
            |-- orchestrator_harness/   Base harness implementation
            |-- adapters/ super-cache/  Harness provider payloads
            |-- docs/product/           Product specification snapshot
            `-- vendor/
                |-- everos/             Local experience-memory engine
                `-- langchain-mongodb/  Atlas/LangChain integration sources
```

The ROOT suite intentionally lives at the product root. The harness setup code
rejects a `root_workspace` located inside the harness source directory, so the
base harness lives one level down in `harness/` and targets its parent product
workspace.

## Product authority and scope

Read the product documents in this order:

1. `new_harness_memory_docs/PRODUCT_CONCEPTS.md` for intent.
2. `PRODUCT_FEATURE_SPEC_v65.md` for observable behavior and trust boundaries.
3. `PRODUCT_IMPLEMENTATION_SPEC_v67.md` for binding integration contracts and
   required verification.
4. `PRODUCT_SPEC_DETAILED_v72.md` for source observations and rationale.

The same snapshot is copied into the active product at
`development/product/worktree_example/harness/docs/product/`.

Current execution is governed by the
[remaining-work specification](.plans/memory-backed-harness/specification/SPEC.md)
and [plan](.plans/memory-backed-harness/PLAN.md). STEP-01 through STEP-03 are
complete; their historical plans are under
`.plans/finished/memory-backed-harness/steps/`. Only STEP-04 through STEP-06 are
active.

The current phase builds the complete fixed-strategy product: reviewed local
experience, cases and approved skills, local templates, Atlas shared procedure
retrieval, bounded Standard/Problem-focused/Deeper search, APC direct-fill /
harness-launched light adaptation / fresh-plan fallback, linked outcomes,
feature switches, and snapshot/isolation support.

Two boundaries are explicit:

- Do not implement the learned search-strategy selector yet.
- Do not run SWE-Marathon, FrontierSWE, MemoryArena, LongMemEval, BEAM, or any
  benchmark/subset/scored comparison in this phase.

## Component responsibilities

| Component | Responsibility |
| --- | --- |
| ROOT suite + base harness | Exact current task/plan state, worker lifecycle, worktrees, review, acceptance, cleanup, and provider execution. |
| EverOS | Local reviewed trajectories, case/skill extraction, Markdown source of truth, SQLite state, and derived local search indexes. |
| MongoDB Atlas path | Published project/shared procedures and material Atlas Vector Search participation. |
| Accepted product integration | Canonical records and SQLite state, feature/privacy foundations, reviewed EverOS experience, and authorized procedure/Atlas lifecycle. |
| Remaining product integration | Bounded preparation, template/APC planning, context/dispatch, terminal reconciliation and usage, snapshots/network/operator controls, and integrated proof. |

Memory is advisory. It never replaces exact current state, ROOT plan authority,
review, or verification. The all-enhancements-off path must remain the ordinary
base harness plus ROOT suite.

## Active product setup

The composed seed is already populated. Its source mapping and commit identities
are recorded in
`development/product/worktree_example/harness/REUSE_MANIFEST.md`.

### What is prepared once and what must run per worktree

The reference repositories are reusable **source snapshots**, not activated
runtimes. Keep source, tests, lockfiles, licenses, and safe configuration
examples in the seed. Do not copy virtual environments, credentials, generated
memory, absolute bindings, live processes, or Atlas resources between
worktrees.

This distinction is required rather than cosmetic:

- Python `.venv` directories contain machine- and path-specific launchers and
  are ignored by Git; running `uv sync` under `references/` would not prepare a
  later product copy.
- Harness setup binds an absolute `root_workspace`, installs hooks into that
  workspace, writes runtime state, and starts a persistent monitor. It must run
  against each real product worktree. In particular, the supplied
  `references/harness-single/harness-config.json` still names the old
  `Orchestrator-Harness-2` workspace and must never be used to activate this
  product.
- EverOS configuration contains credentials and owns a mutable memory root.
  Each product worktree/test partition needs its own ignored root.
- Atlas is an external managed service. A source copy cannot contain its
  project, cluster, database user, network access, collections, or search
  indexes.

| Component | Already portable in the seed | Per-worktree or external setup |
| --- | --- | --- |
| ROOT suite | `.agent/`, `.agents/`, `.codex/`, `.claude/`, validation script, and skills | No package install. Validate after copying; provider login remains host/user state. |
| Base harness | Complete Python 3.11+ standard-library source, adapters, examples, config schemas | Correct the absolute harness config, declare exclusive resources, then run `harness setup` once for that worktree. |
| EverOS | Complete 1.3.1 source, tests, configuration examples, and `uv.lock` | Create its local `.venv`, choose an isolated memory root, initialize config, supply LLM/embedding credentials, and start the service. |
| EverAlgo | Exact compatible wheels/sdists are locked by EverOS | No separate clone, submodule, port, or setup. |
| `langchain-mongodb` | Complete 0.12.0 monorepo/package source and package-level `uv.lock` | Create its package development `.venv`. Atlas is not required for unit tests. |
| MongoDB Atlas | Client integration source only | Provision and secure Atlas, create an isolated product namespace and Vector Search index, and provide the URI through ignored configuration. |

### Host prerequisites

Install these once on every development machine:

- Git and Python 3.12+. Python 3.12 satisfies the harness's Python 3.11+
  requirement and EverOS's Python 3.12+ requirement.
- `uv` for the two vendored Python dependency environments.
- Install and authenticate the launchers required by the current development-role
  mapping: Codex, Claude Code, and Ollama where a role selects its Codex-hosted
  Ollama launcher. Provider login is not stored in this repository. Qwen Code is
  not part of the current mapping.
- Network access and credentials for the selected LLM, embedding, rerank, and
  Atlas services.
- Optional: `just` plus a Bash environment for upstream `langchain-mongodb`
  shortcut commands. The PowerShell instructions below call `uv` directly and
  do not require `just`.
- Optional: Docker/Podman only for upstream local-Atlas integration testing.
  It is not needed for unit tests and does not replace the required live-Atlas
  product demonstration.

### Selected providers and models

The product separates development-agent launches, the deployed APC binding, and
EverOS memory services. Development roles are resolved only from
`.plans/SUBAGENT_ROLE_MODEL_MAPPING.json`; current bindings can use direct Codex,
Claude Code, or an Ollama model through the Codex launcher and are not deployment
defaults. Every product APC run supplies its own explicit
`apc_adaptation_binding`. The EverOS service models below are separate from both.

The initial memory stack uses one DeepInfra account and one API key for all
three EverOS model roles. This avoids local GPU/model hosting and a second
model-provider account while retaining OpenAI-compatible chat and embedding
interfaces.

| Role | Selected model | Endpoint | Price snapshot (2026-09-20) | Reason |
| --- | --- | --- | --- | --- |
| EverOS extraction and memory generation | [`deepseek-ai/DeepSeek-V4-Flash-0731`](https://deepinfra.com/deepseek-ai/DeepSeek-V4-Flash-0731) | `https://api.deepinfra.com/v1/openai` | $0.06 / 1M input tokens; $0.18 / 1M output tokens | Low-cost model with JSON support behind DeepInfra's OpenAI-compatible chat API. |
| Embedding | [`Qwen/Qwen3-Embedding-4B`](https://deepinfra.com/Qwen/Qwen3-Embedding-4B) | `https://api.deepinfra.com/v1/openai` | $0.020 / 1M tokens | API-hosted, instruction-aware, and supports the product's selected 1024-dimensional representation. No model download is required. |
| Reranking | [`Qwen/Qwen3-Reranker-4B`](https://deepinfra.com/Qwen/Qwen3-Reranker-4B) | `https://api.deepinfra.com/v1/inference` | $0.025 / 1M tokens | Matches the embedding family and supports EverOS agentic/hybrid retrieval and Knowledge Wiki paths. |

DeepInfra also hosts the 0.6B Qwen embedding and reranking models for $0.010
per 1M tokens. They are not the initial baseline: the absolute development-cost
saving is very small, while DeepInfra's published retrieval evaluation shows a
material quality gap between the 0.6B and 4B embedding models. Treat model IDs,
availability, and prices as external configuration and recheck their linked
provider pages before a production cost commitment.

The selected embedding representation is 1024 dimensions. Use the same model,
dimension, normalization behavior, and task instruction for both indexed
documents and queries. Changing any part of that representation requires an
EverOS cascade rebuild, re-embedding Atlas documents, and rebuilding or
replacing the affected Atlas Vector Search index.

### Activate a new product worktree

The following is the complete activation order for each new copy. Replace the
example path with that copy's actual product root.

#### 1. Establish Git ownership and validate ROOT

Make the product directory a real standalone repository or a correctly
registered worktree before asking the harness to create lanes. Do not reuse the
stale `.git` indirection inherited by this example seed.

```powershell
$productRoot = (Resolve-Path 'development\product\worktree_example').Path
Set-Location $productRoot
python .agent\validate-workspace.py
```

The ROOT suite itself needs no dependency installation. Its copied
`.codex/config.toml` already enables hooks; preserve `[features] hooks = true`.

#### 2. Configure and set up the base harness

Edit `$productRoot\harness\harness-config.json` so `root_workspace` is exactly
`$productRoot`. Keep `managed_coordination` explicit. Edit
`resource-manifest.json` only for resources that truly require exclusive
leases; an empty list is valid.

Read `harness\QUICK_RULES.md` and `harness\QUICK_START.md`, then run setup from
the harness root:

```powershell
Set-Location "$productRoot\harness"
python -m orchestrator_harness.operator_launch harness setup
python -m orchestrator_harness.operator_launch scan --no-write
```

The harness has no third-party runtime packages. Setup preflights collisions,
preserves shared Codex/Claude configuration, merges harness hook groups, stages
and verifies worker payloads, writes worktree-specific bindings, and starts the
persistent monitor. It starts no lane or provider. Run it only after the
absolute target and Git ownership are correct; use `harness shutdown` when the
runtime is no longer needed.

#### 3. Install and configure EverOS

Create the vendored EverOS development environment from its checked-in lock;
do not re-resolve or replace its compatible `everalgo-*` versions:

```powershell
$env:EVEROS_ROOT = Join-Path $productRoot '.harness-runtime\everos'
Set-Location "$productRoot\harness\vendor\everos"
uv sync --frozen --python 3.12
uv run everos init --root "$env:EVEROS_ROOT"
```

The ignored `EVEROS_ROOT` keeps Markdown memory, SQLite state, LanceDB indexes,
and provider configuration isolated from other product worktrees. Supply
secrets through the generated ignored configuration or the process environment.
The product-capable baseline needs:

```powershell
# Extraction and memory generation (OpenAI-compatible chat endpoint)
$env:EVEROS_LLM__MODEL = "deepseek-ai/DeepSeek-V4-Flash-0731"
$env:EVEROS_LLM__API_KEY = "<deepinfra-key>"
$env:EVEROS_LLM__BASE_URL = "https://api.deepinfra.com/v1/openai"

# Vector/hybrid retrieval, reflection, and skill extraction
$env:EVEROS_EMBEDDING__MODEL = "Qwen/Qwen3-Embedding-4B"
$env:EVEROS_EMBEDDING__API_KEY = "<deepinfra-key>"
$env:EVEROS_EMBEDDING__BASE_URL = "https://api.deepinfra.com/v1/openai"
$env:EVEROS_EMBEDDING__DIMENSIONS = "1024"

# Agentic/default-agent hybrid search and Knowledge Wiki, when enabled
$env:EVEROS_RERANK__MODEL = "Qwen/Qwen3-Reranker-4B"
$env:EVEROS_RERANK__API_KEY = "<deepinfra-key>"
$env:EVEROS_RERANK__BASE_URL = "https://api.deepinfra.com/v1/inference"
```

EverOS can start with only the LLM and then provides keyword-only retrieval.
The intended product needs the embedding provider. Its LanceDB schemas and
adapter target 1024-dimensional vectors and truncate longer results to 1024.
The selected Qwen endpoint is MRL-capable, so the baseline explicitly requests
`EVEROS_EMBEDDING__DIMENSIONS=1024` for provider-side truncation and
renormalization rather than relying only on adapter-side truncation.

Start EverOS in a dedicated terminal and verify the capability matrix:

```powershell
Set-Location "$productRoot\harness\vendor\everos"
$env:EVEROS_ROOT = Join-Path $productRoot '.harness-runtime\everos'
uv run everos server start
```

```powershell
Invoke-RestMethod 'http://127.0.0.1:8000/health'
```

Expect `status` to be `ok` and the LLM/embedding capabilities needed by the
selected product path to be available. Rerank may remain unavailable only when
the selected path does not require it. Multimodal parsing, Milvus, and external
observability exporters are not initial product prerequisites.

If the embedding model or representation changes, stop the EverOS server first,
run `uv run everos cascade rebuild` from this environment, and re-embed any
affected Atlas documents. Rebuild drops and recreates the derived local tables;
it is unsafe alongside a running server. Never mix incompatible vectors in one
index.

#### 4. Install the `langchain-mongodb` development package

This package is client/library code; it does not start MongoDB and does not
need Atlas for its unit suite. Prepare the package environment where its source
and focused tests live:

```powershell
Set-Location "$productRoot\harness\vendor\langchain-mongodb\libs\langchain-mongodb"
uv sync --frozen --python 3.12
uv run pytest tests/unit_tests
```

This environment is for changing and testing the vendored integration itself.
When the product integration package is created, it must declare an explicit
local/path dependency on this package (or a deliberate published version);
creating this `.venv` alone does not make the library importable from an
unrelated product environment.

Upstream integration tests use `MONGODB_URI` and require Atlas or the upstream
local-Atlas fixture plus an embedding provider. Do not run them against a
shared or production namespace. The product adapter should use product-owned
configuration rather than accidentally making this upstream test variable its
permanent public contract.

#### 5. Provision MongoDB Atlas and Vector Search

Atlas setup is external and cannot be completed in `references/`. For the live
product path:

1. Create or select an Atlas organization, project, and supported database
   deployment.
2. Create an application-specific **database user** with access only to the
   intended development databases. Atlas UI users and database users are
   separate identities.
3. Allow the development machine/runner through the Atlas project IP access
   list, private endpoint, or approved network path. Do not use an unrestricted
   network rule as a committed default.
4. Store the `mongodb+srv://...` connection string only in ignored local
   configuration or a secret environment. Never commit it or place it in an
   agent prompt.
5. Allocate a unique database/collection namespace for each worktree or test
   owner so concurrent runs cannot publish, revoke, or clean up each other's
   procedures.
6. After the product's procedure schema is implemented, create its Vector
   Search index over the stored embedding field and every metadata field used
   for mandatory prefiltering. Set `numDimensions` to the actual representation
   dimension (1024 for the initial EverOS-aligned model), use the declared
   similarity metric, and wait for the index to become queryable.
7. Embed stored documents and queries with the same pinned model and
   preprocessing contract. Record the model/revision, effective dimension,
   sanitizer version, and metric as the representation fingerprint.
8. Verify a driver connection, a scoped write/read, and an actual scoped Vector
   Search hit through the product adapter. A package import or ordinary MongoDB
   write is not proof that the required Atlas search path works.

The accepted product now owns its procedure schema and Atlas adapter. A live run
still requires an authorized disposable namespace, matching Vector Search index,
and credentials; local adapter tests do not establish that live claim. MongoDB's
[connection prerequisites](https://www.mongodb.com/docs/atlas/connect-to-database-deployment/)
cover database users and network access, and its
[Vector Search contract](https://www.mongodb.com/docs/atlas/atlas-search/operators-collectors/vectorsearch/)
requires query-vector dimensions to match the index and documents/queries to
use the same embedding model.

### Current seed readiness

| Item | Current state |
| --- | --- |
| Source trees, ROOT files, locks, licenses, and product specifications | Ready |
| Real Git ownership for `worktree_example` | Independent Git repository on clean `main` at the accepted STEP-03 baseline |
| Harness absolute configuration | Correct for the current example path; recompute after every copy |
| Harness run state | Completed native lanes are accepted/retired; no implementation lane is active during this planning pause |
| EverOS and `langchain-mongodb` virtual environments | Created locally from their frozen lockfiles; ignored and never copied to another worktree |
| Accepted product behavior | STEP-01 foundation, STEP-02 reviewed EverOS experience, and STEP-03 trusted procedure/Atlas lifecycle |
| Atlas live evidence | Not yet established; the last check had no configured live URI/database, so only that claim remains unavailable |
| Remaining work | STEP-04 preparation/dispatch, STEP-05 durable operations, and STEP-06 integrated local/live/native proof |

Therefore the references are already prepared as far as a portable reference
can be. The repeatable activation steps above—not copied machine state—are what
turn each new product worktree into an isolated development runtime.

## Development entry points

- Base harness: `development/product/worktree_example/harness/orchestrator_harness/`
- Outer implementation harness: `development/dogfood/harness/`
- Active specification and plan: `.plans/memory-backed-harness/`
- Native worktrees: `development/product/worktree_example/.harness-runtime/worktrees/`
- Harness setup/composition: `orchestrator_harness/setup.py`
- EverOS: `harness/vendor/everos/src/everos/` (Python 3.12+, `uv sync`)
- Atlas integration: `harness/vendor/langchain-mongodb/libs/langchain-mongodb/`
- ROOT skills: `development/product/worktree_example/.agents/skills/`

Resume at STEP-04 through the native outer harness. Every task card must include
absolute paths to the shared `PLAN.md` and its assigned step because product
worktrees do not contain the top-level `.plans` tree.

## Git status note

The outer assembly repository and the active product repository have separate Git
ownership. The supplied reference directories were relocated beneath
`references/` after their submodule metadata was created, so their checked-in
`.git` indirection files still point one level too shallow. The active
`worktree_example` is an independent repository with `main` as its symbolic
`HEAD`; its former stale pointer was moved recoverably to
`development/product/worktree_example.git-export-pointer.backup`.

Consequences:

- `git -C references/<repo> ...` may fail even though the root `.git/modules/`
  object stores remain. `git -C development/product/worktree_example ...` is
  the active product repository and works normally.
- Treat the reference directories as read-only source snapshots.
- Create implementation lanes only through the native harness under the product
  repository's `.harness-runtime/worktrees/` tree.

This assembly does not rewrite reference Git internals. Do not hand-edit their
stale pointers or make multiple mutable trees share one submodule worktree
record.

## Updating the seed

Refresh components deliberately, one owner at a time:

1. Update the reference checkout through its real Git repository.
2. Record the new identity and inspect licenses, setup behavior, and overlapping
   provider files.
3. Recopy the selected tree without nested `.git` metadata.
4. Reapply only documented composition changes (currently the active
   `root_workspace` and product-root runtime ignore).
5. Run structural/hash checks, the ROOT workspace validator, focused component
   tests, and then the product's required synthetic/native verification as the
   implementation matures.

Never treat a successful copy, retrieval hit, generated skill, plan draft, or
database write as product success. Success remains the linked ROOT review and
acceptance result for the actual execution.
