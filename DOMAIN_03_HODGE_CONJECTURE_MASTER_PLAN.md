# DOMAIN_03_HODGE_CONJECTURE_MASTER_PLAN.md

## Domain

**Domain 03: Hodge Conjecture / Rational algebraicity of Hodge classes**

- Campaign identifier: `HC-001`
- Canonical tracker: `MATH-PROGRAMME#65`
- Base field: `C`
- Geometric category: smooth projective algebraic varieties
- Coefficients: rational
- Result status: `OPEN`
- Programme state: `HC_WP00_ACTIVE_SOURCE_NORMALIZATION`

## Canonical challenge

Let `X` be a smooth projective algebraic variety over `C`, let `n=dim_C X`, and let `0<=p<=n`. Hodge decomposition gives

```math
H^{2p}(X,C)=\bigoplus_{a+b=2p}H^{a,b}(X).
```

Define the rational Hodge classes

```math
Hdg^{2p}(X,Q)=H^{2p}(X,Q)\cap H^{p,p}(X).
```

The codimension-`p` cycle-class map is

```math
cl_Q^p:CH^p(X)\otimes_Z Q -> Hdg^{2p}(X,Q).
```

The Hodge conjecture asserts that `cl_Q^p` is surjective for every `X` and `p`.

Equivalently, every rational Hodge class is a finite rational linear combination of cohomology classes of codimension-`p` irreducible algebraic subvarieties.

## Exact campaign posture

The programme separates five logically distinct tasks:

1. recognize that algebraic cycle classes have Hodge type `(p,p)`;
2. retain the rationality condition, not merely complex Hodge type;
3. construct algebraic cycles representing arbitrary rational Hodge classes;
4. prove exact equality in rational cohomology;
5. preserve universal quantifiers across varieties, codimensions, classes, and families.

The easy direction `algebraic -> Hodge` is not evidence for the open converse.

## Mandatory formulation boundaries

The campaign does not identify the canonical target with:

- the naive integral Hodge conjecture, which is false in general;
- an unrestricted compact-Kahler analogue, which is false in general;
- representation by a single effective subvariety;
- the generalized Hodge conjecture on coniveau/support;
- the variational Hodge conjecture in families;
- algebraicity of Hodge loci;
- absolute Hodge or motivated classes;
- algebraicity of Kunneth projectors or inverse Lefschetz correspondences;
- the Tate conjecture or a reduction-modulo-prime statement;
- numerical period recognition;
- equality in Chow groups rather than equality of cohomology classes.

Every bridge between these statements must be recorded separately.

## Elementary known boundary

For `n=dim_C X`, the conjecture is established for

```text
p=0, 1, n-1, n.
```

- `p=1` is Lefschetz `(1,1)`.
- `p=n-1` follows from Lefschetz `(1,1)` and hard Lefschetz as an isomorphism of rational Hodge structures.

Therefore the full conjecture holds for all smooth projective varieties of dimension at most three. The first unrestricted new case is

```text
n=4, p=2.
```

Special fourfold families, including smooth cubic fourfolds, are known and remain source-indexed restricted cases rather than evidence for arbitrary fourfolds.

## Theorem spine

```text
HC-D000  Smooth projective varieties over C; dimension/codimension conventions
HC-D001  Hodge decomposition and rational Hodge classes
HC-D002  Algebraic cycles, CH^p, rational equivalence, and cycle classes
HC-L003  Algebraic cycle classes have type (p,p)
HC-T004  Rational cycle-class surjectivity target
HC-B005  Equivalent rational generation by irreducible subvariety classes
HC-K006  Boundary cases p=0,1,n-1,n
HC-K007  Dimension-at-most-three consequence
HC-K008  Source-indexed special higher-dimensional cases
HC-O009  Integral coefficient obstruction
HC-O010  Compact-Kahler obstruction
HC-O011  Projector/inverse-Lefschetz circularity
HC-O012  Hodge-locus/class algebraicity distinction
HC-O013  Variational/deformation transport debt
HC-O014  Numerical period non-certification
HC-O015  Tate specialization/comparison/lifting debt
HC-O016  Topological versus algebraic Chern generation
HC-O017  Abel-Jacobi incompleteness boundary
HC-O018  Absolute/motivated versus algebraic distinction
HC-O019  Generic-to-every-fiber quantifier obstruction
HC-T020  Full classical Hodge conjecture [OPEN]
HC-R021  First restricted theorem target [UNSELECTED]
```

