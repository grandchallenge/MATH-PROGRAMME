# PAAR-C — October 15 CHAD execution-origin adjudication

**Disposition: HISTORICAL_OUTPUT_HASH_MATCH_ORIGINAL_EXECUTION_ORIGIN_UNATTESTED.**

The actual INTELLECT dossier, Git blob `4b3d108922ed9cf345d6407d81a216a93da697c1`, is protected evidence for MATH-PROGRAMME PR #2624, subject head `e577477b656c6865698d5dbc18962e2810f53a26`, under historical INTELLECT PR #121. It contains three logical Verifier, Adversary and Referee checks. Recovered local stdout/stderr bytes match all three declared SHA-256 digests. This establishes source fidelity to the recorded outputs, **not authenticated original command execution**.

The operations-console SQLite journal spans the original output-creation window (October 15, 2026 at approximately 08:09 UTC). Twenty-seven run_bash accepted/completed events were found in the bounded 08:08–08:12 UTC search. Their rows expose event/run IDs, times, operation, phase, optional receipt, and exit code, but no command text or output; none of those 27 has an embedded receipt. The 191 retained Commander receipts examined contained branch/project/operator metadata but no original executable command-output binding. These results cover **only the inspected sources and time window**, not every possible external or earlier log. Local file modification times are OS-controlled metadata, not independent signatures.

INTELLECT source PR #121 has no native GitHub PR review event. It was admitted under the previous historical branch ruleset. Do not fabricate a retrospective reviewer or invalidate its explicitly pinned legacy receipt merely because today's INTELLECT ruleset requires a native nonauthor approval.

The later, independently corroborated GitHub-hosted test run #38988609732 is separately established with protected original witness under MATH-PROGRAMME PR #2717 and a positive production readback on protected main after PR #2718. It proves **that later runner replay occurred**; it cannot certify the original October 15 CHAD command executions or authenticate independently operating specialist persons.

## Governance consequence

- Preserve the exact-pin historical V1 receipt as `HISTORICAL_LOCKED_V1_NO_CONSUMER_OUTPUT_CHECK` with no independent execution attestation.
- Preserve V2 output identity verification and its explicit `independent_execution_certified=false` result. Do **not** promote the separate platform replay into an original-execution witness.
- Treat claims of authenticated October 15 command origin as **UNVERIFIED** unless an independently authenticated *contemporaneous* record binds exact command, subject head, execution time, executing service, and actual output bytes/hash. Later self-signed or backfilled records do not satisfy this.
- Existing GCL-PAAR-001 parent and PAAR-C remediation remain open. An independent exact-head specialist review of this forensic determination is a distinct obligation; review approval would attest review of the determination, **not** repair historical command provenance.
- Future original-run authority needs prospective, durable, content-addressed execution records with authenticated service origin captured at execution time, before logical reviewer admission. The current protected GitHub-hosted mechanism is a separate replay, not a backfill.

Reproduce the bounded inspection on an authorized CHAD workstation using `governance/assurance/GCL-PAAR-001/paar_original_origin_forensics.py` with `--evidence-dir`, `--console-db`, `--commander-receipts-dir` and `--output`. Run `python3 -m unittest -q tests.test_paar_original_origin_forensics` for adversarial tests. The protected result JSON intentionally contains only hashes, counts, contract fields and limits, not private raw logs.
