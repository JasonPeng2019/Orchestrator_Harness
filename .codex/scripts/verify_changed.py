from __future__ import annotations

import ast
import os
import subprocess
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = ROOT / "stable-general-harness-runner"
DEV_ROOT = ROOT / ".codex" / "dev"
FULL_VERIFY = ROOT / ".codex" / "scripts" / "verify.py"
FIRMWARE_MCP_ROOT = ("Firmware", "BYO-Firmware-MCP")
DESIGN_TOPOLOGY_SCRIPT_ROOT = (
    ".codex",
    "skills",
    "design-project-topology",
    "scripts",
)
DESIGN_TOPOLOGY_VALIDATOR = Path(*DESIGN_TOPOLOGY_SCRIPT_ROOT) / "validate_execution_plan.py"
SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from dev_state import (
    SnapshotError,
    VerificationDelta,
    record_verified_snapshot,
    repository_manifest,
    verification_delta,
    verification_is_current,
)

PYTHON_ROOTS = (
    (".codex", "scripts"),
    (".codex", "tests"),
    DESIGN_TOPOLOGY_SCRIPT_ROOT,
    ("Firmware", "BYO-Firmware-MCP"),
    ("Firmware", ".codex", "skills", "run-firmware-test-suite", "scripts"),
    ("Firmware", ".codex", "skills", "run-firmware-test-suite", "tests"),
    ("Firmware", "scripts", "orchestration"),
    ("stable-general-harness-runner", "harness_common"),
    ("stable-general-harness-runner", "harness_watcher_implementation"),
    ("stable-general-harness-runner", "orchestrator_harness"),
)
MAX_TARGETED_UNITTEST_MODULES = 14
BOUNDED_SUPERVISOR_SCRIPT = Path(".codex/scripts/Invoke-BoundedTest.ps1")
BOUNDED_SUPERVISOR_REGRESSION = Path(".codex/tests/test_bounded_test_supervisor.py")


@dataclass(frozen=True)
class Check:
    label: str
    argv: tuple[str, ...]
    cwd: Path
    env_overrides: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class VerificationPlan:
    checks: tuple[Check, ...] = ()
    full_fallback_reason: str | None = None


def plan_changed_verification(root: Path, delta: VerificationDelta) -> VerificationPlan:
    changed = delta.changed_paths
    unsupported = [path for path in changed if not _has_targeted_route(path)]
    if unsupported:
        listed = ", ".join(path.as_posix() for path in unsupported[:5])
        return VerificationPlan(full_fallback_reason=f"no targeted route for: {listed}")

    firmware_mcp_paths = [path for path in changed if _is_firmware_mcp_path(path)]
    existing = [
        path
        for path in changed
        if path.suffix.casefold() == ".py" and not _is_firmware_mcp_path(path) and (root / path).is_file()
    ]
    checks: list[Check] = []
    relative_arguments = tuple(path.as_posix() for path in existing)
    if relative_arguments:
        checks.append(
            Check(
                "ruff changed Python",
                (
                    "ruff",
                    "check",
                    "--config",
                    str(DEV_ROOT / "pyproject.toml"),
                    "--no-cache",
                    *relative_arguments,
                ),
                root,
            )
        )
        format_arguments = tuple(
            path.as_posix()
            for path in existing
            if path.parts[:2] in {(".codex", "scripts"), (".codex", "tests")}
            or path.parts[: len(DESIGN_TOPOLOGY_SCRIPT_ROOT)] == DESIGN_TOPOLOGY_SCRIPT_ROOT
        )
        if format_arguments:
            checks.append(
                Check(
                    "format changed development Python",
                    (
                        "ruff",
                        "format",
                        "--config",
                        str(DEV_ROOT / "pyproject.toml"),
                        "--no-cache",
                        "--check",
                        *format_arguments,
                    ),
                    root,
                )
            )
        checks.extend(
            (
                Check(
                    "types changed Python",
                    (
                        "basedpyright",
                        "--project",
                        str(root / "pyrightconfig.json"),
                        *relative_arguments,
                    ),
                    root,
                ),
                Check(
                    "compile changed Python",
                    (sys.executable, "-m", "py_compile", *relative_arguments),
                    root,
                ),
            )
        )

    checks.extend(_firmware_mcp_checks(root, firmware_mcp_paths))
    checks.extend(_firmware_change_loop_checks(root, changed))
    checks.extend(_design_topology_checks(root, changed))
    checks.extend(_test_checks(root, delta))
    if not checks:
        return VerificationPlan(full_fallback_reason="changed code produced no targeted checks")
    return VerificationPlan(checks=tuple(_deduplicate_checks(checks)))


