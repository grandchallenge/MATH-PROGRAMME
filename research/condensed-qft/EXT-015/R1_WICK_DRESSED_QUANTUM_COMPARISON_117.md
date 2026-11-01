# EXT-015 REACH / 117 — an actual Wick-dressed quantum map from R1

**Disposition: positive typed comparison candidate, not an equivalence.** This constructs an actual real-liquid source for the admitted R1 model, compares its profinite families with the original fixed normal sectors, and defines a smooth natural quantum cochain map into111's enriched model. Matching Wick disjoint maps commute by their typed formulas. Matching ordinary disjoint maps require, and receive, a separate Gaussian cross-kernel estimate. The map is termwise monic; no general cohomology-injectivity claim follows. Its total-weight-zero cone remains114's nonzero unit cone. Review118 and ledger119 are separate.

## 1. Category, frozen inputs and prescriptions

Work in the real liquid heart $\mathcal A=\mathrm{Liq}_p(\mathbb R)$, for fixed $0<p\le1$, in ZFC, on the existing interval basis and one-dimensional free-scalar model. The input cut is039abcffbb307df20853898c76f086db07658a70 on `research/reach-r1-comparison-input-frozen-20261031`; CP075 binds this attempt.

| Scientific input | Exact Git blob |
| --- | --- |
| Protocol090 |6b642bf10c3328bb64d37474e290810fb45cbca1 |
| R1 locally normal model069 |b3f6fe6651cc1ea59dfdf5f52990576c4f7018c2 |
| Its review070 |01f4911bea83eeac9dfb232e7dd4b9550648639f |
| R1 uniform endpoint077 |4fb34ef83a822f80b4bf107a6964f98345fd0b63 |
| Its review078 |bbd598c8d9f1622f24c30978cc42ecc912b6ed23 |
| Mixed enriched domain108 |587c15fd6e24f6e6b14de574ff878221cdbd5cb6 |
| Its review109 |5a18d43990fdc20fd67384ad74fb7ff2651ec181 |
| Enriched quantum theorem111 |b7b1e5f970904d6e7de065a4fedd382e212a3022 |
| Its review112 |f1c2053d25c71bac169432bb28a7c91819d89147 |
| Unit comparison114 |ee4bfb46c5565b90d6f9015765edc8a773b0997a |
| Its review115 |ffefc5f6cf770e0d9e7492636e057a7f39dd40d2 |
| Unit acceptance116 |1081ab434ed49309a763d5a119c2d88554ca0742 |

The source R1 operators are their admitted zero-scale operators: $B_0$ contracts even pairs with $P_0(t)=|t|/2$, $\Delta_0$ contracts even–odd pairs with $\delta_0(t)$, and $Q_{R1}=d+\hbar\Delta_0=W_0dW_0^{-1}$, with $W_0=\exp(\hbar B_0)$. The source disjoint structure actually chosen in069.3–069.4 is Wick-conjugated. Its ordinary disjoint maps are a second, separately typed prescription.

The positive-regulator mollifier in077 is compactly supported. This return uses077 only for the accepted zero-scale operators, their normal-sector continuity and their source Wick convention, all independent of that positive mollifier. It does not replace077's positive-scale family by a Gaussian. The target Gaussian family and rapid-ideal bounds are108/111; the new off-diagonal Gaussian estimate is proved in section6.

## 2. A real-liquid R1 source with the original families

For compact $K\Subset U^n$ and closed admissible cone $\Gamma$, let $E_{K,\Gamma}^{N}$ be the original069.1 normal sector. Admissible means avoidance of every nonzero partial-partition conormal, including simultaneous collisions. Choose the complete Sobolev graph refinements of108.1,

$$
E_{s,K,\Gamma}
=H^{-s}_K\cap\bigcap_{j,m}\{T:A_jT\in H^m\},
\tag{117.1}
$$

with the fixed off-cone cutoff system and its graph topology. Define before using the target

$$
\mathcal C_n^{R1}(U)
=\mathop{\mathrm{colim}}_{K,\Gamma,s}
\underline{E_{s,K,\Gamma}},
\tag{117.2}
$$

