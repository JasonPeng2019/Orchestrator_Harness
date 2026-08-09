from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = ROOT / "stable-general-harness-runner"
DEV_ROOT = ROOT / ".codex" / "dev"
SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from dev_state import record_verified_snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description="Run development checks for the portable harness.")
    parser.add_argument(
        "--full",
        action="store_true",
        help="Also run the slower attention retention exercise.",
    )
    args = parser.parse_args()

    commands = [
        (
            "ruff",
            [
                "ruff",
                "check",
                "--config",
                str(DEV_ROOT / "pyproject.toml"),
                "--no-cache",
                "stable-general-harness-runner",
                ".codex/scripts",
                ".codex/tests",
            ],
        ),
        (
            "format",
            [
                "ruff",
                "format",
                "--config",
                str(DEV_ROOT / "pyproject.toml"),
                "--no-cache",
                "--check",
                ".codex/scripts",
                ".codex/tests",
            ],
        ),
        ("types", ["basedpyright", "--project", str(ROOT / "pyrightconfig.json")]),
        (
            "compile",
            [
                sys.executable,
                "-m",
                "compileall",
                "-q",
                "orchestrator_harness",
                "harness_common",
                "harness_watcher_implementation",
            ],
        ),
        (
            "orchestrator tests",
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "orchestrator_harness/tests",
                "-t",
                ".",
            ],
        ),
        (
            "watcher tests",
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "harness_watcher_implementation/tests",
                "-t",
                ".",
            ],
        ),
        (
            "Codex integration tests",
            [
                sys.executable,
                "-m",
                "pytest",
                "-p",
                "no:cacheprovider",
                "-q",
                ".codex/tests",
            ],
        ),
    ]
    if args.full:
        commands.append(
            (
                "attention retention",
                [
                    sys.executable,
                    "harness_watcher_implementation/tests/run_attention_practical.py",
                ],
            )
        )

    for label, command in commands:
        print(f"\n== {label} ==", flush=True)
        root_commands = {"ruff", "format", "types", "Codex integration tests"}
        result = subprocess.run(command, cwd=ROOT if label in root_commands else SOURCE_ROOT, check=False)
        if result.returncode != 0:
            print(f"\nVERIFY: FAIL ({label})", file=sys.stderr)
            return result.returncode

    record_verified_snapshot(ROOT)
    print("\nVERIFY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
