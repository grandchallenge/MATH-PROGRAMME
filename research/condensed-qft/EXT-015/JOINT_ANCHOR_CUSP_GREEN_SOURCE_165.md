# EXT-015 REACH / 165 — two-core reduction and matched-partition jets at the joint Green corner

**Scientific disposition: a source-equivalent two-core normal form, an exact joint heat-normal profile, and explicit legal matched-partition representations of the second derivatives. The undifferentiated joint corner and universal 150.L remain OPEN.**

This primary does **not** construct a full mixed-source representative of the joint Green primitive. It replaces that problem by two sharply specified joint-corner cores modulo **actual admitted 108.7 source families**. It also proves that applying the physical second derivative removes the core source-typing obstruction in two explicit, legal finite three-vertex histories. Every conclusion is a whole-positive-regulator identity; weak zero-scale limits are used only to characterize the nonzero normal profile, not to infer source membership.

## 1. Immutable input contract

| Protected input | Exact Git blob |
| --- | --- |
| [105 — Gaussian/Wick scalar stages](GAUSSIAN_WICK_COLLISION_NORMAL_FORM_105.md) | a8ce66ff0edec33e2aff299550fca2089d671033 |
| [108 — mixed completed source and legal jets](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md) | 587c15fd6e24f6e6b14de574ff878221cdbd5cb6 |
| [126 — source-controlled parameter rows](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md) | 5b05c6147d237ca1d22e4dcbce9262b0f038c163 |
| [141 — full one-retained-slot source primitive](SCALAR_RELATIVE_WEIGHT_ONE_COMPARISON_141.md) | de6b608c8def91dd0b8b2d98fe410348ac92a17d |
| [147/150 — extraction, R1 moments and open 150.L](COMPLEMENTARY_WEIGHT_TWO_COMPARISON_150.md) | 03deca9212a9bea56743e482e5cb79edb46b9d7f |
| [159 — corrected labelled and symmetric W input](NONSPECTATOR_GREEN_GAUSSIAN_R1_TEST_159.md) | 555088f3da2c87dc02304dcf44b2738510f65062 |
| [162 — exact punctured-source theorem and finite-jet no-go](LEGAL_HIDDEN_NONSPECTATOR_GREEN_SOURCE_AUDIT_162.md) | 20febc0e1196990addf446f0054f5e9e563ba615 |
| [163 — critical proof audit](AGENT_CRITICAL_REVIEW_PUNCTURED_GREEN_163.md) | 32187f9f0d7031522715259b7be78dc6f4f1b917 |
| [164 — bounded acceptance](PUNCTURED_GREEN_SOURCE_ACCEPTANCE_164.md) | 828876a30e9b16ebb36ef1006a3f4e6ab6159cc3 |

The source collection is the **existing** finite sum of completed histories (108.7), with R1 graph coefficients avoiding every nonzero partial-partition conormal, admitted scalar heat stages and properly typed diagonal inclusions and forgotten vertices. Full amplitude/auxiliary-noise enlargement, arbitrary overlapping R1 products and a regulator-zero Green scalar are not permitted. [CP187](../../../governance/bounded_operation_checkpoints/EXT-015-REACH-COMPLETION-001.json) requires an actual joint anchor/cusp test at the remaining 159 source.

Choose real $\rho\in C_c^\infty(U)$ with $\rho(0)\ne0$, the original moment-dual $b_0,b_1$, and

$$
e(t)=\frac{|t|}{2},\qquad
\kappa_\epsilon(t)=\frac{e^{-t^2/(2\epsilon^2)}}{\sqrt{2\pi}\epsilon},\qquad
C_j=e*b_j,\qquad G=e-C_0.
\tag{165.1}
$$

Put

$$
w_\epsilon(z)=\rho(z)\kappa_\epsilon(z),\quad
M_{j,\epsilon}=\int z^j w_\epsilon(z)\,dz,\quad
w_\epsilon^\circ=w_\epsilon-b_0M_{0,\epsilon}-b_1M_{1,\epsilon},
\tag{165.2}
$$

and set $Q_\epsilon=e*w_\epsilon$, $H_\epsilon=e*w_\epsilon^\circ=Q_\epsilon-C_0M_{0,\epsilon}-C_1M_{1,\epsilon}$, and $u=\delta_0-b_0$. The exact ambient output families are

