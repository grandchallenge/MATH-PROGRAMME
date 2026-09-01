# MATH-CORE-01: Claim Blackboard and Theory-Agent Protocol

## Status

Candidate programme-core specification, protocol version `MATH-CORE-01/0.1.0`.

This specification is additive. It does not replace `CLAIM_LEDGER_STANDARD.md`, the certification ladder, MATHCERT, the Human Steward authority boundary, or any proof kernel. It defines the coordination semantics between them.

Normative terms `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, and `MAY` are used in their ordinary standards sense.

## 1. Purpose

MATH-CORE-01 turns the Programme's distributed mathematical work into an explicit, replayable state machine.

The governing architecture is:

```text
heuristic search / discovery
          |
          v
+-----------------------------+
|       CLAIM BLACKBOARD      |
| claims and obligations      |
| dependencies                |
| conflicts + assurance       |
| learned search constraints  |
| equivalences                |
| witnesses                   |
| evidence and certificates   |
+-------------+---------------+
              |
       proposal / response
              |
   +----------+-----------+
   | theory-agent plugins |
   +----------+-----------+
              |
              v
        independent check
              |
              v
 canonical ledger / MATHCERT / kernel
```

The blackboard is a coordination plane, not a source of mathematical authority. Its job is to make mathematical state explicit enough that independent reasoners can cooperate without silently upgrading evidence, losing failure information, or confusing a plausible branch with a certified result.

The architectural rule is:

> Heuristic search may be permissive; state transitions must be typed; trusted promotion must remain evidence-backed and independently checkable.

## 2. Relationship to existing Programme contracts

The canonical claim ledger remains the trust spine for governed mathematical assertions. A blackboard claim that is absent from the canonical ledger remains a working object and MUST NOT be presented as canonical mathematical content merely because it exists in MATH-CORE-01.

MATH-CORE-01 therefore separates two concerns:

- **live reasoning state**: obligations, speculative claims, derived consequences, conflicts, witnesses, equivalences, and search constraints;
- **governed claim state**: the canonical claim ledger, certification artifacts, review status, and promotion conditions.

A `CERTIFICATE` blackboard event records the existence and result of an independently checkable artifact. It does not itself mutate a canonical claim ledger entry. Ledger promotion continues through the existing governed route.

Repository merge, CI success, agent confidence, majority vote, or blackboard persistence are not proof support types.

## 3. Core objects

MATH-CORE-01 recognizes seven durable reasoning objects.

### 3.1 Claim

A proposition that may be investigated, supported, refuted, or proposed for the canonical claim ledger.

A claim may be speculative. Its presence on the blackboard has no automatic certification effect.

### 3.2 Obligation

An explicit goal to be discharged. An obligation states what must be established and what classes of evidence are acceptable.

The obligation, rather than the agent, is the long-lived unit of work. An obligation is opened exactly once and remains in the materialized `open_obligations` view until an explicit `RESOLVE_OBLIGATION` event moves it to `resolved_obligations` with one of three working outcomes: `DISCHARGED`, `REFUTED`, or `WITHDRAWN`.

`DISCHARGED` and `REFUTED` are reasoning-state outcomes, not canonical claim promotions. They require supporting reasoning objects in addition to the obligation itself. `WITHDRAWN` records deliberate abandonment of the working obligation and does not assert its truth or falsity.

### 3.3 Conflict

A recorded incompatibility, failed obligation, checker rejection, or counterexample-bearing contradiction together with an explanation set.

A conflict MUST identify the finite dependency set sufficient for the reported failure to the precision available. Minimal explanations are preferred but are not required in protocol version 0.1.0.

A conflict also carries an assurance level:

- `HEURISTIC`: a reasoner reports a plausible failure or incompatibility that has not crossed a replay boundary;
- `REPLAYABLE`: the conflict is backed by an independently repeatable artifact or deterministic calculation, but has not necessarily crossed the Programme's certification boundary;
- `CHECKED`: the conflict is recorded by MATHCERT or a designated checker and is backed by checker evidence.

The assurance level limits how aggressively the coordinator may learn from the conflict.

### 3.4 Search constraint

A reusable operational restriction learned from a conflict. Search constraints can reprioritize, locally prune, or, under checked conditions, hard-prune future search.

Every learned search constraint MUST declare `effect: SEARCH_ONLY`. It MUST NOT be silently reinterpreted as a mathematical theorem. Promotion to a canonical mathematical claim requires the ordinary claim-ledger and certification route.

### 3.5 Equivalence

A scoped assertion that two or more identifiers denote the same source object, mathematical object, representation, or certified artifact.

Equivalence is provenance-sensitive. `SOURCE_EQUIVALENT`, `REPRESENTATION_EQUIVALENT`, and `MATHEMATICALLY_EQUIVALENT` are distinct scopes. A syntactic alias MUST NOT be promoted to mathematical equivalence without appropriate evidence.

Only a `MATHEMATICALLY_EQUIVALENT` relation with evidence may be considered for mathematical substitution, and any consumer still applies its own certification and foundational policy. Lower equivalence scopes are navigation/provenance relations, not proof substitution rules.

### 3.6 Witness

A constructive artifact: example, model, assignment, exact computation, counterexample, normal form, source excerpt, proof sketch artifact, or other object that bears on a claim or obligation.

A witness records what exists; it does not imply that the surrounding theorem has been proved.

### 3.7 Certificate

A reference to an independently replayable or independently checked artifact together with checker identity and result.

Certificates are evidence carriers. MATHCERT and the existing certification ladder determine their governed effect. A certificate payload MUST carry a SHA-256 artifact identity in addition to its artifact locator.

## 4. Blackboard event model

The blackboard is event-sourced. The normative wire schema is `schemas/math_core_blackboard.schema.json`.

Every event carries:

- `event_id`: stable unique event identifier;
- `event_type`: one protocol verb;
- `producer`: producer identity class and execution identity;
- `base_checkpoint`: exact state against which the producer reasoned;
- `subject`: typed object identifier created or affected by the event;
- `scope`: programme/family/work-package scope;
- `dependencies`: explicit prior objects required by the event;
- `evidence_refs`: immutable references to supporting evidence when applicable;
- `payload`: event-specific content;
- `created_at`: provenance timestamp, never a semantic ordering mechanism.

The ordered event list is the semantic input to replay. Timestamps MUST NOT determine replay order.

A `GIT_COMMIT` checkpoint MUST carry an exact 40-hex commit identity. A `CONTENT_SET` checkpoint MUST carry a `sha256:<64-hex>` revision. A future transport may define additional exact identities, but a mutable label is not an exact checkpoint.

### 4.1 ASSERT

Introduces a working claim.

`ASSERT` MUST contain a complete statement. It MAY be speculative. It does not alter the canonical claim ledger.

### 4.2 OPEN_OBLIGATION

Introduces a goal and its admissible evidence policy.

An obligation SHOULD be narrow enough that a theory agent can return a concrete propagation, conflict, witness, or `UNKNOWN` response. Opening an obligation creates the durable working object; subsequent reasoning refers to that object rather than recreating it.

### 4.3 RESOLVE_OBLIGATION

Moves one previously opened obligation from the open view to the resolved view.

`RESOLVE_OBLIGATION` MUST target an existing `OBLIGATION`, MUST include that obligation in its dependency set, and MUST occur at most once for that obligation. Its payload contains:

- `outcome: DISCHARGED` when the working goal has been satisfied;
- `outcome: REFUTED` when the working goal has been contradicted or shown impossible under the declared interpretation;
- `outcome: WITHDRAWN` when the Programme deliberately stops pursuing the working goal without asserting truth or falsity;
- a non-empty `reason` describing the disposition.

`DISCHARGED` and `REFUTED` MUST cite at least one supporting prior reasoning object in addition to the obligation itself. A resolution is a state-management event; it does not certify a canonical claim, create a proof support type, or bypass MATHCERT.

### 4.4 PROPAGATE

Introduces a consequence derived from prior objects.

`PROPAGATE` MUST name a non-empty dependency set and MUST state the consequence. A propagation without dependencies is an assertion and must use `ASSERT` instead.

### 4.5 CONFLICT

Records an incompatibility or failure and its explanation.

A conflict MUST name at least one dependency, MUST state why those dependencies cannot jointly support the attempted branch, and MUST declare `assurance` as `HEURISTIC`, `REPLAYABLE`, or `CHECKED`.

`REPLAYABLE` and `CHECKED` conflicts MUST carry evidence references. A `CHECKED` conflict MUST be recorded by MATHCERT or a designated `CHECKER`; a heuristic theory agent cannot self-upgrade its conflict by changing the assurance label.

### 4.6 LEARN

Creates a search constraint from an existing conflict.

`LEARN` MUST reference exactly one source conflict, MUST depend on that conflict, and MUST declare `effect: SEARCH_ONLY` in protocol version 0.1.0.

It also declares one enforcement level:

- `SOFT_AVOID`: reprioritize or avoid the branch, but do not treat it as excluded;
- `LOCAL_PRUNE`: exclude the branch inside the declared search scope/checkpoint; requires source assurance `REPLAYABLE` or `CHECKED`;
- `HARD_PRUNE`: treat the branch as operationally excluded under the same declared semantics; requires a `CHECKED` source conflict from MATHCERT or a designated checker with evidence.

The enforcement monotonicity rule is:

```text
HEURISTIC  -> SOFT_AVOID
REPLAYABLE -> SOFT_AVOID | LOCAL_PRUNE
CHECKED    -> SOFT_AVOID | LOCAL_PRUNE | HARD_PRUNE
```

This rule is essential. In SAT/CDCL, a learned clause is logically entailed by a precisely defined formal state. In frontier mathematical research, an agent-reported conflict may be heuristic, incomplete, or based on a mistaken interpretation. MATH-CORE-01 therefore does not allow a weak conflict report to become a hard global exclusion.

Even `HARD_PRUNE` remains an operational search effect. It is not automatic theorem promotion.

### 4.7 EQUIVALENCE

Records a scoped identity/equivalence relation over at least two members.

The relation scope MUST be one of:

- `IDENTIFIER_ALIAS`;
- `SOURCE_EQUIVALENT`;
- `REPRESENTATION_EQUIVALENT`;
- `MATHEMATICALLY_EQUIVALENT`.

Only the last category asserts mathematical equivalence; it therefore requires evidence references.

### 4.8 WITNESS

Attaches a witness to a claim or obligation.

The witness payload MUST state its role, for example `EXAMPLE`, `COUNTEREXAMPLE`, `MODEL`, `EXACT_COMPUTATION`, `SOURCE_OBJECT`, or `PROOF_ARTIFACT`. A witness SHOULD be content-addressed when it is intended for replay or durable comparison.

### 4.9 CERTIFICATE

Attaches an independent checker result.

A certificate MUST state the checker, certificate kind, immutable artifact reference, SHA-256 artifact identity, result, and target object. `PASS` records evidence; it does not directly edit claim-ledger status. `FAIL` is evidence of a certification conflict and SHOULD normally be accompanied or followed by a `CONFLICT` event.

### 4.10 SUPERSEDE

Retires a blackboard working object in favor of a replacement without deleting history.

MATH-CORE-01 is append-only. Corrections occur by supersession, not mutation of prior events.

## 5. Theory-agent protocol

Theory agents are untrusted or partially trusted reasoning plugins. They do not mutate the blackboard directly.

The normative request/response schema is `schemas/math_core_theory_agent.schema.json`.

A coordinator sends a `REQUEST` containing:

```text
exact checkpoint
obligation identifier
goal
context references
assumptions
acceptable evidence classes
requested capability
resource budget (optional)
```

An agent returns a `RESPONSE` containing zero or more typed proposals:

```text
PROPAGATION
CONFLICT
WITNESS
EQUIVALENCE
```

or a terminal disposition:

```text
UNKNOWN
ERROR
```

The reducer validates a response and decides whether proposed content becomes blackboard events. The producer cannot make an event authoritative merely by returning it.

A response MAY include a heuristic score or confidence estimate for scheduling. Such values are explicitly non-normative and MUST NOT alter claim status, certainty, conflict assurance, pruning enforcement, obligation outcome, certification status, or checker outcome.

## 6. Producer classes and capability boundary

The candidate capability registry is `governance/math_core_01/capability_registry.json`.

Producer classes are roles, not self-declared authority. The reducer MUST validate an event against the external capability registry.

The initial allocation is deliberately conservative:

| Producer class | Intended capability |
| --- | --- |
| `HUMAN_STEWARD` | explicit human-directed working assertions/obligations and supersession; governance authority remains external to automatic inference |
| `INTELLECT` | scheduling, working assertions/obligations, explicit working-obligation resolution, conflict-derived search learning, supersession |
| `MATHFORGE` | exploratory assertions, witnesses, working equivalence events and theory proposals |
| `MATHSOLVE` | obligations, explicit working-obligation resolution, propagations, conflicts, witnesses, search learning, equivalences, supersession |
| `MATHCERT` | checker-backed conflicts, certificate recording, evidence-bearing equivalence review |
| `CHECKER` | machine-checker conflict outcomes and certificate production |
| `EXTERNAL_TOOL` | witness events and theory proposals unless independently wrapped by a checker route |

No producer class is allowed to promote a canonical claim merely by emitting a protocol message.

Authentication of a concrete producer identity is external to the wire payload. A producer cannot obtain capabilities by writing a more privileged class string into its own message.

## 7. State invariants

A conforming reducer MUST enforce the following invariants.

### I1. Append-only history

Accepted events are immutable. Corrections use `SUPERSEDE` or later contrary evidence.

### I2. Exact-checkpoint provenance

Every event and theory-agent exchange is bound to an exact base checkpoint. A stale response MAY be retained as historical evidence but MUST NOT be applied as current state without an explicit revalidation/rebase step.

### I3. Dependency closure

Every local dependency reference MUST resolve to an earlier object in the same replay, or to an explicitly marked external canonical reference.

### I4. No trust by assertion

Neither producer identity, natural-language confidence, repeated agreement, nor blackboard persistence can substitute for the evidence requirements of the canonical claim ledger or certification ladder.

### I5. Certificate independence

A certificate event MUST identify an independent checker or certification route and an immutable, content-addressed artifact identity. The same heuristic agent that proposed a claim cannot manufacture certification authority by relabeling its own prose as a certificate.

### I6. Search/theorem separation

`LEARN` creates operational search constraints only. A learned constraint becomes mathematical content only through a separate claim and ordinary promotion route.

### I7. Assurance-bounded pruning

A learned constraint MUST NOT enforce more strongly than its source conflict assurance permits. Heuristic conflicts are advisory; replayable conflicts may support local pruning; hard pruning requires checked evidence from a certifying producer.

### I8. Scoped equivalence

Equivalence is not transitive across incompatible scopes. In particular, identifier aliasing does not imply source equivalence; source equivalence does not imply proof equivalence; representation equivalence does not imply certification equivalence.

### I9. Deterministic replay

Given the same protocol version, capability registry, external canonical references, and ordered accepted event list, a conforming reducer MUST produce the same materialized blackboard state.

### I10. Fail closed on promotion

Malformed, unauthorized, stale, or insufficiently evidenced events may be rejected or quarantined. They MUST NOT increase governed claim authority.

### I11. Human authority preservation

The protocol does not create, infer, or impersonate Human Steward approval. Existing explicit Human Steward disposition requirements remain outside automatic agent inference.

### I12. Explicit obligation lifecycle

An obligation MUST be opened before it is resolved and MUST NOT be resolved more than once. `DISCHARGED` and `REFUTED` resolutions require at least one supporting prior reasoning object beyond the obligation itself. Resolution changes only the materialized working-obligation state and has no direct canonical claim-ledger effect.

## 8. Conflict-driven learning semantics

The Programme should preserve failure as reusable information without allowing heuristic failure to become unsound global pruning.

Given assumptions or working objects

```text
A = {a1, a2, ..., an}
```

an agent may produce a conflict explanation

```text
{a2, a7, a9} -> conflict C17 [assurance = HEURISTIC]
```

The coordinator may learn:

```text
avoid(all(a2, a7, a9)) [SOFT_AVOID]
```

If independent replay upgrades the conflict to `REPLAYABLE`, a local search scope may use:

```text
not(all(a2, a7, a9)) [LOCAL_PRUNE]
```

Only a `CHECKED` conflict from MATHCERT or a designated checker may justify:

```text
not(all(a2, a7, a9)) [HARD_PRUNE]
```

under the same declared semantics.

None of these events automatically creates the public theorem `¬(a2 ∧ a7 ∧ a9)`. The theorem route remains separate. This is where the Z3/CDCL analogy is deliberately weakened to account for open-world, interpretation-sensitive research mathematics.

## 9. Canonical identity and congruence layer

A recurring Programme problem is that one mathematical object has several names:

```text
source theorem label
repository claim identifier
formal theorem identifier
certificate artifact identifier
knowledge-graph node
```

MATH-CORE-01 treats these as first-class equivalence candidates rather than independent facts.

The materialized blackboard SHOULD maintain scoped equivalence classes. Consumers MUST retain representation provenance even when identifiers are grouped. A formal theorem and a source theorem can therefore be recognized as representations of the same intended object while preserving distinct evidence and certification histories.

## 10. Reducer contract

The reducer is the semantic choke point. A minimal implementation follows this order:

```text
receive proposal
  -> validate JSON schema
  -> validate exact checkpoint
  -> authenticate producer identity externally
  -> check producer capability
  -> resolve dependencies
  -> enforce obligation lifecycle
  -> enforce conflict-assurance / pruning monotonicity
  -> enforce event-specific semantic invariants
  -> append accepted event
  -> materialize deterministic views
  -> emit acceptance/rejection receipt
