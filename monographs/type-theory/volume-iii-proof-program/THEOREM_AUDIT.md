# Volume III Theorem Audit — Full Development

This is an **internal composing-process audit**, not Gate 8 independent mathematical review. Every row binds a result to the exact calculus and evidence route actually used in the manuscript.

| ID | Result | Exact scope | Dependencies / imported result | Critical cases | Disposition |
|---|---|---|---|---|---|
| T3.1 | Rule-level implication term assignment | `CH-0`, implication fragment | recursive assignment | assumption, `→I`, `→E` | proved in Ch. 1 |
| T3.2 | Weakening | `CH-0`, implication fragment | context freshness | abstraction alpha-renaming | proved in Ch. 1 |
| T3.3 | Capture-avoiding substitution | `CH-0`, implication fragment | T3.2 | variable, application, abstraction freshness | proved in Ch. 2 |
| T3.4 | Principal beta preservation | `CH-0`, implication fragment | T3.3 | inversion of application/abstraction typing | proved in Ch. 2 |
| T3.5 | Principal implication detour/beta correspondence | selected ND assignment into `CH-0` | T3.1, T3.3, T3.4 | discharged-assumption substitution | proved in Ch. 2 |
| T3.6 | Product term assignment | `CH-0` with `×` | T3.1 pattern | `×I`, `×E₁`, `×E₂` | proved in Ch. 3 |
| T3.7 | Product canonical form | closed `CH-0` values | value grammar + typing inversion | exclusion of non-pair value constructors | proved in Ch. 3 |
| T3.8 | Principal product preservation | `CH-0` | T3.7/inversion | both projections | proved in Ch. 3 |
| T3.9 | Sum canonical form | closed `CH-0` values | value grammar + typing inversion | left/right injections | proved in Ch. 4 |
| T3.10 | Principal case preservation | `CH-0` | substitution | both injection branches | proved in Ch. 4 |
| T3.11 | Canonical forms | closed values of full stated `CH-0` | T3.7, T3.9 + value grammar | arrow/product/sum/unit/empty | proved in Ch. 5 |
| T3.12 | Progress | closed well-typed `CH-0` under the deterministic teaching evaluator | T3.11 | application, projection, case, abort | proved in Ch. 5 |
| T3.13 | Preservation | stated `CH-0` evaluator reductions | substitution + inversion | beta, projections, case, congruence | proved in Ch. 5 |
| T3.14 | Strong normalization | pure `CH-0` only | standard reducibility/logical-relations theorem; Church/Prawitz/type-theory literature | arrow reducibility clause, fundamental lemma, products/sums | **imported standard result + structured proof architecture**, not independently re-proved |
| T3.15 | Natural-deduction normalization correspondence | selected `CH-0` assignment | Prawitz-style normalization + T3.5/product/sum principal cases | distinction between derivation reduction and term reduction | imported theorem context + exact principal cases proved |
| T3.16 | Dependent quantifier rule correspondence | `CHD-1` Π/Σ layer | exact inherited Volume-II rules | Π abstraction/application; Σ witness/evidence | proved at rule level in Ch. 6 |
| T3.17 | Dependent normalization | richer dependent calculi | none admitted here | — | **explicit non-result**; no transfer from T3.14 |
| T3.18 | Principal implication cut reduction | bounded `LJ-0` | formula/height cut measure | principal `→R/→L` pair | proved in Ch. 7 |
| T3.19 | Cut admissibility / cut elimination | standard intuitionistic propositional sequent calculus matching `LJ-0` | Gentzen Hauptsatz | principal and commuting reductions | **imported theorem**; bounded reducer is illustration only |
| T3.20 | Finite countermodel to excluded middle | two-world Kripke model in Ch. 8 | forcing definitions | root fails both `P` and `¬P` | proved by direct model evaluation |
| T3.21 | Non-derivability of excluded middle in the intuitionistic core | corresponding intuitionistic propositional calculus | standard Kripke soundness theorem + T3.20 | semantic-to-syntactic step | **imported soundness + explicit countermodel** |
| T3.22 | Restricted CPS typing preservation | displayed `CHC-1` arrow translation | structural induction | variable, abstraction, application | proved in Ch. 9 |
| T3.23 | Normalization/extraction for arbitrary control calculi | arbitrary continuation/control extensions | none admitted | — | **explicit non-result** |
| T3.24 | Toy erasure preservation | marked relevance fragment of Ch. 10/lab 10 | relevance checker invariant | ghost binder dependency | proved for toy architecture |
| T3.25 | Selected existential witness preservation | finite package/extractor architecture in lab 11 | package checker + registered predicate replay | corrupt certificate | proved in Ch. 11 |
| T3.26 | Industrial proof-assistant extraction correctness | external systems | system-specific theorems required | — | **explicit non-result** |
| T3.27 | Relational parametricity / abstraction theorem | restricted `CHF-1` conceptual preview | Reynolds abstraction theorem | relational arrow/type-variable interpretation | **imported theorem**; not re-proved |
| T3.28 | Finite relational fixture property | finite carrier/relation universe of lab 12 | exhaustive enumeration | vacuous/nonvacuous relations; hostile nonuniform function | proved from finite enumeration architecture |
| T3.29 | Kernel rechecking boundary | toy elaborator/kernel architecture in Ch. 13 | interface definition | wrong claimed type; unsupported certificate | proved architectural proposition |
| T3.30 | Closed normalization does not imply protocol correctness | finite two-party trace model in Ch. 14 | explicit request/ack counterexample | terminating handlers + illegal initial message | proved by construction |