with finite graded parity sums and the finite permutation projector as required. Supports, cones and finite orders are enlarged by finite joins. This is an actual liquid object, not the definition of the source as the image of a target map. Each graph space is complete Fréchet, hence has the admitted liquid realization. No nuclearity of those graph spaces is asserted.

**Lemma117.1 (source-family comparison).** For each fixed $K,\Gamma$, the filtered liquid union of(117.1) has precisely the continuous profinite families into $E_{K,\Gamma}^{N}$. The source's manifold plots may therefore be specified as the original locally normal069 plots, with their original parameter connection. This assertion does not identify them with plots of a global locally convex inductive limit.

**Proof.** The graph refinement maps continuously to the normal sector: its negative Sobolev norm controls strong distributional seminorms on bounded tests, and its off-cone Sobolev norms control the normal Fourier seminorms after a finite extra derivative loss. Conversely let $T\to E_{K,\Gamma}^{N}$ be a continuous family on a profinite parameter space. Its compact image is bounded in distributions, with common support and uniformly finite distribution order. Sobolev embedding bounds it in some $H^{-s_0}$. Lose a further finite order so that the compact-support Sobolev inclusion is compact. Distributional continuity and uniqueness of distributional limits then imply continuity into the weaker $H^{-s}$: a net has relatively compact Sobolev image, and every possible limit is the designated distributional limit. The normal topology also supplies continuity of every off-cone $A_jH^m$ seminorm. Thus the entire profinite family lifts to one graph refinement.

These two constructions are inverse on the actual distributions and their concrete families. Compactness of the profinite free liquid object in the abelian heart supplies a finite refinement for filtered-union sections; it supplies no arbitrary-profinite projectivity. Taking finite support/cone joins gives the same assertion for(117.2)'s declared finite-sector profinite families. The original locally normal manifold plots are locally Bastiani-smooth into $E_{K,\Gamma}^{N}$. Keep exactly that restricted source plot rule. Graph bounds for their derivatives will verify the target comparison below; no universal liquid-to-DVS functor is introduced. $\square$

For a manifold plot one cannot in general choose a single negative Sobolev order containing every parameter derivative. On each compact parameter chart, each derivative image is bounded in the same normal sector, so has its own finite order. Retain the sequence of those orders, as in108's graph-jet enrichment. This is compatible with the original locally normal plots and does not enlarge them by declaration.

The ordinary disjoint products also have actual liquid typing. On fixed graph sources with nonnegative orders $s_1,s_2$, exterior tensor product has the global estimate

$$
\|T\boxtimes S\|_{H^{-(s_1+s_2)}}
\le\|T\|_{H^{-s_1}}\|S\|_{H^{-s_2}}.
$$

For a fixed output microlocal cutoff outside069.4's product cone, a finite conic partition separates regions where one input is off its cone and its frequency is comparable to the total frequency. Weighted Fourier Cauchy–Schwarz bounds the requested output off-cone Sobolev norm by finitely many products of an input off-cone seminorm and the other input's fixed negative Sobolev norm. Compact physical cutoffs and their smoothing remainders have the same finite bounds, as in108 sections3–4. Thus each fixed pair of graph stages maps jointly continuously to an output graph stage; on disjoint supports069.3 makes its cone admissible. This gives a condensed bilinear map, hence a liquid bilinear map by the liquid tensor adjunction. It assumes neither nuclearity of the graph spaces nor a tensor identity for their spaces of sections. On the original manifold plots, smoothness is the separate hypocontinuity argument of069.2. Finite symmetrization preserves both constructions.

The classical differential is a liquid map on(117.2): it is a finite sum of physical derivatives and parity changes, with a finite graph-order shift. Use the original total weight $w=n+2k$, $n,k\ge0$, and form

$$
\widehat{\mathcal C}_{R1}^{\mathrm{cl}}(U)
=\prod_{w\ge0}\ \bigoplus_{n+2k=w}
\hbar^k\mathcal C_n^{R1}(U).
\tag{117.3}
$$

