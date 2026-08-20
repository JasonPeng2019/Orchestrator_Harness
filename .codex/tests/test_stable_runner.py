from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import types
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = ROOT / ".codex" / "scripts" / "stable_runner.py"
STABLE = ROOT / "stable-general-harness-runner"
LOCK = (
    ROOT
    / "plans"
    / "general-coding-harness"
    / "runtime"
    / "firmware-v2"
    / "runner-migration"
    / "STABLE_RUNNER_LOCK.json"
)
RUNNER_MIGRATION = ROOT / "plans" / "general-coding-harness" / "runtime" / "firmware-v2" / "runner-migration"
PENDING_S2_D1 = (
    ROOT
    / "plans"
    / "general-coding-harness"
    / "runtime"
    / "firmware-v2"
    / "implementation"
    / "lanes"
    / "S2.D1"
    / ".agent-workspace"
    / "worker.invocation.json"
)


def _role_model_mapping_path() -> Path:
    runner = _load_runner()
    path = runner.ROLE_MODEL_MAPPING_PATH
    assert isinstance(path, Path)
    return path


def _role_allocations() -> dict[str, dict[str, object]]:
    runner = _load_runner()
    allocations = runner._read_role_model_mapping(_role_model_mapping_path())
    assert isinstance(allocations, dict)
    return allocations


def _role_allocation(role: str) -> dict[str, object]:
    return _role_allocations()[role]


def _model_settings(role: str) -> dict[str, str]:
    allocation = _role_allocation(role)
    model = allocation["model"]
    effort = allocation["reasoning_effort"]
    tier = allocation["service_tier"]
    assert isinstance(model, str) and isinstance(effort, str) and isinstance(tier, str)
    return {
        "model": model,
        "reasoning_effort": effort,
        "service_tier": tier,
    }


def _full_access_settings() -> dict[str, object]:
    return {
        "sandbox": "danger-full-access",
        "approval_policy": "never",
        "config_overrides": [],
    }


