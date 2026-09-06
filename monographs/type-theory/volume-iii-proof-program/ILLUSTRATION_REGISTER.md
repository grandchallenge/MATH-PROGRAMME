# Volume III Illustration Register — PROOF / PROGRAM

Default target: 42 canonical plates. Each plate must carry one pedagogical burden, remain legible in grayscale, and state an analogy/scope limit where needed. Computed plates retain executable provenance under `labs/` or `evidence/`.

## Gate 1 tranche

### Plate 1 — [PLANNED] One Constructive Object, Two Presentations
**Pedagogical burden:** Align an implication derivation with its assigned lambda term rule-by-rule.
**Composition:** Natural-deduction tree at left; typed term tree at right; shared assumption/binder markers.
**Scope limit:** Exact for the selected `CH-0` term assignment; not every proof formalism has this syntax.

### Plate 2 — [PLANNED] Introduction Then Elimination Is a Detour
**Pedagogical burden:** Show that discharging an assumption and immediately applying the result creates the same principal computational redex as beta reduction.
**Composition:** Proof detour above; beta-redex term below; reduction arrows terminate in aligned normal forms.
**Scope limit:** Principal implication case only; not a proof of global normalization.

### Plate 3 — [PLANNED] The Implication Machine
**Pedagogical burden:** Map assumption discharge to lexical binding and modus ponens to application.
**Composition:** Three-stage flow: open assumption → abstraction boundary → application with supplied evidence.
**Scope limit:** Runtime behavior does not replace semantic truth conditions.

### Plate 4 — [PLANNED] A Normalization Trace
**Pedagogical burden:** Make type preservation visible across a multi-redex reduction sequence.
**Composition:** Typed term states arranged vertically with the invariant type on a side rail.
**Scope limit:** One deterministic trace is evidence for the implementation, not a proof of strong normalization.
**Provenance:** `lab02_normalizer.py` trace fixture.

### Plate 5 — [PLANNED] Conjunction / Product Preview
**Pedagogical burden:** Paired evidence supports two independent projections.
**Composition:** Pair node feeding first and second projections; corresponding conjunction-introduction/elimination rules.
**Scope limit:** Structural alignment in `CH-0`; not a universal semantic identity between products and truth-valued conjunction.

### Plate 6 — [PLANNED] Disjunction Carries a Choice
**Pedagogical burden:** Constructive disjunction records which branch and the evidence for it.
**Composition:** Sum injection splits into left/right cases; case analysis rejoins at common result type.
**Scope limit:** This is not a proof-irrelevant Boolean truth value.

## Full-volume plate programme

### Plate 7 — [PLANNED] Product Detours
**Burden:** Pair-then-project redexes as conjunction detour elimination.
**Limit:** Principal product reductions only.

### Plate 8 — [PLANNED] Case Analysis Is Controlled Branching
**Burden:** Show disjunction elimination as typed branch convergence.
**Limit:** Both branches must produce the same result type in `CH-0`.

### Plate 9 — [PLANNED] Sum Detours
**Burden:** Injection followed by case analysis contracts to the selected branch.
**Limit:** Does not assert confluence for arbitrary extensions.

### Plate 10 — [PLANNED] Truth Has One Canonical Witness
**Burden:** Visualize `1`/truth as a type with one canonical constructor.
**Limit:** Equality of arbitrary proof objects is not inferred.

### Plate 11 — [PLANNED] Empty Has No Constructor
**Burden:** Explain absurd elimination without depicting a fabricated inhabitant of `0`.
**Limit:** “From false, anything follows” is an elimination rule conditioned on an impossible premise.

### Plate 12 — [PLANNED] Canonical Forms by Shape
**Burden:** Associate arrow/product/sum/unit types with the possible shapes of closed values.
**Limit:** Scoped to `CH-0` values.

### Plate 13 — [PLANNED] Universal Construction as a Dependent Function
**Burden:** Read `Π(x:A).B(x)` as evidence-producing construction for each `x`.
**Limit:** Depends on inherited `CHD-1` rules; not every logical universal is represented identically in every semantics.

### Plate 14 — [PLANNED] Existential Evidence Is a Witness Plus Proof
**Burden:** Read `Σ(x:A).B(x)` as witness/evidence pairing.
**Limit:** The witness is computationally present unless an erasure policy removes it.

### Plate 15 — [PLANNED] Quantifier Substitution
**Burden:** Show instantiation as dependent substitution in propositions/types.
**Limit:** Capture avoidance and dependency conditions remain formal obligations.

### Plate 16 — [PLANNED] Natural Deduction and Sequent Views
**Burden:** Show two proof presentations connected by translation rather than identity.
**Limit:** Administrative structure differs even when conclusions coincide.

### Plate 17 — [PLANNED] Cut as Explicit Composition
**Burden:** Expose the intermediate proposition introduced by a cut.
**Limit:** This is `LJ-0`; arbitrary structural/logical systems need separate theorems.

### Plate 18 — [PLANNED] Cut Reduction Trace
**Burden:** Show one bounded cut shrinking through proof structure.
**Limit:** Computed trace does not prove the general cut-elimination theorem.
**Provenance:** `lab07_cut_reducer.py`.

### Plate 19 — [PLANNED] Three Notions That Must Not Collapse
**Burden:** Separate beta reduction, natural-deduction normalization and sequent cut elimination.
**Limit:** Arrows between them denote translations/correspondences, not synonymy.

### Plate 20 — [PLANNED] A Kripke World Where Excluded Middle Fails
**Burden:** Give a finite intuitionistic countermodel for a selected classical schema.
**Limit:** A countermodel refutes derivability under the model's sound semantics; it does not compare all constructive logics.
**Provenance:** `lab08_kripke.py`.

