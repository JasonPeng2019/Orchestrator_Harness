# M5 watcher repair plan after reset epoch 20260802-m5-s1-023043Z

## Root disposition

This sprint is `RESET` and remains preserved. The diagnostic watcher stopped at
02:33:09Z, before any tested worker challenge. Its evidence cannot count toward
the required consecutive sprint total.

## Verified defects

1. The watcher service crashes when an observed JSON record decodes to a scalar;
   `_route` assumes every decoded value is an object and calls `.get`.
2. A large routed batch can exceed the watcher log's 65,536-byte record limit and
   crash an explicit poll instead of retaining bounded diagnostic evidence.
3. Producer metadata can inject canonical provenance field names such as
   `source_id`. Canonicalization overwrites those fields and then computes and
   verifies different source forms, producing misleading source-hash failures.

## Smallest repair

1. Make routing accept only JSON objects. Ignore/reject scalar records with a
   bounded diagnostic entry; never terminate the diagnostic service.
2. Route changed records in bounded entries below the existing per-record limit.
   If one source record itself cannot fit, retain a compact rejection containing
   source path, byte range/offset, size, and digest rather than crashing.
3. Reserve canonical provenance keys at source-record creation/validation so the
   producer CLI rejects them before append. Keep canonical digest validation
   strict; do not weaken it.
4. Add focused regressions for scalar input, oversized routed input, reserved
   producer metadata, continued diagnostic-only service health, and evaluator
   non-invocation.
5. Run focused tests, full watcher tests, Pyright, and an independent review.
   Then run a Luna process-topology smoke with the real optional watcher owner.
6. Rerun M4 readiness because watcher runtime code changes. Only then begin a
   fresh M5 Sprint 1 with the consecutive count at zero.

## Rejected scope

- Do not redesign the watcher.
- Do not add an AI evaluator or relay.
- Do not relax source-integrity checks.
- Do not repair historical epoch evidence in place.
