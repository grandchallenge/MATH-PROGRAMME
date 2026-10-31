# EXT-015 REACH / 108 — mixed R1 pushdown with a fixed-order distributional boundary

**Disposition: positive construction candidate for mixed operator closure; unreviewed.** The domain is an actual image of complete mixed coefficient stages. Its enriched boundary is a quotient by uniformly rapid finite-order distribution families, not by all weakly asymptotic zero families. Scalar heat-space pushforward105 supplies the physical power/logarithmic expansion. Microlocal interpolation supplies the stronger ideal required for operator descent. Neither ordinary strong-distribution smoothness nor a signed joint collar cone is used as a substitute for these two different statements. Review109, ledger110 and protected admission are separate.

## 1. Contract, category and frozen dependencies

Work in real liquid modules for fixed $0<p\le1$, in ZFC, on the same one-dimensional free-scalar model and interval basis. The scientific input cut is 8f630df438e5a0d501b73b805cf99a8fc92d2df2 on `research/reach-mixed-r1-input-frozen-20261031`; CP045 binds this attempt before construction.

| Dependency | Exact Git blob |
| --- | --- |
| Full protocol090 | 6b642bf10c3328bb64d37474e290810fb45cbca1 |
| Intrinsic subtraction087 | 452c494bcdc94ba94e52ae50c7b4d1eb3240ca83 |
| Liquid realization091 | c517fe1ae46bcaa9f4a3fc0e64381ae8096bfe27 |
| Full normal profiles096 | ee15ed47d90123bdd958dcb4a93cd51b428c1702 |
| Actual collar image099 | bcdd5328c52361403b54c24c662c336bff4ce7ae |
| Heat geometry and scalar closure105 | a8ce66ff0edec33e2aff299550fca2089d671033 |
| Distinct review106 | d1d64802076b033218f3c93ac11af96f4c683e6a |
| Generated-normal-form ledger107 | 0a760acc64820df8f271afd19f002f3ecf9a92dd |

The mandatory singular inputs remain the eleven-edge host of087, all277 proper sources, both legal disjoint spinneys and arbitrary fixed finite decorations. The original R1 sectors remain admitted. Products and restrictions below are the typed operations of105: disjoint factorization, noncharacteristic coefficient maps, and finite collision jets against actual model complements smooth at positive regulator. Overlapping source counterterms are not multiplied. Unrestricted products of two singular R1 kernels with overlapping supports are not asserted.

The new mechanism separates three objects: an actual mixed analytic image $\mathcal P_n$, an enriched boundary $\mathcal P_n/(\mathcal P_n\cap\mathcal I_n^{\mathrm{rap}})$, and its weaker physical power/logarithmic coefficient map. The finite-order rapid subobject $\mathcal I_n^{\mathrm{rap}}$ is essential. A strong distributional expansion alone would lose a spatial moment-flat normal profile and need not survive multiplication by a scale-dependent kernel.

