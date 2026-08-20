# Clean-H optional-watcher epoch-baseline repair plan

Authority: current root manager  
Audit: `.agent-workspace/CANARY_AUDIT_20260731_S1_CLEAN_H.md`  
Scope: optional `harness_watcher_implementation` startup/cursor behavior only; no primary harness,
production server, experiment, MCP/provider, or hardware behavior

## Verified defect

The new Clean-H optional-watcher runtime began with no cursor. Its `serve` loop immediately called
`poll()`, whose empty-cursor behavior read the existing tails of manager, harness, and lane logs as
new work. The evaluator consequently emitted startup alert `hwa-76af35289457892226edceef` about
historical pre-epoch material, even though the primary historical-lifetime defect had already been
repaired and later Clean-H polls found no current defect.

Direct one-shot `poll` behavior is intentionally useful for fixtures and diagnostics. The defect is
the background service treating bytes that predate a brand-new watcher epoch/runtime as new
current-epoch observations.

## Required behavior

Implement the smallest correction in `harness_watcher_implementation/poller.py`,
`harness_watcher_implementation/__main__.py`, and focused tests.

1. Before a **brand-new background service runtime** performs its first poll, atomically seed a
   cursor for every source that already exists at that source's current EOF/file identity.
2. Baseline only when the runtime has no cursor. A service restart/resume with an existing cursor
   must preserve the durable cursor and must not skip unread material.
3. Do not retain pre-baseline tail text as no-progress context and do not later submit that
   historical generation merely because the no-progress threshold expires.
4. Records appended after the baseline must be read, routed, and evaluated normally. A source
   absent at baseline and created afterward must also be read normally.
5. File truncation or replacement after baseline must retain current fail-safe `_read` behavior and
   be treated as new observable content.
6. Preserve direct CLI/public `poll()` semantics, alert validation/deduplication, routing to the four
   watcher trees, service ownership/stop behavior, evaluator model/configuration, and the current
   filtering of watcher-derived and resolved-transient records.
7. Do not filter by timestamps or message contents, delete/rewrite source logs, special-case the
   Clean-H alert, suppress all first polls, or alter the primary harness.

## Accepted one-way-door decision

Epoch membership is defined operationally by the cursor established at brand-new background
service startup: preexisting bytes are historical; bytes that arrive after that baseline are
current. This is an EOF/file-identity boundary, not a heuristic timestamp filter. Once a cursor
exists it is authoritative and is never silently re-baselined.

## Focused tests

Use synthetic temporary logs only; no agents, server, provider, or hardware.

- A brand-new service baseline over a preexisting defect-shaped log produces no evaluation/alert.
- A genuine defect-shaped record appended after baseline is evaluated and can alert.
- Restart/initialization with an existing cursor is a no-op and preserves unread bytes rather than
  advancing the offset.
- A source missing during baseline and created afterward is evaluated normally.
- Pre-baseline bytes cannot reappear as no-progress evaluator context.
- Existing direct `poll()` tests remain green, proving the public diagnostic behavior was not
  changed.

Run the focused watcher unit module first. Then run the complete ordinary optional-watcher host
suite exactly once. Do not rerun the primary harness suite, real evaluator canary, agent canary,
Clean-H, or any accepted firmware/HIL evidence unless the implementation unexpectedly crosses
those boundaries.

## Acceptance and successor sprint

Accept only if:

- the focused regressions and complete ordinary optional-watcher host suite pass;
- the diff is confined to the optional watcher and its focused tests;
- an independent manager reproduction proves historical startup bytes are skipped while a
  post-baseline append is observed; and
- no existing cursor is advanced by initialization.

After acceptance, preserve all Clean-H route/cleanup evidence. Create a fresh successor epoch and
fix only the run-local A22 hook indentation, D31 launcher binding, A24 redirect parsing, A26 bounded
measurement path, and manager prompt signal vocabulary. Do not enter a production-server repair
loop or restart locked terminal work.
