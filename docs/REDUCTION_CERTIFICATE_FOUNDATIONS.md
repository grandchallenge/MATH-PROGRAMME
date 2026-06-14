# Reduction and Certificate Foundations

<div class="programme-kicker">Foundation beneath lane 02</div>

# From symbolic transformation to a decision procedure

A Groebner basis is not fundamentally a special list of polynomials. It is a finite presentation of a terminating and confluent reduction system for congruence modulo an ideal.

That distinction matters. It explains why normal forms are canonical, why ideal membership becomes decidable, why critical pairs are certificate obligations, and why a successful computer algebra transcript is not yet a proof.

```text
representation
  -> oriented reduction
  -> termination
  -> local critical-pair closure
  -> confluence
  -> canonical normal forms
  -> decision procedure
  -> explicit certificate
```

This page defines the mathematical contract that sits beneath the [Computational Algebraic Geometry Lane](COMPUTATIONAL_ALGEBRAIC_GEOMETRY_LANE.md).

## Constructive algebra

The programme requires abstract structure and effective construction to meet.

An algebraic campaign is incomplete when it has:

- an existence theorem but no effective representation where one is needed;
- an algorithm but no proof of correctness or termination;
- a successful run but no stable witness;
- a certificate but no proof that the encoding matches the source problem.

The desired shape is:

```text
abstract theorem
  + effective construction
  + explicit representation
  + bounded implementation
  + independently checkable artifact
```

## Computation contract

Before an exact symbolic run, declare the mathematical interface independently of the chosen backend.

```yaml
carrier: polynomial_ring
coefficient_domain: QQ
coefficient_representation: reduced_rationals
variables: [x, y]
term_order: grevlex
order_decidable: true
reduction_strategy: declared
reduction_rules: []
equivalence_relation: congruence_mod_ideal
termination_measure: leading_term
local_confluence_obligations: critical_pairs
adequacy_statement: ""
normal_form_semantics: canonical_residue_representative
```

The backend and version belong in the resource ledger. The contract above explains what another backend must reproduce.

## Four proof obligations

<div class="programme-grid programme-grid--two" markdown>

<div class="programme-panel" markdown>
### Termination

No infinite reduction chain is possible. Polynomial reduction uses a well-founded term order as a decreasing measure.

A finite trace can be checked without proving a global normalization theorem. Do not confuse those claims.
</div>

<div class="programme-panel" markdown>
### Local confluence

Two immediate reductions from the same object must be joinable. In polynomial reduction, the relevant overlaps are represented by S-polynomials.

This is the finite critical-pair layer.
</div>

<div class="programme-panel" markdown>
### Confluence

All reduction paths from one object can be joined. Newman's lemma derives this from termination and local confluence.

Confluence is what makes normal forms independent of reduction choices.
</div>

<div class="programme-panel" markdown>
### Adequacy

Reduction must represent the intended equivalence. For ideal computation, two polynomials are equivalent when their difference belongs to the ideal.

A confluent system for the wrong congruence proves the wrong theorem cleanly.
</div>

</div>

## Certificate levels

Do not request a stronger certificate than the claim requires.

| Claim | Smallest typical certificate |
| --- | --- |
| One polynomial belongs to an ideal | `f = a1*g1 + ... + ak*gk` |
| One polynomial belongs to a radical | `f^N = a1*g1 + ... + ak*gk` |
| A finite set is a Groebner basis | Required critical pairs close under the declared order |
| Reduction gives canonical normal forms | Basis certificate plus termination and adequacy |
| Quotient-ring computation is correct | Canonical forms plus checked operation tables |
| Generated basis preserves the source ideal | Forward and reverse generator transformations |

A membership identity does not certify that its generators form a Groebner basis. A Groebner basis certificate does not certify that the polynomial encoding represents the original mathematical objects.

## Critical-pair ledger

A basis certificate should be reviewable as a finite ledger.

```yaml
left_generator: g_i
right_generator: g_j
lcm_leading_term: ""
s_polynomial: ""
omission_criterion: null
reduction_trace: []
result: 0
checker_status: unchecked
```

