# OZ-RT-BZ-T3-016-A — order-7 Popov/order-basis compression

Issue: #964  
Protected predecessor: `a05c16d2988a9a0c73f9c62b482c96777a49c5ea`  
Predecessor terminal: `GLOBAL_RATIONAL_DELTA_CLASS_OBSTRUCTED__COMPLETENESS_BACKED`

## Scope

This operation does not reopen the T3-015-C 506-function rational-Delta class. It follows the materially different source-declared order-7 left multiple `L_min = A * L_BZ` and its unresolved characteristic-zero certificate compression problem.

The governed preflight checks the source locks, exact lifted `A`, factorization and nonvanishing witness for `a_4`, 15-block order-7 module declaration, exact flatness of the normalized shift connection, and the homogeneous geometry of the E1 residual cofactor operator.

## Source lock

Pinned upstream revision: `rain-1/-odd-zeta-values-moremath@6cc0bf07137815ceeef0d9f340559f85352391e5`.

Exact object identities are recorded in `CONTRACT.json` and checked by both replay programs. The source reports an order-7 left multiple, five degree-58 integer multiplier polynomials, seven transported top blocks, eight unresolved residual blocks, and a 1624-column E1 scalar operator. Source statements are candidate evidence until reconstructed here.

## Exact lifted multiplier preflight

The producer verifies over exact integers that the two locked JSON deposits agree on all five `a_t`; all five have degree 58; `F4_shift2 = F4(n+2)` exactly with strictly positive coefficients; and

`a_4 = 4 (n+5)(n+6)^3(n+7)^2(2n+13)^2 a0(n+1)a0(n+2)a0(n+3) F4(n)`

with `a0(n)=41218 n^3+198849 n^2+320790 n+173057`.

The direct `n=0,1` values are nonzero. For `n>=2`, put `m=n-2`; coefficient positivity of `F4(m+2)` and positivity of every displayed factor give `a_4(n)>0`.

The source coefficient arrays are constant-first. This convention is replayed explicitly rather than relying on SymPy's default coefficient ordering.

The replay also checks the locked 15-monomial module, five Theorem-R transports, and the exact flatness identity

`gk(n,k,l) gl(n,k+1,l) = gl(n,k,l) gk(n,k,l+1)`.

The verifier repeats the factorization and shift proof using integer-list arithmetic and checks flatness by an independent factor-multiset argument.

## Exact E1 homogeneous kernel

The source reported rank `1106` in `1624` columns, hence a `518`-dimensional kernel. That report is **not** the geometry of the stated E1 operator and is downgraded by this tranche.

For the E1 denominator

`D = (k+1)(l+1)(k+l+1)(k+l+2) prod_{j=1..7}(n+k+j)(n+l+j)`

with numerator bidegree at most `(28,28)` and boundary forcing `k | N_r`, `l | N_s`, define

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

Thus every such potential lands inside the E1 ansatz and satisfies the bottom boundary factors. Flatness makes its weighted divergence identically zero.

The generic dimensions are fixed by exact nonzero-minor reasoning:

- at `n=5`, `p=4194301`, the deterministic 576-parameter curl evaluation witness has rank `576`; therefore the generic curl image has dimension 576;
- exact flatness gives `image(curl) subset ker(M)`, so generic `rank(M) <= 1624-576 = 1048`;
- an independently reconstructed `1048 x 1624` E1 evaluation matrix at the same admissible specialization has rank `1048`; therefore a `1048 x 1048` minor is nonzero and generic `rank(M) >= 1048`;
- hence generic `rank(M)=1048`, `dim ker(M)=576`, and `ker(M)=image(curl)` over `Q(n)`.

The producer and verifier use different curl reconstructions. The producer evaluates rational potentials; the verifier builds the denominator-cleared curl coefficient matrix directly and checks that the independently reconstructed E1 operator annihilates it. Deterministic matrix and point-stream SHA-256 witnesses are recorded in `CONTRACT.json`.

This is characteristic-zero information. The modular matrices are nonzero-minor witnesses used only for rank lower bounds; the kernel inclusion itself is an exact rational identity.

## Consequence for compression

There is no unexplained 518-dimensional homogeneous quotient to discover. The full E1 homogeneous freedom is the 576-dimensional discrete-curl potential family.

The affine degree-minimization problem therefore becomes: choose the 576 coefficient functions of `H` over `Q(n)` so that a particular residual cofactor section has minimal `n`-degree/height. A shifted Popov, minimal-approximant, or order-basis computation may still be appropriate, but it must act on this exact potential parameterization rather than on the source-reported 518-dimensional numerical kernel.

The two high-degree pivot gauges reported by the source remain useful negative diagnostics about those representatives. They do not establish a compression obstruction.

## Next exact obligations

1. Reconstruct a particular E1 residual cofactor section over enough exact/modular `n` samples with the corrected 576-potential parameterization attached.
2. Form the affine `Q[n]` section problem directly in the potential coordinates.
3. Compute a degree-minimizing or provably degree-reduced potential section, recording the shift and normalization exactly.
4. Reconstruct the seven standalone residual cofactors in characteristic zero and propagate the compatible gauge into the constant block.
5. Independently replay all fifteen order-7 block identities and pole/boundary obligations.
6. Verify finite initial conditions and the `a_4 != 0` induction input.
7. Only after an exact order-7 certificate exists may a separately governed successor bridge it to T3.

External polynomial-matrix libraries may be used as pinned accelerators, but their output is never proof authority. Every positive candidate must reconstruct and replay in the GCL verifier.

## Current terminal

`ORDER7_E1_KERNEL_IDENTIFIED_AS_DISCRETE_CURL__POTENTIAL_SECTION_REDUCTION_REQUIRED`

This terminal establishes the exact homogeneous E1 geometry and supersedes the source-reported `1106/518` rank/nullity for this normalization. It does **not** establish a compressed affine section, the remaining eight characteristic-zero certificate blocks, or T3.

## Claim firewall

- `t3_proved = false`;
- `t3_refuted = false`;
- `global_certificate_constructed = false`;
- `proof_effect = NONE`;
- `promotion_effect = NONE`.

T1-top, DEPTH, Sharp-12, primes 2/3, formal replay, MATHCERT, irrationality, infinitude, novelty, publication, patentability, deployment, product, and commercial gates remain unchanged.
