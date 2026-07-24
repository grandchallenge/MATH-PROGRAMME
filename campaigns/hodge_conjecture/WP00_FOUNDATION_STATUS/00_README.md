# HC-WP00 — Source, normalization, and equivalence audit

## Metadata

- Domain: Hodge conjecture
- Campaign: `HC-001`
- Work Package: `HC-WP00`
- Canonical tracker: `MATH-PROGRAMME#65`
- Primary type: source audit, statement normalization, known-boundary ledger, and proof-obligation map
- Global theorem-spine node advanced: `HC-T004`
- Claim status: canonical statement and elementary boundaries checked; universal surjectivity open
- Certification target: semantic schema and conditional abstract formalization
- Promotion state: `PROMOTED_2026-07-24`

## 1. Result-status box

| Field | Value |
|---|---|
| Result status | `WP00 PROMOTED / OPEN PROBLEM` |
| Conditions | Smooth projective `X/C`; rational coefficients; codimension-`p` cycles; singular cohomology with Hodge decomposition |
| Strongest supported claim | The exact target is surjectivity of `CH^p(X) tensor Q -> Hdg^(2p)(X,Q)`; it is known in codimensions `0,1,n-1,n`, hence for all dimensions at most three |
| Not claimed | Full Hodge, new known cases, integral/Kahler variants, a Tate reduction, an algorithm, or numerical evidence of algebraicity |
| Support-route class | `CONTINUUM_PROOF`, `PRIMARY_SOURCE_AUDIT`, `NEGATIVE_RESULT`, `SEMANTIC_CORRESPONDENCE_AUDIT` |
| Certification state | Human source and logic audit promoted; abstract schema committed; full geometry formalization unavailable |
| First executable step | Execute WP01 false-proof fixtures and WP02 source-normalized known-case/construction ledger in parallel |

## 2. Lay companion

A smooth projective complex variety has a geometric description by algebraic subvarieties and a topological-analytic description by cohomology. Complex geometry splits cohomology into Hodge types.

Every codimension-`p` algebraic subvariety produces a rational cohomology class of degree `2p` and type `(p,p)`. The Hodge conjecture asks for the converse: does every rational class of type `(p,p)` arise from a rational combination of algebraic subvarieties?

The difficult step is construction. Hodge type is a necessary analytic symmetry, but it does not itself exhibit a subvariety. Several neighboring theories recognize support, deformation loci, arithmetic invariance, or motivic stability without producing the required algebraic cycle.

The adjectives are structural:

- **rational:** the naive integral statement is false in general;
- **projective:** unrestricted compact-Kahler analogues are false;
- **combination:** subtraction and denominators are allowed; one effective cycle is not required;
- **every:** a theorem for very general members or sampled classes is restricted.

## 3. Canonical statement

Let `X` be smooth and projective over `C`, with `n=dim_C X`. Hodge decomposition gives

```math
H^k(X,C)=\bigoplus_{a+b=k}H^{a,b}(X).
```

For `0<=p<=n`, define

```math
Hdg^{2p}(X,Q)=H^{2p}(X,Q)\cap H^{p,p}(X).
```

Let `CH^p(X)` be the Chow group of codimension-`p` cycles modulo rational equivalence. The cohomological cycle map factors as

```math
cl_Q^p:CH^p(X)\otimes_Z Q -> Hdg^{2p}(X,Q).
```

The conjecture is

```math
for every X,p,alpha in Hdg^{2p}(X,Q),
there exists z in CH^p(X) tensor Q with cl_Q^p(z)=alpha.
```

## 4. Exact equivalence

Let `Z^p(X)` be free on irreducible codimension-`p` subvarieties. Its cycle-class image is the rational span of their cohomology classes. Since rationally equivalent cycles have the same cohomology class, quotienting by rational equivalence does not change this image. Therefore

```text
cl_Q^p is surjective
<-> every rational Hodge class is a rational linear combination of irreducible subvariety classes.
```

This equivalence does not assert effectivity, uniqueness, injectivity of the cycle map, or equality in the Chow group between cycles with equal cohomology class.

## 5. Elementary known boundary

For `n=dim_C X`:

- `p=0`: component/fundamental classes generate degree zero;
- `p=n`: point classes generate top degree componentwise;
- `p=1`: Lefschetz `(1,1)` identifies integral degree-two Hodge classes with first Chern classes of line bundles, hence divisor classes;
- `p=n-1`: hard Lefschetz gives an isomorphism of rational Hodge structures

```math
L^{n-2}:H^2(X,Q)->H^{2n-2}(X,Q).
```

A rational `(n-1,n-1)` class therefore has a rational `(1,1)` preimage. Lefschetz `(1,1)` makes that preimage a rational divisor class, and multiplication by the algebraic hyperplane class produces the required codimension-`n-1` algebraic class.

This argument uses a cohomological inverse to identify a preimage. It does **not** assume that inverse Lefschetz is induced by an algebraic correspondence.

For `n<=3`, every codimension lies in `0,1,n-1,n`. Hence the full conjecture holds for all smooth projective complex varieties of dimension at most three. The first unrestricted new case is `n=4,p=2`.

