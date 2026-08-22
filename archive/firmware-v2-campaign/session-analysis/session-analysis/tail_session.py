import json
f = r"C:\Users\Jason\.codex\sessions\2026\08\12\rollout-2026-08-12T21-52-35-019ff977-07cb-7a00-b549-a0cd3ddbef3c.jsonl"
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
        rows.append(ev)
print("total events:", len(rows))
# print last 25 events summarized
for ev in rows[-25:]:
    ts = ev.get("timestamp")
    t = ev.get("type")
    p = ev.get("payload") or {}
    pt = p.get("type") if isinstance(p, dict) else None
    summary = ""
    if pt == "message":
        role = p.get("role")
        content = p.get("content")
        txt = ""
        if isinstance(content, list):
            for c in content:
                if isinstance(c, dict) and c.get("text"):
                    txt += c.get("text", "")[:200]
        summary = f"role={role} text={txt[:200]!r}"
    elif pt == "custom_tool_call":
        summary = f"tool={p.get('name')} args={str(p.get('arguments'))[:150]}"
    elif pt == "custom_tool_call_output":
        summary = f"output={str(p.get('output'))[:150]}"
    elif pt == "task_started" or pt == "task_complete" or pt == "turn_aborted":
        summary = f"turn={p.get('turn_id')} msg={str(p.get('last_agent_message'))[:150]}"
    elif pt == "thread_goal_updated":
        g = p.get("goal") or {}
        summary = f"status={g.get('status')} tokens={g.get('tokensUsed')}"
    elif pt == "reasoning":
        summary = f"reasoning len={len(str(p.get('summary') or p))}"
    elif pt == "token_count":
        summary = f"tokens={p}"
    else:
        summary = f"payload_type={pt}"
    print(f"[{ts}] {t}/{pt} {summary}")
