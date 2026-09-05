# Illustration Register — Volume II: COMPREHENSION

Status key: `FINISHED-B1`, `PLANNED`.

## Plate 1 — FINISHED-B1 — Fixed World / Dependent World
**Pedagogical burden:** isolate the single conceptual step from a fixed type `B` to a family `B(x)` whose well-formedness may mention an earlier term.  
**Composition:** two parallel panels; left with repeated `B`, right with fibers `B(a_0),B(a_1),B(a_2)` over an index line.  
**Analogy/scope limit:** the fiber picture is a geometric reading of dependency, not the syntax itself.

## Plate 2 — FINISHED-B1 — The Telescope
**Pedagogical burden:** make context order visibly semantic.  
**Composition:** declarations descending diagonally, each later declaration allowed to point backward only.  
**Analogy/scope limit:** arrows indicate free-variable dependency, not runtime dataflow.

## Plate 3 — FINISHED-B1 — Substitution Rewrites the World
**Pedagogical burden:** show that substituting for `x` changes both terms and the types of later declarations.  
**Composition:** `n:Nat, i:Fin(n)` transformed by `[3/n]` into `i:Fin(3)`.  
**Analogy/scope limit:** the plate depicts capture-free structural substitution, not evaluation.

## Plate 4 — FINISHED-B1 — Dependency Is Not Runtime Tagging
**Pedagogical burden:** prevent the common confusion between static family formation and dynamic case analysis.  
**Composition:** family-formation judgment on left, runtime branch tree on right, separated by a warning bar.  
**Analogy/scope limit:** both may inspect related information in implementations, but they are different judgments/semantics.

## Plate 5 — FINISHED-B1 — The Comprehension Loop
**Pedagogical burden:** show dependency as a compositional cycle: form family, extend context, construct, substitute, specialize.  
**Composition:** five-stage ring with central judgment.  
**Analogy/scope limit:** the cycle is pedagogical organization; derivations are trees, not literal cyclic proofs.

## Plate 6 — PLANNED — Π as a Bundle of Codomains
**Pedagogical burden:** show one dependent function ranging over varying codomains.  
**Scope limit:** not a set-theoretic function-space construction unless a model is explicitly chosen.

## Plate 7 — PLANNED — Constant-Family Collapse: Π → Arrow
**Pedagogical burden:** make ordinary function types a special case of dependent products.  
**Scope limit:** “collapse” means syntactic specialization when the bound variable is not free in the codomain.

## Plate 8 — PLANNED — Application Changes the Result Type
**Pedagogical burden:** show `f a : B(a)` and why application substitutes into the codomain.  
**Scope limit:** type substitution is not runtime mutation.

## Plate 9 — PLANNED — Σ as a Fibered Space of Pairs
**Pedagogical burden:** show second components whose type depends on the first.  
**Scope limit:** geometric fibers are semantic intuition only.

## Plate 10 — PLANNED — Constant-Family Collapse: Σ → Product
**Pedagogical burden:** recover ordinary products from constant dependent pairs.  
**Scope limit:** no claim of definitional identity across all presentations.

## Plate 11 — PLANNED — The Second Projection Knows the First
**Pedagogical burden:** visualize why `snd p` has type `B(fst p)`.  
**Scope limit:** dependence is typed structure, not object-oriented field lookup.

## Plate 12 — PLANNED — Telescope versus Unordered Environment
**Pedagogical burden:** contrast dependent contexts with ordinary finite maps.  
**Scope limit:** implementations may use maps internally while preserving an ordered dependency invariant.

## Plate 13 — PLANNED — Weakening
**Pedagogical burden:** show when a new independent declaration can be inserted without changing an old derivation.  
**Scope limit:** insertion positions are constrained by dependencies.

## Plate 14 — PLANNED — Exchange Is Conditional
**Pedagogical burden:** show why arbitrary permutation of declarations fails under dependency.  
**Scope limit:** independent declarations may still exchange.

## Plate 15 — PLANNED — `Fin(n)` as an Indexed Boundary
**Pedagogical burden:** show index-controlled inhabitance.  
**Scope limit:** finite-set semantics is an interpretation; the formal burden is carried by formation/constructor rules.

## Plate 16 — PLANNED — Vector Length in the Type
**Pedagogical burden:** distinguish list payload from vector index.  
**Scope limit:** length indices guarantee length, not element-level semantic correctness.

## Plate 17 — PLANNED — Constructors Refine Indices
**Pedagogical burden:** show how constructors determine output indices.  
**Scope limit:** only the admitted strictly-positive family is in scope.

## Plate 18 — PLANNED — Impossible Constructor/Index Combinations
**Pedagogical burden:** make unrepresentable states visually explicit.  
**Scope limit:** impossibility is relative to the exact family definition.

## Plate 19 — PLANNED — The Motive Drives Elimination
**Pedagogical burden:** show why dependent elimination needs a family of result types.  
**Scope limit:** not every eliminator is generated automatically in the volume's toy implementation.

