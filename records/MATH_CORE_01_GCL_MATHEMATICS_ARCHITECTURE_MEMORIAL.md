# MATH-CORE-01 and the GCL Mathematics Architecture

## Council-corrected memorial candidate

**Docket:** COUNCIL-MCORE-ARCH-001 / issue #721  
**Status:** Council `RATIFY_WITH_CORRECTIONS`; corrected candidate pending Human Steward exact-candidate disposition and governed admission  
**Protected baseline:** `grandchallenge/MATH-PROGRAMME@3c7aa5298debd6564e3f93a7a05b4f6821cd3bb2`  
**Submitted memorial reviewed by Council:** exact working commit `691f906b368adce389a0b0bfc94ff2c57f7d1d34`  
**Council record:** `docs/MATH_CORE_01_COUNCIL_DELIBERATION_001.md`  
**Machine review:** `governance/math_core_01_council_review_candidate.json`  
**Authority boundary:** the Human Steward's initial approval covered the submitted architecture, not the material corrections incorporated below; protected authority remains inactive until explicit exact-candidate ratification and the required governed admission/closure sequence

## 1. Architectural thesis

GCL Mathematics should be organized as a governed mathematical operating architecture rather than as a loose collection of repositories or peer agents.

The core separation is:

1. **Governance plane** — MATH-PROGRAMME, Human Steward authority, standards, policy, decision records, claim-boundary doctrine, execution controls, and documentary continuity.
2. **Control and coordination plane** — INTELLECT as search/controller; MATH-CORE-01 as typed reasoning-state semantics and shared blackboard.
3. **Reasoning plane** — the governed institutional pillars MATHFORGE, MATHSOLVE, and MATHCERT, plus specialist theory agents/services operating through MATH-CORE contracts.
4. **Trusted acceptance boundary and acceptance functions** — proof kernels such as Lean, independent replay and assurance, the certification ladder, canonical Claim Ledger recording, protected review, and policy dispositions remain distinct functions rather than one monolithic authority.
5. **Transport and memory substrate** — AETHER may eventually carry state and persistent coordination across the architecture but does not define mathematical truth, certification semantics, protocol semantics, or canonical promotion.

The governing direction is:

> Governance constrains coordination; coordination routes specialized reasoning; independent assurance and proof checking constrain acceptance; canonical state changes only through explicit governed authority.

### Controlled topology vocabulary

For this architecture:

- a **plane** is a system-wide functional layer whose responsibilities cut across domains;
- a **pillar** is a durable governed institution with a distinct responsibility and authority boundary;
- a **domain programme** is a long-lived, scoped mathematical claim/obligation graph hosted by MATH-CORE;
- a **theory agent/service** is a specialized capability operating within an existing institutional authority boundary unless separately elevated by governance;
- a **transport fabric** carries state, memory, or execution coordination without defining the semantic authority of that state;
- the **trusted acceptance boundary** separates live reasoning state from the mechanisms and governed decisions that may establish accepted state;
- **canonical state** is the governed recorded status of claims and artifacts, not a synonym for proof;
- a **protected dependency layer** is an admitted, provenance-bound dependency surface whose exact historical status is preserved when represented in MATH-CORE.

The three current pillars are stable institutions, not immutable ontology. A new pillar may be created, retired, or redefined only by explicit governance when a distinct authority or institutional responsibility cannot be represented adequately as a service within an existing pillar.

## 2. MATH-PROGRAMME

MATH-PROGRAMME is the constitutional and administrative shell around the entire mathematical system. It owns mathematics-specific governance, adopted standards, review contracts, campaign registration, decision records, certification boundaries, policy shards, execution-routing controls, construction integrity, and documentary continuity.

It is not itself a theorem prover. It defines the conditions under which mathematical work may be represented, reviewed, certified, promoted, archived, or described as complete.

## 3. MATH-CORE-01

MATH-CORE-01 is a horizontal coordination substrate, not a peer mathematical-authority pillar.

It hosts an event-sourced Claim Blackboard containing typed claims, obligations, conflicts, search constraints, equivalences, witnesses, certificates, and provenance. Theory agents operate proposal-only; blackboard persistence, agent confidence, CI success, majority vote, or certificate recording do not directly alter canonical mathematical state.

MATH-CORE's principal role is to make live mathematical reasoning state explicit and replayable while preserving a hard distinction between:

- what is being investigated;
- what has been operationally ruled out or deprioritized;
- what evidence exists;
- what has been independently checked; and
- what has actually crossed the governed acceptance boundary.