def _load_runner():
    spec = importlib.util.spec_from_file_location("stable_runner_under_test", LAUNCHER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _init_overlay_repository(path: Path) -> None:
    subprocess.run(
        ["git", "init", "--initial-branch", "main", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )


def _lock_copy(path: Path) -> None:
    path.write_bytes(LOCK.read_bytes())


def _clone_for_validation(base: Path) -> Path:
    destination = base / "stable-general-harness-runner"
    completed = subprocess.run(
        ["git", "clone", "--no-hardlinks", "--no-local", str(STABLE), str(destination)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    subprocess.run(
        [
            "git",
            "-C",
            str(destination),
            "switch",
            "--detach",
            "4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return destination


def test_lock_proves_clean_detached_stable_checkout() -> None:
    runner = _load_runner()
    proof = runner.validate_checkout()
    assert proof["stable_root"] == str(STABLE.resolve())
    assert proof["commit"] == "4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f"
    assert proof["clean"] is True
    assert proof["detached"] is True


def test_dirty_and_wrong_commit_disposable_substitutes_fail_closed() -> None:
    runner = _load_runner()
    with tempfile.TemporaryDirectory() as raw:
        base = Path(raw)
        lock_dir = base / "lock"
        lock_dir.mkdir()
        lock_path = lock_dir / "lock.json"
        _lock_copy(lock_path)
        wrong_base = base / "wrong"
        wrong_base.mkdir()
        wrong = _clone_for_validation(wrong_base)
        subprocess.run(
            ["git", "-C", str(wrong), "switch", "--detach", "HEAD~1"],
            check=True,
            capture_output=True,
        )
        with pytest.raises(runner.RunnerError, match="commit"):
            runner.validate_checkout(lock_path=lock_path, repository_root=base / "wrong")

        dirty_base = base / "dirty"
        dirty_base.mkdir()
        dirty = _clone_for_validation(dirty_base)
        with (dirty / "README.md").open("a", encoding="utf-8") as handle:
            handle.write("\nintentional disposable dirt\n")
        with pytest.raises(runner.RunnerError, match="dirty"):
            runner.validate_checkout(lock_path=lock_path, repository_root=dirty_base)


def test_conflicting_preloaded_import_is_rejected() -> None:
    runner = _load_runner()
    fake = types.ModuleType("orchestrator_harness")
    fake.__file__ = str(Path(tempfile.gettempdir()) / "wrong" / "orchestrator_harness" / "__init__.py")
    prior = sys.modules.get("orchestrator_harness")
    sys.modules["orchestrator_harness"] = fake
    try:
        with pytest.raises(runner.RunnerError, match="conflicting preloaded import"):
            runner.import_stable_module("orchestrator_harness.cli", runner.validate_checkout())
    finally:
        if prior is None:
            sys.modules.pop("orchestrator_harness", None)
        else:
            sys.modules["orchestrator_harness"] = prior


def test_projection_is_explicit_and_role_resolved() -> None:
    runner = _load_runner()
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        source = root / "candidate.json"
        output = root / "stable.json"
        record_path = root / "projection.json"
        source_value = {
            "schema": "orchestrator-coding-invocation/v1",
            "action": "start",
            "run_root": str(root),
            "prompt_path": str(root / "prompt.md"),
            "prompt_sha256": "a" * 64,
            "output_paths": {
                "status": str(root / "status.json"),
                "jsonl": str(root / "out.jsonl"),
                "stderr": str(root / "err.log"),
                "last_message": str(root / "last.txt"),
            },
            "runtime_root": str(root),
            "worker_invocation_id": "worker-1",
            "lane_id": "lane-1",
            "task": "proof",
            "phase": "test",
            "repository": {
                "common_dir": str(root),
                "worktree_root": str(root),
                "branch": "main",
                "base_commit": "a" * 40,
            },
            "codex": {
                "command": ["codex"],
                "model": "source-placeholder",
                "reasoning_effort": "source-placeholder",
                "service_tier": "source-placeholder",
                "sandbox": "danger-full-access",
                "approval_policy": "never",
                "config_overrides": [],
            },
            "finding_gate": {
                "role": _role_allocation("doer-main")["finding_gate_role"],
                "path": str(root / ".agent-workspace" / "FINDINGS.json"),
            },
            "child_environment_isolation": True,
        }
        source.write_text(json.dumps(source_value), encoding="utf-8")
        record = runner.project_invocation(
            input_path=source,
            output_path=output,
            record_path=record_path,
            proof=runner.validate_checkout(),
            workflow_role="doer-main",
        )
        projected = json.loads(output.read_text(encoding="utf-8"))
        assert {
            key: projected["codex"][key] for key in ("model", "reasoning_effort", "service_tier")
        } == _model_settings("doer-main")
        assert "finding_gate" not in projected
        assert "child_environment_isolation" not in projected
        assert {item["field"] for item in record["removed_candidate_only_fields"]} == {
            "finding_gate",
            "child_environment_isolation",
        }
        assert record["projected_invocation_sha256"] == runner.hashlib.sha256(output.read_bytes()).hexdigest()
        assert record["workflow_role"] == "doer-main"
        source_value["unrecognized"] = True
        source.write_text(json.dumps(source_value), encoding="utf-8")
        with pytest.raises(runner.RunnerError, match="unknown fields"):
            runner.project_invocation(
                input_path=source,
                output_path=root / "second.json",
                record_path=root / "second-record.json",
                proof=runner.validate_checkout(),
                workflow_role="doer-main",
            )
        with pytest.raises(runner.RunnerError, match="inside the immutable stable checkout"):
            runner.project_invocation(
                input_path=source,
                output_path=STABLE / "runner-migration-test-output.json",
                record_path=root / "stable-output-record.json",
                proof=runner.validate_checkout(),
                workflow_role="doer-main",
            )


@pytest.mark.parametrize("workflow_role", sorted(_role_allocations()))
def test_workflow_roles_resolve_current_mapping(workflow_role: str) -> None:
    runner = _load_runner()
    allocation = _role_allocation(workflow_role)
    gate_role = allocation["finding_gate_role"]
    invocation = {
        "schema": "orchestrator-coding-invocation/v1",
        "codex": {
            "model": "source-placeholder",
            "reasoning_effort": "source-placeholder",
            "service_tier": "source-placeholder",
            **_full_access_settings(),
        },
    }
    if gate_role is not None:
        invocation["finding_gate"] = {"role": gate_role, "path": "FINDINGS.json"}
    resolved = runner.apply_workflow_role_allocation(invocation, workflow_role, validate_finding_gate=True)
    assert {key: resolved["codex"][key] for key in ("model", "reasoning_effort", "service_tier")} == (
        _model_settings(workflow_role)
    )
    settings = resolved["codex"]
    assert settings["sandbox"] == "danger-full-access"
    assert settings["approval_policy"] == "never"
    assert "--dangerously-bypass-approvals-and-sandbox" not in settings["command"]
    assert "--ignore-user-config" not in settings["command"]
    assert 'approval_policy="never"' in settings["config_overrides"]
    assert 'approvals_reviewer="user"' in settings["config_overrides"]


@pytest.mark.parametrize("workflow_role", sorted(_role_allocations()))
def test_workflow_role_allocations_replace_materialized_settings(
    workflow_role: str,
) -> None:
    runner = _load_runner()
    settings = _model_settings(workflow_role)
    settings["model"] += "-stale"
    gate_role = _role_allocation(workflow_role)["finding_gate_role"]
    invocation = {
        "schema": "orchestrator-coding-invocation/v1",
        "codex": {**settings, **_full_access_settings()},
    }
    if gate_role is not None:
        invocation["finding_gate"] = {"role": gate_role, "path": "FINDINGS.json"}
    resolved = runner.apply_workflow_role_allocation(invocation, workflow_role, validate_finding_gate=True)
    assert {key: resolved["codex"][key] for key in ("model", "reasoning_effort", "service_tier")} == (
        _model_settings(workflow_role)
    )


def test_workflow_role_allocation_rejects_wrong_finding_gate_role() -> None:
    runner = _load_runner()
    allocation = _role_allocation("reviewer-main")
    expected_gate_role = allocation["finding_gate_role"]
    assert isinstance(expected_gate_role, str)
    invocation = {
        "schema": "orchestrator-coding-invocation/v1",
        "codex": {**_model_settings("reviewer-main"), **_full_access_settings()},
        "finding_gate": {
            "role": expected_gate_role + "-wrong",
            "path": "FINDINGS.json",
        },
    }
    with pytest.raises(runner.RunnerError, match="requires finding_gate role"):
        runner.apply_workflow_role_allocation(invocation, "reviewer-main", validate_finding_gate=True)


def test_real_codex_subagent_prompt_requires_bounded_test_contract(
    tmp_path: Path,
) -> None:
    runner = _load_runner()
    prompt = tmp_path / "prompt.md"
    prompt.write_text("Implement the task.\n", encoding="utf-8")
    invocation = {"prompt_path": str(prompt), "codex": {"command": ["codex"]}}
    with pytest.raises(runner.RunnerError, match="bounded-test contract"):
        runner._require_bounded_test_prompt(invocation)

    prompt.write_text(
        "Follow BOUNDED-TEST-v1 through Invoke-BoundedTest.ps1.\n",
        encoding="utf-8",
    )
    runner._require_bounded_test_prompt(invocation)

    runner._require_bounded_test_prompt(
        {
            "prompt_path": str(prompt),
            "codex": {"command": [sys.executable, "fake_codex.py"]},
        }
    )


def test_real_codex_dispatch_gets_temporary_bounded_test_hook(tmp_path: Path) -> None:
    runner = _load_runner()
    _init_overlay_repository(tmp_path)
    hooks = tmp_path / ".codex" / "hooks.json"
    invocation = {"run_root": str(tmp_path), "codex": {"command": ["codex"]}}

    with runner._codex_bounded_test_overlay(invocation):
        value = json.loads(hooks.read_text(encoding="utf-8"))
        assert "PreToolUse" in value["hooks"]
        assert "SessionStart" in value["hooks"]
        assert value["hooks"]["PreToolUse"][0]["matcher"] == "^(Bash|shell_command)$"
        assert any(
            key.startswith("GIT_CONFIG_KEY_") and setting == "core.excludesFile" for key, setting in os.environ.items()
        )
        sanitized = os.environ.copy()
        for key in tuple(sanitized):
            if key.startswith("GIT_CONFIG_"):
                sanitized.pop(key)
        status = subprocess.run(
            [
                "git",
                "-C",
                str(tmp_path),
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ],
            check=False,
            capture_output=True,
            text=True,
            env=sanitized,
        )
        assert status.returncode == 0, status.stderr
        assert status.stdout == ""

    assert not hooks.exists()
    assert not hooks.parent.exists()


def test_injected_hook_bounds_nested_work_but_not_stable_launcher(
    tmp_path: Path,
) -> None:
    runner = _load_runner()
    _init_overlay_repository(tmp_path)
    hooks = tmp_path / ".codex" / "hooks.json"
    invocation = {"run_root": str(tmp_path), "codex": {"command": ["codex"]}}

    with runner._codex_bounded_test_overlay(invocation):
        value = json.loads(hooks.read_text(encoding="utf-8"))
        assert value["hooks"]["PreToolUse"][0]["matcher"] == "^(Bash|shell_command)$"
        command = value["hooks"]["PreToolUse"][0]["hooks"][0]["commandWindows"]
        nested = subprocess.run(
            [
                "C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
                "-NoLogo",
                "-NoProfile",
                "-Command",
                command,
            ],
            cwd=tmp_path,
            input=json.dumps(
                {
                    "cwd": str(tmp_path),
                    "tool_input": {"command": 'python -c "print(1)"'},
                }
            ),
            text=True,
            capture_output=True,
            check=False,
        )
        assert nested.returncode == 0, nested.stderr
        assert json.loads(nested.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny"

        stable = subprocess.run(
            [
                "C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
                "-NoLogo",
                "-NoProfile",
                "-Command",
                command,
            ],
            cwd=tmp_path,
            input=json.dumps(
                {
                    "cwd": str(tmp_path),
                    "tool_input": {
                        "command": f'python -I "{LAUNCHER}" --module orchestrator_harness.lane_controller invocation.json'
                    },
                }
            ),
            text=True,
            capture_output=True,
            check=False,
        )
        assert stable.returncode == 0, stable.stderr
        assert json.loads(stable.stdout) == {}


def test_bounded_test_overlay_merges_and_restores_existing_hook(tmp_path: Path) -> None:
    runner = _load_runner()
    _init_overlay_repository(tmp_path)
    hooks = tmp_path / ".codex" / "hooks.json"
    hooks.parent.mkdir()
    original = b'{"description":"product hook","hooks":{"Stop":[]}}\n'
    hooks.write_bytes(original)
    invocation = {"run_root": str(tmp_path), "codex": {"command": ["codex"]}}

    with runner._codex_bounded_test_overlay(invocation):
        value = json.loads(hooks.read_text(encoding="utf-8"))
        assert value["description"] == "product hook"
        assert value["hooks"]["Stop"] == []
        assert "PreToolUse" in value["hooks"]
        assert "SessionStart" in value["hooks"]

    assert hooks.read_bytes() == original


def test_bounded_test_overlay_restores_existing_hook_after_launch_error(
    tmp_path: Path,
) -> None:
    runner = _load_runner()
    _init_overlay_repository(tmp_path)
    hooks = tmp_path / ".codex" / "hooks.json"
    hooks.parent.mkdir()
    original = b'{"description":"product hook","hooks":{"Stop":[]}}\n'
    hooks.write_bytes(original)
    invocation = {"run_root": str(tmp_path), "codex": {"command": ["codex"]}}

    with pytest.raises(RuntimeError, match="launch failed"):
        with runner._codex_bounded_test_overlay(invocation):
            raise RuntimeError("launch failed")

    assert hooks.read_bytes() == original


def test_workflow_role_mapping_is_adjustable_without_code_changes() -> None:
    runner = _load_runner()
    custom_profile = {
        "model": "custom-model",
        "reasoning_effort": "custom-effort",
        "service_tier": "custom-tier",
        "codex_flags": [],
        "model_context_window": None,
        "model_auto_compact_token_limit": None,
        "model_auto_compact_token_limit_scope": None,
        "model_catalog_path": None,
    }
    custom_role = {
        "primary_profile": "custom-profile",
        "fallback_profile": None,
        "fallback_after_consecutive_backend_failures": None,
        "fallback_error_classes": [],
        "finding_gate_role": None,
    }
    with tempfile.TemporaryDirectory() as raw:
        policy = Path(raw) / "allocations.json"
        policy.write_text(
            json.dumps(
                {
                    "schema": "orchestrator-subagent-role-model-mapping/v2",
                    "profiles": {"custom-profile": custom_profile},
                    "roles": {"custom-role": custom_role},
                }
            ),
            encoding="utf-8",
        )
        invocation = {
            "schema": "orchestrator-coding-invocation/v1",
            "codex": {
                "model": "source-placeholder",
                "reasoning_effort": "source-placeholder",
                "service_tier": "source-placeholder",
                **_full_access_settings(),
            },
        }
        resolved = runner.apply_workflow_role_allocation(
            invocation,
            "custom-role",
            validate_finding_gate=True,
            role_model_mapping_path=policy,
        )
        assert {key: resolved["codex"][key] for key in ("model", "reasoning_effort", "service_tier")} == {
            key: custom_profile[key] for key in ("model", "reasoning_effort", "service_tier")
        }


def _coding_invocation(action: str = "start") -> dict[str, object]:
    return {
        "schema": "orchestrator-coding-invocation/v1",
        "action": action,
        "codex": {
            "command": ["codex", "--dangerously-bypass-hook-trust"],
            "model": "source-placeholder",
            "reasoning_effort": "source-placeholder",
            "service_tier": "source-placeholder",
            "sandbox": "danger-full-access",
            "approval_policy": "never",
            "config_overrides": ["model_auto_compact_token_limit=1"],
        },
    }


@pytest.mark.parametrize(
    ("field", "value"),
    (("sandbox", "workspace-write"), ("approval_policy", "on-request")),
)
def test_workflow_role_allocation_rejects_non_full_access_invocations(field: str, value: str) -> None:
    runner = _load_runner()
    invocation = _coding_invocation()
    settings = invocation["codex"]
    assert isinstance(settings, dict)
    settings[field] = value
    with pytest.raises(runner.RunnerError, match=field):
        runner.apply_workflow_role_allocation(invocation, "doer-main", validate_finding_gate=False)


def _failure_history(*error_classes: str, workflow_role: str = "doer-main") -> dict[str, object]:
    return {
        "schema": "orchestrator-backend-failure-history/v1",
        "workflow_role": workflow_role,
        "logical_task_id": "logical-task-1",
        "attempts": [
            {
                "attempt_id": f"attempt-{index}",
                "profile_id": "deepseek-v4-flash-0731-high",
                "outcome": "BACKEND_FAILURE",
                "error_class": error_class,
                "error_sha256": f"{index:064x}",
            }
            for index, error_class in enumerate(error_classes, start=1)
        ],
    }


def test_launch_profiles_materialize_luna_deepseek_and_terra_compaction_settings() -> None:
    runner = _load_runner()
    coder = runner.apply_workflow_role_allocation(_coding_invocation(), "coder-main", validate_finding_gate=False)
    coder_settings = coder["codex"]
    assert coder_settings["launch_profile"] == "luna-max"
    assert coder_settings["model"] == "gpt-5.6-luna"
    assert coder_settings["reasoning_effort"] == "max"
    assert "model_context_window=272000" in coder_settings["config_overrides"]
    assert "model_auto_compact_token_limit=150000" in coder_settings["config_overrides"]

    test_executor = runner.apply_workflow_role_allocation(
        _coding_invocation(), "doer-main", validate_finding_gate=False
    )
    test_executor_settings = test_executor["codex"]
    assert test_executor_settings["launch_profile"] == "deepseek-v4-flash-0731-high"
    assert test_executor_settings["model"] == "deepseek-v4-flash:0731-cloud"
    assert test_executor_settings["reasoning_effort"] == "high"
    assert test_executor_settings["command"] == [
        "codex",
        "--dangerously-bypass-hook-trust",
        "--oss",
        "--local-provider",
        "ollama",
    ]
    assert "model_context_window=1048576" in test_executor_settings["config_overrides"]
    assert "model_auto_compact_token_limit=230000" in test_executor_settings["config_overrides"]
    assert "model_auto_compact_token_limit=1" not in test_executor_settings["config_overrides"]
    assert test_executor_settings["sandbox"] == "danger-full-access"
    assert test_executor_settings["approval_policy"] == "never"
    assert 'approval_policy="never"' in test_executor_settings["config_overrides"]
    assert 'approvals_reviewer="user"' in test_executor_settings["config_overrides"]
    catalog_override = next(
        item for item in test_executor_settings["config_overrides"] if item.startswith("model_catalog_json=")
    )
    assert ".codex/delegates/deepseek-model-catalog.json" in catalog_override.replace("\\", "/")

    terra = runner.apply_workflow_role_allocation(_coding_invocation(), "reviewer-main", validate_finding_gate=False)
    terra_settings = terra["codex"]
    assert terra_settings["launch_profile"] == "terra-xhigh"
    assert terra_settings["model"] == "gpt-5.6-terra"
    assert "model_context_window=1048576" in terra_settings["config_overrides"]
    assert "model_auto_compact_token_limit=250000" in terra_settings["config_overrides"]

    sprint_evidence_reviewer = runner.apply_workflow_role_allocation(
        _coding_invocation(), "sprint-evidence-reviewer", validate_finding_gate=False
    )
    sprint_evidence_settings = sprint_evidence_reviewer["codex"]
    assert sprint_evidence_settings["launch_profile"] == "terra-xhigh"
    assert sprint_evidence_settings["model"] == "gpt-5.6-terra"
    assert sprint_evidence_settings["reasoning_effort"] == "xhigh"


def test_backend_fallback_requires_three_consecutive_classified_deepseek_failures() -> None:
    runner = _load_runner()
    with pytest.raises(runner.RunnerError, match="requires 3 consecutive"):
        runner.apply_workflow_role_allocation(
            _coding_invocation(),
            "doer-main",
            validate_finding_gate=False,
            fallback_history=_failure_history("HTTP_429", "RATE_LIMIT"),
        )

    fallback = runner.apply_workflow_role_allocation(
        _coding_invocation(),
        "doer-main",
        validate_finding_gate=False,
        fallback_history=_failure_history("HTTP_429", "HTTP_303", "BACKEND_ERROR"),
    )
    settings = fallback["codex"]
    assert settings["launch_profile"] == "luna-high"
    assert settings["model"] == "gpt-5.6-luna"
    assert settings["reasoning_effort"] == "high"
    assert "model_auto_compact_token_limit=150000" in settings["config_overrides"]

    with pytest.raises(runner.RunnerError, match="action=start"):
        runner.apply_workflow_role_allocation(
            _coding_invocation("resume"),
            "doer-main",
            validate_finding_gate=False,
            fallback_history=_failure_history("HTTP_429", "HTTP_303", "BACKEND_ERROR"),
        )


@pytest.mark.parametrize("error_class", ("HTTP_429", "HTTP_303", "RATE_LIMIT", "BACKEND_ERROR"))
def test_each_declared_backend_class_can_complete_the_fallback_streak(
    error_class: str,
) -> None:
    runner = _load_runner()
    fallback = runner.apply_workflow_role_allocation(
        _coding_invocation(),
        "doer-main",
        validate_finding_gate=False,
        fallback_history=_failure_history(error_class, error_class, error_class),
    )
    assert fallback["codex"]["launch_profile"] == "luna-high"


def test_backend_error_classifier_is_narrow_and_redactable() -> None:
    runner = _load_runner()
    assert runner.classify_backend_error("HTTP status 429: too many requests") == "HTTP_429"
    assert runner.classify_backend_error("provider returned HTTP 303 error") == "HTTP_303"
    assert runner.classify_backend_error("Rate limit exceeded") == "RATE_LIMIT"
    assert runner.classify_backend_error("backend service unavailable") == "BACKEND_ERROR"
    assert runner.classify_backend_error("ordinary product test assertion failed") is None


def test_backend_error_classifier_cli_emits_only_the_class_and_content_hash(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    runner = _load_runner()
    raw_error = "provider request failed: HTTP 429; secret detail must not enter history"
    error_path = tmp_path / "provider.stderr"
    error_path.write_text(raw_error, encoding="utf-8")

    assert runner.main(["--classify-backend-error-file", str(error_path)]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result == {
        "backend_error_class": "HTTP_429",
        "error_sha256": hashlib.sha256(raw_error.encode("utf-8")).hexdigest(),
    }
    assert raw_error not in json.dumps(result)


def test_fallback_history_file_is_enforced_by_projection_cli(tmp_path: Path) -> None:
    runner = _load_runner()
    source = tmp_path / "source.json"
    source_invocation = _coding_invocation()
    source_invocation["finding_gate"] = {
        "role": _role_allocation("doer-main")["finding_gate_role"],
        "path": "FINDINGS.json",
    }
    source.write_text(json.dumps(source_invocation), encoding="utf-8")
    history = tmp_path / "backend-history.json"
    history.write_text(
        json.dumps(_failure_history("HTTP_429", "HTTP_303", "BACKEND_ERROR")),
        encoding="utf-8",
    )
    output = tmp_path / "projected.json"
    record = tmp_path / "projection.json"

    assert (
        runner.main(
            [
                "--project-invocation",
                str(source),
                "--workflow-role",
                "doer-main",
                "--launch-profile",
                "luna-high",
                "--fallback-history",
                str(history),
                "--projection-output",
                str(output),
                "--projection-record",
                str(record),
            ]
        )
        == 0
    )
    projected = json.loads(output.read_text(encoding="utf-8"))
    projection = json.loads(record.read_text(encoding="utf-8"))
    assert projected["action"] == "start"
    assert projected["codex"]["launch_profile"] == "luna-high"
    assert projected["codex"]["reasoning_effort"] == "high"
    assert projection["fallback_history_sha256"] == hashlib.sha256(history.read_bytes()).hexdigest()


def test_proof_file_inside_stable_is_rejected_before_any_write() -> None:
    runner = _load_runner()
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        suite = root / "suite"
        suite.mkdir()
        config = root / "config.json"
        config.write_text(
            json.dumps(
                {
                    "suite_root": "suite",
                    "run_globs": ["lanes/*"],
                    "output_dir": str(root / "output"),
                    "attention_logging_enabled": False,
                    "attention_epoch_id": "proof-confinement",
                }
            ),
            encoding="utf-8",
        )
        source = root / "candidate.json"
        source.write_text("{}\n", encoding="utf-8")
        projection_output = root / "projected.json"
        projection_record = root / "projection.json"
        proof_path = STABLE / "runner-proof-confinement-test.json"
        before = subprocess.run(
            [
                "git",
                "-C",
                str(STABLE),
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        try:
            module_result = runner.main(
                [
                    "--module",
                    "orchestrator_harness.cli",
                    "--proof-file",
                    str(proof_path),
                    "--config",
                    str(config),
                    "scan",
                    "--no-write",
                ]
            )
            assert module_result == 2
            assert not proof_path.exists()

            projection_result = runner.main(
                [
                    "--project-invocation",
                    str(source),
                    "--proof-file",
                    str(proof_path),
                    "--projection-output",
                    str(projection_output),
                    "--projection-record",
                    str(projection_record),
                ]
            )
            assert projection_result == 2
            assert not proof_path.exists()
            assert not projection_output.exists()
            assert not projection_record.exists()
            after = subprocess.run(
                [
                    "git",
                    "-C",
                    str(STABLE),
                    "status",
                    "--porcelain=v1",
                    "--untracked-files=all",
                ],
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            assert after == before
        finally:
            proof_path.unlink(missing_ok=True)


def test_module_result_type_boundary_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = _load_runner()
    fake_module = types.SimpleNamespace(main=lambda _argv: "invalid-result")
    proof = runner.validate_checkout()
    monkeypatch.setattr(
        runner,
        "import_stable_module",
        lambda _name, _proof: (fake_module, proof),
    )
    assert runner.main(["--module", "orchestrator_harness.cli"]) == 2


def test_pending_d1_migration_binds_authoritative_s2_d1() -> None:
    migration = json.loads((RUNNER_MIGRATION / "PENDING_D1_MIGRATION.json").read_text(encoding="utf-8"))
    authoritative_bytes = PENDING_S2_D1.read_bytes()
    authoritative = json.loads(authoritative_bytes.decode("utf-8"))
    authoritative_hash = hashlib.sha256(authoritative_bytes).hexdigest()
    candidate_path = RUNNER_MIGRATION / "PENDING_D1_RESUME_CANDIDATE.json"
    candidate_bytes = candidate_path.read_bytes()
    candidate = json.loads(candidate_bytes.decode("utf-8"))
    candidate_hash = hashlib.sha256(candidate_bytes).hexdigest()
    stable_path = RUNNER_MIGRATION / "PENDING_D1_STABLE_INVOCATION.json"
    stable_bytes = stable_path.read_bytes()
    stable_hash = hashlib.sha256(stable_bytes).hexdigest()
    projection = json.loads((RUNNER_MIGRATION / "PENDING_D1_STABLE_PROJECTION.json").read_text(encoding="utf-8"))

    assert authoritative["action"] == "resume"
    assert authoritative["lane_id"] == "S2.D1"
    assert authoritative["worker_invocation_id"] == "s2-d1-001"
    assert authoritative["resume_identity"]["thread_id"] == ("019fcacb-ab71-79c0-bb93-3813ff3d900d")
    assert authoritative["repository"]["branch"] == "firmware/v2-s2-d1"
    assert authoritative["repository"]["base_commit"] == ("7a28b186e91f2945ea9c59869a216fa8caf8407e")
    assert authoritative["prompt_sha256"] == ("f495350ca3a5b5ff15def16c28beea83714db1aafe90e733067fa0b68fc0cf1d")
    assert migration["original_invocation"]["path"].endswith(
        "implementation/lanes/S2.D1/.agent-workspace/worker.invocation.json"
    )
    assert migration["original_invocation"]["sha256"] == authoritative_hash
    assert migration["resume_projection"]["candidate_source_sha256"] == candidate_hash
    assert migration["resume_projection"]["stable_compatible_invocation_sha256"] == (stable_hash)
    assert migration["preserved_resume_identity"] == {
        "worker_invocation_id": "s2-d1-001",
        "thread_id": "019fcacb-ab71-79c0-bb93-3813ff3d900d",
        "worktree_root": "plans/general-coding-harness/runtime/firmware-v2/implementation/lanes/S2.D1",
        "branch": "firmware/v2-s2-d1",
        "tip": "7a28b186e91f2945ea9c59869a216fa8caf8407e",
        "common_dir": ".git/modules/harness-in-progress",
    }
    assert migration["launch_status"] == "not_launched"
    assert "S1.D1" not in json.dumps(migration, sort_keys=True)
    assert "s1-d1-001" not in json.dumps(migration, sort_keys=True)

    assert candidate["lane_id"] == authoritative["lane_id"] == "S2.D1"
    assert candidate["worker_invocation_id"] == authoritative["worker_invocation_id"]
    assert candidate["resume_identity"] == authoritative["resume_identity"]
    assert candidate["repository"] == authoritative["repository"]
    assert candidate["prompt_sha256"] == authoritative["prompt_sha256"]
    assert candidate["finding_gate"] == authoritative["finding_gate"]
    assert candidate["child_environment_isolation"] is True

    assert projection["source_invocation_sha256"] == candidate_hash
    assert projection["projected_invocation_sha256"] == stable_hash
    assert projection["removed_candidate_only_fields"] == [
        {
            "field": "child_environment_isolation",
            "value_sha256": "a17fcf0a2f50e2d495e4f90ce263410edc183add6c62699a2facbccf60410f74",
            "stable_behavior": "not_consumed_by_stable_4699d27",
            "root_responsibility": "ROOT-IM validates the retained candidate artifact and triage before accepting the lane result",
        },
        {
            "field": "finding_gate",
            "value_sha256": "e3338f8e035d3918f11cdfe999232f5041cc4822039d53ea3d5973d5adfc04d4",
            "stable_behavior": "not_consumed_by_stable_4699d27",
            "root_responsibility": "ROOT-IM validates the retained candidate artifact and triage before accepting the lane result",
        },
    ]
    assert projection["unknown_fields"] == []
    assert projection["root_must_validate_before_acceptance"] is True
    for path in RUNNER_MIGRATION.glob("PENDING_D1_*.json"):
        assert "S1.D1" not in path.read_text(encoding="utf-8")
        assert "s1-d1-001" not in path.read_text(encoding="utf-8")


def test_hostile_cwds_and_conflicting_pythonpath_still_prove_stable_import() -> None:
    with tempfile.TemporaryDirectory(prefix="stable-runner-config-") as raw:
        config_root = Path(raw)
        suite = config_root / "suite"
        suite.mkdir()
        config = config_root / "config.json"
        config.write_text(
            json.dumps(
                {
                    "suite_root": "suite",
                    "run_globs": ["lanes/*"],
                    "output_dir": str(config_root / "output"),
                    "attention_logging_enabled": False,
                    "attention_epoch_id": "proof",
                }
            ),
            encoding="utf-8",
        )
        fake_import_root = config_root / "conflict"
        (fake_import_root / "orchestrator_harness").mkdir(parents=True)
        (fake_import_root / "orchestrator_harness" / "__init__.py").write_text(
            "raise RuntimeError('wrong package won')\n", encoding="utf-8"
        )
        candidate = config_root / "hostile-candidate-cwd"
        lane = config_root / "hostile-lane-cwd"
        candidate.mkdir()
        lane.mkdir()
        for cwd in (candidate, lane):
            env = os.environ.copy()
            env["PYTHONPATH"] = str(fake_import_root)
            completed = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    str(LAUNCHER),
                    "--module",
                    "orchestrator_harness.cli",
                    "--config",
                    str(config),
                    "scan",
                    "--no-write",
                ],
                check=False,
                cwd=cwd,
                env=env,
                capture_output=True,
                text=True,
                timeout=30,
            )
            assert completed.returncode == 0, completed.stderr
            assert "stable-general-harness-runner\\\\orchestrator_harness\\\\cli.py" in completed.stderr
            assert str(fake_import_root) not in completed.stderr
        operator = subprocess.run(
            [
                sys.executable,
                "-I",
                str(LAUNCHER),
                "--module",
                "orchestrator_harness.operator_launch",
                "--",
                "--help",
            ],
            cwd=candidate,
            env=env,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert operator.returncode == 0, operator.stderr
        assert '"module": "orchestrator_harness.operator_launch"' in operator.stderr


def test_disposable_controller_refreshes_role_at_dispatch() -> None:
    runner = _load_runner()
    with tempfile.TemporaryDirectory(prefix="stable-controller-proof-") as raw:
        run_root = Path(raw)
        (run_root / ".gitignore").write_text(".agent-workspace/\nruntime/\n", encoding="utf-8")
        prompt = run_root / "prompt.md"
        prompt.write_text("synthetic controller proof\n", encoding="utf-8")
        (run_root / "fake_codex.py").write_text(
            "import json, pathlib, time\n"
            "lock_root = pathlib.Path('runtime/resource-locks')\n"
            "observed = sorted(path.name for path in lock_root.glob('*.json'))\n"
            "pathlib.Path('resource-observed.json').write_text(json.dumps(observed), encoding='utf-8')\n"
            "time.sleep(2)\n"
            "print(json.dumps({'type': 'thread.started', 'thread_id': 'synthetic-thread'}), flush=True)\n",
            encoding="utf-8",
        )
        subprocess.run(
            ["git", "init", "--initial-branch", "main", str(run_root)],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(run_root),
                "config",
                "user.email",
                "proof@example.invalid",
            ],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(run_root), "config", "user.name", "Disposable Proof"],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(run_root),
                "add",
                ".gitignore",
                "prompt.md",
                "fake_codex.py",
            ],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(run_root), "commit", "-m", "proof fixture"],
            check=True,
            capture_output=True,
        )
        base_commit = subprocess.run(
            ["git", "-C", str(run_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        workspace = run_root / ".agent-workspace"
        runtime_root = run_root / "runtime"
        runtime_root.mkdir()
        resource_lock_root = runtime_root / "resource-locks"
        source = run_root / "candidate.invocation.json"
        source_value = {
            "schema": "orchestrator-coding-invocation/v1",
            "action": "start",
            "run_root": str(run_root),
            "prompt_path": str(prompt),
            "prompt_sha256": hashlib.sha256(prompt.read_bytes()).hexdigest(),
            "output_paths": {
                "status": str(workspace / "controller.status.json"),
                "jsonl": str(workspace / "codex.jsonl"),
                "stderr": str(workspace / "codex.stderr"),
                "last_message": str(workspace / "last-message.txt"),
            },
            "runtime_root": str(runtime_root),
            "resource_lock_root": str(resource_lock_root),
            "event_log_path": str(runtime_root / "LANE_EVENTS.jsonl"),
            "worker_invocation_id": "proof-worker-1",
            "lane_id": "PROOF.D1",
            "exclusive_resources": ["stable-controller-proof"],
            "task": "stable controller proof",
            "phase": "verification",
            "repository": {
                "common_dir": str(run_root / ".git"),
                "worktree_root": str(run_root),
                "branch": "main",
                "base_commit": base_commit,
            },
            "codex": {
                "command": [sys.executable, "-m", "fake_codex"],
                **_model_settings("doer-main"),
                "sandbox": "danger-full-access",
                "approval_policy": "never",
                "config_overrides": [],
            },
            "finding_gate": {
                "role": _role_allocation("doer-main")["finding_gate_role"],
                "path": str(workspace / "FINDINGS.json"),
            },
            "child_environment_isolation": True,
        }
        source.write_text(json.dumps(source_value, indent=2) + "\n", encoding="utf-8")
        projected = run_root / "stable-compatible.invocation.json"
        projection_record = run_root / "stable-compatible.projection.json"
        record = runner.project_invocation(
            input_path=source,
            output_path=projected,
            record_path=projection_record,
            proof=runner.validate_checkout(),
            workflow_role="doer-main",
        )
        dispatch_input = run_root / "earlier-materialized.invocation.json"
        dispatch_value = json.loads(projected.read_text(encoding="utf-8"))
        for key in ("model", "reasoning_effort", "service_tier"):
            dispatch_value["codex"][key] = "earlier-materialized"
        dispatch_input.write_text(json.dumps(dispatch_value, indent=2) + "\n", encoding="utf-8")
        hostile_cwd = (
            ROOT / "plans" / "general-coding-harness" / "runtime" / "firmware-v2" / "worktrees" / "harness-candidate"
        )
        env = os.environ.copy()
        env["PYTHONPATH"] = str(run_root / "wrong-import-root")
        completed = subprocess.run(
            [
                sys.executable,
                "-I",
                str(LAUNCHER),
                "--workflow-role",
                "doer-main",
                "--module",
                "orchestrator_harness.lane_controller",
                str(dispatch_input),
            ],
            check=False,
            cwd=hostile_cwd,
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert completed.returncode == 0, (
            completed.stderr
            + completed.stdout
            + "\nstatus: "
            + (workspace / "controller.status.json").read_text(encoding="utf-8")
            if (workspace / "controller.status.json").exists()
            else completed.stderr + completed.stdout
        )
        status = json.loads((workspace / "controller.status.json").read_text(encoding="utf-8"))
        assert status["state"] == "CODEX_EXITED"
        assert status["thread_id"] == "synthetic-thread"
        assert status["result_validation"]["state"] == "MISSING"
        expected_settings = _model_settings("doer-main")
        assert status["launcher_settings"]["model"] == expected_settings["model"]
        assert status["launcher_settings"]["model_reasoning_effort"] == expected_settings["reasoning_effort"]
        assert status["launcher_settings"]["service_tier"] == expected_settings["service_tier"]
        observed_claims = json.loads((run_root / "resource-observed.json").read_text(encoding="utf-8"))
        assert observed_claims == [hashlib.sha256(b"stable-controller-proof").hexdigest() + ".json"]
        assert list(resource_lock_root.iterdir()) == []
        assert "stable-general-harness-runner" in completed.stderr
        assert "finding_gate" not in json.loads(projected.read_text(encoding="utf-8"))
        assert "child_environment_isolation" not in json.loads(projected.read_text(encoding="utf-8"))
        assert record["root_must_validate_before_acceptance"] is True
