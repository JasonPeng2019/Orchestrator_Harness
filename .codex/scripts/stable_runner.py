"""Fail-closed entry point for the immutable implementation runner.

This file is intentionally outside both harness checkouts.  It validates the detached
stable checkout before importing any harness code, removes ambient Python import inputs,
and then delegates only to the stable CLI/controller entry points.  The projection helper
is the explicit compatibility boundary for candidate-only coding fields and resolves
workflow-role allocations from the campaign's adjustable data file.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import re
import subprocess
import sys
import sysconfig
import tempfile
import time
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
LOCK_PATH = (
    ROOT
    / "plans"
    / "general-coding-harness"
    / "runtime"
    / "firmware-v2"
    / "runner-migration"
    / "STABLE_RUNNER_LOCK.json"
)
ROLE_MODEL_MAPPING_PATH = ROOT / "plans" / "general-coding-harness" / "SUBAGENT_ROLE_MODEL_MAPPING.json"
REQUIRED_COMMIT = "4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f"
ALLOWED_MODULES = frozenset(
    {
        "orchestrator_harness.cli",
        "orchestrator_harness.operator_launch",
        "orchestrator_harness.lane_controller",
    }
)
_CANDIDATE_ONLY_FIELDS = frozenset({"finding_gate", "child_environment_isolation"})
_COMMON_FIELDS = frozenset(
    {
        "action",
        "config_overrides",
        "codex_command",
        "doer",
        "label",
        "last_message_path",
        "model_settings",
        "output_paths",
        "phase",
        "prompt_path",
        "prompt_sha256",
        "run_root",
        "schema",
        "server_snapshot",
        "stderr_path",
        "task",
        "resume_thread_id",
    }
)
_FIRMWARE_FIELDS = frozenset(
    {
        "declared_lane_id",
        "lane_event_log",
        "leases",
        "board_tokens",
        "mcp_servers",
        "policy_sha256",
    }
)
_CODING_FIELDS = frozenset(
    {
        "codex",
        "codex_settings",
        "event_log",
        "event_log_path",
        "exclusive_resources",
        "git",
        "lane_id",
        "repository",
        "resource_lock_root",
        "resources",
        "resume",
        "resume_identity",
        "runtime_root",
        "worker_invocation_id",
    }
)
_REQUIRED_SANDBOX = "danger-full-access"
_REQUIRED_APPROVAL_POLICY = "never"
_REQUIRED_APPROVALS_REVIEWER = "user"
_REQUIRED_CONFIG_OVERRIDES = (
    'approval_policy="never"',
    'approvals_reviewer="user"',
)


class RunnerError(RuntimeError):
    """A fail-closed runner validation or dispatch error."""


def _inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def _git_value(root: Path, *args: str) -> str:
    result = _git(root, *args)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RunnerError(f"git {' '.join(args)} failed: {detail}")
    return result.stdout.strip()


def _read_lock(path: Path = LOCK_PATH) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RunnerError(f"cannot read stable runner lock: {exc}") from exc
    if not isinstance(value, dict):
        raise RunnerError("stable runner lock must be a JSON object")
    required = {
        "schema",
        "runner_name",
        "stable_root",
        "required_commit",
        "detached",
        "projection_schema",
    }
    if set(value) != required:
        raise RunnerError("stable runner lock has an unexpected schema")
    if value["schema"] != "stable-implementation-runner-lock/v1":
        raise RunnerError("stable runner lock schema is unsupported")
    if value["runner_name"] != "stable-general-harness-runner":
        raise RunnerError("stable runner lock names the wrong runner")
    if value["stable_root"] != "stable-general-harness-runner":
        raise RunnerError("stable runner lock points outside the pinned checkout name")
    if value["required_commit"] != REQUIRED_COMMIT or value["detached"] is not True:
        raise RunnerError("stable runner lock does not pin detached 4699d27")
    if value["projection_schema"] != "stable-compatible-invocation/v1":
        raise RunnerError("stable runner lock has an unsupported projection schema")
    return value


def validate_checkout(*, lock_path: Path = LOCK_PATH, repository_root: Path | None = None) -> dict[str, Any]:
    """Validate the exact clean detached checkout and return its proof material."""
    lock = _read_lock(lock_path)
    base_root = (repository_root or ROOT).resolve(strict=False)
    locked_path = base_root / str(lock["stable_root"])
    if locked_path.is_symlink():
        raise RunnerError(f"stable checkout is a symlink: {locked_path}")
    stable_root = locked_path.resolve(strict=False)
    if not stable_root.is_dir():
        raise RunnerError(f"stable checkout is not a real directory: {stable_root}")
    top = _git_value(stable_root, "rev-parse", "--show-toplevel")
    if Path(top).resolve(strict=False) != stable_root:
        raise RunnerError("stable checkout top-level path does not match the lock")
    commit = _git_value(stable_root, "rev-parse", "HEAD").lower()
    if commit != REQUIRED_COMMIT:
        raise RunnerError(f"stable checkout commit is {commit}, expected {REQUIRED_COMMIT}")
    status = _git(stable_root, "status", "--porcelain=v1", "--untracked-files=all")
    if status.returncode != 0:
        raise RunnerError(f"cannot inspect stable checkout status: {status.stderr.strip()}")
    if status.stdout:
        raise RunnerError("stable checkout is dirty")
    detached = _git(stable_root, "symbolic-ref", "--quiet", "--short", "HEAD")
    if detached.returncode == 0 and detached.stdout.strip():
        raise RunnerError(f"stable checkout is attached to branch {detached.stdout.strip()}")
    if detached.returncode not in {0, 1}:
        raise RunnerError(f"cannot prove stable checkout is detached: {detached.stderr.strip()}")
    common_dir = _git_value(stable_root, "rev-parse", "--git-common-dir")
    return {
        "stable_root": str(stable_root),
        "commit": commit,
        "clean": True,
        "detached": True,
        "git_common_dir": str(Path(common_dir).resolve(strict=False)),
    }


def _stdlib_roots() -> tuple[Path, ...]:
    paths = sysconfig.get_paths()
    values = [paths.get("stdlib"), paths.get("platstdlib")]
    if os.name == "nt":
        values.extend(str(Path(prefix) / "DLLs") for prefix in (sys.base_prefix, sys.base_exec_prefix) if prefix)
    return tuple(Path(item).resolve(strict=False) for item in values if item)


def _site_package_roots() -> tuple[Path, ...]:
    paths = sysconfig.get_paths()
    return tuple(Path(item).resolve(strict=False) for item in (paths.get("purelib"), paths.get("platlib")) if item)


def _is_stdlib_entry(value: str, roots: tuple[Path, ...], excluded: tuple[Path, ...] = ()) -> bool:
    if not value:
        return False
    path = Path(value).resolve(strict=False)
    if any(_inside(path, root) for root in excluded):
        return False
    if path.suffix == ".zip":
        return any(path.parent == root.parent or root in path.parents for root in roots)
    return any(_inside(path, root) for root in roots)


def _scrub_import_environment(stable_root: Path) -> None:
    for key in (
        "PYTHONPATH",
        "PYTHONHOME",
        "PYTHONUSERBASE",
        "PYTHONSAFEPATH",
    ):
        os.environ.pop(key, None)
    roots = _stdlib_roots()
    excluded = _site_package_roots()
    original = list(sys.path)
    sys.path[:] = [str(stable_root)] + [item for item in original if _is_stdlib_entry(item, roots, excluded)]
    for name, module in list(sys.modules.items()):
        if name != "orchestrator_harness" and not name.startswith("orchestrator_harness."):
            continue
        origin = getattr(module, "__file__", None)
        if origin is not None and not _inside(Path(origin).resolve(strict=False), stable_root):
            raise RunnerError(f"conflicting preloaded import: {name} from {origin}")
        del sys.modules[name]


def import_stable_module(module_name: str, proof: Mapping[str, Any]) -> tuple[ModuleType, dict[str, Any]]:
    if module_name not in ALLOWED_MODULES:
        raise RunnerError(f"module is outside the stable runner boundary: {module_name}")
    stable_root = Path(str(proof["stable_root"])).resolve(strict=True)
    _scrub_import_environment(stable_root)
    try:
        package = importlib.import_module("orchestrator_harness")
        module = importlib.import_module(module_name)
    except Exception as exc:
        raise RunnerError(f"stable module import failed: {exc}") from exc
    origins: dict[str, str] = {}
    for name, value in (("orchestrator_harness", package), (module_name, module)):
        origin = getattr(value, "__file__", None)
        if not isinstance(origin, str):
            raise RunnerError(f"{name} has no file import origin")
        resolved = Path(origin).resolve(strict=False)
        if not _inside(resolved, stable_root):
            raise RunnerError(f"{name} imported outside stable checkout: {resolved}")
        origins[name] = str(resolved)
    actual = dict(proof)
    actual["module"] = module_name
    actual["package_origin"] = origins["orchestrator_harness"]
    actual["module_origin"] = origins[module_name]
    return module, actual


def _canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def _write_new_json(path: Path, value: Mapping[str, Any], *, data: bytes | None = None) -> str:
    path = path.resolve(strict=False)
    if not path.parent.is_dir():
        raise RunnerError(f"output parent does not exist: {path.parent}")
    payload = data if data is not None else _canonical(dict(value))
    try:
        with path.open("xb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise RunnerError(f"refusing to overwrite immutable output: {path}") from exc
    return hashlib.sha256(payload).hexdigest()


def _reject_inside_stable(path: Path | None, stable_root: Path, label: str) -> None:
    if path is not None and _inside(path.resolve(strict=False), stable_root):
        raise RunnerError(f"{label} may not be inside the immutable stable checkout")


def _projection_allowed_fields(raw: Mapping[str, Any]) -> tuple[set[str], set[str]]:
    schema = raw.get("schema")
    if schema is None:
        return set(_COMMON_FIELDS | _FIRMWARE_FIELDS - {"schema"}), set()
    if schema == "orchestrator-coding-invocation/v1":
        return set(_COMMON_FIELDS | _CODING_FIELDS), set(_CANDIDATE_ONLY_FIELDS)
    raise RunnerError("stable projection only accepts schema-less firmware or coding v1 inputs")


_BACKEND_ERROR_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("HTTP_429", re.compile(r"\b(?:http(?:\s+status)?\s*)?429\b", re.IGNORECASE)),
    ("HTTP_303", re.compile(r"\b(?:http(?:\s+status)?\s*)?303\b", re.IGNORECASE)),
    (
        "RATE_LIMIT",
        re.compile(r"\brate[ -]?limit(?:ed|ing)?\b|\btoo many requests\b", re.IGNORECASE),
    ),
    (
        "BACKEND_ERROR",
        re.compile(
            r"\b(?:backend|upstream|service) (?:error|unavailable|overloaded)\b",
            re.IGNORECASE,
        ),
    ),
)


def classify_backend_error(text: str) -> str | None:
    """Return the redacted, workflow-level class of a temporary provider failure."""
    for error_class, pattern in _BACKEND_ERROR_PATTERNS:
        if pattern.search(text):
            return error_class
    return None


def _profile_config_overrides(profile: Mapping[str, Any]) -> list[str]:
    overrides: list[str] = []
    context_window = profile["model_context_window"]
    compact_limit = profile["model_auto_compact_token_limit"]
    compact_scope = profile["model_auto_compact_token_limit_scope"]
    if context_window is not None:
        assert isinstance(context_window, int)
        overrides.append(f"model_context_window={context_window}")
    if compact_limit is not None:
        assert isinstance(compact_limit, int)
        overrides.append(f"model_auto_compact_token_limit={compact_limit}")
        assert isinstance(compact_scope, str)
        overrides.append("model_auto_compact_token_limit_scope=" + json.dumps(compact_scope))
    catalog_path = profile["model_catalog_path"]
    if catalog_path is not None:
        assert isinstance(catalog_path, str)
        catalog = (ROOT / catalog_path).resolve(strict=False)
        overrides.append("model_catalog_json=" + json.dumps(catalog.as_posix()))
    return overrides


def _apply_profile_command(
    command: Any,
    codex_flags: list[str],
) -> list[str]:
    if not isinstance(command, list) or not all(isinstance(item, str) and item for item in command):
        return ["codex", *codex_flags]
    if command and Path(command[0]).name.lower() in {"codex", "codex.exe"}:
        resolved = list(command)
        for flag in codex_flags:
            if flag not in resolved:
                resolved.append(flag)
        return resolved
    return list(command)


def _require_full_access_settings(settings: Mapping[str, Any], settings_name: str) -> None:
    """Refuse any outer worker invocation that could prompt or be sandboxed."""
    if settings.get("sandbox") != _REQUIRED_SANDBOX:
        raise RunnerError(f"{settings_name} sandbox must be {_REQUIRED_SANDBOX!r} for every outer workflow role")
    if settings.get("approval_policy") != _REQUIRED_APPROVAL_POLICY:
        raise RunnerError(
            f"{settings_name} approval_policy must be {_REQUIRED_APPROVAL_POLICY!r} for every outer workflow role"
        )


def _read_backend_failure_history(path: Path) -> tuple[dict[str, Any], str]:
    try:
        data = path.read_bytes()
        raw = json.loads(data.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RunnerError(f"cannot read backend-failure history: {exc}") from exc
    if not isinstance(raw, dict) or set(raw) != {
        "schema",
        "workflow_role",
        "logical_task_id",
        "attempts",
    }:
        raise RunnerError("backend-failure history has an unexpected schema")
    if raw["schema"] != "orchestrator-backend-failure-history/v1":
        raise RunnerError("backend-failure history schema is unsupported")
    if not isinstance(raw["workflow_role"], str) or not raw["workflow_role"]:
        raise RunnerError("backend-failure history workflow_role is invalid")
    if not isinstance(raw["logical_task_id"], str) or not raw["logical_task_id"]:
        raise RunnerError("backend-failure history logical_task_id is invalid")
    attempts = raw["attempts"]
    if not isinstance(attempts, list) or not attempts:
        raise RunnerError("backend-failure history requires at least one attempt")
    for attempt in attempts:
        if not isinstance(attempt, dict) or set(attempt) != {
            "attempt_id",
            "profile_id",
            "outcome",
            "error_class",
            "error_sha256",
        }:
            raise RunnerError("backend-failure history attempt has an unexpected schema")
        if not all(isinstance(attempt[key], str) and attempt[key] for key in attempt):
            raise RunnerError("backend-failure history attempt has an invalid value")
        error_hash = attempt["error_sha256"]
        if len(error_hash) != 64 or any(char not in "0123456789abcdef" for char in error_hash):
            raise RunnerError("backend-failure history error_sha256 is invalid")
    return raw, hashlib.sha256(data).hexdigest()


def _read_role_model_mapping(
    path: Path | None = None,
) -> dict[str, dict[str, Any]]:
    selected = (path or ROLE_MODEL_MAPPING_PATH).resolve(strict=False)
    try:
        data = selected.read_bytes()
        raw = json.loads(data.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RunnerError(f"cannot read subagent role-model mapping: {exc}") from exc
    if not isinstance(raw, dict) or set(raw) != {"schema", "profiles", "roles"}:
        raise RunnerError("subagent role-model mapping must contain only schema, profiles, and roles")
    if raw["schema"] != "orchestrator-subagent-role-model-mapping/v2":
        raise RunnerError("subagent role-model mapping schema is unsupported")
    profiles = raw["profiles"]
    roles = raw["roles"]
    if not isinstance(profiles, dict) or not profiles or not isinstance(roles, dict) or not roles:
        raise RunnerError("subagent role-model mapping requires at least one role")
    normalized_profiles: dict[str, dict[str, Any]] = {}
    profile_keys = {
        "model",
        "reasoning_effort",
        "service_tier",
        "codex_flags",
        "model_context_window",
        "model_auto_compact_token_limit",
        "model_auto_compact_token_limit_scope",
        "model_catalog_path",
    }
    for profile_id, value in profiles.items():
        if not isinstance(profile_id, str) or not profile_id or not isinstance(value, dict):
            raise RunnerError("launch profile names and entries must be non-empty objects")
        if set(value) != profile_keys:
            raise RunnerError(f"launch profile {profile_id} has an unexpected schema")
        if not all(isinstance(value[key], str) and value[key] for key in ("model", "reasoning_effort", "service_tier")):
            raise RunnerError(f"launch profile {profile_id} has empty model settings")
        flags = value["codex_flags"]
        if not isinstance(flags, list) or not all(isinstance(flag, str) and flag for flag in flags):
            raise RunnerError(f"launch profile {profile_id} has invalid codex_flags")
        context_window = value["model_context_window"]
        compact_limit = value["model_auto_compact_token_limit"]
        compact_scope = value["model_auto_compact_token_limit_scope"]
        if (context_window is None) != (compact_limit is None) or (compact_limit is None) != (compact_scope is None):
            raise RunnerError(f"launch profile {profile_id} has incomplete context settings")
        if context_window is not None:
            if (
                not isinstance(context_window, int)
                or not isinstance(compact_limit, int)
                or not isinstance(compact_scope, str)
            ):
                raise RunnerError(f"launch profile {profile_id} has invalid context settings")
            if context_window <= 0 or compact_limit <= 0 or compact_limit >= context_window:
                raise RunnerError(f"launch profile {profile_id} has unsafe context settings")
            if compact_scope != "total":
                raise RunnerError(f"launch profile {profile_id} has unsupported compaction scope")
        catalog_path = value["model_catalog_path"]
        if catalog_path is not None:
            if not isinstance(catalog_path, str) or not catalog_path:
                raise RunnerError(f"launch profile {profile_id} has invalid model_catalog_path")
            catalog = (ROOT / catalog_path).resolve(strict=False)
            if not _inside(catalog, ROOT) or not catalog.is_file():
                raise RunnerError(f"launch profile {profile_id} model_catalog_path is unavailable")
        normalized_profiles[profile_id] = {
            **value,
            "codex_flags": list(flags),
        }
    normalized: dict[str, dict[str, Any]] = {}
    role_keys = {
        "primary_profile",
        "fallback_profile",
        "fallback_after_consecutive_backend_failures",
        "fallback_error_classes",
        "finding_gate_role",
    }
    for role, value in roles.items():
        if not isinstance(role, str) or not role or not isinstance(value, dict):
            raise RunnerError("subagent role-model names and entries must be non-empty objects")
        if set(value) != role_keys:
            raise RunnerError(f"subagent role-model entry {role} has an unexpected schema")
        primary = value["primary_profile"]
        fallback = value["fallback_profile"]
        threshold = value["fallback_after_consecutive_backend_failures"]
        error_classes = value["fallback_error_classes"]
        gate_role = value["finding_gate_role"]
        if not isinstance(primary, str) or primary not in normalized_profiles:
            raise RunnerError(f"subagent role-model entry {role} has an invalid primary_profile")
        if gate_role is not None and (not isinstance(gate_role, str) or not gate_role):
            raise RunnerError(f"subagent role-model entry {role} has an invalid finding_gate_role")
        if fallback is None:
            if threshold is not None or error_classes != []:
                raise RunnerError(f"subagent role-model entry {role} has fallback settings without a fallback profile")
        else:
            if not isinstance(fallback, str) or fallback not in normalized_profiles or fallback == primary:
                raise RunnerError(f"subagent role-model entry {role} has an invalid fallback_profile")
            if not isinstance(threshold, int) or threshold < 2:
                raise RunnerError(f"subagent role-model entry {role} has an invalid fallback threshold")
            if (
                not isinstance(error_classes, list)
                or not error_classes
                or not all(
                    isinstance(item, str) and item in {name for name, _ in _BACKEND_ERROR_PATTERNS}
                    for item in error_classes
                )
            ):
                raise RunnerError(f"subagent role-model entry {role} has invalid fallback error classes")
        primary_profile = normalized_profiles[primary]
        normalized[role] = {
            "model": primary_profile["model"],
            "reasoning_effort": primary_profile["reasoning_effort"],
            "service_tier": primary_profile["service_tier"],
            "finding_gate_role": gate_role,
            "primary_profile": primary,
            "fallback_profile": fallback,
            "fallback_after_consecutive_backend_failures": threshold,
            "fallback_error_classes": list(error_classes),
            "profiles": normalized_profiles,
        }
    return normalized


def _select_launch_profile(
    allocation: Mapping[str, Any],
    workflow_role: str,
    *,
    requested_profile: str | None,
    fallback_history: Mapping[str, Any] | None,
) -> str:
    primary = allocation["primary_profile"]
    fallback = allocation["fallback_profile"]
    assert isinstance(primary, str)
    if fallback_history is None:
        if requested_profile is None or requested_profile == primary:
            return primary
        if requested_profile == fallback:
            raise RunnerError("fallback profile requires a proven backend-failure history")
        raise RunnerError("requested launch profile is not allowed for this workflow role")
    if fallback is None:
        raise RunnerError("workflow role has no fallback profile")
    if fallback_history.get("workflow_role") != workflow_role:
        raise RunnerError("backend-failure history workflow_role does not match the dispatch")
    attempts = fallback_history["attempts"]
    assert isinstance(attempts, list)
    allowed_classes = set(allocation["fallback_error_classes"])
    streak = 0
    for attempt in reversed(attempts):
        if (
            attempt["profile_id"] == primary
            and attempt["outcome"] == "BACKEND_FAILURE"
            and attempt["error_class"] in allowed_classes
        ):
            streak += 1
            continue
        break
    threshold = allocation["fallback_after_consecutive_backend_failures"]
    assert isinstance(threshold, int)
    if streak < threshold:
        raise RunnerError(
            f"fallback profile requires {threshold} consecutive classified backend failures; found {streak}"
        )
    if requested_profile is not None and requested_profile != fallback:
        raise RunnerError("backend-failure fallback can select only the role's declared fallback profile")
    return fallback


def apply_workflow_role_allocation(
    raw: Mapping[str, Any],
    workflow_role: str,
    *,
    validate_finding_gate: bool,
    role_model_mapping_path: Path | None = None,
    launch_profile: str | None = None,
    fallback_history: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Resolve the current role allocation into an invocation."""
    roles = _read_role_model_mapping(role_model_mapping_path)
    expected = roles.get(workflow_role)
    if expected is None:
        raise RunnerError(f"unknown workflow role: {workflow_role}")
    selected_profile = _select_launch_profile(
        expected,
        workflow_role,
        requested_profile=launch_profile,
        fallback_history=fallback_history,
    )
    if (
        selected_profile == expected["fallback_profile"]
        and raw.get("schema") == "orchestrator-coding-invocation/v1"
        and raw.get("action") != "start"
    ):
        raise RunnerError("fallback profile requires a new P02 handoff invocation with action=start")
    profiles = expected["profiles"]
    assert isinstance(profiles, Mapping)
    profile = profiles[selected_profile]
    assert isinstance(profile, Mapping)
    settings_name = "codex" if raw.get("schema") == "orchestrator-coding-invocation/v1" else "model_settings"
    settings = raw.get(settings_name)
    if not isinstance(settings, Mapping):
        raise RunnerError(f"{settings_name} must be an object for workflow-role resolution")
    _require_full_access_settings(settings, settings_name)
    resolved = dict(raw)
    resolved_settings = dict(settings)
    for key in ("model", "reasoning_effort", "service_tier"):
        value = profile[key]
        assert isinstance(value, str)
        resolved_settings[key] = value
    resolved_settings["command"] = _apply_profile_command(
        resolved_settings.get("command", raw.get("codex_command", ["codex"])),
        list(profile["codex_flags"]),
    )
    existing_overrides = resolved_settings.get("config_overrides", raw.get("config_overrides", []))
    if not isinstance(existing_overrides, list) or not all(
        isinstance(item, str) and item for item in existing_overrides
    ):
        raise RunnerError(f"{settings_name} config_overrides must be a string list")
    profile_overrides = _profile_config_overrides(profile)
    managed_override_keys = {
        *{item.partition("=")[0] for item in profile_overrides},
        *{item.partition("=")[0] for item in _REQUIRED_CONFIG_OVERRIDES},
    }
    resolved_settings["config_overrides"] = [
        item for item in existing_overrides if item.partition("=")[0] not in managed_override_keys
    ] + [*_REQUIRED_CONFIG_OVERRIDES, *profile_overrides]
    resolved_settings["launch_profile"] = selected_profile
    resolved[settings_name] = resolved_settings
    if raw.get("schema") != "orchestrator-coding-invocation/v1":
        resolved["codex_command"] = list(resolved_settings["command"])
        resolved["config_overrides"] = list(resolved_settings["config_overrides"])
    if validate_finding_gate:
        gate = resolved.get("finding_gate")
        actual_gate_role = gate.get("role") if isinstance(gate, Mapping) else None
        expected_gate_role = expected["finding_gate_role"]
        if actual_gate_role != expected_gate_role:
            raise RunnerError(
                f"workflow role {workflow_role} requires finding_gate role "
                f"{expected_gate_role!r}, got {actual_gate_role!r}"
            )
    return resolved


