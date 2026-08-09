---
name: always-keep-in-mind
description: "Before making a codebase plan or spec, or before making any mass edit: read this design principle document that you should always keep in mind when designing code."
---

# always-keep-in-mind


# Any edits to any code base should keep the following things in mind:

we are designing for the following design principles:

# Design Charter & Operating Goals


## Mission
Use this charter in addition to whatever concrete task you are given. Wait for the
actual task before acting on it. Do not return an answer unless the task is
blocked by something genuinely unpassable, or it has been fully executed to
completion. When executing a task, for **any** change made to the codebase, build
and maintain software that does its real job well — that solves the problem it
exists to solve — across **arbitrary inputs, environments, and use cases**,
without a human having to hand-hold the setup for each new situation.

This charter is the goal to keep in mind for any active change to an existing
codebase. Do not edit parts that are not broken and were not asked to be edited,
even if parts you have read do not seem to line up perfectly with this charter —
those parts work, and working code is not to be broken in pursuit of tidiness.

This document is the standard every change is measured against. When a design
decision is unclear, resolve it toward these goals using the tie-breakers in
*When principles collide*, and **state the assumption you made** — in the code's
output, its docstring, or a comment, wherever the next reader will see it.


---


## The core properties


### 1. Correctness — behave the way the idea intends
The code does what a competent engineer would expect, not an approximation of it.

- An operation that claims to write **and verify** actually does both; a function
  that claims to return a value returns the true value; an operation that claims
  to reset state leaves the system in a genuinely known state afterward.
- **No silent failure and no fabrication.** If a write fails verification, the
  code reports failure — it never returns success. If the code cannot determine
  something, it says so rather than guessing a plausible-looking answer.
- Anything that deviates from intended behavior — wrong logic, a functionality
  gap, a bug, a swallowed error — gets replaced with an implementation that
  matches the intent.
