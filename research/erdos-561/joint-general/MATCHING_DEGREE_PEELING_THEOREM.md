# Erdős #561 — universal vertex-cover peeling and complete matching-side solution

**Research date:** 2026-11-21. This source establishes an **unconditional analytic theorem for arbitrary finite simple graph hosts**. Ordinary, non-induced embeddings of the vertex-disjoint star components are used. The full Burr–Erdős–Faudree–Rousseau–Schelp conjecture for two *nonmatching* forests remains OPEN/PARTIAL; no MATHCERT certification is asserted. The previous matching saturated-prefix source result is strictly subsumed.

For a nonincreasing list $x=(x_1,\ldots,x_p)$ of positive integers, let $F(x)=\bigsqcup_{i=1}^p K_{1,x_i}$. The arrow $G\to(F(n),F(m))$ means that every red/blue edge colouring of $G$ contains the red forest or the blue forest with all its requested components vertex-disjoint.

## Lemma A — the full opponent forest survives vertex-cover deletion

Let $G\to(F(a),F(b))$, where $a$ has $p\ge2$ **positive** entries and $b$ is any positive star list. For **every** vertex set $S\subseteq V(G)$ with $|S|\le p-1$,

$$
\boxed{G-S\text{ contains an ordinary copy of }F(b).}
$$

**Proof.** Colour red every edge of $G$ having at least one endpoint in $S$ and colour every remaining edge blue. The red graph has vertex cover $S$. Every matching in the red graph therefore has size at most $|S|\le p-1$. Yet any red copy of $F(a)$ contains a matching of size $p$, selecting one edge from each of its $p$ vertex-disjoint positive stars. The red target is impossible. By arrowing, the blue graph contains $F(b)$, and every blue edge has both endpoints outside $S$. QED.

### Sequential degree peeling consequence

Write $B=\sum_i b_i$ and $b_1=\max_i b_i$. If the preceding arrow holds then

$$
\boxed{e(G)\ge(p-1)b_1+B.}
$$

Indeed, start with $S_0=\varnothing$. For $j=0,\ldots,p-2$, Lemma A ensures $G-S_j$ contains $F(b)$ and therefore has a vertex $v_{j+1}$ of degree at least $b_1$. Set $S_{j+1}=S_j\cup\{v_{j+1}\}$. **At that step**, removing $v_{j+1}$ deletes at least $b_1$ edges of the current graph, disjoint from all previously counted deletions. After $p-1$ steps, Lemma A still forces a complete $F(b)$ of $B$ additional, untouched edges. The total is at least $(p-1)b_1+B$ edges.

The degree measured at each step is the degree in the **remaining graph**, not the original graph. Consequently there is no double-counting penalty for edges joining previously selected high-degree centres. This is the crucial distinction from a simultaneous handshake estimate.

## Theorem B — new universal two-sided lower bounds on EVERY joint residual

Let $n_1\ge\cdots\ge n_s\ge1$ and $m_1\ge\cdots\ge m_t\ge1$ with $s,t\ge3$, and write $N=\sum_i n_i$, $M=\sum_jm_j$.

If arbitrary finite simple $Q$ satisfies both residual relations

$$
Q\to(F(n_2,\ldots,n_s),F(m_1,\ldots,m_t)),
$$

$$
Q\to(F(n_1,\ldots,n_s),F(m_2,\ldots,m_t)),
$$

then

$$
\boxed{e(Q)\ge\max\{(s-2)m_1+M,\ (t-2)n_1+N\}.}
$$

**Proof.** In the first residual, the red target has $p=s-1$ positive stars, so the degree-peeling consequence of Lemma A gives $(s-2)m_1+M$. For the second residual, exchange the two colours; its blue target has $t-1$ positive stars, and the red opponent has $n_1$ as largest star and $N$ edges, giving $(t-2)n_1+N$. Both bounds hold simultaneously. QED.

The identical method applied to the **original** Ramsey arrowing relation gives the general necessary bound

$$
e(G)\ge\max\{(s-1)m_1+M,\ (t-1)n_1+N\}.
$$

This is a universal lower bound, **not** an assertion that it always equals the full antidiagonal formula for two nonmatching forests.

## Theorem C — complete matching-versus-arbitrary-star-forest JOINT and ORIGINAL results

