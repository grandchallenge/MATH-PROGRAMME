# Erdős #561: source-corrected degree-core and vertex-budget original transfers

**2026-11-23. Mathematical proof status: UNDER_REVIEW.** Bounded deterministic certificate replay status remains separately CHECKED only when replayed at exact committed source head. This theorem concerns arbitrary finite simple graphs with ordinary non-induced, vertex-disjoint positive star-forest embeddings. It does not prove the unrestricted Erdős #561 conjecture, certify every canonical residual, or issue MATHCERT.

## 1. A source-precondition audit and a new elementary boundary lemma

Let $n$ and $m$ be nonincreasing positive RED and BLUE original star-size lists, with at least three components each. Let $W$ be their canonical ORIGINAL antidiagonal sum, $J$ their canonical simultaneous JOINT residual tail, and

$$
D=n_1+m_1-2,\qquad W=J+D+1.
$$

Assume the simultaneous JOINT lower bound is ALREADY established for the selected pair over all finite simple host graphs:

$$
Q\to(F(n_{2:}),F(m))\ \text{and}\
Q\to(F(n),F(m_{2:}))\quad\Longrightarrow\quad e(Q)\ge J.
$$

By colouring the incident edges at an arbitrary vertex one colour, every ORIGINAL Ramsey host $G$ obeys both residual relations in $G-t$. If $e(G)\le W-1$, then

$$
d_G(t)\le (W-1)-J=D
$$

for EVERY vertex $t$.

