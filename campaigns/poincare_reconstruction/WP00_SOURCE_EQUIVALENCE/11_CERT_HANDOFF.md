# PC-WP00 MATHCERT handoff

## Purpose

The first certification slice should check the terminal logical and combinatorial structure of the Poincaré proof without pretending to formalize Ricci flow, canonical neighbourhoods, surgery existence, or finite extinction.

The guiding separation is:

```text
imported geometric theorem interfaces
  -> finite surgery-history object
  -> connected-sum classification
  -> fundamental-group discharge
  -> S^3 conclusion.
```

Only the latter three layers are initial certification targets.

## Certification boundary

### In scope

1. Explicit definitions for finite factor labels:
   - spherical factor carrying a finite deck group `Gamma`;
   - orientable `S² x S¹` factor carrying `Z`;
   - optional non-orientable sphere-bundle factor, retained only for general theorem fixtures.
2. A finite rooted forest or event log describing:
   - component continuation;
   - connected-sum splitting;
   - removal of a permitted terminal component;
   - final extinction.
3. A validator that reconstructs the multiset/tree of initial factors from a valid extinct history.
4. A theorem that the fundamental group expression is the free product of factor groups, represented initially by a provenance-bearing algebraic interface if the full topological van Kampen theorem is unavailable.
5. A theorem that a free product expression equal to the trivial group has no nontrivial finite or `Z` factors.
6. A terminal rule identifying a spherical factor with trivial deck group as `S³` by the quotient definition.
7. Neutrality/associativity bookkeeping for connected sum with `S³`, represented at the exact level supported by the formal library.
8. Negative fixtures detecting:
   - an unrecorded component deletion;
   - a surgery event with the wrong parent/child count;
   - a non-permitted terminal component;
   - an extinction declaration with live components;
   - a hidden `Z` factor under a claimed trivial fundamental group;
   - use of the Poincaré theorem itself as an axiom in the terminal discharge.

### Explicitly out of scope

- definitions of Ricci curvature or Ricci flow;
- existence/uniqueness of smooth Ricci flow;
- Perelman entropy or reduced volume;
- `kappa`-non-collapsing;
- classification of `kappa`-solutions;
- canonical neighbourhood theorems;
- geometric construction of surgery caps;
- finite-extinction analytic inequalities;
- a theorem-prover badge claiming an independent formal proof of Poincaré.

## Proposed interface layers

### Layer C0 — abstract factors

Schematic Lean-like interface:

```lean
inductive PCFactor
| spherical (deck : FiniteGroupLabel)
| s2xs1
| twistedS2Bundle

inductive SurgeryEvent
| split (parent : ComponentId) (left right : ComponentId)
| discard (component : ComponentId) (factor : PCFactor)
| continue (before after : ComponentId)
| extinct
```

This is schematic and is not asserted to compile.

### Layer C1 — history well-formedness

Define and validate:

- unique live-component identifiers;
- acyclic ancestry;
- conservation of component ownership across events;
- permitted terminal labels;
- extinction only when no component remains.

### Layer C2 — factor reconstruction

Prove by induction over the finite history that each component is represented by a connected-sum expression over permitted factors.

The geometric theorem “actual Ricci surgeries induce such events” remains an explicit imported hypothesis with source identifiers `PC-L007` and `PC-L008`.

### Layer C3 — group-expression interpretation

Interpret the factor expression as a free-product expression:

```text
spherical(Gamma) -> Gamma
s2xs1 -> Z
twistedS2Bundle -> designated nontrivial group
connected_sum -> free_product.
```

If formal group free products are unavailable, begin with a normal-form syntax and prove only the syntactic triviality lemma. The artifact must state that this certifies an algebraic surrogate, not van Kampen's theorem.

### Layer C4 — simply connected discharge

Given the imported equality between the manifold fundamental group and the interpreted group expression, prove:

```text
pi_1(M) = 1
  -> no Z-labeled factors
  -> every finite deck label is trivial
  -> every remaining spherical factor is S^3
  -> the connected sum expression reduces to S^3.
```

## Formalization risks

1. Existing libraries may not have a usable connected-sum construction for topological or smooth manifolds.
2. Fundamental groups are defined only up to isomorphism; rewriting through free products may require substantial category-level infrastructure.
3. “Free product is trivial only if each factor is trivial” is mathematically elementary but may be expensive in a concrete group implementation.
4. A syntactic group-expression surrogate is cheaper but certifies less; the distinction must remain explicit.
5. Diffeomorphism neutrality of connected sum with `S³` may lack library support.
6. A finite history validator can be fully certified while the correspondence from geometric surgery to the history remains unformalized.
7. Naming an imported theorem as an axiom can obscure the boundary unless every interface carries provenance and `UNFORMALIZED_IMPORT` status.

## Acceptance criteria

- Every formal theorem references a `PC-*` spine node and a claim-ledger identifier.
- Every analytic or geometric imported assumption has source provenance and visible unformalized status.
- No imported assumption is named `poincare_conjecture` or otherwise packages the final conclusion.
- Positive fixtures cover single-component extinction, one split, nested splits, and multiple spherical factors.
- Negative fixtures fail closed on malformed histories and nontrivial factor groups.
- The README states exactly which logical layer has been certified.
- No public wording says “formal proof of the Poincaré conjecture” unless the entire imported chain has actually been formalized.

## First MATHCERT task

Implement and certify the finite factor-expression discharge:

> For an expression generated from spherical factors labeled by finite deck groups and sphere-bundle factors labeled by nontrivial groups, if its interpreted free-product expression is trivial, then every factor label is trivial and no sphere-bundle factor occurs.

This advances `PC-L012` and claim `PC-WP00-C006`. It does not depend on Ricci flow and does not certify the geometric decomposition theorem.