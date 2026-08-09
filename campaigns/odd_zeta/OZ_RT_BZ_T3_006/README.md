# OZ-RT-BZ-T3-006: coupled weight-five raw-jet order-2 search

Operation: `COUPLED_WEIGHT5_RAW_JET_ORDER2_SEARCH_001`.

Mathematical predecessor: issue #341 / PR #344 (`OZ-RT-BZ-T3-005`), protected at merge `e99defaabbc0d971e6299360ac03084e516c31c3` / tree `041b4f7afa647fec06d3303503b53fa0fc65350d`.

Execution intake is the then-current protected `main` head `d2cdd1cfb57feb648bdd624a3362dae646a8b72f` / tree `3b7cc40fbf7f82cb1c219aef6b9733429e83e54f`.

## Locked target

The target remains exactly

`sum_{k=0}^n sum_{l=0}^n T(n,k,l) * (W1(k,l) + 2*w5_sym(n,k,l)) = 0`.

No T1-top substitution is permitted.

`OZ-RT-BZ-T3-005` supplies a linear raw-derivative extraction of the complete weight-five cell into 198 exact monomials. Of these, 158 are one-body-only and 40 contain exactly one nested `U/ES` atom; both nested orientations are present. The raw-jet map is symmetric under `k <-> l`.

The search uses normalized raw-jet coordinates. For every monomial, T3-005 records a nonzero integer `raw_derivative_multiplier`; the harmonic representative used here is the corresponding raw mixed derivative divided by that multiplier. All such multipliers are products of factorials of orders at most five and are nonzero in `Q` and modulo `p=1000003`. Passing between the protected raw derivatives and these normalized coordinates is therefore an invertible diagonal column rescaling and does not change rank or nullity.

## Search equation

Let

`F(n,k,l) = T(n,k,l) * (W1(k,l) + 2*w5_sym(n,k,l))`.

The retained order-2 fibre ansatz is

`sum_{j=0}^2 a_j(n,k) F(n,k+j,l) = Delta_l Q(n,k,l)`

with

`Q = T(n,k,l) / ((l+1)^3*(k+l+1)) * sum_{M in M5} q_M(n,k,l) M(n,k,l)`.

Here `M5` is the complete 198-monomial normalized weight-five raw-jet basis from T3-005. Each `a_j` is polynomial in `(n,k)`. Each `q_M` is polynomial in `(n,k,l)`. The denominator is inherited from the exact `l`-shift ratio of the undeformed binomial kernel rather than guessed freely.

Because the target polynomial and basis are exactly invariant under `k <-> l`, the mirror `l`-shift / `k`-flux problem is equivalent by relabeling; the producer verifies this symmetry instead of spending an independent search budget on an isomorphic matrix.

## Bounded ladder

The producer executes two nested classes.

First, a scalar-envelope necessary class uses `Q = F*q/D`, with `a_degree = 0..6` and `q_degree = a_degree+2`, reproducing the same degree frontier used for the undeformed order-2 search while testing the fully extracted T3 cell.

Second, the full weight-five module fixes `a_degree = 2` and allows independent certificate coefficients for all 198 monomials with total coefficient degree `q_degree = 0,1,2`.

Every system is the reduction of an exact rational system. Reduction modulo `p=1000003` is used only as an exact negative rank certificate; every rational entry denominator is required to be nonzero modulo `p`. Full column rank modulo `p` exhibits a nonzero maximal minor modulo `p`, and therefore proves full column rank over `Q` for the declared ansatz.

A nullspace is discovery only. Any positive candidate requires rational reconstruction, exact symbolic substitution, finite-boundary verification, independent replay, and the separate propagation/initial obligations required to turn a fibre telescoper into T3.

## Result

The scalar envelope is full column rank at every retained stage through `a_degree=6`, `q_degree=8`.

The complete 198-dimensional module is also full column rank at every retained coefficient degree:

- coefficient degree 0: rank `216/216`, nullity `0`;
- coefficient degree 1: rank `810/810`, nullity `0`;
- coefficient degree 2: rank `1998/1998`, nullity `0`.

The strongest degree-2 witness uses 1,998 rows selected from a declared 2,278-row exact grid. The independent verifier uses the opposite end of that grid and reversed basis/column ordering.

Thus the exact bounded class

`COUPLED_WEIGHT5_RAW_JET_ORDER2_ADEG_LE_2_QCOEFFDEG_LE_2`

is exhausted.

Terminal search classification:

`ORDER2_COMPLETE_WEIGHT5_MODULE_BOUNDED_CLASS_EXHAUSTED`

This is not a refutation of T3. The next retained route is `COUPLED_WEIGHT5_RAW_JET_ORDER3_4_SEARCH_001`; `SYMMETRIC_2D_RAW_JET_DIVERGENCE_001` and `T3_SEQUENCE_RECURRENCE_EXTRACTION_001` remain distinct alternatives.

## Claim boundary

A full-rank result is an exact negative result only for the declared order-2 raw-jet certificate class. It does not refute T3.

A positive order-2 fibre relation would not by itself prove T3. `T3_PROVED` remains inadmissible unless the relation is promoted through exact finite-boundary handling and all recurrence/initial or direct-divergence obligations needed for the locked zero sum.

This operation has no effect on T1-top, DEPTH, Sharp-12, MATHCERT, `GRAPH_CERTIFIED`, source authority, novelty, priority, publication, patentability, deployment, or commercial claims.

T3 remains `OPEN_WITH_CHARACTERIZED_BLOCKER`.

`proof_effect: NONE`

`promotion_effect: NONE`
