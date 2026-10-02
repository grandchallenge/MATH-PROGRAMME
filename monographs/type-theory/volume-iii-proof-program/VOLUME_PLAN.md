# Volume III — PROOF / PROGRAM: Logic Becomes Executable

## Gate 0 preflight contract

Work set: `TYPE-THEORY-VOL-III-001`

Tracking issue: `#865`

Protected starting head: `98ece0ccb07943ca3690b69a8e831eef5e8bfa80`

Series thesis status: **research hypothesis, not established theorem**.

## Governing question

**Why do logical construction and computational construction repeatedly share the same laws?**

The volume will answer this by exhibiting exact correspondences where they exist, separating them from translations and analogies where they do not, and ending at the point where closed proof/program evaluation is no longer an adequate model of computation because interaction itself becomes primary.

## Institutional inheritance

Volume III inherits formal and pedagogical content from Volumes I and II at the state actually achieved on protected GitHub:

- Volume I — JUDGMENT RC1.1: `RC_COMPOSITION_COMPLETE`, `RC_DURABLY_ADMITTED`, independent mathematical review pending, publication authority not granted.
- Volume II — COMPREHENSION RC1: `RC_COMPOSITION_COMPLETE`, `RC_DURABLY_ADMITTED`, independent mathematical review pending, publication authority not granted.

No Volume III statement may silently upgrade either prior volume to independently reviewed or authoritative publication status.

### Machinery inherited from Volume I

Reused without changing meaning:

- contexts `Γ, Δ`;
- typing judgments `Γ ⊢ t : A`;
- nondependent function, product, sum, unit and empty types;
- capture-avoiding substitution `t[u/x]`;
- one-step and multi-step term reduction;
- definitional/equational equality as calculus-scoped;
- canonical forms, weakening, substitution, preservation and progress patterns for small typed calculi.

Reintroduced for self-containment:

- typing derivations;
- introduction and elimination rules;
- the simply typed lambda-calculus term constructors used by the proof-term correspondence;
- substitution and beta reduction.

### Machinery inherited from Volume II

Reused without changing meaning:

- dependent families `Γ,x:A ⊢ B(x) type`;
- dependent products `Π(x:A).B(x)`;
- dependent sums `Σ(x:A).B(x)`;
- substitution through dependent types.

These appear only after the nondependent proof/program core is established. Volume III does not rely on the still-open independent review status of Volume II to claim more than the exact internal calculus and standard cited metatheory used here.

## Exact calculi in scope

### `CH-0` — constructive proof/program core

`CH-0` is the primary formal calculus of the volume. It is an intuitionistic natural-deduction presentation synchronized with a simply typed lambda calculus containing:

- atomic propositions/types `P, Q, R, ...`;
- implication/function `A → B`;
- conjunction/product `A × B`;
- disjunction/sum `A + B`;
- truth/unit `1`;
- falsity/empty `0`.

Term constructors:

- variables `x`;
- abstraction `λx.t` and application `t u`;
- pairing `⟨t,u⟩` and projections `π₁ t`, `π₂ t`;
- injections `inl t`, `inr t` and case analysis;
- unit inhabitant `⋆`;
- empty elimination `abort_A(t)`.

Logical readings are attached to the same formation/introduction/elimination structure:

- `A → B` as implication;
- `A × B` as conjunction;
- `A + B` as disjunction with chosen evidence;
- `1` as truth;
- `0` as falsity.

The volume will use the phrase **Curry–Howard correspondence** for this rule/term correspondence. It will not assert unrestricted identity between every notion of proof and every notion of program.

### `CHD-1` — dependent quantifier extension

A secondary extension inherits `Π` and `Σ` from Volume II to show the constructive readings

- `Π(x:A).B(x)` as universal construction over `A`;
- `Σ(x:A).B(x)` as existential witness paired with evidence.

`CHD-1` is not the calculus under which all `CH-0` normalization results are automatically claimed. Any theorem used at the dependent layer will be separately scoped and either proved, cited, or explicitly postponed.

### `CHC-1` — classical/control interpretation layer

A separate comparison layer introduces classical principles through translations or typed control constructs, principally double-negation/CPS readings and a restricted continuation calculus.

