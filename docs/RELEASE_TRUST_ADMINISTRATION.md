# Release-Trust Administration

## Purpose

Release Trust maintains the admitted repository-protection and publication contract for MATHCERT, MATHSOLVE, MATH-PROGRAMME, and INTELLECT. The original umbrella issues #7 and #125 are historical closure provenance; the same machinery remains the current administration surface for applying and reading back the admitted contract.

The governed contract is `governance/release_trust_admin_contract.json`. The executor is `ci/release_trust_admin.py`. The workflow is `.github/workflows/release-trust-admin.yml`.

## Current concurrency policy

Each managed repository currently sets `strict_status_checks: false` in its repository entry. This is deliberate: a mergeable candidate whose material closure remains valid does not need an update-branch synchronization merely because protected `main` advanced.

Required status contexts remain exact and repository-specific. In particular, INTELLECT's current Release Trust profile includes `routing-enforcement`. GitHub account-level required approvals remain zero; review-thread resolution and the other admitted protection rules remain enforced.

Do not infer the effective strictness from the shared `branch_policy` template alone. `ci/release_trust_admin.py` derives the effective repository policy by applying the repository-specific entry, and the tests require the resulting strictness to be false for every managed repository.

## Required credential

Use the existing `release-trust` environment secret `GCL_REPOSITORY_ADMIN_TOKEN` with the minimum repository permissions required by the workflow. Do not place the token in files, issues, pull requests, workflow inputs, or command lines.

## Execution

For an admitted contract apply/readback:

1. open **Actions** in MATH-PROGRAMME;
2. select **Release trust administration**;
3. select **Run workflow**;
4. use the workflow mode appropriate to the current contract (`validate` for read-only verification or `apply` for an authorized application);
5. run from protected `main`.

Applying the already-admitted contract is routine repository administration under standing delegation. Changing required contexts, strictness, bypass actors, review semantics, or another security-sensitive protection property is a separate control-plane change and receives the review/authority required by that material change.

The workflow validates the checked-in contract, applies authorized settings when requested, reads settings back through GitHub, verifies current required contexts and repository policy, verifies publication identity where applicable, and emits retained Release Trust evidence. Historical issue-closing behavior remains part of the original umbrella closure; do not treat it as a requirement to reopen or recreate closed historical trackers.

## Branch policy

The effective managed policy requires:

- exact repository-specific required status contexts;
- `strict_status_checks: false` for the currently managed repositories;
- changes through pull requests;
- zero mandatory GitHub approvals, avoiding routine single-operator approval deadlock;
- stale-review dismissal and conversation resolution as admitted by the contract;
- no force pushes or branch deletion;
- the admitted bypass-actor state read back exactly rather than inferred from prose.

The dedicated GH-OS routing ruleset is separate from the Programme Release Trust profile. For MATH-PROGRAMME, ruleset `21969152` independently requires `routing-enforcement` with non-strict status policy and no bypass actors. For INTELLECT, `routing-enforcement` is included in the Release Trust required-context set.

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

Readback establishes protected administrative state. It does not create a second Human Steward or independent-review cycle.

## Historical umbrella closure

The original administration package discharged umbrella issue #6 through issues #7 and #125 and retained App-backed Release Trust evidence. Those closure instructions are historical. Current maintenance should not replay the umbrella closure ceremony simply because the protection contract is revalidated or re-applied.

## Claim boundary

This procedure governs repository administration and publication identity. It certifies no mathematical claim and does not alter any MATHCERT disposition.
