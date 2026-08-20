from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from orchestrator_harness.cli import observe
from orchestrator_harness.config import load_config
from orchestrator_harness.events import conditions_from_snapshot
from orchestrator_harness.models import ProcessSnapshot


NOW = datetime(2026, 7, 30, 12, 0, 0, tzinfo=timezone.utc)
SIGNAL = {
    "schema": "manager-signal/v1",
    "signal_id": "smoke-signal",
    "kind": "HELP",
    "created_utc": "2026-07-30T12:00:00Z",
    "lane_id": "A00_test:Atlas:A00",
    "summary": "native signal discovery smoke",
    "evidence_paths": ["missing/evidence.txt"],
}


def write_json(path: Path, value: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def observe_signal(signals_root: Path, *, duplicate: bool = False, atomic: bool = False) -> None:
    write_json(signals_root / "smoke-signal.json", SIGNAL)
    if duplicate:
        (signals_root / "ordinary-copy.json").write_bytes(
            (signals_root / "smoke-signal.json").read_bytes()
        )
    if atomic:
        (signals_root / ".sig-smoke-signal.tmp.json").write_bytes(
            (signals_root / "smoke-signal.json").read_bytes()
        )


def run_case(name: str, *, duplicate: bool = False, atomic: bool = False) -> None:
    with TemporaryDirectory(prefix="m5-q5-signal-") as temporary:
        root = Path(temporary)
        harness_root = root / "harness"
        suite_root = root / "suite"
        workspace = suite_root / "runs" / "A00_test" / ".agent-workspace"
        harness_root.mkdir()
        workspace.mkdir(parents=True)
        config_path = harness_root / "config.json"
        write_json(
            config_path,
            {
                "suite_root": str(suite_root),
                "run_globs": ["runs/*"],
                "workspace_relpath": ".agent-workspace",
                "output_dir": ".state",
                "stable_read_delay_seconds": 0,
            },
        )
        config = load_config(config_path, harness_root=harness_root)
        signals_root = workspace / "manager-signals"
        signals_root.mkdir()
        observe_signal(signals_root, duplicate=duplicate, atomic=atomic)

        process_provider = lambda: ProcessSnapshot(True, (), (), "smoke")
        first, _ = observe(config, process_provider=process_provider, clock=lambda: NOW)
        second, _ = observe(config, process_provider=process_provider, clock=lambda: NOW)
        first_conditions = conditions_from_snapshot(first)
        second_conditions = conditions_from_snapshot(second)
        signal_conditions = {
            key: value
            for key, value in first_conditions.items()
            if value["type"] == "MANAGER_SIGNAL"
        }
        second_signal_conditions = {
            key: value
            for key, value in second_conditions.items()
            if value["type"] == "MANAGER_SIGNAL"
        }
        errors = {item["code"] for item in first["observation_errors"]}

        assert [item["signal_id"] for item in first["manager_signals"]] == ["smoke-signal"], name
        assert len(signal_conditions) == 1, (name, signal_conditions)
        assert len(second_signal_conditions) == 1, (name, second_signal_conditions)
        assert signal_conditions["manager-signal:smoke-signal"]["event_id"] == second_signal_conditions["manager-signal:smoke-signal"]["event_id"], name
        assert "MANAGER_SIGNAL_READ_ERROR" not in errors, (name, errors)
        print(f"PASS {name}: one signal, one native condition, stable event_id")


if __name__ == "__main__":
    run_case("hidden atomic staging plus final", atomic=True)
    run_case("ordinary final JSON", atomic=False)
    run_case("identical ordinary final duplicate", duplicate=True)
