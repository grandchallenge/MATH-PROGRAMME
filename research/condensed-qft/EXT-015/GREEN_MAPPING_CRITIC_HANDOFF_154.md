# EXT-015 REACH / 154 handoff — Green mapping critical assessment

**Status: PRODUCER-SIDE CRITICAL WORKPAPER; NOT REVIEW 154 AND NOT MATHEMATICAL ACCEPTANCE.** This document is a source-bound review handoff for a genuinely distinct critic. Its authoring context also contributed to primary 153. It therefore cannot claim the independent/non-author review role, even though its proof checks and counterexample can be inspected now. The required exact artifact AGENT_CRITICAL_REVIEW_GREEN_MAPPING_154.md must be produced or independently adjudicated by an eligible distinct reviewer; only then may GREEN_MAPPING_AUDIT_ACCEPTANCE_155.md record a verdict. No mathematical closure or external certification is asserted.

## 1. Immutable subject and authority boundary

| Object | Identity / provenance |
| --- | --- |
| Admitted primary 153 | [MIXED_GREEN_KERNEL_MAPPING_AUDIT_153.md](MIXED_GREEN_KERNEL_MAPPING_AUDIT_153.md), Git blob ad0ba1a607e03337dd7489b1d2ea3415fd2afed9 |
| Primary exact reviewed PR head | c6c43d53d928a7736cc8fb3476a55fb4194cba15 |
| Protected source admission | [PR 3282](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3282), merge 21e9a5ba32362b4ca16588f65e490daa97b5628a |
| Finite arithmetic fixture | [green_moment_control_153.py](fixtures/green_moment_control_153.py), Git blob e9cd1c4e39d1e512c48a13d7c86d2fa6d1ee2be4 |
| Native GitHub approval | jimsteeg review 5888048869 on exact head, empty review body; source-custody evidence, NOT a mathematical critique |
| Existing result 150 | [COMPLEMENTARY_WEIGHT_TWO_COMPARISON_150.md](COMPLEMENTARY_WEIGHT_TWO_COMPARISON_150.md), Git blob 03deca9212a9bea56743e482e5cb79edb46b9d7f |
| Existing source 108 | [MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md), Git blob 587c15fd6e24f6e6b14de574ff878221cdbd5cb6 |
| Existing source 147 | [WEIGHT_TWO_DIAGONAL_JET_COMPARISON_147.md](WEIGHT_TWO_DIAGONAL_JET_COMPARISON_147.md), Git blob 89b3d4a835f3750114e983854585e33d8184cb1f |
| Earlier review 151 | [AGENT_CRITICAL_REVIEW_COMPLEMENTARY_WEIGHT_TWO_151.md](AGENT_CRITICAL_REVIEW_COMPLEMENTARY_WEIGHT_TWO_151.md), Git blob 222424fd3a3d9b49d4268120f24958512c3c5bfe |

All identities above are for already protected sources, not for an asserted recomputation of the old 95-entry frozen manifest. The live protected main is moving independently; use blob identities, not a bare branch name, in the distinct review.

