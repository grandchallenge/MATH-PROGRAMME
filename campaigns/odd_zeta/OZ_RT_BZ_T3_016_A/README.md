# OZ-RT-BZ-T3-016-A — order-7 discrete-curl / Popov compression

Issue: #964  
Protected predecessor: `a05c16d2988a9a0c73f9c62b482c96777a49c5ea`  
Predecessor terminal: `GLOBAL_RATIONAL_DELTA_CLASS_OBSTRUCTED__COMPLETENESS_BACKED`

## Scope

This operation does not reopen the T3-015-C 506-function rational-Delta class. It follows the materially different source-declared order-7 left multiple `L_min = A * L_BZ` and its unresolved characteristic-zero certificate compression problem.

The governed preflight checks the source locks, exact lifted `A`, factorization and nonvanishing witness for `a_4`, 15-block order-7 module declaration, exact flatness of the normalized shift connection, and the homogeneous geometry of the E1 residual cofactor operator.

## Source lock

Pinned upstream revision: `rain-1/-odd-zeta-values-moremath@6cc0bf07137815ceeef0d9f340559f85352391e5`.

Exact object identities are recorded in `CONTRACT.json`. In addition to the original order-7 source objects, the reconciliation locks `o_scan_E1.log`, `o_final.py`, and `o_final.log`, because those objects distinguish two E1 ansatz conventions that were conflated in the prose summary.

## Exact lifted multiplier preflight

The producer verifies over exact integers that the two locked JSON deposits agree on all five `a_t`; all five have degree 58; `F4_shift2 = F4(n+2)` exactly with strictly positive coefficients; and

`a_4 = 4 (n+5)(n+6)^3(n+7)^2(2n+13)^2 a0(n+1)a0(n+2)a0(n+3) F4(n)`

with `a0(n)=41218 n^3+198849 n^2+320790 n+173057`.

The direct `n=0,1` values are nonzero. For `n>=2`, put `m=n-2`; coefficient positivity of `F4(m+2)` and positivity of every displayed factor give `a_4(n)>0`.

The source coefficient arrays are constant-first. This convention is replayed explicitly rather than relying on SymPy's default coefficient ordering.

The replay also checks the locked 15-monomial module, five Theorem-R transports, and the exact flatness identity

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

The generic dimensions are fixed by exact nonzero-minor reasoning:

- at `n=5`, `p=4194301`, the 576-parameter curl witness has rank `576`;
- exact flatness gives `image(curl) subset ker(M)`, so generic `rank(M) <= 1624-576 = 1048`;
- an independently reconstructed `1048 x 1624` E1 evaluation matrix at the same admissible specialization has rank `1048`;
- hence generic `rank(M)=1048`, `dim ker(M)=576`, and `ker(M)=image(curl)` over `Q(n)`.

The producer and verifier use different curl reconstructions. The producer evaluates rational potentials; the verifier builds the denominator-cleared curl coefficient matrix directly and checks that the independently reconstructed E1 operator annihilates it.

## Reconciliation of the source `1106/518` summary

The pinned source prose reports rank `1106` together with `1624` columns and therefore states a 518-dimensional kernel. The raw pinned code and logs show that these numbers came from two different E1 conventions.

`o_scan.run()` constructs its exploratory E1 ansatz with `force_k=0, force_l=0`. At order 7, slack 18, this is a `(28,28)` numerator box with **1682 columns**. `o_scan_E1.log` records rank **1106**. Its homogeneous dimension is therefore

`1682 - 1106 = 576`.

`o_final.build()` constructs the actual certificate ansatz with `force=(1,1)`, enforcing the bottom boundaries. That removes the 29 pure-`l` coefficients of `N_r` and 29 pure-`k` coefficients of `N_s`, leaving **1624 columns**. The Programme reconstruction gives rank **1048**, hence again

`1624 - 1048 = 576`.

Therefore the source rank `1106` is not contradicted; it belongs to the unforced 1682-column scan. The spurious `518` resulted from subtracting that unforced rank from the boundary-forced column count. Both coherent ansatz regimes have the same 576-dimensional curl kernel.

This reconciliation supersedes the earlier draft wording that called the source rank itself incompatible.

## Canonical potential gauge

The affine probe fixes 576 boundary-forced `r`-numerator coefficients: the rectangle `k^a l^b` with `2 <= a <= 25`, `0 <= b <= 23`.

This is an actual curl minor, not an arbitrary coordinate choice. Ordering the potential monomials by the `k` exponent makes the 576-by-576 map block lower triangular. The 24 diagonal blocks are identical 24-by-24 operators on `H(l)`:

`T_n H = (n+7)[(n+l+1)^3(n+7-l)^2 H(l+1) - l^2(l+1)(l+2)(n+l+7)H(l)] mod l^24`.

At the governed witness `n=5`, `p=4194301`, this diagonal block has rank 24 and determinant `2300711 mod 4194301`; therefore the full 576-coordinate gauge minor is invertible at that fiber. The exact-head affine replay still must validate the full residual solve and fresh points before any affine-section claim is admitted.

## Source modular route evidence

The pinned source already contains modular constructive evidence beyond the homogeneous analysis:

- seven standalone E1 blocks solve at sampled fibers;
- the constant block solves in the measured `Z3` ansatz at slack 16;
- `o_final.log` records four `(n,p)` fibers for which all fifteen block identities pass 350 fresh points each and all bottom-boundary checks hold.

This materially changes the engineering expectation: the sampled order-7 route is constructive. It does **not** replace characteristic-zero reconstruction. The current task is to lift and compress a compatible affine section, not to promote the modular samples as a proof.

## Consequence for compression

There is no unexplained 518-dimensional quotient. The full homogeneous freedom in the boundary-forced E1 ansatz is the exact 576-dimensional discrete-curl potential family.

The affine degree-minimization problem therefore becomes: choose the 576 coefficient functions of `H` over `Q(n)` so that a particular residual cofactor section has minimal `n`-degree/height. A shifted Popov, minimal-approximant, or order-basis computation may still be appropriate, but it should act on this exact potential parameterization.

The source's two high-degree pivot gauges remain useful diagnostics about those representatives. They do not establish a compression obstruction.

## Next exact obligations

1. Replay the canonical potential-gauge affine section at fixed fibers and verify fresh points.
2. Reconstruct enough `n`-samples to determine the rational-function degree/denominator structure in the canonical gauge.
3. Form the affine `Q[n]` section problem directly in the potential coordinates.
4. Compute a degree-minimizing or provably degree-reduced potential section, recording the shift and normalization exactly.
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
