# EXT-015 REACH / 150 — the complementary weight-two primitive test

**Disposition: partial construction and a precise unresolved source-closure lemma.** The R1 two-slot complex contracts to its four labelled affine moments, or three graded symmetric moments. Its scalar-derived extension is consequently computed without a flatness assumption. Those three scalar generators split from the enriched complement; the remaining cone is the joint kernel of the jet projection and the affine moment map. The proposed compact primitive has the correct ambient distribution identities and uniform rapid estimates. Its membership in the actual mixed source class is not proved. The relative-coordinate Fourier argument needed to copy 141 fails already for a Gaussian profile. Neither that method failure nor the failure of an unrestricted primitive on diagonal sources is a counterexample to the complementary comparison. Distinct nonauthor review and protected admission remain pending.

## 1. Category, custody and the bounded question

Work in ZFC, in the real liquid heart $\mathcal A=\mathrm{Liq}_p(\mathbb R)$ for fixed $0<p\le1$, with unit $R=\mathbb R_{<p}$, on a nonempty open interval $U$ of the existing physical line. Use exactly the actual source image $\mathcal P_n$ and finite-order uniform rapid quotient $\mathcal Z_n$ of 108, and the source-controlled parameter rows of 126. The scalar algebra $\mathcal C$ is that of 135 and 141. No source class, counterterm, normalization or accepted premise is changed.

CP175 binds this primary attempt to input cut `68115bc76d599edb75a61fd829ce5243bd538d84`, persistent ref `research/reach-complementary-two-input-frozen-20261105`. The external 92-input manifest `complementary-two-input-manifest.json` has SHA256 `a519a6868d21f4b3f4360c2821fa0656f54cbdfe370cd7472772d28ce668514b`. It records 85 scientific sources, six controls and the unchanged 147 fixture. Immediate inputs are [105](GAUSSIAN_WICK_COLLISION_NORMAL_FORM_105.md), [108](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md), [111](RENORMALIZED_QUANTUM_STRUCTURE_111.md), [117](R1_WICK_DRESSED_QUANTUM_COMPARISON_117.md), [126](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md), [135](SOURCE_CONTROLLED_COMPLETED_WEISS_135.md), [141](SCALAR_RELATIVE_WEIGHT_ONE_COMPARISON_141.md), [144](SCALAR_RELATIVE_WEIGHT_TWO_COMPARISON_144.md), and [147](WEIGHT_TWO_DIAGONAL_JET_COMPARISON_147.md) with review [148](AGENT_CRITICAL_REVIEW_WEIGHT_TWO_DIAGONAL_JETS_148.md) and ledger [149](WEIGHT_TWO_DIAGONAL_JET_ACCEPTANCE_149.md). Their source identities are fixed by that manifest; in particular 147 is blob `89b3d4a835f3750114e983854585e33d8184cb1f` and 148 is blob `074c6bb5ec54ec61a80817660a472d4e1f562370`.

Use labelled classical slots first, with $D_i=\partial_{x_i}^2$ and

$$
d=D_1\iota_1+D_2\iota_2,
\qquad |e_i|=-1.
\tag{150.1}
$$

Let $P$ and $I$ be the full finite diagonal-jet extraction and insertion of 147, so $PI=1$. Put $\pi=1-IP$ and $Y=\ker P$. All of these are actual cochain maps, including on the separate fixed-test parameter sheaves. The question is the factored map

$$
\alpha_Y:\mathcal C\otimes_R^L X_2(U)\longrightarrow Y(U),
\qquad
\mathrm{Cone}(\alpha_2)
\simeq\mathcal C^{\oplus3}[0]\oplus\mathrm{Cone}(\alpha_Y)
\tag{150.2}
$$

in the graded symmetric category. The second formula includes the accepted Wick reduction and the relative scalar unit, whose cone is zero. The first summand in (150.2) is accepted 147; only the second is the present question.

