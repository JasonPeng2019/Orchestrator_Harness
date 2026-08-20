"""Materialize ``examples/coding.claude.invocation.example.json`` and load it
end-to-end through ``lane_controller.load_invocation``.

The example file is a valid canonical template whose absolute paths and
content-bound SHA-256 values are placeholders.  This script recreates the
placeholder layout under a temporary root, substitutes the paths, computes the
real task-card / prompt-bundle digests with the same helpers a caller would
use, and proves the resulting record loads through the controller's strict
loader.

Run from the repository root:
    python evidence/0.4/validate_invocation.py
"""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from pathlib import Path

HARNESS_ROOT = Path(__file__).resolve().parents[2]
if str(HARNESS_ROOT) not in sys.path:
    sys.path.insert(0, str(HARNESS_ROOT))

from orchestrator_harness.lane_controller import load_invocation
from orchestrator_harness.prompt_bundle import prompt_bundle_record_from_paths

EXAMPLE = HARNESS_ROOT / "examples" / "coding.claude.invocation.example.json"
PLACEHOLDER_BASE = "C:/absolute/path/to"


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    raw = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    print(f"example: {EXAMPLE}")
    print(f"placeholder base substituted: {PLACEHOLDER_BASE!r}")

    with tempfile.TemporaryDirectory(prefix="claude-example-validate-") as temporary:
        tmp = Path(temporary).resolve()
        # Recreate the placeholder layout.  Every directory the strict loader
        # requires to exist is materialized here.
        # The JSON replaces the whole "C:/absolute/path/to" placeholder base
        # with the temp root, so the materialized paths carry no extra prefix.
        run_root = tmp / "project-worktrees/parser"
        runtime_root = tmp / "runtime/orchestrator-harness/example-epoch"
        repo_common = tmp / "repository/.git"
        workspace = run_root / ".agent-workspace"
        repo_common.mkdir(parents=True)
        run_root.mkdir(parents=True)
        runtime_root.mkdir(parents=True)
        workspace.mkdir(parents=True)
        prompt = workspace / "worker-prompt.md"
        prompt.write_text(
            "Create HELLO.txt containing exactly 'hello from claude' and commit it.\n",
            encoding="utf-8",
        )

        substituted = EXAMPLE.read_text(encoding="utf-8").replace(
            PLACEHOLDER_BASE, str(tmp).replace("\\", "/")
        )
        record = json.loads(substituted)
        assert record["run_root"] == str(run_root).replace("\\", "/")
        assert record["runtime_root"] == str(runtime_root).replace("\\", "/")
        assert record["repository"]["common_dir"] == str(repo_common).replace("\\", "/")

        # Content-bound identity: hash the task-card record and build the real
        # prompt bundle with the canonical helper (same path a caller uses).
        card = {
            "schema": "orchestrator-task-card/v1",
            "card_id": record["task_card"]["id"],
            "lane_id": record["lane_id"],
            "stage_cohort_id": record["cohort_id"],
            "worker_invocation_id": record["worker_invocation_id"],
            "objective": "Create HELLO.txt and commit it",
            "revision": record["task_card"]["revision"],
        }
        record["task_card"]["sha256"] = _sha256_bytes(
            json.dumps(card, sort_keys=True, separators=(",", ":")).encode("utf-8")
        )
        record["prompt_bundle"] = prompt_bundle_record_from_paths(
            workflow_id=record["workflow"]["id"],
            task_card_id=record["task_card"]["id"],
            profile_id=record["profile"]["id"],
            paths=(("instructions", prompt),),
            run_root=run_root,
        )

        invocation_path = workspace / "invocation.json"
        invocation_path.write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

        print("\n--- materialized record (rendered example) ---")
        print(invocation_path.read_text(encoding="utf-8"))

        invocation = load_invocation(invocation_path)
        print("\n--- load_invocation result ---")
        print(f"invocation_schema     = {invocation.invocation_schema}")
        print(f"provider_id           = {invocation.provider_id}")
        print(f"action                = {invocation.action}")
        print(f"lane_id               = {invocation.lane_id}")
        print(f"worker_invocation_id  = {invocation.worker_invocation_id}")
        print(f"model                 = {invocation.model}")
        print(f"command               = {invocation.codex_command}")
        print(f"config_overrides      = {invocation.config_overrides}")
        print(f"permission_mode       = {invocation.provider_options.get('permission_mode')!r}")
        print(f"run_root              = {invocation.run_root}")
        print(f"runtime_root          = {invocation.runtime_root}")
        print(f"event_log             = {invocation.event_log}")
        print(f"resources             = {list(invocation.resources)}")
        print(f"prompt_bundle_sha256  = {invocation.prompt_bundle.bundle_sha256}")
        print(f"prompt_bytes          = {invocation.prompt_bytes!r}")
        print(f"status_path           = {invocation.status_path}")
        print(f"repository            = {invocation.repository}")
        print(f"provider_launch_sha256= {invocation.canonical.provider_launch_sha256}")

        if invocation.invocation_schema != "orchestrator-worker-invocation/v1":
            raise SystemExit("FAIL: wrong schema")
        if invocation.provider_id != "claude-code":
            raise SystemExit("FAIL: wrong provider")
        if invocation.config_overrides != ['model_provider="ollama"']:
            raise SystemExit("FAIL: config_overrides not preserved")
        if invocation.provider_options.get("permission_mode") is not None:
            raise SystemExit("FAIL: permission_mode should default, not be set")
        if not invocation.status_path.is_relative_to(invocation.workspace):
            raise SystemExit("FAIL: status path not under workspace")
        print("\nLOAD_VALIDATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
