from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

import verify_changed
from dev_state import (
    STATE_PATH,
    VerificationDelta,
    record_verified_snapshot,
    repository_manifest,
    verification_delta,
)


def _write(root: Path, relative: str, text: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_versioned_manifest_reports_add_modify_and_delete(tmp_path: Path) -> None:
    source = _write(tmp_path, "source.py", "value = 1\n")
    record_verified_snapshot(tmp_path)
    state = json.loads((tmp_path / STATE_PATH).read_text(encoding="utf-8"))
    assert state["version"] == 2
    assert state["policy"] == "code-diff-v1"
    assert state["mode"] == "full"
    assert state["files"] == {"source.py": state["files"]["source.py"]}
    assert verification_delta(tmp_path).changed_paths == ()  # type: ignore[union-attr]

    source.write_text("value = 2\n", encoding="utf-8")
    assert verification_delta(tmp_path).changed_paths == (Path("source.py"),)  # type: ignore[union-attr]
    record_verified_snapshot(tmp_path)
    source.unlink()
    assert verification_delta(tmp_path).changed_paths == (Path("source.py"),)  # type: ignore[union-attr]


def test_obsolete_or_corrupt_state_requires_full_fallback(tmp_path: Path) -> None:
    _write(tmp_path, "source.py", "value = 1\n")
    state_path = tmp_path / STATE_PATH
    state_path.parent.mkdir(parents=True)
    state_path.write_text('{"snapshot": "legacy"}\n', encoding="utf-8")
    assert verification_delta(tmp_path) is None


def test_manifest_excludes_linked_worktrees_and_legacy_entries(tmp_path: Path) -> None:
    _write(tmp_path, "source.py", "value = 1\n")
    linked = _write(tmp_path, "Firmware/target-harness/.git", "gitdir: elsewhere\n")
    _write(tmp_path, "Firmware/target-harness/target.py", "value = 2\n")
    _write(
        tmp_path,
        "Firmware/fresh-experiments/A21/.agent-workspace/copied_firmware.c",
        "int main(void) { return 0; }\n",
    )
    _write(
        tmp_path,
        "Firmware/.agent-workspace/epochs/20260816-plan2-suite-008/build_prompt_bundle.py",
        "value = 3\n",
    )
    _write(
        tmp_path,
        "harness-single-worktrees/claude-test/orchestrator_harness/__init__.py",
        "value = 4\n",
    )
    _write(tmp_path, "scratch/session-analysis/analyze_session.py", "value = 5\n")

    manifest = repository_manifest(tmp_path)
    assert set(manifest) == {"source.py"}
    record_verified_snapshot(tmp_path, manifest=manifest)
    state_path = tmp_path / STATE_PATH
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["files"]["Firmware/target-harness/target.py"] = "legacy-target-worktree-entry"
    state["files"]["Firmware/fresh-experiments/A21/firmware/main.c"] = "legacy-run-entry"
    state["files"]["Firmware/.agent-workspace/epochs/20260816-plan2-suite-008/validate_invocation.py"] = (
        "legacy-epoch-entry"
    )
    state["files"]["harness-single-worktrees/claude-test/orchestrator_harness/tests/test_x.py"] = (
        "legacy-worktree-entry"
    )
    state["files"]["scratch/search_fw_blobs.py"] = "legacy-scratch-entry"
    state_path.write_text(json.dumps(state), encoding="utf-8")

    assert linked.is_file()
    assert verification_delta(tmp_path).changed_paths == ()  # type: ignore[union-attr]
    state_path.write_text("{bad json\n", encoding="utf-8")
    assert verification_delta(tmp_path) is None


def test_codex_script_change_selects_only_changed_static_and_codex_tests(
    tmp_path: Path,
) -> None:
    _write(tmp_path, ".codex/scripts/dev_state.py", "VALUE = 1\n")
    _write(tmp_path, ".codex/tests/test_hooks.py", "from dev_state import VALUE\n")
    manifest = {
        ".codex/scripts/dev_state.py": "new",
        ".codex/tests/test_hooks.py": "same",
    }
    delta = VerificationDelta(manifest=manifest, changed_paths=(Path(".codex/scripts/dev_state.py"),))
    plan = verify_changed.plan_changed_verification(tmp_path, delta)

    assert plan.full_fallback_reason is None
    labels = {check.label for check in plan.checks}
    assert labels == {
        "ruff changed Python",
        "format changed development Python",
        "types changed Python",
        "compile changed Python",
        "Codex changed tests",
    }
    joined = " ".join(argument for check in plan.checks for argument in check.argv)
    assert ".codex/tests/test_hooks.py" in joined
    assert "orchestrator_harness/tests" not in joined
    assert "harness_watcher_implementation/tests" not in joined
    assert str(verify_changed.FULL_VERIFY) not in joined


def test_bounded_supervisor_script_selects_its_regression_module(
    tmp_path: Path,
) -> None:
    _write(tmp_path, ".codex/scripts/Invoke-BoundedTest.ps1", "# bounded supervisor\n")
    _write(
        tmp_path,
        ".codex/tests/test_bounded_test_supervisor.py",
        "def test_supervisor():\n    pass\n",
    )
    manifest = {
        ".codex/scripts/Invoke-BoundedTest.ps1": "new",
        ".codex/tests/test_bounded_test_supervisor.py": "same",
    }
    delta = VerificationDelta(
        manifest=manifest,
        changed_paths=(Path(".codex/scripts/Invoke-BoundedTest.ps1"),),
    )

    plan = verify_changed.plan_changed_verification(tmp_path, delta)

    assert plan.full_fallback_reason is None
    labels = {check.label for check in plan.checks}
    assert labels == {"Codex changed tests"}
    test_check = next(check for check in plan.checks if check.label == "Codex changed tests")
    assert ".codex/tests/test_bounded_test_supervisor.py" in test_check.argv
    assert ".codex/tests" not in test_check.argv


def test_design_topology_validator_selects_static_and_embedded_self_test(
    tmp_path: Path,
) -> None:
    relative = verify_changed.DESIGN_TOPOLOGY_VALIDATOR.as_posix()
    _write(tmp_path, relative, "VALUE = 1\n")
    delta = VerificationDelta(
        manifest={relative: "new"},
        changed_paths=(verify_changed.DESIGN_TOPOLOGY_VALIDATOR,),
    )

    plan = verify_changed.plan_changed_verification(tmp_path, delta)

    assert plan.full_fallback_reason is None
    checks = {check.label: check for check in plan.checks}
    assert set(checks) == {
        "ruff changed Python",
        "format changed development Python",
        "types changed Python",
        "compile changed Python",
        "design topology validator self-test",
    }
    assert checks["design topology validator self-test"].argv == (
        sys.executable,
        relative,
        "--self-test",
    )


def test_orchestrator_dependency_selects_importing_test_module(tmp_path: Path) -> None:
    _write(
        tmp_path,
        "stable-general-harness-runner/orchestrator_harness/reconcile.py",
        "VALUE = 1\n",
    )
    _write(
        tmp_path,
        "stable-general-harness-runner/orchestrator_harness/tests/test_reconcile.py",
        "from orchestrator_harness.reconcile import VALUE\n",
    )
    manifest = {
        "stable-general-harness-runner/orchestrator_harness/reconcile.py": "new",
        "stable-general-harness-runner/orchestrator_harness/tests/test_reconcile.py": "same",
    }
    delta = VerificationDelta(
        manifest=manifest,
        changed_paths=(Path("stable-general-harness-runner/orchestrator_harness/reconcile.py"),),
    )
    plan = verify_changed.plan_changed_verification(tmp_path, delta)

    test_check = next(check for check in plan.checks if check.label == "orchestrator changed tests")
    assert "orchestrator_harness.tests.test_reconcile" in test_check.argv
    assert "discover" not in test_check.argv
    assert all(check.label != "watcher changed tests" for check in plan.checks)


def test_firmware_skill_change_selects_its_test_suite(tmp_path: Path) -> None:
    relative = "Firmware/.codex/skills/run-firmware-test-suite/scripts/audit_autonomy.py"
    _write(tmp_path, relative, "VALUE = 1\n")
    _write(
        tmp_path,
        "Firmware/.codex/skills/run-firmware-test-suite/tests/test_audit_autonomy.py",
        "VALUE = 1\n",
    )
    delta = VerificationDelta(
        manifest={relative: "new"},
        changed_paths=(Path(relative),),
    )

    plan = verify_changed.plan_changed_verification(tmp_path, delta)

    assert plan.full_fallback_reason is None
    test_check = next(check for check in plan.checks if check.label == "firmware changed tests")
    assert test_check.argv == (
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        "Firmware/.codex/skills/run-firmware-test-suite/tests",
    )


def test_firmware_change_loop_and_prompt_policy_select_targeted_checks(
    tmp_path: Path,
) -> None:
    shell_relative = "Firmware/.codex/skills/change-loop/scripts/agent.sh"
    policy_relative = "Firmware/scripts/orchestration/prompt_policy.py"
    _write(tmp_path, shell_relative, "#!/usr/bin/env bash\n")
    _write(tmp_path, policy_relative, "VALUE = 1\n")
    delta = VerificationDelta(
        manifest={shell_relative: "new", policy_relative: "new"},
        changed_paths=(Path(shell_relative), Path(policy_relative)),
    )

    plan = verify_changed.plan_changed_verification(tmp_path, delta)

    assert plan.full_fallback_reason is None
    checks = {check.label: check for check in plan.checks}
    assert checks["Firmware change-loop self-check"].argv == (
        "bash",
        "Firmware/.codex/skills/change-loop/scripts/run_loop.sh",
        "--self-check",
    )
    assert "firmware changed tests" in checks
    assert "compile changed Python" in checks


def test_firmware_mcp_change_uses_its_package_checks(tmp_path: Path) -> None:
    relative = "Firmware/BYO-Firmware-MCP/tests/test_import_smoke.py"
    path = _write(tmp_path, relative, "VALUE = 1\n")
    delta = VerificationDelta(
        manifest={relative: "new"},
        changed_paths=(path.relative_to(tmp_path),),
    )

    plan = verify_changed.plan_changed_verification(tmp_path, delta)

    assert plan.full_fallback_reason is None
    checks = {check.label: check for check in plan.checks}
    assert set(checks) == {
        "Firmware MCP Ruff",
        "Firmware MCP Pyright",
        "Firmware MCP tests",
    }
    assert all(check.cwd == tmp_path / "Firmware" / "BYO-Firmware-MCP" for check in checks.values())
    assert checks["Firmware MCP Ruff"].argv == (
        "uv",
        "run",
        "--locked",
        "--no-sync",
        "ruff",
        "check",
        ".",
    )
    assert checks["Firmware MCP Pyright"].argv == (
        "uv",
        "run",
        "--locked",
        "--no-sync",
        "pyright",
    )
    assert checks["Firmware MCP tests"].argv == (
        "uv",
        "run",
        "--locked",
        "--no-sync",
        "pytest",
    )


def test_deleted_codex_test_runs_the_codex_test_root(tmp_path: Path) -> None:
    delta = VerificationDelta(
        manifest={},
        changed_paths=(Path(".codex/tests/test_removed.py"),),
    )
    plan = verify_changed.plan_changed_verification(tmp_path, delta)

    test_check = next(check for check in plan.checks if check.label == "Codex changed tests")
    assert ".codex/tests" in test_check.argv


def test_unknown_or_non_python_code_requires_a_targeted_route(tmp_path: Path) -> None:
    for relative in ("Firmware/app/main.c", "other/tool.py"):
        path = _write(tmp_path, relative, "code\n")
        delta = VerificationDelta(manifest={relative: "new"}, changed_paths=(path.relative_to(tmp_path),))
        plan = verify_changed.plan_changed_verification(tmp_path, delta)
        assert plan.full_fallback_reason is not None


def test_unsupported_changed_code_does_not_run_full_verification(monkeypatch, tmp_path: Path, capsys) -> None:
    delta = VerificationDelta(
        manifest={"Firmware/app/main.c": "new"},
        changed_paths=(Path("Firmware/app/main.c"),),
    )
    monkeypatch.setattr(verify_changed, "verification_delta", lambda _root: delta)
    monkeypatch.setattr(
        verify_changed,
        "_run_full_fallback",
        lambda *_args: (_ for _ in ()).throw(AssertionError("must not run full verification")),
    )

    assert verify_changed.run_changed_verification(tmp_path) == 1
    assert "add a targeted verification route" in capsys.readouterr().err


def test_failed_targeted_check_leaves_previous_state(monkeypatch, tmp_path: Path) -> None:
    state_path = _write(tmp_path, STATE_PATH.as_posix(), '{"sentinel": true}\n')
    delta = VerificationDelta(manifest={".codex/scripts/tool.py": "new"}, changed_paths=(Path("tool.py"),))
    check = verify_changed.Check("selected", ("failing",), tmp_path)
    monkeypatch.setattr(verify_changed, "verification_delta", lambda _root: delta)
    monkeypatch.setattr(
        verify_changed,
        "plan_changed_verification",
        lambda _root, _delta: verify_changed.VerificationPlan(checks=(check,)),
    )
    monkeypatch.setattr(
        verify_changed.subprocess,
        "run",
        lambda *_args, **_kwargs: subprocess.CompletedProcess([], 1),
    )

    assert verify_changed.run_changed_verification(tmp_path) == 1
    assert json.loads(state_path.read_text(encoding="utf-8")) == {"sentinel": True}


def test_code_mutation_during_checks_fails_without_recording(monkeypatch, tmp_path: Path) -> None:
    delta = VerificationDelta(manifest={"source.py": "before"}, changed_paths=(Path("source.py"),))
    check = verify_changed.Check("selected", ("passing",), tmp_path)
    monkeypatch.setattr(verify_changed, "verification_delta", lambda _root: delta)
    monkeypatch.setattr(
        verify_changed,
        "plan_changed_verification",
        lambda _root, _delta: verify_changed.VerificationPlan(checks=(check,)),
    )
    monkeypatch.setattr(
        verify_changed.subprocess,
        "run",
        lambda *_args, **_kwargs: subprocess.CompletedProcess([], 0),
    )
    monkeypatch.setattr(verify_changed, "repository_manifest", lambda _root: {"source.py": "after"})
    monkeypatch.setattr(
        verify_changed,
        "record_verified_snapshot",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("state must not be recorded")),
    )

    assert verify_changed.run_changed_verification(tmp_path) == 1