## 2. Ambient compact primitives and their exact bounds

Choose $b_0,b_1\in C_c^\infty(U)$ satisfying $\int x^j b_i(x)\,dx=\delta_{ij}$ for $0\le i,j\le1$, as in 141. On compact two-variable distributions define partial moments and their reinsertion by

$$
m_{i,j}v=\int x_i^j v\,dx_i,
\qquad B_i v=\sum_{j=0}^1 b_j(x_i)m_{i,j}v,
\qquad h_i v=e*_{x_i}(1-B_i)v,
\quad e(t)=|t|/2.
\tag{150.3}
$$

All integrals are distributional pushforwards with the ordinary physical density. The convolution variable has Jacobian one. Fixed compact cutoffs equal to one on the input support make the polynomial moment tests legitimate. No evaluation at a point of a distribution is involved.

The support of $h_i v$ in coordinate $i$ lies in the interval hull of the input coordinate support and the bump supports. Outside this hull the kernel is affine in the integrated coordinate and its two moments vanish. Other coordinate supports are unchanged. Thus the result has compact support in $U^2$. Distributional integration by parts gives

$$
D_i h_i=1-B_i,\qquad h_iD_i=1,\qquad m_{i,j}D_i=0.
\tag{150.4}
$$

Operators in different coordinates commute. These are whole-family identities before any quotient.

Fix a common compact support and choose a compact smooth $\chi$ in the output coordinate and compact smooth $\kappa$ on the difference line such that $k=\kappa e$ agrees with $e$ on every required input-output difference. On this support

$$
h_i v=\chi(k*_{x_i}v)
-\sum_{j=0}^1 \chi(e*b_j)(x_i)m_{i,j}v.
\tag{150.5}
$$

The first term is bounded on every full $H^{-t}(\mathbb R^2)$ by the $L^1$ norm of $k$ and the fixed smooth multiplier bound. For the partial moment map, pairing in one coordinate with a fixed compact smooth function is bounded $H^{-t}(\mathbb R^2)\to H^{-t}(\mathbb R)$ for $t\ge0$: in Fourier variables apply Cauchy–Schwarz to the integrated frequency and use rapid decay of the test transform. The resulting constant is finite after multiplying that transform by $(1+|\xi_i|^2)^{t/2}$. Tensoring the output with a fixed smooth bump is bounded in the reverse direction at the same order. Therefore

$$
\|h_i v\|_{H^{-t}(\mathbb R^2)}
\le C_t\|v\|_{H^{-t}(\mathbb R^2)}.
\tag{150.6}
$$

The constants depend on the fixed supports and bumps, not on the regulator, parameter or requested rapidness power. Every regulator and parameter derivative commutes with the fixed distributional formula. Consequently this ambient operator preserves actual whole-family equality and the uniform rapid relation with one finite order for each mixed derivative. The same estimates hold on compact parameter sets. They do **not** provide a lift into $\mathcal P_2$, so by themselves they define no operator on the analytic source quotient or its liquid parameter sheaves.

## 3. A proved R1 coefficient lemma

**Lemma 150.1.** On a compact block-coordinate space, convolution in one block coordinate by $k=\kappa e$, followed by a smooth compact cutoff, sends every fixed R1 graph source $E_{s,K,\Gamma}$ continuously into a fixed graph source whose cone avoids every nonzero partition conormal. The support may enlarge. The negative Sobolev order need not increase for the global norm; individual off-cone seminorm estimates use finitely many input normal seminorms. This lemma concerns R1 coefficients, not arbitrary mixed products $a_\epsilon T$ as a completed source.

