# S2.A2 test plan

## Overlap audit

`test_firmware_acceptance_kit.py` already proves the packaged seed validator, one seed-tamper rejection, ordered immutable call evidence, raw-result identity, worker capability stripping, and the closed contract validator. This lane adds only the missing disposable-target boundary: all five seed files must be read-only and hash-bound while target-created source, test, build, and configuration files may be committed. It also makes the closed 18-ID route/dependency contract explicit.

## Requirement mapping

| Stable test ID | Requirement coverage | Dependency fingerprint inputs |
|---|---|---|
| `S2.A2.T1` | C43 exact five-file seed, read-only protection, target-created source/test/build/config allowance, initial Git/HEAD validation boundary | `kit.py`, five seed files, target seed manifest, Git executable |
| `S2.A2.T2` | C63 closed 18-ID passed-registry/selective-rerun contract and C59 allowed three-way route vocabulary | `TEST_CONTRACT.json`, `kit.py` campaign validator |
| `S2.A2.T3` | C43 seed substitution rejection after target files exist | `kit.py`, five seed files, target seed manifest |

## Executed stable IDs

`python -m unittest orchestrator_harness.tests.test_firmware_acceptance_target -v`

- `S2.A2.T2` passed.
- `S2.A2.T1` and `S2.A2.T3` failed before target materialization because the accepted seed's charter hash disagrees with its manifest. The finding is recorded in `FINDINGS.json`; no production or seed file was edited.
