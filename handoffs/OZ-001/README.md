# OZ-001 continuity handoff

## Authority and scope

- Workset: `OZ-001`.
- Target repository: `grandchallenge/MATH-PROGRAMME`.
- Constitutional authority repository: `grandchallenge/INTELLECT`.
- Constitutional authority head re-read for this continuation: `fc9ee5537bf07586dffcc621e753204ecd835365`.
- Protected MATH-PROGRAMME predecessor: `a05c16d2988a9a0c73f9c62b482c96777a49c5ea`.
- Umbrella tracker: `grandchallenge/MATH-PROGRAMME#113` is navigation only.
- Current Programme successor issue: `grandchallenge/MATH-PROGRAMME#964` (`OZ-RT-BZ-T3-016-A`).

Always re-read live protected heads before mutation. Hashes here record this handoff state and do not replace protected-state readback.

## Source lock

Current admitted upstream source revision:

- repository: `rain-1/-odd-zeta-values-moremath`;
- commit: `6cc0bf07137815ceeef0d9f340559f85352391e5`;
- tree: `be780558454b704bdd016a3070d698c2e106e2b8`;
- Programme source disposition remains partial admission with blockers;
- `promotion_effect: NONE`.

Source-reported mathematics remains candidate evidence until independently replayed in the Programme. Modular or sampled evidence does not become theorem authority merely because it is source-pinned.

## Exhausted protected T3 classes

Do not silently recycle these as successors:

- T3-011 through R: frozen coordinate-zero Laurent-monomial multiplier-response algebra structurally exhausted.
- T3-012-A: `NORMALIZED_RECURRENCE_OPERATOR_TANGENT_POLY_DEG_LE_9_EXHAUSTED`.
- T3-012-B: `SUPPORT_LOCKED_DEGREE0_COUPLED_CORRECTION_RECOMBINATION_INCOMPATIBLE`.
- T3-013-A: fixed source coefficient class `span_Q {1,rho,sigma}` exhausted.
- T3-015-C: the full protected 506-function reduced-residual class `SOURCE_DECLARED_RATIONAL_DELTA_COEFFICIENT_CLASS_001` is completeness-obstructed under its admitted architecture.

## T3-015-C protected completion

T3-015-C independently reconstructed the canonical 506-generator module and isolated the unique maximal-degree witness coordinate `M = H_k_2 * H_nk_1 * H_nkl_1`. Only generator 59 contributes. Any certificate in the admitted class would require

`q_59(n,k+1,l) - q_59(n,k,l) = 1/(k+l+1)`.

Over `Q(n,l)(k)`, rational forward differences have zero discrete residue on each integer-shift pole orbit, while the right side has simple-orbit residue 1. Hence no rational `q_59` exists.

Protected identities:

- proposal head: `c3f3c2fd2dc71b96133934a05eb578fd6c191173`;
- protected merge/readback: `a05c16d2988a9a0c73f9c62b482c96777a49c5ea`;
- terminal: `GLOBAL_RATIONAL_DELTA_CLASS_OBSTRUCTED__COMPLETENESS_BACKED`.

This refutes only the protected reduced-residual architecture. T3 remains open.

## Current T3 frontier

The current successor is #964, `OZ-RT-BZ-T3-016-A — order-7 discrete-curl / Popov certificate compression`.

The pinned source supplies the order-7 left multiple `L_min = A * L_BZ`, five exact degree-58 multiplier polynomials, seven compact Theorem-R blocks, and modular candidate cofactors for the eight residual blocks. The Programme independently replayed the lifted multiplier data, including exact nonvanishing of `a_4(n)` for every integer `n >= 0`.

### Exact boundary-forced E1 homogeneous geometry

For the actual certificate ansatz with `k | N_r`, `l | N_s`, numerator bidegree `(28,28)`, there are 1624 columns. The exact potential

`h = k^2 l^2 H(k,l) / ((k+l+1) prod_{j=1..6}(n+k+j)(n+l+j))`, `bideg(H)<= (23,23)`,

