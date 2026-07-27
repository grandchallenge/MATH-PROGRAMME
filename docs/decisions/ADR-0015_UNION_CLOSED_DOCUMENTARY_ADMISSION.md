# ADR-0015: Admit the Union-Closed full-tier documentary as the Wave Two pilot

## Status

Accepted, 2026-07-27, conditional on the complete repository policy workflow.

## Context

The seven-volume Documentary Library validated one shared browser-reader contract across the solved Poincaré reconstruction and six Millennium problems. Wave Two was authorized to test that contract on broader programme domains. UC-DOC-WP00 then locked a 48-page illustrated source artifact for Frankl’s union-closed sets conjecture but correctly deferred public web admission.

The existing validator encoded open status through the Millennium-specific phrase `Open Millennium Prize Problem`. A non-Millennium open conjecture exposed a genuine representational deficiency: status validation must preserve the exact manifest status without equating openness with Millennium classification.

## Decision

1. Admit *The Element in Half the Worlds* as a `full`-tier `campaign_documentary` for Domain `UC` and campaign `UC`.
2. Add the semantic page, edition record, native SVG plates, source-record disposition, manifest member, collection index, and MkDocs route atomically.
3. Preserve `ARTIFACT_MANIFEST.json` as the sole discovery authority.
4. Generalize documentary status validation so any manifest status beginning with `Open ` is treated as open and must appear in the edition record and at least twice in the page. Retain the distinct solved-classical-theorem requirement.
5. Keep all release-class artifacts `metadata_only`; no public locator is inferred.
6. Preserve the UC-DOC-WP00 source-lock identities unchanged.
7. Classify every plate as `pedagogical_orientation_only` and retain text, equations, and source records as mathematical authority.
8. Record Frankl’s conjecture as open on every status surface. Bounded enumeration, entropy constants, formal special cases, lattice theorems, and hybrid certificates retain their individual scopes.

## Consequences

- The Documentary Library expands from seven to eight manifest-discovered editions.
- The collection now contains one reference tier, two full tiers, and five orientation tiers.
- Wave Two obtains its first non-Millennium pilot without weakening the shared schema or authority model.
- The status validator becomes problem-class agnostic while remaining fail-closed on exact wording.
- UC-DOC-WP01 completes web admission only; it establishes no new combinatorial theorem.

## Rejected alternatives

### Label Union-Closed as a Millennium problem

Rejected as false.

### Publish the page without a manifest member

Rejected as an orphaned and ungoverned web artifact.

### Add the manifest member before the reader and edition record

Rejected because discovery must fail closed on incomplete admission.

### Treat generated plate text as mathematical authority

Rejected. Plate content remains pedagogical and may be compressed or decorative.

## Affected artifacts

- `docs/documentaries/ARTIFACT_MANIFEST.json`
- `docs/documentaries/index.md`
- `docs/documentaries/union_closed.md`
- `docs/documentaries/union_closed.edition.json`
- `docs/documentaries/sources/the_element_in_half_the_worlds.tex`
- `docs/assets/documentaries/union_closed/`
- `docs/stylesheets/documentary-status.css`
- `ci/validate_documentaries.py`
- `tests/test_uc_doc_source_lock.py`
- `tests/test_union_closed_documentary.py`
- `campaigns/union_closed/UC_DOC_WP01_WEB_ADMISSION/`
- `reviews/union_closed/UC-DOC-WP01.agent_review.yaml`
- `docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md`
- `docs/AGENT_COUNCIL_DECISION_RECORDS.md`
- `mkdocs.yml`

## Claim boundary

This decision governs admission and presentation only. Frankl’s conjecture remains open.
