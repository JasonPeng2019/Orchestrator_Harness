# Clean-H watcher repair audit

## PASS

The optional-watcher repair complies with the accepted plan.

- `serve` establishes a cursor epoch before its first background poll; the direct
  `poll` command remains unchanged.
- A brand-new runtime records each already-present source's file identity and
  EOF, with empty evaluation context.  Historical defect-shaped content is
  therefore not re-evaluated, including as a later no-progress condition.
- An existing cursor is preserved, including unread material.  Sources absent
  at initialization are not suppressed when they later appear.
- The existing reader's identity/size handling continues to read truncation or
  replacement content from the beginning of the new generation.
- The changed watcher implementation, CLI wiring, and smoke coverage match the
  bounded repair scope.  The coder's 28/28 suite and manager's focused 28/28
  verification, including independent historical-skip, post-append,
  existing-cursor, and replacement controls, are green.

No concrete functional blocker was found.  It is safe to begin the next sprint.
