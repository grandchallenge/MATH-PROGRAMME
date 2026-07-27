<link rel="stylesheet" href="../../stylesheets/documentary.css">
<link rel="stylesheet" href="../../stylesheets/documentary-status.css">

<div class="gcl-monograph" data-gcl-reader="navier_stokes" data-edition="1.1.0">
<a class="monograph-skip" href="#monograph-start">Skip to the manuscript</a>
<header class="monograph-hero" aria-labelledby="monograph-title">
  <div class="monograph-hero__art" aria-hidden="true"><img src="../../assets/documentaries/navier_stokes/cover.svg" width="1024" height="1536" alt=""></div><div class="monograph-hero__veil"></div>
  <div class="monograph-hero__copy"><p class="monograph-eyebrow">MATH-PROGRAMME · Documentary Treatment · NS-CI-001</p><h1 id="monograph-title">The River and the Storm</h1><p class="monograph-hero__subtitle">A guided journey through fluid motion and the three-dimensional smoothness problem</p><p class="monograph-hero__thesis">Viscosity dissipates energy, but three-dimensional vortex stretching can drive structure toward scales where the known estimates no longer close.</p><div class="monograph-status" aria-label="Publication status"><span>Open Millennium Prize Problem</span><span>NS-CI-001</span><span>No solution claimed</span></div><div class="monograph-actions"><a class="monograph-button monograph-button--primary" href="#monograph-start">Begin the journey</a><a class="monograph-button" href="../">Documentary library</a><a class="monograph-button" href="../sources/the_river_and_the_storm.tex">Source record</a></div></div>
</header>
<div class="monograph-progress" aria-hidden="true"><span data-reader-progress-bar></span></div>
<div class="monograph-reader" id="monograph-start" tabindex="-1"><nav class="monograph-toolbar" aria-label="Reader controls"><div class="monograph-toolbar__identity"><span>Digital Grand Challenge Library</span><strong>The River and the Storm</strong></div><div class="monograph-toolbar__controls"><button type="button" data-reader-focus aria-pressed="false">Focus mode</button><button type="button" data-reader-print>Print / save</button><button type="button" data-reader-reset>Reset position</button><output data-reader-progress aria-live="polite">0% read</output></div></nav>
<div class="monograph-layout"><aside class="monograph-contents" aria-label="Manuscript contents"><p class="monograph-contents__title">The journey</p><ol><li><a href="#reader-note">How to Read the River</a></li><li><a href="#field-equation">The Language of a Fluid</a></li><li><a href="#energy">Energy: The First Guardian</a></li><li><a href="#vorticity">The Three-Dimensional Difficulty</a></li><li><a href="#solution-classes">Weak, Strong, and Smooth</a></li><li><a href="#millennium-frontier">The Millennium Frontier</a></li></ol><p class="monograph-contents__title">Technical appendix</p><ol><li><a href="#appendix-formulations">Whole-Space and Periodic Formulations</a></li><li><a href="#appendix-scaling">Scaling and Critical Spaces</a></li><li><a href="#appendix-regularity">Continuation and Partial Regularity</a></li><li><a href="#appendix-trust">Claim-Level Trust Matrix</a></li><li><a href="#sources">Sources</a></li></ol></aside>
<article class="monograph-body" aria-label="The River and the Storm manuscript">
<section class="monograph-section" id="reader-note" data-reader-section markdown="1"><p class="monograph-section__eyebrow">A note to the reader</p>
## How to Read the River
A fluid is not a single travelling object. It is a velocity attached to every point of space, changing in time and constrained by pressure, viscosity, and incompressibility. The governing equation is classical. The unresolved question is whether smooth three-dimensional data can ever drive the solution beyond smooth existence in finite time.

This web edition is a derivative, source-normalized exposition. Its streamlines, vortices, and cascades are orientation devices rather than computational evidence. The whole-space and periodic formulations, solution classes, imported theorems, and claim labels govern the mathematics.

