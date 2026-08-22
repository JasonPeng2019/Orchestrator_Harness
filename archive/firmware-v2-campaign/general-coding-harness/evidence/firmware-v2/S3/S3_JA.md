# S3.JA author integration

- S3.CA base: `6325d6d5dec052274d35634ae943994226ecd3a9`.
- Initial A1 test commit: `3831b2a93ddaf06a6597eeaa77c12dc05cf410e1`.
- ROOT-IM rejected the initial evidence because `S3-DUAL-003` read the completed V1 passed registry
  instead of the active firmware-v2 registry; that false-green authoring defect was corrected in the
  same thread without changing product code.
- Corrected A1 tip: `d731032e12ed2c7e65997915d1a74eb64823a285`.
- S3.JA merge tip: `bbc8ad94c32f3ddad4a54afd4c1a2d51ac4bb11e`.
- Final A1 FINDINGS SHA-256:
  `e4724e39dec960c2e731dc5598dfebd2641a2822edf032abddca35b45ded2136` (empty).
- Final A1 RESULT SHA-256:
  `ac0937b2994fd58992912c5a14a0bfef587073bb9ceb829c44777a6241c15051`.
- Final A1 TEST_PLAN SHA-256:
  `14b7cb5a2647cec5583bfa93d9a1c3e3d422453643a7198d55dd43707322de29`.

The integrated gap set is exactly `S3-DUAL-001`, `S3-DUAL-002`, and `S3-DUAL-003` in
`orchestrator_harness.tests.test_s3_operator_journey`. S3.D1 is authorized to run that module only.
No MCP or hardware operation occurred.
