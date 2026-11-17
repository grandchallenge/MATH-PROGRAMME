# Erdős problem 560 — what has actually been verified?

*Documentary evidence record · 17 November 2026 · Grand Challenge Labs*

**Original problem: OPEN.** GCL has independently reconstructed a published **off-diagonal lower-bound lemma** and checked twelve supporting statements using Lean. It has **not** proved the requested diagonal asymptotic, formalized the complete published lemma in Lean, or received a MATHCERT certificate.

[Read the numbered Erdős problem](https://www.erdosproblems.com/560) · [Browse the GCL compendium entry](problems/0560.md) · [Understand the verification programme](../ERDOS_PROOF_VERIFICATION.md)

## The mathematical question

Suppose we colour the edges of a graph red or blue. A graph is *Ramsey for* a target graph if **every** such colouring produces a monochromatic copy of the target. The *size Ramsey number* (widehat r(F)) is the smallest **number of edges** of a graph Ramsey for (F).

Problem 560 asks for the asymptotic behaviour of (widehat r(K_{n,n})), where (K_{n,n}) has two parts of (n) vertices each, with all cross-edges present.

The [maintained catalogue](https://www.erdosproblems.com/560) describes the question as open. It records, for the stated ranges, the established bounds

[
rac{1}{60}n^2 2^n < widehat r(K_{n,n})
   < rac{3}{2}n^3 2^n,
]

and identifies the still-unproved prediction that the correct order is (Theta(n^3 2^n)). These results and that prediction come from the cited mathematical literature; GCL does not claim priority for any of them.

## The narrower theorem we checked

For integers (sgeq 2) and (tgeq s+2), consider a finite simple host graph (H) containing (q) edges. Let (N_{s,t}(H)) count pairs of disjoint vertex subsets of sizes (s) and (t) such that **every cross-edge** is present. Edges *within* the two subsets are allowed; the copies counted are not necessarily induced.

The Phase B ordinary mathematical proof establishes

[
N_{s,t}(H)leq
left(rac{4e^2q}{st}
ight)^t
leq
left(rac{8e^2q}{st}
ight)^t.
]

The looser (8e^2) constant is the published bound in Proposition 2.2 of Conlon, Fox and Wigderson. The smaller displayed constant follows from an elementary tightening of the last factor in the reconstructed counting argument; it is **not a claim of an original research discovery**.

The calculation orders host vertices by decreasing degree, bounds the number of copies in each degree-rank bucket, sums a convergent power-series tail, then colours host edges at random. The probability calculation uses *linearity of expectation*, not the false assumption that two overlapping bipartite copies are independent. The resulting **bounded** Ramsey conclusion is

[
widehat r(K_{s,t})>rac{st,2^s}{100}
qquad(sgeq2, tgeq s+2).
]

This does **not** establish the case (s=t=n). The required gap (t-sgeq2) is a genuine hypothesis of the particular proof: the integral-tail comparison used here fails when that gap is only one.

## What was tested

The mathematical count was checked using two separately implemented finite graph enumerators: one groups candidates by common-neighbour intersections, and the other examines every proposed pair of vertex subsets and its cross-edges directly.

- **36,168 finite graph cases:** every one of the (2^{15}=32,768) simple graphs on six labelled vertices, plus 3,400 seeded tests on graphs with seven to nine vertices.
- **987 exact-rational parameter checks** of the factor used to bound the power-sum tail.
- **Twelve Lean 4.33.0 kernel-checked auxiliary statements**, including the integer-cleared tail factor, the strict numerical first-moment threshold for (tgeq4), and basic semantic facts about disjoint sides, symmetric adjacency and non-induced copies.
- **Three false Lean targets rejected by the compiler**, challenging a weakened exponent condition, the missing power-tail gap, and graph looplessness.

The results have separate logical-role adversarial scrutiny. Those roles were carried out under the same authenticated GCL operator; they are **not independent human referees**. Finite enumeration is useful evidence of implementation correctness but cannot prove a general theorem for every finite graph.

## Exactly what the Lean kernel did not prove

The Lean declarations use an abstract, symmetric, loopless adjacency predicate and import only the standard `Init` library. They do **not** contain a kernel-checked equivalence to the relevant Mathlib `SimpleGraph.IsCompleteBetween` predicate.

The remaining formalization obligations are concrete: prove the number of candidate copies in the (i)-th degree-ranked bucket is bounded by
(inom{i-1}{s-1}inom{d_i}{t}); formalize the real analytic sum; and establish the finite edge-colouring union bound and minimum-edge quantifiers. None has been discharged by compiling the twelve auxiliary lemmas.

The frozen external FormalConjectures snapshot did not contain a statement file for problem 560. Thus there is **no pinned full Lean proof to replay**.

## Evidence and custodial provenance

| Stage | Authenticated result | Protected admission |
| --- | --- | --- |
| Source and scope | [Source audit #1831](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1831#issuecomment-6916199376) | [Phase A triage and source locks](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/governance/erdos_proof_verification/triage/0560-0564.json) |
| B — ordinary mathematical proof | [Worker result](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3230#issuecomment-6944746101) | [PR #3434](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3434), [custody #3436](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3436) |
| C — Lean applicability and adversarial review | [Worker result](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3243#issuecomment-6947981217) | [PR #3443](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3443), [custody #3449](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3449) |
| D — this documentary review | [Cohort issue #3256](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3256) | Governed protected admission required; publication status must be checked against the current branch |

The technical proof, independent finite tests, exact Lean replay and critical notes are stored under [the evidence directory](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/governance/erdos_proof_verification/evidence/0560). The [cohort ledger](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/governance/erdos_proof_verification/coverage/cohorts/0501-0600.json) records which stages have been admitted. A GitHub merge is an evidence-custody event, not a mathematical certification.

## Literature and outstanding work

Conlon, Fox and Wigderson, *Three early problems on size Ramsey numbers*, [arXiv:2111.05420v2](https://arxiv.org/abs/2111.05420) (revised 8 February 2023), Proposition 2.2; published in *Combinatorica* **43** (2023), 743–768, [DOI](https://doi.org/10.1007/s00493-023-00034-7). The [Erdős Problems #560 reference list](https://www.erdosproblems.com/latex/560) also records Erdős–Rousseau (1993), Erdős–Faudree–Rousseau–Schelp (1978), and Nešetřil–Rödl (1978) for the classical diagonal bounds. The primary GCL proof follows the first paper's known counting method; the earlier papers were not independently re-proved in this work package.

**Next mathematical obligation:** implement and kernel-check the degree-rank copy-count injection for actual finite Mathlib graphs, then the analytic and probabilistic bridges. **Next original-problem obligation:** determine the diagonal size-Ramsey asymptotic; that remains an open research question. MATHCERT status is **NOT_SUBMITTED**.
