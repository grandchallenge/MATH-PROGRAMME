# OZ-RT-BZ-T3-009 — locked sequence recurrence extraction

Operation: `T3_SEQUENCE_RECURRENCE_EXTRACTION_001`

Authority: issue #372. Execution intake is protected merge `fa283a283c4584c79af86fec632d50aa49e6d640` / tree `49f644c8ff4462015833d6477dfb6fde5b847970`.

## Locked T3 target

The target remains

`D_n = sum_{k,l=0}^n T(n,k,l) * (W1(n,k,l) + 2*w5_sym(n,k,l)) = 0`

for every integer `n >= 0`. No T1-top substitution is permitted.

Define the nontrivial component sequences `P5_n=sum T*w5_sym`, `W_n=sum T*W1`, and `D_n=W_n+2*P5_n`. Because the retained scalar `D_n` samples are already zero, recurrence fitting to `D_n` is forbidden as vacuous.

## Locked order-3 operator

`L_BZ[Y]_n = c0(n)Y_n + c1(n)Y_(n+1) + c2(n)Y_(n+2) + c3(n)Y_(n+3)`

is locked exactly in `RECURRENCE_LOCK.json` to the existing T3-001 Programme normalization. In particular

`c3(n)=2*(n+3)^5*(2*n+5)*a0(n)`

with `a0(n)=41218*n^3+198849*n^2+320790*n+173057`, so `c3(n)>0` for every integer `n>=0`.

The finite source-normalized baseline remains non-vacuous: `P5_1=87/4`, `W_1=-87/2`, and `L_BZ[P5]=L_BZ[W]=L_BZ[D]=0` for the retained residual range `n=0..3`. These values are finite evidence only.

## First bounded recurrence-divergence search

The complete protected 198-monomial symmetric raw-jet recurrence-divergence family was searched with coefficient degrees `0,1,2`. For each right-hand side `D`, `P5`, and `W`, exact modular coefficient/augmented ranks at `p=1000003` are

- degree 0: `198/199`;
- degree 1: `792/793`;
- degree 2: `1980/1981`.

This exactly exhausts only

`LOCKED_LBZ_NPLUS3_SYMMETRIC_RAW_JET_DIVERGENCE_DEG_LE_2_EXHAUSTED_FOR_D_P5_W`.

It does not refute the locked recurrence or T3. The route therefore pivots away from increasing the same generic flux envelope.

## Exact Q-row replay

The upstream certificate `work/lb5/Qrow_rhosigma.m` is pinned to Git blob

`61f12f412726887f506e1d423b7ee183a22116e5`.

`qrow_replay.wl` is an independent RISC-free replay. It downloads only that exact source object, checks the Git blob SHA and the retained leaf counts `{10553,1819}`, reconstructs the `n`, `k`, and `l` kernel shift ratios directly from the Gamma-product definition of `T`, and tests the Programme-locked identity

`L_BZ[T] = Delta_k(rho*T) + Delta_l(sigma*T)`

with `Delta_k F(n,k,l)=F(n,k+1,l)-F(n,k,l)`. The proof test is exact: form one rational function, clear denominators with `Together`, expand the numerator, and require the resulting polynomial to be identically zero. Finite sampling and a merely syntactic `Cancel[...]===0` test are explicitly not used as proof.

The exact replay output is retained in `QROW_REPLAY_RESULT.json`; the cleared numerator is zero.

## Boundary and apparent poles

The replay also checks

- `rho(n,0,l)=0` exactly;
- `sigma(n,k,0)=0` exactly;
- the only nonnegative shell poles occur at offsets `n+1,n+2,n+3` and have order at most two;
- the reciprocal-Gamma kernel factors `1/Gamma[n-k+1]^2` and `1/Gamma[n-l+1]^2` have order-two zeros at those shells, with leading coefficients `{1,1,4}` for offsets `1,2,3`.

Therefore `rho*T` and `sigma*T` have removable finite extensions on every shell, including joint shell intersections. Define the pole-free certificate fluxes

`R_k = Reg[rho*T]`, `R_l = Reg[sigma*T]`.

For any integer `K>=n+3`, the upper boundary is at coordinate `K+1>=n+4`, beyond the certificate shell poles; the kernel retains its support zero there. Together with the exact lower-boundary zeros, the finite-box Q-row telescoping boundary vanishes.

This regularize-first convention is important: weights are multiplied only after `rho*T` and `sigma*T` have been made finite. It avoids importing an `infinity*zero` or analytic-harmonic continuation convention into the protected discrete T3 target.

## Reduced weight-five residual

For any protected discrete weight `v`, let `Y_v(n)=sum T(n,k,l)*v(n,k,l)`. Exact discrete summation by parts gives

`L_BZ[Y_v](n) = sum_{k,l} E_v(n,k,l)`

with

`E_v = sum_{j=1}^3 c_j(n) T(n+j,k,l)*(v(n+j,k,l)-v(n,k,l))`

`      - R_k(n,k+1,l)*(v(n,k+1,l)-v(n,k,l))`

`      - R_l(n,k,l+1)*(v(n,k,l+1)-v(n,k,l))`.

`REDUCED_WEIGHT5_RESIDUAL.json` locks the three T3 instantiations:

- `E_P5`: `v=w5_sym`;
- `E_W`: `v=W1`;
- `E_D`: `v=W1+2*w5_sym`, with `E_D=E_W+2*E_P5`.

The direct `E_D` residual is the primary next object because it preserves any cancellation between the two components. `E_P5` and `E_W` remain diagnostic projections.

## Current mathematical boundary

The Q-row kernel certificate and its regularized finite boundary are now reverified at the development-head level. The reduced weight-five recurrence residual is constructed and locked, but **its double sum has not been proved zero**.

The next exact obligation is to canonicalize the pole-free `E_D` residual over the protected weight-five atom system, independently verify that canonicalization, and then prove or precisely characterize `sum E_D` without returning to the exhausted generic 198-dimensional flux ansatz.

`proof_effect: NONE`

`promotion_effect: NONE`

T3 remains `OPEN_WITH_CHARACTERIZED_BLOCKER`.