Conflict assurance and search-only learning remain monotone:

```text
HEURISTIC  -> SOFT_AVOID
REPLAYABLE -> SOFT_AVOID | LOCAL_PRUNE
CHECKED    -> SOFT_AVOID | LOCAL_PRUNE | HARD_PRUNE
```

Even `HARD_PRUNE` remains a search effect rather than automatic theorem promotion.

### Production assurance binding

Before production `REPLAYABLE` or `CHECKED` conflict-driven pruning is relied upon, replay evidence must be bound to an exact checkpoint and a content-addressed artifact, content set, or versioned replay manifest. Witness classes used to resolve or prune obligations must carry exact artifact identity according to a controlled evidence policy.

The live reducer/coordinator path should emit deterministic admission or rejection receipts so replay can distinguish an agent proposal from an admitted blackboard event.

## 4. INTELLECT

INTELLECT is the programme search/control layer.

Its proper authority is to:

- inspect materialized MATH-CORE state;
- allocate attention and compute;
- decompose large goals into explicit obligations;
- select and route specialist reasoners;
- consume typed proposals;
- exploit assurance-bounded learned constraints;
- preserve, invalidate, or reopen unresolved work when evidence or dependencies change.

INTELLECT does not own mathematical truth, certification authority, protected-branch authority, or Human Steward authority.

The architectural distinction is:

> INTELLECT decides where to reason; MATH-CORE records what the reasoning state is; specialist pillars perform or check the reasoning; trusted mechanisms and governance determine what may be accepted.

### Live-coordinator gate

Before INTELLECT may operate as a live sustained coordinator, the implementation must provide:

- authenticated producer/execution identity external to the self-declared producer class;
- exact-checkpoint concurrency control and stale-response rejection;
- deterministic proposal admission/rejection receipts;
- explicit supersession and downstream invalidation semantics;
- bounded request/resource budgets and audit provenance;
- no producer or coordinator self-authorization.

These are deployment gates, not mathematical claims.

## 5. Stable institutional pillars

### 5.1 MATHFORGE — discovery and source foundry

MATHFORGE retains the protected three-pillar doctrine's broad foundry role. It ingests open-problem corpora, source papers, surveys, repository data, examples, counterexamples, computational probes, speculative candidates, and source/formal reconstruction work.

Its responsibilities include source integrity, acquisition, reconstruction, normalization, formal-object production, provenance, candidate discovery, and controlled mappings among source, representation, and formal artifacts.

Its natural MATH-CORE outputs include candidate assertions, source witnesses, formal objects, scoped equivalences, provenance-bearing artifacts, examples, and discovery evidence. None becomes mathematical authority merely because MATHFORGE produced it.

### 5.2 MATHSOLVE — disciplined campaign reasoning

MATHSOLVE is the campaign room. It turns candidate ore into explicit mathematical obligations and attacks them through proof search, decomposition, conjecture refinement, computations, counterexamples, reductions, tactics, failed routes, status/theorem spines, and candidate lemmas.

Its natural MATH-CORE outputs include `PROPAGATE`, `CONFLICT`, `WITNESS`, `EQUIVALENCE`, new obligations, and explicit `UNKNOWN` responses. Search breadth and disciplined campaign reasoning belong here; canonical truth authority does not.

### 5.3 MATHCERT — independent assurance

MATHCERT is the independent assurance pillar, deliberately asymmetric with MATHSOLVE.

It independently replays or checks precisely identified targets and evidence, records checked conflicts or certificates, and supplies stronger assurance classes where justified. MATHCERT evidence may support stronger operational consequences in MATH-CORE, but certificate recording does not directly mutate the canonical Claim Ledger.

MATHCERT must not collapse into a merely stronger solver agent; independence and claim-boundary discipline are institutional properties.

## 6. Trusted acceptance boundary

The lower acceptance region contains distinct functions that must not be conflated:

- **proof checking** — Lean or another explicitly admitted proof kernel checks a formal proof object under declared foundations;
- **independent assurance** — MATHCERT and replay/checking machinery establish evidence according to declared certification contracts;
- **canonical recording** — the Claim Ledger records governed claim status and provenance but is not itself a proof kernel;
- **policy disposition and protected admission** — Human Steward, Council, protected review, and repository controls govern authority transitions where required.

MATH-CORE sits above this boundary. It may accumulate checked artifacts and resolved obligations without silently promoting claims.

## 7. Human Steward

The Human Steward retains policy and exceptional disposition authority as defined by standing governance. Steward approval is not a mathematical proof object and does not discharge a mathematical obligation merely by declaration.

