from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

STATE_PATH = Path(".codex/state/verified.json")
STATE_VERSION = 2
VERIFICATION_POLICY = "code-diff-v1"
CODE_SUFFIXES = frozenset(
    {
        ".asm",
        ".bash",
        ".bat",
        ".c",
        ".cc",
        ".cjs",
        ".cmd",
        ".cpp",
        ".cs",
        ".cxx",
        ".fish",
        ".go",
        ".h",
        ".hh",
        ".hpp",
        ".hxx",
        ".inc",
        ".ino",
        ".java",
        ".js",
        ".jsx",
        ".kt",
        ".kts",
        ".lua",
        ".mjs",
        ".php",
        ".ps1",
        ".psm1",
        ".py",
        ".pyi",
        ".rb",
        ".rs",
        ".s",
        ".scala",
        ".sh",
        ".sv",
        ".swift",
        ".ts",
        ".tsx",
        ".v",
        ".vhd",
        ".vhdl",
        ".zsh",
    }
)
SKIP_PARTS = {
    "archive",
    ".git",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "evidence",
    "references",
    "runtime",
}
TOP_LEVEL_VIEW_ONLY_ROOTS = frozenset({"firmware-v2-harness-runner"})


class SnapshotError(RuntimeError):
    """Raised when verification inputs cannot be read consistently."""


@dataclass(frozen=True)
class VerificationDelta:
    manifest: dict[str, str]
    changed_paths: tuple[Path, ...]


def repository_snapshot(root: Path) -> str:
    return _manifest_snapshot(repository_manifest(root))


def repository_manifest(root: Path) -> dict[str, str]:
    manifest: dict[str, str] = {}
    for relative in _repository_files(root):
        path = root / relative
        try:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as exc:
            raise SnapshotError(f"cannot read verification input {relative.as_posix()}: {exc}") from exc
        manifest[relative.as_posix()] = digest
    return manifest


def _manifest_snapshot(manifest: dict[str, str]) -> str:
    hasher = hashlib.sha256()
    for relative, digest in sorted(manifest.items()):
        hasher.update(relative.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(digest.encode("ascii"))
        hasher.update(b"\0")
    return hasher.hexdigest()


def record_verified_snapshot(
    root: Path,
    *,
    mode: str = "full",
    routes: Iterable[str] = (),
    manifest: dict[str, str] | None = None,
) -> None:
    path = root / STATE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    current_manifest = repository_manifest(root) if manifest is None else manifest
    value = {
        "version": STATE_VERSION,
        "policy": VERIFICATION_POLICY,
        "snapshot": _manifest_snapshot(current_manifest),
        "files": dict(sorted(current_manifest.items())),
        "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "mode": mode,
        "routes": sorted(set(routes)),
    }
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def verification_is_current(root: Path) -> bool:
    try:
        value = _read_state(root)
        current = repository_manifest(root)
    except (OSError, json.JSONDecodeError, SnapshotError):
        return False
    previous = value.get("files")
    return (
        value.get("version") == STATE_VERSION
        and value.get("policy") == VERIFICATION_POLICY
        and isinstance(previous, dict)
        and previous == current
        and value.get("snapshot") == _manifest_snapshot(current)
    )


def verification_delta(root: Path) -> VerificationDelta | None:
    """Return the current manifest and changed code paths, or None for an unusable baseline."""

    try:
        value = _read_state(root)
        manifest = repository_manifest(root)
    except (OSError, json.JSONDecodeError, SnapshotError):
        return None
    previous = value.get("files")
    if (
        value.get("version") != STATE_VERSION
        or value.get("policy") != VERIFICATION_POLICY
        or not isinstance(previous, dict)
        or not all(isinstance(path, str) and isinstance(digest, str) for path, digest in previous.items())
    ):
        return None
    previous = {
        path: digest
        for path, digest in previous.items()
        if not _is_linked_worktree_member(root, Path(path)) and not _skip_path(Path(path))
    }
    changed = sorted(path for path in set(previous) | set(manifest) if previous.get(path) != manifest.get(path))
    return VerificationDelta(manifest=manifest, changed_paths=tuple(Path(path) for path in changed))


def _read_state(root: Path) -> dict[str, Any]:
    value: Any = json.loads((root / STATE_PATH).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise json.JSONDecodeError("verification state must be an object", "", 0)
    return value


def _repository_files(root: Path) -> list[Path]:
    candidates: list[Path] = []
    for directory, directory_names, file_names in os.walk(root, topdown=True):
        current = Path(directory)
        relative_directory = current.relative_to(root)
        directory_names[:] = [
            name
            for name in sorted(directory_names)
            if not _skip_path(relative_directory / name) and not _is_linked_worktree(current / name)
        ]
        for name in sorted(file_names):
            relative = relative_directory / name
            if not _skip_path(relative) and relative.suffix.casefold() in CODE_SUFFIXES:
                candidates.append(relative)
    return sorted(candidates)


def _skip_path(relative: Path) -> bool:
    return (
        any(part in SKIP_PARTS for part in relative.parts)
        or bool(relative.parts and relative.parts[0] in TOP_LEVEL_VIEW_ONLY_ROOTS)
        or relative.parts[:2] == ("Firmware", "fresh-experiments")
        or relative.parts[:3] == ("Firmware", ".agent-workspace", "epochs")
        or relative.parts[:1] == ("harness-single-worktrees",)
        or relative.parts[:1] == ("scratch",)
        or relative.parts[:2] == (".codex", "state")
        or relative.parts[:2] == (".codex", "notes")
    )


def _is_linked_worktree(path: Path) -> bool:
    """Return whether *path* is a Git linked worktree owned outside this checkout."""

    return (path / ".git").is_file()


def _is_linked_worktree_member(root: Path, relative: Path) -> bool:
    """Avoid reviving legacy verification entries below a current linked worktree."""

    current = root
    for part in relative.parts[:-1]:
        current /= part
        if _is_linked_worktree(current):
            return True
    return False