**Proof.** Let the shifted coordinate be $y_i$ and write the convolution as pushforward of $k(t)\otimes T(y)$ by $p(t,y)=y+t e_i$, with compact support. For a target covector $\eta\ne0$, the transpose is $(\eta_i;\eta)$. The second covector is nonzero and must belong to $\Gamma$. If $t\ne0$, the first factor is smooth, so necessarily $\eta_i=0$. If $t=0$, no shift of the physical point occurs. Thus a valid closed enclosing output cone is the union of the unchanged cone and the shifts of the part of $\Gamma$ on which $\eta_i=0$. Compact supports and compact shifts make this union closed on the cosphere bundle.

At zero shift a forbidden output conormal would already be forbidden at input. At a nonzero shift, suppose the output point and covector belong to a partition conormal. Each output block consists of coincident coordinates and its covector sum is zero. Remove coordinate $i$ from its block, placing it in a singleton. The other coincident coordinates are unchanged at the input point. Their sum remains zero because $\eta_i=0$, and the singleton also has sum zero. All other blocks are unchanged. This gives an input partition conormal with the same nonzero covector, contradicting the input exclusion. The argument includes intersections of arbitrary partitions, not just a single pair diagonal.

Exterior tensor with a fixed compact distribution and proper pushforward have the normal-topology continuity used and cited in 141 §4 and 117.1. Here their explicit transpose relation and compact support meet those same hypotheses. There is no pullback or multiplication of two distributions at an intersecting diagonal. Smooth cutoff multiplication preserves the enclosing cone. Its global negative Sobolev estimate is the $L^1$ multiplier bound, as in (150.6). The graph refinements of 108.1 and 117.1 turn normal continuity and this global estimate into continuity in the claimed complete graph source. This proves the lemma. $\square$

The extra zero-covector condition at nonzero shift is essential. The larger set of *all* translates of an arbitrary R1 cone need not avoid the partition conormals. The common-center proof in 141 can use that larger set because all relative coordinates remain fixed; the present proof cannot.

In two slots, each partial moment is a proper projection into the unrestricted one-slot R1 distribution space, with the fixed test and Sobolev bounds above. Its bump reinsertion has covectors zero in one coordinate and hence avoids the two-slot diagonal conormal. Applying Lemma 150.1 and subtracting these corrections proves actual R1 membership of $h_i$, with support in $U^2$. These continuous graph maps apply to cover-local complete lifts, and their evaluated pairing identities make them independent of representatives. They therefore define real-liquid maps on the R1 image. The same maps are continuous in the original fixed normal topology; hence they act on the original locally normal R1 parameter plots, commuting with their parameter derivatives.

## 4. The R1 two-slot source is now computed

**Proposition 150.2.** The labelled classical R1 two-slot complex is homotopy equivalent to $R^{\oplus4}[0]$ by the four moments $\langle v,x_1^a x_2^b\rangle$, $a,b\in\{0,1\}$. After graded symmetrization it is homotopy equivalent to $R^{\oplus3}[0]$. In particular its derived scalar extension is $\mathcal C^{\oplus3}[0]$ in the symmetric category. This is also a separate fixed-test smooth homotopy statement for the admitted R1 parameter families.

**Proof.** Put $H_i=h_i e_i\wedge$. Define $\Pi_i$ on the exterior complex to act as $B_i$ when $e_i$ is absent and as zero when $e_i$ is present. The Koszul anticommutators, (150.4), and commutation in the other coordinate give

$$
dH_i+H_i d=1-\Pi_i,
\qquad
H=H_1+\Pi_1 H_2,
\qquad
dH+Hd=1-\Pi_1\Pi_2.
\tag{150.7}
$$

For example the anticommutator with $D_i\iota_i$ is $D_i h_i=1-B_i$ when $e_i$ is absent and $h_iD_i=1$ when it is present. Cross-coordinate anticommutators vanish. Each $\Pi_i$ is a cochain map; this proves the last identity including the degree minus two sign. The product $\Pi_1\Pi_2$ is zero in negative degrees and in degree zero reinserts the four moments with bumps $b_a(x_1)b_b(x_2)$. Moment followed by bump is the identity on $R^4$. Lemma 150.1 proves that every term in this explicit homotopy exists on the actual R1 source; no separable representation of an arbitrary R1 kernel was used.

