# ADR-0021: Adopt the MATH-CORE-centred GCL Mathematics Architecture

## Status

**Council consensus:** `RATIFY_WITH_CORRECTIONS` on 2026-08-31.  
**Human Steward disposition:** `HUMAN_STEWARD_RATIFIED_WITH_COUNCIL_CORRECTIONS`.  
**Council-corrected frozen candidate:** `f4a1daeef803223b819df5f903e4123db6618518`.  
**Construction Gate target:** `MP-MATH-CORE-ARCH-COUNCIL-001`.  
**Protected integration head:** `8aba3f4dfc29042ad5177e168ee7610cc78cd209`.  
**Protected admission:** PR #729 merged as `8773b49ff0b55850278ce83736ac3da55a37f577` on 2026-09-01.  
**Protected-main readback:** `8773b49ff0b55850278ce83736ac3da55a37f577`.  
**Authority condition:** the architecture becomes fully memorialized programme authority only when this ADR and `MATH-CORE-ARCH-AUTHORITY-CLOSURE-001` are themselves protected-admitted with their required exact-head review and readback.

## Context

MATH-PROGRAMME had already separated mathematical execution into MATHFORGE, MATHSOLVE, and MATHCERT, and MATH-CORE-01 had established an event-sourced claim-blackboard protocol for live reasoning state. What remained unresolved was the placement of those institutions relative to INTELLECT, the trusted acceptance machinery, domain programmes, and future AETHER infrastructure.

The architecture memorial at `records/MATH_CORE_01_GCL_MATHEMATICS_ARCHITECTURE_MEMORIAL.md` proposed a MATH-CORE-centred topology. Agent Council docket #721 reviewed that proposal under the stronger docket-specific rule that all fifteen Council offices record a finding before Referee synthesis. The complete deliberation is `docs/MATH_CORE_01_COUNCIL_DELIBERATION_001.md`; the machine-readable pre-ratification review is `governance/math_core_01_council_review_candidate.json`.

Council reached 15/15 support for adoption, with no `RETURN_FOR_REVISION` or `REJECT`, and the Referee synthesized `RATIFY_WITH_CORRECTIONS`. The Human Steward subsequently ratified the Council-corrected exact candidate. The candidate was admitted and frozen through the Construction Gate, independently reviewed, integrated against current protected `main`, and protected-merged without modifying the frozen architecture payload.

## Decision

GCL adopts the MATH-CORE-centred mathematics architecture as the normative placement model for MATH-PROGRAMME.

The architecture is organized by function rather than repository count:

```text
GOVERNANCE / POLICY
  Human Steward + MATH-PROGRAMME

CONTROL / COORDINATION
  INTELLECT
      |
      v
  MATH-CORE claim blackboard / protocol

REASONING INSTITUTIONS
  MATHFORGE     MATHSOLVE     MATHCERT
  + governed theory agents and reasoning services

TRUSTED ACCEPTANCE BOUNDARY
  proof/replay substrate + independent assurance
  + certification ladder + canonical Claim Ledger

ORTHOGONAL INFRASTRUCTURE
  AETHER or other transport/memory fabric
```

These bands describe authority and responsibility, not a requirement that every software call literally traverse every layer.

### Governance and policy

The Human Steward and MATH-PROGRAMME retain governance, integration, publication, and policy authority. Human Steward disposition cannot substitute for mathematical evidence, and mathematical evidence cannot infer Human Steward authority.

### INTELLECT control plane

INTELLECT decides where and how to allocate governed reasoning work. It is a search/routing controller, not a proof kernel or canonical claim authority. Persistent unattended coordination is permitted only through an exact admitted controller under current mandatory GH-OS routing and applicable capability controls.

### MATH-CORE coordination plane

MATH-CORE is the shared live reasoning-state substrate. It records claims, obligations, conflicts, learned search constraints, scoped equivalences, witnesses, and certificates against exact checkpoints. Protocol-valid events remain working state unless separately promoted through the canonical acceptance route.

MATH-CORE is not a fourth mathematical pillar and does not replace the Claim Ledger, certification ladder, MATHCERT, proof kernel, or Human Steward.

### Three stable mathematical pillars

The protected three-pillar doctrine remains intact.

