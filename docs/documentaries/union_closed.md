<link rel="stylesheet" href="../../stylesheets/documentary.css">
<link rel="stylesheet" href="../../stylesheets/documentary-status.css">

<div class="gcl-monograph" data-gcl-reader="union_closed" data-edition="1.1.0">
<a class="monograph-skip" href="#monograph-start">Skip to the manuscript</a>
<header class="monograph-hero" aria-labelledby="monograph-title">
  <div class="monograph-hero__art" aria-hidden="true"><img src="../../assets/documentaries/union_closed/cover.svg" width="1024" height="1536" alt=""></div>
  <div class="monograph-hero__veil"></div>
  <div class="monograph-hero__copy">
    <p class="monograph-eyebrow">MATH-PROGRAMME · Documentary Treatment · Domain 01 · UC</p>
    <h1 id="monograph-title">The Element in Half the Worlds</h1>
    <p class="monograph-hero__subtitle">Frankl’s conjecture and the structure of union-closed families</p>
    <p class="monograph-hero__thesis">A family may close perfectly under union and still conceal the element that should appear in at least half its sets.</p>
    <div class="monograph-status" aria-label="Publication status"><span>Open conjecture</span><span>UC-DOC-WP01</span><span>No proof claimed</span></div>
    <div class="monograph-actions"><a class="monograph-button monograph-button--primary" href="#monograph-start">Enter the garden</a><a class="monograph-button" href="../">Documentary library</a><a class="monograph-button" href="../sources/the_element_in_half_the_worlds.tex">Source record</a></div>
  </div>
</header>
<div class="monograph-progress" aria-hidden="true"><span data-reader-progress-bar></span></div>
<div class="monograph-reader" id="monograph-start" tabindex="-1">
<nav class="monograph-toolbar" aria-label="Reader controls"><div class="monograph-toolbar__identity"><span>Digital Grand Challenge Library</span><strong>The Element in Half the Worlds</strong></div><div class="monograph-toolbar__controls"><button type="button" data-reader-focus aria-pressed="false">Focus mode</button><button type="button" data-reader-print>Print / save</button><button type="button" data-reader-reset>Reset position</button><output data-reader-progress aria-live="polite">0% read</output></div></nav>
<div class="monograph-layout">
<aside class="monograph-contents" aria-label="Manuscript contents">
<p class="monograph-contents__title">The journey</p><ol><li><a href="#reader-note">How to read</a></li><li><a href="#garden">The closing garden</a></li><li><a href="#half-way">The half-way balance</a></li><li><a href="#small-worlds">Exact small worlds</a></li><li><a href="#mirrors-lattices">Mirrors and lattices</a></li><li><a href="#average-size">Average-size door</a></li><li><a href="#entropy">Entropy bridge</a></li><li><a href="#theorem-frontier">Theorem frontier</a></li><li><a href="#certificate-forge">Certificate forge</a></li></ol>
<p class="monograph-contents__title">Technical appendix</p><ol><li><a href="#appendix-definitions">Definitions</a></li><li><a href="#appendix-elementary">Elementary spine</a></li><li><a href="#appendix-entropy">Entropy skeleton</a></li><li><a href="#appendix-lattice">Lattice notes</a></li><li><a href="#appendix-formal">Formal inventory</a></li><li><a href="#appendix-sources">Source audit</a></li><li><a href="#appendix-trust">Trust matrix</a></li><li><a href="#sources">Sources</a></li></ol>
</aside>
<article class="monograph-body" aria-label="The Element in Half the Worlds manuscript">
<section class="monograph-section" id="reader-note" data-reader-section markdown="1">
<p class="monograph-section__eyebrow">A note to the reader</p>
## Wonder first; the universal quantifier always visible

A finite family of sets can obey one simple closure law and still resist a universal abundance theorem. Frankl’s conjecture says that some element belongs to at least half of the sets in every finite nonempty union-closed family. It is an **Open conjecture**.

The plates are mnemonic maps, not proof diagrams. Definitions, exact quantifiers, theorem labels, finite-certificate scopes, source links, and the claim ledger govern the mathematics.

**Edition status:** Open conjecture; full-tier documentary exposition; no proof claim.

<div class="conjecture-box"><strong>Open conjecture · Frankl</strong><p>Let $\mathcal F$ be a finite nonempty union-closed family. Then there is an element $x\in\operatorname{supp}(\mathcal F)$ such that $2\operatorname{freq}_{\mathcal F}(x)\ge |\mathcal F|$.</p></div>
<div class="warning-box"><strong>Claim boundary</strong><p>This is a source-normalized illustrated documentary. It does not prove Frankl's conjecture, establish a new universal frequency bound, certify unreviewed proof claims, or make a novelty, priority, or public-release claim.</p></div>
</section>

<figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate I"><img src="../../assets/documentaries/union_closed/plate_garden.svg" width="1024" height="1536" loading="lazy" alt="A branching garden of finite sets flows upward to their pairwise unions, contrasting local closure with the global search for an abundant element."></button><figcaption><span class="plate-label">Plate I</span><strong>The Garden That Closes</strong><small>Pairwise union is local. The conjectured abundant element is a global witness.</small></figcaption></figure>
<section class="monograph-section" id="garden" data-reader-section markdown="1">
<p class="monograph-section__eyebrow">Chapter I</p>
## The garden that closes under union

A family $\mathcal F$ is union-closed when $A,B\in\mathcal F$ implies $A\cup B\in\mathcal F$.

<div class="definition-box"><strong>Definition</strong><p>The support is $\operatorname{supp}(\mathcal F)=\bigcup_{A\in\mathcal F}A$. The frequency of $x$ is $\operatorname{freq}_{\mathcal F}(x)=|\{A\in\mathcal F:x\in A\}|$.</p></div>

Closure describes what happens after choosing two members. Frankl’s statement asks for a single coordinate whose incidence count reaches half the entire family. The top union belongs to every finite nonempty union-closed family, but that alone does not identify an abundant element.
</section>

<figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate II"><img src="../../assets/documentaries/union_closed/plate_frequency.svg" width="1024" height="1536" loading="lazy" alt="A brass balance compares one element’s frequency with half the number of sets, above the incidence-counting identity linking all frequencies to total set size."></button><figcaption><span class="plate-label">Plate II</span><strong>The Half-Way Balance</strong><small>The threshold is sharp: powersets attain equality for every element.</small></figcaption></figure>
<section class="monograph-section" id="half-way" data-reader-section markdown="1">
<p class="monograph-section__eyebrow">Chapter II</p>
## The half-way balance

In the powerset $\mathcal P(U)$, each element occurs in exactly half the subsets. Thus no universal theorem can demand more than one half. Double-counting incidences gives

$$\sum_x\operatorname{freq}_{\mathcal F}(x)=\sum_{A\in\mathcal F}|A|.$$

<div class="theorem-box"><strong>Established elementary terrain</strong><p>Powersets attain the threshold sharply. A union-closed family containing a singleton $\{x\}$ satisfies Frankl for $x$ through the injection $A\mapsto A\cup\{x\}$ from sets missing $x$ to sets containing it.</p></div>

The identity controls an average. It does not force the maximum frequency to reach one half unless additional structure supplies the missing bridge.
</section>

<section class="monograph-section" id="small-worlds" data-reader-section markdown="1">
<p class="monograph-section__eyebrow">Chapter III</p>
## Small worlds, exact ledgers

For a universe of size $n$, exact enumeration can test union closure and every frequency profile. The programme’s independently replayed certificate finds no nontrivial counterexample for universes $n\le4$.

<div class="theorem-box"><strong>Exact bounded result</strong><p>The $n\le4$ statement is exact finite verification for those universes.</p></div>
<div class="warning-box"><strong>Bounded-computation guardrail</strong><p>Finite replay validates definitions, software, and bounded claims. It does not prove the conjecture for arbitrary finite universes.</p></div>
</section>

<figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate IV"><img src="../../assets/documentaries/union_closed/plate_lattice.svg" width="1024" height="1536" loading="lazy" alt="A finite join-semilattice rises from bottom to top through atoms, joins, and irreducible elements, illustrating the lattice formulation and deletion routes."></button><figcaption><span class="plate-label">Plate IV</span><strong>The Lattice Cathedral</strong><small>Set-family and lattice formulations require an explicit correspondence.</small></figcaption></figure>
<section class="monograph-section" id="mirrors-lattices" data-reader-section markdown="1">
<p class="monograph-section__eyebrow">Chapter IV</p>
## Mirrors, intersections, and lattices

Taking complements turns unions into intersections. Inclusion turns a union-closed family into a finite join-semilattice with $A\vee B=A\cup B$. These viewpoints reveal atoms, irreducibles, upper cones, deletion operations, and minimal-counterexample constraints.

