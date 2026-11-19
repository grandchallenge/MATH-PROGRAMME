# ERDOS-561 / PR #3523 — role-separated adversarial review and odd-core refinement

Date: 2026-11-18. Repository: `grandchallenge/MATH-PROGRAMME`. Original PR material SHA `9ae38666e8bab01182f19b8bc9bd8d6255071521`.

**Disposition:** Ordinary paper-level review: *conditional pass with specific exposition repair and a new proved refinement*. This is a separate logical review pass by the same ChatGPT assistant, **not** a new independent expert or kernel-certified proof. Retain claim ledger status `UNDER_REVIEW`, draft PR, and the unrestricted Erdős #561 conjecture as `OPEN`.

## Reviewed dependencies

1. Lovász's `(g,f)` factor theorem, with `f(v)=α`, `g(v)=max(0,d(v)-β)`, `D=α+β`, and `Δ(G)≤D`. The equality set `g=f` is exactly the degree-`D` vertices; the parity-sensitive component obstruction is correctly specialized. The boundary estimate `Dc−c(c−1)≥D` for `1≤c≤D` is correct, so the degree-`D` induced subgraph must have a component of at least `D+1` vertices if the partition fails.
2. You's arXiv:2610.25958v1 two-component result explicitly covers positive integers including one-edge stars. Its role in zero-switching is within the stated hypotheses. No claim that the preprint is a formally verified library lemma.
3. The three-star positive-switch proof uses one residual relation to force a two-single-star arrowing and the *other* residual relation to obtain the one-star-versus-forest lower bound after vertex deletion. The original manuscript said 'that residual condition', which is ambiguous and in one orientation inaccurate. This is an exposition defect, not a missing hypothesis: both residual relations are part of `J`'s definition. Corrected dependency mapping:
   - If `x>u` and `v>y`, take the **blue-deleted** residual `Q→(F(a,b,c),F(q,r))` for the `(K_{1,a},K_{1,q})` cap obstruction and hence `Δ(Q)≥a+q−2`. Separately take the **red-deleted** residual `Q→(F(b,c),F(p,q,r))`; colouring all edges at the removed vertex red gives `Q−z→(K_{1,c},F(p,q,r))`.
   - In the transposed case `u>x` and `y>v`, take the **red-deleted** residual for `(K_{1,b},K_{1,p})` and the **blue-deleted** residual for `Q−z→(F(a,b,c),K_{1,r})`.
4. `verify_joint3_small.py`/`verify_joint3_finite.py` replay all 7,056 ordered non-increasing triple pairs with sizes `1..7`; exactly 82 positive-switch cases have forced `d≤7`; 74 fail the edge requirement and the remaining 8 fail the vertex requirement. This is an exact arithmetic certificate, not a graph-level numerical extrapolation. `verify_core_and_switching.py` checks 4,115 finite graph/cap instances including 32 authentic failures.
5. The original large-leading-degree theorem `n_1+m_1≥12` follows from the joint-residual theorem and the core edge budget. It is conditional on the external two-component theorem and the Lovász specialization; it remains an internal proof candidate, not a protected mathematical certification.

## New theorem: odd maximum-degree extremal parity

Let `G` be finite and simple with odd maximum degree `D≥3`. Assume `G` has at least `D+1` degree-`D` vertices and exactly

`v_+(G)=2e(G)−D²+1`

nonisolated vertices. Then **`χ′(G)=D`**.

### Proof

Let `k` be the number of degree-`D` vertices. The degree-sum inequality

`2e(G)≥Dk+(v_+(G)−k)=v_+(G)+(D−1)k`

and equality in the stipulated upper bound show `k=D+1`; all other nonisolated vertices have degree `1`. Let `C` be the `D+1` degree-`D` vertices. Because `D` is odd, the complete graph on `C` has even order and admits a proper `D`-edge-colouring (explicit round-robin 1-factorization).

Keep these colours on the existing internal edges of `G[C]`. At each `u∈C`, its missing `K_{D+1}`-edges have pairwise distinct colours. Their number is `D−d_{G[C]}(u)`, precisely the number of edges from `u` to vertices outside `C`. Assign those distinct missing colours, in any order, to the external edges incident to `u`. All noncore endpoints have degree one, so no new edge conflict appears there. Isolated `K_2` components on noncore vertices may be assigned any colour. This is a proper `D`-edge-colouring of `G` and proves the claim. **QED.**

**Corollary for degree-capped partitions.** For any positive `α,β` with `α+β=D`, the colour classes can be grouped into `α` red and `β` blue matchings. Thus no graph in this extremal odd-`D` equality case can be an `(α,β)` degree-partition obstruction.

**Corollary for the original Erdős three-star formula.** Given the now-reviewed joint residual result, a hypothetical `W−1`-edge counterexample has `Δ=D=n_1+m_1−2` and fails the `(n_1−1,m_1−1)` cap partition (when the leading sizes are at least two). If `D` is odd and the required forest order `max(∑n_i+3,∑m_j+3)` equals `2(W−1)−D²+1`, the odd-core theorem contradicts the forced cap obstruction.

The old 851 ordered *not-yet-eliminated-by-these-gates* parameter instances reduce to **845**, excluding six additional ordered entries, corresponding to three pairs up to colour interchange:

| Red star sizes | Blue star sizes | W | D | forbidden host edges |
| --- | --- | ---: | ---: | ---: |
| `(4,1,1)` | `(5,5,5)` | 34 | 7 | 33 |
| `(2,2,1)` | `(7,7,5)` | 36 | 7 | 35 |
| `(2,2,1)` | `(7,6,6)` | 36 | 7 | 35 |

Thus the predicted size-Ramsey formula is established at **paper level** for these pairs, conditional on the existing complete 3×3 joint-residual proof. This is not a claim of publication priority or of the unrestricted conjecture.

## Additional simplification

Theorem C of PR #3523 unnecessarily required `σ=0` to conclude the original 3×3 formula when `W≤D(D+1)/2`. Its proof already invokes Theorem B for **all** `σ`. Remove the `σ=0` hypothesis: all 3×3 parameter pairs with leading sizes at least 2 and `W≤D(D+1)/2` are covered. In the bounded table with sizes ≤10, the scope increases from 43,066 to **46,120** ordered pairs (including 3,054 positive-switch pairs); 104 of the additional pairs have `D≤9` and are not subsumed by the large-leading-degree theorem.

## Exact verification

`verify_odd_core.py` independently enumerates 4,566 bounded low-degree three-star pairs with leading sizes ≥2, implements the existing edge/vertex/equality filtering without importing the old script, and identifies exactly six new exclusions (`851→845`). The same file implements a round-robin colouring of the odd-core equality class and checks explicit examples for `D=3,5,7`. Output: `odd_core_results.json`.

## Governance and remaining work

- Review is **same-model separate-pass**, not independently authenticated non-author scholarship. Do not create a misleading `APPROVED` review to imply otherwise.
- Pin and preserve the Lovász-factor exact statement, two-component arXiv revision, and bounded scripts.
- Update the draft manuscript's residual-direction sentence, Theorem C's unnecessary hypothesis, and the research shortlist with traceable provenance.
- Leave protected mathematical certification / external publication gated by source-semantic adjudication and appropriately independent validation.
- General s,t≥4 joint residual inequality and full Erdős #561 remain OPEN.