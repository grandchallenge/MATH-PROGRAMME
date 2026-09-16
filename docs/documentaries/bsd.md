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
    <p class="monograph-hero__thesis">BSD asks whether two independently constructed notions of rank—one arithmetic and one analytic—always agree, and whether their leading terms encode the same arithmetic data.</p>
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
      <ol><li><a href="#reader-note">How to read</a></li><li><a href="#rational-points">Rational points</a></li><li><a href="#group-law">The group law</a></li><li><a href="#local-counts">Counting at primes</a></li><li><a href="#central-bridge">The strong formula</a></li><li><a href="#theorem-frontier">The theorem frontier</a></li></ol>
      <p class="monograph-contents__title">Technical appendix</p>
      <ol><li><a href="#appendix-curves">Curves and rank</a></li><li><a href="#appendix-lfunction">The L-function</a></li><li><a href="#appendix-strong">Normalization</a></li><li><a href="#appendix-selmer">Selmer and descent</a></li><li><a href="#appendix-trust">Trust matrix</a></li><li><a href="#sources">Sources</a></li></ol>
    </aside>

    <article class="monograph-body" aria-label="The Hidden Music of Elliptic Curves manuscript">
      <section class="monograph-section" id="reader-note" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">A note to the reader</p>
      ## Exact objects first; the open boundary always visible

      Birch and Swinnerton–Dyer links the rational-point structure of an elliptic curve to the behaviour of its $L$-function at $s=1$. The conjecture remains open in general.

      This browser edition is a derivative, source-normalized exposition. Its numbered plates render exact mathematical objects, exact finite computations, or quantified theorem structure whenever the adjacent concept permits it. Wolfram Language is the canonical semantic-master language for the revised plates; the committed web graphics are deterministic publication derivatives. The plates are pedagogical, not proof evidence. Definitions, equations, source links, campaign records, and trust labels govern the mathematics.

      **Edition status:** Open Millennium Prize Problem; documentary exposition; no proof claim.

      <div class="conjecture-box"><strong>Open conjecture</strong><p>For every elliptic curve $E/\mathbb{Q}$, BSD predicts $\operatorname{rank}E(\mathbb{Q})=\operatorname{ord}_{s=1}L(E,s)$. The universal leading-term formula and general finiteness of $\operatorname{Sha}(E/\mathbb{Q})$ remain open.</p></div>
      <div class="warning-box"><strong>Claim boundary</strong><p>Finite computation, parity, Selmer bounds, family averages, one-prime results, $p$-adic formulas, and analytic-rank-zero-or-one theorems do not by themselves establish the universal complex conjecture.</p></div>
      </section>

      <section class="monograph-section" id="rational-points" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Chapter I</p>
      ## Rational points: one exact doorway

      An elliptic curve over $\mathbb{Q}$ can be written in short Weierstrass form

      $$E:y^2=x^3+Ax+B,\qquad 4A^3+27B^2\ne0.$$

      <div class="definition-box"><strong>Definition</strong><p>An elliptic curve over $\mathbb{Q}$ is a smooth projective genus-one curve equipped with a rational base point. A short Weierstrass model has nonzero discriminant.</p></div>

      Its real points form continuous curves. Its rational points form a finitely generated abelian group, but finding all generators can be difficult.

      The congruent-number problem gives a concrete entry point. A positive integer $n$ is the area of a rational right triangle exactly when

      $$E_n:y^2=x^3-n^2x$$

      has a rational point of infinite order. For $n=5$, the exact point

      $$P=\left(\frac{25}{4},\frac{75}{8}\right)$$

      lies on $E_5:y^2=x^3-25x$ and corresponds to a rational right triangle with sides $3/2$, $20/3$, and $41/6$. Its area is exactly $5$.

      <div class="warning-box"><strong>Finite-window guardrail</strong><p>Displaying a real curve and one rational point does not determine the Mordell–Weil rank and does not prove BSD.</p></div>
      </section>

      <figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate I"><img src="../../assets/documentaries/bsd/plate_curve.svg" width="1024" height="1536" loading="lazy" alt="An illustrated map from rational right triangles and cubic curves to sparse rational points, torsion, rank, and the limits of finite search."></button><figcaption><span class="plate-label">Plate I</span><strong>The ancient question of rational solutions</strong><small>Fallback predecessor plate. With JavaScript enabled, the reviewed exact-object successor is activated at this stable source reference.</small></figcaption></figure>

      <section class="monograph-section" id="group-law" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Chapter II</p>
      ## The chord–tangent group law

      A nonsingular cubic carries an addition law. A line through two points meets the cubic a third time; reflecting that third intersection across the horizontal axis gives the sum. A tangent supplies doubling.

      Plate II fixes one exact rational example on

      $$E:y^2=x^3-x+1.$$

      The points $P=(0,1)$ and $Q=(1,1)$ lie on $E$. Their horizontal chord $y=1$ meets $E$ again at $R=(-1,1)$. Reflection gives

      $$P+Q=-R=(-1,-1).$$

      <div class="theorem-box"><strong>Established theorem · Mordell–Weil</strong><p>$E(\mathbb{Q})\cong\mathbb{Z}^r\oplus E(\mathbb{Q})_{\mathrm{tors}}$. The integer $r$ is the algebraic rank.</p></div>

      Canonical heights measure the independent free directions. The determinant of their height pairing is the regulator that appears in the strong BSD formula.
      </section>

      <figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate II"><img src="../../assets/documentaries/bsd/plate_harmony.svg" width="1024" height="1536" loading="lazy" alt="A paired arithmetic and analytic panorama links the Mordell–Weil group of rational points to the vanishing of an elliptic-curve L-function."></button><figcaption><span class="plate-label">Plate II</span><strong>Two ledgers in the same hand</strong><small>Fallback predecessor plate. With JavaScript enabled, the reviewed exact chord–tangent successor is activated at this stable source reference.</small></figcaption></figure>

      <section class="monograph-section" id="local-counts" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Chapter III</p>
      ## Counting at a good prime

      Reduce a suitable integral equation modulo a prime $p$. At a prime of good reduction define

      $$a_p=p+1-\#E(\mathbb{F}_p),$$

      and

      $$L_p(E,s)=\left(1-a_pp^{-s}+p^{1-2s}\right)^{-1}.$$

      For $E_5:y^2=x^3-25x$ at $p=13$, exact enumeration gives $19$ affine solutions. Including the point at infinity,

      $$\#E_5(\mathbb{F}_{13})=20,\qquad a_{13}=13+1-20=-6.$$

      Hence

      $$L_{13}(E_5,s)=\left(1+6\cdot13^{-s}+13^{1-2s}\right)^{-1}.$$

      The finite sample in Plate III is exact for the displayed primes. It is not an estimator of rank.

      <div class="imported-box"><strong>Imported established result · modularity</strong><p>Every elliptic curve over $\mathbb{Q}$ is modular. Its $L$-function therefore has analytic continuation and a functional equation centred at $s=1$.</p></div>
      </section>

      <figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate III"><img src="../../assets/documentaries/bsd/plate_bridge.svg" width="1024" height="1536" loading="lazy" alt="Prime-by-prime point counts are assembled into Euler factors and an L-function whose behaviour at the central point is compared with rank."></button><figcaption><span class="plate-label">Plate III</span><strong>From prime counts to the central point</strong><small>Fallback predecessor plate. With JavaScript enabled, the reviewed exact finite-field successor is activated at this stable source reference.</small></figcaption></figure>

      <section class="monograph-section" id="central-bridge" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Chapter IV</p>
      ## The strong BSD ledger

      The rank statement is

      $$\operatorname{rank}E(\mathbb{Q})=\operatorname{ord}_{s=1}L(E,s).$$

      The strong form predicts the first nonzero Taylor coefficient as an arithmetic factorization. If $r=\operatorname{rank}E(\mathbb{Q})$ and $\operatorname{Sha}(E/\mathbb{Q})$ is finite, then under the displayed normalization,

      $$\frac{L^{(r)}(E,1)}{r!}=\frac{\Omega_E\,\operatorname{Reg}(E/\mathbb{Q})\,\#\operatorname{Sha}(E/\mathbb{Q})\,\prod_p c_p}{\#E(\mathbb{Q})_{\mathrm{tors}}^2}.$$

      The factors have different jobs. $\Omega_E$ is an archimedean period; the regulator measures the Mordell–Weil lattice; $c_p$ records bad-prime component data; torsion contributes a finite denominator; and $\operatorname{Sha}$ measures locally soluble torsors that may fail globally.

      <div class="warning-box"><strong>Three obligations, not one slogan</strong><p>Rank equality, finiteness of $\operatorname{Sha}$, and the normalized leading-term identity are logically distinct. Establishing one does not silently establish the others.</p></div>
      </section>

      <figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate IV"><img src="../../assets/documentaries/bsd/plate_overture.svg" width="1024" height="1536" loading="lazy" alt="A decorative ledger surrounds the leading-term formula with period, regulator, Tamagawa, torsion, and Tate–Shafarevich contributions."></button><figcaption><span class="plate-label">Plate IV</span><strong>The strong BSD ledger</strong><small>Fallback predecessor plate. With JavaScript enabled, the reviewed quantified dependency successor is activated at this stable source reference.</small></figcaption></figure>

      <section class="monograph-section" id="theorem-frontier" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Chapter V</p>
      ## The exact theorem frontier

      The frontier is governed by quantifiers and scope. Mordell–Weil finite generation and modularity hold for every elliptic curve over $\mathbb{Q}$. Through modularity, Gross–Zagier, and Kolyvagin, the established analytic rank zero or one terrain gives matching algebraic rank and finite $\operatorname{Sha}$.

      The higher-rank and universal leading-term frontier remains open: rank equality for every elliptic curve over $\mathbb{Q}$, general finiteness of $\operatorname{Sha}$, and the complete normalized complex leading-term formula.

      <div class="theorem-box"><strong>Established low-rank terrain</strong><p>Analytic rank $0$ or $1$ yields the matching Mordell–Weil rank and finite $\operatorname{Sha}$ for elliptic curves over $\mathbb{Q}$.</p></div>
      <div class="conjecture-box"><strong>Still open universally</strong><p>For every elliptic curve over $\mathbb{Q}$: equality of algebraic and analytic rank, finiteness of $\operatorname{Sha}$, and the complete complex leading-term formula.</p></div>
      </section>

      <figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate V"><img src="../../assets/documentaries/bsd/plate_frontier.svg" width="1024" height="1536" loading="lazy" alt="A map distinguishes established modularity and low-rank results from the unresolved higher-rank and universal leading-term frontier."></button><figcaption><span class="plate-label">Plate V</span><strong>Islands of theorem, ocean of conjecture</strong><small>Fallback predecessor plate. With JavaScript enabled, the reviewed quantified theorem-frontier successor is activated at this stable source reference.</small></figcaption></figure>

      <section class="monograph-section" id="appendix-curves" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Technical appendix A</p>
      ## Elliptic curves and the Mordell–Weil group

      For $E:y^2=x^3+Ax+B$, the discriminant is $\Delta=-16(4A^3+27B^2)\ne0$. The projective point $O=[0:1:0]$ is the identity.

      For distinct $P=(x_1,y_1)$ and $Q=(x_2,y_2)$ with $x_1\ne x_2$,

      $$m=\frac{y_2-y_1}{x_2-x_1},\qquad x_3=m^2-x_1-x_2,\qquad y_3=-y_1+m(x_1-x_3).$$

      Then $P+Q=(x_3,y_3)$. Associativity belongs to the algebraic-group structure; the chord picture alone is not its proof.

      For a basis $P_1,\ldots,P_r$ of the free part, the canonical height pairing gives

      $$\operatorname{Reg}(E/\mathbb{Q})=\det\bigl(\langle P_i,P_j\rangle\bigr),$$

      with empty determinant $1$ when $r=0$.
      </section>

      <section class="monograph-section" id="appendix-lfunction" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Technical appendix B</p>
      ## The $L$-function and analytic rank

      The Euler product converges absolutely initially for $\operatorname{Re}(s)>3/2$. Modularity identifies it with the $L$-series of a weight-two newform. A standard completed normalization is

      $$\Lambda(E,s)=N^{s/2}(2\pi)^{-s}\Gamma(s)L(E,s),$$

      satisfying $\Lambda(E,s)=w_E\Lambda(E,2-s)$. The analytic rank is

      $$r_{\mathrm{an}}(E)=\operatorname{ord}_{s=1}L(E,s).$$

      The root number gives $(-1)^{r_{\mathrm{an}}}=w_E$. This is analytic parity; it is not by itself algebraic rank equality.
      </section>

      <section class="monograph-section" id="appendix-strong" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Technical appendix C</p>
      ## The strong formula and normalization discipline

      Authors distribute real periods, archimedean factors, completed-function terms, and local conventions differently. A comparison must reconcile those conventions before comparing symbols or numbers.

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

      Descent converts an infinite search into finite covering and local-solubility problems and can give an upper bound on rank. The bound is sharp only after the relevant Tate–Shafarevich contribution is controlled.

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
      | Exact-object documentary plates | pedagogical | reproducible representation; never proof evidence |

      <div class="warning-box"><strong>Final claim boundary</strong><p>This web edition changes presentation, not theorem strength. It does not prove BSD, provide a new reduction, independently verify the complete literature, or make a novelty or priority claim.</p></div>
      </section>

      <section class="monograph-section" id="sources" data-reader-section markdown="1">
      <p class="monograph-section__eyebrow">Sources and programme crosswalk</p>
      ## Governing literature and campaign record

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
        <p>This browser edition uses exact-object-first visual pedagogy. The revised BSD plate sequence is bound to a Wolfram Language semantic master, deterministic static delivery assets, and the stable-source activation resolver.</p>
        <p>The web edition is derivative. The committed pointer is a source record; the checksum-locked complete illustrated source bundle is the authoritative source artifact. MathJax 3.2.2 is a version-pinned network enhancement, and the source TeX remains present when it is unavailable.</p>
        <p><strong>Web claim boundary:</strong> Browser-native, source-normalized exposition of rational points, the Mordell–Weil group, the Hasse–Weil L-function, low-rank theorem terrain, and the strong BSD formula. Numerical agreement, parity, Selmer bounds, family results, one-prime theorems, and p-adic analogues are not promoted to the universal complex conjecture.</p>
        <div class="monograph-actions"><a class="monograph-button" href="../bsd.edition.json">Web-edition data</a><a class="monograph-button" href="../documentary_web.schema.json">Reusable schema</a><a class="monograph-button" href="../sources/the_hidden_music_of_elliptic_curves.tex">Source record</a><a class="monograph-button" href="../ARTIFACT_MANIFEST.json">Artifact manifest</a></div>
        <dl class="edition-integrity"><div><dt>Rendered PDF</dt><dd>16,582,087 bytes · <code>36254378e11fd22a067944838341ae04fedbd13e5ea588180023874d7ba49ce9</code> · <code>metadata_only</code></dd></div><div><dt>Complete LaTeX source</dt><dd>50,500 bytes · <code>9b7b95702a5305c51e66e026d44ddf3003029808edb3009ed1b2fcbc92e6b2b4</code> · <code>metadata_only</code></dd></div><div><dt>Authoritative complete illustrated source bundle</dt><dd>16,995,210 bytes · <code>c0782575453227311630e17c443a4dea08091b3a3824bc23a1af17f5bd0d8377</code> · <code>metadata_only</code></dd></div></dl>
      </section>
    </article>
  </div>
</div>

<dialog class="monograph-lightbox" data-plate-dialog aria-labelledby="plate-dialog-title"><form method="dialog"><button class="monograph-lightbox__close" aria-label="Close plate view">Close</button></form><div class="monograph-lightbox__frame"><img data-plate-dialog-image alt=""><p id="plate-dialog-title" data-plate-dialog-caption></p></div></dialog>
<noscript><p>The manuscript and source TeX remain readable without JavaScript. The stable source references retain their reviewed predecessor plates; exact-object successors are activated by the BSD-specific resolver when JavaScript is available. Plate enlargement, rendered mathematics, reading progress, focus mode, and reading-position memory are unavailable; the checksum-locked PDF remains the rendered archival edition.</p></noscript>
</div>

<script defer src="../../javascripts/documentary-mathjax.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js" crossorigin="anonymous" referrerpolicy="no-referrer" data-archival-role="enhancement-only"></script>
<script defer src="../../assets/visual_pedagogy/bsd_exact/bsd_activation.js"></script>
<script defer src="../../javascripts/documentary.js"></script>
