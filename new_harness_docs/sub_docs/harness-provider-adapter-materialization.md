# Proposed simple adapter file bridge

Updated: 2026-08-24.

> **Status: current detailed v2 target contract.** This is the adapter
> materialization design under the master planning decision index; candidate
> binding behavior mentioned elsewhere is background, not a competing protocol.

## Scope

This document describes the pointed neutral harness only:

```text
<root-workspace>/<harness-root>
```

It is a proposed user-facing adapter format. It does not ask an adapter author
to edit the generic controller, change the super-cache design, or alter the
frozen firmware campaign. It does require one strict provider-specific launcher
binding module, supplied in the adapter and loaded by the generic controller.

## Two guides, two audiences

The finished harness should lead users with only these two guides:

```text
<harness-root>/README.md
<harness-root>/adapters/README.md
```

The harness-root `README.md` is the operator guide. It tells ROOT how to choose
an already-shipped binding, fill the fixed config and resource manifest, run
`operator_launch harness setup`, check the generated runtime records, and only
then request a lane bootstrap/launch. The public launcher creates and retires
epoch/lane records; ROOT does not edit them. This guide links here only when
ROOT needs a provider that is not already shipped.

`adapters/README.md` is the adapter-author guide. It tells an author exactly
which small files to create in `root/`, `super-cache/`, and `harness/`; setup
then copies those files to their fixed destinations. It does not tell ROOT to
hand-install hooks, edit a worktree, or run a separate provider setup process.

The standard Codex, Claude Code, and Qwen Code adapter trees already ship with
the product. ROOT normally reads only the harness-root `README.md` and selects
one of those bindings.

## The actual model

The harness already owns the generic machinery:

- the always-enabled shared `<runtime-root>/super-cache`;
- the generic result-check, launcher binding, and monitor processes; and, in the
  explicitly selected managed profile only, hook-dispatch, queue, and worker
  notification processes;
- setup, bootstrap, worktree creation, cache copying, process ownership, and
  provider launch orchestration; and
- built-in Codex, Claude Code, and Qwen Code bridge examples.

An adapter author does **not** change any of that. They write a few
provider-specific project bridge files plus one strict launcher binding in one
adapter folder. Setup first makes the active runtime cache from the shipped
`<harness-root>/super-cache` source tree, then copies adapter project files into
that active cache and the ROOT workspace. It registers the launcher binding under
the harness root. Every lane bootstrap copies base active-cache content into its
worktree. Only managed bootstrap copies the selected adapter's provider hook,
queue, notification, and worktree-configuration payload.

An adapter is therefore a small, controlled filesystem payload: project files
for ROOT and workers, plus one module that translates generic launch data into
that provider's real CLI invocation. It is not an installer, a second
controller, or a separate process manager.

## Exact adapter layout

```text
<harness-root>/adapters/<provider-id>/
  README.md                 # tells an agent exactly what to put below
  root/                     # setup copies this tree into ROOT's workspace root
  super-cache/              # setup copies this tree into the shared super-cache
  harness/
    launcher_binding.py      # setup registers this exact provider launch binding
  shipped-machinery/        # optional reference copies; never copied or executed
```

`root/`, `super-cache/`, and `harness/launcher_binding.py` are setup source
payloads, not runtime state themselves. Setup materializes `root/` as static
ROOT project files, makes `super-cache/` part of the active runtime cache, and
registers `launcher_binding.py` as harness code. `README.md` and
`shipped-machinery/` are documentation for the person or agent writing the
adapter.

Setup does exactly this, preserving paths below each source folder. The cache
destination below is the active working copy; setup never copies an adapter
payload into the shipped `<harness-root>/super-cache` source tree:

```text
adapter/root/         -> <configured-ROOT-workspace>/
adapter/super-cache/  -> <runtime-root>/super-cache/adapter-payloads/<provider-id>/
adapter/harness/launcher_binding.py
                     -> <harness-root>/orchestrator_harness/provider_adapters/<provider-id>/launcher_binding.py
```

Each provider's managed payload lands under its own
`adapter-payloads/<provider-id>/` namespace; the provider-neutral base that every
worktree receives lives under `super-cache/workspace/`. Plain bootstrap copies
`workspace/` only; managed bootstrap copies `workspace/` plus the selected
provider's `adapter-payloads/<provider-id>/`. See resolution R10 in
`harness_single.md`.

Before copying anything, setup calculates every destination in all three trees.
In normal mode, if **any destination file already exists**, setup fails and copies
nothing. Existing directories may be reused; files are never merged, replaced, or
adopted. This applies equally to a provider settings file, wrapper, skill, or
launcher binding.

ROOT may deliberately request a replacement with:

```text
operator_launch harness setup --overwrite
```

`--overwrite` applies only to the complete, preflighted set of known harness/adapter
destination files. It is not permission to overwrite arbitrary files elsewhere in
the ROOT workspace. Setup reports every replaced path, stages the replacement set
first, and restores the prior files if a late write fails. It does not overwrite the
active runtime cache or resource manifest; those retain their separate refresh and
active-epoch rules.

`<provider-id>` is the adapter's fixed declared provider name, not text copied
from a lane prompt. The generic controller loads only the binding at that exact
registered path inside the harness code tree for a selected provider ID. It does
not execute an arbitrary Python path supplied by ROOT or a worker.

The product ships one such adapter tree for each standard provider. In this
document, `adapter/` means the tree selected from the catalog, for example:

```text
<harness-root>/adapters/codex/
<harness-root>/adapters/claude-code/
<harness-root>/adapters/qwen-code/
```

Each tree has the same `root/`, `super-cache/`, and
`harness/launcher_binding.py` layout shown above. Setup installs/checks the
complete shipped catalog so a later lane launch can use any shipped provider;
setup materializes all shipped standard ROOT payloads in the ROOT workspace.

