# PAAR-C — Protected specialist-review provenance boundary

**Disposition:** PARTIAL_WITH_CONFIRMED_CONSUMER_VALIDATION_GAPS.

Source: MATH-PROGRAMME protected head b28049b1969112d649d9e4b99a3cb900a1e6f6c0; INTELLECT protected head d43cdd1b478ad1816ee6c838f8e7500ca11c547f.

This bounded assurance finding is not a demonstrated production forgery, mathematical certification, or GCL-wide conformance verdict.

## Reproduction

1. Run: python3 governance/assurance/GCL-PAAR-001/audit_role_boundary.py. The script invokes the actual ci/agent_role_receipt.py consumer against a sandbox-only simulated protected source and GitHub API. No remote writes.
2. Run: python3 governance/assurance/GCL-PAAR-001/replay_baseline.py --live. Result: 14 pinned source blobs reverified, PASS_BOUNDED_ONLY; the MATH-PROGRAMME main head changed because PAAR #2706 merged, not because of blob drift.
3. Run: python3 -m unittest -q ci.test_erdos_compendium_publication_gate ci.test_erdos_compendium_editorial_replay. Result: 40/40 PASS on the exact protected MATH-PROGRAMME revision (sparse checkout restored .github/workflows, governance/erdos_compendium, governance/erdos_catalogue, and docs/erdos_compendium).
4. Query GET /repos/grandchallenge/INTELLECT/pulls/121, its /reviews endpoint, and GET /repos/grandchallenge/INTELLECT/rules/branches/main. Result: real source PR #121 merged, zero native PR reviews, effective pull_request rule required_approving_review_count=0, with required check contexts.

The replay's exact observations, source SHA-256, source heads and negative controls are recorded in PAAR_C_ROLE_BOUNDARY_REPLAY.json.

## PAAR-C01: Unverified test-digest acceptance

The actual verify_agent_role_receipt verifies that each declared check has a command, integer exit code zero, and syntactically valid 64-character hex receipt digest. It does not resolve the digest to an authenticated execution artifact or replay that command.

An injected, hypothetical protected dossier whose three checks specify command=never-run and digest=64 zeroes is ACCEPTED when the simulated GitHub protected PR, source blob and CI contexts pass.

**Classification:** OBSERVED_CONSUMER_GAP / END_TO_END_EXPLOIT_UNKNOWN. This proves the isolated consumer cannot establish execution from check-digest shape. It does not prove an attacker could merge an invalid dossier through actual GitHub.

## PAAR-C02: Logical role-origin evidence

The same consumer accepts declared VERIFIER, ADVERSARY and REFEREE passes based on structurally valid logical pass IDs, reviewer_system_id and asserted read-only activity, without fetching an independently attributable execution witness per pass. Its mock need not provide a PR /reviews endpoint.

Real INTELLECT [source PR #121](https://github.com/grandchallenge/INTELLECT/pull/121) has zero native GitHub review records, and its actual branch rules require zero native approving reviews. This is **not itself a violation** of the single-account, multiple-logical-role GCL policy. It does mean generic protected CI/merge evidence does not itself establish that claimed specialist executions occurred.

**Classification:** OBSERVED_CONSUMER_GAP / SOURCE_POLICY_CONFORMANCE_NOT_YET_ESTABLISHED.

## PAAR-C03: Effective negative controls

The consumer *does reject* a stale reviewer source head, mismatched protected dossier blob, failure in any required source CI context and a protected source branch moving during readback.

**Classification:** PASS_BOUNDED.

## Existing-policy remediation criteria

- Reuse GCL-ARC-001 and the existing domain receipt adapter. Do not invent another controller, require separate GitHub logins, or introduce routine human review.
- Bind each claimed specialist check to content-addressed, independently verifiable execution evidence, or a trusted, exact-head CI artifact. Verify executable command, environment, exit status and actual evidence digest rather than accepting a syntactically valid hex string.
- Authenticate each declared logical role's nonauthoring execution witness, while permitting multiple roles to use a shared authenticated transport account and, where policy permits, one agent system.
- Preserve distinction between nonauthoring logical-role review and scientifically independent-method validation. No mathematical certification may be inferred from PROTECTION role review.
- Do not require native GitHub approvals where the actual ruleset does not; do not claim approvals absent from GitHub. Bind alternative review provenance to protected evidence if such an alternative is authoritative.
- Add adversarial tests for nonexistent command outputs, missing artifacts, forged role passes, stale heads, duplicated passes, and false theorem promotion. Stage any schema migration so old accepted receipts are reconciled explicitly rather than silently invalidated.
- Require an actual nonauthor independent assurance review before closing PAAR-C or final PAAR-E.

## INTELLECT native review rule corrected — 2026-10-16

The native review-count finding above is **historical**: at the original PAAR-C source capture, the INTELLECT ruleset required zero approvals and PR #121 had zero GitHub approvals. Following an explicit operator directive, the authenticated repository administrator changed active INTELLECT ruleset 19964077, Constitutional profile - main, from zero to **one required native approving review**. Live readback from both the ruleset object and effective /rules/branches/main confirmed one; all other ruleset fields, required checks, branch target, and bypass actor list remained unchanged. At latest readback, INTELLECT open PR #86 reported GitHub reviewDecision REVIEW_REQUIRED. The original protected main commit remained d43cdd1b478ad1816ee6c838f8e7500ca11c547f.

This remedies *missing GitHub approval enforcement going forward*, not the distinct execution-evidence weakness PAAR-C01/02. A native approval may come from an appropriately authorized nonauthor GitHub reviewer. A logical same-login reviewer pass cannot count as a native GitHub nonauthor approval. No historic review was fabricated. See machine-readable INTELLECT_REVIEW_RULESET_RECONCILIATION.json, retained pre/post GitHub API digests, and follow-up independently replayed findings before final closure.

A new native-review regression test now exercises six positive/negative fixtures. The existing PAAR live replay has been extended to read INTELLECT's **effective** GitHub branch rules and fail if a native PR approval is no longer required. Its current authenticated readback reported one required review; this only checks the rule at replay time, not continuous drift alerting.

## Scope and effects

This audit modified no protected main branch, worker custody, protected review record, publication status, or certification. A protected PR proposes these evidence artifacts for review. A sandbox consumer test is not evidence of an end-to-end production exploit. Parent GCL-PAAR-001 stays OPEN.