`CHC-1` is deliberately not merged into `CH-0`. Classical principles, control effects, and their operational behavior can change normalization and extraction properties. Results for `CH-0` do not silently transfer to `CHC-1`.

### `CHF-1` — parametricity preview

A small polymorphic comparison layer is used late in the volume to motivate relational parametricity. It will use a restricted System-F-style syntax only for examples and a finite relation-checking laboratory. The volume will cite rather than re-prove the full abstraction theorem for relational parametricity.

## Operational and equational semantics

### `CH-0` operational reduction

The primary reduction relation is compatible closure of the expected beta/detour reductions:

- `(λx.t) u → t[u/x]`;
- `π₁⟨t,u⟩ → t` and `π₂⟨t,u⟩ → u`;
- `case (inl t) of ... → ...[t/x]`;
- `case (inr t) of ... → ...[t/y]`.

The executable laboratory will implement a deterministic normal-order strategy for trace generation. The mathematical reduction relation is not identified with that single evaluation strategy.

### Equational/definitional layer

Definitional equality `≡` is the congruence/equational closure generated by the scoped beta/eta laws explicitly listed for the current chapter/calculus. Operational one-step reduction `→` and definitional equality `≡` remain distinct relations.

### Logical normalization

Natural-deduction normalization is presented as elimination of introduction-followed-by-elimination detours. For the synchronized `CH-0` term assignment, principal logical detours correspond to beta-like term redexes. “Correspond” does not mean the two metatheories are literally the same presentation.

### Sequent layer

A later intuitionistic sequent-calculus fragment `LJ-0` is introduced to expose cut and cut elimination. Translation between `CH-0` natural deduction and `LJ-0` is used pedagogically. The volume will not claim that every normalization step is a one-to-one cut-elimination step without an explicit translation theorem.

## Intended metatheory

| ID | Result | Disposition | Exact scope | Evidence route |
|---|---|---|---|---|
| T3.1 | Weakening | prove | `CH-0` | structural induction on typing derivation |
| T3.2 | Substitution | prove | `CH-0` | induction on typing derivation with binder case explicit |
| T3.3 | Preservation under principal reduction | prove | `CH-0` | cases using T3.2 |
| T3.4 | Canonical forms | prove | closed `CH-0` values | inversion on typing derivation |
| T3.5 | Progress for deterministic evaluator | prove | closed well-typed `CH-0` terms | induction on typing derivation + canonical forms |
| T3.6 | Strong normalization | cite + structured proof sketch | `CH-0` | reducibility/logical-relations argument; classical standard result |
| T3.7 | Natural-deduction normalization correspondence | cite + demonstrate exact principal cases | `CH-0` assigned proofs/terms | Prawitz-style normalization plus term-assignment map |
| T3.8 | Cut admissibility / cut elimination | cite + prove bounded examples | `LJ-0` | Gentzen-style theorem; executable bounded cut reducer |
| T3.9 | Quantifier/proof-term correspondence | prove rule correspondence; cite deeper normalization | `CHD-1` | inherited `Π/Σ` rules + explicit logical reading |
| T3.10 | Double-negation/CPS typing preservation | prove for translation used | restricted `CHC-1` | structural induction over translated terms |
| T3.11 | Classical law executable reading | demonstrate, not universalize | restricted typed-control examples | CPS/control laboratory |
| T3.12 | Extraction correctness examples | prove per selected examples | `CH-0` / selected `CHD-1` propositions | evaluator equality + type preservation |
| T3.13 | General proof-assistant extraction correctness | cite / explicitly not re-prove | external systems | primary/system documentation and literature |
| T3.14 | Parametricity theorem | cite; finite instances computed | `CHF-1` preview only | Reynolds-style relational interpretation + finite checker |
| T3.15 | Kernel rechecking trust-boundary proposition | prove as system-architecture statement | toy elaborator/kernel lab | independent parser/checker interface and rejection tests |

## Metatheorems explicitly not established by this volume

Unless a later exact revision proves and audits them, Volume III does **not** establish:

- normalization for unrestricted dependent type theory;
- normalization for arbitrary control/effect calculi;
- proof irrelevance as a general principle;
- excluded middle or double-negation elimination in `CH-0`;
- a full Curry–Howard equivalence between all logics and all programming languages;
- a general extraction theorem for industrial proof assistants;
- full relational parametricity for an implemented System F kernel;
- cut elimination for arbitrary sequent calculi;
- termination or liveness of open concurrent protocols.

