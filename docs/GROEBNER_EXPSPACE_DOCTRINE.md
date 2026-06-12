# Gröbner and EXPSPACE Doctrine

## The warning

General Gröbner computation has catastrophic worst-case behavior. In the fully general setting, basis size and related ideal-membership computations can grow beyond practical reach. The warning label is not cosmetic: a naive global encoding can turn a mathematical campaign into an EXPSPACE furnace.

The programme therefore adopts a hard rule:

> Gröbner methods are a bounded certificate lane, not a universal open-problem solver.

## What not to do

Do not encode an entire open problem as one large polynomial system and ask for a full Gröbner basis.

Do not default to lexicographic order merely because elimination is desired.

Do not let a CAS transcript become a theorem.

Do not hide timeouts, degree explosions, intermediate-term blowups, or failed reductions.

## The useful route

Gröbner reasoning is valuable when the obligation is small, local, structured, and certificate-shaped.

Good targets include:

- polynomial identity checking;
- remainder-zero verification;
- ideal-membership witnesses;
- S-polynomial checks for a proposed basis;
- branch elimination in a finite chart;
- denominator-cleared algebra under explicit side conditions;
- finite truncations of a controlled family;
- elimination certificates for a small auxiliary block.

## The pillar split

```text
MATHFORGE:
  search for candidate witnesses using SageMath, SymPy, Singular, Magma, or custom exact routines

MATHSOLVE:
  decide whether the local proof obligation is genuinely algebraic and worth routing

MATHCERT:
  check the explicit witness or local theorem; never trust raw CAS output
```

## Verification beats rediscovery

Finding a Gröbner basis can be expensive. Checking a proposed witness is often smaller and clearer.

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

Every Gröbner-backed lane must record:

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

Use a different certificate lane when the algebra is not naturally small.

Alternatives include:

- direct rewriting;
- exact finite enumeration;
- interval arithmetic;
- SAT/SMT proof artifacts;
- linear or semidefinite programming certificates;
- human structural proof;
- Lean-native reasoning;
- domain-specific certificate ledgers.

## Bottom line

The value of Gröbner theory for this programme is not magic solving. It is exact local masonry.

```text
small algebraic obligation
  -> external witness
  -> explicit certificate
  -> Lean or exact replay
  -> local lemma
  -> larger human-guided theorem spine
```
