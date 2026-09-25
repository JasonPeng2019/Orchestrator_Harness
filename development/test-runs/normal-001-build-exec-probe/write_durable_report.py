"""Write the MI-NORMAL-001-BUILD-EXEC durable writer report (memory-harness-build-result/v1).

Disposable lane helper; produces exactly
development/evidence/STEP-001/NORMAL-001-BUILD-EXEC/result.json.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path("C:/Users/Jason/Documents/Jason/Orchestrator-Harness-3")
OUT = REPO / "development/evidence/STEP-001/NORMAL-001-BUILD-EXEC/result.json"
WT = (
    REPO
    / "development/product/worktree_example/.harness-runtime/worktrees"
    / "77574f69003e45a49701a47083c346c2/normal-001-build-exec"
)

report = {
    "schema": "memory-harness-build-result/v1",
    "status": "REVIEWABLE",
    "authority_note": (
        "Factual writer readback for MI-NORMAL-001-BUILD (M02-A1..A7). This is not ROOT "
        "acceptance and does not decide the next edge; M03/M04/M05 determine acceptance."
    ),
    "module_instance_id": "MI-NORMAL-001-BUILD",
    "card_id": "CARD-NORMAL-001-BUILD-EXEC",
    "invocation_id": "INVOCATION-NORMAL-001-BUILD-EXEC",
    "lane_id": "normal-001-build-exec",
    "run_id": "b5c03ad02022407bb1a2b3a1090518fd",
    "workflow_role": "writer",
    "deliverable_id": "DEL-001",
    "stage_cohort_id": "COHORT-001",
    "gate_id": "GATE-001",
    "loop_id": "LOOP-001",
    "repository_root": "C:/Users/Jason/Documents/Jason/Orchestrator-Harness-3",
    "worktree": {
        "path": str(WT),
        "branch": "lane/normal-001-build-exec",
        "epoch_id": "77574f69003e45a49701a47083c346c2",
    },
    "tips": {
        "starting_tip": "a54ad14a8f59409ee1e88c2473e3617c123f20b8",
        "reviewable_tip": "a54ad14a8f59409ee1e88c2473e3617c123f20b8",
        "tip_changed": False,
        "commit_created": None,
        "changed_paths": [],
        "note": (
            "Unchanged tip by design: no M02 pure helper is earned (helper-necessity "
            "decision below). No production change was made; nothing was committed."
        ),
    },
    "changed_paths_and_diff_status": {
        "tracked_source_changes": [],
        "status_porcelain_lines": [
            " M .codex/hooks/orchestrator_harness_post_tool_use.py",
            " M .codex/hooks/orchestrator_harness_stop.py",
            "?? .agent-workspace/",
            "?? .codex/skills/lane-assignment/",
            "?? .codex/skills/manager-notify/",
            "?? RESULT.json",
        ],
        "interpretation": (
            "The two .codex/hooks modifications and untracked .agent-workspace/, .codex/skills/ "
            "entries are runtime-staged overlay artifacts created by the managed launch "
            "(identical class of entries recorded by the accepted NORMAL-001-ADMIT-EXEC lane). "
            "RESULT.json is this lane's required native result artifact at the worktree root. "
            "No tracked product source file differs from the accepted baseline."
        ),
    },
    "inspected_entrypoints": [
        {
            "path": "development/product/worktree_example/harness/orchestrator_harness/operator_launch.py",
            "seam": "explicit adapter-option grammar/value validation and persistence (rejects NAME=VALUE violations and duplicate provider options)",
            "reimplemented": False,
        },
        {
            "path": "development/product/worktree_example/harness/orchestrator_harness/bootstrap.py",
            "seam": "provider launch-config validation before any lane mutation; requires explicit adapter options (narrow canonical blocker repair from f6948fb)",
            "reimplemented": False,
        },
        {
            "path": "development/product/worktree_example/harness/orchestrator_harness/provider_adapters/codex/launcher_binding.py",
            "seam": "codex launcher binding: requires reasoning_effort+service_tier, optional launcher in {codex, ollama}, rejects unsupported options",
            "reimplemented": False,
        },
        {
            "path": "development/product/worktree_example/harness/adapters/codex/harness/launcher_binding.py",
            "seam": "deployed copy of the same binding contract",
            "reimplemented": False,
        },
        {
            "path": "development/product/worktree_example/harness/orchestrator_harness/launch.py",
            "seam": "re-validates the invocation's canonical option form at launch time",
            "reimplemented": False,
        },
        {
            "path": "development/product/worktree_example/harness/orchestrator_harness/resume.py",
            "seam": "re-writes the invocation from the lane's persisted provider launch_config (effort/tier retained across resume)",
            "reimplemented": False,
        },
        {
            "path": "development/test-tools/resolve-role.py",
            "seam": "role -> canonical argv resolution from the isolated mapping",
            "reimplemented": False,
        },
        {
            "path": "development/test-tools/tests/test_resolve_role.py",
            "seam": "accepted resolver contract self-check (7 tests)",
            "reimplemented": False,
        },
        {
            "path": "references/harness-single/orchestrator_harness/bootstrap.py",
            "seam": "frozen canonical copy carrying the accepted blocker repair",
            "reimplemented": False,
        },
        {
            "path": "references/harness-single/orchestrator_harness/tests/test_v2_materialization.py",
            "seam": "the repair commit f6948fb's test half (frozen)",
            "reimplemented": False,
        },
    ],
    "canonical_repair_commit": {
        "commit": "f6948fb2673661b6c2cfb69cf47b23a198b3f5f8",
        "subject": "Fix managed lane bootstrap blockers",
        "files": [
            "orchestrator_harness/bootstrap.py",
            "orchestrator_harness/tests/test_v2_materialization.py",
        ],
        "consumed_not_reimplemented": True,
    },
    "requirement_invariant_map": [
        {
            "requirement": "REQ-001",
            "owner_deliverable": "DEL-007",
            "module_slice": "baseline subset only (full composition closes in STEP-007; integrated closure STEP-009)",
            "invariant_enforced_by_this_lane": (
                "STEP-001 does not implement the memory product; the pristine baseline keeps zero "
                "optional EverOS/Atlas calls and zero memory/APC context."
            ),
            "observed_evidence": (
                "No product source changed (tip unchanged at a54ad14a8f59409ee1e88c2473e3617c123f20b8); "
                "this lane's only execution was read-only inspection, resolver/unittest smoke, and the "
                "disposable stdlib control probe; M03 independent assets are pending."
            ),
            "claim": "preserved-not-closed",
        },
        {
            "requirement": "REQ-027",
            "owner_deliverable": "DEL-001",
            "invariant_enforced_by_this_lane": (
                "Distinct outer/inner ownership through the actual delegation chain; candidate "
                "entrypoint/build pinned; collision and test-ROOT-failure fixtures leave outer "
                "files/processes intact; nested capacity preflight; no outer-test lineage in ordinary records."
            ),
            "observed_evidence": (
                "Runtime boundary identity recorded: epoch 77574f69003e45a49701a47083c346c2 "
                "(launcher-owned, lifecycle active), single lane normal-001-build-exec, monitor healthy; "
                "invocation launcher entry python -m orchestrator_harness.controller; task card pins base "
                "commit a54ad14a. This lane launched no nested agent/delegation; the disposable probe's "
                "finite children were cleaned up with liveness readback. Fixture coverage is M03-owned."
            ),
            "claim": "boundary-recorded; fixtures-pending-M03",
        },
        {
            "requirement": "REQ-028",
            "owner_deliverable": "DEL-001",
            "invariant_enforced_by_this_lane": (
                "Requested/resolved/actual bindings recorded; explicit adapter options required; "
                "missing/duplicate/unrecognized options rejected before lane mutation; configured "
                "effort/tier retained through launch/resume; no substitution PASS."
            ),
            "observed_evidence": (
                "resolve-role.py 'writer' resolved identically against both harness roots to exactly "
                "['--provider','codex','--model','deepseek-v4.1-flash:cloud','--provider-option',"
                "'reasoning_effort=max','--provider-option','service_tier=normal','--provider-option',"
                "'launcher=ollama']; the lane's invocation.json and provider record carry that same "
                "launch_config (reasoning_effort=max, service_tier=normal, launcher=ollama); option "
                "validation/persistence seams (operator_launch/bootstrap/launcher_binding/launch/resume) "
                "inspected, not reimplemented; 7-test resolver contract self-check passed. Native coverage "
                "is claimed only for this actually-launched binding."
            ),
            "claim": "exact-match-no-substitution",
        },
        {
            "requirement": "REQ-029",
            "owner_deliverable": "DEL-010",
            "invariant_enforced_by_this_lane": (
                "Workload is purpose-built synthetic/source only; no benchmark adapter/task/subset/"
                "scored cohort, no learner implementation."
            ),
            "observed_evidence": (
                "Executed only unittest discovery on development/test-tools/tests "
                "(test_resolve_role.py) and the disposable stdlib probe under development/test-runs/; "
                "no benchmark or learner code was executed or modified."
            ),
            "claim": "clean",
        },
        {
            "requirement": "CONTROL-READY (plan-workflow binding)",
            "invariant_enforced_by_this_lane": (
                "Pre-product CONTROL-READY will run assembly cwd "
                "'python -m unittest discover -s development/test-tools/tests -p test_fixture_controls.py'; "
                "M03 authors the assets, M02 owns only a genuinely needed pure helper, M08 consumes them "
                "to exercise actual dispatch/handle/refill/checkpoint/owned-descendant cleanup with finite "
                "children; no scheduler/mock scheduler."
            ),
            "observed_evidence": (
                "development/test-tools/tests/test_fixture_controls.py does not exist yet "
                "(M03-owned, verified absent); the helper-necessity probe below shows the six required "
                "behaviors are expressible with Python stdlib + native OS controls, so no M02 helper "
                "was earned and no scheduler/runner was created."
            ),
            "claim": "assets-pending-M03; no-helper-earned",
        },
    ],
    "helper_necessity_decision": {
        "decision": "no_helper_earned",
        "rule_applied": (
            "M02 may add at most one small pure helper under development/test-tools/ only if an exact "
            "named M03/M08 consumer cannot express the required deterministic fixture data or readback "
            "without duplicating nontrivial logic; otherwise the correct smallest solution is no "
            "production change."
        ),
        "missing_responsibility_proven": False,
        "probe": {
            "path": "development/test-runs/normal-001-build-exec-probe/stdlib_control_probe.py",
            "disposition": "disposable probe evidence only; NOT an M03 asset; not an acceptance test",
            "command": "python development/test-runs/normal-001-build-exec-probe/stdlib_control_probe.py",
            "exit_code": 0,
            "ok": True,
            "behaviors": {
                "early_incompatible_terminal": "child sys.exit(3) -> 3",
                "independent_slow_success_and_ready_refill": "refill exit 0 observed while slow child still running; slow exit 0",
                "preserved_checkpoint": "JSON checkpoint read back after producing child exited",
                "lost_handle_reconciliation": "child-written pid record matched; liveness readback live=false",
                "lingering_owned_descendant": "descendant live after owner exit true -> taskkill /T /F exit 0 -> readback live=false",
                "probe_cleanup_readback": "no surviving probe child (pid readback live=false)",
            },
            "conclusion": (
                "Python stdlib (subprocess/ctypes/tempfile/json) plus native taskkill are sufficient for "
                "the six CONTROL-READY fixture behaviors; a production helper would duplicate stdlib "
                "capability, so none is earned and no diff was manufactured."
            ),
        },
    },
    "commands": [
        {"cmd": "git -C <worktree> rev-parse HEAD", "exit_code": 0, "observed": "a54ad14a8f59409ee1e88c2473e3617c123f20b8"},
        {"cmd": "git -C <worktree> status --porcelain=v1", "exit_code": 0, "observed": "6 lines: 2 modified runtime hook files, 4 untracked runtime artifacts (incl. RESULT.json); no tracked product source change"},
        {"cmd": "git -C references/harness-single rev-parse HEAD", "exit_code": 0, "observed": "f6948fb2673661b6c2cfb69cf47b23a198b3f5f8"},
        {"cmd": "git -C references/harness-single status --porcelain=v1", "exit_code": 0, "observed": "clean (no porcelain lines)"},
        {"cmd": "git -C references/harness-single show --name-only f6948fb", "exit_code": 0, "observed": "orchestrator_harness/bootstrap.py + orchestrator_harness/tests/test_v2_materialization.py"},
        {"cmd": "python development/test-tools/resolve-role.py --mapping .plans/SUBAGENT_ROLE_MODEL_MAPPING.json --harness-root references/harness-single writer", "exit_code": 0, "observed": "exact writer argv (codex / deepseek-v4.1-flash:cloud / reasoning_effort=max / service_tier=normal / launcher=ollama)"},
        {"cmd": "python development/test-tools/resolve-role.py --mapping .plans/SUBAGENT_ROLE_MODEL_MAPPING.json --harness-root development/product/worktree_example/harness writer", "exit_code": 0, "observed": "identical argv (cross-root equal)"},
        {"cmd": "python -m unittest discover -s development/test-tools/tests -p test_resolve_role.py", "exit_code": 0, "observed": "Ran 7 tests ... OK"},
        {"cmd": "SHA256 per-file comparison: 256 frozen tracked files vs same relative paths under development/dogfood/harness", "exit_code": 0, "observed": "tracked_total=256, match=255, mismatch=1 (harness-config.json only), missing=0"},
        {"cmd": "python development/test-runs/normal-001-build-exec-probe/stdlib_control_probe.py", "exit_code": 0, "observed": "ok: true (six CONTROL-READY behaviors)"},
        {"cmd": "python development/test-runs/normal-001-build-exec-probe/write_result.py", "exit_code": 0, "observed": "wrote worktree-root RESULT.json (result/v1), content_hash=5cc91bdffebd07a3688c0c0e42eaf93fb6bca31c52f3cd7b01e8350f680bba88"},
    ],
    "smoke_results": {
        "resolver_contract_unittest": {"command": "python -m unittest discover -s development/test-tools/tests -p test_resolve_role.py", "exit_code": 0, "tests_run": 7, "result": "OK"},
        "role_resolution_equality": {"result": "exact expected writer argv from both harness roots; equal to the lane's recorded invocation provider launch_config", "exit_code": 0},
        "control_ready_stdlib_probe": {"exit_code": 0, "ok": True, "detail": "six fixture behaviors read back (see helper_necessity_decision.probe)"},
        "deployed_b_byte_identity": {"result": "256 tracked frozen files vs B: match=255, mismatch=1 (harness-config.json, the protected local two-key config), missing=0"},
        "independent_m03_assets": {"path": "development/test-tools/tests/test_fixture_controls.py", "present": False, "note": "M03-owned; later execution is not a prerequisite for this reviewable tip"},
    },
    "protected_scope_confirmation": {
        "references_harness_single": "unchanged, clean at f6948fb2673661b6c2cfb69cf47b23a198b3f5f8",
        "development_dogfood_harness": "unchanged; byte identity re-verified (sole difference is its protected local harness-config.json)",
        "plan_files": "unchanged (read-only)",
        "shared_schemas_benchmarks_learned_selector_vendor_credentials_services": "untouched",
        "live_runtime_state": "untouched; only lane-owned records read/updated via the sanctioned lane-queue and result paths",
        "commits_pushes_deploys": "none",
        "new_scheduler_runner_framework_or_m03_asset": "none created",
        "writes_outside_authorized_paths": "none; durable report under development/evidence/STEP-001/NORMAL-001-BUILD-EXEC/, probe + helper scripts under disposable development/test-runs/, RESULT.json at the lane worktree root",
    },
    "unresolved_facts": [
        "M03 owns development/test-tools/tests/test_fixture_controls.py and its fixture finite children; those assets do not exist yet (verified absent). M03/M04/M05 acceptance and the M08 CONTROL-READY consumption remain pending.",
        "The root superproject HEAD is unresolvable (git exit 128) because of its submodule-style layout; deployed B has no independent git history. Recorded at admission, unchanged.",
        "Non-source __pycache__ bytecode composition differs between frozen source and B; that is outside the tracked-source byte-equality claim (recorded at admission).",
        "Disposable artifacts remain under development/test-runs/normal-001-build-exec-probe/ (stdlib_control_probe.py, write_result.py, write_durable_report.py); development/test-runs/ is disposable lane scope.",
    ],
    "recorded_at": None,  # filled below
}

from datetime import datetime, timezone

report["recorded_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

# verify parse + existence
parsed = json.loads(OUT.read_text(encoding="utf-8"))
assert parsed["schema"] == "memory-harness-build-result/v1"
assert parsed["status"] == "REVIEWABLE"
print(f"WROTE {OUT}")
print(f"bytes={OUT.stat().st_size}")
print(f"schema={parsed['schema']} status={parsed['status']} recorded_at={parsed['recorded_at']}")
