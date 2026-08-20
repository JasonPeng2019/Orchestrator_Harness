"""Invoke the selected package-local target's lane controller in this provider-session process."""

from __future__ import annotations

# pyright: reportMissingImports=false
# The controller API is supplied by the selected disposable target worktree.

import os
import sys
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[2]


def resolve_target_root(value: str | None = None) -> Path:
    """Resolve the package-local WIP target, with an optional disposable override."""

    raw = value if value is not None else os.environ.get("FIRMWARE_TARGET_HARNESS")
    target = Path(raw).expanduser() if raw else PACKAGE_ROOT / "target-harness"
    if not target.is_absolute():
        target = PACKAGE_ROOT / target
    return target.resolve(strict=False)


def main() -> int:
    target = resolve_target_root()
    if not target.is_dir():
        raise SystemExit(f"target harness is unavailable: {target}")
    sys.path.insert(0, str(target))
    from orchestrator_harness.lane_controller import main as lane_controller_main

    return lane_controller_main()


if __name__ == "__main__":
    raise SystemExit(main())
