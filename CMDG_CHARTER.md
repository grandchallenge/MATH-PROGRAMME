# CMDG_CHARTER.md

## Status

**Programme:** CMDG — Certified Reconstruction of the Mathematical Dependency Graph  
**Operation:** `CMDG-CHARTER-001`  
**Authority:** ADR-0017; `HUMAN_STEWARD_RATIFIED_WITH_COUNCIL_CORRECTIONS`  
**Council disposition:** `RATIFY_WITH_CORRECTIONS`  
**Charter state:** protected and active  
**Protected authority baseline:** `e456df8741b707af94012ec45b0341424e44157a`  
**Protected admission:** PR #293 at reviewed head `86238812d6b130378abd1da5bce06e8be5607769`; merge `799a6161f2700c6ffb52848cbf6d007c988398a8`  
**Independent review:** `jimsteeg` — `APPROVED` — 2026-08-08

This charter translates the ratified CMDG conception into the governing programme contract for implementation. It does not replace the protected I–XIX programme memorial or ADR-0017. The memorial preserves the originating conception; ADR-0017 records the ratified decision and Council corrections; this charter governs execution under that authority.

---

## 1. Mission

CMDG shall construct a machine-readable, machine-checked, provenance-bearing reconstruction of the dependency architecture of modern mathematics, from formal logic and foundational systems through structural mathematics, category theory, topology, analysis, sheaf and homological machinery, and demanding modern frontiers such as Condensed Mathematics.

CMDG treats mathematics not merely as a collection of individually checked theorems, but as a dependency-bearing structure of definitions, constructions, equivalences, models, interpretations, and proofs.

The programme objective is therefore twofold:

1. certify mathematical results at their proper theorem or certificate level; and
2. certify the declared dependency structure by which selected results are reconstructed, realized, checked, sourced, and replayed.

The second objective is additional to the first. Machine checking alone does not establish dependency certification.

---

## 2. Grand Challenge closure condition

The long-term Grand Challenge is satisfied only when a substantial modern mathematical theorem, selected under a protected frontier contract, is reachable through a completely certified dependency path from the declared formal substrate, with every material dependency on that path:

- represented by an identified node or declared boundary;
- connected by typed dependency or realization relations;
- separated across semantic, proof, implementation, and provenance layers;
- provenance-bound at the declared trust level;
- accompanied by an explicit foundational and axiom footprint where applicable; and
- independently replayable under a pinned environment.

This closure condition is bounded by the governing manifest and trust boundary. It does not mean that all mathematics has been formalized, that every fact relevant in an informal historical sense has been globally enumerated, or that every imported theorem has been independently reproved.

---

## 3. Scope and non-goals

CMDG is not another attempt to duplicate mathlib, re-formalize all mathematics from first principles, or replace existing formal libraries.

CMDG admits three programme engagement modes:

### 3.1 `REUSED`

An upstream mathematical or formal artifact is retained at a declared trust level. Its identity, source, implementation location, foundational profile, and dependency boundary are recorded. Reuse does not by itself imply semantic completeness or independent proof.

### 3.2 `RECONSTRUCTED`

A mathematical object, theorem, construction, or dependency path is deliberately rebuilt within the Programme to expose or certify its dependency structure.

### 3.3 `CONCORDANT`

Two or more foundational or formal presentations of a mathematical object are related through explicit interpretation, equivalence, universal-property, or transport obligations. Shared naming or informal analogy is insufficient.

The principal CMDG scientific object is the certified dependency structure produced across these modes.

---

## 4. Existing MATH-PROGRAMME architecture remains in force

CMDG operates through the existing three-pillar architecture:

```text
MATHFORGE  ->  MATHSOLVE  ->  MATHCERT
discover       attack         certify
```

The pillar split is not replaced by CMDG.

### 4.1 MATH-PROGRAMME

MATH-PROGRAMME owns:

- CMDG ontology and programme authority;
- canonical graph contracts;
- certification semantics;
- manifest and schema standards;
- demonstration and certified spine definitions;
- foundational-concordance policy;
- frontier registries;
- governance, claim boundaries, and change control.

### 4.2 MATHFORGE

MATHFORGE owns:

