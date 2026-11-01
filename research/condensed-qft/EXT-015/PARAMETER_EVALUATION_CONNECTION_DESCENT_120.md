# EXT-015 REACH / 120 — parameter differentiation does not descend through point evaluation

**Disposition: negative candidate for the exact evaluated-family contract; critical review121 pending.** There is a joint family in117's admitted analytic/source class whose evaluated enriched class is zero at every parameter value, while the evaluated derivative is nonzero. The coefficient curve is smooth in one fixed complete R1 graph space. Thus the failure does not exploit escaping Sobolev orders, scalar index families or an arbitrary ambient moderate example. The existing connection on the joint-family quotient and its source-controlled R1 image survives. This is not a prohibition of every differentiable-sheaf realization or a programme closeout.

## 1. Category, frozen contract and sources

Work in real liquid modules for fixed $0<p\le1$, in ZFC, on the existing interval basis and one-dimensional physical model. CP082 binds construction fromada64e23c6a6535b3b4847773521d20a4e387858 on `research/reach-parameter-descent-input-frozen-20261101`.

| Input | Exact Git blob |
| --- | --- |
| Protocol090 |6b642bf10c3328bb64d37474e290810fb45cbca1 |
| Scalar stages105 |a8ce66ff0edec33e2aff299550fca2089d671033 |
| Review106 |d1d64802076b033218f3c93ac11af96f4c683e6a |
| Mixed analytic domain108 |587c15fd6e24f6e6b14de574ff878221cdbd5cb6 |
| Review109 |5a18d43990fdc20fd67384ad74fb7ff2651ec181 |
| Quantum theorem111 |b7b1e5f970904d6e7de065a4fedd382e212a3022 |
| Review112 |f1c2053d25c71bac169432bb28a7c91819d89147 |
| Unit cone114 |ee4bfb46c5565b90d6f9015765edc8a773b0997a |
| Review115 |ffefc5f6cf770e0d9e7492636e057a7f39dd40d2 |
| Quantum R1 comparison117 |e95b1155ebb2018a80d2dc559560730fd7ea6594 |
| Review118 |b712e319927dd4464b83f9d635cfb35ed6121c0b |
| Ledger119 |865e16fd2970bd30d17e3852d2a0badf5598fa0c |

Keep117's actual sheaf quotient and evaluation map:

$$
\mathfrak F^J_{\mathcal Z}
=\bigl(\mathfrak P^J/\mathfrak I^J\bigr)^\#,
\qquad
\mathrm{ev}_M:\mathfrak F^J_{\mathcal Z}(M;U)
\longrightarrow\mathrm{Map}(M,\widehat{\mathcal O}_{\mathcal Z}(U)(*)).
\tag{120.1}
$$

Here $\mathfrak P^J$ consists of actual joint analytic/source graph-jet families; $\mathfrak I^J$ requires uniform fixed-order rapidness of every mixed parameter/regulator jet, as in section8 of108 and section7 of117. Equality before quotienting is actual positive-regulator equality. Let $\mathfrak E=\mathrm{im}(\mathrm{ev})$ be the evaluated plot rule, with local gluing as in117. The question is whether differentiation on $\mathfrak F^J_{\mathcal Z}$ induces differentiation on $\mathfrak E$. It would require invariance of $\ker(\mathrm{ev})$. Evaluation faithfulness would suffice, but is stronger.

## 2. One fixed complete R1 source and a smooth coefficient curve

Choose an interval $U$ containing zero and small compact source supports in $U^2$. Use

$$
c=(x+y)/2,\qquad t=x-y,\qquad |dx\,dy|=|dc\,dt|.
$$

Let $\chi\in C_c^\infty(\mathbb R)$ equal one near zero, with sufficiently small support in the relative variable. Choose real even $\rho\in C_c^\infty(\mathbb R)$ with integral one. For $h>0$ set $\rho_h(c)=h^{-1}\rho(c/h)$. On a small parameter interval $M=(-a_0,a_0)$ put

$$
h(a)=e^{-1/a^2}\quad(a\ne0),\qquad
v_a=a\rho_{h(a)}\quad(a\ne0),\qquad v_0=0,
\qquad T_a(c,t)=v_a(c)\chi(t).
\tag{120.2}
$$

All supports lie in one compact $K\Subset U^2$. Choose the fixed closed cone $\Gamma$ consisting of centre covectors $(\eta,0)$ in these coordinates, with the relevant compact base. In the physical coordinates these are proportional to $(1,1)$. They avoid the nonzero conormal $(1,-1)$ of the only nontrivial two-vertex collision. Thus this is an admitted R1 cone, including at $c=t=0$.

