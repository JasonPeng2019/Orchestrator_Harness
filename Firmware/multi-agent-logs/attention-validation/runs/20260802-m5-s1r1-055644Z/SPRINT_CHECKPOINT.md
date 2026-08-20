# M5 checkpoint — 20260802-m5-s1r1-055644Z

## Disposition

**RESET — 0/3 accepted.** This attempt does not count.

## Root audit

1. **Accepted: isolation violation.** While the attempt was active, the root directly globbed the
   worker manager-signal directories to check whether requests existed. No request was discovered
   by that probe, but it was still a prohibited discovery path. A counted sprint must use only the
   blocking native harness wait.
2. **Accepted: harness lifecycle interruption.** The first direct managed-harness foreground tool
   call had a 120-second command timeout and was killed by the host tool. A restart correctly
   refused to continue because the committed scan process identity changed. This is a root launch
   procedure error, not a reason to weaken the harness identity guard.
3. **Accepted: watcher source-format config error.** Four pretty-printed controller status JSON
   documents were configured as watched JSONL logs, producing 472 deterministic route rejects.
   One additional malformed harness line arose in the interrupted harness output. Controller
   status documents are not watcher log sources; next config will observe the native harness JSONL,
   lane-events JSONL, and explicit attention producers instead. Process status remains proved by
   native harness scans and the root process registry. No watcher code or external parser is
   justified.
4. **Accepted: insufficient challenges.** Only Atlas completed the native wake chain before the
   harness interruption. Other workers were safely released during invalid-attempt cleanup, not
   counted as harness challenges.
5. **Accepted: cleanup/freeze passed.** The diagnostic watcher stopped natively, all recorded
   processes were absent, the 112-file Python fingerprint matched, and all sealed inputs matched.

## Smallest next action

Start a completely fresh epoch. Use no direct worker/signal/transcript inspection. Launch the
native managed harness with a long-lived host-tool timeout, immediately verify that the foreground
cell remains live, and never restart it within a sprint. Configure only actual JSONL watcher
sources. No source-code repair, runner, wrapper, relay, or retry controller is needed.
