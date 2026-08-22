# S3.A1 test plan

Base checkpoint: `6325d6d5dec052274d35634ae943994226ecd3a9`.

| Stable ID | Requirement mapping | Dependency inputs |
| --- | --- | --- |
| `S3-DUAL-001` | C15, C16, C18: legacy schema-less fixture stays distinct from Coding V1. | `examples/legacy-firmware.invocation.example.json` SHA-256 `43f58e1a27e2ce7a3a6158c00ceba30f11c6b6e57689eb5b3dfcd56f489e7294`; `examples/coding.invocation.example.json` SHA-256 `e9f300683da4f9b9f6062087035530baa04dfe8af493a8654f1a4690ac9857a7`. |
| `S3-DUAL-002` | C18, C24, C71, C73: disposable routes retain separate lane/resource/event identities. | Public discovery/reconciliation APIs and `SuiteFixture`; `examples/dual-path-manager.example.md` SHA-256 `9014ff5949dbdbfbedc9bba5d2597c30302618687dd0258e5d1dcf9be84833af`. |
| `S3-DUAL-003` | C13, C43, C60-C64, C67, C71-C73: operator commands, role/topology limits, registry, templates, and candidate-only safeguard remain bound. | `QUICK_START.md` SHA-256 `1290f1fa9c96df2f3e2116ef36092c0916d851876f752071a2ffcbfc8be6a146`; `tools/Invoke-CandidateSafeguard.ps1` SHA-256 `de260bd204b63e5b76abcfb9f5e4fa70f837c4e798bbbe9121b86334ad2c32ac`; `runtime/firmware-v2/passed-tests.json` SHA-256 `9b9dbb61575c4b73d2b8a0229ab5b9adf8bbc42d9c918756a1d76178859c1541`. |

Exact S3.D1 command:

```powershell
python -m unittest orchestrator_harness.tests.test_s3_operator_journey -v
```

The registry dependency resolves from the lane repository root as
`REPOSITORY_ROOT.parents[2] / "passed-tests.json"`, which is the active
`runtime/firmware-v2/passed-tests.json` registry.
