# Erdős Compendium: complete catalogue coverage audit

**Audit date:** 2026-10-14 UTC  
**Canonical registry:** `governance/erdos_catalogue/REGISTRY.json` (Git blob `90f6499cfbaca8c8a9e1ac4c6beb468ca09127a5`)  
**Protected main observed:** `5bed6a96a49eead42de14ef7a6147dd0439dff3a`

## Findings

The canonical register has 1,221 unique consecutive problem IDs, #1–#1221. The seven cohort registers collectively assign 1,218 distinct IDs. Legacy explanatory entries #1–#3 account for the remaining three. **No assignment gaps, duplicates, unregistered IDs, canonical issue-number mismatches, source-return URL mismatches, or available issue-body hash discrepancies** were found in the checked manifests. All seven manifests use the same canonical registry Git blob.

This is an **assignment coverage audit**, not an assertion that 1,221 explanatory manuscripts or mathematical proofs have been completed. Only EC-BULK-001, -002, and -003 have cohort manifests in protected `main`. The other four manifests were examined on their active GitHub branches.

## Cohort evidence by checked revision

| Owner | Exact assignments | Manifest ref | Source returns | Manuscript files | Protected editorial admissions |
| --- | ---: | --- | ---: | ---: | ---: |
| EC-BULK-001 | 50 | main | 50 | 50 | 50 |
| EC-BULK-002 | 200 | active draft PR #2612 | 108 | 108 | 0 |
| EC-BULK-003 | 200 | main | 200 | 200 | 200 |
| EC-BULK-004 | 200 | editorial/ec-bulk-004-200 | 29 | 19 | 0 |
| EC-BULK-005 | 200 | editorial/ec-bulk-005-200 | 122 | 123 | 0 |
| EC-BULK-006 | 200 | editorial/ec-bulk-006-200 | 26 | 26 | 0 |
| EC-BULK-007 | 168 | editorial/ec-bulk-007-168 | 53 | 53 | 0 |
| Legacy #1–#3 | 3 | main | not assessed | 3 | 0 |
| **Total** | **1,221** | mixed | **588 cohort returns** | **582** | **250** |

These are revision-specific observations, not live progress gauges. EC-BULK-002 has only nine source returns and nine manuscripts on protected main; the 108/108 figures above come from its *draft* PR #2612 branch and must not be added to the nine. Source-return links do not by themselves confer correctness, complete source fidelity, or editorial admission. A manuscript file can exist without a matching completed return. **639** registered entries did not have a manuscript at the checked revisions. The 250 editorial admissions are documentary, not mathematical certifications.

**Branch commit pins:** EC-BULK-002 `38beaaba5d53d6cfda7e0179a50ac3b31624cec5`; EC-BULK-004 `847dd3b12d0e524ce879a0064259eedec01fe6cd`; EC-BULK-005 `699d0cc0243d2c964c718caab5d9d2c5ea4aff0e`; EC-BULK-006 `d48c7440f0c8cde105856d83f6f45810a8ad5eb7`; EC-BULK-007 `906fab4b84d35c82bbd53223d4a9673f27b97f95`.

## Canonical ownership partition

- EC-BULK-001: #4–#41 plus #99, #101, #138, #241, #390, #470, #522, #550, #593, #595, #1052 and #1112.
- EC-BULK-002: #42–#245 excluding #99, #101, #138 and #241.
- EC-BULK-003: #246–#446 excluding #390.
- EC-BULK-004: #447–#651 excluding #470, #522, #550, #593 and #595.
- EC-BULK-005: #652–#851.
- EC-BULK-006: #852–#1051.
- EC-BULK-007: #1053–#1221 excluding #1112.
- Legacy: #1–#3.

## CI and protected-admission policy

The companion test `test_full_1221_catalogue_ownership` in `ci/test_erdos_compendium_publication_gate.py` runs within the normal protected CI workflow. It locks the full 1,221-entry canonical partition and checks any cohort manifest present on main for issue identity, exact membership, source blob, and duplicate membership. While 004–007 remain branch-staged, the test records only their *reserved partition* rather than asserting their manifests or articles are protected-merged. Once these manifests enter main, they are validated automatically.

No editorial return, manuscript, cohort register, admission ledger, or proof-status authority was changed by this audit.

## Remaining production and admission obligations

Complete the pending 639 manuscript slots, source investigations and source-fidelity repairs; reconcile active branch work into protected main; perform editorial QA and full rendered-MathJax website checks; and admit verified articles in protected batches. Keep historic proof claims distinct from GCL mathematical certification.
