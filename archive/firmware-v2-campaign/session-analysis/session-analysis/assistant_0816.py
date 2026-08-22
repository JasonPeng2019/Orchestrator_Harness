import json, io, os
f = r"C:\Users\Jason\.codex\sessions\2026\08\12\rollout-2026-08-12T21-52-35-019ff977-07cb-7a00-b549-a0cd3ddbef3c.jsonl"
outpath = r"C:\Users\Jason\Documents\Jason\Orchestrator_Harness\scratch\session-analysis\assistant-0816.txt"

def extract_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for c in content:
            if isinstance(c, dict) and c.get("type") in ("input_text", "output_text", "text"):
                parts.append(c.get("text", ""))
        return "\n".join(parts)
    return ""

rows = []
with open(f, "r", encoding="utf-8", errors="replace") as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except Exception:
            continue
        ts = ev.get("timestamp") or ""
        if not ts.startswith("2026-08-16"):
            continue
        t = ev.get("type")
        p = ev.get("payload") or {}
        if t == "response_item" and p.get("type") == "message" and p.get("role") == "assistant":
            txt = extract_text(p.get("content"))
            if txt.strip():
                rows.append((ts, txt))
        elif t == "event_msg" and p.get("type") == "message" and p.get("role") == "assistant":
            txt = extract_text(p.get("content"))
            if txt.strip():
                rows.append((ts, txt))

out = io.StringIO()
for ts, txt in rows:
    t = txt.replace("\n", " ").strip()
    out.write(f"[{ts}] {t}\n")
with open(outpath, "w", encoding="utf-8") as fh:
    fh.write(out.getvalue())
print("assistant messages on 08-16:", len(rows), "->", outpath, os.path.getsize(outpath))
