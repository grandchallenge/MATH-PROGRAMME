# OZ-RT-BZ-T3-016-A — order-7 discrete-curl / Popov compression

Issue: #964  
Protected predecessor: `a05c16d2988a9a0c73f9c62b482c96777a49c5ea`  
Predecessor terminal: `GLOBAL_RATIONAL_DELTA_CLASS_OBSTRUCTED__COMPLETENESS_BACKED`

## Scope

This operation does not reopen the T3-015-C 506-function rational-Delta class. It follows the materially different source-declared order-7 left multiple `L_min = A * L_BZ` and its unresolved characteristic-zero certificate compression problem.

The governed preflight checks the source locks, exact lifted `A`, factorization and nonvanishing witness for `a_4`, 15-block order-7 module declaration, exact flatness of the normalized shift connection, and the homogeneous geometry of the E1 residual cofactor operator.

## Source lock

Pinned upstream revision: `rain-1/-odd-zeta-values-moremath@6cc0bf07137815ceeef0d9f340559f85352391e5`.

Exact object identities are recorded in `CONTRACT.json`. The reconciliation also locks `o_scan_E1.log`, `o_final.py`, and `o_final.log`, because those objects distinguish two E1 ansatz conventions that were conflated in the source prose summary.

## Exact lifted multiplier preflight

The producer verifies over exact integers that the two locked JSON deposits agree on all five `a_t`; all five have degree 58; `F4_shift2 = F4(n+2)` exactly with strictly positive coefficients; and

`a_4 = 4 (n+5)(n+6)^3(n+7)^2(2n+13)^2 a0(n+1)a0(n+2)a0(n+3) F4(n)`

with `a0(n)=41218 n^3+198849 n^2+320790 n+173057`.

The direct `n=0,1` values are nonzero. For `n>=2`, put `m=n-2`; coefficient positivity of `F4(m+2)` and positivity of every displayed factor give `a_4(n)>0`.

The source coefficient arrays are constant-first. The replay also checks the locked 15-monomial module, five Theorem-R transports, and

`gk(n,k,l) gl(n,k+1,l) = gl(n,k,l) gk(n,k,l+1)`.

## Exact E1 homogeneous kernel

For the boundary-forced E1 certificate ansatz,

`D = (k+1)(l+1)(k+l+1)(k+l+2) prod_{j=1..7}(n+k+j)(n+l+j)`

with numerator bidegree at most `(28,28)` and `k | N_r`, `l | N_s`, there are 1624 cofactor columns. Define

`h = k^2 l^2 H(k,l) / ((k+l+1) prod_{j=1..6}(n+k+j)(n+l+j))`,

where `bideg(H) <= (23,23)`. There are `24^2 = 576` potential parameters. The exact trivial pair is

`r = gl*h(k,l+1)-h`,  `s = -(gk*h(k+1,l)-h)`.

Exact denominator clearing gives

```
N_r = k^2 (k+1)(n+k+7) [
        (n+7-l)^2 (n+l+1)^2 (n+k+l+1) H(k,l+1)
        - l^2(l+1)(k+l+2)(n+l+7) H(k,l)]

N_s = l^2 (l+1)(n+l+7) [
        k^2(k+1)(k+l+2)(n+k+7) H(k,l)
        - (n+7-k)^2 (n+k+1)^2 (n+k+l+1) H(k+1,l)].
```

Thus every such potential lands inside the boundary-forced E1 ansatz. Flatness makes its weighted divergence identically zero.

At `n=5`, `p=4194301`, the 576-parameter curl witness has rank 576. Exact flatness gives `rank(M) <= 1048`; an independently reconstructed `1048 x 1624` E1 evaluation matrix has rank 1048. Therefore over `Q(n)`:

- `rank(M)=1048`;
- `dim ker(M)=576`;
- `ker(M)=image(curl)`.

## Reconciliation of the source `1106/518` summary

The source prose pairs rank `1106` with `1624` columns and states a 518-dimensional kernel. The pinned raw code and logs show that those values come from two different ansatz conventions.

