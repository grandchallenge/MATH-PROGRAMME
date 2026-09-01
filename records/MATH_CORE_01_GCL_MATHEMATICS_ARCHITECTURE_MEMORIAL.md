# MATH-CORE-01 and the GCL Mathematics Architecture

## Council memorial candidate

**Docket:** COUNCIL-MCORE-ARCH-001 / issue #721  
**Status:** Candidate for Council deliberation; not yet Council-ratified  
**Protected baseline:** `grandchallenge/MATH-PROGRAMME@3c7aa5298debd6564e3f93a7a05b4f6821cd3bb2`  
**Human Steward direction:** architecture approved as submitted and referred to Council for deliberation, potential amendments, approval, and governed memorialization  
**Authority boundary:** material Council corrections require a subsequent Human Steward disposition on the corrected exact candidate before protected admission

## 1. Architectural thesis

GCL Mathematics should be organized as a governed mathematical operating architecture rather than as a loose collection of repositories or peer agents.

The core separation is:

1. **Governance plane** — MATH-PROGRAMME, Human Steward authority, standards, policy, decision records, claim-boundary doctrine, and documentary continuity.
2. **Control and coordination plane** — INTELLECT as search/controller; MATH-CORE-01 as typed reasoning-state semantics and shared blackboard.
3. **Reasoning plane** — stable institutional pillars MATHFORGE, MATHSOLVE, and MATHCERT, plus specialist theory agents/services operating through MATH-CORE contracts.
4. **Trusted acceptance plane** — proof kernels such as Lean, independent replay, the certification ladder, and the canonical Claim Ledger.
5. **Transport and memory substrate** — AETHER may eventually carry state and execution coordination across the architecture but does not define mathematical truth, certification semantics, or canonical promotion.

The governing direction is:

> Governance constrains coordination; coordination routes specialized reasoning; independent assurance gates trusted acceptance; canonical state changes only through explicit governed authority.

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

## 4. INTELLECT

INTELLECT is the programme search/control layer.

Its proper authority is to:

- inspect materialized MATH-CORE state;
- allocate attention and compute;
- decompose large goals into explicit obligations;
- select and route specialist reasoners;
- consume typed proposals;
- exploit assurance-bounded learned constraints;
- preserve or reopen unresolved work when evidence changes.

INTELLECT does not own mathematical truth, certification authority, protected-branch authority, or Human Steward authority.

The architectural distinction is:

> INTELLECT decides where to reason; MATH-CORE records what the reasoning state is; specialist pillars perform or check the reasoning; trusted machinery and governance determine what may be accepted.

## 5. Stable institutional pillars

### 5.1 MATHFORGE

MATHFORGE owns source integrity, source acquisition, reconstruction, normalization, formal-object production, provenance, and controlled mappings among source, representation, and formal artifacts.

Its natural MATH-CORE outputs include source witnesses, formal objects, scoped equivalences, and provenance-bearing assertions. It does not certify mathematical truth merely by reconstructing or formalizing an object.

### 5.2 MATHSOLVE

MATHSOLVE owns exploratory mathematical reasoning: proof search, decomposition, conjecture generation, computations, counterexamples, reductions, tactics, failed routes, and candidate lemmas.

Its natural MATH-CORE outputs include `PROPAGATE`, `CONFLICT`, `WITNESS`, `EQUIVALENCE`, and explicit `UNKNOWN` responses. Search breadth belongs here; canonical truth authority does not.

### 5.3 MATHCERT

MATHCERT is the independent assurance pillar, deliberately asymmetric with MATHSOLVE.

It independently replays or checks precisely identified targets and evidence, records checked conflicts or certificates, and supplies stronger assurance classes where justified. MATHCERT evidence may support stronger operational consequences in MATH-CORE, but certificate recording does not directly mutate the canonical Claim Ledger.

MATHCERT must not collapse into a merely stronger solver agent; independence and claim-boundary discipline are institutional properties.

## 6. Trusted acceptance plane

The trusted acceptance plane contains the mechanisms that may contribute to governed acceptance under declared foundations and policies:

- Lean or other explicitly admitted proof kernels;
- deterministic and independent replay;
- the certification ladder;
- the canonical Claim Ledger;
- protected review and Human Steward dispositions where required.

MATH-CORE sits above this boundary. It may accumulate checked artifacts and resolved obligations without silently promoting claims.

## 7. Human Steward

The Human Steward retains policy and exceptional disposition authority as defined by standing governance. Steward approval is not a mathematical proof object and does not discharge a mathematical obligation merely by declaration.

The Steward may approve architecture, authorize governed transitions, resolve policy questions, and issue required dispositions. Mathematical evidence remains subject to its own proof and certification routes.

