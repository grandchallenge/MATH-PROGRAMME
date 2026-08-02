# GCL-ASSURE-PR-001 Synthetic Assurance Dossier

> Generated deterministically from a synthetic public fixture. This is not a scientific, legal, security, patent, publication, or commercial certificate.

- Candidate repository: `synthetic.example/research-demo`
- Candidate head: `1111111111111111111111111111111111111111`
- Overall disposition: `FAIL`
- Counts: PASS `6`, FAIL `6`, ABSTAIN `3`

## Findings

| Finding | Disposition | Reason | Subject | Detail |
|---|---|---|---|---|
| `F-ART-DIGEST` | `FAIL` | `DIGEST_DRIFT` | ART-DIGEST | 26611d7016584f41310ac4720480ae3a900295619cabbe8ae224a10005a8cbf8 |
| `F-ART-MISSING` | `ABSTAIN` | `OPTIONAL_EVIDENCE_MISSING` | ART-MISSING | artifacts/optional.json |
| `F-ART-STALE` | `FAIL` | `HEAD_DRIFT` | ART-STALE | 0000000000000000000000000000000000000000 |
| `F-ART-VALID` | `PASS` | `EXACT_ARTIFACT_MATCH` | ART-VALID | 672b5475a38a61ecdbd6afff71a79ec6756929649ce1c50ff9619b6803331ff6 |
| `F-AUTHORITY-GRAPH` | `PASS` | `ACYCLIC_AUTHORITY_GRAPH` | authority graph | 5 |
| `F-CLAIM-C-IDENTITY` | `PASS` | `EVIDENCE_SUPPORTS_BOUNDED_CLAIM` | C-IDENTITY | F-ART-VALID |
| `F-CLAIM-C-NOVELTY` | `ABSTAIN` | `UNSUPPORTED_CONCLUSION` | C-NOVELTY | novelty |
| `F-CLAIM-C-REVIEW` | `FAIL` | `SUPPORTING_EVIDENCE_FAILED` | C-REVIEW | F-REVIEW-STATE |
| `F-CLAIM-C-SCIENCE` | `ABSTAIN` | `UNSUPPORTED_CONCLUSION` | C-SCIENCE | scientific_truth |
| `F-CLAIM-C-WORKFLOW` | `FAIL` | `SUPPORTING_EVIDENCE_FAILED` | C-WORKFLOW | F-WF-FABRICATED |
| `F-POLICY-BOUNDARY` | `PASS` | `GENERIC_POLICY_ONLY` | policy profile | generic_public |
| `F-PRIVACY-BOUNDARY` | `PASS` | `SYNTHETIC_PUBLIC_ONLY` | privacy | synthetic_public |
| `F-REVIEW-STATE` | `FAIL` | `UNRESOLVED_CHANGES_REQUESTED` | reviews | 1 |
| `F-WF-FABRICATED` | `FAIL` | `FABRICATED_WORKFLOW_SUCCESS` | WF-FABRICATED | success lacks exported job evidence |
| `F-WF-VALID` | `PASS` | `EXPORTED_WORKFLOW_SUCCESS` | WF-VALID | 1 |

## Unsupported conclusions

- mathematical or scientific truth
- novelty, priority, patentability, or freedom to operate
- legal or security certification
- product-market fit or commercial readiness

## Decision boundary

The dossier identifies evidence integrity and abstention conditions only. Human experts retain all substantive judgment.
