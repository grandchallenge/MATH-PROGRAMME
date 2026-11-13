# EXT-015 REACH / 159 — integrated-coordinate R1 singularity and the zero-scale diagonal trap

**Primary disposition: exact non-spectator test and a restricted source-lifting obstruction; universal 150.L OPEN.** A legal mixed Gaussian/R1 history whose R1 singularity lies in the coordinate integrated by the Green operator has an exactly computable primitive. The test also produces a genuine degree-zero element of the admitted residual joint kernel $W=\ker(P,m)$. Its fixed-positive-regulator output excludes diagonal conormals, but its **zero-regulator distributional leading coefficient has a pure diagonal-conormal wavefront**. A no-go theorem rules out extending the spectator-regular, two-retained-vertex source template of 156 to this example. Neither theorem rules out *every* allowed hidden-vertex or non-spectator mixed history. Thus neither full source nonmembership nor W cohomology is claimed.

## 1. Source lock and question

| Protected input | Git blob |
| --- | --- |
| [105, scalar heat geometry and fixed index stages](GAUSSIAN_WICK_COLLISION_NORMAL_FORM_105.md) | a8ce66ff0edec33e2aff299550fca2089d671033 |
| [108, actual finite mixed sources](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md) | 587c15fd6e24f6e6b14de574ff878221cdbd5cb6 |
| [126, source-controlled parameter rows](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md) | 5b05c6147d237ca1d22e4dcbce9262b0f038c163 |
| [147, intrinsic diagonal extraction](WEIGHT_TWO_DIAGONAL_JET_COMPARISON_147.md) | 89b3d4a835f3750114e983854585e33d8184cb1f |
| [150, Green primitive, residual W and open lemma 150.L](COMPLEMENTARY_WEIGHT_TWO_COMPARISON_150.md) | 03deca9212a9bea56743e482e5cb79edb46b9d7f |
| [153, fixed-scale wavefront theorem](MIXED_GREEN_KERNEL_MAPPING_AUDIT_153.md) | ad0ba1a607e03337dd7489b1d2ea3415fd2afed9 |
| [156, successful Gaussian–spectator lift](MIXED_GREEN_SCALAR_COMMUTATOR_SOURCE_LIFT_156.md) | fb683d69b5536df98805d104c9640234a486a2dd |
| [157, role-scoped critique](AGENT_CRITICAL_REVIEW_MIXED_GREEN_SCALAR_157.md) | f9f195b7e852b716304c060a40a23b14bac7e410 |
| [158, bounded acceptance](MIXED_GREEN_SCALAR_ACCEPTANCE_158.md) | 2f910446b1027be1e28ff13bb901652dd806b355 |

The protected [checkpoint CP185](../../../governance/bounded_operation_checkpoints/EXT-015-REACH-COMPLETION-001.json) requires exactly an *integrated-coordinate-singular* R1 test of a Gaussian edge. Work on an interval $U$ containing $0$, and use the original physical densities, regulator normalization, completed coefficient stages, R1 partition-conormal exclusion and legal 108.7 histories. This return neither adds a coefficient class nor changes the scalar boundary quotient or any counterterm.

## 2. Exact legal input, without a spectator-factor substitution

Choose a fixed real $\rho\in C_c^\infty(U)$ with $\rho(0)\ne0$ and let

$$
\kappa_\epsilon(t)=\frac{1}{\sqrt{2\pi}\epsilon}
\exp\left(-\frac{t^2}{2\epsilon^2}\right),
\qquad
T(y,z)=\delta_0(y)\rho(z).
\tag{159.1}
$$

The wavefront of $T$ consists of the nonzero $(\eta,0)$ covectors above $y=0$. Even at the source point $(0,0)$, it avoids the forbidden conormal $(\tau,-\tau)$ to the retained-label diagonal $y=z$. Thus $T$ is in a fixed admissible two-slot R1 graph stage; the integrated coordinate $y$ is genuinely singular.

The Gaussian scalar $\kappa_\epsilon(y-z)$ is the admitted positive-regulator Wick edge in 105.4–105.6. Its scalar heat index stages and the exterior product with $T$ define a legal distinct-retained-block identity-partition history of 108.7:

$$
v_\epsilon(y,z)
=\kappa_\epsilon(y-z)\delta_0(y)\rho(z)
=\delta_0(y)w_\epsilon(z),
\qquad
w_\epsilon(z)=\kappa_\epsilon(z)\rho(z).
\tag{159.2}
$$

This is **one fixed complete source**; it is not a separately chosen distribution for each regulator. The equality uses the evenness of the Gaussian and the ordinary density. The scalar multiplication does not change the positive-scale R1 wavefront.

Let $b_0,b_1$ be the fixed smooth compact moment-dual bumps of 150.3, and $C_j=e*b_j$ with $e(t)=|t|/2$. Then $m_{y,0}v_\epsilon=w_\epsilon$ and $m_{y,1}v_\epsilon=0$. Therefore the normalized compact Green operator gives an **exact** equality in distributions:

$$
h_yv_\epsilon(x,z)=G(x)w_\epsilon(z),
\qquad
G(x)=e(x)-C_0(x),
\qquad
G''=\delta_0-b_0.
\tag{159.3}
$$

The convolution and moment corrections use the actual physical $dy$. Since $\delta_0-b_0$ has vanishing zeroth and first moments, $G$ is compactly supported in the hull of $\{0\}\cup\mathrm{supp}(b_0)$, and $G$ has a genuine first-derivative jump of size $1$ at $x=0$. No Gaussian approximation to $e$ was substituted.

**Proposition 159.1 (exact non-spectator primitive).** Equations (159.1)–(159.3) are valid for every positive regulator, preserve the full actual family, and identify an R1-admissible original input. They do **not** by themselves identify a legal 108.7 *output* source for $G(x)w_\epsilon(z)$.

## 3. A genuine source-admitted degree-zero W witness

Let $B_y$ and $B_z$ be the moment-reinsertion maps of 150.3 in the respective retained coordinates and set $Q=(1-B_y)(1-B_z)$. These maps commute and are **already source-admitted** by 150 §5: partial moments are smooth decorations followed by vertex forgetting, while bump reinsertion adjoins a singleton block and preserves the R1 cone and fixed completed scalar stages. Their composition also has a finite legal source representation.

Define

$$
w_\epsilon^\circ(z)=(1-B_z)w_\epsilon(z)
=w_\epsilon(z)-b_0(z)M_{0,\epsilon}-b_1(z)M_{1,\epsilon},
\qquad
M_{j,\epsilon}=\int z^j w_\epsilon(z)\,dz.
\tag{159.4}
$$

The degree-zero input

$$
v_\epsilon^W=Qv_\epsilon
=(\delta_0(y)-b_0(y))\,w_\epsilon^\circ(z)
\tag{159.5}
$$

belongs to the **existing actual mixed source image**, not merely the ambient distribution envelope. The formula on the right is an evaluated factorization; its source admissibility is supplied by the finite linear combination of the original legal history and the established $B_y,B_z$ source maps. It does **not** assert that $w_\epsilon^\circ$ is itself a legal two-vertex scalar factor.

The four labelled affine moments of (159.5) vanish exactly. Its intrinsic diagonal extraction $P$ vanishes, since the source expression and its single-coordinate bump reinsertions have *distinct retained blocks*, and 147 annihilates them. Consequently

$$
v^W\in W^0=\ker(P,m)^0.
\tag{159.6}
$$

Because $B_y$ commutes with $B_z$ and $h_y B_y=0$, applying the ambient compact primitive gives

$$
h_yv_\epsilon^W(x,z)
=G(x)w_\epsilon^\circ(z).
\tag{159.7}
$$

**Proposition 159.2 (legally sourced joint-kernel stress test).** The family (159.5) is a nontrivial, source-admitted degree-zero input in the actual residual joint kernel. Formula (159.7) is an exact *ambient* primitive. It does **not** establish that this primitive lies in the complete mixed source image and hence does not imply a contracting homotopy, exactness, nonexactness or nonzero cohomology for $W$.

## 4. The positive-scale / zero-scale wavefront discontinuity

