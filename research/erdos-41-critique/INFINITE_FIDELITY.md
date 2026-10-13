# Erdős #41: infinite-set source fidelity and three non-equivalent hypotheses

**Disposition:** SOURCE-FIDELITY-CLASSIFIED; no solution claim. The infinite lifting result below has an elementary written proof. The finite seed certificates are separately checked in Lean where the recorded compiler receipt is GREEN. We do not claim the entire infinite lift is Lean-formalized.

## Definitions

Let $A$ be a subset of the positive integers.

- **E3, exactly three distinct:** equal sums of three-element subsets of $A$ imply the subsets agree.
- **H3, historical at-most-three:** equal sums of subsets of $A$ of cardinality at most three imply the subsets agree, even when the cardinalities differ.
- **M3, three-term multisets:** equal sums of three-element multisets supported in $A$ imply the multisets agree, preserving repetitions.

For every set $A$, both H3 and M3 imply E3. The second implication identifies every three-element subset with its corresponding multiplicity-one multiset.

## Infinite lifting lemma

Fix $Q=100$ and $T=\{Q^n:n\geq1\}$. For a finite seed $B$ within $\{1,2,3,4,5\}$ define

$$
A_B=B\cup T.
$$

Each sum of at most three terms of $A_B$, even with repetitions, has the finite expression

$$
s_0+\sum_{n\geq1}c_nQ^n,
$$

where $s_0$ is the sum of the small seed terms, $0\leq s_0\leq15$, and the number of occurrences of $Q^n$ is $0\leq c_n\leq3$. These are genuine base-100 digits, with no carries. Uniqueness of finite positional expansions implies that equal sums have the same units value $s_0$ and equal coefficients $c_n$ at every higher position.

For *equal-length* sums, once all higher multiplicities agree, the number of seed terms agrees as well. Therefore a fixed-length collision can only survive if the seed itself has a collision *of the same cardinality*.

It follows rigorously for the full infinite set $A_B$ that:

1. Unique subset sums at each fixed seed cardinality up to three imply E3.
2. Unique seed subset sums across all cardinalities up to three imply H3.
3. Unique seed multiset sums at each fixed cardinality up to three imply M3.

For the first and third implications compare equal-length sums; for the second compare arbitrary subsets of at most three elements. This completes the infinite lifting lemma.

## Three explicit infinite counterexamples

**E3 but neither H3 nor M3:** $B_E=\{1,2,3\}$. Its distinct-element subset sums, grouped by cardinality zero through three, are respectively $[0]$, $[1,2,3]$, $[3,4,5]$ and $[6]$. Each fixed-cardinality list has distinct entries. Thus $A_{B_E}$ satisfies E3. However $1+2=3$ violates H3 and $1+1+3=1+2+2$ violates M3.

**H3 but not M3:** $B_H=\{1,3,5\}$. All eight of its subset sums, $0,1,3,4,5,6,8,9$, are distinct. Thus $A_{B_H}$ satisfies H3. Yet $1+1+5=1+3+3$ violates M3.

**M3 but not H3:** $B_M=\{1,4,5\}$. Its multiset sums by size are:
- size zero: $0$;
- size one: $1,4,5$;
- size two: $2,5,6,8,9,10$;
- size three: $3,6,7,9,10,11,12,13,14,15$.

Each fixed-cardinality list has no repeats. Thus $A_{B_M}$ satisfies M3. However $1+4=5$ violates H3.

**Theorem:** Even on infinite subsets of positive integers, E3 is strictly weaker than H3 and M3, and H3 and M3 are incomparable. There are no additional universal implications among these three predicates.

## Exact primary-source distinctions

**Erdős 1980:** P. Erdős, A survey of problems in combinatorial number theory, Annals of Discrete Mathematics 6 (1980), 89–115, printed pages 98–99, scan https://www.renyi.hu/~p_erdos/1980-03.pdf. Page 98 describes Sidon's B-r sequence using zero-or-one coefficients and explicitly says that sums using r **or fewer** selected distinct terms must differ. Page 99 states the unbounded subsequence growth question for infinite B3 sequences. Its stated definition is H3, not M3.

**Helm 1996:** M. Helm, On the Distribution of B3-Sequences, Journal of Number Theory 58 (1996), 124–129, https://www.sciencedirect.com/science/article/pii/S0022314X96900694. Its definition explicitly allows three summands with repetitions by requiring nondecreasing summand order. Its density question is for M3.

**Maintained catalogue:** https://www.erdosproblems.com/41 describes triple sums of members of A up to trivial rearrangements and associates its entry with both Er80 and later sources. Its current modern repetition-allowed reading is consistent with Helm. It must not be retroactively asserted that the Er80 printed definition also allows repetitions.

**Old frozen Formal Conjectures:** the GCL archived provider revision google-deepmind/formal-conjectures at commit 85f863718beeec7b58a3a1926ee92e3472bc2020 has the old cardinality-three Finset NtupleCondition (E3). Preserve its exact revision in historical provenance.

**Current Formal Conjectures:** upstream PR #5241, https://github.com/google-deepmind/formal-conjectures/pull/5241, merged on 2026-09-01 at commit 1c2a184fabcd54426dd875a3bb50acacd7f67bcf, explicitly replaced Finset by Multiset to preserve repeated summands. The current upstream file uses M3. The old E3 defect had **already been corrected upstream** before the GCL October audit; do not claim it remains unfixed or credit GCL with that upstream correction.

## Equivalence of the asymptotic *conclusions*

Let $A=\{a_1<a_2<\cdots\}$ be any infinite positive-integer set, and let $A(N)$ count elements not exceeding $N$. Without imposing any uniqueness condition,

$$
\limsup_{k\to\infty}\frac{a_k}{k^3}=\infty
\quad\Longleftrightarrow\quad
\liminf_{N\to\infty}\frac{A(N)}{N^{1/3}}=0.
$$

For left-to-right, take $N=a_k$ along the subsequence where $a_k/k^3$ diverges, so that $A(N)=k$. Conversely, take $N_j$ along which the normalized count approaches zero; put $k_j=A(N_j)+1$ and note $a_{k_j}>N_j$. Because the count grows unboundedly, $k_j/N_j^{1/3}\to0$, so $a_{k_j}/k_j^3\to\infty$.

Thus Er80's notation and the modern counting-function formulation have the same **conclusion**, but do not have equivalent **hypotheses**.

## Disposition and limitations

**Resolved:** primary source attribution for H3 (Er80), modern M3 provenance (Helm 1996), original frozen E3 revision, upstream September 2026 correction, and rigorous pairwise non-equivalence on infinite sets. The results justify recording H3 and M3 as separate historically attributed formulations.

**Not resolved:** whether the different density conjectures are logically equivalent in *truth value*. Our infinite counterexamples are very sparse; all have the asserted limiting ratio zero. They are not counterexamples to the Erdős density conjecture. Do not transfer proofs across the H3/M3 boundary without an independently established reduction.

**Requested mathematical adjudication:** accept the finite and infinite semantic classification as a source-critical result, retain historical variants, and keep the original asymptotic problem OPEN. No Solve dispatch, external theorem announcement or MATHCERT certification follows automatically.