- historical and modern source reconstruction;
- library and literature reconnaissance;
- theorem and source identity;
- candidate dependency assertions;
- source-derived provenance evidence.

MATHFORGE assertions are candidate ore until promoted through the governing review route.

### 4.3 MATHSOLVE

MATHSOLVE owns:

- definition and theorem spines;
- dependency reductions;
- foundational-concordance work packages;
- missing-node analysis;
- mathematical reconstruction and campaign work.

### 4.4 MATHCERT

MATHCERT owns:

- proof and certificate replay;
- proof dependency extraction;
- axiom and classicality extraction;
- semantic-to-formal concordance checking;
- graph-certification verification;
- independent clean-environment replay.

Repository location does not confer mathematical authority by itself.

---

## 5. Canonical mathematical object

CMDG models the selected mathematical architecture as a typed directed multigraph

```text
G = (V, E, τV, τE)
```

where `V` is a set of identified nodes, `E` is a set of typed directed edges, `τV` assigns node classes, and `τE` assigns edge classes.

The initial semantic node classes are:

- `Definition`;
- `Theory`;
- `Structure`;
- `Construction`;
- `Theorem`;
- `Equivalence`;
- `Model`.

The initial semantic relation vocabulary includes:

- `REQUIRES_DEFINITION`;
- `USES_THEOREM`;
- `CONSTRUCTS`;
- `INSTANTIATES`;
- `GENERALIZES`;
- `INTERPRETS`;
- `MODELS`;
- `EQUIVALENT_TO`;
- `TRANSPORTS_ALONG`;
- `USES_AXIOM`;
- `USES_CLASSICALITY`;
- `SOURCE_DERIVED`.

Cross-layer and implementation relations are governed separately below. `CMDG-SCHEMA-001` may refine the machine vocabulary, cardinalities, required fields, and admissible source/target type pairs, but it may not silently erase the distinctions fixed by this charter.

---

## 6. Four dependency layers

CMDG SHALL preserve four distinct dependency layers.

### 6.1 `G_semantic`

The mathematical dependency graph. It records what definitions, constructions, theorems, models, interpretations, axioms, or other mathematical objects are materially required for the selected mathematical claim or object under the reviewed semantic account.

### 6.2 `G_proof`

The checked-proof dependency graph. It records declarations, lemmas, proof terms, certificates, axioms, or other formal objects actually consumed by the checked proof or verifier.

### 6.3 `G_implementation`

The implementation and library graph. It records files, modules, package imports, build dependencies, toolchain components, and other software-level dependencies.

### 6.4 `G_provenance`

The documentary graph. It records sources, editions, archival identities, reviews, exact-head evidence, receipts, and other provenance-bearing artifacts.

### 6.5 Non-conflation rule

No edge in one layer becomes an edge in another layer merely because the endpoints share names or appear in the same implementation.

In particular:

```text
implementation import != semantic dependency
proof dependency          != semantic dependency
source citation            != proof dependency
machine-checked            != GRAPH_CERTIFIED
```

A cross-layer relationship requires an explicit realization or evidence relation governed by this charter and later schemas.

---

## 7. Direct edges and computed closure

CMDG SHALL distinguish direct reviewed dependency edges from computed transitive closure.

A direct semantic edge asserts a reviewed immediate dependency under the governing semantic model. It must carry its own evidence or provenance reference.

A transitive relation produced by graph traversal is derived data. It SHALL NOT be stored or presented as a direct reviewed edge unless it has independently undergone the direct-edge review contract.

The governing manifest SHALL state the closure policy used for any certification claim. A closure policy may define, for example:

- which edge types participate in dependency reachability;
- whether direction is traversed only from dependent to prerequisite;
- which boundary nodes terminate traversal;
- how realization relations are crossed;
- how certified equivalence components are treated;
- how cycles and repeated nodes are normalized.

The closure policy is part of the meaning of a graph-certification claim and must be versioned.

---

## 8. Canonical semantic-to-formal realization relation

To satisfy the charter-level requirement of `CMDG-C02`, CMDG adopts `REALIZES_AS` as the canonical cross-layer relation from a semantic mathematical node to a formal or computational realization.

A `REALIZES_AS` assertion SHALL identify at minimum:

- the semantic source node;
- the formal or computational target identity;
- the realization kind;
- the scope of correspondence claimed;
- the evidence supporting the mapping;
- the proof environment or implementation locator when applicable;
- any known mismatch, restriction, universe condition, or boundary.

`REALIZES_AS` does not automatically assert definitional equality, mathematical equivalence, source-faithful identity, or foundational concordance. Those stronger claims require their own typed relation and certification evidence.

A formal declaration's presence in an imported module SHALL NOT create `REALIZES_AS` automatically. The mapping is an explicit reviewed assertion.

Future schemas may define subtypes of `REALIZES_AS`; they must preserve this non-conflation rule.

---

## 9. Equivalence, cycles, and quotient projections

The canonical CMDG object is a typed directed multigraph, not an ordinary dependency DAG.

Mathematics contains equivalences, mutual characterizations, and interpretation cycles. CMDG therefore permits cycles where the underlying mathematics requires them.

For purposes that require an acyclic projection, an equivalence component MAY be collapsed only when every edge used to generate the quotient component is explicitly marked as an admissible certified equivalence-generating edge under the governing ontology and manifest.

The following are prohibited:

- quotienting merely because two nodes have similar names;
- quotienting merely because two declarations are definitionally convenient aliases;
- quotienting from an unreviewed `EQUIVALENT_TO` assertion;
- using implementation aliasing to launder a mathematical equivalence;
- using a one-way interpretation as if it were a certified equivalence.

Any acyclic projection SHALL retain traceability to the uncollapsed graph and to the evidence that authorized each quotient component.

---

## 10. Foundational policy

CMDG treats foundations as an explicit stack of substrates, theories, interpretations, and realizations rather than an undifferentiated contest between labels such as DTT and ZFC.

### 10.1 Operational substrate

Lean dependent type theory is the preferred operational proof substrate for the initial CMDG programme.

### 10.2 Object theories

ZF, ZFC, first-order theories, categorical foundations, or other foundational systems may be formalized or represented as object theories or mathematical realizations within the operational substrate.

Formalizing an object theory inside Lean does not prove that theory consistent. A theorem proved about a formalized proof calculus does not erase the distinction between metatheory and object theory.

### 10.3 Logic before set-theoretic object theory

The foundational reconstruction route SHALL distinguish object-level first-order syntax and proof theory from Lean's own metatheory. The intended logic layer includes, as appropriate:

- terms and formulas;
- binding and substitution;
- proof rules;
- interpretations and models;
- satisfaction;
- soundness;
- completeness;
- compactness.

Using Lean to prove a theorem about first-order logic is not by itself equivalent to representing the object proof system and its semantics.

### 10.4 Foundational profiles

Where mathematically material, CMDG artifacts SHALL record foundational information such as:

- proof substrate;
- object theory or realization;
- choice or excluded-middle dependence;
- quotient or extensionality assumptions;
- universe conditions;
- interpretation bridge;
- known constructive or classical boundary.

Existing `foundational_profile` machinery in the Programme claim-ledger contract remains available and may be extended only through governed schema changes.

---

## 11. Existing theorem certification ladder remains unchanged

The Programme Level 0–5 certification ladder remains authoritative:

- Level 0: intake and source status;
- Level 1: reproducible exploration;
- Level 2: exact computation or exhaustive finite certificate;
- Level 3: formal statement scaffold;
- Level 4: machine-checked local lemmas or reductions;
- Level 5: machine-checked theorem or replayable certificate theorem.

CMDG does not replace, renumber, or weaken these levels.

`GRAPH_CERTIFIED` is orthogonal to this ladder.

---

## 12. Manifest-relative `GRAPH_CERTIFIED` contract

This section is the charter-level incorporation of `CMDG-C01`.

### 12.1 Relative status

A CMDG graph-certification assertion SHALL have the form conceptually equivalent to:

```text
GRAPH_CERTIFIED(root, manifest)
```

It means that the dependency path rooted at `root` satisfies the CMDG graph-certification obligations **relative to the exact versioned manifest named by the assertion**.

It does not mean that the Programme has globally enumerated every mathematically relevant dependency, every historical influence, every alternative proof route, or every theorem in mathematics.

### 12.2 Root eligibility

