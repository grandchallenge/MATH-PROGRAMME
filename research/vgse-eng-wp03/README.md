# VGSE-ENG-WP03 — exact response-manifold feasibility

## Scope

WP03 executes the protected WP02 successor: characterize exactly which eighteen-dimensional log-projective boundary responses are feasible for the admitted fixed positive-weight quotient.

Protected predecessor:

- WP02 native merge-queue commit: `52e2e3df6ac54ab63a03c867b2b82a80d93ee577`
- reviewed WP02 head: `229d5549689fde9d5397ed59f92890e8ba080c75`

The model boundary is unchanged. The eight canonical positive quotient variables are structural graph weights only. They are not crease lengths, stiffnesses, hinge constants, material parameters, or recovered source geometry.

## Result

WP02 proved that eight response coordinates recover the eight canonical quotient variables globally. WP03 uses that inverse to show that the full positive response image is a global graph over those eight coordinates.

Let

`y_I = Delta_I / Delta_124 > 0`

for the eighteen supported projective coordinates `I != 124`.

Use extractor coordinates

`134, 234, 145, 146, 345, 136, 156, 456`.

The remaining ten coordinates are exactly constrained by:

```text
y134*y146*y125 = y134*y156 + y136*y145
y134*y126      = y136
y146*y135      = y134*y156 + y136*y145
y134*y146*y235 = y234*(y134*y156 + y136*y145)
y134*y236      = y136*y234
y134*y245      = y145*y234 + y345
y134*y145*y246 = y134*y456 + y145*y146*y234 + y146*y345
y134*y145*y146*y256 =
    y134*y156*y456 + y136*y145*y456
  + y145*y146*y156*y234 + y146*y156*y345
y145*y346      = y134*y456 + y146*y345
y145*y146*y356 =
    y134*y156*y456 + y136*y145*y456 + y146*y156*y345
```

`analyze_wp03.py` re-enumerates the admitted graph's almost-perfect matchings from the protected WP01 model, reconstructs all nineteen matching polynomials symbolically, substitutes the WP02 global inverse, and proves each retained relation simplifies identically to zero.

## Completeness and minimality

The WP02 inverse recovers

```text
x1 = 1/y134
x2 = y234/y134
x3 = y134/y145
x4 = y146/y145
x5 = y345/y145
x6 = y136/y146
x7 = y156/y146
x8 = y456/y145
```

from any positive extractor tuple.

Substitution into the admitted matching polynomials produces one and only one value for each of the ten dependent coordinates. Therefore the ten equations are necessary and sufficient on this positive chart.

Their Jacobian with respect to the ten dependent coordinates is diagonal. Its diagonal entries are

```text
y134*y146, y134, y146, y134*y146, y134, y134,
y134*y145, y134*y145*y146, y145, y145*y146.
```

All are strictly positive in the admitted domain, so the residual Jacobian has rank ten everywhere.

The feasible response image has dimension eight inside an eighteen-dimensional chart. Its codimension is ten. A regular equality description therefore needs at least ten independent constraints. The retained ten-relation basis reaches that lower bound.

At the protected baseline, the residual-Jacobian determinant is exactly

`23447265625/512`.

## Deterministic target checker

The executable checker works in WP01/WP02 log-response coordinates

`F_I = log(y_I)`.

It:

1. recovers the eight quotient log coordinates with the WP02 extractor;
2. replays all eighteen responses from the admitted matching polynomials;
3. reports the coordinate-wise log-response residual;
4. classifies the target as `feasible`, `numerically_ambiguous`, or `inconsistent`.

Thresholds are declared in code and retained results:

- feasible: maximum absolute log residual `<= 1e-10`;
- inconsistent: maximum absolute log residual `>= 1e-7`;
- intermediate values: numerically ambiguous.

A synthetic feasible eight-parameter perturbation is recovered to floating precision. Ten adversarial probes, each perturbing one dependent response by `0.1` while leaving all extractor coordinates fixed, are all rejected as inconsistent. A `5e-9` probe exercises the declared ambiguity band.

## Canonical feasibility retraction

WP03 also retains

`P(F) = F(recover_theta(F))`.

This leaves all eight extractor coordinates fixed and replaces the ten dependent coordinates with their feasible replay. It is idempotent to floating precision and maps every target into the admitted response image.

This is a feasibility retraction, not a nearest-point theorem. WP03 does not establish that `P` minimizes Euclidean distance, a weighted engineering norm, or any application-specific loss over all feasible responses.

## Engineering consequence

For the admitted fixed graph, target synthesis now separates cleanly into two stages:

1. feasibility: test the ten exact response relations;
2. realization: if feasible, recover the unique eight canonical quotient variables by the WP02 inverse.

Thus arbitrary eighteen-coordinate requests can be rejected before attempting structural parameter recovery.

## Reproduction

From `research/vgse-eng-wp03`:

```bash
python -m pip install -r requirements.txt
python analyze_wp03.py --check
python test_wp03.py
```

## Claim boundary

WP03 does not establish VGSE-C06 source correspondence, geometry-to-weight coupling, physical stiffness, mechanical advantage, rigid foldability, collision freedom, finite thickness, manufacturability, durability, product performance, novelty, priority, patentability, or commercial value.
