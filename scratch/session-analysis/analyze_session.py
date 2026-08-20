import json, collections, sys, io

f = r"C:\Users\Jason\.codex\sessions\2026\08\12\rollout-2026-08-12T21-52-35-019ff977-07cb-7a00-b549-a0cd3ddbef3c.jsonl"

type_counts = collections.Counter()
payload_type_counts = collections.Counter()
user_msgs = []
final_msgs = []
plan_updates = []
tool_calls = []
compactions = []
goals = []
meta = None

def text_of(payload):
    # try common fields
    for key in ("text", "message", "content"):
        v = payload.get(key)
        if isinstance(v, str):
            return v
    return None

with open(f, "r", encoding="utf-8", errors="replace") as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except Exception:
            type_counts["<parse-error>"] += 1
            continue
        t = ev.get("type")
        type_counts[t] += 1
        payload = ev.get("payload") or {}
        if isinstance(payload, dict):
            pt = payload.get("type")
            if pt:
                payload_type_counts[pt] += 1
            if t == "session_meta":
                meta = payload
            if pt == "thread_goal_updated":
                goals.append(payload.get("goal") or {})
            if pt == "user_message":
                txt = text_of(payload)
                user_msgs.append((ev.get("timestamp"), txt))
            if pt == "agent_message" or pt == "assistant_message":
                txt = text_of(payload)
                if txt:
                    final_msgs.append((ev.get("timestamp"), txt))
            if pt == "compaction" or pt == "context_compaction":
                compactions.append((ev.get("timestamp"), payload))
            if pt == "tool_call" or pt == "tool_use":
                name = payload.get("name") or (payload.get("tool_use") or {}).get("name")
                tool_calls.append((ev.get("timestamp"), name))
            if pt == "plan_update":
                plan_updates.append((ev.get("timestamp"), payload))

out = io.StringIO()
def w(*a):
    print(*a, file=out)

w("=== EVENT TYPE COUNTS ===")
for k, v in type_counts.most_common():
    w(f"{k}: {v}")
w()
w("=== PAYLOAD TYPES (event_msg) ===")
for k, v in payload_type_counts.most_common():
    w(f"{k}: {v}")
w()
w("=== SESSION META ===")
if meta:
    w("session_id:", meta.get("session_id"))
    w("cwd:", meta.get("cwd"))
    w("originator:", meta.get("originator"))
    w("cli_version:", meta.get("cli_version"))
    w("model_provider:", meta.get("model_provider"))
    w("git:", meta.get("git"))
w()
w("=== GOALS ===")
for g in goals[-5:]:
    w(json.dumps(g, default=str)[:500])
w()
w("=== USER MESSAGES (count=%d) ===" % len(user_msgs))
for ts, txt in user_msgs:
    t = (txt or "").replace("\n", " ")[:300]
    w(f"[{ts}] {t}")
w()
w("=== FINAL/AGENT MESSAGES (count=%d) ===" % len(final_msgs))
for ts, txt in final_msgs[-40:]:
    t = (txt or "").replace("\n", " ")[:400]
    w(f"[{ts}] {t}")
w()
w("=== PLAN UPDATES (count=%d) ===" % len(plan_updates))
for ts, p in plan_updates[-20:]:
    w(f"[{ts}] {json.dumps(p, default=str)[:600]}")
w()
w("=== TOOL CALLS (count=%d) ===" % len(tool_calls))
tc = collections.Counter(n for _, n in tool_calls if n)
for k, v in tc.most_common(30):
    w(f"{k}: {v}")
w()
w("=== COMPACTIONS (count=%d) ===" % len(compactions))
for ts, p in compactions:
    w(f"[{ts}] {json.dumps(p, default=str)[:300]}")

sys.stdout.write(out.getvalue())
