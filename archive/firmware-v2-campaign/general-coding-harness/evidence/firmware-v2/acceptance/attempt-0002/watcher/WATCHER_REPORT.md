# F.C3.W terminal report — attempt-0002

Final invariant result: **ABORT REQUIRED / NOT CERTIFIED**.

The helper verified ROOT's immutable watcher-launch record and created `WATCHER_READY.json`. It emitted 56 heartbeats through cursor `60bc8cb59f5ad3a32e870cc3b7e7feda9309fd41b55999e92d09621cb099f158`; every heartbeat recorded the required clean candidate `2877ec1385b947a6ed72bbd7c95ac7a28d169782` and clean server `f003f84a7df51cd8595a3203c62e225b21da2a22` identities.

ROOT's abort evidence establishes reproducible candidate control-plane rejection of two authentic initial controller-status records and the watcher misclassification of those rejections. ROOT authored the preserved `watcher/ABORT_REQUIRED.json` override (`watcher_authored: false`), so this watcher did not claim authorship of that evidence. No target worker reached a recorded active lifecycle, no mutating hardware call was dispatched, and candidate-managed shutdown records four exact aborted/reaped sessions with zero claims remaining.

Key evidence hashes:

- `topology/WATCHER_LAUNCH.json`: `f9b8b9c290327bb667fa5a3471a73702201b0a8ebbda702768cc3664f89f938b`
- `watcher/WATCHER_READY.json`: `17a15624e7d43086b92da019ceee5e0f0d4f42cbba9837886c068e6a80f960bc`
- `watcher/WATCHER_SERVICE_TERMINAL.json`: `20a577012b30176fadb78d8c2f834f5a9f6104c566af5195fcdd3ce9593d4b60`
- `watcher/ABORT_REQUIRED.json`: `638cf7a750c238f2407cf0ad7d6d1c3aaacd6ee75f157f10e110e2219f60d52e`
- `topology/ROOT_ABORT_REQUIRED.json`: `757ff52b1dea928871f21b525d72d5b3387ffaec492fd27a217ef6420c22ec74`

The helper process PID 159352 is no longer present and has been reaped. ROOT's `WATCHER_STOP_REQUEST.json` binds candidate shutdown with `all_sessions_exact_reaped: true` and `claims_remaining: 0`.
