# CMDG Council Deliberation 001

## COUNCIL-CMDG-001 — Council review of the Certified Reconstruction of the Mathematical Dependency Graph

**Docket:** MATH-PROGRAMME issue #288  
**Programme:** CMDG — Certified Reconstruction of the Mathematical Dependency Graph  
**Deliberation date:** 2026-08-08  
**Protected baseline reviewed:** `grandchallenge/MATH-PROGRAMME@4c7b5be0a3c0fbea95db66590b57ef57d1b01f56`  
**Motivating memorial reviewed:** PR #289, `docs/CMDG_GRAND_CHALLENGE_PROGRAMME_MEMORIAL.md`, exact head `f5e7462538919bb471cf1c284f6ebf9d6234e5d6`  
**Authority state:** Council recommendation only; Human Steward approval and protected admission remain pending.

## 1. Purpose and review standard

The Human Steward approved the CMDG conception in entirety and directed that it be put to Council. Docket #288 asks the Council to review the architecture, boundaries, certification semantics, implementation order, and initial Condensed Mathematics frontier targets without silently expanding the approved claim boundary.

The current Agent Council schema requires review records for fifteen offices: Axiomatist, Prospector, Experimentalist, Cartographer, Verifier, Adversary, Formalist, Steward, Composer, Grammarian, Amanuensis, Archivist, Mechanist, Typesetter, and Referee. The governance documents do not state a separate numerical quorum rule. For this proceeding, Council therefore adopts the stronger operational rule:

> **Quorum is achieved only when all fifteen schema-required offices have recorded a reviewed finding, the Referee has synthesized the record, and no blocking dissent remains against presentation to the Human Steward.**

This quorum rule is procedural for this docket and does not amend the standing governance documents.

## 2. Materials reviewed

Council reviewed:

- docket #288 and its twelve decision questions;
- the full I–XIX CMDG programme memorial at PR #289 exact head `f5e7462538919bb471cf1c284f6ebf9d6234e5d6`;
- `ARCHITECTURE_OVERVIEW.md`;
- `CERTIFICATION_LADDER.md`;
- `CLAIM_LEDGER_STANDARD.md`;
- `docs/AGENT_COUNCIL_GOVERNANCE.md`;
- `docs/AGENT_COUNCIL_WORK_PACKAGE_CHECKLIST.md`;
- `schemas/agent_review.schema.json`;
- `docs/AGENT_COUNCIL_DECISION_RECORDS.md`;
- current Lean and mathlib reference material relevant to first-order model theory, ZFC encodings, category-theoretic universe handling, and Condensed Mathematics.

External technical references used as feasibility and boundary evidence include:

- Lean language reference and current release documentation: <https://lean-lang.org/doc/reference/latest/>;
- Mathlib first-order satisfiability/compactness: <https://leanprover-community.github.io/mathlib4_docs/Mathlib/ModelTheory/Satisfiability.html>;
- Mathlib ZFC pre-set construction: <https://leanprover-community.github.io/mathlib4_docs/Mathlib/SetTheory/ZFC/PSet.html>;
- Mathlib category-theory core/universe notes: <https://leanprover-community.github.io/mathlib4_docs/Mathlib/CategoryTheory/Category/Basic.html>;
- Mathlib condensed-object definition: <https://leanprover-community.github.io/mathlib4_docs/Mathlib/Condensed/Basic.html>;
- Mathlib discrete/underlying adjunction: <https://leanprover-community.github.io/mathlib4_docs/Mathlib/Condensed/Discrete/Basic.html>;
- Mathlib Cartesian-closed condensed sets: <https://leanprover-community.github.io/mathlib4_docs/Mathlib/Condensed/CartesianClosed.html>;
- Mathlib condensed modules: <https://leanprover-community.github.io/mathlib4_docs/Mathlib/Condensed/Module.html>;
- Mathlib solid modules: <https://leanprover-community.github.io/mathlib4_docs/Mathlib/Condensed/Solid.html>.

## 3. Office deliberations

### 3.1 Axiomatist

**Disposition:** `RATIFY_WITH_CORRECTIONS`

The central foundation split is sound and should be retained. Lean's dependent type theory and kernel-checked proof objects are the operational metatheoretic substrate; ZF/ZFC is to be represented within that substrate rather than silently identified with it. This distinction is one of the strongest parts of CMDG because it prevents the common mistake of treating a theorem proved in Lean as automatically a theorem whose foundational content has been classified.

