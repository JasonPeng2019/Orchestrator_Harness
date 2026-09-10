# From Ambiguous Goal to Safe Agentic Firmware Work

## Abundant RPM technical presentation script

**Core thesis:** I turned an ambiguous request—“let agents work on firmware”—into two explicit system boundaries: a provider-neutral orchestration layer that coordinates work and evidence, and a firmware MCP layer that independently controls access to physical hardware.

**Suggested length:** 15–18 minutes, plus questions.

**Status language to preserve:** The multi-agent harness and firmware MCP are implemented as separate systems. Live hardware evidence currently proves board setup, validation, and authorization re-locking on a NUCLEO-L476RG. A complete harness-to-MCP, build-flash-observe campaign is the next integration milestone. Do not describe that future campaign as already complete.

**Personalize before presenting:** Replace “Contributor A/B/C” with the real ownership split, confirm whether “three contributors” includes you, and add one concrete example of a disagreement or prioritization call you personally resolved.

---

## Slide 1 — Building a Safe Multi-Agent Firmware System

### On the slide

> How I decomposed, coordinated, and evaluated an agent system that can work toward real hardware without inheriting unrestricted hardware authority.

- Persistent orchestrator for planning and acceptance
- Native harness for worker lifecycle, isolation, events, and evidence
- Firmware MCP for guarded debug, serial, deployment, and recovery
- Three-contributor execution model; I owned the system boundaries and integration logic

### Visual

```text
Ambiguous goal                         System outcome
"Agents should work on firmware"  ->  Coordinated work + bounded hardware access
```

### Speaker script

“The project started with a broad goal: let agents do meaningful firmware work. I quickly found that tool access was not the hard part. The hard part was coordinating multiple workers, preserving state across long tasks, deciding who had authority, and proving what happened when the endpoint was a physical device. I mapped that into two systems. The harness coordinates software work and evidence across isolated agent lanes. The firmware MCP exposes board operations but independently enforces identity, plans, permissions, and memory boundaries. Both exist today; the next milestone is evaluating them together in a repeatable end-to-end campaign.”

### Transition

“To understand why that separation matters, start with what unrestricted autonomy would mean on hardware.”

---

## Slide 2 — Capability Versus Control

### On the slide

**Goal:** agents can inspect, build, debug, flash, observe, and recover firmware.

**Risk:** a wrong software action can alter a file; a wrong hardware action can erase a device, write a protected region, attach to the wrong board, or leave volatile state behind.

```text
Agent capability  <-------------------------->  Control and reliability
```

**Safe autonomy meant:** maximize useful independent work while making authority explicit, temporary, scoped, and observable.

### Speaker script

“Normal tool calling was not enough because a valid-looking call can still be wrong for the current board, session, artifact, or memory map. I classified operations by consequence. Discovery, inventory, and most evidence collection are reversible. RAM writes, register changes, flashing, and recovery have progressively larger blast radii. The design therefore does not equate a visible tool with permission. An agent may propose an action, but the hardware boundary must still prove the live identity, validate the exact plan, check scope and freshness, consume the appropriate authority, and refuse before mutation when facts are missing.”

### Transition

“That safety problem was only one of several hidden inside the original sentence.”

---

## Slide 3 — Mapping One Goal Into Workstreams

### On the slide

```text
                    Agentic firmware goal
                             |
        +--------------------+--------------------+
        |                    |                    |
  Orchestration        Hardware boundary      Evaluation
  - task lanes         - board identity       - software tests
  - providers          - plans/permission     - event failures
  - lifecycle          - memory safety        - live HIL
        |                    |                    |
        +---------- contracts and evidence -------+
                             |
                         Integration
```

**Interfaces defined first:** task/result schemas, event identity, lane ownership, MCP plan/action contracts, hardware identity, and acceptance evidence.

### Speaker script

