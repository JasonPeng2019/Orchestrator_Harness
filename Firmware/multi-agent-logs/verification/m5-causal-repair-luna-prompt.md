You are the independent GPT-5.6-luna high practical smoke tester for the focused M5 watcher repair
in the current repository. Read `active-working-spec/m5-watcher-causal-metrics-repair.md`. Do not
edit production code, tests, specs, plans, or existing evidence. Run host-only checks proving:

1. causal metrics use source event timestamps despite reversed watcher ingestion timestamps;
2. genuinely inverted source-stage order fails closed with a named contradiction;
3. analyzing the retained M5 S1 timeline in memory now gives nonnegative causal metrics for all
   four `sig-20260802-m5-s1-052110Z-*` events; and
4. the native wake practical and quiet-timeout control still pass using a fresh evidence directory
   under `multi-agent-logs/verification/m5-causal-repair-luna-evidence`.

You may run tests and create only that fresh verification evidence directory. Do not use hardware,
providers, MCP servers, evaluators, notifications, relays, runners, internal subagents, commit, or
push. Return exact commands, results, and any actionable failure. You advise; the root decides.
