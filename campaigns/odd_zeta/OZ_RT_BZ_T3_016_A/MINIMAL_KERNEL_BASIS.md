# OZ-RT-BZ-T3-016-A — exact minimal polynomial kernel basis

Protected predecessor: `d6fd459b30d4d60f008b2e55e325bbfcec3a9335` (PR #967 protected readback).

This packet refines the admitted 576-parameter discrete-curl description of the boundary-forced E1 homogeneous kernel. It does not construct the affine section and does not change T3 state.

## Result

Let `C(n)` denote the denominator-cleared discrete-curl map from potentials

`H(k,l)`, `bideg(H) <= (23,23)`,

to the 1624 boundary-forced E1 numerator coefficients `(N_r,N_s)`.

The monomial curl columns `C(n)(k^a l^b)`, `0 <= a,b <= 23`, form a basis over `Q(n)`, but not a minimal polynomial basis over `Q[n]`. Each raw column has `n`-degree 6. The raw basis loses one rank exactly at

`n = 0,-1,-2,-3,-4,-5,-6,-7`

and nowhere else in characteristic zero.

For `j=0,...,7`, let `H_j` be the unique monic polynomial potential spanning the fixed-fiber kernel at `n=-j`. Then `bideg(H_j)=(21,21)` and

`C(n) H_j` is divisible coefficientwise by `n+j` in `Z[n,k,l]`.

Define

`Q_j = C(n) H_j / (n+j)`.

Replace the eight raw monomial columns indexed by

`k^21 l^20, k^21 l^19, ..., k^21 l^13`

with `Q_0,...,Q_7`, respectively. The resulting 1624 x 576 polynomial matrix `B(n)` is a minimal polynomial basis for the same rational kernel module.

Its column-degree profile is

- 568 columns of degree 6;
- 8 columns of degree 5;
- total column degree `568*6 + 8*5 = 3448`.

The raw total was `576*6 = 3456`. The exact drop is 8, matching the eight simple finite saturation factors.

## Fixed-fiber classification

After removing nonzero polynomial prefactors from the two curl numerators, a nonzero fixed-fiber kernel potential at `n=alpha` must satisfy

`H(k,l+1)/H(k,l) = A_alpha(l) B_alpha(k+l)`

and its `k`-shift mirror, where

`A_alpha(x) = x^2 (x+1) (alpha+x+7) / ((alpha+7-x)^2 (alpha+x+1)^2)`

and

`B_alpha(t) = (t+2)/(alpha+t+1)`.

Factor orbits under the unit shift separate into vertical, horizontal, and diagonal linear-factor orbits. A rational function periodic under a unit shift is constant, so every polynomial solution has the separated factor form

`H(k,l) = c U(k) U(l) V(k+l)`.

For the vertical factor `U`, if `m(a)` is the root multiplicity at `x=a`, then

`m(a+1)-m(a) = ord_a A_alpha`.

A finite-support polynomial divisor requires zero total order on every shift orbit and nonnegative multiplicities.

If `alpha` is not an integer, the fixed integer orbit containing `0` and `-1` has total order `+3`; none of the `alpha`-dependent factors joins that orbit. Hence no finite divisor exists.

If `alpha >= 1` is an integer, the cumulative multiplicity becomes negative at `a=-alpha-1`: the zero at `-alpha-7` contributes `+1`, then the double pole at `-alpha-1` forces `-1`. Hence no polynomial `U` exists.

If `alpha <= -8`, write `alpha=-j`, `j>=8`. The first relevant event is the double pole at `a=7-j`; for `j=8` it coincides with the simple fixed zero at `-1` and still leaves multiplicity `-1`. Hence no polynomial `U` exists.

Therefore a polynomial fixed-fiber kernel can exist only for `alpha=-j`, `0<=j<=7`.

For those eight fibers the recurrence has a unique nonnegative finite solution. Its degree is

`deg U_j = 20-j`.

The diagonal recurrence is

`V_j(t+1)/V_j(t) = (t+2)/(t-j+1)`,

so one may take

`V_j(t) = prod_{s=-j+1}^{1} (t+s)`,

with `deg V_j=j+1`. Thus

`H_j(k,l)=U_j(k) U_j(l) V_j(k+l)`

has bidegree `(21,21)` for every `j`. The shift recurrences determine it uniquely up to scalar; the implementation uses the monic normalization.

This proves that the raw curl matrix has characteristic-zero fixed-fiber kernel dimension 1 at exactly the eight listed fibers and dimension 0 everywhere else.

## Exact saturation

For every `j`, substituting `H_j` into the exact denominator-cleared curl formulas gives a polynomial pair whose every coefficient vanishes at `n=-j`. Because `n+j` is monic, coefficientwise synthetic division is exact in `Z[n]`. The quotient `Q_j` has `n`-degree 5 in both numerator components.

Let the eight selected potential coordinates be

`p_i = k^21 l^(20-i)`, `i=0,...,7`.

The coefficient matrix `[coeff_{p_i}(H_j)]` is

```
[       1       0      0     0    0   0   0  0 ]
[     -35       1      0     0    0   0   0  0 ]
[     427     -27      1     0    0   0   0  0 ]
[   -1029     246    -22     1    0   0   0  0 ]
[  -23646    -300    171   -20    1   0   0  0 ]
[  217854   -9498   -330   158  -21   1   0  0 ]
[ -248426   59046  -2898  -554  190 -25   1  0 ]
[-5687738  -20288  18756   152 -948 277 -32  1 ]
```

It is unit lower triangular. Therefore the generic change of basis from the raw monomial curls to the saturated columns has determinant

`1 / (n(n+1)(n+2)(n+3)(n+4)(n+5)(n+6)(n+7))`.

Away from the eight exceptional fibers this change is invertible, so `B(n)` has rank 576 because the raw curl map does.

At each exceptional fiber, the independent verifier reconstructs the replacement column without using producer-owned polynomial division:

- for `Q_j` at `n=-m`, `j != m`, it evaluates `C_{-m}(H_j)/(j-m)`;
- for `Q_m` at `n=-m`, it evaluates `d/dn(C_n(H_m))` at `n=-m`.

At `p=4194301`, each resulting exact-integer specialization has rank 576. A nonzero modular 576-minor is a characteristic-zero nonzero-minor witness, so `B(alpha)` has full rank at all eight exceptional characteristic-zero fibers.

Thus `B(n)` is finite-irreducible: it has full column rank for every finite `n` over an algebraic closure of `Q`.

## Column reduction and minimality

The 568 unchanged columns have degree 6. Each saturated replacement has degree 5. The matrix formed from the coefficient of each column at its own highest degree has rank 576; the governed prime witness is independently reconstructed.

Hence `B(n)` is column-reduced. A polynomial basis of a rational subspace is a minimal polynomial basis exactly when it is finite-irreducible and column-reduced. Therefore `B(n)` is a minimal polynomial basis of the 576-dimensional E1 homogeneous kernel over `Q[n]`.

This removes the need for a black-box 576-dimensional Popov computation for the homogeneous kernel itself. The remaining degree-minimization problem is affine: reduce a particular seven-block section modulo this exact minimal kernel basis, then propagate the compatible gauge into the constant block.

## Evidence boundaries

The modular calculations in this packet are used only as nonzero-minor witnesses for exact integer matrices. They do not establish polynomial identities. Polynomial identities, divisor classification, exact divisibility, degree statements, and the generic change-of-basis determinant are all reconstructed exactly over characteristic zero.

The overall campaign terminal remains

`ORDER7_E1_KERNEL_IDENTIFIED_AS_DISCRETE_CURL__POTENTIAL_SECTION_REDUCTION_REQUIRED`.

Claim firewall remains:

- `t3_proved = false`;
- `t3_refuted = false`;
- `global_certificate_constructed = false`;
- `proof_effect = NONE`;
- `promotion_effect = NONE`.
