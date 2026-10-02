# REVIEWER DELIVERY STANDARD — PDF-First Gate 8 Surface

## Purpose

This standard defines the reviewer-facing delivery surface for every volume in **TYPE THEORY — The Grand Unified Theory of Computation**. It controls review logistics only. It does not perform independent mathematical review, certify a theorem, or grant publication authority.

The objective is simple: a genuinely independent mathematical reader must be able to begin from one protected link and read the camera-ready manuscript immediately. Repository archaeology, source reconstruction, and TeX compilation are not prerequisites for Gate 8.

## Applicability

Apply this standard to Volumes I–X whenever an RC has passed Gate 7A and is being prepared for Gate 8. Existing volumes must be retrofitted when their review surface predates this standard.

## Required protected layout

Each `reviews/<RC>/` directory must contain:

- `README.md` — protected reviewer landing page;
- `REVIEWER_START_HERE.md` — one-page operational guide;
- `GATE8_REVIEW_PACKET.md` — mathematical review scope and boundaries;
- `THEOREM_REVIEW_MATRIX.json` — coverage/index surface with reviewer findings initially pending;
- `REVIEW_RECORD_TEMPLATE.yaml` — attributable review record;
- `REVIEWER_ASSET_MANIFEST.json` — cryptographic identity of reviewer-facing assets;
- `BUILD.md` — optional source/reproducibility path;
- `assets/01_<VOLUME>_<RC>.pdf` — primary manuscript review surface;
- `assets/02_SOLUTIONS_COMPANION_<RC>.pdf` — pedagogical companion;
- `assets/03_PLATE_FOLIO_<RC>.pdf` — visual folio;
- `assets/04_<VOLUME>_<RC>_Source.zip` — exact admitted source/rebuild archive;
- `assets/...Reviewer_Bundle.zip` — deterministic all-in-one reviewer bundle.

The issue tracking Gate 8 must begin with a direct link to the protected `README.md`.

## Primary review rule

The manuscript PDF is the primary reading surface. A reviewer may conduct mathematical review directly from the supplied PDFs. Source inspection is required only when the reviewer judges it necessary for a proof, notation choice, executable claim, plate, solution, or trust-boundary question.

TeX recompilation is optional reproducibility evidence. It is not a condition for beginning or completing mathematical review unless a specific defect under review is itself a build/reproducibility defect.

## Exact-target binding

The durably admitted source/rebuild identity remains the canonical mathematical target. Every reviewer surface must record:

1. exact admitted source archive SHA-256 and size;
2. protected source-admission commit;
3. protected release-tree SHA;
4. historical Gate-7 distribution PDF hashes when they exist;
5. reviewer-facing PDF hashes and page counts;
6. reviewer-bundle hash and size;
7. protected reviewer-surface merge and review-directory tree after admission.

A material mathematical or claim-scope change creates a new review target and invalidates stale review evidence.

## Historical PDF bytes versus reviewer renderings

Prefer the exact frozen Gate-7 PDF bytes when they are durably retrievable.

If the exact historical PDF bytes are not available through the repository-ingest path, it is permitted to create a deterministic reviewer rendering from the exact admitted source. In that case:

- use a fixed `SOURCE_DATE_EPOCH` or equivalent deterministic build control;
- require the recorded Gate-7 page counts;
- run PDF preflight;
- record both the historical reference-output hash and the reviewer-rendering hash;
- state explicitly that byte identity is **not** claimed;
- do not replace or rewrite the historical reference-output identity.

A source-derived review rendering is a convenience representation of the exact admitted source; it is not a new mathematical revision.

## Reviewer bundle

The complete reviewer bundle must contain the three PDFs, exact admitted source archive, start guide, Gate-8 packet, theorem matrix, review-record template, optional build instructions, and a non-self-referential contents/checksum manifest. The ZIP must be deterministic: fixed member ordering, fixed timestamps, and no host-specific metadata.

The repository-level `REVIEWER_ASSET_MANIFEST.json` records the final bundle SHA-256 and size.

## Independence and authority boundaries

Preparing, packaging, hashing, rebuilding, visually inspecting, or admitting the reviewer surface does not satisfy Gate 8. CI and machine-assisted checking do not substitute for attributable independent mathematical judgment.

Passing Gate 8 may support only `RC_REVIEW_QUALIFIED`. It does not create Gate-9 publication authority.

Do not use a GitHub Release object, public URL, tag, or polished PDF as a surrogate signal for `PUBLISHED_AUTHORITATIVE_EDITION`.

## Protected admission and readback

Reviewer-delivery changes must pass ordinary protected repository controls. After merge:

- read back protected `main`;
- record the protected reviewer-surface merge commit;
- record the `reviews/<RC>/` tree SHA;
- verify the manifest and asset blob sizes from protected state;
- update the Gate-8 issue entry point if needed.

Reviewer-delivery readiness is a logistics condition under Gate 8, not a new publication-state transition.

## Subsequent-volume rule

For every subsequent volume, reviewer delivery is part of the normal RC pipeline:

`Gate 7 camera-ready composition -> Gate 7A durable admission -> PDF-first reviewer delivery -> Gate 8 independent review -> Gate 9 publication authority`

A composing agent must not hand an external reviewer only a source archive when camera-ready review artifacts exist or can be deterministically rendered from the exact admitted source.
