# Pre-live-run repeated implementation audit

## Purpose

Before the final full-product live integration campaign begins, run a repeated,
source-based implementation audit. This is a separate gate from ordinary code review
and from the live test campaign. Its purpose is to find real implementation gaps while
there is still time to fix them before expensive live-provider testing.

## Required reviewer assignment

Assign one subagent to review the current implementation against the master specification
and the stated product design. The reviewer must inspect the actual code and relevant
tests/records, not infer behavior from implementation-review documents or intended design
notes alone.

## The review guard

The reviewer may record an item only when it is one of the following:

1. A direct failure of the current master specification.
2. Plainly broken behavior in the stated product flow — for example, a worker escalation
   being discarded before it reaches ROOT.
3. An obvious product-design decision that should clearly govern the code from the
   description of how the product works, but where the code instead behaves in a highly
   incorrect way.

The reviewer must **not** turn any of these into a gap merely because they would be
preferable:

- optional observability or extra logging;
- stricter validation or defensive safeguards beyond the product contract;
- alternate designs, abstractions, or architecture preferences; or
- speculative failures unsupported by the current code path.

## Review output requirements

For every claimed gap, the reviewer must provide:

- the exact master-spec or product-design requirement, or a concise explanation of the
  plainly broken user-visible flow;
- exact code locations and the actual observed behavior;
- a minimal failure sequence that demonstrates why the behavior is wrong;
- the smallest correction that restores the required behavior; and
- an explicit statement that the item is not merely an optional improvement.

The reviewer must separately label unimplemented/live-unverified test coverage. Missing
native evidence is not automatically a code defect.

## ROOT/main implementation-agent responsibility

Each time the reviewer returns findings, ROOT/the main implementation agent must read and
audit every item before making changes. ROOT decides whether each proposal is:

- **Valid:** a real master-spec failure, plainly broken product behavior, or highly
  incorrect obvious-design implementation. Add it to the current gap set and fix it.
- **Invalid or overcorrected:** an extra safeguard, design preference, vague concern,
  unsupported inference, or unnecessary change. Record why it is rejected; do not
  implement it as a product requirement.
- **Needs evidence:** not yet proven either way. Obtain focused code/test evidence before
  accepting it as a gap.

The reviewer is advisory and can never block execution, reject a plan, impose a fix, or
declare the gate failed on its own authority. Its review is input to ROOT's decision.
Only ROOT/the main implementation agent determines the disposition of a finding, whether
it is valid, what minimal correction is appropriate, whether the correction is verified,
and whether the pre-live-run gate may proceed. The operator retains ultimate authority
over ROOT's decisions.

ROOT must implement only the valid findings, verify the relevant behavior, then request
another review pass. Repeat this cycle until a review pass finds no remaining valid gaps
or all remaining items are explicitly deferred by the operator.

## Required completion condition before M09/live integration testing

Do not begin the final full-product live integration campaign until:

1. at least one independent audit has completed under this guard;
2. ROOT has dispositioned every finding with evidence;
3. all accepted pre-live-run gaps have been implemented and verified; and
4. a follow-up audit confirms that no undispositioned valid implementation gaps remain.

This gate does not replace the final live integration testing. It makes that campaign a
test of a reviewed implementation rather than the first time obvious implementation gaps
are discovered.