## Dependency and induction-hypothesis audit

- The Chapter 1–5 structural proofs use induction only over the derivation/reduction object named in the statement. No proof step assumes normalization when proving preservation or progress.
- Substitution is invoked only where the premise provides a typed replacement and capture avoidance is explicit.
- The progress proof is restricted to **closed** terms and the declared evaluator. It is not stated for open terms.
- Strong normalization is not inferred from progress, preservation, or laboratory termination.
- The Chapter 6 Π/Σ correspondence imports only rule structure needed for the logical reading. No Volume-II pending independent-review status is silently upgraded.
- The Chapter 7 local cut proof is not used as a proof of the general Hauptsatz; general cut admissibility is explicitly imported.
- The Chapter 8 countermodel becomes a non-derivability result only through the separately imported soundness theorem.
- The Chapter 9 CPS theorem concerns typing preservation for the displayed translation only. It does not imply source/target contextual equivalence or normalization of a general control calculus.
- Chapter 10–13 executable propositions are architecture-specific and do not generalize to industrial proof assistants.
- Chapter 14 proves a separation result only; it establishes no session fidelity, progress, deadlock-freedom, fairness, or liveness theorem.

## Operational / equational separation

Operational one-step reduction `→` remains distinct from calculus-scoped definitional/equational equality `≡`. Product/sum eta laws appear only as equational exercise material unless explicitly oriented as an evaluator rule. Natural-deduction normalization, beta reduction, and sequent cut elimination remain distinct transformations connected by stated translations.

## Executable regression coverage

Fourteen laboratories cover representative executable claims. Labs 1–2 implement the implication checker and capture-avoiding normalizer. Labs 3–14 cover product/sum computation, finite progress/canonical-shape checks, finite dependent witnesses, bounded cut reduction, Kripke countermodel evaluation, CPS fixtures, hostile erasure, witness extraction/replay, finite relational checks, hostile kernel certificates, and protocol traces. Negative/hostile fixtures are present where permissive acceptance would be a false positive.

The retained 14-laboratory suite has passed the camera-ready exact-source replay used for Gate 7. This is regression evidence for the scoped executable claims only; it is not an independent mathematical review of the monograph.

## Gate-2 disposition

**PASS — internal formal closure for the development manuscript.** This disposition does not satisfy Gate 8 and does not certify the mathematical work independently.
