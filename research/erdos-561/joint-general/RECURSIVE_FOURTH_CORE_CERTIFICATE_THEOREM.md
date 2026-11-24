# Erdős #561 — the omitted fourth ORIGINAL core-transfer condition in the recursive proof certificates

**2026-11-24. Status: source-composition paper claim UNDER_REVIEW; deterministic finite trace CHECKED after exact-head replay.** Host graphs are arbitrary finite simple graphs; all star forests are ordinary non-induced vertex-disjoint positive-star unions. **No unrestricted all-profile theorem, no MATHCERT, no historical novelty claim.**

## 1. Exact proof obligation and imported theorem

The protected, previously source-proved \`GENERAL_CORE_ORIGINAL_TRANSFER.md\`, Theorem A, gives **FOUR** sufficient ORIGINAL-Ramsey transfers after an individually proved sharp simultaneous JOINT residual lower bound. Previous machine-readable proof-tree modules \`verify_recursive_three_blue_certificates.py\` and \`verify_recursive_red_matching_certificates.py\` implemented only THREE. The previously unused fourth condition concerns the **support of both original forests**, not the maximum degree alone.

For sorted positive original RED \(n=(n_1,\dots,n_s)\) and BLUE \(m=(m_1,m_2,m_3)\), suppose both leading edge sizes are at least two and have **opposite parity**, and suppose the exact JOINT lower is already proved for this pair:

\[
e(Q)\ge J_{\mathrm{can}}(n,m)
\quad \text{for every simultaneous JOINT residual host }Q.
\]

Let

\[
D=n_1+m_1-2,\qquad
W=W_{\mathrm{can}}(n,m),\qquad
R=\max\Bigl(\sum_{i=1}^{s}n_i+s,\ \sum_{j=1}^{3}m_j+3\Bigr).
\]

The protected Theorem A's **fourth** sufficient condition is

\[
\boxed{2W<2D^2+R.}
\]

Under these exact hypotheses,

\[
\boxed{\widehat r(F(n),F(m))=W.}
\]

The two leading sizes must each be at least two; omitting this guard would apply a factor-theory premise outside its sourced domain. A parity guard and the **strict** inequality are essential and are checked explicitly in executable proof traces.

## 2. Why the fourth transfer is mathematically valid

Assume a counterexample ORIGINAL-arrowing host \(G\) with \(e(G)\le W-1\). Every vertex deletion \(G-v\) jointly arrows both original residual targets; the separately established JOINT theorem gives \(e(G-v)\ge J_{\mathrm{can}}=W-(D+1)\), so every vertex degree satisfies \(d_G(v)\le D\).

A red/blue edge decomposition with maximum red degree \(n_1-1\) and maximum blue degree \(m_1-1\) would avoid both full original star forests, impossible since \(G\) arrows them. Thus no such capped decomposition exists. With **opposite parity leading sizes**, one of the two caps is even and the other odd. The protected \`GENERAL_SATURATED_CORE_UNIQUENESS_THEOREM.md\` therefore forces at least \(k=2D+2\) vertices of degree exactly \(D\); otherwise a capped decomposition exists.

The graph contains each original forest under the all-red/all-blue colouring, so its number of vertices incident with edges is at least \(R\). Every nonisolated vertex outside the saturated set contributes at least one to the degree sum; consequently

\[
2e(G)\ge Dk+(R-k)\ge R+(D-1)(2D+2)=R+2D^2-2.
\]

But \(2e(G)\le2W-2\). The strict fourth condition \(2W<2D^2+R\) contradicts both inequalities. Hence the original canonical value is sharp.

This is **reuse of an already source-admitted all-host proof**, not a new postulated lemma and not an assumption of joint sharpness for arbitrary profiles.

## 3. Well-founded certificate composition, retaining the prior source

The new code \`verify_recursive_vertex_budget_certificates.py\` imports the two **unaltered** protected recursive proof engines. It first asks the existing engine for a JOINT or ORIGINAL trace. A new ORIGINAL certificate is permitted **only** if (i) the prior engine returned UNKNOWN for that ORIGINAL, (ii) this fourth transfer passes with all guards, and (iii) the enhanced engine has an actual recursive JOINT proof trace for **the same exact original profile**. It then retains the dependency tree and exact values \(W,D,R\), including a positive integer strict-inequality margin.

If a JOINT trace is still UNKNOWN, the enhanced engine can attempt to prove it through a **strictly shorter RED list** either by a source-proved exact first residual ORIGINAL or by the existing source-proved zero-deficit RED matching bridge. Both recursion paths reduce the number of RED components, so no cyclic inference or unproved premise is introduced.

Previously accepted certificates are preserved unchanged, and no original certificate for a long RED list may appear without an exact JOINT certificate. The procedure returns UNKNOWN when its sufficient rules do not apply; UNKNOWN is not a counterexample.

## 4. Exact declared finite coverage

The declared deterministic grid consists of every nonincreasing RED list of length \(s=3,\ldots,8\), with terminal RED arm one and preceding arm sizes \(1,\ldots,8\), and BLUE \((U,V,1)\) for \(2\le V\le U\le8\): **179,928** exact parameter cells. The existing source engine certifies JOINT for 165,677 and ORIGINAL for 131,052.

Adding only the source's fourth ORIGINAL transfer and allowing already-admitted RED matching/first-residual inference to reuse the new ORIGINAL traces yields:

| Category | Previous | After source fourth transfer | Additional |
| --- | ---: | ---: | ---: |
| Sharp JOINT proof traces | 165,677 | 165,741 | 64 |
| Sharp ORIGINAL proof traces | 131,052 | 132,393 | 1,341 |
| JOINT UNKNOWN | 14,251 | 14,187 | -64 |

The finite traces demonstrate how many bounded parameter profiles the **mathematical sufficient rule** reaches. They are not a finite graph-host census or proof of full Erdős #561. An illustrative new ORIGINAL profile is RED \((3,3,1,1,1)\), BLUE \((4,4,1)\): here \(W=31\), \(J=25\), \(D=5\), and \(R=14\); the older half-core and one-odd criteria do not apply, but

\[
2W=62<2D^2+R=64.
\]

Its JOINT lower was already source-certified, so the exact unrestricted-host ORIGINAL value is now proved to be \(31\). This example does not depend on extrapolating from test cases.

## 5. Remaining frontier

The 14,187 still UNKNOWN JOINT profiles in the declared integer grid need **new arbitrary-host graph-theoretic lower bounds**, further legitimate transfer rules, or an actual counterexample. Restoring the fourth ORIGINAL transfer does not prove the full JOINT conjecture; it makes existing mathematical knowledge operational and allows some additional recursive deductions. It also reveals a source-to-executor omission: an already admitted theorem was not represented in the automated proof-selection machinery. The correction avoids duplicate mathematical source work and reduces future wasted searches.

**Evidence/certification boundary:** the mathematical fourth transfer is previously protected source paper proof and remains UNDER_REVIEW, the new compositional trace paper claim is UNDER_REVIEW, bounded arithmetic and trace replay can be CHECKED, and the full Erdős #561 remains OPEN/PARTIAL. No MATHCERT is issued.