<div class="theorem-box"><strong>Formal bounded terrain</strong><p>The programme records Lean-checked lattice theorems and hybrid packages through the governed Union-Closed theorem spine. Each result retains its precise hypotheses and certificate boundary.</p></div>
<div class="warning-box"><strong>Correspondence guardrail</strong><p>Order duality, complement duality, ideal-family averaging, and set-family frequency are related but not interchangeable without a complete translation theorem.</p></div>
</section>

<section class="monograph-section" id="average-size" data-reader-section markdown="1">
<p class="monograph-section__eyebrow">Chapter V</p>
## The average-size door

Reimer’s theorem gives a lower bound on the average size of members of a union-closed family. Combined with incidence double-counting, it guarantees some element with nontrivial frequency, but the support-size denominator prevents the argument from reaching the universal half threshold.

<div class="imported-box"><strong>Imported established theorem · Reimer</strong><p>The exact source statement controls this edition. The theorem is a major structural constraint, not a proof of Frankl’s conjecture.</p></div>
</section>

<figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate III"><img src="../../assets/documentaries/union_closed/plate_entropy.svg" width="1024" height="1536" loading="lazy" alt="A uniform random set passes through coordinate entropies and coupled unions to a dimension-free constant lower bound that still falls short of one half."></button><figcaption><span class="plate-label">Plate III</span><strong>The Entropy Bridge</strong><small>Dimension-free positive constants are breakthroughs; they remain below one half.</small></figcaption></figure>
<section class="monograph-section" id="entropy" data-reader-section markdown="1">
<p class="monograph-section__eyebrow">Chapter VI</p>
## Entropy enters the garden

Choose a uniform random member $A\in\mathcal F$ and write its membership indicators as coordinates. Entropy decomposes the uncertainty of the random set, while coupled copies and union closure create inequalities among the coordinate marginals.

<div class="imported-box"><strong>Imported theorem terrain</strong><p>Gilmer established the first dimension-free positive constant; Sawin, Yu, Cambie, Alweiss–Huang–Sellke, Liu, and others refined the entropy and coupling landscape. Exact constants and assumptions remain source-specific.</p></div>
<div class="warning-box"><strong>Entropy guardrail</strong><p>A positive constant below one half, a numerically optimized coupling, or a barrier for one entropy ansatz does not settle the universal conjecture.</p></div>
</section>

<figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate VI"><img src="../../assets/documentaries/union_closed/plate_frontier.svg" width="1024" height="1536" loading="lazy" alt="Islands representing special families, rigorous constant bounds, and formal lattice results approach but do not reach the open one-half threshold."></button><figcaption><span class="plate-label">Plate VI</span><strong>Islands of Theorem</strong><small>The frontier advances without erasing the open boundary.</small></figcaption></figure>
<section class="monograph-section" id="theorem-frontier" data-reader-section markdown="1">
<p class="monograph-section__eyebrow">Chapter VII</p>
## The theorem frontier

Known terrain includes elementary families, bounded exact verification, average-size inequalities, rigorous dimension-free constants, structural restrictions on minimal counterexamples, and formalized lattice results.

<div class="conjecture-box"><strong>Still open universally</strong><p>No admitted result proves that every finite nonempty union-closed family has an element in at least half its sets.</p></div>

Recent posted proof claims remain current-awareness entries until their theorem statements, dependencies, and complete proofs are independently audited. Repository merge, citation count, or public attention does not change mathematical status.
</section>

<figure class="monograph-plate" data-plate><button type="button" data-plate-open aria-label="Enlarge Plate V"><img src="../../assets/documentaries/union_closed/plate_certificate.svg" width="1024" height="1536" loading="lazy" alt="A formal forge separates exact finite replay, Lean theorems, imported results, hybrid packages, source audits, and the universal conjecture’s claim boundary."></button><figcaption><span class="plate-label">Plate V</span><strong>The Certificate Forge</strong><small>A certificate proves only the claim encoded by its contract.</small></figcaption></figure>
<section class="monograph-section" id="certificate-forge" data-reader-section markdown="1">
<p class="monograph-section__eyebrow">Chapter VIII</p>
## The certificate forge

The programme separates human proof, imported theorem, Lean theorem, exact finite replay, numerical evidence, and hybrid certificate. A hybrid package may combine a formal transfer theorem with an independently replayed finite fact, but its public claim must expose both components.

<div class="theorem-box"><strong>Certification discipline</strong><p>Lean checks encoded terms under explicit imports. Exact replay checks a declared finite search space. Neither silently verifies source correspondence or an unbounded theorem.</p></div>
<div class="warning-box"><strong>No promotion by proximity</strong><p>Many correct restricted results surrounding an open conjecture do not add up to a proof unless a complete logical bridge is supplied.</p></div>
</section>

