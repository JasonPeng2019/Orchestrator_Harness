"""Focused unit tests for the package-local Qwen Code adapter bootstrap."""

from __future__ import annotations

import importlib.util
import json
import unittest
from dataclasses import dataclass
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).with_name("qwen_provider_bootstrap.py")
SPEC = importlib.util.spec_from_file_location("qwen_provider_bootstrap", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


@dataclass(frozen=True)
class _InvocationFixture:
    invocation_schema: str | None
    provider_id: str
    codex_command: list[str]


class QwenProviderBootstrapTests(unittest.TestCase):
    def test_schema_less_binding_selects_qwen_and_canonical_is_unchanged(self) -> None:
        legacy = _InvocationFixture(None, "codex", ["codex"])
        canonical = _InvocationFixture(
            "orchestrator-worker-invocation/v1", "codex", ["codex"]
        )
        with mock.patch.object(
            MODULE, "lane_controller_load_invocation", return_value=legacy
        ):
            bound = MODULE.load_invocation(Path("legacy.invocation.json"))
        self.assertEqual("qwen-code", bound.provider_id)
        self.assertEqual(["qwen"], bound.codex_command)
        self.assertIsNot(legacy, bound)

        with mock.patch.object(
            MODULE, "lane_controller_load_invocation", return_value=canonical
        ):
            unchanged = MODULE.load_invocation(Path("canonical.invocation.json"))
        self.assertIs(canonical, unchanged)

        with (
            mock.patch.object(MODULE, "TARGET_ROOT", Path(".")),
            mock.patch.object(MODULE, "register_qwen_code"),
            mock.patch.object(
                MODULE, "lane_controller_load_invocation", return_value=canonical
            ),
            mock.patch.object(MODULE, "lane_controller_run", return_value=7) as run,
        ):
            self.assertEqual(7, MODULE.main(["canonical.invocation.json"]))
        run.assert_called_once_with(canonical)

    def test_deepseek_effort_and_auto_compaction_are_package_local(self) -> None:
        settings = json.loads(MODULE.QWEN_SETTINGS.read_text(encoding="utf-8"))
        deepseek = next(
            item
            for item in settings["modelProviders"]["openai"]
            if item["id"] == "deepseek-v4-flash:0731-cloud"
        )
        context_window = deepseek["generationConfig"]["contextWindowSize"]
        threshold = settings["context"]["autoCompactThreshold"]

        self.assertEqual("high", deepseek["generationConfig"]["extra_body"]["reasoning_effort"])
        self.assertEqual(1_048_576, context_window)
        self.assertEqual(180_000, context_window * threshold)

        with mock.patch.dict(MODULE.os.environ, {"QWEN_HOME": "C:/global-qwen"}):
            MODULE.register_qwen_code()
            self.assertEqual(str(MODULE.QWEN_HOME), MODULE.os.environ["QWEN_HOME"])

    def test_target_root_defaults_or_uses_an_explicit_package_local_path(self) -> None:
        self.assertEqual(MODULE.PACKAGE_ROOT / "target-harness", MODULE.resolve_target_root())
        self.assertEqual(
            MODULE.PACKAGE_ROOT / "alternate-target",
            MODULE.resolve_target_root("alternate-target"),
        )

    def test_stream_events_and_launch_arguments(self) -> None:
        adapter = MODULE.QwenCodeProviderAdapter()
        spec = MODULE.ProviderLaunchSpec(
            action="start",
            command=("qwen",),
            model="deepseek-v4-flash:0731-cloud",
            reasoning_effort="high",
            service_tier="none",
            session_id=None,
            run_root=Path("C:/run"),
            last_message_path=Path("C:/run/last-message.txt"),
        )
        with mock.patch.object(MODULE.shutil, "which", return_value=None):
            argv = adapter.build_argv(spec)
        self.assertEqual(
            ["qwen", "--approval-mode=yolo", "--model", "deepseek-v4-flash:0731-cloud"],
            argv[:4],
        )
        self.assertIn("--auth-type", argv)
        self.assertIn("--openai-base-url", argv)
        config = json.loads(argv[argv.index("--mcp-config") + 1])
        self.assertEqual(str(MODULE.PACKAGE_ROOT), config["mcpServers"]["byo-firmware"]["cwd"])
        started = adapter.parse_transcript_line(
            json.dumps(
                {"type": "system", "subtype": "init", "session_id": "session-1"}
            ).encode()
        )
        completed = adapter.parse_transcript_line(
            json.dumps({"type": "result", "subtype": "success", "is_error": False}).encode()
        )
        self.assertEqual("STARTED", started.kind)
        self.assertEqual("session-1", started.session_id)
        self.assertEqual("COMPLETED", completed.kind)

    def test_windows_batch_launcher_uses_comspec(self) -> None:
        adapter = MODULE.QwenCodeProviderAdapter()
        with (
            mock.patch.object(MODULE.shutil, "which", return_value="C:/qwen/qwen.cmd"),
            mock.patch.dict(MODULE.os.environ, {"COMSPEC": "C:/Windows/System32/cmd.exe"}),
        ):
            self.assertEqual(
                [
                    "C:/Windows/System32/cmd.exe",
                    "/d",
                    "/s",
                    "/c",
                    "C:/qwen/qwen.cmd",
                ],
                adapter._executable_argv(("qwen",)),
            )

    def test_isolated_artifact_root_is_projected_into_mcp_environment(self) -> None:
        isolated = MODULE.PACKAGE_ROOT / "runtime" / "byo-mcp" / "lane-a"
        with mock.patch.dict(
            MODULE.os.environ,
            {"BYO_MCP_ARTIFACT_ROOT": str(isolated)},
            clear=False,
        ):
            argv = MODULE.QwenCodeProviderAdapter._route_argv(
                "deepseek-v4-flash:0731-cloud"
            )
        config = json.loads(argv[argv.index("--mcp-config") + 1])
        self.assertEqual(
            str(isolated),
            config["mcpServers"]["byo-firmware"]["env"]["BYO_MCP_ARTIFACT_ROOT"],
        )

    def test_registration_is_idempotent_and_declares_no_immediate_notification(self) -> None:
        MODULE.register_qwen_code()
        registration = MODULE.provider_registry()["qwen-code"]
        self.assertEqual("qwen-code-stream-json-v1", registration.version)
        self.assertFalse(registration.capabilities.notification)
        MODULE.register_qwen_code()


if __name__ == "__main__":
    unittest.main()
