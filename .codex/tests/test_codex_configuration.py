from __future__ import annotations

import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_all_expected_skills_are_registered_and_present() -> None:
    config = tomllib.loads((ROOT / ".codex" / "config.toml").read_text(encoding="utf-8"))
    configured = {entry["path"] for entry in config["skills"]["config"] if entry["enabled"]}
    expected = {
        "skills/verify",
        "skills/checkpoint",
        "skills/test-first",
        "skills/api-design",
        "skills/worktree",
        "skills/plan-harness-workflow",
    }
    assert configured == expected
    for relative in expected:
        assert (ROOT / ".codex" / relative / "SKILL.md").is_file()
        assert (ROOT / ".codex" / relative / "agents" / "openai.yaml").is_file()


def test_skill_invocation_policy_is_intentional() -> None:
    automatic = {"verify", "checkpoint", "worktree"}
    explicit = {"test-first", "api-design", "plan-harness-workflow"}
    for name in automatic:
        metadata = (ROOT / ".codex" / "skills" / name / "agents" / "openai.yaml").read_text(encoding="utf-8")
        assert "allow_implicit_invocation: true" in metadata
    for name in explicit:
        metadata = (ROOT / ".codex" / "skills" / name / "agents" / "openai.yaml").read_text(encoding="utf-8")
        assert "allow_implicit_invocation: false" in metadata


def test_skill_commands_point_to_the_consolidated_environment() -> None:
    for path in (ROOT / ".codex" / "skills").glob("*/SKILL.md"):
        text = path.read_text(encoding="utf-8")
        if "uv run" in text:
            assert "uv run --project .codex/dev --locked" in text
    assert (ROOT / ".codex" / "dev" / "pyproject.toml").is_file()
    assert (ROOT / ".codex" / "dev" / "uv.lock").is_file()
    assert (ROOT / ".codex" / "scripts" / "verify.py").is_file()
    assert (ROOT / ".codex" / "scripts" / "worktree_task.py").is_file()


def test_hook_catalog_contains_every_installed_action() -> None:
    payload = json.loads((ROOT / ".codex" / "hooks.json").read_text(encoding="utf-8"))
    assert set(payload["hooks"]) == {"SessionStart", "PreToolUse", "PreCompact", "Stop"}
    commands = [
        handler["commandWindows"]
        for groups in payload["hooks"].values()
        for group in groups
        for handler in group["hooks"]
    ]
    assert all(".codex/dev" in command for command in commands)
    assert all(".codex/scripts/hook_runner.py" in command for command in commands)
