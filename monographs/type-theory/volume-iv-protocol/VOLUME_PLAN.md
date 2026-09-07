# Volume IV — PROTOCOL: Computation as Communication

## Gate 0 preflight contract

Work set: `TYPE-THEORY-VOL-IV-001`

Tracking issue: `#877`

Protected starting head: `bf82c2b98870ee487430948309396b952d6506cb`

Series thesis status: **research hypothesis, not established theorem**.

## Governing question

**What changes when the primary computational object is interaction rather than closed function evaluation?**

Volume IV moves from a term that consumes inputs and reduces toward an answer to a process that must coordinate with another process over time. Its central claim is deliberately narrower than “communication is computation.” The volume will identify exact session-typing and process-calculus results where they hold, distinguish them from broader distributed-systems guarantees, and expose the points where typed interaction alone is insufficient.

The intended answer is structural: once computation is interactive, types must constrain not only *what values exist* but also *which communication action may occur next, on which endpoint, with which continuation, and under which resource discipline*. This strengthens the series thesis if interaction can be represented by compositional judgments without hiding liveness, failures, scheduling, or environment assumptions. It weakens the thesis wherever those obligations require semantic structure not captured by the local type discipline.

## Institutional inheritance

Volume IV inherits formal and pedagogical content from Volumes I–III at the exact institutional state protected at commencement:

- Volume I — JUDGMENT RC1.1: `RC_COMPOSITION_COMPLETE`, `RC_DURABLY_ADMITTED`, independent mathematical review pending, publication authority not granted.
- Volume II — COMPREHENSION RC1: `RC_COMPOSITION_COMPLETE`, `RC_DURABLY_ADMITTED`, independent mathematical review pending, publication authority not granted.
- Volume III — PROOF / PROGRAM RC1: `RC_COMPOSITION_COMPLETE`, `RC_DURABLY_ADMITTED`, independent mathematical review pending, publication authority not granted.

No Volume IV statement may silently upgrade a prior volume to independently reviewed, mathematically certified, or authoritatively published status.

### Machinery inherited from Volumes I–II

Reused without changing meaning:

- value contexts `Γ`;
- typing judgments for payload values `Γ ⊢ v : A`;
- nondependent payload types sufficient for the initial protocol core;
- substitution for values;
- dependent families and `Π`/`Σ` only when later examples genuinely need indexed protocol states.

Reintroduced for self-containment:

- the distinction between a value expression and a typing derivation;
- ordinary substitution and preservation patterns;
- the idea that a typing environment records obligations available at a program point.

### Machinery inherited from Volume III

Reused as motivation, not silently identified:

- constructive proofs/programs as closed typed constructions;
- the Chapter-14 boundary between normalization of a closed term and correctness of an open protocol;
- explicit separation of type safety from liveness properties.

Reintroduced for self-containment:

- the closed-term baseline against which interaction is compared;
- the notion that a local typing result does not automatically imply global temporal correctness.

## Exact calculi in scope

### `PROTO-0` — synchronous binary session core

`PROTO-0` is the primary formal calculus for the first half of the volume. It is a deliberately small synchronous binary session calculus with linear channel endpoints.

Payload types are initially drawn from a small value layer:

`A ::= Unit | Bool | Nat | A × B | A + B`

Session types are:

`S ::= end! | end? | !A.S | ?A.S | ⊕{l_i:S_i}_{i∈I} | &{l_i:S_i}_{i∈I}`

where:

- `!A.S` means send a value of type `A`, then continue as `S`;
- `?A.S` means receive a value of type `A`, then continue as `S`;
- `⊕{l_i:S_i}` means internally select one label;
- `&{l_i:S_i}` means externally offer branches;
- `end!` means actively close an endpoint;
- `end?` means wait for peer closure.

Duality is a partial syntactic operation over well-formed session types:

- `dual(!A.S) = ?A.dual(S)`;
- `dual(?A.S) = !A.dual(S)`;
- `dual(⊕{l_i:S_i}) = &{l_i:dual(S_i)}`;
- `dual(&{l_i:S_i}) = ⊕{l_i:dual(S_i)}`;
- `dual(end!) = end?` and conversely.

Process syntax is:

