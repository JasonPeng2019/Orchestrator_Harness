from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POWERSHELL = Path("C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe")
SUPERVISOR = ROOT / ".codex" / "scripts" / "Invoke-BoundedTest.ps1"


def _invoke(
    tmp_path: Path,
    command: str,
    *,
    expected_upper_bound: int,
    cleanup_allowance: int,
    maximum_lifetime: int | None = None,
    heartbeat: int = 1,
    supervisor: Path | None = None,
) -> tuple[subprocess.CompletedProcess[str], Path]:
    result_path = tmp_path / "result.json"
    maximum = expected_upper_bound + cleanup_allowance if maximum_lifetime is None else maximum_lifetime
    completed = subprocess.run(
        [
            str(POWERSHELL),
            "-NoLogo",
            "-NoProfile",
            "-NonInteractive",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(supervisor if supervisor is not None else SUPERVISOR),
            "-Command",
            command,
            "-WorkingDirectory",
            str(tmp_path),
            "-MaximumLifetimeSeconds",
            str(maximum),
            "-ExpectedUpperBoundSeconds",
            str(expected_upper_bound),
            "-CleanupAllowanceSeconds",
            str(cleanup_allowance),
            "-HeartbeatIntervalSeconds",
            str(heartbeat),
            "-TimeoutBasis",
            "Unit-test evidence for the declared upper bound.",
            "-ResultPath",
            str(result_path),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )
    return completed, result_path


def _result(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf")
    value = json.loads(raw.decode("utf-8"))
    assert isinstance(value, dict)
    return value


def test_supervisor_preserves_success_and_calibration(tmp_path: Path) -> None:
    completed, path = _invoke(
        tmp_path,
        "Write-Output 'bounded pass'",
        expected_upper_bound=5,
        cleanup_allowance=1,
    )
    assert completed.returncode == 0, completed.stderr
    result = _result(path)
    assert result["status"] == "PASSED"
    assert result["exit_code"] == 0
    assert result["maximum_lifetime_seconds"] == 6
    assert result["expected_upper_bound_seconds"] == 5
    assert result["cleanup_allowance_seconds"] == 1
    assert result["cleanup_verified"] is True


def test_supervisor_preserves_child_failure_exit_code(tmp_path: Path) -> None:
    completed, path = _invoke(
        tmp_path,
        "Write-Error 'intentional failure'; exit 7",
        expected_upper_bound=5,
        cleanup_allowance=1,
    )
    assert completed.returncode != 0
    result = _result(path)
    assert result["status"] == "FAILED"
    assert result["exit_code"] == 7


def test_supervisor_rejects_padded_two_minute_deadline(tmp_path: Path) -> None:
    completed, path = _invoke(
        tmp_path,
        "Write-Output 'must not launch'",
        expected_upper_bound=120,
        cleanup_allowance=30,
        maximum_lifetime=600,
    )
    assert completed.returncode != 0
    assert not path.exists()
    assert "must equal ExpectedUpperBoundSeconds plus CleanupAllowanceSeconds" in completed.stderr


def test_supervisor_rejects_deadline_below_twenty_minute_bound(tmp_path: Path) -> None:
    completed, path = _invoke(
        tmp_path,
        "Write-Output 'must not launch'",
        expected_upper_bound=1200,
        cleanup_allowance=120,
        maximum_lifetime=600,
    )
    assert completed.returncode != 0
    assert not path.exists()
    assert "must equal ExpectedUpperBoundSeconds plus CleanupAllowanceSeconds" in completed.stderr


def test_supervisor_rejects_excessive_cleanup_padding(tmp_path: Path) -> None:
    completed, path = _invoke(
        tmp_path,
        "Write-Output 'must not launch'",
        expected_upper_bound=120,
        cleanup_allowance=120,
    )
    assert completed.returncode != 0
    assert not path.exists()
    assert "CleanupAllowanceSeconds=120 is excessive" in completed.stderr
    assert "30 seconds" in completed.stderr


def test_supervisor_times_out_and_cleans_descendant_tree(tmp_path: Path) -> None:
    command = (
        "Start-Process powershell.exe "
        "-ArgumentList '-NoProfile','-Command','Start-Sleep -Seconds 30' "
        "-WindowStyle Hidden; Start-Sleep -Seconds 30"
    )
    completed, path = _invoke(
        tmp_path,
        command,
        expected_upper_bound=1,
        cleanup_allowance=1,
    )
    assert completed.returncode != 0
    result = _result(path)
    assert result["status"] == "TIMED_OUT"
    assert result["exit_code"] == 124
    assert result["cleanup_verified"] is True
    observed = result["observed_process_ids"]
    assert isinstance(observed, list)
    assert len(observed) >= 3
    assert "RUNNING" in completed.stdout
    assert "TIMED_OUT" in completed.stdout


def test_timeout_tolerates_taskkill_stderr_via_shim(tmp_path: Path) -> None:
    shim = tmp_path / "taskkill.cmd"
    shim.write_text(
        "@echo off\r\n%SystemRoot%\\System32\\taskkill.exe %*\r\necho deterministic-shim-stderr 1>&2\r\nexit /b 7\r\n",
        encoding="utf-8",
    )
    supervisor_text = SUPERVISOR.read_text(encoding="utf-8")
    literal = '"$env:SystemRoot\\System32\\taskkill.exe"'
    assert literal in supervisor_text
    patched = supervisor_text.replace(literal, "'" + str(shim) + "'")
    patched_supervisor = tmp_path / "Invoke-BoundedTest-Shim.ps1"
    patched_supervisor.write_text(patched, encoding="utf-8")
    completed, path = _invoke(
        tmp_path,
        "Start-Sleep -Seconds 30",
        expected_upper_bound=1,
        cleanup_allowance=1,
        supervisor=patched_supervisor,
    )
    assert completed.returncode != 0
    result = _result(path)
    assert result["status"] == "TIMED_OUT"
    assert result["exit_code"] == 124
    assert result["cleanup_verified"] is True
    assert "TIMED_OUT" in completed.stdout
