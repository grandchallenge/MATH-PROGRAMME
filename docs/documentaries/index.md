# MATH-PROGRAMME Documentary Library

The Documentary Library translates the programme's hardest mathematical terrain into illuminated, source-conscious monographs for the enjoyment and enlightenment of the lay reader. Each volume follows the **GCL–Chaidez** pattern: wonder first, definitions before claims, proof spines before conclusions, adversarial guardrails against attractive errors, and a technical appendix for readers who wish to descend beneath the imagery.

!!! info "Authority and claim boundary"
    The plates are pedagogical artworks, not proof diagrams. The cited literature, campaign ledgers, governing claim-authority artifacts, and claim-level trust matrices govern mathematical assertions. Open problems remain open; the Poincaré volume is a reconstruction of a solved theorem and makes no new-proof claim.

## The collection

| Volume | Domain / campaign | Subject | Status | Length | Source record |
|---|---|---|---|---:|---|
| [The Shape of a Sphere](poincare.md) | `PC` / `PC-001` | Poincaré theorem reconstruction | Solved classical theorem; documentary reconstruction, not a new proof | 33 pages | [Record](sources/the_shape_of_a_sphere.tex) |
| [The Hidden Music of Elliptic Curves](bsd.md) | `BSD` / `BSD-001` | Birch and Swinnerton–Dyer Conjecture | Open Millennium Prize Problem | 37 pages | [Record](sources/the_hidden_music_of_elliptic_curves.tex) |
| [The Geometry of Hidden Harmony](hodge.md) | `HC` / `HC-001` | Hodge Conjecture | Open Millennium Prize Problem | 41 pages | [Record](sources/the_geometry_of_hidden_harmony.tex) |
| [The River and the Storm](navier_stokes.md) | `NSCI` / `NS-CI-001` | Navier–Stokes existence and smoothness | Open Millennium Prize Problem | 47 pages | [Record](sources/the_river_and_the_storm.tex) |
| [The Geometry of Force and Silence](yang_mills.md) | `YM` / `YM-001` | Yang–Mills existence and mass gap | Open Millennium Prize Problem | 58 pages | [Record](sources/the_geometry_of_force_and_silence.tex) |
| [The Shape of Computational Truth](p_vs_np.md) | `PNP` / `PNP-001` | P versus NP | Open Millennium Prize Problem | 50 pages | [Record](sources/the_shape_of_computational_truth.tex) |
| [The Music of the Primes](riemann.md) | `RH` / `RH-001` | Riemann Hypothesis | Open Millennium Prize Problem | 49 pages | [Record](sources/the_music_of_the_primes.tex) |

The Navier–Stokes volume orients the full Millennium problem. Its programme crosswalk points to the narrower `NS-CI-001` critical-integrability campaign and must not be read as an identity between those scopes.

## Editorial form

The series uses cream parchment, deep navy, restrained gold, classical serif typography, ornamental framing, luminous mathematical imagery, explanatory prose, explicit theorem boundaries, and technical appendices that deepen rather than merely repeat the lay account.

## Artifact authority and preservation

Git stores the public web records, archival source-record pointers, metadata, schemas, and validation contracts. The committed `.tex` pointer files are **source records**, not the complete compilable projects.

For each volume:

- the checksum-locked complete illustrated source bundle is the **authoritative source artifact**;
- the checksum-locked PDF is the **rendered edition**;
- the Markdown page is a derivative **web record or web edition**;
- byte lengths, SHA-256 digests, programme crosswalks, and release availability are fixed in [`ARTIFACT_MANIFEST.json`](ARTIFACT_MANIFEST.json).

All release-class artifacts are currently recorded as `metadata_only`: their identities are governed, but no stable public release locator is asserted. A checksum proves identity after a file is obtained; it does not itself establish publication or availability.

## Web-edition policy

The Poincaré page is the reference browser-native implementation. Its reusable content contract is defined by [`documentary_web.schema.json`](documentary_web.schema.json) and [`poincare.edition.json`](poincare.edition.json). MathJax is a version-pinned network enhancement; the source TeX remains in the document when JavaScript is unavailable, and archival identity belongs to the PDF and complete source bundle.

## Reading order

There is no required order. A reader seeking geometry may begin with Poincaré or Hodge; arithmetic with BSD or Riemann; physical law with Navier–Stokes or Yang–Mills; computation with P versus NP. Each volume begins again from first principles.
