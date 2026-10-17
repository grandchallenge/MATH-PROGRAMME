# GCL-PAAR-001 — Fourteen-repository source-to-control mapping and three repairs

**Disposition:** `PAAR-A_SOURCE_TO_CONSUMER_MAP_COMPLETE_14_OF_14`; `PAAR-D_THREE_ORIGINAL_BRANCH_FINDINGS_REMEDIATED`. These results do **not** certify the complete 20-repository estate.

## Exact scope and evidence standard

The source population remains the 20 authenticated pinned default-branch revisions in `ESTATE_SCOPE_20261017.json`, with six original sampled repositories and fourteen additional cases. The 14-repository map contains source/governance/test Git blob pointers, actual workflow dispatch triggers and job IDs from 44 sampled, pinned workflow files, and **live** effective GitHub branch-rule readbacks. A source-mapped producer/consumer **is not** proof of successful execution, correct semantic adjudication, public mirror fidelity or scientific certification. Those controls remain PAAR-B/E obligations in the same existing issue #2705. GCT-EXECUTIVE is private; no private file content was published.

| Repository | Assertion surface | Pinned producer/consumer evidence | Enforced branch gate |
|---|---|---|---|
| `.github` | `ORG_GOVERNANCE_REVIEW_AND_WORKER_CLERKS` | .github/workflows/constitutional-review-tests.yml (`test`) | Protected PR + `policy / policy`, `routing-enforcement`, `security / action-policy` |
| `ADAPTIVE-INTELLIGENCE-ATLAS` | `RESEARCH_MANUSCRIPT_EDITORIAL` | .github/workflows/validate.yml (`validate`) | Protected PR + `validate` |
| `AETHER` | `RESEARCH_SOFTWARE_VALIDATION` | .github/workflows/ci.yml (`scope, rust-pr`) | Protected PR + `Required CI gate`, `Required Supply Chain gate`, `policy / policy` and others |
| `BUTTERFLY` | `RESEARCH_TOOLCHAIN_VALIDATION` | .github/workflows/ci.yml (`quality, governance`) | Protected PR + `governance`, `quality (3.10)`, `quality (3.12)` and others |
| `COMPUTATIONAL-DIFFICULTY-ATLAS` | `MATHEMATICAL_PUBLICATION_AND_EDITORIAL` | .github/workflows/cda-ops-checks.yml (`direct-return-contract`) | Protected PR + `direct-return-contract` |
| `gcl-standards` | `GOVERNANCE_STANDARDS_AND_POLICY_TESTS` | .github/workflows/ci.yml (`standards-policy`) | Protected PR + `policy / policy`, `routing-enforcement`, `security / action-policy` and others |
| `GCT-EXECUTIVE` | `PRIVATE_EXECUTIVE_SOURCE_AND_GOVERNANCE` | Private: only metadata inventoried | Protected PR + `policy / policy`, `routing-enforcement`, `security / action-policy` |
| `GLOSS` | `FORMAL_SOFTWARE_LIBRARY` | .github/workflows/ci.yml (`package-contracts, lean-stable`) | Protected PR + `lean-stable`, `package-contracts`, `policy / policy` and others |
| `GSD` | `RESEARCH_EXPERIMENT_AND_EVALUATOR` | .github/workflows/ci.yml (`unit`) | Protected PR + `unit` |
| `lean-action` | `REUSABLE_PROOF_BUILD_ACTION` | .github/workflows/gcl-conformance.yml (`policy, security`) | Protected PR + `policy / policy`, `routing-enforcement`, `security / action-policy` |
| `MODULUS` | `RESEARCH_SOFTWARE_TESTS` | .github/workflows/ci.yml (`test-and-lint, benchmark-report`) | Protected PR + `benchmark-report`, `policy / policy`, `routing-enforcement` and others |
| `QUANTUM-TECHNOLOGIES` | `RESEARCH_SCIENTIFIC_PROGRAMMES` | .github/workflows/gcl-conformance.yml (`policy, security`) | Protected PR + `policy`, `routing-enforcement`, `security / action-policy` and others |
| `TROVE-CURATA` | `EDITORIAL_CURATION_AND_ACCEPTANCE` | .github/workflows/ci.yml (`acceptance`) | Protected PR + `acceptance (3.11.14)`, `acceptance (3.12.13)`, `policy / policy` and others |
| `upload-pages-artifact` | `REUSABLE_PUBLICATION_ACTION` | .github/workflows/gcl-conformance.yml (`policy, security`) | Protected PR + `policy / policy`, `routing-enforcement`, `security / action-policy` |

The table cites only representative pinned routes; the machine-readable map contains all 44 sampled workflow blobs, triggers, job names, mapped governance and test blobs, full required-check arrays, and current/pinned revision differences. Each repository is tagged `PINNED_PRODUCER_AND_WORKFLOW_CONSUMER_IDENTIFIED` and **not** `SEMANTIC_ENFORCEMENT_PASS`. Private repository contents are not re-published.

## Completed three branch-rule corrections

The initial negative capture showed no effective `main` branch controls in three research repositories. Authenticated repository admin settings were changed under the explicit operator directive to address the findings. All three were read back from both `/branches/main` and `/rules/branches/main`.

| Repository | Ruleset ID | Required check | CI coverage and evidence |
|---|---:|---|---|
| `ADAPTIVE-INTELLIGENCE-ATLAS` | `25299675` | `validate` | Existing unconditional `validate` workflow; successful main check observed |
| `COMPUTATIONAL-DIFFICULTY-ATLAS` | `25299676` | `direct-return-contract` | PR #53 merged at `d85c4bc1386d37434e1f297e7e5f3218d92e4460`; actual check `direct-return-contract` success ID `117377738166` |
| `GSD` | `25299668` | `unit` | PR #2 merged at `8cdb3377ab6686a0f192dd2346ba12442f3d3601`; actual check `unit` success ID `117377732298` |

Each ruleset actively enforces pull-request merges with **zero blanket approving reviews**, no bypass actors, no force-push, no deletion, and an actual required CI context. The agent-first review doctrine is preserved: domain-specific independent review still applies to substantive mathematical/protection promotions. For GSD and the Computational Difficulty Atlas, earlier workflow path filters were removed through **protected PRs** before the check was made universally required; no intentionally absent check was installed. All three latest protected branch SHAs were read back and included in the receipt.

**Important boundary:** checks validate their code-specific contracts, not all mathematical claims or public deployments. The audit neither rewrites historical direct pushes nor retroactively approves old manuscripts. The three originally identified PAAR-D branch configuration exceptions are resolved; broader life-cycle and mirror checks remain in the unchanged existing parent PAAR register.

## Reproduce

`python3 governance/assurance/GCL-PAAR-001/complete_14_control_map.py` retrieves live GitHub branch and workflow metadata against the pinned source map. A new run may legitimately see later protected commits and should be saved under a distinct timestamp rather than overwriting this snapshot. `python3 governance/assurance/GCL-PAAR-001/verify_branch_control_repairs.py` re-reads all three active rulesets, their effective branch rules, protected merges and passing exact-head job checks. `python3 -m unittest -q tests.test_paar_control_mapping` tests the protected JSON evidence structure and mutation rejection.