The question under test is source-lifting Lemma 150.L on actual complete mixed histories (108.7), with the fixed scalar stages and completed projective coefficient tensors. The primary 153 explicitly does **not** prove it. The governing issues [#2657](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2657), [#2617](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2617), and [#2798](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2798) remain open.

## 2. Microlocal argument: sound within its narrow scope, not new mapping input

Write the retained coordinates as $(x_1,x_2)$, let $\Delta$ be the diagonal, and put

$$
D_i=\partial_{x_i}^{2},\qquad
B_i v=\sum_{j=0}^{1}b_j(x_i)m_{i,j}v,\qquad
h_i v=e*_{x_i}(1-B_i)v,\quad e(t)=|t|/2.
$$

The identity $D_i h_i v=(1-B_i)v$ is the already admitted (150.4). Since $B_i v$ is smooth in $x_i$ with possibly distributional coefficients in the other coordinate, its nonzero wavefront covectors have vanishing $x_i$ component. Every nonzero pure diagonal conormal has $x_i$ component $\tau\neq0$. The principal symbol of $D_i$ is $-\xi_i^2$, nonzero at all those covectors. Hence microlocal elliptic regularity gives

$$
\mathrm{WF}(h_i v)\cap(N^*\Delta\setminus0)
=
\mathrm{WF}((1-B_i)v)\cap(N^*\Delta\setminus0)
=
\varnothing
$$

when the input has the same avoidance. This is a valid fixed-positive-regulator proof in the ambient compact distribution space, provided all outputs are considered with the compact normalization already specified in 150.3–150.6.

**Essential novelty check:** accepted **Lemma 150.1** is stronger. It establishes that the one-coordinate Green convolution, with the moment corrections, maps an entire fixed R1 graph source into another fixed R1 graph source with a conormal-excluding cone and finite graph estimates. In two slots its conclusion already implies pure diagonal avoidance. Thus Proposition 153.1 is an alternative elliptic proof or explicit corollary of accepted 150.1, not a previously missing R1 mapping mechanism.

An independent review should determine whether the claimed finite normal-topology bounds follow from a uniform fixed-cone microlocal parametrix and (150.6) at the precise Sobolev order used. Wavefront exclusion for each individual distribution alone does *not* imply a continuous map of complete families; the stated fixed compact supports and fixed closed cones are doing indispensable work. On those stages, the standard parametrix estimate and fixed negative-Sobolev operator bound appear sufficient. This assessment does not extend to arbitrary unpinned parameter rows, regulator asymptotic families or the analytic source image.

**Finding 154-F1: scoped mathematical consequence appears justified; claimed new input to 150.L is ABSENT.**

## 3. Augmented interior Green factor: distribution-theoretic existence versus admissibility

For old block variables $(y,z)$, the formal augmented integrand is

$$
K_\epsilon(x,y,z)=\chi(x)e(x-y)a_\epsilon(y,z)T(y,z).
$$

At fixed positive regulator, $a_\epsilon$ is smooth and $T$ is an admitted R1 distribution. The wavefront of the pulled-back $T(y,z)$ has zero covector component in the new $x$ direction; a nonzero wavefront covector of $e(x-y)$ has nonzero new $x$ component. Thus there is no opposing wavefront pair; the distribution product is defined. Compact support permits proper pushforward in the eliminated variable.

This says **nothing** about an allowed source representative. The nonsmooth factor $e(x-y)$ lies outside the fixed positive-regulator smooth scalar coefficient stages. Used as a new R1 factor it has the forbidden conormal to the enlarged $x=y$ block. The output may lose that forbidden conormal after integrating $y$; however existence of the output in ambient distributions is not a proof that it belongs to the **existing** finite 108.7 image. A scalar b-fibration for the old collision arrangement is not an all-corner mixed pushforward theorem for the enlarged interior conormal.

**Finding 154-F2: product/pushforward well-defined at fixed epsilon; no source-admissible finite history map, scalar index control, complete tensor continuity or mixed-row estimate has been constructed.**

## 4. Exact hostile test against commuting a scalar through the primitive

This elementary counterexample is **new as an explicit control in the 154 handoff**, but is *not* a counterexample to 150.L itself. It rules out a particularly tempting unsupported simplification.

Let $U$ contain the origin. Choose a nonzero compact smooth $\rho(z)$ and take the compact two-slot R1 distribution

$$
T(y,z)=\delta_0(y)\rho(z).
$$

Its wavefront covectors, when nonzero, have the form $(\eta,0)$ in $(y,z)$ coordinates. They are not pure diagonal conormals $(\eta,-\eta)$. Thus this is a permissible fixed R1 input even where its support meets $y=z$.

Let $a(y,z)=y^2\chi(y,z)$, with a fixed compact smooth cutoff $\chi$ equal to one near $(y,z)=(0,z_0)$ for a point $z_0$ where $\rho(z_0)\neq0$. This is a smooth positive-regulator scalar coefficient (independent of the regulator). Then $aT=0$, giving

$$
h_1(aT)=0.
$$

But

$$
h_1T(x,z)=
\rho(z)\bigl(e(x)-(e*b_0)(x)\bigr).
$$

Indeed $m_{1,0}T=\rho$ and $m_{1,1}T=0$. The bracketed compact function satisfies

$$
\partial_x^2\bigl(e-e*b_0\bigr)=\delta_0-b_0.
$$

It has a nonzero first-derivative jump at the origin and cannot vanish on every punctured neighborhood of zero. Consequently choose $x\neq0$ near zero and $z$ near $z_0$ where $\chi=1$ and the bracket does not vanish. Then

$$
a(x,z)h_1T(x,z)
=x^2\chi(x,z)\rho(z)\bigl(e(x)-(e*b_0)(x)\bigr)\neq0.
$$

Thus, as actual distributions,

$$
h_1(aT)\neq a\,h_1T.
$$

This holds in an R1-admissible two-slot sector with an ordinary smooth scalar; no same-block diagonal delta or Gaussian Fourier construction is required. The test only refutes **naively pulling a scalar depending on the integrated coordinate outside Green convolution**. It does not prove that the left side lacks a different finite legal history; here the left side is simply zero. Source-lifting 150.L remains open.

**Finding 154-F3: a proposed factor-through-R1 proof must control the nonzero Green/scalar commutator, including its fixed scalar indices and all collisions, instead of assuming it vanishes.**

## 5. Negative controls, novelty and verdict boundaries

- The same-block diagonal-delta cusp from 150 is excluded from Proposition 153.1 by its conormal hypothesis, so it does not refute the restricted distinct-block closure claim.
- The Gaussian relative-Fourier control from 150 refutes a fixed-stage rapid-decay ansatz; Proposition 153.1 asserts no such decay, so it survives that test. No alternative Fourier-lifting theorem is thereby proved.
- The 242-case rational lattice fixture checks algebra and compact-support/moment identities only. It cannot validate an analytic fixed-cone bound or a completed liquid source map.
- Source 147 supplies actual normal smoothness and diagonal jet decomposition for **admitted** sources. Pure diagonal conormal avoidance of an ambient result does not by itself define the intrinsic jet projection on that ambient object; the primary correctly states this limitation.
- The chain of source stages $E_{s,K,\Gamma}\widehat\otimes_\pi S_\lambda$ has not been constructed for the augmented Green integral. This is the original missing inference.

| Claim proposed for 154 | Current producer-side finding | Mandatory distinct-critic determination |
| --- | --- | --- |
| 153.1 fixed-regulator pure diagonal avoidance | Appears valid by elliptic regularity | Check exact hypotheses and all normal seminorm losses |
| 153.1 is a new mixed mapping mechanism | **No**; weaker than 150.1 on R1 | Confirm subsumption, prohibit novelty overclaim |
| Augmented Green product at fixed scale | Defined ambiently | Verify microlocal transversality, density and properness |
| Finite 108.7 lift for general scalar/Wick stage | **Not proved** | Do not accept by implication from 153.1 |
| Scalar commutation with $h_i$ | False even on permitted R1 input | Check explicit delta/bump counterexample |
| Residual $W$ acyclicity or original R3 | **Open** | Keep 150.L and all downstream targets open |
| Source-custody and independent review | PR 3282 merged; its GitHub review had no mathematical body | Require genuinely distinct, source-bound 154 verdict |

**Producer-side recommendation:** accept the fixed-regulator elliptic implication only as an alternative derivation of the existing 150.1-controlled R1 statement. The 153 return provides an accurate *negative audit* of proposed mapping input, not an exit from 150.L. Independent review may find further corrections. The protected scientific milestone should remain **NO_NEW_MIXED_MAPPING_INPUT / 150.L OPEN**, not **GREEN_MAPPING_PROVED**.

## 6. Distinct reviewer handoff and next operation

The independent reviewer must inspect the exact primary 153 blob ad0ba1a607e03337dd7489b1d2ea3415fd2afed9, this workpaper, the exact inputs 150/108/147 and the original 150.L wording. Their report must:

1. Give a substantive, original mathematical assessment of F1–F3 and the finite-loss estimate, with ACCEPT / CORRECTION / REJECT at exact source identity.
2. If correction is required, specify one consolidated source correction and re-review the corrected blob rather than silently accepting unseen changes.
3. Preserve authorship: this document is **not** the distinct critic's report. A native GitHub approval with no mathematical findings is not a substitute for it.
4. Produce the definitive AGENT_CRITICAL_REVIEW_GREEN_MAPPING_154.md only after the distinct-role review is actually performed. Then create GREEN_MAPPING_AUDIT_ACCEPTANCE_155.md with a scoped scientific decision and separately verify protected admission.
5. Avoid declaring completion of 150.L, the derived/LF comparison, full family recovery 126.14, original R3, higher weights, actual lifting or M5/R4 integration.

No additional declaration of protected acceptance is made by committing this handoff. The earlier CP183 main checkpoint remains a historical continuum record pending explicit reconciliation.
