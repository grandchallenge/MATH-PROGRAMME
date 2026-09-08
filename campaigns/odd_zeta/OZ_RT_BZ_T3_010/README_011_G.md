# OZ-RT-BZ-T3-011-G

This operation asks whether the protected T3-011-E/F cokernel obstruction closes the entire frozen genuinely mixed polynomial-multiplier class.

For each F-admitted distinct-coordinate pair `(c,d)`, endpoint, and frozen candidate `G`, the admitted monomials are exactly

`x_c^r x_d^s`, with integers `r >= 1` and `s >= 1`.

Pure-axis monomials and same-coordinate pairs are excluded because T3-011-E already closes the corresponding single-coordinate polynomial class.

The producer does not choose a maximum degree. It derives the exact finite multidegree overlap from the normalized endpoint witness support for the four direct components of

`Delta_c Delta_d(x_c^r x_d^s G)`.

Outside that finite overlap every component pairing is identically zero. Inside it the response pairing is computed exactly over `Q`. The `(1,1)` value must reproduce the protected T3-011-F pairing for every admitted record.

An independent verifier reconstructs the F banks and witnesses, independently shifts the source monomials, independently derives the multidegree support overlap, and recomputes every exact rational pairing.

Possible terminals are:

- `MIXED_POLYNOMIAL_MULTIPLIER_COKERNEL_CLOSURE_CERTIFIED`;
- `MIXED_POLYNOMIAL_CLOSURE_REDUCES_TO_FINITE_MULTIDEGREE_SET`;
- `MIXED_POLYNOMIAL_CLOSURE_NOT_CERTIFIED__SEMANTIC_FUNCTIONAL_AMBIGUITY`;
- `MIXED_POLYNOMIAL_CLOSURE_NOT_CERTIFIED__CHARACTERIZED_BLOCKER`.

The operation does not widen support, harmonic basis, candidate banks, scalar namespaces, rational prefactors, recurrence classes, correction architecture, or representative identity.

The claim firewall is unchanged:

`residual_sum_zero_proved = false`

`proof_effect = NONE`

`promotion_effect = NONE`

`t3_status = OPEN_WITH_CHARACTERIZED_BLOCKER`
