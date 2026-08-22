# Focused Candidate Gate

- Product commit tested: `776c6fb3ffaed38de3b6e9b1699ffdea046e709a`.
- Orchestrator suite: 248 tests, 1 skipped, 0 failures, 0 errors in 107.161 seconds.
- Watcher suite: 100 tests, 0 failures, 0 errors in 14.148 seconds.
- Compile check: passed for `orchestrator_harness`, `harness_common`, and `harness_watcher_implementation`.
- Ruff: passed from the locked outer development environment.
- BasedPyright initially found two optional-path errors in the new regression test. Commit `41c891ac569a5fc68ab85389a3996f1abd6bac59` makes the test precondition explicit.
- BasedPyright after the test-only fix: 0 errors, 0 warnings, 0 notes.
- Directly affected lock-cleanup regressions after the test-only fix: 2 passed.

The full product suites were not repeated after `41c891a` because that commit changes only test type narrowing. The accumulated safeguard subsequently ran exactly once on final candidate `4699d27` and passed; see `full-verification.json`. The unchanged result remained locked green through fresh V2 acceptance.
