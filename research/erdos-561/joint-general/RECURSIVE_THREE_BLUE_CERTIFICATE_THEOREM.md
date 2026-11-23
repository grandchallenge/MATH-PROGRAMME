# Erdős #561 — a recursive proof-carrying decision procedure for three BLUE stars

**2026-11-23. Mathematical state:** a valid logical consequence of the listed source-proved paper theorems, UNDER_REVIEW; finite checker evidence CHECKED at exact-head replay. The procedure is not a universal solver and is not Lean-certified or MATHCERT certified. The full all-profile size-Ramsey conjecture remains OPEN/PARTIAL.

**New result:** A deterministic, well-founded, proof-carrying certificate combines all three previously proved mechanisms and certifies **162,839** of the 179,928 profiles in one fully specified bounded grid, versus **134,447** from the one-BLUE-matching criterion alone. It also certifies the exact ORIGINAL formula for 129,885 profiles. Every certified profile receives a *named theorem dependency*, not merely a numerical match. The logical theorem applies to arbitrary star sizes and arbitrarily long RED lists; only the count is bounded.

## 1. Canonical values and individually exact residual imports

Let $n=(n_1,\ldots,n_s)$ be a nonincreasing list of positive RED star sizes, with $s\ge3$, and let $m=(u,v,g)$ be three positive BLUE star sizes. Let the canonical antidiagonal weights be $w_k=\max_{i+j=k}(n_i+m_j-1)$ for $2\le k\le s+3$; set

$$
W(n,m)=\sum_{k=2}^{s+3}w_k,\qquad
J(n,m)=\sum_{k=3}^{s+3}w_k.
$$

The canonical disjoint-star host supplies these values as UPPER bounds for the ORIGINAL and simultaneous JOINT problems, respectively. The two individually required original residual values are

$$
S_1=W(n_{2:},m),\qquad
S_2=W(n,m_{2:}).
$$

The pinned two-component theorem (Chunlin You, arXiv:2610.25958v1) proves the original second residual has EXACT edge-minimum $S_2$ **for every number of RED stars**. The source-reconstructed three-by-three ORIGINAL theorem proves EXACT $W$ for every positive three-RED/three-BLUE profile. For two RED components and any BLUE length, use the same pinned two-component theorem with colours exchanged.

## 2. Two mutually recursive, well-founded proof judgments

Write $J^\sharp(n,m)$ when we can PROVE the arbitrary-host simultaneous JOINT residual minimum equals the canonical value $J(n,m)$, and $O^\sharp(n,m)$ when we can PROVE the ORIGINAL arbitrary-host size Ramsey minimum equals $W(n,m)$.

**JOINT rule, base:** If the RED list length is at most THREE, $J^\sharp$ is furnished by the source-proved complete three-by-three theorem (length exactly three) or the two-component residual bridge (length two).

For longer RED lists, certify $J^\sharp(n,m)$ when **any ONE** of the following sufficient routes succeeds:

**(B) One BLUE matching.** Normalize RED by $a_i=n_i-n_s+1$ and BLUE by $(U,V,1)=(u-g+1,v-g+1,1)$. The source-proved ALL-s single-BLUE-matching theorem gives $J^\sharp$ if $V\ge2$, normalized RED support $\sum_i(a_i+1)\ge3s-1$, and its explicit nonnegative interference penalty $P_{\mathrm B}(a,(U,V,1))=0$.

**(R2) Individually exact second residual.** If $S_2=J(n,m)$, the *exact* pinned two-BLUE-component ORIGINAL theorem establishes the lower bound $e(Q)\ge S_2=J$. No hypothesis on the BLUE matching penalty or RED support is necessary.

**(R1) Recursively exact first residual.** If $O^\sharp(n_{2:},m)$ has already been certified and $S_1=J(n,m)$, any JOINT host $Q$ arrows that FIRST original residual; therefore $e(Q)\ge S_1=J$. This invokes the exact original theorem ONLY for a **strictly shorter** RED list.

