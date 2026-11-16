# EXT-015 REACH / 195 — zero-width Gaussian source integral and the original completed-stage boundary

**Primary mathematical disposition: BOUNDED POSITIVE SOURCE APPROXIMATION WITH AN EXACT FIXED-STAGE NONCONVERGENCE OBSTRUCTION.** The nonrapid joint Green defect can be expressed as an improper continuum integral of *genuine* finite legal Gaussian source histories. Every fixed positive lower-width truncation is itself a complete admitted original 108.7 source. Nevertheless no fixed anchored-scalar complete source stage with the original independent pure-anchor R1 input can contain the zero-width limit: the evaluated limit has a physical cusp for every positive regulator whereas that fixed stage evaluates smoothly. Each fixed positive-width truncation also leaves a nonrapid error, even though the family converges in ordinary distributions as its lower width tends to zero. This is not a nonmembership theorem for arbitrary original 108.7 histories, and not a proof of universal Lemma150.L or residual W acyclicity.

## 1. Source lock, question and scope

Use the protected original scalar Gaussian/Wick source105 (Git blob a8ce66ff0edec33e2aff299550fca2089d671033), original completed mixed source108 (587c15fd6e24f6e6b14de574ff878221cdbd5cb6), original source-controlled parameter rows126 (5b05c6147d237ca1d22e4dcbce9262b0f038c163), first Green source reduction165 (24b82716d41d309438fcb7a97bbacab0b724afde), legal second-arm168 (e2c43f218c9175b919c51f371acb8c04e659faea), and the protected nonpolynomial Gaussian anchored-source construction NONPOLYNOMIAL_GAUSSIAN_SOURCE_AUDIT_186.md in PR3355 (protected merge f71362ef0fba3a3b73d023a63f74efc3651b2bc3). The separately admitted DOUBLE_GAUSSIAN_HIDDEN_MEAN_SOURCE_186.md is a different supplemental mathematical manuscript: PR3352 merge 3dc09319b417272b3c1ec35b74e2bb30392e5c31 and source blob 7985fec06cb3134110b16afa4aa4fc5b71444341. Its DG-186B critic and ledger are protected in PR3354 merge 51aecf3d1d42a41127ef1b5e890dafb8e16d232f; this work does not reuse the numbered canonical 186–191 slots.

The **protected** zero-energy audit [192](ZERO_ENERGY_SOURCE_MECHANISM_AUDIT_192.md), exact frozen blob 6003987b03980ae65ead3e286109be1eed02c8c7, identifies a legal Wick-smoothed core and a residual defect. The source-locked logical review193 and ledger194 passed native protected admission in PR3360, merge `ff1f71ff5686a4adcac659bd6e6e817a77139666`; the actual protected review193 blob is `39873b26b2b1e9085d77cdb0964658ef7bd6b69d` after a reconciled supplemental reviewer record, and ledger194 was admitted at `feb36d49385f004ef197fcdc79ae98697f5fa876`. The current programme checkpoint is nonterminal CP210 after PR3363. The identities below are independently derived from protected105/108 and elementary heat convolution, not inferred from administrative admission.

Fix $e(x)=|x|/2$, smooth compact cutoffs $\chi,\rho$ with $\chi=1$ near0 and $\rho(0)\ne0$, and normalized Gaussian $\kappa_\sigma(t)=\sigma^{-1}(2\pi)^{-1/2}\exp(-t^2/(2\sigma^2))$. For fixed $b>0$, define

$$
P_\sigma=e*\kappa_\sigma,\qquad
A_\epsilon(x,z)=\chi(x)e(x)\rho(z)\kappa_\epsilon(z),
\qquad
D^{(b)}_\epsilon(x,z)=
\chi(x)\bigl[P_{b\epsilon}(x)-e(x)\bigr]
\rho(z)\kappa_\epsilon(z).
\tag{195.1}
$$

The original source membership of $A$ is equivalent to that of $D^{(b)}$ because the companion $\chi P_{b\epsilon}\rho\kappa_\epsilon$ is itself an admitted original hidden-anchor Wick source. This equivalence is asserted at exact positive-regulator evaluation and for existence of a representative modulo the unchanged rapid ideal; it does not decide either membership question.

## 2. Every positive Gaussian-width component is a genuine legal original source

For each fixed $a>0$ and positive regulator, introduce one hidden physical vertex $h$ and original R1 coefficient $\eta(h)\delta_0(h)$, extended by fixed compact smooth cutoffs in the independent retained coordinates $(x,z)$. Its wavefront has only an $h$ covector; no forbidden nonzero partial-partition conormal can have this pure covector, since every collision block has zero conormal covector sum. Attach the two original scalar Gaussian edges

$$
\kappa_{a\epsilon}(x-h),\qquad
\kappa_\epsilon(z-h)
\tag{195.2}
$$

