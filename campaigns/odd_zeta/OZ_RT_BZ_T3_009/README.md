# OZ-RT-BZ-T3-009 — locked sequence recurrence extraction

Operation: `T3_SEQUENCE_RECURRENCE_EXTRACTION_001`

Authority: issue #372. Execution intake is protected merge `fa283a283c4584c79af86fec632d50aa49e6d640` / tree `49f644c8ff4462015833d6477dfb6fde5b847970`.

## Target

The target remains

`D_n = sum_{k,l=0}^n T(n,k,l) * (W1(n,k,l) + 2*w5_sym(n,k,l)) = 0`

for every integer `n >= 0`.

No T1-top substitution is permitted.

Define the nontrivial component sequences

- `P5_n = sum T*w5_sym`;
- `W_n = sum T*W1`;
- `D_n = W_n + 2*P5_n`.

The scalar `D_n` samples are already zero, so recurrence fitting to `D_n` is forbidden as vacuous. The operator is pre-locked by T3-001 and must be proved by an exact summand/module certificate, directly for `D`, or through sufficient nontrivial component recurrences.

## Locked operator

`L_BZ[Y]_n = c0(n)Y_n + c1(n)Y_(n+1) + c2(n)Y_(n+2) + c3(n)Y_(n+3)`

with the exact polynomials in `RECURRENCE_LOCK.json`, source-pinned to `rain-1/-odd-zeta-values-moremath@968477ed7e406df6542f8da6fbe1cd6ca7273c47:work/lb5/core.py` and rebound to the existing Programme T3-001 lock.

The forward coefficient is

`c3(n)=2*(n+3)^5*(2*n+5)*a0(n)`

where `a0(n)=41218*n^3+198849*n^2+320790*n+173057`. Hence `c3(n)>0` for every integer `n>=0` by coefficient positivity.

## First exact baseline

`BASELINE_RESULT.json` is generated from the protected T3-002 target evaluator, not from fitted sequence data. It records:

- exact `P5`, `W`, and `D` values for `n=0..6`;
- `D_n=0` on that retained range;
- nonzero component values, e.g. `P5_1=87/4`, `W_1=-87/2`;
- exact locked-operator residuals `L_BZ[P5]=L_BZ[W]=L_BZ[D]=0` for `n=0..3`.

These are finite evidence only. They establish that the component-recurrence route is non-vacuous; they do not establish a recurrence theorem.

## Moving support

The order-3 recurrence combines summands at `n,n+1,n+2,n+3`. The search will use a common square through `n+3` only after exact zero-extension is established: the binomial kernel vanishes outside each natural square, and the protected harmonic convention remains finite. Any alternative certificate must account for all shell terms explicitly.

## Source audit

The upstream `CERTS_RESUME.md` contains useful creative-telescoping methodology and a certified unweighted Q-row certificate. Its `RFD_ann.m` checkpoint belongs to a weight-3 middle-row route, not T3, and is absent from both source commit `968477ed...` and later source head `790685b7...`. It is not an admissible T3 dependency.

## Current state

`proof_effect: NONE`

`promotion_effect: NONE`

T3 remains `OPEN_WITH_CHARACTERIZED_BLOCKER`.

The next mathematical step inside this operation is an exact bounded search for a summand-level certificate of the locked recurrence, with the direct defect route and component routes kept distinct and with the moving-support proof encoded rather than assumed.