Give it the componentwise original restricted plots. This is the liquid source with the finite-weight and formal-completion conventions of069. It is not a claim that the refuted global R1 inductive topology is complete or regular.

## 3. Finite joint graph bounds for the source Wick operator

**Lemma117.2.** Each zero-scale contraction $B_0$ or $\Delta_0$ maps a fixed graph source(117.1) continuously to one fixed output graph sector $E_{t,K',\Gamma'}$, with finite $t$, projected compact support and an admissible output cone. Every finite weightwise composition, including $W_0^{\pm1}$, has finite such bounds.

**Proof.** The fixed normal-sector multiplication and proper-pushforward theorem035, used in069/077, gives a continuous linear map $E_{K,\Gamma}^{N}\to E_{K',\Gamma'}^{N}$. The input cone excludes the pair conormal; the full partition exclusion gives the admissible output cone by the accepted035/077 calculation. Restrict to the Fréchet source(117.1).

There is also a finite negative Sobolev bound, which is needed to land in one graph stage rather than only pointwise in its union. For this source Fréchet space $E$, let $L$ denote the contraction. The closed sets

$$
\{T\in E:\|LT\|_{H^{-t}}\le l\},
\qquad t,l\in\mathbb N,
\tag{117.4}
$$

cover $E$, since every individual compactly supported output distribution has finite order. Closedness follows from continuity into distributions and weak compactness of compact-support Hilbert balls. Baire's theorem makes one such set have interior. Subtract two elements and use linearity to obtain a zero-neighborhood bound, hence an $H^{-t}$ bound by finitely many input graph seminorms. Each output off-cone seminorm is already continuous by the normal-sector theorem and is likewise bounded by finitely many input graph seminorms. Together these are continuity into $E_{t,K',\Gamma'}$.

At any fixed total weight there are only finitely many arities, contraction choices and powers in each Wick exponential. Compose these fixed-stage estimates and take finite unions of the output supports and admissible cones, and sufficiently large finite orders. The resulting maps remain continuous and preserve the original normal-sector plots. $\square$

For manifold plots, $L\partial_a^\alpha T=\partial_a^\alpha LT$ in the original normal sectors. On each compact parameter set apply the preceding estimates with the finite source order available for that derivative. This gives the target graph-jet derivative-order sequence, not a false common Hilbert order for all derivatives. For profinite families the same fixed-stage maps apply to their actual lifts from Lemma117.1. The finite Reynolds projector is continuous throughout.

## 4. Classical inclusion and the actual dressed cochain map

Let $\widehat{\mathcal O}_{\mathcal Z}^{\mathrm{cl}}$ be111's underlying enriched weighted object with classical differential $d$. The map

$$
i_{\mathrm{cl}}:
\widehat{\mathcal C}_{R1}^{\mathrm{cl}}\longrightarrow
\widehat{\mathcal O}_{\mathcal Z}^{\mathrm{cl}}
\tag{117.5}
$$

sends a distribution to its constant actual regulator family and then takes the108 boundary class. On a graph source this is its actual mixed coefficient source tensored with the scalar unit. It is continuous and liquid-linear. It commutes with $d$, interval extension by zero, and ordinary disjoint exterior composition. It is termwise monic: a nonzero constant distribution cannot be rapid in any fixed finite Sobolev norm. On arbitrary profinite tests this is checked after an extremally disconnected lift of the target rapid image, using the concrete source graph families and descent. It is not deduced from point detection on an arbitrary target internal Hom.

For $s>0$ let $B_{\mathcal Z,s}$ use the target Gaussian $P_{s\epsilon}$, and set $W_{\mathcal Z,s}=\exp(\hbar B_{\mathcal Z,s})$. The target operators, record interpretation and rapid-ideal preservation are108/111. On compact $s$ intervals inside $(0,\infty)$ their differentiated kernels have the same finite-stage estimates. Define the typed composition

$$
J_s=W_{\mathcal Z,s}\ i_{\mathrm{cl}}\ W_0^{-1}:
(\widehat{\mathcal C}_{R1},Q_{R1})
\longrightarrow
(\widehat{\mathcal O}_{\mathcal Z},Q_{\mathcal Z,s}).
\tag{117.6}
$$

