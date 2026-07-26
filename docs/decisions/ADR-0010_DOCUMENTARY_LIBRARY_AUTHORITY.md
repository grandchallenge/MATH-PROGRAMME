# ADR-0010: Govern Documentary Library authority, release artifacts, and web editions

## Status

Accepted, 2026-07-26.

## Context

The MATH-PROGRAMME Documentary Library publishes seven GCL–Chaidez volume records and a browser-native Poincaré reference web edition. The initial publication correctly preserved mathematical claim boundaries, but a subsequent consistency audit found that its artifact authority and continuity model was under-specified:

1. committed `.tex` files were archival source records, while public labels and the artifact manifest sometimes called them authoritative LaTeX sources;
2. checksum-locked PDFs and complete illustrated source bundles were identified but their availability and release locators were not explicit;
3. the Documentary Library and Poincaré web edition were absent from the Agent Council artifact ledger and schema-bound review registry;
4. the web-edition schema did not define the base used to resolve asset paths;
5. programme CI built the pages but did not validate manifest crosswalks, source-record identities, edition metadata, reader landmarks, or external mathematics-rendering policy;
6. RH-WP01 and RH-WP02 had merged and passed repository CI, but the public RH page still described them as future work and their legacy review records retained blocking pre-promotion language.

## Decision

1. Define four distinct documentary artifact classes:
   - **source record** — the small Git-tracked pointer identifying a complete source artifact by title, page count, byte length where available, and digest;
   - **authoritative source artifact** — the checksum-locked complete illustrated source bundle, not the pointer file;
   - **rendered edition** — the checksum-locked PDF;
   - **web edition** — a derivative public presentation whose theorem strength cannot exceed its governing campaign and source artifacts.
2. Require each documentary manifest entry to identify its programme domain, campaign, scope relation, public page, governing claim-authority artifact, source record, and release availability.
3. Use `metadata_only` when a release-class artifact has an identity record but no stable public release locator. Do not imply public availability from a checksum alone.
4. Register the Documentary Library and the Poincaré reference web edition in the Agent Council artifact ledger and bind their review record to `schemas/agent_review.schema.json` in CI.
5. Add a machine-readable documentary manifest schema, semantic validator, and adversarial rejection tests. Validation must cover manifest structure, domain and campaign crosswalks, source-record identities, page identities, web-edition schema conformance, asset existence, section correspondence, authority wording, accessibility landmarks, and mathematics-rendering policy.
6. Declare documentary edition assets as documentation-root-relative through an explicit `asset_base` contract.
7. Treat MathJax as a version-pinned, network-delivered enhancement. The source mathematics must remain present and readable without JavaScript; the checksum-locked PDF and source bundle, not the CDN response, carry archival identity.
8. Use one document main landmark supplied by MkDocs. The embedded monograph uses an `article` landmark, and skip navigation must move keyboard focus to a focusable manuscript target.
9. Record RH-WP01 and RH-WP02 as implemented, merged, and CI-passed but **not formally promoted**. Their retained blockers are independent source-locator review and migration or replacement of the legacy blocking review disposition. Repository merge and CI alone do not override that record.
10. Normalize human-facing typography to `Poincaré`, `Hamilton–Perelman`, and `GCL–Chaidez`; ASCII remains appropriate for filenames, stable identifiers, and machine keys.

## Alternatives considered

### Treat the committed source-record pointers as the authoritative source

Rejected. They intentionally do not contain the complete illustrated LaTeX project and are not expected to compile.

### Treat checksum publication as equivalent to release publication

Rejected. A digest establishes identity after a file is obtained; it does not tell a reader where the file is available.

### Promote RH-WP01 and RH-WP02 automatically because PR #90 merged and CI passed

Rejected. The legacy reviews retain blocking Referee dispositions and explicitly recommend no promotion. Merge and CI discharge repository checks but do not silently replace independent review obligations.

### Vendor the complete MathJax distribution into ordinary documentation history

Deferred. The web edition remains readable without JavaScript, the provider and version are pinned, and archival identity belongs to the PDF and complete source bundle. A future self-hosting decision may supersede this delivery policy.

## Consequences

- Documentary authority is explicit and no longer split between pointer records and complete source artifacts.
- Readers can distinguish `metadata_only` artifact identity from a published release.
- Documentary pages, metadata, assets, campaign crosswalks, and reader semantics become CI-enforced contracts.
- The Documentary Library and Poincaré web edition gain continuity ownership and schema-bound review provenance.
- RH public documentation reflects repository reality without over-promoting WP01 or WP02.
- No open problem, solved theorem, novelty claim, or formal-certification boundary is strengthened.

## Affected artifacts

- `docs/documentaries/`
- `schemas/documentary_manifest.schema.json`
- `ci/validate_documentaries.py`
- `ci/test_validate_documentaries.py`
- `ci/validate_programme.py`
- `ci/test_validate_programme.py`
- `docs/domains/riemann_hypothesis.md`
- `docs/domains/index.md`
- `docs/CAMPAIGN_PROMOTION_REGISTER.md`
- `docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md`
- `docs/AGENT_COUNCIL_DECISION_RECORDS.md`
- `docs/AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md`
- `docs/GLOSSARY.md`
- `docs/REPOSITORY_DOCS.md`
- `FILE_MANIFEST.md`
- `mkdocs.yml`
- `reviews/documentation/DOCUMENTARY-LIBRARY.agent_review.yaml`

## Review provenance

- Trigger: user-authorized thorough consistency review and maximum bounded repair.
- Documentary publication PRs inspected: #92 and #93.
- RH post-WP00 integration inspected: PR #90 and its final successful programme policy run.
- Governing claim boundaries checked against `PC-001`, `RH-001`, the public domain catalogue, and the existing status taxonomy.

## Supersession

This decision extends ADR-0008 and ADR-0009. It does not supersede their domain-coverage or governed-campaign discovery rules.