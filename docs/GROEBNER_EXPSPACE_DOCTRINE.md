# Groebner and EXPSPACE Doctrine

## The warning

General Groebner computation has catastrophic worst-case behavior. In the fully general setting, basis size and related ideal-membership computations can grow beyond practical reach. The warning label is not cosmetic: a naive global encoding can turn a mathematical campaign into an EXPSPACE furnace.

The programme therefore adopts a hard rule:

> Groebner methods are a bounded certificate lane, not a universal open-problem solver.

This doctrine is the safety boundary for Groebner-backed work. The broader selection of resultants, quotient algebras, local methods, syzygies, and sparse geometry is defined in the [Computational Algebraic Geometry Lane](COMPUTATIONAL_ALGEBRAIC_GEOMETRY_LANE.md).

## What not to do

Do not encode an entire open problem as one large polynomial system and ask for a full Groebner basis.

Do not default to lexicographic order merely because elimination is desired.

Do not assume a Groebner basis is the right first method merely because the input is polynomial.

Do not let a CAS transcript become a theorem.

Do not hide timeouts, degree explosions, intermediate-term blowups, or failed reductions.

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

## The pillar split

```text
MATHFORGE:
  search for candidate witnesses using SageMath, SymPy, Singular, Magma, or custom exact routines

MATHSOLVE:
  classify the algebraic obligation, compare routes, declare budgets, and minimize the witness

MATHCERT:
  check the explicit witness or local theorem; never trust raw CAS output
```

## Verification beats rediscovery

Finding a Groebner basis can be expensive. Checking a proposed witness is often smaller and clearer.

MATHCERT should prefer artifacts such as:

```text
f = a1*g1 + a2*g2 + ... + ak*gk
```

or

```text
each S-polynomial reduces to zero by the listed reductions
```

or

```text
f^N belongs to I with an explicit coefficient witness
```

The certificate must be smaller and more auditable than the search that found it.

## Safeguards

Every Groebner-backed lane must record:

- coefficient domain;
- variable universe;
- monomial order;
- side conditions;
- maximum variables;
- maximum total degree;
- maximum runtime;
- maximum basis elements;
- maximum intermediate terms;
- backend and version;
- fallback route;
- failure status if the budget is exceeded.

## When to choose another lane

Use a different certificate lane when the algebra is not naturally small or another algebraic representation is structurally better.

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

## Bottom line

The value of Groebner theory for this programme is not magic solving. It is exact local masonry inside a larger method router.

```text
small algebraic obligation
  -> route comparison
  -> external witness
  -> explicit certificate
  -> Lean or exact replay
  -> local lemma
  -> larger human-guided theorem spine
```
