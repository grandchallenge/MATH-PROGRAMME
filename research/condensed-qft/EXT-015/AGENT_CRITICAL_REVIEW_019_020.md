# EXT-015C — GCL mathematical critical adjudication 020

**Verdict:** ACCEPT the positive first-degree Ext comparison of [theorem 019](FIXED_SOURCE_EXT1_ISOMORPHISM_019.md) for its exact fixed-source and strict LF target hypotheses. This is a separate critical argument by GCL's mathematical review function, not a claim of an external referee, independent GitHub identity, or formal Lean certification.

**Protected source:** [MATH-PROGRAMME PR #2768](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2768), exact merged commit f8fe9566dbba1c24a8609b2e820d008dca528235.

## Audit I — the categorical relation presentation

For any profinite $S$ choose a surjective profinite cover $T\to S$ with $T$ extremally disconnected and let $R=T\times_ST$. The morphism $T\to S$ is an effective epimorphism in condensed sets: the pair $R\rightrightarrows T$ has coequalizer $S$. The free real liquid object on a profinite set is $\mathcal M_{<p}$, by Scholze's [Theorem 6.5](https://people.mpim-bonn.mpg.de/scholze/Analytic.pdf), printed page 35. Its extension to condensed sets is a left adjoint and preserves coequalizers.

Therefore $\mathcal M(R)\to\mathcal M(T)\to\mathcal M(S)\to0$ is right exact. The first morphism sends a relation pair to the difference of its two projections. The image $L$ is the kernel of the second map, and $\mathcal M(R)\twoheadrightarrow L$ is epic. Crucially, only $\mathcal M(T)$ is asserted projective: this follows because **$T$ is extremally disconnected**. Neither $\mathcal M(S)$, $\mathcal M(R)$ nor $L$ is silently assumed projective.

## Audit II — actual first Ext, not ordinary Hom masquerading as Ext

Let $E=\varinjlim_mE_m$ be a monomorphic strict LF output filtration, and suppose every map from a free liquid object on a compact profinite set to $E$ factors through one stage. The maps $\mathcal M(R)\to E$ and $\mathcal M(T)\to E$ then have finite output stage. For $f:L\to E$, precomposition along the epimorphism $\mathcal M(R)\twoheadrightarrow L$ has finite stage. Its image equals the image of $f$, so a monomorphic stage inclusion implies that $f$ itself factors through that stage.

Using the genuine short exact projective presentation $0\to L\to\mathcal M(T)\to\mathcal M(S)\to0$, first Ext is the cokernel of $\mathrm{Hom}(\mathcal M(T),E)\to\mathrm{Hom}(L,E)$. The factorization property proves **both** surjectivity of the filtered-stage first-Ext map and eventual annihilation of any class that becomes a boundary. The latter point precludes a hidden injectivity assumption.

For $E=\bigoplus_n\underline s$ with its finite Fréchet-summand stages, the hypothesis follows from compact-image boundedness in a regular strict LF space. Every kernel-pair space used is itself **profinite compact**. The conclusion is relative Ext-continuity in degree one, not an unjustified statement that all free liquid objects are derived compact.

## Audit III — countably directed source, including derived-limit residuals

Taroyan's liquid weight-stage representation, as recorded with exact caveats in [theorem 018](FIXED_SOURCE_WEIGHT_LOCALIZATION_018.md), gives a countably directed colimit of scaled objects $T_r$ isomorphic as liquid objects to retracts of $\mathcal M(\mathbb N\cup\{\infty\})$. Thus the first-Ext result of Audit II passes to each $T_r$ and implies

$$
\mathrm{Ext}^1(T_r,\bigoplus_n\underline s)
\cong\bigoplus_n\mathrm{Ext}^1(T_r,\underline s).
$$

For one global $\xi$, compatibility of its restrictions and countable direction force **one finite set of output coordinates** to contain all locally nonzero component classes. Subtract their corresponding global finite-coordinate classes. The residual then restricts to zero at every weight stage, but this does **not** automatically mean it is zero: it lies in a first derived inverse-limit edge. The countably directed subspace lemma of [018](FIXED_SOURCE_WEIGHT_LOCALIZATION_018.md) proves that this edge is itself a **direct sum of coordinate edges**, and the residual therefore also has finite coefficient support. This separately checks the potential lim-first obstruction instead of ignoring it.

Neither the Continuum Hypothesis nor scalar Ext vanishing is needed; a nonzero scalar Ext class under CH is compatible because it already occupies one coefficient.

## Audit IV — actual test-function output and counterexamples

The Valdivia–Vogt sequence-space representation cited in [018](FIXED_SOURCE_WEIGHT_LOCALIZATION_018.md) identifies the fixed compact-support Fréchet source with $s$ and the strict LF output $\mathcal D(\mathbb R)$ with a countable locally convex direct sum of copies of $s$. The established Fréchet-to-strict-LF factorization [LFO-013](../LFO3_SURJECTIVITY_THEOREM_013.md) works in both directions: each finite-summand source factors into a common compact-support output stage and each compact-support Fréchet output stage maps into a common finite summand prefix. Thus the two output filtrations have the same degree-one Ext image.

The non-Fréchet-source escaping extension in [017](SCALAR_PHANTOM_ESCAPE_017.md) remains valid: its source is not a nuclear Fréchet test-function stage. The theorem also makes no claim for arbitrary irregular LF output, varying test-function source supports, higher Ext degrees, complete quantum filtrations or differentiable Costello–Gwilliam cochains.

## Exact conclusion

Combining the new positive argument with injectivity admitted in [A/B review 016](AGENT_CRITICAL_REVIEW_AB_016.md), for every $0<p\le1$ the map

$$
\varinjlim_b
\mathrm{Ext}^1_{\mathrm{Liq}_p(\mathbb R)}
\left(\underline{\mathcal D_{[-1,1]}(\mathbb R)},
\underline{\mathcal D_{[-b,b]}(\mathbb R)}\right)
\longrightarrow
\mathrm{Ext}^1_{\mathrm{Liq}_p(\mathbb R)}
\left(\underline{\mathcal D_{[-1,1]}(\mathbb R)},
\underline{\mathcal D(\mathbb R)}\right)
$$

is an isomorphism under the precise published real-liquid realization hypotheses.

**GCL specialist critical verdict: ACCEPT.** The original fixed-source EXT-015C-positive-versus-negative question is resolved positively in degree one. The next genuine research obligation is EXT-015D, not another round of Human Steward review. Preserve the full proof chain 016–020 and do not inflate the claim into a complete derived QFT equivalence.