More literally, each fresh controller process reads only the invocation's
`provider.id`, validates it as a safe provider identifier, derives the one fixed
path above, loads that one file, and checks that its `PROVIDER_ID` matches. It
does this before normal invocation validation checks whether the provider is
registered. The generic loader then registers the binding in that controller
process. No outside wrapper process calls registration, and no lane input can
supply a Python module path.

For example:

```text
adapter/root/.example-cli/settings.json
    becomes
<ROOT-workspace>/.example-cli/settings.json

adapter/super-cache/.example-cli/hooks/harness-stop.py
    becomes
<runtime-root>/super-cache/adapter-payloads/example-cli/.example-cli/hooks/harness-stop.py
    and then, for every managed lane,
<lane-worktree>/.example-cli/hooks/harness-stop.py
```

There is no caller-supplied path registry, arbitrary binding writer, custom
installer, or per-lane cache-source choice. Every lane uses the same active
shared cache as its source. Bootstrap copies the common base cache tree plus,
for a managed lane only, the shipped provider payload selected for that lane; it
does not copy the other provider payloads into that worktree. A plain lane
deliberately receives neither hook/config payload nor manager-notification skill,
but it still receives the same provider launch binding and normal
controller/result contract. The launcher binding has one additional fixed
registration path because it is used by the controller, not by a CLI project
configuration file.

## ROOT is already running; bootstrap chooses only the lane binding

No bootstrap program or adapter chooses a provider or model. ROOT is the
already-running CLI in the project workspace; it is not represented by a
`root_provider`, `root_model`, session ID, or dynamic provider binding in the
harness configuration.

`operator_launch harness setup` materializes all shipped standard ROOT payloads
in `root_workspace`: `.codex/`, `.claude/`, and `.qwen/`. It also materializes
any static custom ROOT adapter payload that was installed before setup. The
active ROOT CLI simply discovers the files at its native project path. In the
managed profile every ROOT hook wrapper opens the same fixed runtime manager
queue and cross-checks its epoch/queue IDs against `CURRENT_EPOCH.json`; neither
record identifies a ROOT provider, model, or session. In the plain profile, the
static wrapper's explicit no-op branch opens no queue, emits no notice, and
applies no Stop gate.

For each new lane, ROOT provides an explicit provider and model in the public
prepare request, for example:

```text
operator_launch lane bootstrap \
  --lane-id lane-001 \
  --provider claude-code \
  --model <chosen-Claude-model> \
  ...
```

The bootstrap program reads those ROOT-supplied values. It validates the
provider against the shipped adapter catalog, finds the fixed matching payload,
and, for a managed lane, copies its worktree configuration/hooks into the new
worktree. A plain lane skips that feature payload while retaining the selected
launcher binding. Both write the provider/model values into the prepared
invocation. The later public lane-launch command consumes that frozen invocation;
it does not choose or replace the provider/model. If a public API combines
preparation and launch, ROOT still supplies the two values to that single call
before any worktree/provider process exists.

The binding ID is a small fixed identifier such as `codex`, `claude-code`, or
`qwen-code`; it is not a model string, executable path, or Python path. The
generic launcher writes it to `provider.id` in the invocation, validates it,
and loads only this deterministic file:

```text
<harness-root>/orchestrator_harness/provider_adapters/<binding-id>/launcher_binding.py
```

The selected binding passes the separately recorded model value in the provider
CLI's normal syntax. Selecting `codex` does not force every Codex lane to use
the same underlying model, and a model name never selects a filesystem path.

The shipped catalog contains Codex, Claude Code, and Qwen Code templates and
bindings at the same time. Setup installs/checks every shipped lane binding;
the active shared cache retains every shipped worker payload. Therefore ROOT
can use Codex while concurrently launching, for example, a Claude lane and two
Qwen lanes with different Qwen model values. Their separate worktrees and
separate invocation files prevent one lane's provider/model choice from
altering another's.

Setup does **not** filter the super-cache by ROOT or by a lane's binding. The
product-owned shared cache contains all shipped standard
provider payloads side by side. Bootstrap copies the common tree into every
worker and materializes only the selected provider payload into that worker's
normal provider path, such as `.codex`, `.claude`, or `.qwen`. Cache setup
therefore needs no per-lane provider argument, but the public lane bootstrap
request does: ROOT provides it so bootstrap knows which shipped payload to use.

ROOT setup always places the common ROOT skills and native hook wrappers for all
shipped providers at their normal provider paths. A static custom adapter uses
the same pattern. Changing which already-running ROOT CLI is used therefore
does not require a runtime rebind, a second cache, or changed worker overlays.

## What the adapter README is for

`adapter/README.md` must let an agent take a supported CLI and fill the two
adapter folders without touching harness code. It is an authoring instruction,
not a request to redesign the harness.

### Built-in providers versus a new provider

The README is a checklist for adding a **new provider CLI binding**, not for
choosing a different foundation model behind an existing CLI. For example, a
different Codex model still uses the shipped `codex` binding and passes its
model name through the normal `--model` option. It does not need another
adapter.

Codex, Claude Code, and Qwen Code are product-owned built-in bindings. The
harness repository must already contain their complete, materialization-ready
payloads: ROOT files, super-cache files, and `launcher_binding.py`. Setup copies
those shipped files to their fixed destinations; a caller does not write or
complete an adapter for those three providers.

For a new, ordinary supported provider CLI, the adapter README is the single
authoring checklist. The author fills exactly these three payload locations:

