# S2.R1 Review

Reviewed commit: `b558ffc198f4931b4fe97a91e42f45d957825766`

## Admitted Findings

1. Duplicate-active detection scanned only `*.status.json`, but coding invocations allow other confined status filenames. A live declaration could therefore be missed.
2. Git subprocesses inherited repository-redirection and config environment variables, so `git -C` could inspect fabricated Git state rather than the declared worktree.
3. Discovery associated one global result with the newest controller status. A newer firmware status could route a coding result through legacy validation and let a firmware-shaped result terminate a coding lane.

## Planned Test Work

- Update pre-S2 coding fixtures with required repository declarations.
- Add the complete Git, duplicate, Windows, result identity, dirty-tree, firmware-routing, and correction matrix.

## Triage

The three bypasses return to S2.P. Existing fixture updates and coverage gaps remain in S2.A1 after Checkpoint A.

## Repair Verification

Commit `3d457712b7b01447738014f769283ca5cc5fc0ed` resolves all three bypasses. The reviewer confirmed complete permitted coding-status discovery, a minimal Windows-capable Git environment, and exact lane-specific coding versus firmware result association. Checkpoint A is closed.
