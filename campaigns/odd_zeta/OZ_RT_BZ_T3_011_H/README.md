# OZ-RT-BZ-T3-011-H

T3-011-G closes the entire frozen pairwise polynomial-multiplier algebra. This operation therefore changes mechanism rather than increasing polynomial degree.

For each protected distinct-coordinate pair `(c,d)`, endpoint, frozen candidate `G`, and prefactor side `q in {c,d}`, admit exactly

`x_q^{-r}`, with integer `r >= 1`.

The direct response is

`Delta_c Delta_d(x_q^{-r} G)`.

This is the smallest controlled rational extension that remains inside the protected Laurent-monomial specialization semantics. The only admitted pole is `x_q=0`. Every unshifted and shifted coordinate specialization must already be a nonzero Laurent monomial on every frozen stratum before inversion. A zero or non-monomial specialization is a characterized blocker.

For `q=c`, the four exact components are:

- `(x_c+h_c)^{-r} S_cS_d(G)`;
- `(x_c+h_c)^{-r} S_c(G)`;
- `x_c^{-r} S_d(G)`;
- `x_c^{-r} G`.

For `q=d`, the shifted reciprocal factor occurs in the `S_cS_d(G)` and `S_d(G)` components instead.

The producer derives the finite reciprocal-degree support overlap exactly by negating the protected Laurent signatures. It does not choose a degree cutoff. The deterministic order is pair, endpoint, candidate, left prefactor side, right prefactor side, then increasing reciprocal degree. Execution stops on the first exact nonzero normalized cokernel pairing; otherwise the full reciprocal-axis class is exhausted.

The independent verifier reconstructs the endpoint banks and witnesses through the reverse verifier path, independently derives reciprocal coordinate factors, independently shifts source monomials, independently solves the exact Laurent signature equations, and recomputes every tested pairing.

Possible terminals are:

- `RECIPROCAL_AXIS_RESPONSE_ESCAPE_FOUND`;
- `RECIPROCAL_AXIS_RESPONSE_CLASS_COKERNEL_INVISIBLE`;
- `RECIPROCAL_AXIS_RESPONSE_NOT_CERTIFIED__SEMANTIC_FUNCTIONAL_AMBIGUITY`;
- `RECIPROCAL_AXIS_RESPONSE_NOT_CERTIFIED__CHARACTERIZED_BLOCKER`.

Not admitted: shifted poles, mixed reciprocal products, polynomial numerators, arbitrary rational functions, support/harmonic enlargement, new candidate banks, recurrence widening, correction recombination, representative changes, or candidate linear combinations.

The claim firewall is unchanged:

`residual_sum_zero_proved = false`

`proof_effect = NONE`

`promotion_effect = NONE`

`t3_status = OPEN_WITH_CHARACTERIZED_BLOCKER`

A nonzero pairing is only a response-class escape witness. It does not prove the T3 residual identity or any zeta-value theorem.
