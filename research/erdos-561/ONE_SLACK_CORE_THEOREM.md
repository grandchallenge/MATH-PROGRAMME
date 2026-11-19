# ERDOS-561: one-unit-slack stability of the degree-core cap partition

Date: 2026-11-18. Claim class `PROVED_IN_PACKAGE`; programme status `UNDER_REVIEW`. This is a standalone ordinary mathematical proof, conditional on the earlier joint residual theorem only when making the size-Ramsey corollary. No assertion about the full Erdős #561 conjecture.

## Theorem (near equality classification)

Let `G` be a finite simple graph with maximum degree `D=α+β≥3`, `α,β≥1`, and at least `D+1` degree-`D` vertices. Suppose

`v_+(G)=2e(G)−D²`.

Then a red/blue edge partition satisfying `Δ(red)≤α` and `Δ(blue)≤β` exists **except exactly when** `D` is even, `α,β` are odd, and the degree-`D` vertices induce the complete graph `K_(D+1)`. In that exceptional case `G` consists, up to isolates, of `K_(D+1)⊔P₃⊔hK₂`, where `P₃` denotes a two-edge path and `h≥0`; the complete core prevents the capped partition by parity.

### 1. Degree-sum stability and residual geometry

Put `C={v:d(v)=D}`, `k=|C|≥D+1`. Since `2e−v_+=Σ_{d(v)>0}(d(v)−1)=D²`, we have

`D²≥(D−1)k≥(D−1)(D+1)=D²−1`.

For `D≥3`, adding one more degree-`D` vertex would increase the right side by at least `D−1≥2`, impossible. Consequently `k=D+1`, and the total remaining degree-excess equals exactly one. Thus precisely one noncore vertex `x` has degree 2; all other noncore nonisolated vertices have degree 1.

The core is `K_(D+1)` with a set `M` of missing edges. Each missing edge corresponds to one deficit stub at each of its endpoints, giving `2|M|` edges from the core to noncore vertices. These stubs terminate at ordinary leaves, except possibly zero, one or two of them can terminate at the exceptional vertex `x`. If zero, `x` is the middle of a disjoint `P₃`; if one, `x` is joined to a core vertex and a leaf; if two, `x` joins **distinct** core vertices. Any remaining outside edges are disjoint `K₂`.

### 2. M nonempty: constructive capped partition

The equality-core theorem `EVEN_CORE_CAP_PARTITION_THEOREM.md` constructs a core/pendant partition in which each core vertex has exact red degree α and blue degree β. We must only ensure that the two edges incident with `x` respect both caps.

**Zero core incidences at x.** Colour the two edges of its isolated `P₃` oppositely. Both caps are positive.

**One core incidence at x.** Keep the core-stub colour given by the equality-core construction; give the second, leaf edge the other colour. Vertex `x` has red degree 1 and blue degree 1.

**Two core incidences at x.** Label the endpoints `u,v` in the core, and choose missing edges `f` incident with `u` and `g` incident with `v` to be represented by the respective `x` stubs. Because the deficit stubs at one core vertex are interchangeable, any such choice is legitimate. If `uv` itself is missing, choose `f=g=uv` whenever useful.

If `α,β≥2`, the two edges at `x` automatically respect the caps irrespective of their colours. Only a cap equal to 1 needs attention.

If `D` is odd, use the one-factorization of `K_(D+1)` from the equality-core proof. A factorization has `D≥3` perfect matchings, and each of `f,g` belongs to precisely one matching; hence some matching contains **neither** edge. Choose that factor as the sole colour class of the cap-1 side, assigning every other factor to the side with cap `D−1≥2`. The two `x` stubs then both have the larger-cap colour, so `x` satisfies its caps. All core vertices retain exact red/blue degrees.

If `D` is even, then the only possibility with a cap 1 is an odd/odd pair of caps and `D≥4`. Take `f` as the distinguished missing edge in the equality-core Hamilton-cycle construction. Remove it from its Hamilton cycle, alternately colour the resulting *even-length* path red and blue, and use opposite colours on the two endpoint stubs. This alternating path can be coloured in either of its two orientations (equivalently, flip every path-edge colour together with its two endpoint-stub colours). If `f=g`, the two `x` edges are its two endpoint stubs, receiving opposite colours, and both caps are respected. Otherwise, the `f` stub at `x` flips when we switch the alternating colours. The `g` stub is either on the same Hamilton path and also flips, or is on another Hamilton cycle and is fixed. In the former case, the two `x` colours are either different under both orientations or equal under both; if equal, choose the orientation making them both the colour with cap at least 3. In the latter case choose the orientation making the `f` stub opposite to the `g` stub. Either way at most one `x` edge has the cap-1 colour. All other core degrees are unchanged by the path flip, and the pendant stubs can receive their required incident colours.

