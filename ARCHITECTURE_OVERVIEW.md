# Architecture Overview

## The missing middle

The earlier two-part split, MATHFORGE plus MATHCERT, was logically clean but structurally incomplete. It separated exploration from certification, yet omitted the long middle process where Grand Challenge work actually happens. The Chaidez-style Work Packages did not merely discover problems or certify final theorems. They built mathematical campaigns: normal forms, restricted theorem targets, proof attempts, compact residual reductions, exact screens, interval scaffolds, failure ledgers, and plain-language companions.

That middle is now named **MATHSOLVE**.

```text
MATHFORGE  ->  MATHSOLVE  ->  MATHCERT
discover       attack         certify
```

A more faithful picture is:

```text
raw mathematical signal
  -> reconstructed source context
  -> problem card
  -> status spine
  -> theorem spine
  -> work-package campaign
  -> claim ledger
  -> certification handoff
  -> checked artifact or rejected claim
```

The architecture exists to prevent each stage from pretending to be the next one.

## Three-pillar doctrine

### MATHFORGE

MATHFORGE is the exploratory foundry. It ingests open-problem corpora, source papers, surveys, repository data, examples, counterexamples, computational searches, and speculative conjectures. Its output is not mathematical authority. Its output is candidate ore.

Its governing question is:

> What is worth carrying into a disciplined campaign?

### MATHSOLVE

MATHSOLVE is the campaign room. It turns promising ore into disciplined mathematical form: status spines, theorem candidates, reductions, exact computations, Work Packages, failed attempts, lay explanations, and certification handoffs. MATHSOLVE is allowed to be incomplete, but it must be honest.

Its governing question is:

> What exact mathematical obligation have we clarified?

### MATHCERT

MATHCERT is the assay office. It checks, rejects, certifies, or records the exact status of claims. It is Lean-first but not Lean-only. It also admits exact rational computation, interval arithmetic, SAT/SMT proof artifacts, theorem prover alternatives, and independently replayable certificate ledgers.

Its governing question is:

> What has crossed a trusted proof or replay boundary?

## The promotion path

```text
Candidate problem card
  -> Status audit
  -> Work Package 01: problem spine
  -> Work Package 02: definitions and reductions
  -> Work Package 03+: restricted results, exact screens, failure analysis
  -> MATHCERT handoff
  -> formal statement / checked lemma / exact certificate / interval certificate
  -> public claim
```

No artifact is promoted merely because it sounds mathematical. Promotion requires a claim type, support type, source trail, and certification route.

## Why three pillars instead of one repo

The three functions have different failure modes.

- MATHFORGE fails by hallucinating promise, over-selecting fashionable problems, or producing noisy conjectures.
- MATHSOLVE fails by writing impressive prose without theorem-grade obligations, hiding dead ends, or confusing evidence with proof.
- MATHCERT fails by becoming a technical shrine disconnected from mathematical understanding, or by formalizing statements that nobody has explained.

Separating the pillars allows each to check the others.

## Cross-pillar lanes

Some workflows cut across all three pillars. These are called lanes. A lane is a reusable route from discovery to tactic to certification.

The first explicit lane is the algebraic witness-to-certificate route:

```text
MATHFORGE: external CAS or exact symbolic search emits a witness
MATHSOLVE: recognizes the algebraic subproblem and routes the tactic
MATHCERT: replays or Lean-checks the certificate before promotion
```

The lane doctrine lives in `docs/CROSS_PILLAR_LANES.md`.

## MATH-CORE-01 coordination substrate

The three pillars require a shared semantics for live mathematical state. `MATH_CORE_01_CLAIM_BLACKBOARD_PROTOCOL.md` supplies that missing coordination substrate.

```text
                    INTELLECT
                 search controller
                       |
                       v
             +-------------------+
             | CLAIM BLACKBOARD  |
             | claims            |
             | obligations       |
             | conflicts         |
             | learned search    |
             | constraints       |
             | equivalences      |
             | witnesses         |
             | certificates      |
             +---------+---------+
                       |
          +------------+-------------+
          |            |             |
      MATHFORGE     MATHSOLVE      MATHCERT
       theory        theory         checker /
       plugins       plugins        certifier
```

MATH-CORE-01 is event-sourced and proposal-driven. Theory agents do not mutate canonical mathematical authority directly. They propose propagations, conflicts, witnesses, and equivalences against an exact checkpoint. A reducer validates capabilities, dependencies, and evidence boundaries before accepting blackboard events.

Conflict-derived learning is explicitly operational and assurance-bounded. A heuristic conflict may only bias search; a replayable conflict may support local pruning; hard pruning requires a checked conflict from MATHCERT or a designated checker. Every learned constraint remains `SEARCH_ONLY` until separately stated, supported, and promoted through the canonical claim-ledger and certification route. Certificates are content-addressed evidence carriers and likewise have no direct ledger mutation effect.