def _firmware_mcp_checks(root: Path, changed: list[Path]) -> list[Check]:
    if not changed:
        return []
    package_root = root.joinpath(*FIRMWARE_MCP_ROOT)
    project_python = package_root / ".venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    package_environment = (("VIRTUAL_ENV", str(package_root / ".venv")),)
    return [
        Check(
            "Firmware MCP Ruff",
            (str(project_python), "-m", "ruff", "check", "."),
            package_root,
            package_environment,
        ),
        Check(
            "Firmware MCP Pyright",
            (str(project_python), "-m", "pyright", "--pythonpath", str(project_python)),
            package_root,
            package_environment,
        ),
        Check(
            "Firmware MCP tests",
            (str(project_python), "-m", "pytest"),
            package_root,
            package_environment,
        ),
    ]


def _firmware_change_loop_checks(root: Path, changed: tuple[Path, ...]) -> list[Check]:
    if not any(_is_firmware_change_loop_path(path) or _is_firmware_prompt_policy_path(path) for path in changed):
        return []
    return [
        Check(
            "Firmware change-loop self-check",
            (
                "bash",
                "Firmware/.codex/skills/change-loop/scripts/run_loop.sh",
                "--self-check",
            ),
            root,
        )
    ]


def _design_topology_checks(root: Path, changed: tuple[Path, ...]) -> list[Check]:
    if DESIGN_TOPOLOGY_VALIDATOR not in changed:
        return []
    return [
        Check(
            "design topology validator self-test",
            (sys.executable, DESIGN_TOPOLOGY_VALIDATOR.as_posix(), "--self-test"),
            root,
        )
    ]


def _test_checks(root: Path, delta: VerificationDelta) -> list[Check]:
    changed = set(delta.changed_paths)
    module_paths = _module_paths(delta.manifest)
    imports = {
        module: _imports_for(root / path, module) for module, path in module_paths.items() if (root / path).is_file()
    }
    changed_modules = {module for module, path in module_paths.items() if path in changed}
    changed_modules.update(module for path in changed if (module := _module_for_path(path)) is not None)
    impacted = _reverse_dependency_closure(changed_modules, imports)

    codex_tests: set[Path] = set()
    orchestrator_tests: set[str] = set()
    watcher_tests: set[str] = set()
    deleted_test_domains: set[str] = set()
    for path in changed:
        domain = _test_domain(path)
        if domain is None:
            continue
        if not (root / path).is_file():
            deleted_test_domains.add(domain)
            continue
        if domain == "codex":
            codex_tests.add(path)
        else:
            module = _module_for_path(path)
            if module is not None:
                (orchestrator_tests if domain == "orchestrator" else watcher_tests).add(module)

    for module in impacted:
        path = module_paths.get(module)
        if path is None:
            continue
        domain = _test_domain(path)
        if domain == "codex":
            codex_tests.add(path)
        elif domain == "orchestrator":
            orchestrator_tests.add(module)
        elif domain == "watcher":
            watcher_tests.add(module)

    changed_domains = {_source_domain(path) for path in changed}
    checks: list[Check] = []
    if "codex" in changed_domains:
        if BOUNDED_SUPERVISOR_SCRIPT in changed:
            codex_tests.add(BOUNDED_SUPERVISOR_REGRESSION)
        if "codex" in deleted_test_domains or not codex_tests:
            codex_tests = {Path(".codex/tests")}
        checks.append(
            Check(
                "Codex changed tests",
                (
                    sys.executable,
                    "-m",
                    "pytest",
                    "-p",
                    "no:cacheprovider",
                    "-q",
                    *(path.as_posix() for path in sorted(codex_tests)),
                ),
                root,
            )
        )

    if "orchestrator" in changed_domains or "common" in changed_domains:
        checks.append(
            _unittest_check(
                "orchestrator changed tests",
                orchestrator_tests,
                "orchestrator_harness/tests",
            )
        )
    if "watcher" in changed_domains or "common" in changed_domains:
        checks.append(
            _unittest_check(
                "watcher changed tests",
                watcher_tests,
                "harness_watcher_implementation/tests",
            )
        )
    if "firmware" in changed_domains:
        checks.append(
            Check(
                "firmware changed tests",
                (
                    sys.executable,
                    "-m",
                    "unittest",
                    "discover",
                    "-s",
                    "Firmware/.codex/skills/run-firmware-test-suite/tests",
                ),
                root,
            )
        )
    return checks


