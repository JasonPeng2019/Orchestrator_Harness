from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, cast

import pytest

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / ".codex" / "scripts" / "c3_outer_support.py"
SPEC = importlib.util.spec_from_file_location("c3_outer_support", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot import {MODULE_PATH}")
support = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = support
SPEC.loader.exec_module(support)


def _evidence(path: Path, value: object | None = None) -> dict[str, str]:
    support.write_new_json(path, value if value is not None else {"evidence": True})
    return cast(dict[str, str], support.artifact_reference(path))


def _resolution(fact_id: str, reference: dict[str, str], *, mode: str = "PRIMARY") -> dict[str, Any]:
    sources = [{"source_class": "root", "reference": reference}]
    if mode == "BACKUP":
        sources.append({"source_class": "operating-system", "reference": reference})
    return {
        "fact_id": fact_id,
        "mode": mode,
        "conclusion": f"{fact_id} is established",
        "sources": sources,
        "correlation": {"attempt_id": "attempt-test", "identity": "same"},
    }


def test_noncritical_observation_is_pooled(tmp_path: Path) -> None:
    reference = _evidence(tmp_path / "observation.json")
    result = support.classify_observer_record({"invariant": "ordinary defect", "evidence": [reference]})
    assert result == {
        "disposition": "POOL_FOR_POST_GATE_TRIAGE",
        "condition": None,
        "product_gate_invalidated": False,
    }


@pytest.mark.parametrize("condition", sorted(support.IMMEDIATE_STOP_CONDITIONS))
def test_only_defined_evidenced_conditions_request_immediate_stop(tmp_path: Path, condition: str) -> None:
    reference = _evidence(tmp_path / f"{condition}.json")
    result = support.classify_observer_record({"immediate_stop_condition": condition, "evidence": [reference]})
    assert result["disposition"] == "IMMEDIATE_SAFETY_STOP"
    assert result["condition"] == condition
    assert result["product_gate_invalidated"] is False


def test_unknown_or_unevidenced_stop_is_pooled(tmp_path: Path) -> None:
    reference = _evidence(tmp_path / "unknown.json")
    unknown = support.classify_observer_record(
        {"immediate_stop_condition": "ordinary_test_failure", "evidence": [reference]}
    )
    missing = support.classify_observer_record(
        {
            "immediate_stop_condition": "unauthorized_or_wrong_resource_operation",
            "evidence": [],
        }
    )
    malformed = support.classify_observer_record(
        {"immediate_stop_condition": ["not", "hashable"], "evidence": [reference]}
    )
    assert unknown["disposition"] == "POOL_FOR_POST_GATE_TRIAGE"
    assert missing["disposition"] == "POOL_FOR_POST_GATE_TRIAGE"
    assert malformed["disposition"] == "POOL_FOR_POST_GATE_TRIAGE"


def test_outer_support_failure_stays_out_of_product_gate() -> None:
    correctable = support.classify_outer_failure(attempt_closeable=True)
    uncloseable = support.classify_outer_failure(attempt_closeable=False)
    assert correctable["action"] == "CORRECT_SUPPORT_IN_PLACE"
    assert uncloseable["action"] == "ROLL_OUTER_ATTEMPT_ONLY"
    assert correctable["candidate_gate_invalidated"] is False
    assert uncloseable["candidate_gate_invalidated"] is False
    assert correctable["preserve_valid_product_credit"] is True
    assert uncloseable["preserve_valid_product_credit"] is True


def test_product_escalation_requires_valid_exact_evidence(tmp_path: Path) -> None:
    reference = _evidence(tmp_path / "candidate-defect.json")
    result = support.classify_outer_failure(
        attempt_closeable=False,
        candidate_defect_evidence=[reference],
    )
    assert result["classification"] == "PRODUCT_MATERIAL_EVIDENCE"
    assert result["action"] == "TRIAGE_CANDIDATE_DEFECT"
    assert result["candidate_gate_invalidated"] is True
    changed = dict(reference)
    changed["sha256"] = "0" * 64
    with pytest.raises(support.OuterSupportError, match="reference changed"):
        support.classify_outer_failure(
            attempt_closeable=False,
            candidate_defect_evidence=[changed],
        )


def test_scoped_lock_and_indeterminate_result_do_not_claim_candidate_failure(
    tmp_path: Path,
) -> None:
    lock = _evidence(tmp_path / "changed-lock-domain.json")
    lock_result = support.classify_outer_failure(
        attempt_closeable=False,
        locked_input_change_evidence=[lock],
    )
    assert lock_result["action"] == "REFRESH_SCOPED_LOCK"
    assert lock_result["lock_refresh_required"] is True
    assert lock_result["candidate_gate_invalidated"] is False

    missing_result = _evidence(tmp_path / "untrustworthy-result.json")
    result = support.classify_outer_failure(
        attempt_closeable=False,
        candidate_result_untrustworthy_evidence=[missing_result],
    )
    assert result["action"] == "MARK_AFFECTED_RESULT_INDETERMINATE"
    assert result["affected_result_invalidated"] is True
    assert result["candidate_gate_invalidated"] is False
    assert result["preserve_valid_product_credit"] is True


class _FakeProcess:
    def __init__(self, pid: int, polls: list[int | None]) -> None:
        self.pid = pid
        self._polls = polls
        self.terminated = False
        self.killed = False

    def poll(self) -> int | None:
        if len(self._polls) > 1:
            return self._polls.pop(0)
        return self._polls[0]

    def terminate(self) -> None:
        self.terminated = True

    def kill(self) -> None:
        self.killed = True

    def wait(self, timeout: float | None = None) -> int:
        _ = timeout
        self._polls = [0]
        return 0


def test_cleanup_identity_race_does_not_block_other_children() -> None:
    uncertain = _FakeProcess(101, [None, None])
    live = _FakeProcess(102, [None])
    matches = {101: False, 102: True}
    outcomes = support.cleanup_registered_children(
        [
            support.RegisteredChild("uncertain", cast(subprocess.Popen[Any], uncertain), "first"),
            support.RegisteredChild("live", cast(subprocess.Popen[Any], live), "second"),
        ],
        identity_matches=lambda pid, _native: matches[pid],
        terminate_timeout=0.1,
        kill_timeout=0.1,
    )
    assert outcomes[0]["outcome"] == "identity_unverified"
    assert outcomes[0]["signalled"] is False
    assert uncertain.terminated is False
    assert outcomes[1]["outcome"] == "terminated"
    assert live.terminated is True


def test_cleanup_recognizes_exit_during_identity_check() -> None:
    raced = _FakeProcess(201, [None, 0])
    outcomes = support.cleanup_registered_children(
        [support.RegisteredChild("raced", cast(subprocess.Popen[Any], raced), "identity")],
        identity_matches=lambda _pid, _native: False,
    )
    assert outcomes[0]["outcome"] == "already_exited_after_identity_race"
    assert outcomes[0]["signalled"] is False


def test_backup_fact_requires_independent_sources(tmp_path: Path) -> None:
    reference = _evidence(tmp_path / "backup.json")
    weak = _resolution("ready", reference, mode="BACKUP")
    weak["sources"] = weak["sources"][:1]
    with pytest.raises(support.AttemptIncomplete, match="two independent source classes"):
        support.validate_fact_resolutions([weak], required_facts=frozenset({"ready"}))


def test_fact_validation_rejects_missing_required_fact(tmp_path: Path) -> None:
    reference = _evidence(tmp_path / "ready.json")
    with pytest.raises(support.AttemptIncomplete, match="unresolved"):
        support.validate_fact_resolutions(
            [_resolution("ready", reference)],
            required_facts=frozenset({"ready", "terminal_service"}),
        )


def test_observation_close_accepts_primary_and_independent_backup(
    tmp_path: Path,
) -> None:
    launch = _evidence(tmp_path / "launch.json")
    primary = _evidence(tmp_path / "primary.json")
    backup_a = _evidence(tmp_path / "backup-a.json")
    backup_b = _evidence(tmp_path / "backup-b.json")
    resolutions: list[dict[str, Any]] = []
    for fact_id in sorted(support.REQUIRED_OBSERVATION_FACTS):
        if fact_id == "heartbeat":
            resolutions.append(
                {
                    "fact_id": fact_id,
                    "mode": "BACKUP",
                    "conclusion": "heartbeat interval reconstructed",
                    "sources": [
                        {"source_class": "root", "reference": backup_a},
                        {"source_class": "operating-system", "reference": backup_b},
                    ],
                    "correlation": {"attempt_id": "attempt-test", "pid": 10},
                }
            )
        else:
            resolutions.append(_resolution(fact_id, primary))
    path = tmp_path / "WATCHER_OBSERVATION_CLOSE.json"
    value = support.write_observation_close(
        path=path,
        attempt_id="attempt-test",
        launch_reference=launch,
        fact_resolutions=resolutions,
        exit_code=0,
        reaped=True,
    )
    assert value["required_observation_complete"] is True
    assert value["optional_ai_watcher"] is None
    assert json.loads(path.read_text(encoding="utf-8")) == value
    assert (
        support.validate_observation_close(
            path,
            attempt_id="attempt-test",
            expected_launch_reference=launch,
        )
        == value
    )
    invalid = dict(value)
    invalid["required_observation_complete"] = False
    support.write_replace_json(path, invalid)
    with pytest.raises(support.OuterSupportError, match="identity/status"):
        support.validate_observation_close(
            path,
            attempt_id="attempt-test",
            expected_launch_reference=launch,
        )


def test_mechanical_observer_rejects_semantically_invalid_primary_records(
    tmp_path: Path,
) -> None:
    topology = tmp_path / "topology"
    watcher = tmp_path / "watcher"
    identity = {"pid": 17, "created_native": "test-created"}
    launch_path = topology / "WATCHER_HELPER_LAUNCH.json"
    support.write_new_json(
        launch_path,
        {
            "schema": "firmware-c3-watcher-helper-launch/v1",
            "attempt_id": "attempt-test",
            "identity": identity,
        },
    )
    observer = support.MechanicalObserver(
        attempt_id="attempt-test",
        command=["unused"],
        cwd=tmp_path / "cwd",
        topology_root=topology,
        evidence_root=watcher,
        stop_path=topology / "stop.json",
        ready_path=watcher / "ready.json",
        heartbeat_path=watcher / "heartbeats.jsonl",
        terminal_path=watcher / "terminal.json",
        abort_path=watcher / "abort.json",
        identity=identity,
        launch_path=launch_path,
    )
    support.write_new_json(
        observer.ready_path,
        {
            "schema": "firmware-c3-watcher-ready/v1",
            "attempt_id": "attempt-test",
            "helper_identity": identity,
            "helper_launch": support.artifact_reference(launch_path),
            "capability_environment_empty": False,
        },
    )
    with pytest.raises(support.OuterSupportError, match="capability environment"):
        observer._validate_primary_fact("ready", observer.ready_path)

    observer.heartbeat_path.parent.mkdir(parents=True, exist_ok=True)
    observer.heartbeat_path.write_text(
        json.dumps(
            {
                "schema": "firmware-c3-watcher-heartbeat/v1",
                "attempt_id": "wrong-attempt",
                "helper_identity": identity,
                "sequence": 1,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    with pytest.raises(support.OuterSupportError, match="schema/attempt"):
        observer._validate_primary_fact("heartbeat", observer.heartbeat_path)


def test_failed_observer_readiness_reaps_the_registered_helper(tmp_path: Path) -> None:
    topology = tmp_path / "topology"
    watcher = tmp_path / "watcher"
    ready_path = watcher / "ready.json"
    child = (
        "import json,pathlib,sys,time; "
        "time.sleep(0.2); "
        "pathlib.Path(sys.argv[1]).write_text(json.dumps({"
        "'schema':'firmware-c3-watcher-ready/v1','attempt_id':'attempt-test',"
        "'capability_environment_empty':True}),encoding='utf-8'); "
        "time.sleep(60)"
    )
    observer = support.MechanicalObserver(
        attempt_id="attempt-test",
        command=[sys.executable, "-c", child, str(ready_path)],
        cwd=tmp_path / "cwd",
        topology_root=topology,
        evidence_root=watcher,
        stop_path=topology / "stop.json",
        ready_path=ready_path,
        heartbeat_path=watcher / "heartbeats.jsonl",
        terminal_path=watcher / "terminal.json",
        abort_path=watcher / "abort.json",
    )
    with pytest.raises(support.AttemptIncomplete, match="identity is missing"):
        observer.start(timeout=5.0)
    assert observer.process is not None
    assert observer.process.poll() is not None
    failure = support.read_json_object(topology / "WATCHER_HELPER_START_FAILURE.json")
    assert failure["cleanup"][0]["outcome"] in {"terminated", "killed"}


def test_practical_smoke_covers_all_required_scenarios() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / ".codex" / "scripts" / "run_c3_outer_support_smoke.py"),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    value = json.loads(result.stdout)
    assert value["outcome"] == "PASS"
    assert value["check_count"] == 8
    assert value["hardware_accessed"] is False
    assert value["mcp_launched"] is False