## Dependency architecture

```text
D000 ─┬─> D001 ──────────────┐
      └─> D002 ─> L003 ──────┼─> T004 <─> B005 ─> T020
                              │
K006 ─> K007 ─────────────────┘

O009..O019 constrain every route into T004.
WP00 source/equivalence audit -> WP01 false-proof atlas + WP02 known-case ledger.
WP00 + WP01 + WP02 + prior-art audit -> R021 selection gate.
```

## Work Package sequence

### HC-WP00 — source, normalization, and equivalence audit

Status: active.

Required outputs:

- official/primary source ledger;
- notation registry;
- statement lattice;
- known-case boundary ledger;
- implication/non-implication ledger;
- theorem DAG;
- false-proof seeds;
- proof-debt register;
- MATHCERT formalization boundary;
- Agent Council review and Amanuensis integration.

### HC-WP01 — false-proof atlas

Status: closed until WP00 promotion.

Every semantic substitution and circular correspondence must become an executable fixture with an exact failure and scope.

### HC-WP02 — known-case and construction ledger

Status: closed until WP00 promotion.

For each admitted variety class, reconstruct the mechanism that constructs cycles or proves generation. A theorem-name list is insufficient.

### HC-WP03 — computational observatory

Status: closed.

Possible later role: exact symbolic intersection calculations, certified period computations, monodromy diagnostics, and finite lattice audits for explicit families. Computation can falsify proposed identities or guide construction; it cannot prove universal algebraicity without exact geometric closure.

### HC-WP04 — restricted-target selection

Status: closed.

A target is selected only after source, false-proof, known-case, and prior-art review. It must name an exact variety class, codimension, input class, cycle-construction obligation, and equality certificate.

### HC-WP05 — certification substrate

Status: abstract statement-hygiene lane active in MATHCERT.

Initial targets are claim-schema validation, statement-lattice checks, boundary-case implication logic, and generator/surjectivity equivalence in an abstract algebraic interface.

## Three-pillar split

### MATHFORGE

- primary and official source audit;
- current-status and known-case reconnaissance;
- hypothesis matrix;
- counterexample boundaries;
- false-proof fixtures;
- claimed-proof and novelty triage.

### MATHSOLVE

- formal statement and equivalence proof;
- theorem spine and dependency DAG;
- proof-obligation templates;
- construction-mechanism reconstruction;
- restricted-target selection after its gate.

### MATHCERT

- machine-readable claim schema;
- semantic mutation fixtures;
- conditional abstract proofs;
- formal-library gap ledger;
- provenance-bearing interfaces for imported Hodge and Chow theory.

## Foundational profile

- Carrier: smooth projective schemes/varieties over `C`, algebraic cycles, singular cohomology, and rational Hodge structures.
- Ambient structures: complex algebraic geometry, topology, sheaf cohomology, Hodge theory, intersection theory, and correspondences.
- Classical base: standard classical mathematics.
- Witness policy: a positive theorem requires an explicit or theorem-constructed algebraic cycle class, not merely a period signature or enlarged correspondence.
- Pathology risk: high, due to coefficient drift, torsion, cycle-equivalence drift, family quantifiers, non-algebraic correspondences, and conflation of necessary conditions with construction.

## Claim boundary

This campaign does not claim a proof, a new known case, an algorithm deciding Hodge classes, a reduction to Tate, or evidence from numerical periods. It organizes the exact open problem and its admissible proof obligations.

## Current executable stage

Complete `HC-WP00`. Mechanism generation, numerical experiments, restricted-target promotion, and novelty claims remain closed until the source-and-equivalence audit passes Agent Council and repository gates.