**Lemma120.1.** The curve $a\mapsto T_a$ is smooth into the single complete Fréchet graph space $E_{2,K,\Gamma}$ of108.1. Its derivative at zero is $\delta(c)\chi(t)$, and every parameter derivative of order at least two at zero is zero. Every fixed nonzero-parameter coefficient is spatially smooth.

**Proof.** Put $D_h=h\partial_h$ and $R_h=(\rho_h-\delta)\chi$. The centre Fourier transform of $D_h^j(\rho_h-\delta)$ is $g_j(h\eta)$, where

$$
g_0(z)=\widehat\rho(z)-1,
\qquad g_j(z)=(z\partial_z)^j\widehat\rho(z)\quad(j\ge1).
$$

For each $j$, $|g_j(z)|\le C_j\min(|z|,1)$. With $\alpha=1/2$, the inequality $\min(|z|,1)\le |z|^\alpha$ and the integrability of $(1+\eta^2)^{-2}|\eta|^{2\alpha}$ imply

$$
\|D_h^jR_h\|_{H^{-2}(dc\,dt)}\le C_j h^\alpha.
\tag{120.3}
$$

The factor $\widehat\chi$ is Schwartz, so the extra $t$ integration is harmless. The same bound holds for every graph seminorm away from $\Gamma$. To verify localization, insert any fixed smooth physical cutoff $\psi(c,t)$. For $j=0$, its Fourier transform is the integral against $\rho(z)$ of the difference between $\psi(hz,t)e^{-ihz\eta}$ and $\psi(0,t)$. The mean-value bound gives a factor $h(1+|\eta|)$, with arbitrary decay in the $t$ frequency after integration by parts in $t$. For $j\ge1$, write $D_h^j\rho_h$ as the rescaling of a compact smooth function of integral zero and use the same subtraction. Outside $\Gamma$, the $t$ frequency is bounded below by a positive multiple of total frequency. Its arbitrarily rapid decay absorbs every fixed centre-frequency power and every requested graph order. This gives $O(h)$ there, hence $O(h^\alpha)$ for $0<h\le1$. Fixed pseudodifferential cutoffs have the same finite localized Fourier estimates, including their smoothing remainders.

Now write $T_a=a\delta(c)\chi(t)+aR_{h(a)}$. Each parameter derivative of the second summand is a finite sum of $D_h^jR_{h(a)}$ multiplied by functions bounded by a finite inverse power of $|a|$: $h'(a)/h(a)=2a^{-3}$ and its further derivatives have only such losses. Every fixed graph seminorm is therefore bounded by

$$
C_r|a|^{-N_r}e^{-\alpha/a^2}
\tag{120.4}
$$

for each fixed parameter derivative request. These bounds vanish to every order at zero. The second summand extends as a flat smooth curve into the complete graph space. The first is a linear smooth curve there. This proves the statement, with one fixed space for all derivatives. No order-escaping interpretation of the source plots is needed. $\square$

## 3. An admitted source operator carrying the family

Choose a nonzero real even $\widehat\phi\in C_c^\infty(\mathbb R)$ supported in a small annulus away from zero. It may be chosen where $\widehat\rho>1/2$, by continuity and $\widehat\rho(0)=1$. Its inverse Fourier transform $\phi$ is real even Schwartz and satisfies

$$
\int t^j\phi(t)\,dt=0\quad\text{for every }j\ge0.
\tag{120.5}
$$

The scalar normal kernel $\epsilon^{-1}\phi(t/\epsilon)$ is in the admitted full Schwartz-profile sector. After compact physical localization it lies in one scalar105 power/logarithmic stage: in the chart $t=\epsilon u$ its normalized front coefficient is $\phi(u)$; at the adjoining old regulator face its Schwartz tails are flat. All derivatives have the computed finite weight shifts. This is the nonzero all-moments-zero profile explicitly retained in090/096/108, not an arbitrary auxiliary-noise amplitude. The scalar stage is independent of $a$.

Let $q(x,y)=x$ and define the actual family

$$
u_{a,\epsilon}
=q_*\bigl[\epsilon^{-1}\phi(t/\epsilon)T_a(c,t)\bigr].
\tag{120.6}
$$

Projection is proper on the common compact support. This is exactly an allowed source expression108.7: one R1 coefficient, one scalar stage, identity source stratum, no normal derivative, and one physical vertex projection. The map from the completed mixed source into $\mathcal P_1$ is the admitted continuous source map. Lemma120.1 supplies a smooth curve in one fixed coefficient stage; the scalar factor is fixed. Finite mixed parameter/regulator estimates of108 consequently supply a joint family in $\mathfrak P^J(M;U)$, not merely pointwise membership in $\mathcal P_1$.