**ORIGINAL rule, base:** If RED length is two or three, use the pinned complete two-component or full three-by-three ORIGINAL theorem, respectively.

For longer RED lists, first certify $J^\sharp(n,m)$, then apply **one of the source-proved original degree-capped transfer conditions**. Write $D=n_1+u-2$; certify $O^\sharp$ if:

$$
\begin{aligned}
&\text{(i)} &&n_1,u\text{ both odd, without an edge-budget restriction};\\
&\text{(ii)} &&W(n,m)\le D(D+1)/2,\text{ any parity};\\
&\text{(iii)} &&\text{at least one of }n_1,u\text{ odd and }W(n,m)\le D(D+1).
\end{aligned}
$$

These are source-proved in \`GENERAL_CORE_ORIGINAL_TRANSFER.md\`. We do not infer any other original-lower theorem from a canonical construction alone.

**Termination and soundness.** The only recursive reference from $J^\sharp$ is to $O^\sharp$ on the shorter RED tail $n_{2:}$. The latter refers to $J^\sharp$ only on its own strictly smaller RED list. Thus the recursion is strictly decreasing in RED length and terminates. Each leaf uses a named sourced unrestricted-host theorem, and each internal node is a lower-bound implication, so every returned certificate justifies sharpness of its corresponding canonical upper. The procedure intentionally returns UNKNOWN when none of its sufficient routes applies. UNKNOWN is **not a counterexample**.

## 3. Finite declared completeness of the proof-tree audit

Run the deterministic standalone verifier \`verify_recursive_three_blue_certificates.py --grid\`. Its exhaustive bounded grid is:

- RED component length $s=3,\ldots,8$, nonincreasing positive first $s-1$ RED sizes in $1,\ldots,8$ and final RED size one;
- BLUE list $(U,V,1)$ with $2\le V\le U\le8$.

Exactly **179,928** profiles are enumerated. Under a fixed, documented proof priority (complete three-by-three base; one BLUE matching; exact second residual; recursive first residual), independent integer computations produce:

| JOINT proof status | Number |
| --- | ---: |
| Complete three-by-three base | 1,008 |
| Direct single-BLUE zero-deficit theorem | 133,949 |
| Individually exact TWO-BLUE second residual | 13,924 |
| Recursively sharp first residual, via ORIGINAL transfer | 13,958 |
| Still UNKNOWN by these methods | 17,089 |
| **Total exact JOINT certificates** | **162,839** |

The original decision procedure independently proves EXACT ORIGINAL values in **129,885** cells. The grid has **17,089 unresolved JOINT cells by THESE methods**, but this says nothing about whether their canonical formula is true or false. It is NOT a graph census.

The checker returns an inspectable JSON proof dependency tree for any supplied sorted RED list and THREE-BLUE list (e.g. \`--red 2,2,1,1,1 --blue 8,2,1\`). The grid run prints all counts and an SHA-256 classification fingerprint, deterministically bound to profile and rule. Every proof step is audited through the executable conditions and the source contracts; source theorems are not dynamically re-proved by the script.

## 4. Mathematical novelty and remaining obligations

This is a **compositional exactness theorem and proof-carrying algorithm**, not a new universal all-profile Ramsey formula. Its practical advance is to turn disparate source-proved all-host lower bounds into a terminating sufficient-certificate procedure with clear provenance and no false promotion of canonical upper bounds to actual minima.

Further work must prove or refute the residual profiles where every existing sufficient route fails. In particular, the restricted grid's remaining 17,089 cases include positive BLUE interference, unavailable first-residual transfer conditions, and small-support exceptions. Their correct disposition is **OPEN**, not an implied violation of the conjecture. The component-count recursion here is on source-proved ORIGINAL LOWER CERTIFICATES, never on an unproved all-profile induction hypothesis.

**Governance:** claim for this source remains paper-level UNDER_REVIEW until substantive mathematical adjudication; finite integer implementation CHECKED after exact-head hash and replay. Neither protected GitHub admission nor the classification fingerprint implies external mathematical certification or MATHCERT.
