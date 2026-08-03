from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from worktree_task import close_task, create_task, list_tasks


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, text=True, capture_output=True)


def test_create_list_close_on_windows_paths(tmp_path: Path) -> None:
    root = tmp_path / "repo with spaces"
    root.mkdir()
    _git(root, "init")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test User")
    (root / "README.md").write_text("baseline\n", encoding="utf-8")
    _git(root, "add", "README.md")
    _git(root, "commit", "-m", "baseline")

    created = create_task("demo task", None, "codex", root)
    assert Path(created.path).exists()
    assert list_tasks(root) == [created]

    closed = close_task("demo task", root)
    assert closed == created
    assert not Path(created.path).exists()