<section class="monograph-section" id="appendix-definitions" data-reader-section markdown="1"><p class="monograph-section__eyebrow">Technical appendix A</p>
## Precise definitions and normalizations

For finite $\mathcal F\subseteq\mathcal P(U)$, define $\operatorname{supp}(\mathcal F)=\bigcup\mathcal F$ and $\operatorname{freq}_{\mathcal F}(x)=|\{A\in\mathcal F:x\in A\}|$. An element is abundant when $2\operatorname{freq}_{\mathcal F}(x)\ge|\mathcal F|$. The canonical target excludes the empty family and reduces the ground set to the support.
</section>
<section class="monograph-section" id="appendix-elementary" data-reader-section markdown="1"><p class="monograph-section__eyebrow">Technical appendix B</p>
## Elementary proof spine

The top union belongs to the family by finite repeated closure. Powerset sharpness follows by toggling a chosen coordinate. The singleton theorem uses the injective map $A\mapsto A\cup\{x\}$. These are complete arguments within their scopes and suitable for direct formalization.
</section>
<section class="monograph-section" id="appendix-entropy" data-reader-section markdown="1"><p class="monograph-section__eyebrow">Technical appendix C</p>
## Entropy method skeleton

For membership indicators $(X_x)_x$, $H(A)=H((X_x)_x)\le\sum_x H(X_x)$. Coupled copies are combined through union closure. Assuming all marginals lie below a selected threshold, one seeks an entropy contradiction. The coupling, concavity estimates, and optimization domain are theorem-bearing details.
</section>
<section class="monograph-section" id="appendix-lattice" data-reader-section markdown="1"><p class="monograph-section__eyebrow">Technical appendix D</p>
## Lattice correspondence notes

Inclusion supplies a finite join-semilattice. Upper cones and irreducible elements can encode frequency-like data. Translation obligations include separation, the ground-set representation, internal versus ambient lattices, and the exact relation between lattice elements and set coordinates.
</section>
<section class="monograph-section" id="appendix-formal" data-reader-section markdown="1"><p class="monograph-section__eyebrow">Technical appendix E</p>
## Formal and computational inventory

| Artifact class | Supports | Does not support |
|---|---|---|
| Lean theorem | Encoded theorem under imports | Unencoded source correspondence |
| Exact finite certificate | Declared finite search | Arbitrary universes |
| Hybrid package | Explicit components and bridge | A stronger unstated theorem |
| Numerical optimization | Candidates and diagnostics | Rigorous universal bounds |
</section>
<section class="monograph-section" id="appendix-sources" data-reader-section markdown="1"><p class="monograph-section__eyebrow">Technical appendix F</p>
## Source audit ledger

Reimer’s theorem and the post-2022 entropy results are literature-derived imports. Programme lattice claims are governed by Domain 01 and their individual formal or hybrid records. Recent proof claims remain `NEEDS_AUDIT` until complete independent review.

<div class="imported-box"><strong>Imported-source discipline</strong><p>A bibliography identifies provenance. It does not replace theorem-body verification, normalization checks, or proof.</p></div>
</section>
<section class="monograph-section" id="appendix-trust" data-reader-section markdown="1"><p class="monograph-section__eyebrow">Technical appendix G</p>
## Claim-level trust matrix

| Claim | Trust class | Qualification |
|---|---|---|
| Frankl’s half-frequency statement | open | no admitted proof |
| Top union, powerset, singleton injection | established | elementary proofs |
| No nontrivial counterexample for $n\le4$ | exact finite verification | bounded universe |
| Reimer average-size theorem | imported established | source statement governs |
| Dimension-free constant bounds | imported established | constants and hypotheses are source-specific |
| Programme lattice results | formal or hybrid bounded | individual records govern |
| 2026 posted proof claims | needs audit | not promoted here |
| SVG plates | pedagogical | never proof authority |

<div class="warning-box"><strong>Final claim boundary</strong><p>This web edition changes presentation and collection membership, not theorem strength. Frankl’s conjecture remains open, and no interaction, plate, bounded replay, or formal special case supplies the missing universal proof.</p></div>
</section>
<section class="monograph-section" id="sources" data-reader-section markdown="1"><p class="monograph-section__eyebrow">Sources and programme crosswalk</p>
## Governing literature and campaign record

