# HC-WP00 — Problem, source, and equivalence audit

**Audit date:** 2026-07-24  
**Campaign:** `HC-001`  
**Canonical tracker:** `MATH-PROGRAMME#65`

## 1. Audit determination

WP00 supports the following statements.

1. The canonical Hodge conjecture is a rational cycle-class surjectivity statement for smooth projective varieties over `C`.
2. The image of the algebraic cycle-class map lies in rational Hodge classes.
3. Surjectivity from `CH^p(X) tensor Q` is equivalent to rational generation by classes of irreducible codimension-`p` subvarieties.
4. The conjecture is established for `p=0,1,n-1,n`, and hence for all smooth projective varieties of complex dimension at most three.
5. The first unrestricted case not covered by those boundary arguments is dimension four, codimension two.
6. The naive integral conjecture is false in general.
7. The unrestricted compact-Kahler analogue is false in general.
8. Generalized, variational, Hodge-locus, absolute, motivated, standard-conjecture, and Tate statements are not equivalent restatements of the classical target.
9. The conjecture remains open according to the official current status.

WP00 proves no new algebraicity theorem.

## 2. Canonical statement

For smooth projective `X/C` and `0<=p<=dim X`, define

```math
Hdg^{2p}(X,Q)=H^{2p}(X,Q)\cap H^{p,p}(X).
```

The cycle class map factors through rational equivalence:

```math
cl_Q^p:CH^p(X)\otimes Q -> Hdg^{2p}(X,Q).
```

The target is surjectivity for every `X,p`.

The formulation permits finite rational combinations, including negative coefficients and denominators. It does not require a single effective cycle.

## 3. Source ledger summary

| ID | Source | Audited use | State | Remaining limitation |
|---|---|---|---|---|
| `HC-SRC-CLAY-DELIGNE` | Deligne official Clay essay | canonical statement, integral/Kahler boundaries, neighboring theories | `AUDITED` | not a complete modern special-case bibliography |
| `HC-SRC-HODGE-1950` | Hodge ICM address | historical formulation | `PRIMARY_IDENTIFIED` | exact passage concordance pending |
| `HC-SRC-KODAIRA-SPENCER-1953` | divisor class groups | Lefschetz `(1,1)` source family | `OPERATIONALLY_AUDITED` | exact historical locator refinement pending |
| `HC-SRC-ATIYAH-HIRZEBRUCH-1962` | analytic cycles | integral obstruction | `CORE_RESULT_AUDITED` | refined integral distinctions pending |
| `HC-SRC-KAHLER-ZUCKER-APPENDIX` | compact-Kahler counterexample | projectivity boundary | `OFFICIAL_RESULT_AUDITED` | exact appendix host/locator pending |
| `HC-SRC-VOISIN-2002` | Kahler counterexample | coherent-sheaf Chern-generation failure | `ABSTRACT_AUDITED` | keep formulation distinct from all analytic-cycle variants |
| `HC-SRC-GROTHENDIECK-1969` | general Hodge formulation | generalized statement boundary | `PRIMARY_IDENTIFIED` | corrected statement extraction pending |
| `HC-SRC-CDK-1995` | Hodge loci | parameter-locus theorem | `AUDITED` | does not construct cycles |
| `HC-SRC-ZUCKER-CUBIC-1977` | cubic fourfolds | selected higher-dimensional known case | `AUDITED` | special family only |
| `HC-SRC-DELIGNE-ABSOLUTE-1980` | abelian varieties | absolute Hodge result | `AUDITED` | absolute does not mean algebraic |
| `HC-SRC-ANDRE-1996` | motivated cycles | unconditional motivic substitute | `AUDITED` | motivated class broader than algebraic cycle |
| `HC-SRC-TATE-1965` | arithmetic cycles | Tate parallel | `PRIMARY_IDENTIFIED` | exact theorem-body normalization pending |
| `HC-SRC-CLAY-STATUS` | official status page | current open status | `AUDITED_2026-07-24` | not a complete bibliography |

The detailed source record is maintained in `grandchallenge/MATHFORGE`, branch `campaign/hc-source-audit`.

## 4. Equivalence audit