Three corrections are required.

First, CMDG must separate the **kernel substrate**, the **library-level axioms or principles actually consumed by a declaration**, and the **object theories represented inside Lean**. Axiom availability in an environment is not the same as axiom dependence of a theorem. Foundational fingerprints must therefore record declaration-level footprints rather than merely list principles available in mathlib.

Second, the phrase "set-theoretic/von Neumann realization inside the formalized set-theoretic object theory" is underdetermined. Mathlib contains a ZFC-style `ZFSet` construction as a quotient of pre-sets and a von Neumann `omega`, but CMDG must decide whether its ZFC lane means: (a) a syntactic first-order theory of ZFC plus models and satisfaction; (b) a semantic ZFC set universe implemented in Lean; or (c) both, connected by an interpretation/model theorem. These are not interchangeable documentary labels. The selected profile must be explicit before `CMDG-NAT-CONCORDANCE-001` is allowed to claim three-foundation concordance.

Third, the categorical natural-numbers-object presentation must be stated by its universal property in a precisely named ambient category, with universe levels and required categorical structure explicit. A type equivalence with `Nat` is not by itself an NNO certification.

No correction blocks adoption of CMDG or drafting `CMDG-CHARTER-001`. The second and third corrections block the natural-number concordance stage until discharged.

### 3.2 Prospector

**Disposition:** `RATIFY`

The programme has unusually high leverage because it converts existing formalization activity from a collection of theorem artifacts into an explicit research object: the structure of mathematical dependence itself. This creates useful work even when no new theorem is proved. Missing definitions, unexpected classicality, library bottlenecks, noncanonical structural choices, and disagreements between informal and formal dependency descriptions all become inspectable outputs.

The choice of natural numbers as the first concordance experiment is well judged. It is simple enough to permit complete foundational comparison while remaining rich enough to exercise recursion, induction, arithmetic operations, order, divisibility, and transport of the existing Euclid GCD exemplar. That gives CMDG a direct historical continuation instead of an arbitrary foundation demo.

Condensed Mathematics is also an appropriate frontier because it forces interaction among topology, category theory, sheaves, algebra, and eventually homological and analytic machinery. The frontier should be understood as a load test, not as a claim that Condensed Mathematics is the unique or final organization of modern mathematics.

No competing programme has higher immediate strategic value as the successor to the Euclid campaign. Prospector recommends adoption and the vertical-spine-first strategy.

### 3.3 Experimentalist

**Disposition:** `RATIFY_WITH_CORRECTIONS`

The two-dimensional strategy is approved: a thin end-to-end spine should be exercised before horizontal expansion. However, CMDG should treat the first graph implementation as an experimental protocol, not immediately as a universal ontology.

Before broad graph population, the validator should be challenged with retained positive and negative fixtures. Minimum fixtures should include:

1. a small constructive arithmetic theorem with no classical dependencies;
2. a theorem whose proof imports a large module but semantically depends on very little;
3. a theorem that acquires `Classical.choice` through a downstream declaration;
4. two definitions that are mathematically equivalent but implemented through different library routes;
5. an intentionally circular `EQUIVALENT_TO` component;
6. an implementation alias that must not become a second semantic node;
7. a boundary theorem marked `REUSED` whose internal dependencies are intentionally not reconstructed;
8. the Euclid GCD exemplar as the first realistic end-to-end fixture.

The experiment should measure not only validator correctness but graph stability under refactoring. If a mathlib implementation changes while the mathematics does not, `G_implementation` may change without forcing a false semantic revision. That separation is a key empirical test of the four-graph design.

This correction blocks horizontal scale-up, not CMDG adoption or charter work.

### 3.4 Cartographer

**Disposition:** `RATIFY_WITH_CORRECTIONS`

The typed directed multigraph is the correct base object. A naive DAG is insufficient because equivalence, mutual definability, interpretation, and multiple realizations introduce legitimate cycles. The proposed quotient-by-certified-equivalence idea is acceptable provided only relations explicitly declared as equivalence-generating participate in that quotient.

