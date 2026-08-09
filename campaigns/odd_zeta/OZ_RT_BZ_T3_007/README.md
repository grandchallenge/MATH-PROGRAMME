# OZ-RT-BZ-T3-007 — coupled weight-five raw-jet orders 3–4 search

Authority: issue #359. Predecessor: issue #356 / PR #357, protected at
`d9b9ed1a3a4c7ab56d25091e724fa585fbcea071` with tree
`2a7bd5d53af76b6705ebd526dae667a381860374`.

## Locked target

`sum_{k=0}^n sum_{l=0}^n T(n,k,l) * (W1(k,l)+2*w5_sym(n,k,l)) = 0`

T1-top substitution is forbidden.

## Search

This operation raises only the external fibre-telescoper order while holding the
T3-006 polynomial envelope fixed.

For `r in {3,4}`:

`sum_{j=0}^r a_j(n,k) F(n,k+j,l) = Delta_l Q_r(n,k,l)`

with

`Q_r = T(n,k,l)/((l+1)^3*(k+l+1)) * sum_M q_{r,M}(n,k,l) M(n,k,l)`.

The coefficient constraints are:

- `a_j(n,k)` total degree `<= 2`;
- all 198 protected weight-five raw-jet monomials have independent certificate coefficients;
- certificate coefficient total degrees `0,1,2`;
- the exact `k <-> l` mirror remains a relabeling, not independent evidence.

The protected raw derivative coordinates are normalized by the nonzero integer
`raw_derivative_multiplier` attached to each T3-005 monomial. The 198
multipliers are nonzero over `Q` and nonzero modulo `1000003`; this is an
invertible diagonal coordinate change and therefore preserves rank.

## Exact result

All declared stages are full column rank modulo `p = 1000003`.

Order 3:

- degree 0: rank `222 / 222`;
- degree 1: rank `816 / 816`;
- degree 2: rank `2004 / 2004`.

Order 4:

- degree 0: rank `228 / 228`;
- degree 1: rank `822 / 822`;
- degree 2: rank `2010 / 2010`.

Every exact rational denominator on the declared grids is nonzero modulo the
rank prime. Each full modular rank therefore exhibits a nonzero maximal minor
and certifies rational full column rank for the corresponding bounded class.

Producer witnesses use the first square subset of each order-aware
lexicographic grid. The independent verifier reconstructs the source-locked T3
cell through the protected direct formula path and uses the last square subset,
reversed basis ordering, and reversed elimination-column ordering.

Terminal bounded-search classification:

`ORDER3_4_COMPLETE_WEIGHT5_MODULE_BOUNDED_CLASS_EXHAUSTED`

## Claim boundary

This does **not** prove T3 and does **not** refute T3.

T3 remains:

`OPEN_WITH_CHARACTERIZED_BLOCKER`

with:

- `proof_effect: NONE`;
- `promotion_effect: NONE`;
- no effect on T1-top, DEPTH, Sharp-12, MATHCERT, `GRAPH_CERTIFIED`, source
  authority, novelty, priority, publication, patentability, deployment, or
  commercial claims.

The primary next distinct research architecture is
`SYMMETRIC_2D_RAW_JET_DIVERGENCE_001`. The direct
`T3_SEQUENCE_RECURRENCE_EXTRACTION_001` route remains retained as an
alternative. These are research successors only and carry no theorem
promotion.
