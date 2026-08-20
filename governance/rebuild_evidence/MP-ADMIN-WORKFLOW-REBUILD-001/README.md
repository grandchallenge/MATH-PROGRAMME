# MP-ADMIN-WORKFLOW-REBUILD-EVIDENCE-001

This directory is the durable, in-repository evidence package for the 2026-08-20 administrative workflow rebuild. It converts the previously distributed proof into a single protected, machine-checkable record.

## What is proved

The evidence proves an operational control-plane statement only: the rebuilt administrative remediation admission path successfully executed exact-head validation, separated Referee disposition, separated Candidate expected-head protected merge, and automatic post-merge qualification without a manual/bootstrap merge or intermediate Human Steward action. A subsequent real protected reactivation transition traversed the same rebuilt admission path successfully.

The package does **not** create or imply mathematical, certification, publication, product, receipt, ledger, mirror, bypass, direct-push, ruleset-widening, cadence, or other substantive authority.

## Proof chain

1. **Steady-state self-test — PR #626**
   - exact head `e40f8ba7c39bf469498a9db0429d368ed24993e7`;
   - Referee `github-actions[bot]`, comment `5353413444`;
   - admission run `32349157243`, comment `5353414322`, state `REMEDIATION_PR_PROTECTED_MERGE_COMPLETE`;
   - Candidate `gcl-release-trust[bot]`;
   - signed protected merge `ce370735fa05fb55b5e38c19870ff23c91578110`;
   - automatic qualification run `32349281060`: `LIVE_QUALIFICATION_GREEN__REACTIVATION_NOT_AUTHORIZED`.

2. **Real protected transition — PR #627**
   - exact head `f0a6c92aecf35c40e32c2044c7bd9d0e1ef68fb2`;
   - Referee `github-actions[bot]`, comment `5353633935`;
   - admission run `32350965910`, comment `5353634806`, state `REMEDIATION_PR_PROTECTED_MERGE_COMPLETE`;
   - Candidate `gcl-release-trust[bot]`;
   - signed protected merge `e052be7f100976d25694019b55dfafc0a3bec954`;
   - automatic qualification run `32351044135`: `LIVE_QUALIFICATION_GREEN__REACTIVATION_NOT_AUTHORIZED`.

## Retained Actions payloads

The original Actions artifacts expire. Their two JSON payloads are therefore preserved verbatim here for both the pre-reactivation self-test and post-reactivation confirmation. `attestation.json` records the original archive digests and SHA-256 hashes of each retained payload.

Run `python ci/validate_administrative_workflow_rebuild_attestation.py` to validate the schema, hashes, cross-record identities, exact heads, actor separation, qualification states, and authority boundaries. The ordinary administrative automation validator invokes the same validation, so future drift fails CI.