Using the same bumps in both coordinates makes the moment retraction equivariant under exchange. Average $H$ with its conjugate by the graded exchange involution to get an equivariant homotopy. Exchange interchanges the two mixed moments and fixes the other two, leaving a three-dimensional invariant space. A convenient symmetric coordinate list is $(m_{00},(m_{10}+m_{01})/2,m_{11})$. Since two is invertible in the real heart, exact averaging gives the symmetric result.

The maps and identities are actual liquid maps through graph stages, and actual parameter maps as established above. Derived scalar extension preserves this explicit homotopy equivalence. Its finite free right side computes $\mathcal C\otimes_R^L R^3=\mathcal C^3$. No nuclear flatness, arbitrary-profinite projectivity or evaluation of an arbitrary liquid-derived tensor is used. $\square$

The ordinary scalar pairing takes these finite free generators to the corresponding smooth bump products in $Y$. They are distinct-block sources and have zero extraction by 147. Consequently (150.2) may be represented, in $D(\mathcal A)$, by the explicit map

$$
\beta:\mathcal C^{\oplus3}[0]\longrightarrow Y(U)
\tag{150.8}
$$

given by those symmetric bump generators.

There is a further unconditional splitting. The four ordinary two-slot moments define a cochain map to $\mathcal C^4[0]$ on the enriched labelled complex: multiply by the smooth compactly supported versions of $x_1^a x_2^b$, then forget all vertices using 108 and 135. The polynomials are affine in each coordinate, so integration by parts annihilates both $D_i$ boundaries. This uses the actual scalar regulator curves, not their physical finite coefficients. Fixed test bounds preserve the rapid relation, and the accepted all-vertex source maps preserve complete coefficients and fixed scalar indices across the 126 rows. Taking symmetric moments gives a cochain map $m:Z_2\to\mathcal C^3[0]$. Its restriction $m_Y$ to $Y$ satisfies $m_Y\beta=1$, by the chosen bump moments. Hence, as actual symmetric cochain objects,

$$
Y=\beta(\mathcal C^3[0])\oplus W,
\qquad W=\ker(m_Y),
\qquad \mathrm{Cone}(\alpha_Y)\simeq W.
\tag{150.8a}
$$

Here the kernel is the cochain kernel: $m$ is zero in negative degrees. Thus $W$ is precisely the joint cochain kernel of $P$ and $m$, not the kernel of additional unspecified moment maps in negative degrees. The explicit projection onto $W$ in the entire $Z_2$ is $(1-\beta m)\pi$. One must apply $\pi$ first: ordinary moments of the extracted jets need not vanish. This ordering avoids treating $m$ as if it annihilated the diagonal summand. The cone of $\beta$ splits as the contractible identity cone on $\mathcal C^3$ plus $W$, proving the last formula after the finite free source replacement in Proposition 150.2.

All moment maps, bump sections and projections just used are explicit maps on the source-controlled parameter rows, with their uniform rapid bounds. They give the same direct decomposition of actual differentiable module-sheaf complexes at each fixed profinite test, commuting with the flat connection. This is a separate splitting statement; it does not evaluate an arbitrary derived liquid tensor. Consequently the unconditional unresolved question is the acyclicity of $W$. The cohomology of that residual object is not computed here. Together with (150.2), the full symmetric comparison cone is $\mathcal C^3[0]\oplus W$ in the derived category.

## 5. The exact enriched closure lemma that is still missing

Represent a section of $Y$ locally on a source and rapid cover. Subtract its entire same-block jet contribution using the positive-scale coefficient maps of 147. The remainder is a finite sum of distinct-retained-block histories. For a quotient section with $P=0$, the subtracted contribution is rapid, by the extraction/insertion estimates. Thus these histories suffice; they do not make the remaining normal profiles regular at zero scale.