“I decomposed the project by failure domain, not by file tree. Orchestration had to answer how work starts, pauses, resumes, and gets accepted. The hardware boundary had to answer what can be done to which physical board under what authority. Evaluation had to distinguish worker completion, system correctness, and actual firmware behavior. Those areas could progress independently once I defined their contracts. The dependency order was interfaces first, isolated implementation second, integration third, and live validation last. Provider-neutrality, strict result acceptance, deterministic observation, and cleanup proof became stronger as testing exposed ambiguity.”

### RPM point

“The roadmap was a dependency graph with explicit gates, not a list of features.”

---

## Slide 4 — Two Boundaries, One End-to-End System

### On the slide

```text
                   Persistent orchestrator
             plans / assigns / reviews / accepts
                              |
                 Native multi-agent harness
            lanes / events / leases / lifecycle
                   /                    \
          Worker agent(s)       Deterministic watcher
     reason / code / investigate      observe only
                   |
              Firmware MCP
       validate / plan / gate / contain
                   |
          pyOCD + pyserial adapters
                   |
             Physical device
```

**Current state:** the harness and MCP are implemented; the complete integrated evaluation is next.

### Speaker script

“The orchestrator owns the project: decomposition, sequencing, review, and acceptance. The harness is an execution boundary beneath it. It launches one provider worker per isolated lane, routes durable events, serializes declared resources, and tracks exact process and Git identities. A deterministic watcher can inspect health evidence, but it does not manage work. In the intended firmware flow, a worker uses the MCP as a client. The MCP—not the worker and not the harness—owns the live board handle and enforces every hardware precondition. This separation lets each boundary fail closed and be evaluated independently.”

### Transition

“The architecture is really an authority map.”

---

## Slide 5 — Who Is Allowed to Decide What?

### On the slide

| Component | May decide | Must not decide |
|---|---|---|
| Orchestrator | scope, assignment, dependencies, review, acceptance, recovery | bypass MCP safety |
| Worker | how to execute its assigned technical task; when to request help | accept its own result; expand its authority |
| Harness | deterministic lifecycle, routing, resource serialization, identity checks | schedule work; choose outcomes; operate hardware |
| Watcher | nothing; it reports evidence | launch, repair, approve, or kill |
| Firmware MCP | whether a hardware call satisfies policy | choose the project goal or artifact |
| Human | approvals required by the plan, especially destructive recovery | supply hidden authority through casual conversation |

### Speaker script

“My rule was to avoid overlapping authority. The orchestrator decides; workers execute and report; the watcher observes; and the MCP enforces hardware boundaries. Even the harness does not declare a task successful. A worker result becomes merge-ready only after identity, schema, evidence, content hash, branch tip, and clean-worktree validation, followed by a separate orchestrator acceptance. On hardware, conversation is not permission. Permission is structured, scoped to the unchanged plan and live session, and invalidated by changes such as reconnect, artifact drift, or restart.”

### Takeaway

> Durable state may preserve evidence; it must not silently restore authority.

---

## Slide 6 — Coordinating Multiple Agents Without Losing Control

### On the slide

```text
Task card
   -> bootstrap isolated lane
   -> launch one provider worker
   -> worker emits a durable signal
   -> harness promotes an actionable event
   -> orchestrator blocks on native wait
   -> orchestrator validates and responds
   -> acknowledge receipt
   -> close with outcome
   -> validate RESULT
   -> independently accept or reject
```

- Signal identity and queue-event identity are distinct and preserved
- Acknowledged means “received,” not “fixed”
- Resume creates a fresh run identity without inventing prior process state
- Exact process identity and cleanup proof prevent broad or accidental termination

### Speaker script

“Each task begins as a bounded card in an isolated Git worktree. A worker can publish a progress, help, or completion signal. The harness durably promotes actionable work, and the orchestrator waits on the native event mechanism instead of polling through another AI manager. Every event is correlated to its lane and run. Handling is explicit: receive, acknowledge, respond, close, then evaluate the result. Duplicate or stale records are not guessed into coherence. If a lane stops, resume uses a fresh run ID while preserving the legitimate worktree and provider session. That gives us persistence without pretending an old process is still alive.”

