# The River and the Storm

**Source status:** Open Millennium Prize Problem · NS-CI-001 · No solution claimed.

> **GitHub equation reader; automatically generated from the original manuscript.**
> The [illustrated documentary](../navier_stokes.md) has the canonical layout, figures and reader controls.
> This is not independent mathematical or publication certification.

A note to the reader

## How to Read the River

A fluid is not a single travelling object. It is a velocity attached to every point of space, changing in time and constrained by pressure, viscosity, and incompressibility. The governing equation is classical. The historic question is whether smooth three-dimensional data can drive a solution beyond smooth existence in finite time; see the October 2026 update above for the newly announced breakdown construction.

This web edition is a derivative, source-normalized exposition. Its streamlines, vortices, and cascades are orientation devices rather than computational evidence. The whole-space and periodic formulations, solution classes, imported theorems, and claim labels govern the mathematics.

**Edition status:**

Open Millennium Prize Problem; parent-challenge documentary; no smoothness proof claim.

**Original Millennium question · announced result under evaluation**

For smooth divergence-free initial data in three dimensions, prove global smooth existence with the required decay or periodicity, or construct an admissible finite-time breakdown example in one of the official settings.

**Claim boundary**

Weak existence is not smooth existence. Partial regularity is not regularity. A numerical cascade is not a singularity certificate. The narrower NS-CI-001 critical-integrability campaign remains a bounded research lane, not a solution of the parent Clay problem.

> **Plate I.** Plate I A fluid has a velocity everywhere Pedagogical orientation only. The semantic manuscript, equations, and trust labels govern the mathematical claim. [Illustration](../../assets/documentaries/navier_stokes/field.svg). *Alt text:* A vector field flows through a channel while pressure and viscosity act across the moving fluid.

Chapter I

## The Language of a Fluid

The incompressible Navier–Stokes equation for velocity $u(x,t)$, pressure $p(x,t)$, viscosity $\nu>0$, and force $f$ is

$$
\partial_tu+(u\cdot\nabla)u=-\nabla p+\nu\Delta u+f,
\qquad \nabla\cdot u=0.
$$

Transport carries momentum with the flow. Pressure enforces the divergence-free constraint. Viscosity smooths gradients. The nonlinearity is quadratic and nonlocal once pressure is recovered from incompressibility.

**Definition**

A classical solution has enough differentiability for the equation to hold pointwise. A strong solution satisfies it in a function-space sense with enough regularity for uniqueness and continuation. A weak solution satisfies an integrated formulation and may possess much less regularity.

Taking divergence gives $-\Delta p=\partial_i\partial_j(u_i u_j)-\nabla\cdot f$, up to the normalization appropriate to the domain.

> **Plate II.** Plate II Energy guards; vorticity stretches Pedagogical orientation only. The energy identity and vorticity equation govern the claim. [Illustration](../../assets/documentaries/navier_stokes/vorticity.svg). *Alt text:* Energy cascades downward while a vortex tube lengthens and thins under three-dimensional stretching.

Chapter II

## Energy: The First Guardian

For smooth unforced flow,

$$
\frac12\Vert{}u(t)\Vert{}_{L^2}^2+\nu\int_0^t\Vert{}\nabla u(s)\Vert{}_{L^2}^2\,ds=\frac12\Vert{}u_0\Vert{}_{L^2}^2.
$$

Leray–Hopf weak solutions satisfy the corresponding inequality. Kinetic energy cannot spontaneously increase in the unforced problem, and viscosity controls the time-integrated $H^1$ seminorm.

**Established theorem**

Global Leray–Hopf weak solutions exist for finite-energy divergence-free data in three dimensions. In two dimensions, the analogous theory closes strongly enough to give global regularity under standard hypotheses.

**Energy guardrail**

A bounded $L^2$ norm and finite total dissipation do not imply a uniform bound on vorticity, $L^\infty$ velocity, or every scaling-critical quantity.

Chapter III

## The Three-Dimensional Difficulty

Let $\omega=\nabla\times u$. Then

$$
\partial_t\omega+(u\cdot\nabla)\omega=(\omega\cdot\nabla)u+\nu\Delta\omega+\nabla\times f.
$$

The term $(\omega\cdot\nabla)u$ is vortex stretching. It is absent in the scalar two-dimensional vorticity equation but active in three dimensions.

### Two dimensions

Vorticity behaves like an advected-diffused scalar.

No vortex-stretching term.

Global regularity closes.

↔

### Three dimensions

Vorticity is a vector.

Stretching can amplify magnitude.

Critical control remains open.

> **Plate III.** Plate III Weak existence is not smooth existence Pedagogical orientation only. Each theorem retains its exact solution class. [Illustration](../../assets/documentaries/navier_stokes/classes.svg). *Alt text:* Nested solution classes distinguish Leray–Hopf weak solutions, strong solutions, and globally smooth solutions.

Chapter IV

## Weak, Strong, and Smooth

A Leray–Hopf solution is global and finite-energy, but classical theory does not prove that every such solution is smooth or unique in three dimensions. A strong solution is unique while its controlling norm remains finite. Weak–strong uniqueness identifies the two while the strong solution exists.

**Imported established result**

Suitable weak solutions satisfy a local energy inequality. Caffarelli–Kohn–Nirenberg partial regularity bounds the parabolic Hausdorff dimension of the possible singular set; it does not prove that the set is empty.

**Solution-class guardrail**

Moving silently between weak, suitable, strong, mild, and classical solutions changes the claim. Modern nonuniqueness results in broader weak classes do not constitute smooth finite-time blowup.