Let `Z^p(X)` be free on irreducible codimension-`p` subvarieties. The image of

```math
Z^p(X)\otimes Q -> H^{2p}(X,Q)
```

is exactly the rational span of their cohomology classes. Since rationally equivalent cycles have the same cohomology class, the map factors through `CH^p(X) tensor Q` without changing its image. Therefore:

```text
cl_Q^p surjective
<-> every rational Hodge class is a rational linear combination of subvariety classes.
```

This is the only equivalence promoted at WP00.

## 5. Boundary-case reconstruction

### Degree zero and top degree

Component and point classes generate the relevant rational Hodge groups, componentwise when `X` is disconnected.

### Divisors

Lefschetz `(1,1)` identifies degree-two integral Hodge classes with first Chern classes of line bundles. Divisors therefore generate the rational degree-two Hodge classes.

### One-cycles / codimension `n-1`

Let `h` be a hyperplane class. Hard Lefschetz gives

```math
L^{n-2}:H^2(X,Q) -> H^{2n-2}(X,Q).
```

This is an isomorphism of rational Hodge structures. A rational `(n-1,n-1)` class has a rational `(1,1)` preimage, represented by a rational divisor class. Its product with `h^{n-2}` is algebraic.

This argument uses the cohomological inverse to identify a preimage. It does not assume that the inverse Lefschetz operator is induced by an algebraic correspondence.

### Dimension at most three

For `n<=3`, every codimension lies in `0,1,n-1,n`. Thus the conjecture holds universally in these dimensions.

## 6. Counterexample boundaries

### Integral

Atiyah-Hirzebruch cohomology-operation obstructions give projective examples disproving naive integral surjectivity. The failure does not refute rational surjectivity and does not settle every restricted integral variant.

### Compact Kahler

Hodge decomposition survives on compact Kahler manifolds, but algebraic-cycle generation does not. The projectivity hypothesis supplies algebraic structure not encoded by Hodge decomposition alone.

## 7. Neighboring statements

### Hodge loci

Cattani-Deligne-Kaplan establishes algebraicity of loci where a flat integral class remains of Hodge type. This is a theorem about parameters, not a relative cycle.

### Generalized Hodge

The generalized conjecture concerns algebraic support/coniveau of Hodge substructures. Its corrected formulation and implications require separate source records.

### Variational Hodge

Remaining of type `(p,p)` under flat transport does not automatically transport an algebraic representative. That missing bridge is the variational problem.

### Absolute and motivated

Algebraic classes have strong stability properties. Absolute Hodge and motivated classes preserve enough structure to support motivic arguments, but they do not supply a general algebraic-cycle representative.

### Standard conjectures

Kunneth components and inverse Lefschetz operators define Hodge classes on products. Their algebraicity is a consequence expected from Hodge/standard conjectures, not free input.

### Tate

A Tate theorem after reduction does not automatically lift a cycle over `C`. Comparison, good reduction, specialization, field of definition, and lifting are independent obligations.

## 8. Computational boundary

Numerical periods may suggest that a class is rational and of type `(p,p)`. Exact certified arithmetic may prove a candidate cohomology relation for an explicit variety. Neither result by itself constructs a cycle or proves that all rational Hodge classes are generated.

## 9. Claim decisions

| Claim | Decision |
|---|---|
| Classical target uses `Q` and smooth projective `X/C` | promote |
| Cycle-map surjectivity equals rational generation | promote with direct proof |
| Boundary cases `0,1,n-1,n` | promote |
| Dimension at most three | promote |
| Arbitrary fourfold codimension two | retain open |
| Cubic fourfolds | retain as restricted known case |
| Naive integral conjecture | record false in general |
| Unrestricted compact-Kahler analogue | record false in general |
| Hodge locus implies class algebraic | reject |
| Absolute or motivated implies algebraic | reject without bridge |
| Tate implies Hodge by reduction/lifting | reject without complete bridge |
| Numerical periods decide algebraicity | reject |

## 10. Stage decision

The substantive source, normalization, and equivalence work is complete in draft. Promotion requires Amanuensis cross-document review, Referee review, and CI evidence. Until then, WP01, WP02, mechanism generation, computational work, and restricted-target selection remain closed.