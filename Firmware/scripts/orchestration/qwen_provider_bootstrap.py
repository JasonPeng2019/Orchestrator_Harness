"""Register the package-local Qwen Code adapter, then invoke the WIP lane controller.

This is intentionally outside ``target-harness/``: the accepted WIP product already exposes a
provider-adapter registry, while this Firmware package owns its Qwen Code/Ollama route.  The module
must run in the same interpreter as ``lane_controller`` because registrations are process-local.
"""

from __future__ import annotations

# pyright: reportMissingImports=false
# The provider API is imported dynamically from the selected disposable target worktree.

import json
import os
import shutil
import sys
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[2]


def resolve_target_root(value: str | None = None) -> Path:
    """Resolve the package-local target worktree, defaulting to its normal location."""

    raw = value if value is not None else os.environ.get("FIRMWARE_TARGET_HARNESS")
    candidate = Path(raw).expanduser() if raw else PACKAGE_ROOT / "target-harness"
    if not candidate.is_absolute():
        candidate = PACKAGE_ROOT / candidate
    return candidate.resolve(strict=False)


TARGET_ROOT = resolve_target_root()
QWEN_SETTINGS = PACKAGE_ROOT / ".qwen" / "settings.json"
QWEN_HOME = QWEN_SETTINGS.parent
if str(TARGET_ROOT) not in sys.path:
    sys.path.insert(0, str(TARGET_ROOT))

from orchestrator_harness.lane_controller import main as lane_controller_main
from orchestrator_harness.provider import (
    BaseProviderAdapter,
    ProviderAdapterError,
    ProviderCapabilities,
    ProviderEvent,
    ProviderLaunchSpec,
    provider_registry,
    redact_command,
    register_provider_adapter,
)


class QwenCodeProviderAdapter(BaseProviderAdapter):
    """Small adapter for Qwen Code's documented stream-JSON CLI protocol."""

    provider_id = "qwen-code"

    @staticmethod
    def _route_argv(model: str) -> list[str]:
        """Project the package-owned Ollama and MCP configuration into Qwen CLI flags."""

        try:
            settings = json.loads(QWEN_SETTINGS.read_text(encoding="utf-8"))
            definitions = settings["modelProviders"]["openai"]
            definition = next(item for item in definitions if item.get("id") == model)
            servers = settings["mcpServers"]
        except (OSError, KeyError, StopIteration, TypeError, json.JSONDecodeError) as exc:
            raise ProviderAdapterError(f"cannot load package-local Qwen route for model {model!r}: {exc}") from exc
        env_key = definition.get("envKey")
        base_url = definition.get("baseUrl")
        if not isinstance(env_key, str) or not env_key or not isinstance(base_url, str) or not base_url:
            raise ProviderAdapterError("package-local Qwen model route is incomplete")
        if not isinstance(servers, dict) or not servers:
            raise ProviderAdapterError("package-local Qwen MCP route is missing")
        artifact_root = os.environ.get("BYO_MCP_ARTIFACT_ROOT", "").strip()
        mcp_servers: dict[str, dict[str, object]] = {}
        for name, server in servers.items():
            if not isinstance(name, str) or not isinstance(server, dict):
                continue
            routed: dict[str, object] = {**server, "cwd": str(PACKAGE_ROOT)}
            if artifact_root:
                declared_env = server.get("env", {})
                if not isinstance(declared_env, dict):
                    raise ProviderAdapterError(
                        f"package-local Qwen MCP route {name!r} has malformed env"
                    )
                routed["env"] = {
                    **declared_env,
                    "BYO_MCP_ARTIFACT_ROOT": artifact_root,
                }
            mcp_servers[name] = routed
        if len(mcp_servers) != len(servers):
            raise ProviderAdapterError("package-local Qwen MCP route is malformed")
        return [
            "--auth-type",
            "openai",
            "--openai-api-key",
            os.environ.get(env_key, "ollama"),
            "--openai-base-url",
            base_url,
            "--mcp-config",
            json.dumps({"mcpServers": mcp_servers}, separators=(",", ":")),
        ]

    @staticmethod
    def _executable_argv(command: tuple[str, ...]) -> list[str]:
        """Use cmd.exe only when Windows resolves the declared CLI to a batch file."""

        executable = command[0]
        resolved = shutil.which(executable)
        if resolved and resolved.lower().endswith((".cmd", ".bat")):
            return [os.environ.get("COMSPEC", "cmd.exe"), "/d", "/s", "/c", resolved, *command[1:]]
        return list(command)

    def build_argv(self, spec: ProviderLaunchSpec) -> list[str]:
        if spec.action not in {"start", "resume"}:
            raise ProviderAdapterError("Qwen Code action must be start or resume")
        argv = [
            *self._executable_argv(spec.command),
            "--approval-mode=yolo",
            "--model",
            spec.model,
            "--output-format",
            "stream-json",
            *self._route_argv(spec.model),
        ]
        if spec.action == "resume":
            if not spec.session_id:
                raise ProviderAdapterError("Qwen Code resume requires a session ID")
            argv.extend(["--resume", spec.session_id])
        return argv

    def encode_prompt(self, prompt: bytes) -> bytes:
        if not isinstance(prompt, bytes) or not prompt:
            raise ProviderAdapterError("Qwen Code prompt must be non-empty bytes")
        return prompt

    def parse_transcript_line(self, line: bytes) -> ProviderEvent | None:
        try:
            value = json.loads(line.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None
        if not isinstance(value, dict):
            return None
        event_type = value.get("type")
        session_id = value.get("session_id")
        if not isinstance(session_id, str) or not session_id.strip():
            session_id = None
        if event_type == "system" and value.get("subtype") == "init":
            return ProviderEvent("STARTED", session_id=session_id, raw_type="system:init")
        if event_type != "result":
            return None
        is_error = value.get("is_error") is True or value.get("subtype") != "success"
        return ProviderEvent(
            "FAILED" if is_error else "COMPLETED",
            session_id=session_id,
            outcome="FAILED" if is_error else "COMPLETED",
            raw_type=f"result:{value.get('subtype')}",
        )

    def terminal_outcome(self, event: ProviderEvent | None, exit_code: int) -> str:
        if event is not None and event.kind == "FAILED":
            return "FAILED"
        return "COMPLETED" if exit_code == 0 else "FAILED"

    def redact_argv(self, argv: list[str] | tuple[str, ...]) -> tuple[str, ...]:
        return redact_command(argv)


def register_qwen_code() -> None:
    """Register exactly one truthful external adapter in this process."""

    # Keep model effort and compaction settings package-local for every provider
    # process launched by this bootstrap.  This process-local environment change
    # never reads or mutates the user's global Qwen configuration.
    os.environ["QWEN_HOME"] = str(QWEN_HOME)
    if "qwen-code" in provider_registry():
        return
    os.environ.setdefault("OLLAMA_API_KEY", "ollama")
    register_provider_adapter(
        "qwen-code",
        QwenCodeProviderAdapter(),
        version="qwen-code-stream-json-v1",
        capabilities=ProviderCapabilities(
            launch=True,
            prompt=True,
            event_result=True,
            session=True,
            resume=True,
            permission=True,
            configuration=True,
            notification=False,
        ),
    )


def main(argv: list[str] | None = None) -> int:
    if not TARGET_ROOT.is_dir():
        raise SystemExit(f"missing package-local target harness: {TARGET_ROOT}")
    register_qwen_code()
    return lane_controller_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
