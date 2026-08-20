#!/usr/bin/env python3
"""Phase 3.B live-subprocess probe: watch --until-actionable real wake path.

Proves, at the *real CLI subprocess* level (not the in-process helper the unit
suite already exercises), that:

  POSITIVE  a genuinely actionable event (MANAGER_SIGNAL) injected while
            `python -m orchestrator_harness watch --until-actionable` is blocked
            wakes it: the process returns EXIT_OK (0) and prints that event
            BEFORE the timeout deadline.

  NEGATIVE  a NON-actionable event (a malformed manager-signal file, which the
            harness records as an observation error, never an actionable
            condition) injected mid-watch does NOT wake it: the process runs to
            its deadline and returns EXIT_TIMEOUT (3) with a WATCH_TIMEOUT event.

Quota-free: actionable conditions derive from `observe()` reading on-disk suite
state; no live provider (claude/codex/ollama) is invoked at all.

Run:  PYTHONPATH=<clone-root> python probe_watch_actionable.py [--keep DIR]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

EXIT_OK = 0
EXIT_TIMEOUT = 3

# Clone root == the harness package parent (…/compat-test). This probe lives at
# …/compat-test/scratch/3B/, so parents[2] is the clone root that holds the
# orchestrator_harness package.
CLONE_ROOT = Path(__file__).resolve().parents[2]


def _write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _make_suite(base: Path) -> tuple[Path, Path]:
    """Create a minimal harness suite; return (config_path, run_workspace)."""
    harness = base / "harness"
    suite = base / "suite"
    harness.mkdir(parents=True, exist_ok=True)
    suite.mkdir(parents=True, exist_ok=True)
    config_path = harness / "config.json"
    _write_json(
        config_path,
        {
            "suite_root": str(suite),
            "run_globs": ["runs/*"],
            "workspace_relpath": ".agent-workspace",
            "output_dir": ".state",
            # Poll briskly so an injected signal is seen within a second, but
            # keep a generous timeout so the wake is unambiguously pre-deadline.
            "poll_interval_seconds": 0.4,
            "watch_timeout_seconds": 30,
            "request_warning_seconds": 120,
            "request_critical_seconds": 30,
            "process_start_tolerance_seconds": 2,
            "stable_read_delay_seconds": 0,
        },
    )
    workspace = suite / "runs" / "A00_test" / ".agent-workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    return config_path, workspace


def _valid_signal(signal_id: str) -> dict:
    return {
        "schema": "manager-signal/v1",
        "signal_id": signal_id,
        "kind": "HELP",
        "created_utc": "2026-07-30T12:00:00Z",
        "lane_id": "A00_test:Atlas:A00",
        "summary": "manager input needed",
        "evidence_paths": ["missing/secret.txt"],
    }


def _launch_watch(config_path: Path, timeout_seconds: float) -> subprocess.Popen:
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONPATH"] = str(CLONE_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    # Scrub any ambient provider credentials: this path must never reach a
    # provider, and stripping proves it.
    for key in list(env):
        if key.startswith("ANTHROPIC_"):
            env.pop(key, None)
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "orchestrator_harness",
            "--config",
            str(config_path),
            "watch",
            "--until-actionable",
            "--timeout",
            str(timeout_seconds),
        ],
        cwd=str(CLONE_ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def _run_case(
    name: str,
    base: Path,
    *,
    inject,
    timeout_seconds: float,
    inject_after: float,
) -> dict:
    config_path, workspace = _make_suite(base)
    started = time.monotonic()
    proc = _launch_watch(config_path, timeout_seconds)

    injected_at = {"value": None}

    def _do_inject() -> None:
        time.sleep(inject_after)
        # Only inject if the watch is still running (proves mid-watch injection).
        if proc.poll() is None:
            inject(workspace)
            injected_at["value"] = time.monotonic() - started

    injector = threading.Thread(target=_do_inject)
    injector.start()

    # Hard cap well beyond the watch's own deadline so a hung probe still exits.
    try:
        out, err = proc.communicate(timeout=timeout_seconds + 30)
    except subprocess.TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
    injector.join()
    elapsed = time.monotonic() - started

    events = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    types = [e.get("type") for e in events]
    return {
        "case": name,
        "returncode": proc.returncode,
        "elapsed_s": round(elapsed, 2),
        "injected_at_s": (
            round(injected_at["value"], 2) if injected_at["value"] else None
        ),
        "event_types": types,
        "stdout": out,
        "stderr_tail": "\n".join(err.splitlines()[-15:]),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", metavar="DIR", help="keep fixtures under DIR")
    args = ap.parse_args()

    if args.keep:
        root = Path(args.keep).resolve()
        root.mkdir(parents=True, exist_ok=True)
        cleanup = None
    else:
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        cleanup = tmp

    results = []

    # POSITIVE: valid MANAGER_SIGNAL injected mid-watch -> wake (EXIT_OK).
    def _inject_valid(ws: Path) -> None:
        _write_json(ws / "manager-signals" / "wake.json", _valid_signal("wake"))

    pos = _run_case(
        "positive-manager-signal-wake",
        root / "positive",
        inject=_inject_valid,
        timeout_seconds=30,
        inject_after=2.5,
    )
    pos_pass = (
        pos["returncode"] == EXIT_OK
        and "MANAGER_SIGNAL" in pos["event_types"]
        and "WATCH_TIMEOUT" not in pos["event_types"]
        and pos["injected_at_s"] is not None
        and pos["elapsed_s"] < 30
    )
    pos["verdict"] = "PASS" if pos_pass else "FAIL"
    results.append(pos)

    # NEGATIVE: malformed signal injected mid-watch -> NON-actionable -> no wake
    # (EXIT_TIMEOUT). A short deadline keeps the case quick; injection still
    # happens well before it.
    def _inject_malformed(ws: Path) -> None:
        p = ws / "manager-signals" / "bad.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("{not-json", encoding="utf-8")

    neg = _run_case(
        "negative-nonactionable-no-wake",
        root / "negative",
        inject=_inject_malformed,
        timeout_seconds=6,
        inject_after=2.0,
    )
    neg_pass = (
        neg["returncode"] == EXIT_TIMEOUT
        and "WATCH_TIMEOUT" in neg["event_types"]
        and "MANAGER_SIGNAL" not in neg["event_types"]
        and neg["injected_at_s"] is not None
    )
    neg["verdict"] = "PASS" if neg_pass else "FAIL"
    results.append(neg)

    overall = "PASS" if pos_pass and neg_pass else "FAIL"
    report = {
        "probe": "3.B watch --until-actionable live subprocess",
        "clone_root": str(CLONE_ROOT),
        "python": sys.version.split()[0],
        "overall": overall,
        "cases": results,
    }
    print(json.dumps(report, indent=2))

    if cleanup is not None:
        cleanup.cleanup()
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
