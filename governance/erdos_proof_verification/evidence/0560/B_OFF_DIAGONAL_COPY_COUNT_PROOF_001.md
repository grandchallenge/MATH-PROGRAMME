# Erdős #560, Phase B — bounded off-diagonal size-Ramsey counting theorem

**Assignment:** `ERDOS-PV-0560-B`. **Scope:** reconstruct a *known* off-diagonal lemma; do not claim to determine the diagonal size Ramsey number. **Claim:** `refs/heads/gcl-pv-claims/ERDOS-PV-0560-B`, SHA `321bcc27a63b0732b7154cc7dd0aa6d1fe3549f5` (held until protected admission). **Original source audit:** [issue #1831, RESULT/1 #6916199376](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1831#issuecomment-6916199376); frozen source-issue body SHA-256 `2bafa6656b0d797f8b7637be2d7ff77e7682e329467a9df9c858da7e9b7708c1`.

**Primary source:** D. Conlon, J. Fox, Y. Wigderson, *Three early problems on size Ramsey numbers*, arXiv:2111.05420v2 (2023-02-08), §2, Proposition 2.2 and its equation (1), https://arxiv.org/html/2111.05420v2 . The primary statement is also published in *Combinatorica* 43 (2023), 743–768. The following is an independently written derivation of the elementary counting method appearing there, including a tighter numerical simplification. It is not an independent replay of Theorem 1.1's later hypergeometric argument, nor of the original 1993 article.

## Exact definitions and claim

Let $H=(V,E)$ be any finite simple undirected graph with $q=|E|$ edges. For integers $s\geq2$ and $t\geq s+2$, define $N_{s,t}(H)$ to be the number of **ordered pairs of disjoint vertex sets** $(S,T)$ with $|S|=s$, $|T|=t$ and all $st$ cross-edges in $E$. Edges inside either side are unrestricted; this is not induced counting. Since $s<t$, this counts each individual copy of $K_{s,t}$ once, according to its uniquely sized bipartition.

**Theorem.** For all such $H,s,t$,

$$
N_{s,t}(H)\leq\left(\frac{4e^2q}{st}\right)^t
\leq\left(\frac{8e^2q}{st}\right)^t.
$$

Consequently, for every integer $q\leq st2^s/100$, no graph with $q$ edges is two-colour Ramsey for $K_{s,t}$. Thus, with the usual minimum-edge definition,

$$
\widehat r(K_{s,t})>\frac{st2^s}{100},
$$

which in particular implies the published weaker non-strict lower bound. Nothing here asserts the open diagonal asymptotic $\widehat r(K_{n,n})=\Theta(n^32^n)$.

## Independent complete derivation

If $q=0$ there are no copies and the bound holds. Otherwise enumerate $V$ as $v_1,\ldots,v_m$ in nonincreasing order of degrees $d_1\geq\cdots\geq d_m$. All ties may be broken arbitrarily. Counting both endpoints of each edge gives

$$
i d_i\leq\sum_{j=1}^i d_j\leq 2q,
\qquad
d_i\leq\frac{2q}{i}.
$$

Partition counted copies by the greatest index on their smaller bipartition side. Let $N_i$ count the copies in index bucket $i$. Buckets below index $s$ are empty. For an index $i$ at least $s$, the remaining $s-1$ members of the smaller side can be chosen among the first $i-1$ vertices. Any admissible $T$ must be a subset of size $t$ of the neighbours of $v_i$; ignoring its additional edges to the other vertices in $S$ and ignoring disjointness where it only overcounts gives

$$
N_i\leq\binom{i-1}{s-1}\binom{d_i}{t}.
$$

Use $\binom{i-1}{s-1}=\frac{s}{i}\binom{i}{s}$, the standard $\binom{a}{b}\leq(ea/b)^b$ for $a\geq b\geq1$, and the degree bound. The estimate also holds when $d_i<t$, because then $N_i=0$. Since $s\leq t$,

$$
N_i\leq
\left(\frac{ei}{s}\right)^s
\left(\frac{2eq}{it}\right)^t
\leq
\frac{(2e^2q)^t}{s^s t^t i^{t-s}}.
$$

Set $a=t-s\geq2$. The function $x\mapsto x^{-a}$ is positive and decreasing, so an integral dominates the tail:

$$
\sum_{i=s}^{m}i^{-a}
\leq\sum_{i=s}^{\infty}i^{-a}
\leq\int_{s-1}^{\infty}x^{-a}\,dx
=\frac{(s-1)^{1-a}}{a-1}.
$$

Summation and exact factorization yield

$$
N_{s,t}(H)
\leq
\left(\frac{2e^2q}{st}\right)^t
\frac{s-1}{a-1}\left(\frac{s}{s-1}\right)^a.
$$

Here $a\geq2$ and $s\geq2$ imply $(s-1)/(a-1)\leq s\leq2^s$ and $s/(s-1)\leq2$. Therefore the remaining factor is at most $2^s2^a=2^t$. This proves the asserted $4e^2$ bound. Proposition 2.2 uses a looser last comparison and reports $8e^2$; our purely algebraic tightening is **not a priority or novelty claim**. The exponent restriction $a\geq2$ is essential to convergence of the integral.

To obtain the Ramsey lower bound, colour each of the $q$ host edges independently and fairly red or blue. A particular pair $(S,T)$ has $st$ distinct cross-edges, and the probability that all are the same colour is exactly $2^{1-st}$. Copies need **not** be probabilistically independent: linearity of expectation gives

$$
\mathbb{E}[X]
=2^{1-st}N_{s,t}(H)
\leq
2\left(\frac{8e^2q}{st2^s}\right)^t.
$$

When $q\leq st2^s/100$, use the elementary strict bound $e<3$ to conclude

$$
\mathbb{E}[X]
\leq 2\left(\frac{8e^2}{100}\right)^t
<2\left(\frac{18}{25}\right)^t
\leq2\left(\frac{18}{25}\right)^4
<1,
$$

because $t\geq4$. A nonnegative integer-valued random variable with expectation below one has at least one realization equal to zero; otherwise its expectation would be at least one. Thus some edge two-colouring has no monochromatic copy, for **every** graph at that edge budget. All graphs with at most the threshold edges are non-Ramsey; the minimum possible Ramsey graph edge count exceeds it. No assumption about vertex count, regularity, connectivity, or induced copies was used.

## Independent computational evidence and stopping boundary

The producer groups pairs by $S$ and counts $\binom{|\bigcap_{v\in S}N(v)|}{t}$ via common-neighbour bitmasks. A separately implemented oracle enumerates **all disjoint** $(S,T)$ and inspects each cross-edge directly, without using common-neighbour intersection. Both agree on all 32,768 simple graphs on six vertices for $(s,t)=(2,4)$, plus 3,400 reproducible seeded graph cases of orders 7–9 at six parameter choices. Per-index $N_i$ upper bounds and degree ordering were also checked. For example, $K_7$ has 105 copies of $K_{2,4}$ and 30 in the last-vertex bucket, versus only 15 choices of four neighbours of the last vertex; removing the factor counting $S\setminus\{v_i\}$ would be false. A separate exact-rational loop checks the integral factor for 987 admissible $(s,t)$ parameter pairs.

Implementation: `ci/erdos_pv_bipartite_count_0560.py`; adversarial tests: `ci/test_erdos_pv_bipartite_count_0560.py`; deterministic receipt: `governance/erdos_proof_verification/evidence/0560/B_FINITE_COUNTING_001.json`. These finite checks test the count conventions and provide counterexamples to tempting incorrect shortcuts. The general claim follows from the displayed proof, **not** from extrapolating finite test counts.

**Result scope:** a complete, direct ordinary-paper proof of the bounded Proposition 2.2 interface for $s\geq2,t\geq s+2$ and a valid first-moment transfer. **Not established:** the diagonal asymptotic, the improved hypergeometric Theorem 1.1, a Lean no-`sorry` theorem, a source-to-Lean equivalence, independent external mathematical adjudication, or MATHCERT certification.

**Phase C obligation:** encode oriented $(S,T)$ subgraphs without inducedness, the degree-ranking combinatorial inequality, the convergent tail bound, and the strict first-moment threshold in a pinned Lean/Mathlib setting, followed by axiom output and adversarial type/semantic review. Phase B alone cannot unlock certification or count as a complete original-problem proof.