<div class="bibliography">
<p>David Reimer, <a href="https://doi.org/10.1017/S0963548302005230">“An Average Set Size Theorem”</a>.</p>
<p>Justin Gilmer, <a href="https://arxiv.org/abs/2211.09055">“A constant lower bound for the union-closed sets conjecture”</a>.</p>
<p>Will Sawin, <a href="https://arxiv.org/abs/2211.11504">“An improved lower bound for the union-closed set conjecture”</a>.</p>
<p>Lei Yu, <a href="https://arxiv.org/abs/2212.00658">“Dimension-Free Bounds for the Union-Closed Sets Conjecture”</a>.</p>
<p>Stijn Cambie, <a href="https://arxiv.org/abs/2212.12500">“Better bounds … using the entropy approach”</a>.</p>
<p>Ryan Alweiss, Bo’az Huang, and Mark Sellke, <a href="https://doi.org/10.37236/12232">“Improved Lower Bound for Frankl’s Union-Closed Sets Conjecture”</a>.</p>
<p>Jingbo Liu, <a href="https://arxiv.org/abs/2306.08824">“Improving the Lower Bound … via Conditionally IID Coupling”</a>.</p>
<p>Antoine Bouchard, <a href="https://arxiv.org/abs/2503.00277">lattice formulation work</a>.</p>
<p>Masahiro Hachimori and Kenji Kashiwabara, <a href="https://arxiv.org/abs/2504.13454">ideal-family work with Lean 4 formal proof</a>.</p>
</div>

Programme links: [Domain 01](../../domains/union_closed/) · [canonical master plan](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/DOMAIN_01_UNION_CLOSED_MASTER_PLAN.md) · [UC-DOC-WP00 source lock](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/union_closed/UC_DOC_WP00_DOCUMENTARY_SOURCE_LOCK) · [UC-DOC-WP01 admission](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/union_closed/UC_DOC_WP01_WEB_ADMISSION) · [review records](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/reviews/union_closed)
</section>
<section class="monograph-colophon" aria-labelledby="edition-record-title"><h2 id="edition-record-title">Edition record</h2><p>This is the first Wave Two admission and the first non-Millennium full-tier edition. It exercises the shared reader against finite combinatorics, exact enumeration, formal proof artifacts, hybrid certificates, and active source-audit obligations.</p><p>The web edition is derivative. The committed pointer is a source record; the checksum-locked complete illustrated source bundle is the authoritative source artifact. MathJax 3.2.2 is a version-pinned network enhancement, and the source TeX remains present when it is unavailable.</p><p><strong>Web claim boundary:</strong> This is a source-normalized illustrated documentary. It does not prove Frankl's conjecture, establish a new universal frequency bound, certify unreviewed proof claims, or make a novelty, priority, or public-release claim.</p><div class="monograph-actions"><a class="monograph-button" href="../union_closed.edition.json">Web-edition data</a><a class="monograph-button" href="../documentary_web.schema.json">Reusable schema</a><a class="monograph-button" href="../sources/the_element_in_half_the_worlds.tex">Source record</a><a class="monograph-button" href="../ARTIFACT_MANIFEST.json">Artifact manifest</a></div><dl class="edition-integrity"><div><dt>Rendered PDF</dt><dd>3,343,773 bytes · <code>6ea03bef444f19ae8013e80c76a5112fda9c6b740d61387c2bfeea5921ac71dc</code> · <code>metadata_only</code></dd></div><div><dt>Complete LaTeX source</dt><dd>50,548 bytes · <code>e889079fc77163e57b0c239e8f25ae29a3ded640b32120f65d1f3708c05dfdde</code> · <code>metadata_only</code></dd></div><div><dt>Authoritative complete illustrated source bundle</dt><dd>3,100,936 bytes · <code>3a1fcf16dee92c6bbf5fd8285702e31c828aa6d1666e5605e8981346f4bd2daf</code> · <code>metadata_only</code></dd></div></dl></section>
</article></div></div>
<dialog class="monograph-lightbox" data-plate-dialog aria-labelledby="plate-dialog-title"><form method="dialog"><button class="monograph-lightbox__close" aria-label="Close plate view">Close</button></form><div class="monograph-lightbox__frame"><img data-plate-dialog-image alt=""><p id="plate-dialog-title" data-plate-dialog-caption></p></div></dialog>
<noscript><p>The manuscript and source TeX remain readable without JavaScript. Plate enlargement, rendered mathematics, reading progress, focus mode, and reading-position memory are unavailable; the checksum-locked PDF remains the rendered archival edition.</p></noscript>
</div>
<script defer src="../../javascripts/documentary-mathjax.js"></script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js" crossorigin="anonymous" referrerpolicy="no-referrer" data-archival-role="enhancement-only"></script><script defer src="../../javascripts/documentary.js"></script>
