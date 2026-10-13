# Erdős #41: logarithmic shell-energy audit and an exact multiscale target

**Research disposition:** proved discrete reduction; old proposed M3 shell-energy deficit is still OPEN. We did not prove it or refute it on M3 sets. Exact proofs below are elementary; computer tests are finite witnesses, not proofs of the infinite statements.

## 1. Definitions and triple-shell reduction

Let A be an infinite set of positive integers, and write

$$
m_j = |A\cap[2^j,2^{j+1})|,\quad
E_J = \sum_{0\le j<J}\frac{m_j^3}{2^j}.
$$

The earlier proposed M3 shell-energy statement is

$$
\liminf_{J\to\infty}\frac{E_J}{J}=0. \tag{S}
$$

Group three ordinary dyadic shells at a time:

$$
M_k=m_{3k}+m_{3k+1}+m_{3k+2},\qquad
u_k=\frac{M_k}{2^k},\qquad
d_k=\frac{|A\cap[1,8^{k+1})|}{2^k}.
$$

Then the exact recursion is

$$
d_k=u_k+\tfrac12d_{k-1},\qquad d_{-1}=0.
$$

Denote the energy of the kth grouped shell by

$$
z_k=\sum_{r=0}^{2}\frac{m_{3k+r}^3}{2^{3k+r}}.
$$

For all nonnegative occupancies (with no M3 assumption), we have

$$
z_k\le u_k^3\le36z_k. \tag{1}
$$

The first inequality follows from the elementary inequality that the sum of three cubes is bounded by the cube of the sum, using denominators at least $2^{3k}$. For the second, convexity gives $(x+y+z)^3\le9(x^3+y^3+z^3)$; each of the three denominators is at most $4\cdot2^{3k}$.

For $x,y\ge0$, the identity

$$
4(x^3+y^3)-(x+y)^3=3(x+y)(x-y)^2\ge0
$$

and the recursion imply

$$
d_k^3\le4u_k^3+\tfrac12d_{k-1}^3.
$$

Summing this inequality from $k=0$ to $K-1$, and using $u_k\le d_k$, gives

$$
\sum_{k<K}u_k^3\le\sum_{k<K}d_k^3
\le8\sum_{k<K}u_k^3.
$$

Together with (1) this yields the **exact finite inequality**

$$
\boxed{\frac1{288}\sum_{k<K}d_k^3
\ \le\ E_{3K}\ \le\ \sum_{k<K}d_k^3.} \tag{2}
$$

For an M3 set, the usual three-sum packing bound gives $m_j^3\le36\cdot2^j$, so the difference $E_{3K+r}-E_{3K}$ for $r=0,1,2$ is at most 72. Thus the difference between general J and J divisible by three has no effect on normalized liminf-zero questions.

**Conclusion:** for M3 sets, (S) is equivalent to

$$
\boxed{\liminf_{K\to\infty}\frac1K\sum_{k<K}
\left(\frac{A(8^{k+1}-1)}{2^k}\right)^3=0.} \tag{LC}
$$

This is a **logarithmic Cesàro cubic-density condition**, not merely the original pointwise liminf density dip. We are not asserting novelty for the elementary convolution estimate.

## 2. Why (LC) is genuinely stronger than a density dip under ordinary packing bounds

The following is **not an M3 set**. Its purpose is to disprove the assertion that the known cubic packing estimate, plus the Erdős density conclusion, implies (S).

Define the sparse excluded-shell index set

$$
G=\bigcup_{n\ge2}\{n^4,n^4+1,\ldots,n^4+n\}.
$$

In every dyadic shell indexed by $j\notin G$, place precisely $2^{\lfloor j/3\rfloor}$ integers, for example the first that many integers starting at $2^j$. Place no integers in the shells in G. Call the resulting infinite set F. It is a valid set because each shell has $2^j$ available positions.

Its shell occupancy satisfies $m_j\le2^{j/3}$, and

$$
\frac{m_j^3}{2^j}
=\begin{cases}
0 & j\in G,\\
1,\frac12,\frac14 & j\notin G,\quad j\bmod3=0,1,2.
\end{cases}
$$

The number of excluded indices below J is $O(\sqrt J)$, because the n-th excluded block contains n+1 indices and begins at $n^4$. Consequently

$$
\lim_{J\to\infty}\frac{E_J}{J}
=\frac{1+1/2+1/4}{3}=\frac7{12}>0.
$$

Nevertheless, at the end $j=n^4+n$ of each empty block, the number of elements preceding it is at most $6\cdot2^{n^4/3}$, while $N=2^{j+1}-1\ge2^{n^4+n}$. Hence

$$
\frac{F(N)}{N^{1/3}}\le6\cdot2^{-n/3}\longrightarrow0.
$$

Indeed $F(N)\le6N^{1/3}$ for **every** N. So F satisfies a global ordinary cubic counting bound, has the original density dips, and still violates (S). This construction does not assert F is B3; cross-shell B3 relations are precisely the missing information.

### Even isolated three-shell packing is insufficient

