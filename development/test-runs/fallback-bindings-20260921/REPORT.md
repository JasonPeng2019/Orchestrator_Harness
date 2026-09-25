# Non-Codex fallback launch verification

2026-09-21 — VERIFY: PASS (focused live launch/tool/result/cleanup).

## Scope and result

The canonical mapping has eight fallback entries. Seven use direct Codex and
were explicitly excluded by the user. The only in-scope entry is test_author's
first fallback: Claude Opus 4.8, MAX, through the Claude CLI.

That binding passed: actual tool execution, computed answer 424, identity-bound
proof, valid RESULT.json SHA256, native successful provider result and model usage,
zero exit code, and proven process-tree cleanup. The provider reported
claude-opus-4-8. No other model was launched, and no automatic fallback was enabled.

## Correction

The original mapped identifier, claude-opus-4.8, returned model_not_found / HTTP
404 before model execution. [Anthropic's model reference](https://platform.claude.com/docs/fr/models/opus-4-8/overview)
specifies claude-opus-4-8. Corrected that single value in
.plans/SUBAGENT_ROLE_MODEL_MAPPING.json and tested it in a fresh invocation after
the failed provider's cleanup was proven. This preserves the requested model
version, MAX effort, fallback order, OAuth/usage-cap-only transition policy, and
reset-to-preferred behavior for subsequent ordinary launches.

This task explicitly tested a fallback candidate directly; it did not exercise
or claim a policy-triggered failover. The 404 did not advance the fallback chain.

No harness/product source changes were needed. The disposable harness was cloned
from references/harness-single at d679c1f792bd46e78a0bfcefc0e4991e43dfb409 with the
existing authorized Ollama repair overlaid. Its Claude binding was byte-identical
to the master. Local core.longpaths=true was set only in the disposable workspace.

## Evidence

- [audit_result.py](audit_result.py): read-only independent checks.
- [audit-result.json](audit-result.json): PASS, tested binding, excluded entries,
  exact invocation/session, actual model, result hash, argv and cleanup.
- [Original card](cards/test-author-opus.json) and
  [corrected-invocation card](cards/test-author-opus-corrected.json).
- Native records: workspace/.harness-runtime/epochs/
  d5f003706ec444198a018186f69ed547/lanes/.
  test-author-opus-01 preserves the 404; test-author-opus-02 is the passing retry.
- Runtime state is CLOSED. Both lanes are retired, both provider boundaries
  have proven cleanup, the monitor stopped, and both manager events were closed.

## Commands and checks

From harness/:
- python -B -m orchestrator_harness.operator_launch --json harness setup
- python -B -m orchestrator_harness.operator_launch --json scan --no-write
- python -B -m orchestrator_harness.operator_launch --json lane bootstrap --lane-id test-author-opus-02 --provider claude-code --model claude-opus-4-8 --provider-option effort=max --task-card ../cards/test-author-opus-corrected.json
- python -B -m orchestrator_harness.operator_launch --json lane launch --lane-id test-author-opus-02
- Native watch, acknowledgement, PASS/ACCEPTED completion review, and shutdown:
  SHUTDOWN_OK.

From this directory: python -B audit_result.py — PASS.
Formal compiler check and canonical plan validator — PASS; no changed source
units or review candidates, source hash remains
b81317479f7c2f9bc7f00555fecb8e96f015bd662d9a4558b79987c637ea9fc4.

No direct-Codex fallback was retested. No benchmark, full product test, test-authoring
quality evaluation, failover-policy execution, live resume or release gate is
claimed. Claude's warning about untrusted workspace allow entries did not prevent
this explicitly bypass-permissions launch; no global trust settings were edited.