`P ::= 0 | x!⟨v⟩.P | x?(y).P | x⊕l.P | x&{l_i:P_i}_{i∈I} | close x.P | wait x.P | P | Q | (ν x y)P`

The restriction `(ν x y)P` creates paired endpoints `x` and `y` governed by dual session types. Parallel composition is not assumed to be physically parallel; it is a process-calculus constructor.

Typing judgments have two environments:

`Γ ; Δ ⊢ P`

where `Γ` is an unrestricted value-variable context and `Δ` is a linear channel environment. Linear splitting in the parallel rule prevents the same endpoint obligation from being consumed independently by two subprocesses.

`PROTO-0` is intentionally finite and nonrecursive. Its core theorems concern communication safety, session fidelity, preservation, and a narrowly scoped single-session progress theorem.

### `PROTO-N1` — multi-session network extension

`PROTO-N1` permits a process to hold and interleave multiple independent binary sessions. It retains local binary session typing but is used principally to expose the difference between communication safety and global deadlock freedom.

A central negative example will be a closed, locally well-typed network whose peers wait on different sessions in a cyclic order and therefore cannot reduce. This is not treated as a failure of preservation or local fidelity; it is evidence that stronger global structure is needed for deadlock-freedom claims.

### `PROTO-R1` — guarded recursive session extension

`PROTO-R1` adds guarded recursive session types and process recursion:

`S ::= ... | μt.S | t`

with contractiveness/guardedness requirements stated explicitly. Recursive sessions describe potentially unbounded interaction. They are not identified with terminating computations. The volume will prove only bounded unfolding properties and preservation for the concrete guarded teaching fragment; general productivity/fairness claims are postponed or cited when used.

### `PROTO-A1` — asynchronous queue semantics

`PROTO-A1` replaces synchronous handshakes with explicit FIFO queues between paired endpoints. Send can enqueue without a simultaneously ready receiver; receive dequeues when the expected message is available.

The asynchronous layer is separate because synchronous fidelity/progress statements do not transfer verbatim. Queue well-formedness, message ordering, orphan-message possibilities, and bounded-vs-unbounded queue assumptions are made explicit.

### `PROTO-M1` — multiparty/global-type preview

A bounded multiparty comparison layer introduces global choreography descriptions and projection to local roles for finite acyclic examples. The volume demonstrates projection and compatibility on selected protocols and cites the broader multiparty-session literature. It does not claim a general projection theorem for arbitrary recursive global types unless the exact fragment is separately defined and proved.

### `PROTO-S1` — subtyping/refinement comparison layer

A later chapter introduces a deliberately bounded notion of session subtyping/refinement to show when one endpoint behavior can safely replace another. Variance rules, branch width conditions, and semantic assumptions are scoped to the selected synchronous binary fragment. General asynchronous subtyping is explicitly outside the proved core because it introduces substantially harder questions.

### `PROTO-MON1` — runtime monitoring layer

A finite-state runtime monitor is generated from selected finite session types. The monitor can detect local trace violations against its observation model. Monitoring is not identified with static typing, global correctness, or recovery from faults.

## Operational and equational semantics

### `PROTO-0` reduction

The primary reduction relation is a process relation `P → P'`, closed under restriction, parallel evaluation contexts, and structural congruence where explicitly stated.

Principal communications include:

- send/receive synchronization across paired restricted endpoints;
- selection/branch synchronization on the same label;
- close/wait synchronization.

The value sent by a sender is substituted into the receiver continuation using ordinary capture-avoiding substitution.

A deterministic laboratory scheduler is used only to generate reproducible traces. The mathematical reduction relation remains nondeterministic where multiple independent communications are enabled.

### Structural congruence

A separate relation `P ≡p Q` is used for benign rearrangements such as associativity/commutativity of parallel composition, identity of `0`, and scope extrusion under stated freshness conditions.

`≡p` is not the same object as definitional equality `≡` for value terms inherited from earlier volumes. The notation registry will record the process-specific overload explicitly.

### Session environment evolution

The process typing proof tracks protocol state through a channel environment transition relation `Δ ⇒ Δ'` synchronized with communication. Session fidelity will state that process reduction preserves typing under the corresponding evolution of protocol obligations.

