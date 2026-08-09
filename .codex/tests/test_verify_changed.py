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


def test_deleted_codex_test_runs_the_codex_test_root(tmp_path: Path) -> None:
    delta = VerificationDelta(
        manifest={},
        changed_paths=(Path(".codex/tests/test_removed.py"),),
    )
    plan = verify_changed.plan_changed_verification(tmp_path, delta)

    test_check = next(check for check in plan.checks if check.label == "Codex changed tests")
    assert ".codex/tests" in test_check.argv


def test_unknown_or_non_python_code_uses_full_fallback(tmp_path: Path) -> None:
    for relative in ("Firmware/app/main.c", "other/tool.py"):
        path = _write(tmp_path, relative, "code\n")
        delta = VerificationDelta(manifest={relative: "new"}, changed_paths=(path.relative_to(tmp_path),))
        plan = verify_changed.plan_changed_verification(tmp_path, delta)
        assert plan.full_fallback_reason is not None


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
