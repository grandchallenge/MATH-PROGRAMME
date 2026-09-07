# Claims Ledger — Volume IV: PROTOCOL

This ledger separates proved results, imported results, executable evidence, analogies, and explicit non-results. Status labels are provisional until the corresponding theorem audit and exact candidate evidence are complete.

| ID | Claim | Status | Exact scope | Evidence/source route |
|---|---|---|---|---|
| C4.1 | Finite binary session duality is involutive. | intended theorem | `PROTO-0` finite session types | T4.1, structural induction |
| C4.2 | Linear environment splitting prevents two parallel subprocesses from independently consuming the same endpoint obligation. | intended theorem / formal invariant | `PROTO-0` typing | T4.2 + typing rules |
| C4.3 | A principal send/receive step between dual endpoints advances both process state and session obligations compatibly. | intended theorem | principal `PROTO-0` redex | T4.4–T4.5 |
| C4.4 | Well-typed `PROTO-0` communication does not produce a protocol action mismatch at a principal redex. | intended theorem | closed finite `PROTO-0` | T4.6 |
| C4.5 | A closed finite one-session `PROTO-0` network is either terminated/closing appropriately or can reduce. | intended theorem | exact T4.7 hypotheses only | progress proof |
| C4.6 | Local binary session typing alone does not imply deadlock freedom for arbitrary multi-session networks. | intended counterexample theorem | `PROTO-N1` | T4.8–T4.9 + executable witness |
| C4.7 | Guarded recursive session syntax permits finite unfoldings without constituting a termination or productivity theorem. | intended theorem + boundary | `PROTO-R1` | T4.10–T4.12 |
| C4.8 | Queue well-formedness is preserved by the selected bounded asynchronous semantics. | intended theorem | `PROTO-A1` | T4.13–T4.14 |
| C4.9 | Selected synchronous and asynchronous protocol examples can be related by normalized finite traces. | computed demonstration | named finite examples only | lab08 evidence |
| C4.10 | Finite projectable choreography examples yield compatible local traces under the implemented projection. | theorem per exemplar / computed | bounded acyclic `PROTO-M1` examples | T4.16 + lab09 |
| C4.11 | General multiparty projection correctness is available only through explicitly cited external results whose hypotheses must be preserved. | cited/imported boundary | cited MPST calculus only | bibliography + theorem audit |
| C4.12 | Selected finite synchronous session subtyping rules support safe replacement in the stated fragment. | intended theorem | `PROTO-S1` | T4.18 |
| C4.13 | General asynchronous session subtyping decidability/completeness is not established. | explicit non-result | asynchronous sessions | claim boundary |
| C4.14 | A monitor generated from a finite session type accepts every trace produced by the selected monitored core when observations are complete. | intended theorem | `PROTO-MON1` | T4.20 |
| C4.15 | Runtime monitoring does not establish facts about unobserved events or arbitrary distributed faults. | explicit non-result / counterexample | open systems | T4.21 |
| C4.16 | Session fidelity is distinct from deadlock freedom, lock freedom, starvation freedom, fairness, fault tolerance, and security. | scoped conceptual distinction supported by formal counterexamples | throughout Volume IV | theorem/claims ledger + labs |
| C4.17 | Linear typing of channel endpoints does not by itself establish unique physical ownership in a deployed runtime. | explicit limitation | implementation boundary | architecture analysis |
| C4.18 | Protocol conformance does not imply application-level semantic correctness of payloads. | intended counterexample | finite typed protocol | Chapter 12/14 fixture |
| C4.19 | Session duality is not asserted to be logical negation in general. | explicit non-result / terminology boundary | all calculi | Chapter 2 and Chapter 13 |
| C4.20 | The propositions-as-sessions/processes-as-proofs relationship is calculus-specific and may be exact only under stated translations. | cited/scoped correspondence | Chapter 13 selected systems | primary literature + bounded lab |
| C4.21 | Correct interaction can be intentionally nonterminating. | formal/pedagogical observation | guarded recursive examples | `PROTO-R1` |
| C4.22 | Protocol state alone is insufficient to specify external state mutation, I/O, exceptions, nondeterminism, probability, or other effects. | transition thesis / scope boundary | series transition | Chapter 14; motivates Volume V |

## Claims prohibited without new evidence

The manuscript must not promote any of the following from the present work set without a separately audited theorem/evidence route:

- arbitrary deadlock freedom;
- lock freedom, starvation freedom, fairness, or real-time responsiveness;
- fault tolerance under network or process faults;
- general security guarantees;
- general multiparty realizability/projectability;
- general asynchronous subtyping decidability/completeness;
- semantic equivalence of synchronous and asynchronous models;
- correctness of concrete transport protocols/runtimes;
- application/business semantic correctness from protocol types;
- universal Curry–Howard identity between proofs and processes;
- mathematical certification or external-referee status of the volume before Gate 8.
