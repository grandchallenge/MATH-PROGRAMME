# GCL-TCS pilot measurement and successor evaluation

**Operation:** `GCL-TCS-PILOT-INSTITUTIONALIZATION-001`  
**Tracker:** `grandchallenge/MATH-PROGRAMME#788`  
**Measurement baseline:** `66aaa9175fe8d91907c3cf113efc2d08a113a780`  
**Status:** non-authoritative measurement and successor recommendation

## Result in one line

The bounded pilot has produced useful evidence, but it does not justify a version-1.0 promotion. The evidence supports:

```text
CONTINUE_CANDIDATE__NARROW_AND_SIMPLIFY__NO_V1_PROMOTION
```

This is a successor recommendation, not a promotion decision.

## Coverage

Six artifact classes are required by GCL-TCS-00 criterion 8. Five now have real protected pilot evidence:

| Class | Evidence | Current pilot posture |
|---|---|---|
| Mathematical | `LOG-GCD-001-TCS-PILOT-001` | protected Stage A; candidate / in review |
| Experimental / computational | none verified | explicit deficit |
| Software | `GHOS_ESTATE_MEMBERSHIP_SENTINEL` | protected Stage A; candidate / in review |
| Operational | `GHOS-ESTATE-ROLLOUT-001-DOC-001` | existing completed pilot |
| Governance | `MP-STREAMLINED-EXECUTION-001-TCS-PILOT-001` | protected Stage A; candidate / in review |
| Public | `PUB-LOG-GCD-001-TCS-PILOT-001` | protected Stage A; candidate / in review |

The experimental/computational P04 row remains deliberately unfilled. A benchmark plan, notebook, harness, or manufactured experiment is not accepted as a substitute for a completed real result package.

## Defects caught before protected merge

Three concrete communication/governance defects were found during the four new Stage-A transactions:

1. The initial software pilot used internal G1-G7 labels that did not match protected GCL-TCS gate semantics.
2. The same software pilot did not state Python compatibility and repository-root replay instructions precisely enough.
3. The initial public pilot assigned a synthetic artifact identifier to `MATH_CORE_INTEGRITY.md` instead of treating the file as governing guidance/provenance and using protected ADR-0021 as the registered architecture authority.

All three were corrected before protected merge. Where a correction changed the material candidate closure, earlier exact-head CI was discarded and the corrected head was revalidated.

A fourth defect was caught during this measurement transaction itself: the new `GCL_TCS_PILOT_MEASUREMENT_001.md` page was initially missing from `mkdocs.yml`. The docs policy shard failed closed in `ci/validate_docs.py` before merge. The missing navigation entry was added and the failed head was discarded. This is direct evidence that document-to-navigation orphan detection is operating on at least one real surface.

These examples show that the review and documentation controls can catch real defects. They do not measure review sensitivity.

## False positives and false negatives

The software sentinel includes two useful probes. An identity-equivalent population must classify as `UNCHANGED`; a synthetic new stable repository ID must route to successor admission. A live reconciliation also found `grandchallenge/GCT-EXECUTIVE` outside the historical frozen estate and routed it to successor issue #791.

The limits matter as much as the successes. The unchanged and injected-member probes are synthetic and do not establish a live false-positive or false-negative rate. The classifier also cannot detect a repository omitted by the acquisition layer, so end-to-end recall remains unknown.

No post-merge defect has yet been observed in the four new Stage-A packages during this pass. That observation is not evidence of a zero false-negative rate.

## Burden

The four new Stage-A candidate packages used:

```text
4 packages
36 changed files
2,138 added lines
0 deleted lines
7 pre-merge commits
```

These repository-diff counts are only a paperwork and iteration proxy. They are not elapsed-time, cognitive-load, or cost measurements.

The more important qualitative burdens were:

- exact material-closure classification and identity tracking;
- complete private-estate acquisition outside the sentinel classifier itself;
- synchronization of public prose with certified/audited mathematical source identities;
- synchronization of mathematical explanation with exact theorem hypotheses and replay provenance;
- strict pre-state/post-state protection checks where tool-surface limits forced guarded administration.

## Unnecessary friction found

Each new pilot currently carries a nine-file communication/conformance envelope, including deferred G8/G9 records. That structure was useful while testing the full model, but the controlling handoff makes an important distinction: routine pilot-record work does not itself require a promotion decision.

A successor template should therefore preserve the material controls but avoid generating promotion-specific G8/G9 packet material until a promotion is actually requested. A candidate pilot still needs clear promotion status and authority boundaries; it does not need ceremonial review artifacts for a transition that is not being attempted.

This is a simplification recommendation, not a change to the current GCL-TCS candidate standard.

## Controls that earned retention

The following controls provided concrete value during the pilot:

- immutable source and candidate identities;
- strict distinction between candidate supplements and authoritative source artifacts;
- claim-scoped evidence and explicit limitations;
- preserved counterexamples and negative prior-art evidence;
- material-closure-sensitive invalidation of stale review/CI;
- proportional CI with protected unchanged-attestation reuse;
- fail-closed treatment of unknown or ambiguous transitions;
- document-to-navigation orphan detection;
- explicit domain-authority firewalls, especially for mathematics, certification, publication, and MATH-CORE.

## Readiness result

The companion readiness record evaluates all ten version-1.0 criteria. At this baseline:

```text
SATISFIED                 1
PARTIAL                   6
UNSATISFIED               2
OUTSIDE_CURRENT_TRANCHE   1
```

Criterion 9 is now satisfied in the narrow sense required by the candidate standard: the pilots record false-positive evidence, false-negative evidence, burden, and unresolved ambiguities. The empirical error rates themselves remain unknown.

Criterion 8 remains partial because P04 is still missing. Criterion 2 remains unsatisfied because the complete profile owner/review-role map is not established. Criterion 4 remains unsatisfied because dedicated fail-closed exception tests are not established.

Criterion 7 is now partial rather than unsatisfied. The docs shard demonstrated a real fail-closed Markdown-to-MkDocs orphan check on this transaction, but the broader web/source/candidate/asset/static/TeX/JSON/directory coverage required by the criterion remains unestablished.

Criterion 10 remains outside the current tranche because no version-1.0 promotion is requested. No G8 decision should be manufactured merely to complete the pilot.

## Successor recommendation

Retain the candidate framework, but narrow and simplify its operating form.

Keep the controls that protect exact identity, claim status, provenance, negative evidence, material closure, and domain authority. Automate shallow evidence discovery, measurement aggregation, and orphan detection where this can be done without creating a new authority plane. Extend the demonstrated Markdown navigation check across the remaining required surfaces rather than building a duplicate authority registry. Generate promotion-specific review packets only when a real promotion transition is requested.

Do not seek version 1.0 now. If future work naturally produces a completed P04 result and there is a reason to consider v1.0, first close the remaining structural gaps: profile owner/review-role mapping, exception fail-closed tests, broad cross-surface orphan detection, and a complete normative-text/policy/schema agreement audit.

## Interpretation boundary

This pilot does not establish that GCL-TCS is optimal or that it causally improves research quality, safety, correctness, throughput, or review latency. It establishes a narrower result: several controls caught concrete defects and preserved authority boundaries, while the current packet structure also revealed opportunities to reduce ceremony without weakening those material protections.
