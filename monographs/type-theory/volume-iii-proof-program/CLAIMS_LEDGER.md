# Volume III Claims Ledger — PROOF / PROGRAM

Statuses below are exact to the full-development manuscript. `proved` means proved internally in the stated manuscript calculus/architecture; it does **not** mean independently reviewed.

| ID | Claim | Status | Exact scope / evidence |
|---|---|---|---|
| C3.001 | Implication ND rules correspond structurally to lambda abstraction/application. | proved structural correspondence | `CH-0` implication; Ch. 1 |
| C3.002 | Principal implication detour corresponds to beta substitution under the assignment. | proved structural correspondence | `CH-0` implication; Ch. 2 |
| C3.003 | Weakening preserves typing. | proved | `CH-0` implication; Ch. 1 |
| C3.004 | Capture-avoiding substitution preserves typing under its premises. | proved | `CH-0` implication; Ch. 2 |
| C3.005 | Principal beta reduction preserves types. | proved | `CH-0` implication; Ch. 2 |
| C3.006 | Closed well-typed terms do not get stuck under the teaching evaluator. | proved | full stated `CH-0`; Ch. 5 |
| C3.007 | Every well-typed pure `CH-0` term is strongly normalizing. | imported standard theorem + proof architecture | pure `CH-0`; Ch. 5 |
| C3.008 | ND normalization and term normalization align under the chosen assignment. | imported context + proved principal cases | `CH-0`; Chs. 2–5 |
| C3.009 | Conjunction corresponds to product construction/projection. | proved structural correspondence | `CH-0`; Ch. 3 |
| C3.010 | Constructive disjunction carries branch choice/evidence matching sums/case. | proved structural correspondence | `CH-0`; Ch. 4 |
| C3.011 | Empty elimination constructs any target only from an impossible empty premise. | proved by rules/canonical forms | `CH-0`; Ch. 5 |
| C3.012 | Π/Σ rules support universal/existential constructive readings. | proved rule correspondence | `CHD-1`; Ch. 6 |
| C3.013 | Volume-II Π/Σ material is inherited at durable-but-unreviewed state. | institutional fact | protected series records |
| C3.014 | Cut is explicit composition and cut elimination is related to normalization through translation. | local reductions proved; general theorem imported | `LJ-0`; Ch. 7 |
| C3.015 | Excluded middle is not derivable from the intuitionistic core alone. | finite countermodel + imported soundness | Ch. 8 |
| C3.016 | Classical principles can receive computational readings through translations/control. | scoped interpretation | `CHC-1`; Ch. 9 |
| C3.017 | The selected restricted CPS translation preserves typing. | proved | `CHC-1`; Ch. 9 |
| C3.018 | Proof relevance and proof irrelevance are distinct; `CH-0` assumes no global irrelevance. | calculus scope fact | Ch. 10 |
| C3.019 | Selected constructive packages extract witnesses that replay their registered specification. | proved per finite architecture | Ch./lab 11 |
| C3.020 | General industrial extraction correctness is established here. | explicit non-result | excluded |
| C3.021 | Relational parametricity constrains polymorphic programs beyond typing. | imported theorem / preview | `CHF-1`; Ch. 12 |
| C3.022 | Finite relation checks illustrate selected consequences only. | computed finite observation | lab 12 |
| C3.023 | Independent toy kernel rechecking rejects malformed elaborator output. | proved architectural proposition + hostile fixtures | Ch./lab 13 |
| C3.024 | Selected executable successes establish the monograph's metatheory as a whole. | explicit non-result | all labs |
| C3.025 | Propositions-as-types does not mean all types are truth values. | scope statement | entire volume |
| C3.026 | “Proofs are programs” is not unrestricted identity across all logics/languages. | scope statement | entire volume |
| C3.027 | Normalization, cut elimination, and execution strategy remain distinct. | formal scope statement | `CH-0` / `LJ-0` |
| C3.028 | Constructive normalization/extraction transfers automatically to classical control. | explicit non-result | `CHC-1` excluded transfer |
| C3.029 | Closed proof-term evaluation alone does not express open communication correctness. | proved separation example + synthesis | Ch. 14 |
| C3.030 | Volume IV is forced by the need to type peer-relative interaction obligations. | series transition thesis | Ch. 14 |

## Explicit non-results retained

No claim is made of unrestricted dependent normalization; arbitrary-control normalization; global proof irrelevance; constructive excluded middle; universal Curry–Howard identity; arbitrary-sequent cut elimination; general Coq/Lean/Agda extraction correctness; a full implemented-System-F parametricity proof; or protocol fidelity/deadlock/liveness/distributed-system correctness.