def _unittest_check(label: str, modules: set[str], test_root: str) -> Check:
    if not modules or len(modules) > MAX_TARGETED_UNITTEST_MODULES:
        return Check(
            label,
            (sys.executable, "-m", "unittest", "discover", "-s", test_root, "-t", "."),
            SOURCE_ROOT,
        )
    selected = tuple(sorted(modules))
    return Check(label, (sys.executable, "-m", "unittest", *selected), SOURCE_ROOT)


def _module_paths(manifest: dict[str, str]) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for raw in manifest:
        path = Path(raw)
        if path.suffix.casefold() != ".py":
            continue
        module = _module_for_path(path)
        if module is not None:
            result[module] = path
    return result


def _module_for_path(path: Path) -> str | None:
    parts = path.parts
    if parts[:2] == (".codex", "scripts") and len(parts) == 3:
        return path.stem
    if parts[:2] == (".codex", "tests") and len(parts) == 3:
        return f"_codex_tests.{path.stem}"
    if parts and parts[0] == "stable-general-harness-runner" and len(parts) >= 3:
        module_parts = list(parts[1:])
        module_parts[-1] = Path(module_parts[-1]).stem
        if module_parts[-1] == "__init__":
            module_parts.pop()
        return ".".join(module_parts) if module_parts else None
    return None


def _imports_for(path: Path, module: str) -> set[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, UnicodeError):
        return set()
    imports: set[str] = set()
    package = module if path.name == "__init__.py" else module.rpartition(".")[0]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            base = _resolve_import(package, node.level, node.module)
            if base:
                imports.add(base)
                imports.update(f"{base}.{alias.name}" for alias in node.names if alias.name != "*")
    return imports


def _resolve_import(package: str, level: int, imported: str | None) -> str:
    if level == 0:
        return imported or ""
    parts = package.split(".") if package else []
    keep = max(0, len(parts) - (level - 1))
    base = parts[:keep]
    if imported:
        base.extend(imported.split("."))
    return ".".join(base)


def _reverse_dependency_closure(changed: set[str], imports: dict[str, set[str]]) -> set[str]:
    impacted = set(changed)
    progress = True
    while progress:
        progress = False
        for module, dependencies in imports.items():
            if module in impacted:
                continue
            if any(_modules_overlap(dependency, candidate) for dependency in dependencies for candidate in impacted):
                impacted.add(module)
                progress = True
    return impacted


def _modules_overlap(left: str, right: str) -> bool:
    return left == right or left.startswith(f"{right}.") or right.startswith(f"{left}.")


def _test_domain(path: Path) -> str | None:
    parts = path.parts
    if parts[:2] == (".codex", "tests"):
        return "codex"
    if parts[:3] == ("stable-general-harness-runner", "orchestrator_harness", "tests"):
        return "orchestrator"
    if parts[:3] == (
        "stable-general-harness-runner",
        "harness_watcher_implementation",
        "tests",
    ):
        return "watcher"
    return None