The same counterprofile satisfies each elementary M3 **single-shell or fixed-three-shell occupancy count**. For any $i\le j\le k$, classify a hypothetical unordered triple of elements by its three shell indices. If all indices are different the number of choices is $m_i m_j m_k$. If two coincide it is $\binom{m_i+1}{2}m_k$ (or its symmetric variant), and if all three coincide it is $\binom{m_i+2}{3}$. Since $m_t\le2^{t/3}$, all these counts are bounded by $2^{\max(i,j,k)}$ (the binomial factors are at most the corresponding powers of $m_t$ for integer occupancies). Thus each is at most the exact available sum-range cardinality $2^i+2^j+2^k-2$, since the other two powers sum to at least two. The synthetic occupancies obey these elementary necessary mixed-shell packing bounds simultaneously, yet their shell-energy mean approaches $7/12$ while their normalized counting function has dips to zero.

This is still **not** a B3 counterexample: satisfying isolated volume constraints does not ensure actual three-sum injectivity across different shell-label patterns. A proof must exploit genuine *simultaneous collision exclusion between patterns*, not simply reuse one packing inequality per shell triple.

**Adversarial conclusion:** the proposed shell lemma would be a strict strengthening of Erdős #41 at the level of general counting profiles obeying the same standard packing bounds. It cannot follow solely from those bounds, or from the density-dip conclusion alone.

## 3. A multiscale condition exactly equivalent to Erdős #41

For an M3 set A, the standard bound $\binom{A(N)+2}{3}\le3N$ implies $A(N)^3\le18N$. In particular $0\le u_k\le6$ for every k.

The recursion gives the exact formula

$$
d_k=\sum_{r=0}^k2^{-r}u_{k-r}.
$$

For any integer $L\ge1$ and $k\ge L-1$,

$$
\max_{0\le r<L}2^{-r}u_{k-r}
\le d_k
\le\sum_{r=0}^{L-1}2^{-r}u_{k-r}+12\cdot2^{-L}. \tag{3}
$$

The tail bound follows from $u_i\le6$ and summing a geometric series.

Sampling the monotone counting function at powers of eight shows the original M3 Erdős density conjecture is equivalent to $\liminf_k d_k=0$. Indeed, if $8^k\le N<8^{k+1}$ then $A(8^k-1)\le A(N)$ and $d_{k-1}\le4A(N)/N^{1/3}$, so a density dip at arbitrary N forces a dip at a preceding sample. Conversely a subsequence $d_k\to0$ yields a density dip at $N=8^{k+1}-1$, since $N^{1/3}\ge2^k$. These comparisons are uniform for large k. Using (3) and letting L increase gives an exact **finite-window valley equivalence**:

$$
\boxed{
\liminf_{N\to\infty}\frac{A(N)}{N^{1/3}}=0
\quad\Longleftrightarrow\quad
\forall L\ge1:\
\liminf_{k\to\infty}
\max_{0\le r<L}\frac{M_{k-r}}{2^{k-r}}=0.
} \tag{V}
$$

For the forward direction, take a subsequence with $d_k\to0$; the finite-window maximum is at most $2^{L-1}d_k$. For the converse, first choose L so that the tail $12\cdot2^{-L}$ is smaller than half a prescribed error, then use the valley condition to make each of the L preceding $u_i$ small enough that their weighted sum is below the other half. This gives arbitrarily late $d_k$ as small as desired.

Thus (V) is an **exactly equivalent** multiscale target, while (S) is an unproved potentially stronger averaging target.

## 4. New mathematical boundary: cross-scale obstruction

The standard signed-sum and mixed-window packing counts provide at most a uniform upper bound on each normalized local cubic occupancy. When summed over J shells they give only $O(J)$, not $o(J)$. Neither Helm's exclusion of a regular asymptotic $A(N)\sim\alpha N^{1/3}$ nor a finite greedy sequence fills this gap.

For M3, the unmet obligation is now precise: prove for every fixed L and every positive threshold that arbitrarily late **L consecutive base-8 shells** all have occupancy below that threshold times $2^k$; or instead prove a source-grounded shell-energy deficit using genuinely global B3 interactions.

A useful bounded auxiliary experiment is to fix L, a low threshold, and impose M3 uniqueness on a finite interval. Optimize the smallest possible maximum normalized occupancy across L consecutive shells subject to critical-density boundary constraints. This must include adversarial hostile tests, not only greedy growth. Neither a finite positive result nor a finite failure establishes the infinite theorem.

## 5. Related sources and provenance

- Martin Helm, *On the Distribution of B3-Sequences*, Journal of Number Theory **58** (1996), 124–129, DOI:10.1006/jnth.1996.0069; proves there is no infinite B3 sequence with $A(N)\sim\alpha N^{1/3}$, a restriction weaker than (S).
- Javier Cilleruelo and Rafael Tesoro, *Dense infinite Bh sequences* (2012), https://arxiv.org/abs/1206.3087; infinite B3 constructions with exponent below $1/3$.
- Christian Táfula, *Infinite Sidon-type sets for zero-sum linear forms* (2026), https://doi.org/10.1007/s00605-026-02211-4; balanced zero-sum forms admit stronger density arguments; odd B3 sign asymmetry remains a relevant obstacle.
- Source-controlled original GCL proposal: research/erdos-41-density/MULTISCALE_GATE.md, protected PR #2621.
- Research docket: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2622.

**Verdict:** conditional shell deficit remains OPEN. Quantitative equivalence (LC), the packing-only counterprofile, and the exact valley criterion (V) are established mathematical results with separate finite computational checks. There is no proof of Erdős #41.
