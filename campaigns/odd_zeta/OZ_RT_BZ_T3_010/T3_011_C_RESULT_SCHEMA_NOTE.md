# T3-011-C result ledger semantics

The producer emits one deterministic JSON object. Each independent channel records the frozen candidate count and order digest, the active-cell namespace digest, and one row per candidate.

Each candidate binds two evidence layers for four response paths: direct raw finite difference, direct product-rule expansion, T3-011-B producer response, and T3-011-B independent-verifier response.

1. **Representation digests** preserve the exact Laurent-signature encoding emitted by each path. They are provenance evidence only; they are not semantic equality authority because an affine factor such as `n+1` need not be stored in the same representation as the additive expression `n + 1`.
2. **Semantic digests** use `COMMON_DENOMINATOR_EXPANDED_Q_N_K_L_NUMERATOR_V1`. After protected shell specialization, coefficient signatures are grouped by cell/scalar/harmonic monomial; all four Laurent rational functions are lifted to one exact common denominator; every integer-affine factor is expanded in `Q[n,k,l]`; the resulting numerator polynomials are compared coefficient-for-coefficient. No finite sampling is used.

The `l1` ledger audits all 110 mirror images of the frozen `k1` bank and preserves the exact source-candidate marker.

The only positive terminal is `T3_011_B_LIFTED_RESPONSE_GENERATOR_SEMANTICS_CERTIFIED`; any semantic response disagreement yields `T3_011_B_LIFTED_RESPONSE_GENERATOR_SEMANTICS_MISMATCH`.

Neither terminal proves the T3 residual identity. The claim firewall remains `proof_effect=NONE`, `promotion_effect=NONE`, and `t3_status=OPEN_WITH_CHARACTERIZED_BLOCKER`.