$$
F_\epsilon^{\mathrm{lab}}(x,z)=G(x)w_\epsilon^\circ(z),\qquad
F_\epsilon^{\mathrm{sym}}(x,z)
=\tfrac12\bigl[G(x)w_\epsilon^\circ(z)+H_\epsilon(x)u(z)\bigr].
\tag{165.3}
$$

Here the input for $F^{\mathrm{sym}}$ is genuinely symmetric $W^0$, whereas $h_y$ is a labelled primitive component. These outputs are *not* assumed to be members of the complete two-slot source.

## 2. Fix a compact common Green patch

Take a fixed $\chi\in C_c^\infty(U)$, equal to one on a neighborhood of the convex hull of $\mathrm{supp}(\rho)$ and the two original moment-bump supports. That hull also contains the support of $G$ and, for **every** regulator, the support of $H_\epsilon$, by exact cancellation of their two affine moments. Consequently

$$
G=\chi(e-C_0),\qquad
H_\epsilon=\chi(Q_\epsilon-C_0M_{0,\epsilon}-C_1M_{1,\epsilon})
\tag{165.4}
$$

as exact distributions on $U$, despite the noncompact uncut $e$ and $Q_\epsilon$. No cutoff depends on $\epsilon$ or the requested source seminorm. If $U$ is too small to contain the relevant compact hull, this proposition is applied on an original cover-local compact stage with all supports strictly in $U$; the theorem is not asserted for arbitrarily enlarged supports outside the original open.

The following are **compact** two-slot actual curves:

$$
A_\epsilon(x,z)=\chi(x)e(x)w_\epsilon(z),\qquad
B_\epsilon(x,z)=\chi(x)Q_\epsilon(x)\delta_0(z).
\tag{165.5}
$$

Both expressions are legitimate ambient distributions at every positive regulator. Their membership in $\mathcal P_2$ is precisely **not** assumed.

## 3. Exact source-equivalent two-core normal form

**Proposition 165.1 (joint-corner reduction).** There are *explicit actual legal source families* $R_\epsilon^{\mathrm{lab}},R_\epsilon^{\mathrm{sym}}\in\mathcal P_2$ with

$$
F_\epsilon^{\mathrm{lab}}=A_\epsilon+R_\epsilon^{\mathrm{lab}},
\qquad
F_\epsilon^{\mathrm{sym}}=\tfrac12(A_\epsilon+B_\epsilon)
+R_\epsilon^{\mathrm{sym}}.
\tag{165.6}
$$

The source families are built from a fixed finite list of already admitted histories, complete coefficient maps and fixed 126 parameter rows; they have exact equality for each positive regulator, not merely modulo rapid. Thus, as *actual membership statements*,

$$
F^{\mathrm{lab}}\in\mathcal P_2
\ \Longleftrightarrow\ A\in\mathcal P_2,\qquad
F^{\mathrm{sym}}\in\mathcal P_2
\ \Longleftrightarrow\ (A+B)\in\mathcal P_2.
\tag{165.7}
$$

Neither equivalence is an assertion that its right side holds.

**Proof.** Define the following two explicit remainders:

$$
R_\epsilon^{\mathrm{lab}}
=-\chi(x)C_0(x)w_\epsilon^\circ(z)
-\chi(x)e(x)\sum_{j=0}^1 b_j(z)M_{j,\epsilon},
\tag{165.8}
$$

$$
R_\epsilon^{\mathrm{sym}}
=\tfrac12\left[
R_\epsilon^{\mathrm{lab}}
-\chi(x)Q_\epsilon(x)b_0(z)
-\chi(x)\bigl(C_0(x)M_{0,\epsilon}
+C_1(x)M_{1,\epsilon}\bigr)u(z)
\right].
\tag{165.9}
$$

Substitute $G=\chi(e-C_0)$, $w^\circ=w-\sum b_jM_j$ and $H=\chi(Q-C_0M_0-C_1M_1)$ from (165.4). Inserting $u=\delta_0-b_0$ produces (165.6) algebraically, including every moment correction and the ordinary physical density.

