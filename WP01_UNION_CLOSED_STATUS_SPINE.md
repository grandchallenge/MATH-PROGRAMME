# WP01_UNION_CLOSED_STATUS_SPINE.md

## Work Package 01

**Title:** Union-Closed Sets: Status Spine and Certification Entry Point

**Primary type:** STATUS_SPINE

**Domain:** finite combinatorics, set systems, lattice-theoretic combinatorics

**Claim status:** no new theorem claimed

## 1. Lay executive companion

Frankl's union-closed sets conjecture is one of those mathematical problems that looks almost too simple to be dangerous.

Take a finite collection of sets. Suppose the collection has the following closure property: if two sets are in the collection, then their union is also in the collection. The conjecture says that, unless the collection is trivial, some element must appear in at least half of the sets.

The problem is easy to understand because it is about ordinary finite sets. It is hard because union-closure is a global condition. It says what happens when sets combine, but it does not directly tell us how often any single element must appear. The conjecture predicts that the closure pressure cannot be evenly hidden across all elements.

This Work Package does not prove the conjecture. It establishes the programme spine: the exact statement, known terrain, current partial-progress landscape, first finite sanity checks, formalization route, and the next certification target.

## 2. Formal problem statement

Let `U` be a finite universe and let `F ⊆ P(U)` be a finite family of subsets of `U`.

`F` is **union-closed** if for every `A, B ∈ F`, we have `A ∪ B ∈ F`.

For `x ∈ U`, define the frequency

```text
freq_F(x) = |{ A ∈ F : x ∈ A }|.
```

The family `F` is **Frankl-abundant** if there exists `x ∈ U` such that

```text
2 * freq_F(x) >= |F|.
```

Frankl's conjecture states:

> Every finite nontrivial union-closed family is Frankl-abundant.

The phrase nontrivial must be fixed carefully. For formalization we avoid ambiguous cases by requiring that `F` is nonempty and contains at least one nonempty set, or equivalently that the support of the family is nonempty.

## 3. Known terrain

The conjecture is open in general. It was posed by Péter Frankl in 1979 and is often called Frankl's conjecture. It is known for many special cases. Recent progress beginning with Justin Gilmer established the first dimension-free constant lower bound for the maximum element frequency proportion. Subsequent work improved the bound to approximately `(3 - sqrt(5))/2` and slightly beyond through refined information-theoretic and coupling methods.

This matters for the programme because it shows that the field is not stagnant. There is active structure to learn from. But these constant-bound results remain below the conjectured `1/2` threshold.

## 4. Equivalent viewpoints

The following viewpoints are relevant for future Work Packages:

### Union-closed families

The primary finite-set formulation.

### Intersection-closed dual families

Taking complements relative to the universe converts union-closure into intersection-closure and reverses frequency inequalities.

### Lattice formulation

Union-closed families can be studied through finite lattices, join-irreducibles, and closure systems. This is mathematically rich but requires care before Lean formalization.

### Information-theoretic formulation

Recent constant-bound progress uses entropy/coupling methods. This is powerful but less immediately Lean-friendly.

### Exact finite certificate viewpoint

For bounded universes or restricted classes, a finite enumerator can emit certificates that MATHCERT can verify.

## 5. First exact finite sanity audit

A small exact enumerator in this package checks all families on universes of size `n <= 4`. It verifies union-closure exactly and checks the Frankl condition exactly. Raw union-closed counts include the empty family. Frankl-facing counts use only nontrivial families with nonempty support. The result is:

```text
n = 0: raw union-closed families = 2, nontrivial = 0, violations = 0
n = 1: raw union-closed families = 4, nontrivial = 2, violations = 0
n = 2: raw union-closed families = 14, nontrivial = 12, violations = 0
n = 3: raw union-closed families = 122, nontrivial = 120, violations = 0
n = 4: raw union-closed families = 4960, nontrivial = 4958, violations = 0
```

The independent MATHCERT replay verifier reproduces these bounded counts and finds no violations. This is finite-domain certification and tooling validation, not evidence that the general conjecture is near resolution.

## 6. Claim ledger summary

| Claim ID | Claim | Class | Status | Promotion condition |
|---|---|---|---|---|
| UC-WP01-C001 | Frankl's conjecture states the half-frequency assertion for finite nontrivial union-closed families. | LITERATURE_DERIVED | OPEN_PROBLEM | Source audit and formal Lean statement. |
| UC-WP01-C002 | The conjecture remains open in general. | LITERATURE_DERIVED | AUDITED | Periodic literature refresh. |
| UC-WP01-C003 | Recent work gives dimension-free constants below 1/2. | LITERATURE_DERIVED | AUDITED | WP03 detailed source synthesis. |
| UC-WP01-C004 | Exact enumeration and independent replay find no violations for n <= 4. | COMPUTED_EXACTLY | CERTIFIED | Extend only with a separately reviewed larger-domain verifier. |
| UC-WP01-C005 | Union-Closed Sets is Lean-friendly relative to analytic domains. | HEURISTIC | PLAUSIBLE | WP02 formalization feasibility. |

A machine-readable ledger appears in `templates/union_closed_claim_ledger_wp01.yaml`.

## 7. Failure and danger analysis

The main danger is false simplicity. Many naive averaging arguments fail because union-closure constrains pairwise combinations without directly enforcing local frequency balance. A second danger is overvaluing small finite enumeration. A third danger is treating recent constant lower bounds as if they were morally close to the `1/2` conjecture.

WP01 therefore sets a conservative posture:

- use exact enumeration for tooling only;
- use literature synthesis for status only;
- use Lean definitions to control ambiguity;
- reserve theorem claims for later packages.

## 8. Certification boundary

This package contains:

- literature-derived claims;
- exact small finite computation;
- no new theorem;
- no Lean-certified proof yet.

The next certification movement is WP02: formal definitions and checked elementary lemmas.

## 9. MATHCERT handoff

The handoff should include:

```text
UnionClosedFamily.lean
Frequency.lean
FranklStatement.lean
MATHCERT/ci/replay_certificates.py
claim_ledger_wp01.yaml
certificate schema for finite-family enumeration
```

First Lean definitions:

```text
isUnionClosed(F)
freq(F, x)
support(F)
isNontrivial(F)
isFranklAbundant(F)
FranklConjecture
```

## 10. Next analytic target

WP02 proves the singleton-containing case in Lean:

> If `F` is union-closed and `{a} ∈ F`, then `a` appears in at least half of the members of `F`.

This is elementary but meaningful. The checked proof maps every set not containing `a` injectively to its union with `{a}`, which does contain `a`. WP04 extends the same pairing discipline to the two-element-member case.
