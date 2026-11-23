# EXT-015 REACH / UC043 — two-slot family recovery through compact history quotients

**Disposition.** On the original two-slot sources, local boundedness in each seminorm of the entire-history quotient suffices for exact coefficient rows. A single loss in scalar auxiliary weights and finite losses in the R1 Sobolev orders give the needed compact transitions, including through the completed mixed tensors and the actual evaluation kernels. The argument leaves one inference open. An arbitrary family in the prior retained rule still needs these quotient bounds, possibly after a uniform mixed-jet rapid correction.

## 1. Original domain and recovery data

CP270 bound this attempt to protected input aa3ea5cddbb12f3525bac2711ae19e0be7133f96. Work on a nonempty physical interval $U$ and one real parameter interval $V_0$. Use the two labelled output slots, coefficient singleton and one fixed positive regulator interval. A finite geometric history can have any finite number of internal vertices and any of the original support, cone, scalar, partition-jet, proper projection and density data. Finite slot symmetrization, when required, uses the same finite joins and averaging as 126.

| Input | Git blob at the protected cut |
| --- | --- |
| [Scalar stages 105 §8](GAUSSIAN_WICK_COLLISION_NORMAL_FORM_105.md) | a8ce66ff0edec33e2aff299550fca2089d671033 |
| [Mixed domain and parameters 108 §§2–4, 8](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md) | 587c15fd6e24f6e6b14de574ff878221cdbd5cb6 |
| [Retained family rule 117 §7](R1_WICK_DRESSED_QUANTUM_COMPARISON_117.md) | e95b1155ebb2018a80d2dc559560730fd7ea6594 |
| [Evaluation obstruction 120](PARAMETER_EVALUATION_CONNECTION_DESCENT_120.md) | 89f910e1d04d82da3f45d00c4ac7bb3ad0fbad13 |
| [Prior retained sheaf 123 §§2, 4.1](RETAINED_FAMILY_DIFFERENTIABLE_LIQUID_AUDIT_123.md) | c5195a38414e3b45dbf75bb89b0db055ce01a5a2 |
| [Coefficient rows and recovery 126 §§2–4, 9](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md) | 5b05c6147d237ca1d22e4dcbce9262b0f038c163 |
| [Compactness route 138 §5](REACH_M5_REMAINING_CONTRACT_AUDIT_138.md) | de621fb8f1ddd384c2ed0fce5f542068517e69cd |

The data are the complete evaluated positive-regulator family and its actual compatible jets. The recovery target is a local original source-controlled representative of its class, up to the uniform rapid relation on every mixed jet. Exact equality of evaluated histories already identifies different coefficient representations. Neither source kernels nor that rapid relation justify recovering a unique coefficient tensor. Point evaluation on the parameter chart can lose even a derivative of a nonzero class, as in 120. That example itself has a smooth lift to one original fixed source, so it supplies no negative instance of (126.14).

For one finite history $h$, retain the notation of (126.2)–(126.3) and put

$$
Y_{h,s}=H_{h,s}/\ker(e_{h,s}),\qquad
H_{h,s}=\bigoplus_{\nu\in h} E_{s_\nu,K_\nu,\Gamma_\nu}
  \widehat\otimes_\pi S_{\lambda_\nu}.
\tag{UC043.1}
$$

Each $Y_{h,s}$ is a Fréchet quotient by a closed linear subspace. It identifies with the image as a vector space of distributions in the regulator and two physical variables. We use its quotient topology and the induced continuous injection into the distribution envelope.

## 2. Compactness through the actual complete history quotients

**Proposition UC043.1.** Increase each R1 order $s_\nu$ by one. In each scalar stage lower the auxiliary remainder weights by one at every recursive stage, using the same support, face index families and truncation rules. Denote the resulting history stage by $H^+_{h,s}$ and its actual evaluation quotient by $Y^+_{h,s}$. For every continuous seminorm on $H^+_{h,s}$ there is a continuous seminorm on $H_{h,s}$ whose unit ball maps to a totally bounded set for the target seminorm. The corresponding assertion holds for $Y_{h,s}\to Y^+_{h,s}$, which in particular takes any bounded set to a relatively compact set.

