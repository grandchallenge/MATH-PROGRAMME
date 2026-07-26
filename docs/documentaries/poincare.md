<link rel="stylesheet" href="../../stylesheets/documentary.css">

<div class="gcl-monograph" data-gcl-reader="poincare" data-edition="1.0.0">
<a class="monograph-skip" href="#monograph-start">Skip to the manuscript</a>

<header class="monograph-hero" aria-labelledby="monograph-title">
  <div class="monograph-hero__art" aria-hidden="true"><img src="../../assets/documentaries/poincare/cover.svg" width="1055" height="1491" alt=""></div>
  <div class="monograph-hero__veil"></div>
  <div class="monograph-hero__copy">
    <p class="monograph-eyebrow">MATH-PROGRAMME · Documentary Treatment · PC-001</p>
    <h1 id="monograph-title">The Shape of a Sphere</h1>
    <p class="monograph-hero__subtitle">A gentle illustrated guide to the Poincaré theorem</p>
    <p class="monograph-hero__thesis">A closed three-dimensional world in which every loop contracts must be the three-sphere.</p>
    <div class="monograph-status" aria-label="Publication status"><span>Classical solved theorem</span><span>Archival reconstruction</span><span>No new-proof claim</span></div>
    <div class="monograph-actions"><a class="monograph-button monograph-button--primary" href="#monograph-start">Begin the journey</a><a class="monograph-button" href="../">Documentary library</a><a class="monograph-button" href="../sources/the_shape_of_a_sphere.tex">LaTeX source</a></div>
  </div>
</header>

