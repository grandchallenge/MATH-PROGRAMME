# EXT-015 REACH / 162 — punctured-source lifting and the finite Wick-jet obstruction

**Primary disposition: a constructive, exact source lift away from the joint anchor/cusp point, plus a quantitative negative test for finite Wick-jet repair. Universal Lemma 150.L remains OPEN.** This is a new positive *localized* mapping result for both the labelled and graded-symmetric residual families of 159. It is not a global source lift, a negative theorem for every hidden history, or a proof about residual cohomology.

## 1. Exact scientific contract and scope

| Protected input | Git blob |
| --- | --- |
| [105: Gaussian/Wick scalar stages and all-corner geometry](GAUSSIAN_WICK_COLLISION_NORMAL_FORM_105.md) | a8ce66ff0edec33e2aff299550fca2089d671033 |
| [108: finite completed mixed sources and rapid quotient](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md) | 587c15fd6e24f6e6b14de574ff878221cdbd5cb6 |
| [126: genuine source-controlled parameter rows](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md) | 5b05c6147d237ca1d22e4dcbce9262b0f038c163 |
| [141: actual one-retained-slot Green source homotopy](SCALAR_RELATIVE_WEIGHT_ONE_COMPARISON_141.md) | de6b608c8def91dd0b8b2d98fe410348ac92a17d |
| [147: intrinsic diagonal extraction](WEIGHT_TWO_DIAGONAL_JET_COMPARISON_147.md) | 89b3d4a835f3750114e983854585e33d8184cb1f |
| [150: partial Green primitive and open 150.L](COMPLEMENTARY_WEIGHT_TWO_COMPARISON_150.md) | 03deca9212a9bea56743e482e5cb79edb46b9d7f |
| [159: corrected labelled/symmetric non-spectator example](NONSPECTATOR_GREEN_GAUSSIAN_R1_TEST_159.md) | 555088f3da2c87dc02304dcf44b2738510f65062 |
| [160: substantive logical critic](AGENT_CRITICAL_REVIEW_NONSPECTATOR_GREEN_160.md) | c11d08c17b5819a8042cc816520b920ede022ffa |
| [161: bounded acceptance ledger](NONSPECTATOR_GREEN_ACCEPTANCE_161.md) | eed5790361f58c6724bfc2c53481b064febdc5d4 |

The governing [CP186](../../../governance/bounded_operation_checkpoints/EXT-015-REACH-COMPLETION-001.json) sets the task of testing permitted hidden-vertex/non-spectator R1 history types against the exact source in 159. This work fixes one interval $U$ containing the anchor $0$, fixed moment-dual bumps, the original real-liquid heart, and **the already admitted** geometric maps, physical densities, scalar stages and completed graph sources. It neither enlarges 108.7 nor assumes a formal unregulated Green edge is a scalar coefficient.

Set

$$
u(t)=\delta_0(t)-b_0(t),\qquad
w_\epsilon(t)=\rho(t)\kappa_\epsilon(t),\qquad
w_\epsilon^\circ=(1-B)w_\epsilon,
\tag{162.1}
$$

with $\rho\in C_c^\infty(U)$ and $\rho(0)\ne0$. Write $e(t)=|t|/2$, $C_j=e*b_j$, $G=e-C_0$ and $H_\epsilon=e*w_\epsilon^\circ$. The two **exact ambient** primitives from 159 are

$$
F_\epsilon^{\mathrm{lab}}(x,z)=G(x)w_\epsilon^\circ(z),
\quad
F_\epsilon^{\mathrm{sym}}(x,z)
=\frac12\bigl[
G(x)w_\epsilon^\circ(z)+H_\epsilon(x)u(z)
\bigr].
\tag{162.2}
$$

All physical distributions have compact supports by affine moment normalization. The input generating the symmetric primitive is actually in $W^0$; the intermediate labelled source is not silently called symmetric.

## 2. One-slot admissibility, the missing simplification

**Lemma 162.1.** The whole regulator family $w_\epsilon^\circ$ is an admitted **one-retained-vertex** source, and $H_\epsilon=h(w_\epsilon^\circ)$ is another admitted one-retained-vertex source, with complete fixed-stage maps and all compatible 126 parameter rows.

