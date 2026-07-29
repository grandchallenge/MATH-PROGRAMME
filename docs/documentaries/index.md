# MATH-PROGRAMME Documentary Library

The Documentary Library translates the programme's hardest mathematical terrain into illuminated, source-conscious monographs for the enjoyment and enlightenment of the lay reader. Each volume follows the **GCL–Chaidez** pattern: wonder first, definitions before claims, proof spines before conclusions, adversarial guardrails against attractive errors, and a technical appendix for readers who wish to descend beneath the imagery.

!!! info "Authority and claim boundary"
    The plates are pedagogical artworks, not proof diagrams. The cited literature, campaign ledgers, governing claim-authority artifacts, and claim-level trust matrices govern mathematical assertions. Open problems remain open; the Poincaré volume is a reconstruction of a solved theorem and makes no new-proof claim.

## Discovery authority

[`ARTIFACT_MANIFEST.json`](ARTIFACT_MANIFEST.json) is the sole machine discovery authority for **admitted public editions**. Every admitted volume names exactly one source record, web page, web-edition record, claim authority, scope relation, documentary tier, claim status, problem class, and display status.

[`DOCUMENTARY_CANDIDATES.json`](DOCUMENTARY_CANDIDATES.json) is the separate public metadata authority for **pre-admission source locks**. Candidate metadata confer no collection membership. The registry remains authoritative when empty. Candidate source pointers remain repository-only until a page, edition record, native assets, public source record, collection entry, navigation entry, and manifest volume are admitted atomically.

CI rejects missing or orphaned edition records, pages, admitted source records, documentary source locks, asset files, asset directories, root static files, and shared reader CSS or JavaScript. It also rejects drift among the manifest, candidate registry, domain registry, source records, source locks, edition records, and rendered pages.

## Documentary tiers

The tiers describe expository scope, not mathematical authority.

- **Reference** — the canonical browser-reader implementation and most complete substrate exemplar. The Poincaré reconstruction occupies this tier.
- **Full** — a sustained documentary treatment comparable in narrative and technical depth to the reference while retaining its own problem-specific structure. The BSD and Union-Closed volumes occupy this tier.
- **Orientation** — a complete, claim-safe first-principles map of the problem, theorem terrain, guardrails, and technical vocabulary. Orientation editions are intentionally more compressed and may later be expanded without changing theorem strength.

All tiers obey the same artifact-authority, accessibility, source, release-identity, and claim-boundary contracts.

## The admitted collection

| Volume | Tier | Domain / campaign | Subject | Status | Length | Source record | Edition record |
|---|---|---|---|---|---:|---|---|
| [The Shape of a Sphere](poincare.md) | Reference | `PC` / `PC-001` | Poincaré theorem reconstruction | Archival reconstruction | 33 pages | [Record](sources/the_shape_of_a_sphere.tex) | [Edition](poincare.edition.json) |
| [The Hidden Music of Elliptic Curves](bsd.md) | Full | `BSD` / `BSD-001` | Birch and Swinnerton–Dyer Conjecture | Open Millennium Prize Problem | 37 pages | [Record](sources/the_hidden_music_of_elliptic_curves.tex) | [Edition](bsd.edition.json) |
| [The Geometry of Hidden Harmony](hodge.md) | Orientation | `HC` / `HC-001` | Hodge Conjecture | Open Millennium Prize Problem | 41 pages | [Record](sources/the_geometry_of_hidden_harmony.tex) | [Edition](hodge.edition.json) |
| [The River and the Storm](navier_stokes.md) | Orientation | `NSCI` / `NS-CI-001` | Navier–Stokes existence and smoothness | Open Millennium Prize Problem | 47 pages | [Record](sources/the_river_and_the_storm.tex) | [Edition](navier_stokes.edition.json) |
| [The Geometry of Force and Silence](yang_mills.md) | Orientation | `YM` / `YM-001` | Yang–Mills existence and mass gap | Open Millennium Prize Problem | 58 pages | [Record](sources/the_geometry_of_force_and_silence.tex) | [Edition](yang_mills.edition.json) |
| [The Shape of Computational Truth](p_vs_np.md) | Orientation | `PNP` / `PNP-001` | P versus NP | Open Millennium Prize Problem | 50 pages | [Record](sources/the_shape_of_computational_truth.tex) | [Edition](p_vs_np.edition.json) |
| [The Music of the Primes](riemann.md) | Orientation | `RH` / `RH-001` | Riemann Hypothesis | Open Millennium Prize Problem | 49 pages | [Record](sources/the_music_of_the_primes.tex) | [Edition](riemann.edition.json) |
| [The Element in Half the Worlds](union_closed.md) | Full | `UC` / `UC` | Frankl's Union-Closed Sets Conjecture | Open conjecture | 48 pages | [Record](sources/the_element_in_half_the_worlds.tex) | [Edition](union_closed.edition.json) |

The Navier–Stokes volume orients the full Millennium problem. Its programme crosswalk points to the narrower `NS-CI-001` critical-integrability campaign and must not be read as an identity between those scopes.

## Pre-admission candidates

The candidate registry is currently empty. Union-Closed completed atomic admission through UC-DOC-WP01; its historical UC-DOC-WP00 source lock remains governed through the admitted manifest volume's `source_lock` provenance field.

## Editorial form

The series uses cream parchment, deep navy, restrained gold, classical serif typography, ornamental framing, luminous mathematical imagery, explanatory prose, explicit theorem boundaries, and technical appendices that deepen rather than merely repeat the lay account.

## Artifact authority and preservation

Git stores admitted web records, admitted source-record pointers, edition records, candidate metadata, schemas, and validation contracts. Pre-admission source pointers remain under their governing campaign until admission; admitted volumes may retain those historical source-lock paths as provenance.

For each admitted volume:

- the checksum-locked complete illustrated source bundle is the **authoritative source artifact**;
- the checksum-locked PDF is the **rendered edition**;
- the Markdown page is a derivative **web edition**;
- the `*.edition.json` file is the machine-readable browser-edition contract;
- byte lengths, SHA-256 digests, programme crosswalks, release availability, documentary tier, status class, and discovery identity are fixed in [`ARTIFACT_MANIFEST.json`](ARTIFACT_MANIFEST.json).

All release-class artifacts are currently recorded as `metadata_only`: their identities are governed, but no stable public release locator is asserted. A checksum proves identity after a file is obtained; it does not itself establish publication or availability.

## Web-edition policy

The Poincaré page is the reference browser-native implementation. Its reusable content contract is defined by [`documentary_web.schema.json`](documentary_web.schema.json). Every manifest-discovered edition is validated against that schema and against shared semantic, accessibility, source, release, section, plate, and mathematics-rendering contracts. MathJax is a version-pinned network enhancement; source TeX remains in the document when JavaScript is unavailable, and archival identity belongs to the PDF and complete source bundle.

## Reading order

There is no required order. A reader seeking geometry may begin with Poincaré or Hodge; arithmetic with BSD or Riemann; physical law with Navier–Stokes or Yang–Mills; computation with P versus NP; finite combinatorics with Union-Closed. Each volume begins again from first principles.
