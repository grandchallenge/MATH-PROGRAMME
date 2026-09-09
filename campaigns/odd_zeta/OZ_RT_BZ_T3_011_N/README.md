# OZ-RT-BZ-T3-011-N

T3-011-I closes the pairwise negative-negative Laurent quadrant. T3-011-M closes both single-reciprocal-active trivariate octants with a positive unshifted spectator. N changes one further active sign relative to M and tests only

`x_c^-r x_d^-s x_e^t`,

with integers `r,s,t >= 1`, where `e` is the unique coordinate axis not represented by the active pair `(c,d)`.

The producer reconstructs the protected endpoint banks, normalized witnesses, shifted semantic support indexes, reciprocal factors for both active axes, and the positive spectator factor. For each witness/base support equation it solves

`target - base = r L^- + s R^- + t E^+`

exactly in the signed Laurent lattice. No degree cutoff is used. A nonnegative homogeneous direction becomes a blocker only when an actual protected support seed lies on the resulting ray; otherwise the complete finite overlap is derived from the affine signature equations.

Two boundaries are mandatory:

1. `t = 0` reproduces protected T3-011-I negative-negative pairwise semantics.
2. Setting either reciprocal-active degree to zero reproduces the corresponding protected T3-011-M single-reciprocal-active positive-spectator semantics.

The independent verifier reconstructs the affine equations separately, recomputes all exact rational pairings, and independently determines escape, ambiguity, blocker, or exhaustive closure.

N does not admit a reciprocal spectator, an active-plus-spectator double-reciprocal octant, the all-reciprocal trivariate octant, shifted poles, arbitrary rational functions, support or harmonic enlargement, new candidate banks or scalar namespaces, recurrence widening, correction-layer recombination, candidate linear combinations, or a third finite-difference operator.

The claim firewall remains `residual_sum_zero_proved=false`, `proof_effect=NONE`, `promotion_effect=NONE`, and `t3_status=OPEN_WITH_CHARACTERIZED_BLOCKER`. No terminal proves the T3 residual identity or promotes an odd-zeta theorem.
