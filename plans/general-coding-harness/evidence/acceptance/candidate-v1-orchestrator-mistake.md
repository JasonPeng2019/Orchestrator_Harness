# Candidate Acceptance v1 Orchestrator Mistake

The acceptance watcher initially treated inconsistent auxiliary process bookkeeping as a harness defect. That classification was too broad.

- The orchestrator-maintained `process-manifest.json` assigned the original P2 process identities to retry `candidate-p2-retry-002`.
- The candidate harness's authoritative controller status and native event log recorded the retry's correct identities and were mutually consistent.
- The candidate harness safely rejected P2's first malformed result; the orchestrator retried it and the harness accepted the corrected result.
- This is expected orchestrator fallibility, not a harness failure.
- The outside writer-manager happened to stop the topology between completed P2 and unstarted P3. No target or harness process was active, so v1 can resume from its accepted P2 checkpoint.

The false abort is itself a watcher defect under the corrected acceptance contract. V1 was allowed to finish so its retained evidence could prove the harness correctly contained ordinary orchestrator mistakes, but V1 cannot be the final promotion acceptance because it resumed the same target after that watcher defect.

Disposition: preserve V1 as diagnostic evidence, keep its product and full-verifier results locked green, and run final acceptance from a fresh V2 runtime and target repository with the corrected watcher boundary active from the start.