For every $\epsilon>0$, $w_\epsilon^\circ$ is a smooth compact function of $z$. As $G$ is singular only at $x=0$, the nonzero wavefront covectors of $h_yv_\epsilon^W$ have the form $(\xi,0)$ above $x=0$. They avoid the pure diagonal conormal $(\tau,-\tau)$, exactly as predicted by admitted Proposition 153.1.

The zero-scale distributional limit is different. Standard Gaussian test-function Taylor expansion, with every derivative taken against the full test, gives

$$
w_\epsilon\longrightarrow \rho(0)\delta_0
\quad\text{in }\mathcal E'(U),
\qquad
M_{0,\epsilon}\longrightarrow \rho(0),\quad
M_{1,\epsilon}\longrightarrow0.
\tag{159.8}
$$

More precisely, on compact tests the entire strong distributional expansion is

$$
w_\epsilon\sim
\sum_{n\ge0}\frac{\epsilon^{2n}}{2^n n!}
\,\rho(z)\delta_0^{(2n)}(z).
\tag{159.9}
$$

Here the even distributional derivatives have positive test-pairing signs. Taylor's integral remainder after order $2N$ is bounded by finitely many $C^{2N+2}$ seminorms of the full test and by $O(\epsilon^{2N+2})$; differentiating the scaled Gaussian gives the corresponding finite-order estimates for each fixed regulator derivative. The expansion and all coefficient moments are therefore strong and source-test uniform on bounded smooth test families, not pointwise approximations of an arbitrary profinite section.

Since $B_z$ is fixed and continuous on compact distributions, (159.8) implies

$$
h_yv_\epsilon^W\longrightarrow
\rho(0)\,G(x)\bigl[\delta_0(z)-b_0(z)\bigr]
\quad\text{in }\mathcal E'(U^2).
\tag{159.10}
$$

At $(x,z)=(0,0)$, both $G$ and $\delta_0-b_0$ are genuinely singular. Their external tensor product has pure diagonal conormal covectors $(\tau,-\tau)$, $\tau\ne0$: with product localizers, the Fourier transform has the nonrapid $|\xi|^{-2}$ cusp tail in $x$ and the nondecaying delta transform in $z$ along these directions.

**Proposition 159.3 (new zero-scale microlocal boundary trap).** A legal positive-regulator family in the **actual residual $W^0$** has an ambient compact Green primitive whose wavefront excludes the diagonal conormal at every positive scale, yet the distributional leading boundary coefficient of that primitive has a nonzero pure diagonal-conormal wavefront. Therefore fixed-positive-scale exclusion from 153.1 cannot be promoted to a zero-scale diagonal regularity assertion. This is not a counterexample to the existing 108 source class, which allows distributional coefficients on boundary faces; source *membership* of the primitive remains the missing step.

## 5. Two concrete source-lift shortcuts that fail

### 5.1 The hidden-vertex R1 product is forbidden

To produce the regulator layer $\kappa_\epsilon(z)$, a tempting exact output history is to retain a hidden vertex $y$ fixed at zero and attach the legal edge $\kappa_\epsilon(y-z)$. If one tries to assign the spatial factor $G(x)$ to the new three-coordinate R1 coefficient

$$
T'(x,y,z)=G(x)\delta_0(y)\rho(z),
\tag{159.11}
$$

then at $(x,y,z)=(0,0,0)$ its wavefront contains $(\tau,-\tau,0)$ for $\tau\ne0$, because the $x$ cusp and $y$ delta are independent. That is a forbidden conormal to the partition block $\{x,y\}$ (with $z$ singleton). The Gaussian scalar edge does not license such an R1 input, and arbitrary multiplication of overlapping singular coefficients is not an admitted operation. Thus (159.11) is **not a legal candidate source**. This is a rigorous no-go for that *particular augmented-factor construction*, not for all other histories.

### 5.2 No spectator-regular, no-hidden two-slot lift