### Why no AI manager-of-managers?

“Coordination mechanics are deterministic; model judgment stays at the orchestrator and worker boundaries where it adds value.”

---

## Slide 7 — Firmware Was the Reality Check

### On the slide

The MCP can expose:

- board discovery, setup, support admission, connection, and validation
- halt/resume/step/reset, registers, symbols, breakpoints, and bounded memory access
- bounded UART capture and stateful serial exchanges
- explicit artifact collection with hashes
- application/bootloader flashing and deliberately approved recovery

> A successful flash proves deployment, not correct firmware behavior.

### Speaker script

“Firmware made abstract agent reliability concrete. The agent must know which probe maps to which board, whether the observed MCU matches the profile, whether an ELF is still the one that was planned, and whether every byte falls inside an authoritative range. The MCP supports setup, debugging, serial evidence, artifact intake, deployment, and recovery, but it never chooses a firmware artifact or silently connects. Physical state also outlives individual calls, so cleanup and final MCU state become part of correctness. That is a much stronger systems test than editing code until a unit test turns green.”

### Evidence boundary

“The current live HIL result validates setup, real-board identity, automatic validation, and authorization re-locking on a NUCLEO-L476RG. It intentionally did not flash, erase, unlock, or write the target.”

---

## Slide 8 — Capability Did Not Equal Permission

### On the slide

```text
Discover -> Resolve profile -> Validate live identity -> Build safety map
    -> Plan exact action -> Approve when required -> Execute within bounds
    -> Verify the intended behavior separately
```

**Enforcement principles**

- Tool visibility is advisory; the physical handler rechecks the lock
- Plans bind run, board, session, tool, parameters, artifact digest, and call budget
- Unknown/unmapped spans and prohibited writes fail closed
- One board serializes hardware operations; separate boards may proceed concurrently
- Disconnect/restart clears live gates, plans, permissions, and assignments
- Destructive recovery requires a fresh, one-time, plan-bound human approval

### Speaker script

“The important design is the sequence. Discovery guides the agent but grants nothing. Live validation establishes the board and map association in memory. The plan then binds the exact action and parameters, and selected operations require structured approval. At dispatch, the server rechecks the handler lock, artifact digest, plan identity, session, permission, live validation, memory containment, budget, and timeout before the backend can mutate hardware. Durable `.firm` records are useful evidence, but they cannot reopen a live gate after restart. Missing facts produce a refusal with a specific remedy rather than an inferred range or identity.”

### Takeaway

> A tool being callable is a transport fact, not an authorization fact.

---

## Slide 9 — Four Decisions That Shaped the System

### On the slide

| Decision | Choice | Tradeoff accepted | Failure prevented |
|---|---|---|---|
| Observation | deterministic watcher by default | less “smart” automatic intervention | recursive AI management and untraceable repairs |
| Product boundary | provider-neutral harness; firmware policy in MCP | two explicit integration surfaces | duplicated or conflicting safety authority |
| Dangerous actions | plan first, execute second | extra interaction and latency | stale, ambiguous, or over-broad calls |
| Persistence | durable evidence, ephemeral live authority | reconnect requires revalidation | disk state silently reopening hardware access |

### Speaker script

“I made four choices that reduced capability in the short term to improve the system boundary. First, observation is deterministic by default; the watcher can surface facts but cannot take over. Second, I removed firmware semantics from the harness’s canonical invocation path. The harness coordinates any provider worker, while the MCP owns hardware policy. Third, guarded actions use a strict plan-to-execute split. Finally, durable state is evidence rather than live authority. These decisions add explicit steps, but they make failures local, reviewable, and much harder to turn into unintended action.”

### Interview follow-up

“If latency became a product problem, I would optimize plan reuse only inside the existing scope and budget rules; I would not collapse planning and execution into one opaque call.”

---

## Slide 10 — Parallel Work With Architectural Coherence

### On the slide

