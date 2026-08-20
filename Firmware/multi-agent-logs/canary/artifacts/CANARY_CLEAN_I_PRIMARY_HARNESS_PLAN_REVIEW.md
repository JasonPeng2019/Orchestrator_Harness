# Clean-I primary-harness repair plan review

## PASS

The amendment resolves the prior functional blocker.  Slice 2 now requires one
shared active/unknown lifecycle predicate covering `RUNNING_CODEX`,
`WAITING_RELAY`, `HELPER_RUNNING`, `PROCESS_STATE_UNKNOWN`, and applicable
`UNKNOWN`, and it requires positive controls for those live states.  It therefore
retains genuine live missing-MCP detection while exempting terminal pre-MCP
checkpoints.

The remaining slices directly address the validated explicit-lane/session
correlation and stale actionable-resource-ambiguity defects.  The prescribed
tests preserve real request, resource-conflict, and live helper/MCP detection;
scope remains appropriately limited to the primary harness.

## Advisory (non-blocking)

Use the actual Clean-I-shaped HELP/signal schema in the synthetic control as
well as a current request fixture, since the D31 evidence exposes both activity
forms.  This improves regression coverage but is not required to begin the
bounded repair.
