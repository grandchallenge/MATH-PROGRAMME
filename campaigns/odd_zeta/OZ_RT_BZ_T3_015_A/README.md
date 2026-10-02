# OZ-RT-BZ-T3-015-A

This tranche extracts the canonical global rational-difference module for the already-admitted T3 rational-Δ class.

## Scope

T3-014 established only that the exact inherited strict-interior obstruction disappears when each of the 506 protected correction generators is allowed an arbitrary coefficient in `Q(n,k,l)`. T3-015-A does not widen that class.

The target, correction support, harmonic alphabet, scalar namespace, recurrence data, and channel shifts remain protected and unchanged. For generator `i`, channel shift `δ`, support monomial `M`, and locked scalar multiplier `μ_s`, the global operator column is

`μ_s(n,k,l) [ q_i(n+δ) M(n+δ) - q_i(n) M(n) ]`.

The unknown `q_i` is a single rational function. Its values at different lattice points are therefore not independent in the global problem.

## Exact output

The producer reconstructs from protected state:

- the 506 canonical generator identities;
- exact channel shifts;
- exact shifted-monomial expansions in the protected harmonic basis;
- the protected target grouped by the seven scalar functions `TN1,TN2,TN3,SK,AK,LKK,LLK`;
- canonical rational-function serialization;
- coordinate and target counts;
- one SHA-256 digest of the complete module.

The verifier reconstructs the same object independently through the verifier lineage and a reverse traversal before canonical sorting. It does not import the producer module as authority.

No finite `(n,k,l)` sample grid is used by this tranche. No numerator-degree, denominator-degree, denominator-family, recurrence-order, or support scan is admitted.

## Source doctrine

The pinned source revision maps the T3 continuation to rational Δ / creative telescoping and states that the relevant letter shifts close in a finite module over `Q(n,k,l)`:

- `work/Z5T3_BRIDGE.md`, blob `002c96d28123e5949c38656f26677ae5a723ee93`;
- `work/Z5CF_LINALG.md`, blob `637ecaa7f3ee941a87932de390eb7336d7fde677`;
- `work/lb5/Qrow_rhosigma.m`, blob `61f12f412726887f506e1d423b7ee183a22116e5`.

The historical source ansatz scans are evidence about bounded searches. They are not used here as completeness bounds.

## Terminal

Successful extraction has terminal

`GLOBAL_RATIONAL_DELTA_DIFFERENCE_MODULE_EXTRACTED__COMPLETE_RATIONAL_SOLVER_REQUIRED`.

That terminal is administrative/mathematical infrastructure for the same admitted class. It does not establish a global rational certificate or a nonexistence result. The next tranche must solve this exact rational difference system globally or provide a completeness-backed obstruction.

## Claim firewall

Always:

- `global_certificate_constructed = false`;
- `residual_sum_zero_proved = false`;
- `proof_effect = NONE`;
- `promotion_effect = NONE`;
- `t3_status = OPEN_WITH_CHARACTERIZED_BLOCKER`.

No other OZ lane or downstream claim is promoted.
