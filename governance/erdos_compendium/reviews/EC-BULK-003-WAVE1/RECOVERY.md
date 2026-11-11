# EC-BULK-003 wave-one critical review: archival custody

**State:** HISTORICAL_REVIEW_ONLY. This record does not admit, certify, or publish a manuscript.

## Scope

This package preserves four original editorial-worker reviews for Erdős problems 246–265, their historical reconciliation note, their reviewed-manuscript hash list, and an arithmetic erratum. The historical review summary records 12 PASS, seven REQUEST_CHANGES, and one SOURCE_BLOCKED verdict. These are worker review judgments about historical manuscript versions, not current protected editorial acceptance or mathematical certification.

The reports are preserved byte-for-byte as `worker-review-*.md.txt`, rather than modified into compliant mathematical Markdown. This maintains the original evidence. Some reports contain legacy mathematical delimiters and absolute paths to historical worker worktrees. Such paths are historical provenance, not working public links. The machine-readable file hashes and original names are in `custody-manifest.json`.

## Chronology and current-state boundary

The historical reconciliation note records protected head `229aa4e20c1a8a273e81a747aea4df0e318a6a29` and a then-observed count of 41 source returns, with 159 missing. That is a **past observation**. It must not overwrite the later protected EC-BULK-003 cohort readback at `354c4bb14cb3820a0ad9988ca6b182b8a3b6f96f`, whose cohort record reports 200 source RESULT/1 returns. A source return is not an editorial admission.

The historical worker records report corrections to several manuscript drafts. No manuscript changes are imported by this archival package. Each draft correction requires comparison and, where material, a new review against the exact present manuscript hash before any admission.

## Unresolved evidence and correction

Problem 259 remains **SOURCE_BLOCKED** in the historical review because the decisive primary Chen–Ruzsa theorem text and page were not verified. Its status is not cleared by archiving this record.

The fourth original review has an incorrect finite-sum equality for problem 264. The separately preserved `worker-review-04-erratum.md` gives the correct finite partial-sum identity and explicitly leaves the original worker report unchanged. Neither the incorrect equality nor its repair is evidence of mathematical certification.

## Documentary obligations

The four original reviews, historical reviewed-text hashes, and erratum are now source-identifiable. Outstanding obligations remain: reconcile the reviewed historical manuscripts with the exact current protected texts; review any material corrections against new source hashes; resolve or explicitly retain source exceptions; and complete any separately applicable editorial admission and publication gates.

This archive makes no change to the cohort batch registry, admissions ledger, review dispositions, or current protected manuscripts.
