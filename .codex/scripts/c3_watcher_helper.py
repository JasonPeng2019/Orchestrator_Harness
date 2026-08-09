from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import time
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any, cast

SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from c3_outer_support import (
    append_jsonl,
    artifact_reference,
    read_json_object,
    utc_now,
    write_new_json,
)


def _required_string(value: Mapping[str, Any], key: str) -> str:
    item = value.get(key)
    if not isinstance(item, str) or not item:
        raise ValueError(f"observer config {key} must be a non-empty string")
    return item


def _load_config(path: Path) -> dict[str, Any]:
    value = read_json_object(path)
    required = {
        "schema",
        "attempt_id",
        "runtime_root",
        "evidence_root",
        "topology_root",
        "watcher_evidence_root",
        "candidate_root",
        "candidate_commit",
        "server_root",
        "server_commit",
        "launch_record",
        "stop_request",
        "oracle_module",
        "capability_environment_keys",
        "heartbeat_interval_seconds",
    }
    if set(value) != required or value.get("schema") != "firmware-c3-watcher-helper-config/v1":
        raise ValueError("observer config keys/schema are invalid")
    for key in required - {"capability_environment_keys", "heartbeat_interval_seconds"}:
        _required_string(value, key)
    keys = value["capability_environment_keys"]
    if not isinstance(keys, list) or not all(isinstance(item, str) and item for item in keys):
        raise ValueError("capability_environment_keys must be a string list")
    interval = value["heartbeat_interval_seconds"]
    if not isinstance(interval, (int, float)) or isinstance(interval, bool) or interval <= 0:
        raise ValueError("heartbeat_interval_seconds must be positive")
    return value


