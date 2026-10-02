# OZ-RT-BZ-T3-011-J

T3-011-G closes the genuinely mixed positive polynomial quadrant. T3-011-H closes the pure reciprocal axes. T3-011-I closes the genuinely mixed negative-negative Laurent quadrant. J therefore tests only the two remaining mixed-sign pairwise Laurent quadrants without changing the frozen source, endpoint banks, poles, candidate namespace, support, or harmonic content.

For each protected distinct-coordinate pair `(c,d)`, endpoint and frozen candidate `G`, J admits exactly

`x_c^r x_d^{-s}` and `x_c^{-r} x_d^s`, with integers `r >= 1`, `s >= 1`.

The direct response remains `Delta_c Delta_d(prefactor * G)` with the same four endpoint components used by F/G/H/I. Positive factors are the protected G forward coordinate factors. Negative factors are the protected H reciprocal coordinate factors. The only admitted poles are `x_c=0` and `x_d=0`.

J does not impose a degree cutoff. For every witness/source signature intersection, it solves the exact two-variable integer Laurent-signature equation. If the positive and reciprocal step signatures become rank-one opposites and an actual support intersection admits one solution, the operation reports the resulting infinite arithmetic bidegree family as an explicit blocker instead of truncating it.

The `(0,0)` component must reproduce the direct unweighted mixed response. The pure positive-axis boundary must remain annihilated under the protected polynomial closure. The pure reciprocal-axis boundary must remain annihilated under T3-011-H. The negative-negative quadrant remains the protected T3-011-I predecessor and is not reopened.

Possible terminals are:

- `MIXED_SIGN_LAURENT_RESPONSE_ESCAPE_FOUND`;
- `MIXED_SIGN_LAURENT_RESPONSE_CLASS_COKERNEL_INVISIBLE`;
- `MIXED_SIGN_LAURENT_RESPONSE_NOT_CERTIFIED__SEMANTIC_FUNCTIONAL_AMBIGUITY`;
- `MIXED_SIGN_LAURENT_RESPONSE_NOT_CERTIFIED__UNBOUNDED_SIGNATURE_OVERLAP`;
- `MIXED_SIGN_LAURENT_RESPONSE_NOT_CERTIFIED__CHARACTERIZED_BLOCKER`.

Not admitted: shifted poles, arbitrary rational functions, support/harmonic enlargement, new candidate banks or scalar namespaces, recurrence widening, correction recombination, candidate linear combinations, spectator-coordinate/trivariate multipliers, theorem promotion, or certification.

The claim firewall remains unchanged:

`residual_sum_zero_proved = false`

`proof_effect = NONE`

`promotion_effect = NONE`

`t3_status = OPEN_WITH_CHARACTERIZED_BLOCKER`

A nonzero pairing is only a response-class escape witness. An unbounded signature overlap is only a failure of the finite-support reduction used by this audit. Neither outcome proves the T3 residual identity or any zeta-value theorem.