Partial moments $m_{i,j}$ already act on such histories by smooth decoration and forgetting one vertex. The accepted 108 operations give a one-slot source. Bump reinsertion is exterior composition with a compact smooth one-slot source. Its retained labels are distinct blocks, so its extraction is zero. Their complete-source bounds and output scalar index families are fixed across the parameter rows. The unresolved part of (150.3) is solely convolution of the **whole** mixed history.

**Unresolved lemma 150.L.** For every fixed finite collection of distinct-retained-block sources

$$
v_\epsilon=q_*\partial^\gamma(i_\sigma)_*
[a_\epsilon T]
\tag{150.9}
$$

of 108.7, including their completed $E_{s,K,\Gamma}\widehat\otimes_\pi S_\lambda$ coefficients, construct actual source representatives of $h_i v$ in a finite collection of the *existing* output histories. Require continuous maps on the complete coefficient sources, with fixed compact supports, admissible R1 cones, scalar index families, auxiliary remainder weights, physical densities and finite jet lists. For every relaxed graph order needed by a genuine 126 parameter row, these same scalar and geometric choices must work with finite seminorm bounds. The maps must evaluate to (150.3) for the entire summed history, not merely match its physical asymptotic coefficients.

The finite list of histories and fixed scalar choices, rather than merely existence at every regulator, are needed for profinite descent and the actual source-controlled family rule. The proof must include every collision stratum of the extra integration variable with old and retained vertices, not only the external two-slot diagonal. The desired result does not follow from Lemma 150.1: the scalar factor depends on the coordinate being integrated, and cannot be pulled out of the convolution.

If this lemma is proved for the distinct-block sources, (150.6) supplies uniform rapid descent and whole-evaluation independence. It would give the ambient $H$ of (150.7) on $Y$ with values in $Z_2$, because the intermediate $\Pi_1$ and moments have the already proved source maps. To avoid any unproved claim that the primitive preserves $Y$, use explicitly

$$
H_Y=\pi H|_Y.
\tag{150.10}
$$

Since $\pi$ is an actual cochain map and is the identity on $Y$, (150.7) would imply

$$
dH_Y+H_Yd=1_Y-\pi\Pi_1\Pi_2|_Y.
\tag{150.11}
$$

The bump image is distinct-block, so $\pi\Pi_1\Pi_2=\Pi_1\Pi_2$. The ordinary two-slot moments restricted to $Y$ are cochain maps and split this bump image. Their target is $\mathcal C^4$ by the all-vertex scalarization of 108/135. Averaging then gives a contraction to $\mathcal C^3$ and identifies (150.8) as a quasi-isomorphism. This paragraph is an implication **conditional on 150.L**, not a cohomology verdict. Commutation of the projected homotopy with the differential is the cochain identity for $\pi$, not an assumed commutation of $P$ with $h_i$.

## 6. A demonstrated failure of the relative Fourier estimate

The center-coordinate argument in 141 separates $a_\epsilon(y,z)$ into Fourier modes in the common translation variable $y$. Every collision boundary is a product in $y$, so integration by parts preserves the same scalar indices and gives rapid mode decay in every scalar-stage seminorm. Moving one retained coordinate while holding the others fixed changes collision distances. The required analogue of that estimate is false.

To see this within the admitted Gaussian sector, take a smooth compact cutoff $\chi$ supported inside a period cell $(-\pi,\pi)$ and equal to one near zero. Put

$$
a_\epsilon(z)=\chi(z)\kappa_\epsilon(z),
\quad
\kappa_\epsilon(z)=\frac{1}{\sqrt{2\pi}\epsilon}
\exp\left(-\frac{z^2}{2\epsilon^2}\right),
\quad
c_\ell(\epsilon)=\frac1{2\pi}
\int a_\epsilon(z)e^{-i\ell z}\,dz.
\tag{150.12}
$$

