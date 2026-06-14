# Groebner and EXPSPACE Doctrine

## The warning

General Groebner computation has catastrophic worst-case behavior. In the fully general setting, basis size and related ideal-membership computations can grow beyond practical reach. The warning label is not cosmetic: a naive global encoding can turn a mathematical campaign into an EXPSPACE furnace.

The programme therefore adopts a hard rule:

> Groebner methods are a bounded certificate lane, not a universal open-problem solver.

This doctrine is the safety boundary for Groebner-backed work. The broader method selection is defined in the [Computational Algebraic Geometry Lane](COMPUTATIONAL_ALGEBRAIC_GEOMETRY_LANE.md). The proof-engineering basis is defined in [Reduction and Certificate Foundations](REDUCTION_CERTIFICATE_FOUNDATIONS.md).

## What not to do

Do not encode an entire open problem as one large polynomial system and ask for a full Groebner basis.

Do not default to lexicographic order merely because elimination is desired.

Do not assume a Groebner basis is the right first method merely because the input is polynomial.

Do not let a CAS transcript become a theorem.

Do not hide timeouts, degree explosions, coefficient growth, intermediate-term blowups, skipped critical pairs, or failed reductions.

## The reduction contract

A Groebner basis is a finite presentation of a reduction system for congruence modulo an ideal. Canonical normal forms require four ingredients:

- **termination:** the declared term order is well-founded and reduction decreases it;
- **local confluence:** every required critical pair is joinable;
- **confluence:** termination plus local confluence yields path-independent normal forms;
- **adequacy:** reduction represents equality modulo the intended ideal.

Do not request this whole contract when a smaller witness proves the claim. A single ideal-membership identity does not require certification of a complete basis.

## Certificate levels

```text
membership claim
  -> f = a1*g1 + ... + ak*gk

radical-membership claim
  -> f^N = a1*g1 + ... + ak*gk

basis claim
  -> complete critical-pair ledger under the declared order

canonical-normal-form claim
  -> basis claim + termination + adequacy

quotient-computation claim
  -> canonical forms + checked operation tables
```

The certificate must match the promoted claim exactly.

## The useful route

Groebner reasoning is valuable when the obligation is small, local, structured, and certificate-shaped.

Good targets include:

- polynomial identity checking;
- remainder-zero verification;
- ideal-membership witnesses;
- S-polynomial checks for a proposed basis;
- branch elimination in a finite chart;
- denominator-cleared algebra under explicit side conditions;
- finite truncations of a controlled family;
- elimination certificates for a small auxiliary block.

## Route before computing

Before committing to a basis computation, compare:

- a resultant or subresultant route for structured elimination;
- quotient-algebra and multiplication-matrix methods for finite systems;
- a favorable graded order followed by FGLM conversion;
- a Groebner walk toward an expensive target order;
- a local standard basis when the question concerns one point;
- Newton-polytope and mixed-volume methods for sparse systems;
- direct rewriting or another certificate lane.

The selected route must match the obligation, not the operator's preferred software.

## Provenance preservation

If search replaces the source generators `F` by a computed basis `G`, retain polynomial transformation matrices:

```text
G = A * F
F = B * G
```

These identities prove ideal preservation and translate a basis-relative witness back into source notation. Without them, a generated polynomial may be computationally useful but poorly connected to the theorem statement.

## Critical-pair accounting

A basis certificate must account for every possible critical pair:

- processed with an exact zero-reduction trace; or
- omitted under a named product, chain, or syzygy criterion.

An optimized algorithm may skip work. An auditable certificate may not skip explanation.

## The pillar split

```text
MATHFORGE:
  search for candidate witnesses, reduction systems, orders, and parametric branches

MATHSOLVE:
  classify the obligation, compare routes, declare budgets, preserve provenance, and minimize the witness

MATHCERT:
  check the explicit identity, critical-pair ledger, or local theorem; never trust raw CAS output
```

## Verification beats rediscovery

Finding a Groebner basis can be expensive. Checking a proposed witness is often smaller and clearer.

MATHCERT should prefer artifacts such as:

```text
f = a1*g1 + a2*g2 + ... + ak*gk
```

or

```text
each required S-polynomial reduces to zero by the listed reductions
```

or

```text
f^N belongs to I with an explicit coefficient witness
```

The certificate must be smaller and more auditable than the search that found it.

## Safeguards

Every Groebner-backed lane must record:

- coefficient domain and representation;
- variable universe;
- monomial order and reduction strategy;
- side conditions;
- maximum variables and total degree;
- maximum runtime and memory;
- maximum basis elements and intermediate terms;
- maximum coefficient size;
- critical pairs generated, processed, and omitted;
- backend and version;
- fallback route;
- failure status if the budget is exceeded.

## Parametric work

Specialization can change leading terms and destroy a basis. A parametric campaign therefore needs a branch ledger containing vanishing and nonvanishing conditions, specialized bases, consistency status, and the conclusion supported on each branch.

Do not promote a generic computation across exceptional parameter values.

## When to choose another lane

Use a different certificate lane when the algebra is not naturally small or another representation is structurally better.

Alternatives include:

- resultants and subresultants;
- quotient algebras and exact linear algebra;
- local standard bases;
- syzygy or Hilbert-data calculations;
- sparse resultants and mixed-volume forecasts;
- direct rewriting;
- exact finite enumeration;
- interval arithmetic;
- SAT/SMT proof artifacts;
- linear or semidefinite programming certificates;
- human structural proof;
- Lean-native reasoning;
- domain-specific certificate ledgers.

## Transfer boundary

Do not move this doctrine unchanged into noncommutative, differential, power-series, or local settings. Re-establish representation, termination, finite critical-pair control, confluence, and adequacy. In some settings termination fails; in others ideal membership is undecidable.

## Bottom line

The value of Groebner theory for this programme is not magic solving. It is exact local masonry inside a larger method router and a rigorously specified reduction system.

```text
small algebraic obligation
  -> semantic and reduction contract
  -> route comparison
  -> external witness with provenance
  -> explicit certificate
  -> Lean or exact replay
  -> local lemma
  -> larger human-guided theorem spine
```