For theorem or certificate roots governed by the Level 0–5 ladder, a production `GRAPH_CERTIFIED` claim requires the root mathematical claim to satisfy Level 5 or the exact replayable-certificate equivalent admitted by the Level 5 contract.

The future node schema may define dependency-certification states for definitions, structures, models, constructions, or other non-theorem nodes. Such states SHALL NOT be represented as theorem-level `GRAPH_CERTIFIED` claims unless their semantics are explicitly defined.

### 12.3 Required manifest identity

Every graph-certification manifest SHALL be immutable by version and shall bind at minimum:

- `manifest_id` and manifest version;
- certification root identity;
- ontology version;
- applicable schema versions;
- direct semantic dependency assertions for the governed root or path;
- the declared closure policy;
- boundary nodes and their trust classes;
- semantic-to-formal realization bindings;
- proof environment identity and pins;
- axiom footprint;
- classicality footprint;
- reviewed semantic-edge evidence;
- implementation dependency references sufficient for replay;
- provenance references sufficient to identify the source basis;
- replay evidence or the exact replay obligation;
- unresolved obligations, if any.

A production `GRAPH_CERTIFIED` manifest SHALL have no unresolved obligation that falls inside the declared certification boundary.

### 12.4 Boundary discipline

A boundary node terminates an internal reconstruction obligation only when the manifest explicitly states:

- the boundary node identity;
- why it is outside the current reconstruction boundary;
- its trust class;
- the evidence or authority under which it is accepted;
- whether it may be traversed for provenance, proof, or implementation purposes.

Undocumented imports, opaque assumptions, unclassified external oracles, and unnamed library trust are not valid boundary declarations.

### 12.5 Completeness semantics

`GRAPH_CERTIFIED(root, manifest)` asserts completeness only with respect to:

1. the manifest's declared semantic scope;
2. the reviewed direct-edge discipline;
3. the declared closure policy;
4. the declared boundary and trust classes; and
5. the pinned proof and replay environment.

The certification claim SHALL be invalidated or superseded when a material dependency within that declared scope is shown to be missing, misclassified, unsupported, stale, or incorrectly realized.

### 12.6 Axiom and classicality discipline

The manifest SHALL distinguish axioms and classicality introduced by:

- the operational proof substrate;
- imported formal declarations;
- the root proof;
- foundational object-theory assumptions;
- boundary trust.

Axiom extraction alone is not a semantic dependency audit; semantic review alone is not an axiom extraction. Both are required where applicable.

### 12.7 Replay discipline

A production graph-certification claim SHALL identify a pinned environment and replay route capable of reconstructing the checked formal evidence and the governed dependency verification from a clean state, subject only to explicitly declared boundary services or artifacts.

### 12.8 Schema gate remains

This charter fixes the normative semantics required by `CMDG-C01`. `CMDG-C01` is not fully discharged for schema finalization until `CMDG-SCHEMA-001` encodes these requirements in machine-checkable contracts and demonstrates that malformed or incomplete manifests fail closed.

No production `GRAPH_CERTIFIED` status is authorized by this charter alone.

---

## 13. Cross-layer realization and graph reconciliation contract

This section completes the charter-level incorporation of `CMDG-C02`.

### 13.1 Layer-preserving reconciliation

CMDG tooling SHALL be capable of comparing, without conflating:

- declared semantic dependencies;
- dependencies consumed by the checked proof;
- implementation imports and package dependencies;
- provenance assertions and source identities.

### 13.2 Required discrepancy classes

The future semantic graph reconciler SHALL at minimum be able to surface candidate cases of:

- unexpected proof dependency;
- declared semantic dependency absent from formal realization evidence;
- implementation-only dependency;
- proof-only helper with no claim of semantic materiality;
- introduced classicality or axiom use;
- foundation-boundary crossing;
- unresolved `REALIZES_AS` mapping;
- unsupported equivalence used for quotienting;
- direct-edge/transitive-closure confusion;
- stale or mismatched source or environment pin.

A discrepancy report is evidence for review; it does not automatically decide mathematical materiality.

### 13.3 Direct versus transitive discipline

Only direct reviewed semantic edges carry direct-edge authority. Computed closure may support navigation, audit, and certification traversal, but SHALL remain distinguishable from direct evidence.

