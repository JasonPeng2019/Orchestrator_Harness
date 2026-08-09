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


def _load_runner():
    spec = importlib.util.spec_from_file_location("stable_runner_under_test", LAUNCHER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def test_projection_is_explicit_and_hash_bound() -> None:
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
                "model": "model",
                "reasoning_effort": "medium",
                "service_tier": "default",
                "sandbox": "danger-full-access",
                "approval_policy": "never",
                "config_overrides": [],
            },
            "finding_gate": {
                "role": "test_executor",
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
        )
        projected = json.loads(output.read_text(encoding="utf-8"))
        assert "finding_gate" not in projected
        assert "child_environment_isolation" not in projected
        assert {item["field"] for item in record["removed_candidate_only_fields"]} == {
            "finding_gate",
            "child_environment_isolation",
        }
        assert record["projected_invocation_sha256"] == runner.hashlib.sha256(output.read_bytes()).hexdigest()
        source_value["unrecognized"] = True
        source.write_text(json.dumps(source_value), encoding="utf-8")
        with pytest.raises(runner.RunnerError, match="unknown fields"):
            runner.project_invocation(
                input_path=source,
                output_path=root / "second.json",
                record_path=root / "second-record.json",
                proof=runner.validate_checkout(),
            )
        with pytest.raises(runner.RunnerError, match="inside the immutable stable checkout"):
            runner.project_invocation(
                input_path=source,
                output_path=STABLE / "runner-migration-test-output.json",
                record_path=root / "stable-output-record.json",
                proof=runner.validate_checkout(),
            )


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


def test_module_result_type_boundary_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
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
        candidate = (
            ROOT / "plans" / "general-coding-harness" / "runtime" / "firmware-v2" / "worktrees" / "harness-candidate"
        )
        lane = (
            ROOT / "plans" / "general-coding-harness" / "runtime" / "firmware-v2" / "implementation" / "lanes" / "S1.A1"
        )
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


def test_disposable_controller_proof_uses_projected_stable_invocation() -> None:
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
                "model": "proof-model",
                "reasoning_effort": "medium",
                "service_tier": "default",
                "sandbox": "danger-full-access",
                "approval_policy": "never",
                "config_overrides": [],
            },
            "finding_gate": {
                "role": "test_executor",
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
        )
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
                "--module",
                "orchestrator_harness.lane_controller",
                str(projected),
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
        observed_claims = json.loads((run_root / "resource-observed.json").read_text(encoding="utf-8"))
        assert observed_claims == [hashlib.sha256(b"stable-controller-proof").hexdigest() + ".json"]
        assert list(resource_lock_root.iterdir()) == []
        assert "stable-general-harness-runner" in completed.stderr
        assert "finding_gate" not in json.loads(projected.read_text(encoding="utf-8"))
        assert "child_environment_isolation" not in json.loads(projected.read_text(encoding="utf-8"))
        assert record["root_must_validate_before_acceptance"] is True