**Proof.** Start with the original legal two-retained-vertex history $\delta_0(y)\rho(z)\kappa_\epsilon(y-z)$ of (159.2). The admitted proper projection forgetting $y$ evaluates exactly to $w_\epsilon(z)$. In one retained coordinate its affine moment corrections are the all-vertex smooth-decoration/forgetting maps of 108, 135 and 150 §5; reinsertion by $b_0,b_1$ is a smooth singleton source. Thus $w_\epsilon^\circ$ is a finite legal one-slot history with fixed scalar index data and coefficient graph stages. Its two affine moments vanish. The actual one-retained-vertex convolution theorem in 141 §§4–6 applies to **every** such complete source, including an auxiliary hidden anchor, and produces the exact normalized compact primitive $e*w_\epsilon^\circ=H_\epsilon$ in a finite *existing* one-slot source collection. The proof of 141 carries fixed cones, scalar indices and finite seminorm bounds across graph-order relaxations and the permitted 126 parameter rows. The equality is before passing to the rapid quotient. No two-slot mixed Green mapping theorem is invoked. $\square$

A useful consequence of the same bump-adjoining argument in 150 §5 is that **any fixed smooth compact function** $g$ may be inserted as a new singleton coefficient. Its added covector is zero; the partition-conormal, complete-tensor and scalar b-map proof for $b_j$ is unchanged. This does **not** allow insertion of a singular $\delta_0$ as though it were a smooth bump.

## 3. Two scalar asymptotic lemmas on ordinary strict faces

Let $\alpha,\beta\in C_c^\infty(U)$ be identically one on neighborhoods of the anchor $0$, chosen so that all relevant supports stay in $U$. Define the output cutoff

$$
L(x,z)=1-\alpha(x)\beta(z)
=(1-\alpha(x))+\alpha(x)(1-\beta(z)).
\tag{162.3}
$$

All assertions below concern fixed source stages, complete scalar coefficients and their full actual positive-regulator values.

**Lemma 162.2 (spectator coordinate away from the anchor).** The family $(1-\beta(z))w_\epsilon^\circ(z)$ is a compact smooth scalar source with a **single fixed scalar index family** generated by even nonnegative regulator powers and saturated by all nonnegative integer face shifts, including a smooth regulator-flat remainder. Its pullback to the *two*-retained-vertex scalar collision heat space satisfies the same fixed all-face and all-corner polyhomogeneous estimates.

**Proof.** Write

$$
M_{j,\epsilon}
=\int t^j\rho(t)\kappa_\epsilon(t)\,dt,\qquad
w_\epsilon^\circ(z)=\rho(z)\kappa_\epsilon(z)
-b_0(z)M_{0,\epsilon}-b_1(z)M_{1,\epsilon}.
\tag{162.4}
$$

As $\beta=1$ near zero, $(1-\beta)\rho\kappa_\epsilon$ is $O(\epsilon^N)$ for every $N$, in every fixed physical, regulator and bounded-parameter derivative seminorm: the nonzero support has $|z|\ge\delta$ and derivatives cost only fixed powers of $\epsilon^{-1}$. Meanwhile Gaussian Taylor expansion gives the whole strong scalar expansion

$$
M_{j,\epsilon}\sim
\sum_{n\ge0}
\frac{\epsilon^{2n}}{2^n n!}
\left.\partial_t^{2n}(t^j\rho(t))\right|_{t=0}.
\tag{162.5}
$$

At every truncation its remainder and each fixed regulator derivative have the required finite seminorm and weight bound. Multiplying by $(1-\beta)b_j$ gives a smooth physical coefficient with this *fixed* scalar even-power expansion and its fixed face-shift-saturated index family. The flat part is retained, not discarded. After multiplying by any fixed compact cutoff in $x$ that equals one on the support of the intended R1 coefficient, its pullback across the existing interior heat b-maps is polyhomogeneous on all two-vertex collision corners: the physical coefficient is smooth and the regulator is a positive unit times a finite boundary monomial. The positive smooth units have ordinary Taylor expansions; their integer shifts are included in the fixed saturated face index family. This is exactly the completed scalar stage from 105.5–105.6. $\square$