## 8. AETHER

AETHER is orthogonal infrastructure for transport, durable memory, coordination, and eventually distributed execution.

The intended relation is:

```text
MATH-CORE = semantics and reasoning-state contract
AETHER    = transport / memory / coordination fabric
```

MATH-CORE events must retain their meaning whether transported today through GitHub/JSON/CI or later through AETHER. AETHER availability is therefore not part of the current MATH-CORE trust assumption.

## 9. Domain mathematical programmes

Condensed Mathematics, Odd Zeta, Union-Closed, BSD, Hodge, Navier-Stokes, Yang-Mills, Riemann, and successor programmes should not normally become new authority pillars.

They are better modeled as long-lived domain-specific claim/obligation subgraphs hosted by MATH-CORE. The same institutional pillars operate across them according to their distinct roles.

The exact model is not that domain programmes form an intermediate software layer between MATH-CORE and the pillars. Rather:

> MATH-CORE hosts many mathematical programmes; the pillars operate on their typed objects.

This permits stable governance and reasoning institutions while allowing the programme portfolio to expand without architectural proliferation.

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

MATH-CORE should make three blocker classes explicit:

1. **Mathematical blocker** — the implication, construction, or theorem is not presently known or established.
2. **Formalization blocker** — the mathematics is known or otherwise justified, but the formal substrate, API, implementation, or representation bridge is absent.
3. **Governance/evidence blocker** — mathematical or formal evidence exists, but provenance, exact identity, independent review, certification, or governed promotion requirements remain incomplete.

This classification should prevent the present operational shorthand `blocked` from obscuring the type of work actually required.

## 11. Specialist capabilities

New mathematical capabilities should normally enter as theory agents or services behind MATH-CORE rather than as new top-level pillars. Examples include algebraic reasoners, SAT/SMT, CAS, numerical and combinatorial search, literature retrieval, geometric reasoning, proof repair, source reconstruction, counterexample search, and specialized formal tactics.

Promotion to a new institutional pillar should therefore require a demonstrated authority or governance distinction that cannot be represented adequately as a service within an existing pillar.

## 12. Migration and compatibility principle

Existing protected artifacts, campaign ledgers, certificates, CI receipts, formal proofs, and historical decisions remain authoritative according to their existing contracts. MATH-CORE representation must not silently reclassify historical evidence.

Migration should be additive:

- import existing canonical claims as external canonical references;
- bind exact source/formal/certificate identities;
- preserve existing certification and claim boundaries;
- materialize currently open obligations without pretending they were historically recorded as MATH-CORE events;
- distinguish reconstructed historical state from newly generated live state;
- retain programme-specific semantic validators where generic protocol validity is insufficient.

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
    source      search     assurance
       \          |          /
        \         |         /
         +--------+--------+
                  |
       TRUSTED ACCEPTANCE BOUNDARY
                  |
       Lean / replay / certification
                  |
          canonical Claim Ledger
```

AETHER may transport interactions across this system but does not alter the authority structure.

## 14. Ratification questions

Council is specifically asked to test:

- whether the plane/pillar/programme distinction is coherent and durable;
- whether MATH-CORE's role is sufficiently authority-neutral;
- whether INTELLECT can coordinate safely without acquiring implicit truth authority;
- whether MATHFORGE, MATHSOLVE, and MATHCERT remain sufficiently separated;
- whether domain-programme subgraphs need additional cross-domain invariants;
- whether the Condensed placement is faithful to its protected CM1-CM4 evidence spine;
- whether additional adversarial, concurrency, invalidation, or identity controls are required before live coordination;
- whether any terminology in this memorial could cause claim or authority laundering;
- what the first post-ratification integration stage should be.

## 15. Memorialization and authority boundary

This memorial is a candidate architectural statement for Council review. It does not itself amend standing governance, create a new programme status, certify mathematics, promote a claim, or authorize external representations.

A Council recommendation must be durably recorded with all required office findings and Referee synthesis. Material corrections must be incorporated into an exact candidate and returned to the Human Steward for explicit disposition. Final authority requires the applicable protected-review, CI, independent-review, merge, readback, and documentary-continuity route.

## 16. Claim boundary

Ratification of this architecture, if it occurs, would authorize an organizational and technical integration model only. It would not:

- prove or certify any new mathematical theorem;
- upgrade existing Condensed Mathematics frontier targets;
- certify dependency edges merely because they are represented in MATH-CORE;
- establish foundational consistency;
- confer novelty or priority;
- authorize publication or external scientific claims;
- confer patentability, product, deployment, or commercial authority.

Those remain governed by their separate evidentiary and authority routes.