> **Plate IV.** Plate IV The critical frontier Pedagogical orientation only. A continuation criterion identifies a sufficient condition, not its universal truth. [Illustration](../../assets/documentaries/navier_stokes/frontier.svg). *Alt text:* A scaling ladder and a singular-set diagram separate continuation criteria, partial regularity, and the unresolved endpoint.

Chapter V

## The Millennium Frontier

The natural scaling is $u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2t)$, $p_\lambda(x,t)=\lambda^2p(\lambda x,\lambda^2t)$. The Ladyzhenskaya–Prodi–Serrin family gives continuation if

$$
u\in L^q(0,T;L^p),\qquad \frac2q+\frac3p\le1,\quad p>3.
$$

**The unresolved universal estimate**

The Clay problem requires proving that admissible smooth data never leave the smooth class, or producing a valid breakdown example. A continuation criterion does not prove its sufficient condition always holds.

The active NS-CI-001 lane studies bounded obligations near $L^4_tL^6_x$ and related weighted dissipation estimates. Its partial results refine the proof map without changing the parent problem's open status.

The equation spends energy. The problem is whether it can concentrate structure faster than the accounting can see.

Technical appendix A

## Whole-Space and Periodic Formulations

The official problem separates whole-space and periodic alternatives. The projected equation is $\partial_tu-\nu\Delta u=-\mathbb P\nabla\cdot(u\otimes u)$. Equivalence among pointwise, projected, mild, and distributional forms requires the stated regularity and domain assumptions.

Technical appendix B

## Scaling and Critical Spaces

For mixed norms,

$$
\Vert{}u_\lambda\Vert{}_{L^q_tL^p_x}=\lambda^{1-3/p-2/q}\Vert{}u\Vert{}_{L^q_tL^p_x}
$$

Thus $2/q+3/p=1$ is the velocity-critical line. Energy-class information does not directly dominate it. Small-data critical theorems retain their smallness hypothesis.

Technical appendix C

## Continuation and Partial Regularity

Continuation criteria have the logical form: critical norm finite on $[0,T)$ implies extension beyond $T$. Partial regularity locates the possible defect set; it neither certifies nor eliminates every defect. Numerical resolution criteria are method-dependent and cannot replace the continuum quantifier.

Technical appendix D

## Claim-Level Trust Matrix

| Claim | Trust class | Qualification |
| --- | --- | --- |
| Smooth local well-posedness | established | standard strong/mild theory |
| Global Leray–Hopf weak existence | imported established | energy-class weak solutions |
| Global two-dimensional regularity | imported established | not a three-dimensional theorem |
| Serrin continuation criteria | imported established | conditional |
| CKN partial regularity | imported established | singular set may still be nonempty |
| Universal 3D smoothness or breakdown | open | exact Clay alternative |
| NS-CI-001 progress | bounded programme evidence | no parent-problem promotion |
| Numerical simulations | empirical | no continuum proof object |
| Illuminated plates | pedagogical | never authoritative PDE diagrams |

**Final claim boundary**

This web edition changes presentation, not theorem strength. It does not prove global regularity, construct blowup, establish uniqueness of all weak solutions, or promote a neighbouring model into the true equation.

Sources and programme crosswalk

## Governing literature and campaign record

[Clay Mathematics Institute: Navier–Stokes Equation](https://www.claymath.org/millennium/navier-stokes-equation/).

[Charles Fefferman, official problem description](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf).

[Jean Leray, weak-solution foundations](https://doi.org/10.1007/BF02547754).

[Caffarelli, Kohn, and Nirenberg, partial regularity](https://doi.org/10.1002/cpa.3160350604).

[Escauriaza, Seregin, and Šverák, endpoint regularity](https://doi.org/10.1070/RM2003v058n02ABEH000608).

Programme links: [Domain 02](../../domains/navier_stokes/) · [claim-authority record](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/DOMAIN_02_NAVIER_STOKES_CRITICAL_INTEGRABILITY_MASTER_PLAN.md) · [campaign artifacts](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/navier_stokes_critical_integrability) · [review records](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/reviews/navier_stokes)

## Edition record

This browser-native edition uses the immutable Poincaré reference contract and shared open-problem status vocabulary. Its native SVG plates are pedagogical derivatives; semantic HTML carries the searchable text and equations.

The committed pointer is a source record; the checksum-locked complete illustrated source bundle is the authoritative source artifact. MathJax 3.2.2 is a version-pinned network enhancement, and the source TeX remains present when it is unavailable.

**Web claim boundary:** Browser-native, source-normalized exposition of the three-dimensional incompressible Navier–Stokes existence-and-smoothness problem. Energy estimates, Leray–Hopf weak existence, two-dimensional regularity, small-data theory, continuation criteria, partial regularity, numerical simulations, and NS-CI-001 progress are not promoted to global smoothness or finite-time breakdown.

[Web-edition data](../navier_stokes.edition.json)[Reusable schema](../documentary_web.schema.json)[Source record](../sources/the_river_and_the_storm.tex)[Artifact manifest](../ARTIFACT_MANIFEST.json)

Rendered PDF

14,246,784 bytes ·

`1ece7069787eee27c225db773826b09c513f5b1b9d25972cd1a45fa46dfef34a`

·

`metadata_only`

Complete LaTeX source

55,720 bytes ·

`d6627a7965c974e3de0b99dc9e1ea4b179b20ae41df56e505ad2b76e5f58e594`

·

`metadata_only`

Authoritative complete illustrated source bundle

14,536,994 bytes ·

`847a5bb2f68da797ca90782c3ba480e47067f323c54c8eb0b91a171353dce895`

·

`metadata_only`
