"""M02-A5 focused smoke probe: prove the six CONTROL-READY fixture behaviors
are expressible with Python stdlib + native OS controls alone.

Disposable probe evidence for the STEP-001 M02 helper-necessity decision.
This is NOT an M03 test asset and not an acceptance test; M03 owns
development/test-tools/tests/test_fixture_controls.py.
"""
from __future__ import annotations

import ctypes
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

K32 = ctypes.WinDLL("kernel32", use_last_error=True)
K32.OpenProcess.argtypes = (ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32)
K32.OpenProcess.restype = ctypes.c_void_p
K32.GetExitCodeProcess.argtypes = (ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint32))
K32.GetExitCodeProcess.restype = ctypes.c_int
K32.CloseHandle.argtypes = (ctypes.c_void_p,)
STILL_ACTIVE = 259


def liveness_readback(pid: int) -> object:
    handle = K32.OpenProcess(0x1000, False, pid)
    if not handle:
        return {"live": False, "exit_code": None}
    try:
        code = ctypes.c_uint32()
        ok = K32.GetExitCodeProcess(handle, ctypes.byref(code))
        if not ok:
            return {"live": None, "exit_code": None}
        if code.value == STILL_ACTIVE:
            return {"live": True, "exit_code": None}
        return {"live": False, "exit_code": int(code.value)}
    finally:
        K32.CloseHandle(handle)


def main() -> int:
    results = {}
    work = Path(tempfile.mkdtemp(prefix="m02-control-probe-"))
    py = sys.executable
    lingering_pids = []

    # 1. early incompatible terminal + 3. complete status
    early = subprocess.Popen([py, "-c", "import sys; sys.exit(3)"])
    results["early_terminal_exit"] = early.wait(timeout=30)

    # 2. independent slow success and ready refill
    checkpoint = work / "checkpoint.json"
    slow = subprocess.Popen(
        [py, "-c",
         "import json,time;time.sleep(1.5);"
         f"open(r'{checkpoint}','w',encoding='utf-8').write(json.dumps({{'state':'complete','step':'slow'}}))"]
    )
    refill = subprocess.Popen([py, "-c", "import sys; sys.exit(0)"])
    refill_exit = refill.wait(timeout=30)
    refill_was_ready_while_slow_ran = slow.poll() is None
    slow_exit = slow.wait(timeout=30)
    results["refill_exit"] = refill_exit
    results["refill_completed_while_slow_running"] = refill_was_ready_while_slow_ran
    results["slow_exit"] = slow_exit

    # 5. preserved checkpoint (read back after the producing child exited)
    results["checkpoint_preserved"] = (
        checkpoint.is_file()
        and json.loads(checkpoint.read_text(encoding="utf-8"))["state"] == "complete"
    )

    # 4. lost-handle reconciliation via a child-written record + stdlib liveness readback
    record = work / "reconcile.json"
    child = subprocess.Popen(
        [py, "-c",
         "import json,os,sys,time;"
         f"open(r'{record}','w',encoding='utf-8').write(json.dumps({{'pid':os.getpid(),'state':'running'}}));"
         "time.sleep(0.8)"]
    )
    child_pid = child.pid
    del child  # handle intentionally lost; record is the reconciliation channel
    time.sleep(1.6)
    record_state = json.loads(record.read_text(encoding="utf-8"))
    results["reconciled_pid_matches"] = record_state["pid"] == child_pid
    results["reconciled_liveness"] = liveness_readback(child_pid)

    # 6. lingering owned descendant with actual cleanup attempt and exit readback
    marker = work / "grandchild.pid"
    parent = subprocess.Popen(
        [py, "-c",
         "import subprocess,sys;"
         f"c=subprocess.Popen([sys.executable,'-c','import time;time.sleep(20)']);"
         f"open(r'{marker}','w',encoding='utf-8').write(str(c.pid))"]
    )
    parent_exit = parent.wait(timeout=30)
    grandchild_pid = int(marker.read_text(encoding="utf-8").strip())
    lingering_pids.append(grandchild_pid)
    time.sleep(0.4)
    results["descendant_live_after_owner_exit"] = liveness_readback(grandchild_pid)
    cleanup = subprocess.run(
        ["taskkill", "/PID", str(grandchild_pid), "/T", "/F"],
        capture_output=True, text=True,
    )
    results["cleanup_attempt_exit"] = cleanup.returncode
    time.sleep(0.4)
    results["descendant_after_cleanup"] = liveness_readback(grandchild_pid)
    results["parent_exit"] = parent_exit

    # safety cleanup of any surviving probe child
    final = []
    for pid in lingering_pids:
        readback = liveness_readback(pid)
        if readback.get("live"):
            subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"],
                           capture_output=True, text=True)
            readback = liveness_readback(pid)
        final.append({"pid": pid, "readback": readback})
    results["probe_cleanup_readback"] = final

    results["ok"] = (
        results["early_terminal_exit"] == 3
        and results["refill_exit"] == 0
        and results["refill_completed_while_slow_running"] is True
        and results["slow_exit"] == 0
        and results["checkpoint_preserved"] is True
        and results["reconciled_pid_matches"] is True
        and results["reconciled_liveness"]["live"] is False
        and results["descendant_live_after_owner_exit"]["live"] is True
        and results["cleanup_attempt_exit"] == 0
        and results["descendant_after_cleanup"]["live"] is False
    )
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0 if results["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