def _git_state(root: Path) -> dict[str, Any]:
    head = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    branch = subprocess.run(
        ["git", "-C", str(root), "branch", "--show-current"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    status = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain=v1", "--untracked-files=all"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return {
        "path": str(root.resolve()),
        "head": head,
        "branch": branch,
        "clean": not bool(status),
    }


def _load_oracle(path: Path) -> Callable[[Path, Path, Path, Path], dict[str, Any]]:
    spec = importlib.util.spec_from_file_location("c3_watcher_oracle_runtime", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load observer oracle: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    classify = getattr(module, "classify", None)
    if not callable(classify):
        raise TypeError("observer oracle has no callable classify")
    return cast(Callable[[Path, Path, Path, Path], dict[str, Any]], classify)


class WatcherLoop:
    def __init__(self, config: Mapping[str, Any]) -> None:
        self.attempt_id = _required_string(config, "attempt_id")
        self.runtime = Path(_required_string(config, "runtime_root")).resolve(strict=True)
        self.evidence = Path(_required_string(config, "evidence_root")).resolve(strict=True)
        self.topology = Path(_required_string(config, "topology_root")).resolve(strict=True)
        self.watcher = Path(_required_string(config, "watcher_evidence_root")).resolve(strict=True)
        self.candidate = Path(_required_string(config, "candidate_root")).resolve(strict=True)
        self.candidate_commit = _required_string(config, "candidate_commit")
        self.server = Path(_required_string(config, "server_root")).resolve(strict=True)
        self.server_commit = _required_string(config, "server_commit")
        self.launch_path = Path(_required_string(config, "launch_record")).resolve()
        self.stop_path = Path(_required_string(config, "stop_request")).resolve()
        self.capability_keys = tuple(config["capability_environment_keys"])
        self.heartbeat_interval = float(config["heartbeat_interval_seconds"])
        self.oracle = _load_oracle(Path(_required_string(config, "oracle_module")).resolve(strict=True))
        self.seen_claims: set[tuple[str, str]] = set()
        self.seen_assignments: set[str] = set()
        self.seen_findings: set[str] = set()
        self.observed_claims = 0
        self.observed_assignments = 0

    def inventory_cursor(self) -> dict[str, Any]:
        files: list[tuple[str, str, int, int]] = []
        for label, root in (("runtime", self.runtime), ("evidence", self.evidence)):
            for path in root.rglob("*"):
                try:
                    if path.is_file() and not path.is_symlink():
                        stat = path.stat()
                        files.append(
                            (
                                label,
                                path.relative_to(root).as_posix(),
                                stat.st_size,
                                stat.st_mtime_ns,
                            )
                        )
                except OSError:
                    continue
        raw = json.dumps(sorted(files), separators=(",", ":")).encode("utf-8")
        return {"sha256": hashlib.sha256(raw).hexdigest(), "regular_files": len(files)}

    def _finding(
        self,
        *,
        kind: str,
        sequence: int,
        cursor: Mapping[str, Any],
        evidence: list[dict[str, str]],
        correlated: Mapping[str, Any],
        immediate_stop_condition: str | None = None,
    ) -> None:
        if kind in self.seen_findings:
            return
        self.seen_findings.add(kind)
        value = {
            "schema": "firmware-c3-watcher-finding/v1",
            "attempt_id": self.attempt_id,
            "kind": kind,
            "sequence": sequence,
            "cursor": dict(cursor),
            "evidence": evidence,
            "correlated": dict(correlated),
            "immediate_stop_condition": immediate_stop_condition,
            "observed_utc": utc_now(),
        }
        append_jsonl(self.watcher / "WATCHER_FINDINGS.jsonl", value)
        if immediate_stop_condition is None or (self.watcher / "ABORT_REQUIRED.json").exists():
            return
        snapshot = self.watcher / f"IMMEDIATE_STOP_EVIDENCE_{sequence:06d}.json"
        write_new_json(snapshot, value)
        write_new_json(
            self.watcher / "ABORT_REQUIRED.json",
            {
                "schema": "firmware-c3-watcher-immediate-stop/v1",
                "attempt_id": self.attempt_id,
                "immediate_stop_condition": immediate_stop_condition,
                "evidence": [artifact_reference(snapshot)],
                "observed_utc": utc_now(),
            },
        )

    def _request_for_assignment(self, assignment_id: str) -> Path | None:
        for path in sorted((self.runtime / "manager-signals/c3-requests").glob("*.json")):
            try:
                value = read_json_object(path)
            except (OSError, ValueError, json.JSONDecodeError):
                continue
            payload = value.get("payload")
            if (
                value.get("kind") == "assignment"
                and isinstance(payload, dict)
                and payload.get("assignment_id") == assignment_id
            ):
                return path
        return None

    def scan_claims(self, sequence: int) -> None:
        claim_root = self.runtime / "claims"
        for path in sorted(claim_root.rglob("*.json")) if claim_root.is_dir() else []:
            try:
                item = artifact_reference(path)
            except (OSError, RuntimeError):
                continue
            key = (item["path"], item["sha256"])
            if key in self.seen_claims:
                continue
            self.seen_claims.add(key)
            self.observed_claims += 1
            append_jsonl(
                self.watcher / "WATCHER_OBSERVATIONS.jsonl",
                {
                    "schema": "firmware-c3-watcher-semantic-observation/v1",
                    "attempt_id": self.attempt_id,
                    "kind": "RESOURCE_CLAIM_OBSERVED",
                    "sequence": sequence,
                    "claim": item,
                    "observed_utc": utc_now(),
                },
            )

    def scan_assignments(self, sequence: int, cursor: Mapping[str, Any]) -> None:
        assignment_root = self.runtime / "assignments"
        paths = sorted(assignment_root.glob("*.CONTROLLER_OBSERVATION.json")) if assignment_root.is_dir() else []
        for observation_path in paths:
            key = str(observation_path)
            if key in self.seen_assignments:
                continue
            try:
                observation = read_json_object(observation_path)
                assignment_id = str(observation["assignment_id"])
                request_path = self._request_for_assignment(assignment_id)
                if request_path is None:
                    continue
                request = read_json_object(request_path)
                response_path = self.runtime / "manager-signals/c3-responses" / f"{request['request_id']}.json"
                status_path = Path(str(observation["status_source"]["path"]))
                references = [
                    artifact_reference(request_path),
                    artifact_reference(observation_path),
                    artifact_reference(status_path),
                ]
                oracle: dict[str, Any] | None = None
                if response_path.is_file():
                    references.append(artifact_reference(response_path))
                    oracle = self.oracle(request_path, response_path, observation_path, status_path)
                append_jsonl(
                    self.watcher / "WATCHER_OBSERVATIONS.jsonl",
                    {
                        "schema": "firmware-c3-watcher-semantic-observation/v1",
                        "attempt_id": self.attempt_id,
                        "kind": "ASSIGNMENT_CONTROLLER_LIFECYCLE_OBSERVED",
                        "sequence": sequence,
                        "assignment_id": assignment_id,
                        "request_id": request["request_id"],
                        "references": references,
                        "oracle": oracle,
                        "observed_utc": utc_now(),
                    },
                )
                self.seen_assignments.add(key)
                self.observed_assignments += 1
                if isinstance(oracle, dict) and oracle.get("classification") == "ABORT_REQUIRED":
                    self._finding(
                        kind="CANDIDATE_CONTROLLER_ORACLE_FINDING",
                        sequence=sequence,
                        cursor=cursor,
                        evidence=references,
                        correlated={
                            "assignment_id": assignment_id,
                            "request_id": request["request_id"],
                        },
                    )
            except (
                OSError,
                KeyError,
                TypeError,
                ValueError,
                json.JSONDecodeError,
            ) as exc:
                append_jsonl(
                    self.watcher / "WATCHER_OBSERVATIONS.jsonl",
                    {
                        "schema": "firmware-c3-watcher-semantic-observation/v1",
                        "attempt_id": self.attempt_id,
                        "kind": "ASSIGNMENT_OBSERVATION_DEFERRED",
                        "path": str(observation_path),
                        "reason": str(exc),
                        "observed_utc": utc_now(),
                    },
                )

    def run(self) -> int:
        deadline = time.monotonic() + 60.0
        while time.monotonic() < deadline and not self.launch_path.is_file():
            time.sleep(0.05)
        launch = read_json_object(self.launch_path)
        identity = launch.get("identity")
        if not isinstance(identity, dict):
            raise TypeError("ROOT helper launch identity is missing")
        candidate = _git_state(self.candidate)
        server = _git_state(self.server)
        if candidate["head"] != self.candidate_commit or not candidate["clean"]:
            raise RuntimeError(f"candidate identity is not ready: {candidate}")
        if server["head"] != self.server_commit or not server["clean"]:
            raise RuntimeError(f"server identity is not ready: {server}")
        cursor = self.inventory_cursor()
        write_new_json(
            self.watcher / "WATCHER_READY.json",
            {
                "schema": "firmware-c3-watcher-ready/v1",
                "attempt_id": self.attempt_id,
                "helper_identity": identity,
                "helper_launch": artifact_reference(self.launch_path),
                "observation_cursor": cursor,
                "candidate": candidate,
                "server": server,
                "capability_environment_empty": all(not os.environ.get(key) for key in self.capability_keys),
                "ready_utc": utc_now(),
            },
        )
        sequence = 0
        last_heartbeat = 0.0
        while not self.stop_path.is_file():
            self.scan_claims(sequence)
            self.scan_assignments(sequence, cursor)
            now = time.monotonic()
            if now - last_heartbeat >= self.heartbeat_interval:
                candidate = _git_state(self.candidate)
                server = _git_state(self.server)
                prior_cursor = cursor
                cursor = self.inventory_cursor()
                sequence += 1
                append_jsonl(
                    self.watcher / "WATCHER_HEARTBEATS.jsonl",
                    {
                        "schema": "firmware-c3-watcher-heartbeat/v1",
                        "attempt_id": self.attempt_id,
                        "sequence": sequence,
                        "helper_identity": identity,
                        "observation_cursor": cursor,
                        "cursor_changed": cursor != prior_cursor,
                        "semantic_counts": {
                            "unique_claim_versions_observed": self.observed_claims,
                            "assignment_controller_lifecycles_observed": self.observed_assignments,
                        },
                        "candidate": candidate,
                        "server": server,
                        "immediate_stop_present": (self.watcher / "ABORT_REQUIRED.json").is_file(),
                        "monotonic": now,
                        "observed_utc": utc_now(),
                    },
                )
                last_heartbeat = now
                if candidate["head"] != self.candidate_commit or not candidate["clean"]:
                    self._finding(
                        kind="CANDIDATE_IMMUTABILITY_CHANGED",
                        sequence=sequence,
                        cursor=cursor,
                        evidence=[],
                        correlated=candidate,
                        immediate_stop_condition="irreversible_acceptance_evidence_corruption",
                    )
                if server["head"] != self.server_commit or not server["clean"]:
                    self._finding(
                        kind="PINNED_SERVER_IMMUTABILITY_CHANGED",
                        sequence=sequence,
                        cursor=cursor,
                        evidence=[],
                        correlated=server,
                        immediate_stop_condition="unauthorized_or_wrong_resource_operation",
                    )
                forbidden = self.runtime / "targets/target"
                if forbidden.exists():
                    self._finding(
                        kind="NONCANONICAL_TARGET_ROOT",
                        sequence=sequence,
                        cursor=cursor,
                        evidence=[],
                        correlated={"forbidden_path": str(forbidden.resolve())},
                    )
            time.sleep(0.1)
        self.scan_claims(sequence)
        self.scan_assignments(sequence, cursor)
        write_new_json(
            self.watcher / "WATCHER_SERVICE_TERMINAL.json",
            {
                "schema": "firmware-c3-watcher-service-terminal/v1",
                "attempt_id": self.attempt_id,
                "last_sequence": sequence,
                "last_cursor": self.inventory_cursor(),
                "semantic_counts": {
                    "unique_claim_versions_observed": self.observed_claims,
                    "assignment_controller_lifecycles_observed": self.observed_assignments,
                },
                "candidate": _git_state(self.candidate),
                "server": _git_state(self.server),
                "immediate_stop_present": (self.watcher / "ABORT_REQUIRED.json").is_file(),
                "stopped_utc": utc_now(),
            },
        )
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the reusable external C3 deterministic observer.")
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    return WatcherLoop(_load_config(args.config.resolve(strict=True))).run()


if __name__ == "__main__":
    raise SystemExit(main())