The map uses multiplication by a positive-regulator smooth scalar kernel and proper integration. It takes no restriction of a delta to its own support and no product of overlapping singular counterterms. All equalities are equalities of actual families. Complete-stage continuity also gives the admitted profinite source restrictions; no arbitrary-profinite projectivity or point detection on an internal Hom is invoked. The two-vertex projection is a defining analytic source for the output arity-one object. It is not being asserted to be a weight-preserving quantum map from arity two to arity one.

## 4. Every evaluated parameter value is zero

For $a\ne0$, $v_a$ is a fixed compact smooth function and

$$
u_{a,\epsilon}(x)
=\int\epsilon^{-1}\phi(t/\epsilon)\chi(t)
v_a(x-t/2)\,dt.
\tag{120.7}
$$

Taylor expansion of the smooth factor in $t$, with arbitrary depth, has zero polynomial integrals by(120.5). Replacing $\chi$ by one only adds a Schwartz-tail error away from $t=0$. Every fixed spatial derivative has the same estimate. Each regulator derivative replaces the profile by a Schwartz function with all moments zero and introduces a finite extra inverse regulator power. Increasing Taylor depth absorbs that power. Therefore, for every fixed $a\ne0$, $m,k,L$,

$$
\|\partial_x^m\partial_\epsilon^k u_{a,\epsilon}\|_{L^\infty}
\le C_{a,m,k,L}\epsilon^L.
\tag{120.8}
$$

Compact output support converts these to the required fixed-order rapid graph estimates. Constants are allowed to depend on the fixed parameter value. At $a=0$ the entire family is zero. Hence every point restriction belongs to the actual rapid ideal, and

$$
\mathrm{ev}_M([u])=0.
\tag{120.9}
$$

Uniformity of(120.8) over a neighborhood of zero has not been asserted. Joint moderation, already proved from the complete sources, is a different property.

## 5. Its evaluated derivative is nonzero

Differentiating the continuous source formula and using Lemma120.1 gives

$$
\left.\partial_a u_{a,\epsilon}(x)\right|_{a=0}
=q_*\bigl[\delta(c)\chi(t)\epsilon^{-1}\phi(t/\epsilon)\bigr]
=2\epsilon^{-1}\phi(2x/\epsilon)\chi(2x).
\tag{120.10}
$$

The factor two is the actual projection Jacobian: $x=t/2$ after $c=0$, whereas $|dx\,dy|=|dc\,dt|$. Let $g_\epsilon(x)=2\epsilon^{-1}\phi(2x/\epsilon)$. Its Fourier transform is $\widehat\phi(\epsilon\xi/2)$. For every fixed finite real Sobolev order $\tau$, annular support gives positive finite constants such that

$$
\|g_\epsilon\|_{H^{-\tau}}^2
\asymp
\epsilon^{2\tau-1}
\int |\eta|^{-2\tau}|\widehat\phi(\eta)|^2\,d\eta.
\tag{120.11}
$$

Indeed substitute $\eta=\epsilon\xi/2$ in the defining norm; the remaining weight is uniformly comparable to $|\eta|^{-2\tau}$ on the fixed annulus. The cutoff error $(\chi(2x)-1)g_\epsilon$ is rapid in every Sobolev norm, with every regulator derivative, by Schwartz decay on $|x|$ bounded away from zero. Thus the right side of(120.10) has norm comparable to $\epsilon^{\tau-1/2}$ in each fixed $H^{-\tau}$. It cannot satisfy every rapid power in any fixed finite order. Its class in $\mathcal Z_1(*)$ is nonzero.

This last statement is about the actual liquid quotient as well. If the class vanished, a rapid lift would exist after a nonempty extremally disconnected cover of the point, locally through finite rapid stages. Pullback along a point of such a cover would make this same actual curve rapid in a fixed finite order. Equation(120.11) rules that out for every order. No arbitrary-profinite point-detection principle is used.

**Theorem120.2 (failure of parameter descent).** The kernel of(120.1) is not invariant under parameter differentiation. In particular evaluation is not faithful. There is no linear derivative on the evaluated plot rule satisfying

$$
D\,\mathrm{ev}_M=\mathrm{ev}_M\,\partial_a
\tag{120.12}
$$

on all admitted joint families.

**Proof.** Differentiation exists upstairs because $\mathfrak I^J$ is defined using all mixed jets. The section $[u]$ lies in its evaluation kernel by(120.9), but its derivative has nonzero evaluation at zero by(120.10)–(120.11). It also follows that $[u]\ne0$ in the joint-family quotient. Any linear $D$ sends the zero evaluated map to zero, contradicting(120.12). This is a local obstruction, so sheafification does not remove it. $\square$

