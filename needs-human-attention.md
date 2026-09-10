# Needs human attention

## Result of the v2 optional-capability audit

**No unresolved human decision.** The proposed v2 harness has no capability
that a custom CLI can fail to support while still being inseparably required for
the harness to run.

The only retained optional setting is `managed_coordination` in
`<harness-root>\harness-config.json`:

- `enabled` is the managed profile: native ROOT/worker hooks, manager queue,
  event delivery, and worker coordination files are materialized together.
- `disabled` is the plain profile for a custom CLI that cannot prove those
  native hook capabilities. The same launcher/controller/worktree/result/monitor
  path continues to work. ROOT deliberately uses `scan --no-write` and
  `watch --until-actionable` instead of being woken by a hook.

All other former settings are no longer configurable:

- The shared cache, persistent monitor, normal `.agent-workspace` payload, and
  resource-manifest/lock facility are required harness structure.
- A no-hardware project declares an empty resource manifest. It does not turn
  off the lock facility.
- A managed or plain lane can claim a declared resource; the controller creates
  a lease only for that request.

## Evidence from the current candidate

The current controller constructs `ResourceClaims` only when an invocation has
non-empty resources (`harness-single\orchestrator_harness\lane_controller.py`),
so ordinary non-hardware lanes already run without a claim. The existing
`watch --until-actionable` command is a diagnostic blocking wait that does not
need a manager queue (`harness-single\orchestrator_harness\cli.py`). Those two
facts support the plain-profile fallback rather than exposing another optional
v2 feature.

The current candidate also contains older optional watcher/evaluator settings
and manually installed overlay/adapter paths. They are not part of the proposed
v2 `harness-config.json`; the v2 contract makes its monitor and shared cache
mandatory and does not carry those non-v2 toggles forward.
