# HC-WP00 — Source, normalization, and equivalence audit

## Metadata

- Domain: Hodge conjecture
- Campaign: `HC-001`
- Work Package: `HC-WP00`
- Canonical tracker: `MATH-PROGRAMME#65`
- Primary type: source audit, statement normalization, known-boundary ledger, and proof-obligation map
- Global theorem-spine node advanced: `HC-T004`
- Incoming dependencies: Hodge decomposition; algebraic cycle-class construction; Lefschetz `(1,1)`; hard Lefschetz
- Claim status: canonical statement and elementary boundaries checked; universal surjectivity open
- Certification target: semantic schema and conditional abstract formalization
- Promotion state: draft pending integrated Council and CI review

## 1. Result-status box

| Field | Value |
|---|---|
| Result status | `WP00 DRAFT / OPEN PROBLEM` |
| Conditions | Smooth projective `X/C`; rational coefficients; codimension-`p` cycles; singular cohomology with Hodge decomposition |
| Strongest supported claim | The exact target is surjectivity of `CH^p(X) tensor Q -> Hdg^(2p)(X,Q)`; it is known in codimensions `0,1,n-1,n`, hence for all dimensions at most three |
| Not claimed | Full Hodge, new known cases, integral/Kahler variants, a Tate reduction, an algorithm, or numerical evidence of algebraicity |
| Support-route class | `CONTINUUM_PROOF`, `PRIMARY_SOURCE_AUDIT`, `NEGATIVE_RESULT`, `SEMANTIC_CORRESPONDENCE_AUDIT` |
| Certification state | Human audit complete in draft; abstract schema committed; full geometry formalization unavailable |
| First executable step | Execute WP01 false-proof fixtures and WP02 source-normalized known-case/construction ledger after promotion |

## 2. Foundational profile

```yaml
foundational_profile:
  carrier_type: continuum_and_algebraic
  ambient_structure:
    - smooth_projective_varieties_over_C
    - algebraic_cycles_and_Chow_groups
    - singular_cohomology
    - rational_Hodge_structures
    - correspondences_and_intersection_theory
  axiom_profile:
    base: classical_mathematics
    choice_usage: standard
    excluded_middle: used
  witness_policy:
    positive_claim: explicit_or_theorem_constructed_algebraic_cycle
    rejected_surrogates:
      - floating_point_period_relation
      - topological_correspondence_without_algebraicity
      - motivated_or_absolute_label_without_cycle_bridge
  certification_target:
    - human_source_audit
    - semantic_schema_validation
    - conditional_abstract_Lean
  pathology_risk:
    level: high
    notes: Coefficient, category, equivalence-relation, correspondence, and family-quantifier drift are principal risks.
```

## 3. Lay executive companion

### The two descriptions

A smooth projective complex variety can be studied through algebraic subvarieties and through cohomology. Algebraic subvarieties produce cohomology classes. Complex geometry splits cohomology into Hodge types.

A codimension-`p` algebraic subvariety always produces a degree-`2p` class of type `(p,p)`. The conjecture asks for the converse only for rational classes: does every rational class of type `(p,p)` come from a rational combination of algebraic subvarieties?

### The obstruction

Hodge type is an analytic/topological condition. Algebraicity is a construction requirement. Knowing that a class has the correct symmetry does not exhibit a subvariety. Many neighboring theories detect stability, support, deformation loci, or arithmetic invariance without constructing the required cycle.

### Why the adjectives matter

- **Rational:** the integral statement is false in general.
- **Projective:** arbitrary compact Kahler analogues are false.
- **Combination:** one may subtract cycles and use denominators; a single effective representative is not required.
- **Every:** a theorem for very general members or sampled classes is restricted.

### What WP00 achieved

1. Fixed the cycle-class-surjectivity statement and its exact coefficients.
2. Proved the equivalence with rational generation by irreducible subvariety classes.
3. Reconstructed the elementary boundary cases and the dimension-at-most-three consequence.
4. Separated eleven neighboring or false formulations.
5. Built a source ledger, statement lattice, implication map, theorem DAG, false-proof seeds, proof debt, and certification boundary.
6. Identified the first unrestricted new case as fourfolds in codimension two.

### What WP00 did not achieve

It did not construct a new algebraic cycle, prove a new family, or reduce the full problem to computation or arithmetic. It prepares the ground on which such a claim could be judged.

## 4. Formal problem statement

Let `X` be smooth and projective over `C`, with `n=dim_C X`. Hodge decomposition gives

```math
H^k(X,C)=\bigoplus_{a+b=k}H^{a,b}(X).
```

For `0<=p<=n`, set

```math
Hdg^{2p}(X,Q)=H^{2p}(X,Q)\cap H^{p,p}(X).
```

Let `CH^p(X)` be the Chow group of codimension-`p` cycles modulo rational equivalence. The cohomological cycle map factors as

```math
cl_Q^p:CH^p(X)\otimes_Z Q -> Hdg^{2p}(X,Q).
```

The target is:

```math
for every X,p,alpha in Hdg^{2p}(X,Q),
there exists z in CH^p(X) tensor Q with cl_Q^p(z)=alpha.
```

## 5. Object and obstruction

### 5.1 Necessary direction

For an irreducible codimension-`p` algebraic subvariety `Z`, its fundamental cohomology class has degree `2p` and type `(p,p)`. Linear combinations give

```math
image(cl_Q^p) subset Hdg^{2p}(X,Q).
```

### 5.2 Missing direction

The reverse inclusion asks for a geometric construction from an arbitrary rational Hodge class. Hodge decomposition alone contains no cycle-producing operation.

