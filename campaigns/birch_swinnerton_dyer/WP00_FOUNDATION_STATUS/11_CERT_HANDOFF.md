# BSD-WP00 — MATHCERT handoff

## Purpose

This handoff separates the parts of WP00 that are suitable for exact machine checking from deep imported arithmetic-geometry theorems that must remain provenance-bearing interfaces.

## Claim boundary

MATHCERT must not encode any of the following as axioms merely to make the graph close:

- `rank(E(Q)) = ord_{s=1} L(E,s)` for all elliptic curves;
- finiteness of `Sha(E/Q)`;
- the strong leading-term formula;
- an unrestricted converse theorem;
- a comparison between a `p`-adic and complex order of vanishing without a named theorem.

## First formal targets

### `BSD-CERT-001` — statement-type separation

Represent rank BSD, `Sha` finiteness, the strong leading-term formula, Selmer-corank statements, and parity statements as distinct propositions. Prove only the explicitly admitted logical arrows in `05_STATEMENT_LATTICE.md`.

### `BSD-CERT-002` — corank consequence of the Selmer exact sequence

Given an exact sequence of cofinitely generated `Z_p`-modules

```math
0\to E(\mathbb Q)\otimes\mathbb Q_p/\mathbb Z_p
\to \operatorname{Sel}_{p^\infty}(E/\mathbb Q)
\to \Sha(E/\mathbb Q)[p^\infty]\to0,
```

certify

```math
\operatorname{corank}\operatorname{Sel}_{p^\infty}
=\operatorname{rank}E(\mathbb Q)+\operatorname{corank}\Sha[p^\infty].
```

The elliptic-curve and cohomological construction of the sequence may initially be imported. The corank algebra should be formal.

### `BSD-CERT-003` — complete/incomplete Euler-product conversion

Represent a finite omitted set `S` of Euler factors and certify that

```math
L^{(S)}(E,s)=L(E,s)\prod_{\ell\in S}P_\ell(\ell^{-s})
```

under the registry convention. Record the exact condition under which the finite multiplier is nonzero at `s=1`, hence preserves the order of vanishing.

### `BSD-CERT-004` — functional-equation parity interface

From an imported analytic function satisfying

```math
\Lambda(s)=w\Lambda(2-s),\qquad w\in\{-1,1\},
```

certify that the order of vanishing at `s=1` has parity determined by `w`. Do not infer its magnitude.

### `BSD-CERT-005` — ledger validation

Validate:

- unique claim, node, debt, and source identifiers;
- all dependency edges reference existing nodes;
- every implication has hypotheses and a direction;
- every theorem-derived claim has a source ID;
- every `p`-adic claim names a branch profile;
- no family-level scope is promoted to universal scope.

## Imported theorem interfaces

The following remain external theorem objects until dedicated formalization exists:

- Mordell–Weil finite generation;
- modularity of elliptic curves over `Q`;
- Gross–Zagier;
- Kolyvagin's Euler-system theorems;
- Rubin and Kato main-conjecture/Euler-system results;
- `p`-parity theorems;
- restricted converse theorems;
- strong-BSD or `p`-part formulas in restricted classes.

Each imported interface requires source metadata, exact hypotheses, conclusion, and normalization profile. A theorem name alone is not a valid interface.

## Suggested formalization boundary

A practical first implementation can use abstract types for:

- an elliptic curve;
- its Mordell–Weil group and rank;
- a cofinite `p`-primary Selmer module;
- a `p`-primary Tate–Shafarevich module;
- an analytic function with central functional equation;
- finite Euler-factor modifications.

This boundary captures the semantic errors WP00 is designed to prevent without requiring a complete formal library of arithmetic geometry.

## Completion criterion

The initial MATHCERT lane is complete when the statement lattice, corank calculation, finite-factor order invariance, parity interface, and artifact-ledger schemas replay without importing any open BSD statement.
