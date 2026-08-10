# ADR-0018 — Governed visual-pedagogy reform

**Date:** 2026-08-09  
**Status:** Human Steward strongly approved for bounded pilot; protected merge required for repository authority  
**Docket:** `MP-DOC-VISUAL-PEDAGOGY-001`  
**Council disposition:** `VISUAL_PEDAGOGY_REFORM_APPROVED_FOR_BOUNDED_PILOT`  
**Canonical tracker:** MATH-PROGRAMME issue #377

## Context

The documentary library currently uses native SVG plates as its dominant visual-production method. SVG remains a capable and appropriate format for exact diagrams, graphs, labels, overlays, finite constructions, and other intrinsically vector objects. The defect identified by the Council is therefore not the SVG standard itself. It is an SVG-first production policy that asks a small vocabulary of generated vector primitives to carry mathematical geometry, fields, dynamics, numerical data, topology, and spatial relationships that the resulting plates do not actually express.

The bounded visual audit found a more serious problem than style. Some concept-defining plates are so schematic that their visible semantics do not support the mathematical relation asserted by their title, description, caption, or nearby prose. A polished but semantically false or underdetermined image can teach a stronger wrong intuition than no image at all.

ADR-0010 remains the documentary-library authority and discovery contract. This ADR extends documentary governance with a visual-semantic fidelity layer. It does not supersede ADR-0010 and does not allow a visual artifact to acquire mathematical evidentiary authority.

## Human Steward authorization

The Human Steward strongly approved Council docket `MP-DOC-VISUAL-PEDAGOGY-001` and authorized the bounded visual-pedagogy reform pilot under the disposition `VISUAL_PEDAGOGY_REFORM_APPROVED_FOR_BOUNDED_PILOT`.

The authorized operation shall:

1. audit the current MATH-PROGRAMME documentary visual inventory and classify each existing plate as `KEEP`, `REDRAW`, `REPLACE`, or `RETIRE`;
2. establish a governed visual-semantic contract distinguishing exact, data-derived, simulation-derived, schematic, metaphorical, and historical representations;
3. replace SVG-first production with a medium-neutral pipeline in which the mathematical representation is selected before its delivery format;
4. permit SVG, PNG/WebP, JPG, PDF, and motion or interactive media according to their appropriate mathematical and documentary roles;
5. require provenance and reproducibility for data-derived, simulation-derived, and computationally rendered visual artifacts;
6. preserve explicit claim boundaries so that visual exposition cannot acquire mathematical evidentiary or certification authority;
7. preserve the identity and disposition of superseded documentary assets rather than silently overwriting the historical record;
8. implement a bounded reference pilot of approximately six to ten plates spanning materially different mathematical visualization problems, including difficult geometric, analytic, dynamical, arithmetic, and diagrammatic cases;
9. subject the pilot to independent visual-semantic and domain-sensitive review; and
10. withhold programme-wide migration until the pilot has demonstrated mathematical fidelity, pedagogical utility, accessibility, provenance integrity, and satisfactory web and archival delivery.

No mathematical claim is promoted by this authorization. Full documentary-library propagation requires a subsequent governed disposition based on the completed pilot evidence.

## Decision

MATH-PROGRAMME adopts **representation first; delivery format second** for the bounded pilot.

The canonical production graph is:

```text
mathematical source
  -> domain renderer or exact construction
  -> annotated master
  -> reviewed visual-semantic contract
  -> delivery derivatives
       |- SVG
       |- PNG / WebP
       |- JPG
       |- PDF
       `- motion / interactive representation