Choose a small interval $I\Subset U\setminus\{0\}$ where $G$ is smooth and nonzero, and $J\Subset U$ containing zero, with disjoint closures. Consider a finite collection of **identity-partition output histories with no hidden vertices**, each with a scalar coefficient from a fixed admissible two-retained-vertex 105.5 heat-stage and a fixed R1 graph coefficient whose cone over $I\times J$ has no nonzero $z$ covectors. Include their completed projective tensor coefficients and fixed Sobolev refinements. Such R1 coefficients are smooth in $z$ with values in distributions in $x$.

On the product rectangle $I\times J$, the collision face $x=z$ is absent. The scalar coefficients therefore have complete fixed-index power/logarithmic expansions at the *ordinary strict regulator face*, with coefficients smooth in $(x,z)$ and uniform tangential remainder bounds. After multiplication by the stated spectator-regular R1 stages and completion, every asymptotic coefficient of the finite sum is smooth in $z$ with values in $\mathcal D'(I)$. If the whole family converges distributionally as $\epsilon\downarrow0$, every negative-power or divergent-logarithm coefficient of the sum must cancel, and its actual limit is the smooth-in-$z$ exponent-zero coefficient. This follows from uniqueness of the locally finite fixed-index expansion, applied after any compact distributional test in $x$.

But the actual limit (159.10) on this rectangle equals

$$
\rho(0)\,G(x)\bigl[\delta_0(z)-b_0(z)\bigr],
\tag{159.12}
$$

which is **not** smooth in $z$ on $I\times J$. This contradiction proves:

**Proposition 159.4 (strict-face obstruction).** No finite sum of fixed completed, *spectator-regular*, no-hidden, identity-partition two-slot histories of the specified type can evaluate to the whole family (159.7). In particular the one-history spectator template of 156 does not generalize by merely changing its R1 factor to a spatial cusp and keeping a scalar two-vertex heat coefficient.

This proposition does **not** address histories with hidden vertices, fixed R1 cones permitting $z$ singularities, same-block jets later canceled in evaluated sums, or any other full 108.7 presentation. It is explicitly **not** nonmembership of (159.7) in $\mathcal P_2$.

## 6. Exact finite tests and research verdict

The standard-library [159 fixture](fixtures/nonspectator_green_controls_159.py) uses exact rational arithmetic. It verifies the two affine bump moments, the Green second-difference and finite support, the moment-zero $W$ input and exact Green output for all 242 nonzero ternary five-site input vectors (13,310 output pairings), and 81 polynomial Gaussian/Wick moment expansions. This detects sign, projection and normalization mistakes but is not a computational proof of wavefront, scalar conormal stages or categorical source nonmembership.

| Required scientific obligation | Result of primary 159 |
| --- | --- |
| Genuine integrated-coordinate-singular R1 Gaussian source | **EXPLICIT, ADMITTED SOURCE** |
| Whole normalized compact Green formula | **EXACT AMBIENT IDENTITY** |
| Explicit residual $W^0$ input | **CONSTRUCTED IN EXISTING SOURCE** |
| Zero-scale boundary diagonal conormal after fixed-scale avoidance | **PROVED** |
| Illegal hidden-variable R1 product shortcut | **REFUTED** by a forbidden partition conormal |
| Spectator-regular no-hidden two-slot output template | **REFUTED** by strict-face distributional singularity |
| Every possible existing 108.7 output history | **NOT ANALYZED EXHAUSTIVELY** |
| Universal Lemma 150.L and residual $W$ acyclicity | **OPEN** |
| Original R3, 126.14 recovery, higher weights and M5/R4 | **OPEN** |

**Next substantive mathematical input:** attack the hidden-vertex and non-spectator R1 cones *within the existing category*, incorporating the additional Gaussian contraction, proper physical densities, source conormal transversality and completed all-corner scalar index stages. Either give a legal exact history for (159.7), or prove that **all** such histories fail. Neither strict-face no-go above nor the zero-scale wavefront phenomenon alone establishes global failure.

**Custody:** This is a primary 159 manuscript, not a reviewed mathematical acceptance or final REACH proof. It requires source-locked logical critical review 160, bounded ledger 161, protected CI/merge/readback and CP186 continuity. No previously admitted assertion or protected policy is modified.