| Adapter location | The author writes | Setup copies it to |
| --- | --- | --- |
| `root/` | The provider's ROOT configuration, PostToolUse and Stop wrappers, plus the `manager-notification-watch`, `acknowledge-manager-notification`, `close-manager-notification`, `review-lane-completion`, `send-lane-notification`, `resume-lane`, and `harness-shutdown` skills. | The configured ROOT workspace, preserving paths. |
| `super-cache/` | The provider's **managed-worker** configuration, PostToolUse and Stop wrappers, optional native-notification wrapper, plus the `manager-notify` and `lane-assignment` skills. | The one shared super-cache, preserving paths; managed bootstrap then copies it into the selected worker. Plain bootstrap omits this feature payload and copies only base cache content. |
| `harness/launcher_binding.py` | The strict `PROVIDER_ID`, `ADAPTER_VERSION`, `build_argv`, and `parse_line` binding. | The fixed registered provider path inside harness code. |

The README must say that an empty required item is an adapter-authoring error,
not a reason to add a special case to setup. Setup preflights all three payloads
and fails without copying anything on a target-file collision. An exotic CLI
that cannot meet the documented command/stdout/hook boundary remains unsupported;
the author does not add a daemon, relay, or custom process manager to its adapter.

## Exact contents of `adapter/README.md`

The README must contain this checklist, in this direct form. The later sections
in this document give the detailed contract behind each item.

### 1. Provider facts

State the provider/binding ID, executable command, tested version range, project
configuration path, hook-wrapper directory, ROOT skill directory, worker skill
directory, start command syntax, resume command syntax, and the standard-output
records used to find a session ID and terminal outcome. State whether the CLI has
native PostToolUse, Stop, and optional notification events.

### 2. Required `adapter/root/` files

List the literal provider paths for:

```text
<provider configuration file>
<hook directory>/post-tool wrapper
<hook directory>/stop wrapper
<skill directory>/manager-notification-watch/SKILL.md
<skill directory>/acknowledge-manager-notification/SKILL.md
<skill directory>/close-manager-notification/SKILL.md
<skill directory>/review-lane-completion/SKILL.md
<skill directory>/send-lane-notification/SKILL.md
<skill directory>/resume-lane/SKILL.md
<skill directory>/force-stop-lane/SKILL.md
<skill directory>/harness-shutdown/SKILL.md
```

State that the configuration registers the real PostToolUse-equivalent and Stop
events. State the exact native response shape for a non-blocking ROOT notice and
for a rejected/allowed ROOT Stop. The wrappers call the generic harness dispatcher;
they do not read or edit queue files themselves.

### 3. Required managed `adapter/super-cache/` files

List the literal provider paths for:

```text
<provider configuration file>
<hook directory>/post-tool wrapper
<hook directory>/stop wrapper
<skill directory>/manager-notify/SKILL.md
<skill directory>/lane-assignment/SKILL.md
```

If the provider supports a useful native notification event, list its optional
wrapper and configuration declaration too. State that the worker PostToolUse
wrapper checks only the local incoming queue, while the Stop wrapper rejects
unresolved local assignments or an invalid `RESULT.json` through the generic
harness checker.

State the two worker skills exactly:

- `manager-notify`: call the declared `.agent-workspace/manager-notify.py`
  helper when ROOT intervention is needed; do not edit a queue file.
- `lane-assignment`: use the declared `.agent-workspace/lane-queue.py` helper
  to acknowledge, complete, or block a ROOT assignment; a block also calls
  `manager-notify.py`; never edit either queue directly.

### 4. Required harness binding

Require exactly this file:

```text
adapter/harness/launcher_binding.py
```

It must define `PROVIDER_ID`, `ADAPTER_VERSION`, `build_argv(...)`, and
`parse_line(...)`. State that it creates an argument array for start/resume and
parses only a session ID or a terminal fact. It does not manage processes,
worktrees, queues, hooks, cleanup, or credentials.

### 5. Files and behavior that are forbidden

Forbid lane-specific bindings, `QUEUE.json`, `manager-notify.py`,
`lane-queue.py`, `RESULT.json`, completion-review/acceptance files, credentials,
daemons, relays, and custom process managers. State that setup fails rather than
overwriting or merging any target file, including a settings file, wrapper, skill,
or launcher binding.

### 6. Required host-only proof

Require proof that setup copies all ROOT, super-cache, and launcher-binding files
to their fixed paths; the CLI discovers its hooks and all ten skills (eight ROOT
plus the two managed worker skills, `manager-notify` and `lane-assignment`); a real
PostToolUse hook runs; the Stop hook rejects unresolved work and invalid results;
new and resumed launches use the binding; and each possible destination-file
collision leaves no partial copy. No firmware, MCP server, or hardware is needed.

The README must also state this boundary: Codex, Claude Code, and Qwen Code already
ship completed versions of this payload in the harness. This checklist is for a
new supported CLI binding, not for selecting a different underlying model through
one of those existing providers.

The README must specify every item below.

### 1. CLI facts and destination paths

State:

- provider/CLI name and executable command;
- tested version or version range;
- project-root directory used by the CLI;
- project hook configuration path;
- project hook-wrapper directory; and
- worker and ROOT skill directories, if the CLI supports project-local skills.

For the existing bridge examples, those paths are:

| CLI | Hook configuration | Hook wrapper directory | Skill root |
| --- | --- | --- | --- |
| Codex | `.codex/hooks.json` | `.codex/hooks/` | `.codex/skills/` |
| Claude Code | `.claude/settings.json` | `.claude/hooks/` | `.claude/skills/` |
| Qwen Code | `.qwen/settings.json` | `.qwen/hooks/` | `.qwen/skills/` |

For another CLI, the adapter author writes that CLI's equivalent paths below
`adapter/root` and `adapter/super-cache`.

### 2. Exact files the agent must create in `adapter/root`

The README must give a literal file list for ROOT. Usually this is:

