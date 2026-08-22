# Candidate-root verification protocol

The outer verifier is hard-bound to `harness-in-progress`; it cannot prove V2 code in the isolated `harness-candidate` worktree.

During S1-S3, run only focused candidate-root commands whose dependencies changed, preserve unchanged green IDs in `runtime/firmware-v2/passed-tests.json`, and set a fresh lane-local `PYTHONPYCACHEPREFIX`.

S3 must materialize and test a candidate-owned safeguard launcher that runs the candidate's complete Ruff, format, BasedPyright, compilation, orchestrator, watcher, Codex-integration, attention-retention, and synthetic-firmware regression gates. The accumulated safeguard runs once after C4 on the exact C1-locked revision. Environment-only interruption resumes the same logical run and reruns only incomplete components. A locked-input source change requires the owning-step route, a fresh C0/C1/C2/C3/C4 sequence, and a new safeguard run ID.

The existing unchanged V1 full-gate evidence is credited at preflight from `plans/general-coding-harness/evidence/final/full-verification.json` (SHA-256 `036e4af20e4c097c3e5a92f38e057e173babfd86c8e8fcb114cdfe2973c14fe3`) and is not rerun now.
