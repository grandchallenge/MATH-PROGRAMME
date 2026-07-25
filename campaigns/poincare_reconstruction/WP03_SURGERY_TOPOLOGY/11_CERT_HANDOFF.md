# PC-WP03 — MATHCERT handoff

## Certification target

Formalize the finite surgery-history logic without importing the target theorem or pretending to formalize the Hamilton–Perelman analytic core.

## Trusted boundary

The formal development may assume an abstract event contract corresponding to `PC02-T014`:

```text
each changed pre-component is diffeomorphic to a connected sum
of its post-component children and a finite list of permitted factors.
```

It may also assume:

```text
finite_on_bounded_intervals
finite_extinction
```

The source identity and hypothesis profile of these assumptions must remain in theorem statements or certificate metadata.

## Proposed data types

```text
FactorAtom
  | s3
  | sphericalSpaceFormNontrivial
  | s2BundleOrientable
  | s2BundleNonorientable

FactorCertificate
  factor_id
  source_refs
  normal_form : List FactorAtom

Summand
  | component ComponentId
  | factor FactorId

ReconstructionGroup
  pre_component : ComponentId
  summands : List Summand

Event
  index
  time
  active_before
  active_after
  ancestry
  groups
  source_refs

History
  initial_active
  events
  terminal_active
  extinction_time
```

`RP3#RP3` is parsed as an input certificate whose normal form contains two nontrivial spherical atoms; it need not be a primitive formal atom.

## First theorem slice

### `finite_history`

```text
finite_on_bounded_intervals(events)
and all event times <= T_ext
implies events is finite
```

For an imported JSON certificate the event list is already finite; the theorem records why the mathematical history can be represented by such a list.

### `backward_eval_sound`

Define a terminating evaluator that substitutes reconstruction groups from last event to first.

Prove, conditional on the abstract connected-sum interpretation:

```text
valid_history H
-> interpretation(initial_component)
   = connected_sum(Backward.eval H initial_component)
```

### `no_component_loss`

Prove that the active-set and partition invariants imply every changed component is represented by exactly one event equation and every new component has exactly one parent.

### `poincare_profile_discharge`

Over an abstract group-profile interface, prove:

```text
initial_group = trivial
-> every normal-form atom has trivial group profile
-> every atom is s3
```

The geometric theorem identifying a trivial-deck spherical space form with `S^3` remains an explicit imported interface unless already available.

## Executable certificate lane

The committed Python validator is a reference executable, not a proof kernel. MATHCERT should:

1. parse the same JSON format or a normalized export;
2. reject the malformed histories;
3. certify the two positive histories;
4. compare formal evaluator output with the Python output;
5. preserve source references in the resulting certificate.

## Soundness boundary

A formal proof of the history evaluator establishes:

```text
event contract + finite valid history => factor reconstruction.
```

It does not establish:

```text
Ricci flow produces the event contract.
```

No badge, README, or publication may omit this implication boundary.

## Acceptance gate

The first formal certificate is complete when:

- all identifiers and references are typed;
- event order and active-set evolution are checked;
- separating and nonseparating equations are represented;
- backward evaluation terminates structurally;
- evaluator soundness is kernel-checked;
- malformed fixtures fail;
- source provenance survives serialization;
- the theorem names state the imported assumptions.
