# GCL-TCS-00 machine-contract migration note — 0.1.0-r1

**Operation:** `GCL-TCS-CANDIDATE-HARDENING-004`  
**Tracker:** `grandchallenge/MATH-PROGRAMME#814`  
**Normative standard:** `GCL-TCS-00/0.1.0` (`candidate`)  
**Machine-contract revision:** `0.1.0-r1`

## Purpose

This is a candidate-standard machine-contract correction. It reconciles machine-readable policy, schemas, templates, and validation surfaces with obligations that already exist in the protected `GCL-TCS-00/0.1.0` normative source.

It does not change the seven ordered normative Markdown parts, their assembled SHA-256, the candidate's constitutional meaning, or any claim/promotion/publication authority.

## Normative source binding

The controlling source remains the seven ordered files in `council_submissions/GCL-TCS-00/parts/`.

Assembled SHA-256:

`ea750b9b80b53c7d6ed755978fa4bdf59413fad93cec1db81eb3238372ce61c9`

If a machine representation disagrees with those source bytes, the source controls and the machine surface is nonconforming.

## Corrections

Revision `0.1.0-r1`:

1. binds the current policy back to the ordered source parts and assembled digest;
2. explicitly represents hard conformance, claim/evidence/review/exception, language/structure, gate, review-separation, promotion, and change-control obligations that were previously partial or implicit;
3. tightens the conformance declaration schema so the charter and profile identifiers are version-locked to `0.1.0`;
4. adds `gcl-tcs-record-contracts.schema.json` for normative claim, evidence, review, exception, gate, conformance-statement, and release record bodies;
5. supplies machine-readable candidate templates for the conformance declaration and governed record bodies;
6. adds a source-bound reconciliation matrix and fail-closed agreement validation.

## Compatibility

This correction is intended to be backward compatible with conforming `GCL-TCS-00/0.1.0` artifacts. It adds validation coverage for obligations already present in the candidate charter. It does not add a new normative requirement, authority state, gate, profile, promotion behavior, or exception permission.

An artifact that depended on an omitted or under-specified machine field may newly fail validation. That is defect detection, not a new substantive obligation.

## Historical record boundary

`docs/council/submissions/SUBMISSION_MANIFEST.yaml` remains the historical, hash-locked record of the originally issued candidate review/admission package. This successor hardening does not rewrite that transaction. Historical hashes identify those original bytes at their historical revision.

The current candidate machine contract is bound by this migration note, issue #814, the reconciliation matrix, exact-head CI, and the eventual protected merge identity.

## Promotion boundary

No version-1.0 promotion is requested or implied. Criterion-1 readiness can be satisfied without satisfying criterion 10. `GCL-TCS-00` remains candidate `0.1.0`.
