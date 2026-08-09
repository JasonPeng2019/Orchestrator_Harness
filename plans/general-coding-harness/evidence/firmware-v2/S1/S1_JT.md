# S1.JT test-execution join

- Tested join before the non-behavioral cleanup: `b534b5c17fc5e2aa476cacee88ff0f893243cf47`
- Final clean S1 product/candidate revision: `5d7c36e3dd38dc813c91f4462f4298c73883c59a`
- Shared dependency map SHA-256: `dbe652b34b7e61710de98784878b2fc9fe77089f2a2d4f8c3c33021fa6cbfa52`
- Final product result SHA-256: `c89af0515c41955df3e4b7fdb29b45f0e9a1329dae9bb0bb8f5567b7b2efa4a2`

## D1 protected and route-contract shard

`S1.D1` passed 26 tests and 23 subtests in 98.53 seconds with no failures, skips, or
expected failures. That execution included all 19 dependency-mapped protected baseline IDs, all
three A1 route-contract IDs, and four additional S1 product regressions collected from the selected
modules. The result is
`plans/general-coding-harness/runtime/firmware-v2/implementation/lanes/S1.D1/.agent-workspace/RESULT.json`
at SHA-256 `7583790a80c988bcc60184349c78b3f9bd0465c24b57776fd976a5005cc02bac`;
the report SHA-256 is `8bab6b910dd947226d90d4c369052a061812d472cf31b7a8fa8cc5a6609911ee`.

## D2 lifecycle and static-check classification

The first D2 run passed both `S1-LIFE` IDs but invoked Ruff with a nonexistent lane-local
`.codex/dev` project, so its broader default diagnostics were not an authoritative repository check.
ROOT-IM reproduced the base and joined revision with the exact outer Ruff configuration. Eleven
diagnostics were command/configuration or pre-existing baseline noise; the only new owned diagnostic
was A1's unused `json` import. A1 removed only that import in commit `f987a05`, with a passing exact
changed-file Ruff check. ROOT-IM merged it without changing runtime or assertion behavior.

D1 was therefore not rerun. D2 preserved its two exact lifecycle credits and reran only the corrected
final-tip Ruff check, which passed. The final D2 result SHA-256 is
`d6d9ed6db947ce486c3afb026274d6595f1d7ae10bd229674f2ac8e3235fb778`; the final report SHA-256 is
`b99bcfb9040d02f4c127e9699c5eec7a96fb43eca768d92bcd52e0cad9272207`.

## Join decision

S1 Loop 2 is green. All surfaced findings followed their owning lane; no phase reset occurred and no
unrelated green test was rerun. The final no-write scan at `2026-08-04T01:34:43.643891Z` found seven
known lanes, no live lane, claim, conflict, observation/process error, manager signal, request, or MCP
record. The manager notification state has no pending or deferred item. No hardware or physical MCP
mutation occurred. `S1.P` bound a schema-valid PASS result to the exact clean final tip.