### Asynchronous semantics

`PROTO-A1` states configurations explicitly as processes plus queues. Its reduction relation therefore changes the state space. Synchronous process equivalence and progress claims are not reused without a separate theorem.

## Intended metatheory

| ID | Result | Disposition | Exact scope | Evidence route |
|---|---|---|---|---|
| T4.1 | Session-type well-formedness and involutive duality | prove | finite `PROTO-0` session types | structural induction on `S` |
| T4.2 | Linear environment splitting is disjoint and reconstructible | prove | `PROTO-0` typing derivations | induction on split construction |
| T4.3 | Value substitution | inherit/restate and prove for payload layer | `PROTO-0` payload expressions | structural induction |
| T4.4 | Communication redex compatibility | prove | principal `PROTO-0` redexes | inversion on dual endpoint typings |
| T4.5 | Session fidelity / subject reduction | prove | `PROTO-0` | induction on reduction; environment evolution explicit |
| T4.6 | Communication safety | derive from T4.5 + inversion | closed well-typed `PROTO-0` configurations | canonical redex analysis |
| T4.7 | Single-session progress | prove | closed finite `PROTO-0` networks with one restricted session and no free endpoints | canonical forms + duality |
| T4.8 | Multi-session global progress from local typing | **explicit non-result** | unrestricted `PROTO-N1` | well-typed cyclic-wait counterexample |
| T4.9 | Local typing does not imply deadlock freedom | prove by counterexample | `PROTO-N1` | executable stuck-network witness + typing derivations |
| T4.10 | Guarded unfolding preserves session well-formedness | prove | `PROTO-R1` | structural/guardedness argument |
| T4.11 | Preservation under one guarded recursive communication step | prove | bounded `PROTO-R1` teaching fragment | reduction cases |
| T4.12 | General productivity / lock freedom for recursive sessions | postpone / do not claim | `PROTO-R1` | outside volume core |
| T4.13 | Asynchronous queue typing invariant | prove | finite `PROTO-A1` with FIFO queues | induction on enqueue/dequeue steps |
| T4.14 | Asynchronous fidelity | prove for bounded queue-aware fragment | `PROTO-A1` | configuration preservation |
| T4.15 | Synchronous/asynchronous trace equivalence | demonstrate selected examples only | chosen finite protocols | trace normalization comparison; no universal theorem |
| T4.16 | Finite global-to-local projection preserves selected protocol traces | prove per exemplar | acyclic `PROTO-M1` examples | executable projection + trace enumeration |
| T4.17 | General multiparty projection correctness | cite / explicitly not re-prove | external MPST theory | literature dependency only |
| T4.18 | Bounded synchronous session subtyping safety | prove for selected `PROTO-S1` rules | binary finite sessions | coinductive/structural relation specialized to finite syntax |
| T4.19 | General asynchronous subtyping decidability/completeness | explicit non-result | asynchronous sessions | outside scope |
| T4.20 | Monitor soundness for observed finite traces | prove | `PROTO-MON1` | automaton construction + induction on trace |
| T4.21 | Monitor completeness for all distributed failures | explicit non-result | open systems | unobservable/environmental failures counterexamples |
| T4.22 | Process structural congruence preserves typing | prove | selected `PROTO-0` congruence laws | rule cases with freshness conditions |
| T4.23 | Session fidelity implies fault tolerance | explicit non-result | distributed deployments | claim-boundary analysis |
| T4.24 | Typed protocol conformance implies application-level correctness | explicit non-result | arbitrary applications | counterexamples with semantically wrong but protocol-conforming payloads |

## Metatheorems explicitly not established by this volume

Unless a later exact revision proves and audits them, Volume IV does **not** establish:

- deadlock freedom for arbitrary well-typed multi-session networks;
- lock freedom, starvation freedom, fairness, real-time guarantees, or scheduler independence;
- fault tolerance under crashes, partitions, Byzantine behavior, duplication, loss, or reordering beyond the chosen semantics;
- general liveness for recursive sessions;
- correctness of arbitrary multiparty projection;
- decidability or completeness of general asynchronous session subtyping;
- semantic equivalence between synchronous and asynchronous semantics;
- correctness of real network transports such as TCP, QUIC, MPI, actor runtimes, RPC systems, or message brokers;
- security properties such as confidentiality, integrity, authentication, or noninterference merely from session fidelity;
- application-level functional correctness of communicated payloads merely from protocol conformance;
- that linear type use implies unique physical ownership in a distributed implementation;
- that runtime monitoring can establish properties about unobserved events or recover from faults;
- a universal identification of propositions with protocols or of session duality with logical negation.