### 5.3 Minimal semantic obstruction

The vector space `H^{p,p}(X)` is complex. The input set is the rational intersection `H^{2p}(X,Q) intersect H^{p,p}(X)`. A basis or dimension calculation over `C` does not establish rationality, and rationality does not establish algebraicity.

### 5.4 Circular correspondence obstruction

Hard Lefschetz supplies cohomological isomorphisms. Treating their inverses or Kunneth projectors as algebraic correspondences in general assumes standard-conjecture-type algebraicity. Such use must be independently sourced for the selected variety class.

## 6. Known terrain and source audit

The authoritative detailed audit is `04_PROBLEM_AND_STATUS_AUDIT.md`; the cross-pillar primary ledger is in MATHFORGE.

| Source family | Use | Audit state |
|---|---|---|
| Deligne / Clay official description | canonical statement, boundaries, neighboring theories | `AUDITED` |
| Hodge 1950 | historical formulation | primary identified; passage concordance pending |
| Kodaira-Spencer / Lefschetz `(1,1)` | divisor case | operational theorem audited; historical locator refinement pending |
| Atiyah-Hirzebruch | integral obstruction | core result audited |
| Zucker/Voisin | compact-Kahler boundaries | result audited; one exact appendix locator pending |
| Cattani-Deligne-Kaplan | Hodge-locus theorem | audited |
| Zucker cubic fourfolds | selected fourfold known case | audited |
| Deligne absolute Hodge / Andre motivated cycles | substitute notions | audited at result level |
| Tate 1965 | arithmetic parallel | primary identified; exact modern statement extraction pending |
| Clay status | current open status | `AUDITED_2026-07-24` |

## 7. Claim ledger and trust quartet

### What is proved?

- Cycle-map surjectivity is equivalent to rational generation by irreducible subvariety classes.
- The boundary cases `p=0,n`.
- The reduction of `p=n-1` to the divisor case through hard Lefschetz as a Hodge-structure isomorphism.
- The dimension-at-most-three consequence.
- Effectivity is a strict extra demand, not part of the canonical statement.

### What is checked?

- Official formulation and current open status.
- Divisor theorem interface.
- Integral and compact-Kahler failure boundaries.
- Hodge-locus, generalized, variational, absolute, motivated, standard, and Tate statement separation.
- Cubic fourfolds as a restricted known case.

### What remains open?

- The universal cycle-class surjectivity target.
- Arbitrary fourfold codimension-two classes.
- Higher-dimensional unrestricted cases.
- Any bridge not independently established for a restricted class.

### What requires external verification?

- Hodge 1950 exact passage concordance.
- Exact Zucker appendix host/locator.
- Corrected generalized-Hodge theorem extraction.
- Tate 1965 exact theorem-body and coefficient normalization.
- Comprehensive known-case bibliography.
- Full theorem-prover foundations for Hodge and Chow theory.

## 8. Theorem spine

The machine-readable graph is `06_DEPENDENCY_DAG.json`. Its central chain is

```text
cycles -> rational Hodge classes
surjectivity <-> rational generation
Lefschetz (1,1) + hard Lefschetz -> boundary cases -> dimension <=3
all obstruction nodes constrain any route to universal surjectivity
```

## 9. Proofs and classified computations

WP00 uses no numerical evidence.

- Formal equivalence and boundary arguments: `CONTINUUM_PROOF`.
- Integral/Kahler failures: `NEGATIVE_RESULT`, literature-derived.
- Official/current determinations: `PRIMARY_SOURCE_AUDIT`.
- Statement lattice: `SEMANTIC_CORRESPONDENCE_AUDIT`.
- Certification artifacts: statement-schema and conditional abstract interfaces only.

## 10. Failure and negative-result analysis

Rejected shortcuts include:

- replacing `Q` by `Z`;
- replacing rational Hodge classes by arbitrary complex `(p,p)` classes;
- extrapolating Lefschetz `(1,1)` to higher codimension;
- assuming algebraicity of projectors or inverse Lefschetz;
- promoting algebraic Hodge loci to algebraic classes;
- transporting cycles through deformation without a relative-cycle theorem;
- promoting numerical periods, Tate classes, absolute classes, or motivated classes directly to algebraic cycles;
- extending very-general results to all fibers;
- demanding effectivity.

Each becomes a WP01 fixture.

## 11. Proof-debt register

`09_PROOF_DEBT.json` separates nonblocking provenance and formalization work from the open theorem itself. No debt is silently discharged by a secondary source.

## 12. Certification boundary

The first certifiable layer checks statement identity, relation graphs, boundary-case logic under visible imports, and generator/surjectivity equivalence. The universal theorem remains outside the current formal substrate.

## 13. First executable step

- Input: promoted WP00 artifacts and cross-pillar source/schema packages.
- Operation: execute WP01 semantic fixtures and WP02 known-case/construction reconstruction in parallel.
- Output: governed false-proof atlas and source-normalized mechanism ledger.
- Completion test: every false route fails exactly; every admitted known case identifies how cycles are actually produced.
- Spine nodes advanced: `HC-O009` through `HC-O019`, and `HC-K008`.

## 14. Escalation gate

- [x] Exact canonical target recorded.
- [x] Equivalent formulation proved.
- [x] Elementary known boundary reconstructed.
- [x] Source ledger and audit states created.
- [x] Statement lattice and implication map created.
- [x] False-proof seeds created.
- [x] Proof debt and certification boundary created.
- [ ] Cross-document Amanuensis review complete.
- [ ] Referee review complete.
- [ ] Cross-pillar CI evidence recorded.

WP01 and WP02 remain closed until the final three checks pass.