<div class="monograph-progress" aria-hidden="true"><span data-reader-progress-bar></span></div>
<div class="monograph-reader" id="monograph-start">
  <nav class="monograph-toolbar" aria-label="Reader controls">
    <div class="monograph-toolbar__identity"><span>Digital Grand Challenge Library</span><strong>The Shape of a Sphere</strong></div>
    <div class="monograph-toolbar__controls"><button type="button" data-reader-focus aria-pressed="false">Focus mode</button><button type="button" data-reader-print>Print / save</button><button type="button" data-reader-reset>Reset position</button><output data-reader-progress aria-live="polite">0% read</output></div>
  </nav>

  <div class="monograph-layout">
    <aside class="monograph-contents" aria-label="Manuscript contents">
      <p class="monograph-contents__title">The journey</p>
      <ol><li><a href="#reader-note">How to read</a></li><li><a href="#loops">The loop</a></li><li><a href="#geometry">Geometry as engine</a></li><li><a href="#surgery">Controlled surgery</a></li><li><a href="#extinction">Extinction and reversal</a></li></ol>
      <p class="monograph-contents__title">Technical appendix</p>
      <ol><li><a href="#appendix-categories">Categories and definitions</a></li><li><a href="#appendix-flow">Ricci-flow controls</a></li><li><a href="#appendix-trust">Trust matrix</a></li><li><a href="#sources">Sources</a></li></ol>
    </aside>

    <main class="monograph-body">
      <section class="monograph-section" id="reader-note" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">A note to the reader</p>
      ## Wonder first; authority always visible

      This web edition is meant to be entered as one enters an old observatory: first by wonder, then by instruments, and finally by exact measurement. Its illuminated plates are aids to orientation and memory. They are not proof diagrams. The prose, equations, cited sources, and explicit trust labels govern every mathematical claim.

      The Poincaré theorem is solved. This volume reconstructs the classical Hamilton–Perelman route for a broad reader; it does not offer a new proof, an independent verification of the nonlinear estimates, or a machine-checked formalization of Ricci flow with surgery.

      <div class="claim-box"><strong>Established theorem</strong><p>Every closed, connected, simply connected topological three-manifold is homeomorphic to the three-sphere.</p></div>
      <div class="guardrail"><strong>Category guardrail</strong><p>Pictures of two-dimensional spheres and tori are analogies. The theorem concerns three-manifolds. Passing among topological, PL, smooth, and Riemannian categories uses dimension-three theorems; it is not definitional.</p></div>
      </section>

      <figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate I"><img src="../../assets/documentaries/poincare/plate_question.svg" width="1055" height="1491" loading="lazy" alt="A lower-dimensional analogy comparing contractible loops on a sphere with a loop trapped around a torus hole."></button><figcaption><span class="plate-label">Plate I</span><strong>The question hidden inside a loop</strong><small>Pedagogical orientation only. The sphere and torus are lower-dimensional models of the loop obstruction.</small></figcaption></figure>

      <section class="monograph-section" id="loops" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Chapter I</p>
      ## The question hidden inside a loop

      Imagine living in a universe with no outside. There is no surrounding room from which to inspect its shape. You may travel, draw loops, stretch them, and ask whether they can be pulled tight without tearing the world. Topology begins from this austere freedom: it studies what survives every continuous deformation.

      A space is **simply connected** when every loop can be contracted continuously to a point. On the ordinary sphere, a loop can slide and shrink until nothing remains. On a torus, a loop winding through the central hole cannot disappear. The loop remembers a global obstruction that no local inspection reveals.

      The theorem asks whether this loop test completely recognizes the three-sphere among closed three-dimensional worlds:

      $$M\text{ closed and connected},\qquad \pi_1(M)=1\quad\Longrightarrow\quad M\cong_{\mathrm{Top}}S^3.$$

      The hypothesis is terse. The conclusion is absolute. Yet the bridge between them cannot be built from pictures alone. A loop is one-dimensional; a three-manifold may hide its complexity in nested surfaces, prime factors, and geometric regions that only become visible after one equips it with a metric.

      <p class="monograph-pullquote">Topology asks what the world is. Geometry lends us a way to make the world answer.</p>
      </section>

      <figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate II"><img src="../../assets/documentaries/poincare/plate_geometry.svg" width="1055" height="1491" loading="lazy" alt="A curved geometry smoothing under Ricci flow while concentrated curvature signals a possible singularity."></button><figcaption><span class="plate-label">Plate II</span><strong>When geometry becomes an engine</strong><small>The metric evolves; curvature concentrates; analysis must distinguish harmless smoothing from singular behaviour.</small></figcaption></figure>

      <section class="monograph-section" id="geometry" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Chapter II</p>
      ## When geometry becomes an engine

      Richard Hamilton’s proposal was to place a Riemannian metric on the manifold and let that metric evolve by **Ricci flow**:

      $$\frac{\partial g}{\partial t}=-2\operatorname{Ric}(g).$$

      The equation is often compared with heat diffusion. Uneven curvature tends to spread and smooth. This is useful, but incomplete: nonlinear geometry can concentrate faster than diffusion can disperse it. A thin neck may form; curvature may blow up; the classical flow may cease to exist in finite time.

      Perelman supplied the controls that turn this apparent failure into information. Entropy and reduced-volume quantities restrain collapse. Blow-up limits reveal ancient geometric models. Canonical-neighbourhood theorems say that regions of sufficiently high curvature resemble a controlled catalogue—necks, caps, and compact positively curved pieces—at the relevant scale.

      <div class="proof-spine"><div><span>01</span><strong>Choose a metric</strong></div><div><span>02</span><strong>Run Ricci flow</strong></div><div><span>03</span><strong>Classify high curvature</strong></div><div><span>04</span><strong>Continue through surgery</strong></div></div>

      <div class="guardrail"><strong>Analytic import</strong><p>Entropy monotonicity, no local collapse, ancient-solution structure, canonical neighbourhoods, and surgery continuation are deep imported theorems. The web presentation explains their role but does not independently prove them.</p></div>
      </section>

      <figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate III"><img src="../../assets/documentaries/poincare/plate_surgery.svg" width="1055" height="1491" loading="lazy" alt="A neck-like high-curvature region is cut along controlled spheres and replaced by standard caps."></button><figcaption><span class="plate-label">Plate III</span><strong>The craft of controlled surgery</strong><small>Surgery is not topology-preserving. Its exact topological effect must be recorded and later reversed.</small></figcaption></figure>

      <section class="monograph-section" id="surgery" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Chapter III</p>
      ## The craft of controlled surgery

      Once a high-curvature neck is known to be close to a standard cylinder, the flow can be stopped just before catastrophe. One cuts across carefully chosen two-spheres, removes the most singular ends, attaches standard caps, and restarts the evolution on the surviving components.

      The word *surgery* can sound like an informal repair. Mathematically it is a theorem-bound operation with scale hierarchies, curvature thresholds, cap models, noncollapsing estimates, and a finite catalogue of topological transitions. A separating sphere cut records a connected-sum decomposition. A nonseparating cut records an $S^2\!\times S^1$-type factor in the orientable setting. Discarded components must belong to permitted, source-certified classes.

      <div class="claim-box"><strong>Bookkeeping theorem</strong><p>Conditional on the imported geometric event relation, a finite source-bound surgery history can be read backward to reconstruct a connected-sum expression for the original manifold.</p></div>

      <div class="guardrail"><strong>Extinction is not classification</strong><p>Many nontrivial spherical space forms also become extinct under Ricci flow. Finite extinction alone does not imply that the initial manifold was $S^3$; the backward factor reconstruction and the fundamental-group argument are indispensable.</p></div>
      </section>

      <figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate IV"><img src="../../assets/documentaries/poincare/plate_extinction.svg" width="1055" height="1491" loading="lazy" alt="A finite surgery history is read backward into factors, after which simple connectivity eliminates nontrivial factors and leaves the sphere."></button><figcaption><span class="plate-label">Plate IV</span><strong>Extinction, reversal, and the sphere</strong><small>Local finiteness plus finite extinction yields a finite history. Reverse induction restores the initial topology.</small></figcaption></figure>

      <section class="monograph-section" id="extinction" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Chapter IV</p>
      ## Extinction, reversal, and the sphere

      Perelman proved finite extinction for the relevant class of three-manifolds: after finite time the surgery flow has no surviving component. This endpoint is useful because a finite process can be reversed. Local finiteness of surgery times on each bounded interval, combined with a finite extinction time, gives a finite event history.

      Reading the history backward expresses the initial manifold as a connected sum of standard terminal and discarded factors. The final sieve is algebraic. By the Seifert–van Kampen theorem, connected sum becomes free product at the level of fundamental groups. Every nontrivial spherical space-form factor contributes a nontrivial finite group; every $S^2\!\times S^1$ factor contributes an infinite cyclic group. If the original fundamental group is trivial, none of these nontrivial factors can remain.

      What survives is the three-sphere.

      $$\pi_1(M)=1\quad\Longrightarrow\quad M\cong S^3.$$

      <p class="monograph-pullquote">The proof does not stare directly at the sphere. It governs a process until every alternative has nowhere left to hide.</p>
      </section>

      <section class="monograph-section" id="appendix-categories" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Technical appendix A</p>
      ## Definitions and category bridges

      A **closed** manifold is compact and has empty boundary. A **topological three-manifold** is Hausdorff, second countable, and locally homeomorphic to $\mathbb{R}^3$. In dimension three, classical triangulation and smoothing theorems permit the topological manifold to be treated through PL and smooth structures, after which one chooses a Riemannian metric.

      The conclusion produced by the analytic route is naturally smooth: the simply connected component is diffeomorphic to $S^3$. Forgetting smooth structure gives the required homeomorphism. These arrows are mathematical theorems, not changes of vocabulary.

      | Interface | Role | Status in this edition |
      |---|---|---|
      | Topological $\to$ PL $\to$ smooth | permits Ricci-flow input | imported classical theorem |
      | Smooth $\to$ Riemannian | choose initial metric | established construction |
      | Diffeomorphic $\to$ homeomorphic | returns to Clay statement | immediate implication |
      </section>

      <section class="monograph-section" id="appendix-flow" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Technical appendix B</p>
      ## Ricci flow and its controls

      Under parabolic rescaling, curvature and time transform together. The surgery parameters therefore form a hierarchy rather than a collection of universal constants: a canonical-neighbourhood accuracy is fixed; associated curvature controls are obtained; surgery tolerances are chosen sufficiently small; cutting and trigger scales are then derived. Silent interchange of local, stagewise, and global constants is a common source of false proofs.

      The analytic spine is:

      1. short-time existence for the initial metric;
      2. entropy and reduced-geometry monotonicity;
      3. no local collapse at controlled scales;
      4. compactness and structure of blow-up limits;
      5. canonical neighbourhoods at high curvature;
      6. construction and continuation of Ricci flow with surgery;
      7. finite extinction under the topological hypothesis.

      The full estimates belong to Perelman’s papers and detailed expositions by Kleiner–Lott and Morgan–Tian.
      </section>

      <section class="monograph-section" id="appendix-trust" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Technical appendix C</p>
      ## Claim-level trust matrix

      | Claim | Trust class | Qualification |
      |---|---|---|
      | Poincaré theorem | established | classical solved theorem |
      | Top/PL/Diff bridge in dimension three | imported | classical category theorem |
      | Ricci-flow analytic core | imported | not independently reconstructed here |
      | Finite extinction route | imported | source-normalized to Perelman and Morgan–Tian |
      | Finite-event backward evaluator | kernel-checked, bounded | conditional on imported event equations |
      | Illuminated plates | pedagogical | never authoritative proof diagrams |
      | New proof or novelty | not claimed | explicitly excluded |

      <div class="guardrail"><strong>Final claim boundary</strong><p>This web edition changes presentation, not theorem strength. It adds responsive reading, searchability, accessibility, source links, plate enlargement, reading-position memory, and print fidelity. It does not alter the archived mathematical disposition of PC-001.</p></div>
      </section>

      <section class="monograph-section" id="sources" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Sources</p>
      ## The governing literature

      <div class="bibliography">
      <p>Richard S. Hamilton, “Three-manifolds with positive Ricci curvature,” <em>Journal of Differential Geometry</em> 17 (1982), 255–306.</p>
      <p>Grisha Perelman, <a href="https://arxiv.org/abs/math/0211159">The entropy formula for the Ricci flow and its geometric applications</a> (2002).</p>
      <p>Grisha Perelman, <a href="https://arxiv.org/abs/math/0303109">Ricci flow with surgery on three-manifolds</a> (2003).</p>
      <p>Grisha Perelman, <a href="https://arxiv.org/abs/math/0307245">Finite extinction time for the solutions to the Ricci flow on certain three-manifolds</a> (2003).</p>
      <p>Bruce Kleiner and John Lott, <a href="https://arxiv.org/abs/math/0605667">Notes on Perelman’s papers</a>, version 5 (2013).</p>
      <p>John W. Morgan and Gang Tian, <a href="https://www.claymath.org/resource/ricci-flow-and-the-poincare-conjecture/"><em>Ricci Flow and the Poincaré Conjecture</em></a> (2007).</p>
      </div>
      </section>

      <section class="monograph-colophon" aria-labelledby="edition-record-title">
        <h2 id="edition-record-title">Edition record</h2>
        <p>This is the reference implementation for the Grand Challenge Library web format. Its content schema, plate contract, scoped palette, responsive rules, accessibility landmarks, interactive controls, and print treatment are intended for reuse by the remaining documentary volumes.</p>
        <div class="monograph-actions"><a class="monograph-button" href="../poincare.edition.json">Web-edition data</a><a class="monograph-button" href="../documentary_web.schema.json">Reusable schema</a><a class="monograph-button" href="../sources/the_shape_of_a_sphere.tex">Authoritative LaTeX</a></div>
        <dl class="edition-integrity"><div><dt>Facsimile PDF</dt><dd>18,426,001 bytes · <code>0e1499ee13a6966a3b190b850b6acd2db647952826c54b3abc575d607a2f6ea4</code></dd></div><div><dt>LaTeX source</dt><dd>59,039 bytes · <code>58dc94e7296bdfad5f31720f2e3b53be4097ff356f6c83a58db769db357e7b9d</code></dd></div><div><dt>Illustrated bundle</dt><dd>42,084,814 bytes · <code>670cb6a4d63ed79a21fbbe70857bd0d46ad63ce546c92d320de7e39f06612771</code></dd></div></dl>
      </section>
    </main>
  </div>
</div>

<dialog class="monograph-lightbox" data-plate-dialog aria-labelledby="plate-dialog-title"><form method="dialog"><button class="monograph-lightbox__close" aria-label="Close plate view">Close</button></form><div class="monograph-lightbox__frame"><img data-plate-dialog-image alt=""><p id="plate-dialog-title" data-plate-dialog-caption></p></div></dialog>
<noscript><p>The manuscript remains fully readable without JavaScript. Plate enlargement, reading progress, focus mode, and reading-position memory are unavailable.</p></noscript>
</div>

<script defer src="../../javascripts/documentary-mathjax.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js"></script>
<script defer src="../../javascripts/documentary.js"></script>
