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
already present on a domain-authorized protected `main`: MATHFORGE for
source-semantic review, MATHSOLVE for execution/replay/adjudication integrity,
MATHCERT for independent mathematical proof review, and INTELLECT for
protection/authority review. This four-domain registry lives at
`governance/specialist_admission_domains.json` and is checked against a
bounded protected-controller code contract. A change to the registry alone
cannot expand App review authority. The deterministic receipt path is

`governance/material_admission_receipts/MATH-PROGRAMME-<exact-subject-head>.json`.

A valid envelope must assert the precise subject Git commit and canonical
complete changed-file fingerprint, positive protected-admission disposition,
named review scope, and exact Git blob of a separate domain-owned source
document. Both receipt and underlying evidence are fetched from pinned
protected repository commits; the protected source must remain unchanged
throughout the operation. The underlying evidence must additionally anchor an
actual merged PR in the domain repository. The adapter reads the source PR,
verifies the exact reviewed head, the precise underlying evidence blob in that
PR, a real non-author GitHub `APPROVED` review with the declared review ID,
and that no later reviewer disposition supersedes the approval. The role and
independence assertions are checked against this attributable GitHub review
and exact protected bytes; GitHub approval alone still cannot certify a theorem.
The read token has domain-only contents and pull-request read permissions.
The adapter never reads a candidate-supplied
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

## MATHSOLVE — solution and execution integrity only

MATHSOLVE is now an explicitly recognized specialist domain:
`SOLUTION_INTEGRITY`, protected owner `grandchallenge/MATHSOLVE`, and
evidence confined to `contributions/` on the owning repository's protected
`main`. Its role is **to test whether a provisional returned result was
captured faithfully, reproduced, and adjudicated on the recorded evidence**.
It does *not* verify mathematical truth by itself.

The new Solve-scoped review record type is
`GCL_DOMAIN_ROLE_SCOPED_REVIEW_V1`, with positive disposition
`ROLE_SCOPED_REVIEW_ACCEPTED` and
`ROLE_SCOPED_NON_AUTHOR_SPECIALIST` independence declaration. This is not
relabelled as a MATHCERT-independent theorem review. An authenticated
non-author GitHub review of the exact evidence PR remains necessary for the
specialist evidence packet, but not for ordinary MATHSOLVE maintenance.

The Solve proof record and admission receipt must refer to the *same*
`solve_execution` source-locked record. That record binds dispatch ID,
result reference and SHA-256, plus exact blobs of three distinct, already
protected JSON artifacts:

1. `GCL_SOLVE_CAPTURE_RECEIPT_V1` — captured result digest.
2. `GCL_SOLVE_REPLAY_RECEIPT_V1` — passed replay of that captured digest.
3. `GCL_SOLVE_ADJUDICATION_RECEIPT_V1` — adjudicated replay, with exact
   replay-blob and dispatch/result lineage.

Every artifact is fetched from protected MATHSOLVE and checked against
its Git blob SHA and the other links in the chain. Missing, ambiguous,
negative, stale, or cross-campaign evidence fails closed. The following
claim effects are **all false** in both the Solve binding and adjudication:
mathematical claim promotion, certification, publication, source-semantic
adjudication, and security authority expansion.

For now the protected Programme routing surface for MATHSOLVE is deliberately
narrow: `governance/mathsolve_*`, `governance/solve_execution_*`, and
`governance/solution_integrity_*`. A source theorem in a Lean file still
routes to MATHCERT; workflow, admission-controller, and protection changes
still route to INTELLECT. Mixed or unknown scopes remain unadmitted. This
registration **does not** install a required `material-admission` status
or bypass existing protection. A real domain-produced protected positive
receipt and PR/merge-group replay remain necessary before enforcement.

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
