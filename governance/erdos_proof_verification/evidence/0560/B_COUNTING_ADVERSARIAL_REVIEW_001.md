# Erdős #560 — adversarial critical pass on bounded Phase B proof

**Scope:** independent *logical-role* critique of `ERDOS-PV-0560-B`. This is a separate adversarial checking pass under the same authenticated operator, not a claim of a distinct human referee or independent Lean/MATHCERT certification. Source audit #1831; held reservation SHA `321bcc27a63b0732b7154cc7dd0aa6d1fe3549f5`.

## Exact obligations examined

1. **Non-induced semantics and unique orientation.** The producer uses vertex-set pairs, not induced bipartite subgraphs. Its direct independent oracle enumerates disjoint pairs without shared implementation of common-neighbour counting. Because the hypothesis is strictly $s<t$, no reversal of the bipartition is counted as another copy. In a host with extra intra-side edges, the cross-edges still determine a permitted non-induced subgraph.
2. **No dependence on tie ordering.** A deterministic choice among equal-degree vertices defines the buckets, but the proof relies only on nonincreasing degrees, not on a particular tie-break. All finite oracle cases agree with the bucket sum.
3. **Potentially fatal omitted factor.** If one tries to replace the paper's binomial choice of the other smaller-side vertices with one, the bound becomes false: for the complete seven-vertex graph and parameters $(s,t)=(2,4)$, the final index bucket has **30** oriented copies, while the last vertex has only $\binom{6}{4}=15$ possible four-neighbour sets. A legitimate count must select the smaller side too.
4. **Degree count and zero graph.** The sum of the first $i$ degrees is at least $i d_i$ and at most $2q$, including ties. All edgeless graphs yield zero target copies and the analytic bound is exactly zero, rather than generating division by zero.
5. **Power sum and exact range.** The integral step requires $t-s>1$; at $t=s+1$ the comparison integral diverges. The proof explicitly restricts to $s\geq2$, $t\geq s+2$. The factor $((s-1)/(t-s-1))(s/(s-1))^{t-s}$ is bounded by $2^t$ using only the integer inequalities $s\leq2^s$ and $s/(s-1)\leq2$. The resulting $4e^2$ coefficient is an elementary tightening of the original conservative $8e^2$ coefficient; no new theorem credit is claimed.
6. **Probabilistic independence correctly scoped.** Cross-edges within one copy are distinct, so its monochromatic probability is $2^{1-st}$. Events for different copies generally depend on common edges, but linearity of expectation does not require independence. The disjoint vertex-side choices do not imply independence of events.
7. **Strict expectation threshold.** For $s\geq2$ and $t\geq s+2$, necessarily $t\geq4$. The elementary bound $e<3$ reduces the published threshold to the exact rational inequality $2(18/25)^4<1$. Consequently the argument proves a strict lower bound on the minimum number of host edges. Non-integral threshold values require no fictitious rounding.
8. **Claim separation.** The proof is only of the Erdős–Rousseau/CFW *known* off-diagonal counting interface. It does not prove the 2023 hypergeometric bound, determine the order of the diagonal size Ramsey number, or certify the primary authors' full paper.

## Executed verification and deliberately hostile controls

The finite producer and a separately implemented direct enumerator agreed on **36,168** graph cases, of which 32,768 exhaust all simple graphs on six labeled vertices. Six further parameter configurations were sampled with one fixed PRNG seed; every configuration includes its complete graph as a positive control. The actual evidence fixture stores the precise per-configuration counts. The degree-rank bucket bound was checked for every case. A further **987** rational parameter cases independently evaluate the integral comparison.

Failures deliberately detectable by the checks include: replacing the non-induced count by an induced count; forgetting the smaller-side multiplicity; accepting $t=s+1$ or $s=1$ into the convergent-tail proof; accepting looped or asymmetric adjacency; using an expectation above one as a certificate of a monochromatic-free coloring; or treating finite enumeration as a universal mathematical proof.

One test fixture initially expected an incorrect value for the exact factor at $(s,t)=(3,5)$. Re-evaluation gives $9/2$, not $27/8$. The test was corrected and the full affected suite replayed green; no proof statement or implementation inequality was changed.

## Critical disposition

**PASS — BOUNDED OFF-DIAGONAL ORDINARY MATHEMATICAL PROOF, NOT THE OPEN PROBLEM.** The degree counting, integral tail and first-moment chain are valid under their explicit finite-simple-graph hypotheses. The finite checks and source-scoped adversarial pass support, but do not replace, the universal derivation. No-sorry Lean replay, axiom inspection, external review, original Erdős–Rousseau proof recheck, or MATHCERT certification has been performed.

**Next phase:** formalize the exact typed combinatorial and probabilistic claims with a pinned Lean/Mathlib toolchain, including source-to-formal semantic review, and retain the independent proof status as an ordinary bounded-lemma verification until the protected evidence package and held claim have been admitted.
