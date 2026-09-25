# BEHAVIOR-06 - Setup and readiness preserve actual workspace ownership

## Dictated outcome and source

An authorized operator can compose the product harness with the supplied
ROOT-suite behavior in an isolated workspace, inspect whether the actual
launched product is ready, and recover interrupted or overwritten composition
without silently losing either family. Binding Implementation Section 10 and
Feature Sections 2 and 16 govern this outcome.

## Actors, triggers, and preconditions

The operator supplies an exact product root, installed harness and ROOT-suite
inputs, provider configuration, and scope for setup. Existing repository
instructions and unrelated roots are protected. Readiness may inspect service,
schema, binding, network, and pending-operation state without launching work.

## Behavioral flow and decision rules

1. Before mutation, inspect destination ownership and reject an unknown
   command/provider collision. Compose a deterministic view preserving both
   harness lifecycle and ROOT-suite capabilities plus repository instructions.
2. Validate staged and actual launched worker payload/tool configuration, not
   merely source templates. Commit through a recoverable completion boundary;
   repeat setup is idempotent when the composed result is already correct.
3. Detect later upstream overwrite or interrupted composition. Recompose or
   recover exactly before enhanced dispatch, leaving unaffected ordinary behavior
   and unrelated roots alone.
4. Readiness exposes exact build/root, composition state, compatible schema,
   available services and bindings, requested/effective feature/network state,
   pending/uncertain operations, and the next actionable step without credentials.
5. Supported operator surfaces for setup/readiness and the remaining network,
   snapshot, recovery, and usage outcomes use the same product domain contracts;
   they are not a second controller, launcher, or review system.

## State, data, and observable effects

The operator sees whether the active payload is composed, valid, overwritten,
partially committed, or not ready, and which exact dependency prevents the next
action. A source-directory check alone does not create a ready claim.

## Edge, failure, and recovery behavior

A preflight ownership conflict leaves live destinations unchanged. An interrupted
commit blocks only enhanced dispatch until validation or repair. A service outage
blocks only dependent operations; a missing binding is not silently substituted.
Setup recovery touches only the owned workspace and never deletes unrelated
user changes to manufacture a clean state.

## Constraints and preserved behavior

Existing harness and ROOT-suite lifecycle behavior and repository instructions
remain compatible. Product setup does not create another scheduler or nested
development-test harness in ordinary deployment. Diagnostics are secret-free.

## Acceptance scenarios

- Setup detects an ownership collision before mutation, composes both behavior
  families, validates the actual launched payload, and repeats idempotently.
- An upstream overwrite or interrupted composition is detected and repaired
  before enhanced dispatch; unrelated roots remain untouched.
- Readiness on a valid isolated root reports build, composition, schema,
  services, bindings, effective mode, pending work, and next action without a
  credential value.
- Operators can invoke the supported recovery, network-state, snapshot, and
  usage outcomes through the product's existing domain behavior rather than a
  second controller.

## Implementation freedom and unresolved decisions

The smallest supported operator interface and composition mechanism are
implementation choices. No product decision remains unresolved.