## Central distinctions not to collapse

1. **Closed evaluation vs open interaction.** A value-normalizing term has a terminal answer; a correct protocol may be intentionally nonterminating.
2. **Value context vs channel environment.** `Γ` records reusable value assumptions; `Δ` records linear communication obligations in the core calculus.
3. **Duality vs negation.** Session duality swaps complementary communication actions. It is not by itself classical or intuitionistic logical negation.
4. **Linearity vs physical uniqueness.** A linear typing rule controls use in the formal derivation; deployment identity and aliasing require separate implementation assumptions.
5. **Fidelity vs progress.** Fidelity says reductions respect the protocol type. It does not guarantee that some reduction is always available.
6. **Progress vs deadlock freedom.** A narrowly scoped progress theorem can depend on topology or one-session restrictions. General deadlock freedom is stronger.
7. **Deadlock freedom vs lock freedom.** A system can always have some enabled action while starving a particular action forever.
8. **Lock freedom vs fairness.** Fairness is a scheduler/environment assumption, not a synonym for a typing property.
9. **Synchronous vs asynchronous semantics.** A handshake and an enqueue/dequeue system have different state spaces and observable traces.
10. **Binary local typing vs multiparty global consistency.** Pairwise-compatible endpoints do not automatically yield a globally realizable choreography.
11. **Recursion vs termination.** Recursive session types intentionally express unbounded conversations; guardedness is not a termination theorem.
12. **Static typing vs monitoring.** A static derivation constrains source terms; a monitor observes runtime events according to an observation boundary.
13. **Protocol conformance vs application correctness.** A process can send the wrong *meaning* in a value of the right type at the right time.
14. **Protocol correctness vs distributed-system correctness.** Crashes, partitions, timing, security, durability, and external resources are separate obligations.
15. **Process equivalence vs syntax.** Behavioral equivalence quotients observable differences according to a semantic criterion; it is not textual identity.

## Chapter and laboratory map

Target: 14 teaching chapters, one executable laboratory per chapter.

| Ch. | Working title | Formal/pedagogical burden | Laboratory |
|---:|---|---|---|
| 1 | A Program With Someone on the Other End | conversations as typed state machines; first send/receive protocol | `lab01_protocol_trace.py` — validate and execute finite binary protocol traces |
| 2 | Two Ends of One Obligation | session duality, linear endpoint environments, synchronous reduction | `lab02_duality_checker.py` — parse session types, compute duals, reject incompatible peers |
| 3 | Say It, Then Continue | send/receive typing and session fidelity | `lab03_fidelity.py` — typed communication-step checker with environment evolution |
| 4 | Choice Has Two Sides | selection/branching and labeled protocol states | `lab04_branching.py` — branch compatibility and trace exploration |
| 5 | Use the Channel Exactly as Promised | linear resource discipline and environment splitting | `lab05_linearity.py` — detect duplicated/dropped endpoint obligations |
| 6 | Safe Can Still Be Stuck | multi-session cyclic wait; progress vs deadlock freedom | `lab06_deadlock.py` — enumerate wait-for graph and well-typed deadlock witness |
| 7 | Conversations That Do Not End | guarded recursive session types | `lab07_recursion.py` — bounded unfoldings and guardedness checks |
| 8 | Messages in Flight | asynchronous FIFO semantics and queue invariants | `lab08_async.py` — explicit queue simulator and bounded state-space explorer |
| 9 | More Than Two Voices | global descriptions and local projections | `lab09_multiparty.py` — finite choreography projection and trace comparison |
| 10 | One Protocol Standing In for Another | bounded session subtyping/refinement | `lab10_subtyping.py` — finite subtyping relation explorer |
| 11 | When the Network Is Not the Calculus | loss, crashes, partitions, timing and the failure model boundary | `lab11_failures.py` — fault-injection traces showing which claims leave the typed model |
| 12 | Watching the Conversation | finite runtime monitors from session types | `lab12_monitor.py` — generate monitor automata and classify traces |
| 13 | Processes as Proofs, Carefully | linear logic/process correspondences and their limits | `lab13_logic_process.py` — bounded correspondence table and proof/process step alignment |
| 14 | The World Pushes Back | protocol conformance versus environmental effects | `lab14_effect_threshold.py` — compare pure protocol state with explicit external effect events |

