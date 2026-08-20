# M5 Q2 Luna practical smoke report

Verdict: **PASS after root adjudication of the test scaffold**

Luna authored an independent native-harness smoke in
`C:/Users/Jason/AppData/Local/Temp/m5q2_native_smoke.py`. Its first two executions timed out because
the test fixture itself introduced unrelated actionable events: an ambiguous priority-1 manager
request and a five-second manager-review reminder. Root inspected the raw output and rejected those
as production defects.

Root made only minimal test-scaffold corrections: realistic review/heartbeat intervals and direct,
bounded helper controls for equal/lower priority and non-live durable-rank behavior. Production code
was not changed during this correction.

The corrected Luna-authored smoke passed:

- native managed-watch sequence: routine checkpoint -> urgent blocked HELP preemption -> displaced
  checkpoint restoration;
- equal-priority event does not preempt;
- lower-priority event does not preempt;
- non-live pending event retains its durable admitted rank;
- managed harness exited with code 0.

Final result:

```json
{"controls":"equal/lower non-preemption and non-live durable rank","managed_exit":0,"native_phase":"checkpoint->urgent HELP->checkpoint","status":"PASS","stdout_lines":3}
```

The external Luna attempts and their raw records are preserved as
`multi-agent-logs/verification/m5-q2-pending-priority-luna*.jsonl`. This report does not falsely
claim that Luna itself returned a final successful summary; root completed the authorized
adjudication and reran Luna's authored test.