The source-locked \`GENERAL_CORE_ORIGINAL_TRANSFER.md\` states its degree-factor theorem under the explicit hypothesis **both leading star sizes are at least two**. Earlier executable proof traces did not uniformly enforce that hypothesis before attributing a certificate to its degree-core clauses. We repair this **source-precondition / provenance mismatch** by proving and using the following independent, stronger boundary rule.

**Lemma A (zero-cap monochromatic original transfer).** If $\min(n_1,m_1)=1$, and the exact simultaneous JOINT residual lower $J$ is source-proved, then the ORIGINAL unrestricted-host size Ramsey number equals $W$, without any numerical core inequality.

**Proof.** Suppose an original arrowing host has fewer than $W$ edges. The previously proved vertex-deletion bound gives maximum degree at most $D$.

If $n_1=1$, colour **every edge BLUE**. The RED graph has no edges, so it cannot contain the positive RED forest. The BLUE graph has maximum degree at most $D=m_1-1$, so it cannot contain the largest BLUE star of size $m_1$ and therefore cannot contain the full BLUE forest. Contradiction. If $m_1=1$, instead colour every edge RED and use $\Delta(G)\le D=n_1-1$. Both arguments also cover $n_1=m_1=1$ where $D=0$. The canonical disjoint-star original host supplies the $W$-edge upper bound. QED.

This lemma **justifies** exact ORIGINAL outcomes previously attributed to a degree-factor theorem whose formal hypotheses exclude the zero-cap case. A provenance fix is not a permission to assert new mathematical independence or to alter earlier source-lock hashes.

## 2. Previously proved opposite-parity core transfer, correctly guarded

Now assume

$$
n_1\ge2,\qquad m_1\ge2,
$$

and that the two leading sizes have OPPOSITE parity. Set

$$
R=\max\left(\sum_{i=1}^s n_i+s,\quad
\sum_{j=1}^t m_j+t\right).
$$

The existing source-locked \`GENERAL_CORE_ORIGINAL_TRANSFER.md\`, Theorem A(4), proves an additional sufficient ORIGINAL condition:

$$
\boxed{2W<2D^2+R.}
$$

For completeness, the essential graph count is as follows. If an original host $G$ with at most $W-1$ edges admitted an edge partition into degree caps $\alpha=n_1-1$ and $\beta=m_1-1$, it would admit a colouring avoiding BOTH forests. The source-proved Lovász factor / saturated-core uniqueness consequence says that, since the leading parities are opposite and at least one cap is even, **failure** of such a partition with $\Delta(G)\le D$ forces at least $k\ge2D+2$ vertices of degree exactly $D$. Both all-RED and all-BLUE original arrowings force at least $R$ nonisolated vertices. Thus

$$
2e(G)\ge Dk+(R-k)=R+(D-1)k
\ge R+2D^2-2.
$$

But $e(G)\le W-1$ gives $2e(G)\le2W-2$, impossible if $2W<2D^2+R$. This is a theorem IMPORT with its explicit assumptions, not a new replacement proof for the Lovász factor classification.

## 3. Sound extension of the recursive sufficient-certificate procedure

The previous protected proof-tree procedure in \`RECURSIVE_THREE_BLUE_CERTIFICATE_THEOREM.md\` and the complementary RED-matching enhancement in \`RECURSIVE_RED_MATCHING_CERTIFICATE_THEOREM.md\` provide exact JOINT certificates for arbitrary sorted RED length $s\ge3$ against THREE positive sorted BLUE stars.

Keep all their previously admitted rules and add these two guarded ORIGINAL-transfer branches:

1. **ZERO_CAP_MONOCHROME** when $\min(n_1,m_1)=1$ and the same selected pair has an actual source-backed sharp JOINT certificate. This branch is independent of factor-theory preconditions.
2. **OPPOSITE_PARITY_VERTEX_BUDGET** when $n_1,m_1\ge2$, the leading values have opposite parity, the sharp JOINT certificate exists, and $2W<2D^2+R$.

For $n_1,m_1\ge2$ also retain the earlier source-proved cap transfer rules (both leading odd, the universal half-core bound, and the one-odd full-core bound). Each ORIGINAL certificate stores the precise guard and its sourced nested JOINT certificate. It can then feed the independently source-proved exact first-residual JOINT rule, and the new RED matching reduction may recursively invoke the improved shorter JOINT procedure. Every recursion strictly decreases RED list length, so the procedure terminates.

**Soundness:** all ORIGINAL rules are valid implications from an ACTUAL exact JOINT lower bound, not from the existence of a canonical star host. Every JOINT rule is itself backed by an admitted source theorem. Hence a returned certificate proves the canonical value for its indicated arbitrary-host pair, subject to substantive review of the source theorems. UNKNOWN remains UNKNOWN; it does not imply a counterexample.

### Example newly covered by the vertex-budget inequality

Take original RED

$$
n=(2,1,1,1,1)
$$

and BLUE

$$
m=(5,4,1).
$$

The canonical leading cap is $D=5$. Its ORIGINAL antidiagonal total is $W=31$, and the larger required vertex support is $R=13$. The previously admitted one-odd core gate $W\le D(D+1)$ FAILS, since $31>30$. However

$$
2W=62<2D^2+R=63.
$$

The source-proved opposite-parity transfer therefore certifies the ORIGINAL canonical value as soon as its JOINT proof tree is source-backed. This concrete example has both leading star sizes at least two, so no zero-cap assumption is smuggled into the factor-theoretic argument.

## 4. Exact bounded classification, no extrapolation

On precisely the same declared 179,928-profile grid as previous claims 047–050, the RED-matching-enhanced classifier already admitted 165,677 sharp JOINT, 131,052 sharp ORIGINAL and 14,251 JOINT UNKNOWN.

After the explicitly guarded ZERO_CAP_MONOCHROME and OPPOSITE_PARITY_VERTEX_BUDGET rules, the deterministic finite proof-tree calculation yields:

| Source-backed sufficient exactness status | Previous | With both guarded transfers |
| --- | ---: | ---: |
| JOINT exact | 165,677 | **165,851** |
| ORIGINAL exact | 131,052 | **132,487** |
| JOINT UNKNOWN by these methods | 14,251 | **14,077** |

This supplies **174 additional sharp JOINT** and **1,435 additional sharp ORIGINAL** classifications within the bounded grid. The newly proved ORIGINAL values may propagate through the first-residual JOINT rule, explaining the additional 174 joint proofs. These counts must be reproduced by a fresh exact-source checker before final claim admission.

These are **complete arithmetic classification counts within the declared finite profile grid**, NOT enumeration of arbitrary host graphs or formal certification of every imported mathematical theorem. The resulting closed families remain subject to the imported source theorems' UNDER_REVIEW statuses.

## 5. Evidence and remaining obligations

The new standalone verifier \`verify_recursive_vertex_budget_certificates.py\` imports previous protected certificate code WITHOUT modifying its historical files. It uses explicit, non-monkeypatched zero-cap and opposite-parity source guards, recomputes the enhanced nested proof tree, and checks all old certificates are preserved profile by profile. A reproducible classification SHA-256 fingerprint binds each result to the exact profile and theorem branch. It tests both canonical indexing conventions and explicit algebraic guard examples.

The remaining 14,077 JOINT UNKNOWN profiles represent a *precise insufficiency* of the combined existing criteria, not violations of the Erdős conjecture. Positive matching deficits, missing finite-graph structural bounds, and original-transfer gaps remain mathematically substantive. Full #561 remains OPEN/PARTIAL; no MATHCERT is issued.