## Initial plate register

The full target is 42 canonical plates. The first six form the Gate-1 tranche; later plates are already assigned one burden each so visual closure cannot be achieved by decorative padding.

1. **Closed function, open conversation.** Contrast `input → term → value` with an interaction trace whose next state depends on another participant. Limit: the picture does not claim all computation is either purely closed or purely interactive.
2. **A protocol is a typed state machine.** Show `!Nat.?Bool.end!` as a sequence of obligations rather than a bag of message types. Limit: temporal ordering here is finite and synchronous.
3. **Two ends, complementary actions.** Align a session type with its dual action-by-action. Limit: duality is complementary protocol behavior, not logical negation in general.
4. **A handshake consumes obligations.** Show send/receive reduction and simultaneous `Δ ⇒ Δ'` evolution. Limit: one reduction picture does not establish global liveness.
5. **Linear splitting of channel authority.** Parallel subprocesses receive disjoint endpoint obligations. Limit: formal linearity does not prove unique physical ownership after compilation/deployment.
6. **Safe but stuck.** A well-typed cyclic wait across two sessions has no enabled communication. Limit: the example refutes an unrestricted progress inference, not session fidelity.
7. **Send then continue.** A process and its session type advance in lockstep after a payload transfer. Limit: payload semantic correctness is separate.
8. **Branching is asymmetric choice.** Internal selection chooses; external branching offers. Limit: label agreement alone is not global protocol correctness.
9. **The environment is a protocol frontier.** `Δ` records only the communication obligations currently available. Limit: it is not a runtime socket table.
10. **Dropping an endpoint leaves an obligation unpaid.** Linear typing rejection as an accounting failure. Limit: the metaphor is formal resource accounting only.
11. **Duplicating an endpoint forks one promise into two claims.** Show why a linear endpoint cannot be independently consumed twice. Limit: shared-channel systems require a different calculus.
12. **Local safety versus global waiting.** Separate protocol mismatch edges from wait-for-cycle edges. Limit: the wait-for graph is one liveness abstraction.
13. **Guarded recursion folds a conversation.** Visualize `μt.!Nat.?Bool.t` as a finite syntax denoting unbounded unfolding. Limit: the loop does not imply productive scheduling.
14. **Unfolding is not running forever correctly.** Separate guarded type formation from runtime fairness/productivity. Limit: neither property is inferred from the other.
15. **Handshake versus queue.** Synchronous rendezvous beside asynchronous enqueue/dequeue. Limit: trace equivalence is not claimed globally.
16. **Messages become state.** Queue contents are part of asynchronous configuration. Limit: FIFO is an explicit model assumption.
17. **An orphan message.** A queued message remains after a peer terminates in a deliberately ill-disciplined variant. Limit: the example is diagnostic, not a theorem about every async calculus.
18. **Queue growth changes the proof burden.** Finite versus unbounded queues. Limit: resource exhaustion is outside pure type fidelity.
19. **A choreography seen globally.** Three roles and ordered interactions in a finite global description. Limit: a global script is not a deployed orchestrator.
20. **Projection gives each role a local view.** One choreography projected to three local session types. Limit: projection correctness requires projectability conditions.
21. **Pairwise sensible can still be globally impossible.** Exhibit incompatible local ordering among three peers. Limit: finite witness only.
22. **Branch knowledge must reach the right roles.** Multiparty choice propagation. Limit: no universal MPST theorem is claimed.
23. **Subtyping as safe replacement.** One finite protocol is accepted where another is expected under stated variance rules. Limit: asynchronous subtyping is excluded.
24. **Offer more, select less.** Branch-width intuition for external/internal choice. Limit: exact variance follows the defined relation, not the slogan.
25. **Behavioral refinement is not syntactic inclusion.** Trace-level intuition beside the formal relation. Limit: semantic and syntactic subtyping need not coincide generally.
26. **Network faults live outside `PROTO-0`.** Crash/loss/partition icons outside the core reduction box. Limit: placement outside the box is a scope statement, not evidence that types cannot model faults.
27. **A perfect protocol over a broken transport.** Type-correct peers separated by a lossy channel. Limit: transport assumptions are deliberately changed.
28. **Timing adds another dimension.** Protocol order versus deadlines/timeouts. Limit: timed session types are not developed as a full calculus here.
29. **Security is another obligation plane.** Authentication/confidentiality separated from session order. Limit: no security theorem is inferred from layout.
30. **Monitor as automaton.** Compile a finite session type to an observer state machine. Limit: the monitor sees only instrumented events.
31. **Static proof and runtime observation.** Compare pre-execution typing with trace-time monitoring. Limit: neither subsumes the other in general.
32. **An unobservable violation.** Application meaning can be wrong while the observed protocol trace is accepted. Limit: finite witness to a boundary.
33. **Session fidelity triangle.** Process step, environment step, and typing derivation commute for the core theorem. Limit: diagram states T4.5 only.
34. **Progress hypothesis map.** Show which extra assumptions are needed when moving from one-session progress toward stronger liveness. Limit: implication arrows appear only where proved/cited.
35. **Deadlock, lock freedom, starvation, fairness.** Four separate temporal notions on one comparison grid. Limit: examples illustrate distinctions rather than prove equivalences.
36. **One syntax, several semantics.** Same protocol under synchronous, asynchronous, and monitored readings. Limit: semantics are alternatives, not automatically equivalent.
37. **Processes and proofs: a disciplined correspondence.** Selected linear-logic rule beside communication construct. Limit: correspondence is calculus-specific.
38. **Cut as channel composition, with conditions.** Proof cut and restricted process connection shown structurally. Limit: no unrestricted identification of proof normalization with concurrent execution.
39. **Protocol state is not world state.** Distinguish channel obligations from database/filesystem/device state. Limit: sets up Volume V rather than proving an effect calculus result.
40. **A protocol-conforming semantic bug.** Correct message type/order, wrong business meaning. Limit: application invariants need additional specification.
41. **From conversation to effect.** External event changes state not owned by either endpoint. Limit: the event model belongs to Volume V.
42. **Series atlas IV.** Locate PROTOCOL after proof/program and before effects in the ten-volume argument. Limit: atlas is organizational, not evidence for the grand-unification thesis.