The four-graph separation is adequate for V0, but the schema needs a first-class cross-layer relation between mathematical nodes and formal realizations. `SOURCE_DERIVED` is provenance, not realization. Council therefore recommends adding a relation such as `REALIZES_AS` or `FORMALIZES_AS` before schema freeze. Without it, one cannot cleanly say that a semantic natural-number structure is realized by a particular Lean declaration while keeping semantic and implementation graphs distinct.

Every dependency edge should also distinguish **direct asserted dependency** from **transitive closure**. The graph should never materialize transitive closure as if every derived edge were a primitive reviewed assertion. Closure can be computed, cached, and certified against the direct graph.

A further conceptual correction is important: V0 is a **certified demonstration spine**, not necessarily a minimal or unique semantic dependency path. For example, category theory does not mathematically require the prior development of ring theory merely because one chosen pedagogical path lists rings before categories. CMDG must not confuse a useful end-to-end route with a proof that the history or logic of mathematics is linearly ordered.

The correction adding cross-layer realization semantics blocks `CMDG-SCHEMA-001` finalization but not `CMDG-CHARTER-001`.

### 3.5 Verifier

**Disposition:** `RATIFY_WITH_CORRECTIONS`

The programme is independently checkable in principle. The declaration dependency extractor, axiom footprint extractor, graph validator, and replay manifests can all be implemented with deterministic outputs. The semantic graph reconciler is also feasible provided it is not represented as an oracle that can infer mathematical meaning automatically.

The most important verification correction concerns the meaning of `GRAPH_CERTIFIED`. The phrase "every material dependency" cannot be validated unless the certification object names its closure rule and its trust boundary. A theorem imported from a trusted upstream library may have thousands of internal declaration dependencies that CMDG intentionally does not reconstruct. Therefore graph certification must be relative to a **versioned dependency manifest** containing at least:

- graph version/ontology version;
- root theorem or artifact;
- direct semantic dependencies;
- allowed boundary nodes and their trust class (`REUSED`, `RECONSTRUCTED`, `CONCORDANT`, or successor terms);
- closure policy;
- pinned proof environment;
- exact axiom/classicality extraction result;
- provenance evidence for reviewed semantic edges.

`GRAPH_CERTIFIED` should mean that the recorded manifest is complete under its declared policy and contains no unresolved boundary, not that an undecidable global notion of "all mathematically relevant facts" has somehow been mechanically established.

Schema validation should reject unknown nodes, dangling refs, illegal source/target combinations, unauthorized cycle-forming edges, stale pins, undeclared boundary nodes, and mismatches between declared and extracted axiom footprints.

This correction is blocking before the first artifact may receive `GRAPH_CERTIFIED`, and its core semantics should be fixed before `CMDG-SCHEMA-001` is finalized.

### 3.6 Adversary

**Disposition:** `RATIFY_WITH_CORRECTIONS`

The proposed programme is valuable precisely because it creates new opportunities for false confidence. The Adversary therefore tested the design against the following failure classes.

**Hidden classicality.** A root theorem appears constructive but consumes a downstream declaration that uses choice or propositional extensionality. The axiom extractor must follow actual declaration dependencies and the manifest must not substitute an expected footprint for the extracted one.

**Import/semantic conflation.** A theorem imports a large category-theory module for notation but has a small mathematical dependency set. Import edges must never be automatically promoted to semantic edges.

**Equivalence laundering.** A cycle of asserted `EQUIVALENT_TO` edges can collapse unrelated nodes unless each equivalence edge carries its own certification status and the quotient only consumes certified edges.

**Boundary laundering.** A large imported theorem can be marked `REUSED`, after which an incomplete graph may look complete. Boundary nodes therefore require explicit trust classification and provenance; graph certification is relative to that boundary declaration.

**Alias inflation.** Definitional aliases, notation wrappers, and type synonyms can create false semantic multiplicity unless identity rules are defined.

**Transitive omission.** Recording only direct semantic edges is legitimate, but certification must verify closure through them. Conversely, recording only a flattened transitive list destroys local accountability.

**Universe laundering.** `ULift`, resizing, and universe-polymorphic constructions can conceal assumptions or change the exact categorical statement. Universe data must be part of formal profiles where material.

**Source laundering.** A citation to a source theorem is not evidence that the formal declaration has the same hypotheses and conclusion. Source-to-formal concordance remains a distinct obligation.

