# EXT-015 / 154 — source-locked critical review of the Green mapping audit

**Verdict: BOUNDED ACCEPT of the fixed-regulator microlocal theorem and diagnostic audit. Source-lifting lemma 150.L is OPEN.** This is the canonical review return for [primary 153](MIXED_GREEN_KERNEL_MAPPING_AUDIT_153.md), not an acceptance of the mixed-source comparison or full REACH.

## 1. Exact sources and role provenance

| Object | Fixed identity |
| --- | --- |
| Primary 153 | Blob ad0ba1a607e03337dd7489b1d2ea3415fd2afed9 |
| Primary PR | [#3282](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3282), head c6c43d53d928a7736cc8fb3476a55fb4194cba15, protected merge 21e9a5ba32362b4ca16588f65e490daa97b5628a |
| Exact finite fixture | Blob e9cd1c4e39d1e512c48a13d7c86d2fa6d1ee2be4 |
| [Source 150](COMPLEMENTARY_WEIGHT_TWO_COMPARISON_150.md) | Blob 03deca9212a9bea56743e482e5cb79edb46b9d7f |
| [Source 108](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md) | Blob 587c15fd6e24f6e6b14de574ff878221cdbd5cb6 |
| [Source 147](WEIGHT_TWO_DIAGONAL_JET_COMPARISON_147.md) | Blob 89b3d4a835f3750114e983854585e33d8184cb1f |
| [Source review 151](AGENT_CRITICAL_REVIEW_COMPLEMENTARY_WEIGHT_TWO_151.md) | Blob 222424fd3a3d9b49d4268120f24958512c3c5bfe |
| [Producer handoff](GREEN_MAPPING_CRITIC_HANDOFF_154.md) | Blob f8cdde946eb24f19da5875845a88c03cab23a04e |
| [Earlier self-review](SELF_CRITICAL_REVIEW_GREEN_MAPPING_154.md) | Blob 455b4861a7799588f1deb1f430a8eba9f1db9c09 |
| Handoff and self-review admission | [PR #3289](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3289), protected merge d46ac14c89259f4c53dd8618bd600ca56d78df5a |

The previous review was accurately labeled a producer-origin *self-review*. This separate return implements two genuinely different **logical audit passes** against the immutable primary, as permitted by GCL-AGENT-STAFFING-001: V154 (Verifier) independently rederives the claimed implication and its quantitative hypotheses; A154 (Adversary) constructs and tests attempts to invalidate or overextend it. Their different objectives, arguments and permitted negative findings are recorded below. They are performed by one ChatGPT system with shared historical context and the same GitHub identity, **not** by separately authenticated agents, people, or external mathematical referees. No MATHCERT or external certification authority is claimed.

## 2. V154 — distribution and microlocal proof obligations

Fix compact $v\in\mathcal E'(U^2)$, an interval $U$, and normalized compact bumps satisfying $\int x^j b_k(x)\,dx=\delta_{jk}$ for $j,k=0,1$. With partial moments $m_{i,j}$ put

$$
B_i v=\sum_{j=0}^1 b_j(x_i)m_{i,j}v,\qquad
h_i v=e*_{x_i}(1-B_i)v,\qquad e(t)=|t|/2.
$$

In distributions $e''=\delta_0$, so the identity from source 150.4 gives

$$
\partial_{x_i}^2h_iv=(1-B_i)v.
$$

Each $B_i v$ is smooth in $x_i$, with distribution coefficients only in the other coordinate. Thus every nonzero wavefront covector of $B_i v$ has $\xi_i=0$. Along the pure diagonal conormal the covectors are $(x,x;\tau,-\tau)$ with $\tau\neq0$. The principal symbol of $\partial_{x_i}^2$ is $-\xi_i^2$, nonzero there. Microlocal elliptic regularity therefore identifies the wavefront presence of $h_i v$ and $(1-B_i)v$ at these covectors. If $v$ has no pure diagonal conormal, neither term on the right does. Hence

$$
\mathrm{WF}(h_i v)\cap(N^*\Delta\setminus0)=\varnothing.
$$

The global compact normalization is also valid: $(1-B_i)v$ has zero zeroth and first moments in the integrated coordinate. The convolution with the affine tails of $|t|/2$ is therefore zero outside the interval hull of the original supports and the bump supports. No singular distribution product is used in this argument. The same-block delta input in 150.15 violates the hypothesis and does not refute the conclusion.

**V154 qualitative verdict: ACCEPT**, strictly for the ambient fixed-positive-regulator conormal-exclusion claim.

## 3. V154 — finite normal-topology bounds and hostile uniformity test

Qualitative wavefront exclusion at each regulator is not uniform source continuity. The proposed estimate needs a common spatial compact $K$, a fixed enclosing input cone $\Gamma$ disjoint from the target diagonal conormal, and fixed compact conic localizers in a smaller conic neighborhood $\Omega$ avoiding both $\Gamma$ and $\{\xi_i=0\}$. Let $A$ be properly supported of order zero in that sector, $Q$ a microlocal order-minus-two parametrix of $\partial_{x_i}^2$, and $R$ its smoothing remainder on the sector. Local elliptic regularity yields

$$
Ah_iv=AQ(1-B_i)v+Rh_iv.
$$

For a fixed target Sobolev index, finitely many graph seminorms of $v$ outside $\Gamma$ control the first term, together with a global negative Sobolev norm for the fixed spatial cutoffs. The moment term is microlocally absent on $\Omega$, and its fixed smooth-tensor/partial-moment operator is continuous in the required finite normal seminorms. The remainder is bounded by a global negative Sobolev norm of $h_iv$, which source 150.6 bounds by that of $v$ at fixed supports and bumps. Source 108 permits finite order relaxation. All fixed parameter and regulator derivatives commute with $h_i$, but each derivative must be controlled in the input stage. Therefore the claimed finite loss is justified on these fixed stages only.

**Adversarial check:** for $\chi\in C_c^\infty(U^2)$ the smooth family $\chi(x_1,x_2)\exp(i(x_1-x_2)/\epsilon)$ has empty wavefront at every positive regulator, yet its normal-direction Sobolev seminorms grow with $\epsilon^{-1}$. The fact that each slice is smooth does not furnish the uniform input stage bounds required by 108 and 126. The primary theorem survives because it expressly includes the fixed stages; applying it to arbitrary unpinned families would be invalid.

Source 150.1 already proves a stronger graph-source R1 mapping theorem, whose pure diagonal exclusion includes this narrow microlocal conclusion. Thus 153 is an alternative elliptic derivation, not a new mixed scalar-coefficient mapping input.

**V154 quantitative verdict: ACCEPT WITH FIXED-STAGE HYPOTHESES; REJECT unconditional family continuity or a claim of new 150.L progress.**

## 4. A154 — enlarged Green kernel and type admissibility

At each fixed $\epsilon>0$ the formal augmented integrand is

$$
K_\epsilon(x,y,z)=\chi(x)e(x-y)a_\epsilon(y,z)T(y,z).
$$

The wavefront of $e(x-y)$ at its singular diagonal has a nonzero component in the new $x$ direction; every wavefront covector of the pullback of $a_\epsilon T$ from $(y,z)$ has zero component in the new $x$ direction. The Hörmander opposite-covector obstruction therefore does not occur. The compact $y$ support makes its physical pushforward proper, with affine Jacobian one.

**Attacked inference:** If the new Green factor is placed in the original scalar stage, it fails smoothness on the positive-regulator interior $x=y$ diagonal. If put in an R1 graph coefficient, its conormal to the new collision diagonal is forbidden. The whole product is a well-defined **ambient distribution** but has no demonstrated representation by the typed finite completed histories of 108.7. All simultaneous collision corners, scalar index families, physical densities, finite jets and 126 mixed derivatives remain unverified for a proposed lift. Ordinary scalar b-fibration and source 150.1 do not supply this theorem.

**A154 verdict: ACCEPT ambient product and pushforward; REJECT the jump to a legal mixed history.**

## 5. A154 — exact scalar/Green commutator and two earlier hostile controls

Choose nonzero $\rho\in C_c^\infty(U)$ and $T(y,z)=\delta_0(y)\rho(z)$ (after translating the chosen interior origin if necessary). Its covectors are $(\eta,0)$ and avoid the forbidden two-slot diagonal conormals, so it is an admissible R1 coefficient. Let $a(y,z)=y^2\chi(y,z)$ with $\chi=1$ near $(0,z_0)$ and $\rho(z_0)\neq0$. Then $aT=0$, hence $h_1(aT)=0$. But direct moment evaluation gives

$$
h_1T(x,z)=\rho(z)\bigl(e(x)-(e*b_0)(x)\bigr),
\qquad
\partial_x^2(e-e*b_0)=\delta_0-b_0.
$$

A smooth function $e*b_0$ cannot cancel the derivative jump of $e$ at zero; the bracket is nonzero in every sufficiently small punctured neighborhood, at least at some point. Consequently

$$
a(x,z)h_1T(x,z)\neq0=h_1(aT).
$$

This **disproves scalar commutation**, not lemma 150.L: the Green primitive of the mixed input $aT$ is zero and itself legal. The same-block delta cusp in 150 disproves only unrestricted closure outside the distinct-block hypothesis. The Gaussian Fourier test in 150 disproves the relative-mode rapid-decay method, not the restricted mapping theorem. The 242-input finite lattice test cannot certify an infinite-dimensional liquid or normal-topology statement.

**A154 verdict: hostile controls PASS with no false counterexample promotion.**

## 6. Final exact-source review matrix

| Question | Decision |
| --- | --- |
| Fixed-positive-regulator microlocal noncreation in 153.1 | **ACCEPT** |
| Fixed common-support/cone finite normal seminorm estimates | **ACCEPT WITH STATED HYPOTHESES** |
| Novelty of 153 versus admitted source 150.1 | **NO NEW MIXED MAPPING** |
| Fixed-scale augmented Green product and proper pushforward | **ACCEPT AS AMBIENT DISTRIBUTION ONLY** |
| Arbitrary scalar commutes through $h_i$ | **REJECT** |
| Mixed finite 108.7 completed-source lift 150.L | **UNPROVED** |
| Residual $W=\ker(P,m)$ acyclicity; original R3 | **UNPROVED** |
| Full 126.14 family recovery, higher weights, actual lifting and M5/R4 | **OPEN** |

**Canonical disposition: BOUNDED_ACCEPT__NO_MIXED_SOURCE_LIFT__150L_OPEN.** Verifier and Adversary are separate logical audit roles under the admitted one-system GCL staffing policy, not third-party proof certifications. They supply a documented source-bound critique rather than a manufactured independent reviewer identity. Review, the subsequent ledger, native GitHub checks and protected merge/readback are distinct facts.

**Next mathematical obligation:** prove a finite legal mixed 108.7 representation of the Green integral on the existing completed scalar/R1 stages with uniform all-corner and mixed parameter-row bounds, or construct an actual distinct-block residual $Y$ counterexample. The 153 audit does not settle either alternative.