Smooth cubic fourfolds are retained as a special known case; they do not settle arbitrary fourfolds.

## 6. Formulation boundaries

The following are separate nodes in the statement lattice:

- naive integral Hodge: stronger and false in general;
- compact-Kahler analogue: broader and false in general;
- generalized Hodge: coniveau/support of Hodge substructures;
- variational Hodge: transport of algebraicity in families;
- Hodge-locus algebraicity: theorem about parameter loci, not cycle construction;
- absolute Hodge: stability property; no general converse to algebraicity;
- motivated cycles: broader correspondence class;
- Lefschetz standard conjecture: algebraicity of inverse Lefschetz correspondences;
- Tate conjecture: arithmetic parallel requiring comparison, specialization, and lifting;
- effectivity: an additional strengthening not present in the classical claim.

## 7. Principal obstruction nodes

Any proposed proof must survive:

1. rational versus integral coefficient control;
2. rationality versus arbitrary complex `(p,p)` type;
3. higher-codimension non-extrapolation from the divisor theorem;
4. non-algebraicity-by-default of Kunneth projectors and inverse Lefschetz;
5. Hodge-locus versus cycle-class distinction;
6. deformation transport without a relative-cycle theorem;
7. numerical period non-certification;
8. Tate comparison/specialization/lifting debt;
9. topological versus algebraic Chern generation;
10. incompleteness of Abel-Jacobi and normal-function tests in general;
11. absolute/motivated versus algebraic distinction;
12. very-general versus every-fiber quantifier control;
13. effectivity drift.

The canonical false-proof seed registry contains fifteen fixtures.

## 8. Trust quartet

### What is proved in the package?

- cycle-map surjectivity is equivalent to rational generation by irreducible subvariety classes;
- the `p=0,n` cases;
- the reduction of `p=n-1` to `p=1` through hard Lefschetz;
- the dimension-at-most-three consequence;
- effectivity is not part of the canonical statement.

### What is source-checked?

- Deligne's official rational/projective formulation;
- Lefschetz `(1,1)` as the divisor interface;
- the Atiyah-Hirzebruch integral obstruction;
- compact-Kahler failure boundaries;
- Cattani-Deligne-Kaplan Hodge-locus algebraicity;
- cubic fourfolds as a restricted known case;
- absolute, motivated, projector, and Tate distinctions;
- current official open status.

### What remains open?

- universal rational cycle-class surjectivity;
- arbitrary fourfold codimension-two classes;
- all higher unrestricted cases;
- every unproved algebraic-cycle bridge.

### What remains as nonblocking debt?

- exact Hodge 1950 passage concordance;
- exact Zucker compact-Kahler appendix locator;
- exact Grothendieck 1969 and Tate 1965 theorem-body normalization;
- comprehensive higher-dimensional known-case catalogue;
- full theorem-prover foundations for Hodge and Chow theory.

## 9. Certification boundary

MATHCERT may check claim-record schemas, semantic mutations, statement relations, abstract generator equivalence, and the boundary-case implication under explicit imported interfaces.

It may not encode the missing complex-algebraic-geometry stack as axioms and report the resulting conditional term as a proof of the Hodge conjecture.

## 10. Promotion evidence

- Programme PR: `grandchallenge/MATH-PROGRAMME#68`
- Forge PR: `grandchallenge/MATHFORGE#22`
- Solve PR: `grandchallenge/MATHSOLVE#63`
- Cert PR: `grandchallenge/MATHCERT#24`
- Programme policy checks: workflow `30084154340`, success
- Forge checks: workflow `30084108503`, success
- Solve checks: workflow `30084121944`, success
- Cert checks: workflow `30084135657`, success
- Agent Council: all blocking offices reviewed; no cross-document conflict
- Review record: `reviews/hodge_conjecture/HC-WP00.agent_review.yaml`

CI certifies repository and schema contracts. It does not certify the open mathematical conjecture.

## 11. Promotion decision

`HC-WP00` is promoted.

The promotion establishes only the canonical source, statement, equivalence, known-boundary, obstruction, debt, and certification architecture. It establishes no new Hodge theorem.

## 12. Next controlled stage

The following may proceed in parallel:

- `HC-WP01`: false-proof atlas;
- `HC-WP02`: source-normalized known-case and cycle-construction ledger.

The following remain closed:

- broad numerical period experiments;
- mechanism generation detached from a selected theorem target;
- `HC-R021` restricted-target selection;
- novelty claims;
- claimed-proof promotion;
- universal algebraicity claims.

## 13. Escalation gate

- [x] Exact canonical target recorded.
- [x] Equivalent formulation proved.
- [x] Elementary known boundary reconstructed.
- [x] Source ledger and audit states created.
- [x] Statement lattice and implication map created.
- [x] False-proof seeds created.
- [x] Proof debt and certification boundary created.
- [x] Cross-document Amanuensis review complete.
- [x] Referee review complete.
- [x] Cross-pillar CI evidence recorded.

The immediate obligations are now `HC-WP01` and `HC-WP02`.