### 13.4 Schema gate remains

This charter fixes `REALIZES_AS`, layer preservation, direct-edge discipline, and equivalence-quotient restrictions. `CMDG-C02` is not fully discharged for schema finalization until `CMDG-SCHEMA-001` encodes these relations and constraints in machine-checkable form.

---

## 14. Demonstration and certified spines

This section incorporates `CMDG-C08` as a continuing terminology and claim-discipline rule.

### 14.1 Demonstration spine

A **CMDG demonstration spine** is a selected end-to-end route used to exercise the dependency architecture across substantial mathematical layers.

A demonstration spine may contain incomplete, reused, reconstructed, or not-yet-certified segments provided each segment's status and boundary are explicit.

### 14.2 Certified spine

A **CMDG certified spine** is a demonstration spine whose included certification roots, dependency relations, realization mappings, boundaries, and replay obligations satisfy the certification contract declared for that spine.

The phrase `certified spine` does not imply that every theorem in the surrounding mathematical subject has been certified.

### 14.3 Prohibited overclaim

Neither `demonstration spine` nor `certified spine` asserts that a route is:

- mathematically minimal;
- historically canonical;
- the unique dependency path;
- the shortest proof route;
- the only valid foundational realization.

Minimality, canonicity, or uniqueness requires a separate explicit theorem, decision, or optimization criterion.

`CMDG-C08` is therefore incorporated as a permanent terminology constraint rather than a one-time implementation task.

---

## 15. Foundational concordance

Foundational concordance is a core CMDG scientific objective.

The first major experiment remains:

`CMDG-NAT-CONCORDANCE-001`

with intended presentations including:

- `N_DTT`;
- `N_ZFC`;
- `N_NNO`.

The experiment shall not promote merely because the presentations have similarly behaving carriers. It must state and check the appropriate interpretation, universal-property, equivalence, or transport obligations required by the selected foundational profiles.

The intended transported structure includes, subject to the work-package contract:

- zero;
- successor;
- addition;
- multiplication;
- order;
- divisibility.

`CMDG-C03` remains a blocking stage gate before promotion of this experiment. In particular, the set-theoretic realization must be declared syntactic, semantic, or both with an explicit bridge, and the NNO presentation must name its ambient category and universe conditions.

---

## 16. Euclid bridge

The first historical-to-foundational bridge remains:

`CMDG-EUCLID-BRIDGE-001`

Its purpose is to transport or recover the Programme's existing Euclidean arithmetic work, including the GCD exemplar, through the certified natural-number concordance route.

This bridge is intended to demonstrate continuity between the completed Euclid end-to-end certification work and the new dependency-reconstruction programme.

It shall not be used to claim foundational equivalence until the required concordance obligations have been certified.

---

## 17. Epoch architecture

CMDG retains the following programme epochs as a dependency-oriented planning structure:

| Epoch | Scope |
|---|---|
| F0 | Formal substrate: kernel, proof terms, universes, axiom census |
| F1 | Logic and metatheory: syntax, semantics, soundness, completeness, compactness |
| F2 | Arithmetic: `N`, `Z`, `Q`, recursion, induction |
| F3 | Set theory: formal ZF/ZFC object theory; ordinals and cardinals |
| F4 | Structural mathematics: algebra, order, modules, morphisms |
| F5 | Category theory: functors, naturality, Yoneda, limits, adjunctions |
| F6 | Spaces: topology, compactness, uniform and metric structures, profinite spaces |
| F7 | Analysis: real and complex analysis, measure, integration, functional analysis |
| F8 | Sheaf and homological mathematics: sites, sheaves, abelian categories, complexes, derived machinery |
| F9 | Condensed frontier: condensed sets, groups, modules, solid and liquid structures |

These epochs are not a claim that mathematics forms one total linear sequence. They may branch, merge, and interact through typed dependencies.

---

## 18. Demonstration spines V0, V1, and V2

The ratified programme retains three initial demonstration spines.

### 18.1 V0

```text
Lean/DTT substrate
  -> first-order logic
  -> natural numbers
  -> groups/rings
  -> categories
  -> topological spaces
  -> compact Hausdorff/profinite
  -> Grothendieck topologies
  -> sheaves
  -> condensed sets
  -> discrete/underlying adjunction
```

