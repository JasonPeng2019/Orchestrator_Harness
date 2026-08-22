# S3.R1 Lock Review

- High: partial cleanup failure was ignored before retry/wait, potentially retaining claims indefinitely.
- High: claim liveness ignored the persisted exact process creation identity.
- Residual tests belong to S3.A1.

Repair verification is clean at `b831a71ff4b46be39cc5942ed7d3a0c5d4ebdf2d`.
