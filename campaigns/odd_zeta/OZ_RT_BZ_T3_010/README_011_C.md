# OZ-RT-BZ-T3-011-C

This operation audits the response-generator semantics used by the completed T3-011-B bounded search. It freezes the exact 311 independent nonzero-response single-channel lifts from T3-011-B and the 110 mirror-derived `l1` checks.

For each frozen candidate, a third response path reconstructs the raw finite difference of `x_c G` directly from the protected primitive harmonic shift semantics:

`Delta_c(x_c G) = (x_c + Delta_c x_c) S_c(G) - x_c G`.

The same path independently expands the discrete product rule

`Delta_c(x_c G) = x_c Delta_c(G) + (Delta_c x_c) S_c(G)`,

then requires exact equality with the existing T3-011-B producer response and the separately implemented T3-011-B verifier response.

The direct path is source-audited so it cannot call either predecessor lifted response generator, or the producer/verifier shift-specialization-response helper chain that would collapse the comparison into shared authority.

A successful audit terminates only as `T3_011_B_LIFTED_RESPONSE_GENERATOR_SEMANTICS_CERTIFIED`. A disagreement terminates fail-closed as `T3_011_B_LIFTED_RESPONSE_GENERATOR_SEMANTICS_MISMATCH`.

No candidate widening, pair search, generic degree-one envelope, support or harmonic enlargement, rational prefactor, raw-jet reopening, correction-layer recombination, recurrence search, or theorem promotion is authorized.
