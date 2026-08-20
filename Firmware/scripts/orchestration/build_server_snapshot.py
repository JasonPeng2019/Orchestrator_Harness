from __future__ import annotations

import hashlib
import json
import struct
import subprocess
import sys
from pathlib import Path

SUITE_ROOT = Path(__file__).resolve().parents[2]
SERVER_ROOT = SUITE_ROOT / "BYO-Firmware-MCP"
DEFAULT_OUTPUT = (
    SUITE_ROOT / ".agent-workspace" / "server-snapshots" / "server-snapshot.json"
)
OUTPUT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_OUTPUT


def git(*args: str, input_bytes: bytes | None = None) -> bytes:
    return subprocess.run(
        ["git", *args],
        cwd=SERVER_ROOT,
        input=input_bytes,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout


head = git("rev-parse", "HEAD").decode("ascii").strip()
diff = git("diff", "--binary", "HEAD", "--", "src")
dirty_fingerprint = (
    git("hash-object", "--stdin", input_bytes=diff).decode("ascii").strip()
)
paths = sorted(
    path for path in git("ls-files", "src").decode("utf-8").splitlines() if path
)

tree_digest = hashlib.sha256()
files: list[dict[str, object]] = []
for relative in paths:
    data = (SERVER_ROOT / relative).read_bytes()
    encoded_path = relative.encode("utf-8")
    tree_digest.update(encoded_path)
    tree_digest.update(b"\0")
    tree_digest.update(struct.pack(">Q", len(data)))
    tree_digest.update(data)
    files.append(
        {
            "path": relative,
            "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
    )

document = {
    "schema": "firmware-suite-server-snapshot/v1",
    "head": head,
    "tracked_dirty_diff_fingerprint": dirty_fingerprint,
    "tracked_dirty_diff_method": "git diff --binary HEAD -- src | git hash-object --stdin",
    "production_src_tree_sha256": tree_digest.hexdigest(),
    "production_src_tree_method": (
        "SHA-256 over sorted git ls-files src; for each: UTF-8 path + NUL + "
        "uint64be byte length + working-tree bytes"
    ),
    "tracked_src_file_count": len(files),
    "files": files,
}
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8", newline="\n")
print(f"manifest={OUTPUT}")
print(f"head={head}")
print(f"diff={dirty_fingerprint}")
print(f"tree={tree_digest.hexdigest()}")
print(f"files={len(files)}")
print(f"manifest_sha256={hashlib.sha256(OUTPUT.read_bytes()).hexdigest()}")
