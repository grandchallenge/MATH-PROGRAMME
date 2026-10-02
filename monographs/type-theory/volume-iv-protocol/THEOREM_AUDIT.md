# Volume IV theorem audit

Status: full-composition candidate; independent mathematical review pending.

| ID | Statement | Exact scope | Status | Evidence / location |
|---|---|---|---|---|
| T4.1 | Finite duality involution | PROTO-0 finite sessions | PROVED | Ch. 2; choice cases completed Ch. 4 |
| T4.2 | Disjoint linear splitting | finite channel environments | PROVED | Ch. 2; reused Ch. 5 |
| T4.3 | Payload substitution | first-order payload layer | PROVED | Ch. 3 |
| T4.4 | Principal communication compatibility | send/receive, select/branch, close/wait | PROVED | Chs. 3-4 |
| T4.5 | Subject reduction / session fidelity | finite synchronous PROTO-0 | PROVED | Ch. 5 |
| T4.6 | Communication safety | closed well-typed PROTO-0 principal redexes | PROVED | Ch. 5 |
| T4.7 | Single-session progress | closed canonical one-session sequential networks | PROVED | Ch. 6 |
| T4.8 | Unrestricted multi-session progress | PROTO-N1 | NON_RESULT | Refuted by T4.9 witness |
| T4.9 | Local typing does not imply deadlock freedom | closed two-session PROTO-N1 witness | PROVED_BY_COUNTEREXAMPLE | Ch. 6; Lab 06 |
| T4.10 | Guarded unfolding preserves well-formedness | PROTO-R1 guarded session types | PROVED | Ch. 7 |
| T4.11 | One-step recursive preservation | bounded one-unfolding PROTO-R1 step | PROVED | Ch. 7 |
| T4.12 | General productivity / lock freedom | recursive sessions | NON_RESULT | Explicitly unclaimed |
| T4.13 | Finite asynchronous queue invariant | bounded FIFO PROTO-A1 | PROVED | Ch. 8; Lab 08 |
| T4.14 | Bounded asynchronous fidelity | bounded FIFO PROTO-A1 | PROVED | Ch. 8 |
| T4.15 | Universal sync/async trace equivalence | general | NON_RESULT | Selected examples only |
| T4.16 | Projection trace preservation | registered finite PROTO-M1 exemplars | EXHAUSTIVE_FINITE_EVIDENCE | Ch. 9; Lab 09 |
| T4.17 | General multiparty projection correctness | general MPST | LITERATURE_DEPENDENT | Cite exact external theorem; not re-proved |
| T4.18 | Bounded synchronous session subtyping safety | finite PROTO-S1; invariant payloads | PROVED | Ch. 10; Lab 10 |
| T4.19 | General asynchronous subtyping decidability/completeness | general | NON_RESULT | Explicitly excluded |
| T4.20 | Monitor soundness for observed finite traces | PROTO-MON1 full local observation | PROVED | Ch. 12; Lab 12 |
| T4.21 | Monitor completeness for distributed failures | general | NON_RESULT | Observation boundary explicit |
| T4.22 | Selected structural congruence preserves typing | PROTO-0 selected laws | PROVED | Ch. 5 |
| T4.23 | Fidelity implies fault tolerance | deployment faults | NON_RESULT | Counterexample boundary Ch. 11 |
| T4.24 | Protocol conformance implies application correctness | application semantics | NON_RESULT | Counterexample boundary Chs. 11, 14 |

## Audit conclusion

The positive theorem set is intentionally finite and local. The negative rows are first-class scope controls, not unfinished positive theorems. No row grants external review qualification or publication authority.
