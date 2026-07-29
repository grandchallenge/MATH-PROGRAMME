# ADR-0010: Govern Documentary Library authority, release artifacts, and web editions

## Status

Accepted, 2026-07-26. Implementation extended, 2026-07-27 for manifest discovery and documentary tiers; extended again, 2026-07-27 for pre-admission candidates, machine status classes, trust-spine registration, and complete documentary inventory discovery.

## Context

The MATH-PROGRAMME Documentary Library publishes seven GCL–Chaidez volume records and browser-native web editions. Successive consistency audits established that claim-safe presentation was not enough: artifact classes, discovery boundaries, release availability, machine status, review registration, and pre-admission lifecycle states also had to be explicit.

The audits found:

1. committed `.tex` files were pointer records, while public labels sometimes confused them with complete source artifacts;
2. checksum-locked PDFs and illustrated bundles had identities but no explicit availability state;
3. the original validator treated Poincaré specially and left other editions in separate tests;
4. the manifest did not initially name edition records or documentary tiers;
5. omitted or orphaned edition records could escape collection governance;
6. expository depth differed without a declared editorial vocabulary;
7. UC-DOC-WP00 introduced a legitimate source-locked documentary state before public web admission, but no machine authority represented that intermediate state;
8. a pre-admission source pointer under `docs/` would be copied to the public site despite the Work Package declaring public admission deferred;
9. one exact English status token, `Open Millennium Prize Problem`, could not represent an open non-Millennium conjecture such as Frankl's conjecture;
10. documentary orphan detection covered edition JSON only, not pages, admitted source records, candidate locks, assets, asset directories, static files, or shared reader code;
11. the UC-DOC claim ledger and Agent Council review were locally tested but not yet bound to the programme's canonical claim-ledger and central review registries.

## Decision

1. Define four admitted documentary artifact classes:
   - **source record** — a small Git-tracked pointer identifying a complete source artifact by title, page count, and digest;
   - **authoritative source artifact** — the checksum-locked complete illustrated source bundle;
   - **rendered edition** — the checksum-locked PDF;
   - **web edition** — a derivative public presentation whose theorem strength cannot exceed its governing campaign and source artifacts.
2. Require each admitted manifest entry to identify its programme domain, campaign, scope relation, public page, edition record, governing claim authority, source record, documentary tier, machine claim status, problem class, display status, and release availability.
3. Use `metadata_only` when a release-class artifact has an identity record but no stable public release locator. Do not imply public availability from a checksum alone.
4. Register the Documentary Library, the Poincaré reference web edition, and the six open-problem web editions in the Agent Council artifact ledger and bind their review record to the current review schema.
5. Use `docs/documentaries/ARTIFACT_MANIFEST.json` as the sole machine discovery authority for admitted public editions.
6. Every admitted manifest volume must name exactly one existing edition record, web page, source record, and asset directory. Every discovered admitted edition record, page, source record, asset file, and asset directory must be declared by exactly one manifest volume.
7. Use `docs/documentaries/DOCUMENTARY_CANDIDATES.json` as the separate public metadata authority for pre-admission documentary source locks.
8. Candidate metadata may be public, but pre-admission source pointers remain under the governing campaign and are repository-only until atomic manifest admission.
9. Candidate membership does not confer collection membership, public source-record status, browser-edition publication, or release availability.
10. Candidate admission must atomically add the web page, edition record, native assets, public source record, collection entry, MkDocs navigation entry, and manifest volume.
11. Separate status into:
    - `claim_status`: machine state such as `open` or `solved`;
    - `problem_class`: mathematical/documentary class such as `millennium_open_problem`, `open_conjecture`, or `solved_classical_theorem`;
    - `display_status`: reader-facing wording.
    Validation must branch on machine state, never on an exact English phrase.
12. Define three expository tiers:
    - **reference** — canonical browser-reader substrate and most complete implementation exemplar;
    - **full** — sustained narrative and technical treatment using the shared authority contract;
    - **orientation** — complete but compressed first-principles map of problem, theorem terrain, vocabulary, and guardrails.
    Tiers are editorial metadata only and do not encode theorem strength, campaign promotion, certification, or release availability.
13. Assign Poincaré to `reference`, BSD to `full`, and Hodge, Navier–Stokes, Yang–Mills, P versus NP, and Riemann to `orientation`.
14. Declare documentary edition assets documentation-root-relative through the `asset_base` contract.
15. Treat MathJax as a version-pinned network enhancement. Source mathematics must remain readable without JavaScript; archival identity belongs to the PDF and complete source bundle.
16. Use one document main landmark supplied by MkDocs. Embedded monographs use an `article` landmark and focusable skip target.
17. Keep problem-specific mathematical-spine tests separate, but place shared discovery, schema, authority, accessibility, asset, release, source, section, and rendering invariants in the manifest-driven validator.
18. Discover and reject documentary cruft across all governed file classes:
    - edition records;
    - web pages;
    - admitted source records;
    - candidate source locks;
    - asset files and asset directories;
    - root documentary `.txt`, `.tex`, and `.json` files;
    - shared documentary CSS and JavaScript authority files.
