# OZ-RT-BZ-T3-011-L

T3-011-K closes the positive unshifted-spectator trivariate class. L changes exactly one mechanism: the spectator exponent becomes negative while the two active coordinate exponents remain positive.

The admitted multiplier is

`x_c^r x_d^s x_e^-t`, with integers `r >= 1`, `s >= 1`, `t >= 1`,

where `e` is the unique remaining coordinate axis and is not shifted by either finite difference.

The first question is whether the exact Laurent support still gives a finite exhaustive tridegree domain. A geometric cancellation relation alone is not sufficient. L requires both:

1. a primitive nonnegative recession ray

   `dr L + ds R - dt E = 0`, with `dt > 0` and `dr + ds > 0`; and

2. an actual protected witness/base support match with a positive integer seed

   `target - base = r L + s R - t E`, with `r,s,t >= 1`.

Only when both conditions hold does the ray pass through the admitted response domain. Then every seed plus a nonnegative multiple of the primitive ray is another admissible tridegree with the same endpoint Laurent signature. The domain is genuinely unbounded, and issue #920 requires termination with a characterized blocker instead of an arbitrary degree cutoff.

This distinction is material. Protected shell specialization can identify distinct ambient coordinate factors, for example by setting `k=n` or `l=n`, but such a local factor coincidence does not by itself prove that any admitted witness/base support pair lies on the resulting ray.

The producer binds the protected K and G source objects, reconstructs the protected shell strata, endpoint banks, coordinate-factor maps, witness indexes, and shifted semantic base indexes, then scans the canonical pair/endpoint/candidate/component/support order. It reports an unbounded blocker only at the first support-feasible recession ray.

The independent verifier reconstructs the endpoint banks and factor maps through the reverse G verification path. It independently checks integer feasibility of the same support equation, reproduces the first canonical ray-bearing support match, and verifies the producer's emitted positive seed and primitive ray factor-by-factor.

If a support-feasible unbounded ray is found, no cokernel-pairing candidate record is tested. That is deliberate: finite truncation of an unbounded class would create a false closure claim. The result records how many candidate support records and ray-bearing signature pairs were inspected before the blocker.

No reciprocal power is admitted on the two active axes. No shifted spectator, shifted pole, second reciprocal axis, arbitrary rational function, support/harmonic/candidate-bank widening, recurrence widening, correction recombination, candidate linear combination, third finite difference, theorem promotion, or certification is admitted.

The claim firewall remains:

`residual_sum_zero_proved = false`

`proof_effect = NONE`

`promotion_effect = NONE`

`t3_status = OPEN_WITH_CHARACTERIZED_BLOCKER`

A characterized reciprocal-spectator cancellation ray is a statement about the admitted response-class parameterization. It does not prove or refute T3 and does not promote any odd-zeta theorem.
