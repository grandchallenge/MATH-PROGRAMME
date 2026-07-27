# ADR-0010: Govern Documentary Library authority, release artifacts, and web editions

## Status

Accepted, 2026-07-26. Implementation extended, 2026-07-27.

## Context

The MATH-PROGRAMME Documentary Library publishes seven GCL–Chaidez volume records and browser-native web editions. The initial publication correctly preserved mathematical claim boundaries, but a subsequent consistency audit found that its artifact authority and continuity model was under-specified:

1. committed `.tex` files were archival source records, while public labels and the artifact manifest sometimes called them authoritative LaTeX sources;
2. checksum-locked PDFs and complete illustrated source bundles were identified but their availability and release locators were not explicit;
3. the Documentary Library and Poincaré web edition were absent from the Agent Council artifact ledger and schema-bound review registry;
4. the web-edition schema did not define the base used to resolve asset paths;
5. programme CI built the pages but did not validate manifest crosswalks, source-record identities, edition metadata, reader landmarks, or external mathematics-rendering policy;
6. RH-WP01 and RH-WP02 had merged and passed repository CI, but the public RH page still described them as future work and their legacy review records retained blocking pre-promotion language;
7. after PRs #99 and #103, all seven volumes had web editions, but the primary validator still treated Poincaré specially while BSD and the remaining five volumes relied on separate hard-coded tests;
8. the manifest did not name edition records, so omitted or orphaned `*.edition.json` files could escape the collection authority model;
9. expository depth differed materially across volumes without a declared editorial vocabulary.

## Decision

1. Define four distinct documentary artifact classes:
   - **source record** — the small Git-tracked pointer identifying a complete source artifact by title, page count, byte length where available, and digest;
   - **authoritative source artifact** — the checksum-locked complete illustrated source bundle, not the pointer file;
   - **rendered edition** — the checksum-locked PDF;
   - **web edition** — a derivative public presentation whose theorem strength cannot exceed its governing campaign and source artifacts.
2. Require each documentary manifest entry to identify its programme domain, campaign, scope relation, public page, web-edition record, governing claim-authority artifact, source record, documentary tier, and release availability.
3. Use `metadata_only` when a release-class artifact has an identity record but no stable public release locator. Do not imply public availability from a checksum alone.
4. Register the Documentary Library, the Poincaré reference web edition, and the six open-problem web editions in the Agent Council artifact ledger and bind their review record to `schemas/agent_review.schema.json` in CI.
5. Add a machine-readable documentary manifest schema, semantic validator, and adversarial rejection tests. Validation must cover manifest structure, manifest-to-directory discovery, domain and campaign crosswalks, source-record identities, edition metadata, topic and authority concordance, scope and tier compatibility, asset existence and uniqueness, section correspondence, authority wording, accessibility landmarks, and mathematics-rendering policy.
6. Declare `docs/documentaries/ARTIFACT_MANIFEST.json` the sole machine discovery authority. Every manifest volume must name exactly one existing edition record. Every discovered `*.edition.json` file must be registered. Omitted and orphaned editions fail policy.
7. Declare documentary edition assets as documentation-root-relative through an explicit `asset_base` contract.
8. Treat MathJax as a version-pinned, network-delivered enhancement. The source mathematics must remain present and readable without JavaScript; the checksum-locked PDF and source bundle, not the CDN response, carry archival identity.
9. Use one document main landmark supplied by MkDocs. The embedded monograph uses an `article` landmark, and skip navigation must move keyboard focus to a focusable manuscript target.
10. Record RH-WP01 and RH-WP02 as implemented, merged, and CI-passed but **not formally promoted**. Their retained blockers are independent source-locator review and migration or replacement of the legacy blocking review disposition. Repository merge and CI alone do not override that record.
11. Normalize human-facing typography to `Poincaré`, `Hamilton–Perelman`, and `GCL–Chaidez`; ASCII remains appropriate for filenames, stable identifiers, and machine keys.
12. Define three expository tiers:
    - **reference** — the canonical browser-reader substrate and most complete implementation exemplar;
    - **full** — a sustained narrative and technical treatment using the shared authority contract;
    - **orientation** — a complete but compressed first-principles map of the problem, theorem terrain, vocabulary, and guardrails.
    Tiers are editorial metadata only. They do not encode theorem strength, campaign promotion, certification, or release availability.
13. Assign Poincaré to `reference`, BSD to `full`, and Hodge, Navier–Stokes, Yang–Mills, P versus NP, and Riemann to `orientation`.
14. Keep problem-specific mathematical-spine tests separate, but move all shared discovery, schema, authority, accessibility, asset, release, source, section, and rendering invariants into the manifest-driven validator.

## Alternatives considered

### Treat the committed source-record pointers as the authoritative source

Rejected. They intentionally do not contain the complete illustrated LaTeX project and are not expected to compile.

### Treat checksum publication as equivalent to release publication

Rejected. A digest establishes identity after a file is obtained; it does not tell a reader where the file is available.

### Discover editions by glob without a manifest authority

Rejected. A directory glob can find files but cannot determine whether a file is governed, complete, intentionally retired, or correctly crosswalked. The manifest owns membership; directory discovery is used adversarially to detect omissions and orphans.

### Require identical expository length across all seven editions

Rejected. Equal length is not a mathematical or accessibility requirement and would invite padding. Explicit tiers make depth differences reviewable while preserving one shared authority contract.

### Promote RH-WP01 and RH-WP02 automatically because PR #90 merged and CI passed

Rejected. The legacy reviews retain blocking Referee dispositions and explicitly recommend no promotion. Merge and CI discharge repository checks but do not silently replace independent review obligations.

### Vendor the complete MathJax distribution into ordinary documentation history

Deferred. The web editions remain readable without JavaScript, the provider and version are pinned, and archival identity belongs to the PDF and complete source bundle. A future self-hosting decision may supersede this delivery policy.

## Consequences

- Documentary authority is explicit and no longer split between pointer records and complete source artifacts.
- Readers can distinguish `metadata_only` artifact identity from a published release.
- The manifest is the fail-closed collection inventory rather than one metadata file among several.
- All seven documentary pages, metadata records, assets, campaign crosswalks, and reader semantics are validated through one generalized contract.
- Omitted, orphaned, topic-drifted, authority-drifted, scope-incompatible, and duplicate-asset states are rejected.
- Expository depth differences are visible through reference, full, and orientation tiers without implying mathematical hierarchy.
- Shared infrastructure tests no longer diverge across Poincaré, BSD, and Wave One.
- RH public documentation reflects repository reality without over-promoting WP01 or WP02.
- No open problem, solved theorem, novelty claim, or formal-certification boundary is strengthened.

## Affected artifacts

- `docs/documentaries/`
- `docs/documentaries/ARTIFACT_MANIFEST.json`
- `docs/documentaries/*.edition.json`
- `schemas/documentary_manifest.schema.json`
- `ci/validate_documentaries.py`
- `ci/test_validate_documentaries.py`
- `tests/test_documentary_web_editions.py`
- `tests/test_documentary_wave_one.py`
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

- Trigger: user-authorized consistency and coverage review followed by explicit implementation authorization.
- Documentary publication PRs inspected: #92, #93, #99, and #103.
- Governing claim boundaries checked against all seven manifest claim authorities, the public domain catalogue, and the existing status taxonomy.
- The 2026-07-27 extension closes the post-PR-103 discovery and test-fragmentation gap without rewriting the historical status of earlier reviews.

## Supersession

This decision extends ADR-0008 and ADR-0009. It does not supersede their domain-coverage or governed-campaign discovery rules.