### Plate 21 — [PLANNED] Constructive Information vs Classical Commitment
**Burden:** Contrast a witness-producing proof with a classical principle that selects no constructive branch.
**Limit:** “Nonconstructive” is calculus-relative, not pejorative.

### Plate 22 — [PLANNED] Double Negation as a Translation Boundary
**Burden:** Visualize a classical proposition entering a constructive target through double-negation translation.
**Limit:** Translation preserves selected logical validity; it is not literal identity of proofs.

### Plate 23 — [PLANNED] Continuation-Passing Control Flow
**Burden:** Show explicit continuation arguments turning control context into data/terms.
**Limit:** Operational behavior belongs to `CHC-1`, not the pure `CH-0` core.

### Plate 24 — [PLANNED] Classical Proof as Control
**Burden:** Connect a typed classical principle with a continuation/control interpretation.
**Limit:** One interpretation among several; not a universal computational semantics of classical logic.

### Plate 25 — [PLANNED] Relevance: Two Proofs, Two Behaviors
**Burden:** Show when distinct evidence changes runtime output.
**Limit:** Only for a relevance-sensitive example.

### Plate 26 — [PLANNED] Erasure: What Disappears and What Must Remain
**Burden:** Partition proof-term structure into computationally retained and erased components under a stated policy.
**Limit:** Erasure criteria are system/calculus specific.

### Plate 27 — [PLANNED] Proof Irrelevance Is an Additional Principle
**Burden:** Prevent the reader from inferring proof irrelevance from propositions-as-types alone.
**Limit:** Some systems validate proof irrelevance in selected universes/propositions; `CH-0` does not assume it globally.

### Plate 28 — [PLANNED] Extraction Pipeline
**Burden:** Proof object → erasure/translation → executable program → replayed specification.
**Limit:** Exact only for the selected extraction examples.

### Plate 29 — [PLANNED] Witness-Preserving Extraction
**Burden:** Track an existential witness from proof construction into runtime output.
**Limit:** Demonstrates selected `Σ`-style examples, not a general proof-assistant extraction theorem.

### Plate 30 — [PLANNED] Extraction Failure Modes
**Burden:** Show how axioms, classical principles, opaque constants or effects can alter executable content.
**Limit:** Failure taxonomy is illustrative and system-dependent.

### Plate 31 — [PLANNED] Parametricity as Uniformity
**Burden:** Show one polymorphic program acting coherently across several type instantiations.
**Limit:** Finite examples illustrate consequences; they do not prove relational parametricity.

### Plate 32 — [PLANNED] Relations Travel Through a Polymorphic Term
**Burden:** Visualize a relational interpretation preserved by a selected polymorphic function.
**Limit:** Restricted `CHF-1` preview.
**Provenance:** `lab12_parametricity.py` finite fixtures.

### Plate 33 — [PLANNED] Free-Theorem Constraint Surface
**Burden:** Show how a polymorphic type removes possible implementations.
**Limit:** Requires purity/parametricity hypotheses that are stated in the chapter.

### Plate 34 — [PLANNED] Tactic, Elaborator, Kernel
**Burden:** Separate convenience automation from trusted checking.
**Limit:** Architecture is a toy abstraction; industrial systems differ.

### Plate 35 — [PLANNED] The Kernel Trust Cone
**Burden:** Depict which inputs must be independently rechecked before acceptance.
**Limit:** Trustworthiness still depends on the kernel implementation and foundational assumptions.

### Plate 36 — [PLANNED] Hostile Certificate Rejection
**Burden:** Show malformed elaborator output rejected by the independent tiny kernel.
**Limit:** Demonstrates the lab's trust boundary only.
**Provenance:** `lab13_kernel_boundary.py`.

### Plate 37 — [PLANNED] Proof / Program Correspondence Atlas
**Burden:** Summarize exact correspondences, translations, analogies and non-correspondences with distinct edge styles.
**Limit:** Classification is scoped to the calculi treated in this volume.

### Plate 38 — [PLANNED] Where Normalization Stops Being the Main Question
**Burden:** Contrast terminating closed evaluation with an intentionally nonterminating interactive service.
**Limit:** Nontermination can be correct for open systems; the plate does not establish protocol correctness.

### Plate 39 — [PLANNED] Closed Term vs Open Conversation
**Burden:** Place `input → output` computation beside a bilateral state machine with alternating obligations.
**Limit:** State machines alone do not provide session fidelity or liveness theorems.

### Plate 40 — [PLANNED] The Missing Dual
**Burden:** Show that a single closed type does not yet express complementary obligations of two communicating peers.
**Limit:** Previews, but does not formalize, session-type duality.

### Plate 41 — [PLANNED] Threshold to PROTOCOL
**Burden:** Collect the unresolved concepts—channel, duality, linearity, protocol state, progress, deadlock—that Volume IV must formalize.
**Limit:** A roadmap, not a theorem.

### Plate 42 — [PLANNED] Series Atlas: From Judgment to Interaction
**Burden:** Locate Volume III in the ten-volume argument and show the forced move from judgment/comprehension to proof/program and then protocol.
**Limit:** The series-wide unification remains a research thesis.

## Visual audit obligations

Before Gate 4:

- inspect every plate at actual manuscript scale and folio scale;
- reroute every connector that crosses readable text unless the crossing is semantically intentional;
- use `gcllabel` shields for free-standing text;
- verify grayscale legibility and nondependence on color;
- retain executable provenance for plates 4, 18, 20, 32 and 36 and any later computed visual;
- verify every caption states the pedagogical claim and scope/analogy limit where relevant.
