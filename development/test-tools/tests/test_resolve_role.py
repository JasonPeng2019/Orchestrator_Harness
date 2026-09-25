"""Focused contract tests for the launch-time role resolver."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
RESOLVER = REPO_ROOT / "development" / "test-tools" / "resolve-role.py"
MAPPING = REPO_ROOT / ".plans" / "SUBAGENT_ROLE_MODEL_MAPPING.json"
FROZEN_HARNESS = REPO_ROOT / "references" / "harness-single"
DOGFOOD_HARNESS = REPO_ROOT / "development" / "dogfood" / "harness"


class ResolveRoleTests(unittest.TestCase):
    def run_resolver(
        self,
        role: str,
        *,
        mapping: Path = MAPPING,
        harness_root: Path = FROZEN_HARNESS,
        fallback_index: int | None = None,
    ) -> subprocess.CompletedProcess[str]:
        argv = [
            sys.executable,
            str(RESOLVER),
            "--mapping",
            str(mapping),
            "--harness-root",
            str(harness_root),
        ]
        if fallback_index is not None:
            argv.extend(["--fallback-index", str(fallback_index)])
        argv.append(role)
        return subprocess.run(argv, text=True, capture_output=True, check=False)

    def test_preferred_role_projects_only_native_bootstrap_arguments(self) -> None:
        result = self.run_resolver("routine")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(
            json.loads(result.stdout),
            [
                "--provider",
                "codex",
                "--model",
                "deepseek-v4.1-flash:cloud",
                "--provider-option",
                "reasoning_effort=high",
                "--provider-option",
                "service_tier=normal",
                "--provider-option",
                "launcher=ollama",
            ],
        )

    def test_output_round_trips_through_unchanged_native_operator_parser(self) -> None:
        result = self.run_resolver("routine")
        self.assertEqual(result.returncode, 0, result.stderr)
        resolved = json.loads(result.stdout)

        sys.path.insert(0, str(FROZEN_HARNESS))
        try:
            from orchestrator_harness import operator_launch

            parsed = operator_launch._build_parser().parse_args(
                [
                    "lane",
                    "bootstrap",
                    "--lane-id",
                    "resolver-roundtrip",
                    "--task-card",
                    "task-card.json",
                    *resolved,
                ]
            )
            options = operator_launch._provider_options(parsed.provider_option)
        finally:
            sys.path.pop(0)

        self.assertEqual(parsed.provider, "codex")
        self.assertEqual(parsed.model, "deepseek-v4.1-flash:cloud")
        self.assertEqual(
            options,
            {
                "reasoning_effort": "high",
                "service_tier": "normal",
                "launcher": "ollama",
            },
        )

    def test_every_executable_preferred_role_round_trips(self) -> None:
        mapping = json.loads(MAPPING.read_text(encoding="utf-8"))
        executable = {
            role: allocation
            for role, allocation in mapping["roles"].items()
            if allocation.get("launch", True)
        }
        self.assertEqual(len(executable), 13)

        sys.path.insert(0, str(FROZEN_HARNESS))
        try:
            from orchestrator_harness import operator_launch

            for role, allocation in executable.items():
                with self.subTest(role=role):
                    result = self.run_resolver(role)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    resolved = json.loads(result.stdout)
                    parsed = operator_launch._build_parser().parse_args(
                        [
                            "lane",
                            "bootstrap",
                            "--lane-id",
                            f"resolver-{role}",
                            "--task-card",
                            "task-card.json",
                            *resolved,
                        ]
                    )
                    self.assertEqual(parsed.provider, allocation["provider"])
                    self.assertEqual(parsed.model, allocation["model"])
                    self.assertEqual(
                        operator_launch._provider_options(parsed.provider_option),
                        allocation["launch_config"],
                    )
        finally:
            sys.path.pop(0)

    def test_deployed_builder_resolves_the_same_preferred_arguments(self) -> None:
        frozen = self.run_resolver("routine", harness_root=FROZEN_HARNESS)
        deployed = self.run_resolver("routine", harness_root=DOGFOOD_HARNESS)

        self.assertEqual(frozen.returncode, 0, frozen.stderr)
        self.assertEqual(deployed.returncode, 0, deployed.stderr)
        self.assertEqual(json.loads(deployed.stdout), json.loads(frozen.stdout))

    def test_root_unknown_and_empty_roles_are_rejected(self) -> None:
        for role in ("root", "unknown-role", ""):
            with self.subTest(role=role):
                result = self.run_resolver(role)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")

    def test_explicit_fallback_selection_is_root_controlled_and_projected(self) -> None:
        result = self.run_resolver("test_author", fallback_index=1)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            [
                "--provider",
                "codex",
                "--model",
                "gpt-5.6-terra",
                "--provider-option",
                "reasoning_effort=max",
                "--provider-option",
                "service_tier=normal",
            ],
        )
        rejected = self.run_resolver("test_author", fallback_index=99)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertEqual(rejected.stdout, "")

    def test_malformed_or_adapter_invalid_binding_is_rejected(self) -> None:
        canonical = json.loads(MAPPING.read_text(encoding="utf-8"))
        cases = []

        empty = copy.deepcopy(canonical)
        empty["roles"]["routine"] = {}
        cases.append(empty)

        invalid_option = copy.deepcopy(canonical)
        invalid_option["roles"]["routine"]["launch_config"]["unknown"] = "value"
        cases.append(invalid_option)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for index, candidate in enumerate(cases):
                with self.subTest(index=index):
                    path = root / f"mapping-{index}.json"
                    path.write_text(json.dumps(candidate), encoding="utf-8")
                    result = self.run_resolver("routine", mapping=path)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
