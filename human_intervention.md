My best evidence-based estimate for the 18h13m run is:

   Category                                                  Time     Share
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━  ━━━━━━━━
   Core development and live testing                  11–13 hours    60–70%
  ─────────────────────────────────────────────────  ─────────────  ────────
   Required review, integration, and evidence work      2–3 hours    10–15%
  ─────────────────────────────────────────────────  ─────────────  ────────
   Clearly removable inefficiency                       3–5 hours    20–30%

  If we count the required assurance work as necessary under the current quality standard, approximately 14–15 hours were useful or necessary and 3–4 hours were obvious waste. With more aggressive consolidation, the
  removable portion approaches five hours.

  The necessary portion included:

  - Roughly six hours establishing the original 96-cell live baseline.
  - Roughly two hours executing the affected-only 51-cell Series 2 pass.
  - Several hours constructing controls, fixing real product defects, writing focused regressions, classifying failures, and reviewing the resulting changes.

  The clearly removable portion included:

  - 53 minutes in one repair session that produced a 5 MB transcript and no edit.
  - More than 12 minutes in the Qwen CHECK8 self-loop.
  - Another integration attempt that explored for over seven minutes without performing its explicitly requested copy.
  - Repeated result-envelope, handoff-shape, digest, BOM, and incomplete-fixture corrections.
  - Provider quota failure discovered only after allocating and starting a review lane.
  - Repeated agent discovery of known paths and result-emission commands.
  - ROOT time manually reconciling stale status files, large transcripts, and evidence that should have been summarized mechanically.

  Some additional time came from extremely fine-grained patch → review → integration cycles. That can be reduced, but I would not classify all of it as easily removable because independent review caught at least one
  real false validation claim.

  A better setup should realistically cut a comparable from-scratch run from 18.2 hours to around 14–15 hours without weakening coverage. The straightforward changes are a five-minute progress watchdog, machine-
  injected result emission, exact first-action commands in every task card, provider preflight, automatic phase timing, and automatic stale-status reconciliation.

  The topology’s preservation change still delivered its intended benefit: it avoided replaying 45 cells on one pass and planned to preserve 55 on the next. The remaining clear inefficiency is mostly in agent execution
  and lane administration, rather than matrix invalidation.


## Most recent run audit - authoritative scope correction

This section supersedes the earlier 3-5 hour removable-waste estimate above.

### Scope

- This audit covers only the most recent long run between the previous human
  intervention and the current human-intervention checkpoint.
- Project wall-clock runtime at the ending checkpoint: **18 hours, 13 minutes,
  38 seconds**.
- It excludes all project history before that run and all activity after that
  checkpoint.
- Durations are project wall-clock durations reconstructed from preserved
  controller, checkpoint, decision, and observer evidence. They are not
  calendar clock times.

### Where the run's wall-clock time went

The preserved phase boundaries divide the run approximately as follows:

| Phase | Wall-clock duration | Work performed |
|---|---:|---|
| Pre-live control construction, review, and readiness | 3h49m | Finished CHECK14-16 controls, observer controls, reviews, and live admission |
| Initial 96-cell Windows live matrix | 4h52m | Executed the six provider/profile manifests, including contained live stalls |
| Initial pool validation and first correction route | 3h51m | Joined and classified the pool, repaired product and control defects, reviewed and integrated them, and ran Series 2 readiness |
| Affected-only Series 2 live execution | 1h59m | Executed 51 fresh affected cells while preserving 45 prior credits |
| Series 2 evidence, verdict, and follow-on repairs | 3h42m | Validated and classified the second pool and repaired newly exposed atomic, cleanup, controller-exit, and retirement defects |

Thus, approximately **6h51m** was spent in the two live matrix phases and
approximately **11h23m** was spent on development and assurance surrounding the
matrix. The latter includes genuine implementation work, focused tests,
independent reviews, integration, classification, cleanup proof, and ROOT
evidence reconciliation; it is not all waste.

### Directly verified removable inefficiency

| Source | Gross observed duration | Conservative removable duration |
|---|---:|---:|
| Three repair lanes that produced no accepted output | 1h12m55s | 57m55s after allowing five diagnostic minutes per lane |
| Six live-cell stalls beyond the existing five-minute evidence threshold | 38m52s | 38m52s |
| Serial administrative corrections caused by fixture, result-shape, or BOM mistakes | at least 9m40s | at least 9m40s |
| **Verified total** |  | **at least 1h46m27s** |

Counting the full duration of the three failed repair lanes gives **2h01m27s**.
The conservative and gross figures therefore place the directly supported,
clearly removable waste at **1h46m-2h01m**, or approximately **9.7%-11.1%** of
this run.

The failed repair-lane durations were:

- 53m21s: 694 completed items, 27 tool errors, a 5 MB transcript, useful
  diagnostic findings, and zero tracked product edits.
- 13m28s: more than 400 trace items and redundant retained-evidence summaries,
  with no product diff or accepted product credit.
- 6m06s: 60 shell commands and 420 KB of transcript without the required first
  failing test or any tracked change.

The live-stall overshoot consisted of:

- 25m25s after Codex managed CHECK8 had satisfied the existing five-minute
  thrash-evidence threshold.
- 8m08s after Qwen managed CHECK8 had satisfied the same threshold.
- 5m19s combined across the other four contained CHECK8, CHECK12, and CHECK16
  stalls.

The administrative subtotal includes a 2m51s readiness correction caused by an
omitted fixture, result-envelope corrections, two BOM corrections, and a
prelaunch serialization repair. A one-minute bundle-digest correction is not
included in project wall-clock waste because it overlapped the 53-minute
product-repair stall.

### Exclusions and conclusion

The later Claude quota failure and later integration exploration stall happened
after this checkpoint and are excluded. Earlier project history is also
excluded. Long ROOT reconciliation intervals are not labeled as waste because
their artifacts combine necessary validation with administration and do not
support an honest exact split.

For this most recent run, the main reason development took so long was the
combination of nearly seven hours of real live execution and more than eleven
hours of serial control, repair, review, integration, and evidence work. The
clearly verified setup inefficiency was about two hours. The most direct
remedies are an enforced progress watchdog for repair agents, automatic
containment immediately when the existing P02 threshold is met, machine-created
result envelopes, complete fixture staging, and strict UTF-8 serialization at
the emitter boundary.
