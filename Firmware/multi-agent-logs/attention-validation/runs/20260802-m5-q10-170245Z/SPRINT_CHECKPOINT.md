# M5 Q10 sprint checkpoint

## Identity and boundary

- Epoch: `20260802-m5-q10-170245Z`
- Active-goal attempt: `10/10` (final permitted attempt)
- Tested surface: Q9 passive-ineligibility-repaired baseline
- Python manifest SHA-256:
  `8c428d5f610a2d2ecf9d3a8f71a60e595d7350752817842a5d658be8606b5d83`
- Runtime-policy projection SHA-256:
  `89bb18cb67282fe4e71c198d9a3b4a279c6cb1412710a98b9a0a720316ec0f04`
- Runtime ended naturally; all registered processes are absent and resources are empty.

## Runtime and isolation

- One persistent root manager, one native managed harness, one deterministic diagnostic-only
  watcher, and four real external E2E worker/controller lanes ran.
- The watcher evaluator was disabled.
- Root discovered requests only through direct native blocking waits.
- No runner, harness/watcher wrapper, relay, scheduler, retry controller, watcher subagent,
  collaboration notification, transcript inspection, or user-message discovery influenced the
  sprint.
- Workers remained host-only and preserved their real E2E authorization-boundary progress; no
  provider, MCP, lease, board, flash, reset, serial, or RF action occurred.

## Genuine request sample

Four genuine HELP requests were natively observed and returned: Delta/A26, Cygnus/A24, Atlas/A22,
and Boreal/D31. All four are `UNCLASSIFIABLE` for the architecture gate:

1. root recorded `MANAGER_WAIT_FINISHED` before `MANAGER_WAKE_RECEIVED`, contradicting the required
   receipt-first causal order; and
2. each published manager response had an empty `lane_id`, so every worker correctly rejected it
   and omitted response-received/work-resumed records.

The exact stage rows are preserved in `CORRELATION_SUMMARY.json`. The response rejection truth is in
the four worker Q10 checkpoints under `fresh-experiments/*/.agent-workspace/m5/`.

## Controls

- Busy control: valid paired 55.338-second bounded hash audit, but it does not cover the complete
  late intervals and cannot excuse them.
- Quiet control: not clean; four retained Q9 stale-status events surfaced before the final timeout.
- More-than-90-second spans: not causally attributable; none is accepted as valid busy contention.

## Component health

- Harness: `HARNESS_PASS`. It observed, selected, returned, and acknowledged all four requests; no
  verified in-scope native defect occurred.
- Watcher: `WATCHER_PASS`. It remained diagnostic-only, had no observation/evaluator error, drained,
  and correctly failed closed on broken causal evidence.
- Manager evidence: `MANAGER_EVIDENCE_INSUFFICIENT`. Zero of four genuine requests has a complete
  manager-to-worker causal chain.

The sprint finalizer failed because four pre-worker stale-status claims used
`NATIVE_BLOCKING_WAIT` instead of the required `SELECT_ACTIONABLE` selection reason. This is a root
evidence-procedure defect, not a component defect. The genuine request claims themselves have valid
source-event selection snapshots.

## Review and root decision

- Advisory review: `REVIEW.md`
- Root audit: `ROOT_ADJUDICATION.md`
- Root accepted the component gates and cleanup findings, but rejected the reviewer's event-ID
  substitution diagnosis after comparison with Q8 and direct finalizer validation.

## Final disposition

`EVIDENCE_INSUFFICIENT`; comparable count remains `0/3`. The hard attempt budget is exhausted.
Never launch Q11. M5 therefore ends without a persistent-manager-versus-`codex exec` architecture
verdict. The bounded required final category is **Focused implementation repair still required —
evidence remains inadequate**, with the important qualification that Q10 verifies no new harness or
watcher code defect and does not justify a production repair by itself.
