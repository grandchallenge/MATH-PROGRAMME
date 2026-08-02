# GCL-DISCLOSE-PR-001 Control Model

## Threat and failure model

- `T-IDENTITY-DRIFT` — A release artifact differs from its reviewed repository, commit, path, blob, or digest.
- `T-MISSING-CLASSIFICATION` — A release lacks an explicit current disposition.
- `T-ACTIVE-HOLD-BYPASS` — An active no-release, patent, legal, confidentiality, contractual, or export hold is ignored.
- `T-STALE-HOLD-AUTHORITY` — An expired or superseded hold is reused as current authority.
- `T-ATTRIBUTION-OMISSION` — Required authors, contributors, or inventor-review fields are absent.
- `T-CLAIM-INFLATION` — Public text exceeds approved claim language.
- `T-UNSUPPORTED-IP-LANGUAGE` — Novelty, priority, inventorship, or patentability language lacks professional review.
- `T-CONFIDENTIAL-EXPORT` — Confidential, customer, credential, or unpublished-invention material enters an export surface.
- `T-REVIEW-MISMATCH` — A review is stale, superseded, author-only, or bound to another head.
- `T-CIRCULAR-RELEASE-AUTHORITY` — A release or generated artifact authorizes itself through a cycle.
- `T-PARTIAL-EVIDENCE-CLEARANCE` — Missing evidence is mistaken for clearance instead of ABSTAIN or FAIL.

## Privacy and confidentiality

Tranche 1 accepts synthetic-public material only. Real confidential material, customer information, credentials, regulated data, and unpublished inventions are prohibited.

## Abstention and recovery

Missing optional evidence produces `ABSTAIN`; malformed, stale, contradictory, required-missing, hold-blocked, or simulated-confidential evidence produces `FAIL`. Partial evidence never becomes implicit release clearance.

## Operator responsibility

- identify the exact proposed release
- supply complete provenance and disposition records
- protect confidential and unpublished material
- obtain professional review where required
- interpret abstentions
- retain final human responsibility

## Professional boundary

CI validates records and identities. It does not determine novelty, patentability, inventorship, legal validity, export eligibility, confidentiality duties, publication merit, or commercial value.