To check complete source membership of the *remainders*, use only already proved maps:

* $\chi C_0\,w_\epsilon^\circ$ and $\chi Q_\epsilon b_0$ have one-slot sources in the free variable (respectively $w^\circ$ and compactly cut off $Q=H+C_0M_0+C_1M_1$), followed by smooth compact singleton insertion, as in 141 and 150 §5. The one-slot source theorem applies to $H$ and multiplication by the fixed compact smooth $\chi,C_j$; the $M_j$ are admitted scalar zero-slot moment stages.
* $\chi e(x)b_j(z)M_{j,\epsilon}$ is a no-hidden identity-partition source. Its **fixed R1** coefficient $\chi e(x)b_j(z)$ is compact, with wavefront only in the $x$ covector, so no forbidden diagonal conormal; its scalar zero-slot coefficient $M_j$ has the admitted fixed nonnegative-even Gaussian moment expansion and the necessary saturated all-face index shifts.
* $\chi(C_0M_0+C_1M_1)u(z)$ uses smooth compact scalar heat coefficients times a fixed R1 distribution with wavefront only in the $z$ covector; hence it is one legal no-hidden identity source. The compact passive-coordinate cutoff is $\chi$; the original $u$ is compact.

The same fixed supports, R1 cones, scalar indices, finite derivative lists, pushdown densities and completed projective seminorm estimates as in the admitted 141/150 and 162 constructions work here without any new collision restriction. No term multiplies a cusp and an anchored hidden delta in a single R1 coefficient. The 126 parameter derivatives commute with these fixed actual operations and differentiate the moments and scalar stages with their already available finite derivative estimates. Thus each displayed $R$ is a finite complete source. Since $\mathcal P_2$ is an additive source image and two is invertible in the real liquid heart, subtracting the remainders gives precisely the two equivalences. $\square$

**Consequence.** The obstruction to the complete example is **not** any of its normalized moment subtractions. It is the *coupled anchored-Gaussian/cusp core* $A$ and, for the symmetric input, the additional *convolved-cusp/delta core* $B$. This is an exact, testable reformulation of the unfinished joint-corner problem, stronger than saying only that a punctured cutoff is admitted.

## 4. Explicit joint normal profiles, not just zero-scale physical limits

Let $K(t)=e^{-t^2/2}/\sqrt{2\pi}$. Use the simultaneous joint radial chart

$$
x=\epsilon X,\qquad z=\epsilon Z,
\qquad
P_1(X)=\int_{\mathbb R} e(X-Y)K(Y)\,dY.
\tag{165.10}
$$

This chart is an *analytic diagnostic* on compact $(X,Z)$ sets. The following limits are statements about the indicated pullback distributions. They do not assert that the original actual curves are in a fixed scalar source on every collision face.

**Proposition 165.2 (nonzero two-arm profile).** On every compact joint-normal chart and against every compact smooth test, with the usual distributional dilation of $\delta_0$,

$$
A_\epsilon(\epsilon X,\epsilon Z)
\longrightarrow \rho(0)e(X)K(Z),
\tag{165.11}
$$

$$
B_\epsilon(\epsilon X,\epsilon Z)
\longrightarrow \rho(0)P_1(X)\delta_0(Z).
\tag{165.12}
$$

These are the leading terms of complete fixed-order distributional Taylor expansions. For every $N\ge0$, their coefficients at order $\epsilon^n$, $0\le n\le N$, are respectively

$$
\frac{\rho^{(n)}(0)}{n!}e(X)Z^nK(Z),
\qquad
\frac{\rho^{(n)}(0)}{n!}
\left[\int e(X-Y)Y^nK(Y)\,dY\right]\delta_0(Z).
\tag{165.13}
$$

The remainders after degree $N$ are $O(\epsilon^{N+1})$ on bounded compact test families and under every fixed derivative after the corresponding finite power adjustment. The nontrivial symmetric *core* profile is

$$
\mathscr N_{\mathrm{sym}}(X,Z)
=\frac{\rho(0)}2\left[e(X)K(Z)+P_1(X)\delta_0(Z)\right].
\tag{165.14}
$$

Its second derivative is a symmetric pair of differently anchored Gaussian jets:

$$
\partial_X^2\mathscr N_{\mathrm{sym}}
=\frac{\rho(0)}2
\left[\delta_0(X)K(Z)+K(X)\delta_0(Z)\right].
\tag{165.15}
$$

**Proof.** In the first core, $e(\epsilon X)=\epsilon e(X)$ and $\kappa_\epsilon(\epsilon Z)=\epsilon^{-1}K(Z)$, while $\chi(\epsilon X)=1$ for all sufficiently small $\epsilon$ on any fixed compact $X$ patch. Hence the first formula is exactly $e(X)\rho(\epsilon Z)K(Z)$ there. For the second core substitute $y=\epsilon Y$ into $Q_\epsilon(\epsilon X)$, giving

$$
Q_\epsilon(\epsilon X)
=\epsilon\int e(X-Y)\rho(\epsilon Y)K(Y)\,dY.
\tag{165.16}
$$

The distributional pullback of $\delta_0(z)$ under $z=\epsilon Z$ contributes $\epsilon^{-1}\delta_0(Z)$, and so the second profile is $\left[\int e(X-Y)\rho(\epsilon Y)K(Y)\,dY\right]\delta_0(Z)$. Ordinary Taylor expansion of the *fixed smooth compact* $\rho$ in $\epsilon$ and Gaussian moments controls each remainder uniformly after any fixed derivative, including the $Y$ tails where the compact Taylor polynomial must be estimated with polynomial Gaussian weights. Because $e$ grows only linearly and $K$ decays rapidly, the coefficient integrals converge smoothly in $X$. The $(X,Z)$ distribution seminorm bounds follow from these observations. Finally $e''=\delta_0$ and $P_1''=K$ give (165.15). $\square$

At fixed positive regulator the first profile has possible wavefront only in the $X$ direction; the second has possible wavefront only in the $Z$ direction. Their sum contains no pure $(\tau,-\tau)$ diagonal conormal on this finite-normal chart, even though the *physical distributional leading coefficient at $\epsilon=0$* can have one (159–160). This is a precise noncommutation of **normal rescaling** and **taking the physical boundary limit**, not a contradiction.

## 5. The two second derivatives have legal matched-partition sources

**Proposition 165.3 (source-level differentiated syzygy).** On any joint patch where $\chi=1$, the two derivatives

$$
\partial_x^2 A_\epsilon(x,z)=
\delta_0(x)\rho(z)\kappa_\epsilon(x-z),
\qquad
\partial_x^2 B_\epsilon(x,z)=
\rho(x)\kappa_\epsilon(x-z)\delta_0(z)
\tag{165.17}
$$

are *actual* two-retained-slot sources in $\mathcal P_2$, each given by **one** pre-existing legal three-vertex 108.7 partition-inclusion history followed by forgetting the auxiliary vertex. With the compact $\chi$ reinstated, both derivatives remain in $\mathcal P_2$ by the additional already admitted smooth strict-face corrections.

**Proof.** For the first term introduce a hidden auxiliary vertex $y$ and the partition $\{x,y\}\mid\{z\}$. On its block-coordinate space $(t,z)$ place the original R1 distribution

$$
T_A(t,z)=\delta_0(t)\rho(z)
\tag{165.18}
$$

and the admitted scalar Gaussian heat edge $\kappa_\epsilon(t-z)$. Include the diagonal $x=y=t$, then properly forget $y$. The exact evaluated result is $\delta_0(x)\rho(z)\kappa_\epsilon(x-z)$, which equals $\delta_0(x)\rho(z)\kappa_\epsilon(z)$ because the Gaussian is even. The R1 coefficient has wavefront covectors only $(\eta,0)$ and avoids the forbidden partition conormal $(\tau,-\tau)$ on the two *block coordinates*. The delta on $x=y$ is supplied by the **typed partition inclusion**, not by multiplying two overlapping singular R1 coefficients.

For the second term use a hidden vertex $y$ and the different partition $\{z,y\}\mid\{x\}$, with block variables $(x,t)$, R1 coefficient

$$
T_B(x,t)=\rho(x)\delta_0(t)
\tag{165.19}
$$

