from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

STATE_PATH = Path(".codex/state/verified.json")
SKIP_PARTS = {
    ".git",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "references",
    "runtime",
}
SKIP_FILES = {"HANDOFF.md", "PLAN.md"}


def repository_snapshot(root: Path) -> str:
    hasher = hashlib.sha256()
    for relative in _repository_files(root):
        path = root / relative
        hasher.update(relative.as_posix().encode("utf-8"))
        hasher.update(b"\0")
        try:
            hasher.update(path.read_bytes())
        except OSError:
            hasher.update(b"<unreadable>")
        hasher.update(b"\0")
    return hasher.hexdigest()


def record_verified_snapshot(root: Path) -> None:
    path = root / STATE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    value = {
        "snapshot": repository_snapshot(root),
        "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    }
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def verification_is_current(root: Path) -> bool:
    path = root / STATE_PATH
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return value.get("snapshot") == repository_snapshot(root)


def _repository_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root,
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode == 0:
        candidates = [Path(item) for item in result.stdout.split("\0") if item]
    else:
        candidates = [path.relative_to(root) for path in root.rglob("*") if path.is_file()]
    return sorted(
        relative
        for relative in candidates
        if relative.name not in SKIP_FILES
        and not any(part in SKIP_PARTS for part in relative.parts)
        and relative.parts[:2] != (".codex", "state")
        and relative.parts[:2] != (".codex", "notes")
    )
