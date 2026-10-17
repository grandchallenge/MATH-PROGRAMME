# GCL-PAAR-001 — bounded routing and public-content readback

2026-10-17 UTC. This is one evidence tranche for completed existing [#2705](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2705), not a new assurance programme.

**Seven real routing failures:** [CAUSAL_ROUTING_CASES_20261017.tsv](CAUSAL_ROUTING_CASES_20261017.tsv) pins original PR heads, failing Actions run IDs and candidate workflow paths. For all seven, GitHub logs report `RoutingGateError: workflow routing coverage mismatch`; exact candidate Git trees contain the unregistered workflow absent from their own registry. [Reproduce](verify_causal_routing_witnesses.sh) with authenticated read-only GitHub CLI. Positive comparator: TROVE-CURATA PR #6, successful routing check 101215034855, protected merged.

**Two real published Erdős examples:** [ERDOS_PUBLIC_PARITY_20261017.md](ERDOS_PUBLIC_PARITY_20261017.md) records four exact protected-source-to-live-HTML matches for #99 and #1053, including non-certification statements.

**Decision:** `PASS_BOUNDED` for these concrete validator and text specimens. NOT proof that every PR closure was caused by the failed check, domain-specific REVISE validity, complete publication parity, or GCL-wide certification. Private executive readback and the bounded internal PAAR-E final receipt are now protected-admitted; neither creates publication certification. Historical October 15 CHAD original origin remains UNATTESTED. PAAR-C #2708 and INTELLECT #126 remain closed.