has 576 parameters. Its discrete curl lies exactly inside E1, and normalized-shift flatness annihilates it.

At `n=5`, `p=4194301`, independent nonzero-minor witnesses give curl rank 576 and boundary-forced E1 rank 1048. Therefore over `Q(n)`:

- `rank(E1)=1048`;
- `dim ker(E1)=576`;
- `ker(E1)=image(discrete curl)`.

### Reconciliation of the source `1106/518` prose

Do not treat `1106/518` as a contradictory second geometry. The pinned raw source resolves it:

- `o_scan.run()` uses `force_k=0, force_l=0`; at order 7/slack 18 it has **1682 columns**, and `o_scan_E1.log` reports rank **1106**, so nullity is **576**.
- `o_final.build()` uses `force=(1,1)`; the boundary-forced certificate has **1624 columns**. Programme replay gives rank **1048**, so nullity is again **576**.

The prose summary mixed the unforced rank 1106 with the forced column count 1624, producing the spurious arithmetic figure 518. Both coherent regimes agree on the 576-dimensional curl freedom.

### Modular route evidence

Pinned `o_final.log` reports four sampled `(n,p)` fibers where:

- all seven standalone E1 blocks solve;
- the constant block solves in the measured `Z3` ansatz;
- 350 fresh points × 15 blocks all satisfy the identities;
- bottom-boundary obligations hold.

This is useful construction evidence only. The remaining obligation is characteristic-zero lifting and compression.

### Current affine construction

The branch contains a source-locked canonical potential-gauge probe. It fixes the 576 `r`-numerator coordinates `k^a l^b`, `2<=a<=25`, `0<=b<=23`, solves the seven standalone residual blocks, and checks fresh unused points. The chosen coordinate minor is structurally block-lower-triangular; at `n=5`, `p=4194301`, its 24-by-24 diagonal block has determinant `2300711 mod 4194301`, so the 576-coordinate gauge is invertible at the governed witness.

The affine sample remains diagnostic until the exact-head governed replay succeeds and its output is recorded.

Current intermediate terminal:

`ORDER7_E1_KERNEL_IDENTIFIED_AS_DISCRETE_CURL__POTENTIAL_SECTION_REDUCTION_REQUIRED`.

Next: obtain canonical fixed-`n` samples; reconstruct their rational dependence on `n`; compute a degree-minimizing potential section; propagate the compatible gauge into the constant block; independently replay all fifteen blocks in characteristic zero.

## Claim firewall

Until a separately governed successor changes protected state:

- `t3_proved = false`;
- `t3_refuted = false`;
- `global_certificate_constructed = false`;
- `residual_sum_zero_proved = false` for the promoted T3 target;
- `proof_effect = NONE`;
- `promotion_effect = NONE`.

T1-top, DEPTH, Sharp-12, primes `2,3`, formal replay, MATHCERT, irrationality, infinitude, novelty, publication, patentability, deployment, product, and commercial gates remain unchanged.

## Authoritative pointers for continuation

Read from protected state before mutation:

- `governance/governed_campaign_registry.json`;
- `governance/mathsolve_routing_audit.json`;
- `campaigns/odd_zeta/OZ_SOURCE_REVISION_DELTA_003/OZ_SOURCE_REVISION_DELTA_003.json`;
- `campaigns/odd_zeta/OZ_RT_BZ_T3_015_C/`;
- `campaigns/odd_zeta/OZ_RT_BZ_T3_016_A/`;
- issue #964;
- `grandchallenge/MATHCERT:governance/certification_routes.json`, route `MC-ROUTE-OZ-001`.

## Stop conditions

Stop only on a genuine authority, governance, authentication, safety, material source/target drift, exact verification failure that cannot be repaired within scope, a completeness-backed mathematical obstruction, or separately established material closure. Routine solver engineering, modular acceleration, polynomial-matrix/order-basis implementation, CI recovery, exact reconstruction, and documentary repair are not Human-Steward stop conditions.
