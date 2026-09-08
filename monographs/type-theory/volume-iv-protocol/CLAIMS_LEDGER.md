# Volume IV claims ledger

Status: Stage C-E full-composition candidate.

| Claim | Status | Scope / evidence | Excluded inference |
|---|---|---|---|
| Session types record ordered communication obligations | INTERNAL_DEFINITION_AND_EXAMPLES | PROTO-0, Chs. 1-2 | Not arbitrary application meaning |
| Finite duality is involutive | PROVED | T4.1 | Not logical negation in general |
| Linear channel environments split disjointly | PROVED | T4.2 | Not physical/runtime unique ownership |
| Finite synchronous session fidelity | PROVED | T4.5 | Not availability or liveness |
| Communication safety in PROTO-0 | PROVED | T4.6 | Not network fault tolerance |
| Canonical one-session progress | PROVED | T4.7 | Not unrestricted multi-session progress |
| Local binary typing does not imply deadlock freedom | PROVED_BY_COUNTEREXAMPLE | T4.9 / Lab 06 | Counterexample does not refute fidelity |
| Guarded recursion preserves well-formedness under unfolding | PROVED | T4.10 | Not productivity/fairness |
| Bounded FIFO queue invariant and async fidelity | PROVED_IN_DEFINED_FRAGMENT | T4.13-T4.14 | Not universal sync/async equivalence |
| Multiparty projection trace agreement | FINITE_EXEMPLARS_ONLY | T4.16 / Lab 09 | Not general MPST theorem |
| Bounded synchronous subtyping is safe | PROVED_IN_DEFINED_FRAGMENT | T4.18 | Not general async subtyping |
| Finite local monitor is sound for fully observed accepted traces | PROVED | T4.20 | Not completeness for hidden/distributed faults |
| Propositions-as-sessions correspondences exist in cited calculi | EXTERNAL_LITERATURE | Caires-Pfenning; Wadler | Not identity of PROTO-0 with linear logic |
| Protocol fidelity implies fault tolerance | REJECTED_GENERAL_INFERENCE | T4.23 boundary | Requires failure-aware semantics |
| Protocol conformance implies arbitrary application correctness | REJECTED_GENERAL_INFERENCE | T4.24 boundary | Requires application/effect specification |
| “Grand unified theory” | RESEARCH_THESIS | Series framing | Not an established theorem |

The ledger must be read with `THEOREM_AUDIT.md` and `VOLUME_PLAN.md`; prose cannot promote a stronger claim than those artifacts.