def _source_domain(path: Path) -> str:
    parts = path.parts
    if parts[:2] in {(".codex", "scripts"), (".codex", "tests")}:
        return "codex"
    if parts[:5] == (
        "Firmware",
        ".codex",
        "skills",
        "run-firmware-test-suite",
        "scripts",
    ) or parts[:5] == (
        "Firmware",
        ".codex",
        "skills",
        "run-firmware-test-suite",
        "tests",
    ):
        return "firmware"
    if parts[:3] == ("Firmware", "scripts", "orchestration"):
        return "firmware"
    if parts[:2] == ("stable-general-harness-runner", "orchestrator_harness"):
        return "orchestrator"
    if parts[:2] == ("stable-general-harness-runner", "harness_watcher_implementation"):
        return "watcher"
    if parts[:2] == ("stable-general-harness-runner", "harness_common"):
        return "common"
    return "unknown"


def _under_python_root(path: Path) -> bool:
    return any(path.parts[: len(prefix)] == prefix for prefix in PYTHON_ROOTS)


def _has_targeted_route(path: Path) -> bool:
    return (
        (path.suffix.casefold() == ".py" and _under_python_root(path))
        or _is_firmware_change_loop_path(path)
        or path == BOUNDED_SUPERVISOR_SCRIPT
    )


def _is_firmware_change_loop_path(path: Path) -> bool:
    return (
        path.parts[:5] == ("Firmware", ".codex", "skills", "change-loop", "scripts") and path.suffix.casefold() == ".sh"
    )


def _is_firmware_prompt_policy_path(path: Path) -> bool:
    return path.parts == ("Firmware", "scripts", "orchestration", "prompt_policy.py")


def _is_firmware_mcp_path(path: Path) -> bool:
    return path.parts[: len(FIRMWARE_MCP_ROOT)] == FIRMWARE_MCP_ROOT


def _deduplicate_checks(checks: Iterable[Check]) -> list[Check]:
    result: list[Check] = []
    seen: set[tuple[tuple[str, ...], Path, tuple[tuple[str, str], ...]]] = set()
    for check in checks:
        identity = (check.argv, check.cwd, check.env_overrides)
        if identity not in seen:
            seen.add(identity)
            result.append(check)
    return result


def run_changed_verification(root: Path = ROOT) -> int:
    delta = verification_delta(root)
    if delta is None:
        return _run_full_fallback(root, "missing, obsolete, or unreadable verification manifest")
    if not delta.changed_paths:
        print("VERIFY_CHANGED: SKIP (no code changes)")
        return 0
    plan = plan_changed_verification(root, delta)
    if plan.full_fallback_reason is not None:
        print(
            f"VERIFY_CHANGED: FAIL ({plan.full_fallback_reason}; add a targeted verification route before finishing)",
            file=sys.stderr,
        )
        return 1

    for check in plan.checks:
        print(f"\n== {check.label} ==", flush=True)
        env = None
        if check.env_overrides:
            env = os.environ.copy()
            env.update(check.env_overrides)
        result = subprocess.run(check.argv, cwd=check.cwd, env=env, check=False)
        if result.returncode != 0:
            print(f"\nVERIFY_CHANGED: FAIL ({check.label})", file=sys.stderr)
            return result.returncode
    try:
        final_manifest = repository_manifest(root)
    except SnapshotError as exc:
        print(f"VERIFY_CHANGED: FAIL ({exc})", file=sys.stderr)
        return 1
    if final_manifest != delta.manifest:
        print("VERIFY_CHANGED: FAIL (code changed during verification)", file=sys.stderr)
        return 1
    record_verified_snapshot(
        root,
        mode="changed",
        routes=(check.label for check in plan.checks),
        manifest=final_manifest,
    )
    print(f"\nVERIFY_CHANGED: PASS ({len(delta.changed_paths)} changed code path(s))")
    return 0


def _run_full_fallback(root: Path, reason: str) -> int:
    print(f"VERIFY_CHANGED: full fallback ({reason})", flush=True)
    result = subprocess.run([sys.executable, str(FULL_VERIFY)], cwd=root, check=False)
    if result.returncode != 0:
        print("VERIFY_CHANGED: FAIL (full fallback)", file=sys.stderr)
        return result.returncode
    if not verification_is_current(root):
        print(
            "VERIFY_CHANGED: FAIL (full fallback did not record the current code state)",
            file=sys.stderr,
        )
        return 1
    print("VERIFY_CHANGED: PASS (full fallback)")
    return 0


def main() -> int:
    return run_changed_verification()


if __name__ == "__main__":
    raise SystemExit(main())