## Central distinctions not to collapse

1. **Derivation vs term.** A proof derivation and a proof term can encode the same constructive content under a term assignment, but their syntax and bureaucracy differ.
2. **Normalization vs execution strategy.** A normalization theorem concerns all reduction sequences or existence of normal forms under stated hypotheses; a laboratory evaluator chooses one strategy.
3. **Logical detour vs beta redex.** They correspond under the chosen assignment; neither phrase is a universal synonym for the other.
4. **Operational reduction vs definitional equality.** `→` is directed computation; `≡` is an equational relation.
5. **Constructive vs classical validity.** Classical principles require additional proof principles, translations, semantics, or control structure.
6. **Proof relevance vs proof irrelevance.** `CH-0` proof terms are computationally relevant unless a separate erasure/irrelevance policy is stated.
7. **Extraction vs evaluation.** Evaluation runs an already executable term; extraction removes or reorganizes logically irrelevant structure according to an external criterion.
8. **Propositions-as-types vs all types are propositions.** The logical reading selects a use of types; data types need not be collapsed into truth values.
9. **Normalization vs cut elimination.** Closely related under translations, but not literally the same theorem statement.
10. **Closed computation vs interaction.** A term reducing to a value does not by itself model an indefinitely open protocol with independent peers.

## Chapter and laboratory map

Target: 14 teaching chapters, one executable laboratory per chapter.

| Ch. | Working title | Formal/pedagogical burden | Laboratory |
|---:|---|---|---|
| 1 | A Proof That Runs | implication introduction/elimination and lambda abstraction/application | `lab01_implication_checker.py` — parse/check implication proofs and terms |
| 2 | Detours That Compute | natural-deduction detours and beta normalization | `lab02_normalizer.py` — typed reduction traces and normal forms |
| 3 | Conjunction Carries Both | conjunction/product and proof relevance | `lab03_products.py` — product construction/projections and derivation traces |
| 4 | Disjunction Makes a Choice | sum types, disjunction evidence and case analysis | `lab04_sums.py` — case evaluator with branch typing |
| 5 | Truth, Falsity, and Impossible Branches | unit/empty, absurd elimination, canonical forms | `lab05_empty_unit.py` — canonical-value enumerator and rejection tests |
| 6 | Quantifiers Are Dependent Construction | universal/`Π`, existential/`Σ` | `lab06_quantifiers.py` — finite-domain dependent witness/checking examples |
| 7 | Cut Is Substitution Wearing Different Clothes | `LJ-0`, cut, substitution and translations | `lab07_cut_reducer.py` — bounded cut-reduction traces |
| 8 | What Constructive Logic Refuses to Guess | intuitionistic/classical boundary; excluded middle | `lab08_kripke.py` — finite Kripke countermodel for selected classical schemas |
| 9 | Classical Logic as Control | double negation, CPS, continuations | `lab09_cps.py` — typed CPS translation and trace comparison |
| 10 | When Proofs Matter | relevance, erasure and proof-irrelevance policies | `lab10_erasure.py` — compare relevant and erased execution traces |
| 11 | Extraction | witness-preserving constructive extraction | `lab11_extractor.py` — selected certified examples with replay |
| 12 | Uniformity Has Teeth | polymorphism and parametricity preview | `lab12_parametricity.py` — finite relational checks for polymorphic exemplars |
| 13 | Proof Assistants Have a Trust Boundary | elaboration, kernel checking, certificates | `lab13_kernel_boundary.py` — untrusted elaborator + independent tiny kernel |
| 14 | Where Proof / Program Stops Being Enough | limits of the correspondence and open interaction | `lab14_protocol_threshold.py` — closed term vs interactive state-machine comparison |

## Initial plate register — Gate 1 tranche

The first six plates each carry one burden.

