---
name: harness-api-design
description: Explicitly review or design harness APIs, event schemas, configuration, command-line contracts, or compatibility boundaries; use only when invoked by the user.
---

# Design a harness interface

Define observable behavior before implementation:

- Callers and ownership boundaries.
- Inputs, outputs, defaults, and validation failures.
- Compatibility and migration requirements.
- Concurrency, idempotency, and retry semantics.
- Stable identifiers and persistence rules.
- What is deliberately outside the interface.

Prefer the smallest general contract. Keep firmware-specific behavior behind an adapter rather than in the core protocol.
