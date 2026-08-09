from __future__ import annotations

import hashlib
import json
import os
import subprocess
import time
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

IMMEDIATE_STOP_CONDITIONS = frozenset(
    {
        "unauthorized_or_wrong_resource_operation",
        "loss_of_live_process_containment_or_cleanup",
        "irreversible_acceptance_evidence_corruption",
    }
)

REQUIRED_OBSERVATION_FACTS = frozenset(
    {
        "helper_identity",
        "ready",
        "heartbeat",
        "terminal_service",
        "abort_disposition",
        "helper_exit",
    }
)


class OuterSupportError(RuntimeError):
    """Base error for the external C3 support layer."""


class AttemptIncomplete(OuterSupportError):
    """The outer attempt lacks enough evidence to close honestly."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_reference(path: Path) -> dict[str, str]:
    resolved = path.resolve(strict=True)
    if resolved.is_symlink() or not resolved.is_file():
        raise OuterSupportError(f"unsafe evidence reference: {resolved}")
    return {"path": str(resolved), "sha256": sha256(resolved)}


def validate_reference(value: Mapping[str, Any]) -> dict[str, str]:
    if set(value) != {"path", "sha256"}:
        raise OuterSupportError("evidence reference must contain exactly path and sha256")
    path_value = value.get("path")
    digest = value.get("sha256")
    if not isinstance(path_value, str) or not isinstance(digest, str) or len(digest) != 64:
        raise OuterSupportError("evidence reference values are invalid")
    observed = artifact_reference(Path(path_value))
    if observed != dict(value):
        raise OuterSupportError(f"evidence reference changed: {path_value}")
    return observed


def read_json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise OuterSupportError(f"expected JSON object: {path}")
    return value


def read_jsonl_objects(path: Path) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line:
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise OuterSupportError(f"expected JSON object at {path}:{line_number}")
        values.append(value)
    if not values:
        raise OuterSupportError(f"expected at least one JSONL record: {path}")
    return values


def write_new_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0),
        0o600,
    )
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as stream:
            stream.write(canonical_json(value))
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        os.close(descriptor)


def write_replace_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    if temporary.exists():
        raise OuterSupportError(f"stale temporary file: {temporary}")
    try:
        with temporary.open("xb") as stream:
            stream.write(canonical_json(value))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def append_jsonl(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(canonical_json(value).decode("utf-8") + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def _filetime_to_utc(ticks: int) -> str:
    epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
    microseconds, remainder = divmod(ticks, 10)
    rendered = (epoch + timedelta(microseconds=microseconds)).strftime("%Y-%m-%dT%H:%M:%S.%f")
    return f"{rendered}{remainder}Z"


def _windows_process_identity(pid: int) -> dict[str, Any]:
    import ctypes
    from ctypes import wintypes

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel32.OpenProcess.restype = wintypes.HANDLE
    kernel32.GetProcessTimes.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(wintypes.FILETIME),
        ctypes.POINTER(wintypes.FILETIME),
        ctypes.POINTER(wintypes.FILETIME),
        ctypes.POINTER(wintypes.FILETIME),
    ]
    kernel32.GetProcessTimes.restype = wintypes.BOOL
    kernel32.GetExitCodeProcess.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(wintypes.DWORD),
    ]
    kernel32.GetExitCodeProcess.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL
    handle = kernel32.OpenProcess(0x1000, False, pid)
    if not handle:
        raise OuterSupportError(f"OpenProcess failed for {pid}: {ctypes.get_last_error()}")
    try:
        created = wintypes.FILETIME()
        exited = wintypes.FILETIME()
        kernel = wintypes.FILETIME()
        user = wintypes.FILETIME()
        if not kernel32.GetProcessTimes(
            handle,
            ctypes.byref(created),
            ctypes.byref(exited),
            ctypes.byref(kernel),
            ctypes.byref(user),
        ):
            raise OuterSupportError(f"GetProcessTimes failed for {pid}: {ctypes.get_last_error()}")
        exit_code = wintypes.DWORD()
        if not kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code)):
            raise OuterSupportError(f"GetExitCodeProcess failed for {pid}: {ctypes.get_last_error()}")
        ticks = (created.dwHighDateTime << 32) | created.dwLowDateTime
        alive = exit_code.value == 259
        return {
            "pid": pid,
            "created_native": f"windows-filetime:{ticks}",
            "created_utc": _filetime_to_utc(ticks),
            "alive": alive,
            "exit_code_snapshot": None if alive else exit_code.value,
        }
    finally:
        kernel32.CloseHandle(handle)


def _procfs_process_identity(pid: int) -> dict[str, Any]:
    stat_path = Path("/proc") / str(pid) / "stat"
    try:
        raw = stat_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise OuterSupportError(f"cannot read process identity for {pid}") from exc
    close = raw.rfind(")")
    fields = raw[close + 2 :].split()
    if len(fields) < 20:
        raise OuterSupportError(f"invalid /proc identity for {pid}")
    start_ticks = fields[19]
    return {
        "pid": pid,
        "created_native": f"procfs-start-ticks:{start_ticks}",
        "created_utc": None,
        "alive": True,
        "exit_code_snapshot": None,
    }


def process_identity(pid: int) -> dict[str, Any]:
    if os.name == "nt":
        return _windows_process_identity(pid)
    return _procfs_process_identity(pid)


def process_identity_matches(pid: int, expected_native: str) -> bool:
    try:
        observed = process_identity(pid)
    except OuterSupportError:
        return False
    return bool(observed["alive"] and observed["created_native"] == expected_native)


@dataclass(frozen=True)
class RegisteredChild:
    name: str
    process: subprocess.Popen[Any]
    created_native: str


def cleanup_registered_children(
    children: Iterable[RegisteredChild],
    *,
    identity_matches: Callable[[int, str], bool] = process_identity_matches,
    terminate_timeout: float = 15.0,
    kill_timeout: float = 15.0,
) -> list[dict[str, Any]]:
    """Clean registered children without ever signalling an unverified PID.

    Every child receives an outcome even if an earlier child's identity is uncertain or cleanup
    raises. This keeps one harmless race from preventing cleanup of the rest of the topology.
    """

    outcomes: list[dict[str, Any]] = []
    for child in children:
        process = child.process
        base = {
            "name": child.name,
            "pid": process.pid,
            "created_native": child.created_native,
        }
        try:
            exit_code = process.poll()
            if exit_code is not None:
                outcomes.append(
                    {
                        **base,
                        "outcome": "already_exited",
                        "exit_code": exit_code,
                        "signalled": False,
                    }
                )
                continue
            if not identity_matches(process.pid, child.created_native):
                exit_code = process.poll()
                outcome = "already_exited_after_identity_race" if exit_code is not None else "identity_unverified"
                outcomes.append(
                    {
                        **base,
                        "outcome": outcome,
                        "exit_code": exit_code,
                        "signalled": False,
                    }
                )
                continue
            process.terminate()
            try:
                exit_code = process.wait(timeout=terminate_timeout)
                outcomes.append(
                    {
                        **base,
                        "outcome": "terminated",
                        "exit_code": exit_code,
                        "signalled": True,
                    }
                )
            except subprocess.TimeoutExpired:
                if not identity_matches(process.pid, child.created_native):
                    outcomes.append(
                        {
                            **base,
                            "outcome": "identity_unverified_after_terminate_timeout",
                            "exit_code": process.poll(),
                            "signalled": True,
                        }
                    )
                    continue
                process.kill()
                exit_code = process.wait(timeout=kill_timeout)
                outcomes.append(
                    {
                        **base,
                        "outcome": "killed",
                        "exit_code": exit_code,
                        "signalled": True,
                    }
                )
        except Exception as exc:  # noqa: BLE001 - cleanup must continue for the remaining registered children
            outcomes.append(
                {
                    **base,
                    "outcome": "cleanup_error",
                    "exit_code": process.poll(),
                    "signalled": False,
                    "error": str(exc),
                }
            )
    return outcomes


def classify_observer_record(record: Mapping[str, Any]) -> dict[str, Any]:
    condition = record.get("immediate_stop_condition")
    evidence = record.get("evidence")
    if (
        isinstance(condition, str)
        and condition in IMMEDIATE_STOP_CONDITIONS
        and isinstance(evidence, list)
        and evidence
    ):
        validated = [validate_reference(item) for item in evidence if isinstance(item, Mapping)]
        if len(validated) == len(evidence):
            return {
                "disposition": "IMMEDIATE_SAFETY_STOP",
                "condition": condition,
                "evidence": validated,
                "product_gate_invalidated": False,
            }
    return {
        "disposition": "POOL_FOR_POST_GATE_TRIAGE",
        "condition": condition,
        "product_gate_invalidated": False,
    }


def _validated_evidence_list(
    values: Sequence[Mapping[str, Any]],
) -> list[dict[str, str]]:
    return [validate_reference(value) for value in values]


def classify_outer_failure(
    *,
    attempt_closeable: bool,
    candidate_defect_evidence: Sequence[Mapping[str, Any]] = (),
    locked_input_change_evidence: Sequence[Mapping[str, Any]] = (),
    candidate_result_untrustworthy_evidence: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    candidate_evidence = _validated_evidence_list(candidate_defect_evidence)
    lock_evidence = _validated_evidence_list(locked_input_change_evidence)
    result_evidence = _validated_evidence_list(candidate_result_untrustworthy_evidence)
    material = bool(candidate_evidence or lock_evidence or result_evidence)
    if candidate_evidence:
        action = "TRIAGE_CANDIDATE_DEFECT"
    elif result_evidence:
        action = "MARK_AFFECTED_RESULT_INDETERMINATE"
    elif lock_evidence:
        action = "REFRESH_SCOPED_LOCK"
    elif attempt_closeable:
        action = "CORRECT_SUPPORT_IN_PLACE"
    else:
        action = "ROLL_OUTER_ATTEMPT_ONLY"
    return {
        "classification": "PRODUCT_MATERIAL_EVIDENCE" if material else "OUTER_ATTEMPT_PROCEDURE_FAILURE",
        "action": action,
        "candidate_gate_invalidated": bool(candidate_evidence),
        "affected_result_invalidated": bool(result_evidence),
        "lock_refresh_required": bool(lock_evidence),
        "preserve_valid_product_credit": True,
        "evidence": {
            "candidate_defect": candidate_evidence,
            "locked_input_change": lock_evidence,
            "candidate_result_untrustworthy": result_evidence,
        },
    }


def validate_fact_resolutions(
    resolutions: Sequence[Mapping[str, Any]],
    *,
    required_facts: frozenset[str] = REQUIRED_OBSERVATION_FACTS,
) -> list[dict[str, Any]]:
    validated: list[dict[str, Any]] = []
    seen: set[str] = set()
    for resolution in resolutions:
        fact_id = resolution.get("fact_id")
        mode = resolution.get("mode")
        conclusion = resolution.get("conclusion")
        sources = resolution.get("sources")
        correlation = resolution.get("correlation")
        if not isinstance(fact_id, str) or not fact_id or fact_id in seen:
            raise OuterSupportError("observation fact IDs must be unique non-empty strings")
        if mode not in {"PRIMARY", "BACKUP"}:
            raise OuterSupportError(f"invalid fact resolution mode for {fact_id}")
        if not isinstance(conclusion, str) or not conclusion:
            raise OuterSupportError(f"missing fact conclusion for {fact_id}")
        if not isinstance(sources, list) or not sources:
            raise OuterSupportError(f"missing fact sources for {fact_id}")
        if not isinstance(correlation, dict) or not correlation:
            raise OuterSupportError(f"missing fact correlation for {fact_id}")
        normalized_sources: list[dict[str, Any]] = []
        source_classes: set[str] = set()
        for source in sources:
            if not isinstance(source, Mapping) or set(source) != {
                "source_class",
                "reference",
            }:
                raise OuterSupportError(f"invalid fact source for {fact_id}")
            source_class = source.get("source_class")
            reference_value = source.get("reference")
            if not isinstance(source_class, str) or not source_class:
                raise OuterSupportError(f"invalid source class for {fact_id}")
            if not isinstance(reference_value, Mapping):
                raise OuterSupportError(f"invalid source reference for {fact_id}")
            source_classes.add(source_class)
            normalized_sources.append(
                {
                    "source_class": source_class,
                    "reference": validate_reference(reference_value),
                }
            )
        if mode == "BACKUP" and len(source_classes) < 2:
            raise AttemptIncomplete(f"backup resolution for {fact_id} lacks two independent source classes")
        seen.add(fact_id)
        validated.append(
            {
                "fact_id": fact_id,
                "mode": mode,
                "conclusion": conclusion,
                "sources": normalized_sources,
                "correlation": dict(correlation),
            }
        )
    missing = sorted(required_facts - seen)
    if missing:
        raise AttemptIncomplete(f"required observer facts are unresolved: {missing}")
    return validated


def write_observation_close(
    *,
    path: Path,
    attempt_id: str,
    launch_reference: Mapping[str, Any],
    fact_resolutions: Sequence[Mapping[str, Any]],
    exit_code: int,
    reaped: bool,
    optional_ai_watcher: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    launch = validate_reference(launch_reference)
    facts = validate_fact_resolutions(fact_resolutions)
    value = {
        "schema": "firmware-c3-watcher-observation-close/v1",
        "attempt_id": attempt_id,
        "owner": "ROOT-IM",
        "helper_launch": launch,
        "fact_resolutions": facts,
        "helper_exit": {"exit_code": exit_code, "reaped": reaped},
        "optional_ai_watcher": dict(optional_ai_watcher) if optional_ai_watcher is not None else None,
        "required_observation_complete": True,
        "closed_utc": utc_now(),
    }
    write_new_json(path, value)
    return value


def validate_observation_close(
    path: Path,
    *,
    attempt_id: str,
    expected_launch_reference: Mapping[str, Any],
) -> dict[str, Any]:
    value = read_json_object(path)
    expected_keys = {
        "schema",
        "attempt_id",
        "owner",
        "helper_launch",
        "fact_resolutions",
        "helper_exit",
        "optional_ai_watcher",
        "required_observation_complete",
        "closed_utc",
    }
    if set(value) != expected_keys:
        raise OuterSupportError("observation-close root keys are invalid")
    if (
        value.get("schema") != "firmware-c3-watcher-observation-close/v1"
        or value.get("attempt_id") != attempt_id
        or value.get("owner") != "ROOT-IM"
        or value.get("required_observation_complete") is not True
        or not isinstance(value.get("closed_utc"), str)
    ):
        raise OuterSupportError("observation-close identity/status is invalid")
    launch = value.get("helper_launch")
    if not isinstance(launch, Mapping) or validate_reference(launch) != validate_reference(expected_launch_reference):
        raise OuterSupportError("observation-close helper launch is invalid")
    resolutions = value.get("fact_resolutions")
    if not isinstance(resolutions, list) or not all(isinstance(item, Mapping) for item in resolutions):
        raise OuterSupportError("observation-close fact resolutions are invalid")
    validate_fact_resolutions(resolutions)
    helper_exit = value.get("helper_exit")
    if (
        not isinstance(helper_exit, dict)
        or set(helper_exit) != {"exit_code", "reaped"}
        or not isinstance(helper_exit.get("exit_code"), int)
        or isinstance(helper_exit.get("exit_code"), bool)
        or helper_exit.get("reaped") is not True
    ):
        raise OuterSupportError("observation-close helper exit is invalid")
    optional = value.get("optional_ai_watcher")
    if optional is not None and not isinstance(optional, dict):
        raise OuterSupportError("observation-close optional AI evidence is invalid")
    return value


@dataclass
class MechanicalObserver:
    attempt_id: str
    command: Sequence[str]
    cwd: Path
    topology_root: Path
    evidence_root: Path
    stop_path: Path
    ready_path: Path
    heartbeat_path: Path
    terminal_path: Path
    abort_path: Path
    environment: Mapping[str, str] | None = None
    process: subprocess.Popen[bytes] | None = None
    identity: dict[str, Any] | None = None
    launch_path: Path | None = None

    def _expected_identity(self) -> dict[str, Any]:
        if self.identity is None:
            raise OuterSupportError("mechanical observer identity is unavailable")
        return {
            "pid": self.identity["pid"],
            "created_native": self.identity["created_native"],
        }

    def _validate_identity(self, value: object, *, label: str) -> None:
        if not isinstance(value, Mapping):
            raise OuterSupportError(f"{label} identity is missing")
        expected = self._expected_identity()
        actual = {key: value.get(key) for key in expected}
        if actual != expected:
            raise OuterSupportError(f"{label} identity differs from helper launch")

    def _validate_primary_fact(self, fact_id: str, path: Path) -> None:
        if self.launch_path is None:
            raise OuterSupportError("mechanical observer launch record is unavailable")
        if fact_id == "heartbeat":
            records = read_jsonl_objects(path)
            prior_sequence = -1
            for record in records:
                if (
                    record.get("schema") != "firmware-c3-watcher-heartbeat/v1"
                    or record.get("attempt_id") != self.attempt_id
                ):
                    raise OuterSupportError("helper heartbeat schema/attempt is invalid")
                self._validate_identity(record.get("helper_identity"), label="helper heartbeat")
                sequence = record.get("sequence")
                if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence <= prior_sequence:
                    raise OuterSupportError("helper heartbeat sequence is invalid")
                prior_sequence = sequence
            return

        value = read_json_object(path)
        expected_schemas = {
            "helper_identity": "firmware-c3-watcher-helper-launch/v1",
            "ready": "firmware-c3-watcher-ready/v1",
            "terminal_service": "firmware-c3-watcher-service-terminal/v1",
            "abort_disposition": "firmware-c3-root-watcher-abort-observation/v1",
            "helper_exit": "firmware-c3-watcher-helper-exit/v1",
        }
        if value.get("schema") != expected_schemas[fact_id] or value.get("attempt_id") != self.attempt_id:
            raise OuterSupportError(f"{fact_id} schema/attempt is invalid")
        if fact_id == "helper_identity":
            self._validate_identity(value.get("identity"), label="helper launch")
        elif fact_id == "ready":
            self._validate_identity(value.get("helper_identity"), label="helper ready")
            launch = value.get("helper_launch")
            if not isinstance(launch, Mapping) or validate_reference(launch) != artifact_reference(self.launch_path):
                raise OuterSupportError("helper ready launch reference is invalid")
            if value.get("capability_environment_empty") is not True:
                raise OuterSupportError("helper ready record retained a capability environment")
        elif fact_id == "abort_disposition":
            present = value.get("abort_present")
            abort = value.get("abort")
            if not isinstance(present, bool):
                raise OuterSupportError("helper abort disposition is invalid")
            if present:
                if (
                    not isinstance(abort, Mapping)
                    or validate_reference(abort) != artifact_reference(self.abort_path)
                    or self.observer_disposition() is None
                ):
                    raise OuterSupportError("helper abort reference is invalid")
            elif abort is not None or self.abort_path.exists():
                raise OuterSupportError("helper abort absence is inconsistent")
        elif fact_id == "helper_exit":
            self._validate_identity(value.get("identity"), label="helper exit")
            launch = value.get("launch")
            if not isinstance(launch, Mapping) or validate_reference(launch) != artifact_reference(self.launch_path):
                raise OuterSupportError("helper exit launch reference is invalid")
            if value.get("reaped") is not True or not isinstance(value.get("exit_code"), int):
                raise OuterSupportError("helper exit/reap result is invalid")

    def start(self, *, timeout: float = 30.0) -> dict[str, Any]:
        if self.process is not None:
            raise OuterSupportError("mechanical observer already started")
        self.cwd.mkdir(parents=True, exist_ok=True)
        self.topology_root.mkdir(parents=True, exist_ok=True)
        self.evidence_root.mkdir(parents=True, exist_ok=True)
        stdout_path = self.cwd / "watcher-helper.stdout.log"
        stderr_path = self.cwd / "watcher-helper.stderr.log"
        stdout = stdout_path.open("xb")
        stderr = stderr_path.open("xb")
        flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) | getattr(subprocess, "CREATE_NO_WINDOW", 0)
        try:
            process = subprocess.Popen(
                list(self.command),
                cwd=self.cwd,
                env=dict(self.environment) if self.environment is not None else None,
                stdout=stdout,
                stderr=stderr,
                creationflags=flags,
            )
        finally:
            stdout.close()
            stderr.close()
        self.process = process
        self.identity = process_identity(process.pid)
        self.launch_path = self.topology_root / "WATCHER_HELPER_LAUNCH.json"
        write_new_json(
            self.launch_path,
            {
                "schema": "firmware-c3-watcher-helper-launch/v1",
                "attempt_id": self.attempt_id,
                "owner": "ROOT-IM",
                "command": list(self.command),
                "cwd": str(self.cwd.resolve()),
                "identity": self.identity,
                "outputs": {
                    "stdout": str(stdout_path.resolve()),
                    "stderr": str(stderr_path.resolve()),
                },
                "launched_utc": utc_now(),
            },
        )
        deadline = time.monotonic() + timeout
        try:
            while time.monotonic() < deadline:
                if self.ready_path.is_file():
                    ready = read_json_object(self.ready_path)
                    if ready.get("attempt_id") != self.attempt_id:
                        raise AttemptIncomplete("mechanical observer ready record has the wrong attempt")
                    try:
                        self._validate_primary_fact("ready", self.ready_path)
                    except OuterSupportError as exc:
                        raise AttemptIncomplete(str(exc)) from exc
                    return ready
                if process.poll() is not None:
                    raise AttemptIncomplete(f"mechanical observer exited before ready: exit={process.returncode}")
                time.sleep(0.05)
            raise AttemptIncomplete(f"mechanical observer did not become ready: {self.ready_path}")
        except (OSError, ValueError, json.JSONDecodeError, AttemptIncomplete) as exc:
            cleanup = cleanup_registered_children(
                [
                    RegisteredChild(
                        "deterministic-observer",
                        process,
                        str(self.identity["created_native"]),
                    )
                ]
            )
            failure_path = self.topology_root / "WATCHER_HELPER_START_FAILURE.json"
            if not failure_path.exists():
                write_new_json(
                    failure_path,
                    {
                        "schema": "firmware-c3-watcher-helper-start-failure/v1",
                        "attempt_id": self.attempt_id,
                        "launch": artifact_reference(self.launch_path),
                        "reason": str(exc),
                        "cleanup": cleanup,
                        "failed_utc": utc_now(),
                    },
                )
            if isinstance(exc, AttemptIncomplete):
                raise
            raise AttemptIncomplete(str(exc)) from exc

    def observer_disposition(self) -> dict[str, Any] | None:
        if not self.abort_path.is_file():
            return None
        value = read_json_object(self.abort_path)
        if value.get("schema") != "firmware-c3-watcher-immediate-stop/v1" or value.get("attempt_id") != self.attempt_id:
            raise OuterSupportError("helper immediate-stop record is invalid")
        return classify_observer_record(value)

    def stop_and_close(
        self,
        *,
        timeout: float = 30.0,
        fallback_resolutions: Sequence[Mapping[str, Any]] = (),
        optional_ai_watcher: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        if self.process is None or self.identity is None or self.launch_path is None:
            raise OuterSupportError("mechanical observer was not started")
        if not self.stop_path.exists():
            write_new_json(
                self.stop_path,
                {
                    "schema": "firmware-c3-root-watcher-stop-request/v1",
                    "attempt_id": self.attempt_id,
                    "requested_utc": utc_now(),
                },
            )
        try:
            exit_code = self.process.wait(timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            cleanup = cleanup_registered_children(
                [
                    RegisteredChild(
                        "deterministic-observer",
                        self.process,
                        str(self.identity["created_native"]),
                    )
                ]
            )
            failure_path = self.topology_root / "WATCHER_HELPER_STOP_FAILURE.json"
            if not failure_path.exists():
                write_new_json(
                    failure_path,
                    {
                        "schema": "firmware-c3-watcher-helper-stop-failure/v1",
                        "attempt_id": self.attempt_id,
                        "launch": artifact_reference(self.launch_path),
                        "cleanup": cleanup,
                        "failed_utc": utc_now(),
                    },
                )
            raise AttemptIncomplete(f"mechanical observer did not stop within the closure timeout: {cleanup}") from exc

        helper_exit_path = self.topology_root / "WATCHER_HELPER_EXIT.json"
        if not helper_exit_path.exists():
            write_new_json(
                helper_exit_path,
                {
                    "schema": "firmware-c3-watcher-helper-exit/v1",
                    "attempt_id": self.attempt_id,
                    "launch": artifact_reference(self.launch_path),
                    "identity": self.identity,
                    "exit_code": exit_code,
                    "reaped": True,
                    "terminal_service": artifact_reference(self.terminal_path)
                    if self.terminal_path.is_file()
                    else None,
                    "exited_utc": utc_now(),
                },
            )

        abort_observation_path = self.topology_root / "WATCHER_ABORT_OBSERVATION.json"
        if not abort_observation_path.exists():
            write_new_json(
                abort_observation_path,
                {
                    "schema": "firmware-c3-root-watcher-abort-observation/v1",
                    "attempt_id": self.attempt_id,
                    "abort_present": self.abort_path.is_file(),
                    "abort": artifact_reference(self.abort_path) if self.abort_path.is_file() else None,
                    "observed_utc": utc_now(),
                },
            )

        primary_paths = {
            "helper_identity": self.launch_path,
            "ready": self.ready_path,
            "heartbeat": self.heartbeat_path,
            "terminal_service": self.terminal_path,
            "abort_disposition": abort_observation_path,
            "helper_exit": helper_exit_path,
        }
        fallback_by_fact = {
            str(item.get("fact_id")): item for item in fallback_resolutions if isinstance(item, Mapping)
        }
        resolutions: list[dict[str, Any]] = []
        for fact_id in sorted(REQUIRED_OBSERVATION_FACTS):
            primary = primary_paths[fact_id]
            if primary.is_file():
                try:
                    self._validate_primary_fact(fact_id, primary)
                except (
                    OSError,
                    ValueError,
                    json.JSONDecodeError,
                    OuterSupportError,
                ) as exc:
                    if fact_id not in fallback_by_fact:
                        raise AttemptIncomplete(
                            f"observer fact is invalid and has no approved backup: {fact_id}: {exc}"
                        ) from exc
                    resolutions.append(dict(fallback_by_fact[fact_id]))
                else:
                    resolutions.append(
                        {
                            "fact_id": fact_id,
                            "mode": "PRIMARY",
                            "conclusion": f"{fact_id} established by the normal observer path",
                            "sources": [
                                {
                                    "source_class": "mechanical_observer"
                                    if fact_id not in {"helper_identity", "abort_disposition"}
                                    else "root_supervisor",
                                    "reference": artifact_reference(primary),
                                }
                            ],
                            "correlation": {
                                "attempt_id": self.attempt_id,
                                "helper_pid": self.identity["pid"],
                            },
                        }
                    )
            elif fact_id in fallback_by_fact:
                resolutions.append(dict(fallback_by_fact[fact_id]))
            else:
                raise AttemptIncomplete(f"observer fact is missing and has no approved backup: {fact_id}")

        close_path = self.topology_root / "WATCHER_OBSERVATION_CLOSE.json"
        return write_observation_close(
            path=close_path,
            attempt_id=self.attempt_id,
            launch_reference=artifact_reference(self.launch_path),
            fact_resolutions=resolutions,
            exit_code=exit_code,
            reaped=True,
            optional_ai_watcher=optional_ai_watcher,
        )
