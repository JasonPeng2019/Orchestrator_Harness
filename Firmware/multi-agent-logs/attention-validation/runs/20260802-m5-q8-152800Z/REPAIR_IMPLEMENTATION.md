# Q8 publication repair implementation

Coder: GPT-5.6-terra medium
Result: **PASS**

Added passive `AGENT_SIGNAL_PUBLISHED` evidence, exact captured
`record-attention --source-timestamp-utc`, publication-based detection metrics, and fail-closed
missing/duplicate/mismatched/reversed/post-deadline handling. No harness scheduling, wake transport,
manager logic, worker controller, or runtime assistance changed.

Focused tests: **36 passed, 3 subtests**. Full watcher suite: **98 passed, 27 subtests**. Attention
practical: **PASS**. No commit.
