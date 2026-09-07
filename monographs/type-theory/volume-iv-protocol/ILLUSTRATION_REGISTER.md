# Illustration Register — Volume IV: PROTOCOL

Status at Gate 0: conceptual register complete; plates are not yet rendered. Every plate carries one primary pedagogical burden and an explicit scope/analogy limit.

| Plate | Working title | Pedagogical burden | Scope / analogy limit | Gate-1? |
|---:|---|---|---|:---:|
| 1 | Closed function, open conversation | show why interaction changes the computational object | not all computation is purely closed or purely interactive | yes |
| 2 | A protocol is a typed state machine | session type as ordered obligations | finite synchronous fragment only | yes |
| 3 | Two ends, complementary actions | action-by-action duality | duality is not logical negation in general | yes |
| 4 | A handshake consumes obligations | process reduction synchronized with environment evolution | one step does not prove liveness | yes |
| 5 | Linear splitting of channel authority | disjoint endpoint obligations across parallel subprocesses | formal linearity is not physical uniqueness | yes |
| 6 | Safe but stuck | well-typed cyclic wait | refutes unrestricted progress, not fidelity | yes |
| 7 | Send then continue | continuation state advances after transfer | payload meaning remains separate | no |
| 8 | Branching is asymmetric choice | distinguish selection from offered branching | labels alone do not give global correctness | no |
| 9 | The environment is a protocol frontier | explain `Δ` as current obligations | not a runtime socket table | no |
| 10 | Dropping an endpoint leaves an obligation unpaid | linear weakening failure | accounting metaphor only | no |
| 11 | Duplicating an endpoint forks one promise | linear contraction failure | shared channels need another calculus | no |
| 12 | Local safety versus global waiting | mismatch graph versus wait-for graph | one liveness abstraction only | no |
| 13 | Guarded recursion folds a conversation | finite recursive syntax, unbounded unfolding | not a scheduling/productivity theorem | no |
| 14 | Unfolding is not running forever correctly | guardedness versus productivity | neither implies fairness | no |
| 15 | Handshake versus queue | synchronous vs asynchronous step shape | no universal trace equivalence | no |
| 16 | Messages become state | queue contents enter configuration | FIFO is assumed | no |
| 17 | An orphan message | expose queue/lifecycle failure mode | diagnostic variant only | no |
| 18 | Queue growth changes the proof burden | bounded versus unbounded queue state | resource exhaustion outside pure fidelity | no |
| 19 | A choreography seen globally | finite global interaction description | not a deployed orchestrator | no |
| 20 | Projection gives each role a local view | choreography-to-local projection | requires projectability | no |
| 21 | Pairwise sensible can still be globally impossible | global inconsistency despite local views | finite witness only | no |
| 22 | Branch knowledge must reach the right roles | multiparty choice propagation | no general theorem implied | no |
| 23 | Subtyping as safe replacement | replacement intuition under formal relation | synchronous finite fragment only | no |
| 24 | Offer more, select less | branch-width variance intuition | exact rules control, not slogan | no |
| 25 | Behavioral refinement is not syntactic inclusion | distinguish relation from syntax | semantic/syntactic subtyping may differ | no |
| 26 | Network faults live outside `PROTO-0` | make failure model boundary visible | types can model faults in other calculi | no |
| 27 | A perfect protocol over a broken transport | show transport assumptions matter | deliberately changes semantics | no |
| 28 | Timing adds another dimension | order versus deadlines | timed session theory not developed fully | no |
| 29 | Security is another obligation plane | separate order from auth/confidentiality | no security theorem inferred | no |
| 30 | Monitor as automaton | finite session to observer | observation boundary is explicit | no |
| 31 | Static proof and runtime observation | typing versus monitoring | neither generally subsumes the other | no |
| 32 | An unobservable violation | accepted trace with wrong semantics | finite boundary witness | no |
| 33 | Session fidelity triangle | process step / environment step / typing commute | represents T4.5 only | no |
| 34 | Progress hypothesis map | additional hypotheses for stronger liveness | implication arrows only where justified | no |
| 35 | Deadlock, lock freedom, starvation, fairness | separate four temporal notions | examples, not equivalence theorem | no |
| 36 | One syntax, several semantics | synchronous/asynchronous/monitored readings | not automatically equivalent | no |
| 37 | Processes and proofs: a disciplined correspondence | selected linear-logic/process alignment | calculus-specific | no |
| 38 | Cut as channel composition, with conditions | structural relation between cut and connection | no unrestricted identity | no |
| 39 | Protocol state is not world state | channel obligations versus external state | prepares Volume V | no |
| 40 | A protocol-conforming semantic bug | right type/order, wrong meaning | application invariants separate | no |
| 41 | From conversation to effect | external event beyond protocol state | effect calculus deferred | no |
| 42 | Series atlas IV | locate Volume IV in ten-volume argument | organizational, not evidentiary | no |

## Visual production rules

- Use the shared `gclplate` and `gcllabel` styles.
- No semantic dependence on color.
- Inspect grayscale and manuscript-scale placement.
- Route connectors before moving or shrinking text.
- Computed state graphs and trace diagrams retain producing scripts/data under `labs/` or `evidence/`.
