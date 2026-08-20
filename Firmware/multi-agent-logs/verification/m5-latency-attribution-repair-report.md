# M5 latency-attribution repair verification

Updated: $utc

## Accepted change

The watcher now distinguishes a late harness observation from a late actionable endpoint after an
on-time observation. It assigns BUSY_MANAGER_DELAY only when one gap-free explicit manager-work
chain covers the full late window from delivery deadline to actionability. A fully covering native blocking wait
remains HARNESS_DELIVERY_DELAY; partial, overlapping, or incomplete activity is
INSUFFICIENT_EVIDENCE.

## Review and smoke

- Terra-medium implementer completed the focused code/test/doc change.
- Independent Terra-medium review found two fail-closed gaps; both were repaired and re-reviewed
  resolved.
- Independent practical smoke found a partial-native-wait gap; it was repaired and the exact
  reproducer passed on rerun.

## Verification

- Watcher suite: 95 passed.
- Harness suite: 201 passed, 1 skipped.
- Focused attribution unit suite: 27 passed; the separate host-only practical also passed.
- Host-only practical attention check: passed.
- python -m py_compile harness_watcher_implementation/attention.py: passed.
- pyright harness_watcher_implementation/attention.py: 0 errors.
- python -m compileall -q harness_common orchestrator_harness harness_watcher_implementation:
  passed.
- A broad ad-hoc Pyright invocation over whole directories is not a valid project gate because it
  includes retained canary workspaces and pre-existing test typing debt; it reported 183 unrelated
  errors. The established changed-production-file Pyright gate passed.

## Retained sprint reanalysis

For 20260802-m5-r1-110513Z: Atlas is NO_BLOCKING_IMPACT; Boreal and Cygnus remain
HARNESS_DELIVERY_DELAY; Delta is now truthfully INSUFFICIENT_EVIDENCE because neither native
wait nor a busy interval covers its full late-window gap.

## Final design-alignment amendment

The accepted M5 policy allows an overrun beyond 90 seconds when a valid reason covers the overrun,
not necessarily all time since harness observation. The analyzer therefore evaluates the exact
late window from `delivery_deadline_utc` through actionability. Focused tests cover genuine busy
work beginning at the deadline, a complete native wait, a partial native wait, unfinished
pre-deadline activity, handling an earlier genuine request, overlapping work, late observation,
and completed work that ended before the late window. The focused suite, host-only practical, full 95-test watcher suite, changed-file
Pyright, and compile check all pass.

No commit or push was performed.
