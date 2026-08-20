from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


def findings(root: Path) -> Counter[tuple[str, str, str]]:
    completed = subprocess.run(
        [sys.executable, "-m", "ruff", "check", ".", "--output-format", "json"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode not in (0, 1):
        raise RuntimeError(completed.stderr or completed.stdout)
    records = json.loads(completed.stdout)
    normalized: Counter[tuple[str, str, str]] = Counter()
    for record in records:
        filename = Path(record["filename"])
        absolute = filename if filename.is_absolute() else root / filename
        relative = absolute.resolve().relative_to(root.resolve()).as_posix()
        message = re.sub(r"\bline \d+\b", "line <n>", record["message"])
        normalized[(relative, record["code"], message)] += 1
    return normalized


parser = argparse.ArgumentParser()
parser.add_argument("parent", type=Path)
parser.add_argument("tip", type=Path)
args = parser.parse_args()
parent = findings(args.parent.resolve())
tip = findings(args.tip.resolve())
introduced = tip - parent
print(
    json.dumps(
        {
            "parent_finding_count": parent.total(),
            "tip_finding_count": tip.total(),
            "introduced_finding_count": introduced.total(),
            "introduced": [
                {"path": key[0], "code": key[1], "message": key[2], "count": count}
                for key, count in sorted(introduced.items())
            ],
        },
        indent=2,
    )
)
if introduced:
    raise SystemExit(1)