```text
adapter/root/<provider-config-path>                 # registers ROOT hooks
adapter/root/<provider-hook-directory>/post-tool.* # calls generic ROOT notice route
adapter/root/<provider-hook-directory>/stop.*      # calls generic ROOT Stop route
adapter/root/<provider-skill-root>/manager-notification-watch/SKILL.md
adapter/root/<provider-skill-root>/acknowledge-manager-notification/SKILL.md
adapter/root/<provider-skill-root>/close-manager-notification/SKILL.md
adapter/root/<provider-skill-root>/review-lane-completion/SKILL.md
adapter/root/<provider-skill-root>/send-lane-notification/SKILL.md
adapter/root/<provider-skill-root>/resume-lane/SKILL.md
adapter/root/<provider-skill-root>/force-stop-lane/SKILL.md
adapter/root/<provider-skill-root>/harness-shutdown/SKILL.md
```

The configuration file must register the CLI's actual PostToolUse-equivalent
and Stop-equivalent events, pointing at the wrapper files in the same tree.

The ROOT PostToolUse wrapper calls the existing generic harness process, which
opens the fixed runtime manager queue and validates its IDs against
`CURRENT_EPOCH.json`. It must return the CLI's native non-preempting
notice response while any ROOT event remains unacknowledged. The exact notice
says that ROOT must finish its current task, then use the
`acknowledge-manager-notification` skill to read the queue and acknowledge the
specific top-level event IDs it actually read. It must not tell ROOT to edit the
queue file directly.

The ROOT Stop wrapper calls the existing generic ROOT Stop process. It must
return the CLI's native reject-completion response while manager items are
`PENDING` or `ACKNOWLEDGED`, and native allow-completion response after ROOT
has resolved them.

The eight ROOT skills use the harness's existing public commands (the eighth, `force-stop-lane`, invokes `lane force-stop`). They do not
implement polling, queue mutation, bindings, or hooks themselves.

`adapter/root/<provider-skill-root>/manager-notification-watch/SKILL.md`
must say exactly when ROOT uses `watch --until-actionable`: only after ROOT has
finished its current task and is deliberately waiting for worker activity. The
skill must say that this command occupies the current ROOT CLI session while it
waits; ROOT must not start it while actively working, and must handle the
returned actionable report before starting another wait. It is an operational
instruction for ROOT, not a background process or a replacement queue.

`adapter/root/<provider-skill-root>/acknowledge-manager-notification/SKILL.md`
must say: after finishing the current ROOT task, inspect the fixed runtime manager
queue read-only; for every top-level event ID ROOT actually read, run:

```text
operator_launch manager acknowledge --event-id <top-level-event-id>
```

It must say that this command, rather than direct JSON editing or a transport
`DELIVERED` record, changes acknowledgement. The skill must not acknowledge an
event ROOT has not inspected.

`adapter/root/<provider-skill-root>/close-manager-notification/SKILL.md` must
say: after ROOT has completed an acknowledged ordinary manager notification, run
`operator_launch manager close --event-id <id> --outcome COMPLETE|BLOCKED
--summary "<what ROOT did or needs>"`. Do not close an event ROOT has not read,
edit `QUEUE.json`, or start a lane. Completion review closes its own event through
the completion-review command rather than this generic route.

`adapter/root/<provider-skill-root>/review-lane-completion/SKILL.md` must say:
after ROOT reads and acknowledges a `COMPLETION_REVIEW_REQUIRED` event, compare
the copied task criteria, result, and evidence; then run
`operator_launch lane completion-review --event-id <id> --review-outcome
PASS|FAIL|BLOCKED --approval ACCEPTED|REJECTED --review-summary "<reason>"`.
It must explain that `--review-outcome` and `--approval` are two independent fields
given together on every call — the factual finding versus ROOT's separate
accept/reject decision, not alternatives, with `ACCEPTED` requiring a `PASS`
finding — and forbid direct edits of review, acceptance, lane, or queue files. A
`REJECTED` approval creates a separate ROOT queue event; the skill must not
automatically run resume. If the public command returns
`COMPLETION_REVIEW_STALE_SOURCE`, ROOT normally resumes the lane; after inspecting
the difference, ROOT may use `--force-accept --force-reason "<reason>"` only for a
structurally valid current chain it judges harmlessly changed.

`adapter/root/<provider-skill-root>/resume-lane/SKILL.md` must direct ROOT to
the public `resume-lane` command when a lane has stopped but remains unaccepted.
It supplies a new resume task card, a truthful rationale, and current resume
instructions. It must say not to reconstruct a session ID, PID, worktree,
invocation file, or hash-amendment record by hand. `LANE_RUNNING` means ROOT
uses the live-lane route instead; `ALREADY_ACCEPTED` is never bypassed; and a
provider's expired-session error is reported rather than turned into a fresh
provider session.

`adapter/root/<provider-skill-root>/harness-shutdown/SKILL.md` is ROOT-only.
It tells ROOT to use `operator_launch harness shutdown` only when intentionally
ending the harness run. It must say not to close a terminal, kill by process
name, or edit process records. The command closes live lanes through their normal
cleanup route, then stops the persistent monitor, and refuses success if either
cleanup cannot be proved. On failure, preserve the command output and runtime
state for investigation; do not retry with broad process kills.

`adapter/root/<provider-skill-root>/force-stop-lane/SKILL.md` is ROOT-only. It
tells ROOT to use `operator_launch lane force-stop --lane-id <lane-id>` to
hard-stop a single stuck lane — for example a `cleanup_unproven` lane whose
processes will not exit, or a lane whose controller is itself wedged. It must say
the command terminates that lane's provider, helper, and controller processes
(matched by the identities in `lane.json`), force-releases any exclusive lease the
lane held, and marks the lane retired — and that this is a deliberate forced action
whose safety ROOT owns. It must say to target exactly one lane by `--lane-id` and to
use `harness shutdown` for the whole runtime instead; and not to close terminals,
kill by broad process name, or edit lease/process records.

