# OZ-RT-BZ-T3-015-B

This operation continues the protected rational-Delta coefficient class after T3-015-A. It does not widen the class and does not use a finite sample fit.

## Protected input

T3-015-A merged at `a4eec4259ae6f7e12028cae1384a17ba865926e4` and admitted the canonical global module with SHA-256

`cdabf6d7873f3aa8e9d53b39fd7b15341dbee58ce9684911d015aee9aaae04da`.

The module has 506 protected generators, 167 coordinate monomials, and 513 target records over the scalar namespace `TN1,TN2,TN3,SK,AK,LKK,LLK`.

## Current tranche

The first T3-015-B tranche performs an exact structural solver reduction. It reconstructs the protected module and derives, without samples or denominator guesses:

- the exact scalar-family partition;
- the support monomials and channel multiplicities available to each scalar family;
- the non-self monomial dependency graph induced by every exact shift expansion;
- graph acyclicity and topological levels;
- exact target/support coverage;
- the distinct shift directions used by each scalar family.

The verifier reconstructs the predecessor module independently through the T3-015-A verifier lineage and repeats the structural analysis with an independent traversal.

This structural reduction is used to decide whether the global rational system decomposes into triangular scalar rational-recurrence blocks, and therefore whether a complete Abramov-Bronstein-style rational recurrence solver can be applied blockwise. It is not itself a certificate search.

## Completeness discipline

The upstream `work/z5la/cascade.py` is explicitly a measured-pole adaptive ansatz. It may be used later to discover positive candidates, but a failure of that bounded machinery cannot establish nonexistence in `Q(n,k,l)`.

A positive T3-015-B exit requires explicit rational coefficients followed by independent exact symbolic replay of every protected coordinate. A negative exit requires a complete rational-solution argument, including justified universal denominator constraints; arbitrary denominator families and degree cutoffs are forbidden.

## Current terminal

Successful structural reduction has terminal

`GLOBAL_RATIONAL_DELTA_SOLVER_STRUCTURE_EXTRACTED__COMPLETE_RATIONAL_SOLVER_REQUIRED`.

The issue remains open after this terminal. The next in-issue tranche must consume the reported exact block structure and execute the complete rational solver.

## Claim firewall

Always in this structural tranche:

- `global_certificate_constructed = false`;
- `residual_sum_zero_proved = false`;
- `proof_effect = NONE`;
- `promotion_effect = NONE`;
- `t3_status = OPEN_WITH_CHARACTERIZED_BLOCKER`.
