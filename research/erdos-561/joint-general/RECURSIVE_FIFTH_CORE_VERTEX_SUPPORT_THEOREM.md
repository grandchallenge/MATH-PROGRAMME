# Erdős #561 — FIFTH sharp-JOINT-to-ORIGINAL transfer by saturated-core vertex support

**Research date:** 2026-11-24. **Mathematics:** new paper-level unrestricted-host deduction UNDER_REVIEW, bounded proof-tree classification CHECKED only after exact-head replay. **Scope:** arbitrary finite simple graphs, ordinary non-induced vertex-disjoint positive-star forests. This theorem is conditional on an INDIVIDUALLY proved sharp JOINT residual lower bound for the **same exact original lists**. The full Erdős #561 conjecture, the unrestricted JOINT hypothesis #3490, and MATHCERT certification remain OPEN/PARTIAL.

The protected source `GENERAL_CORE_ORIGINAL_TRANSFER.md` contained FOUR sufficient ORIGINAL transfers but left out a simple consequence of its already proved **maximum-degree core necessity lemma** and its ORIGINAL-forest vertex support bound. This addendum proves that consequence and integrates it as a FIFTH sound, source-dependent rule. It makes **no** assertion that the general JOINT bound is known for all profiles.

## 1. New fifth ORIGINAL transfer theorem

Let $n=(n_1,\ldots,n_s)$ and $m=(m_1,\ldots,m_t)$ be sorted positive star edge-size lists, $s,t\ge3$, with $n_1,m_1\ge2$. Put

$$
w_k=\max_{i+j=k}(n_i+m_j-1),\quad
W=\sum_{k=2}^{s+t}w_k,\quad
J=W-(n_1+m_1-1),
$$

$$
D=n_1+m_1-2,\qquad
R=\max\left(\sum_{i=1}^s(n_i+1),\ \sum_{j=1}^t(m_j+1)\right).
$$

Assume a **separate proven sharp simultaneous JOINT residual lower** for this pair: every finite simple graph $Q$ satisfying BOTH

$$
Q\to(F(n_2,\ldots,n_s),F(m)),\qquad
Q\to(F(n),F(m_2,\ldots,m_t))
$$

has at least $J$ edges.

**Theorem F (nonisolated-vertex saturated-core transfer, ANY leading parity):** Under those hypotheses, if

$$
\boxed{2W\le D^2+R,}
$$

then the exact original arbitrary-host size-Ramsey formula holds:

$$
\boxed{\widehat r(F(n),F(m))=W.}
$$

No leading-parity restriction is required. This is a fifth **sufficient** criterion, not a necessary condition, and does not replace the four previously admitted source criteria.

### Proof

The canonical antidiagonal disjoint-star host has $W$ edges and arrows the original forests, so assume toward a contradiction there exists an original-arrowing finite simple host $G$ with $e(G)\le W-1$.

Colouring all edges incident to any vertex $v$ RED or BLUE in the standard extension argument makes $G-v$ arrow BOTH specified residual pairs. Our individually assumed sharp JOINT lower thus gives

$$
e(G-v)\ge J=W-(D+1),\qquad
d_G(v)\le (W-1)-J=D.
$$

Let $\alpha=n_1-1\ge1$, $\beta=m_1-1\ge1$, so $\alpha+\beta=D$. If $G$ had a red/blue edge partition with red maximum degree at most $\alpha$ and blue maximum degree at most $\beta$, that colouring would avoid both full original target forests; contradiction. Hence no such capped partition exists.

Under the positive degree caps and the established degree bound, the source-proved Lovász degree-core necessity theorem in `research/erdos-561/formal-graph/LOVASZ_CAP_PARTITION_BRIDGE.md` forces a connected component of the induced subgraph of **degree-$D$ vertices** with at least $D+1$ vertices. In particular, writing $k$ for the number of vertices of degree exactly $D$, we have

$$
\boxed{k\ge D+1.}
$$

Under the all-RED and all-BLUE edge colourings, $G$ must contain the full original red and blue forests respectively. Every original star has positive size, so $G$ has at least $R$ **nonisolated** vertices. Let $N=v_+(G)\ge R$ denote their number; every nonisolated vertex not of degree $D$ contributes at least one to the degree sum. The handshake lemma therefore gives the **joint degree-and-vertex budget**