Every possible pair has one of two dispositions:

- processed, with an exact zero-reduction trace; or
- omitted, with the precise product, chain, or syzygy criterion that makes it redundant.

Optimized search and auditable certification are compatible only when skipped obligations remain explained.

## Standard representations

An ordinary identity proves membership:

```text
f = a1*g1 + ... + ak*gk
```

A standard representation additionally controls the leading terms of the summands. It shows that the representation respects the reduction structure rather than relying on cancellation above the target's leading term.

A standard-representation certificate records:

- the exact identity;
- the declared term order;
- the target leading term;
- the leading term of every nonzero product `ai*gi`;
- verification that each product lies within the required bound.

Weaker bounded representations may be used inside completion proofs, but must retain their actual bound.

## Provenance through generated bases

Search often replaces the source generators `F` by a computational basis `G`. The programme must preserve the route back.

```text
G = A * F
F = B * G
```

The polynomial matrices `A` and `B` provide:

- proof that the ideal did not change;
- provenance for each generated polynomial;
- translation of a basis-relative witness into source equations;
- a stable handoff from search notation to theorem notation.

Use:

```text
GENERATOR_TRANSFORMATION_CERTIFICATE
```

Required checks:

- generator ordering and matrix dimensions;
- exact forward and reverse identities;
- coefficient domain;
- canonical serialization of generators;
- the term order used to construct `G`.

## Syzygies and dependency

Syzygies identify all relations among generators. They serve two roles:

1. mathematical structure: redundancy, compatibility, and higher relations;
2. computation control: identifying critical-pair obligations generated by others.

A smaller generating set of leading-term syzygies can support a smaller critical-pair certificate. This is not automatically faster: the cost of proving redundancy can exceed the cost of processing the redundant pair. Record both the mathematical deletion and its measured computational effect.

## Effective ideal operations

Many apparently different obligations compile into a small set of constructions.

| Source question | Effective algebraic form |
| --- | --- |
| Remove auxiliary variables | Elimination ideal |
| Combine alternative algebraic branches | Intersection of ideals |
| Enforce a nonzero factor or remove its component | Saturation `I : f^infinity` |
| Prove vanishing over extension fields | Radical membership |
| Determine whether an expression is generated by invariants | Subring membership |
| Test finite solution structure | Finite canonical term basis of `K[X]/I` |
| Determine dimension | Independent variables or Hilbert data |

Each transformation needs a semantic note. Elimination projects; saturation removes components; radicalization discards multiplicity. They are not interchangeable cleanup operations.

## Universal-claim compiler

MATHSOLVE may compile a universal implication into an algebraic obligation only after declaring the model class.

For extension rings of a field:

```text
for all x, f1(x)=...=fm(x)=0 implies f0(x)=0
  -> f0 belongs to ideal(f1,...,fm)
```

For extension fields or integral domains:

```text
for all x, f1(x)=...=fm(x)=0 implies f0(x)=0
  -> f0 belongs to radical(ideal(f1,...,fm))
```

The corresponding artifact is:

```yaml
source_claim: ""
quantifier_shape: universal_implication
model_class: extension_fields
hypothesis_polynomials: []
conclusion_polynomial: ""
compiled_obligation:
  type: radical_membership
  ideal_generators: []
side_conditions: []
semantic_equivalence_argument: ""
```

Real validity is a different problem. Complex or algebraically closed validity can imply a real universal statement in some settings, but that route and its limitations must be explicit.

## Parametric branches

Specializing parameters can change leading terms and invalidate a basis. Parametric work therefore needs conditions, not one generic transcript.

A `PARAMETRIC_BRANCH_LEDGER` records for each branch:

- vanishing conditions;
- nonvanishing conditions;
- consistency status;
- specialized basis;
- critical-pair status;
- source-ideal preservation;
- conclusion valid on the branch;
- translation into source-language hypotheses.

This supports disciplined theorem repair:

```text
failed generic conjecture
  -> expose parameters
  -> split specialization branches
  -> identify missing hypotheses
  -> state restricted theorem
  -> certify branch conditions
```