V0 is the thin architecture test.

### 18.2 V1

```text
rings/modules
  -> abelian categories
  -> chain complexes
  -> homology
  -> Grothendieck abelian categories
  -> condensed abelian groups/modules
```

V1 tests the homological route.

### 18.3 V2

```text
R/C
  -> topological vector spaces
  -> measure/integration
  -> functional analysis
  -> condensed modules
  -> solid/liquid mathematics
```

V2 is the intended full modern-load route.

These are demonstration spines unless and until their exact governed routes satisfy a declared certified-spine contract. No minimality, uniqueness, or historical canonicity is claimed.

---

## 19. Structural mathematics and categorical bridge

CMDG shall reconstruct the progression from elementwise structure to morphism and universal-property formulations where that progression is mathematically material.

Representative structural chains include:

```text
relation/operation
  -> magma
  -> semigroup
  -> monoid
  -> group
```

and

```text
ring
  -> module
  -> algebra
```

Representative universal-property translations include:

```text
product     -> categorical product
quotient    -> coequalizer, where appropriate
free object -> adjunction, where appropriate
```

The purpose is not historical reenactment. It is to expose the dependency transition from Bourbaki-style structures toward Grothendieck-style morphisms, universal properties, sites, sheaves, and homological machinery.

---

## 20. Condensed Mathematics frontier

Condensed Mathematics is the first major modern load test for CMDG. It is not treated as a fashionable endpoint detached from the foundational reconstruction.

The initial frontier stages remain:

- `CM0`: exact foundational definition and interface for selected condensed objects;
- `CM1`: discrete/underlying adjunction;
- `CM2`: Cartesian closedness of condensed sets under the pinned formal target;
- `CM3`: condensed abelian and homological structure;
- `CM4`: solid mathematics under a formally supported scope;
- `CM5`: a completely dependency-accounted route terminating in a substantial Liquid-Tensor-class Clausen–Scholze theorem or comparably demanding protected target.

`CMDG-C04` remains a blocking gate before CM0–CM2 promotion. The exact target definition and any cardinality or presentation concordance boundary must be pinned.

`CMDG-C05` remains a blocking gate before a general-ring CM4 claim. The Programme shall restrict to a formally supported ring regime or reconstruct the intended general definition rather than overstate an implementation.

Existing formal results may be reused at explicit trust levels. Reuse does not waive dependency identity, provenance, realization, or boundary requirements.

---

## 21. Historical geometry lane

The programme retains the lateral geometry lane:

```text
Euclid -> Hilbert -> Tarski -> formal geometry
```

This lane is connected principally to logic, foundational object theories, and structural mathematics. It is not on the mandatory V0 trunk unless a later protected decision places it there.

The lane shall distinguish reconstruction of Euclidean source arguments from later axiom systems that repair or replace implicit assumptions.

---

## 22. Stage-bounded Council corrections

The Council correction register remains binding.

| Correction | Charter status | Remaining gate |
|---|---|---|
| `CMDG-C01` | normative manifest-relative semantics fixed in Section 12 | machine schema and fail-closed enforcement before `CMDG-SCHEMA-001` finalization; production `GRAPH_CERTIFIED` still prohibited |
| `CMDG-C02` | `REALIZES_AS`, layer separation, direct-edge discipline, and quotient restrictions fixed in Sections 7, 8, 9, and 13 | machine schema and constraint enforcement before `CMDG-SCHEMA-001` finalization |
| `CMDG-C03` | preserved | exact ZFC profile and categorical NNO profile before `CMDG-NAT-CONCORDANCE-001` promotion |
| `CMDG-C04` | preserved | exact Condensed target and cardinality/concordance boundary before CM0–CM2 promotion |
| `CMDG-C05` | preserved | supported solid-module ring regime or reconstruction before general-ring CM4 claim |
| `CMDG-C06` | preserved | adversarial, mutation, stale-pin, and clean-replay gates before first production `GRAPH_CERTIFIED` artifact |
| `CMDG-C07` | discharged by protected Council authority closure | no remaining charter gate |
| `CMDG-C08` | incorporated as continuing terminology discipline in Section 14 | remains binding unless a later protected decision establishes minimality, uniqueness, or another stronger route property |

