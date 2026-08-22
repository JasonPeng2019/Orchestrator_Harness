import json

f = r"C:\Users\Jason\.codex\sessions\2026\08\12\rollout-2026-08-12T21-52-35-019ff977-07cb-7a00-b549-a0cd3ddbef3c.jsonl"
targets = {"response_item": 3, "event_msg": 0}
shown = {"response_item": 0, "message": 0, "custom_tool_call": 0, "task_started": 0, "task_complete": 0, "compacted": 0, "turn_aborted": 0, "function_call": 0}
with open(f, "r", encoding="utf-8", errors="replace") as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except Exception:
            continue
        t = ev.get("type")
        if t == "response_item" and shown["response_item"] < 3:
            shown["response_item"] += 1
            print("=== response_item ===")
            print(json.dumps(ev, default=str)[:2000])
            print()
        if t == "event_msg":
            p = ev.get("payload") or {}
            pt = p.get("type")
            if pt in shown and shown[pt] < 2:
                shown[pt] += 1
                print(f"=== event_msg/{pt} ===")
                print(json.dumps(ev, default=str)[:2000])
                print()
        if t == "compacted" and shown["compacted"] < 2:
            shown["compacted"] += 1
            print("=== compacted ===")
            print(json.dumps(ev, default=str)[:2000])
            print()