The Steward may approve architecture, authorize governed transitions, resolve policy questions, and issue required dispositions. Mathematical evidence remains subject to its own proof and certification routes.

## 8. AETHER and persistent execution

AETHER is orthogonal infrastructure for transport, durable memory, coordination, and eventually distributed execution.

The intended relation is:

```text
MATH-CORE = semantics and reasoning-state contract
AETHER    = transport / memory / coordination fabric
```

MATH-CORE events must retain their meaning whether transported today through GitHub/JSON/CI or later through AETHER. AETHER availability is therefore not part of the current MATH-CORE trust assumption.

Transport independence does not override mandatory execution routing. Any unattended persistent INTELLECT/MATH-CORE controller must use the exact admitted persistent controller with compatible capabilities required by current GHOS routing policy. A bounded conversational agent may perform individual authorized transactions but may not be represented as the sole persistent controller for an unattended campaign.

## 9. Domain mathematical programmes

Condensed Mathematics, Odd Zeta, Union-Closed, BSD, Hodge, Navier-Stokes, Yang-Mills, Riemann, and successor programmes should not normally become new authority pillars.

They are better modeled as long-lived domain-specific claim/obligation subgraphs hosted by MATH-CORE. The same institutional pillars operate across them according to their distinct roles.

The exact model is not that domain programmes form an intermediate software layer between MATH-CORE and the pillars. Rather:

> MATH-CORE hosts many mathematical programmes; the pillars operate on their typed objects.

### Domain-subgraph isolation and bridge semantics

Every domain graph must carry explicit programme/family scope and a declared migration or live-state checkpoint. Cross-domain dependency, equivalence, witness reuse, or certificate reuse must be represented by explicit typed bridge relations with provenance and evidence appropriate to the relation.

No bridge may silently transfer mathematical equivalence, certification, canonical status, or obligation discharge from one domain into another. Cross-domain convenience is navigation until a stronger relation is explicitly justified.

## 10. Condensed Mathematics Programme placement

The Condensed Mathematics Programme is the leading substantial application of this architecture because it already possesses a protected dependency spine, formal replay, exact source-lineage checks, adversarial validators, explicit frontier blockers, and accumulated negative knowledge.

The current CM structure is naturally interpreted as a persistent proof-development graph:

```text
                         CM4 TARGET
                       frontier / open
                             |
                    +--------+--------+
                    |                 |
                CM4-P2 / C05      open blockers
                    |
                    v
                   CM3
          abelian / AB exactness
                    |
                    v
                   CM2
          Cartesian closedness
                    |
                    v
                   CM1
       discrete-underlying adjunction
                    |
          +---------+---------+
          |         |         |
          v         v         v
          V0    NAT concord.  Euclid bridge
             protected substrate
```

CM1-CM3 should increasingly be treated as protected dependency layers rather than repeatedly rediscovered search territory. CM4 and successors form the active frontier obligation graph.

### Condensed migration discipline

Existing CM1-CM4/CMDG artifacts were not historically produced as MATH-CORE live events. Their initial MATH-CORE representation must therefore be an additive, provenance-bound import from an explicit migration checkpoint, not retroactive event history.

The representation must preserve distinctions among:

- exact formal replay evidence;
- protected dependency-layer status;
- canonical claim status;
- MATHCERT certification status;
- open mathematical frontier obligations.

A formal replay or protected fixture must not be upgraded to a certified or canonical theorem merely by import.

### Blocker taxonomy

Active programme blockers should be typed at least as:

1. **`MATHEMATICAL`** — the implication, construction, or theorem is not presently known or established.
2. **`FORMALIZATION`** — the mathematics is known or otherwise justified, but the formal substrate, API, implementation, or representation bridge is absent.
3. **`GOVERNANCE_EVIDENCE`** — mathematical/formal evidence exists, but provenance, exact identity, independent review, certification, or governed promotion requirements remain incomplete.
4. **`EXECUTION_INFRASTRUCTURE`** — runtime, controller, tooling, resource, connector, or operational execution conditions block progress without constituting a mathematical or formalization deficit.

This classification prevents the shorthand `blocked` from obscuring the kind of work actually required and prevents recoverable execution failures from being mislabeled as mathematical deficits.

## 11. Specialist capabilities

New mathematical capabilities should normally enter as theory agents or services behind MATH-CORE rather than as new top-level pillars. Examples include algebraic reasoners, SAT/SMT, CAS, numerical and combinatorial search, literature retrieval, geometric reasoning, proof repair, source reconstruction, counterexample search, and specialized formal tactics.