Complex notation abbreviates real sine and cosine coefficients. The actual cutoff and Gaussian are permitted scalar factors. At each fixed $\ell$, substituting $z=\epsilon u$ and using Gaussian domination gives

$$
\lim_{\epsilon\downarrow0}c_\ell(\epsilon)=\frac1{2\pi}.
\tag{150.13}
$$

More precisely its expansion agrees to all orders with $(2\pi)^{-1}\exp(-\epsilon^2\ell^2/2)$; the cutoff error and each regulator derivative are rapidly small for fixed $\ell$. Thus every fixed scalar stage containing these actual scalar curves has a continuous coefficient functional extracting the constant regulator coefficient, and its associated seminorm satisfies

$$
q(c_\ell)\ge\frac1{2\pi}
\quad\hbox{for every }\ell.
\tag{150.14}
$$

There can be no bound $q(c_\ell)\le C_N(1+|\ell|)^{-N}$ for $N>0$, with a constant independent of the mode. Enlarging the index family while still retaining continuous constant-coefficient extraction does not fix this failure. For a retained-coordinate expansion with the other retained coordinate fixed, a Gaussian depending on their difference gives the same calculation at the other coordinate equal to zero. Compact center factors can be chosen equal to one on that patch.

This disproves the relative analogue of estimate 141.5, which was the ingredient used there to sum arbitrary completed R1 coefficients against polynomially growing graph seminorms. It does not prove that any particular series diverges after cancellation, that the compact primitive is outside every allowed source representation, or that (150.8) fails. For each positive regulator the Fourier series is rapidly convergent; that weaker fact does not give the required fixed-stage conclusion. The input is a smooth normal Gaussian at every positive regulator and belongs to $Y$, by 147. Removing its finite delta jets removes nothing and does not remove its concentration as the regulator goes to zero.

## 7. Why unrestricted convolution and a formal new edge are insufficient

An unrestricted version of 150.L on all histories has a direct positive-scale obstruction. Choose $\rho\in C_c^\infty(U)$ equal to one near an interior point and take the admitted same-block source

$$
v(x_1,x_2)=\rho(x_2)\delta(x_1-x_2).
\tag{150.15}
$$

Its normalized ambient primitive is

$$
h_1v=\rho(x_2)
\left[\frac{|x_1-x_2|}{2}
-(e*b_0)(x_1)-x_2(e*b_1)(x_1)\right].
\tag{150.16}
$$

The correction terms are smooth. Near a point where $\rho=1$, the first term is a genuine normal cusp. It cannot be a sum of finitely many normal delta derivatives and a center-distribution-valued smooth function of the normal variable, as required by 147.7 for every actual positive source. Indeed shrinking normal tests show that all delta coefficients of a locally bounded cusp are zero. Pairing with a center test of nonzero integral then leaves a nonzero multiple of $|z|$, which is not smooth in $z$. Thus this exact ambient primitive does not belong to $\mathcal P_2$. This is a failure of unrestricted positive-source closure, not a failure of the restricted lemma on $Y$. No assertion about all possible rapid-equivalent substitute families is needed for this control.

A direct augmented-history construction would introduce the Green factor $|x_i-y|/2$ before forgetting $y$. That factor is not an admitted scalar stage of 105: it is nonsmooth on a physical diagonal at **positive** regulator, whereas the scalar stages are smooth on the positive interior. Nor is that factor by itself an admissible R1 coefficient on the augmented variables: its conormal on $x_i=y$ is precisely a forbidden partition conormal. One cannot classify it as an allowed factor simply by drawing a new edge. Lemma 150.1 avoids this problem for a pure R1 coefficient by computing the output cone of the entire integral; it does not turn the intermediate Green factor into an admitted source.