No attack requires rejection of CMDG. Adversary requires retained mutation fixtures for these failure classes before any `GRAPH_CERTIFIED` status is emitted.

### 3.7 Formalist

**Disposition:** `RATIFY_WITH_CORRECTIONS`

Lean/mathlib feasibility is strong. Current mathlib contains mature first-order syntax and satisfiability infrastructure, including a compactness theorem; ZFC-style set encodings and von Neumann constructions; extensive category theory; and active Condensed Mathematics modules. The proposed CM1 discrete/underlying adjunction and CM2 Cartesian-closed condensed-set endpoints already have corresponding upstream formal results, which makes them appropriate dependency-reconstruction tests rather than speculative proof targets.

Two technical scope controls are mandatory.

First, mathlib's current `Mathlib.Condensed.Basic` documentation states that its `Condensed` construction uses sheaves on compact Hausdorff spaces and notes that the implementation more closely resembles pyknotic objects because it does not impose the usual cardinality bounds. CMDG must therefore name exactly which condensed category is being certified at CM0–CM2. It must not silently use the word "condensed" to claim literal identity with every Clausen–Scholze set-theoretic presentation. If equivalence with a cardinal-bounded presentation is desired, that becomes a separate concordance theorem.

Second, current `Mathlib.Condensed.Solid` documentation explicitly notes that its predicate is not the correct general definition for an arbitrary ring `R`; the correct general formulation requires a more careful reduction through finite-type `Z`-algebras. Therefore CM4 must either restrict its ring scope to a regime supported by the formal definition or reconstruct the intended general definition before claiming a general solid-module frontier.

The categorical NNO experiment may require new library infrastructure; no canonical current mathlib NNO abstraction was identified during this review. That is a tractable research task, not a programme blocker.

Formalist supports adoption with the above stage-specific corrections.

### 3.8 Steward

**Disposition:** `RATIFY`

The reader contract is unusually clear if the claim boundary remains intact. Public descriptions should emphasize that CMDG certifies a declared dependency structure and trust boundary, not "all dependencies of mathematics" in an absolute philosophical sense.

The programme should retain three audience-facing distinctions:

- a theorem can be machine checked without being graph certified;
- a graph-certified path can legitimately terminate at trusted imported boundary nodes;
- a reconstructed theorem is not automatically novel mathematics.

The Euclid-to-foundations transition gives the programme an intelligible narrative for non-specialists: Euclid showed durable deductive structure; modern foundations make the hidden substrate explicit; CMDG then exposes how increasingly abstract mathematics is supported by that substrate. Condensed Mathematics is best explained as the load test at the far end of the bridge.

No reader-contract defect blocks adoption.

### 3.9 Composer

**Disposition:** `RATIFY`

The I–XIX memorial should remain a historical motivating document and should not gradually mutate into the normative implementation specification. `CMDG-CHARTER-001` should extract the normative commitments into a shorter charter; the architecture document should carry the graph model; schemas should carry machine contracts; work packages should carry execution detail.

This separation will reduce drift because a later implementation refinement can alter a schema or work package without rewriting the original rationale. Conversely, any deliberate architectural departure from the memorial should be recorded as an explicit decision delta.

The proposed ordering is coherent. The only presentational amendment is Cartographer's terminology: call V0/V1/V2 "demonstration spines" or "certified spines" unless minimality has actually been proved.

### 3.10 Grammarian

**Disposition:** `RATIFY_WITH_CORRECTIONS`

Several controlled terms need normative definitions in the charter.

**Dependency** must mean a typed relation whose kind determines what is being claimed. It must never be an unqualified synonym for "import".

**Foundation** must distinguish metatheoretic proof substrate, represented object theory, and foundation-specific realization.

**Concordant** must not mean that two foundational theories are equivalent. It means that specified objects, operations, constructions, or theorems have been related by certified maps/equivalences under explicit assumptions.

**Independent replay** means an independent execution/check of the pinned artifact and environment; it does not mean an independent mathematical reproof unless that stronger condition is explicitly stated.

**GRAPH_CERTIFIED** should grammatically attach to a theorem/claim **under a named graph manifest and trust profile**, not be treated as an intrinsic timeless adjective.

**Complete dependency path** must be read relative to the declared closure policy and boundary set.

