"""Resolve one canonical execution role into native harness bootstrap argv.

The resolver is deliberately side-effect free.  It reads the allocation at the
moment ROOT dispatches a lane, validates the selected launch configuration with
the frozen harness adapter, and prints only arguments accepted by
``operator_launch lane bootstrap``.  It never launches a provider or chooses a
fallback automatically.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any


class ResolveRoleError(ValueError):
    """The requested role cannot be projected into a native launch binding."""


def _positive_integer(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def _read_mapping(path: Path) -> dict[str, Any]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ResolveRoleError(f"cannot read mapping {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ResolveRoleError("mapping root must be an object")
    if raw.get("schema_version") != 1:
        raise ResolveRoleError("mapping schema_version must be 1")
    if not isinstance(raw.get("roles"), dict) or not raw["roles"]:
        raise ResolveRoleError("mapping roles must be a non-empty object")
    return raw


def _selected_allocation(
    mapping: dict[str, Any], role: str, fallback_index: int | None
) -> dict[str, Any]:
    if not isinstance(role, str) or not role or role.strip() != role:
        raise ResolveRoleError("role must be a non-empty exact name")
    roles = mapping["roles"]
    if role not in roles:
        raise ResolveRoleError(f"unrecognized role: {role}")
    preferred = roles[role]
    if not isinstance(preferred, dict) or not preferred:
        raise ResolveRoleError(f"role {role} has an empty allocation")
    if role == "root" or preferred.get("launch") is False:
        raise ResolveRoleError(f"role {role} is not a worker launch target")
    if fallback_index is None:
        return preferred

    policy = preferred.get("fallback_policy")
    if not isinstance(policy, dict):
        raise ResolveRoleError(f"role {role} has no fallback policy")
    fallbacks = policy.get("fallbacks")
    if not isinstance(fallbacks, list) or not fallbacks:
        raise ResolveRoleError(f"role {role} has no configured fallbacks")
    if fallback_index > len(fallbacks):
        raise ResolveRoleError(
            f"role {role} fallback index {fallback_index} is out of range"
        )
    selected = fallbacks[fallback_index - 1]
    if not isinstance(selected, dict) or not selected:
        raise ResolveRoleError(
            f"role {role} fallback index {fallback_index} is empty"
        )
    return selected


def _exact_nonempty_string(allocation: dict[str, Any], key: str, role: str) -> str:
    value = allocation.get(key)
    if not isinstance(value, str) or not value or value.strip() != value:
        raise ResolveRoleError(f"role {role} {key} must be a non-empty exact string")
    return value


def _load_adapter(harness_root: Path, provider: str) -> ModuleType:
    if Path(provider).name != provider or any(separator in provider for separator in ("/", "\\")):
        raise ResolveRoleError(f"invalid provider id: {provider}")
    binding_path = (
        harness_root
        / "orchestrator_harness"
        / "provider_adapters"
        / provider
        / "launcher_binding.py"
    )
    if not binding_path.is_file():
        raise ResolveRoleError(
            f"launcher binding missing for provider {provider}: {binding_path}"
        )
    module_name = f"role_resolver_{provider.replace('-', '_')}"
    spec = importlib.util.spec_from_file_location(module_name, binding_path)
    if spec is None or spec.loader is None:
        raise ResolveRoleError(f"cannot load launcher binding: {binding_path}")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise ResolveRoleError(
            f"cannot load launcher binding for provider {provider}: {exc}"
        ) from exc
    if getattr(module, "PROVIDER_ID", None) != provider:
        raise ResolveRoleError(
            f"launcher binding identity does not match provider {provider}"
        )
    return module


def resolve_role_argv(
    *,
    mapping_path: Path,
    harness_root: Path,
    role: str,
    fallback_index: int | None = None,
) -> list[str]:
    """Return the provider/model/options fragment for native lane bootstrap."""
    mapping = _read_mapping(mapping_path)
    allocation = _selected_allocation(mapping, role, fallback_index)
    provider = _exact_nonempty_string(allocation, "provider", role)
    _exact_nonempty_string(allocation, "cli", role)
    model = _exact_nonempty_string(allocation, "model", role)
    launch_config = allocation.get("launch_config")
    if not isinstance(launch_config, dict):
        raise ResolveRoleError(f"role {role} launch_config must be an object")

    adapter = _load_adapter(harness_root, provider)
    validate = getattr(adapter, "validate_launch_config", None)
    if not callable(validate):
        raise ResolveRoleError(
            f"launcher binding lacks launch validation for provider {provider}"
        )
    try:
        configured = validate(model=model, launch_config=launch_config)
    except (TypeError, ValueError) as exc:
        raise ResolveRoleError(str(exc)) from exc
    if not isinstance(configured, dict) or not all(
        isinstance(key, str)
        and key
        and isinstance(value, str)
        and value
        for key, value in configured.items()
    ):
        raise ResolveRoleError(
            f"launcher binding returned invalid launch configuration for {provider}"
        )

    argv = ["--provider", provider, "--model", model]
    for key, value in configured.items():
        argv.extend(["--provider-option", f"{key}={value}"])
    return argv


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="project one canonical role into native harness bootstrap argv"
    )
    parser.add_argument("--mapping", required=True, type=Path)
    parser.add_argument("--harness-root", required=True, type=Path)
    parser.add_argument(
        "--fallback-index",
        type=_positive_integer,
        help="explicit one-based fallback selected by ROOT; never chosen automatically",
    )
    parser.add_argument("role")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        resolved = resolve_role_argv(
            mapping_path=args.mapping.resolve(strict=True),
            harness_root=args.harness_root.resolve(strict=True),
            role=args.role,
            fallback_index=args.fallback_index,
        )
    except (OSError, ResolveRoleError) as exc:
        sys.stderr.write(f"resolve-role: error: {exc}\n")
        return 2
    sys.stdout.write(json.dumps(resolved, separators=(",", ":")) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