The three maps respectively have domains source quantum to source classical, source classical to target classical, and target classical to target quantum. No subtraction $B_{\mathcal Z,s}-B_0$ is defined as an operator on the entire target. In particular(117.6) is not shorthand for an unproved global exponential of that difference.

**Theorem117.3 (actual quantum comparison).** Formula(117.6) is a natural real-liquid quantum cochain map, smooth for the original locally normal source parameters and108's specified target graph-jet parameters. It is termwise monic on graded cochain objects, preserves total weight and has bounded source/normal filtration shifts at each fixed weight. It is natural under interval inclusions and has the projected support bounds of its finite contraction terms.

**Proof.** Lemmas117.1–117.2 define $W_0^{-1}$ on the actual source. The actual classical inclusion and108/111 define the other two maps. Every finite-weight formula is a finite sum of continuous maps between complete source/target stages or their actual images; it therefore gives the asserted liquid morphism and parameter bounds. Image or rapid quotient lifts, when needed on a general profinite test, are taken on an extremally disconnected cover and use finitely many stages by compactness. Equality of actual distributions and rapid-equivalent target families descends, since all target operations preserve that ideal. No graph presentation is retained as input data.

The cochain identity is the typed calculation

$$
Q_{\mathcal Z,s}J_s
=W_{\mathcal Z,s}d\,i_{\mathrm{cl}}W_0^{-1}
=W_{\mathcal Z,s}i_{\mathrm{cl}}dW_0^{-1}
=J_sQ_{R1}.
\tag{117.7}
$$

The target quantum identities here hold on the actual rapid quotient by111, not merely on positive-regulator records. In record coordinates all target operations reconstruct the actual sum before contraction and reproject the counterterm/remainder pair afterwards.

Both Wick operators are degree-zero automorphisms of their respective underlying graded weighted objects. The middle map is monic, so $J_s$ is termwise monic. Products preserve monomorphisms by their left-exact universal property; no assertion of exactness of arbitrary infinite products is needed to pass to(117.3).

Each contraction lowers arity by two and gains one power of $\hbar$ in a Wick exponential. Thus every term preserves $w=n+2k$, and at source arity $n$ has at most $\lfloor n/2\rfloor$ total contractions. Finite graph-order losses, source supports and cone enlargements are those of Lemma117.2; target normal homogeneities, density powers and scalar index shifts are those of108/111. These give a finite output source collection for every fixed finite input collection and weight quotient. No common scalar homogeneity is assigned to every mixed R1 kernel.

Contraction only deletes slots, so an output term's support is contained in the corresponding projection of the source compact support. The same global kernels $P_0$ and $P_{s\epsilon}$ commute with extension by zero under interval inclusions, because each input support is compact inside its open. Coefficient extraction and target rapid passage do not enlarge those supports. This proves support/inclusion naturality. Source parameter derivatives commute with the fixed linear source operators; their compact derivative images have the order sequences already discussed. Target mixed parameter derivatives obey the finite Leibniz estimates of108. This proves the stated smoothness without a universal liquid-to-DVS realization. $\square$

Termwise monicity is not cohomology injectivity: a source cycle can in principle acquire a primitive outside the source image. No such injectivity assertion is made.

A concrete smooth R1 input checks that the dressing is necessary. In coordinates $c=(x+y)/2$, $t=x-y$, whose density determinant has absolute value one, take one even and one odd slot with kernel $a(x,y)=\chi(c)\phi(t)$. Choose $\int\chi=1$ and $\phi(t)=\eta(t)(1+t^2)$, with an even compact cutoff $\eta=1$ near zero and supports small enough to lie in $U^2$. Then

$$
\Delta_0a=1,\qquad
\Delta_{s\epsilon}a=1+s^2\epsilon^2+v_{s,\epsilon},
\qquad v_{s,\epsilon}\text{ rapid}.
\tag{117.7a}
$$

