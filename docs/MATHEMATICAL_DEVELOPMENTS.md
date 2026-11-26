# Mathematical developments · November 2026

<p class="page-deck">An account of consequential mathematical results, the ideas connecting them, and the distinction between a released proof, a checked formal theorem and an independently understood argument.</p>

**Observation date:** 26 November 2026. This is a source-linked editorial synthesis, not independent certification of the releases.

## Riemann: from prime distribution to arithmetic constraints

On 20 November Levent Alpöge released a Lean proof of the Riemann Hypothesis. On 21 November the Lean FRO and Mathlib Initiative reported reproducible builds, two independent statement-comparison tools and multiple checkers accepting an inert proof export against the vetted Mathlib statement. Read the [joint statement](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/). [Clay](https://www.claymath.org/millennium-problems/) lists RH as Active; formal validation and prize disposition are separate.

The hypothesis asserts that nontrivial zeros of the zeta function lie on the critical line. It gives strong control of fluctuations in prime distribution. GCL's [arithmetic reconstruction](domains/rh_a26_audit_explained.md) examines local arithmetic data, character inequalities, tower estimates and the eventual analytic conclusion. The challenge now is to recover a readable proof spine with explicit hypotheses, not to mistake our incomplete reconstruction for a failure of the externally checked proof.

The September Navier–Stokes announcement is another landmark, involving forced-flow breakdown rather than universal unforced regularity. See the [Millennium status record](MILLENNIUM_PRIZE_STATUS.md).

## Tensor geometry: a possible new language of lower bounds

The [November 24 release](https://github.com/openai/math/blob/3344da59991ed94f9ba711217b29c1d760badfa6/history.md) groups seven papers under [Family 379](https://grandchallenge.ai/MATH-PROGRAMME/oai26/families/379/). Rather than treat them as unrelated headlines, begin with the tensor-price construction.

Imagine sites at the corners of a triangle with sides 3, 4 and 5. Three independent shared bits on the edges have total distance cost 12. A single bit shared by all three sites has normalized mean-width cost 6, half the perimeter. This illustrates the proposed price law: the cost of a relationship depends on its joint structure, not just the number of coordinates. The geometric theorem and its applicability to general computation are the difficult parts.

The manuscript proposes spectral invariants compatible with tensor composition and local transformations. Companion results compare the cost of a target tensor to that of a computational network. The matrix lower bound requires more than the triangle estimate; the source develops rigidity and compression arguments. The [family analysis](https://grandchallenge.ai/MATH-PROGRAMME/oai26/families/379/) explains the proof architecture.

| Manuscript claim | Why it matters | Verification boundary |
| --- | --- | --- |
| Tensor geometry and mean width | Candidate accounting principle for shared information | Publisher formal scope imposes finite-dimensional chart and convexity conditions |
| Strict Valiant hierarchy (VF, VBP, VP, VNP) | Separates arithmetic resource classes | Selected inclusions and grid lower bound formalized by publisher; explicit rate separate |
| Hamiltonian cycle and permanent | Superpolynomial arithmetic circuit complexity; permanent excludes characteristic two | Publisher scope covers exact eventual superpolynomial bounds, not every stronger approximation statement |
| Matrix multiplication exponent 9/4 | Matching asymptotic upper and lower bounds | GCL hardened Comparator accepted square, dual and rectangular declarations; finite-size gate count not covered |
| Fourier transforms | Claimed binary linear-gate logarithmic exponent one-half | Selected single and batched transforms, not polynomial-multiplication lower bound |
| Integer multiplication | Claimed nearly linear time with square-root logarithmic factor on a fixed multitape machine | Matching lower exponent conditional on variable-count Weak ETH; division and square-root extensions separate |
| Sunflowers | Exponential threshold for fixed petal count | Fixed-base uniform-set version formalized, not quantitative base dependence |

**Evidence:** [GCL matrix Comparator run](https://github.com/grandchallenge/MATHFORGE/actions/runs/45584629927) accepted three named statements from the original pinned challenge. The other six manuscripts do not inherit that replay. No independent paper-wide certification is claimed.

### Why this matters for P versus NP

Arithmetic circuits compute polynomials by field operations; Boolean decision algorithms return bits. A transfer needs a theorem relating representation, computation model, uniformity and charged resource bounds. Without such a theorem, algebraic separation is not Boolean P versus NP.

For GCL's [PNP-ABOVE](pnp_above/index.md) and [Structural Capacity Calculus](https://github.com/grandchallenge/MATHSOLVE/issues/1309), the productive question is whether tensor prices control logical relations under the actual operations of a classical machine. Study the primitive laws, the induced quotient, reuse and cancellation, and exactly where the lower-bound comparison applies. Do not assume a general Boolean invariant.

## Optimization: finding a destination need not mean walking there

[Family 380](https://grandchallenge.ai/MATH-PROGRAMME/oai26/families/380/) pairs two apparently conflicting claims: a strongly polynomial algorithm for explicit linear programming and bounded simple rational polytopes whose graph diameters exceed every fixed polynomial in the number of facets.

There is no contradiction. An edge-walking algorithm moves between adjacent vertices. A certificate-based method derives an optimum directly from inequalities, potentially without following such a path. The first manuscript claims the latter kind of resource bound; the second limits geometric traversal. The rational RAM formalization is narrower than the arbitrary-real manuscript claim. Independent GCL replay is not established for either paper.

## October developments: exact counting and wave geometry

[Family 378](https://grandchallenge.ai/MATH-PROGRAMME/oai26/families/378/) claims deterministic exact counting for fixed-width CNF in subexponential variable-count time and polynomial space. A positive count decides SAT. This would refute ordinary ETH, not establish polynomial time or refute the weaker variable-count hypothesis used for integer multiplication. The selected Lean bound is weaker than the sharp manuscript bound; GCL has not independently replayed it.

[Family 079](https://grandchallenge.ai/MATH-PROGRAMME/oai26/families/079/) claims Euclidean wave local smoothing, with consequences for Kakeya, restriction and related estimates. A Kakeya set contains a unit segment in every direction; the dimensional question asks how much space such a set must occupy. The proof uses wave-packet geometry and an auxiliary PDE. The strict-loss and exponent assumptions must be read separately from the headlines. GCL has not independently replayed the new release.

## Research priorities suggested by the releases

These are analytical priorities, not new campaign authorizations.

1. Family 379: reconstruct tensor prices, rigidity and compression, then examine the Valiant and circuit lower-bound endpoints in their exact computational models.
2. Family 378: establish the counting model and time and space bounds; compare ordinary ETH with variable-count Weak ETH.
3. Family 380: check the rational RAM and Hirsch challenges separately, including charged control work and polytope realizability.
4. RH: continue independent mathematical reconstruction and expose the key arithmetic ideas while retaining the externally validated formal status.
5. Family 079: trace the critical annular estimate, packet geometry and consequences through their exact exponent ranges.

For the underlying source inventory, see the [OpenAI Mathematics 2026 compendium](oai26/index.md). For ongoing GCL work, see [Current Work](CURRENT_WORK.md). The release has not settled Boolean P versus NP by implication, nor has the existence of a formalization established every statement of every associated manuscript.