Comprehensive Groebner bases and Groebner systems are routes for constructing such branch decompositions. Their output remains a candidate theorem partition until the branch conditions are interpreted mathematically.

## Order robustness

Term orders are computational choices that expose different initial ideals. The source ideal remains fixed, but intermediate size and explanatory form can change dramatically.

For small systems, an `ORDER_ROBUSTNESS_REPORT` may compare:

- reduced bases under several orders;
- leading ideals;
- basis and coefficient growth;
- invariant conclusions;
- conclusions that disappear when the order changes.

Universal Groebner bases provide an order-independent cover, but full computation is not a default requirement.

## Complexity contract

The programme records empirical and formal complexity separately.

### Empirical ledger

```yaml
variables: 0
input_polynomials: 0
max_input_degree: 0
max_coefficient_bits: 0
support_sizes: []
critical_pairs_generated: 0
critical_pairs_processed: 0
critical_pairs_omitted: 0
max_intermediate_degree: 0
max_intermediate_terms: 0
max_coefficient_bits_seen: 0
basis_elements: 0
wall_time_seconds: 0
peak_memory_mb: 0
```

### Formal warning

General ideal membership and Groebner construction have severe worst-case behavior. Historical lower-bound results include exponential-space hardness and doubly exponential degree growth in the number of variables.

These results are warning labels, not instance predictions. A small structured obligation can still be appropriate. A toy success does not weaken the warning.

## Transfer boundary

Do not transfer this certificate architecture to another algebraic category by analogy alone.

Before moving to noncommutative, differential, power-series, or local settings, re-establish:

- finite representation;
- computable coefficient operations;
- a well-founded reduction measure;
- a finite critical-pair theory;
- confluence or the exact weaker property required;
- adequacy for the intended equivalence;
- termination of completion.

Some noncommutative ideal-membership problems are undecidable. Differential polynomial rings introduce infinitely many derivative variables. Local and power-series methods reverse or modify the term-order logic. The transfer audit is a mathematical obligation.

## Pillar use

### MATHFORGE

MATHFORGE asks:

- What equivalence should normal forms decide?
- Which orientation makes reduction terminate?
- Which overlaps control local confluence?
- Can specialization change leading terms?
- Which source assumptions become inequations or saturation conditions?
- What transformation data will be needed to return to source notation?

It may emit:

```text
REDUCTION_SYSTEM_CARD
ADEQUACY_AND_CONFLUENCE_NOTE
CRITICAL_PAIR_LEDGER
STANDARD_REPRESENTATION_CERTIFICATE
GENERATOR_TRANSFORMATION_CERTIFICATE
WORD_PROBLEM_COMPILATION
PARAMETRIC_BRANCH_LEDGER
ORDER_ROBUSTNESS_REPORT
TRANSFER_VALIDITY_AUDIT
```

All remain candidate artifacts until replayed.

### MATHSOLVE

MATHSOLVE decomposes the campaign into:

```text
semantic obligation
  -> encoding obligation
  -> reduction and adequacy obligation
  -> termination obligation
  -> critical-pair obligation
  -> construction provenance
  -> minimized certificate
  -> independent replay
```

It selects the weakest sufficient certificate and records whether a failure came from representation, semantics, termination risk, critical-pair growth, coefficient growth, inconsistent branches, or an oversized witness.

## Deeper fixture

The first deeper fixture should prove a small universal implication over extension fields.

```text
source implication
  -> radical-membership compilation
  -> saturation for inequations
  -> favorable-order computation
  -> generator transformation matrices
  -> explicit identity f0^N = sum(ai*fi)
  -> independent polynomial-identity replay
  -> optional parametric branch split
  -> source-language restricted theorem
  -> MATHCERT handoff
```

The fixture succeeds when the semantic equivalence and final identity are checked. A zero normal form from one backend is insufficient.

## Source basis

This doctrine is substantially informed by Thomas Becker and Volker Weispfenning, with Heinz Kredel, *Groebner Bases: A Computational Approach to Commutative Algebra*. It extracts the source's reduction-theoretic and effective-algebra architecture without treating the text as authority for any new theorem claim.