These terminology corrections should be incorporated into `CMDG-CHARTER-001` and the terminology registry. They do not block Human Steward approval.

### 3.11 Amanuensis

**Disposition:** `RATIFY_WITH_CORRECTIONS`

The record chain is coherent but not yet authoritative. Docket #288 is a mutable issue. The I–XIX memorial is versioned at PR #289 exact head `f5e7462538919bb471cf1c284f6ebf9d6234e5d6` but remains outside protected `main`. This deliberation is being added to the same candidate branch so that the memorial, Council record, and eventual Human Steward disposition can be reviewed against one exact package.

The following documentary requirements apply before CMDG becomes protected programme authority:

1. preserve the I–XIX memorial as an immutable motivating reference after admission;
2. preserve this full office-by-office deliberation;
3. preserve a machine-readable Council review record;
4. create an ADR recording the Council recommendation and Human Steward decision;
5. update the Agent Council decision index after the Human Steward acts;
6. update the artifact ledger and terminology registry;
7. bind the final reviewed head, review identity, Human Steward disposition, protected merge, and post-merge readback;
8. keep issue #288 as navigation/discussion rather than sole authority.

The current correction register must not be silently edited away. If the Human Steward ratifies with corrections, their stage boundaries become normative obligations.

### 3.12 Archivist

**Disposition:** `RATIFY_WITH_CORRECTIONS`

The historical narrative is defensible as a conceptual genealogy, but it should not be presented as a simple chronological or exclusive lineage. Euclid, Hilbert/Tarski, set theory, Bourbaki, Grothendieck, dependent type theory, and Clausen–Scholze represent different dimensions of the development of mathematical structure.

CMDG should maintain versioned primary or authoritative-source references for each historical and modern layer. In particular:

- foundational claims about Lean should cite the Lean reference/manual and pinned Lean version;
- claims about library capabilities should cite pinned mathlib declarations and commits rather than only current web documentation;
- Condensed Mathematics terminology should distinguish Clausen–Scholze sources from mathlib implementation choices;
- Liquid Tensor Experiment references should distinguish the historical formalization achievement from any future CMDG dependency reconstruction;
- Bourbaki and Grothendieck should be used as conceptual structural anchors, not as claims of direct software ancestry.

No novelty or priority claim follows from the architecture itself.

### 3.13 Mechanist

**Disposition:** `RATIFY_WITH_CORRECTIONS`

The initial tooling can be implemented deterministically. The declaration dependency extractor should operate on elaborated Lean environment declarations rather than source-text heuristics. It should emit stable identifiers, declaration kinds, direct constant dependencies, and hashes/pins sufficient for replay. The axiom extractor should cross-check the transitive declaration graph against Lean's own axiom reporting where available.

The graph validator should be offline-capable once the pinned input artifacts are present. CI should not require live web documentation or mutable external endpoints to decide a certification result. External source acquisition belongs upstream; certification replay consumes pinned artifacts.

The semantic reconciler should not generate authoritative semantic edges autonomously. It may propose candidate mappings and inconsistencies, but review must promote them into the canonical graph.

Minimum reproducibility controls are:

- pinned Lean/toolchain version;
- pinned mathlib/source revision;
- deterministic serialization;
- schema version and ontology version;
- exact input manifest;
- retained positive/mutation fixtures;
- clean-environment replay;
- stale-pin rejection.

These requirements block production certification tooling, not programme adoption.

### 3.14 Typesetter

**Disposition:** `RATIFY`

Graph presentation should be generated from authoritative graph data, never maintained manually as a second source of truth. Human-facing diagrams may suppress implementation edges, collapse reviewed equivalence classes, or show only one spine, but every such view should display its projection/filter criteria.

The ten epochs F0–F9 are suitable as navigation bands. They should not be drawn in a way that implies a single linear hierarchy. Visuals should prefer layered DAG projections after equivalence collapse, with cycle-bearing semantic views available when relevant.

No presentation issue blocks adoption.

### 3.15 Referee

**Disposition:** `RATIFY_WITH_CORRECTIONS`

The Referee finds that the Council has reached substantive consensus. No office recommends `RETURN_FOR_REVISION` or `REJECT`. The architecture is coherent, technically feasible, aligned with existing MATH-PROGRAMME trust boundaries, and materially strengthened by the identified corrections.