```

The reducer MUST NOT execute arbitrary proof code merely because an agent includes it in a response. Proof or certificate replay occurs through the designated checker route.

## 11. Materialized views

Implementations MAY materialize indexes for efficiency. At minimum, a useful blackboard view contains:

```text
claims
open obligations
resolved obligations + outcomes
conflicts + assurance
active search constraints + enforcement
scoped equivalence classes
witnesses
certificates
supersession links
```

Materialized views are caches. The ordered accepted event log is the replay authority for MATH-CORE-01 state.

## 12. Transport independence

Protocol semantics are independent of transport.

The initial implementation may use:

```text
GitHub repositories + JSON + CI + content-addressed artifacts
```

A future implementation may use:

```text
AETHER typed tuples + subscriptions + distributed workers
```

A transport change MUST NOT alter the meaning of protocol events or weaken the evidence boundary. AETHER is therefore an implementation accelerator, not a semantic dependency.

## 13. Conformance

Protocol version 0.1.0 defines three conformance surfaces.

### C1. Wire conformance

Blackboard traces, capability registries, and theory-agent exchanges validate against their JSON Schemas.

### C2. Semantic conformance

The reducer enforces invariants I1-I12, including producer capabilities, dependency closure, explicit obligation lifecycle, assurance-bounded conflict learning, certificate independence, scoped equivalence, and deterministic replay.

### C3. Governance conformance

No MATH-CORE-01 event bypasses canonical claim-ledger registration, certification policy, protected review, or Human Steward authority requirements.

`ci/validate_programme_math_core.py` checks C1 and the mechanically decidable subset of C2 for the reference artifacts. `ci/test_programme_math_core.py` supplies negative regression cases.

## 14. Non-goals

MATH-CORE-01 is not:

- a new proof kernel;
- a replacement for Lean or other theorem provers;
- a replacement for the canonical claim ledger;
- a generic conversational message bus;
- a guarantee of search completeness;
- a claim that mathematical discovery is reducible to SAT/SMT;
- an authorization mechanism for protected merge or public mathematical promotion;
- a runtime dependency on AETHER.

## 15. Initial deployment sequence

The candidate deployment sequence is deliberately narrow:

1. validate the protocol schemas and controlled capability registry;
2. replay the reference trace deterministically in CI, including explicit open-to-resolved obligation transitions;
3. require theory-agent exchanges to be exact-checkpoint-bound and proposal-only;
4. enforce assurance-bounded learning so heuristic conflicts cannot hard-prune research branches;
5. pilot one existing MATHSOLVE -> MATHCERT handoff through the protocol without changing its certification semantics;
6. measure whether replayable conflicts and learned search constraints prevent repeated dead branches without suppressing viable alternatives;
7. only then generalize the protocol across families or transport it into AETHER.

The success criterion for MATH-CORE-01 is not more agent activity. It is a smaller gap between what the Programme has actually established, what it is currently trying, why branches failed, and what can be independently replayed.