and scalar Gaussian heat edge $\kappa_\epsilon(x-t)$. Include $z=y=t$ and forget $y$; the exact result is $\rho(x)\kappa_\epsilon(x-z)\delta_0(z)$. Its R1 cone is purely in the $t$ covector, so it too excludes the forbidden conormal. These constructions are in the original finite-jet/partition class of 108, with insertion order zero, one hidden vertex, ordinary pushforward density, fixed supports after output cutoff and the unchanged scalar index families. Proper pushdown, noncharacteristic source restriction, completed coefficient maps and genuine 126 parameter rows are the admitted 105/108 operations. There is no forbidden R1 input $e(x-y)\delta_0(y)$ or $G(x)\delta_0(y)$.

For the globally cut off cores, $\partial_x^2(\chi e)=\delta_0+f_\chi$ where $f_\chi=2\chi'e'+\chi''e$ is a *fixed smooth compact function* because $\chi=1$ near zero. The extra $f_\chi(x)w_\epsilon(z)$ is legal by one-slot source plus smooth singleton insertion. Also

$$
\partial_x^2(\chi Q_\epsilon)
=\chi w_\epsilon+2\chi'Q_\epsilon'+\chi''Q_\epsilon.
\tag{165.20}
$$

The first term times $\delta_0(z)$ is the matched-partition source above, with output cutoff $\chi$. For the remaining two terms $\chi',\chi''$ are supported away from the anchor: there $Q_\epsilon$ and $Q_\epsilon'$ are actual compactly cut-off smooth scalar heat-stage families by the same Gaussian-core affine decomposition and fixed saturated all-face indices proved in 162.3, together with the smooth moment corrections $C_jM_j$. Multiplication by fixed R1 $\delta_0(z)$ gives two legal no-hidden identity histories. All extra terms are retained exactly, not discarded as rapidly negligible. Thus the globally cut-off derivatives are legal as well. $\square$

**Logical limit.** Admitted source status of $\partial_x^2(A+B)$ does **not** imply a source primitive of $A+B$: an inverse of $\partial_x^2$ on these particular *mixed complete* source stages is exactly the still-missing map 150.L. Proposition 165.3 isolates the obstruction to source-level antiderivative closure. It does not establish that $\mathcal P_2$ is closed under inverse derivatives, nor that the cohomology of $W$ is nonzero.

## 6. Tests, acceptance boundary and deterministic successor

The finite standard-library [control fixture](fixtures/joint_anchor_core_controls_165.py) verifies the two-core identities (165.6), both actual normalizations and their differentiated lattice analogues, as well as the even Gaussian moment coefficients of the two joint rescaling arms. These are exact rational tests of algebra, not a proof of completed analytic source membership or an external mathematical certificate.

| Question | 165 result |
| --- | --- |
| Removal of all already sourced normalized-moment corrections | **EXACT** two-core equivalence in $\mathcal P_2$ |
| Complete nonzero joint-normal profile | **DERIVED**, with all finite-order strong distributional coefficient bounds |
| Source of each second derivative at the simultaneous corner | **CONSTRUCTED**, legal matched-partition Gaussian history |
| Full source of $A$, $A+B$, or either joint Green primitive | **OPEN** |
| Universal 150.L, $W$ acyclicity or original R3 | **OPEN** |
| Full 126.14, higher weights, actual lifting and M5/R4 | **OPEN** |

**Next substantive research step 168:** investigate whether the two matched-partition differentiated histories in (165.17) admit a *single finite complete source antiderivative* with the exact profiles (165.14), full all-corner scalar indices, proper densities, noncharacteristic R1 cones, rapid relation and 126 source-controlled parameter rows. If not, produce a source-invariant obstruction for **every legal finite history** on the actual restricted $W$ domain. Simply restating a bad hidden-anchor factorization or the finite point-jet failure (162.5) will not suffice.

**Custody:** This document is a primary mathematical return requiring distinct logical Verifier/Adversary critical review 166, bounded acceptance ledger 167, protected review/CI/merge and exact main readback, followed by CP188 continuity. Its claims are bounded: universal 150.L, residual $W$ cohomology, original R3 and full REACH are not resolved. The model-origin reviewer will not be described as an independent human or externally certified mathematician.