with true physical densities, a fixed compact output multiplier $\chi(x)\rho(z)$, and scalar Laurent factor $a\epsilon^2$. After proper forgetting of $h$ the evaluated source is exactly

$$
H^{(a)}_\epsilon(x,z)=
a\epsilon^2\chi(x)\rho(z)
\kappa_{a\epsilon}(x)\kappa_\epsilon(z).
\tag{195.3}
$$

There is no missing Jacobian in pairing against the anchored delta. At fixed $a>0$, both edges are admitted Gaussian scalar105 stages, their product and scalar Laurent shift have one fixed all-corner polyhomogeneous index family and auxiliary weights, and the original R1 input is permitted. Thus (195.3) is a **genuine finite simple-tensor complete 108.7 source**, with finite graph, proper supports and legitimate126 parameter derivatives. Its source-stage constants may depend on $a$; no uniform source-stage estimate as $a\downarrow0$ is asserted.

The Wick analogue

$$
\widetilde A^{(a)}_\epsilon(x,z)
=\chi(x)P_{a\epsilon}(x)\rho(z)\kappa_\epsilon(z)
\tag{195.4}
$$

is also a complete original source for **each fixed positive** $a$, replacing the first Gaussian edge in (195.2) by the admitted relative Wick factor $P_{a\epsilon}(x-h)$, then evaluating at $h=0$. Positive scale rescaling, fixed scalar stage bounds and the same R1/proper-density/126 checks apply. This is precisely the legal *anchored scalar* channel, not an arbitrary allowed R1 coefficient after forgetting.

## 3. The defect as an improper integral over admitted sources

For $P_\sigma=e*\kappa_\sigma$, the heat equation and $e''=\delta_0$ give

$$
\frac{\partial P_\sigma}{\partial\sigma}
=\sigma\partial_x^2P_\sigma
=\sigma\kappa_\sigma.
\tag{195.5}
$$

At fixed $\epsilon>0$, replacing $\sigma=a\epsilon$ gives

$$
\frac{\partial}{\partial a}P_{a\epsilon}(x)
=a\epsilon^2\kappa_{a\epsilon}(x).
\tag{195.6}
$$

Since $P_{a\epsilon}\to e$ as $a\downarrow0$ in distributions, we obtain the exact **improper distributional integral**

$$
D^{(b)}_\epsilon(x,z)
=\int_0^b H^{(a)}_\epsilon(x,z)\,da.
\tag{195.7}
$$

The limit is in the ordinary distribution topology at each fixed positive regulator and on compact positive-regulator intervals, **not** in an asserted original completed source stage. Each integrand of (195.7) is legal by section2. An uncountable integral of such histories is not itself one of the finite 108.7 source expressions merely because all its pointwise summands are legal.

For any fixed lower width $0<d<b$, use the legal Wick sources (195.4) to form the finite *two-term* legal source

$$
D^{[d,b]}_\epsilon
=\widetilde A^{(b)}_\epsilon
-\widetilde A^{(d)}_\epsilon
=\int_d^b H^{(a)}_\epsilon\,da
=\chi(x)\rho(z)\kappa_\epsilon(z)
\bigl[P_{b\epsilon}(x)-P_{d\epsilon}(x)\bigr].
\tag{195.8}
$$

No integral over source stages is needed to establish admission of (195.8): it is simply the difference of two explicitly typed finite original108 histories. For each $d>0$ its scalar source has a fixed stage and all compatible126 rows. Thus $D^{[d,b]}_\epsilon$ converges to $D^{(b)}_\epsilon$ as $d\downarrow0$ in ordinary distributions, but that fact alone does **not** establish completed source membership of its limit.

## 4. Every fixed positive-width truncation misses a nonrapid class

The exact residual is

$$
D^{(b)}_\epsilon-D^{[d,b]}_\epsilon
=\chi(x)\bigl[P_{d\epsilon}(x)-e(x)\bigr]
\rho(z)\kappa_\epsilon(z).
\tag{195.9}
$$

The heat equation also yields

$$
P_\sigma-e=
\int_0^{\sigma^2/2}\kappa_{\sqrt{2t}}\,dt,
\qquad
\int_{\mathbb R}(P_\sigma-e)(x)\,dx=\sigma^2/2.
\tag{195.10}
$$

Choose a fixed compact smooth test $\phi(x)\zeta(z)$, each equal to one near zero, with $\phi$ supported where $\chi=1$ near the anchor. Gaussian tail estimates on the region where $\phi\chi\ne1$, and ordinary even Gaussian test moments in $z$, show

$$
\left\langle D^{(b)}_\epsilon-D^{[d,b]}_\epsilon,
\phi\otimes\zeta\right\rangle
=\frac{d^2}{2}\rho(0)\epsilon^2+O(\epsilon^4)
\quad(\epsilon\downarrow0).
\tag{195.11}
$$

