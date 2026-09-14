# OZ-RT-BZ-T3-016-A Section C — global canonical gauge domain

Protected predecessor: `cb2cb529211eae9beb9a7fbae96930b6d0d5fbad` (PR #965).

This packet closes one bounded Section C question: whether the admitted canonical 576-coordinate potential gauge is merely a good sampled fiber or is available uniformly on the integer fibers used for affine lifting.

It does not construct the affine characteristic-zero section and does not change the admitted intermediate terminal.

## Canonical diagonal block

Order the 576 potential monomials by the `k` exponent. The admitted curl minor is block lower triangular with 24 identical diagonal blocks. On `H(l)` of degree at most 23, the block is

`T_n H = (n+7)[(n+l+1)^3(n+7-l)^2 H(l+1) - l^2(l+1)(l+2)(n+l+7)H(l)] mod l^24`.

In the basis `1,l,...,l^23`, every entry has degree at most 6 in `n`. Therefore `det(T_n)` has degree at most 144.

## Exact determinant reconstruction

`gauge_domain.py` evaluates the exact integer determinant at `n=0,...,144`, reconstructs the unique polynomial of degree at most 144 by exact finite-difference interpolation, and verifies it at the unused exact point `n=145`.

The reconstructed determinant has degree exactly 144 and factors as

`det(T_n) = n (n+8) (n+1)^7 (n+2)^2 (n+3)^2 (n+4)^2 (n+5)^2 (n+6)^2 (n+7)^31 R_94(n)`,

where `R_94` is monic of degree 94.

Exact coefficient translation gives that every coefficient of `R_94(n+9)` is strictly positive. Hence `R_94(n)>0` for every integer `n>=9`.

For the only remaining positive integer fibers, direct exact evaluation gives `R_94(n) != 0` for `n=1,...,8`. Thus

- `det(T_n) != 0` for every integer `n>=1`;
- `n=0` is the only nonnegative integer singular fiber;
- because the full 576-coordinate gauge minor is block lower triangular with 24 copies of `T_n` on the diagonal, the full canonical gauge is nonsingular for every integer `n>=1`.

The previously admitted modular witness is replayed exactly:

`det(T_5) mod 4194301 = 2300711`.

## Independent replay

`gauge_domain_verifier.py` does not import producer polynomial objects. It independently:

1. reconstructs the block entries from binomial coefficient formulas for `(n+7-l)^2(n+l+1)^3` and `(l+1)(l+2)(n+l+7)`;
2. recomputes all 145 determinant samples over `Z`;
3. reconstructs the determinant via a separate falling-factorial finite-difference conversion;
4. checks the unused exact point `n=145`;
5. removes each declared linear factor by sequential exact synthetic division;
6. verifies the monic residual degree 94;
7. independently verifies strict coefficient positivity after the shift `n -> n+9`;
8. verifies nonvanishing at `n=1,...,8` and the governed modular witness.

Finite sampling is not used as an unbounded proof. The finite determinant evaluations reconstruct an exact polynomial under the proved degree bound; exact factor division and coefficient positivity then prove the integer-domain result.

## Consequence for Section C

Fixed-fiber affine sampling may use every integer `n>=1` without a per-fiber gauge-validity hypothesis. Fiber `n=0` must be handled separately or excluded from the interpolation set.

This removes gauge singularity as a possible explanation for irregular affine samples. The remaining task is the actual rational dependence of the seven-block affine section on `n`, followed by degree-minimizing use of the admitted 576-dimensional potential freedom.

Current terminal remains

`ORDER7_E1_KERNEL_IDENTIFIED_AS_DISCRETE_CURL__POTENTIAL_SECTION_REDUCTION_REQUIRED`.

Claim firewall remains unchanged:

- `t3_proved = false`;
- `t3_refuted = false`;
- `global_certificate_constructed = false`;
- `proof_effect = NONE`;
- `promotion_effect = NONE`.