**Proof.** For the R1 graph factor take the same properly supported cutoffs $A_j$ in (108.1). The base target norm $H^{-s_\nu-1}$ has a compact inclusion from $H^{-s_\nu}_{K_\nu}$. Each target seminorm $\|A_j u\|_m$ has relatively compact image under the source bound $\|A_j u\|_{m+1}$. Proper support keeps the images of the fixed compact $K_\nu$ in a fixed compact for each $j$. These claims are the compact-support Sobolev inclusions, obtained by localization to a box and Fourier series with a tail bounded by the inverse of the frequency cutoff. For a finite maximum of target requests use the maximum of the finitely many source bounds and take total boundedness in their finite product.

For the scalar factor work in the finite compact corner atlas and in the recursive coefficient spaces of 105.5. Normalize the face defining functions to take values at most one on the relevant chart. Interior smooth seminorms have the asserted property by bounding one additional derivative on a slightly larger compact set. Proceed by induction on face dimension for the coefficient seminorms. For a given target face remainder request of depth $D$ and b-derivative order at most $m$, take a truncation at a strictly greater depth $D'$. The remainder at depth $D$ is the deeper remainder plus finitely many intervening terms. Use the same collar extensions as in the scalar stage. Depths may be chosen between powers, or with all the terms at an included power removed according to the stage's truncation convention. The intervening terms, weighted as in the target, are continuous images of a finite collection of target coefficient seminorms on the face. Indeed their normal powers and logarithms, after weighting at depth $D$ and taking the prescribed b-derivatives, have bounded normal factors. Tangential derivatives and the auxiliary weights use precisely the corresponding lower-dimensional coefficient seminorms. The inductive compactness assertion handles those terms.

For the deeper remainder, write $r_H$ for the distinguished face variable and $r_G$ for the other face variables on the corner patch. A source bound on the remainder at depth $D'$ in derivatives through $m+1$ bounds its target weighted derivatives at depth $D$, through $m$, by a constant times

