from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from c3_outer_support import (
    MechanicalObserver,
    RegisteredChild,
    artifact_reference,
    canonical_json,
    classify_observer_record,
    classify_outer_failure,
    cleanup_registered_children,
    process_identity,
    read_json_object,
    validate_observation_close,
    write_new_json,
    write_replace_json,
)


def _check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _init_repo(path: Path) -> str:
    path.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(
        ["git", "-C", str(path), "config", "user.email", "smoke@example.invalid"],
        check=True,
    )
    subprocess.run(["git", "-C", str(path), "config", "user.name", "C3 Support Smoke"], check=True)
    (path / "README.txt").write_text("immutable smoke fixture\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(path), "add", "README.txt"], check=True)
    subprocess.run(["git", "-C", str(path), "commit", "-q", "-m", "fixture"], check=True)
    return subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def main() -> int:
    checks: list[dict[str, str]] = []
    with tempfile.TemporaryDirectory(prefix="c3-outer-support-") as raw_root:
        root = Path(raw_root)
        candidate = root / "candidate"
        server = root / "server"
        candidate_commit = _init_repo(candidate)
        server_commit = _init_repo(server)
        runtime = root / "runtime"
        runtime.mkdir()
        topology = root / "evidence" / "topology"
        watcher = root / "evidence" / "watcher"
        stop_path = topology / "WATCHER_STOP_REQUEST.json"
        ready_path = watcher / "WATCHER_READY.json"
        heartbeat_path = watcher / "WATCHER_HEARTBEATS.jsonl"
        terminal_path = watcher / "WATCHER_SERVICE_TERMINAL.json"
        abort_path = watcher / "ABORT_REQUIRED.json"
        oracle = root / "oracle.py"
        oracle.write_text(
            "def classify(request, response, observation, status):\n    return {'classification': 'PASS'}\n",
            encoding="utf-8",
        )
        config = root / "observer-config.json"
        write_new_json(
            config,
            {
                "schema": "firmware-c3-watcher-helper-config/v1",
                "attempt_id": "attempt-smoke",
                "runtime_root": str(runtime.resolve()),
                "evidence_root": str((root / "evidence").resolve()),
                "topology_root": str(topology.resolve()),
                "watcher_evidence_root": str(watcher.resolve()),
                "candidate_root": str(candidate.resolve()),
                "candidate_commit": candidate_commit,
                "server_root": str(server.resolve()),
                "server_commit": server_commit,
                "launch_record": str((topology / "WATCHER_HELPER_LAUNCH.json").resolve()),
                "stop_request": str(stop_path.resolve()),
                "oracle_module": str(oracle.resolve()),
                "capability_environment_keys": ["MCP_ENDPOINT", "PYOCD_PROBE_UID"],
                "heartbeat_interval_seconds": 0.05,
            },
        )
        environment = os.environ.copy()
        environment["MCP_ENDPOINT"] = ""
        environment["PYOCD_PROBE_UID"] = ""
        helper_path = Path(__file__).resolve().with_name("c3_watcher_helper.py")
        observer = MechanicalObserver(
            attempt_id="attempt-smoke",
            command=[sys.executable, "-I", str(helper_path), "--config", str(config)],
            cwd=root / "control" / "watcher",
            topology_root=topology,
            evidence_root=watcher,
            stop_path=stop_path,
            ready_path=ready_path,
            heartbeat_path=heartbeat_path,
            terminal_path=terminal_path,
            abort_path=abort_path,
            environment=environment,
        )
        ready = observer.start(timeout=10.0)
        _check(
            ready["schema"] == "firmware-c3-watcher-ready/v1",
            "ROOT did not accept helper readiness",
        )
        checks.append({"name": "root-direct-helper-launch", "outcome": "PASS"})

        forbidden_target = runtime / "targets" / "target"
        forbidden_target.mkdir(parents=True)
        finding_path = watcher / "WATCHER_FINDINGS.jsonl"
        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline and not finding_path.is_file():
            time.sleep(0.03)
        findings = [json.loads(line) for line in finding_path.read_text(encoding="utf-8").splitlines()]
        selected_test_marker = root / "selected-test-completed.json"
        write_new_json(selected_test_marker, {"outcome": "PASS"})
        _check(
            any(item["kind"] == "NONCANONICAL_TARGET_ROOT" for item in findings),
            "helper finding missing",
        )
        _check(
            not abort_path.exists(),
            "non-critical helper finding incorrectly requested an abort",
        )
        _check(
            selected_test_marker.is_file(),
            "selected test did not complete after pooled finding",
        )
        checks.append({"name": "noncritical-observer-finding-pooled", "outcome": "PASS"})

        observed = root / "immediate-stop-observation.json"
        write_new_json(observed, {"observation": "unauthorized operation"})
        immediate = classify_observer_record(
            {
                "immediate_stop_condition": "unauthorized_or_wrong_resource_operation",
                "evidence": [artifact_reference(observed)],
            }
        )
        _check(
            immediate["disposition"] == "IMMEDIATE_SAFETY_STOP",
            "defined stop was not classified",
        )
        _check(
            immediate["product_gate_invalidated"] is False,
            "safety stop incorrectly invalidated product credit",
        )
        registered = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
        registered_identity = process_identity(registered.pid)
        unrelated = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
        try:
            stopped = cleanup_registered_children(
                [
                    RegisteredChild(
                        "registered-topology",
                        registered,
                        str(registered_identity["created_native"]),
                    )
                ],
                terminate_timeout=5.0,
                kill_timeout=5.0,
            )
            _check(
                stopped[0]["outcome"] in {"terminated", "killed"},
                "registered topology was not stopped",
            )
            _check(
                unrelated.poll() is None,
                "unregistered process was touched by topology cleanup",
            )
        finally:
            if unrelated.poll() is None:
                unrelated.terminate()
                unrelated.wait(timeout=5.0)
        checks.append({"name": "defined-immediate-stop", "outcome": "PASS"})

        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline and not heartbeat_path.is_file():
            time.sleep(0.03)
        close = observer.stop_and_close(timeout=10.0)
        _check(
            close["optional_ai_watcher"] is None,
            "optional AI watcher absence was not accepted",
        )
        _check(
            close["required_observation_complete"] is True,
            "helper closure was not complete",
        )
        close_path = topology / "WATCHER_OBSERVATION_CLOSE.json"
        if observer.launch_path is None:
            raise AssertionError("helper launch path was not retained")
        validated_close = validate_observation_close(
            close_path,
            attempt_id="attempt-smoke",
            expected_launch_reference=artifact_reference(observer.launch_path),
        )
        _check(validated_close == close, "close record did not validate exactly")
        checks.append({"name": "optional-ai-watcher-nonblocking", "outcome": "PASS"})
        checks.append({"name": "helper-observation-close", "outcome": "PASS"})

        exited = subprocess.Popen([sys.executable, "-c", "pass"])
        exited_identity = process_identity(exited.pid)
        exited.wait(timeout=10.0)
        live = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
        live_identity = process_identity(live.pid)
        cleanup = cleanup_registered_children(
            [
                RegisteredChild("already-exited", exited, str(exited_identity["created_native"])),
                RegisteredChild("still-live", live, str(live_identity["created_native"])),
            ],
            terminate_timeout=5.0,
            kill_timeout=5.0,
        )
        _check(
            cleanup[0]["outcome"] == "already_exited",
            "already-exited child was mishandled",
        )
        _check(
            cleanup[1]["outcome"] in {"terminated", "killed"},
            "remaining live child was not cleaned",
        )
        _check(live.poll() is not None, "live child remained after cleanup")
        checks.append({"name": "cleanup-continues-past-exited-child", "outcome": "PASS"})

        report = root / "outer-report.json"
        write_new_json(report, {"schema": "wrong"})
        in_place = classify_outer_failure(attempt_closeable=True)
        _check(
            in_place["action"] == "CORRECT_SUPPORT_IN_PLACE",
            "closeable report failure did not stay in place",
        )
        write_replace_json(report, {"schema": "correct", "outcome": "PASS"})
        _check(
            read_json_object(report)["schema"] == "correct",
            "report correction was not retained",
        )
        checks.append({"name": "outer-report-correction-in-place", "outcome": "PASS"})

        rollover = classify_outer_failure(attempt_closeable=False)
        _check(
            rollover["action"] == "ROLL_OUTER_ATTEMPT_ONLY",
            "uncloseable support failure did not roll attempt",
        )
        _check(
            rollover["preserve_valid_product_credit"] is True,
            "rollover discarded valid product credit",
        )
        _check(
            rollover["candidate_gate_invalidated"] is False,
            "rollover invalidated candidate gate",
        )
        checks.append({"name": "outer-attempt-only-rollover", "outcome": "PASS"})

        output = {
            "schema": "firmware-c3-outer-support-practical-smoke/v1",
            "outcome": "PASS",
            "checks": checks,
            "check_count": len(checks),
            "hardware_accessed": False,
            "mcp_launched": False,
            "candidate_source_changed": False,
            "observation_close_sha256": artifact_reference(close_path)["sha256"],
        }
        print(canonical_json(output).decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