**Lemma 162.3 (integrated coordinate away from the anchor).** The family $(1-\alpha(x))H_\epsilon(x)$ is a compact smooth scalar source of the same fixed saturated scalar index family, including actual regulator-flat terms, on the two-vertex heat space (after passive pullback in $z$).

**Proof.** For $x$ in any fixed compact support of $(1-\alpha)$, choose a positive distance $\delta$ from zero. On the Gaussian peak $|t|<\delta/2$ the Green kernel is **exactly affine in $t$**, so

$$
e(x-t)=e(x)-\frac12\mathrm{sgn}(x)t
\qquad(|t|<|x|).
\tag{162.6}
$$

The part with $|t|\ge\delta/2$ is uniformly exponentially flat under every fixed derivative. Hence, *as an equality of actual functions including an explicitly retained flat remainder*,

$$
(1-\alpha)H_\epsilon
=(1-\alpha)\left[
G(x)M_{0,\epsilon}
-\left(C_1(x)+\frac12\mathrm{sgn}(x)\right)M_{1,\epsilon}
+R_{\epsilon}(x)
\right],
\tag{162.7}
$$

where $R_\epsilon$ and all fixed derivatives are $O(\epsilon^N)$ for every $N$ on the prescribed compact patch. Here $G$ and $\mathrm{sgn}(x)$ are smooth on the support of $1-\alpha$; after multiplying by the compactly supported $H_\epsilon$ or applying a fixed output cutoff, all functions are compact on the required physical source patch. The Taylor stages for $M_j$ are those of (162.5). Every collision face has a smooth tangential coefficient, and the same b-map estimates as in Lemma 162.2 apply. $\square$

These two lemmas deliberately **do not** assert that $w_\epsilon^\circ$ is a scalar source near $z=0$, or that $H_\epsilon$ is a scalar source near $x=0$. Those are the simultaneous anchor/cusp regimes not covered by the result.

## 4. The constructive punctured-source theorem

**Theorem 162.4 (exact two-slot lift away from the joint anchor/cusp).** For every fixed choice of $\alpha,\beta$ above, the families

$$
L F_\epsilon^{\mathrm{lab}}
\quad\text{and}\quad
L F_\epsilon^{\mathrm{sym}}
\tag{162.8}
$$

belong to the *actual* two-retained-vertex source image $\mathcal P_2$ of 108.7. They admit a **finite fixed list of existing source histories** and jointly continuous completed coefficient maps with common spatial compact supports, admissible R1 cones, fixed scalar index families and weight bounds, proper densities, the original rapid relation and all genuine source-controlled 126 parameter rows. The representation gives equality for every positive regulator, not only equality of physical asymptotic coefficients or a rapid quotient.

**Proof.** Expand (162.3) against the two summands of (162.2). There are exactly four types:

1. $(1-\alpha(x))G(x)w_\epsilon^\circ(z)$. The fixed multiplier $g(x)=(1-\alpha)G$ is **smooth compact**, because $\alpha=1$ near the cusp. Lemma 162.1 supplies a complete one-slot source for $w_\epsilon^\circ$; adjoin the smooth singleton coefficient $g(x)$ using the already admitted bump-reinsertion construction in 150 §5, with its finite source list, proper unit density and zero added covector.

2. $(1-\alpha(x))H_\epsilon(x)u(z)$. Lemma 162.3 makes $(1-\alpha)H_\epsilon(x)$ an actual scalar heat-stage coefficient with fixed even index family. Multiply this scalar factor by a fixed compact cutoff in $z$ equal to one on $\mathrm{supp}(u)$, so it has the required compact two-slot physical support. The R1 factor $u(z)=\delta_0(z)-b_0(z)$ has covectors purely in the $z$ direction, which avoid all nonzero two-slot partition conormals. Their product is a legal **no-hidden, identity-partition** history, even though the R1 distribution is singular.

