# ADR-0017: Adopt CMDG — Certified Reconstruction of the Mathematical Dependency Graph

## Status

**Council consensus:** `RATIFY_WITH_CORRECTIONS` on 2026-08-08.  
**Human Steward disposition:** `HUMAN_STEWARD_RATIFIED_WITH_COUNCIL_CORRECTIONS`.  
**Human Steward evidence:** PR #289 top-level comment `5225270603`, binding exact reviewed head `11ed37d35825a381ce75bcc935bb87d2273eed53`.  
**Protected admission:** PR #289 merged as `076bcdf1631b6f39b8ac84046c301344a43310da` on 2026-08-08.  
**Protected authority:** active subject to the stage-bounded corrections `CMDG-C01` through `CMDG-C08`; documentary closure is recorded by `CMDG-COUNCIL-AUTHORITY-CLOSURE-001`.

## Context

The Euclid end-to-end exemplars demonstrated that MATH-PROGRAMME can carry a bounded mathematical statement from source reconstruction through formalization and certification. The Human Steward then approved a broader successor conception: rather than immediately select another isolated advanced theorem, reconstruct and certify the dependency architecture that permits modern mathematics to stand.

The motivating conception is preserved verbatim in `records/CMDG_GRAND_CHALLENGE_PROGRAMME_MEMORIAL.md`, with a rendered pointer at `docs/CMDG_GRAND_CHALLENGE_PROGRAMME_MEMORIAL.md`. Council docket #288 requested ratification of the programme architecture, foundation policy, typed dependency graph, certification semantics, execution order, cross-foundational natural-number experiment, and Condensed Mathematics frontier.

The Agent Council reviewed the docket under `docs/AGENT_COUNCIL_GOVERNANCE.md`, `docs/AGENT_COUNCIL_WORK_PACKAGE_CHECKLIST.md`, and `schemas/agent_review.schema.json`. All fifteen schema-required offices recorded findings. The complete historical deliberation is `docs/CMDG_COUNCIL_DELIBERATION_001.md`; the machine-readable pre-ratification candidate record is `governance/cmdg_council_review_candidate.json`.

## Council finding

Quorum was defined for this docket as completion of all fifteen schema-required office reviews plus Referee synthesis and absence of blocking dissent against presentation to the Human Steward.

- offices reviewed: 15/15;
- offices supporting adoption: 15/15;
- `RETURN_FOR_REVISION`: 0;
- `REJECT`: 0;
- Referee synthesis: `RATIFY_WITH_CORRECTIONS`.

Council found CMDG coherent, technically feasible, aligned with the existing MATHFORGE → MATHSOLVE → MATHCERT authority split, and suitable as an overarching MATH-PROGRAMME Grand Challenge.

## Human Steward decision

The Human Steward ratified the Council disposition at PR #289 exact head `11ed37d35825a381ce75bcc935bb87d2273eed53` and adopted:

> **CMDG — Certified Reconstruction of the Mathematical Dependency Graph**

with the mission to construct a machine-readable, machine-checked, provenance-bearing reconstruction of the dependency architecture of modern mathematics, from formal logic and foundational systems through structural mathematics, category theory, topology, analysis, sheaf/homological machinery, and a demanding modern frontier such as Condensed Mathematics.

The binding disposition is:

`HUMAN_STEWARD_RATIFIED_WITH_COUNCIL_CORRECTIONS`

Adoption preserves the following core decisions:

1. CMDG is not a project to re-formalize all mathematics from scratch.
2. CMDG separates semantic mathematical dependency, checked-proof dependency, implementation/import dependency, and provenance dependency.
3. The canonical mathematical object is a typed directed multigraph; only certified equivalence-generating edges may be collapsed for acyclic dependency projections.
4. Lean dependent type theory is the operational proof substrate; ZF/ZFC and other foundational systems are represented object theories or realizations, not silently identified with Lean's metatheory.
5. The existing Level 0–5 theorem certification ladder remains in force.
6. `GRAPH_CERTIFIED` is an orthogonal dependency-certification status and is not synonymous with `machine_checked`.
7. CMDG proceeds by thin vertical demonstration spines followed by horizontal closure.
8. `CMDG-NAT-CONCORDANCE-001` is the first cross-foundational experiment, followed by `CMDG-EUCLID-BRIDGE-001`.
9. Condensed Mathematics is the first major modern load test, beginning with exact bounded CM0–CM2 targets before later homological, solid, and liquid stages.
10. MATH-PROGRAMME owns ontology and authority; MATHFORGE owns source reconstruction/candidate dependency evidence; MATHSOLVE owns mathematical reconstruction; MATHCERT owns proof replay, dependency extraction, concordance checking, and certification.

## Council correction register

The Human Steward adopted the following stage-bounded corrections as binding obligations.

### CMDG-C01 — Manifest-relative graph certification

Before `CMDG-SCHEMA-001` finalization or any `GRAPH_CERTIFIED` status, define graph certification relative to a versioned manifest recording root, ontology version, direct semantic dependencies, closure policy, boundary nodes/trust classes, proof environment, axiom/classicality footprint, and reviewed semantic-edge evidence.

### CMDG-C02 — Cross-layer realization semantics

