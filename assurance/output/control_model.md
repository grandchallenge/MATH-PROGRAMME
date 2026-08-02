# GCL-ASSURE-PR-001 Control Model

## Threat and failure model

- `T-HEAD-DRIFT` — Evidence belongs to a different candidate head.
- `T-DIGEST-DRIFT` — Artifact bytes differ from the declared digest.
- `T-REVIEW-MISMATCH` — Review state is stale, contradictory, author-only, or unresolved.
- `T-MISSING-EVIDENCE` — Required or optional evidence is absent; the evaluator fails or abstains explicitly.
- `T-FABRICATED-WORKFLOW` — A success label lacks exported job evidence.
- `T-CIRCULAR-AUTHORITY` — Generated output is used to authorize itself or an authority graph contains a cycle.
- `T-POLICY-LEAKAGE` — GCL-private policy or institutional content enters the generic core.
- `T-UNSUPPORTED-PROMOTION` — Evidence-integrity findings are promoted into truth, novelty, legal, security, or commercial conclusions.

## Privacy and confidentiality

Tranche 1 accepts synthetic or expressly public material only. Credentials, personal data, customer secrets, unpublished inventions, and regulated data are prohibited.

## Abstention and recovery

Missing optional evidence produces `ABSTAIN`; malformed, stale, contradictory, fabricated, or required-missing evidence produces `FAIL`. Partial evidence never becomes implicit PASS.

## Operator responsibility

- identify the candidate head
- supply complete exported evidence
- protect secrets and confidential material
- interpret abstentions
- retain expert responsibility

## Claim boundary

No output determines scientific truth, novelty, patentability, legal compliance, security certification, publication authority, product-market fit, or commercial readiness.
