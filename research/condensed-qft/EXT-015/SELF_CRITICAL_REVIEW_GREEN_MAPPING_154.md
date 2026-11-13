# EXT-015 / 154 — source-bound mathematical self-review of the Green mapping-input audit

**Disposition: BOUNDED ACCEPT as an ambient microlocal lemma and diagnostic audit; NO NEW MIXED SOURCE LIFT; 150.L OPEN.**

**Review provenance:** This is a substantive mathematical **self-review** performed at the user's request by the same assistant context that contributed to primary 153 and the 154 handoff. It is *not* a genuinely nonauthor or separately executed critic review, not an external referee report, not a GitHub native nonauthor approval, and not mathematical certification. It does not satisfy the logically distinct critic-role condition by merely calling itself a review. No 155 acceptance ledger may assert independent mathematical acceptance on the basis of this artifact alone. The narrow mathematical findings can nevertheless be checked and used for a later distinct review. Publication of this review in a protected source PR is a separate event.

## 1. Exact source custody

| Record | Identity |
| --- | --- |
| Primary source | [MIXED_GREEN_KERNEL_MAPPING_AUDIT_153.md](MIXED_GREEN_KERNEL_MAPPING_AUDIT_153.md) |
| Frozen primary Git blob | ad0ba1a607e03337dd7489b1d2ea3415fd2afed9 |
| Source PR reviewed head | c6c43d53d928a7736cc8fb3476a55fb4194cba15 |
| Source protected merge | [PR 3282](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3282), commit 21e9a5ba32362b4ca16588f65e490daa97b5628a |
| Finite fixture blob | e9cd1c4e39d1e512c48a13d7c86d2fa6d1ee2be4 |
| Existing 150 | [COMPLEMENTARY_WEIGHT_TWO_COMPARISON_150.md](COMPLEMENTARY_WEIGHT_TWO_COMPARISON_150.md), blob 03deca9212a9bea56743e482e5cb79edb46b9d7f |
| Existing 108 | [MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md), blob 587c15fd6e24f6e6b14de574ff878221cdbd5cb6 |
| Existing 147 | [WEIGHT_TWO_DIAGONAL_JET_COMPARISON_147.md](WEIGHT_TWO_DIAGONAL_JET_COMPARISON_147.md), blob 89b3d4a835f3750114e983854585e33d8184cb1f |
| Producer-side adversarial handoff | [GREEN_MAPPING_CRITIC_HANDOFF_154.md](GREEN_MAPPING_CRITIC_HANDOFF_154.md), independent reviewer still required |

Source 150 §2 supplies the normalized compact Green operator and negative-Sobolev estimates. Source 150 §3 already proves the stronger one-coordinate R1 graph-source convolution theorem, with cone exclusion and finite off-cone estimates. Source 147 §2 describes fixed-stage center-valued normal regularity for distinct-block outputs. Source 108 §4 defines the complete mixed image as finite sums of evaluated histories with coefficients in the completed product $E_{s,K,\Gamma}\widehat\otimes_\pi S_\lambda$. Review below does not upgrade the old primary source from historical "unreviewed" wording or amend any protected prior claim.

## 2. Independent mathematical derivation of the restricted wavefront statement

Let $v\in\mathcal E'(U^2)$ with $\mathrm{WF}(v)\cap N^*\Delta=\varnothing$, where $\Delta$ is $x_1=x_2$ and zero covectors are excluded by wavefront convention. Fix $i\in\{1,2\}$, bumps $b_0,b_1$, moments $m_{i,j}$, $B_i=\sum_jb_j(x_i)m_{i,j}$ and $h_i=e*_{x_i}(1-B_i)$.

Distributional differentiation gives

$$
\partial_{x_i}^2 h_iv=(1-B_i)v,
\qquad
e(t)=|t|/2,
\qquad e''=\delta_0.
$$

For every fixed test function of $x_i$, the partial moment has distributional dependence only on the other variable. The tensor $b_j(x_i)m_{i,j}v$ is smooth in $x_i$, so its wavefront is contained in the characteristic set $\{\xi_i=0\}$ of the partial derivative operator. At any diagonal conormal $(x,x;\tau,-\tau)$ with $\tau\ne0$, the principal symbol of $\partial_{x_i}^2$ is $-\tau^2\ne0$. Microlocal elliptic regularity supplies both inclusions of the wavefront sets of $h_iv$ and $\partial_{x_i}^2 h_iv$ at that covector. The latter equals $(1-B_i)v$, which has no diagonal conormal; thus neither does $h_iv$.