1. **One constructive object, two presentations.** A natural-deduction implication proof and its lambda term are aligned rule-by-rule. Limit: this is for the `CH-0` term assignment, not every proof formalism.
2. **Introduction then elimination is a detour.** The proof detour and beta redex are shown side-by-side. Limit: the visual aligns principal reductions only.
3. **The implication machine.** Assumption discharge becomes lexical binding; modus ponens becomes application. Limit: semantic truth conditions are not replaced by runtime behavior.
4. **A normalization trace.** A typed term contracts through several redexes to normal form with its proof derivation remaining type-correct. Limit: one deterministic trace does not prove strong normalization.
5. **Conjunction/product preview.** Paired evidence supports both projections. Limit: logical conjunction and arbitrary data products are structurally aligned here, not universally identical semantic objects.
6. **Disjunction/sum preview.** Constructive disjunction carries which branch and its evidence. Limit: this differs from a proof-irrelevant Boolean truth value.

Default full visual target remains 42 plates; no padding is permitted.

## Exercise ecology and solutions plan

Each teaching chapter targets 12 exercises:

- 3 Checkpoint;
- 3 Core;
- 2 Synthesis;
- 2 Proof Workshop;
- 1 Design Clinic;
- 1 Challenge.

Expected full volume: 168 exercises. Every exercise receives either a worked solution or an explicit rubric in `solutions_companion.tex`. Research/open problems must be labeled as such rather than presented as deterministic exercises.

Gate 1 requires complete solutions/rubrics for Chapters 1–2 before scaling.

## Bibliography and historical-attribution plan

Primary/foundational source families to verify and cite:

- Gentzen on natural deduction and sequent calculi/cut elimination;
- Church on typed lambda calculus;
- Curry and Feys / Curry-school term-assignment history;
- Howard on formulae-as-types;
- Prawitz on natural-deduction normalization;
- Girard/Reynolds on polymorphism and parametricity;
- Griffin and subsequent work on classical logic/control;
- foundational proof-assistant/kernel and extraction literature where system-specific claims are made.

Modern expository reference families:

- proof theory and constructive logic texts;
- typed lambda-calculus texts;
- programming-language type-system references;
- proof-assistant metatheory/extraction references.

Historical scholarship rules:

- distinguish manuscript/circulation/publication dates where relevant;
- do not compress “Curry–Howard” into a single-origin event;
- identify which correspondence is being attributed: propositions/types, proofs/terms, normalization/reduction, or later extensions;
- primary sources are preferred for priority claims.

No novelty claim about the Curry–Howard correspondence will be made without a separate literature audit.

## Pressure points against the grand-unification thesis

Volume III must actively test the thesis against these failures of naive identity:

1. Classical logic can require continuations/control or a translation rather than direct constructive execution.
2. Proof irrelevance can intentionally erase distinctions that ordinary programs preserve.
3. Effects and nontermination can break simple normalization stories.
4. Some logics correspond more naturally to process calculi, linear calculi, modal calculi, games, or categorical semantics than to plain functions.
5. Proof assistants separate elaboration, kernels, tactics, certificates and extracted programs; “the proof is the program” can hide a substantial trust architecture.
6. Open reactive systems do not naturally terminate in a value. Their correctness concerns traces, protocols, fairness and liveness.
7. Semantic equivalence of proofs/programs can quotient away syntactic distinctions differently on the logical and computational sides.

If these pressure points force the volume to weaken the series thesis, the text will do so explicitly.

## Next-volume threshold

**Open interaction and protocols.**

Volume III ends when the reader can see a precise limitation: Curry–Howard explains closed constructive objects and many transformations of evidence exceptionally well, but a computation whose primary object is an ongoing conversation is not adequately characterized by “evaluate this proof term to a value.” The next volume must therefore type interaction itself: channels, duality, linear resources, protocol states, fidelity, progress and deadlock distinctions.

## Smallest safe executable tranche

Gate 1 tranche:

- Chapter 1 — implication/function correspondence;
- Chapter 2 — detour elimination/beta normalization;
- formal definitions and proofs needed for weakening, substitution and preservation in the implication fragment;
- `lab01_implication_checker.py` and `lab02_normalizer.py`;
- Plates 1–6;
- 24 exercises using the six-mode ecology;
- 24 worked solutions/rubrics;
- executable evidence fixtures for successful checking, rejection of ill-typed terms, and normalization traces;
- notation-registry extension for the new proof-theoretic symbols actually introduced.

Only after this tranche compiles, executes, validates and is visually inspected should the remaining twelve chapters scale out.
