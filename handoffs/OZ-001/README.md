# OZ-001 continuity handoff

## Authority and scope

- Workset: `OZ-001`.
- Target repository: `grandchallenge/MATH-PROGRAMME`.
- Constitutional authority repository: `grandchallenge/INTELLECT`.
- Constitutional authority head re-read for this continuation: `fc9ee5537bf07586dffcc621e753204ecd835365`.
- Protected MATH-PROGRAMME predecessor: `a05c16d2988a9a0c73f9c62b482c96777a49c5ea`.
- Umbrella tracker: `grandchallenge/MATH-PROGRAMME#113` is navigation only.
- Current Programme successor issue: `grandchallenge/MATH-PROGRAMME#964` (`OZ-RT-BZ-T3-016-A`).

Always re-read live protected heads before mutation. Hashes here record the exact state of this handoff and are not substitutes for current protected-state readback.

## Source lock

Current admitted upstream source revision:

- repository: `rain-1/-odd-zeta-values-moremath`;
- commit: `6cc0bf07137815ceeef0d9f340559f85352391e5`;
- tree: `be780558454b704bdd016a3070d698c2e106e2b8`;
- Programme source disposition remains partial admission with blockers;
- `promotion_effect: NONE`.

Order-7 loci used by the current successor:

- `work/Z5CF_TELESCOPER.md`: blob `a634b070d5d95d09749137c26bc51012f318683b`;
- `work/Z5CF_LIFT.md`: blob `f1c48b2ce0951ef4a4aefa1d449e53fe33ce5cc5`;
- `work/Z5CF_LINALG.md`: blob `637ecaa7f3ee941a87932de390eb7336d7fde677`;
- `work/z5la/z5cf_order7_partial.json`: blob `d6024c7244a4a45ac759b455f65fca6d377b735d`;
- `work/z5la/a_lift.json`: blob `564fc9637f31b870d85dab293d6cbb5cfe52bae0`.

Source-reported mathematics remains candidate evidence until independently replayed in the Programme. Modular evidence is used only where it supplies an exact nonzero-minor witness or other completeness-backed implication.

## Exhausted protected T3 classes

Do not silently recycle these as successors:

- T3-011 through R: frozen coordinate-zero Laurent-monomial multiplier-response algebra structurally exhausted; terminal corollary `FROZEN_COORDINATE_ZERO_LAURENT_MONOMIAL_RESPONSE_ALGEBRA_COKERNEL_INVISIBLE`.
- T3-012-A: `NORMALIZED_RECURRENCE_OPERATOR_TANGENT_POLY_DEG_LE_9_EXHAUSTED`.
- T3-012-B: `SUPPORT_LOCKED_DEGREE0_COUPLED_CORRECTION_RECOMBINATION_INCOMPATIBLE`.
- T3-013-A: fixed source coefficient class `span_Q {1,rho,sigma}` exhausted; terminal `QROW_CERTIFICATE_WEIGHTED_STRICT_INTERIOR_SUBSYSTEM_INCONSISTENT`.
- T3-015-C: the full protected 506-function reduced-residual class `SOURCE_DECLARED_RATIONAL_DELTA_COEFFICIENT_CLASS_001` is completeness-obstructed under its admitted architecture.

## T3-015-C protected completion

T3-015-A extracted the canonical 506-generator rational-difference module with SHA-256

`cdabf6d7873f3aa8e9d53b39fd7b15341dbee58ce9684911d015aee9aaae04da`.

T3-015-B established its exact structural reduction. T3-015-C isolated the unique maximal-degree witness coordinate

`M = H_k_2 * H_nk_1 * H_nkl_1`.

Only generator 59 contributes. Every global certificate in the admitted class would have to satisfy

`q_59(n,k+1,l) - q_59(n,k,l) = 1/(k+l+1)`.

Over `Q(n,l)(k)`, every rational forward difference has zero discrete residue on each integer-shift pole orbit. The right-hand side has simple-orbit residue 1. Hence no rational `q_59` exists.

Protected identities:

- proposal head: `c3f3c2fd2dc71b96133934a05eb578fd6c191173`;
- protected merge/readback: `a05c16d2988a9a0c73f9c62b482c96777a49c5ea`;
- terminal: `GLOBAL_RATIONAL_DELTA_CLASS_OBSTRUCTED__COMPLETENESS_BACKED`.

This refutes only the protected reduced-residual architecture. T3 itself remains open.

## Current T3 frontier

The current successor is issue #964:

`OZ-RT-BZ-T3-016-A — order-7 discrete-curl / Popov certificate compression`.

This is a separately governed architecture route and does **not** reopen T3-015-C.

The pinned source reports a minimal order-7 left multiple

`L_min = A * L_BZ`,

with

`A = sum_{t=0}^4 a_t(n) S_n^t`, `a_t in Z[n]`.

The current PR #965 independently replays the constant-first lifted coefficient objects, exact `a_4(n) != 0` argument, module shape, and normalized-shift flatness.

### Reconciled E1 geometry

