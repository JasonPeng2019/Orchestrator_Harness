from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

root = Path.cwd()
examples = root / "examples"
sys.path.insert(0, str(examples))
import disposable_claude_coding_fixture as fixture

qwen = shutil.which("qwen")
if not qwen:
    raise fixture.FixtureError("no qwen CLI on PATH")

keep = root / ".agent-workspace" / "live-qwen-fixture-004"
project = keep / "project"
worktrees = keep / "worktrees"
runtime = keep / "runtime"
project.mkdir(parents=True, exist_ok=False)
worktrees.mkdir()
runtime.mkdir()
fixture._git(project, "init", "-b", "main")
fixture._git(project, "config", "user.email", "fixture@example.invalid")
fixture._git(project, "config", "user.name", "Disposable Fixture")
(project / "README.md").write_text("# Fixture project\n", encoding="utf-8")
(project / ".gitignore").write_text(".agent-workspace/\n", encoding="utf-8")
fixture._git(project, "add", "README.md", ".gitignore")
fixture._git(project, "commit", "-m", "Initial fixture project")
base = fixture._git(project, "rev-parse", "HEAD")
lane = worktrees / "lane-qwen"
fixture._git(project, "worktree", "add", "-b", "lane/qwen-hello", str(lane), base)
prompt = (
    "This is a disposable fixture task. Do exactly this:\n\n"
    "1. Create HELLO_QWEN.txt with exactly one line: hello from qwen\n"
    "2. Stage and commit it with message add HELLO_QWEN.txt.\n"
    "Then reply with the commit hash. Do not modify anything else.\n"
)
invocation_path = fixture._invocation(
    lane="qwen-hello", worktree=lane, common_dir=(project / ".git").resolve(),
    base_commit=base, runtime=runtime, prompt_text=prompt, command=[qwen, "exec"],
)
invocation = json.loads(invocation_path.read_text(encoding="utf-8"))
invocation["cohort_id"] = "cohort-qwen-live-001"
invocation["provider"] = {
    "id": "qwen-code", "model": "deepseek-v4-flash:0731-cloud", "command": [qwen, "exec"],
}
invocation["profile"]["provider"] = "qwen-code"
invocation["profile"]["model"] = "deepseek-v4-flash:0731-cloud"
invocation["profile"].pop("provider_needs", None)
fixture._write_json(invocation_path, invocation)
receipt = fixture._start_controller(invocation_path)
status = fixture._finish_controller(receipt)
if status.get("state") != "PROVIDER_EXITED" or status.get("exit_code") != 0:
    raise fixture.FixtureError(f"Qwen controller terminal failure: {status}")
if status.get("provider_terminal_outcome") != "COMPLETED":
    raise fixture.FixtureError(f"Qwen outcome was {status.get('provider_terminal_outcome')!r}")
artifact = lane / "HELLO_QWEN.txt"
if not artifact.is_file() or artifact.read_text(encoding="utf-8").strip() != "hello from qwen":
    raise fixture.FixtureError("Qwen lane did not create the exact artifact")
head = fixture._git(lane, "rev-parse", "HEAD")
if head == base:
    raise fixture.FixtureError("Qwen lane made no commit")
events = fixture._lane_events(runtime)
print(json.dumps({
    "schema": "orchestrator-disposable-qwen-live/v1", "provider_id": "qwen-code",
    "model": "deepseek-v4-flash:0731-cloud", "terminal_state": status.get("state"),
    "provider_terminal_outcome": status.get("provider_terminal_outcome"),
    "provider_exit_code": status.get("exit_code"), "provider_session_id": status.get("provider_session_id"),
    "base_commit": base, "head_commit": head, "hello_content": artifact.read_text(encoding="utf-8"),
    "lane_event_types": [row.get("event") for row in events],
}, indent=2, sort_keys=True))
