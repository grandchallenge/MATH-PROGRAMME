# Volume III Claims Ledger — PROOF / PROGRAM

Status vocabulary follows the series communication contract. A row marked `theorem-intended` is an obligation, not an established theorem, until its proof/audit state changes.

| ID | Claim | Status | Exact scope | Evidence/source route |
|---|---|---|---|---|
| C3.001 | Implication introduction/elimination and lambda abstraction/application have the same term-assignment shape. | theorem-intended / structural correspondence | `CH-0`, implication fragment | rule-by-rule translation in Ch. 1 |
| C3.002 | Under the selected term assignment, a principal implication detour corresponds to beta reduction. | theorem-intended / structural correspondence | `CH-0`, implication fragment | Ch. 2 principal reduction proof + lab trace |
| C3.003 | Weakening preserves `CH-0` typing. | theorem-intended | `CH-0` | structural induction |
| C3.004 | Capture-avoiding substitution preserves `CH-0` typing under the standard premise. | theorem-intended | `CH-0` | induction on typing derivation |
| C3.005 | Principal beta/detour reduction preserves `CH-0` types. | theorem-intended | `CH-0` | substitution lemma + reduction cases |
| C3.006 | Closed well-typed `CH-0` terms do not get stuck under the deterministic teaching evaluator. | theorem-intended | `CH-0`, chosen evaluator | canonical forms + progress proof |
| C3.007 | Every well-typed `CH-0` term is strongly normalizing. | cited standard theorem + structured proof sketch | `CH-0` only | reducibility/logical-relations literature |
| C3.008 | Natural-deduction normalization and typed term normalization are tightly aligned under the chosen `CH-0` assignment. | cited theorem + bounded exact correspondence | `CH-0` | Prawitz-style normalization; principal-case derivations |
| C3.009 | Conjunction corresponds to product construction/projection under `CH-0`. | theorem-intended / structural correspondence | `CH-0` | Ch. 3 rules + evaluator |
| C3.010 | Constructive disjunction carries branch choice and evidence, matching typed sums/case analysis. | theorem-intended / structural correspondence | `CH-0` | Ch. 4 rules + evaluator |
| C3.011 | Empty elimination permits construction of any target from an impossible inhabitant, without creating an inhabitant of `0`. | theorem-intended | `CH-0` | typing rule + canonical-forms argument |
| C3.012 | Universal and existential constructive readings align with `Π` and `Σ` formation/introduction/elimination rules. | theorem-intended / structural correspondence | `CHD-1` | inherited Volume-II rules + Ch. 6 translation |
| C3.013 | The Volume-II `Π/Σ` rules are inherited at their actual durable-but-unreviewed institutional state. | institutional fact | protected prior-volume records | series manifest/release records |
| C3.014 | Cut in a bounded intuitionistic sequent calculus can be read as explicit substitution/composition, with cut elimination related to normalization. | cited theorem + bounded executable examples | `LJ-0` | Gentzen-style theorem + lab 07 |
| C3.015 | `A ∨ ¬A` is not derivable in `CH-0` merely from the constructive rules. | theorem/countermodel-intended | propositional `CH-0` | finite Kripke countermodel + standard intuitionistic semantics |
| C3.016 | Classical principles may be given computational readings through translations or control operators, but those readings extend/change the constructive core. | scoped interpretation | `CHC-1` | CPS translation + typed-control examples |
| C3.017 | The selected CPS translation preserves typing. | theorem-intended | restricted `CHC-1` translation | structural induction |
| C3.018 | Proof relevance and proof irrelevance are distinct design choices; `CH-0` does not assume global proof irrelevance. | formal scope statement | Volume III | calculus definition + erasure chapter |
| C3.019 | Selected constructive proofs can be transformed into executable witness-producing programs whose outputs replay the proved specification. | theorem-intended per example | selected `CH-0` / `CHD-1` examples | extraction lab + direct replay |
| C3.020 | The volume does not establish a general industrial proof-assistant extraction theorem. | explicit non-result | external systems | claim boundary |
| C3.021 | Relational parametricity constrains polymorphic programs beyond ordinary typing alone. | cited theorem / preview | `CHF-1` examples | Reynolds-style literature + finite relation lab |
| C3.022 | Finite relation checks in lab 12 illustrate selected parametricity consequences but do not prove the full abstraction theorem. | computed observation | finite fixtures only | machine-readable evidence |
| C3.023 | A proof assistant's elaborator and kernel occupy different trust roles; independent kernel rechecking can reject malformed elaborator output. | theorem-intended system proposition | toy lab 13 architecture | independent checker + hostile fixtures |
| C3.024 | Successful checking, normalization or extraction of selected examples does not establish the monograph's metatheory as a whole. | evidentiary boundary | all labs | series technical-writing contract |
| C3.025 | The slogan “propositions are types” is accurate only after fixing a logical/type-theoretic correspondence; it is not a claim that all types are truth values. | scope statement | entire volume | formal exposition |
| C3.026 | The slogan “proofs are programs” is a compressed description of structural correspondences, not unrestricted identity across every logic/programming language. | scope statement | entire volume | cross-calculus comparison |
| C3.027 | Normalization, cut elimination and execution strategy must remain distinct theorem/operational notions even when translations connect them. | scope statement | `CH-0` / `LJ-0` | theorem audit + Chs. 2,7 |
| C3.028 | Classical control can invalidate naive transfer of constructive normalization/extraction claims. | pressure-point claim | `CHC-1` comparison | typed-control examples + cited literature |
| C3.029 | Closed proof-term evaluation does not by itself express the central correctness questions of indefinitely open communication. | bounded conceptual result | transition chapter | closed-term/open-protocol comparison lab |
| C3.030 | Volume IV is forced by the need to type interaction, dual obligations, protocol state and liveness/deadlock distinctions rather than merely returned values. | series transition thesis | end of Volume III | Ch. 14 synthesis |

## Explicit non-results

The current work set must not silently promote any of the following:

- full normalization for unrestricted dependent type theory;
- full normalization for arbitrary continuations/effects;
- global proof irrelevance;
- constructive derivability of excluded middle;
- unrestricted Curry–Howard identity across all logics and languages;
- full cut elimination for arbitrary sequent systems;
- general extraction correctness for Coq, Lean, Agda or other industrial systems;
- full relational parametricity for an implemented System F kernel;
- protocol fidelity, deadlock freedom or distributed-system correctness.

These remain outside the exact formal scope unless a later revision explicitly changes the calculus and reopens the corresponding audits.