```text
                         System goal
                             |
          +------------------+------------------+
          |                  |                  |
  Contributor A       Contributor B       Contributor C
  harness/runtime     firmware MCP        evaluation/HIL
  provider adapters   safety contracts    fixtures/docs
          |                  |                  |
          +--------- reviewed integration -----+
                             |
                            Me
        boundaries / dependency map / interface decisions /
              review criteria / final integration
```

### Speaker script

“I organized the three contributors around independently testable failure domains rather than assigning arbitrary features. The harness owner could work against versioned task, result, and event contracts. The MCP owner could work against plan, permission, validation, and action contracts. The evaluation owner could build software and HIL evidence against both. I retained the cross-cutting decisions: where authority lived, the order of dependencies, what evidence counted, and whether an integrated result was acceptable. Parallelism stopped at shared interfaces and physical resources; those were reviewed or serialized rather than edited concurrently.”

### Coordination mechanisms

- Write the interface and acceptance condition before implementation
- Give one writer ownership of overlapping code
- Isolate lanes by branch/worktree and exact base identity
- Require durable handoffs instead of relying on chat memory
- Integrate only reviewed tips; preserve unaffected test credit only when inputs are unchanged

---

## Slide 11 — The First Design Was Too Coupled

### On the slide

**Initial direction:** let the orchestration layer understand a firmware-specific invocation shape.

**Problem:** scheduling concerns and hardware semantics began to share a boundary.

**Change:** remove the schema-less firmware path from the harness; use one provider-neutral worker lifecycle and make the MCP the sole hardware-policy boundary.

```text
Before:  Orchestrator + harness + firmware semantics
After:   Orchestrator -> generic harness -> worker -> guarded firmware MCP
```

### Speaker script

“A major correction was architectural. The harness had a firmware-specific, schema-less invocation path. That looked convenient but made the coordination layer aware of hardware semantics and created another place where policy could drift. I removed that path and converged every worker onto a versioned provider-neutral contract. The firmware MCP now remains client-neutral and independently distrusts the caller. That simplified the harness and made the safety model stronger. It also gave us a cleaner evaluation question: did orchestration deliver the right work, and did the hardware boundary independently authorize the resulting action?”

### A second failure that validated the boundary

“In an early nested-agent HIL attempt, the workflow stopped at an external approval request. The agent correctly refused to run its own approval command. That blocked the test, but it was the right safety outcome. We completed a later clean setup/validation run without granting the agent hidden approval authority. The lesson was that safe refusal and good approval UX are separate product requirements.”

---

## Slide 12 — Evaluation: Capability, Reliability, and Safety

### On the slide

| Evaluation layer | Question | Example evidence |
|---|---|---|
| Capability | Can the agent achieve the technical goal? | build, deploy, observe, and diagnose a defined firmware task |
| Reliability | Does the system behave correctly across repeats and failures? | event correlation, resume, resource leases, exact cleanup, repeated runs |
| Safety | Does it constrain or refuse invalid action? | stale plan, wrong board, changed artifact, unknown range, restart, missing approval |

**Success is layered:**

1. Command success — a tool returned successfully.
2. Deployment success — the intended bytes were programmed.
3. Firmware success — observed device behavior met the task criterion.
4. System success — the outcome was evidenced, accepted, and left no unsafe residual state.

### Speaker script

“I evaluate the agent and the system separately. Capability asks whether the technical task gets done. Reliability asks whether events, identities, retries, and cleanup remain correct across repeated runs. Safety asks whether invalid or stale actions are refused before mutation. The portable harness snapshot reports 208 harness tests with one environment-gated skip and 99 watcher tests. The firmware repository has a live non-destructive HIL pass for setup replacement, real validation, and re-locking. The honest gap is a repeatable end-to-end campaign where harness-managed workers build, flash, observe behavior, recover from injected failures, and compare against a single-agent baseline.”

### Failure cases to include in the next benchmark

- malformed, duplicate, stale, and wrong-lane events
- provider exit after a valid result; timeout and interrupted resume
- board/probe mismatch and reconnect during a task
- artifact digest drift between plan and execution
- unknown or prohibited memory ranges
- successful flash with incorrect UART or memory behavior
- approval withheld, malformed, stale, or scoped to a different plan