`o_scan.run()` constructs the exploratory E1 ansatz with `force_k=0, force_l=0`. At order 7/slack 18, it has **1682 columns**; `o_scan_E1.log` records rank **1106**, hence nullity **576**.

`o_final.build()` constructs the actual certificate ansatz with `force=(1,1)`. Removing the 29 pure-`l` coefficients of `N_r` and 29 pure-`k` coefficients of `N_s` leaves **1624 columns**. Programme reconstruction gives rank **1048**, hence nullity **576**.

The source rank `1106` is therefore valid for its exploratory unforced scan. The spurious `518` arose only from pairing that rank with the boundary-forced column count. Both coherent ansatz regimes have the same 576-dimensional curl kernel. The Programme does not promote the cross-regime `518` figure.

## Canonical potential gauge

The affine probe fixes 576 boundary-forced `r`-numerator coefficients: `k^a l^b` with `2 <= a <= 25`, `0 <= b <= 23`.

Ordering potential monomials by `k` exponent makes this curl minor block lower triangular. Its 24 diagonal blocks are the same operator on polynomials `H(l)` of degree at most 23:

`T_n H = (n+7)[(n+l+1)^3(n+7-l)^2 H(l+1) - l^2(l+1)(l+2)(n+l+7)H(l)] mod l^24`.

At `n=5`, `p=4194301`, the diagonal block has rank 24 and determinant `2300711 mod 4194301`; the full 576-coordinate gauge minor is therefore invertible at the governed witness.

## Source modular route evidence

The pinned source already contains modular constructive evidence beyond the homogeneous analysis. `o_final.log` records four fibers:

- `n=5, p=4194301`;
- `n=9, p=4194301`;
- `n=5, p=4194287`;
- `n=11, p=4194287`.

At every listed fiber, all seven standalone E1 blocks solve; the constant block solves in the measured `Z3` ansatz; 350 fresh points across all 15 blocks give zero violations; and bottom-boundary obligations hold.

The source's `o_zero3.log` also records that `Z3` first closes at slack 16 in the tested progression, with zero violations on 300 fresh points. These are modular candidate facts only. They show that the sampled order-7 route is constructive; they do not replace characteristic-zero reconstruction.

## Consequence for compression

There is no unexplained 518-dimensional quotient. The homogeneous freedom in the boundary-forced E1 ansatz is the exact 576-dimensional discrete-curl potential family.

The affine degree-minimization problem is therefore to choose the 576 coefficient functions of `H` over `Q(n)` so that a particular residual cofactor section has minimal `n`-degree/height. Shifted Popov, minimal approximant, or order-basis machinery may act on this exact potential parameterization.

## Next exact obligations

1. Replay the canonical potential-gauge affine section at fixed fibers and verify fresh points.
2. Reconstruct enough `n`-samples to determine rational-function degree/denominator structure in the canonical gauge.
3. Form the affine `Q[n]` section problem directly in the potential coordinates.
4. Compute a degree-minimizing or provably degree-reduced potential section, recording shift and normalization exactly.
5. Reconstruct the seven standalone residual cofactors in characteristic zero and propagate the compatible gauge into the constant block.
6. Independently replay all fifteen order-7 block identities and pole/boundary obligations.
7. Verify finite initial conditions and the `a_4 != 0` induction input.
8. Only after an exact order-7 certificate exists may a separately governed successor bridge it to T3.

## Current terminal

`ORDER7_E1_KERNEL_IDENTIFIED_AS_DISCRETE_CURL__POTENTIAL_SECTION_REDUCTION_REQUIRED`

This terminal establishes the exact homogeneous E1 geometry. It does **not** establish a compressed affine section, the remaining eight characteristic-zero certificate blocks, or T3.

## Claim firewall

- `t3_proved = false`;
- `t3_refuted = false`;
- `global_certificate_constructed = false`;
- `proof_effect = NONE`;
- `promotion_effect = NONE`.

T1-top, DEPTH, Sharp-12, primes 2/3, formal replay, MATHCERT, irrationality, infinitude, novelty, publication, patentability, deployment, product, and commercial gates remain unchanged.