- **MATHFORGE** is the broad discovery/source foundry: source intake, reconstruction, examples, counterexamples, computational exploration, formal-object production, and speculative candidates.
- **MATHSOLVE** performs disciplined campaign reasoning against explicit obligations, reductions, theorem targets, exact screens, failures, and certification handoffs.
- **MATHCERT** supplies independent assurance and certificate/replay checking. It does not directly mutate canonical claim state merely by emitting a certificate.

A pillar is a stable governed institution, not immutable ontology. New capabilities default to governed theory agents or services. Creation, retirement, or material redefinition of a pillar requires explicit governance.

### Trusted acceptance boundary

The trusted acceptance boundary is deliberately plural rather than monolithic. It contains distinct functions:

1. proof or replay checking;
2. independent assurance;
3. certification status under the standing ladder;
4. canonical governed recording in the Claim Ledger;
5. policy disposition where required.

No one function silently implies the others.

### Domain programmes

A mathematical domain programme is represented as a scoped, long-lived MATH-CORE claim/obligation subgraph with explicit programme or family identity and an explicit migration checkpoint. A domain programme is not a peer pillar.

Cross-domain dependencies, equivalences, or imported evidence require typed bridge relations with explicit evidence. Evidence or certification in one domain does not silently transfer canonical or certified status into another.

Existing historical campaigns are imported additively as provenance-bound reconstructed/protected state. They are not rewritten as though MATH-CORE had generated their historical event sequence.

### AETHER and transport

AETHER is an authority-neutral transport and memory fabric. GitHub, JSON, CI, content-addressed artifacts, or future AETHER services may carry the same semantic protocol. Transport identity never creates mathematical or governance authority.

## Council correction register

The Human Steward ratified the following corrections.

### MCORE-ARCH-C01 — Preserve and reconcile the three-pillar doctrine

MATHFORGE remains the broad discovery/source foundry; MATHSOLVE remains disciplined campaign reasoning; MATHCERT remains independent assurance. This ADR and the reconciled architecture overview preserve that boundary.

### MCORE-ARCH-C02 — Controlled topology and authority vocabulary

The programme controls `plane`, `pillar`, `domain programme`, `theory agent/service`, `transport fabric`, `trusted acceptance boundary`, `canonical state`, and `protected dependency layer`, and distinguishes proof checking, assurance, canonical recording, and policy disposition.

### MCORE-ARCH-C03 — Domain isolation and bridge semantics

Domain subgraphs require explicit scope identity and migration checkpoints. Cross-domain relations are typed and evidence-bearing and do not transfer authority implicitly.

### MCORE-ARCH-C04 — Live coordinator identity, concurrency, and invalidation

Before live INTELLECT coordination, require authenticated execution identity outside self-declared producer class; exact-checkpoint concurrency; stale-response rejection; deterministic admission/rejection receipts; supersession/invalidation semantics; bounded budgets; and prohibition on self-authorization.

### MCORE-ARCH-C05 — Exact evidence for replayable assurance

Before production `REPLAYABLE` or `CHECKED` conflict-driven pruning, bind relied-upon evidence to exact checkpoints and content-addressed artifacts, content sets, or versioned replay manifests. Witnesses used operationally for resolution or pruning require exact artifact identity.

### MCORE-ARCH-C06 — Condensed migration and blocker taxonomy

Protected Condensed/CMDG state is imported as provenance-bound state rather than fictitious retroactive live history. Formal replay, protected dependency status, canonical claim status, and certification remain distinct. Active blockers are classified at least as `MATHEMATICAL`, `FORMALIZATION`, `GOVERNANCE_EVIDENCE`, or `EXECUTION_INFRASTRUCTURE`.

### MCORE-ARCH-C07 — Persistent execution routing

Unattended persistent INTELLECT/MATH-CORE coordination must run under an exact admitted controller compatible with current GH-OS routing. A bounded conversational agent may execute authorized transactions but is not represented as the sole unattended persistent controller.

### MCORE-ARCH-C08 — Governed memorialization

The memorial, Council deliberation, machine review, exact corrected candidate, Human Steward dispositions, ADR, decision index, artifact ledger, terminology registry, architecture overview, exact-head CI, independent review, protected merge, protected-main readback, and terminal closure record must agree before the architecture is described as fully memorialized protected authority.