Thus the capped partition exists in every case `M≠∅`.

### 3. M empty: exact exception

If `M=∅`, no edge joins the complete core to the exterior. The noncore graph is exactly one `P₃` plus disjoint `K₂` components. The complete core can be capped-partitioned if `D` is odd (one-factorization) or both caps are even (Hamilton 2-factorization). Give the exterior `P₃` opposite colours on its edges and colour the `K₂`s arbitrarily. If `D` is even and both caps odd, the complete core has odd order and would require an odd-degree red regular spanning subgraph; the handshaking lemma forbids it. **QED.**

**Why `D≥3` is explicit.** For `D=2`, a single unit of slack can instead arise from **an extra maximum-degree vertex**: `K₃⊔P₃` satisfies `v_+=2e−D²` and its `(1,1)` cap partition fails. Thus the same decomposition statement cannot simply be asserted at `D=2`.

## Size-Ramsey corollary: one-slack parameter elimination

Consider two three-component star forests with largest star sizes `n₁,m₁≥2`. Assume the existing joint-residual theorem `J=W−(n₁+m₁−1)` (still under substantive review). Put `D=n₁+m₁−2`, `T=D(D+1)/2`, `E=W−1`, `B=2E−D²+1`, and `R=max(∑n_i+3,∑m_j+3)`.

If `D≥3`, `E>T`, and `B−R=1`, then the original size-Ramsey conjectured value **W is exact**.

**Proof.** As in Theorem C of `JOINT_3x3_AND_DEGREE_CORE_PROOF.md`, any hypothetical Ramsey host with fewer than W edges must have exactly E edges, maximum degree D, and a failed `(n₁−1,m₁−1)` capped partition. The degree-core theorem gives at least D+1 degree-D vertices and `v_+≤B`. Since G contains each target forest in some monochromatic full colouring, `v_+≥R=B−1`. Thus either `v_+=B` or `v_+=B−1`.

If `v_+=B`, the earlier equality-core theorem and its Ramsey corollary apply because `E>T`: the host admits a capped avoiding colouring unless its degree-D core is complete; in the latter case the core is `K_(D+1)` and the exterior is a nonempty matching, which is also defeated by a monochromatic-core avoiding colouring.

If `v_+=B−1`, the near-equality theorem above applies. If `M≠∅`, the capped partition itself avoids the target forests. If `M=∅`, the host is `K_(D+1)⊔P₃⊔hK₂` (plus isolates). Then `E=T+2+h`, so `R=B−1=D+4+2h`. Choose a target forest with R vertices and colour all core edges **and one P₃ edge** in that target's colour. Colour the other P₃ edge and every outside K₂ oppositely. The first-colour graph has at most `D+3<R` nonisolated vertices and hence cannot contain that target forest. The opposite-colour graph is a matching, so cannot contain the other target's largest star (at least two edges). This is an explicit avoiding colouring, a contradiction. The canonical W-edge upper host completes the proof. **QED.**

## Exact parameter and finite-check results

The independently implemented pure-Python verifier `verify_one_slack.py` checks every missing-core pattern and two-core-attachment pair for D=3 and D=4, together with bounded D=5 and D=6 patterns, using a direct exhaustive search for degree-cap feasibility **not employing** a Hamilton decomposition. Result: **29,685 / 29,685** feasible near-equality configurations with at least one missing core edge. A separate exact integer loop reproduces the old 851 parameters, removes six odd-equality and ten even-equality cases, and then excludes **80 additional one-slack ordered pairs**, leaving **755** parameters not excluded by these specific gates. These are not 755 established open problems.

The new 80 are distributed by forced D: D=4 (1 case), D=5 (8), D=6 (27), D=7 (34), D=8 (10). Some examples: `(2,1,1)/(5,2,1)` predicted W=19; `(2,1,1)/(6,6,1)` W=27; `(2,1,1)/(6,5,4)` W=28. The full deterministic 80-pair list is in `one_slack_results.json`.

**Governance:** This is a single-origin mathematical proof with independent-algorithm finite corroboration, not a non-author peer review or kernel-certified theorem. The joint residual theorem is a prerequisite for the Ramsey corollary. Retain all new and inherited mathematical claims `UNDER_REVIEW`. Erdős #561 in unrestricted component counts remains OPEN.
