# T3-011-C result ledger semantics

The producer emits one deterministic JSON object. Each independent channel records the frozen candidate count and order digest, the active-cell namespace digest, and one row per candidate. Every row binds four exact response digests: direct raw finite difference, direct product-rule expansion, T3-011-B producer response, and T3-011-B independent-verifier response.

The `l1` ledger audits all 110 mirror images of the frozen `k1` bank and preserves the exact source-candidate marker.

The only positive terminal is `T3_011_B_LIFTED_RESPONSE_GENERATOR_SEMANTICS_CERTIFIED`; any response disagreement yields `T3_011_B_LIFTED_RESPONSE_GENERATOR_SEMANTICS_MISMATCH`.

Neither terminal proves the T3 residual identity. The claim firewall remains `proof_effect=NONE`, `promotion_effect=NONE`, and `t3_status=OPEN_WITH_CHARACTERIZED_BLOCKER`.