3. $\alpha(x)G(x)(1-\beta(z))w_\epsilon^\circ(z)$. Let $T(x,z)=\alpha(x)G(x)\theta(z)$ where fixed $\theta\in C_c^\infty(U)$ equals one on the support of $(1-\beta)w_\epsilon^\circ$. Its covectors are purely in the $x$ direction and therefore avoid the forbidden diagonal conormal. Lemma 162.2 makes $a_\epsilon(x,z)=\vartheta(x)(1-\beta(z))w_\epsilon^\circ(z)$ an **actual fixed scalar stage**, where the fixed compact $\vartheta(x)$ equals one on $\mathrm{supp}(\alpha G)$. The identity-partition product $a_\epsilon T$ is legal and equals this term. A common fixed support for $\theta$ exists because the source compact supports and the bumps are fixed for the entire stage.

4. $\alpha(x)H_\epsilon(x)(1-\beta(z))u(z)$. Since $\delta_0(z)$ is killed by $(1-\beta)$, the second factor is the **fixed smooth compact** function $-(1-\beta(z))b_0(z)$. Lemma 162.1 supplies a complete one-slot source for $H_\epsilon(x)$. Multiplication by the fixed smooth $\alpha(x)$ and smooth singleton reinsertion in $z$ give an existing legal source.

Every term is a source transformation *already admitted* in 105/108/141/150. The total for $L F^{\mathrm{sym}}$ is half the sum of the four terms and has the corrected symmetric input provenance; no assertion that $h_y$ itself preserves the symmetric subspace is made. In terms 2 and 3, fixed scalar-stage and R1 normal estimates give bilinear joint continuity on the completed projective sources exactly as in 108.6. In terms 1 and 4, the one-slot and singleton maps are continuous on their fixed complete stages. The source lists and geometric data are independent of relaxed graph orders and all genuine 126 parameter-row derivatives, which act through the same fixed maps and the Gaussian moment Taylor bounds. Fixed compact source supports make every pushforward proper and keep the ordinary physical density; no Jacobian or finite normal-jet contribution is discarded. As the four evaluated terms add to $L F$ algebraically for **every** $\epsilon>0$, equality descends through the actual evaluator and the finite-order rapid relation. $\square$

**Scope:** For arbitrary arbitrarily small neighborhoods $V$ of $(0,0)$, choose $\alpha\beta$ supported in $V$. The **complementary cutoff** $(1-\alpha\beta)F$ then has an exact admitted mixed source. This shows that the remaining 159 output-admission question is concentrated in the **simultaneous** anchor/cusp corner. It does not identify a quotient sheaf's support or assert that $F$ itself belongs to $\mathcal P_2$.

## 5. A sharp negative test of smoothing plus finitely many collision jets

A tempting attempt to fix the corner is to replace the cusp $e(x)$ by the Gaussian Wick edge $P_\epsilon=e*\kappa_\epsilon$, and then add a **fixed finite** list of distributions supported on $x=0$. The next result demonstrates an unbounded normal-jet obstruction for that *particular* repair, even after allowing arbitrary regulator-dependent coefficients in the spectator coordinate.

**Proposition 162.5 (no rapid finite-jet Wick repair).** Fix an integer $J\ge0$. Let

$$
E_\epsilon(x,z)=
\bigl[P_\epsilon(x)-e(x)\bigr]\,w_\epsilon^\circ(z),
\qquad P_\epsilon=e*\kappa_\epsilon.
\tag{162.9}
$$

For **any** choice of distributional functions $c_{j,\epsilon}(z)$, $0\le j\le J$, the difference

$$
E_\epsilon-\sum_{j=0}^{J}
\delta_0^{(j)}(x)c_{j,\epsilon}(z)
\tag{162.10}
$$

is **not rapid** as $\epsilon\downarrow0$ in the distributional finite-order sense (and therefore not rapid in the stricter completed mixed-source normal topology). This remains true if the $c_{j,\epsilon}$ are allowed to have arbitrary bounded-below fixed scalar indices and arbitrary, even singular, $z$ dependence.

**Proof.** The heat semigroup identity holds strongly on compactly supported tests and gives the exact distributional asymptotic expansion

$$
P_\epsilon-e
\sim\sum_{n\ge1}
\frac{\epsilon^{2n}}{2^n n!}\,
\delta_0^{(2n-2)}.
\tag{162.11}
$$