```

No output format is authoritative merely by being canonical, lossless, vector, high resolution, or reproducible. Mathematical authority continues to reside in the governed claim/support route.

## Representation classes

Every governed pilot plate declares exactly one primary representation class:

- `exact` — represented spatial, combinatorial, symbolic, or data relationships are intended literally;
- `data-derived` — visible quantities are rendered from identified exact or numerical data;
- `simulation-derived` — visible states are rendered from a recorded computational process;
- `schematic` — explanatory relations are intentional but geometry, scale, placement, or multiplicity may be nonliteral;
- `metaphorical` — the plate is intentionally nonliteral and exists as a mnemonic or conceptual bridge;
- `historical` — the plate is a documentary witness, facsimile, photograph, scan, or faithful reproduction of an external historical object.

A plate must separately state which visual semantics are literal and which are nonliteral.

## Media roles

The pilot uses the following default roles, subject to the mathematical object rather than the file extension:

| Medium | Default role |
|---|---|
| SVG | exact diagrams, dependency graphs, reductions, commutative diagrams, simple constructions, labels, axes, and overlays |
| PNG | lossless rich mathematical/scientific rendering, especially fields, surfaces, dense plots, rendered geometry, and fixed teaching plates |
| WebP | optimized web derivative of appropriate raster imagery |
| JPG | historical or photographic continuous-tone material where lossy compression is acceptable; not the default for equation-heavy mathematical figures |
| PDF | canonical composed print/review/archive plate combining vector typography, equations, raster imagery, citations, and provenance |
| motion / interactive | intrinsically dynamical processes, with an accessible static fallback |

## Visual-semantic rule

> No theorem-bearing or concept-defining visual may use an unlabeled schematic as though it were a literal mathematical representation.

A caption cannot cure an image whose visible geometry materially contradicts the represented mathematics. Conversely, a deliberately schematic or metaphorical visual remains permitted when its nonliteral status and intended teaching role are explicit.

## Pedagogical composition

Where the concept is sequential, the preferred visual grammar is:

```text
Orientation -> Construction -> Invariant or relation -> Consequence
```

A single plate should not silently compress several mathematically distinct transformations when staged presentation would make the dependency visible.

## Provenance and reproducibility

For `data-derived` and `simulation-derived` plates, retain where applicable:

- bound source data or an immutable source reference;
- generator or renderer identity;
- parameters needed to reproduce the mathematical content;
- exact output identity or digest for retained canonical artifacts;
- annotation source and any transformations applied after rendering;
- an explicit statement of which visible quantities are mathematically meaningful.

A reproducible rendering is still not a proof unless the underlying support route independently carries that status.

## Continuity and supersession

The pilot must not silently overwrite existing documentary plate identities. Each audited plate receives `KEEP`, `REDRAW`, `REPLACE`, or `RETIRE`. Superseded assets remain identifiable through the audit record and, where repository history alone would be insufficient for interpretation, through explicit predecessor/successor references.

`REDRAW` means the conceptual role survives but the visual encoding requires material correction. `REPLACE` means the present visual grammar is unsuitable for the concept and a different representation is required. `RETIRE` removes a visual role without implying that the surrounding mathematical text is false. `KEEP` preserves an asset subject to ordinary review and accessibility obligations.

## Bounded pilot

The bounded reference set contains eight materially different cases:

- Poincaré Ricci-flow geometry/evolution — `REPLACE`;
- Poincaré controlled surgery — `REPLACE`;
- Navier–Stokes vortex stretching — `REPLACE`;
- Riemann critical strip and zero structure — `REPLACE`;
- Birch–Swinnerton-Dyer arithmetic curve example — `REDRAW`;
- Hodge cycle/class visualization — `REDRAW`;
- P-vs-NP reduction — `KEEP`, exact diagrammatic SVG positive control;
- Euclid Book VII repeated subtraction — `KEEP`, exact discrete/historical-concordance SVG positive control.

The pilot deliberately includes positive SVG controls so that reform cannot collapse into a blanket rasterization policy.

## Implemented first-stage evidence

The first-stage governance and contract layer has now closed two authorized obligations without closing the pilot itself:

1. `governance/documentary_visual_pedagogy_pilot_audit.json` enumerates all 45 current documentary visual assets at baseline protected `main` `839e04e1b862ffddfe5ce1d4d733ba954cd45d96`, binds exact predecessor Git blob identities, and records 19 `KEEP`, 21 `REDRAW`, 5 `REPLACE`, and 0 `RETIRE` dispositions. The record distinguishes rendered visual review from source/context-only first-pass classification and does not misstate either as independent domain review.
2. Eight machine-readable pilot contracts under `governance/visual_pedagogy/plates/` are schema-bound by `schemas/documentary_visual_plate.schema.json`. `ci/validate_documentary_visual_pedagogy.py`, its adversarial unit tests, and integration through the governed documentation-policy root enforce inventory identity, contract shape, provenance declarations, accessibility declarations, positive-control presence, and the hard `visual_is_evidence: false` boundary.

These mechanical controls establish auditable documentary state. They do not establish mathematical visual fidelity.

## Review and propagation gate

Pilot completion still requires implementation of the six corrective successor visuals and independent visual-semantic and domain-sensitive review of all eight pilot cases. Programme-wide migration remains unauthorized until a later governed disposition confirms that the pilot demonstrates:

1. mathematical fidelity;
2. pedagogical utility;
3. accessibility;
4. provenance integrity;
5. satisfactory web delivery;
6. satisfactory archival/print delivery.

The later disposition may approve, condition, modify, block, or reject propagation.

## Authority boundary

This ADR changes how the Programme governs visual exposition. It does not:

- certify a theorem;
- promote a mathematical claim;
- make a visualization proof evidence;
- alter the support class of any documentary claim;
- authorize full-library replacement;
- silently supersede ADR-0010.

## Required governed outputs

The bounded operation must leave behind:

- a whole-library plate audit — **first-pass identity/disposition audit complete**;
- the visual-semantic standard — **complete for bounded pilot**;
- machine-readable plate metadata/schema — **complete for the eight-case pilot set**;
- reproducibility and provenance rules — **contract established; successor renderer records still required where applicable**;
- the bounded pilot successor assets and their source/generator records — **pending for six corrective cases; two exact SVG controls retained**;
- independent review evidence — **pending**;
- Amanuensis continuity evidence — **active; final ledger/terminology/cross-document integration pending**;
- a final pilot disposition controlling any proposed propagation — **pending**.