The failed positive mechanism is explicit. In the fixed complete coefficient source, the subspace whose image under(120.6) is rapid contains every smooth centre mollifier $\rho_h(c)\chi(t)$, $h>0$. Those converge in $E_{2,K,\Gamma}$ to $\delta(c)\chi(t)$ by(120.3), whose image is nonrapid. The preimage of the rapid ideal is not closed in that complete analytic source. Completeness of the source therefore supplies no closed-kernel or uniform-rapidness theorem. The smooth curve(120.2) gives an actual derivative leaving that subspace, beyond nonclosedness alone.

## 6. The specified Gaussian scale connection also fails to descend

Choose $s_0>0$ and set $a=s-s_0$ on a small positive scale interval. Regard(120.6) as an even output arity-one family at total weight one. Nonnegative quantum powers imply that this weight has only $n=1,k=0$. An even pair contraction has no pair there. Consequently the fixed connection117.14 acts on this family as

$$
\nabla_s=\partial_s-\hbar B_{\partial_sP_{s\epsilon}}
=\partial_s.
\tag{120.13}
$$

Its evaluated derivative at $s_0$ is exactly the nonzero class(120.10), although the evaluated input is identically zero. Thus no linear evaluated connection can intertwine this specified joint-family connection with evaluation. A pointwise linear correction applied to the zero evaluated map cannot cancel the defect. This does not classify all changes of family domain, coefficient object, weighting or quantum normalization.

Fixed-scale transport111 remains an actual cochain map; on this weight it is the identity. The connection on $\mathfrak F^J_{\mathcal Z}$ itself also remains defined. The obstruction is passing its parameter derivative through point evaluation, not an error in the finite transport formula or the quantum identities.

## 7. Hostile controls and exact limits

| Control | Result |
| --- | --- |
| Admitted source, not an ambient moving regulator bump | Lemma120.1 gives one complete fixed R1 graph space; the scalar stage and projection are fixed |
| Full collision-conormal condition | Centre-only source covectors avoid the relative collision conormal, including at zero parameter |
| Pointwise rapidness with every regulator derivative | Arbitrary Taylor depth and all vanishing moments give(120.8); no uniform rapidness is inferred |
| Nonzero retained output | Annular Fourier support gives(120.11) in every finite Sobolev order; parity cannot annul the test |
| Physical coefficient records | The uncut normal profile has all moments zero; cutoff errors change its moments only rapidly, so physical power/logarithmic coefficients vanish while the enriched class is nonzero |
| Proper projection and density | Common compact supports, unit centre/difference density determinant and the factor two in(120.10) |
| Actual source equality and completion | Continuous mixed source maps define the same actual family; no graph label or finite-separable-completion assumption |
| Quantum-weight control | Output weight one has no pair contraction or hidden higher-arity quantum correction |
| Existing Gaussian/Wick results | No change to the propagator,087 scheme,277 sources, legal spinneys or accepted111 identities |

The witness belongs to the declared analytic class, which deliberately retains arbitrary admitted full Schwartz normal profiles. It is not asserted to lie in the smaller algebraic span of raw finite Gaussian-polynomial graphs alone. No failure of that smaller span is inferred without a separate membership proof. No overlapping singular product, illegal source restriction or new physical spacetime dimension is used.

Theorem120.2 settles the exact proposed evaluated-family descent question negatively. It does not refute117's liquid cochain arrow or its source-controlled image connection, where source uniqueness remains available. It does not prove that every possible Costello–Gwilliam differentiable sheaf must be point-determined, or that every retained-family target is impossible. The joint-family quotient keeps precisely the information that evaluation loses here. A future categorical audit must check the actual differentiable-sheaf and liquid interfaces on that retained object, rather than silently identify it with point-valued plots or restrict away the witness. Extended completed Weiss descent and the remaining lifting/comparison conditions still require their own proofs.

R0/R1/R2 and separate087–089 retain their completed reviewed scopes. Original R3's actual degree-two support equation, its two residual channels, full M5/R4 and both parents remain open. This parameter kernel is not an original R3 syzygy, and no new opposed R3 cycle follows from it.

## 8. Provenance and admission boundary

This is one primary construction jointly reasoned by the parent and a delegated same-system construction context. Both identified the bandpass/mollifier mechanism; the parent supplied the one-fixed-stage flat-width strengthening, exact norm and quotient checks, and wrote this artifact after the construction role ended with a service-usage-limit error before writing files. No completed artifact or review is inferred from that failed role return. The parent is an author. Distinct nonauthor121 must inspect the frozen actual source and its hypotheses before acceptance. One correction pass remains available after that review.

No numerical fixture is supplied: fixed Fréchet estimates, exact moments, a Fourier norm lower bound and a commuting-square contradiction prove the claim. Unchanged277-source calculations are not replayed. Source preflight, frozen custody, critical review, final editorial integration, current checks, native protected admission/readback and explicit tracker reconciliation remain separate requirements. This candidate alone grants no external certification, protected bypass or programme closure.