The argument depends on **compact normalization** for the globally defined primitive but the local wavefront step depends only on the differential identity and ellipticity. It does not require any representation of $h_iv$ by a mixed-source history. The same-block diagonal delta violates the input hypothesis, so the accepted $\lvert x_1-x_2\rvert$ cusp is not an objection.

**Finding R154.1 — ACCEPT, fixed-positive-scale ambient wavefront statement.** This is a valid direct elliptic derivation. It is not a result about scalar index families, completion, the rapid quotient, or the zero-regulator boundary.

## 3. Finite normal seminorm estimate, with its indispensable uniform hypotheses

The qualitative statement cannot be applied to arbitrary collections with independently varying wavefront cones. Take a *fixed* compact $K$ and closed input cone $\Gamma$ disjoint from the diagonal conormal over the relevant spatial compact. Choose a compact conic neighborhood $\Omega$ of the target part of the diagonal conormal whose closure avoids both $\Gamma$ and the characteristic set $\{\xi_i=0\}$. Choose properly supported order-zero localizers $A$ microlocalized in $\Omega$ and a microlocal inverse $Q$ of order $-2$ to $\partial_{x_i}^2$ there, with a smooth microlocal remainder $R$ on $\Omega$. On the common support,

$$
A h_iv=AQ(1-B_i)v+R h_iv.
$$

For every fixed requested $H^m$ or localized Fourier seminorm, the first term is controlled by finitely many input off-$\Gamma$ seminorms of order at most $m-2$ and one global negative-Sobolev norm to handle the proper cutoffs. The $B_i v$ term is microlocally absent on $\Omega$ and has bounded fixed smooth-tensor/partial-moment maps. The remainder is smoothing in this sector and bounded by a global negative-Sobolev norm of $h_iv$. Source 150.6 controls that norm by a fixed negative-Sobolev norm of $v$, after any finite order relaxation needed by the fixed cutoffs. Thus the proof has finite loss, with one fixed compact/conic stage and finite input seminorms for each target seminorm.

Since the operators and bumps are independent of regulators and parameters, they commute with **each fixed mixed derivative**; but that derivative must itself be included in a fixed admitted stage with moderate input norms. A statement only saying that each individual regulator slice has a wavefront gap would not provide uniform constants, so it must not be used in place of the actual fixed-stage assumptions of 108/126. The accepted Lemma 150.1 already has a stronger R1 graph mapping conclusion under precisely such stage control.

**Finding R154.2 — ACCEPT with this fixed-stage reading.** No proof of global scalar-stage continuity, uniform asymptotic index control or full completed parameter sheaf follows. Any later quotation must state the fixed compact/cone and finite seminorm hypotheses. No unsupported universal family estimate is authorized.

## 4. Novelty and interaction with admitted results

The new Proposition 153.1 is **not** the missing original mapping input. For a two-coordinate R1 coefficient, forbidden partition conormals reduce to the pure diagonal-conormal condition. Source 150.1 already maps such inputs to R1 graph stages with controlled cones, including all fixed normal seminorms. Proposition 153.1 can be retained as a short alternate proof of the microlocal noncreation consequence, but is **logically weaker as a mapping theorem** than source 150.1. The 153 corollary about absence of a new diagonal delta jet at fixed regulator is correspondingly a compatibility statement with 147, not a replacement for 147's intrinsic source-domain projection.

The real 150.L is different: $a_\epsilon T$ is a **complete mixed scalar/R1 coefficient**, and $h_i$ integrates the coordinate on which the scalar can depend. Moving $a_\epsilon$ outside the primitive is not justified. The finite list of legal 108.7 histories, the completed projective tensor map, all finite normal-jet and corner strata, proper densities and 126 mixed parameter rows remain untouched.

**Finding R154.3 — ACCEPT 153 as a bounded audit, not a new 150.L result.**

## 5. Augmented Green product and proper pushforward

At fixed $\epsilon>0$, write $K_\epsilon(x,y,z)=\chi(x)e(x-y)a_\epsilon(y,z)T(y,z)$. A nonzero conormal of $e(x-y)$ at $x=y$ has new-$x$ component $t\ne0$. Every wavefront covector of the pullback of $a_\epsilon T$ from $(y,z)$ has new-$x$ component zero. Therefore opposite covectors never occur, the Hörmander product exists, and the fixed compact support allows proper pushforward in $y$. The density is the ordinary physical $dy$; in the displayed $x-y$ affine coordinate its Jacobian is $1$. These ambient operations are valid distribution operations.