The admitted Gaussian Wick propagator $P_\epsilon$ is smooth and satisfies $P_\epsilon''=\kappa_\epsilon$. Replacing $e$ by it is a legal model operation in suitable typed histories, but then the right side of (150.4) is convolution with $\kappa_\epsilon$, not the identity. Gaussian smoothing minus identity is generally of finite regulator order, not uniformly rapid to all orders. An infinite formal inverse heat expansion is not a finite history or a proved convergent completed-source map. The marked Wick identity therefore does not resolve 150.L.

## 8. Exact residual inference, controls and next admissible input

The primary construction stops at 150.L. A genuinely new mechanism would be a **mixed conormal Green-kernel pushforward theorem** on the augmented collision arrangement: starting with a distinct-retained-block history, integrate the zero-width conormal Green factor against its entire scalar-PHG/R1 coefficient and prove that the output has a representation by the existing finite completed histories, with the fixed-stage and all-mixed-row bounds stated in 150.L. Such a theorem must separate the forbidden same-block cusp example and account for the true densities and every simultaneous collision. The scalar b-fibration and scalar pushforward theorem in 105 does not cover this new positive-interior conormal factor or its mixed distributional coefficients. Geometry of the forgetting map alone is not the missing mapping theorem.

A proof of that theorem, an alternative fixed-stage representation with those estimates, or a genuine class in $Y$ shown to survive every allowed boundary and bump correction would be new input for another bounded cycle. A fresh context, positive-regulator Fourier convergence, a successful raw Gaussian primitive, or another check of finite polynomial algebra would not be new input. There is no claim here that the Green-kernel theorem is true, false or the only possible route.

| Control or inference | Result in this return |
| --- | --- |
| Compact support and affine correction | Proved ambient identities and fixed-support bounds; interval hull essential. |
| R1 cones across the entire partition arrangement | Proved for the pure coefficient convolution by the zero-covector-at-nonzero-shift argument. |
| R1 labelled and symmetric cohomology | Four and three affine moment classes respectively, with explicit actual homotopies. |
| Derived scalar source and actual comparison map | Reduced to (150.8) without flatness; three scalar bump classes split from $Y$, and the complementary cone is the actual joint kernel $W$ in (150.8a). Its acyclicity remains unknown. |
| Actual equality and uniform rapidness | Ambient fixed-order bounds proved for whole sums and every mixed derivative. Source maps still required for enriched liquid descent. |
| Full mixed scalar indices and completed coefficients | Unresolved 150.L; direct relative Fourier estimate demonstrably false. |
| Full diagonal jets | Preserved as accepted; unrestricted primitive fails on the explicit cusp control. |
| Projection to the complement | Conditional homotopy is explicitly $\pi H|_Y$; no assumed preservation or commutation with extraction. |
| Densities, signs and moments | Actual density in convolution; Koszul signs derived in (150.7); no finite coefficient extraction substituted for scalar families. |
| Normal profiles and decorations | Gaussian control remains in $Y$; arbitrary fixed finite jets and completed histories remain obligations of 150.L. |
| Legal sources and overlaps | No overlapping singular counterterms are multiplied; all277 sources and both legal spinneys stay in the unchanged model. |
| Parameter and liquid scope | Proved R1 maps and conditional enriched maps distinguished; no full126.14 recovery or derived-evaluation interchange. |

This is one primary construction. No correction has yet been consumed. A distinct same-system nonauthor must review the new coefficient-cone proof, actual R1 homotopy, Fourier control and the conditional boundary before admission; shared historical inputs are not external certification. No numerical fixture is needed for the analytic gap. The finite identities in (150.7) follow from the displayed operator equations rather than numerical sampling. Existing expensive host and 147 algebra fixtures are unchanged and need no replay for this result.

The complementary cone, higher weights, full family recovery (126.14), original liquid-cohomology comparison R3, actual lifting and the broader derived and multiplicative integration remain open. R0, R1, R2 and the fixed-host procedure retain their admitted scopes. No original programme obligation is closed by this bounded return.