def test_successful_targeted_checks_record_routes(monkeypatch, tmp_path: Path) -> None:
    manifest = {"source.py": "stable"}
    delta = VerificationDelta(manifest=manifest, changed_paths=(Path("source.py"),))
    check = verify_changed.Check("selected", ("passing",), tmp_path)
    recorded: dict[str, object] = {}
    monkeypatch.setattr(verify_changed, "verification_delta", lambda _root: delta)
    monkeypatch.setattr(
        verify_changed,
        "plan_changed_verification",
        lambda _root, _delta: verify_changed.VerificationPlan(checks=(check,)),
    )
    monkeypatch.setattr(
        verify_changed.subprocess,
        "run",
        lambda *_args, **_kwargs: subprocess.CompletedProcess([], 0),
    )
    monkeypatch.setattr(verify_changed, "repository_manifest", lambda _root: manifest)

    def record(_root: Path, **kwargs: object) -> None:
        recorded.update(kwargs)

    monkeypatch.setattr(verify_changed, "record_verified_snapshot", record)
    assert verify_changed.run_changed_verification(tmp_path) == 0
    assert recorded["mode"] == "changed"
    assert tuple(recorded["routes"]) == ("selected",)  # type: ignore[arg-type]
    assert recorded["manifest"] == manifest


def test_missing_manifest_runs_full_fallback(monkeypatch, tmp_path: Path) -> None:
    calls: list[tuple[str, ...]] = []
    monkeypatch.setattr(verify_changed, "verification_delta", lambda _root: None)

    def run(argv: tuple[str, ...] | list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append(tuple(argv))
        return subprocess.CompletedProcess(argv, 0)

    monkeypatch.setattr(verify_changed.subprocess, "run", run)
    monkeypatch.setattr(verify_changed, "verification_is_current", lambda _root: True)
    assert verify_changed.run_changed_verification(tmp_path) == 0
    assert calls == [(sys.executable, str(verify_changed.FULL_VERIFY))]