## Construction Gate and protected admission

The architecture package was governed through target `MP-MATH-CORE-ARCH-COUNCIL-001`.

- registration PR #722 exact reviewed head: `fb75f79bf8d6e3ffc156a07d669bab00f07d69c1`;
- registration protected merge: `8254fdef4fe45d3767e606860c2bc3c642e15e69`;
- authorized predecessor: `3c7aa5298debd6564e3f93a7a05b4f6821cd3bb2`;
- corrected frozen candidate: `f4a1daeef803223b819df5f903e4123db6618518`;
- governed development ref: exact frozen candidate;
- governed candidate ref: exact frozen candidate.

Direct merge of the original candidate PR was correctly denied after protected `main` advanced through the prerequisite registration because strict GH-OS up-to-date routing evidence was required. Integration wrapper PR #729 therefore combined current protected `main` with the immutable frozen candidate without revising candidate bytes.

PR #729 exact integration head `8aba3f4dfc29042ad5177e168ee7610cc78cd209` received independent Referee approval by `jimsteeg`, passed the required exact-head checks including GH-OS routing enforcement, received explicit Human Steward exact-head protected-merge approval, and merged as `8773b49ff0b55850278ce83736ac3da55a37f577`.

GitHub verified the merge commit signature. Its parents are protected main `8254fdef4fe45d3767e606860c2bc3c642e15e69` and exact reviewed integration head `8aba3f4dfc29042ad5177e168ee7610cc78cd209`. Protected-main readback matched the merge commit, and the frozen governed candidate remained unchanged.

## First authorized application

After documentary closure, the first substantial implementation operation is:

`MCORE-DOMAIN-SHADOW-001`

It is a read-only Condensed Mathematics shadow materialization from existing protected CM/CMDG state into a provenance-preserving MATH-CORE domain graph. It introduces no retroactive live-event fiction and drives no autonomous allocation or pruning. C03-C07 remain capability gates at their stated stages.

## Consequences

- MATH-CORE becomes the shared reasoning-state semantics for mathematical coordination without becoming canonical truth authority.
- INTELLECT may coordinate work over MATH-CORE only within admitted execution and identity controls.
- The three mathematical pillars remain stable institutional boundaries.
- Domain-specific mathematical programmes default to scoped MATH-CORE subgraphs rather than new top-level pillars.
- Domain semantic validators may impose stronger requirements than generic MATH-CORE protocol validity.
- Search constraints remain assurance-bounded and operational; they do not become mathematical claims by reuse.
- AETHER may replace or supplement transport without changing semantic or authority boundaries.
- Existing CMDG and Condensed authority remains intact; this architecture changes placement and coordination semantics rather than mathematical status.

## Rejected alternatives

### Make MATH-CORE a fourth mathematical pillar

Rejected. It is horizontal coordination semantics shared by the pillars.

### Make every domain or new capability a top-level pillar

Rejected. Domains are scoped programmes; most new capabilities are governed theory agents/services. Pillar changes remain possible only through explicit governance.

### Treat the trusted acceptance boundary as one monolithic checker

Rejected. Proof checking, independent assurance, certification, canonical recording, and policy disposition remain distinct.

### Rewrite historical campaigns as retroactive MATH-CORE event streams

Rejected. Migration is additive, provenance-bound, and checkpointed.

### Treat transport or certificate existence as authority

Rejected. AETHER/GitHub transport is authority-neutral, and a certificate has no direct Claim Ledger mutation effect.

## Claim boundary

This ADR authorizes an organizational and technical architecture only. It does not:

- prove or certify a new mathematical theorem;
- promote any working blackboard event to canonical claim state;
- upgrade the Condensed Mathematics frontier;
- certify a dependency edge merely because it is represented;
- establish consistency or relative consistency of any foundation;
- authorize novelty, priority, publication, patentability, product, deployment, manufacturing, or commercial claims.

## Authority record

The complete exact-head and protected-admission evidence is bound by `governance/math_core_01_architecture_authority_closure_001.json`. The historical memorial, Council deliberation, and pre-ratification machine review remain preserved rather than rewritten by the closure record.