The equality uses the exact Gaussian second moment; the cutoff error and all its regulator/scale derivatives are rapid. Thus the constant-family inclusion has quantum cochain defect $\hbar(s^2\epsilon^2+v_{s,\epsilon})$, which is nonzero in the target scalar boundary by114. A term of order $\epsilon^2$ is not identified with a rapid family.

There is no even pair in $a$, so $J_sa=i_{\mathrm{cl}}a$. But $da$ has two even slots, and the source and target Wick corrections give the exact identity

$$
J_s(da)=i_{\mathrm{cl}}(da)
+\hbar\bigl(\Delta_{s\epsilon}a-\Delta_0a\bigr).
\tag{117.7b}
$$

Together with $J_s(\hbar\Delta_0a)=\hbar\Delta_0a$, this cancels the defect and verifies(117.7) on the witness. The physical derivative of the kernel is the full expression $\partial_y^2a=\chi''\phi/4-\chi'\phi'+\chi\phi''$. Distributional integration by parts gives the contractions just used; it does not discard the centre derivative or mixed term before applying the operator. This is an exact sign/domain check, not a new numerical fixture.

## 5. The matching Wick disjoint maps

Use the actual source and target prescriptions

$$
\mu_{R1}^{W}=W_0\mu_{R1}^{\mathrm{ord}}\bigotimes_iW_0^{-1},
\qquad
\mu_{\mathcal Z,s}^{W}
=W_{\mathcal Z,s}\mu_{\mathcal Z}^{\mathrm{ord}}
\bigotimes_iW_{\mathcal Z,s}^{-1}.
\tag{117.8}
$$

For disjoint $U_1,\ldots,U_r\subset V$, the classical inclusion intertwines the ordinary exterior maps. Substitute(117.6) and(117.8), with the operator at each indicated open. Cancelling only typed neighboring inverse maps gives

$$
J_{s,V}\mu_{R1}^{W}
=\mu_{\mathcal Z,s}^{W}\bigotimes_iJ_{s,U_i}.
\tag{117.9}
$$

Every cancellation is within the source or within the target, never between an undefined source $B_0$ and a target operator. All maps are finite on weight quotients and smooth there. Source/target associativity, graded equivariance, unit and nested disjoint diagrams then give the corresponding coherent comparison diagrams. This proves compatibility with the Wick prescription actually used in069/077.

Ordinary multiplication does not follow from those cancellations alone. Wick and ordinary maps differ by nonzero cross-propagator contractions on disjoint inputs. Section6 supplies the independent comparison needed for the matching ordinary prescription.

## 6. Gaussian cross-difference and matching ordinary composition

**Lemma117.4 (all-derivative cross flatness).** Fix disjoint compact physical supports and a compact scale interval $s\in[s_{\min},s_{\max}]\Subset(0,\infty)$. If the paired coordinates have separation $|t|\ge\delta>0$, then for every fixed spatial, regulator and scale derivative,

