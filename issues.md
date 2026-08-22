# Active issues

## Legacy firmware launches are blocked by universal overlay-receipt enforcement

**V2 resolution (2026-08-22):** Superseded. The neutral-cache correction made super-cache optional,
and commit `09e5786e338d9ebcf71230c8ad327808b2ec229b` then removed the schema-less legacy firmware
route entirely from v2. There is therefore no v2 legacy launch to repair or exempt. V1.5 remains
the preserved historical line; this section is retained as historical diagnosis only.

**Introduced in:** `firmware-v2-harness-runner` commit
`4ed577cb39bdb7330290496e5c0f6b29595a7210` and therefore present in the
published `working/firmware/v2-candidate` tip `3bf43c306cab8c1f8999ad4c637b37146b5dec8d`.

### Observed contract conflict

`lane_controller.run()` now calls the prepared-overlay receipt verifier before provider launch for
every invocation.  A schema-less legacy firmware invocation does not carry the modern
`overlay_receipt` field: its parser intentionally rejects modern coding-route fields and retains
its own policy/lease/board/MCP contract.  The universal check therefore rejects a supported legacy
firmware launch before its Codex provider process starts.

### Impact

The ordinary canonical coding lane is correctly required to use a prepared cache receipt.  The
separate legacy firmware compatibility route is unintentionally unavailable, contradicting the
published README and overview statement that schema-less firmware invocations remain supported.

### Minimal repair

Apply prepared-cache receipt verification and the cache Stop fallback only to canonical and coding
provider lanes.  Leave the schema-less legacy firmware route governed by its existing policy,
authorization, lease, relay, MCP, and physical-cleanup rules.  Do not merge the two invocation
schemas or attach the standalone `FirmwareHardwareAdapter` to the lane controller as part of this
repair.

### Verification needed after repair

1. A schema-less legacy firmware fixture reaches provider launch without an overlay receipt.
2. Canonical and coding lanes still reject a missing or mismatched receipt before provider launch.
3. Existing policy/lease validation on the legacy route remains unchanged.

## Repository-owned payload was incorrectly bundled into the neutral super-cache

**Introduced in:** `firmware-v2-harness-runner` commit
`4ed577cb39bdb7330290496e5c0f6b29595a7210`.

### Observed design error

The super-cache is a neutral mechanism for ingesting a caller-selected folder and preparing lane
worktrees from those exact contents. Commit `4ed577cb39bdb7330290496e5c0f6b29595a7210`
incorrectly treated one experiment's cache payload as product defaults: it added
`.agent/stop-verify.ps1` and `.codex/hooks.json`, then coupled the lane controller to that exact
verifier. The later setup commit also added a cache-owned `AGENTS.md` and control declaration.

`super-cache-problems.md` recorded problems encountered by that experiment. It was evidence about
one caller-selected payload, not a requirement that the runner distribute those files.

### Impact

The checked-in payload makes every prepared lane inherit harness-owned hooks and rules even when the
caller selected no such content. Requiring the cached verifier also makes an optional, generic file
overlay behave like one mandatory verification product.

This is separate from provider-adapter event-notification hooks and from the explicit command that
installs packaged manager rules into the ROOT workspace. Those features have their own installation
contracts and must not be inferred from super-cache use.

### Recommended disposition for v2

Base the corrected v2 runner on `9f383712438d57cfcd8aea6b85c7fb284c7ecf3a`. Keep the generic
ingest, prepare, receipt, collision, and restoration machinery. Keep super-cache optional and verify
a supplied receipt early for its exact worktree and orchestrator/subagent role. Do not ship a cache
payload or require a particular cached file. Install manager rules and provider-adapter hooks only
through their separate explicit commands.
