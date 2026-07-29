# Release-Trust Administration

## Purpose

This package discharges the two remaining administration obligations under umbrella issue #6:

- issue #7: repository homepage and current-main Pages verification;
- issue #125: protected-branch enforcement across MATHCERT, MATHSOLVE, MATH-PROGRAMME, and INTELLECT.

The governed contract is `governance/release_trust_admin_contract.json`. The executor is `ci/release_trust_admin.py`. The workflow is `.github/workflows/release-trust-admin.yml`.

## Required credential

Create a fine-grained GitHub personal access token or GitHub App installation token with access only to:

- `grandchallenge/MATHCERT`;
- `grandchallenge/MATHSOLVE`;
- `grandchallenge/MATH-PROGRAMME`;
- `grandchallenge/INTELLECT`.

Required repository permissions are:

- Administration: read and write;
- Actions: read;
- Issues: read and write;
- Metadata: read.

Do not put the token in a file, issue, pull request, workflow input, or command line. Add it to the MATH-PROGRAMME `release-trust` environment as the secret `GCL_REPOSITORY_ADMIN_TOKEN`.

## Execution

1. Open **Actions** in MATH-PROGRAMME.
2. Select **Release trust administration**.
3. Select **Run workflow**.
4. Use `mode: apply`.
5. Keep `close_child_issues: true`.
6. Run the workflow from `main`.

The workflow:

1. sets the MATH-PROGRAMME homepage;
2. applies the exact protected-branch contract to all four repositories;
3. reads every setting back through the GitHub API;
4. requires strict required checks and pull-request-only changes;
5. requires admin enforcement and resolved review conversations;
6. rejects force pushes, branch deletion, and bypass actors;
7. locates successful policy and Pages runs for current `main`;
8. downloads and verifies the `validated-site` artifact;
9. verifies the inner archive checksum;
10. compares the live Pages `index.html` byte-for-byte with the policy artifact;
11. uploads `release-trust-evidence.json` for 90 days;
12. closes issues #7 and #125 only after all checks pass.

The workflow does not close umbrella issue #6.

## Branch policy

The branch contract requires:

- exact required status-check contexts;
- strict, up-to-date status checks;
- changes through pull requests;
- zero mandatory GitHub approvals, to avoid a single-operator approval deadlock;
- stale-review dismissal enabled;
- conversation resolution required;
- administrators governed by the same rule;
- no bypass actors;
- no force pushes;
- no branch deletion.

Council, Adversary, Formalist, Amanuensis, and Referee review remain governed repository artifacts. They are not replaced by GitHub account-level approval.

## Final closure

After issues #7 and #125 close:

1. download the `release-trust-evidence` workflow artifact;
2. admit its exact workflow run, artifact identity, and SHA-256 into the umbrella audit;
3. set `administrative_children_complete: true`;
4. set `operational_release_complete: true`;
5. set `operational_release_closure: COMPLETE`;
6. remove all remaining blockers;
7. run exact-head Programme policy CI;
8. merge the audit;
9. close issue #6.

## Claim boundary

This procedure governs repository administration and publication identity. It certifies no mathematical claim and does not alter any MATHCERT disposition.
