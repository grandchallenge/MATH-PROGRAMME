# OZ-RT-BZ-T3-003 — parameter-lifted higher-order creative telescoping

This package is the first executable operation after `OZ-RT-BZ-T3-002`. It does **not** prove or refute T3. It changes the representation and records the first exact higher-order search frontier in that new representation.

## Locked target

The target remains the protected T3 zero form

`sum_{k=0}^n sum_{l=0}^n T(n,k,l) * (W1(k,l) + 2*w5_sym(n,k,l)) = 0`.

No T1-top representative substitution is permitted.

## Parameter lift

For integers `length, offset >= 0`, define

`Q(length,offset;alpha) = prod_{i=1}^length (offset+i+alpha)/(offset+i)`.

Its logarithmic derivatives satisfy

`d^r log Q / d alpha^r |_(alpha=0) = (-1)^(r-1) (r-1)! (H_(offset+length)^(r) - H_offset^(r))`.

This generates `H`, `A`, and `C`; `B` is a difference of two such cumulants.

The nested `ES` and `U` letters remain liftable after introducing an auxiliary finite summation index `t`: each nested summand is `t^(-r)` times a cumulant recovered from a normalized Pochhammer lift at `t` or `t+b`. The retained exact-rational fixture therefore reconstructs the full locked `W1`, `w5sym`, and T3 cell, not merely the one-body harmonic sector.

This is the principal structural result of the first T3-003 fixture: depth-two letters require an auxiliary hypergeometric summation dimension; they do not force abandonment of the parameter-lift programme.

The fixture checks every `1 <= n <= 6`, `0 <= k,l <= n`, with harmonic orders through five.

## Correct creative-telescoping orientation

For an `l`-fibre sum, a nontrivial creative telescoper shifts an external parameter. The retained search therefore uses

`sum_{j=0}^r a_j(n,k) F(n,k+j,l) = Delta_l(F(n,k,l) q(n,k,l))`

for `r in {2,3,4}`.

An `l`-shift on the left is not used because it can reduce to a tautological finite difference.

At zero lift parameters the undeformed parent is the exact binomial kernel `T(n,k,l)`. Its exact ratios are

`F(n,k+1,l)/F(n,k,l) = (n+k+1)(n-k)^2(n+k+l+1) / ((k+1)^3(k+l+1))`

and

`F(n,k,l+1)/F(n,k,l) = (n+l+1)(n-l)^2(n+k+l+1) / ((l+1)^3(k+l+1))`.

The certificate denominator is analytically locked to the denominator factors of the `l`-shift ratio:

`D = (l+1)^3(k+l+1)`.

## Exact bounded higher-order search

For each order `r=2,3,4`, the total degree of each `a_j(n,k)` runs from 0 through 6 and the numerator degree of `q(n,k,l)` runs from 2 through 8. The retained ledger contains 21 exact systems.

All systems are constructed over `Q`. Reduction modulo `p=1000003` is used only as an exact negative rank certificate. Full column rank modulo `p` exhibits a nonzero maximal minor modulo `p`; the corresponding rational minor is nonzero, so the rational matrix has full column rank.

The strongest stages are:

- order 2: 720 equations, 249 unknowns, rank 249, nullity 0;
- order 3: 795 equations, 277 unknowns, rank 277, nullity 0;
- order 4: 870 equations, 305 unknowns, rank 305, nullity 0.

Therefore

`UNDEFORMED_PARENT_ORDERS_2_TO_4_K_SHIFT_DSHIFT_DENOM_ADEG_LE_6_QDEG_LE_8`

is exactly inconsistent. This is not evidence that T3 is false.

## Independent verifier

`verify.py` does not import the producer or the parameter-lift implementation. It independently expands normalized Pochhammer products as exact polynomials, converts ordinary derivatives to logarithmic cumulants, reconstructs the locked harmonic letters and nested auxiliary sums, reconstructs all 21 higher-order matrices in a different monomial order, and performs an independent modular elimination.

## Next route

The next mathematically distinct search is parameter-dependent order 2 with the auxiliary `t` dimension retained inside the telescoping system. This allows differentiation of a genuine parameterized telescoping relation to generate the harmonic-weighted target.

If that class remains inconsistent:

1. advance the parameter-dependent search to orders 3 and 4;
2. test the structured symmetric two-dimensional divergence route;
3. derive an exact recurrence for the T3 sequence and discharge initial/propagation obligations;
4. reserve integral or coefficient-extraction representations for the next representation change.

Terminal candidate disposition: `OPEN_WITH_CHARACTERIZED_BLOCKER`.

`proof_effect: NONE`; `promotion_effect: NONE`.