def project_invocation(
    *,
    input_path: Path,
    output_path: Path,
    record_path: Path,
    proof: Mapping[str, Any],
    workflow_role: str,
    launch_profile: str | None = None,
    fallback_history: Mapping[str, Any] | None = None,
    fallback_history_sha256: str | None = None,
) -> dict[str, Any]:
    """Create an explicit stable-compatible projection for the selected workflow role."""
    stable_root = Path(str(proof["stable_root"])).resolve(strict=True)
    _reject_inside_stable(output_path, stable_root, "projection output")
    _reject_inside_stable(record_path, stable_root, "projection record")
    try:
        source_bytes = input_path.read_bytes()
        raw = json.loads(source_bytes.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RunnerError(f"cannot read candidate invocation: {exc}") from exc
    if not isinstance(raw, dict):
        raise RunnerError("candidate invocation must be a JSON object")
    resolved = apply_workflow_role_allocation(
        raw,
        workflow_role,
        validate_finding_gate=True,
        launch_profile=launch_profile,
        fallback_history=fallback_history,
    )
    allowed, removable = _projection_allowed_fields(resolved)
    unknown = set(resolved) - allowed - removable
    if unknown:
        raise RunnerError("projection refuses unknown fields: " + ", ".join(sorted(unknown)))
    present = sorted(set(resolved) & removable)
    if resolved.get("schema") is None and present:
        raise RunnerError("candidate-only coding fields cannot appear on a schema-less firmware route")
    if "finding_gate" in present:
        gate = resolved["finding_gate"]
        if not isinstance(gate, dict) or set(gate) != {"role", "path"}:
            raise RunnerError("finding_gate must retain its closed role/path shape")
        if (
            gate["role"] not in {"reviewer", "test_writer", "test_executor"}
            or not isinstance(gate["path"], str)
            or not gate["path"]
        ):
            raise RunnerError("finding_gate is malformed")
    if "child_environment_isolation" in present and not isinstance(resolved["child_environment_isolation"], bool):
        raise RunnerError("child_environment_isolation must be boolean")
    projected = dict(resolved)
    removed_material: list[dict[str, Any]] = []
    for key in present:
        value_hash = hashlib.sha256(_canonical(resolved[key])).hexdigest()
        projected.pop(key)
        removed_material.append(
            {
                "field": key,
                "value_sha256": value_hash,
                "stable_behavior": "not_consumed_by_stable_4699d27",
                "root_responsibility": "ROOT-IM validates the retained candidate artifact and triage before accepting the lane result",
            }
        )
    projected_bytes = (json.dumps(projected, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    projected_hash = _write_new_json(output_path, projected, data=projected_bytes)
    record = {
        "schema": "stable-compatible-invocation-projection/v1",
        "stable_runner_commit": proof["commit"],
        "source_invocation": str(input_path.resolve(strict=False)),
        "source_invocation_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "projected_invocation": str(output_path.resolve(strict=False)),
        "projected_invocation_sha256": projected_hash,
        "removed_candidate_only_fields": removed_material,
        "unknown_fields": [],
        "projection_is_deterministic": True,
        "root_must_validate_before_acceptance": True,
        "workflow_role": workflow_role,
        "launch_profile": resolved.get("codex", resolved.get("model_settings", {})).get("launch_profile"),
        "fallback_history_sha256": fallback_history_sha256,
    }
    _write_new_json(record_path, record)
    return record


def _write_proof(path: Path | None, proof: Mapping[str, Any]) -> None:
    stable_root = Path(str(proof["stable_root"])).resolve(strict=True)
    _reject_inside_stable(path, stable_root, "proof file")
    if path is not None:
        _write_new_json(path, proof)
    print(
        "STABLE_RUNNER_PROOF " + json.dumps(dict(proof), sort_keys=True),
        file=sys.stderr,
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the pinned stable implementation harness")
    parser.add_argument("--module", choices=sorted(ALLOWED_MODULES))
    parser.add_argument("--proof-file", type=Path)
    parser.add_argument("--project-invocation", type=Path)
    parser.add_argument("--projection-output", type=Path)
    parser.add_argument("--projection-record", type=Path)
    parser.add_argument("--workflow-role")
    parser.add_argument("--launch-profile")
    parser.add_argument("--fallback-history", type=Path)
    parser.add_argument("--classify-backend-error-file", type=Path)
    return parser


def _dispatch_resolved_invocation(
    entry: Any,
    argv: Sequence[str],
    resolved_invocation: Mapping[str, Any],
) -> Any:
    """Dispatch through a temporary invocation resolved from the current role mapping."""
    with tempfile.TemporaryDirectory(prefix="stable-runner-dispatch-") as temporary_root:
        dispatch_path = Path(temporary_root) / "invocation.json"
        dispatch_path.write_text(
            json.dumps(resolved_invocation, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        resolved_argv = list(argv)
        resolved_argv[0] = str(dispatch_path)
        with _codex_bounded_test_overlay(resolved_invocation):
            return entry(resolved_argv)


def _is_real_codex_invocation(invocation: Mapping[str, Any]) -> bool:
    settings = invocation.get("codex", invocation.get("codex_settings"))
    if not isinstance(settings, Mapping):
        return False
    command = settings.get("command", invocation.get("codex_command", ["codex"]))
    if not isinstance(command, list) or not command:
        return False
    return Path(str(command[0])).name.casefold() in {"codex", "codex.exe"}


def _bounded_overlay_hooks() -> dict[str, list[dict[str, Any]]]:
    adapter = ROOT / ".codex" / "scripts" / "bounded_test_adapter.py"
    command = subprocess.list2cmdline([sys.executable, str(adapter)])
    return {
        "SessionStart": [
            {
                "matcher": "startup|resume|clear|compact",
                "hooks": [
                    {
                        "type": "command",
                        "command": f"{command} session-start",
                        "commandWindows": f"{command} session-start",
                        "timeout": 60,
                        "additionalContextLimit": 2000,
                        "statusMessage": "Loading bounded-test enforcement",
                    }
                ],
            }
        ],
        "PreToolUse": [
            {
                "matcher": "^(Bash|shell_command)$",
                "hooks": [
                    {
                        "type": "command",
                        "command": f"{command} pre-tool-use",
                        "commandWindows": f"{command} pre-tool-use",
                        "timeout": 60,
                        "statusMessage": "Enforcing bounded-test execution",
                    }
                ],
            }
        ],
    }


def _write_atomic(path: Path, data: bytes) -> None:
    temporary = path.with_name(f".{path.name}.{os.getpid()}.{time.time_ns()}.tmp")
    try:
        temporary.write_bytes(data)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _ensure_runtime_hook_git_exclusion(run_root: Path) -> Path:
    """Persist the temporary hook exclusion where sanitized Git reads it."""
    completed = subprocess.run(
        ["git", "-C", str(run_root), "rev-parse", "--git-path", "info/exclude"],
        check=False,
        capture_output=True,
        text=True,
        timeout=15,
    )
    raw_path = completed.stdout.strip()
    if completed.returncode != 0 or not raw_path or "\n" in raw_path or "\r" in raw_path:
        detail = completed.stderr.strip() or "Git returned no repository-local exclude path"
        raise RunnerError(f"cannot locate Git exclude file for temporary Codex hook: {detail}")
    exclude_path = Path(raw_path)
    if not exclude_path.is_absolute():
        exclude_path = run_root / exclude_path
    exclude_path = exclude_path.resolve(strict=False)
    pattern = b"/.codex/hooks.json"
    try:
        exclude_path.parent.mkdir(parents=True, exist_ok=True)
        existing = exclude_path.read_bytes() if exclude_path.is_file() else b""
        if pattern not in {line.rstrip(b"\r") for line in existing.splitlines()}:
            with exclude_path.open("ab") as stream:
                if existing and not existing.endswith((b"\n", b"\r")):
                    stream.write(b"\n")
                stream.write(pattern + b"\n")
                stream.flush()
                os.fsync(stream.fileno())
        verified = exclude_path.read_bytes()
    except OSError as exc:
        raise RunnerError(f"cannot persist Git exclusion for temporary Codex hook: {exc}") from exc
    if pattern not in {line.rstrip(b"\r") for line in verified.splitlines()}:
        raise RunnerError("could not verify Git exclusion for temporary Codex hook")
    return exclude_path


def _merged_bounded_hooks(original: bytes | None) -> bytes:
    if original is None:
        value: dict[str, Any] = {
            "description": "Runtime hooks for the current ROOT-managed subagent session.",
            "hooks": {},
        }
    else:
        try:
            loaded = json.loads(original.decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RunnerError(f"cannot merge existing Codex hooks: {exc}") from exc
        if not isinstance(loaded, dict):
            raise RunnerError("existing Codex hooks must be a JSON object")
        value = loaded
    hooks = value.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise RunnerError("existing Codex hooks.hooks must be an object")
    for event, additions in _bounded_overlay_hooks().items():
        existing = hooks.setdefault(event, [])
        if not isinstance(existing, list):
            raise RunnerError(f"existing Codex hooks.{event} must be a list")
        existing.extend(additions)
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


@contextmanager
def _codex_bounded_test_overlay(invocation: Mapping[str, Any]) -> Iterator[None]:
    """Merge ROOT-side current-run enforcement, then restore exact original bytes."""
    if not _is_real_codex_invocation(invocation):
        yield
        return
    run_root_value = invocation.get("run_root")
    if not isinstance(run_root_value, str) or not run_root_value:
        raise RunnerError("real Codex dispatch requires run_root for bounded-test enforcement")
    run_root = Path(run_root_value).resolve(strict=True)
    _ensure_runtime_hook_git_exclusion(run_root)
    codex_directory = run_root / ".codex"
    hooks_path = codex_directory / "hooks.json"
    codex_directory_preexisted = codex_directory.exists()
    codex_directory.mkdir(parents=True, exist_ok=True)
    original = hooks_path.read_bytes() if hooks_path.is_file() else None
    overlay_bytes = _merged_bounded_hooks(original)
    _write_atomic(hooks_path, overlay_bytes)
    if hooks_path.read_bytes() != overlay_bytes:
        _write_atomic(hooks_path, overlay_bytes)
    if hooks_path.read_bytes() != overlay_bytes:
        if original is None:
            hooks_path.unlink(missing_ok=True)
        else:
            _write_atomic(hooks_path, original)
        raise RunnerError("could not establish bounded-test hooks for Codex subagent")

    existing_count = os.environ.get("GIT_CONFIG_COUNT", "0")
    try:
        config_index = int(existing_count)
    except ValueError as exc:
        hooks_path.unlink(missing_ok=True)
        raise RunnerError("GIT_CONFIG_COUNT is not an integer") from exc

    with tempfile.TemporaryDirectory(prefix="bounded-test-git-exclude-") as temporary:
        exclude_path = Path(temporary) / "exclude"
        exclude_path.write_text("/.codex/hooks.json\n", encoding="utf-8")
        environment_updates = {
            "GIT_CONFIG_COUNT": str(config_index + 1),
            f"GIT_CONFIG_KEY_{config_index}": "core.excludesFile",
            f"GIT_CONFIG_VALUE_{config_index}": str(exclude_path),
        }
        prior = {key: os.environ.get(key) for key in environment_updates}
        os.environ.update(environment_updates)
        try:
            yield
        finally:
            for key, value in prior.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value
            if original is None:
                hooks_path.unlink(missing_ok=True)
                if hooks_path.exists():
                    hooks_path.unlink(missing_ok=True)
                if hooks_path.exists():
                    raise RunnerError("could not remove ROOT-side bounded-test hook overlay")
            else:
                _write_atomic(hooks_path, original)
                if hooks_path.read_bytes() != original:
                    _write_atomic(hooks_path, original)
                if hooks_path.read_bytes() != original:
                    raise RunnerError("could not restore original Codex hook configuration")
            if not codex_directory_preexisted:
                try:
                    codex_directory.rmdir()
                except OSError:
                    pass


def _require_bounded_test_prompt(invocation: Mapping[str, Any]) -> None:
    """Reject a real Codex subagent prompt that omits the bounded-test contract."""
    if not _is_real_codex_invocation(invocation):
        return
    prompt_value = invocation.get("prompt_path")
    if not isinstance(prompt_value, str) or not prompt_value:
        raise RunnerError("Codex subagent invocation requires prompt_path")
    try:
        prompt = Path(prompt_value).read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise RunnerError(f"cannot read Codex subagent prompt: {exc}") from exc
    required = ("BOUNDED-TEST-v1", "Invoke-BoundedTest.ps1")
    missing = [marker for marker in required if marker not in prompt]
    if missing:
        raise RunnerError("Codex subagent prompt omits the mandatory bounded-test contract: " + ", ".join(missing))


def main(argv: Sequence[str] | None = None) -> int:
    args, remainder = _parser().parse_known_args(argv)
    if remainder[:1] == ["--"]:
        remainder = remainder[1:]
    try:
        if args.classify_backend_error_file is not None:
            if (
                any(
                    value is not None
                    for value in (
                        args.module,
                        args.project_invocation,
                        args.workflow_role,
                        args.launch_profile,
                        args.fallback_history,
                    )
                )
                or remainder
            ):
                raise RunnerError("backend-error classification cannot carry a dispatch or profile option")
            try:
                error_bytes = args.classify_backend_error_file.read_bytes()
                error_text = error_bytes.decode("utf-8", errors="replace")
            except OSError as exc:
                raise RunnerError(f"cannot read backend-error input: {exc}") from exc
            print(
                json.dumps(
                    {
                        "backend_error_class": classify_backend_error(error_text),
                        "error_sha256": hashlib.sha256(error_bytes).hexdigest(),
                    },
                    sort_keys=True,
                )
            )
            return 0
        proof = validate_checkout()
        _reject_inside_stable(
            args.proof_file,
            Path(str(proof["stable_root"])).resolve(strict=True),
            "proof file",
        )
        fallback_history: Mapping[str, Any] | None = None
        fallback_history_sha256: str | None = None
        if args.fallback_history is not None:
            fallback_history, fallback_history_sha256 = _read_backend_failure_history(args.fallback_history)
        if args.project_invocation is not None:
            if args.module is not None or remainder:
                raise RunnerError("projection mode cannot carry a module command")
            if args.workflow_role is None:
                raise RunnerError("--workflow-role is required for invocation projection")
            output = args.projection_output or args.project_invocation.with_name("STABLE_COMPATIBLE_INVOCATION.json")
            record = args.projection_record or args.project_invocation.with_name("STABLE_COMPATIBLE_PROJECTION.json")
            result = project_invocation(
                input_path=args.project_invocation,
                output_path=output,
                record_path=record,
                proof=proof,
                workflow_role=args.workflow_role,
                launch_profile=args.launch_profile,
                fallback_history=fallback_history,
                fallback_history_sha256=fallback_history_sha256,
            )
            _write_proof(
                args.proof_file,
                {
                    **proof,
                    "operation": "project_invocation",
                    "projection_record": result,
                },
            )
            print(json.dumps(result, sort_keys=True))
            return 0
        if args.module is None:
            raise RunnerError("--module is required unless --project-invocation is used")
        dispatch_invocation: dict[str, Any] | None = None
        if args.module == "orchestrator_harness.lane_controller":
            if args.workflow_role is None:
                raise RunnerError("--workflow-role is required for lane-controller dispatch")
            if not remainder:
                raise RunnerError("lane-controller dispatch requires an invocation path")
            try:
                raw_dispatch_invocation = json.loads(Path(remainder[0]).read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise RunnerError(f"cannot read dispatch invocation for role resolution: {exc}") from exc
            if not isinstance(raw_dispatch_invocation, dict):
                raise RunnerError("dispatch invocation must be a JSON object")
            dispatch_invocation = apply_workflow_role_allocation(
                raw_dispatch_invocation,
                args.workflow_role,
                validate_finding_gate=False,
                launch_profile=args.launch_profile,
                fallback_history=fallback_history,
            )
            _require_bounded_test_prompt(dispatch_invocation)
        module, actual = import_stable_module(args.module, proof)
        _write_proof(
            args.proof_file,
            {
                **actual,
                "operation": "module_dispatch",
                "argv": list(remainder),
                **(
                    {
                        "workflow_role": args.workflow_role,
                        "launch_profile": dispatch_invocation.get("codex", {}).get("launch_profile"),
                        "fallback_history_sha256": fallback_history_sha256,
                    }
                    if dispatch_invocation is not None
                    else {}
                ),
            },
        )
        entry = getattr(module, "main", None)
        if not callable(entry):
            raise RunnerError(f"stable module has no callable main: {args.module}")
        if dispatch_invocation is None:
            result = entry(list(remainder))
        else:
            result = _dispatch_resolved_invocation(entry, remainder, dispatch_invocation)
        if result is None:
            return 0
        if isinstance(result, int):
            return result
        raise RunnerError(f"stable module returned unsupported result type: {type(result).__name__}")
    except (RunnerError, OSError, ValueError) as exc:
        print(f"stable runner refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