Before `CMDG-SCHEMA-001` finalization, add an explicit semantic-to-formal realization relation such as `REALIZES_AS` or `FORMALIZES_AS`; distinguish direct reviewed edges from computed transitive closure; restrict equivalence quotienting to certified equivalence-generating edges.

### CMDG-C03 — Exact ZFC and NNO profiles

Before `CMDG-NAT-CONCORDANCE-001`, specify whether the set-theoretic realization is syntactic, semantic, or both with an interpretation bridge; define categorical natural-numbers objects by universal property in a named ambient category with explicit universe conditions.

### CMDG-C04 — Exact Condensed Mathematics target

Before CM0–CM2 promotion, pin the exact condensed-object definition and state the cardinality/concordance boundary between the chosen formal implementation and Clausen–Scholze formulations. Any equivalence across presentations is a separate concordance obligation.

### CMDG-C05 — Solid-module scope

Before any general-ring CM4 claim, restrict to a formally supported ring regime or reconstruct the intended general solid-module definition; do not overstate an implementation whose own documentation carries a generality caveat.

### CMDG-C06 — Adversarial and replay gate

Before the first production `GRAPH_CERTIFIED` artifact, install retained fixtures for hidden classicality, import/semantic conflation, equivalence laundering, boundary laundering, alias inflation, transitive omission, universe issues, source mismatch, stale pins, and clean-environment replay.

### CMDG-C07 — Documentary integration

Before protected CMDG authority activation, preserve the memorial, full Council deliberation, machine-readable review, Human Steward disposition, this ADR and index entry, artifact-ledger and terminology updates, exact-head review evidence, protected merge receipt, and post-merge readback.

`CMDG-COUNCIL-AUTHORITY-CLOSURE-001` is the dedicated closure operation for this correction. Its protected receipt binds the Human Steward disposition, PR #289 exact head, protected merge, protected-main readback, and pre/post-merge workflow evidence. The historical Council deliberation and candidate review remain unchanged as pre-ratification records.

### CMDG-C08 — Spine terminology

Use `demonstration spine` or `certified spine` for V0/V1/V2 unless minimality or uniqueness is separately proved.

## Consequences of ratification

- `CMDG-CHARTER-001` is authorized immediately and must incorporate C01, C02, C08, and the controlled terminology identified by Council.
- Schema and validator work may proceed only after the charter fixes the manifest-relative certification contract.
- Natural-number concordance may not promote until C03 is discharged.
- Condensed frontier promotion may not proceed past the corresponding C04/C05 gates.
- No theorem becomes `GRAPH_CERTIFIED` until C01, C02, and C06 are operational.
- The I–XIX memorial remains a stable motivating reference; later architectural departures require explicit decision deltas rather than silent rewriting.

## Protected admission evidence

PR #289 was admitted from the exact reviewed head named by the Human Steward disposition:

- reviewed PR: `#289`;
- exact reviewed head: `11ed37d35825a381ce75bcc935bb87d2273eed53`;
- Human Steward top-level comment: `5225270603`;
- pre-merge Programme policy: run `31247672054`, success;
- pre-merge GCL conformance: run `31247672257`, success;
- pre-merge administrative dispatcher: run `31247672063`, success;
- ready-for-review dispatcher: run `31247891459`, success;
- protected merge commit: `076bcdf1631b6f39b8ac84046c301344a43310da`;
- protected-main readback: `076bcdf1631b6f39b8ac84046c301344a43310da`;
- post-merge Programme policy: run `31247906697`, success;
- post-merge GCL conformance: run `31247906944`, success;
- post-merge administrative dispatcher: run `31247906696`, success;
- post-merge protected synchronization: run `31247924635`, success;
- post-merge workflow-run dispatcher: run `31247924653`, success.

The machine-readable closure record is `governance/cmdg_council_authority_closure_001.json`.

## Rejected alternatives

### Return CMDG for redesign

Rejected. No office identified a defect requiring abandonment or fundamental restructuring. All identified corrections are stage-bounded refinements of the approved thesis.

### Treat import graphs as mathematical dependency graphs

Rejected. This would collapse the programme's central semantic distinction.

### Treat `machine_checked` as `GRAPH_CERTIFIED`

Rejected. Kernel checking establishes proof validity under a formal environment; CMDG additionally requires a reviewed dependency manifest and declared trust boundary.

### Require exhaustive bottom-up formalization before a frontier test

Rejected. The Council supports a thin vertical demonstration spine followed by horizontal closure.

### Treat current mathlib Condensed/Solid implementations as automatically identical to every source formulation

Rejected. Exact target identity and any concordance must be stated and checked.

## Claim boundary

This ADR authorizes a programme architecture and controlled implementation route. It does not:

- prove a new mathematical theorem;
- establish consistency or relative consistency of ZFC or another foundation;
- certify any existing mathlib theorem as semantically dependency-complete;
- claim formalization of all mathematics;
- claim independent reproval of Clausen–Scholze results;
- authorize novelty, priority, publication, patentability, product, deployment, or commercial claims.

## Authority record

The Human Steward disposition, exact-head validation, protected merge, and protected-main workflow evidence are bound by `CMDG-COUNCIL-AUTHORITY-CLOSURE-001`. The original Council deliberation and candidate review remain historical evidence of the pre-ratification state and are not rewritten by this closure record.