This charter SHALL NOT describe C01 or C02 as fully discharged merely because their normative semantics are now written. Their machine-enforcement obligations belong to `CMDG-SCHEMA-001` and `CMDG-VALIDATOR-001`.

---

## 23. Automated tooling mandate

CMDG shall develop three early tool classes.

### 23.1 Declaration Dependency Extractor

Extract formal declaration and proof dependencies from the pinned proof environment.

### 23.2 Axiom Footprint Extractor

Extract or replay the actual axiom and classicality footprint relevant to the governed formal root.

### 23.3 Semantic Graph Reconciler

Compare the declared semantic graph against the proof, implementation, realization, and provenance evidence without conflating the layers.

Automated extraction creates evidence. It does not automatically promote a semantic dependency assertion. Material semantic classification remains a governed review act until a later protected contract explicitly automates a bounded class of such judgments.

---

## 24. Adversarial and fail-closed doctrine

CMDG shall fail closed when certification-critical information is absent, malformed, stale, ambiguous, or outside the governing trust policy.

Before the first production `GRAPH_CERTIFIED` artifact, `CMDG-C06` requires retained adversarial or mutation fixtures covering at minimum:

- hidden classicality;
- import/semantic conflation;
- equivalence laundering;
- boundary laundering;
- alias inflation;
- transitive omission or direct-edge confusion;
- universe mismatch;
- source mismatch;
- stale pins;
- clean-environment replay failure.

A validator that merely accepts the happy path is not sufficient for production graph certification.

---

## 25. Provenance and source discipline

Every material semantic edge intended for certification SHALL be provenance-backed by one or more of:

- a governing mathematical source;
- a checked formal declaration plus reviewed semantic realization evidence;
- an independently replayable certificate;
- a protected reconstruction artifact whose claim boundary permits the edge assertion.

Provenance identifies why an assertion is admitted. It does not by itself prove a stronger mathematical claim than the source or artifact supports.

Source identity, theorem identity, formal declaration identity, and implementation file identity SHALL remain distinguishable.

---

## 26. Foundational fingerprint

Major CMDG certification roots shall be capable of carrying a foundational fingerprint that records, as applicable:

- prover or operational substrate;
- object foundational theory;
- exact axiom footprint;
- classicality footprint;
- semantic dependencies;
- foundational realizations;
- implementation dependencies;
- concordance or equivalence status;
- graph-certification manifest identity;
- replay environment.

The schema is deferred to the appropriate schema operation. The charter fixes the obligation, not its final serialization.

---

## 27. Claim-ledger integration

The existing canonical claim-ledger contract remains the trust spine for meaningful programme assertions.

CMDG SHALL NOT infer mathematical promotion from:

- repository merge;
- CI success;
- documentation publication;
- graph presence;
- source citation alone;
- implementation import alone;
- formal statement alone.

A CMDG graph assertion that materially supports a mathematical claim shall be traceable to the relevant claim ledger or to a dedicated dependency manifest whose relationship to the claim ledger is defined by the future schema.

`GRAPH_CERTIFIED` is not added as a replacement claim class by this charter.

---

## 28. Implementation sequence

The ratified immediate sequence remains:

1. `CMDG-CHARTER-001`;
2. `CMDG-SCHEMA-001`;
3. `CMDG-VALIDATOR-001`;
4. `CMDG-LEAN-DEPENDENCY-EXTRACTOR-001`;
5. `CMDG-NAT-CONCORDANCE-001`;
6. `CMDG-EUCLID-BRIDGE-001`;
7. `CMDG-VERTICAL-SPINE-V0-001`;
8. `CMDG-CONDENSED-CM1-001`;
9. `CMDG-CONDENSED-CM2-001`;
10. `CMDG-VERTICAL-SPINE-V1-001`.

The word `VERTICAL-SPINE` in retained operation identifiers is historical naming. Governing prose SHALL use `demonstration spine` or `certified spine` according to Section 14.

Broad parallel foundational work SHOULD remain bounded until the charter, schemas, validator, and first demonstration-spine contract are protected and replayable.

---