### 3. Exact files the agent must create in `adapter/super-cache`

The README must give a literal file list for worker worktrees. Usually this is:

```text
adapter/super-cache/<provider-config-path>                 # registers worker hooks
adapter/super-cache/<provider-hook-directory>/post-tool.* # calls generic worker notice route
adapter/super-cache/<provider-hook-directory>/stop.*      # calls generic worker Stop/result route
adapter/super-cache/<provider-skill-root>/manager-notify/SKILL.md
adapter/super-cache/<provider-skill-root>/lane-assignment/SKILL.md
```

If the CLI has a useful native notification event, the adapter may also add:

```text
adapter/super-cache/<provider-hook-directory>/notification.*
```

and the corresponding event declaration in its configuration. This is only an
extra notice route. The adapter must still work through PostToolUse and Stop,
because not every CLI has a notification event.

In a managed worktree, the worker PostToolUse wrapper calls the existing generic worker notice route.
It reads only that lane's local `.agent-workspace/QUEUE.json` through the
binding the generic bootstrap already wrote.

In a managed worktree, the worker Stop wrapper calls the existing generic worker Stop/result route.
That process blocks completion if the lane has unresolved local assignments or
`RESULT.json` is missing, malformed, or names the wrong task/lane/invocation.
It permits structurally valid `PASS`, `FAIL`, and `BLOCKED` results. The
adapter wrapper only translates its result to the CLI's real hook protocol.

In a managed worktree, the worker `manager-notify` skill tells the worker to call the existing
`.agent-workspace/manager-notify.py` helper when it needs ROOT intervention.

In a managed worktree, the worker `lane-assignment` skill covers the other direction: ROOT has placed
an assignment in this worker's local incoming queue. It tells the worker to use
the lane's declared `.agent-workspace/lane-queue.py` helper to move that one
assignment from `PENDING` to `ACKNOWLEDGED`, then to `COMPLETE` or `BLOCKED`.
For `BLOCKED`, it also calls `manager-notify.py` with the decision ROOT must
make. It never edits `QUEUE.json`, ROOT's manager queue, or another lane's
queue directly.

The shipped active super-cache must already contain this managed worker skill
at all three standard paths: `.codex/skills/manager-notify/SKILL.md`,
`.claude/skills/manager-notify/SKILL.md`, and
`.qwen/skills/manager-notify/SKILL.md`. Managed bootstrap copies the selected
provider's copy along with the rest of its feature payload; a plain bootstrap
does not. For a custom
supported CLI, the adapter author supplies the equivalent skill under that
CLI's `adapter/super-cache` skill path. It gives the same instruction to call
the existing helper, rather than making the worker edit a queue file.

The same shipped cache must contain managed `lane-assignment/SKILL.md` at the matching
`.codex/skills`, `.claude/skills`, and `.qwen/skills` paths. A custom supported
CLI supplies that equivalent in its `adapter/super-cache` payload. The selected
worker reads its own provider-local copy; every other provider's copy stays inert.

## Published generic bridge contract used by every adapter

Before an agent writes an adapter, the harness must already expose this one
provider-neutral contract. It is product machinery. An adapter author uses it;
they do not inspect, copy, or change its code.

Every **managed** worker worktree contains this generic binding file, written by
bootstrap. A plain worktree deliberately does not:

```text
.agent-workspace/harness-hook-binding.json
```

It contains the worker role, lane/invocation identity, and the exact local queue
path the generic worker hook process may read. It is not an adapter file. ROOT
never receives this file: its static hook wrapper invokes the generic ROOT
dispatcher, which resolves the fixed runtime manager queue from the harness
configuration and cross-checks its IDs against `CURRENT_EPOCH.json`.

Every managed worker adapter wrapper calls this one public command from its
worktree:

```text
python .agent-workspace/hook-dispatch.py --boundary <boundary>
```

Each ROOT adapter wrapper instead calls the same generic dispatcher through the
installed harness entry point with `--boundary root-post-tool-use` or
`--boundary root-stop`. It receives no provider/session binding file and, in
managed mode, uses `<runtime-root>/manager/QUEUE.json`. Its explicit plain-mode
branch returns without opening that path.

The only permitted boundary values are:

```text
root-post-tool-use
worker-post-tool-use
root-stop
worker-stop
```

The wrapper gives the command the provider's raw hook payload on standard
input. The command writes exactly one JSON object on standard output:

```json
{"decision":"ALLOW"}
```

```json
{"decision":"NOTICE","notice":"<short direct message>"}
```

```json
{"decision":"REJECT","reason":"<specific truthful reason>"}
```

`ALLOW` means the wrapper returns the provider's native allow response.
`NOTICE` means it returns the provider's native non-blocking notice response.
`REJECT` means a Stop wrapper returns that provider's native continue/reject
response. A PostToolUse wrapper reports `REJECT` as an honest hook diagnostic;
it does not invent an acknowledgement.

The generic command applies the existing harness rules:

| Boundary | Generic behavior |
| --- | --- |
| `root-post-tool-use` | Reads only ROOT's manager queue and returns `NOTICE` after every tool boundary while one or more events are unacknowledged. The notice names the `acknowledge-manager-notification` skill; it never edits or acknowledges an event. |
| `worker-post-tool-use` | Reads only this worker's local queue and returns `NOTICE` when a local assignment is pending. |
| `root-stop` | Returns `REJECT` while ROOT manager work is `PENDING` or `ACKNOWLEDGED`; otherwise `ALLOW`. |
| `worker-stop` | Returns `REJECT` while local work is unresolved or `RESULT.json` fails the existing result check; otherwise `ALLOW`. |

