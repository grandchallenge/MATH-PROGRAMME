# VGSE-MS-M0 — TE3 realization atlas

**Governed work:** `VGSE-TE3-REALIZATION-ATLAS-001`  
**Parent phase:** `VGSE-MECHANICAL-SEMANTICS-001`  
**Tracker:** `grandchallenge/MATH-PROGRAMME#1085`  
**Admission base:** `f32a1e0cf2b90cb0fda8552effe8de4e713712d2`  
**State at campaign admission:** `AUTHORIZED_READY`

## Objective

Construct genuinely independent GCL-designed TE3-conformant realizations over nontrivial regions of the protected eight-dimensional positive quotient space.

This directory is the M0 substantive work surface. At admission it contains only the work contract. It contains no positive realization result.

## Protected inputs

Use, but do not reopen:

- WP02 global quotient inverse: protected merge `52e2e3df6ac54ab63a03c867b2b82a80d93ee577`;
- WP03 exact response-manifold result: protected merge `4a13e2deb6dfc56bc5dcbd121d076919217f68dc`;
- WP04 geometry-to-quotient non-identifiability: protected merge `05e384156859269221e77fdcd61606e06f56ddd1`;
- WP05 cycle/path invariant decomposition: protected result retained under `research/vgse-eng-wp05/`;
- WP06 terminal boundary-calibration result: protected merge `9663a9bc8f71af808ea4578a02467cfd47c29d92`;
- independent MATHCERT TE3 audit: `15b68c196d020045bea42fc34236e0647b87cbb9`.

## First execution sequence

1. Reconstruct the exact mathematical model contract needed for a forward TE3 realization solve.
2. Separate variables that are fixed by the quotient point from variables introduced by boundary convention, Euclidean frame, scale, orientation, and branch choice.
3. Choose an initial independently generated quotient sample around and away from the protected baseline.
4. Solve for candidate realizations.
5. Independently replay TE3 and declared geometric admissibility on every candidate.
6. Record multiplicity, nonexistence, degeneracy, singularity, and numerical failure separately.
7. Compute a first local continuation/Jacobian diagnostic only after the model contract is explicit.
8. Attempt to falsify local uniqueness or universal positive-quadrant realizability.
9. Retain a machine-readable atlas and exact claim boundary.

## GCL-ID-00 applicability

M0 is primarily a forward construction problem `x -> g`, so GCL-ID-00 does not require a preflight merely because the work uses a solver.

If M0 changes into a claim that geometry or latent realization data can be uniquely recovered from observations, that new inverse/reconstruction claim enters the adopted GCL-ID-00 trigger and must create the appropriate preflight record before substantial inverse-solver effort.

M2 is explicitly planned as an in-scope GCL-ID-00 inverse-design tranche.

## Stop rule

Do not continue searching indefinitely for a globally positive result.

Stop at one declared M0 terminal disposition. Preserve a negative, partial, branch-restricted, or component-restricted atlas if that is what the evidence supports.

## Claim boundary

No source correspondence or `VGSE-C06`. No mechanics, rigid foldability, collision, finite thickness, stiffness, material, manufacture, product, patent, or commercial claim.


## Current M0 result

The first deterministic atlas tranche is complete enough for protected review.

- Exact finite graph audit: 31 almost-perfect matchings, `kmin = 2`, and all six adjacent boundary pairs satisfy the two-boundary-nondegeneracy witness condition.
- Protected baseline: a new GCL-designed numerical t-embedding satisfies TE1-TE5 and the noncrossing/injectivity replay. The maximum TE3 relative gauge error is below `1e-12` across the retained successful atlas.
- Independent quotient coverage: 41 quotient points were attempted. The representative selector found 40 valid numerical t-embeddings. Every baseline, axis, log-radius-`0.5`, and log-radius-`1.5` sample succeeded. One of eight log-radius-`3` stress samples hit `SELECTOR_COVERAGE_LIMIT`.
- The selector limit is not a nonexistence result. Galashin Corollary 1.13 supplies a separate source-conditional existence statement once the exact graph hypotheses and the pinned source theorem are accepted.
- Uniqueness is falsified numerically: five admissible representatives at the same protected quotient point have distinct perimeter-normalized boundary-edge signatures.
- The local Jacobian of one fixed representative branch from eight log-quotient coordinates to six perimeter-normalized boundary-edge lengths has numerical rank `5` at tolerance `1e-8`. This is geometric branch sensitivity, not a mechanical response.

The retained disposition is:

`TE3_REALIZATION_ATLAS_PARTIAL`

“Partial” refers to constructor/branch coverage, not failure of the source existence theorem. M0 does not claim a complete classification of all t-embedding branches or a globally complete numerical selector.

## Replay

```bash
python -m pip install -r research/vgse-ms-m0/requirements.txt
python research/vgse-ms-m0/analyze_m0.py --check
python research/vgse-ms-m0/test_m0.py
```

A path-scoped GitHub Actions workflow runs the same replay when the M0 evidence surface changes.

## Successor boundary

The retained atlas is a genuine TE3-native design family and is sufficient evidence to ask whether a separately defined kinematic model attaches stable meaning to any of its coordinates.

That question belongs to M1. M0 does not authorize M1 automatically.