Take **any** integers $s,t\ge3$, and any nonincreasing positive list $m=(m_1,\ldots,m_t)$. Let the red original list be the matching profile

$$
n=(\underbrace{1,\ldots,1}_{s}).
$$

Then the **exact joint residual minimum** is

$$
\boxed{\mathcal J((1^s),m)=(s-2)m_1+\sum_{j=1}^t m_j.}
$$

Moreover the **exact ORIGINAL size-Ramsey number** over ALL finite simple graph hosts is

$$
\boxed{\widehat r(F(1^s),F(m))=(s-1)m_1+\sum_{j=1}^t m_j.}
$$

These hold without any parity, tail-uniformity, saturation or relation between $s$ and $t$. By symmetry, the same conclusion applies when the **blue** original forest is a matching.

**Lower bounds:** Theorem B supplies the sharp joint lower $(s-2)m_1+M$ from the first residual alone. Lemma A applied directly to original arrowing supplies the sharp original lower $(s-1)m_1+M$.

**Upper bounds:** The canonical antidiagonal list for the ORIGINAL matching-versus-star pair, under the one-based indexing convention of issue #3490, is

$$
w_2,\ldots,w_{s+t}
=(\underbrace{m_1,\ldots,m_1}_{s},m_2,\ldots,m_t).
$$

The original canonical star forest with this list arrows both targets and has $(s-1)m_1+M$ edges. Removing its first $m_1$-star leaves the canonical joint-residual antidiagonal host, of edge-size list

$$
(\underbrace{m_1,\ldots,m_1}_{s-1},m_2,\ldots,m_t),
$$

which arrows BOTH residual pairs and has $(s-2)m_1+M$ edges. This uses the independently source-proved exact disjoint-star antidiagonal criterion, not the unproved arbitrary-host conjecture. Both upper bounds match their analytic arbitrary-host lower bounds. QED.

### Example where earlier saturated-prefix conditions fail

Take the original red matching of four edges and a blue forest with star sizes $(9,3,2,1,1)$. The previous saturated-prefix result does not apply, because $9\ne3$. Here $s=4$, $M=16$, so the universal theorem proves

$$
\mathcal J((1,1,1,1),(9,3,2,1,1))=2\cdot9+16=34,
$$

$$
\widehat r(F(1,1,1,1),F(9,3,2,1,1))=3\cdot9+16=43.
$$

The exact canonical residual host has arm sizes $(9,9,9,3,2,1,1)$; the original host has $(9,9,9,9,3,2,1,1)$. Neither formula requires bounding the number of vertices or enumerating arbitrary graph shapes.

## General sufficient certificate for nonmatching pairs

For arbitrary lists $n,m$ define the **universal peeled bound**

$$
P(n,m)=\max\{(s-2)m_1+M,\ (t-2)n_1+N\}.
$$

Compute the canonical joint antidiagonal sum $J_{\mathrm{can}}=\sum_{k=3}^{s+t}w_k(n,m)$. If **for a particular nonmatching parameter pair** exact arithmetic shows

$$
P(n,m)=J_{\mathrm{can}},
$$

Theorem B and the canonical upper host immediately prove the full exact arbitrary-host joint residual at that pair. When strict inequality holds, $J_{\mathrm{can}}-P(n,m)$ is the remaining gap **of this peeling certificate**, not automatically a counterexample to the original conjecture. Other individually proved GCL bounds may fill it.

This explicit check is a theorem-to-theorem reduction and does not close issue #3490 for all nonmatching lists.

## Reproducibility and review boundary

The deterministic checker \`verify_matching_degree_peeling.py\` independently evaluates the antidiagonal maxima in zero- and one-based indices; checks every declared finite parameter tuple; independently audits the two-sided universal lower is no larger than the canonical joint upper; and exhausts complete star-arm red/blue allocation classes on selected original and joint canonical hosts with **nonuniform blue tails**. It verifies finite arithmetic and upper-host semantics, not the unbounded graph-topology proof, which is the vertex-cover argument above.

Claim 025 records the mathematical unrestricted-host theorem UNDER_REVIEW. Claim 026 records exact bounded checks CHECKED. The source proof is complete on paper for the stated matching-side cases; it has no Lean kernel certificate, independent MATHCERT review, or claim of unrestricted all-profiles Erdős #561.
