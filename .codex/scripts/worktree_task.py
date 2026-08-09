from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class TaskRecord:
    task: str
    slug: str
    path: str
    branch: str
    owner: str | None


def _git(*args: str, cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=cwd, check=check, text=True, capture_output=True)


def repo_root(cwd: Path | None = None) -> Path:
    result = _git("rev-parse", "--show-toplevel", cwd=cwd or Path.cwd())
    return Path(result.stdout.strip()).resolve()


def state_dir(root: Path) -> Path:
    result = _git("rev-parse", "--git-common-dir", cwd=root)
    common = Path(result.stdout.strip())
    if not common.is_absolute():
        common = root / common
    path = common.resolve() / "orchestrator-worktrees"
    path.mkdir(parents=True, exist_ok=True)
    return path


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-._")
    if not slug:
        raise RuntimeError("task name must contain letters or digits")
    return slug


def _record_path(root: Path, slug: str) -> Path:
    return state_dir(root) / f"{slug}.json"


def list_tasks(root: Path) -> list[TaskRecord]:
    records = []
    for path in sorted(state_dir(root).glob("*.json")):
        records.append(TaskRecord(**json.loads(path.read_text(encoding="utf-8"))))
    return records


def create_task(task: str, branch: str | None, owner: str | None, root: Path) -> TaskRecord:
    if _git("rev-parse", "--verify", "HEAD", cwd=root, check=False).returncode != 0:
        raise RuntimeError("the repository needs an initial commit before Git can create a worktree")

    slug = slugify(task)
    metadata = _record_path(root, slug)
    if metadata.exists():
        raise RuntimeError(f"task already exists: {task}")

    worktree = root.parent / f".{slugify(root.name)}-worktrees" / slug
    if worktree.exists():
        raise RuntimeError(f"worktree path already exists: {worktree}")
    worktree.parent.mkdir(parents=True, exist_ok=True)

    branch_name = branch or slug
    branch_exists = _git("rev-parse", "--verify", f"refs/heads/{branch_name}", cwd=root, check=False).returncode == 0
    args = (
        ("worktree", "add", str(worktree), branch_name)
        if branch_exists
        else (
            "worktree",
            "add",
            "-b",
            branch_name,
            str(worktree),
            "HEAD",
        )
    )
    _git(*args, cwd=root)

    record = TaskRecord(task, slug, str(worktree), branch_name, owner)
    metadata.write_text(json.dumps(asdict(record), indent=2) + "\n", encoding="utf-8")
    return record


def close_task(task: str, root: Path) -> TaskRecord:
    slug = slugify(task)
    metadata = _record_path(root, slug)
    if not metadata.exists():
        raise RuntimeError(f"unknown task: {task}")
    record = TaskRecord(**json.loads(metadata.read_text(encoding="utf-8")))
    worktree = Path(record.path)
    status = _git("status", "--porcelain", cwd=worktree, check=False)
    if status.returncode != 0:
        raise RuntimeError(f"cannot inspect worktree: {worktree}")
    if status.stdout.strip():
        raise RuntimeError(f"refusing to close dirty worktree: {worktree}")
    _git("worktree", "remove", str(worktree), cwd=root)
    metadata.unlink()
    return record


def _print_record(record: TaskRecord) -> None:
    print(f"task={record.task} path={record.path} branch={record.branch} owner={record.owner or 'n/a'}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage isolated development worktrees.")
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("create")
    create.add_argument("task")
    create.add_argument("--branch")
    create.add_argument("--owner")
    commands.add_parser("list")
    close = commands.add_parser("close")
    close.add_argument("task")
    args = parser.parse_args()

    try:
        root = repo_root()
        if args.command == "create":
            _print_record(create_task(args.task, args.branch, args.owner, root))
        elif args.command == "list":
            records = list_tasks(root)
            for record in records:
                _print_record(record)
            if not records:
                print("no task worktrees")
        else:
            _print_record(close_task(args.task, root))
    except (
        OSError,
        RuntimeError,
        subprocess.CalledProcessError,
        json.JSONDecodeError,
    ) as exc:
        parser.exit(1, f"worktree-task: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
