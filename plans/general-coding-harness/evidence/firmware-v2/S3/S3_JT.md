# S3.JT test join

- Joined candidate tip: `bbc8ad94c32f3ddad4a54afd4c1a2d51ac4bb11e`.
- Executor: S3.D1, GPT-5.6 Luna-high-default, launched by the pinned clean stable runner.
- Exact command executed once:
  `python -m unittest orchestrator_harness.tests.test_s3_operator_journey -v`.
- Exact stable IDs: `S3-DUAL-001`, `S3-DUAL-002`, and `S3-DUAL-003`.
- Result: 3/3 PASS; zero skips, expected failures, unexpected successes, or reruns.
- Test-report SHA-256:
  `88c8c151ce6d7dbe0eec184f42ee6c7bc9a6e54eb5f0e3a855cc70d372986a50`.
- Empty FINDINGS SHA-256:
  `6d907610f1a8deccb5ed7fd700557fe28575f9b2076d8d0ee790e3cbe13d6c4a`.
- Valid RESULT SHA-256:
  `7087ce0114175866c9fe89f2cad1ce3ead321141b81628d3953e25d19078bfaa`.

ROOT-IM independently matched the stable-ID array, outcomes, counts, finding identity, clean Git
state, terminal controller state, and empty post-exit resource-lock root because the stable runner
does not consume the newer finding gate. No MCP or hardware operation occurred. All unrelated green
registry entries remain credited and must not be rerun unless a later change invalidates them.