## Exercise ecology and solutions plan

Each teaching chapter targets 12 exercises:

- 3 Checkpoint;
- 3 Core;
- 2 Synthesis;
- 2 Proof Workshop;
- 1 Design Clinic;
- 1 Challenge.

Expected full volume: 168 exercises. Every exercise receives a worked solution or an explicit rubric in `solutions_companion.tex`. Research questions and literature-dependent extensions are labeled as open/design work rather than deterministic exercises.

Gate 1 requires complete keyed solutions/rubrics for Chapters 1–2 before scaling.

The exercise design will repeatedly ask learners to distinguish:

- protocol mismatch from deadlock;
- local from global properties;
- model assumptions from implementation facts;
- static typing from temporal/failure guarantees.

## Bibliography and historical-attribution plan

Primary/foundational source families to verify and cite:

- Milner on CCS and the π-calculus/process-calculus tradition;
- Hoare on CSP and communicating sequential processes;
- Girard on linear logic;
- Honda and collaborators on session types and structured communication;
- Honda, Yoshida, Carbone and related work on multiparty session types;
- Gay, Hole and later session-subtyping literature;
- asynchronous session-type and communicating-automata literature where exact claims are used;
- runtime monitoring/session-monitor literature for monitor claims;
- propositions-as-sessions / linear-logic process correspondences, including Curry–Howard-style process interpretations where scoped.

Modern expository reference families:

- typed process calculi and concurrency texts;
- programming-language type-system references with session typing;
- surveys on binary and multiparty session types;
- distributed-systems references used specifically to delimit what session typing does not establish.