Indeed $P_\epsilon=e^{(\epsilon^2/2)\partial_x^2}e$, and $e''=\delta_0$. The Gaussian convolution/Taylor remainder gives the strong estimate after any fixed regulator derivative. Choose an **even integer $m>J$** and a compact test $\varphi_m(x)$ equal to $x^m/m!$ near zero. Then $\varphi_m^{(j)}(0)=0$ for every $j<m$ and $\varphi_m^{(m)}(0)=1$. Choose a compact smooth $\psi(z)$ with

$$
\langle u,\psi\rangle
=\psi(0)-\int b_0(z)\psi(z)\,dz\ne0,
\tag{162.12}
$$

possible since $\delta_0-b_0\ne0$. The correction (162.10) vanishes identically when tested against $\varphi_m\otimes\psi$, for **every** $\epsilon$. But (162.11) and $w_\epsilon^\circ\to\rho(0)u$ give

$$
\left\langle E_\epsilon,\varphi_m\otimes\psi\right\rangle
=\frac{\rho(0)\langle u,\psi\rangle}
{2^{m/2+1}(m/2+1)!}\,
\epsilon^{m+2}
+O(\epsilon^{m+4}).
\tag{162.13}
$$

The coefficient is nonzero by construction, so the pairing fails the rapid bound with a power above $m+2$. This proves the result even in the weak distributional sense. The argument fixes the test after $J$ is fixed, without choosing a moving normal-jet order or a regulator-dependent test. $\square$

The sharpness is conceptual: the Gaussian smoothing error contains **every** even delta derivative at higher orders. A single *fixed* finite list of $x=0$ jets cannot render it rapid. This does not exclude a genuinely different **finite complete source history** whose scalar coefficient already contains an entire compatible polyhomogeneous expansion, nor does it exclude a non-spectator R1 sector or a collision-jet map supported on a different stratum. It is not general nonmembership in $\mathcal P_2$.

## 6. Test obligations, adversarial limits and successor

A [finite exact fixture](fixtures/hidden_corner_localization_controls_162.py) checks the four-term cutoff identity for the labelled and symmetric Green outputs, the two affine moments of both the labelled and symmetric joint-kernel inputs, and the polynomial Gaussian heat coefficients in (162.11) through fixed orders. These finite controls cannot certify source stage membership or infinite-dimensional completion. The positive result uses 141's actual complete one-slot theorem, 105's scalar all-corner contract and 108's original tensor/partition tests, not an unaccepted auxiliary-noise enlargement.

| Question | 162 outcome |
| --- | --- |
| Source of $w_\epsilon^\circ$ and its one-slot compact primitive $H_\epsilon$ | **EXISTING SOURCE** by 108/141 |
| Actual two-slot source for either Green primitive away from $(0,0)$ | **CONSTRUCTED**, fixed four-type source list |
| Scalar stages on strict faces away from the anchor | **PROVED**, full even Taylor and exponentially flat remainders |
| Any fixed finite $x=0$ jet repair of the naive Wick substitution | **DISPROVED** even modulo rapid |
| A legal complete source through the simultaneous anchor/cusp point | **NOT ESTABLISHED** |
| General 150.L for all distinct-block mixed histories | **OPEN** |
| Residual W acyclicity, original R3, 126.14, higher weights, actual lifting, M5/R4 | **OPEN** |

**Next substantive task:** test actual mixed-source constructions supported at the remaining joint anchor/cusp corner. In particular determine whether a legal *same-block partition jet coupled to a proper Gaussian hidden-vertex history*, with fixed admissible R1 cone and full completed all-corner scalar stages, can lift the joint singular term while avoiding the forbidden $G(x)\delta_0(y)$ coefficient. Alternatively seek a genuinely global source-invariant obstruction, not another narrowly defined ansatz failure. It must account for the full even tower (162.11) without an escaping normal-jet order.

**Custody:** This is an unreviewed primary 162 mathematical candidate. It requires exact-source Verifier/Adversary critic 163, bounded ledger 164, protected CI/merge/readback and CP187 continuity. No protected mathematical claim, original review policy or source class is changed by writing it.
