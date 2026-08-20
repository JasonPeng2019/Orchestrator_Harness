import json
f = r"C:\Users\Jason\.codex\sessions\2026\08\12\rollout-2026-08-12T21-52-35-019ff977-07cb-7a00-b549-a0cd3ddbef3c.jsonl"
goals = []
with open(f, "r", encoding="utf-8", errors="replace") as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except Exception:
            continue
        p = ev.get("payload") or {}
        if isinstance(p, dict) and p.get("type") == "thread_goal_updated":
            g = p.get("goal") or {}
            goals.append((ev.get("timestamp"), g.get("status"), g.get("tokensUsed"), (g.get("objective") or "")[:120]))
out = []
for ts, st, tok, obj in goals:
    out.append(f"[{ts}] status={st} tokens={tok} obj={obj}")
with open(r"C:\Users\Jason\Documents\Jason\Orchestrator_Harness\scratch\session-analysis\goal-history.txt", "w", encoding="utf-8") as fh:
    fh.write("\n".join(out))
print("goal updates:", len(goals))