$$
r_H^{D'-D}\prod_{G\ne H}r_G.
\tag{UC043.2}
$$

Thus these weighted functions are uniformly small near any participating boundary of the patch. Away from the boundary the same source bound controls an additional ordinary derivative. Arzelà–Ascoli on the compact truncated patch, followed by the uniform bound on the omitted boundary neighborhoods, gives total boundedness in the specified target remainder seminorm. The argument applies on compact exhaustions wherever an interior seminorm is used and inductively at every recursive coefficient request. Finite sums and maxima preserve the assertion. Completeness and the compatibility of the actual functions and their records are those of 105.5. The inclusion only relaxes bounds on remainders. All scalar indices and actual evaluations are preserved.

For a target projective seminorm from a pair of target factor seminorms, choose the two stronger source seminorms just constructed. Pass to the corresponding normed seminorm quotients and their completions. The induced factor maps are compact. In the completed projective tensor norm, the image of the algebraic unit ball is contained in the closed absolute convex hull of a compact set, up to a fixed factor. To see this, decompose an algebraic tensor with sum of products of source factor norms at most twice its projective bound, and normalize each nonzero factor. The compact set in the target is the set of simple tensors from the closures of the two factor unit-ball images. The tensor map on those two compact sets is continuous. The closed absolute convex hull is compact because any finite net of radius $\delta$ for the set gives an approximation within $\delta$ by the bounded absolute convex hull in its finite-dimensional span. Completion preserves the resulting total boundedness for the source unit ball. This uses the projective seminorm on the seminorm completions, equivalently the original projective seminorm after taking its kernel quotient. It requires no injectivity of a completed tensor transition. Use a finite maximum for finitely many seminorm requests and a finite product for the finite sums in (UC043.1).

Finally, the transition commutes with entire evaluation, so it takes the old evaluation kernel into the new one. For a target source seminorm $p^+$ write $\bar p^+$ for its quotient seminorm. Choose a stronger source seminorm $P$ using the compactness just proved. For every $y$ in the source quotient choose a representative $c$ with $P(c)\le\bar P(y)+1$, where $\bar P$ is the source quotient seminorm. A ball of finite radius for $\bar P$ therefore has a totally bounded image for $\bar p^+$, because passage to the target quotient is nonexpansive for that seminorm. Choices of $c$ can vary with the seminorm. A bounded set is then totally bounded for every finite set of quotient seminorms, hence for the Fréchet topology. Completeness gives relative compactness. $\square$

## 3. Local boundedness criterion for whole-source jets

**Theorem UC043.2.** Let $u\in\mathfrak P^J(V_0;U)$ in the original two-slot rule. Suppose one fixed finite history $h$ and fixed scalar stages suffice for the following data near a point $a_0$. For every finite parameter order $p$, choose finite Sobolev orders $s(p)$ in that history. Suppose $u_j(a)=\partial_a^j u(a)$ for $0\le j\le p$ belongs as an entire family to $Y_{h,s(p)}$ there, and for every compact parameter set $C$ and each continuous source seminorm $P$,

$$
\sup_{a\in C}\ \inf\{P(c):\, c\in H_{h,s(p)},\
                      e_{h,s(p)}c=u_j(a)\}<\infty.
\tag{UC043.3}
$$

Then $u$ has exact (126.6) coefficient rows on a smaller interval about $a_0$. Conversely, the existence of these rows implies (UC043.3) locally with their history and scalar stages.

**Proof.** Fix $p$. The hypothesis is boundedness of each jet image in the actual history quotient on compact sets. Proposition UC043.1 makes its image relatively compact in $Y^+_{h,s(p)}$. The jet is continuous when paired against every compactly supported test in regulator and physical variables by the original compatible graph-jet rule on compact positive-regulator subintervals. If $a_m\to a$, every subsequence in the relatively compact quotient image has a further subsequence with a limit there. Its evaluated limit must equal $u_j(a)$ since every such test separates actual distributions. The quotient injects into that envelope, so every limit is the prescribed quotient value. Metrizability gives continuity of the jet in $Y^+_{h,s(p)}$.

Integrate these continuous quotient jets on compact parameter segments. Each distributional test identifies the integral of the jet of order $j+1$ with the difference of the jet of order $j$ at the endpoints. Since whole evaluation is injective on the quotient, the identity holds in the complete quotient itself. This proves $C^p$ regularity in that quotient. For row depth $r$ choose $p=r+3$, and apply Lemma 126.1 to $H^+_{h,s(p)}\to Y^+_{h,s(p)}$. A single fixed cutoff supported in the original chart and equal to one on a smaller common interval is used for every $r$. It gives a genuine $C^r$ coefficient lift for that row. The relaxed scalar stages are chosen once for all rows. The evaluated families agree on the smaller interval, so their actual derivatives agree between the rows. Every regulator derivative follows by differentiating the whole history as in 108. The mixed estimates follow from those source estimates on compact images of the parameter derivatives. The rapid error in this construction is zero. Conversely the coefficient derivatives in a genuine row have bounded image in each source seminorm on compact parameter sets. Their classes satisfy (UC043.3). $\square$

The criterion allows a different coefficient representative for each quotient seminorm. It needs neither a simultaneous bounded set of true lifts nor a continuous section of the evaluation map. It also accommodates arbitrary cancellations inside a fixed finite sum of histories. If there is a prior representative $v$ with $u-v\in\mathfrak I^J$ and satisfying (UC043.3), apply the theorem to $v$ to get (126.14) for $u$. Conversely any representative supplied by (126.14) satisfies (UC043.3) by its rows. In this formulation, the missing step is to deduce (UC043.3) locally for some finite history and fixed scalar stages from the original bounds on $u$, or to produce a uniform all-mixed-jet rapid correction making (UC043.3) hold. The argument uses the entire-evaluation kernel, which is closed. Passing to the rapid quotient first would give no such closed-kernel premise.

## 4. Moment-flat control on a weaker output rule

Even simultaneous ambient mixed estimates and strong fixed-test physical expansions do not give (UC043.3) from pointwise analytic membership. The following control omits uniform scalar-stage estimates. Its failure after a fixed allowed rescaled scalar multiplier gives a specific check on attempted proofs from those weaker premises.

Use $c=(x+y)/2$ and $t=x-y$, with density $|dc\,dt|=|dx\,dy|$. Choose $b\in C^\infty_c$ with integral one and $\zeta\in C^\infty_c$ in $t$ equal to one near zero, so their joint support is compact in $U^2$. Choose a nonzero real even Schwartz function $f$ with Fourier support away from zero, so all its moments vanish. Let $\chi$ be a smooth cutoff equal to one near zero and supported in $[0,2)$ on the positive half-line. Put $a_m=2^{-m}$ and choose smooth real bumps $\beta_m$ on disjoint intervals of radius $a_m/8$ about $a_m$, each equal to one at $a_m$, with $|\partial_a^j\beta_m|\le C_j a_m^{-j}$. Define, for $a$ near zero,

$$
g(a,\epsilon;c,t)
 = b(c)\zeta(t)\epsilon^{-1} f(t/\epsilon)
   \sum_{m\ge1} a_m^{-1}\beta_m(a)\chi(\epsilon/a_m).
\tag{UC043.4}
$$

At each positive $\epsilon$ the expression is smooth in the chart, identically zero near $a=0$, and at most one bump is active at any $a$. For every fixed $a$, each parameter derivative has an actual scalar history in one fixed localized full-profile stage of 105. The regulator cutoff is identically one at sufficiently small regulator for the given bump. For each mixed jet and each fixed physical $C^\ell$ norm, differentiation gives an ambient polynomial bound, uniformly in $a$. In fact on a nonzero summand $\epsilon\le2a_m$ and the factors $a_m^{-1-j-k'}$ from the bump and cutoff derivatives are bounded by a constant times $\epsilon^{-1-j-k'}$. The normal front factor and its remaining physical and regulator derivatives have only their usual finite scaling losses. Compact support then gives the ambient fixed-order polynomial bounds, including the off-cone estimates since every physical derivative is controlled.

For a fixed physical test $\varphi$, substitute $t=\epsilon z$ in the pairing with the front factor before the bump multiplier. Every fixed regulator derivative then gives an integral of $f(z)$ against a polynomial factor in $z$ times a differentiated test at $(c,\epsilon z)$. Taylor's formula and zero moments give arbitrary decay powers, with a finite physical test seminorm at each Taylor depth. This remains uniform on bounded physical test families after the polynomial bump losses above. Hence all fixed-test physical power/logarithmic coefficients vanish, even uniformly at every mixed-jet request. This calculation allows the physical test order to increase with the requested Taylor depth.

Now choose a fixed $\omega\in C_c^\infty(\mathbb R)$ with $\int \omega f\ne0$. On this compact physical patch, multiplication by $\omega(t/\epsilon)$ with a fixed physical cutoff equal to one on the support of $g$ is multiplication by an actual scalar 105 stage. Its front profile has compact support in the normal chart and it vanishes near the adjoining old face away from that chart. Every physical derivative of this multiplier costs only a fixed power of $\epsilon^{-1}$. For an original source-controlled family, multiply by this scalar and then integrate both physical vertices. The result has continuous physical finite coefficient in the parameter, by the finite complete-source bounds of 108 §§4–5, 7. These source maps act on the whole histories, including their completed coefficients and proper projections. A rapid error tested by the same scaled multiplier gives a rapid scalar error, since the test norm in each fixed finite Sobolev order costs only a finite regulator power.

For (UC043.4) the resulting scalar coefficient at $a=a_m$ is $a_m^{-1}\int\omega f$, and the coefficient at $0$ is zero. For sufficiently small $\epsilon$ at a fixed $a_m$, both the regulator cutoff and $\zeta(\epsilon z)$ equal one on the scaled compact test support. The coefficient therefore diverges along $a_m\to0$. This rules out any local source-controlled representative of this control modulo a uniform rapid error in the ambient equation, including a representative using any other finite original history. It does not establish failure of (126.14). The front scalar coefficients of the explicit presentation are unbounded on every neighborhood of zero, and its membership in the prior rule with uniform scalar-stage control has not been established. The control isolates why one needs the original scalar-stage hypothesis in addition to the graph-jet and physical coefficient estimates.

## 5. Return boundary

The bounded attempt supplies compact transitions for actual completed coefficient sources and their closed evaluation quotients, and a necessary and sufficient local quotient-boundedness criterion for exact source-controlled recovery with a suitable history. It does not derive such bounds for arbitrary admitted old families, nor exhibit an admitted family that defeats every local original history modulo uniform rapidness. The two-slot instance of (126.14) remains open. The argument concerns the coefficient singleton and one real chart. It uses no lifting across arbitrary profinite tests and makes no change to the prior analytic or rapid domains. Distinct scientific review and protected admission are separate. No closure of original R3, higher weights, or M5/R4 follows.
