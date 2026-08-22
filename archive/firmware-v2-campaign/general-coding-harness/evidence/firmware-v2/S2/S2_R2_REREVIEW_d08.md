# S2.R2 repaired-tip rereview — FAIL

Reviewed `c998e41ad30b7a20ab36ed8f659483a29b376e7f..d08b6ccf3d2e0eacd3686b01658645249dfcc0a0`
on `firmware/v2-s2-r2`, read-only and without MCP, hardware, or product-test execution. The original
review remains unchanged in `REVIEW.md`.

## Repair credit

The repair materially improves the initial state: materialization is confined below the broker and
creates a disposable Git commit ([kit.py:118-137](../firmware_acceptance/kit.py#L118-L137));
validation checks seed hashes and file read-only mode ([kit.py:139-150](../firmware_acceptance/kit.py#L139-L150));
the immutable call chain now requires the immediately prior same-call record and `admit` checks its
complete sequence ([kit.py:170-227](../firmware_acceptance/kit.py#L170-L227)); policy now includes
the RF bounds it enforces ([kit.py:254-266](../firmware_acceptance/kit.py#L254-L266)); and the
findings schema validator is closed for a submitted findings file
([git_safety.py:47-77](../orchestrator_harness/git_safety.py#L47-L77)). The non-gating list remains
properly bounded ([TEST_CONTRACT.json:1](../firmware_acceptance/seed/TEST_CONTRACT.json#L1)).

## Accepted findings

Three functionality-breaking findings are recorded in `FINDINGS.json`:

1. `S2R2-F01`: the declared per-ID acceptance contract, fingerprint/selective-rerun registry,
   executable oracles, failure routes, and closed evidence objects are still absent. The revised
   charter asserts these properties, but the contract remains only lists plus strings
   ([TARGET_CHARTER.md:3](../firmware_acceptance/seed/TARGET_CHARTER.md#L3),
   [TEST_CONTRACT.json:1](../firmware_acceptance/seed/TEST_CONTRACT.json#L1)).
2. `S2R2-F02`: seed integrity and no-capability claims are check-on-demand conventions, not a
   continuously enforced target-worker isolation boundary; hostile proofs remain untested
   ([kit.py:118-168](../firmware_acceptance/kit.py#L118-L168),
   [test_firmware_acceptance_kit.py:21-48](../orchestrator_harness/tests/test_firmware_acceptance_kit.py#L21-L48)).
3. `S2R2-F03`: manager triage is an unused validator, so mandatory finding disposition is not
   gated by the result path ([git_safety.py:80-100](../orchestrator_harness/git_safety.py#L80-L100),
   [lane_controller.py:597-617](../orchestrator_harness/lane_controller.py#L597-L617)).

## Rejected criticisms

I reject requiring live boards, MCP execution, manual oracles, DIO2 wiring, or a generalized
scheduler/hardware platform: each is outside this deliberately static and DIO2-independent
acceptance scope. I also reject style-only, cleanup-only, speculative hardening, and preference
criticisms. The three findings are retained because each has a direct failure path and a narrow,
lower-cost fix recorded in the closed findings artifact.

The refreshed governing-observation, ROOT join, and ROOT triage artifacts named in the request
were not present in this isolated worktree's supplied files. This rereview therefore does not
assert facts from them; the three findings above are independently reproducible from the repaired
candidate itself.