## Plate 20 — PLANNED — Safe Lookup
**Pedagogical burden:** connect `Fin(n)` indices to vector lookup without bounds failure.  
**Scope limit:** memory safety beyond the modeled operation is not claimed.

## Plate 21 — PLANNED — List Head / Vector Head
**Pedagogical burden:** compare partial list head with a type-directed nonempty vector head.  
**Scope limit:** totality depends on the precise input type, not on “dependent types” generically.

## Plate 22 — PLANNED — Conversion by Definitional Equality
**Pedagogical burden:** show a term crossing between definitionally equal types.  
**Scope limit:** no propositional equality evidence is introduced.

## Plate 23 — PLANNED — Where Definitional Equality Runs Out
**Pedagogical burden:** expose equalities that require more than computation/congruence.  
**Scope limit:** the plate motivates later identity structure but does not formalize it.

## Plate 24 — PLANNED — The Transport Problem Before Identity Types
**Pedagogical burden:** make the need for transport visible without prematurely importing Volume VII.  
**Scope limit:** transport is only posed as a problem here.

## Plate 25 — PLANNED — Bidirectional Synthesis / Checking
**Pedagogical burden:** show information flow in two typing modes.  
**Scope limit:** algorithmic judgments are implementation artifacts relative to the chosen calculus.

## Plate 26 — PLANNED — Why Lambdas Need an Expected Type
**Pedagogical burden:** show loss of synthesis information at binders.  
**Scope limit:** annotation policy varies by checker.

## Plate 27 — PLANNED — Annotation as Local Evidence
**Pedagogical burden:** show how explicit types restore algorithmic direction.  
**Scope limit:** annotations do not strengthen the declarative theory by themselves.

## Plate 28 — PLANNED — Metavariables and Constraint Flow
**Pedagogical burden:** expose elaboration as constrained inference, not magic.  
**Scope limit:** no claim of complete higher-order unification.

## Plate 29 — PLANNED — Elaboration Success / Failure Boundary
**Pedagogical burden:** show where omitted information can and cannot be recovered.  
**Scope limit:** boundary is checker-specific.

## Plate 30 — PLANNED — Algorithmic Equality versus Semantic Equality
**Pedagogical burden:** separate decidable comparison from broader mathematical sameness.  
**Scope limit:** semantic equality depends on model/logic.

## Plate 31 — PLANNED — Codes and Decoding
**Pedagogical burden:** preview Tarski-style universe structure.  
**Scope limit:** no full universe hierarchy is developed.

## Plate 32 — PLANNED — Why `Type : Type` Is Dangerous
**Pedagogical burden:** visualize self-reference pressure.  
**Scope limit:** paradox proof is deferred; plate is motivation, not derivation.

## Plate 33 — PLANNED — Stratification Pressure
**Pedagogical burden:** show hierarchy as one response to self-reference.  
**Scope limit:** not the only possible universe discipline.

## Plate 34 — PLANNED — Comprehension as Context Projection
**Pedagogical burden:** connect a context extension `Γ,x:A` to projection back to `Γ`.  
**Scope limit:** categorical reading begins here and must not replace syntax.

## Plate 35 — PLANNED — Fiber over a Context Element
**Pedagogical burden:** show family semantics over a base context.  
**Scope limit:** fibers are model-dependent semantic objects.

## Plate 36 — PLANNED — Syntax / Semantics Correspondence Map
**Pedagogical burden:** pair judgments with categorical structures.  
**Scope limit:** correspondence is scoped to a chosen model notion.

## Plate 37 — PLANNED — Language Design by Formation Rules
**Pedagogical burden:** show formation principles as controls on what programs can be expressed.  
**Scope limit:** expressibility is not computational efficiency.

## Plate 38 — PLANNED — Two Calculi, Two Computational Worlds
**Pedagogical burden:** compare fragments with/without a dependent former.  
**Scope limit:** toy fragments do not exhaust real language design.

## Plate 39 — PLANNED — Expressiveness versus Checking Cost
**Pedagogical burden:** surface the tradeoff pressure introduced by richer equality/dependency.  
**Scope limit:** no universal complexity law is asserted.

## Plate 40 — PLANNED — What Indices Cannot Guarantee
**Pedagogical burden:** mark the boundary between encoded and unencoded invariants.  
**Scope limit:** type systems can encode more than shown; the point is that guarantees are representation-relative.

## Plate 41 — PLANNED — From Inhabited Type to Proposition
**Pedagogical burden:** reveal the proof/program threshold without asserting Curry–Howard by slogan.  
**Scope limit:** Volume III establishes the structural correspondence.

## Plate 42 — PLANNED — Series Atlas: Volume II
**Pedagogical burden:** locate comprehension between judgment and proof/program in the ten-volume argument.  
**Scope limit:** atlas arrows are conceptual dependencies, not theorem implications.
