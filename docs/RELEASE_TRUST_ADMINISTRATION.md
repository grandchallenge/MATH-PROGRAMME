# Release-Trust Administration

## Purpose

Release Trust maintains the admitted repository-protection and publication contract for MATHCERT, MATHSOLVE, MATH-PROGRAMME, and INTELLECT. The original umbrella issues #7 and #125 are historical closure provenance; the same machinery remains the current administration surface for applying and reading back the admitted contract.

The governed contract is `governance/release_trust_admin_contract.json`. The executor is `ci/release_trust_admin.py`. The workflow is `.github/workflows/release-trust-admin.yml`.

MATH-PROGRAMME formal required-context migration is intentionally narrower than a general Release Trust apply. Its governed contract is `governance/programme_formal_context_migration.json` and its executor is `ci/programme_formal_context_migration.py`. That operation may change only the required-status-check context list in ruleset `17137629`; it must preserve every other writable Programme ruleset field exactly.

## Current concurrency policy

Each managed repository currently sets `strict_status_checks: false` in its repository entry. This is deliberate: a mergeable candidate whose material closure remains valid does not need an update-branch synchronization merely because protected `main` advanced.

Required status contexts in the **checked-in contract** remain exact and repository-specific. MATH-PROGRAMME's target Release Trust contract requires `validate-json`, `formal-validation / formal-validation`, `policy / policy`, and `security / action-policy`. The dedicated GH-OS routing rule remains separate. The Programme Release Trust profile also records the admitted Release Trust integration actor exactly as live state requires; it is not inferred from prose or silently deleted during migration.

A checked-in contract is not proof that live GitHub state already matches it. Always read the live ruleset before asserting application. The October 2026 reconciliation retains the October 7 Programme review-gate repair: MATH-PROGRAMME and MATHCERT each require one approval from a non-last-pusher reviewer; MATHSOLVE and INTELLECT retain zero blanket approvals. MATHCERT and MATHSOLVE also require the separately admitted `routing-enforcement` status in their profiles. These are **repository-specific current live controls**, not a return to the pre-repair zero-approval ruleset.

Do not infer the effective strictness or bypass state from the shared `branch_policy` template alone. `ci/release_trust_admin.py` derives the effective repository policy from the repository-specific entry, and the tests require the resulting strictness and bypass map to match that entry exactly.

## Required credential

Use the existing `release-trust` environment with the short-lived Release Trust GitHub App token minted by the workflow. Do not place the token in files, issues, pull requests, workflow inputs, or command lines.

## Execution

For an admitted general contract apply/readback:

1. open **Actions** in MATH-PROGRAMME;
2. select **Release trust administration**;
3. select **Run workflow**;
4. choose `release_trust` and the mode appropriate to the current contract;
5. run from protected `main`.

For the formal-context migration after the routing repair is protected on `main`:

1. confirm ruleset `17137629` still has exactly the six legacy required contexts recorded in `governance/programme_formal_context_migration.json`;
2. confirm ruleset `21969152` remains independently active with `routing-enforcement` and the mandatory merge queue;
3. run **Release trust administration** from protected `main` with operation `programme_formal_context` and mode `apply`;
4. retain `programme-formal-context-migration-evidence.json`;
5. read ruleset `17137629` back independently and require exactly the four target contexts;
6. compare the preservation projection before and after; every writable ruleset field other than the required-context list must be unchanged;
7. only after that readback may the legacy compatibility alias jobs be removed in a follow-up protected change.

A broad general-contract `apply` now checks every live managed ruleset against the approved repository-specific policy **before any write**. If all settings match, it leaves rulesets untouched; only an incorrect repository homepage may be updated. If any ruleset differs, the general operation fails closed and requires a separately admitted, exact-scope ruleset migration. Non-destructive application is routine repository administration under standing delegation. Changing required contexts, strictness, bypass actors, review semantics, or another security-sensitive property is a control-plane change and receives the review/authority required by that material change.

The narrow Programme migration is idempotent at its target state and fails closed if it sees any required-context state other than the exact legacy source or exact target. It does not mutate GH-OS protection, bypass actors, review rules, strictness, merge-queue configuration, or mathematical/certification state.

## Branch policy

The effective admitted policy requires:

- exact repository-specific required status contexts;
- `strict_status_checks: false` for the currently managed repositories;
- changes through pull requests;
- repository-specific approval requirements: one approval for MATHCERT and MATH-PROGRAMME to preserve protected theorem-grade review guards; zero for MATHSOLVE and INTELLECT, as their separate material-boundary controls permit;
- automated non-human routine disposition through a bounded App reviewer where protected and explicitly admitted (e.g., exact MkDocs image-removal canary #1246), without treating a GitHub review as mathematical certification;
- stale-review dismissal and conversation resolution as admitted by the contract;
- no force pushes or branch deletion;
- the admitted bypass-actor state read back exactly rather than inferred from prose.

The dedicated GH-OS routing ruleset is separate from the Programme Release Trust profile. For MATH-PROGRAMME, ruleset `21969152` independently requires `routing-enforcement` with non-strict status policy and no bypass actors. A Programme formal-context migration must not write that ruleset.

Council, Adversary, Formalist, Amanuensis, and Referee records remain available where their material jurisdiction applies. They are not replaced by GitHub account-level approval, and they are not universal routine merge gates.

## Evidence and readback

A Release Trust operation should record enough evidence to establish:

- checked-in contract identity;
- target repositories and branches;
- effective repository-specific strictness and required contexts;
- review and bypass settings;
- exact readback from GitHub;
- publication artifact identity where the Pages contract is being verified;
- workflow/run identity for the administration transaction.

The narrow Programme migration additionally records the exact ruleset id/name, source and target context lists, whether a mutation occurred, and SHA-256 identities of the before/after preservation projection.

Contract conformance is established by live readback, not by intent. A mismatch between checked-in policy and live ruleset is an administrative defect to repair; do not rewrite documentation to pretend it is already applied.

Readback establishes protected administrative state. It does not create mathematical, certification, publication, deployment, or commercial authority.

## Historical umbrella closure

The original administration package discharged umbrella issue #6 through issues #7 and #125 and retained App-backed Release Trust evidence. Those closure instructions are historical. Current maintenance should not replay the umbrella closure ceremony simply because the protection contract is revalidated or re-applied.

## Claim boundary

This procedure governs repository administration and publication identity. It certifies no mathematical claim and does not alter any MATHCERT disposition.

## October 2026 admission-liveness reconciliation

The legacy Release Trust profile formerly set zero GitHub approvals across all four repositories. On 2026-10-07, a **deliberate** Programme review-gate repair (see `governance/mp_main_review_gate_repair_20261007_001.json`) protected against an unreviewed theorem-bearing PR. This reconciliation preserves the live protection instead of blindly reapplying the old profile. The snapshot also includes newer GH-OS required contexts.

Under `GI-STEWARD-0003` and `MP-STREAMLINED-EXECUTION-001`, routine decisions may be discharged by an authorized agent with explicit scope and logical review provenance. Delegation does not waive materially required mathematical, security, constitutional or other specialist review, and an App approval is not independent scientific evidence. Protected [#1248](https://github.com/grandchallenge/MATH-PROGRAMME/pull/1248) demonstrates a real positive routine case and fail-closed negative out-of-scope case. Full generalized class-dependent review routing remains tracked by [#1247](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1247).

Before any future Release Trust apply, compare the current ruleset identities, checks, approval policies, strictness and bypass actors for every repository. Drift outside the exact admitted contract demands an independently governed migration rather than resetting settings from historical documentation.
