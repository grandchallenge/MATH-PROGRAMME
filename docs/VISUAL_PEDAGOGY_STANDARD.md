# Documentary Visual Pedagogy Standard

## Status

Binding standard for the bounded pilot authorized by `MP-DOC-VISUAL-PEDAGOGY-001` and ADR-0018. It does not authorize programme-wide documentary migration.

## Governing compact

Choose the mathematical representation before choosing the delivery format.

A documentary visual succeeds only when a reader can distinguish:

1. the mathematical object being represented;
2. the relation, obstruction, invariant, transformation, or datum that the visual is meant to teach;
3. which visible features are literal;
4. which visible features are schematic or metaphorical;
5. the source, generator, or witness from which the visual was produced;
6. the mathematical claim boundary.

A beautiful image that obscures any of these distinctions is not Grand Challenge pedagogy.

The converse is now also binding for the pilot: semantic safety alone is not sufficient. A corrective image that merely avoids error but produces no memorable mathematical intuition is unfinished.

## Representation classes

Every governed plate declares one primary class.

### `exact`

Spatial, combinatorial, symbolic, graph, or data relationships are intended literally within stated conventions. Examples include reduction diagrams, commutative diagrams, exact finite constructions, correctly scaled plots, and verified coordinate drawings.

### `data-derived`

The visible structure is rendered from identified exact or numerical data. The data source, transformation, plotting convention, and mathematically meaningful encodings must be recoverable.

### `simulation-derived`

The visible structure is rendered from a recorded computational process. Initial conditions, relevant parameters, method identity, and the scope of any numerical approximation must be stated or linked.

### `schematic`

The image teaches a relation or organization while some geometry, scale, placement, multiplicity, or appearance is deliberately nonliteral. Those nonliteral dimensions must be disclosed.

### `metaphorical`

The image is intentionally nonliteral and serves as a mnemonic, analogy, or conceptual bridge. It must not masquerade as a mathematical model, plot, geometry, or computation.

### `historical`

The image is a documentary witness: a facsimile, scan, photograph, archival diagram, manuscript page, or faithful reproduction of an external historical object. Its provenance must identify the witnessed source.

## Literal-semantics contract

Every plate must state both:

- `literal_semantics`: the visible properties the reader is permitted to interpret mathematically;
- `nonliteral_semantics`: visible properties that must not be interpreted mathematically.

The second field may be empty only when the plate is genuinely exact under the declared conventions.

The following rule is binding:

> No theorem-bearing or concept-defining visual may use an unlabeled schematic as though it were a literal mathematical representation.

A caption cannot repair a material contradiction between the visible geometry and the represented mathematics. If the image is intentionally nonliteral, label it before the reader is likely to draw the wrong inference.

## Production graph

```text
mathematical source or documentary witness
  -> domain renderer / exact construction / reproduction process
  -> annotated master
  -> literary-pedagogical composition
  -> visual-semantic and visual-quality review
  -> delivery derivatives
```

The annotated master is the composition source for the pedagogical object. Delivery derivatives are not required to share one file format.

For the bounded pilot, unapproved successor images live outside `docs/assets/documentaries/`. They are review candidates, not admitted documentary assets. Promotion into the live documentary namespace requires the recorded independent review and a subsequent governed publication transition.

## Delivery formats

### SVG

Prefer SVG when the mathematical content is naturally vectorial and its semantics can be represented exactly or clearly: dependency graphs, reductions, commutative diagrams, proof-state diagrams, timelines, simple geometric constructions, finite combinatorics, axes, labels, and overlays.

Do not select SVG merely because previous documentary plates used SVG.

### PNG

Prefer PNG for lossless fixed renderings in which raster structure is intrinsic or convenient: scalar/vector fields, dense analytic plots, rendered manifolds or surfaces, phase portraits, scientific visualization, exact raster exports, and composed teaching frames.

### WebP

Use WebP as a web-delivery derivative when it materially improves transfer size while preserving the pedagogically relevant content. Keep a provenance link to the canonical source/master.

### JPG

Use JPG primarily for continuous-tone historical or photographic material when lossy compression is acceptable. Do not make JPG the default for mathematical linework, small text, equations, or plots requiring sharp pixel boundaries.

### PDF

Use PDF for canonical composed print/review/archive plates when vector equations, labels, citations, provenance, and raster scientific imagery need to coexist. PDF is a delivery and archival container, not a proof authority.

### Motion and interaction

Use motion or interaction when temporal evolution, parameter change, spatial navigation, or staged transformation is part of the mathematics being taught. Provide an accessible static fallback that preserves the essential relation and claim boundary.

## Composition grammar

For processes or multi-stage concepts, prefer:

```text
Orientation -> Construction or transformation -> Invariant or relation -> Consequence or boundary
```

Each stage should introduce a bounded visual fact. Do not compress several logically distinct changes into one icon when the compression forces the reader to infer the mathematics.

Composition is not synonymous with a card grid. The mathematical object or process should normally dominate the plate. Definitions, equations, captions, process sequences, historical cues, and claim-boundary notes should orbit that object in a hierarchy appropriate to the subject.

## Literary visual quality

The bounded pilot adopts `PC-001-VISUAL-QUALITY-REFERENCE` in `governance/visual_pedagogy/quality_reference_pc001.json` as its first positive literary-visual reference. The reference is *The Shape of a Sphere*, whose checksum-locked rendered PDF is already identified by the Documentary Library manifest.