Elevation to a new institutional pillar requires an explicit governance decision identifying a durable responsibility or authority distinction that cannot be represented adequately as a service within the existing pillars.

## 12. Migration and compatibility principle

Existing protected artifacts, campaign ledgers, certificates, CI receipts, formal proofs, historical decisions, and programme names remain authoritative according to their existing contracts. MATH-CORE representation must not silently reclassify historical evidence.

Migration is additive:

- import existing canonical claims as external canonical references;
- bind exact source/formal/certificate identities;
- preserve existing certification and claim boundaries;
- represent currently open obligations as imported/reconstructed state rather than pretending they were historically emitted as MATH-CORE events;
- distinguish reconstructed historical state from newly generated live state;
- retain programme-specific semantic validators where generic protocol validity is insufficient;
- establish an explicit migration checkpoint after which newly admitted events constitute live MATH-CORE history.

## 13. Intended operational flow

```text
Human Steward / MATH-PROGRAMME governance
                 |
                 v
             INTELLECT
          search / routing
                 |
             MATH-CORE
        typed reasoning state
          /      |       \
         /       |        \
 MATHFORGE   MATHSOLVE   MATHCERT
 discovery/    campaign    assurance
   source      reasoning
       \          |          /
        \         |         /
         +--------+--------+
                  |
       TRUSTED ACCEPTANCE BOUNDARY
                  |
     proof checking / replay / certification
                  |
         governed canonical recording
```

AETHER may transport interactions across this system but does not alter the authority structure.

## 14. First post-ratification integration stage

Subject to the stage gates recorded by Council, the first integration operation should be:

**`MCORE-DOMAIN-SHADOW-001` — Condensed Mathematics read-only shadow materialization.**

It should:

- import protected CM1-CM4/CMDG state into a scoped MATH-CORE domain graph;
- preserve exact provenance and historical status distinctions;
- introduce no retroactive live-event fiction;
- classify open blockers using the controlled blocker taxonomy;
- compare the materialized graph with existing protected CMDG/CM validators;
- drive no autonomous allocation, pruning, certification, or canonical promotion.

Only after the domain-bridge, coordinator-safety, assurance-binding, and execution-routing gates are discharged should INTELLECT use the graph to allocate or prune live research work.

## 15. Council correction register incorporated

This corrected candidate incorporates the eight Council amendments recorded in `docs/MATH_CORE_01_COUNCIL_DELIBERATION_001.md`:

- `MCORE-ARCH-C01` — preserve/reconcile the three-pillar doctrine;
- `MCORE-ARCH-C02` — controlled topology and authority vocabulary;
- `MCORE-ARCH-C03` — domain-subgraph isolation and bridge semantics;
- `MCORE-ARCH-C04` — live coordinator identity, concurrency, admission, and invalidation controls;
- `MCORE-ARCH-C05` — exact evidence binding for replayable/checked operational assurance;
- `MCORE-ARCH-C06` — provenance-safe Condensed migration and four-way blocker taxonomy;
- `MCORE-ARCH-C07` — mandatory persistent execution routing and AETHER boundary;
- `MCORE-ARCH-C08` — governed memorialization and terminal documentary closure.

C01, C02, and C08 block protected architectural authority. C03-C07 are stage-bounded implementation gates that must be satisfied before their corresponding live capabilities are enabled.

## 16. Memorialization and authority boundary

This memorial is the Council-corrected architectural candidate. It does not itself amend standing governance, create a new programme status, certify mathematics, promote a claim, or authorize external representations.

Final authority requires:

1. protected registration of the Construction Gate review target;
2. exact corrected-candidate admission/freeze under the governed route when appropriate;
3. explicit Human Steward disposition on the corrected exact candidate;
4. exact-head CI and independent review;
5. protected merge and protected-main readback;
6. a dedicated ADR and reconciliation of the decision index, artifact ledger, terminology registry, and `ARCHITECTURE_OVERVIEW.md`;
7. applicable documentary closure/readback sealing before terminal status is claimed.

## 17. Claim boundary

Ratification of this architecture, if it occurs, would authorize an organizational and technical integration model only. It would not:

- prove or certify any new mathematical theorem;
- upgrade existing Condensed Mathematics frontier targets;
- certify dependency edges merely because they are represented in MATH-CORE;
- establish foundational consistency;
- confer novelty or priority;
- authorize publication or external scientific claims;
- confer patentability, product, deployment, or commercial authority.

Those remain governed by their separate evidentiary and authority routes.
