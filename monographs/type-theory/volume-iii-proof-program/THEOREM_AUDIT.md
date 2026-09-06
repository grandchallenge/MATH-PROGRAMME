# Volume III Theorem Audit — Stage B

Current scope: `CH-0` implication fragment unless stated otherwise. This is an internal authoring audit, not independent mathematical review.

| ID | Result | Statement scope | Dependencies | Critical cases | Proof status |
|---|---|---|---|---|---|
| T3.1 | Rule-level term assignment | implication-only natural deduction to typed terms | recursive term assignment | assumption, implication introduction, implication elimination | proved in Ch. 1 |
| T3.2 | Weakening | `CH-0` implication fragment | context freshness | binder renaming in `→I` | proved in Ch. 1 |
| T3.3 | Capture-avoiding substitution | `CH-0` implication fragment | T3.2 | variable case; abstraction with freshness/alpha-renaming | proved in Ch. 2 |
| T3.4 | Preservation for principal beta reduction | `CH-0` implication fragment | T3.3 | inversion of application and abstraction typing | proved in Ch. 2 |
| T3.5 | Principal detour/beta correspondence | implication natural deduction under selected term assignment | T3.1, T3.3, T3.4 | discharged-assumption substitution | proved in Ch. 2 |
| T3.6 | Strong normalization | full planned `CH-0` | standard reducibility/logical-relations theorem | arrow reducibility clause; fundamental lemma | cited obligation; full citation and structured proof sketch deferred to development pass |
| T3.7 | Progress/canonical forms | full planned `CH-0` | canonical forms, evaluator semantics | application head cases | planned for Ch. 5/full-core formal closure |

## Audit notes

- Operational reduction `→` is not identified with definitional equality `≡`.
- The deterministic normal-order evaluator is an implementation strategy over the mathematical reduction relation.
- Laboratory traces are evidence for the implementation on retained fixtures; they are not proofs of strong normalization.
- No result in this audit applies automatically to the later classical/control layer `CHC-1` or dependent layer `CHD-1`.
- Full Gate-2 formal closure remains open until all named results in the completed manuscript are reconciled.
