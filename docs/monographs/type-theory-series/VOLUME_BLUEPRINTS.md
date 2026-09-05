# VOLUME BLUEPRINTS — Volumes II–X

These are intellectual spines, not immutable tables of contents. The composing agent may alter chapter boundaries while preserving the governing question, formal burden, and next-volume threshold.

## Volume II — COMPREHENSION: How Computational Worlds Are Built

**Governing move:** from `Γ ⊢ a : A` to families `Γ,x:A ⊢ B(x) type` and the rules that create new spaces of possibilities.

Suggested arc: context extension; dependent families; substitution in types; Π-types; Σ-types; equality/transport preview; inductive families; indexed data; propositions with data; universes as codes preview; comprehension/categorical reading; type formation as language design; implementation of a small dependent checker; limits of definitional equality; threshold into proof/program.

**Core metatheory:** generalized substitution, weakening under dependency, subject reduction, decidable checking for a carefully chosen fragment, canonicity where justified. Do not silently claim normalization for a fragment not proved/cited.

**Labs:** dependent family evaluator/checker, length-indexed vectors, typed protocols as indexed states, elaboration experiments.

## Volume III — PROOF / PROGRAM: Logic Becomes Executable

**Governing move:** propositions-as-types as a precise structural correspondence rather than a slogan.

Suggested arc: natural deduction; implication/function; conjunction/product; disjunction/sum; universal/Π; existential/Σ; absurdity/empty; normalization as detour elimination; constructive vs classical principles; continuations/control; proof irrelevance/relevance distinctions; extraction; parametricity preview; proof assistants; limits of correspondence.

**Core metatheory:** normalization correspondences, proof-term preservation, admissibility/cut-elimination relations where scoped, extraction correctness examples.

## Volume IV — PROTOCOL: Computation as Communication

**Governing move:** replace closed input→output computation with typed interaction.

Suggested arc: conversations as state machines; channels; linearity; session types; duality; branching/selection; recursion; multiparty structure; progress vs deadlock freedom; subtyping/refinement; asynchronous semantics; process calculi; distributed failures; protocol monitoring; transition into effects.

**Core metatheory:** fidelity, communication safety, progress/deadlock hypotheses stated distinctly. Do not conflate session fidelity with distributed-system correctness.

## Volume V — EFFECTS: Computation Meets the World

**Governing move:** type the event, not only the returned value.

Suggested arc: pure/effectful split; state; exceptions; I/O; monads; algebraic effects; handlers; graded effects; capabilities; resource accounting; nondeterminism; probability; concurrency boundary; recursion/partiality; effect polymorphism; interaction with verification.

**Core metatheory:** effect soundness for chosen calculi, handler equations, capability confinement examples, probabilistic semantics with explicit assumptions.

## Volume VI — UNIVERSES: Languages That Speak About Languages

**Governing move:** make types/descriptions of types first-class while preserving stratification.

Suggested arc: codes and decoding; universe formation; hierarchy; Russell/Girard-style paradox pressure; polymorphism; generic programming; inductive-recursive ideas preview; reflection; quotation/elaboration; metaprogramming; staged computation; theorem-prover kernels; self-description limits; transition to identity.

## Volume VII — IDENTITY: Equality Becomes Structure

**Governing move:** internalize equality evidence.

Suggested arc: identity type; reflexivity; J; transport; dependent congruence; UIP/K; extensionality; equivalences; paths; higher paths; HITs; univalence; cubical computation preview; proof engineering; geometric semantics; computational content and unresolved boundaries.

**Critical discipline:** never let geometric pictures outrun the exact type-theoretic rules; every geometric reading pays rent computationally or semantically.

## Volume VIII — SEMANTICS: What Makes a Type Theory Mean Something?

**Governing move:** one syntax, multiple validating worlds.

Suggested arc: operational semantics; denotation; domains; categorical semantics; CCC/LCCC; realizability; logical relations; presheaves; games; linear categories; probabilistic semantics; homotopical semantics; adequacy; full abstraction; model comparison; invariants across semantics.

**Core question:** what survives change of model and is therefore genuinely structural?

## Volume IX — THE LIMITS OF CONSTRUCTION

**Governing move:** stress the unification thesis with what typed construction cannot simultaneously guarantee.

Suggested arc: undecidability; incompleteness; normalization vs universality; general recursion; recursive types; partiality; guarded recursion; effectful divergence; oracles; interaction/open systems; concurrency; continuous/analog computation; probability; physical computation; resource bounds; paradoxes; epistemic limits.

**Required tone:** adversarial. This volume must be capable of weakening the series thesis.

## Volume X — THE TYPE-THEORETIC SYNTHESIS

**Governing move:** state only the strongest thesis that survives Volumes I–IX.

Suggested arc: judgment; context; comprehension; substitution; construction; proof/program; interaction; effects; reflection; identity; semantics; limits; cross-domain case studies; what remains outside; minimal transferable structure; research agenda.

The final synthesis should distinguish at least three levels:

1. exact mathematical equivalences/correspondences;
2. robust structural analogies;
3. speculative research hypotheses.

The volume succeeds if the reader can see precisely where “type theory is what computation is” is theorem, framework, metaphor, or open problem.