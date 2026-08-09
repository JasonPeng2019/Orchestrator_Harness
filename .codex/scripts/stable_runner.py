"""Fail-closed entry point for the immutable implementation runner.

This file is intentionally outside both harness checkouts.  It validates the detached
stable checkout before importing any harness code, removes ambient Python import inputs,
and then delegates only to the stable CLI/controller entry points.  The projection helper
is the explicit compatibility boundary for candidate-only coding fields.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import subprocess
import sys
import sysconfig
from collections.abc import Mapping, Sequence
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


def project_invocation(
    *, input_path: Path, output_path: Path, record_path: Path, proof: Mapping[str, Any]
) -> dict[str, Any]:
    """Create an explicit stable-compatible artifact and hash-bound projection record."""
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
    allowed, removable = _projection_allowed_fields(raw)
    unknown = set(raw) - allowed - removable
    if unknown:
        raise RunnerError("projection refuses unknown fields: " + ", ".join(sorted(unknown)))
    present = sorted(set(raw) & removable)
    if raw.get("schema") is None and present:
        raise RunnerError("candidate-only coding fields cannot appear on a schema-less firmware route")
    if "finding_gate" in present:
        gate = raw["finding_gate"]
        if not isinstance(gate, dict) or set(gate) != {"role", "path"}:
            raise RunnerError("finding_gate must retain its closed role/path shape")
        if (
            gate["role"] not in {"reviewer", "test_writer", "test_executor"}
            or not isinstance(gate["path"], str)
            or not gate["path"]
        ):
            raise RunnerError("finding_gate is malformed")
    if "child_environment_isolation" in present and not isinstance(raw["child_environment_isolation"], bool):
        raise RunnerError("child_environment_isolation must be boolean")
    projected = dict(raw)
    removed_material: list[dict[str, Any]] = []
    for key in present:
        value_hash = hashlib.sha256(_canonical(raw[key])).hexdigest()
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
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args, remainder = _parser().parse_known_args(argv)
    if remainder[:1] == ["--"]:
        remainder = remainder[1:]
    try:
        proof = validate_checkout()
        _reject_inside_stable(
            args.proof_file,
            Path(str(proof["stable_root"])).resolve(strict=True),
            "proof file",
        )
        if args.project_invocation is not None:
            if args.module is not None or remainder:
                raise RunnerError("projection mode cannot carry a module command")
            output = args.projection_output or args.project_invocation.with_name("STABLE_COMPATIBLE_INVOCATION.json")
            record = args.projection_record or args.project_invocation.with_name("STABLE_COMPATIBLE_PROJECTION.json")
            result = project_invocation(
                input_path=args.project_invocation,
                output_path=output,
                record_path=record,
                proof=proof,
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
        module, actual = import_stable_module(args.module, proof)
        _write_proof(
            args.proof_file,
            {**actual, "operation": "module_dispatch", "argv": list(remainder)},
        )
        entry = getattr(module, "main", None)
        if not callable(entry):
            raise RunnerError(f"stable module has no callable main: {args.module}")
        result = entry(list(remainder))
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
