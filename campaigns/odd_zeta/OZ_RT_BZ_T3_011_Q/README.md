# OZ-RT-BZ-T3-011-Q

Q audits the lower-dimensional faces already present in the protected T3-011 trivariate Laurent ladder when exactly one active-coordinate exponent is zero.

It does not widen the multiplier syntax. It source-locks protected M, N, O, and P, then reconstructs only the required face rows rather than rerunning the full parent search classes.

The four surviving active-axis/spectator sign families are `++`, `-+`, `+-`, and `--`:

- `++`: reconstructed from the protected K-boundary semantics used by M;
- `-+`: reconstructed from the double-reciprocal N boundary with one active exponent zero;
- `+-`: reconstructed from the O class with the reciprocal active exponent zero;
- `--`: reconstructed from the P class with one reciprocal active exponent zero.

The producer computes the exact rows in deterministic family, pair, endpoint, candidate, and side order. It stops at the first exact nonzero protected cokernel pairing or closes all four one-zero sign families. No arbitrary degree cutoff is used.

The verifier uses the protected independent M/N/O/P ledger implementations and their independent signed-degree solvers to reconstruct the same face partition and exact rational pairings. It does not consume producer face matrices or pairings. Exact parent source/blob locks remain mandatory.

A Q closure does **not** close the full coordinate-zero Laurent monomial algebra. The strictly lower-dimensional family with both active exponents zero and a nonzero spectator exponent remains outside Q and must be handled separately before any full-algebra corollary is admitted.

Authorized terminals:

- `ACTIVE_ZERO_LAURENT_FACE_ESCAPE_FOUND`;
- `ACTIVE_ZERO_LAURENT_FACES_COKERNEL_INVISIBLE`;
- `ACTIVE_ZERO_LAURENT_FACES_NOT_CERTIFIED__CHARACTERIZED_BLOCKER`.

Claim firewall remains:

`residual_sum_zero_proved = false`

`proof_effect = NONE`

`promotion_effect = NONE`

`t3_status = OPEN_WITH_CHARACTERIZED_BLOCKER`
