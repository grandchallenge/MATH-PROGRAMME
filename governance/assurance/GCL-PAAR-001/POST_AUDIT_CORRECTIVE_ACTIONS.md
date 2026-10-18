# GCL-PAAR-001 — finite corrective actions

**Source:** completed [GCL audit #2705](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2705), protected final receipt [PR #2736](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2736), supplemented by [PR #2737](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2737). **This is not another audit or a general remediation programme.** GCL itself is the independent infrastructure-integrity reviewer. Separate verification is applicable only when required for certification or publishing.

## R1 — Future original-execution evidence for material CHAD commands

**Existing owner:** [CONTROL #5](https://github.com/grandchallenge/CONTROL/issues/5), coordinated with the CHAD Commander owner. **Classification:** preventive correction to a proven evidence-capture deficiency, not a claim that current commands are forged. **Status:** IMPLEMENTED, with locally captured command evidence and separately required independent origin for material assertions.

**Finding:** matching recorded October 15 command-output hashes did not authenticate those original executions: the inspected event journal and receipts lack a contemporaneously authenticated link between source, command, output, time and executing service. Original CHAD provenance remains `UNATTESTED`; separate later authenticated GitHub-hosted execution does not retroactively fix it.

**Correction:** for *future material executions that require original-run provenance*, issue a durable authenticated, content-addressed record **at execution time**, binding run ID, UTC start/end, service/runner identity, protected source revision, command digest, exit code, stdout/stderr or output digests, and an immutable retrieval location. Validate this receipt before accepting an `ORIGINAL_EXECUTION_ATTESTED` assertion. Reuse the existing GitHub-hosted attestable runner when it already suffices. Do not require extra GitHub identities for GCL agent roles, new human routine approvals, or signatures minted by the claimant itself.

**Acceptance:** one genuinely executed positive specimen and authenticated consumer replay; negative tests for changed source, command or output, missing/forged runner, duplicate or replayed ID, and post-hoc evidence; fail closed without blocking unrelated valid work. Historical October 15 evidence must remain `UNATTESTED`. Deliver through the **existing CONTROL work**, with one protected source change and exact-head tests rather than another broad initiative.

## R2 — Accepted-publication source/rendered-page comparison

**Existing owner:** [Erdős editorial programme #2552](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2552). **Classification:** publication verification coverage improvement, *not* a presently demonstrated false article. **Status:** IMPLEMENTED and VERIFIED on a real accepted publication via GitHub Actions.

**Finding:** protected-source deployments and particular passages matched live pages, but those specimens cannot establish complete parity for each newly accepted article. Existing `ci/erdos_compendium_public_html_readback.py` checks a specific article (#7), including whether its status is accepted and its maths visibly renders; it is not a reusable per-batch accepted-publication receipt.

**Correction:** extend the existing editorial/publishing check at the **next protected batch acceptance/publishing boundary**. For articles newly marked `ACCEPTED` or promoted to certified publication, bind the approved source digest, protected admission, deploy commit and actual public URL. Compare rendered title, status, substantive text and display equations against approved source; capture a replayable source/deployment/DOM evidence receipt. Explicitly public `UNACCEPTED` drafts remain drafts and do not require theorem certification or per-article independent human reviewers.

**Acceptance:** one actual accepted-and-deployed article with exact-source receipt, and tests that reject stale deployment, swapped accepted/draft banner, changed mathematics, missing/unrendered equations, changed source hash, and broken URL. Failures stay `UNVERIFIED` until corrected; integrate into existing batch governance, not another certification authority. Claim-specific independent certification remains a separate existing publication condition where appropriate.

## Dispositions: no further remediation issue

- **Three branch protections:** fixed and checked in [PR #2729](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2729); standard branch controls continue to guard them.
- **Reject/revise enforcement:** existing validators passed 243 ordinary control tests and 43 audit evidence tests, while seven genuine routing rejections were reproduced in [PR #2737](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2737). These bounded proofs justify preserving the existing guards, **not** inventing an unobserved general rejection failure. Future new claim classes should exercise positive and hostile checks as ordinary change validation.
- **Historical CHAD:** permanent `UNATTESTED` original-execution classification unless authentic contemporaneous evidence is independently found. Never backfill it.
- **Private executive repository:** protected branch and three required checks independently inspected with authorized private access; no remedial defect established. Preserve privacy.
- **Mathematical certification:** audit did not certify theorems. Keep the established independent verification path for publication-grade certification; do not place it on routine internal audit reviews.

## Finite completion boundary

Only R1 and R2 are prospective tasks. Reuse CONTROL #5 and MATH-PROGRAMME #2552 for ownership; create no umbrella issue or additional generic review requirement. Each closes upon authenticated positive and hostile acceptance evidence protected through its existing process, **or** an exact-source determination that existing controls already satisfy the same requirements. The original audit #2705 remains closed. Reassess only on a demonstrated new defect, not merely because the full past history cannot be proved.

## Final bounded implementation readback — October 17, 2026

R1: [CONTROL #32](https://github.com/grandchallenge/CONTROL/pull/32) was protected merged at `d70696e9c17d9bf329eba7966ac74510746c3972`. The live supervised CHAD service is now using this exact release and owner-private records were observed from real commands. All 342 CONTROL tests passed. These records have command, output, timing and exit hashes but remain **LOCAL OS ONLY**, not independent execution attestation. Material claims still require the existing authenticated hosted execution verifier (positive hosted run #38988609732). Historical October 15 provenance remains UNATTESTED.

R2: [MATH-PROGRAMME #2741](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2741) protected merged at `8d4493be38b2d1c7b7999c75f58d51399adfdefd`. The existing public-browser workflow offers an accepted-article check bound to the admitted source, current protected commit and deployed Pages revision. [Actual GitHub-hosted run #39076844379](https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/39076844379) passed on accepted Erdős #99 (six full editorial sections; ten original mathematical expressions and ten rendered MathJax outputs), retaining artifact 12117650433. Twelve hostile/positive tests passed. The existing editorial controller must dispatch this check for future new or amended accepted articles after deployment; the test does not certify theorems or all historical catalogue pages.

**Decision:** Both finite mechanisms are implemented in the bounded form described; their evidence is in POST_AUDIT_REMEDIATION_IMPLEMENTATION_20261017.json. The closed audit is not reopened. Neither mechanism manufactures independent CHAD attestation or a mathematical certificate.