For each fixed $d>0$, the coefficient is nonzero. A family in the original108 fixed-order uniform rapid ideal has pairing $O(\epsilon^L)$ for every $L$ against this fixed test. Therefore **no fixed positive lower width $d$ yields even a rapid-equivalent representative of the defect**. Passing to $d\downarrow0$ after fixing the regulator cannot be substituted for the required uniform rapid ideal or source-stage completion.

## 5. An exact obstruction to fixed-stage anchored scalar completion

The crucial point is not merely that the scalar-stage seminorm bounds might deteriorate: the evaluated limit fails an elementary interior smoothness condition.

For every fixed $\epsilon>0$, $P_{b\epsilon}$ is smooth in $x$, while $e(x)=|x|/2$ has derivative jump one at zero. Since $\chi=1$ near the anchor,

$$
\Bigl[\partial_xD^{(b)}_\epsilon(0^+,z)
-\partial_xD^{(b)}_\epsilon(0^-,z)\Bigr]
=-\rho(z)\kappa_\epsilon(z)\ne0.
\tag{195.12}
$$

Thus $D^{(b)}_\epsilon$ is **not $C^1$ in $x$ at $x=0$**, for any positive regulator. In contrast, every fixed-stage anchored-scalar source with original R1 coefficient $\eta(h)\delta_0(h)$ and completed smooth scalar105 coefficients evaluates, after pairing the delta in $h$, to a smooth function of the retained coordinates at every fixed positive regulator. Its source map into interior $C^\infty$ is continuous in the stated complete scalar-stage topology: fixed-regulator $C^r$ bounds on the restricted scalar coefficient are among the complete-stage seminorms. The continuous linear evaluation extends through the completed projective tensor product with this fixed R1 coefficient.

**Proposition195.1 (anchored scalar channel not closed under the improper zero-width integral).** The exact limit (195.7) is not the image of any single source element in this fixed anchored-scalar channel. In particular the family of legal finite sources (195.8) does not converge to such a source in any fixed completed scalar stage whose positive-regulator evaluation is continuous into interior $C^1$.

There is a quantitative manifestation of the failure. With $\chi=1$ near zero,

$$
\partial_x^2
\bigl[P_{b\epsilon}(x)-P_{d\epsilon}(x)\bigr]_{x=0}
=\kappa_{b\epsilon}(0)-\kappa_{d\epsilon}(0)
=\frac{1}{\sqrt{2\pi}\epsilon}
\left(\frac1b-\frac1d\right).
\tag{195.13}
$$

For fixed $\epsilon>0$ this diverges as $d\downarrow0$. It rules out uniform interior $C^2$ bounds even before the loss of $C^1$ regularity in the limit. This is an exact **source-stage continuity obstruction** for the displayed anchored-scalar presentations, not merely a weak boundary heuristic.

The proposition deliberately does **not** assert that the full original 108 image consists only of such smooth anchored outputs. Original 108 also admits singular R1 coefficients and legal partition jets, which can create nonsmooth positive-regulator distributions. An alternative finite completed history could in principle represent $D^{(b)}$, and its membership remains OPEN. Nor does the above exclude a specially constructed rapidly equivalent family in some genuinely different legal fixed complete stage; (195.11) rejects only every **fixed positive** lower-width truncation.

## 6. Source boundaries and scientific next step

| Mathematical question | Bounded status |
| --- | --- |
| Each fixed positive Gaussian width component of the defect is a legal original finite 108 source | CONSTRUCTED |
| Each fixed positive lower-width truncated defect is a legal complete source | CONSTRUCTED as two genuine Wick histories |
| The improper width integral converges as an ordinary distribution | EXACT by the heat equation |
| A fixed positive lower-width truncated source is rapid-equivalent to the defect | NO, by nonzero order-two fixed-test coefficient |
| The zero-width integral converges in the same anchored-scalar complete source stage | NO, by explicit positive-interior cusp/C-smoothness and divergent derivative seminorm |
| Another legal original R1/partition/completed source might represent the defect | OPEN |
| Full first-core A membership, universal150.L, residual W acyclicity, originalR3, full126.14, higher weights, lifting, M5/R4 | OPEN |

The valid next question is **not** whether all components of the integral are sources; they are. It is whether original108 has an *alternative finite source history* in which the defect's joint-corner cusp is carried by a genuinely permitted R1 coefficient or nonidentity partition jet **without** the illegal independent anchor, with one fixed scalar index/auxiliary-weight stage, proper densities and126 parameter rows. Equivalently, a negative proof must establish an all-history obstruction that does not mistake weak source limits for completed source-stage limits.

This bounded research195 was initiated before upstream192–194 admission; upstream is now protected via PR3360 and CP210. The primary195 must receive an exact-source-locked critical review, bounded acceptance, native protected checks and final source readback before it can be recorded as admitted. The separately documented same-system logical reviewer is not external mathematical certification.