The corrections are not changes to the core thesis. They make explicit several boundaries that the motivating memorial already implies: certification is relative to a trust contract; foundational realizations require exact statements; semantic dependencies are not imports; and frontier claims must match the exact formal object implemented.

The Referee therefore recommends adoption of CMDG as an overarching Grand Challenge under the disposition `RATIFY_WITH_CORRECTIONS`, with the correction register in Section 5 treated as binding stage gates if the Human Steward approves.

## 4. Council answers to docket #288 decision questions

1. **Adopt CMDG as an overarching MATH-PROGRAMME Grand Challenge?**  
   **Yes.** Consensus: 15/15 offices support adoption; no dissent.

2. **Is the four-graph separation adequate?**  
   **Yes for V0, with correction.** Add explicit cross-layer realization semantics and direct-versus-transitive edge discipline.

3. **Is `GRAPH_CERTIFIED` correctly orthogonal to Level 0–5?**  
   **Yes, with correction.** It must be relative to a named graph manifest, closure policy, boundary set, and trust profile.

4. **Is the DTT-substrate/ZFC-object-theory distinction sound?**  
   **Yes, with correction.** Specify the exact ZFC profile and distinguish kernel substrate, consumed axioms, and represented object theory.

5. **Is `CMDG-NAT-CONCORDANCE-001` the correct first foundational experiment?**  
   **Yes.** Its exact set-theoretic and categorical realizations must be fixed first.

6. **Is Euclid GCD transport the correct first bridge?**  
   **Yes.** It gives continuity with the existing certified Euclid exemplar and tests transport of genuine arithmetic structure.

7. **Is vertical-spine-first/horizontal-closure-second correct?**  
   **Yes.** V0 is a demonstration spine, not a claim of a unique minimal dependency chain.

8. **Are CM1 and CM2 appropriate first frontier tests?**  
   **Yes, with exact-target correction.** State the precise mathlib condensed category and any cardinality/concordance boundary.

9. **Is repository ownership coherent?**  
   **Yes.** Programme owns ontology/authority; Forge sources candidates; Solve reconstructs; Cert checks/replays.

10. **Are the ten initial operations correctly ordered?**  
    **Yes with one refinement.** The charter must resolve certification-manifest semantics and cross-layer relation requirements before schema freeze; the set/NNO profile must be fixed before NAT concordance.

11. **Are CMDG-1.0 and closure conditions strong enough?**  
    **Yes after the manifest-relative certification correction.** They then prevent completion-by-documentation and completion-by-import.

12. **What blockers exist before `CMDG-CHARTER-001`?**  
    **None.** The Council corrections are requirements to be encoded by the charter and subsequent stage gates; they do not require returning the programme for redesign.

## 5. Binding correction register recommended by Council

If the Human Steward approves the Council recommendation, the following corrections become stage gates.

### CMDG-C01 — Manifest-relative graph certification

**Owner:** Verifier / Grammarian / Cartographer  
**Severity:** high  
**Blocks:** `CMDG-SCHEMA-001` finalization and any use of `GRAPH_CERTIFIED`  

Define `GRAPH_CERTIFIED` relative to a versioned dependency manifest with root, ontology version, direct semantic dependencies, closure policy, allowed boundary nodes/trust classes, exact proof environment, axiom/classicality footprint, and evidence for reviewed semantic edges.

### CMDG-C02 — Cross-layer realization and direct-edge semantics

**Owner:** Cartographer  
**Severity:** high  
**Blocks:** `CMDG-SCHEMA-001` finalization  

Add an explicit semantic-to-formal realization relation such as `REALIZES_AS`/`FORMALIZES_AS`; distinguish primitive reviewed edges from computed transitive closure; restrict equivalence quotienting to certified equivalence-generating edges.

### CMDG-C03 — Exact set-theoretic and NNO profiles

**Owner:** Axiomatist / Formalist  
**Severity:** high  
**Blocks:** `CMDG-NAT-CONCORDANCE-001`  

Specify whether the ZFC realization is syntactic, semantic, or both with an interpretation bridge. Define categorical NNO by universal property in an explicit ambient category with universe requirements.

### CMDG-C04 — Exact Condensed Mathematics target

