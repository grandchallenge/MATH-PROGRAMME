# PAAR-001 — Second-pass exact-source reconciliation (2026-10-17)

**Parent:** MATH-PROGRAMME #2705. This is an evidence tranche under the existing finite closure register, not a new audit programme. Status remains **PARTIAL**; do not certify GCL-wide invariants.

## PAAR-A: fourteen previously unmapped repository sources

`ESTATE_CONTRACT_SOURCES_20261017.json` identifies the remaining **14/14** repositories at the exact heads in `ESTATE_SCOPE_20261017.json`. Each public repository has immutable Git blob identifiers for selected governance/test sources and parsed workflow job IDs, triggering events, path filters, and actual declared commands. **This is source-level contract discovery, not a proof that checks ran, are required by branch rules, cover every assertion, or govern public claims.** Up to four representative workflows per repository were parsed; repositories with more are explicitly not exhaustively workflow-mapped. The GCT-EXECUTIVE private repository is represented by aggregate counts only, with no internal source paths or content disclosed in the public report. Its contract must be verified within the authorized private domain before PAAR-A can be closed.

Replay using `map_estate_contracts.py` with partitions `0 3`, `3 6`, `6 9`, `9 12`, `12 14`, then `combine_source_map.py`. All reads use GitHub's immutable `/git/trees/{head}` and `/git/blobs/{sha}` endpoints; the script checks each Git blob SHA. The five intermediate shard files are reproducible output, not required protected inputs.

## PAAR-B: actual, narrow positive execution witnesses

`RESEARCH_RUN_WITNESSES_20261017.json` binds three **actual successful** GitHub Actions runs to the exact pinned repository heads, with GitHub job and step conclusions:

| Repository | Original Actions run | Scope |
|---|---:|---|
| ADAPTIVE-INTELLIGENCE-ATLAS | 39008087687 | Scheduled direct editorial return replay at pinned head |
| COMPUTATIONAL-DIFFICULTY-ATLAS | 39020937362 | Scheduled direct editorial return replay at pinned head |
| GSD | 37856762182 | Push-triggered evaluator tests at pinned head |

These observations prove that the named workflow jobs ran successfully at those commits. They do **not** prove that branch protection required the jobs, that scientific assertions were independently admitted, or that public status mirrors reconcile. The source-level and run-level evidence remain separately typed.

## PAAR-D: three verified protection exceptions and one CI trigger defect

`BRANCH_PROTECTION_EXCEPTIONS_20261017.json` records authenticated readback for ADAPTIVE-INTELLIGENCE-ATLAS, COMPUTATIONAL-DIFFICULTY-ATLAS and GSD: branch `protected=false`, effective GitHub branch rules `[]`, and legacy branch-protection endpoint HTTP 404 for each. These are actual **missing enforced GitHub main-branch controls**, not merely undocumented policy. There is no observed unauthorized merge or false mathematical admission. Disposition requires existing governance to determine whether each research repository should require protected review/status checks or a precisely bounded approved exception. The audit did not mutate any ruleset.

**Reproduced GSD workflow defect:** at pinned GSD head `da7ddadc9743c14549e5132e8fc98b66d5223de6`, actual workflow `.github/workflows/ci.yml` filters `pull_request` and `push` paths for `.github/workflows/gsd-ci.yml` (which is not the workflow filename) and `experiments/gsd-001/**`. Consequently, a change to `.github/workflows/ci.yml` alone is excluded by its own declared path filters. The exact-source negative test in `tests/test_paar_contract_source_map.py` reproduces this discrepancy. The minimal proposed correction is to replace those two references with `.github/workflows/ci.yml` through a normal GSD PR. This is a workflow-trigger defect, not proof of incorrect research results.

## Assurance status and next finite gates

The second pass improves **PAAR-A source discovery** and **PAAR-B sampled real execution**, and produces exact evidence for **PAAR-D governance disposition**. PAAR-A's actual assertion producer-to-consumer mappings, PAAR-B's positive/negative lifecycle-to-public-mirror replay across material classes, the private domain's internal verification, and PAAR-E independent final report/receipt are still required. No historical October 15 CHAD execution has been retroactively authenticated. Do not close #2705 on these observations alone.

Run `python3 -m unittest -v tests.test_paar_contract_source_map tests.test_paar_estate_scope` for positive and adversarial offline validation. Re-run read-only live collectors against current GitHub APIs to detect head or branch-policy drift; preserve this original immutable observation as a historical checkpoint.