---

## Slide 13 — What the Project Established

### On the slide

**1. Agents are useful for reasoning; authority should remain explicit.**

**2. Deterministic infrastructure makes multi-agent behavior inspectable and recoverable.**

**3. Physical systems expose coordination failures that code-only benchmarks hide.**

### Speaker script

“Three conclusions changed how I think about agent products. First, models are valuable where the work requires decomposition, diagnosis, and adaptation, but authority should be encoded in explicit system state. Second, deterministic infrastructure around models—identities, schemas, leases, event states, and cleanup—makes behavior debuggable. Third, hardware forces a more honest definition of success because deployment, behavior, and cleanup are different outcomes. I would not claim that this project has proven general autonomous firmware engineering. It has established the architecture and safety boundaries needed to evaluate that claim rigorously.”

### Transition

“The next step is therefore an evaluation program, not just another feature sprint.”

---

## Slide 14 — Turning It Into an Agent Research Platform

### On the slide

**If I had one month**

1. Integrate harness-managed workers with a firmware-project MCP configuration.
2. Build 10–20 repeatable tasks across build, flash, UART, debugging, and recovery.
3. Add deterministic fault injection: stale event, provider crash, reconnect, wrong artifact, invalid range.
4. Compare single-agent and multi-agent strategies under the same task and hardware state.
5. Produce an evaluation dashboard and failure taxonomy.

**Metrics**

- task success and behavior-verification rate
- unsafe-action attempt rate and correct-refusal rate
- human interventions per task
- time, tokens, and tool calls to accepted result
- duplicate work and coordination overhead
- recovery rate and time from injected failures
- residual-state failures: leaked process, lease, connection, or authority

### Speaker script

“My next milestone would be a small but rigorous benchmark. Every task would begin from a resettable project and device state and end with an externally observable criterion, not a self-reported result. I would compare a single agent with parallel specialists, keep models and budgets controlled, and inject the failures we expect in production. With more compute, I would expand across models, boards, task difficulty, and orchestration policies. I would redesign the multi-agent strategy if it failed to beat a single agent after accounting for coordination cost, or if it increased correlated mistakes or human intervention.”

### Research question

> Which parts of firmware work benefit from parallel reasoning, and which are safer and faster as one serialized owner?

---

## Slide 15 — How I Work

### On the slide

```text
Frame the capability
    -> identify failure modes
    -> decompose by responsibility
    -> define authority and interfaces
    -> assign independent ownership
    -> integrate at explicit gates
    -> evaluate behavior and safety
    -> revise the architecture
```

### Speaker script

“This project is representative of how I would operate as an RPM. I begin by turning an ambiguous capability goal into concrete system outcomes and failure modes. I decide where probabilistic reasoning is valuable and where deterministic enforcement is necessary. I create workstreams around stable interfaces, give contributors independent ownership, and keep integration and acceptance explicit. When assumptions break, I use the failure to update the system boundary and the evaluation—not just patch the demo. The result is a roadmap that connects research questions, engineering execution, safety, and measurable product progress.”

### Closing line

> “My job was not simply to give agents more tools. It was to design the system that lets us learn—safely and measurably—when agents can be trusted with consequential work.”

---

## Optional appendix — Likely interview questions

### Why multi-agent instead of one strong agent?

“Parallel agents are a hypothesis, not an assumption. They may reduce elapsed time and provide independent review when work decomposes cleanly. They also add coordination cost and failure modes. That is why I isolate lanes, define ownership, and propose a controlled single-versus-multi-agent benchmark.”

### Why not let the watcher repair obvious problems?

“Because detection evidence and repair authority are different. Automatic repair would create a second scheduler and decision-maker, complicating attribution and potentially conflicting with the orchestrator. The default watcher is deterministic and diagnostic; the orchestrator decides the response.”

### Why is application flashing not always human-approved?