The current transport may be GitHub, JSON, CI, and content-addressed artifacts. A future AETHER implementation may carry the same protocol without becoming a semantic dependency.

## Ratified programme placement

ADR-0021 places the existing three-pillar doctrine inside a larger authority topology. The pillars remain the stable mathematical reasoning institutions; MATH-CORE is horizontal coordination semantics rather than a fourth pillar.

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
  proof/replay checking
  + independent assurance
  + certification ladder
  + canonical Claim Ledger
  + policy disposition where required

ORTHOGONAL INFRASTRUCTURE
  GitHub / JSON / CI / content-addressed artifacts / AETHER
```

A plane is an authority and responsibility band, not necessarily a literal software hop. The trusted acceptance boundary is likewise plural: proof checking, independent assurance, certification, canonical recording, and policy disposition are separate functions and no one function silently implies the others.

### Stable pillars and services

MATHFORGE retains its broad foundry role: source intake and reconstruction, examples and counterexamples, computational exploration, formal-object production, and speculative candidates. MATHSOLVE remains disciplined campaign reasoning against explicit obligations. MATHCERT remains independent assurance. New capabilities default to governed theory agents or reasoning services rather than new pillars; creation, retirement, or material redefinition of a pillar requires explicit governance.

### Domain programmes are scoped subgraphs

A long-lived mathematical programme such as Condensed Mathematics is represented as a scoped MATH-CORE claim/obligation subgraph with explicit programme or family identity and an explicit migration checkpoint. It is not a fourth pillar and is not literal middleware through which all pillar calls must pass.

Cross-domain dependencies, equivalences, and evidence are represented by typed bridge relations. A bridge must carry explicit evidence and does not transfer certification or canonical status implicitly. Existing historical campaigns are imported as provenance-bound reconstructed/protected state rather than rewritten as fictitious retroactive MATH-CORE event history.

Domain-specific semantic validators may therefore impose stronger obligations than generic MATH-CORE protocol validity. A well-formed event envelope does not by itself discharge a mathematical domain obligation.

### Live coordinator boundary

INTELLECT is the search and routing function: it decides where to reason, while MATH-CORE records exact reasoning state. Before live sustained coordination, authenticated execution identity, exact-checkpoint concurrency, stale-result rejection, deterministic admission receipts, supersession/invalidation, bounded budgets, and no-self-authorization controls are required. Production replayable or checked pruning must bind evidence to exact checkpoints and content-addressed artifacts, content sets, or versioned replay manifests.

Unattended persistent coordination must run under an exact admitted controller compatible with current GH-OS routing. A bounded conversational agent may perform individually authorized transactions but is not represented as the sole unattended persistent controller.

### Condensed migration and blocker classes

The first substantial domain integration is `MCORE-DOMAIN-SHADOW-001`, a read-only shadow materialization of existing protected Condensed/CMDG state. It must preserve distinctions among formal replay, protected dependency state, certification, and canonical claim state; it introduces no retroactive live-event fiction and drives no autonomous allocation or pruning.

Operational blockers are classified at least as:

- `MATHEMATICAL`;
- `FORMALIZATION`;
- `GOVERNANCE_EVIDENCE`;
- `EXECUTION_INFRASTRUCTURE`.

This prevents tooling or runtime failures from being mislabeled as formal or mathematical blockers.

### Transport remains authority-neutral

AETHER is an orthogonal transport and memory fabric. It may eventually carry MATH-CORE and INTELLECT state, but it does not become the reasoning semantics, proof boundary, Claim Ledger, or policy authority. The same rule applies to GitHub, JSON, CI, and other transport mechanisms.

## Classification and discovery layer

The three-pillar workflow also shares a programme-owned information layer:

```text
MSC2020-SKOS          -> versioned subject mappings
external discovery    -> reviewed evidence records
internal graph        -> programme concepts, relations, and state
```

MSC2020-SKOS is the stable classification spine. It does not define mathematical
dependencies or programme meaning. Those belong to the versioned internal
knowledge graph.

MATHFORGE queries zbMATH Open for mathematics-specific literature, OpenAlex for
semantic and citation discovery, and arXiv for current-awareness intake. Results
remain discovery evidence until a human review promotes a normalized record into
an audited mapping or graph assertion. OntoMathPRO may inform graph design but is
not a runtime or governance dependency.

## Naming note

MATHSMELT remains a useful internal term for the refinement phase inside MATHSOLVE, but it is not the public pillar. MATHSOLVE is clearer and more institutional. It does not mean that the system magically solves mathematics. It means the system organizes the struggle.

## Binding maxim

> No theorem without a spine. No computation without a ledger. No conjecture without a map. No proof without a reader.