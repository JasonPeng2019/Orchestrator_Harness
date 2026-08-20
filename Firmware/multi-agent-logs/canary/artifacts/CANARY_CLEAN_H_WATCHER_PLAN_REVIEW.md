# Adversarial review — Clean-H optional watcher epoch-baseline plan

## PASS

The plan is minimal, correct, and testable for the accepted Clean-H startup old-log false
positive.

* It limits behavior change to a brand-new **background service** runtime with no cursor; direct
  public `poll()` behavior remains intact for fixtures and diagnostics.
* EOF plus file identity is a sound epoch boundary: preexisting bytes are not evaluated, while
  bytes appended after baseline, a source created later, and replacement/truncation remain visible
  through the existing `_read` rules.
* Preserving an existing cursor prevents a restart from silently dropping unread content.
* The explicit no-progress-context requirement closes the otherwise plausible delayed re-evaluation
  of baseline text.
* Planned tests cover each safety-relevant branch: skip historical startup bytes, observe an
  appended record, preserve existing cursor offset, observe a later-created source, prevent
  no-progress resurrection, and retain direct-poll behavior.

The plan does not use timestamp/message heuristics, special-case Clean-H, suppress current epoch
records, or change primary/watcher ownership, evaluator, server, or hardware scope.  No blocking
concern was found.
