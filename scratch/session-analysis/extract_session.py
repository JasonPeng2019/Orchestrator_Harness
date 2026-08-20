import json, collections, io, sys, os

f = r"C:\Users\Jason\.codex\sessions\2026\08\12\rollout-2026-08-12T21-52-35-019ff977-07cb-7a00-b549-a0cd3ddbef3c.jsonl"
outpath = r"C:\Users\Jason\Documents\Jason\Orchestrator_Harness\scratch\session-analysis\extract-session-001.output.txt"

user_msgs = []
assistant_msgs = []
tool_calls = []
plan_updates = []
turns = []
compactions = []
goals = []

def extract_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for c in content:
            if isinstance(c, dict):
                if c.get("type") in ("input_text", "output_text", "text"):
                    parts.append(c.get("text", ""))
        return "\n".join(parts)
    return ""

with open(f, "r", encoding="utf-8", errors="replace") as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except Exception:
            continue
        ts = ev.get("timestamp")
        t = ev.get("type")
        p = ev.get("payload") or {}
        if t == "response_item":
            pt = p.get("type")
            if pt == "message":
                role = p.get("role")
                txt = extract_text(p.get("content"))
                if role == "user" and txt.strip():
                    user_msgs.append((ts, txt))
                elif role == "assistant" and txt.strip():
                    assistant_msgs.append((ts, txt))
        elif t == "event_msg":
            pt = p.get("type")
            if pt == "message":
                role = p.get("role")
                txt = extract_text(p.get("content"))
                if role == "user" and txt.strip():
                    user_msgs.append((ts, txt))
                elif role == "assistant" and txt.strip():
                    assistant_msgs.append((ts, txt))
            elif pt == "custom_tool_call":
                name = p.get("name") or ""
                args = p.get("arguments") or p.get("input") or {}
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except Exception:
                        args = {"raw": args[:200]}
                tool_calls.append((ts, name, args))
            elif pt == "function_call":
                name = p.get("name") or ""
                args = p.get("arguments") or {}
                tool_calls.append((ts, name, args))
            elif pt == "task_started":
                turns.append((ts, "task_started", p.get("turn_id"), ""))
            elif pt == "task_complete":
                turns.append((ts, "task_complete", p.get("turn_id"), (p.get("last_agent_message") or "")[:200]))
            elif pt == "turn_aborted":
                turns.append((ts, "turn_aborted", p.get("turn_id"), p.get("reason") or ""))
            elif pt == "thread_goal_updated":
                g = p.get("goal") or {}
                goals.append(g)
        elif t == "compacted":
            rh = p.get("replacement_history") or []
            summary = ""
            for item in rh:
                if isinstance(item, dict) and item.get("role") == "user":
                    summary += extract_text(item.get("content"))[:2000] + "\n---\n"
            compactions.append((ts, summary))

out = io.StringIO()
def w(*a):
    print(*a, file=out)

w("=== USER MESSAGES (count=%d) ===" % len(user_msgs))
for i, (ts, txt) in enumerate(user_msgs):
    t = txt.replace("\n", " ").strip()
    w(f"[{i}] [{ts}] {t[:600]}")
w()
w("=== ASSISTANT MESSAGES (count=%d) ===" % len(assistant_msgs))
for i, (ts, txt) in enumerate(assistant_msgs):
    t = txt.replace("\n", " ").strip()
    w(f"[{i}] [{ts}] {t[:400]}")
w()
w("=== TOOL CALLS (count=%d) ===" % len(tool_calls))
tc = collections.Counter(n for _, n, _ in tool_calls if n)
for k, v in tc.most_common(40):
    w(f"{k}: {v}")
w()
w("=== PLAN UPDATES (count=%d) ===" % len(plan_updates))
for ts, ptxt in plan_updates[-30:]:
    w(f"[{ts}] {ptxt[:800]}")
w()
w("=== TURN LIFECYCLE (count=%d) ===" % len(turns))
for ts, kind, tid, detail in turns[-80:]:
    w(f"[{ts}] {kind} {tid} {detail[:150]}")
w()
w("=== COMPACTIONS (count=%d) ===" % len(compactions))
for ts, s in compactions:
    w(f"[{ts}] {s[:2000]}")
w()
w("=== GOAL (latest) ===")
if goals:
    w(json.dumps(goals[-1], default=str)[:800])

with open(outpath, "w", encoding="utf-8") as fh:
    fh.write(out.getvalue())
print("WROTE", outpath, "bytes=", os.path.getsize(outpath))
