# Main-model plan-authoring contract — BYO-Firmware-MCP production-server repair only

The current main/orchestrating model authors this plan directly. Do not delegate plan authorship to
a planner subagent, provider-side planner, the implementation doer, or either tester.

Plan only a verified production-code repair in the BYO-Firmware-MCP repository root. Do not plan
fresh-experiment, firmware, fixture, SDK, test-spec, documentation-only, or metadata-only work.

Turn the supplied raw change list into one implementation-ready, testable plan. Inspect the
repository directly before planning so filenames, interfaces, callers, tests, and preservation
constraints are evidence-based rather than guessed.

Write only the required `.change-loop/plan.md`; do not edit source, tests, configuration, or
existing project files. Use the supplied plan template as the structural contract.

For every plan item:

1. State the concrete change.
2. Name the verified file, module, or area.
3. Specify exact externally observable behavior after the change.
4. State existing behaviors, compatibility contracts, and invariants that must remain intact.
5. Give objective verification that an adversarial tester can automate.
6. Split verification into the smallest targeted check, affected regressions, and any genuinely
   necessary expensive acceptance check. Name which existing passing checks the planned
   source/contract change invalidates; retain every unrelated pass.

Resolve minor ambiguity toward the requested behavior and simplicity. Ask the user when a material
ambiguity remains. Record each accepted interpretation as an HTML comment beginning
`<!-- Assumption:` immediately beside the affected item so the doer and testers cannot miss it.
Do not invent unverified capabilities. Put exclusions in the explicit out-of-scope section. The
plan must be implementable without the doer guessing and assertable item by item without the
tester interpreting intent.

Optimize for a working, maintainable product rather than theoretical perfection. Do not plan a
full-suite or from-scratch rerun merely because one check or adversarial review fails. Treat
speculative hardening, style preferences, vanishingly unlikely cases without evidence, and
unrelated feature requests as advisory exclusions. A review finding becomes blocking only when it
demonstrates an accepted-requirement violation, credible safety/data-loss risk, reproducible
failure, or likely production/orchestration failure.
