# GCL-DISCLOSE-PR-001 Synthetic Disclosure Dossier

> Generated deterministically from a synthetic-public fixture. This is not a legal, patent, export, publication, confidentiality, or commercial opinion.

- Proposed release: `SYNTHETIC-RELEASE-001`
- Repository: `synthetic.example/disclosure-demo`
- Candidate head: `2222222222222222222222222222222222222222`
- Overall disposition: `FAIL`
- Counts: PASS `7`, FAIL `10`, ABSTAIN `3`

## Findings

| Finding | Disposition | Reason | Subject | Detail |
|---|---|---|---|---|
| `F-ART-DIGEST` | `FAIL` | `DIGEST_DRIFT` | ART-DIGEST | 2824563a90ce353c2a49ad932f04c8242e02d7ca2f0a1846cf40aa65dc06d19f |
| `F-ART-MISSING` | `ABSTAIN` | `OPTIONAL_EVIDENCE_MISSING` | ART-MISSING | artifacts/optional_prior_disclosure.json |
| `F-ART-NOTE` | `PASS` | `EXACT_ARTIFACT_MATCH` | ART-NOTE | 8c2d9d0d69fc9dbff119927727781905a5112a52623dcf349604b3ce87d55fa7 |
| `F-ART-VALID` | `PASS` | `EXACT_ARTIFACT_MATCH` | ART-VALID | b0c5f1bc49d11934fce324ca9f7f730ca30da662441864f0fbf227f116fbba5b |
| `F-ATTR-COMPLETE` | `PASS` | `ATTRIBUTION_COMPLETE` | ATTR-COMPLETE | complete |
| `F-ATTR-MISSING` | `FAIL` | `ATTRIBUTION_INCOMPLETE` | ATTR-MISSING | incomplete |
| `F-AUTHORITY-GRAPH` | `FAIL` | `CIRCULAR_RELEASE_AUTHORITY` | authority graph | cycle detected |
| `F-CLAIM-APPROVED` | `PASS` | `APPROVED_CLAIM_EXACT` | CLAIM-APPROVED | This synthetic fixture validates identity-bound disclosure records. |
| `F-CLAIM-INFLATED` | `FAIL` | `CLAIM_EXCEEDS_APPROVED_LANGUAGE` | CLAIM-INFLATED | This synthetic fixture validates identity-bound disclosure records and proves universal release safety. |
| `F-CLAIM-NOVELTY` | `FAIL` | `UNSUPPORTED_IP_LANGUAGE` | CLAIM-NOVELTY | first,novel,patentable |
| `F-CLASS-MISSING` | `ABSTAIN` | `CLASSIFICATION_ABSENT` | CLASS-MISSING | no disposition |
| `F-CLASS-VALID` | `PASS` | `ACTIVE_CLASSIFICATION` | CLASS-VALID | open_scientific_infrastructure |
| `F-CONF-LEAK` | `FAIL` | `CONFIDENTIAL_EXPORT_LEAK` | CONF-LEAK | simulated_external |
| `F-CONF-PUBLIC` | `PASS` | `SYNTHETIC_PUBLIC_EXPORT` | CONF-PUBLIC | synthetic_public |
| `F-HOLD-ACTIVE` | `FAIL` | `ACTIVE_NO_RELEASE_HOLD` | HOLD-ACTIVE | no_external_release |
| `F-HOLD-STALE` | `FAIL` | `STALE_HOLD_USED_AS_AUTHORITY` | HOLD-STALE | expired |
| `F-PRIOR-DISCLOSURE` | `ABSTAIN` | `PRIOR_DISCLOSURE_EVIDENCE_MISSING` | prior disclosure | evidence/prior_disclosures.json |
| `F-RELEASE-AUTHOR` | `FAIL` | `AUTHOR_ONLY_RELEASE_AUTHORITY` | REV-RELEASE-AUTHOR | fixture-author |
| `F-REVIEW-EXACT` | `PASS` | `EXACT_NON_AUTHOR_REVIEW` | REV-DISCLOSURE-EXACT | independent-disclosure-reviewer |
| `F-REVIEW-MISMATCH` | `FAIL` | `REVIEW_HEAD_MISMATCH` | REV-DISCLOSURE-MISMATCH | 3333333333333333333333333333333333333333 |

## Unresolved holds

- `HOLD-ACTIVE`

## Unsupported conclusions

- novelty, priority, inventorship, patentability, or freedom to operate
- legal validity, export eligibility, or confidentiality obligations
- publication merit, customer suitability, or commercial value

## Decision boundary

The dossier validates record identity, completeness, consistency, expiry, supersession, claim concordance, and authority only. Professional and Human Steward judgment remains external.