**Edition status:** Open Millennium Prize Problem; parent-challenge documentary; no smoothness proof claim.
<div class="conjecture-box"><strong>Open problem</strong><p>For smooth divergence-free initial data in three dimensions, prove global smooth existence with the required decay or periodicity, or construct an admissible finite-time breakdown example in one of the official settings.</p></div>
<div class="warning-box"><strong>Claim boundary</strong><p>Weak existence is not smooth existence. Partial regularity is not regularity. A numerical cascade is not a singularity certificate. The narrower NS-CI-001 critical-integrability campaign remains a bounded research lane, not a solution of the parent Clay problem.</p></div></section>
<figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate I"><img src="../../assets/documentaries/navier_stokes/field.svg" width="1024" height="1536" loading="lazy" alt="A vector field flows through a channel while pressure and viscosity act across the moving fluid."></button><figcaption><span class="plate-label">Plate I</span><strong>A fluid has a velocity everywhere</strong><small>Pedagogical orientation only. The semantic manuscript, equations, and trust labels govern the mathematical claim.</small></figcaption></figure>
<section class="monograph-section" id="field-equation" data-reader-section markdown="1"><p class="monograph-section__eyebrow">Chapter I</p>
## The Language of a Fluid
The incompressible Navier–Stokes equation for velocity \(u(x,t)\), pressure \(p(x,t)\), viscosity \(\nu>0\), and force \(f\) is

\[
\partial_tu+(u\cdot\nabla)u=-\nabla p+\nu\Delta u+f,
\qquad \nabla\cdot u=0.
\]

