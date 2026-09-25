#!/usr/bin/env python3
"""Finite subprocess fixtures for independent CONTROL-READY boundary checks."""

from __future__ import annotations

import argparse
import ctypes
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


def emit(record: dict[str, Any]) -> None:
    print(json.dumps(record, sort_keys=True, separators=(",", ":")), flush=True)


def write_checkpoint(path: str, record: dict[str, Any]) -> None:
    target = Path(path).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(f"{target.name}.{os.getpid()}.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(record, handle, sort_keys=True, separators=(",", ":"))
        handle.write("\n")
    os.replace(temporary, target)


def run_terminal(code: int) -> int:
    emit({"mode": "terminal", "exit_code": code})
    return code


def run_success(checkpoint: str, delay: float) -> int:
    time.sleep(delay)
    record = {
        "mode": "success",
        "pid": os.getpid(),
        "status": "complete",
        "exit_code": 0,
    }
    write_checkpoint(checkpoint, record)
    emit(
        {
            "mode": "success",
            "checkpoint": str(Path(checkpoint).resolve()),
            "pid": os.getpid(),
        }
    )
    return 0


def run_record(checkpoint: str, delay: float) -> int:
    write_checkpoint(
        checkpoint,
        {
            "mode": "record",
            "pid": os.getpid(),
            "status": "running",
            "exit_code": None,
        },
    )
    time.sleep(delay)
    write_checkpoint(
        checkpoint,
        {
            "mode": "record",
            "pid": os.getpid(),
            "status": "complete",
            "exit_code": 0,
        },
    )
    emit(
        {
            "mode": "record",
            "checkpoint": str(Path(checkpoint).resolve()),
            "pid": os.getpid(),
        }
    )
    return 0


def process_creation_identity(pid: int) -> dict[str, Any] | None:
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
            value = (creation.dwHighDateTime << 32) | creation.dwLowDateTime
            return {
                "pid": pid,
                "creation_filetime": f"windows-filetime:{value}",
            }
        finally:
            kernel32.CloseHandle(handle)
    except (OSError, ValueError, AttributeError):
        return None


def run_owner(checkpoint: str, linger_seconds: float) -> int:
    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "linger",
        "--seconds",
        str(linger_seconds),
    ]
    creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    descendant = subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=creationflags,
    )
    descendant_identity = process_creation_identity(descendant.pid)
    write_checkpoint(
        checkpoint,
        {
            "mode": "owner",
            "parent_pid": os.getpid(),
            "descendant_pid": descendant.pid,
            "descendant_identity": descendant_identity,
            "status": "spawned",
            "descendant_command": command,
        },
    )
    emit(
        {
            "mode": "owner",
            "checkpoint": str(Path(checkpoint).resolve()),
            "parent_pid": os.getpid(),
            "descendant_pid": descendant.pid,
        }
    )
    return 0


def run_linger(seconds: float) -> int:
    time.sleep(seconds)
    emit({"mode": "linger", "pid": os.getpid(), "seconds": seconds})
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="mode", required=True)

    terminal = subparsers.add_parser("terminal")
    terminal.add_argument("--exit-code", type=int, required=True)

    success = subparsers.add_parser("success")
    success.add_argument("--checkpoint", required=True)
    success.add_argument("--delay", type=float, required=True)

    record = subparsers.add_parser("record")
    record.add_argument("--checkpoint", required=True)
    record.add_argument("--delay", type=float, required=True)

    owner = subparsers.add_parser("owner")
    owner.add_argument("--checkpoint", required=True)
    owner.add_argument("--linger-seconds", type=float, required=True)

    linger = subparsers.add_parser("linger", help=argparse.SUPPRESS)
    linger.add_argument("--seconds", type=float, required=True)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.mode in {"success", "record"} and args.delay < 0:
        parser.error("--delay must be non-negative")
    if args.mode == "linger" and args.seconds < 0:
        parser.error("--seconds must be non-negative")

    if args.mode == "terminal":
        return run_terminal(args.exit_code)
    if args.mode == "success":
        return run_success(args.checkpoint, args.delay)
    if args.mode == "record":
        return run_record(args.checkpoint, args.delay)
    if args.mode == "owner":
        return run_owner(args.checkpoint, args.linger_seconds)
    if args.mode == "linger":
        return run_linger(args.seconds)
    parser.error(f"unsupported mode: {args.mode}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
