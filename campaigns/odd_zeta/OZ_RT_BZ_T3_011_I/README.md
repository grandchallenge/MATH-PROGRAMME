# OZ-RT-BZ-T3-011-I

T3-011-G closes the full frozen genuinely mixed positive polynomial quadrant. T3-011-H closes every pure reciprocal-axis power on either admitted coordinate. This operation therefore tests the smallest remaining Laurent interaction without changing source representation or pole location.

For each protected distinct-coordinate pair `(c,d)`, endpoint and frozen candidate `G`, admit exactly

`x_c^{-r} x_d^{-s}`, with integers `r >= 1`, `s >= 1`.

The direct response is

`Delta_c Delta_d(x_c^{-r} x_d^{-s} G)`.

The only admitted poles are `x_c=0` and `x_d=0`. Every shifted and unshifted coordinate specialization must already be a nonzero Laurent monomial on every frozen stratum before inversion.

The producer derives the finite reciprocal bidegree overlap exactly from witness/source Laurent signatures. It uses no total-degree or coordinate-degree cutoff. The `(r,0)` and `(0,s)` boundaries must exactly reproduce protected T3-011-H, while `(0,0)` must reproduce the direct unweighted mixed response. Only `r,s>=1` can constitute a new escape.

The independent verifier reconstructs the endpoint banks and witnesses through the reverse G/F path, independently derives reciprocal coordinate factors, independently solves the two-variable Laurent signature equations, independently shifts source monomials, and recomputes every tested rational pairing.

Possible terminals are:

- `MIXED_RECIPROCAL_RESPONSE_ESCAPE_FOUND`;
- `MIXED_RECIPROCAL_RESPONSE_CLASS_COKERNEL_INVISIBLE`;
- `MIXED_RECIPROCAL_RESPONSE_NOT_CERTIFIED__SEMANTIC_FUNCTIONAL_AMBIGUITY`;
- `MIXED_RECIPROCAL_RESPONSE_NOT_CERTIFIED__CHARACTERIZED_BLOCKER`.

Not admitted: shifted poles, numerator polynomials, mixed-sign Laurent monomials, arbitrary rational functions, support/harmonic enlargement, new candidate banks, recurrence widening, correction recombination, representative changes, or candidate linear combinations.

The claim firewall remains unchanged:

`residual_sum_zero_proved = false`

`proof_effect = NONE`

`promotion_effect = NONE`

`t3_status = OPEN_WITH_CHARACTERIZED_BLOCKER`

A nonzero pairing is only a response-class escape witness. It does not prove the T3 residual identity or any zeta-value theorem.