The source report `rank=1106` in 1624 columns / kernel dimension `518` is **not** promoted. Independent reconstruction of the stated E1 ansatz yields the corrected generic geometry

- `rank(E1) = 1048`;
- `dim ker(E1) = 576`;
- `ker(E1) = image(discrete curl)` over `Q(n)`.

For

`D = (k+1)(l+1)(k+l+1)(k+l+2) prod_{j=1..7}(n+k+j)(n+l+j)`,

with E1 numerator bidegree at most `(28,28)` and boundary forcing, the complete homogeneous freedom is parameterized by

`h = k^2 l^2 H(k,l) / ((k+l+1) prod_{j=1..6}(n+k+j)(n+l+j))`,

`bideg(H) <= (23,23)`, giving exactly `24^2 = 576` parameters, and

`(r,s) = (gl*h(k,l+1)-h, -(gk*h(k+1,l)-h))`.

Exact denominator clearing puts every such pair inside E1. Exact flatness makes its divergence zero. A rank-576 modular nonzero-minor witness proves generic curl dimension 576; a rank-1048 witness for an independently reconstructed 1048-by-1624 E1 evaluation matrix proves generic operator rank at least 1048. Since the 576-dimensional curl image already lies in the kernel, rank is at most 1048. Equality follows in characteristic zero.

Deterministic witness data are recorded in `campaigns/odd_zeta/OZ_RT_BZ_T3_016_A/CONTRACT.json` and replayed independently by producer and verifier.

Current intermediate terminal, subject to protected admission of PR #965:

`ORDER7_E1_KERNEL_IDENTIFIED_AS_DISCRETE_CURL__POTENTIAL_SECTION_REDUCTION_REQUIRED`.

### Remaining affine compression problem

The remaining task is not to discover an opaque 518-dimensional quotient. It is to choose the 576 coefficient functions of the exact potential `H` so that a particular residual cofactor section has minimal `n`-degree and height.

The next exact sequence is:

1. reconstruct a particular E1 residual section over sufficient exact/modular `n` samples;
2. attach the exact 576-potential homogeneous parameterization;
3. formulate the affine section problem over `Q[n]`;
4. compute a shifted Popov/minimal-approximant/order basis, or equivalent completeness-backed degree reduction, in the potential coordinates;
5. reconstruct the seven standalone residual blocks in characteristic zero;
6. propagate the compatible gauge into the constant block;
7. independently replay all fifteen order-7 identities and pole/boundary obligations;
8. verify finite initial conditions and the `a_4 != 0` induction before any separately governed T3 bridge.

The source's two high-degree pivot gauges remain negative diagnostics about those representatives. They are not a completeness-backed obstruction to a lower-degree potential section.

A positive compression result is not itself T3.

## Claim firewall

Until a separately governed successor changes protected state:

- `t3_proved = false`;
- `t3_refuted = false`;
- `global_certificate_constructed = false`;
- `residual_sum_zero_proved = false` for the promoted T3 target;
- `proof_effect = NONE`;
- `promotion_effect = NONE`.

T3 does not automatically discharge T1-top, DEPTH, Sharp-12, primes `2,3`, formal replay, MATHCERT, irrationality, infinitude, novelty, publication, patentability, deployment, product, or commercial gates.

## Independent OZ lanes

- T1-top remains `OPEN_WITH_CHARACTERIZED_BLOCKER`.
- DEPTH remains `OPEN_WITH_CHARACTERIZED_BLOCKER`.
- Sharp-12 remains gated by separately accepted T1-top and DEPTH results.
- Primes `2,3` remain outside the current conditional `p >= 5` chain.
- Eisenstein-companion and cuspidal/Fricke packets retain their existing source-admission blockers.
- Formal replay remains independently governed.
- MATHCERT route `MC-ROUTE-OZ-001` remains pending absent an accepted certifiable OZ proof object.

## Authoritative pointers for continuation

Read from protected state before mutation:

- `governance/governed_campaign_registry.json`;
- `governance/mathsolve_routing_audit.json`;
- `campaigns/odd_zeta/OZ_SOURCE_REVISION_DELTA_003/OZ_SOURCE_REVISION_DELTA_003.json`;
- `campaigns/odd_zeta/OZ_RT_BZ_T3_015_A/`;
- `campaigns/odd_zeta/OZ_RT_BZ_T3_015_B/`;
- `campaigns/odd_zeta/OZ_RT_BZ_T3_015_C/`;
- `campaigns/odd_zeta/OZ_RT_BZ_T3_016_A/`;
- issue #964 for the current work contract;
- `grandchallenge/MATHCERT:governance/certification_routes.json`, route `MC-ROUTE-OZ-001`.

## Stop conditions

Stop only on a genuine authority, governance, authentication, safety, material source/target drift, exact verification failure that cannot be repaired within scope, a completeness-backed mathematical obstruction, or separately established material closure.

Routine solver engineering, modular acceleration, polynomial-matrix/order-basis implementation, CI recovery, exact reconstruction, and documentary repair are not Human-Steward stop conditions under the currently authorized continuation.
