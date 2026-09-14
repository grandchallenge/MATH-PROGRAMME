# OZ-RT-BZ-T3-016-A — order-7 Popov/order-basis compression

Issue: #964  
Protected predecessor: `a05c16d2988a9a0c73f9c62b482c96777a49c5ea`  
Predecessor terminal: `GLOBAL_RATIONAL_DELTA_CLASS_OBSTRUCTED__COMPLETENESS_BACKED`

## Scope

This operation does not reopen the T3-015-C 506-function rational-Delta class. It begins a materially different route from the admitted source revision: the source-declared order-7 left multiple `L_min = A * L_BZ` and its unresolved characteristic-zero certificate compression problem.

The first governed substage independently checks the source locks, exact lifted `A`, factorization and nonvanishing witness for `a_4`, 15-block order-7 module declaration, and exact flatness identity underlying the source's trivial-pair gauge. It deliberately does not promote the source-reported `1106/1624` generic rank or 518-dimensional kernel until a characteristic-zero polynomial-matrix replay exists.

## Source lock

Pinned upstream revision: `rain-1/-odd-zeta-values-moremath@6cc0bf07137815ceeef0d9f340559f85352391e5`.

Exact object identities are recorded in `CONTRACT.json` and checked by both replay programs. The source reports an order-7 left multiple, five degree-58 integer multiplier polynomials, seven transported top blocks, eight unresolved residual blocks, and a 1624-column scalar operator with reported rank 1106 and kernel dimension 518. These remain source claims until replayed here.

## Exact preflight

The producer verifies over exact integers that the two locked JSON deposits agree on all five `a_t`; all five have degree 58; `F4_shift2 = F4(n+2)` exactly with strictly positive coefficients; and

`a_4 = 4 (n+5)(n+6)^3(n+7)^2(2n+13)^2 a0(n+1)a0(n+2)a0(n+3) F4(n)`

with `a0(n)=41218 n^3+198849 n^2+320790 n+173057`.

The direct `n=0,1` values are nonzero. For `n>=2`, put `m=n-2`; coefficient positivity of `F4(m+2)` and positivity of every displayed factor give `a_4(n)>0`.

The replay also checks the locked 15-monomial module, five Theorem-R transports, and the exact flatness identity

`gk(n,k,l) gl(n,k+1,l) = gl(n,k,l) gk(n,k,l+1)`.

The verifier repeats the polynomial factorization and shift proof using integer-list arithmetic rather than importing the producer's symbolic result, and checks flatness by an independent factor-multiset argument.

## Structured gauge before Popov

The source records the trivial-pair freedom

`(delta, epsilon) = (gl*h(l+1)-h, -(gk*h(k+1)-h))`.

The flatness identity makes its weighted divergence vanish identically. Therefore the 518-dimensional source-reported nullspace must not be treated as an opaque numerical accident. The next construction must identify the exact characteristic-zero image of this discrete-curl map, compare it with the full homogeneous cofactor kernel, and quotient the structured gauge before asking for a minimal-degree affine section.

A pivot gauge merely chooses a representative. The quotient identifies which freedom is mathematically inessential.

## Next exact obligations

1. Reconstruct the denominator-cleared E1 scalar cofactor matrix over `Q[n]`, preserving the 1624 columns.
2. Establish generic rank and kernel over characteristic zero; `1106/1624` and dimension 518 remain non-authoritative until then.
3. Construct the exact discrete-curl syzygy module and determine whether it generates the full homogeneous kernel, or what quotient remains.
4. On the quotient, compute a shifted Popov/minimal-approximant/order basis chosen for certificate degree/height rather than lexical pivot convenience.
5. Reconstruct the seven standalone residual cofactors and then the constant block in characteristic zero.
6. Independently replay all fifteen order-7 block identities and pole/boundary obligations.
7. Only after an exact order-7 certificate exists may a separately governed successor bridge it to T3.

External polynomial-matrix libraries may be used as pinned accelerators, but their output is never proof authority. Every positive candidate must reconstruct and replay in the GCL verifier.

## Current terminal

`ORDER7_SOURCE_PREFLIGHT_REPLAYED__POPOV_REDUCTION_REQUIRED`

This terminal means only that the order-7 source object, leading-coefficient induction input, module shape, and structured-gauge identity passed the bounded preflight. It does not establish the residual 518-dimensional geometry, a compressed certificate, or T3.

## Claim firewall

- `t3_proved = false`;
- `t3_refuted = false`;
- `global_certificate_constructed = false`;
- `proof_effect = NONE`;
- `promotion_effect = NONE`.

T1-top, DEPTH, Sharp-12, primes 2/3, formal replay, MATHCERT, irrationality, infinitude, novelty, publication, patentability, deployment, product, and commercial gates remain unchanged.