Historical scholarship rules:

- distinguish independent process-calculus traditions rather than narrating session types as a single linear progression;
- distinguish original session-type formulations from later linear-logic correspondences;
- distinguish synchronous and asynchronous results by exact calculus;
- avoid priority or novelty claims without a dedicated literature audit.

## Bibliography claims requiring explicit verification

Before RC closure, verify at minimum:

1. dates and exact publication identities for foundational CSP/CCS/π-calculus sources used in historical exposition;
2. the exact bibliographic identity and calculus of early session-type papers;
3. which source first supports each quoted fidelity/progress/subtyping statement;
4. exact hypotheses of any imported deadlock-freedom/global-progress theorem;
5. the source and scope of any propositions-as-sessions correspondence used in Chapter 13;
6. the exact fragment and projectability hypotheses for multiparty projection claims;
7. the monitoring observation model for any cited monitor soundness/completeness result.

## Pressure points against the grand-unification thesis

Volume IV must actively test the series thesis against the following obstacles:

1. **Open systems have no intrinsic final value.** Correctness may concern traces, responsiveness, or perpetual service rather than normalization.
2. **Local types may not determine global liveness.** Session fidelity can hold while a network deadlocks.
3. **Scheduling assumptions matter.** Fairness and starvation are not ordinarily derivable from a local typing judgment.
4. **Failure models matter.** Crashes, partitions, loss, duplication, reordering, clocks, and retries change the semantics materially.
5. **Global structure can be irreducible.** Multiparty realizability/projectability can require information not visible in pairwise local types.
6. **Communication order is not application meaning.** A protocol-correct trace can carry semantically invalid payloads.
7. **Physical resources exceed formal linearity.** Runtime aliasing, buffering, replication, brokers, and transport endpoints complicate the linear-resource story.
8. **Security is orthogonal.** A perfectly typed protocol can be unauthenticated or leak secrets.
9. **Asynchrony changes equivalence.** Synchronous and queued semantics can differ observably and in decidability properties.
10. **The environment becomes part of computation.** Once external state and events matter, protocol state alone is insufficient; this forces Volume V.

If these pressure points require weakening the claim that type theory alone forms a complete grammar of computation, the manuscript will state that weakening explicitly rather than treating it as an implementation detail.

## Next-volume threshold

Volume IV ends when protocol state is no longer enough to describe the computation.

A session type can say that a process must next send a request and then receive a reply. It does not, by itself, say that the request mutates a database, consumes a capability, throws an exception, samples randomness, performs I/O, modifies external state, or can fail because the world refuses the action.

That is the forced transition to Volume V — **EFFECTS: Computation Meets the World**:

> Once communication is typed, how do we type the events by which computation changes or observes a world not reducible to the protocol itself?

## Smallest safe executable tranche

Gate 1 is deliberately narrower than the final volume.

It contains:

1. **Chapter 1 — A Program With Someone on the Other End**
   - closed-term baseline versus interaction trace;
   - finite session-type syntax for send/receive/end;
   - first typed two-party example;
   - protocol as ordered obligation;
   - failure example: same payload types in the wrong order.
2. **Chapter 2 — Two Ends of One Obligation**
   - duality;
   - linear channel environment `Δ`;
   - paired restriction `(ν x y)`;
   - synchronous send/receive and close/wait reduction;
   - first preservation/fidelity statement for principal redexes;
   - failure example: nondual peers.
3. `lab01_protocol_trace.py`
   - dependency-free finite protocol parser/trace validator;
   - deterministic positive and hostile fixtures.
4. `lab02_duality_checker.py`
   - dependency-free parser, duality computation, involution checks, peer-compatibility rejection fixtures.
5. Plates 1–6 as registered above.
6. Twenty-four exercises: 12 per chapter in the full six-mode ecology, with complete solutions/rubrics.
7. Notation registration for session syntax, `dual(S)`, `Γ ; Δ ⊢ P`, process reduction, process structural congruence, and environment evolution.

Gate 1 passes only after the two chapters compile, both laboratories pass, the six plates are inspected at manuscript scale, the 24 exercises have keyed solutions/rubrics, and the new notation is reconciled with the series registry.
