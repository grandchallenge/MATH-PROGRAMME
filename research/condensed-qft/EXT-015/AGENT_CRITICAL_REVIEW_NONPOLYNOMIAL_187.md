# EXT-015 REACH / 187 — critical review of the anchored nonpolynomial Gaussian source

**Disposition: BOUNDED ACCEPT of unchanged primary186. No correction requested.** The explicit scalar and matched-partition width changes are actual original105/108 sources on their stated sectors. The undifferentiated cusp core and general mixed multiplier remain unresolved.

## 1. Source lock and review provenance

Reviewed [NONPOLYNOMIAL_GAUSSIAN_SOURCE_AUDIT_186.md](NONPOLYNOMIAL_GAUSSIAN_SOURCE_AUDIT_186.md), frozen commit `63fa56956547c5e82e225cf3bfe6dedb7c1d06ac`, reference `research/reach-nonpolynomial-primary-frozen-20261115`, Git blob `4c62aec3917223549ffee8cce58a560ff5d23065`. The local bytes reproduce that blob using the Git blob header and SHA1, without invoking Git. Commit/reference custody is supplied by the parent and the checkpoint; no remote readback was performed by this reviewer.

Read AGENTS, protocol090, actual105/108/126, joint-corner165 and183–185. The current checkpoint is **CP195**, succeeding the construction's CP194: it names precisely the frozen186 source and this187 review as the next action. That numbering change does not change the scientific input.

This is a distinct nonauthor logical review in the same Codex system, sharing the accepted source dependencies. It is not an external referee assessment, independent human certification, GitHub APPROVED review or protected admission. No producer recurrence state, numerical fixture or Python execution was used. Only this review file was written.

## 2. Verifier: exact maps, density and finite derivatives

For the identity partition on physical vertices $(x,z,h)$, the compact coefficient consisting of $\delta_0(h)$ and smooth spectator cutoffs has only an $h$ wavefront component. Every partition conormal requires zero covector sum separately on each block, which is impossible on the block containing that nonzero component. Thus this is an original R1 input, including at simultaneous collisions. Forgetting $h$ pulls back the fixed scalar stage by the105.4 heat map; compact cutoffs make the eventual projection proper.

Let $c^{-2}=a^{-2}+b^{-2}$. Directly from the normalized Gaussian,

$$
\sqrt{2\pi}b\epsilon\,\kappa_{a\epsilon}(s)\kappa_{b\epsilon}(s)
=\frac{1}{\sqrt{2\pi}a\epsilon}e^{-s^2/(2c^2\epsilon^2)}
=\frac ca\kappa_{c\epsilon}(s).
$$

Pairing $\delta_0(h)$ with ordinary $dh$ sets $h=0$ with coefficient one. This proves186.2 with exactly the claimed $c/a$ factor. The hidden cutoff equals one there. There is no extra projection determinant.

On the matched partition $\{x,h\}\mid\{z\}$, the block coefficient $\delta_0(t)\rho(z)$ has only a $t$ covector and avoids the two-block conormal $(\tau,-\tau)$. For a retained test $\psi$, inclusion followed by forgetting pairs the source as

$$
\int \rho(z)\sqrt{2\pi}b\epsilon\,
\kappa_{a\epsilon}(z)\kappa_{b\epsilon}(z)\psi(0,z)\,dz.
$$

This verifies186.3 using the specified block density, without inserting an inadmissible independent product of anchor deltas. Whole-output differentiation pairs against $(-1)^r\partial_x^r\psi(0,z)$ and therefore proves186.4 for every fixed finite $r$. When derivatives are commuted through the pre-pushforward source, all complement derivatives are necessary. A lone derivative of its delta factor would give the wrong expression. Fixed $z$ derivatives are legal too, but differentiate the multiplier and do not commute with multiplication by it.

## 3. Adversary: analytic source bounds and scope

The all-corner statement is justified by the actual finite source maps, rather than positive-scale smoothness alone. Fixed-width Gaussian edges are original scalar stages by105.4 and positive regulator rescaling. Scalar pullback, their product and the Laurent factor use105.6 with its fixed index sums and auxiliary remainder weights. For each requested seminorm these operations use finitely many input seminorms in a fixed output refinement. Tensoring the fixed permitted R1 coefficient and applying inclusion, finite derivatives and proper forgetting then use108.6–108.7. Their continuous finite bounds extend to the complete scalar input stage; no finite-separable approximation is being substituted for completed coefficients.

For126 this yields maps on **given source-controlled rows**: the geometric history, widths, supports and scalar stages stay fixed while finite Sobolev orders may relax. Every requested mixed parameter/regulator jet follows the finite chain and Leibniz rules. The admitted108.1 estimates preserve the uniform rapid relation on these typed domains. This establishes neither coefficient lifts for arbitrary output families nor a quotient-wide operation of multiplying an arbitrary mixed family by the anchored exponential. Full126.14 remains unresolved.

The proposed independent-anchor extension really fails: at the joint anchor, $\delta_0(x)\rho(z)\delta_0(h)$ has covectors $(\tau,0,-\tau)$, forbidden for $\{x,h\}\mid\{z\}$. The compact cusp has nonzero one-coordinate wavefront at zero as well, so $f(x)\delta_0(h)$ has the same forbidden directions. These are counterexamples to that coefficient construction, not nonmembership invariants for all histories.

Matching $x=h=t$ with a cusp coefficient instead evaluates to a Gaussian centered at $x$. On points with $f(x)\ne0$ and $x\ne0$, the functions $\kappa_{a\epsilon}(z-x)$ and $\kappa_{a\epsilon}(z)$ differ. The delta case permits replacing their centers only before whole differentiation, because its coefficient is supported at zero. No analogous cusp substitution or source antiderivative follows.

## 4. Critical-inference decisions

| Inference | Verdict and reason |
| --- | --- |
| Anchored scalar two-Gaussian history186.2 | **JUSTIFIED**: permitted R1 cone, actual heat pullback/edge maps, proper projection and exact normalized pairing. |
| Matched-partition source186.3 | **JUSTIFIED**: permitted block coefficient; typed inclusion and forgetting have unit pairing density. |
| Every fixed finite anchored $x$ jet186.4 | **JUSTIFIED** by whole-source differentiation with all complement terms. |
| Full fixed-stage corner, completed coefficient and source-controlled126 estimates | **JUSTIFIED** by the specified finite105/108 maps and row witnesses, within their existing hypotheses. |
| Uniform rapid preservation on these typed operations | **JUSTIFIED** by108.1; no arbitrary mixed anchored-multiplier operator inferred. |
| Independent anchor works for every original R1 input | **INCORRECT**, as the explicit delta and cusp tensor cones show; primary186 correctly rejects it. |
| Matched cusp construction equals the anchored cusp core | **INCORRECT** because of the center shift; primary186 correctly rejects it. |
| Some other legal finite completed history constructs the first cusp core | **UNRESOLVED**: this review supplies neither that history nor an all-history obstruction. |
| General mixed multiplication, universal150.L, residual W acyclicity, original R3, full126.14 or full integration | **UNRESOLVED**, with no new inference from the bounded constructions. |

Accept186 without correction for its explicit sector constructions and negative method controls. Ledger188 must retain these exact boundaries. Editorial checks, protected admission, exact readback and tracker reconciliation remain separate obligations.