The `worker-stop` route uses the existing `result-stop-check.py` internally.
The adapter does not invoke a second result checker and does not parse result
rules itself.

If this binding file, command, boundary set, or JSON response contract is not
already available in the harness, a file-only adapter cannot make that CLI work
honestly. That is a harness capability gap, not something the adapter author
is expected to repair.

## Strict but small harness-side `launcher_binding.py`

Project hook files tell a CLI what to do *after it has started*. They cannot tell
the generic controller how to invoke that CLI or recognize its session ID. Every
provider adapter therefore supplies exactly one small harness-side file:

```text
adapter/harness/launcher_binding.py
```

Setup copies it to the fixed registered provider path shown above. The generic
controller loads it only for the selected provider ID. The controller still owns
the worktree path, `Popen`, process tracking, locks, queue/binding files, cleanup,
controller status, environment setup, result checks, and all hook decisions.

The binding has only two required functions and two identity constants:

```python
PROVIDER_ID = "example-cli"
ADAPTER_VERSION = "example-cli-v1"

def build_argv(action, prompt, session_id, launch_options):
    """Return this CLI's argument array for start or resume."""

def parse_line(line):
    """Return a session ID and/or terminal fact from one output line."""
```

`build_argv` receives either `start` or `resume`, the already-built prompt, and,
for resume only, the saved session ID. It returns an argument array, never a shell
string. It may reject an unsupported option or resume request with a clear error.
It does not choose a worktree, create a process, build another queue, or start a
fresh session when the saved session is bad.

`parse_line` returns only the few facts the generic controller cannot know:

```json
{"session_id": "provider-session-id"}
```

or:

```json
{"terminal": "COMPLETED", "detail": "provider's final result"}
```

The only allowed terminal values are `COMPLETED`, `FAILED`, and `CANCELLED`.
Ordinary non-terminal output is returned as `null`. The generic controller captures
all output, writes its transcript, and treats an unexplained non-zero exit as
`FAILED`; the binding does not need a separate terminal-classification function.

The binding handles the unavoidable provider spelling: for example, Codex's
headless command and resume form, Claude Code's print/stream-JSON command, or
Qwen Code's equivalent. It may add documented model/permission flags from
`launch_options`, but it must never put credentials in command arguments.

Everything else is generic. Prompt text is UTF-8; the controller supplies the
worktree working directory; it preserves normal user/project configuration; it
adds the harness import path for generic hook wrappers; and it removes ROOT-only
secrets before launch. The adapter does not need separate prompt encoders,
environment mappers, command-redaction code, last-message handlers, notification
delivery methods, or capability files.

Provider notification, PostToolUse, and Stop behavior are supplied by the small
project hook/wrapper files in `root/` and `super-cache/`. They all call the same
generic harness dispatcher. The old separate `HostAdapter`/provider-delivery
implementation should be replaced by that generic route rather than copied into
every new provider adapter.

## Deliberately narrow provider support

The harness does not promise to support every AI CLI. It supports ordinary
headless coding CLIs only when they fit the same simple boundary as Codex, Claude
Code, and Qwen Code:

- start and resume can be invoked as a normal child command;
- the CLI accepts the normal UTF-8 prompt transport used by the harness;
- it communicates its machine-readable records on standard output, one record per
  line, so the small parser can find a session ID and terminal result;
- it can run from the generated worktree while retaining normal user and project
  configuration; and
- for the **managed** profile, it has project-local hook/skill files, or a
  documented equivalent that can be copied into `root/` and `super-cache/`.

A CLI that meets the ordinary launch/session/result boundary but cannot use those
hook/skill files is still supported as a **plain** lane. It receives no manager
queue, worker queue, hook payload, or lease. Nothing automatically notifies ROOT
when it changes state: ROOT must run `scan --no-write` when returning to
management work and `watch --until-actionable` while idle, then use the returned
lane status to take the direct review or resume action. Such a CLI must not be
silently admitted to the managed profile.

The adapter does not select that profile at runtime. Before setup, the operator
stores the complete plain flag combination in
`<harness-root>/harness-config.json`; setup then materializes the matching
plain facilities. No adapter, bootstrap, or launch argument may turn managed
coordination back on for one lane. Hardware locking is not part of that package:
the generic controller may lock a declared resource in either profile.

If a CLI instead needs a daemon protocol, a browser-control channel, a private
binary RPC, a separate persistent client, non-UTF-8 prompts, custom process
supervision, or another special transport, it is **unsupported**. Do not add a
new adapter framework, relay, watcher, or provider-specific service to make it
fit. A clear unsupported-provider error is the correct result.

## How to write the small bridge wrappers

The README must show the exact wrapper template for the CLI. Each wrapper does
only four things:

1. Read hook input in that CLI's documented format: standard input,
   environment variables, arguments, or another documented interface.
2. Run `python .agent-workspace/hook-dispatch.py --boundary <boundary>` from
   that prepared workspace/worktree, with the raw hook payload on standard
   input. It does not create or edit the generic binding.
3. Read the command's one JSON decision object: `ALLOW`, `NOTICE`, or
   `REJECT`.
4. Convert that decision into the CLI's exact native hook response.

The README must state the exact success and refusal response shapes. In
particular, the worker and ROOT Stop wrappers have to make the CLI actually
continue running when the generic process rejects completion. Printing an error
and exiting with success is not a valid Stop bridge.

The wrappers must not:

- implement a second queue;
- acknowledge, complete, or block queue items;
- modify `RESULT.json`;
- create a completion review or acceptance record;
- start a watcher, monitor, provider, or process tree; or
- read a different lane's queue or ROOT's manager queue from a worker.

## How to write the skill files

The README must give the literal text requirements for each skill file:

