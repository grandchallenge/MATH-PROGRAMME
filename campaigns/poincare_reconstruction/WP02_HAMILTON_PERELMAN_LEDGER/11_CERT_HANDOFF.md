# PC-WP02 — MATHCERT handoff

## Certification boundary

The first formal target is not Ricci flow, canonical neighbourhoods, surgery existence, or finite extinction. Those remain provenance-bearing imported interfaces.

MATHCERT should certify the finite logical substrate that begins **after** a valid surgery-history certificate is supplied.

## Proposed abstract data model

```text
FactorType
  | sphere_form(deck_group)
  | s2_bundle_over_s1(twist_profile)
  | neutral_s3

TopologyEvent
  | split(parent, left, right)
  | nonseparating_cut(parent, child, bundle_factor)
  | discard(component, factor_expression)
  | extinction(component)

SurgeryHistory
  initial_component
  finite_ordered_events
  final_components = empty
  ancestry_well_formed
  every_event_satisfies_imported_topology_contract
```

The geometric proposition “this spacetime surgery satisfies the imported topology contract” is not part of the first formal slice. It appears as an explicit certificate input or unformalized theorem interface.

## Stage C0 — representation audit

Select library representations for:

- finite directed acyclic graphs or finite event lists;
- free groups/free products or a sufficient abstract group-expression algebra;
- connected-sum expressions as syntax;
- finite groups and triviality predicates;
- provenance-bearing assumptions.

Output: `PC_CERT_LIBRARY_AUDIT.md`.

## Stage C1 — finite backward reconstruction

Prove that a well-formed finite history ending in the empty component set reconstructs an expression for the initial component by backward induction over the event list.

The theorem should be purely combinatorial:

```text
valid_history H -> exists E, reconstructs H.initial E.
```

It must not assert that an arbitrary geometric surgery produces a valid event.

## Stage C2 — factor-group semantics

Assign group semantics to permitted factors:

```text
pi1(sphere_form Gamma) = Gamma
pi1(s2_bundle_over_s1 _) is nontrivial
pi1(connected_sum E1 E2) = free_product(pi1(E1), pi1(E2)).
```

Where full manifold/fundamental-group formalization is unavailable, use an explicitly labeled algebraic surrogate theorem over factor expressions. The surrogate must not be advertised as a theorem about all manifolds.

## Stage C3 — trivial free-product discharge

Prove the bounded algebraic statement:

```text
if the group expression associated with a permitted-factor connected sum is trivial,
then every deck group is trivial and no bundle factor occurs.
```

The proof may require a library theorem that canonical injections into a free product are injective. If that infrastructure is absent, formalize an inductive normal-form version for the specific finite expression grammar.

## Stage C4 — terminal `S3` normalization

Normalize a connected-sum expression containing only `sphere_form(1)` or `neutral_s3` factors to `S3`, using the imported identifications:

```text
sphere_form(trivial_group) = S3
M # S3 = M.
```

If these are not available as manifold theorems, keep them as named geometric imports and certify only the expression normalization.

## Stage C5 — adversarial malformed histories

Reject histories with:

- an event referring to a nonexistent component;
- multiple incompatible parents for one component;
- an unrecorded discarded component;
- a nonseparating cut without its bundle factor;
- a final nonempty component set labeled extinct;
- an event order that creates a cycle;
- a factor outside the imported permitted list;
- global finiteness inferred from local finiteness without an extinction time;
- an imported geometric proposition hidden as a definitional equality.

These fixtures operationalize `PC-FP-008`, `PC-FP-009`, `PC-FP-012`, `PC-FP-013`, and `PC-FP-014`.

## Proposed theorem interface

Schematic only:

```lean
structure ImportedSurgeryTopologyContract where
  -- provenance and theorem identifier remain visible
  source_id : String
  version : String

structure CertifiedHistory where
  events : List TopologyEvent
  wellFormed : WellFormed events
  finalEmpty : FinalComponents events = ∅
  importedContract : ImportedSurgeryTopologyContract

theorem terminal_discharge
    (H : CertifiedHistory)
    (hpi : groupSemantics (reconstruct H) = 1) :
    normalizeFactors (reconstruct H) = s3Expression := by
  ...
```

No `axiom` named `PerelmanProof` or equivalent may be hidden behind generated code.

## Acceptance criteria

- Every formal theorem has a `PC-WP02` or `PC-WP03` claim identifier.
- Every geometric input names its source/version and carries `UNFORMALIZED_IMPORT` status.
- Positive and malformed-history fixtures replay in CI.
- Local finiteness and finite extinction remain separate fields.
- The output wording is “certified terminal logic conditional on imported surgery topology,” not “formal proof of Poincaré.”
- The proof assistant and library versions are pinned.

## First executable certification item

Implement the finite factor-expression grammar and prove that a trivial group expression over spherical-space-form and `S2`-bundle factors contains no nontrivial factor, conditional on the declared free-product semantics.

This advances `PC02-T018`. It does not depend on solving a PDE or formalizing surgery geometry.
