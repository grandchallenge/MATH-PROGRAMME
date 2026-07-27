<link rel="stylesheet" href="../../stylesheets/documentary.css">
<link rel="stylesheet" href="../../stylesheets/documentary-status.css">

<div class="gcl-monograph" data-gcl-reader="bsd" data-edition="1.1.0">
<a class="monograph-skip" href="#monograph-start">Skip to the manuscript</a>

<header class="monograph-hero" aria-labelledby="monograph-title">
  <div class="monograph-hero__art" aria-hidden="true"><img src="../../assets/documentaries/bsd/cover.svg" width="1024" height="1536" alt=""></div>
  <div class="monograph-hero__veil"></div>
  <div class="monograph-hero__copy">
    <p class="monograph-eyebrow">MATH-PROGRAMME · Documentary Treatment · BSD-001</p>
    <h1 id="monograph-title">The Hidden Music of Elliptic Curves</h1>
    <p class="monograph-hero__subtitle">A guided journey to the Birch and Swinnerton–Dyer conjecture</p>
    <p class="monograph-hero__thesis">The rational points on a curve and the silence of its analytic function at one central point are conjectured to measure the same hidden rank.</p>
    <div class="monograph-status" aria-label="Publication status"><span>Open Millennium Prize Problem</span><span>BSD-001</span><span>No proof claimed</span></div>
    <div class="monograph-actions"><a class="monograph-button monograph-button--primary" href="#monograph-start">Begin the journey</a><a class="monograph-button" href="../">Documentary library</a><a class="monograph-button" href="../sources/the_hidden_music_of_elliptic_curves.tex">Source record</a></div>
  </div>
</header>