19. Delete obsolete static files rather than retaining unlinked public copies. Historical content remains recoverable through Git.
20. Require UC-DOC-WP00's claim ledger to conform to the canonical claim-ledger schema and be centrally registered. Require its schema-bound Agent Council review to be centrally registered. Omitted canonical ledgers and discoverable schema-bound reviews fail policy.
21. Retain RH-WP01 and RH-WP02 as implemented, merged, and CI-passed but not formally promoted while their independent retained blockers remain open.
22. Normalize human-facing typography to `Poincaré`, `Hamilton–Perelman`, and `GCL–Chaidez`; ASCII remains appropriate for filenames, stable identifiers, and machine keys.

## Candidate public-copy policy

Public candidate metadata are useful because they expose status, authority, proposed tier, release identities, review record, and exact admission obligations. The source pointer itself is withheld from the generated site because its presence under `docs/` would create an unlisted public artifact before the page and edition contract exist.

This is not secrecy or release withdrawal. The complete source and PDF remain `metadata_only`, and the pointer remains available in repository history and the governing campaign. Atomic admission will move or copy the pointer into `docs/documentaries/sources/` only when the complete public edition enters the manifest.

## Alternatives considered

### Treat committed source-record pointers as authoritative source

Rejected. They intentionally do not contain the complete illustrated LaTeX project and are not expected to compile.

### Treat checksum publication as release publication

Rejected. A digest establishes identity after acquisition; it does not provide an acquisition route.

### Discover admitted editions by directory glob alone

Rejected. A glob cannot decide whether a file is governed, complete, intentionally retired, or correctly crosswalked. The manifest owns membership; directory discovery is adversarial and detects omissions or orphans.

### Put pre-admission candidates directly in the admitted manifest

Rejected. That would permit manifest membership without a public page, edition record, assets, navigation, and accessibility contract, defeating atomic admission.

### Keep candidate source pointers under `docs/` but omit them from navigation

Rejected. MkDocs copies non-Markdown static files under `docs_dir`; unlisted is not the same as unpublished.

### Encode openness in display prose only

Rejected. Exact-English branching cannot represent non-Millennium conjectures and confuses reader language with machine state.

### Require identical expository length across all editions

Rejected. Equal length is not a mathematical or accessibility requirement and would invite padding. Explicit tiers make depth differences reviewable.

### Vendor the complete MathJax distribution

Deferred. The editions remain readable without JavaScript; provider and version are pinned; archival identity belongs to the PDF and source bundle.

## Consequences

- Admitted edition authority and pre-admission candidate authority are distinct and explicit.
- Union-Closed can remain honestly classified as an open conjecture without using a false Millennium label or falling into a solved branch.
- Candidate metadata are public while candidate source pointers remain repository-only until admission.
- Omitted or orphaned pages, source records, candidate locks, assets, directories, static files, and reader code are rejected.
- Canonical claim ledgers and schema-bound reviews cannot silently evade central registration.
- Release identities remain separate from availability claims.
- Expository tier remains separate from theorem strength.
- No open problem, solved theorem, novelty claim, or formal-certification boundary is strengthened.

## Affected artifacts

- `CLAIM_LEDGER_STANDARD.md`
- `schemas/claim_ledger.schema.json`
- `templates/claim_ledger_template.yaml`
- `templates/union_closed_claim_ledger_wp01.yaml`
- `campaigns/union_closed/UC_DOC_WP00_DOCUMENTARY_SOURCE_LOCK/`
- `reviews/union_closed/UC-DOC-WP00.agent_review.yaml`
- `docs/documentaries/ARTIFACT_MANIFEST.json`
- `docs/documentaries/DOCUMENTARY_CANDIDATES.json`
- `schemas/documentary_manifest.schema.json`
- `schemas/documentary_candidate_registry.schema.json`
- `docs/documentaries/sources/README.md`
- `ci/validate_documentaries.py`
- `ci/test_validate_documentaries.py`
- `ci/validate_programme.py`
- `ci/test_validate_programme.py`
- `tests/test_uc_doc_source_lock.py`
- `mkdocs.yml`

## Review provenance

- Initial publication and authority work: PRs #92, #93, #99, #103, and #104.
- Wave Two source lock: PR #105.
- Trigger for this extension: post-merge consistency, coverage, dangling-artifact, and cruft audit.
- The extension repairs governance and discovery only. It does not revise the mathematical content of the seven admitted editions or promote Frankl's conjecture.

## Supersession

This decision extends ADR-0008 and ADR-0009. It does not supersede their public-domain coverage or governed-campaign discovery rules. Later semantic-binding and reference-tier normalization work may extend this ADR without changing the candidate/admission boundary established here.
