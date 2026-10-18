# Erdős #41: audited predicate boundary

**Status:** new critical-review candidate, not a solution or a certified historical equivalence.

## Exactly what Lean checks

The pinned Formal Conjectures file at commit 85f863718beeec7b58a3a1926ee92e3472bc2020, blob 5e9eeb26586d087f4b2ab3d82734ea5ed87ddf50, defines an n-tuple condition by comparing equal sums of finite subsets of cardinality exactly n. It does not quantify repeated elements. PredicateComparison.lean defines the pinned provider quantifier form and proves its finite-carrier equivalence with our exact-three predicate. It implements this finite restriction for cardinality three and compares it with two other predicates.

On $B=\{1,2,3\}$:

- **Frozen exact-three Finset:** holds because $B$ has only one three-element subset.
- **Erdős 1980 at-most-three distinct-subset sums:** fails because $1+2=3$ compares a two-element subset with a one-element subset.
- **Repetition-allowed triple Multiset:** fails because $1+1+3=1+2+2$, although the two multisets differ.

Lean also proves that either stronger predicate implies the frozen exact-three predicate for every finite carrier. It does not prove either stronger predicate equivalent to the other, or any infinite density assertion.

## Primary-source evidence

P. Erdős, *A survey of problems in combinatorial number theory*, Annals of Discrete Mathematics **6** (1980), pp. 89–115, printed pp. **98–99**, PDF pp. 10–11:

https://www.renyi.hu/~p_erdos/1980-03.pdf

Printed p. 98 defines a Sidon-type B-r sequence using distinct summands selected with zero-or-one coefficients and at most r selected terms; all such sums must differ. This is a distinct-subset, at-most-r requirement, not repetition-permitted multiset uniqueness. Printed p. 99 then explicitly asks about the asymptotic growth of an infinite $B_3$ sequence. Consequently the **documented Er80 formulation differs from both** the frozen exactly-three-only predicate and the repetition-allowed predicate. For the original $B_3$ definition, the $B=\{1,2,3\}$ finite witness is not itself a $B_3$ set.

The maintained https://www.erdosproblems.com/41 uses the informal phrase triple sums of members of $A$, aside from trivial coincidences. That wording alone is not an exact formal quantifier declaration. The 1980 Erdős/Graham monograph and other citations may employ related but distinct conventions; their full cross-source concordance remains open. Do not relabel Er80 as definitively repetition-permitted or infer a refutation of the infinite conjecture.

## Reproducibility

Frozen Lean: leanprover/lean4:v4.29.1. Frozen mathlib commit: 5e932f97dd25535344f80f9dd8da3aab83df0fe6. The exact 104-line proof source has SHA-256 596a8a86cc67f75e8f67afa197f96732238b5979f77b349c91161a6c14f94e32, with companion receipt VERIFICATION.json. It compiled with exit code zero on authenticated CHAD in the existing mathlib cache at that exact git commit. Reproduce independently from this folder:

    lake update
    lake exe cache get
    lake env lean PredicateComparison.lean

This is a mathematical review candidate. A positive Lean kernel run is mathematical evidence for stated definitions only. Protected acceptance, Solve dispatch, MATHCERT and public claims remain separate.

## 2026-10-13: source-fidelity resolution on infinite carriers

The earlier frozen-provider finding above applies to historical Formal Conjectures commit 85f863718beeec7b58a3a1926ee92e3472bc2020 only. Upstream Formal Conjectures PR #5241 merged on **2026-09-01** and changed the live Erdős #41 hypothesis to a repetition-preserving Multiset. Thus the frozen exactly-three Finset defect is already corrected upstream, rather than being an open upstream issue.

See [Infinite-set fidelity and exact counterexamples](INFINITE_FIDELITY.md). Explicit infinite base-100 sets establish that (i) exact-three distinct-subset uniqueness is weaker than either historical at-most-three subset-sum uniqueness or modern repeated-summand uniqueness, and (ii) those two stronger hypotheses are incomparable. A rigorous positional-digit proof and finite table certificates accompany the examples.

Historical Er80 p. 98 uses zero-or-one summand coefficients and sums of at most three terms, while the explicitly repetition-permitted version is documented by Helm (1996) and represented in the current Formal Conjectures file. The two asymptotic *conclusions* are equivalent for any infinite set; the underlying *hypotheses* are not. Keep the modern M3 question OPEN and the Er80 H3 form as a distinct documented historical variant.
