# VGSE-ENG-WP02 — global quotient-response inversion

## Status and scope

VGSE-ENG-WP02 executes the quotient-response continuation and singular-locus search specified by protected WP01.

The starting point is protected MATH-PROGRAMME commit `8f43a8211c0236595eecee1cc5c195905bf5d27b`, which admitted WP01 after exact-head Adversary and Referee review and native merge-queue replay.

This work remains inside the WP01 structural boundary-response model. It does not identify the graph weights with physical stiffness, crease lengths, hinge constants, material parameters, or source geometry.

## Result in one sentence

The eight-coordinate quotient response is not merely locally identifiable near the protected representative. It has an explicit global inverse on the entire strictly positive canonical weight domain.

Consequently, the canonical log-response Jacobian has rank eight everywhere in that domain and has a uniform finite condition-number bound. There is no finite positive-domain rank-loss locus for this response map.

## Canonical coordinates

WP01 fixes

`B1=B2=B3=B4=B5=B6=F01|F04=F03|F06=1`

and leaves the eight positive quotient coordinates

1. `x1 = F01|F02`
2. `x2 = F07|F02`
3. `x3 = F03|F04`
4. `x4 = F03|F08`
5. `x5 = F07|F04`
6. `x6 = F05|F04`
7. `x7 = F05|F06`
8. `x8 = F07|F08`.

Direct enumeration of the admitted almost-perfect matchings gives the following exact monomials:

- `Delta_124 = x1 x3`
- `Delta_134 = x3`
- `Delta_234 = x2 x3`
- `Delta_145 = 1`
- `Delta_146 = x4`
- `Delta_345 = x5`
- `Delta_136 = x4 x6`
- `Delta_156 = x4 x7`
- `Delta_456 = x8`.

These identities are checked from matching exponent vectors by `analyze_wp02.py`. They do not depend on a numerical fit.

## Exact global inverse

The monomial identities give the quotient coordinates directly:

- `x1 = Delta_124 / Delta_134`
- `x2 = Delta_234 / Delta_134`
- `x3 = Delta_134 / Delta_145`
- `x4 = Delta_146 / Delta_145`
- `x5 = Delta_345 / Delta_145`
- `x6 = Delta_136 / Delta_146`
- `x7 = Delta_156 / Delta_146`
- `x8 = Delta_456 / Delta_145`.

WP01 uses the eighteen log-projective response coordinates

`F_I = log(Delta_I / Delta_124)`, for supported `I != 124`.

Let `theta = (log x1, ..., log x8)`. The inverse above becomes a fixed linear extraction from the eighteen response coordinates:

- `theta1 = -F_134`
- `theta2 = F_234 - F_134`
- `theta3 = F_134 - F_145`
- `theta4 = F_146 - F_145`
- `theta5 = F_345 - F_145`
- `theta6 = F_136 - F_146`
- `theta7 = F_156 - F_146`
- `theta8 = F_456 - F_145`.

Therefore there is a constant `8 x 18` matrix `A` such that

`A F(theta) = theta`

for every strictly positive canonical weight vector.

Differentiating gives

`A J(theta) = I_8`

everywhere in the positive quotient domain.

This is the decisive result. The Jacobian cannot lose column rank at any finite positive point.

## Uniform conditioning bound

The exact left inverse gives

`sigma_min(J(theta)) >= 1 / ||A||_2`.

The retained extractor has

`||A||_2 = 2.3276325739771573`,

so

`sigma_min(J(theta)) >= 0.42962107128932703`

globally.

Each Jacobian entry is a difference of two matching-edge occupancy probabilities. Every entry is therefore in `[-1, 1]`. For an `18 x 8` matrix,

`||J||_2 <= ||J||_F <= sqrt(18 * 8) = 12`.

Hence

`kappa_2(J(theta)) <= 27.93159088772589`

for every strictly positive canonical weight vector.

The bound is conservative. It is sufficient to exclude conditioning blow-up inside the positive domain.

## Wide numerical replay

The exact result is supplemented by a deterministic implementation stress test.

`analyze_wp02.py` evaluates 4,096 seeded samples in the log-coordinate box

`[-8, 8]^8`.

This permits each canonical weight to vary by a multiplicative factor as large as `exp(8)` relative to the protected baseline.

The retained replay finds:

- minimum rank: `8`;
- smallest observed `sigma_min`: `0.6291192604162438`;
- largest observed condition number: `9.228322965117584`;
- maximum `A J - I` error: `0`;
- maximum inverse reconstruction error: `3.552713678800501e-15`.

The numerical screen is not the proof. It checks the executable implementation across a broad dynamic range.

## Inverse design consequence

For any response that lies on the WP01 quotient-response image, the eight canonical log weights are recovered directly by `A F`.

A deterministic feasible perturbation of all eight log coordinates is recovered with maximum parameter error below `1.4e-16` and forward-response replay error below `4.5e-16`.

An arbitrary eighteen-dimensional target need not lie on the eight-dimensional response image. WP02 tests this explicitly by changing only `F_125` by `0.1` while leaving the extraction coordinates unchanged. The inverse recovers the original parameters, and forward replay returns a consistency residual of `0.1` at minor `125`.

This separates two inverse-design questions:

1. parameter recovery for a feasible structural response is globally identifiable in the canonical quotient;
2. arbitrary desired response vectors require a separate response-manifold feasibility test.

## Negative result from the singular-locus search

WP01 asked where the quotient Jacobian loses rank or becomes badly conditioned.

Within the strictly positive WP01 structural-response model, that candidate phenomenon is falsified. The explicit left inverse excludes finite positive-domain rank loss and gives a global finite condition bound.

Any later claim of mechanical amplification, locking, multistability, or physical singularity must therefore enter through a separately justified geometric or physical model. It cannot be inferred from a singularity of this quotient boundary-response map because this map has none in its admitted positive domain.

## Reproduction

From `research/vgse-eng-wp02`:

```bash
python -m pip install -r requirements.txt
python analyze_wp02.py --check
python test_wp02.py
```

`analyze_wp02.py` reuses the protected WP01 matching enumerator and response Jacobian. It independently checks the exact monomial certificates before accepting the global inverse.

## Claim boundary

WP02 does not establish:

- VGSE-C06 source correspondence;
- physical stiffness or mechanical advantage;
- rigid foldability;
- collision freedom;
- finite-thickness feasibility;
- manufacturability;
- durability or fatigue life;
- novelty, priority, patentability, product performance, or commercial value.

The result is a structural-response law for the admitted fixed graph and the GCL canonical positive-weight quotient.
