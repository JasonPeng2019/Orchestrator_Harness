from __future__ import annotations

import json
from pathlib import Path

import tomllib

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
        "skills/design-project-topology",
    }
    assert configured == expected
    for relative in expected:
        assert (ROOT / ".codex" / relative / "SKILL.md").is_file()
        assert (ROOT / ".codex" / relative / "agents" / "openai.yaml").is_file()


def test_new_root_sessions_receive_the_requested_compaction_limit() -> None:
    config = tomllib.loads((ROOT / ".codex" / "config.toml").read_text(encoding="utf-8"))
    assert config["model_auto_compact_token_limit"] == 280000
    assert config["model_auto_compact_token_limit_scope"] == "total"


def test_skill_invocation_policy_is_intentional() -> None:
    automatic = {"verify", "checkpoint", "worktree"}
    explicit = {"test-first", "api-design", "design-project-topology"}
    for name in automatic:
        metadata = (ROOT / ".codex" / "skills" / name / "agents" / "openai.yaml").read_text(encoding="utf-8")
        assert "allow_implicit_invocation: true" in metadata
    for name in explicit:
        metadata = (ROOT / ".codex" / "skills" / name / "agents" / "openai.yaml").read_text(encoding="utf-8")
        assert "allow_implicit_invocation: false" in metadata
    assert "skills/plan-harness-workflow" not in (ROOT / ".codex" / "config.toml").read_text(encoding="utf-8")


def test_skill_commands_point_to_the_consolidated_environment() -> None:
    for path in (ROOT / ".codex" / "skills").glob("*/SKILL.md"):
        text = path.read_text(encoding="utf-8")
        if "uv run" in text:
            assert "uv run --project .codex/dev --locked" in text
    assert (ROOT / ".codex" / "dev" / "pyproject.toml").is_file()
    assert (ROOT / ".codex" / "dev" / "uv.lock").is_file()
    assert (ROOT / ".codex" / "scripts" / "verify.py").is_file()
    assert (ROOT / ".codex" / "scripts" / "verify_changed.py").is_file()
    assert (ROOT / ".codex" / "scripts" / "worktree_task.py").is_file()


def test_verify_skill_keeps_full_gate_separate_from_stop_gate() -> None:
    skill = (ROOT / ".codex" / "skills" / "verify" / "SKILL.md").read_text(encoding="utf-8")
    assert ".codex/scripts/verify.py" in skill
    assert ".codex/scripts/verify_changed.py" in skill
    assert "never replaces this skill" in skill


def test_hook_catalog_contains_every_installed_action() -> None:
    payload = json.loads((ROOT / ".codex" / "hooks.json").read_text(encoding="utf-8"))
    assert set(payload["hooks"]) == {"SessionStart", "PreToolUse", "PreCompact", "Stop"}
    commands = [
        handler["commandWindows"]
        for groups in payload["hooks"].values()
        for group in groups
        for handler in group["hooks"]
    ]
    assert all(
        (".codex/dev" in command and ".codex/scripts/hook_runner.py" in command)
        or ".codex/scripts/bounded_test_adapter.py" in command
        for command in commands
    )
    assert any(".codex/scripts/bounded_test_adapter.py" in command for command in commands)
