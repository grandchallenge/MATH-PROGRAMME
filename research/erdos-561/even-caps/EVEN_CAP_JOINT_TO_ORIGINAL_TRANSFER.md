# Erdős #561 — joint-residual to ORIGINAL transfer with positive even caps

**Research date:** 2026-11-21. **Status:** new paper-level deduction UNDER_REVIEW, not independent public certification. This theorem transfers *any already proved sharp joint-residual lower bound* to the original size-Ramsey formula when both leading target star sizes are odd and at least three. It gives four explicit infinite families of original three-versus-many-star equalities using previously source-locked GCL residual proofs. This does **not** prove unrestricted Erdős #561 or general joint-residual issue #3490.

All graph hosts are finite simple graphs. Star-forest containment is ordinary, non-induced, and uses vertex-disjoint positive-edge stars. Let $n=(n_1,\ldots,n_s)$ and $m=(m_1,\ldots,m_t)$ be nonincreasing positive integers with $s,t\ge3$. Write $F(n)$ for the disjoint union of the corresponding stars. For the original antidiagonal sizes define

$$
w_k(n,m)=\max_{\substack{i+j=k\\1\le i\le s,\ 1\le j\le t}}(n_i+m_j-1),
\qquad
W=\sum_{k=2}^{s+t}w_k,
\qquad
J=W-w_2.
$$

As $w_2=n_1+m_1-1$, the difference $W-J=n_1+m_1-1$ is always exact.

## Theorem A: general even-cap sharp-residual transfer

Assume $n_1,m_1\ge3$ are both **odd**, and that every finite simple graph satisfying BOTH joint residual arrowing properties

$$
Q\to(F(n_2,\ldots,n_s),F(m))
$$

and

$$
Q\to(F(n),F(m_2,\ldots,m_t))
$$

has at least $J$ edges. Then the *original* asymmetric size-Ramsey equality holds:

$$
\boxed{\widehat r(F(n),F(m))=W.}
$$

**Proof.** The canonical disjoint-star upper host with star sizes $w_2,\ldots,w_{s+t}$ has exactly $W$ edges and arrows the original pair by the elementary greedy star-host theorem. Suppose for contradiction a finite simple graph $G$ has $e(G)<W$ and arrows $(F(n),F(m))$.

For every vertex $v$, the graph $G-v$ satisfies **both** residual arrowing properties. To prove the first, suppose a red/blue colouring of $G-v$ avoids red $F(n_2,\ldots,n_s)$ and blue $F(m)$, then colour every edge incident with $v$ red. In a red $F(n)$ at most one component can meet $v$; the other $s-1$ components dominate $F(n_2,\ldots,n_s)$ componentwise since $n$ is nonincreasing, contradiction. To prove the second, colour all edges incident with $v$ blue in an avoiding colouring of $G-v$; the same reasoning forces a blue $F(m_2,\ldots,m_t)$ if a full blue $F(m)$ were present. No previously absent opposite-colour edges are introduced.

By the hypothesis, $e(G-v)\ge J$ for every $v$. Hence

$$
d_G(v)=e(G)-e(G-v)\le(W-1)-J=n_1+m_1-2.
$$