- If the spec is ambiguous, resolve to the behavior the design most clearly
  implies (e.g. "reset" almost always means "get the system into a clean known
  state," so do the reset that achieves that) and record the assumption.


### 2. Simplicity — Occam's razor
The simplest form that is still highly effective.

- Each unit — function, module, endpoint — does **one** job well. No forty-knob
  configuration where three knobs cover the real cases.
- No speculative abstraction, no gold-plating, no plugin framework built for a
  single plugin, no machinery that isn't earning its keep.
- Prefer flat, obvious control flow. If wrapping an existing, battle-tested
  library or tool does the job, wrap it — don't reimplement a protocol, a parser,
  or an algorithm that already exists in mature form.
- Litmus test: a new engineer should be able to understand a unit's
  implementation in one sitting.
- *Extremely Important*: Never overengineer, double-guard something that passes, or do extra "just in case" engineering. If it works, it works. If it doesnt work, it doesn't work. Every extra feature/change added on should be heavily weighed: does the addition of this code outweigh the maintenance effort, bug fix effort, and risk of breaking something else in the code vastly? if it does, its worth adding. If it doesn't have a good benefit: cost ratio, its not worth adding. Keep the minimal subset of the most valuable changes and features for this product.  


### 3. Generalizability — works for situations it has never seen
The code must work for any reasonable input, platform, and environment — not just
the one it was tested on.

- **No environment-specific constants.** No hardcoded paths, hostnames, ports,
  credentials, user names, or region codes; no "this OS only" assumptions; no
  baked-in core or memory counts; no fixed toolchain or dependency locations that
  will differ on another machine.
- **Detect, parameterize, or degrade gracefully — in that order.** Discover what
  varies (available services, config, versions, capabilities, resource limits) at
  runtime. Parameterize what varies. If auto-detection fails, expose a way for the
  caller to supply the missing piece — and persist it so the gap closes
  permanently.
- **Autonomous onboarding.** The setup path should take an unknown input or
  configuration and bring it to the same known-good state a supported one reaches,
  on its own. Handling a new case must never require editing source.


### 4. Neatness — organized for reader and maintainer alike
No sloppiness, no tangled web.

- Consistent naming: functions read as `verb_noun`; shared parameters keep the
  same name and units across every call site.
- One home per responsibility — detection, validation, or configuration logic
  lives in one place, not smeared across five call sites.
- No dead code, no commented-out experiments, no confusing control flow.
  Interfaces are predictable enough that the shape of the next one is guessable
  from the last.


### 5. Usability — the code must teach its user how to use it
Simplicity includes being intuitive to operate, for both a machine caller and a
human.

- Every public unit's documentation states: **what it does, when to reach for it,
  its parameters (with units and an example), what it returns, and its common
  failure modes with the recovery step.**
- Ship a top-level "start here" document the reader can read first: the normal
  workflow and how the pieces chain together.
- The user should never have to guess a contract or discover behavior by trial. If
  outside knowledge is needed to use a unit correctly, its documentation is
  incomplete.


### 6. Dynamism — solve the novel case with the existing pieces, not a code change
This is the differentiator. When the code meets an input, configuration, or
environment it has never seen, it should be able to succeed using the
capabilities that already exist.

- **Introspection first:** the ability to enumerate what is present and identify
  what it is (list resources, probe config, read versions, discover
  capabilities).
- **A generic path** to operate over a standard interface even when no named
  profile for that exact case exists yet.
- **Learn and persist:** a way to register what was figured out so the
  previously-unknown case is *known* on the next run.

Design the pieces to be composable and general enough that "I've never seen this
case" is handled by orchestrating what exists — **not** by adding another branch
to a `switch` statement.


---


## 7. Operating assumptions — design for the actual case
Build for ordinary work under the conditions this code will actually run in, not
for exotic edge cases that won't happen — and not against a threat that can't
reach it.

- **Know your real trust boundary and design to it honestly.** Decide who and what
  can actually reach this code. Callers and users *inside* the boundary are
  assumed non-hostile; input from *outside* it is not. The boundary is about
  hostility, not competence — even a fully trusted caller is assumed **fallible**.
- **Non-hostile does not mean infallible.** A trusted caller follows contracts in
  good faith but will make honest mistakes: misread returned state, act on a stale
  or unverified assumption, select the wrong target, or thrash in a retry loop.
  Guarding against the caller's own mistakes is always in scope. Hardening against
  an attacker is in scope **only when your trust boundary actually includes one** —
  a public endpoint faces hostile input and must harden against it; a purely
  internal helper reached only by trusted code does not.
- **Trusted input is trusted about hostility, not about correctness.** Anything a
  trusted caller hands the code — a path, a file, a target selection, a command —
  is not an attack, but it is **not** assumed *correct*. Validate it for
  correctness (is it the right, real thing; does it match verified state; will it
  make the code behave correctly?). Do not treat a trusted operator as an
  attacker, but do treat them as capable of error — catch the mistake rather than
  faithfully executing it.
- **Handle the failure modes that actually occur** every day: missing resource,
  wrong address, insufficient permission, malformed input, a verification
  mismatch, a dependency that dropped offline mid-operation. **Also handle the
  mistakes a mediocre caller actually makes:** operating on a target that doesn't
  match the detected one, issuing a destructive step against an unverified or wrong
  target, acting on detection results that have gone stale, or repeating a failing
  operation in a loop instead of surfacing the real error. These are all part of
  correctness.
- **Don't** spend the complexity budget on adversarial input your threat model
  excludes, impossible states, or bizarre configurations that won't arise. Robust
  where reality demands it; not paranoid where it doesn't.


## 8. No paternalistic guarding — but do catch the caller's mistakes
The code protects **correctness**. It does **not** protect the engineer from their
own legitimate project, and it does **not** harden trusted input against attacks
the deployment model says cannot happen. Over-defensive guarding is a defect: it
burns the complexity budget and, worse, it blocks real work.

Paternalism is refusing or second-guessing an operation the caller *intended* and
*correctly aimed*. It is **not** paternalism to catch an operation the caller did
*not* intend — one that contradicts verified state, targets the wrong or an
unverified resource, or is the product of a thrash loop. Guarding against the
fallible caller's own mistakes is a correctness duty, not nannying.

- **Safety of the project is the engineer's job; catching mistakes is the code's.**
  If the engineer is *intentionally* doing something risky — deleting data,
  overwriting a config, running an irreversible migration — the code performs the
  requested operation (with honest verification and honest reporting of what
  happened) and lets the engineer own the risk. It does not refuse, second-guess,
  gate a coherent correctly-targeted request behind "are you sure," or nanny. **But
  an intended risky operation and a mistaken destructive one look different, and the
  code must tell them apart by checking against what it has verified.** Before a
  destructive or hard-to-reverse step, confirm the operation is consistent with
  verified state — the target named is the one actually present, the artifact
  matches the detected target, the address is the one that was detected. If the
  request contradicts verified state, that is a mistake, not a brave choice: stop
  and report the mismatch instead of faithfully executing it. Never block the risk
  the engineer *chose*; do block the damage the caller *didn't mean to do*.
- **No adversarial-input hardening on trusted input.** When the trust model says an
  input arrives from inside the boundary, don't layer on defenses aimed at an
  attacker who can't reach it — they defend against nobody real and routinely break
  legitimate work (e.g. an arbitrary size cap that rejects a real, oversized-but-
  valid input). Reserve that hardening for the inputs that genuinely cross into
  hostile territory, where it *is* correctness.
- **Every limit must trace to a real constraint.** A cap, buffer size, timeout, or
  count limit is allowed only when it comes from actual hardware, a protocol, a
  correctness requirement, a real security boundary, or the need to stop a fallible
  caller from thrashing (a bounded retry that ends in an honest error, so a mistake
  surfaces instead of spinning) — never from a hypothetical adversary outside the
  model or "just in case." An arbitrary magic number with no basis is an
  anti-pattern; raise it out of the way or delete it.
- **Keep checks that catch the code *or the caller* getting it wrong.** Rejecting a
  genuinely corrupt or wrong input so the code doesn't silently do the wrong thing
  is correctness, and it stays. Catching a requested operation that contradicts
  verified state — wrong target, mismatched artifact, stale detection — is
  correctness, and it stays. Rejecting a valid input because it *could* have been
  malicious, when nothing malicious can reach it, is paternalism, and it goes.

**The test for any guard:** *"Does removing this let a non-hostile but fallible
caller — one that may thrash, misread state, target the wrong resource, or act on
an unverified assumption — get a wrong, destructive, or misreported outcome they
did not intend?"* If yes, it is correctness — keep it. If it only ever stops an
attacker outside the threat model, or stops the user from doing something
*risky-but-intended and correctly-targeted*, delete it. The dividing line is intent
versus mistake: **guard the mistake, permit the intended risk.**


### Worked example — applying a change to a mismatched target

The same scenario resolved three ways. A caller invokes
`apply_migration(connection="prod-db-01", migration="add_billing_index.sql")`. The
code has already probed the live database on that connection and read back its
identity — schema fingerprint says it is the **analytics** store. The migration's
own header declares it targets the **billing** store. Applying it will fail
strangely, corrupt data, or no-op in a way the caller then misdiagnoses.

- **Naive / stripped bare (wrong).** The code applies whatever it was handed and
  reports success because the statements ran without a syntax error. The caller,
  being only OK at its job, now believes the billing index exists and burns the
  next hour debugging a "performance" problem that is really a wrong-target
  mistake. This is a **correctness failure**: the code faithfully executed a
  mistake and misled the reader about what happened.

- **Paternalistic (also wrong).** The code refuses to apply any migration to a
  connection whose name contains "prod," or pops "this could affect production —
  are you sure? [y/N]" on every migration. This blocks the engineer who
  *deliberately* runs a migration against a correctly-identified production store,
  and it defends against nothing real. Delete it.

- **Mistake-guard (correct).** Before applying, the code compares the migration's
  declared target against the **verified** identity it already read from the live
  connection. They disagree, so it stops and returns an honest, actionable error:
  probed `analytics` on `prod-db-01`, but `add_billing_index.sql` targets
  `billing` — refusing to apply a mismatched migration; point at the billing store
  or select the correct migration. It does **not** ask "are you sure"; it reports a
  contradiction with reality. Note the precise boundary: if the identity probe was
  **unavailable** (the store exposes no readable fingerprint), the code cannot
  assert a mismatch — so it does not invent one. It applies the migration, states
  in its result that the target could not be verified, and lets the engineer own
  that gap. The guard fires only on a *verified* contradiction, never on an
  *unverified* suspicion.

The test applied: removing the mismatch check lets a fallible caller corrupt the
wrong store and be told it succeeded → correctness → keep it. Removing the "are you
sure" prompt costs a caller nothing except a speed bump on work it meant to do →
paternalism → delete it. Same operation, opposite verdicts, decided entirely by
*verified state* and *intent versus mistake*.


---


## When principles collide
- **Simplicity vs Generalizability** → choose the simplest design that still
  handles the unknown *by detection*, not the most abstract one. Runtime detection
  beats an abstraction layer.
- **Generalizability / Dynamism vs Correctness** → generality never licenses
  guessing. On a novel case, **verify** (read back, confirm identity) instead of
  assuming; if it can't be verified, report the uncertainty and let the user decide
  how to proceed.
- **Correctness vs Simplicity** → correctness wins — but once the real requirement
  is understood, the correct implementation is usually also the simpler one.
- **Normal-case assumption vs Correctness** → assuming the normal case decides
  *which situations to handle*. It is never an excuse to misreport what happened.
- **Defensive guarding vs Functionality** → within the trust boundary,
  functionality wins. A guard that blocks legitimate work to defend against an actor
  the deployment excludes — or to protect the engineer from an intended,
  correctly-targeted risky operation — is removed, not tuned. But a guard that
  catches the fallible caller's own mistake — an operation contradicting verified
  state, a destructive step on an unverified target, an unbounded thrash loop — is a
  **correctness** guard, not defensive guarding, and it stays. Correctness guards
  (verify, don't fabricate, don't misreport, don't misprocess a broken input, don't
  faithfully execute a mistake) are non-negotiable.


---


## Definition of done
A change is done when all of these hold:

1. It does the intended thing and reports honestly (no silent failure, no
   fabricated results).
2. It is the simplest form that is still effective — nothing speculative.
3. It contains no environment-specific constants; it detects or parameterizes
   everything that varies.
4. It is cleanly named and lives in the one place that owns its responsibility.
5. Its documentation lets a user use it correctly with zero outside knowledge,
   including how to recover from its common failures.
6. A novel-but-reasonable input is handled by composing existing pieces, not by
   editing source.
7. Every guard, limit, and rejection it introduces traces to a correctness, real
   hardware/protocol, or genuine security-boundary constraint — none of it hardens
   against a threat outside the model, and none of it nannies the engineer out of a
   legitimate, correctly-targeted operation they chose to run. Guards that catch the
   fallible caller's own mistakes — a request contradicting verified state, a
   destructive step on an unverified target, an unbounded retry loop — are
   correctness guards and are expected to be present, not stripped.


---


## Anti-patterns — reject these
- Hardcoded paths, hosts, ports, credentials; OS checks that break elsewhere; fixed
  core, memory, or dependency-location assumptions.
- Silent failure, swallowed errors, or fabricated success/data.
- Speculative abstraction, unused config knobs, a plugin framework with one plugin.
- Detection, validation, or config logic scattered across many call sites;
  inconsistent parameter names or units.
- Units with missing docs, or docs that omit failure modes and recovery.
- A `switch`/`if` ladder that must grow every time a new case appears — that is a
  detection-plus-generic-path job instead.
- Any hardcoded case list that biases toward a specific few supported inputs without
  offering the same treatment to every other reasonable input.
- **Adversarial-input hardening on trusted input** — defenses aimed at an attacker
  who cannot reach this code, applied to input that arrives from inside the trust
  boundary. Reserve that hardening for the inputs that genuinely cross a hostile
  boundary.
- **Paternalistic refusals, prompts, or caps** that block a legitimate,
  correctly-targeted, *intended* risky operation on the engineer's own project. The
  engineer owns the risk of their own work. (This is **not** a license to drop
  guards that catch the caller's *mistakes* — an operation contradicting verified
  state, a destructive step on an unverified target, or a thrash loop. Those are
  correctness guards and must stay.)
- **Arbitrary magic-number limits** (size / buffer / count / timeout) not derived
  from a real hardware, protocol, security, or correctness constraint — e.g. a fixed
  ceiling that blocks a real, valid, oversized input.