$$
\left|\partial_t^a\partial_\epsilon^b\partial_s^c
\bigl(P_{s\epsilon}(t)-P_0(t)\bigr)\right|
\le C\epsilon^{-M}\exp\bigl(-\delta^2/(C'\epsilon^2)\bigr).
\tag{117.10}
$$

Hence those kernels are rapid multipliers, uniformly on the stated support/scale sets, for every admitted moderate input and every fixed parameter derivative request.

**Proof.** With $\sigma=s\epsilon$ and the standard Gaussian density $\varphi$, write for $t\ne0$

$$
P_\sigma(t)-|t|/2
=\sigma\varphi(|t|/\sigma)
-|t|\,\overline\Phi(|t|/\sigma),
\tag{117.11}
$$

where $\overline\Phi(a)=\int_a^\infty\varphi(v)\,dv$. Its Gaussian tail bound, and its differentiated formulas, give(117.10). For at least two $t$ derivatives the same assertion is immediate from Gaussian derivatives of $P_\sigma''=\kappa_\sigma$; the zeroth and first use(117.11). Mixed $\epsilon,s$ derivatives introduce only finitely many powers of $\sigma^{-1}$ and $t/\sigma$ on the fixed compact physical support. The lower and upper scale bounds make their constants uniform. Exponential decay absorbs every requested inverse regulator power.

Multiply by a fixed compact cutoff avoiding $t=0$ and equal to one on the paired support. Every requested multiplier seminorm is therefore rapid. The finite Sobolev/normal operator estimates of108, including the finite Leibniz terms for regulator and manifold-parameter derivatives, multiply it by at most a fixed polynomial regulator loss. Proper projection preserves rapidness. This proves rapid output with one finite Sobolev order for each derivative, as required by the actual ideal, rather than only scalar pointwise smallness. $\square$

This is an off-diagonal statement. $P_{s\epsilon}-P_0$ is not asserted to be globally Schwartz: $P_0$ has a cusp at zero. The difference of two positive-scale smooth Wick kernels has a different global Schwartz statement, already used in111.

**Proposition117.5 (matching ordinary maps).** The same $J_s$ also obeys

$$
J_{s,V}\mu_{R1}^{\mathrm{ord}}
=\mu_{\mathcal Z}^{\mathrm{ord}}\bigotimes_iJ_{s,U_i}
\tag{117.12}
$$

for the matching ordinary disjoint prescriptions, on their stated quantum complexes.

**Proof.** Work at a finite output weight with labeled input groups supported in the fixed disjoint opens. Decompose the even pair contractions in each finite Wick matching into internal pairs within an input group and cross pairs between groups. Cross $P_0$ contractions are defined on this target sector too: a cutoff away from zero makes that cross kernel an ordinary smooth multiplier on the joint support. This is not an operator $B_0$ on arbitrary target kernels.

The source and target internal contractions are just their respective Wick operators on the separate inputs. The finite matching identity separates the joint exponential into its commuting internal and cross contributions. Moving the source cross contribution through the constant-family inclusion is legitimate because it is the same smooth cutoff kernel on the separated support. By Lemma117.4 its difference from each target Gaussian cross contribution is rapid. Every term of the finite difference of the corresponding cross matching sums contains at least one such rapid cross kernel. All remaining contractions are admitted moderate operations and preserve that ideal by108. Thus the two cross exponentials cancel in the boundary comparison. The remaining internal terms are exactly the two sides of(117.12).

The argument applies after every fixed parameter derivative and regulator derivative by Lemma117.4, and remains finite on each output weight. Completion is by those same weight quotients. The source ordinary maps are quantum cochain maps on disjoint supports because the delta cross-contractions vanish exactly. The target ordinary maps are quantum cochain maps because the Gaussian cross-contractions are rapid, as111.3 proves. This supplies their quantum typing independently of the Wick calculation. $\square$

Equations(117.9) and(117.12) concern matching prescriptions. They do not identify ordinary and Wick multiplication. Even linear deltas at separated points have a nonzero cross $P_0$ pairing, so that stronger assertion would be false. Nor does this proof multiply overlapping source counterterms or admit an arbitrary overlapping R1 product.

## 7. Smooth scale transport and the cochain connection

All assertions here are local on compact $s$ intervals in $(0,\infty)$, with a common sufficiently small regulator interval. They do not define $B_0$ on the whole target by taking $s=0$.

The parameter domain is the admitted joint source graph-jet enrichment of108 section8: local lifts have the stated uniform support, cone, scalar-stage and Sobolev bounds for every mixed parameter/regulator derivative, and null lifts are rapid graph jets with uniform rapidness for every such derivative. Parameter differentiation preserves these null relations, so the displayed operators descend on this declared family domain. Pointwise rapidness at each parameter value alone is insufficient. No assertion is made that every manifold-valued family in an abstract liquid quotient admits these lifts, or that this constructs a universal liquid-to-DVS connection.

Let

$$
T_{s,t}=W_{\mathcal Z,t}W_{\mathcal Z,s}^{-1}.
\tag{117.13}
$$

The actual target scale theorem111 gives its cochain and factorization transport, and the typed formula immediately gives $T_{s,t}J_s=J_t$. The source is the constant $Q_{R1}$ family. The compatible target scale connection is

$$
\nabla_s
=W_{\mathcal Z,s}\partial_sW_{\mathcal Z,s}^{-1}
=\partial_s-\hbar B_{\partial_sP_{s\epsilon}}.
\tag{117.14}
$$

The notation on the right is an even two-even contraction with the differentiated kernel. The Gaussian identity is

$$
\partial_sP_{s\epsilon}(t)
=s\epsilon^2\kappa_{s\epsilon}(t).
\tag{117.15}
$$

It follows from Gaussian integration by parts in the defining convolution, or from $\partial_\sigma P_\sigma=\sigma\kappa_\sigma$. The kernel and all its fixed derivatives have the admitted scalar-stage bounds uniformly on the compact scale interval. Its operator preserves the rapid ideal by108. Since all even constant-kernel contractions commute, differentiating the finite weightwise Wick exponential proves(117.14). Thus $[\nabla_s,Q_{\mathcal Z,s}]=0$ and

$$
\nabla_s(J_sf)=J_s(\partial_sf)
\tag{117.16}
$$

for scale-dependent source sections. In particular each constant source section maps to a horizontal target section. The transport(117.13) is its horizontal transport and satisfies the strict cocycle. Ordinary source manifold derivatives commute with $J_s$; their joint derivatives with(117.14) satisfy the finite graph-jet bounds already established. Target record formulas use the actual reconstructed family and reprojected entries, rather than an independent action on an inadmissible pole component.

The factorization transport imported from111 is its matching Wick prescription. For matching ordinary disjoint maps, apply Lemma117.4 to $P_{t\epsilon}-P_{s\epsilon}$ and its derivatives by subtracting the two off-diagonal differences from $P_0$. Every cross term in the finite transport-matching difference is rapid, by the proof of Proposition117.5. This proves ordinary disjoint transport compatibility too. Differentiating those finite identities gives the connection Leibniz rule on the same admitted disjoint family domain.

## 8. Unit cone, exact limitations and provenance

At total weight zero the source is $R[0]$, both Wick operators are the identity and(117.6) is exactly the unit $u:R\to\mathcal Z_0$. Its cone is the nonzero $K_{\mathrm{unit}}[0]$ of114, containing $A/R$. Consequently this particular strict weight-preserving comparison is not a quasi-isomorphism. Its full cone has that weight-zero cone as a split factor by the finite binary weight-zero/tail decomposition. This does not require exactness of an arbitrary infinite product.

The theorem establishes an actual natural quantum comparison arrow, not equality of the two domains, cohomology injectivity or a weightwise equivalence. It does not identify the real scalar unit with the larger retained scalar coefficient object. A comparison relative to a declared larger coefficient algebra is a different problem and receives no automatic base-change or flatness theorem here.

The corrected scalar field-source bridge026 concerns the full compact distributional classical field dual, whereas the present source is the proper admitted R1 microlocal domain. No map from every026 field-dual kernel to R1, and no universal liquid/DVS realization, has been supplied. The target's extended completed Weiss descent, the remaining typed integration cones, smooth/connection comparisons outside the declared graph parameters and cofibration/fibration obligations remain M5 work. The existence of $J_s$ does not transfer all those statements from the source by monicity.

R0/R1 and original R2 retain their completed reviewed scopes, and separate087–089 retains its historical finite normalization. All mandatory source jets and both spinney choices remain inside the target domain; this comparison adds none of the forbidden overlapping counterterm products. R3 and its actual degree-two equation remain independent and open. R4, full M5 and both parents remain open. No new opposed R3 cycle or new physical objective is inferred from this arrow.

This is one primary bounded construction by a delegated same-system context with substantive source/typing and Gaussian-estimate input from the parent. Distinct non-author118 must check the actual source-family theorem, finite joint graph bounds, the separately proved ordinary cross calculation, scale connection and scope before acceptance. No numerical fixture is supplied: the new claims are analytic/categorical maps and finite contraction identities. No Python, Git, tracker or external mutation was performed to prepare this draft. Source freeze, one correction, required gates, protected admission/readback and tracker reconciliation remain separate.