$$
\begin{aligned}
2e(G)&=\sum_{v\in V(G)}d_G(v)
\ge kD+(N-k)\\
&=N+(D-1)k\\
&\ge R+(D-1)(D+1)
=R+D^2-1.
\end{aligned}
$$

On the other hand the putative smaller host satisfies $2e(G)\le2W-2$. Combining with the fifth sufficient inequality $2W\le R+D^2$ yields

$$
2e(G)\le R+D^2-2<R+D^2-1\le2e(G),
$$

a contradiction. Thus no smaller original host exists. The canonical upper host attains $W$. QED.

**Important exact comparison.** The earlier ANY-parity transfer `W<=D(D+1)/2` uses only $k\ge D+1$ and ignores all other nonisolated vertices. The fifth criterion incorporates the required $R$ and can be strictly stronger whenever $R>D$. Conversely, the earlier parity-specific criteria remain potentially stronger elsewhere. Neither the stronger $2D+1$ saturated-core uniqueness theorem nor any new graph-factor theorem is needed here.

## 2. One newly settled simple original pair

Take original RED $n=(4,1,1,1)$ and original BLUE $m=(4,2,1)$. The exact canonical original antidiagonal weights are

$$
(w_2,\ldots,w_7)=(7,5,4,4,2,1),
\qquad W=23,\quad J=16.
$$

The RED original forest needs $4+1+1+1+4=11$ vertices, the BLUE needs $4+2+1+3=10$, so $R=11$. The leading degree budget is $D=4+4-2=6$, and

$$
2W=46\le D^2+R=36+11=47.
$$

The previously protected source engine has a provenance-bearing JOINT certificate for this exact profile. Therefore **the unrestricted-host ORIGINAL value equals $23$** by Theorem F.

The prior FOUR transfer conditions do NOT settle this example: both leading sizes are even; the any-parity half-core test requires $46\le D(D+1)=42$, false; neither leading size is odd, so both other parity-conditioned transfers are illegal. This is a genuine new original deduction, not a rephrasing of a previous admitted condition.

## 3. Executable well-founded proof-certificate composition

For the existing three-BLUE original profile domain, `verify_recursive_fifth_core_certificates.py` imports and **does not modify** the previously protected full four-condition engine `verify_recursive_vertex_budget_certificates.py` and its RED matching and THREEBLUE predecessors.

Its fifth transfer is enabled only when ALL of the following are checked on the exact source lists:

1. BOTH leading sizes are at least two; $D=n_1+m_1-2$ and $R=\max(\sum n+s,\sum m+3)$.
2. $2W\le D^2+R$ exactly, with an **inclusive** inequality. Equality is legal: the original host edge upper bound is $W-1$, giving the strict unit gap in the above contradiction.
3. An actual source-proved JOINT certificate is available for the SAME lists; no canonical star-host construction is substituted for a lower bound.
4. The previous four-condition engine has NOT already proved ORIGINAL, preventing redundant new certificate promotion.

A newly derived ORIGINAL result may recursively prove a JOINT relation for a STRICTLY shorter RED residual list if and only if its exact individually required first-residual canonical original $W(n_{2:},m)$ equals the current original JOINT canonical $J(n,m)$. The previous source-proved zero-deficit RED matching rule can also recurse on a strictly shorter RED list. Both operations strictly reduce RED list length, so recursion terminates and never consumes itself as evidence.

The new engine retains all predecessor certificates, including their theorem source labels. It reports additional ORIGINAL and additional JOINT profiles separately, and emits explicit nested theorem dependency traces. An `UNKNOWN` result is **not** a counterexample and must not be promoted.

## 4. Exact mathematical boundary and review requirements

Theorem F is an unrestricted-host implication from the source-proved Lovász degree-core necessity theorem and an EXACT individually proved sharp JOINT residual bound, but it does not establish the latter for unrestricted lists. The executable source classifier can identify large bounded regions where this new ORIGINAL transfer is effective; those are proofs by theorem composition, **not** a census of host graphs.

The mathematical manuscript and proof-tree composition remain **UNDER_REVIEW**, with finite integer/trace checking separately **CHECKED** after exact-head replay. Full general Erdős #561 JOINT and ORIGINAL statements remain OPEN/PARTIAL. Neither a protected source merge nor local OS-account test receipt constitutes external independent certification.