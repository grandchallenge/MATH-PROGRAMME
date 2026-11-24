# Erdős 27 — source-scope reconciliation and finite residue bound

**Assignment:** ERDOS-PV-0027-A. **Scope:** source verification and reproduction of a published elementary lemma, not an independent replay of the full analytic proof. Source audit #1296 was already closed; reuse its RESULT/1 (6121316701) and separate review (6762158786). Same accountable GCL operator performs this separately scoped mathematical and adversarial pass; no external independent execution claimed.

## Source correspondence

The maintained problem asks whether a fixed real constant $C>1$ permits, for every positive epsilon and every $N\geq1$, a finite system of distinct moduli in the inclusive interval $[N,CN]$ with uncovered natural density at most epsilon. Its live page (24 November 2026 retrieval, last edit 16 July 2026) reports disproof. Source registry lock remains unchanged. The author manuscript of Filaseta, Ford, Konyagin, Pomerance and Yu, *Sieving by large integers and covering systems of congruences*, 21 December 2006, JAMS 20 (2007), 495–517, DOI 10.1090/S0894-0347-06-00549-2, PDF pp. 2–5, identifies the original quantitative conjecture and Theorem B. Theorem B concerns the minimum uncovered density over residue choices, not merely one choice; its uniform error depends only on fixed $c\in(0,1/2)$, under the stated upper bound for $K$.

For any fixed $C>1$, take $N'=N-1$ and $K=2C$ for $N\geq2$. Then $[N,CN]\subset(N',KN']$. Fix $c=1/4$; the permitted upper bound for $K$ grows without bound. Theorem B gives, for every such set of moduli and every residue choice, uncovered density at least $(1-o(1))\alpha$, where $\alpha=\prod_i(1-1/n_i)$. Since removing factors increases the product, the full inclusive interval gives the lower bound $(\lceil N\rceil-1)/\lfloor CN\rfloor$, tending to $1/C$. Consequently for all sufficiently large $N$ the density is at least $1/(2C)$, and epsilon $1/(4C)$ is impossible. This is exact quantifier/endpoint transfer from the published theorem, conditional on its proof, not a fresh analytic reconstruction. Historical original Er95 page remains a literature pointer; no claim of an independently inspected original Er95 scan.

## Reproduced finite lemma (paper Lemma 2.1 and Remark 1)

Use one uniform integer modulo the least common multiple of all moduli, and let $A_j$ be the event that it satisfies the j-th residue class. Write $p_j=1/n_j$, $q_j=P(\bigcap_{i\leq j}A_i^c)$, with $q_0=1$. Let $I_j$ consist of previous indices coprime to $n_j$; let $D_j$ be the other previous indices. The event of avoiding all classes indexed by $I_j$ depends only on the residue modulo their least common multiple, which is coprime to $n_j$. CRT therefore gives joint independence of that event from $A_j$ (not just pairwise independence). By the union bound, its probability is at most $q_{j-1}+\sum_{i\in D_j}p_i$. Hence

$$
q_j\geq(1-p_j)q_{j-1}-p_j\sum_{i\in D_j}p_i.
$$

Iterate this exact recurrence, retaining nonnegative factors:

$$
q_k\geq\prod_{j=1}^k(1-p_j)-\sum_{j=1}^k\sum_{i\in D_j}p_ip_j\prod_{u>j}(1-p_u).
$$

Each trailing product is at most one. Dropping these products in the subtraction yields Lemma 2.1. Independently uniform choices of the residues, followed by averaging over the same period, give expectation exactly $\prod_j(1-p_j)$, even for noncoprime moduli. This is the upper existence bound and must not be confused with the deterministic lower bound. Original credit FFKPY, not new GCL mathematics.

## Adversarial pass

The CRT argument uses coprimality with the LCM of the entire independent subfamily. Pairwise independence by itself fails: on two independent fair bits, the events first bit zero, second bit zero and bits unequal are pairwise independent but have empty joint intersection. In the arithmetic setting, moduli 2 and 4, residues 0 and 1, leave fraction 1/4, below the product 3/8; the correction term 1/8 is essential and sharp in that case. Finite replay checked all residue choices in 46 declared families (4,033 assignments) using exact rational arithmetic, including 1,815 weighted equalities. Source PDF page 4 visually inspected; theorem/lemma pages also text-checked, screenshot for page 5 unavailable. These finite checks do not certify the asymptotic theorem.

## Disposition and next action

Source scope ready for bounded verification. No frozen formal-provider file for #27. Proposed next Phase B: separately reproduce the smooth-modulus decomposition (Lemma 3.1) with exact LCM residue-class normalization, then kernel-formalize Lemma 2.1 and its weighted refinement in the pinned toolchain in the applicable formal lane. The full analytic Theorem B remains un-replayed. No new proof claim, MathCERT, article admission, or full-cohort closure. Phase B remains subject to protected selection and eligibility.