The moderate/rapid design has a precedent in generalized-function constructions, for example [Garetto, math/0407015](https://arxiv.org/abs/math/0407015). That precedent supplies terminology, not the theorem here. The sources below are complete real locally convex graph spaces; their evaluated images, intersections and quotients are formed in the fixed real liquid heart. No generalized-number topology, arbitrary product of distributions, or liquid realization of a Colombeau algebra is imported by analogy. The analytic mixed source class, its physical finite map and its full-profile comparison still require the proofs below.

## 2. Fixed-order spatial stages and actual regulator curves

Fix a physical compact support $K\Subset U^n$, a closed wavefront cone $\Gamma$, and a finite real Sobolev index $s$. Choose countably many properly supported order-zero pseudodifferential cutoffs $A_j$ whose microsupports are disjoint from $\Gamma$ and exhaust its complement. Use coordinate partitions of unity as necessary. Put

$$
E_{s,K,\Gamma}
=H^{-s}_K\cap\bigcap_{j,m\ge0}
\{u:A_ju\in H^m\},
\qquad
\|u\|_{-s},\quad\|A_ju\|_m.
\tag{108.1}
$$

This is a complete Fréchet graph space. Indeed it is the closed subspace of $H^{-s}_K\times\prod_{j,m}H^m$ given by the distributional equalities $v_{j,m}=A_ju$ and agreement of the Sobolev representatives. Its realization is liquid by the complete-locally-convex measure criterion used in096/099. No projectivity or derived exactness is inferred.

For regulator derivatives use sequences of finite orders $\mathbf s=(s_k)$, not one common order. A moderate stage consists of compatible continuous curves $u_k:(0,e_0)\to H^{-s_k}_K$ such that $\partial_\epsilon u_k=u_{k+1}$ distributionally, with seminorms

$$
\sup_{0<\epsilon\le e_0}
\epsilon^{N_k}\|u_k(\epsilon)\|_{-s_k},
\qquad
\sup_{0<\epsilon\le e_0}
\epsilon^{N_{j,m,k}}\|A_ju_k(\epsilon)\|_m.
\tag{108.2}
$$

All displayed exponents are fixed finite integers at a stage. Derivative compatibility is a closed condition in the product of weighted continuous-curve spaces. These are therefore complete Fréchet graph stages as well. The off-cone part may be omitted for the ambient actual-curve object; it is retained when specifying a noncharacteristic operator domain. Filter over orders, exponent sequences, compact supports and cones. Actual evaluation identifies coincident curves as distributions for every positive regulator. The resulting liquid image is denoted $\mathcal M_n$.

A general R1 fixed normal sector need not embed continuously into one globally fixed $H^{-s}$. Its profinite plots do. A compact image of a continuous profinite plot is bounded in distributions with one fixed support, hence has uniformly finite distribution order. Sobolev embedding bounds it in some $H^{-s_0}$. A further finite loss makes the compact-support Sobolev inclusion compact. Distributional continuity together with that compactness implies continuity into the weaker $H^{-s}$: any convergent net has relatively compact Sobolev image and its only possible distributional limit is the specified one. The off-cone Sobolev seminorms are continuous by the normal topology. Thus every such profinite plot lifts to some(108.1). This proves the required condensed map without claiming that the unrestricted inductive topology has been repaired.

## 3. The rapid subobject and the interpolation lemma

A rapid stage has one fixed order $t_k$ for each regulator derivative and satisfies, for every $L\ge0$,

$$
\sup_{0<\epsilon\le e_0}
\epsilon^{-L}\|\partial_\epsilon^ku_\epsilon\|_{-t_k}<\infty.
\tag{108.3}
$$

The orders may depend on $k$; they may not increase with the requested rapidness $L$. These complete graph stages define a liquid subobject $\mathcal I_n^{\mathrm{rap}}\subset\mathcal M_n$. The symbol $\mathcal I^{\mathrm{rap}}$ denotes only this rapid subobject; it is different from096's historical full normal-profile object $\mathcal N_d$. Intersections and images are taken in the liquid heart. On arbitrary profinite tests the statement means a lift locally on an extremally disconnected cover through finitely many such fixed stages, followed by actual-family descent. It does not use arbitrary-profinite projectivity.

**Lemma108.1 (microlocal saturation).** Suppose a curve is moderate in a stage(108.2) and rapid in the sense(108.3). After a finite loss of Sobolev order for each derivative it is rapid in every seminorm of an admissible fixed spatial cone stage. Consequently polynomially regulator-bounded, noncharacteristic spatial operations preserve $\mathcal I^{\mathrm{rap}}$.

**Proof.** Fix one regulator derivative. Write $u=u_\epsilon$, with $H^{-s}$ moderate and $H^{-t}$ rapid. Increase $t$ if needed. For $\delta>0$, interpolation between these two norms gives rapidness in $H^{-s-\delta}$; if $t\le s+\delta$ this follows simply by continuous Sobolev inclusion. Otherwise the interpolation exponent of the rapid factor is positive, while the other factor loses only one fixed regulator power. Given any desired output power, increase the input rapid power before applying the estimate. Thus that output norm is rapid with one order independent of the desired power.

For a fixed $A_j$ and $m$, use the rapid $H^{-t}$ norm of $A_ju$ and its moderate $H^{m+1}$ norm. Sobolev interpolation gives

$$
\|A_ju\|_m
\le C\|A_ju\|_{-t}^{\theta}
\|A_ju\|_{m+1}^{1-\theta},
\qquad \theta>0.
\tag{108.4}
$$

The second factor loses a fixed finite power. The first is available with arbitrary power, so the result is rapid. Repeat for each finite requested seminorm and each derivative. This is precisely where moderation outside the chosen cone is used; weak fixed-order rapidness by itself is insufficient.

For completeness, the fixed-cone operator estimate needed next uses finitely many of these seminorms. A noncharacteristic diagonal restriction has a bound of the form

$$
\|i^*u\|_{-r}
\le C\left(\|u\|_{-s}
+\sum_{(j,m)\in F}\|A_ju\|_m\right)
\tag{108.5}
$$

with finite $F$ and finite $r$. In coordinates $i(x')=(x',0)$, the Fourier integral for restriction splits into the allowed cone, where $|\xi''|\le C|\xi'|$, and its complement. Cauchy–Schwarz bounds the first integral in a Sobolev space after a loss larger than half the codimension; finitely many off-cone cutoffs with sufficiently large positive Sobolev index bound the second integral. The same split after an output microlocal cutoff gives every fixed target off-cone seminorm. Compact coordinate partitions make the constants uniform on the specified support and cone. Fixed linear changes of variables and finite derivatives have the analogous finite seminorm estimates. Proper projection has the corresponding estimates by its compact-support dual test map. Finite normal-jet pushforward is bounded after a finite Sobolev loss by the same Fourier calculation.

Multiplication by an actual scalar heat kernel has these estimates with a finite additional regulator power for each requested seminorm and derivative. On the compact resolved patch its physical derivatives have such bounds: the regulator is a positive unit times a finite boundary monomial, so any fixed inverse boundary weight and any fixed logarithmic power is bounded by a finite inverse regulator power. Leibniz gives only finitely many terms. The bilinear noncharacteristic product estimates follow from the corresponding Fourier convolution split under the no-opposite-covectors condition. Apply(108.4) to the negligible factor and moderation to the other factors. All these finite estimates preserve rapidness. $\square$

For finite normal jets, the permitted operators are compositions of submersion pullback, proper pushforward, derivatives and the admitted products. Their estimates apply to the entire evaluated distribution. Ideal preservation does not require extracting coefficients separately from a sum of jets on intersecting strata. Such extraction is not asserted to be uniformly bounded in a negative Sobolev norm. The positive-scale canonical jet grouping used for analytic closure is a different statement. In particular no restriction of a delta to its own support is taken.

The cone requirement is a real domain condition. A smooth family can be extremely oscillatory as the regulator tends to zero and negligible in a weak Sobolev norm, while its value on a later diagonal is large. If it lacks the required moderate off-cone estimates, Lemma108.1 does not license that diagonal restriction. Positive-scale smoothness alone is not the stated operator domain.

## 4. Complete mixed analytic sources

Use the full heat collision spaces of096 and the accepted scalar power/logarithmic stages of105.5–105.6, with their fixed index families, finite lower orders, asymptotic remainder seminorms and auxiliary remainder weights. Let $S_\lambda$ be one such complete scalar stage, over a compact physical patch, including a fixed finite collision-jet order where present.

For an original R1 coefficient choose(108.1) with its cone avoiding every partial-partition conormal. Its pullback to the heat space is noncharacteristic also at every face and corner by096.2. It is smooth in the normal boundary variables with distributional tangential coefficients, with every fixed normal derivative continuous in the corresponding fixed normal sector. The finite-order graph form(108.1) and the Fourier estimate(108.5) give finite Sobolev losses for every such requested seminorm. This supplies the uniform coefficient estimates, beyond scalarwise smoothness.

Here is an explicit finite-order justification also for the nonlinear heat chart pullbacks. Let $E=E_{s,K,\Gamma}$ and let $T\mapsto v_T(r)$ be one of the continuous linear normal pullback families on a compact radial parameter box furnished by099. Fix finitely many radial derivatives. For each individual $T$, those derivatives range over a bounded set of tangential distributions with common compact support, hence have one finite Sobolev order and one common norm bound. For integers $t,l$, the sets

$$
\left\{T\in E:
\sup_{r,\,|\alpha|\le k}
\|\partial_r^\alpha v_T(r)\|_{H^{-t}}\le l\right\}
\tag{108.6a}
$$

are closed: a compact-support Sobolev ball is closed in distributions, by weak compactness and uniqueness of the distributional limit. They cover the Fréchet space $E$. Baire's theorem makes one have interior; subtract two elements and use linearity to obtain a zero-neighborhood estimate, hence a bound by finitely many defining seminorms of $E$. Thus every fixed radial derivative request has a uniformly finite tangential Sobolev order and a finite source seminorm bound. This does not demand one order for all derivative requests. It supplies the finite test-derivative order needed for the bilinear estimates below, rather than an unsupported assertion of joint continuity for unrestricted distributional duality.

Form completed mixed coefficient stages from

$$
E_{s,K,\Gamma}\mathbin{\widehat\otimes}_{\pi}S_\lambda
\tag{108.6}
$$

and finite sums, with the actual geometric pullback, multiplication and finite-jet maps. The completion is part of(108.6); no completeness of an uncompleted tensor product is assumed. These maps extend to the completion because they have jointly continuous finite seminorm estimates. To check this, a fixed coefficient derivative of a scalar kernel uses finitely many $C^r$ seminorms, while a fixed distributional target seminorm uses the fixed $H^{-s}$ norm and finitely many off-cone norms of the R1 coefficient by(108.5). Their product bounds that target seminorm. Higher asymptotic depth requests more finite seminorms, all present in the source. Thus the bilinear map is jointly continuous on these fixed-order stages. This does not assert joint continuity of unrestricted distribution/test duality on the entire original normal sector.

A source expression is a finite sum of actual kernels

$$
q_*\partial^\beta(i_\sigma)_*
\bigl[a_\epsilon\,T\bigr],
\tag{108.7}
$$

where $a$ is in a scalar stage $S_\lambda$, $T$ is a pulled-back R1 coefficient, $i_\sigma$ is a partition stratum inclusion, and $q$ is a proper physical vertex projection. The completed coefficients in(108.6) are allowed in this formula by continuity. Take the image of the direct sum of these complete sources inside the ordinary positive-regulator internal-Hom envelope. Denote it by $\mathcal P_n$. The graph, source history and tensor presentation are not retained as distinctions between equal evaluated kernels.

An R1 restriction to a partition remains an R1 coefficient on its block coordinates. If a pulled-back covector were forbidden for a further block partition, its lift would have zero covector sum on each block of the corresponding joined physical partition. That would be a forbidden original conormal, contradicting the chosen input cone. This also gives the fixed output cone for the restriction. For any further coefficient product, the joined output cone must again avoid the forbidden partition conormals; absence of opposite input covectors alone does not imply this stronger condition. In particular this theorem does not add arbitrary same-variable products of overlapping R1 coefficients.

Every source maps continuously to some moderate graph stage(108.2). Indeed each fixed physical or regulator derivative of a scalar source has a finite regulator-power bound, and the fixed-cone operations on $T$ have the finite estimates above. The required order and power may depend on the derivative or microlocal seminorm. Completion preserves those estimates. Thus $\mathcal P_n\subset\mathcal M_n$ as an actual liquid subobject.

This definition includes every mandatory Gaussian/Wick family, all finite normal derivatives, all277 proper sources, both legal spinneys and the admitted R1 sector. It also includes the accepted scalar power/logarithmic enlargement, rather than asserting that finite poles alone are closed. The scalar coefficient spaces have fixed asymptotic stages through completion; an ambient escaping-index plot is not inserted.

It does not identify $\mathcal P$ with105's entire auxiliary-noise image. That positive-scale envelope admitted arbitrary completed Schwartz-noise amplitudes with a joint noise cone, without an accepted zero-scale contract for all of them. The present analytic sources, their mandatory input maps and their operator closure specify the common class here; no arbitrary auxiliary amplitude is declared asymptotic solely from its membership in that larger envelope.

The filtration is constructed before passing to a boundary. Let $\Lambda$ run over finite collections of the just-defined weighted source stages, including their fixed scalar index families, auxiliary weights, Sobolev orders, normal homogeneities, compact supports, cone bounds and finite insertion/derivative data. Put $F_\Lambda\mathcal P$ equal to the actual evaluated image of their finite direct sum. Enlarge $\Lambda$ by finite joins, including stages with relaxed bounds when needed. These are increasing image subobjects, their filtered union is $\mathcal P$, and equal evaluated families are not distinguished by which stage supplied them. Every declared operation has a finite output collection $\Lambda'$ from the source pullback, density, index and derivative estimates; multilinear operations use a finite join of the input collections. Thus it has a bounded shift in this filtration. This is not convergence in the weaker ambient positive-family topology.

## 5. Strong physical power/logarithmic coefficients

**Lemma108.2 (scalarization before all-vertex pushforward).** Each source(108.7), including its completed coefficient stage, has an intrinsic bounded-below physical power/logarithmic expansion with distributional coefficients. The remainder estimates are strong, uniform on bounded physical test families and bounded coefficient sets. Each fixed derivative of the regulator has the differentiated expansion.

**Proof.** Pair the actual output with a compact smooth physical test $\phi$. Transfer $q_*$ and finite derivatives to the test, obtaining finitely many smooth input test factors. All coordinates and actual densities are retained. On a compact corner chart of the input heat space, the all-vertex map has regulator

$$
\epsilon=b(\rho,v)\rho_1^{a_1}\cdots\rho_l^{a_l},
\qquad b>0,
\tag{108.8}
$$

where $v$ is tangential. This is the all-vertex b-fibration already checked in105.4, including integration of the compact centre. A face-preserving change of one participating radial variable absorbs $b$. Such a change preserves the full corner conormal exclusion of the pulled-back R1 distribution.

The pulled-back R1 coefficient, including its transformed density and the transferred test, is a smooth function of $\rho$ with values in distributions in $v$. The assertion follows from the noncharacteristic restrictions and their derivatives, not from a general assertion that every distributional family has such smoothness. Multiply by the scalar polyhomogeneous source and pair the tangential variables first. Every coefficient and Taylor remainder is then a scalar polyhomogeneous radial function. The estimate for a fixed requested radial derivative and asymptotic depth uses finitely many normal seminorms of $T$, scalar asymptotic seminorms of $a$, and $C^r$ seminorms of $\phi$. It is uniform on bounded sets. The same proof works for finite source jets after transferring their derivatives first and using their smaller partition spaces.

Now apply the scalar monomial-density pushforward argument of105.6 to(108.8). It supplies the powers, logarithmic multiplicities and arbitrarily high remainders, with the actual density shifts. Its finite seminorm estimates compose with the preceding bounds. Each resulting coefficient is therefore a continuous linear functional of $\phi$, hence a distribution. Bounds uniform on bounded physical tests give the strong distributional remainder. Bounds by some finite $C^r$ norm at each requested depth also give a finite negative Sobolev order at that depth. These orders need not be uniform in depth.

The estimates are jointly continuous in the fixed mixed source stages, so they extend to(108.6). They hold for regulator derivatives by the same finite differentiated estimates. If two actual source sums agree, subtract them. Pair with any test, use uniqueness of scalar bounded-below power/logarithmic asymptotics, and conclude equality of every distribution coefficient. Thus these are coefficients of the actual family, not its presentation. $\square$

Write these physical coefficients as $a_{r,l}(u)$ for $\epsilon^r(\log\epsilon)^l$. The finite value on this actual class is

$$
\mathrm{CT}_{\mathrm{phys}}(u)=a_{0,0}(u).
\tag{108.9}
$$

The principal part and evaluated remainder remain distinct from this weaker coefficient map. On087/096's local Schwartz image there are no added logarithms and the coefficients are exactly their admitted moment formula, so(108.9) recovers the historical finite normalization. No proper counterterm is silently changed. The actual positive family is reconstructed before any same-variable product. Rescaling acts on the whole power/logarithmic record by $\log(s\epsilon)=\log\epsilon+\log s$, including the resulting mixing of coefficients.

More explicitly, let $\mathrm{PP}_{\mathrm{phys}}u$ be the finite sum of terms with $r<0$, together with the terms $r=0,l>0$. Local finiteness of the fixed index family makes this sum finite. Then

$$
Z(u)=\bigl(\mathrm{PP}_{\mathrm{phys}}u,
u-\mathrm{PP}_{\mathrm{phys}}u\bigr)
\tag{108.9a}
$$

is an actual subtraction record in the product of distribution-family envelopes, with addition as inverse onto its image. Its remainder has strong limit(108.9). The two record entries need not individually belong to $\mathcal P$: a coefficient such as $P_0$ times an R1 kernel can already be a nonsmooth positive-scale distribution, outside the scalar smooth stages. No claim that $\mathrm{PP}_{\mathrm{phys}}:\mathcal P\to\mathcal P$ is made. The record domain is the evaluated image $Z(\mathcal P)$, and operations reconstruct $u$ before applying the proved actual operations. This is a real-linear record, not an assertion of regulator-linear coefficient extraction or arbitrary multiplication of its singular entries. On the studied source forests, the finite jets of087 remain admitted inputs and its finite-normalized auxiliary counterterms are unchanged.

## 6. The enriched boundary and its nonzero normal-profile comparison

Define in the liquid heart

$$
\mathcal Z_n
=\mathcal P_n/(\mathcal P_n\cap\mathcal I_n^{\mathrm{rap}})
\hookrightarrow\mathcal M_n/\mathcal I_n^{\mathrm{rap}}.
\tag{108.10}
$$

It is an enriched asymptotic boundary, not the fibre of a localized module at an invertible regulator. It retains regulator powers and the distributional normal-profile germ. It is also not the quotient by all families with zero physical power/logarithmic coefficients. The latter quotient would be weaker.

Give it the quotient-image filtration $F_\Lambda\mathcal Z=\mathrm{im}(F_\Lambda\mathcal P\to\mathcal Z)$. Equivalently each level is the image of its weighted actual source modulo its intersection with the rapid subobject. The normal homogeneity and scalar face-index filtrations are retained as these image filtrations, rather than discarded by an unfiltered localization. Their bounded operation shifts descend because the rapid subobject is stable, as proved below. No single homogeneity is assigned to every possible mixed distribution by choosing a presentation.

**Lemma108.3 (full local profile survives).** The map from096's local profile domain to(108.10) kills exactly its regulator-flat Schwartz profiles. Consequently the full formal normal-profile boundary $\mathcal N_d$ of096 maps monically into this enriched boundary after the same compact physical localization. The R1 constant-family map is monic. Both statements hold on every profinite test.

**Proof.** A regulator-flat Schwartz profile and every fixed regulator derivative are rapid in $L^2$ after the finite scaling and weight shifts, hence satisfy(108.3). Conversely let $F$ have first nonzero Taylor coefficient $F_j=f\ne0$ in its Schwartz stage. The actual family has a leading term $\epsilon^{j-d-h}f(y/\epsilon)$. Choose a compact Fourier annulus on which $\widehat f$ has positive $L^2$ mass. This is possible for every nonzero Schwartz $f$, including one with all physical moments zero. On that annulus, after $\xi=\eta/\epsilon$, the squared $H^{-t}$ norm has a lower bound by a nonzero constant times

$$
\epsilon^{2(j-h)+2t-d}.
\tag{108.11}
$$

The higher profile Taylor remainder is smaller there. A cutoff equal to one near the collision changes the term only by a regulator-flat Schwartz tail. Thus no fixed finite $H^{-t}$ order makes the family rapid at every power. This excludes(108.3), for every possible order witnessing the rapid subobject. The same argument after a fixed nonzero compact centre pairing handles centre variables. A nonzero constant-in-regulator R1 distribution has a fixed nonzero negative Sobolev norm, so it is not rapid either.

At a continuous profinite source plot, zero means zero of every actual coefficient section. If one were nonzero at a point, the preceding ordinary lower bound would contradict a local fixed-order rapid lift on an extremally disconnected cover. Conversely regulator flatness is uniform on compact coefficient images by the Schwartz seminorm estimates. Image/kernel descent and091 compactness give the result for arbitrary profinite tests. $\square$

In particular a nonzero moment-flat Schwartz profile is not discarded as a zero physical Laurent series. The exact mixed control105.12 is admitted as $\chi(x)\chi_3(x)\kappa_\epsilon(x)$. Gaussian test Taylor estimates give its strong power expansion and(108.9) is $\delta_0$ with the stated cutoffs. Its negative Sobolev norms have only finite scaling decay, so its enriched boundary is nonzero. No joint regulator-wavefront conclusion, or failure of every signed collar extension, is inferred from that observation.

The comparison also retains the full scalar and finite-jet boundary of105. A scalar family flat at every resolved face is rapid in a fixed finite negative Sobolev order: arbitrarily high face weights absorb each physical derivative, blowdown Jacobian and finite jet loss, because $\epsilon$ is a positive unit times the product of the face defining monomials. Conversely a nonzero scalar face record has a first nonzero power/logarithmic coefficient on some open face stratum. A nonzero corner record cannot arise from an actual coefficient function identically zero on that face's interior. Use105's canonical normal-jet grouping to isolate a maximal support stratum off its smaller intersections and choose a compact angular test, with prescribed finite normal test jets, detecting that coefficient. Near this open face, $\epsilon=b\rho_H^{a_H}$ with $a_H>0$. For each positive regulator the blowdown is a diffeomorphism. Pulling the chosen chart test back to physical variables gives a regulator-dependent physical test whose Sobolev norm of any fixed finite order grows by only a finite power of $\epsilon^{-1}$. The pairing isolates a nonzero leading power/logarithmic term, also with a finite density power. If the family were rapid in any fixed $H^{-t}$, the same pairing would be rapid after that finite test-norm loss, a contradiction. Thus the intersection of the scalar105 image with $\mathcal I^{\mathrm{rap}}$ is exactly its all-face-flat kernel, and its full scalar boundary maps monically to(108.10). This argument is for scalar105 coefficients and finite jets; it does not assume bounded coefficient extraction for arbitrary mixed jet sums.

Normal-rescaling data are explicit, rather than replaced by physical finite outputs. For a partition of normal dimension $d$, use its adapted linear chart $\Theta_{D,\epsilon}(c,u)=(c,\epsilon u)$. Extend the original compact physical kernel by zero before using the linear chart; this introduces no boundary singularity because its physical support is compactly contained in the interval configuration. The rescaled distribution can have expanding support in $u$ and is not claimed to be a global compact-support or Schwartz analytic source.

Here is its precise local codomain. Choose compact cutoffs $\chi_j(c,u)$ exhausting the auxiliary chart, with $\chi_{j+1}=1$ on $K_j=\mathrm{supp}(\chi_j)$. Form the ambient graph stages of section2, with the off-cone part omitted, on each compact $K_j$ and form their rapid quotient. Set

$$
\mathcal G_D=
\varprojlim_j
\left(\mathcal M_{K_j}^{\mathrm{amb}}/
\mathcal I_{K_j}^{\mathrm{rap}}\right).
\tag{108.12}
$$

Transition to level $j$ is multiplication by $\chi_j$. Compatibility follows from $\chi_j\chi_{j+1}=\chi_j$. The objects are liquid images and cokernels as before, and this inverse limit is taken in the liquid heart. Different exhaustions give the same compatible local classes by common refinement; an arbitrary member of the limit is not asserted to be realized by one analytic source. The variables $(c,u)$ are auxiliary relative-coordinate variables of the same model, not a different physical spacetime.

There is now an actual typed map

$$
\mathcal R_{D,h}:\mathcal Z_n\longrightarrow\mathcal G_D,
\qquad
[u]\longmapsto
\left[\chi_j\epsilon^{d+h}
\Theta_{D,\epsilon}^*u_\epsilon\right]_j.
\tag{108.13}
$$

Dilation on each fixed $K_j$, its regulator derivatives and the actual density factors have finite Sobolev power bounds. They preserve moderation and the rapid ideal, and therefore prove(108.13). General heat-corner chart changes are the actual pullback equalities on their overlaps. In resolved charts they have smooth units and finitely many radial monomials in their derivatives; the relation between the regulator and those monomials bounds each requested loss by a finite inverse-regulator power on a compact patch. The same estimates give local quotient maps there. Actual overlap equalities hence persist in these local targets. Joined-partition changes and legal restrictions commute before the quotient and afterwards; no arbitrary distributional trace is being added.

On homogeneous normal-profile stages, the integer $h$ gives the prescribed normalization. Physical normal differentiation shifts $h$ to $h+1$, multiplication by a normal monomial of degree $r$ shifts it to $h-r$, exterior composition adds homogeneities, and same-normal-variable multiplication has the additional dimension shift $d$, as in096. Physical normal integration has its actual dimension/density shift from096; general source projections use105's finite Jacobian and scalar index shifts. These are shifts of the specified image stages and their quotient images. Full scalar face filtrations are retained likewise. The construction never first takes an unfiltered localization and then sets an invertible regulator to zero.

Every curve satisfying(108.3) has zero weak physical power/logarithmic coefficients: pairing a fixed test is bounded by its fixed Sobolev norm times an arbitrary rapid power. Uniqueness in Lemma108.2 therefore makes(108.9), and the entire physical coefficient record, descend to(108.10). The enriched boundary is stronger than that record, as the moment-flat control proves.

## 7. Closed actual operations and boundary descent

**Theorem108.4 (mixed operator-domain closure).** The actual image $\mathcal P$ is closed under the typed Gaussian/Wick operations of105, with all fixed finite decorations, legal partition-jet insertions, proper physical vertex projections, legal disjoint composition and semilinear scale transport. Each operation preserves $\mathcal P\cap\mathcal I^{\mathrm{rap}}$ and hence induces an operation on the enriched boundary(108.10). Its physical coefficient comparison is intrinsic and agrees with087 on that historical subdomain. The theorem does not assert BV identities or quantum factorization identities on this boundary.

**Proof.** At positive regulator use the exact integral normal-form operations105.3. A scalar output multiplier pulls back along $q$ to the input scalar stage. The heat map is an interior b-map by105.4, so scalar power/logarithmic pullback has the accepted finite stage and remainder bounds. A physical projection composes $q$. For a legal output partition restriction, its preimage under a vertex-forgetting map is again a partition subspace; the corresponding base change restricts the original R1 coefficient noncharacteristically. Finite normal derivatives produce a finite full Leibniz sum. A source jet factors through its smaller partition configuration and target diagonal inclusion, retaining finite normal order and every derivative of the complement. This is exactly the typed finite-jet factorization of105.6. Self-restrictions and overlapping counterterm products are excluded.

Disjoint composition gives the joined R1 coefficient cone and the scalar product stage. Since physical opens are disjoint, no cross-collision conormal meets the support; this is the actual R1 operation069.3. Other coefficient products require both the fixed-cone noncharacteristic condition and the R1-admissible resulting coefficient cone specified in section4. Their coefficient maps have finite bilinear estimates in section3 and scalar index/remainder estimates from105.6. The continuous coefficient maps induce maps of completed projective tensor sources by their finite product-seminorm bounds and the universal property of that tensor product. Thus all source sums remain in $\mathcal P$; no finite-separable decomposition of a completed coefficient is assumed. Regulator derivatives, Laurent factors, physical derivatives and polynomial decorations change only finite stage indices and derivative orders. Scale transport rescales the actual family, preserves finite-order rapidness and uses the full logarithmic binomial rule.

Now take a negligible input. On any fixed spatial cone stage admitting the specified operation, Lemma108.1 upgrades it to rapidness in every finite normal seminorm needed by that operation, with one finite Sobolev order for each derivative. Its finite operator estimate loses only a fixed regulator power. The output is therefore rapid in a finite-order norm for each derivative. For multilinear operations apply the finite Leibniz expansion; each term contains a negligible factor and moderate remaining factors. For finite source-jet insertion, use its actual submersion pullback, admitted complement product and proper pushforward; the estimates apply to the whole distribution, including summed cancellations. No recovery of a source coefficient from a negligible mixed sum is assumed. Thus every stated operation preserves the ideal. This proof applies to the actual input curve and its intrinsic admissible operator domain, independently of a chosen source expression for that negligible curve.

Positive-scale operations already preserve equality of actual evaluated families. The rapid ideal and its image are likewise defined on those actual curves. Hence these operations descend first through actual evaluation and then through(108.10). For a general profinite section lift to complete stages on an extremally disconnected cover, use the uniform estimates and compactness to obtain finite source stages there, and descend through actual equality. No graph label, arbitrary-profinite projectivity, or point detection on an arbitrary internal Hom is used. The physical coefficient comparison follows from Lemma108.2 and its vanishing on the ideal. $\square$

This proof uses the mixed analytic image, not the whole ambient moderate-curve object. An arbitrary moderate curve need not have power/logarithmic coefficients or a finite physical value. The finite evaluation map is claimed only on $\mathcal P$ and its boundary. This prevents a vacuous enlargement that supplies operator stability while losing the renormalization comparison.

The marked Wick-to-delta conversion is also an actual operator on this domain. For the fixed marked difference $t=x_5-x_4$, define multiplication by $R_\epsilon(t)=\kappa_\epsilon(t)/P_\epsilon(t)$. Convexity and evenness give $P_1(t)\ge P_1(0)>0$, so $R_\epsilon(t)=\epsilon^{-2}R_1(t/\epsilon)$ with $R_1=\kappa_1/P_1$ a Schwartz function. All physical and regulator derivatives have finite polynomial regulator bounds. Its lifted scalar kernel belongs to105's scalar stages, so the multiplier preserves $\mathcal P$ and the rapid ideal. On an actual marked input $P_\epsilon(t)G_\epsilon$ its output is exactly $\kappa_\epsilon(t)G_\epsilon$. The marked difference is the specified operator datum, while equality and regulator allocation of the full input remain actual kernel equality. This conversion does not replace the full tangent derivative identity, whose mixed terms are still present.

## 8. Parameters, controls and remaining obligations

For manifold parameters prescribe a separate graph-jet enrichment: on each compact parameter chart, every parameter derivative $\partial_a^\alpha\partial_\epsilon^k$ has its own fixed finite Sobolev order and polynomial regulator bound, together with the corresponding fixed-cone seminorm bounds and scalar asymptotic stage. Derivative compatibility is imposed distributionally. Rapid graph stages require uniform rapidness for every such derivative. This allows the derivative orders of a curve such as a translated delta to grow; it does not incorrectly demand one Hilbert space containing all its derivatives. Original R1 Bastiani plots satisfy these conditions because each compact derivative image has bounded distribution order and fixed normal cone. The same finite chain and product estimates prove preservation by the stated operations and their parameter derivatives. This is the declared restricted enrichment, not a universal smooth enrichment of all liquid modules, and does not prove the M5 connection/descent comparisons.

The following controls are structural parts of the proof:

- Actual regulator reallocations give identical families before either quotient; coefficient extraction is real-linear and regulator action is reprojected.
- Full profile information survives(108.11), including a nonzero Schwartz profile with all moments zero. Strong physical flatness is not the rapid ideal.
- Exact105.12 is handled with spatial distribution orders and regulator derivative sequences, without a joint signed-collar wavefront inference.
- The scalar logarithm102 is admitted by the scalar power/logarithmic stages. The theorem does not claim that every actual Gaussian/Wick formula forces a logarithm or that its finite-pole subspace is closed.
- The marked identity $P_\epsilon''=\kappa_\epsilon$ and the full tangent identity105.5 hold on actual families, so pass to the enriched boundary. Both mixed derivative terms remain present.
- All277 sources, both disjoint spinneys, normal derivatives, Wick bridges and disconnected Gaussian backbones enter through the admitted scalar105 stages. Their unchanged nonzero even-rank finite controls remain087's exact values.
- Units at arity zero, actual densities under projection and semilinear scale transport are retained. No multiplication of overlapping singular counterterms occurs.

The submitted theorem is closure and comparison for this declared mixed domain. Establishing $Q_{\mathrm{ren}}$, $[d,\Delta_{\mathrm{ren}}]=0$, $\Delta_{\mathrm{ren}}^2=0$, quantum locality/coherence, scheme compatibility and the full original GB2 acceptance conditions remains M3. R3 is independent and unresolved; no degree-two inference follows from this construction. Extended Weiss descent and the typed final integration remain M5. Original R2, R3, R4 and both parents are not closed by this candidate.

The precise M2 clause adjudication is therefore as follows, subject to final corrected-source review and protected admission.

| M2 requirement from090 | Construction and exact boundary |
| --- | --- |
| Compact-localized normal profiles with regulator bounds |105 scalar stages and108.3 full local normal-profile injection; actual cutoff and derivative estimates |
| Separate regular R1 sector | Constant-family liquid map into $\mathcal P$ and monic map into $\mathcal Z$, preserving the declared original plots |
| Collision jets, sources and legal forest operations |108.4 typed operators, full complement derivatives, all277 sources and both legal spinneys; no overlapping counterterm products |
| Full collision arrangement and corner compatibility |105 heat geometry, actual source pullback identities and local quotient targets(108.12)–(108.13) |
| Filtration before boundary specialization | Source images $F_\Lambda\mathcal P$, quotient images $F_\Lambda\mathcal Z$ and prescribed normal homogeneity/index shifts |
| Nonzero enriched boundary retaining normal data |108.3 and the full scalar105 boundary injection, including moment-flat profiles and arity-zero unit |
| Separate physical finite evaluation recovering087 |108.2–108.9, vanishing on the rapid ideal and actual subtraction record108.9a; no finite-output multiplicativity or regulator-linear extraction |
| Actual operator descent on liquid parameter families | Fixed-order saturation and finite operator estimates, completed source bounds and all-profinite actual-equality descent |

These clauses meet the M2 domain/comparison exit on the declared mixed analytic class. They do not identify that class with the whole arbitrary-noise envelope105 or the whole broader collar image099. Neither a quantum structure nor a derived comparison is a clause of this M2 conclusion.

This is one primary attempt. The saturation lemma and the all-vertex scalarization proof are the new mechanisms beyond105. The single correction after distinct non-author109 renames the rapid subobject, specifies the local normal-profile codomains and actual corner maps, and records source/quotient image filtrations and the M2 clause table. Its primary source remains preserved. Final exact-source readback and protected admission are separate obligations. No numerical fixture is supplied: finite algebra has not changed, and the new statements are infinite-dimensional analytic and categorical assertions requiring proof. Local gates, source freeze, protected merge/readback and explicit tracker reconciliation remain separate obligations.
