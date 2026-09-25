"""Independent stdlib unittest controls for the STEP-001 fixture boundary."""

from __future__ import annotations

import ctypes
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from typing import Any, Iterable
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[3]
TESTS_ROOT = REPO_ROOT / "development" / "test-tools" / "tests"
FIXTURES_ROOT = TESTS_ROOT / "fixtures"
MANIFEST_PATH = FIXTURES_ROOT / "fixture_manifest.json"
CONTROL_CHILD_PATH = FIXTURES_ROOT / "control_child.py"


class FixtureControlTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.manifest: dict[str, Any] = json.loads(
            MANIFEST_PATH.read_text(encoding="utf-8")
        )
        self.fixture_root = REPO_ROOT / self.manifest["root"]
        self.control_child = self.fixture_root / self.manifest["control_child"]
        self._process_identities: dict[int, dict[str, Any] | None] = {}

    def _readback(self, record: dict[str, Any]) -> None:
        print(json.dumps(record, sort_keys=True, separators=(",", ":")), flush=True)

    def _run(
        self,
        args: list[str],
        *,
        cwd: Path | None = None,
        timeout: float = 5.0,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            args,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )

    def _popen(
        self,
        args: list[str],
        *,
        cwd: Path | None = None,
    ) -> subprocess.Popen[Any]:
        process = subprocess.Popen(
            args,
            cwd=cwd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self._process_identities[process.pid] = self._process_creation_identity(
            process.pid
        )
        return process

    def _process_creation_identity(
        self, pid: int
    ) -> dict[str, Any] | None:
        if not isinstance(pid, int) or pid <= 0:
            return None
        if os.name != "nt":
            try:
                fields = (Path("/proc") / str(pid) / "stat").read_text(
                    encoding="utf-8"
                ).split()
            except (OSError, UnicodeError):
                return None
            if len(fields) < 22:
                return None
            return {
                "pid": pid,
                "creation_filetime": f"linux-starttime:{fields[21]}",
            }

        try:
            class FILETIME(ctypes.Structure):
                _fields_ = [
                    ("dwLowDateTime", ctypes.c_uint32),
                    ("dwHighDateTime", ctypes.c_uint32),
                ]

            kernel32 = ctypes.windll.kernel32
            kernel32.OpenProcess.argtypes = [
                ctypes.c_uint32,
                ctypes.c_int,
                ctypes.c_uint32,
            ]
            kernel32.OpenProcess.restype = ctypes.c_void_p
            kernel32.GetProcessTimes.argtypes = [
                ctypes.c_void_p,
                ctypes.POINTER(FILETIME),
                ctypes.POINTER(FILETIME),
                ctypes.POINTER(FILETIME),
                ctypes.POINTER(FILETIME),
            ]
            kernel32.GetProcessTimes.restype = ctypes.c_int
            kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
            kernel32.CloseHandle.restype = ctypes.c_int
            handle = kernel32.OpenProcess(0x1000, False, pid)
            if not handle:
                return None
            try:
                creation = FILETIME()
                exit_time = FILETIME()
                kernel_time = FILETIME()
                user_time = FILETIME()
                if not kernel32.GetProcessTimes(
                    handle,
                    ctypes.byref(creation),
                    ctypes.byref(exit_time),
                    ctypes.byref(kernel_time),
                    ctypes.byref(user_time),
                ):
                    return None
                value = (
                    creation.dwHighDateTime << 32
                ) | creation.dwLowDateTime
                return {
                    "pid": pid,
                    "creation_filetime": f"windows-filetime:{value}",
                }
            finally:
                kernel32.CloseHandle(handle)
        except (OSError, ValueError, AttributeError):
            return None

    def _terminate_pid_checked(
        self,
        pid: int,
        identity: dict[str, Any],
    ) -> subprocess.CompletedProcess[str] | None:
        return self._terminate_pid(pid, identity)

    def _wait(self, process: subprocess.Popen[str], timeout: float) -> int:
        try:
            return process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            self._terminate_pid(
                process.pid, self._process_identities.get(process.pid)
            )
            process.wait(timeout=1.0)
            raise

    def _pid_exists(self, pid: int) -> bool:
        if os.name == "nt":
            result = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
                capture_output=True,
                text=True,
                check=False,
            )
            return str(pid) in result.stdout
        try:
            os.kill(pid, 0)
            return True
        except ProcessLookupError:
            return False
        except PermissionError:
            return True

    def _wait_for_pid_state(
        self,
        pid: int,
        *,
        present: bool,
        timeout: float = 5.0,
    ) -> bool:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self._pid_exists(pid) is present:
                return True
            time.sleep(0.05)
        self.fail(
            f"PID {pid} did not reach present={present!r} within {timeout!r} seconds"
        )
        raise AssertionError

    def _terminate_pid(
        self,
        pid: int,
        identity: dict[str, Any] | None = None,
    ) -> subprocess.CompletedProcess[str] | None:
        current_identity = self._process_creation_identity(pid)
        if (
            identity is None
            or current_identity is None
            or current_identity != identity
        ):
            return None
        if os.name == "nt":
            return subprocess.run(
                ["taskkill", "/PID", str(pid), "/T", "/F"],
                capture_output=True,
                text=True,
                check=False,
            )
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        return None

    def _cleanup_pids(self, pids: Iterable[int]) -> None:
        for pid in pids:
            if self._pid_exists(pid):
                self._terminate_pid(
                    pid, self._process_identities.get(pid)
                )

    def _base_path(self, name: str) -> Path:
        entry = self.manifest["task_bases"][name]
        return self.fixture_root / entry["path"]

    def _run_base(
        self,
        name: str,
        command_key: str,
        *,
        timeout: float = 5.0,
    ) -> subprocess.CompletedProcess[str]:
        entry = self.manifest["task_bases"][name]
        return self._run(
            list(entry[command_key]),
            cwd=self._base_path(name),
            timeout=timeout,
        )

    def _wait_for_checkpoint(
        self,
        path: Path,
        *,
        status: str | None = None,
        timeout: float = 5.0,
    ) -> dict[str, Any]:
        deadline = time.monotonic() + timeout
        last_error: Exception | None = None
        while time.monotonic() < deadline:
            if path.exists():
                try:
                    value = json.loads(path.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError) as error:
                    last_error = error
                else:
                    if status is None or value.get("status") == status:
                        return value
            time.sleep(0.02)
        self.fail(f"checkpoint did not reach status {status!r}: {path}: {last_error}")
        raise AssertionError

    def _excerpt(self, text: str, marker: str) -> str:
        for line in text.splitlines():
            if marker in line:
                return line.strip()
        return ""

    def test_manifest_and_independent_base_layout(self) -> None:
        self.assertEqual(
            self.manifest["schema"], "memory-harness-fixture-manifest/v1"
        )
        self.assertEqual(
            self.manifest["root"], "development/test-tools/tests/fixtures"
        )
        self.assertTrue(self.control_child.is_file(), self.control_child)
        self.assertTrue(MANIFEST_PATH.is_file(), MANIFEST_PATH)

        expected_files = {
            "routine": {"clamp.py", "test_prerequisites.py", "test_task.py"},
            "middle": {"clamp.py", "test_prerequisites.py", "test_task.py"},
            "heavy": {
                "clamp.py",
                "parse_numbers.py",
                "test_prerequisites.py",
                "test_task.py",
            },
        }
        self.assertEqual(set(self.manifest["task_bases"]), set(expected_files))
        gap_ids = set()
        for name, required_files in expected_files.items():
            entry = self.manifest["task_bases"][name]
            base = self._base_path(name)
            actual_files = {item.name for item in base.iterdir() if item.is_file()}
            self.assertEqual(actual_files, required_files, name)
            self.assertEqual(set(entry["required_files"]), required_files, name)
            self.assertFalse((base / "__init__.py").exists(), name)
            self.assertEqual(entry["expected_prerequisite_exit"], 0, name)
            self.assertEqual(entry["expected_designated_pre_task_exit"], 1, name)
            self.assertTrue(entry["self_contained"], name)
            self.assertTrue(entry["no_cross_base_imports"], name)
            gap_ids.add(entry["gap_id"])
            task_source = (base / "test_task.py").read_text(encoding="utf-8")
            self.assertIn(entry["gap_id"], task_source, name)

            siblings = set(expected_files) - {name}
            for source in base.glob("*.py"):
                source_text = source.read_text(encoding="utf-8")
                for sibling in siblings:
                    self.assertNotIn(sibling, source_text, f"{name}:{source.name}")

        self.assertEqual(len(gap_ids), 3)
        self.assertEqual(
            self.manifest["qualification_commands"]["control_ready"]["command"],
            "python -m unittest discover -s development/test-tools/tests -p test_fixture_controls.py",
        )
        self.assertEqual(
            self.manifest["qualification_commands"]["ordinary_combined_discovery"][
                "command"
            ],
            "python -m unittest discover -s development/test-tools/tests -p test*.py",
        )
        self.assertEqual(
            set(self.manifest["control_child_modes"]),
            {"terminal", "success", "record", "owner"},
        )

    def test_routine_prerequisite_and_designated_gap(self) -> None:
        name = "routine"
        entry = self.manifest["task_bases"][name]
        prerequisite = self._run_base(name, "prerequisite_command")
        task = self._run_base(name, "designated_task_command")

        self.assertEqual(
            prerequisite.returncode, entry["expected_prerequisite_exit"], prerequisite.stderr
        )
        self.assertEqual(
            task.returncode,
            entry["expected_designated_pre_task_exit"],
            task.stdout + task.stderr,
        )
        output = task.stdout + task.stderr
        self.assertIn(entry["gap_id"], output)
        other_gaps = {
            item["gap_id"]
            for other, item in self.manifest["task_bases"].items()
            if other != name
        }
        self.assertFalse(any(gap in output for gap in other_gaps))
        self._readback(
            {
                "behavior": "routine_base",
                "prerequisite_exit_code": prerequisite.returncode,
                "designated_task_exit_code": task.returncode,
                "gap_id": entry["gap_id"],
                "intended_failure_excerpt": self._excerpt(
                    output, entry["gap_id"]
                ),
            }
        )

    def test_middle_prerequisite_and_designated_gap(self) -> None:
        name = "middle"
        entry = self.manifest["task_bases"][name]
        prerequisite = self._run_base(name, "prerequisite_command")
        task = self._run_base(name, "designated_task_command")

        self.assertEqual(
            prerequisite.returncode, entry["expected_prerequisite_exit"], prerequisite.stderr
        )
        self.assertEqual(
            task.returncode,
            entry["expected_designated_pre_task_exit"],
            task.stdout + task.stderr,
        )
        output = task.stdout + task.stderr
        self.assertIn(entry["gap_id"], output)
        other_gaps = {
            item["gap_id"]
            for other, item in self.manifest["task_bases"].items()
            if other != name
        }
        self.assertFalse(any(gap in output for gap in other_gaps))
        self._readback(
            {
                "behavior": "middle_base",
                "prerequisite_exit_code": prerequisite.returncode,
                "designated_task_exit_code": task.returncode,
                "gap_id": entry["gap_id"],
                "intended_failure_excerpt": self._excerpt(
                    output, entry["gap_id"]
                ),
            }
        )

    def test_heavy_prerequisite_and_designated_gap(self) -> None:
        name = "heavy"
        entry = self.manifest["task_bases"][name]
        prerequisite = self._run_base(name, "prerequisite_command")
        task = self._run_base(name, "designated_task_command")

        self.assertEqual(
            prerequisite.returncode, entry["expected_prerequisite_exit"], prerequisite.stderr
        )
        self.assertEqual(
            task.returncode,
            entry["expected_designated_pre_task_exit"],
            task.stdout + task.stderr,
        )
        output = task.stdout + task.stderr
        self.assertIn(entry["gap_id"], output)
        other_gaps = {
            item["gap_id"]
            for other, item in self.manifest["task_bases"].items()
            if other != name
        }
        self.assertFalse(any(gap in output for gap in other_gaps))
        self._readback(
            {
                "behavior": "heavy_base",
                "prerequisite_exit_code": prerequisite.returncode,
                "designated_task_exit_code": task.returncode,
                "gap_id": entry["gap_id"],
                "intended_failure_excerpt": self._excerpt(
                    output, entry["gap_id"]
                ),
            }
        )

    def test_designated_task_files_do_not_poison_discovery(self) -> None:
        for name in self.manifest["task_bases"]:
            with self.subTest(name=name):
                result = self._run(
                    [
                        sys.executable,
                        "-m",
                        "unittest",
                        "discover",
                        "-s",
                        ".",
                        "-p",
                        "test_task.py",
                    ],
                    cwd=self._base_path(name),
                    timeout=5.0,
                )
                self.assertEqual(result.returncode, 5, result.stderr)
                self.assertIn("NO TESTS RAN", result.stderr, name)

    def test_control_child_terminal_refill_slow_success_and_statuses(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint = Path(temporary) / "success.json"
            slow = self._popen(
                [
                    sys.executable,
                    str(self.control_child),
                    "success",
                    "--checkpoint",
                    str(checkpoint),
                    "--delay",
                    "2.0",
                ]
            )
            slow_pid = slow.pid
            try:
                self.assertIsNone(slow.poll())

                early = self._run(
                    [
                        sys.executable,
                        str(self.control_child),
                        "terminal",
                        "--exit-code",
                        "2",
                    ],
                    timeout=2.0,
                )
                self.assertEqual(early.returncode, 2, early.stderr)
                self.assertEqual(
                    json.loads(early.stdout), {"mode": "terminal", "exit_code": 2}
                )

                refill = self._run(
                    [
                        sys.executable,
                        str(self.control_child),
                        "terminal",
                        "--exit-code",
                        "0",
                    ],
                    timeout=2.0,
                )
                self.assertEqual(refill.returncode, 0, refill.stderr)
                self.assertEqual(
                    json.loads(refill.stdout), {"mode": "terminal", "exit_code": 0}
                )
                self.assertIsNone(slow.poll())

                slow_status = self._wait(slow, timeout=5.0)
                self.assertEqual(slow_status, 0)
                self.assertEqual(
                    [slow_status, early.returncode, refill.returncode], [0, 2, 0]
                )
                self.assertTrue(checkpoint.exists(), checkpoint)
                checkpoint_value = json.loads(checkpoint.read_text(encoding="utf-8"))
                self.assertEqual(
                    checkpoint_value,
                    {
                        "mode": "success",
                        "pid": slow_pid,
                        "status": "complete",
                        "exit_code": 0,
                    },
                )
                self._readback(
                    {
                        "behavior": "early_terminal_slow_success_ready_refill",
                        "early_terminal_exit_code": early.returncode,
                        "ready_refill_exit_code": refill.returncode,
                        "slow_success_exit_code": slow_status,
                        "slow_was_running_before_refill": True,
                        "complete_exit_statuses": [
                            slow_status,
                            early.returncode,
                            refill.returncode,
                        ],
                        "checkpoint_preserved_after_producer_exit": True,
                        "checkpoint": checkpoint_value,
                    }
                )
            finally:
                self._cleanup_pids([slow_pid])

    def test_control_child_lost_handle_checkpoint_reconciliation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint = Path(temporary) / "record.json"
            child = self._popen(
                [
                    sys.executable,
                    str(self.control_child),
                    "record",
                    "--checkpoint",
                    str(checkpoint),
                    "--delay",
                    "1.0",
                ]
            )
            child_pid = child.pid
            # Intentionally detach the handle; this also prevents Popen.__del__
            # from emitting ResourceWarning for the still-running child.
            child.returncode = 0
            child = None
            try:
                initial = self._wait_for_checkpoint(checkpoint, timeout=5.0)
                self.assertEqual(initial["mode"], "record")
                self.assertEqual(initial["pid"], child_pid)
                self.assertEqual(initial["status"], "running")
                self.assertTrue(
                    self._wait_for_pid_state(child_pid, present=True, timeout=5.0)
                )

                final = self._wait_for_checkpoint(
                    checkpoint, status="complete", timeout=5.0
                )
                self.assertEqual(final["status"], "complete")
                self.assertEqual(final["exit_code"], 0)
                self.assertTrue(
                    self._wait_for_pid_state(child_pid, present=False, timeout=5.0)
                )
                self.assertTrue(checkpoint.exists(), checkpoint)
                self._readback(
                    {
                        "behavior": "lost_handle_reconciliation",
                        "pid_from_child_checkpoint": child_pid,
                        "status_before_reconciliation": initial["status"],
                        "status_after_reconciliation": final["status"],
                        "process_absent_after_complete": True,
                        "checkpoint_preserved_after_producer_exit": True,
                    }
                )
            finally:
                self._cleanup_pids([child_pid])

    def test_control_child_pid_identity_mismatch_is_safe_no_op(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint = Path(temporary) / "owner.json"
            owner = self._popen(
                [
                    sys.executable,
                    str(self.control_child),
                    "owner",
                    "--checkpoint",
                    str(checkpoint),
                    "--linger-seconds",
                    "20.0",
                ]
            )
            owner_pid = owner.pid
            descendant_pid: int | None = None
            try:
                owner_status = self._wait(owner, timeout=5.0)
                self.assertEqual(owner_status, 0)
                record = self._wait_for_checkpoint(checkpoint, timeout=5.0)
                self.assertEqual(record["mode"], "owner")
                self.assertEqual(record["parent_pid"], owner_pid)
                descendant_pid = record["descendant_pid"]
                self.assertIsInstance(descendant_pid, int)
                assert descendant_pid is not None
                self.assertNotEqual(descendant_pid, owner_pid)
                self.assertTrue(
                    self._wait_for_pid_state(
                        descendant_pid, present=True, timeout=5.0
                    )
                )

                checkpoint_identity = record.get("descendant_identity")
                identity = (
                    checkpoint_identity
                    if checkpoint_identity is not None
                    else self._process_creation_identity(descendant_pid)
                )
                if checkpoint_identity is not None:
                    self.assertEqual(
                        checkpoint_identity,
                        self._process_creation_identity(descendant_pid),
                    )
                self.assertIsNotNone(identity)
                assert identity is not None
                self._process_identities[descendant_pid] = identity
                mismatched = dict(identity)
                mismatched["creation_filetime"] = "mismatched-identity"

                with mock.patch.object(
                    subprocess, "run", wraps=subprocess.run
                ) as run:
                    mismatch_cleanup = self._terminate_pid_checked(
                        descendant_pid, mismatched
                    )
                    mismatch_taskkills = [
                        call
                        for call in run.call_args_list
                        if call.args
                        and call.args[0]
                        and call.args[0][0] == "taskkill"
                    ]
                alive_after_mismatch = self._pid_exists(descendant_pid)
                self.assertEqual(
                    (alive_after_mismatch, mismatch_taskkills),
                    (True, []),
                )
                self.assertIsNone(mismatch_cleanup)

                with mock.patch.object(
                    subprocess, "run", wraps=subprocess.run
                ) as run:
                    exact_cleanup = self._terminate_pid_checked(
                        descendant_pid, identity
                    )
                    exact_taskkills = [
                        call
                        for call in run.call_args_list
                        if call.args
                        and call.args[0]
                        and call.args[0][0] == "taskkill"
                    ]
                self.assertIsNotNone(exact_cleanup)
                assert exact_cleanup is not None
                self.assertEqual(exact_cleanup.returncode, 0)
                self.assertEqual(len(exact_taskkills), 1)
                self.assertTrue(
                    self._wait_for_pid_state(
                        descendant_pid, present=False, timeout=5.0
                    )
                )
                parent_absent = self._wait_for_pid_state(
                    owner_pid, present=False, timeout=5.0
                )
                self.assertTrue(parent_absent)
                self._readback(
                    {
                        "behavior": "pid_identity_mismatch_safe_no_op",
                        "owner_exit_code": owner_status,
                        "parent_pid": owner_pid,
                        "descendant_pid": descendant_pid,
                        "identity": identity,
                        "mismatched_identity": mismatched,
                        "mismatch_cleanup_result": None,
                        "process_alive_after_mismatch": True,
                        "taskkill_issued_after_mismatch": False,
                        "exact_cleanup_exit_code": exact_cleanup.returncode,
                        "taskkill_issued_for_exact_match": True,
                        "descendant_absent_after_exact_cleanup": True,
                        "parent_absent_after_owner_exit": parent_absent,
                    }
                )
            finally:
                pids = [owner_pid]
                if descendant_pid is not None:
                    pids.append(descendant_pid)
                self._cleanup_pids(pids)

    def test_control_child_owned_descendant_cleanup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint = Path(temporary) / "owner.json"
            owner = self._popen(
                [
                    sys.executable,
                    str(self.control_child),
                    "owner",
                    "--checkpoint",
                    str(checkpoint),
                    "--linger-seconds",
                    "20.0",
                ]
            )
            owner_pid = owner.pid
            descendant_pid: int | None = None
            try:
                owner_status = self._wait(owner, timeout=5.0)
                self.assertEqual(owner_status, 0)
                record = self._wait_for_checkpoint(checkpoint, timeout=5.0)
                self.assertEqual(record["mode"], "owner")
                self.assertEqual(record["parent_pid"], owner_pid)
                descendant_pid = record["descendant_pid"]
                self.assertIsInstance(descendant_pid, int)
                assert descendant_pid is not None
                self.assertNotEqual(descendant_pid, owner_pid)
                self.assertTrue(
                    self._wait_for_pid_state(descendant_pid, present=True, timeout=5.0)
                )
                descendant_identity = record.get("descendant_identity")
                self.assertIsNotNone(descendant_identity)
                assert descendant_identity is not None
                self._process_identities[descendant_pid] = descendant_identity

                cleanup = self._terminate_pid(
                    descendant_pid, descendant_identity
                )
                cleanup_exit = cleanup.returncode if cleanup is not None else 0
                cleanup_output = (
                    (cleanup.stdout + cleanup.stderr).strip()
                    if cleanup is not None
                    else ""
                )
                self.assertEqual(cleanup_exit, 0, cleanup_output)
                descendant_absent = self._wait_for_pid_state(
                    descendant_pid, present=False, timeout=5.0
                )
                self.assertTrue(descendant_absent)
                parent_absent = self._wait_for_pid_state(
                    owner_pid, present=False, timeout=5.0
                )
                self.assertTrue(parent_absent)
                self._readback(
                    {
                        "behavior": "owned_descendant_cleanup",
                        "owner_exit_code": owner_status,
                        "parent_pid": owner_pid,
                        "descendant_pid": descendant_pid,
                        "descendant_identity": descendant_identity,
                        "descendant_present_before_cleanup": True,
                        "cleanup_command": f"taskkill /PID {descendant_pid} /T /F",
                        "cleanup_exit_code": cleanup_exit,
                        "cleanup_output": cleanup_output,
                        "descendant_absent_after_cleanup": descendant_absent,
                        "parent_absent_after_owner_exit": parent_absent,
                    }
                )
            finally:
                pids = [owner_pid]
                if descendant_pid is not None:
                    pids.append(descendant_pid)
                self._cleanup_pids(pids)


if __name__ == "__main__":
    unittest.main()