<div class="monograph-progress" aria-hidden="true"><span data-reader-progress-bar></span></div>
<div class="monograph-reader" id="monograph-start" tabindex="-1">
  <nav class="monograph-toolbar" aria-label="Reader controls">
    <div class="monograph-toolbar__identity"><span>Digital Grand Challenge Library</span><strong>The Hidden Music of Elliptic Curves</strong></div>
    <div class="monograph-toolbar__controls"><button type="button" data-reader-focus aria-pressed="false">Focus mode</button><button type="button" data-reader-print>Print / save</button><button type="button" data-reader-reset>Reset position</button><output data-reader-progress aria-live="polite">0% read</output></div>
  </nav>

  <div class="monograph-layout">
    <aside class="monograph-contents" aria-label="Manuscript contents">
      <p class="monograph-contents__title">The journey</p>
      <ol><li><a href="#reader-note">How to read</a></li><li><a href="#rational-points">Rational points</a></li><li><a href="#group-law">A curve that adds</a></li><li><a href="#local-counts">Counting at primes</a></li><li><a href="#central-bridge">One number, two languages</a></li><li><a href="#theorem-frontier">The theorem frontier</a></li></ol>
      <p class="monograph-contents__title">Technical appendix</p>
      <ol><li><a href="#appendix-curves">Curves and rank</a></li><li><a href="#appendix-lfunction">The L-function</a></li><li><a href="#appendix-strong">Strong BSD</a></li><li><a href="#appendix-selmer">Selmer and descent</a></li><li><a href="#appendix-trust">Trust matrix</a></li><li><a href="#sources">Sources</a></li></ol>
    </aside>

    <article class="monograph-body" aria-label="The Hidden Music of Elliptic Curves manuscript">
      <section class="monograph-section" id="reader-note" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">A note to the reader</p>
      ## Wonder first; the open boundary always visible

      An elliptic curve may be written in a line, yet its rational points can resist every direct search. Birch and Swinnerton–Dyer proposes that this arithmetic difficulty is reflected exactly by a complex analytic object assembled from point counts at every prime. The conjecture remains open.

      This browser edition is a derivative, source-normalized exposition. The plates provide memory and atmosphere; text inside them is decorative. The definitions, equations, source links, campaign records, and trust labels govern the mathematics.

      **Edition status:** Open Millennium Prize Problem; documentary exposition; no proof claim.

      <div class="conjecture-box"><strong>Open conjecture</strong><p>For every elliptic curve $E/\mathbb{Q}$, the Mordell–Weil rank is conjectured to equal the order of vanishing of $L(E,s)$ at $s=1$. The universal leading-term formula and the general finiteness of the Tate–Shafarevich group remain open.</p></div>
      <div class="warning-box"><strong>Claim boundary</strong><p>Numerical agreement, parity, Selmer bounds, family averages, one-prime results, $p$-adic formulas, and the analytic-rank-zero-or-one theorem terrain do not by themselves establish the universal complex conjecture.</p></div>
      </section>

      <figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate I"><img src="../../assets/documentaries/bsd/plate_curve.svg" width="1024" height="1536" loading="lazy" alt="An illustrated map from rational right triangles and cubic curves to sparse rational points, torsion, rank, and the limits of finite search."></button><figcaption><span class="plate-label">Plate I</span><strong>The ancient question of rational solutions</strong><small>Pedagogical orientation only. The depicted curves and diagrams compress exact arithmetic into visual analogy.</small></figcaption></figure>

      <section class="monograph-section" id="rational-points" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Chapter I</p>
      ## The ancient question of rational solutions

      Over the real numbers, a cubic curve is a continuous shape. Over the rational numbers, its points form a sparse constellation. The question is not merely whether a point exists, but whether all rational points can be described by finitely many instructions.

      <div class="definition-box"><strong>Definition</strong><p>An elliptic curve over $\mathbb{Q}$ is a smooth projective genus-one curve equipped with a rational base point. In a short Weierstrass model it may be written $E:y^2=x^3+Ax+B$ with $4A^3+27B^2\ne0$.</p></div>

      The congruent-number problem supplies an ancient doorway. A positive integer $n$ is the area of a rational right triangle exactly when the curve

      $$E_n:y^2=x^3-n^2x$$

      has a rational point of infinite order. For $n=5$, the point $(25/4,75/8)$ corresponds to a rational right triangle with sides $3/2$, $20/3$, and $41/6$.

      Search can find points and prove lower bounds. Search cannot certify that no hidden generator of enormous height remains. That stopping problem is why descent, height pairings, Selmer groups, and local information enter.
      </section>

      <figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate II"><img src="../../assets/documentaries/bsd/plate_harmony.svg" width="1024" height="1536" loading="lazy" alt="A paired arithmetic and analytic panorama links the Mordell–Weil group of rational points to the vanishing of an elliptic-curve L-function."></button><figcaption><span class="plate-label">Plate II</span><strong>Two ledgers in the same hand</strong><small>The rational-point ledger and the analytic ledger are distinct constructions. BSD predicts their exact concordance.</small></figcaption></figure>

      <section class="monograph-section" id="group-law" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Chapter II</p>
      ## A curve that adds

      Draw a line through two rational points on a nonsingular cubic. The line meets the cubic a third time; reflecting that third intersection across the horizontal axis defines the sum. Tangency supplies doubling. The geometry hides rational formulas, so rational points add to rational points.

      <div class="theorem-box"><strong>Established theorem · Mordell–Weil</strong><p>The group of rational points is finitely generated: $E(\mathbb{Q})\cong\mathbb{Z}^r\oplus E(\mathbb{Q})_{\mathrm{tors}}$. The integer $r$ is the algebraic rank.</p></div>

      The torsion subgroup cycles through finitely many points. The free part extends in $r$ independent directions. Canonical heights measure those directions quadratically, and their height-pairing determinant becomes the regulator in the refined conjecture.

      <div class="ledger-pair"><div><h3>Arithmetic ledger</h3><p>Rational points</p><p>Torsion subgroup</p><p>Rank and regulator</p></div><span aria-hidden="true">↔</span><div><h3>Analytic ledger</h3><p>Prime point counts</p><p>Euler product</p><p>Central zero and leading term</p></div></div>
      </section>

      <figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate III"><img src="../../assets/documentaries/bsd/plate_bridge.svg" width="1024" height="1536" loading="lazy" alt="Prime-by-prime point counts are assembled into Euler factors and an L-function whose behaviour at the central point is compared with rank."></button><figcaption><span class="plate-label">Plate III</span><strong>From prime counts to the central point</strong><small>No single prime determines the rank. The analytic object arises only after all local factors are assembled.</small></figcaption></figure>

      <section class="monograph-section" id="local-counts" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Chapter III</p>
      ## Counting at every prime

      Reduce a suitable integral equation modulo a prime $p$ and count its points over the finite field $\mathbb{F}_p$. At a prime of good reduction define

      $$a_p=p+1-\#E(\mathbb{F}_p).$$

      The local factor is

      $$L_p(E,s)=\left(1-a_pp^{-s}+p^{1-2s}\right)^{-1},$$

      with separate factors at bad primes. Their Euler product defines the Hasse–Weil $L$-function in its initial half-plane of convergence.

      <div class="imported-box"><strong>Imported established result · modularity</strong><p>Every elliptic curve over $\mathbb{Q}$ is modular. Consequently its $L$-function has analytic continuation and a functional equation centred at $s=1$. This web edition uses that theorem; it does not reconstruct its proof.</p></div>

      The functional equation has a sign $w_E\in\{\pm1\}$. It constrains the parity of the analytic order of vanishing, but a sign of $-1$ does not force the order to be exactly one.

      <div class="proof-spine"><div><span>01</span><strong>Count modulo $p$</strong></div><div><span>02</span><strong>Build Euler factors</strong></div><div><span>03</span><strong>Continue $L(E,s)$</strong></div><div><span>04</span><strong>Listen at $s=1$</strong></div></div>
      </section>

      <figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate IV"><img src="../../assets/documentaries/bsd/plate_overture.svg" width="1024" height="1536" loading="lazy" alt="A decorative ledger surrounds the leading-term formula with period, regulator, Tamagawa, torsion, and Tate–Shafarevich contributions."></button><figcaption><span class="plate-label">Plate IV</span><strong>The strong BSD ledger</strong><small>The visual balance is mnemonic. Every factor requires an exact mathematical definition and normalization.</small></figcaption></figure>

      <section class="monograph-section" id="central-bridge" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Chapter IV</p>
      ## One number in two languages

      The public face of the conjecture is the equality

      $$\operatorname{rank}E(\mathbb{Q})=\operatorname{ord}_{s=1}L(E,s).$$

      The left side counts independent rational generators. The right side counts how many derivatives vanish before the first nonzero Taylor coefficient appears at the central point.

      The strong form predicts more. If $r=\operatorname{rank}E(\mathbb{Q})$ and the Tate–Shafarevich group is finite, then—after fixing standard conventions—

      $$\frac{L^{(r)}(E,1)}{r!}=\frac{\Omega_E\,\operatorname{Reg}(E/\mathbb{Q})\,\#\operatorname{Sha}(E/\mathbb{Q})\,\prod_p c_p}{\#E(\mathbb{Q})_{\mathrm{tors}}^2}.$$

      Period measures the real geometry; the regulator measures the arithmetic lattice; Tamagawa numbers record bad-prime component defects; torsion corrects finite symmetry; the Tate–Shafarevich group records locally soluble torsors that may fail globally.

      <div class="warning-box"><strong>Three obligations, not one slogan</strong><p>Rank equality, finiteness of $\operatorname{Sha}$, and the normalized leading-term formula are logically distinct. A theorem about one of them does not silently prove the others.</p></div>
      </section>

      <figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate V"><img src="../../assets/documentaries/bsd/plate_frontier.svg" width="1024" height="1536" loading="lazy" alt="A map distinguishes established modularity and low-rank results from the unresolved higher-rank and universal leading-term frontier."></button><figcaption><span class="plate-label">Plate V</span><strong>Islands of theorem, ocean of conjecture</strong><small>Known results retain their exact rank range, prime dependence, family quantifier, and normalization hypotheses.</small></figcaption></figure>

      <section class="monograph-section" id="theorem-frontier" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Chapter V</p>
      ## Islands of theorem, ocean of conjecture

      Modularity and Mordell–Weil finite generation are theorems. Gross–Zagier and Kolyvagin establish the decisive low-rank terrain: for elliptic curves over $\mathbb{Q}$ of analytic rank zero or one, algebraic rank agrees with analytic rank and the Tate–Shafarevich group is finite.

      <div class="theorem-box"><strong>Established low-rank terrain</strong><p>Analytic rank $0$ or $1$ yields the matching Mordell–Weil rank and finite $\operatorname{Sha}$ for elliptic curves over $\mathbb{Q}$, through modularity, Gross–Zagier, and Kolyvagin.</p></div>

      Higher rank is not merely a longer version of rank one. The regulator becomes a determinant of several independent global directions; higher-order vanishing must be matched by enough arithmetic classes; local conditions and hidden Tate–Shafarevich contributions must be controlled simultaneously.

      <div class="conjecture-box"><strong>Still open universally</strong><p>For every elliptic curve over $\mathbb{Q}$: equality of algebraic and analytic rank, finiteness of $\operatorname{Sha}$, and the complete complex leading-term formula.</p></div>

      <p class="monograph-pullquote">Geometry writes the instrument. Arithmetic chooses the notes. Analysis reveals the score.</p>
      </section>

      <section class="monograph-section" id="appendix-curves" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Technical appendix A</p>
      ## Elliptic curves and the Mordell–Weil group

      For a short Weierstrass model $E:y^2=x^3+Ax+B$, the discriminant is $\Delta=-16(4A^3+27B^2)\ne0$. The projective point $O=[0:1:0]$ is the identity.

      For distinct $P=(x_1,y_1)$ and $Q=(x_2,y_2)$ with $x_1\ne x_2$,

      $$m=\frac{y_2-y_1}{x_2-x_1},\qquad x_3=m^2-x_1-x_2,\qquad y_3=-y_1+m(x_1-x_3).$$

      Then $P+Q=(x_3,y_3)$. Associativity is not a consequence of the picture alone; it belongs to the algebraic-group structure.

      The canonical height pairing on a basis $P_1,\ldots,P_r$ of the free part yields

      $$\operatorname{Reg}(E/\mathbb{Q})=\det\bigl(\langle P_i,P_j\rangle\bigr),$$

      with the empty determinant convention $1$ when $r=0$.
      </section>

      <section class="monograph-section" id="appendix-lfunction" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Technical appendix B</p>
      ## The $L$-function and analytic rank

      The Euler product converges absolutely initially for $\operatorname{Re}(s)>3/2$. Modularity identifies it with the $L$-series of a weight-two newform. A standard completed normalization is

      $$\Lambda(E,s)=N^{s/2}(2\pi)^{-s}\Gamma(s)L(E,s),$$

      satisfying $\Lambda(E,s)=w_E\Lambda(E,2-s)$. The analytic rank is

      $$r_{\mathrm{an}}(E)=\operatorname{ord}_{s=1}L(E,s).$$

      The root number gives $(-1)^{r_{\mathrm{an}}}=w_E$. This is analytic parity, not by itself the algebraic rank equality.
      </section>

      <section class="monograph-section" id="appendix-strong" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Technical appendix C</p>
      ## The strong formula and normalization discipline

      Authors distribute real periods, archimedean factors, completed-function terms, and local conventions differently. A claimed comparison must first reconcile those choices. The formula displayed here uses the incomplete Hasse–Weil $L$-function and a standard real-period convention.

      <div class="warning-box"><strong>Normalization guardrail</strong><p>A missing period component, factorial, torsion square, bad-prime factor, or completed-function term can create a false disagreement—or a false proof. Symbol matching is not normalization matching.</p></div>

      The phrase “BSD is true for this curve” must identify whether it means rank equality, finite $\operatorname{Sha}$, the full complex leading term, a $p$-part, or a computational certificate for a fixed curve.
      </section>

      <section class="monograph-section" id="appendix-selmer" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Technical appendix D</p>
      ## Selmer groups, descent, and the hidden term

      Kummer theory yields

      $$0\longrightarrow E(\mathbb{Q})/nE(\mathbb{Q})\longrightarrow \operatorname{Sel}_n(E/\mathbb{Q})\longrightarrow \operatorname{Sha}(E/\mathbb{Q})[n]\longrightarrow0.$$

      For a prime $p$,

      $$0\longrightarrow E(\mathbb{Q})\otimes\mathbb{Q}_p/\mathbb{Z}_p\longrightarrow \operatorname{Sel}_{p^\infty}(E/\mathbb{Q})\longrightarrow \operatorname{Sha}(E/\mathbb{Q})[p^\infty]\longrightarrow0.$$

      Descent converts an infinite search into finite covering and local-solubility problems and can give an upper bound on rank. The upper bound is sharp only after the relevant Tate–Shafarevich contribution is controlled.

      <div class="warning-box"><strong>Selmer guardrail</strong><p>Selmer corank is not automatically Mordell–Weil rank. A nontrivial $p$-primary Tate–Shafarevich contribution may remain.</p></div>
      </section>

      <section class="monograph-section" id="appendix-trust" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Technical appendix E</p>
      ## Known results and claim-level trust matrix

      | Claim | Trust class | Qualification |
      |---|---|---|
      | $E(\mathbb{Q})$ is finitely generated | established | Mordell–Weil theorem |
      | Every elliptic curve over $\mathbb{Q}$ is modular | imported established | supplies continuation and functional equation |
      | Analytic rank $0$ or $1$ gives matching algebraic rank and finite $\operatorname{Sha}$ | imported established | exact low-rank terrain |
      | Universal rank equality | open | no finite computation, parity theorem, or family result promotes it |
      | Universal finiteness of $\operatorname{Sha}$ | open | separate from rank equality |
      | Universal complex leading-term formula | open | requires every normalization and arithmetic factor |
      | A fixed-curve rigorous computation | bounded evidence or certificate | does not imply the universal statement |
      | A $p$-adic or one-prime theorem | hypothesis-sensitive theorem terrain | not identical to the global complex formula |
      | Illuminated plates | pedagogical | never authoritative proof diagrams |

      <div class="warning-box"><strong>Final claim boundary</strong><p>This web edition changes presentation, not theorem strength. It does not prove BSD, provide a new reduction, independently verify the complete literature, or make a novelty or priority claim.</p></div>
      </section>

      <section class="monograph-section" id="sources" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Sources and programme crosswalk</p>
      ## The governing literature and campaign record

      <div class="bibliography">
      <p>Andrew Wiles, <a href="https://www.claymath.org/wp-content/uploads/2022/05/birchswin.pdf">The Birch and Swinnerton–Dyer Conjecture</a>, official Millennium Problem description.</p>
      <p>B. J. Birch and H. P. F. Swinnerton-Dyer, <a href="https://doi.org/10.1515/crll.1965.218.79">“Notes on elliptic curves II”</a> (1965).</p>
      <p>Christophe Breuil, Brian Conrad, Fred Diamond, and Richard Taylor, <a href="https://doi.org/10.1090/S0894-0347-01-00370-8">“On the modularity of elliptic curves over $\mathbb{Q}$”</a> (2001).</p>
      <p>Benedict Gross and Don Zagier, <a href="https://doi.org/10.1007/BF01388809">“Heegner points and derivatives of $L$-series”</a> (1986).</p>
      <p>V. A. Kolyvagin and D. Yu. Logachev, <a href="https://www.mathnet.ru/eng/aa47">“Finiteness of the Shafarevich–Tate group and the group of rational points for some modular abelian varieties”</a> (1989/1990).</p>
      <p><a href="https://www.claymath.org/millennium/birch-and-swinnerton-dyer-conjecture/">Clay Mathematics Institute: Birch and Swinnerton–Dyer Conjecture</a>.</p>
      </div>

      Programme links: [Domain 04](../../domains/birch_swinnerton_dyer/) · [canonical master plan](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/DOMAIN_04_BIRCH_SWINNERTON_DYER_MASTER_PLAN.md) · [campaign artifacts](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/birch_swinnerton_dyer) · [review records](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/reviews/birch_swinnerton_dyer)
      </section>

      <section class="monograph-colophon" aria-labelledby="edition-record-title">
        <h2 id="edition-record-title">Edition record</h2>
        <p>This is the first conversion built on the immutable Poincaré reference contract. It tests the shared reader against arithmetic geometry, local-to-global diagrams, layered conjecture statements, dense notation, and a stronger distinction among theorem, imported result, evidence, and open claim.</p>
        <p>The web edition is derivative. The committed pointer is a source record; the checksum-locked complete illustrated source bundle is the authoritative source artifact. MathJax 3.2.2 is a version-pinned network enhancement, and the source TeX remains present when it is unavailable.</p>
        <p><strong>Web claim boundary:</strong> Browser-native, source-normalized exposition of rational points, the Mordell–Weil group, the Hasse–Weil L-function, low-rank theorem terrain, and the strong BSD formula. Numerical agreement, parity, Selmer bounds, family results, one-prime theorems, and $p$-adic analogues are not promoted to the universal complex conjecture.</p>
        <div class="monograph-actions"><a class="monograph-button" href="../bsd.edition.json">Web-edition data</a><a class="monograph-button" href="../documentary_web.schema.json">Reusable schema</a><a class="monograph-button" href="../sources/the_hidden_music_of_elliptic_curves.tex">Source record</a><a class="monograph-button" href="../ARTIFACT_MANIFEST.json">Artifact manifest</a></div>
        <dl class="edition-integrity"><div><dt>Rendered PDF</dt><dd>16,582,087 bytes · <code>36254378e11fd22a067944838341ae04fedbd13e5ea588180023874d7ba49ce9</code> · <code>metadata_only</code></dd></div><div><dt>Complete LaTeX source</dt><dd>50,500 bytes · <code>9b7b95702a5305c51e66e026d44ddf3003029808edb3009ed1b2fcbc92e6b2b4</code> · <code>metadata_only</code></dd></div><div><dt>Authoritative complete illustrated source bundle</dt><dd>16,995,210 bytes · <code>c0782575453227311630e17c443a4dea08091b3a3824bc23a1af17f5bd0d8377</code> · <code>metadata_only</code></dd></div></dl>
      </section>
    </article>
  </div>
</div>

<dialog class="monograph-lightbox" data-plate-dialog aria-labelledby="plate-dialog-title"><form method="dialog"><button class="monograph-lightbox__close" aria-label="Close plate view">Close</button></form><div class="monograph-lightbox__frame"><img data-plate-dialog-image alt=""><p id="plate-dialog-title" data-plate-dialog-caption></p></div></dialog>
<noscript><p>The manuscript and source TeX remain readable without JavaScript. Plate enlargement, rendered mathematics, reading progress, focus mode, and reading-position memory are unavailable; the checksum-locked PDF remains the rendered archival edition.</p></noscript>
</div>

<script defer src="../../javascripts/documentary-mathjax.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js" crossorigin="anonymous" referrerpolicy="no-referrer" data-archival-role="enhancement-only"></script>
<script defer src="../../javascripts/documentary.js"></script>