## 29. CMDG-1.0 programme criteria

CMDG-1.0 requires at minimum:

- a versioned typed mathematical dependency graph;
- fail-closed graph validation;
- semantic, proof, implementation, and provenance separation;
- representation of epochs F0 through F9 in the governed ontology or registry;
- a fully certified V0 route under an explicit manifest, at which point it may be called a certified spine;
- at least one significant foundational concordance, beginning with the natural-number experiment;
- explicit axiom and classicality footprints;
- no undocumented assumptions on the declared certified route;
- independent replay;
- successful CM1 and CM2 targets under the pinned Condensed definition;
- a V1 homological/condensed-module route;
- a documented protected route toward a Liquid-Tensor-class capstone.

These are programme criteria. They do not themselves certify a theorem or discharge the correction gates attached to particular stages.

---

## 30. Change control and anti-drift rule

The protected I–XIX CMDG memorial remains the stable record of the originating programme conception.

A later change is architectural and requires an explicit protected decision delta when it would materially:

1. collapse the four dependency layers into one;
2. treat implementation imports as mathematical dependencies by default;
3. equate machine checking with `GRAPH_CERTIFIED`;
4. erase the explicit metatheory/object-theory distinction between the operational DTT substrate and formal ZF/ZFC;
5. remove foundational concordance as a core CMDG objective;
6. replace the demonstration-spine-first strategy with unconstrained breadth;
7. treat Condensed Mathematics as an isolated topic rather than a modern dependency load test;
8. declare programme completion from documentation or imports without a certified semantic path;
9. weaken the manifest-relative or boundary-relative meaning of graph certification without explicit review;
10. silently rewrite the originating programme motivation after a Council or Human Steward decision.

Operational refinements that preserve these invariants may proceed through ordinary governed work packages and schema decisions.

---

## 31. Claim boundary

This charter authorizes a programme architecture and controlled implementation route only.

It does not:

- prove a new mathematical theorem;
- establish consistency or relative consistency of ZFC or another foundation;
- certify any existing mathlib theorem as semantically dependency-complete;
- confer `GRAPH_CERTIFIED` status on any theorem or graph;
- claim formalization of all mathematics;
- claim that V0, V1, or V2 is minimal, canonical, or unique;
- claim independent reproval of Clausen–Scholze results;
- authorize novelty, priority, publication, patentability, product, deployment, or commercial claims.

Any public or repository statement that exceeds this boundary requires separate mathematical, documentary, or governance authority.

---

## 32. Governing references

This charter is interpreted together with:

- `docs/decisions/ADR-0017_CMDG_CERTIFIED_MATHEMATICAL_DEPENDENCY_GRAPH.md`;
- `records/CMDG_GRAND_CHALLENGE_PROGRAMME_MEMORIAL.md`;
- `docs/CMDG_GRAND_CHALLENGE_PROGRAMME_MEMORIAL.md`;
- `docs/CMDG_COUNCIL_DELIBERATION_001.md`;
- `governance/cmdg_council_review_candidate.json`;
- `governance/cmdg_council_authority_closure_001.json`;
- `ARCHITECTURE_OVERVIEW.md`;
- `CERTIFICATION_LADDER.md`;
- `CLAIM_LEDGER_STANDARD.md`;
- `docs/AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md`;
- `docs/CLAIM_BOUNDARY_DOCTRINE.md`;
- `docs/CHAIDEZ_PEDAGOGICAL_PROTOCOL.md`.

When a mutable issue or discussion conflicts with a protected repository authority record, the protected record governs within its stated claim boundary.

---

## 33. Next gate

After protected admission of this charter, the next authorized operation is:

`CMDG-SCHEMA-001`

That operation shall encode the charter's typed graph, manifest-relative certification, `REALIZES_AS` relation, direct-edge discipline, boundary/trust semantics, and equivalence-quotient constraints into machine-checkable schemas.

Schema finalization must fail closed if it cannot express the C01 and C02 obligations fixed here.

`CMDG-VALIDATOR-001` follows schema admission and shall supply the first executable enforcement of those contracts. Production `GRAPH_CERTIFIED` claims remain prohibited until the required schema, validator, and `CMDG-C06` adversarial/replay gates are in force.
