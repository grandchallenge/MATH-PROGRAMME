# Erdős direct-editorial return → queue projection: governed transaction

Status: IMPLEMENTATION_CANDIDATE; not admitted; no mathematical certification.
Authority: GitHub comment / RESULT/1 = worker evidence; read-only intake = validation; Project #2 Status = operational queue projection; protected Programme records = claim authority.

## Defect and invariant

A returned direct-editorial task must not remain discoverable as AVAILABLE. The authoritative invariant is:
For each catalogue issue with exactly one **current**, structurally valid RESULT/1, the issue must have no `gcl-state:available` label and its unique Project #2 item must have Status=RETURNED. This is an operational receipt, not mathematical adjudication or accepted source semantics.

## Bounded implementation

1. Preserve `erdos-catalogue-intake.yml` as **read-only**. Reuse its `REPORT.json`; do not invent separate parsers or infer dispositions from regex-only comments.
2. A separately governed, idempotent projection controller consumes *current* task/receipt data; checks issue ID, assignment ID, comment identity, current SHA-256, issue pickup labels, Project item uniqueness and status field identity before mutation. A deleted/edited/ambiguous result fails closed; cancellation and reruns must not restore AVAILABLE.
3. Restrict credentials to the job and installation required for Project/issue mutation; the policy exception, if needed, must target exactly this workflow and validate its job-specific permission/absence of broad write. Never weaken global validation.
4. Replay both paths: event wake on new or edited result; periodic whole-catalogue reconciliation after outages. Preserve provenance, errors and independent Project/label readback. Do not automatically mark evidence adjudicated.
5. Protected PR admission follows all mandatory security/policy reviews. Candidate class is operational PROTECTION, not mathematical; this categorization does not supply or bypass an approval.

## Tests and acceptance gates

- Valid #2491 and #2492 are RETURNED; labels not AVAILABLE (already independently verified).
- Positive: one fresh valid RESULT/1 produces one Project/label transition without human re-entry.
- Replay: duplicate dispatch and scheduled reconciliation are idempotent; interrupted Project/issue half-transition heals.
- Hostile: wrong task/issue, deleted comment, edited mismatch, duplicate valid returns, missing/ambiguous Project item or Status, missing credential → no unauthorized transition and explicit failure receipt.
- CI: intake tests, projection tests, GH-OS routing, workflow coverage, security checks and protected material-profile review pass on exact head.
- End condition: PR merged to main under protection; production runner has Project write capability; positive, hostile and replay test evidence is recorded with exact commit and GitHub Actions run references.

## Recovery

If a connected operator cannot inspect Project GraphQL or provision a token, provide one isolated, paste-compatible `gh` transaction, with prerequisite checks and readback. No `set -e` or `exit` in the caller's interactive shell; no broad personal token stored as an Actions secret. The controller must remain blocked rather than claiming live completion without the protected credential.
