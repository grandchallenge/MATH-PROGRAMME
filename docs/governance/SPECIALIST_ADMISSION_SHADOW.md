# Specialist material admission: protected shadow controller

**Control:** `GCL-AGENT-ADMISSION-SPECIALIST-001`  
**Work package:** [MATH-PROGRAMME #1251](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1251)  
**Current authority:** OBSERVE_ONLY_NOT_REQUIRED.

The shadow controller reads the live pull request or GitHub-native merge group,
classifies actual changed bytes/paths against the protected bounded-routine
registry, and writes a structured nonauthoritative artifact. It never posts a
GitHub approval, publishes an admission status, certifies a mathematical
statement, modifies a protected branch, or claims that external specialist
evidence exists.

On `pull_request_target`, it reads the current PR file manifest, pins its exact
head/base GitHub objects and routes the full file bytes through the protected
routine classifier. Files/bytes/metadata outside the admitted scope become
`SPECIALIST_REVIEW_PENDING` or `RESERVED_OR_CONTROL_PLANE_PENDING`, not
`ROUTINE_CANDIDATE_ONLY`.

On `merge_group: checks_requested`, it requires the GitHub-owned queue ref and
head SHA to agree with the event, checks the current protected `main`
ancestry, obtains the queue ref without checking out or executing candidate
code, inspects the effective diff, and fails closed if protected `main`
moves during a positive routine decision.

`ROUTINE_CANDIDATE_ONLY` is an *observation* about the changed material, not
permission to merge or proof of scientific correctness. It cannot substitute
for a GitHub App review, actual specialist evidence, a required status, or a
protected merge queue's own decision.

## Protected-domain review evidence (candidate read-only adapter)

`ci/specialist_receipt_adapter.py` now implements a fail-closed readback
for a future protected specialist-review route. It recognizes *only* a receipt
already present on a domain-authorized protected `main`: MATHCERT for
mathematical review, MATHFORGE for source-semantic review, and INTELLECT for
protection/authority review. The deterministic receipt path is

`governance/material_admission_receipts/MATH-PROGRAMME-<exact-subject-head>.json`.

A valid envelope must assert the precise subject Git commit and canonical
complete changed-file fingerprint, positive protected-admission disposition,
named review scope, and exact Git blob of a separate domain-owned source
document. Both receipt and underlying evidence are fetched from pinned
protected repository commits; the protected source must remain unchanged
throughout the operation. The adapter never reads a candidate-supplied
`GCL-REVIEW/1` comment as review authority. GitHub review statuses alone
are not proof of the domain record.

The positive unit fixtures exercise the *adapter's* identity checks, **not**
an actual protected mathematical certificate. There are currently no
new protected domain receipts granted by this code. Even when a valid receipt
is observed, the shadow mode returns an explicitly nonauthoritative
`SPECIALIST_EVIDENCE_RECOGNIZED_SHADOW` finding. Domain-issued admission
depends upon the original domain's protected certification/review process.

This model is intentionally exact-head rather than general evidence-closure
equivalence. Accepting an exact material closure across independent base
commits will require a separately reviewed normalization/identity migration;
it must never be inferred from a SHA coincidence or PR comment.

## Evidence still missing for enforcement

An authoritative specialist-evidence adapter must independently verify
source, role, exact material closure and promotion boundary from already
protected Forge/Solve/Cert/INTELLECT/Council records, rather than a comment
by the candidate. It must distinguish appropriate logical agent passes from
truly independent domain certification where required.

Before `material-admission` becomes a mandatory ruleset context, demonstrate
real positive and hostile cases, the candidate-independent controller bytes,
merge-group status publication against the queue SHA, and a safe way for
legitimately reviewed existing substantive PRs to proceed.

Never change security-sensitive branch ruleset `17137629` or dedicated
GH-OS merge-queue ruleset `21969152` under a routine shadow transaction.
The governed, exact-scope migration with preservation readback is WP-E of
issue #1251.

The source-of-truth work index remains the issue and protected repository.
MkDocs is this explanatory read model, not an independent source of claim
authority.