| File | Required instruction |
| --- | --- |
| ROOT `manager-notification-watch/SKILL.md` | After ROOT has completed its current task and is deliberately waiting, run the existing public `watch --until-actionable` command. It occupies that CLI session; do not use it while actively working. Handle its returned report before waiting again. |
| ROOT `acknowledge-manager-notification/SKILL.md` | After completing the current ROOT task, read the fixed runtime manager queue. For each top-level event ID actually read, run `operator_launch manager acknowledge --event-id <id>`. Never edit the queue file or treat delivery as acknowledgement. |
| ROOT `close-manager-notification/SKILL.md` | After handling an acknowledged ordinary ROOT event, run `operator_launch manager close --event-id <id> --outcome COMPLETE|BLOCKED --summary "<what ROOT did or needs>"`. Never edit the queue file, close unread work, or restart a lane. Completion review closes its own event. |
| ROOT `review-lane-completion/SKILL.md` | In managed mode, for an acknowledged `COMPLETION_REVIEW_REQUIRED` event, review the copied task/result/evidence and run `operator_launch lane completion-review --event-id <id> --review-outcome PASS|FAIL|BLOCKED --approval ACCEPTED|REJECTED --review-summary "<reason>"`. In plain mode, select the controlled terminal review-pending lane and use the identical command with `--lane-id <id>`. Never hand-edit review, acceptance, lane, or queue files. The factual review outcome and ROOT approval are separate. A stale-source error normally means resume; `--force-accept --force-reason` is available only after ROOT inspected a harmless current-record difference. A managed rejection produces `LANE_RESUME_REQUIRED`; a plain rejection returns direct resume-required output. Use `resume-lane` only after that result. |
| ROOT `send-lane-notification/SKILL.md` | Use the existing public send-lane-notification command with the lane ID and prompt. |
| ROOT `resume-lane/SKILL.md` | For a stopped, unaccepted lane, use the public `resume-lane` command with a new resume task card, truthful rationale, and current instructions. Do not reconstruct a session, PID, worktree, invocation, or amendment/hash record. |
| ROOT `force-stop-lane/SKILL.md` | To hard-stop one stuck lane (e.g. `cleanup_unproven` that will not clear, or a wedged controller), use `operator_launch lane force-stop --lane-id <id>`. It terminates that lane's provider/helper/controller processes, force-releases its lease, and marks it retired. Use for one lane; use `harness shutdown` for the whole runtime. Do not kill by broad process name or edit lease/process records. |
| ROOT `harness-shutdown/SKILL.md` | When intentionally ending the harness run, use `operator_launch harness shutdown`. Do not close terminals, kill by broad process name, or edit process records. Preserve failed shutdown evidence; do not retry with broad kills. |
| Worker `manager-notify/SKILL.md` | Managed profile only: when ROOT intervention is needed, run `.agent-workspace/manager-notify.py` with the decision/action needed. Do not hand-edit manager queue files. Plain lanes do not receive this skill. |
| Worker `lane-assignment/SKILL.md` | Managed profile only: for a ROOT assignment, use the declared `.agent-workspace/lane-queue.py` helper to acknowledge, complete, or block it. Escalate a block with `manager-notify.py`; never hand-edit either queue. Plain lanes do not receive this skill. |

The shipped product supplies all ten standard skill files for Codex, Claude
Code, and Qwen Code: the eight ROOT skills through `adapter/root`, and the two
worker skills through the shared cache. A custom supported CLI must include the
same ROOT skills in `adapter/root` and the same worker skills in
`adapter/super-cache`. Setup copies them to the central locations and managed
bootstrap copies the worker tree into its worktree. The README must also say whether the
CLI requires a fresh session after these skills or its project configuration are
copied.

## Existing Codex, Claude Code, and Qwen Code bridge references

The optional `adapter/shipped-machinery/` folder can hold copies of the known
working bridge files as templates. They exist solely to show an adapter author
what they need to imitate for another CLI.

The current harness's corresponding provider-specific files are:

| CLI | Configuration and bridge files |
| --- | --- |
| Codex | `.codex/hooks.json`; `.codex/hooks/orchestrator_harness_post_tool_use.py`; `.codex/hooks/orchestrator_harness_stop.py`; `.codex/hooks/orchestrator_harness_bounded_policy.py`; `.codex/policies/bounded-launchers.json`; `.codex/policies/bounded-exclusions.gitignore` |
| Claude Code | `.claude/settings.json`; `.claude/hooks/orchestrator_harness_post_tool_use.py`; `.claude/hooks/orchestrator_harness_stop.py` |
| Qwen Code | `.qwen/settings.json`; `.qwen/hooks/orchestrator_harness_post_tool_use.py`; `.qwen/hooks/orchestrator_harness_stop.py`; `.qwen/hooks/orchestrator_harness_notification.py` |

Their native event registrations are:

| CLI | Registered events |
| --- | --- |
| Codex | `PostToolUse` matcher `.*`; `Stop`; and `PreToolUse` matcher `^(Bash|shell_command)$` for bounded policy. |
| Claude Code | `PostToolUse` matcher `.*`; `Stop` matcher `.*`. |
| Qwen Code | `Notification` matcher `idle_prompt`; `PostToolUse` matcher `*`; `Stop`. |

An agent writing an adapter for another CLI copies the *pattern*: configuration
declares native hooks; thin bridge wrappers call generic existing harness
processes; skills give the same worker/ROOT instructions in that CLI's own skill
format and path. It does not copy a Codex file into a different CLI unchanged.

## Things an adapter author must not write

The README must explicitly forbid static copies of these lane-specific files:

