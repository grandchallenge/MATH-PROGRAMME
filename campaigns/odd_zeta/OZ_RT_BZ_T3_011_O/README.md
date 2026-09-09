# OZ-RT-BZ-T3-011-O

`T3-011-O` audits the two remaining trivariate Laurent sign octants with exactly one reciprocal active coordinate and one reciprocal unshifted spectator:

- `Delta_c Delta_d(x_c^-r x_d^s x_e^-t G)`;
- `Delta_c Delta_d(x_c^r x_d^-s x_e^-t G)`;

for integers `r,s,t >= 1`, where `e` is the unique coordinate axis not shifted by the active pair `(c,d)`.

The operation retains the protected seven unordered channel pairs, endpoint banks, witnesses, candidate order, scalar namespace, support, harmonics, shifts, and coefficient system. It derives admissible overlap from exact Laurent-factor signatures. It does not use an arbitrary degree cutoff. A homogeneous cancellation direction is admitted as an unbounded response family only when an actual protected witness/base support seed lies on that direction.

## Boundary semantics

The spectator reciprocal degree-zero face must reproduce protected `T3-011-M` single-reciprocal-active positive-spectator semantics. The reciprocal-active degree-zero face must reproduce the protected `T3-011-L` reciprocal-spectator factorization. The positive-active degree-zero face is recorded only as a direct-response anchor. It is not identified with `T3-011-I`, because the second reciprocal coordinate on that face is the unshifted spectator rather than the second active finite-difference axis.

## Exclusions

The all-reciprocal `---` trivariate octant remains excluded. The operation also excludes shifted poles, arbitrary rational functions, support or harmonic widening, candidate-bank or scalar-namespace widening, recurrence/telescoper widening, correction-layer recombination, candidate linear combinations, a third finite-difference operator, and every theorem or certification promotion.

## Producer/verifier separation

`producer.py` extends the protected signed Laurent solver from `T3-011-N` to the two `-+-` / `+--` octants. `verifier.py` reconstructs the endpoint support and response algebra independently and uses a separate exact Diophantine solver. Both paths bind the protected N source blobs and exact protected merge.

## Claim firewall

This is a response-class cokernel audit only. `residual_sum_zero_proved` remains false. `proof_effect` and `promotion_effect` remain `NONE`. T3 remains `OPEN_WITH_CHARACTERIZED_BLOCKER` unless and until a separately governed operation proves or refutes it.