“Permission is only one control. Application flashing still requires a current validated board, an exact artifact-bound plan, a current map, deployment authority, and containment of target, segments, entry/vector, and erase sectors. Higher-risk operations such as bootloader work, execution-state changes, and destructive recovery add explicit permission, with recovery requiring a fresh one-time grant. I would revisit that policy using task risk and evaluation data.”

### What is the largest unresolved risk?

“The largest uncertainty is integrated agent behavior over repeated live tasks. The boundaries have independent evidence, but we still need to measure whether multi-agent coordination improves task outcomes without increasing unsafe attempts, approval burden, or recovery time.”

### What would you demo?

“A bounded sequence: start from a known board and project state, have the orchestrator assign build and review lanes, collect an artifact, initialize a flash plan, show the MCP’s exact validation and containment, execute only within the approved boundary, then use UART or a memory-level assertion to verify behavior. I would also include one injected refusal or reconnect to show recovery rather than only the happy path.”

---

## Repository evidence map

Use these references for backup slides and technical follow-up. They are intentionally more precise than the main deck.

| Claim | Repository evidence |
|---|---|
| Harness is provider-neutral across Codex, Claude Code, and Qwen Code | `harness-single/final_v2-harness_overview.md:3-9`; `harness-single/README.md:69-77` |
| Harness owns lanes, events, resource serialization, and review records—not scheduling or hardware | `harness-single/README.md:14-22` |
| Worker result and orchestrator acceptance are separate | `harness-single/README.md:88-96` |
| Resume, retirement, and shutdown use explicit lifecycle and exact ownership | `harness-single/README.md:98-107`; `harness-single/final_v2-harness_overview.md:16-23` |
| Static fixtures are not live-provider proof | `harness-single/README.md:118-125` |
| Watcher is deterministic/read-only by default and cannot manage lanes | `harness-single/docs/HARNESS_WATCHER_GUIDE.md:3-15`; `:114-121` |
| Watcher alerts are at-least-once and acknowledgement means received, not repaired | `harness-single/docs/HARNESS_WATCHER_GUIDE.md:93-110` |
| Portable snapshot validation reported 208 harness and 99 watcher tests | `harness-single/docs/HARNESS_WATCHER_GUIDE.md:196-201` |
| Firmware MCP capability and client-neutral boundary | `BYO-Firmware-MCP/README.md:1-8`; `:29-45` |
| Restart/disconnect clear live authority; durable files are evidence only | `BYO-Firmware-MCP/README.md:47-58`; `BYO-Firmware-MCP/docs/architecture.md:103-122` |
| Exact plan validation and guarded dispatch order | `BYO-Firmware-MCP/docs/architecture.md:76-134` |
| Memory and deployment containment | `BYO-Firmware-MCP/docs/architecture.md:143-180`; `BYO-Firmware-MCP/docs/client-contract.md:167-215` |
| Conversation is not permission; recovery is fresh and one-time | `BYO-Firmware-MCP/docs/client-contract.md:81-96`; `:230-233` |
| Successful flash is not firmware-behavior proof | `BYO-Firmware-MCP/README.md:42-45` |
| Live HIL proved setup/validation/re-locking and performed no destructive action | `BYO-Firmware-MCP/testing_folder/HIL_RESULTS.md:1-24`; `BYO-Firmware-MCP/testing_folder/agent/final-clean-run-summary.md:1-16` |
| An earlier agent HIL run correctly stopped at external approval | `BYO-Firmware-MCP/testing_folder/agent/nested-agent-final-summary.md:1-7` |
| Firmware-specific schema-less harness input was removed | `harness-single/final_v2-harness_overview.md:32-36` |

## Claims to avoid unless new evidence is added

- “The multi-agent harness has already completed an end-to-end firmware task on hardware.”
- “The system has autonomously flashed or recovered a physical board.”
- “A successful flash proves the firmware works.”
- “The watcher autonomously manages or repairs agents.”
- “Persisted plans or reports restore hardware permission after restart.”
- “The current evidence proves broad cross-board or cross-platform reliability.”