```text
.agent-workspace/QUEUE.json
.agent-workspace/manager-notify.py
.agent-workspace/lane-queue.py
.codex/orchestrator-harness-binding.json
.claude/orchestrator-harness-binding.json
.qwen/orchestrator-harness-binding.json
RESULT.json
COMPLETION_REVIEW.json
ORCHESTRATOR_ACCEPTANCE.json
```

Generic setup/bootstrap writes those files with actual ROOT/lane paths,
identities, and queue details. The adapter never writes them.

The README must also say that setup refuses **every** target-file collision—not
only a collision with product-owned Codex, Claude Code, or Qwen Code files. An
adapter collision must fail rather than merge or replace any settings file,
wrapper, helper, skill, or launcher binding.

## Generic harness corrections required before this adapter format is real

This proposal is not the current external harness implementation. The current
source has hard-coded Codex/Claude/Qwen branches that generic harness code must
replace before a copied standard-provider adapter can work. None of these are
extra adapter files.

- Load/register the fixed `launcher_binding.py` in every fresh controller process
  before provider validation. Today `provider.py` starts with only three literal
  registry entries.
- Make provider-option validation call the selected binding's ordinary
  start/resume argument builder. Today `invocation.py` has explicit Claude and
  Qwen option branches.
- Make normal child environment and generic hook-import setup apply to every
  prepared standard provider. Today `lane_controller.py` has a Claude environment
  branch, a Codex hook-override branch, and a three-provider hook-import list.
- Retire the separate provider-specific installer/check/upgrade routes and the
  older `HostAdapter` delivery selector. Generic setup performs the three-tree
  copy/collision check; generic hook dispatch handles ROOT/worker notification
  and Stop behavior.
- Use only generic provider PID/status and configured transcript paths in new
  records. The current `codex_pid` compatibility fields and Codex-named transcript
  fallbacks are candidate-only read compatibility, not requirements for a new adapter.
- Keep Codex's bounded-command `PreToolUse` policy as a Codex-only product
  feature. An ordinary adapter author does not copy or recreate it merely to
  support PostToolUse, Stop, queues, or result checking.

The generic hook dispatcher is a release gate, not an assumption. Before this
hook-dependent design is implemented for a provider, a real disposable headless run
must prove that its project configuration is discovered, PostToolUse runs, Stop can
actually reject completion, and the wrapper's response is honored. The external
harness's earlier Codex failure is historical: the current `harness-single`
candidate has since proven native PostToolUse delivery for Codex, Claude Code,
and Qwen Code. See `subagent_hooks.md`. Files existing at the correct paths are
still not proof a hook ran, and the role-aware Stop/rejection behavior in this
new design still needs its own live proof for each provider. A provider that
cannot pass the applicable proof is unsupported for hook-dependent lanes until
a controller-level fallback is designed and proven.

## Adapter boundary and launch limitations

The adapter has two deliberately separate parts:

- `root/` and `super-cache/` contain only provider project files: hook
  configuration, thin hook wrappers, project-local skills, and provider-supported
  settings.
- `harness/launcher_binding.py` contains only the provider-specific start/resume
  argument spelling and the tiny output parser described above.

The binding can express a documented CLI launch flag or output-mode choice. It
cannot replace generic controller behavior: it cannot acquire a lock, make a
worktree, supervise a process tree, write a lane binding, alter the child
environment, decide queue behavior, or recover a missing provider session. If a
CLI cannot provide a required capability through its documented command line and
project files, the adapter README must say so plainly; that CLI is not supported
until the harness gains a real generic capability for it.

For Codex, generic harness launch must preserve user configuration and apply the
established hook enabling, exact-worktree trust, and session-hook declarations.
Its small binding must not add `--ignore-user-config` or redirect Codex to
another project root.

## Required proof recorded by the README

The README must give a small host-only proof for the adapter files:

1. Run setup into a clean disposable ROOT workspace; prove every `adapter/root`
   file arrived at the expected path and the CLI discovers its hook config plus
   the `manager-notification-watch`, `acknowledge-manager-notification`,
   `close-manager-notification`, `review-lane-completion`,
   `send-lane-notification`, `resume-lane`, and `harness-shutdown` ROOT skills.
2. Prove setup copied only the declared
   `adapter/harness/launcher_binding.py` to that provider's fixed registered
   harness path, and that the generic controller can load its two required
   functions and matching identity constants. A wrong provider ID, missing
   function, or arbitrary external binding path must be rejected.
3. Create a clean disposable **managed** worker; prove every
   `adapter/super-cache` file was included in the full managed cache overlay at
   the expected worktree path and the CLI discovers its worker hooks plus the
   `manager-notify` and `lane-assignment` skills. Also prove a plain worker starts
   and finishes with no copied hook/config/queue payload.
4. Launch a host-only new lane and a host-only resumed lane. Prove the binding
   built the provider's exact argument array, the generic controller used the
   generated worktree as its working directory, the parser captured a real
   session ID, and an invalid saved session is reported instead of causing a new
   session to start.
5. Cause one real PostToolUse event and prove the wrapper calls the generic
   notice process rather than merely existing on disk.
6. Attempt worker completion with malformed `RESULT.json`; prove the CLI's Stop
   hook actually rejects completion.
7. Write valid `PASS`, `FAIL`, and `BLOCKED` results in separate runs; prove
   the CLI permits completion for each.
8. Leave ROOT work `PENDING` or `ACKNOWLEDGED`; prove the ROOT Stop hook rejects
   completion, then resolve the work and prove it permits completion.
9. Put an existing file at each destination in turn: one harness binding, one
   super-cache file, and one ROOT file. Prove normal setup performs its full
   preflight, copies nothing, and never overwrites or merges any file. Then prove
   `setup --overwrite` replaces exactly the planned harness/adapter paths, reports
   each replacement, and restores prior files if its staged copy cannot complete.

This proof does not need firmware, an MCP server, or hardware.