Set $\alpha=n_1-1$ and $\beta=m_1-1$. Both are positive **even** integers and $\Delta(G)\le\alpha+\beta$. Apply the unconditional classical even-cap splitting theorem already proved in \`EVEN_CAP_DEGREE_SPLITTING_THEOREM.md\`: the edges can be coloured red/blue with red maximum degree at most $\alpha$ and blue maximum degree at most $\beta$. This colouring has no red star with $n_1$ edges and no blue star with $m_1$ edges, hence avoids the full original red and blue forests. That contradicts $G$ arrowing them. Therefore $e(G)\ge W$, completing the exact equality. QED.

**Constructive independence of the even-cap input.** The source-locked cap theorem is not a new conjectural Ramsey assumption. For $\alpha+\beta=2k$, complete two copies of $G$ to a $2k$-regular loopless multigraph using $\alpha+\beta-d(v)$ parallel cross-copy edges for each original vertex. Euler-orient to indegree and outdegree $k$, lift to a $k$-regular bipartite multigraph, split into $k$ perfect matchings by the classical regular bipartite matching theorem, and pull back the corresponding two-factors. Allocate $\alpha/2$ factors red, $\beta/2$ blue and discard the artificial edges. This gives the required degree caps without appealing to any unsolved size-Ramsey claim.

The hypothesis of Theorem A is a sharp *joint lower bound*, not the full unrestricted joint-residual conjecture. The transfer theorem is unconditional as an implication.

## Theorem B: four infinite families of original size-Ramsey values

Each formula below is obtained by applying Theorem A to a *previously proved paper-level sharp joint-residual family* in \`research/erdos-561/joint-general/\`. The original formula is exact for **all arbitrary finite simple graph hosts**, subject to mathematical review of the cited paper proofs, not merely for star hosts.

### Family B1 — nonuniform three-versus-t spikes with arbitrary t

Let $t\ge4$, let $a,b\ge3$ be odd, and let $1\le c\le a$ and $b\ge a+c-1$. Set

$$
n=(a,1,1),\qquad m=(b,c,1^{t-2}).
$$

The unrestricted-host iterative-peeling theorem gives the sharp joint-residual value

$$
J=2b+(t-3)a+2.
$$

Adding the leading weight $w_2=a+b-1$ yields the **original** exact equality

$$
\boxed{\widehat r(F(a,1,1),F(b,c,1^{t-2}))=3b+(t-2)a+1.}
$$

For example, $(a,b,c,t)=(3,5,3,4)$ yields 22 edges. The two target forests are generally nonisomorphic and nonuniform; $t$ is unrestricted above four.

### Family B2 — equal-leading spikes with arbitrary component counts

Let $s,t\ge3$ and $a\ge3$ odd, with

$$
n=(a,1^{s-1}),\qquad m=(a,1^{t-1}).
$$

The previously proved sharp joint residual bound is

$$
J=(\max(s,t)-1)a+\min(s,t)-1.
$$

The resulting **original** value is

$$
\boxed{\widehat r(F(a,1^{s-1}),F(a,1^{t-1}))
=(\max(s,t)+1)a+\min(s,t)-2.}
$$

This applies for all component counts, not only three-by-three cases.

### Family B3 — a red two-edge secondary star

For every odd $a\ge5$, let

$$
n=(a,2,1),\qquad m=(a,1,1,1).
$$

The independently proved paper theorem in \`JOINT_RESIDUAL_ITERATED_PEELING_THEOREM.md\` and \`RIGID_15EDGE_THEOREM.md\` gives $J=3a+4$. Thus

$$
\boxed{\widehat r(F(a,2,1),F(a,1,1,1))=5a+3.}
$$

### Family B4 — sharp unequal residual profiles

Let $a,b\ge3$ be odd, $b\ge2a-2$, and set

$$
n=(a,1,1),\qquad m=(b,a-1,2,1).
$$

The unrestricted-host profile-mismatch theorem in \`JOINT_PROFILE_MISMATCH_THEOREM.md\` proves the sharp joint value $J=2b+a+3$. Since $w_2=a+b-1$, the original exact equality is

$$
\boxed{\widehat r(F(a,1,1),F(b,a-1,2,1))=3b+2a+2.}
$$

The source paper establishes the residual profile-mismatch result via two-centre rigidity; the present deduction does not claim to re-prove it independently.

## Bounded independent arithmetic verification

The script \`verify_even_cap_original_transfer.py\` uses two different antidiagonal index conventions and checks the residual tail identities and original displayed formulas over explicit bounded parameter grids, including all four families. It never assumes or numerically verifies universal Ramsey arrowing for arbitrary graphs. Theorem A is the analytic argument; the parent sharp residual results carry their existing source identities and review status.

## Unresolved boundary and review status

This proves the *general transfer implication* from a true sharp joint residual theorem to original Erdős #561 when both leading sizes are odd at least three. It **does not** establish the hypothesis for arbitrary $s,t$; therefore unrestricted Erdős #561 is OPEN. The four infinite formula corollaries depend on already admitted but still UNDER_REVIEW paper proofs of the corresponding unrestricted-host residual families. No new Lean kernel certificate, independent MATHCERT certification, or unrestricted novel priority claim is asserted. Source admission and specialist mathematical certification are separate.
