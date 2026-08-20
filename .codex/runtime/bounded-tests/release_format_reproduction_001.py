from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


GUIDE = Path("harness_watcher_implementation/CANARY_GUIDE.md")


def normalize() -> None:
    data = GUIDE.read_bytes()
    non_ascii = [(index, byte) for index, byte in enumerate(data) if byte >= 128]
    assert non_ascii == [(26, 0x97)], non_ascii
    text = data.decode("cp1252")
    assert text.encode("cp1252") == data
    normalized = text.encode("utf-8")
    GUIDE.write_bytes(normalized)
    assert GUIDE.read_bytes().decode("utf-8") == text
    assert text.encode("cp1252") == data
    print(f"normalized {GUIDE}: {len(data)} -> {len(normalized)} bytes")


def scan() -> None:
    completed = subprocess.run(
        ["git", "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    paths = [Path(raw.decode("utf-8")) for raw in completed.stdout.split(b"\0") if raw]
    checked = 0
    for path in paths:
        if path.is_file():
            path.read_bytes().decode("utf-8")
            checked += 1
    print(f"strict UTF-8: {checked} tracked files")


parser = argparse.ArgumentParser()
parser.add_argument("operation", choices=("normalize", "scan"))
args = parser.parse_args()
normalize() if args.operation == "normalize" else scan()
