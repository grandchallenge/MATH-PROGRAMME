# OZ-RT-BZ-T3-009 — locked sequence recurrence extraction

Operation: `T3_SEQUENCE_RECURRENCE_EXTRACTION_001`

Authority: issue #372. Execution intake is protected merge `fa283a283c4584c79af86fec632d50aa49e6d640` / tree `49f644c8ff4462015833d6477dfb6fde5b847970`.

## Target and non-vacuity

The target remains

`D_n = sum_{k,l=0}^n T(n,k,l) * (W1(n,k,l) + 2*w5_sym(n,k,l)) = 0`

for every integer `n >= 0`. No T1-top substitution is permitted.

Define the nontrivial component sequences `P5_n=sum T*w5_sym`, `W_n=sum T*W1`, and `D_n=W_n+2*P5_n`. Because the retained scalar `D_n` samples are already zero, recurrence fitting to `D_n` is forbidden as vacuous. The pre-locked operator must be proved at summand/module level or through sufficient nonzero component recurrences.

## Locked Brown-Zudilin operator

`L_BZ[Y]_n = c0(n)Y_n + c1(n)Y_(n+1) + c2(n)Y_(n+2) + c3(n)Y_(n+3)`

with the exact polynomials in `RECURRENCE_LOCK.json`, source-pinned to `rain-1/-odd-zeta-values-moremath@968477ed7e406df6542f8da6fbe1cd6ca7273c47:work/lb5/core.py` and rebound to the Programme T3-001 lock.

`c3(n)=2*(n+3)^5*(2*n+5)*a0(n)` with `a0(n)=41218*n^3+198849*n^2+320790*n+173057`, so `c3(n)>0` for every integer `n>=0` by coefficient positivity. A uniform proof of `L_BZ[D]=0` plus `D_0=D_1=D_2=0` would therefore propagate T3 to all `n`.

## Exact finite baseline

`BASELINE_RESULT.json` is generated from the protected T3-002 target evaluator. It records exact `P5`, `W`, and `D` values for `n=0..6`, including the nonzero witnesses `P5_1=87/4` and `W_1=-87/2`, and exact finite residuals `L_BZ[P5]=L_BZ[W]=L_BZ[D]=0` for `n=0..3`.

These are finite evidence only and confer no recurrence theorem.

## Moving support

The moving-support obstruction is resolved exactly. All four shifted summands extend by zero to the common square `0<=k,l<=n+3`: if `k>n+j` or `l>n+j`, a binomial factor in `T(n+j,k,l)` vanishes, while every protected weight atom remains finite under the retained harmonic convention. No shell term is omitted.

## First bounded recurrence-certificate search

The direct `n+3` symmetric raw-jet divergence family was searched on the complete protected 198-monomial weight-five basis with independent coefficient polynomials of total degree `0,1,2`.

For each of the three recurrence right-hand sides `D`, `P5`, and `W`, exact modular affine-rank certification at `p=1000003` gives:

- degree 0: `rank(A)=198`, `rank([A|b])=199`;
- degree 1: `rank(A)=792`, `rank([A|b])=793`;
- degree 2: `rank(A)=1980`, `rank([A|b])=1981`.

All declared denominators are nonzero modulo the rank prime. These nonzero minors certify rational affine inconsistency only for this declared bounded recurrence-divergence family.

Bounded terminal:

`LOCKED_LBZ_NPLUS3_SYMMETRIC_RAW_JET_DIVERGENCE_DEG_LE_2_EXHAUSTED_FOR_D_P5_W`

This does not refute the locked recurrence and is not evidence that T3 is false.

## Q-row product-rule successor

The mathematically justified pivot is the exact unweighted-kernel Q-row architecture. Upstream `work/lb5/Qrow_rhosigma.m` is the identical Git blob `61f12f412726887f506e1d423b7ee183a22116e5` at both source commit `968477ed...` and later audited head `790685b7...`.

Conditionally on independently replaying

`L_BZ[T] = Delta_k(rho*T) + Delta_l(sigma*T)`,

the discrete product rule reduces the recurrence of any weighted sum `sum T*v` to a canonical residual built from shifted differences of `v`; see `QROW_PRODUCT_RULE.json`. This is a structurally different certificate space from the exhausted generic 198-dimensional raw-jet divergence fit.

The upstream `[CERTIFIED]` label is not Programme authority. Exact rational re-verification of the Q-row identity and its apparent-pole boundary cancellation remains pending before the reduced `E_P5`, `E_W`, or `E_D` residual can affect T3.

The source `RFD_ann.m` checkpoint is not a T3 certificate; it belongs to a weight-3 middle-row route and is absent from both audited source heads.

## Current state

`proof_effect: NONE`

`promotion_effect: NONE`

T3 remains `OPEN_WITH_CHARACTERIZED_BLOCKER`.

The active internal successor is `QROW_PRODUCT_RULE_REDUCTION_001`: independently certify the Q-row kernel identity and boundary semantics, then work on the reduced weight-five recurrence residual rather than escalating the exhausted generic flux envelope by inertia.