Transport carries momentum with the flow. Pressure enforces the divergence-free constraint. Viscosity smooths gradients. The nonlinearity is quadratic and nonlocal once pressure is recovered from incompressibility.
<div class="definition-box"><strong>Definition</strong><p>A classical solution has enough differentiability for the equation to hold pointwise. A strong solution satisfies it in a function-space sense with enough regularity for uniqueness and continuation. A weak solution satisfies an integrated formulation and may possess much less regularity.</p></div>
Taking divergence gives \(-\Delta p=\partial_i\partial_j(u_i u_j)-\nabla\cdot f\), up to the normalization appropriate to the domain.</section>
<figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate II"><img src="../../assets/documentaries/navier_stokes/vorticity.svg" width="1024" height="1536" loading="lazy" alt="Energy cascades downward while a vortex tube lengthens and thins under three-dimensional stretching."></button><figcaption><span class="plate-label">Plate II</span><strong>Energy guards; vorticity stretches</strong><small>Pedagogical orientation only. The energy identity and vorticity equation govern the claim.</small></figcaption></figure>
<section class="monograph-section" id="energy" data-reader-section markdown="1"><p class="monograph-section__eyebrow">Chapter II</p>
## Energy: The First Guardian
For smooth unforced flow,
\[
\frac12\|u(t)\|_{L^2}^2+\nu\int_0^t\|\nabla u(s)\|_{L^2}^2\,ds=\frac12\|u_0\|_{L^2}^2.
\]
Leray–Hopf weak solutions satisfy the corresponding inequality. Kinetic energy cannot spontaneously increase in the unforced problem, and viscosity controls the time-integrated \(H^1\) seminorm.
<div class="theorem-box"><strong>Established theorem</strong><p>Global Leray–Hopf weak solutions exist for finite-energy divergence-free data in three dimensions. In two dimensions, the analogous theory closes strongly enough to give global regularity under standard hypotheses.</p></div>
<div class="warning-box"><strong>Energy guardrail</strong><p>A bounded \(L^2\) norm and finite total dissipation do not imply a uniform bound on vorticity, \(L^\infty\) velocity, or every scaling-critical quantity.</p></div></section>
<section class="monograph-section" id="vorticity" data-reader-section markdown="1"><p class="monograph-section__eyebrow">Chapter III</p>
## The Three-Dimensional Difficulty
Let \(\omega=\nabla\times u\). Then
\[
\partial_t\omega+(u\cdot\nabla)\omega=(\omega\cdot\nabla)u+\nu\Delta\omega+\nabla\times f.
\]
The term \((\omega\cdot\nabla)u\) is vortex stretching. It is absent in the scalar two-dimensional vorticity equation but active in three dimensions.
<div class="ledger-pair"><div><h3>Two dimensions</h3><p>Vorticity behaves like an advected-diffused scalar.</p><p>No vortex-stretching term.</p><p>Global regularity closes.</p></div><span aria-hidden="true">↔</span><div><h3>Three dimensions</h3><p>Vorticity is a vector.</p><p>Stretching can amplify magnitude.</p><p>Critical control remains open.</p></div></div></section>
<figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate III"><img src="../../assets/documentaries/navier_stokes/classes.svg" width="1024" height="1536" loading="lazy" alt="Nested solution classes distinguish Leray–Hopf weak solutions, strong solutions, and globally smooth solutions."></button><figcaption><span class="plate-label">Plate III</span><strong>Weak existence is not smooth existence</strong><small>Pedagogical orientation only. Each theorem retains its exact solution class.</small></figcaption></figure>
<section class="monograph-section" id="solution-classes" data-reader-section markdown="1"><p class="monograph-section__eyebrow">Chapter IV</p>
## Weak, Strong, and Smooth
A Leray–Hopf solution is global and finite-energy, but classical theory does not prove that every such solution is smooth or unique in three dimensions. A strong solution is unique while its controlling norm remains finite. Weak–strong uniqueness identifies the two while the strong solution exists.
<div class="imported-box"><strong>Imported established result</strong><p>Suitable weak solutions satisfy a local energy inequality. Caffarelli–Kohn–Nirenberg partial regularity bounds the parabolic Hausdorff dimension of the possible singular set; it does not prove that the set is empty.</p></div>
<div class="warning-box"><strong>Solution-class guardrail</strong><p>Moving silently between weak, suitable, strong, mild, and classical solutions changes the claim. Modern nonuniqueness results in broader weak classes do not constitute smooth finite-time blowup.</p></div></section>
<figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate IV"><img src="../../assets/documentaries/navier_stokes/frontier.svg" width="1024" height="1536" loading="lazy" alt="A scaling ladder and a singular-set diagram separate continuation criteria, partial regularity, and the unresolved endpoint."></button><figcaption><span class="plate-label">Plate IV</span><strong>The critical frontier</strong><small>Pedagogical orientation only. A continuation criterion identifies a sufficient condition, not its universal truth.</small></figcaption></figure>
<section class="monograph-section" id="millennium-frontier" data-reader-section markdown="1"><p class="monograph-section__eyebrow">Chapter V</p>
## The Millennium Frontier
The natural scaling is \(u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2t)\), \(p_\lambda(x,t)=\lambda^2p(\lambda x,\lambda^2t)\). The Ladyzhenskaya–Prodi–Serrin family gives continuation if
\[
u\in L^q(0,T;L^p),\qquad \frac2q+\frac3p\le1,\quad p>3.
\]
<div class="conjecture-box"><strong>The unresolved universal estimate</strong><p>The Clay problem requires proving that admissible smooth data never leave the smooth class, or producing a valid breakdown example. A continuation criterion does not prove its sufficient condition always holds.</p></div>
The active NS-CI-001 lane studies bounded obligations near \(L^4_tL^6_x\) and related weighted dissipation estimates. Its partial results refine the proof map without changing the parent problem's open status.
<p class="monograph-pullquote">The equation spends energy. The problem is whether it can concentrate structure faster than the accounting can see.</p></section>
<section class="monograph-section" id="appendix-formulations" data-reader-section markdown="1"><p class="monograph-section__eyebrow">Technical appendix A</p>
## Whole-Space and Periodic Formulations
The official problem separates whole-space and periodic alternatives. The projected equation is \(\partial_tu-\nu\Delta u=-\mathbb P\nabla\cdot(u\otimes u)\). Equivalence among pointwise, projected, mild, and distributional forms requires the stated regularity and domain assumptions.</section>
<section class="monograph-section" id="appendix-scaling" data-reader-section markdown="1"><p class="monograph-section__eyebrow">Technical appendix B</p>
## Scaling and Critical Spaces
For mixed norms, \(\|u_\lambda\|_{L^q_tL^p_x}=\lambda^{1-3/p-2/q}\|u\|_{L^q_tL^p_x}\). Thus \(2/q+3/p=1\) is the velocity-critical line. Energy-class information does not directly dominate it. Small-data critical theorems retain their smallness hypothesis.</section>
<section class="monograph-section" id="appendix-regularity" data-reader-section markdown="1"><p class="monograph-section__eyebrow">Technical appendix C</p>
## Continuation and Partial Regularity
Continuation criteria have the logical form: critical norm finite on \([0,T)\) implies extension beyond \(T\). Partial regularity locates the possible defect set; it neither certifies nor eliminates every defect. Numerical resolution criteria are method-dependent and cannot replace the continuum quantifier.</section>
<section class="monograph-section" id="appendix-trust" data-reader-section markdown="1"><p class="monograph-section__eyebrow">Technical appendix D</p>
## Claim-Level Trust Matrix
| Claim | Trust class | Qualification |
|---|---|---|
| Smooth local well-posedness | established | standard strong/mild theory |
| Global Leray–Hopf weak existence | imported established | energy-class weak solutions |
| Global two-dimensional regularity | imported established | not a three-dimensional theorem |
| Serrin continuation criteria | imported established | conditional |
| CKN partial regularity | imported established | singular set may still be nonempty |
| Universal 3D smoothness or breakdown | open | exact Clay alternative |
| NS-CI-001 progress | bounded programme evidence | no parent-problem promotion |
| Numerical simulations | empirical | no continuum proof object |
| Illuminated plates | pedagogical | never authoritative PDE diagrams |
<div class="warning-box"><strong>Final claim boundary</strong><p>This web edition changes presentation, not theorem strength. It does not prove global regularity, construct blowup, establish uniqueness of all weak solutions, or promote a neighbouring model into the true equation.</p></div></section>
<section class="monograph-section" id="sources" data-reader-section markdown="1"><p class="monograph-section__eyebrow">Sources and programme crosswalk</p>
## Governing literature and campaign record
<div class="bibliography"><p><a href="https://www.claymath.org/millennium/navier-stokes-equation/">Clay Mathematics Institute: Navier–Stokes Equation</a>.</p><p><a href="https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf">Charles Fefferman, official problem description</a>.</p><p><a href="https://doi.org/10.1007/BF02547754">Jean Leray, weak-solution foundations</a>.</p><p><a href="https://doi.org/10.1002/cpa.3160350604">Caffarelli, Kohn, and Nirenberg, partial regularity</a>.</p><p><a href="https://doi.org/10.1070/RM2003v058n02ABEH000608">Escauriaza, Seregin, and Šverák, endpoint regularity</a>.</p></div>
Programme links: [Domain 02](../../domains/navier_stokes/) · [claim-authority record](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/DOMAIN_02_NAVIER_STOKES_CRITICAL_INTEGRABILITY_MASTER_PLAN.md) · [campaign artifacts](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/navier_stokes_critical_integrability) · [review records](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/reviews/navier_stokes)</section>
<section class="monograph-colophon" aria-labelledby="edition-record-title"><h2 id="edition-record-title">Edition record</h2><p>This browser-native edition uses the immutable Poincaré reference contract and shared open-problem status vocabulary. Its native SVG plates are pedagogical derivatives; semantic HTML carries the searchable text and equations.</p><p>The committed pointer is a source record; the checksum-locked complete illustrated source bundle is the authoritative source artifact. MathJax 3.2.2 is a version-pinned network enhancement, and the source TeX remains present when it is unavailable.</p><p><strong>Web claim boundary:</strong> Browser-native, source-normalized exposition of the three-dimensional incompressible Navier–Stokes existence-and-smoothness problem. Energy estimates, Leray–Hopf weak existence, two-dimensional regularity, small-data theory, continuation criteria, partial regularity, numerical simulations, and NS-CI-001 progress are not promoted to global smoothness or finite-time breakdown.</p><div class="monograph-actions"><a class="monograph-button" href="../navier_stokes.edition.json">Web-edition data</a><a class="monograph-button" href="../documentary_web.schema.json">Reusable schema</a><a class="monograph-button" href="../sources/the_river_and_the_storm.tex">Source record</a><a class="monograph-button" href="../ARTIFACT_MANIFEST.json">Artifact manifest</a></div><dl class="edition-integrity"><div><dt>Rendered PDF</dt><dd>14,246,784 bytes · <code>1ece7069787eee27c225db773826b09c513f5b1b9d25972cd1a45fa46dfef34a</code> · <code>metadata_only</code></dd></div><div><dt>Complete LaTeX source</dt><dd>55,720 bytes · <code>d6627a7965c974e3de0b99dc9e1ea4b179b20ae41df56e505ad2b76e5f58e594</code> · <code>metadata_only</code></dd></div><div><dt>Authoritative complete illustrated source bundle</dt><dd>14,536,994 bytes · <code>847a5bb2f68da797ca90782c3ba480e47067f323c54c8eb0b91a171353dce895</code> · <code>metadata_only</code></dd></div></dl></section>
</article></div></div>
<dialog class="monograph-lightbox" data-plate-dialog aria-labelledby="plate-dialog-title"><form method="dialog"><button class="monograph-lightbox__close" aria-label="Close plate view">Close</button></form><div class="monograph-lightbox__frame"><img data-plate-dialog-image alt=""><p id="plate-dialog-title" data-plate-dialog-caption></p></div></dialog><noscript><p>The manuscript and source TeX remain readable without JavaScript. Plate enlargement, rendered mathematics, reading progress, focus mode, and reading-position memory are unavailable; the checksum-locked PDF remains the rendered archival edition.</p></noscript></div>
<script defer src="../../javascripts/documentary-mathjax.js"></script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js" crossorigin="anonymous" referrerpolicy="no-referrer" data-archival-role="enhancement-only"></script><script defer src="../../javascripts/documentary.js"></script>