The reference does not require later work to imitate PC-001's palette, ornament, typography, or specific artwork. Its binding lesson is structural: a Grand Challenge plate may be beautiful, atmospheric, and emotionally memorable while remaining exact about what the reader is and is not entitled to infer.

A mature plate should therefore aim for all of the following:

1. **Memorable true mental model.** It does more than remove a false picture; it gives the reader a durable substantially true picture within the declared representation class.
2. **Hero composition.** The principal mathematical object or process owns the visual hierarchy. Annotation serves the object rather than turning the plate into a dashboard.
3. **Narrative movement.** The eye can follow a mathematical question, transformation, obstruction, invariant, reconstruction, or consequence.
4. **Atmosphere with semantic discipline.** Texture, depth, scientific ornament, and visual wonder may be used freely when they do not impersonate data, scale, topology, multiplicity, or proof evidence.
5. **Annotation economy.** Definitions, equations, and callouts are sufficient to stabilize interpretation but sparse enough to preserve visual composition.
6. **Precision ladder.** The plate hands the reader to prose, equations, appendices, and sources. Higher-resolution layers restore detail without declaring the visual intuition fraudulent.
7. **Claim-boundary legibility.** Important nonliteral departures and the non-evidentiary status remain findable without becoming the visual subject.
8. **Literary coherence.** The plate feels authored for its mathematics and documentary. A subject-independent template is not a substitute for composition.

The positive rule is binding:

> A corrective visual is not complete merely because it eliminates a false mental model. It should also create a memorable true one.

The programme-level aspiration is:

> Grand Challenge visual pedagogy should combine the beauty of a scientific plate, the clarity of a proof sketch, and the imaginative force of an illustrated book—without confusing any of those with proof.

Beauty cannot be reduced to a checksum or schema. Mechanical validation may establish identities, provenance, accessibility fields, and declared boundaries. Independent review must judge whether the plate actually achieves pedagogical revelation, compositional coherence, and visual delight without sacrificing mathematical fidelity.

## Mathematical fidelity

A visual-semantic review asks at minimum:

- Does the object shown have the right mathematical type and dimension for the intended lesson?
- Are axes, units, coordinates, scale, multiplicity, direction, topology, and time literal when the plate invites the reader to treat them literally?
- Are plotted curves, points, fields, surfaces, or states generated from the stated object rather than aesthetically invented substitutes?
- Does every highlighted relation appear in the image?
- Does the image omit a feature that the caption or description claims is visible?
- Could an informed reader acquire a materially false mental model from the representation?
- Are schematic and metaphorical departures disclosed before they can mislead?

Passing a JSON schema does not answer these questions. The schema establishes an auditable contract; independent review establishes whether the visible artifact honors it.

## Provenance and reproducibility

`data-derived` and `simulation-derived` plates must retain, as applicable:

- source dataset, exact object, or immutable source reference;
- generator or renderer identifier;
- renderer version or environment where material;
- parameters and plotting conventions needed to reproduce mathematical content;
- relevant random seed if stochastic output materially affects the image;
- canonical master identity and digest when retained;
- derivative identities;
- post-render annotation operations;
- a statement distinguishing mathematical encodings from aesthetic choices.

`exact` generated plates should retain their construction source when the final asset alone is not sufficient to audit correctness.

## Accessibility

Every reader-facing plate requires meaningful alternative text. A complex plate also requires a long description or equivalent adjacent semantic explanation sufficient to recover the intended structure without the image.

Alternative text must describe the mathematical teaching content, not merely visual appearance. Decorative or repeated imagery may remain hidden only when the same semantic content is already available in adjacent accessible structure.

Motion must not be the sole carrier of essential information. Interactive content must provide a keyboard-accessible route where the interaction itself is reader-facing.

## Authority boundary

A visual may orient, explain, reconstruct, compare, or expose a structure. It cannot independently promote a mathematical claim.

For every plate:

- the mathematical claim/support route remains separately governed;
- reproducibility of rendering does not imply proof;
- a simulation frame is not a continuum theorem;
- a verified plot is not a universal quantifier;
- a historical witness is not present Programme authority;
- a schematic is not a literal model unless the contract states which relations are exact.

## Audit dispositions

Every existing documentary plate receives exactly one audit disposition:

- `KEEP` — retain the current visual role and asset, subject to the new contract;
- `REDRAW` — retain the conceptual role but materially correct or enrich the visual encoding;
- `REPLACE` — the current visual grammar is unsuitable; create a different representation;
- `RETIRE` — remove the visual role without implying that surrounding prose or mathematics is false.

The audit must preserve predecessor identity and the reason for disposition.

## Pilot review gate

The bounded pilot must span materially different representational problems and include at least one case where SVG remains appropriate. Before any proposal for programme-wide propagation, independent reviewers must assess:

- mathematical fidelity;
- pedagogical revelation and utility;
- memorable true mental model;
- compositional coherence;
- visual wonder and delight;
- annotation economy;
- accessibility;
- provenance and reproducibility;
- web behavior;
- print/archive behavior;
- supersession continuity;
- claim-boundary integrity.

Only a later governed disposition may authorize migration beyond the bounded pilot.