But on the augmented space $e(x-y)$ is neither a smooth positive-scale scalar factor from $S_\lambda$ nor an admissible R1 factor (its conormal is forbidden on the new block diagonal). There is no theorem permitting this augmented factor as a typed 108.7 history. Even if its **output** becomes R1-admissible after integration, this says nothing about representing the *mixed coefficient and all regulator asymptotics* by existing finite completed sources. No false global source conclusion is derived.

**Finding R154.4 — ACCEPT ambient existence and non-admissibility warning; the asserted missing mixed mapping theorem remains absent.**

## 6. Independent exact analytic hostile calculation

A compact distribution $T(y,z)=\delta_0(y)\rho(z)$ with smooth nonzero compact $\rho$ has wavefront covectors $(\eta,0)$ and is admissible as a two-slot R1 coefficient: its nonzero covectors never equal pure diagonal normals $(\eta,-\eta)$. Let $a(y,z)=y^2\chi(y,z)$ with $\chi$ smooth compact and $1$ near a region of $(0,z)$ where $\rho\ne0$. Then $aT=0$ identically, hence $h_1(aT)=0$.

On the other hand $m_{1,0}T=\rho$, $m_{1,1}T=0$, so

$$
h_1T(x,z)=\rho(z)\left(e(x)-(e*b_0)(x)\right).
$$

The smooth convolution $e*b_0$ cannot cancel the jump of $e'$ at zero, and

$$
\partial_x^2(e-e*b_0)=\delta_0-b_0.
$$

Thus $e-e*b_0$ is nonzero on at least one punctured neighborhood of zero. Multiplication by $x^2\chi(x,z)\rho(z)$ then gives a nonzero distribution there. Consequently

$$
h_1(aT)=0\ne a\,h_1T.
$$

This is an **exact distributional counterexample** to commuting an arbitrary smooth coefficient through the partial Green primitive. It is not an example of failure of $h_1(aT)$ to have a legal representation (the left side is zero), and therefore not a counterexample to 150.L.

**Finding R154.5 — PASS, narrow hostile test; no overclaim.** No numerical sample is required to establish the jump of $e'$.

## 7. Negative controls, coefficient-stage boundary and review verdict

The Gaussian Fourier negative control of source 150 forbids inferring rapid Fourier coefficient decay in a fixed asymptotic scalar stage from pointwise positive-regulator convergence. The same-block delta cusp forbids extending the primitive to all source histories; neither refutes its **restricted** distinct-block hypothesis. The 242-input lattice fixture checks only moment and difference algebra. None of these checks supplies completed-source membership.

| Critical obligation | Mathematical disposition |
| --- | --- |
| Fixed-regulator pure conormal noncreation | **BOUNDED ACCEPT** from ellipticity |
| Fixed-stage finite normal-topology estimates | **BOUNDED ACCEPT** under common compact/conic stage and derivative hypotheses |
| Novel Green mixed-source mapping mechanism | **NOT ESTABLISHED**; weaker R1 result already in 150.1 |
| Ambient augmented Green product and pushforward | **ACCEPT** fixed-regulator distributional operation |
| Typed finite 108.7 mixed-source lift | **OPEN — 150.L** |
| Scalar/Green commutation shortcut | **REJECTED** by exact R1-admissible counterexample |
| Residual $W$ acyclicity; original R3 | **OPEN** |
| Whole-source 126 parameter rows and liquid descent | **OPEN** |
| Independent reviewer provenance | **NOT SATISFIED** by this self-review |

**Technical outcome:** No defect was found that requires altering the accepted scoped statement of 153.1. Its *novelty* must not be overestimated. The appropriate result is **VALID_BOUNDED_MICROLOCAL_AUDIT / NO_NEW_MIXED_SOURCE_MAPPING / 150.L_OPEN**. The distinct mathematical critic may issue a different disposition after its own analysis.

**Process outcome:** This is the actual substantive self-review requested by the user, not merely a call to summon another reviewer. The logical nonauthor critic condition, if imposed for formal acceptance, remains an independent control: this reviewer cannot self-attest its satisfaction. The review text may be protected-admitted as a scientific record through native checks without constituting independent acceptance. Do not issue a 155 ledger claiming acceptance or close 150.L on this basis.

The next constructive *mathematical* input is a genuine mixed Green pushforward/source representation with fixed completed scalar/R1 stages and all-corner uniform parameter estimates, or a restricted counterexample in the actual $Y=\ker P$ source. The next independent *process* obligation, if substantive acceptance is required, is source-bound nonauthor review of this material before the final 155 ledger.
