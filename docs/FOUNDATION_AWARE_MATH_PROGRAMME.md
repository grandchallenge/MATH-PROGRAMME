# Foundation-Aware MATH-PROGRAMME Doctrine

Status: active programme doctrine  
Scope: MATH-PROGRAMME, MATHFORGE, MATHSOLVE, MATHCERT  
Doctrine: **No object without structure. No existence without provenance. No proof without an axiom profile.**

This doctrine is part of the current operating standards alongside the [Grand Challenge Pedagogy Standard](GRAND_CHALLENGE_PEDAGOGY_STANDARD.md), [Claim Boundary Doctrine](CLAIM_BOUNDARY_DOCTRINE.md), and [Classification and Discovery Standard](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/CLASSIFICATION_DISCOVERY_STANDARD.md).

## Purpose

The Grand Challenge MATH-PROGRAMME is foundation-aware by design. The stack should not treat every mathematical statement as an untyped assertion about bare sets. It should record the structure, regularity, construction discipline, proof strength, and certificate target that make the statement meaningful and trustworthy.

A naked set is not intrinsically convex, measurable, computable, topological, smooth, algebraic, or certifiable. Those properties appear only after the set is placed in an ambient structure with declared admissible operations. The programme therefore treats mathematical objects as structured records rather than anonymous membership collections.

## Core distinction

Every intake card, solver work package, and certificate ledger should distinguish:

```text
membership != geometry != measure != computation != certificate
```

A problem statement such as `let A be a subset of R` is incomplete unless the intended discipline is explicit. The correct refinement may be `A is finite`, `A is Borel`, `A is Lebesgue measurable`, `A is arbitrary and the claim is choice-sensitive`, or `A is computably presented`.

## Foundation layers

The programme uses a layered foundation model. This is not an attempt to ban classical mathematics. It is an attempt to make mathematical evidence explicit.

### F0: finite and computable core

Use whenever possible. Preferred for certificates and executable fixtures.

Typical objects:

- finite graphs, words, programs, matrices, complexes, polytopes, proof traces;
- decidable predicates and computably enumerable searches;
- rational, integer, interval, SAT, SMT, pseudo-Boolean, and proof-producing CAS artifacts.

Preferred evidence:

- explicit witness;
- bounded exhaustive check;
- small verifier;
- Lean/Coq theorem;
- SAT/SMT/PB/Groebner/interval certificate.

### F1: constructive and type-theoretic layer

Use when witness extraction, algorithmic meaning, or proof terms matter.

Typical obligations:

- avoid unmarked use of excluded middle;
- distinguish existence from construction;
- identify whether a witness is extractable;
- record any classical escape hatch.

### F2: ZF + DC regular analytic layer

Use as the default discipline for ordinary analysis, probability, dynamics, PDE, measure theory, and geometric analysis when full choice is unnecessary.

Preferred ambient settings:

- Polish spaces;
- standard Borel spaces;
- separable Banach/Hilbert spaces;
- compact metric spaces;
- Borel or Lebesgue-measurable sets;
- regular measures;
- explicitly stated compactness and separability hypotheses.

Dependent choice is permitted for countable iterative constructions, sequences, limits, and approximation procedures.

### F3: ZFC classical layer

Use when full choice, ultrafilters, arbitrary bases, maximal ideals, Tychonoff-style compactness, Hahn-Banach in full generality, or comparable principles are needed.

This layer is legitimate, but it must be marked. A theorem is not demoted because it is classical. It is made more trustworthy because its proof strength is declared.

### F4: determinacy, large-cardinal, and exotic-foundation research layer

Use only when the problem itself is foundational, descriptive-set-theoretic, or consistency-strength sensitive.

Claims in this layer must clearly separate:

- theorem inside a stated theory;
- consistency implication;
- relative consistency;
- heuristic or programme conjecture.

## Required foundational profile

All new MATH-PROGRAMME cards, work packages, and certificate ledgers should include this block, either inline or by reference. The machine-readable contract lives in [`schemas/foundational_profile.schema.json`](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/schemas/foundational_profile.schema.json).

```yaml
foundational_profile:
  carrier_type: finite | countable | continuum | higher_type | categorical | unknown
  ambient_structure:
    - vector_space
    - affine_space
    - metric_space
    - topological_space
    - measurable_space
    - probability_space
    - algebraic_structure
    - order_structure
    - computable_presentation
  regularity:
    - finite
    - decidable
    - computable
    - Borel
    - Lebesgue_measurable
    - compact
    - convex
    - smooth
    - Noetherian
    - separable
  axiom_profile:
    base: finite | constructive | ZF | ZF+DC | ZFC | stronger | unknown
    choice_usage: none | finite_choice | countable_choice | dependent_choice | full_choice | unknown
    excluded_middle: avoided | local | used | unknown
    large_cardinal_usage: none | consistency_background | essential | unknown
    determinacy_usage: none | local | essential | unknown
  witness_policy:
    existence_claim: explicit_witness | extractable | nonconstructive | contradiction_only | unknown
    witness_location: card | solver_artifact | certificate_artifact | absent
  certification_target:
    - Lean
    - Coq
    - SAT_certificate
    - SMT_certificate
    - pseudo_boolean_certificate
    - CAS_certificate
    - interval_certificate
    - human_audit
  pathology_risk:
    level: low | medium | high | unknown
    notes: ""
```

Historical artifacts may be backfilled gradually. New artifacts should include the profile unless the owning issue explicitly records why the profile is deferred.

## Stack responsibilities

### MATHFORGE

MATHFORGE owns intake discipline. It must preserve provenance, identify the carrier and ambient structure, mark regularity assumptions, and refuse to silently turn vague objects into classical arbitrary sets.

### MATHSOLVE

MATHSOLVE owns route discipline. It must choose tactics based not only on domain but also on foundational texture: finite, constructive, regular analytic, classical choice-heavy, or foundations-sensitive.

### MATHCERT

MATHCERT owns evidence discipline. It must certify not only whether a claim has a proof or artifact, but what kind of proof strength, choice dependence, witness status, and machine-checkable boundary the claim carries.

## Pathology governance

The presence of non-measurable sets, arbitrary selectors, nonconstructive bases, ultrafilters, or uncountable products is not forbidden. It is a signal that the problem has entered a high-pathology region and must be tagged accordingly.

When possible, replace arbitrary subsets with one of:

- finite;
- decidable;
- computable;
- open/closed;
- Borel;
- analytic/coanalytic;
- Lebesgue measurable;
- compact;
- convex;
- standard Borel;
- explicitly arbitrary and choice-sensitive.

## Review checklist

Before merging a mathematical work package, reviewers should be able to answer:

1. What is the carrier?
2. What ambient structure gives the statement meaning?
3. What operations are admissible?
4. What regularity assumptions are required?
5. What foundation or axiom profile is being used?
6. Does the proof use any form of choice?
7. Is the existence claim witnessed, extractable, or merely classical?
8. What certificate target, if any, can check the claim?
9. What pathology risk remains?
10. What would fail if the object were only a bare set?

## Programme invariant

The MATH stack should preserve this invariant end-to-end:

```text
structured object -> explicit route -> evidence artifact -> trust ledger
```

The point is not to make the stack philosophically ornate. The point is to make it harder for ambiguous mathematical objects, hidden choice principles, and uncheckable existence claims to pass through the pipeline as if they were ordinary executable evidence.
