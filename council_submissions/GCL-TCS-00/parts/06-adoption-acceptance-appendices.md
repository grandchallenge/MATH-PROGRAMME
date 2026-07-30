# 18. Adoption sequence

GCL SHOULD adopt the standards family in this order:

1. GCL-TCS-00 - Charter and conformance model.
2. GCL-TCS-01 - Controlled technical language.
3. GCL-TCS-02 - Terminology, notation, and ontology.
4. GCL-TCS-03 - Claims and epistemic status.
5. GCL-TCS-04 - Mathematical exposition and proof records.
6. GCL-TCS-05 - Experimental and computational reporting.
7. GCL-TCS-06 - Software, API, and notebook documentation.
8. GCL-TCS-07 - Artifact, provenance, and manifest integrity.
9. GCL-TCS-08 - Review, promotion, and referee practice.
10. GCL-TCS-09 - Audience and publication profiles.

The detailed modules MUST conform to this charter. A later module can specialize a rule but cannot silently remove a non-waivable requirement.

# 19. Minimum conformance declaration

The following example is informative. The machine-readable templates in this package are normative for version 0.1.0.

```yaml
schema_version: "0.1.0"
standard:
  id: "GCL-TCS-00"
  version: "0.1.0"
artifact_id: "EXAMPLE-ARTIFACT-001"
title: "Example technical artifact"
artifact_type: "research_report"
version: "0.1.0"
date: "2026-07-27"
owner: "Example owner"
authority_status: "candidate"
promotion_status: "registered"
primary_profile:
  id: "GCL-TCS-P02"
  version: "0.1.0"
secondary_profiles: []
impact_class: "IC-2"
audience: ["researcher"]
scope: "The exact subject covered by the artifact."
out_of_scope: ["An explicit exclusion."]
source_location: "repository/path"
source_revision: "immutable-revision-or-hash"
dependencies: []
terminology_registry: "registry/TERMS.yaml"
notation_registry: "registry/NOTATION.yaml"
claim_register: "claims/CLAIMS.yaml"
evidence_register: "evidence/EVIDENCE.yaml"
review_register: []
exceptions: []
conformance_dimensions:
  L: "DECLARED"
  T: "DECLARED"
  S: "DECLARED"
  C: "DECLARED"
  E: "UNASSESSED"
  R: "UNASSESSED"
  P: "DECLARED"
  V: "UNASSESSED"
  G: "DECLARED"
supersedes: []
superseded_by: null
licence_and_access:
  licence: "project-defined"
  access: "internal"
generated_content:
  present: true
  method: "machine-assisted drafting"
  review: "Human technical review required before promotion"
```

# 20. Acceptance criteria for GCL-TCS-00 version 1.0

This candidate can become version 1.0 only when:

1. The policy manifest and conformance schema agree with the normative text.
2. Each profile has an approved owner and review role map.
3. Mandatory fields have machine-readable definitions and validation tests.
4. The exception workflow has fail-closed tests.
5. Gate records bind to immutable artifact revisions.
6. Candidate and authoritative source records are distinct in the schema.
7. Orphan detection covers documents, web pages, source records, candidate records, assets, static text, TeX, JSON, and directories where applicable.
8. At least one mathematical, experimental, software, operational, governance, and public artifact has completed a pilot conformance review.
9. The pilots record false positives, false negatives, burden, and unresolved ambiguities.
10. The Referee approves promotion with an explicit statement of remaining limitations.

# Appendix A - Profile selection guide

Use the following questions:

1. Does the artifact tell a reader how to do something in sequence? Select P01.
2. Does it report or evaluate a research question? Select P02.
3. Does it define or prove mathematical statements? Select P03.
4. Does it depend on data, simulation, computation, or plots? Select P04.
5. Does it define software behaviour, interfaces, or executable notebooks? Select P05.
6. Is it intended primarily for a public audience? Select P06.
7. Does it govern records, authority, review, or lifecycle? Select P07.

Select all applicable profiles. Use the main reader task to choose the primary profile.

# Appendix B - Exception decision test

A reviewer SHOULD reject an exception when any answer is no:

1. Is the exact rule identified?
2. Is the affected content narrow and identifiable?
3. Would strict compliance create a material problem?
4. Does the reason concern correctness, authority, safety, interoperability, accessibility, or disproportionate burden?
5. Are the risks explicit?
6. Are compensating controls adequate?
7. Is the approver authorized and independent enough for the impact class?
8. Is a review or expiry date present?
9. Does the exception preserve all non-waivable requirements?

# Appendix C - Promotion decision statement

A G8 referee decision SHOULD use this structure:

- **Artifact and revision:** Exact identifier and immutable revision.
- **Requested authority:** What promotion permits.
- **Established:** Claims and properties supported by the completed review.
- **Not established:** Claims and properties that remain outside the evidence.
- **Exceptions:** Active exceptions and their effects.
- **Residual risk:** Known uncertainty and unresolved debt.
- **Downstream use:** Authorized and prohibited uses.
- **Decision:** PASS, FAIL, or DEFERRED.

# Appendix D - Reference basis

This charter uses ASD-STE100 Simplified Technical English, Issue 9, as a baseline for ordinary technical prose. Relevant baseline topics include controlled words and technical terms, active voice, clear sentence structure, procedural writing, stable key terms, short descriptive sentences, topic-bounded paragraphs, and limited paragraph length.

GCL adds claim governance, mathematical precision, experimental reporting, software contracts, provenance, exception control, and promotion gates. These additions are necessary because linguistic clarity alone does not establish technical validity or authority.