**Owner:** Formalist / Archivist  
**Severity:** high  
**Blocks:** `CMDG-CONDENSED-CM0/CM1/CM2` promotion  

Pin the exact condensed-object definition and explain any difference between the current mathlib implementation and cardinal-bounded Clausen–Scholze formulations. Any claimed equivalence is a separate concordance obligation.

### CMDG-C05 — Solid-module scope

**Owner:** Formalist  
**Severity:** high  
**Blocks:** `CM4` general-ring claim  

Do not treat the current mathlib `CondensedMod.IsSolid R` predicate as a fully general arbitrary-ring definition where its own documentation states otherwise. Restrict scope or reconstruct the intended general definition.

### CMDG-C06 — Adversarial and replay gate

**Owner:** Adversary / Experimentalist / Mechanist / Verifier  
**Severity:** high  
**Blocks:** first production `GRAPH_CERTIFIED` artifact  

Retain fixtures for hidden classicality, import/semantic conflation, equivalence laundering, boundary laundering, aliases, transitive omission, universe issues, provenance mismatch, stale pins, and clean-environment replay.

### CMDG-C07 — Documentary integration

**Owner:** Amanuensis  
**Severity:** medium  
**Blocks:** protected CMDG authority activation  

Preserve memorial, Council deliberation, machine-readable review, Human Steward disposition, ADR/index entry, artifact-ledger entry, terminology changes, exact-head review evidence, protected merge receipt, and post-merge readback.

### CMDG-C08 — V0 terminology

**Owner:** Composer / Grammarian / Typesetter  
**Severity:** low  
**Blocks:** none  

Describe V0/V1/V2 as certified or demonstration spines unless minimality or uniqueness is separately established.

## 6. Quorum and consensus determination

| Office | Review state | Adoption position |
|---|---|---|
| Axiomatist | reviewed | RATIFY_WITH_CORRECTIONS |
| Prospector | reviewed | RATIFY |
| Experimentalist | reviewed | RATIFY_WITH_CORRECTIONS |
| Cartographer | reviewed | RATIFY_WITH_CORRECTIONS |
| Verifier | reviewed | RATIFY_WITH_CORRECTIONS |
| Adversary | reviewed | RATIFY_WITH_CORRECTIONS |
| Formalist | reviewed | RATIFY_WITH_CORRECTIONS |
| Steward | reviewed | RATIFY |
| Composer | reviewed | RATIFY |
| Grammarian | reviewed | RATIFY_WITH_CORRECTIONS |
| Amanuensis | reviewed | RATIFY_WITH_CORRECTIONS |
| Archivist | reviewed | RATIFY_WITH_CORRECTIONS |
| Mechanist | reviewed | RATIFY_WITH_CORRECTIONS |
| Typesetter | reviewed | RATIFY |
| Referee | reviewed | RATIFY_WITH_CORRECTIONS |

**Quorum:** 15/15 required offices reviewed.  
**Adoption support:** 15/15.  
**Return/reject votes:** 0.  
**Unresolved dissent against presentation to Human Steward:** none.  
**Council consensus:** `RATIFY_WITH_CORRECTIONS`.

## 7. Council recommendation to Human Steward

The Council recommends that the Human Steward approve:

> **CMDG — Certified Reconstruction of the Mathematical Dependency Graph** as an overarching Grand Challenge of MATH-PROGRAMME under disposition `HUMAN_STEWARD_RATIFIED_WITH_COUNCIL_CORRECTIONS`, with `CMDG-C01` through `CMDG-C08` adopted as the stage-bounded correction register.

Such approval should authorize `CMDG-CHARTER-001` immediately. It should not authorize later stages to bypass their correction gates, and it should not itself certify any mathematical theorem, dependency edge, foundational equivalence, or Condensed Mathematics result.

## 8. Claim and authority boundary

This Council record:

- recommends programme adoption;
- records office deliberations and stage-bounded corrections;
- does not itself create protected programme authority;
- does not prove or certify mathematics;
- does not establish consistency of ZFC or any other foundational theory;
- does not claim that mathlib's condensed-object implementation is definitionally identical to every Clausen–Scholze presentation;
- does not independently reprove a Liquid Tensor theorem;
- does not authorize novelty, priority, publication, patentability, product, deployment, or commercial claims.

Human Steward disposition and protected repository admission remain required.