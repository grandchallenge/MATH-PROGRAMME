# PNP-WP00 — Source, Definition, and Equivalence Audit

**Artifact ID:** `PNP-WP00-source-definition-equivalence-audit`  
**Challenge:** P versus NP  
**Campaign:** `PNP-001`  
**Programme lane:** MATHSOLVE  
**Status:** `INTERNAL REVIEW COMPLETE — PROMOTION ELIGIBLE`  
**Version:** 0.1.0  
**Audit date:** 2026-07-24  
**Promotion authority:** Referee  
**Claim class:** `SOURCE-NORMALIZED / NON-SOLUTION ARTIFACT`

---

## 0. Executive disposition

This Work Package fixes the canonical P-versus-NP statement, computational model, encoding conventions, reduction notion, exact equivalences, non-equivalence boundaries, barrier register, and adversarial rejection tests.

The first binding components are:

- `campaigns/p_vs_np/WP00_SOURCE_DEFINITION_EQUIVALENCE/00_CHARTER.md`;
- `campaigns/p_vs_np/WP00_SOURCE_DEFINITION_EQUIVALENCE/02_MACHINE_AND_ENCODING_LOCK.md`.

This artifact does **not** claim:

- `P = NP`;
- `P != NP`;
- a new deterministic polynomial-time algorithm for an NP-complete language;
- a new lower bound against unrestricted computation or circuits;
- a new barrier theorem;
- a new collapse or separation of neighboring complexity classes;
- a novelty result.

It is promotion-eligible as a source, model, and equivalence-control dossier only.

---

## 1. Charter lock

The canonical proposition is

```math
\mathbf P \stackrel{?}{=} \mathbf{NP}.
```

The objects are decision languages over finite strings. The cost measure is deterministic worst-case polynomial time in encoded bit-length. `NP` is defined by polynomially bounded certificates checked by a deterministic polynomial-time verifier.

The programme does not replace this proposition by the informal slogan “easy to check means easy to solve.” The slogan omits:

- decision-language semantics;
- the certificate-length bound;
- deterministic verification;
- worst-case quantification;
- uniformity;
- input encoding;
- bit complexity;
- total halting.

The full binding charter is `PNP-WP00-00-CHARTER`.

## 2. Machine-and-encoding lock

The normative source is Cook’s official Clay formulation using Turing machines. The working algorithmic model is a deterministic multitape Turing machine, admitted through standard polynomial simulation equivalence.

The canonical representation is binary. Input size is the complete encoded bit-length. Parsing, malformed-input handling, memory access, copying, arithmetic, coefficient growth, precision, and output are charged.

The default completeness notion is deterministic polynomial-time many-one reducibility.

The full binding representation contract is `PNP-WP00-02-MACHINE-ENCODING-LOCK`.

---

## 3. Binding source ledger

| ID | Source | Role | Binding use |
|---|---|---|---|
| `SRC-PNP-00` | Stephen Cook, *The P versus NP Problem*, official Clay problem description, <https://www.claymath.org/wp-content/uploads/2022/06/pvsnp.pdf> | Normative theorem statement | Turing-machine model; formal definitions of `P` and verifier-form `NP`; finite alphabets; worst-case polynomial time; polynomial reductions; NP-completeness; search relation; `coNP`; circuit route; relativization and natural-proofs discussion. |
| `SRC-PNP-01` | Clay Mathematics Institute, *P vs NP*, <https://www.claymath.org/millennium/p-vs-np/> | Current institutional status | The problem remains listed as unsolved; public informal orientation. |
| `SRC-PNP-02` | S. A. Cook, “The Complexity of Theorem-Proving Procedures,” STOC 1971, DOI `10.1145/800157.805047` | Completeness foundation | Polynomial reducibility and the satisfiability completeness route. |
| `SRC-PNP-03` | R. M. Karp, “Reducibility Among Combinatorial Problems,” 1972 | Standard many-one completeness | Polynomial many-one reduction discipline and natural NP-complete representatives. |
| `SRC-PNP-04` | T. Baker, J. Gill, R. Solovay, “Relativizations of the P =? NP Question,” *SIAM J. Comput.* 4(4), 1975, DOI `10.1137/0204037` | Barrier source | Oracles relative to which `P = NP` and oracles relative to which `P != NP`. |
| `SRC-PNP-05` | S. Cook, R. Reckhow, “The Relative Efficiency of Propositional Proof Systems,” *J. Symbolic Logic* 44, 1979 | Proof-complexity boundary | Polynomially bounded proof systems and the `NP` versus `coNP` bridge. |
| `SRC-PNP-06` | A. Razborov, S. Rudich, “Natural Proofs,” *JCSS* 55, 1997, DOI `10.1006/jcss.1997.1494` | Conditional barrier source | Constructivity/largeness/usefulness barrier for broad circuit-lower-bound methods under pseudorandomness assumptions. |
| `SRC-PNP-07` | S. Aaronson, A. Wigderson, “Algebrization: A New Barrier in Complexity Theory,” STOC 2008 / *Theory of Computing* | Barrier source | Extension of relativization-style limitations to broad arithmetizing methods. |

### 3.1 Source hierarchy

1. `SRC-PNP-00` fixes the canonical challenge.
2. `SRC-PNP-02` and `SRC-PNP-03` fix the completeness and reduction lineage.
3. `SRC-PNP-04`, `SRC-PNP-06`, and `SRC-PNP-07` constrain proof-method claims.
4. `SRC-PNP-05` fixes the proof-complexity implication boundary.
5. Later literature may update known algorithms, lower bounds, or routes, but cannot silently alter the theorem target.

### 3.2 Temporal status

The challenge is open as of the audit date. Any later claim that it has been solved requires a fresh source and acceptance audit; repository activity never upgrades theorem status.

---

## 4. Class-definition lock

### 4.1 `P`

For a finite alphabet `Sigma`,

```math
\mathbf P
=
\left\{
L\subseteq\Sigma^*:
\exists\text{ deterministic TM }M,\exists k,
L=L(M),
T_M(n)\le n^k+k
\right\}.
```

A decider halts on all strings. Worst-case time is maximized over all strings of length `n`, including malformed encodings.

### 4.2 `NP`

A language `L` lies in `NP` when there exist a polynomial-time relation `R` and a polynomial `p` such that

```math
x\in L
\iff
\exists y\,(|y|\le p(|x|)\land R(x,y)).
```

The nondeterministic-machine and verifier definitions are accepted as equivalent only under the standard polynomial simulation proof.

### 4.3 `coNP`

```math
\mathbf{coNP}
=
\{L:\overline L\in\mathbf{NP}\}.
```

`NP = coNP` is not identified with `P = NP`.

### 4.4 Polynomial-time many-one reduction

```math
A\le_m^p B
```

means there is a total polynomial-time computable function `f` with

```math
x\in A\iff f(x)\in B
```

for all strings `x`.

### 4.5 NP-hard and NP-complete

A language `B` is NP-hard when every `A in NP` satisfies `A <=_m^p B`.

It is NP-complete when it is NP-hard and `B in NP`.

NP-hardness alone does not imply membership in `NP`, decidability, or even a decision-language presentation unless these are separately proved.

---

## 5. Canonical reduction certificates

The reduction certificates in this section are theorem schemas. A later formal or executable package must instantiate all parser, size, and correctness details under the machine-and-encoding lock.

### 5.1 `CIRCUIT-SAT`

**Membership in `NP`.** A certificate is an assignment to input gates. Evaluate the topologically ordered circuit in time polynomial in the complete circuit encoding length.

**NP-hardness route.** For any `L in NP` with verifier `V` and certificate bound `p`, compile the polynomial-time computation of `V(x,y)` for fixed `x` and symbolic `y` into a Boolean circuit `C_x` such that

```math
x\in L
\iff
C_x\text{ is satisfiable}.
```

Required discharge items:

- uniform circuit construction;
- polynomial gate and wiring count;
- polynomial output-encoding length;
- exact simulation of the verifier;
- malformed-input convention.

### 5.2 `SAT`

**Membership in `NP`.** The certificate is a truth assignment; parse and evaluate the formula in polynomial time.

**NP-hardness route.** Convert `CIRCUIT-SAT` to `SAT` by introducing a variable for each gate and local constraints enforcing the gate semantics. The conjunction is satisfiable exactly when the circuit is satisfiable.

A Tseitin-style encoding supplies linear or polynomial size, depending on the selected formula syntax.

Required discharge items:

- gate-basis cases;
- output gate forced true;
- extension of any satisfying input assignment to gate values;
- recovery of a satisfying circuit input from any satisfying formula assignment;
- polynomial total encoding length.

### 5.3 `3-SAT`

**Membership in `NP`.** The certificate is a truth assignment; each clause is checked directly.

**NP-hardness route.** Convert the SAT formula to CNF using a satisfiability-preserving definitional encoding, then replace every clause longer than three literals by a chain of 3-clauses using fresh variables.

For example, a clause

```text
(l1 OR l2 OR ... OR lm),  m > 3
```

may be replaced by

```text
(l1 OR l2 OR z1)
AND (NOT z1 OR l3 OR z2)
AND ...
AND (NOT z_{m-3} OR l_{m-1} OR lm).
```

Required discharge items:

- both directions of equisatisfiability;
- fresh-variable hygiene;
- clauses of size one and two;
- exactly-three versus at-most-three convention;
- linear or polynomial output-size bound.

### 5.4 Reduction implication

For any NP-complete language `K`,

```math
K\in\mathbf P
\Longrightarrow
\mathbf{NP}\subseteq\mathbf P
\Longrightarrow
\mathbf P=\mathbf{NP}.
```

The converse follows because `K in NP`.

---

## 6. Exact equivalence matrix

| Statement | Relation to canonical target | Conditions |
|---|---|---|
| `P = NP` | Canonical target | Locked language model |
| `SAT in P` | Equivalent | `SAT` NP-completeness under `<=_m^p` |
| `3-SAT in P` | Equivalent | Canonical encoding and reduction certificate |
| `CIRCUIT-SAT in P` | Equivalent | Canonical circuit model and reduction certificate |
| Every NP-complete language is in `P` | Equivalent | Standard NP-completeness |
| Some NP-complete language is in `P` | Equivalent | Standard NP-completeness |
| Every polynomially balanced NP search relation has a polynomial-time witness finder | Equivalent | Total output convention; decision-to-search self-reduction through NP prefix languages |
| `SAT notin P` | Equivalent to `P != NP` | `SAT in NP` and NP-complete |
| Some language in `NP` is not in `P` | Equivalent to `P != NP` | Direct class separation |

### 6.1 Search equivalence boundary

If `P = NP`, every polynomially balanced polynomial-time decidable relation admits a polynomial-time search procedure: query whether a witness with a given prefix exists and build the witness bit by bit.

The proof must include:

- polynomial witness length;
- a polynomial number of prefix queries;
- prefix-query languages in `NP`;
- a deterministic decision procedure supplied by `P = NP`;
- final witness verification.

This does not imply that every informal optimization or creative task has a polynomial-time solution; the task must first be represented by a polynomially balanced relation with efficiently decidable validity.

---

## 7. One-way implications and stronger statements

| Statement | Correct relation |
|---|---|
| `NP != coNP` | Implies `P != NP`; not known equivalent |
| Polynomial hierarchy does not collapse | Implies `P != NP`; stronger working statement |
| `NP not subseteq P/poly` | Implies `P != NP`; stronger nonuniform separation |
| An NP-complete language requires superpolynomial unrestricted Boolean circuits | Implies `NP not subseteq P/poly`, hence `P != NP`; stronger target |
| Exponential Time Hypothesis | Implies `P != NP`; much stronger quantitative hypothesis |
| Strong Exponential Time Hypothesis | Implies ETH and `P != NP`; stronger still |
| Existence of standard one-way functions | Implies `P != NP`; converse is not known |
| No polynomially bounded Cook–Reckhow proof system for tautologies | Equivalent to `NP != coNP`, not directly to `P != NP` |
| `VP != VNP` | Algebraic analogue; not a proved equivalent of classical `P != NP` |
| `P_C != NP_C` | Different machine model over `C`; not the classical target |
| `FPT != W[1]` | Parameterized analogue; not a classical equivalence |
| `BPP != NP`, `BQP != NP`, or similar | Distinct class questions |

---

## 8. Non-equivalence boundaries

### 8.1 Decision versus optimization

A polynomial-time algorithm for a bounded decision threshold can sometimes yield an optimizer by binary search and self-reduction. This requires:

- polynomially bounded output length;
- exact objective encoding;
- polynomially many decision queries;
- a reconstruction theorem.

No generic optimization equivalence is presumed.

### 8.2 Worst case versus average case

An algorithm that is polynomial on most inputs, in expectation under a distribution, or on benchmark suites does not place the language in `P`.

A worst-case-to-average-case reduction must identify the distribution, reduction type, success probability, amplification cost, and exact target consequence.

### 8.3 Uniform versus nonuniform

Polynomial-size circuit families place a language in `P/poly`, not necessarily `P`.

Uniform circuit-generation conditions must be stated when transferring circuit constructions to Turing algorithms.

### 8.4 Exact versus approximate

Approximation algorithms, heuristics, relaxations, and probabilistic certificates do not decide an NP-complete language unless the approximation gap and reduction prove exact YES/NO recovery.

### 8.5 Fixed parameter versus input parameter

A polynomial algorithm for each fixed parameter value may have a different exponent or machine for every value. This is not one uniform polynomial-time algorithm when the parameter is part of the input.

### 8.6 Restricted instances

Polynomial algorithms for Horn-SAT, 2-SAT, bounded treewidth, planar subclasses, random instances, sparse instances, or formulas with additional structure do not solve unrestricted SAT without a reduction covering all instances.

### 8.7 Succinct representations

A polynomial algorithm in the expanded object size can be exponential in the succinct input length. Representation-expansion cost is binding.

### 8.8 Proof verification

Polynomial-time verification of a supplied formal proof shows membership in an NP-style relation only when proof length is polynomially bounded. It does not imply polynomial-time proof discovery.

---

## 9. Barrier register

### 9.1 Relativization

Baker, Gill, and Solovay construct oracles `A` and `B` with

```math
\mathbf P^A=\mathbf{NP}^A,
\qquad
\mathbf P^B\ne\mathbf{NP}^B.
```

Therefore a proof technique that relativizes uniformly cannot by itself resolve the unrelativized question.

**Audit question:** does every step remain valid after adding an arbitrary oracle to all machines and reductions?

The barrier does not say diagonalization is useless. It says a fully relativizing diagonalization route cannot decide the target.

### 9.2 Natural proofs

Razborov and Rudich identify a broad class of circuit-lower-bound arguments with constructivity, largeness, and usefulness properties. Under strong pseudorandomness assumptions, such methods cannot prove the required general circuit lower bounds.

**Audit questions:**

- Is the separating property efficiently recognizable from a truth table?
- Does it hold for a large fraction of Boolean functions?
- Does it exclude all small circuits?
- Which cryptographic or pseudorandomness assumption activates the barrier?

This is a conditional barrier to a method class, not an impossibility theorem for all circuit lower bounds.

### 9.3 Algebrization

Aaronson and Wigderson show that many nonrelativizing arithmetization techniques still obey a stronger oracle-style invariance involving low-degree extensions.

**Audit question:** does the proposed argument survive algebraic oracle access in the sense relevant to the barrier?

A route that fails to algebrize may be promising only in the weak negative sense that this barrier does not immediately classify it.

### 9.4 Explicitness gap

Counting proves that almost all Boolean functions need large circuits. It does not identify a specific NP language with the required lower bound.

**Audit question:** where is the explicit language, and how is its truth table or local behavior connected to the lower-bound measure?

### 9.5 Restricted-model trap

Strong lower bounds exist for restricted models. Promotion requires an explicit lifting theorem from the restricted model to all polynomial-time algorithms or unrestricted circuits.

### 9.6 Proof-complexity scope trap

Lower bounds for a named propositional proof system show only that system is weak. Even lower bounds for every Cook–Reckhow proof system target `NP != coNP`, which is sufficient but stronger than `P != NP`.

### 9.7 Hierarchy-theorem misuse

Time hierarchy separates sufficiently different deterministic time bounds. It does not place an NP language outside `P` without resolving the simulation and completeness obstacles.

### 9.8 Self-reference and diagonalization closure debt

A diagonal language may fall outside `NP`, fail to be explicit enough, or defeat only the enumerated machines under a time bound that does not transfer to the target class.

### 9.9 Algorithmic hidden-cost barrier

A proposed SAT solver fails if exponential work is hidden in:

- state count;
- table construction;
- coefficient or integer growth;
- precision;
- recursion-tree width;
- symbolic canonicalization;
- data structure operations;
- preprocessing;
- nonuniform advice;
- an unproved structural lemma.

---

## 10. False-proof atlas seeds

`PNP-WP01` must turn at least the following into explicit adversarial fixtures.

| ID | False-proof pattern | Minimal rejection witness |
|---|---|---|
| `PNP-FP-001` | Greedy SAT assignment chooses a locally best literal | Formula family where every greedy local choice can enter a dead end although another assignment satisfies |
| `PNP-FP-002` | Dynamic program has polynomial depth but exponentially many states | State-count derivation indexed by subsets or partial assignments |
| `PNP-FP-003` | Linear-programming relaxation is integral “in practice” | Fractional optimum or integrality-gap instance |
| `PNP-FP-004` | Branch-and-bound prunes typical instances | Worst-case family forcing an exponential search tree |
| `PNP-FP-005` | Polynomial number of arithmetic operations | Intermediate operands require exponentially many bits |
| `PNP-FP-006` | Analog or real constant encodes the answer | Infinite precision or noncomputable advice exposed |
| `PNP-FP-007` | Neural solver generalizes on benchmarks | Adversarial exact instance and absence of universal correctness proof |
| `PNP-FP-008` | Quantum speedup settles classical `P` | Algorithm lies in `BQP`; no deterministic simulation supplied |
| `PNP-FP-009` | Small circuits imply fast algorithms | Nonuniform family lacks a uniform polynomial-time generator |
| `PNP-FP-010` | Circuit counting proves SAT hard | Counting applies to almost all functions, not the explicit SAT function |
| `PNP-FP-011` | Lower bound for monotone or bounded-depth circuits | General circuits may use excluded gates or depth |
| `PNP-FP-012` | Proof-system lower bound proves `P != NP` | Scope reaches only one proof system or at most `NP != coNP` |
| `PNP-FP-013` | Finite verification establishes asymptotic separation | Unchecked input lengths remain; no inductive theorem |
| `PNP-FP-014` | Unary polynomial algorithm transferred to binary input | Numeric value is exponential in bit-length |
| `PNP-FP-015` | Parameter is “small” | Parameter is unbounded and part of the input |
| `PNP-FP-016` | Average-case hardness equals worst-case hardness | Missing reduction and distributional control |
| `PNP-FP-017` | `NP = coNP` would settle `P = NP` | Logical implication direction is invalid |
| `PNP-FP-018` | `VP != VNP` settles classical P versus NP | Missing model-transfer theorem |

---

## 11. Claim taxonomy

Every descendant claim must use one primary support type.

| Type | Meaning |
|---|---|
| `SRC` | Direct statement from an authoritative source |
| `DEF` | Campaign definition or convention |
| `EQV` | Proved equivalence, both directions and hypotheses explicit |
| `IMP` | Proved one-way implication |
| `RED` | Reduction certificate |
| `ALG` | Algorithm with correctness and resource proof |
| `LB` | Lower bound with exact computational model |
| `BAR` | Barrier classification or theorem |
| `RES` | Restricted-model or restricted-instance result |
| `AVG` | Average-case result |
| `NUM` | Experimental or finite evidence |
| `HEUR` | Heuristic argument |
| `CONJ` | Conjecture or working hypothesis |
| `OPEN` | Named unresolved obligation |

No `NUM`, `HEUR`, `RES`, or `CONJ` claim may be promoted as `ALG`, `LB`, `EQV`, or resolution evidence without a new proof artifact.

---

## 12. Theorem-obligation ledger

### 12.1 Equality lane

| ID | Obligation | Acceptance condition | Status |
|---|---|---|---|
| `PNP-E01` | Exact target language | One canonical NP-complete language and encoding fixed | Locked |
| `PNP-E02` | Algorithm | Finite uniform deterministic machine specified | Open |
| `PNP-E03` | Total correctness | Every binary string handled; YES/NO proof complete | Open |
| `PNP-E04` | Polynomial time | Worst-case bit-complexity proof with all hidden costs charged | Open |
| `PNP-E05` | Completeness bridge | Reduction certificate audited under `<=_m^p` | WP00 schema fixed |
| `PNP-E06` | Resource exclusions | No advice, oracle, randomness, hidden precision, or exponential preprocessing | Open |
| `PNP-E07` | Independent replay | Implementation and proof obligations independently checked | Open |

### 12.2 Separation lane

| ID | Obligation | Acceptance condition | Status |
|---|---|---|---|
| `PNP-S01` | Explicit language | Named language in `NP`, preferably NP-complete | Open |
| `PNP-S02` | Lower-bound model | Bound applies to all deterministic polynomial-time machines, or a stronger model with transfer | Open |
| `PNP-S03` | Quantitative bound | Superpolynomial lower bound in canonical input length | Open |
| `PNP-S04` | Uniformity bridge | Nonuniform lower bound implication stated correctly | Open |
| `PNP-S05` | Barrier profile | Relativization, natural-proofs, and algebrization classification completed | Open |
| `PNP-S06` | Restricted-model escape | No unsupported lifting from a restricted model | Open |
| `PNP-S07` | Explicitness | Counting or generic-function arguments tied to the target language | Open |
| `PNP-S08` | Independent verification | Proof checked against semantic mutation fixtures | Open |

---

## 13. Formalization boundary

`PNP-WP00` authorizes formal work on:

- finite alphabets and binary strings;
- total deterministic machine semantics;
- step-count and worst-case runtime definitions;
- polynomial bounds;
- verifier-form `NP`;
- polynomially balanced relations;
- polynomial-time many-one reductions;
- transitivity and class-closure lemmas;
- the theorem that an NP-complete language in `P` implies `P = NP`;
- abstract search-to-decision under `P = NP`;
- syntax and semantics of Boolean circuits, formulas, CNF, and 3-CNF;
- checked reduction schemas among `CIRCUIT-SAT`, `SAT`, and `3-SAT`;
- semantic mutation tests for encoding and implication drift.

It does not authorize a formal claim of `P = NP`, `P != NP`, unrestricted circuit lower bounds, or completeness until all imported machine and reduction infrastructure is available and checked.

---

## 14. Agent Council review

### Axiomatist

Accepted the finite-string language ontology, classical foundation, total decision semantics, and explicit quantifier order. Rejected informal “problem solving” as the primary object.

### Cartographer

Accepted the dependency route:

```text
charter
-> machine and encoding lock
-> class definitions
-> reduction certificates
-> equivalence matrix
-> non-equivalence boundaries
-> barrier register
-> false-proof atlas
-> theorem-ledger and target selection
```

### Grammarian

Locked `P`, `NP`, `coNP`, `P/poly`, NP-hard, NP-complete, and `<=_m^p` against typographic or semantic substitution. The campaign identifier `PNP` is documentary and must not be confused with the complexity class notation.

### Verifier

Checked implication directions, especially:

- `P = NP -> NP = coNP`;
- `NP != coNP -> P != NP`;
- `NP not subseteq P/poly -> P != NP`;
- circuit lower bounds as a stronger sufficient route;
- proof-complexity scope;
- search-to-decision hypotheses.

### Adversary

Added hidden-cost, representation-expansion, uniformity, restricted-model, average-case, parameter, precision, and empirical-evidence rejection tests.

### Formalist

Restricted initial certification to definitions, reductions, implication logic, and semantic fixtures. No open separation statement is represented as proved.

### Amanuensis

Designated this file as the integrated WP00 authority and the two component locks as binding subordinate artifacts. Later revisions must preserve provenance and explicitly supersede changed clauses.

### Referee

Verdict:

```text
PROMOTION ELIGIBLE AS PNP-WP00
```

This verdict concerns documentary correctness and proof-route hygiene only. It confers no mathematical progress toward either terminal outcome.

---

## 15. Promotion and next-stage gate

`PNP-WP00` may be promoted after repository review and merge when a reviewer confirms:

1. the charter matches the official language formulation;
2. the machine and encoding lock charges all computational resources;
3. `P`, `NP`, reductions, hardness, and completeness are defined without drift;
4. the reduction certificates state both correctness directions and size obligations;
5. exact equivalences are separated from stronger sufficient statements;
6. search, optimization, average-case, random, quantum, nonuniform, parameterized, and algebraic variants remain typed separately;
7. the barrier register does not overstate impossibility;
8. the false-proof seeds cover the principal semantic and resource failures;
9. no claim implies that the problem is solved or close to solution.

After promotion, the next authorized stages are:

- `PNP-WP01` — false-proof atlas and executable semantic mutations;
- `PNP-WP02` — source-normalized theorem, lower-bound, and algorithm ledger.

These may proceed in parallel. Mechanism generation, unrestricted target promotion, large-scale experiments, and novelty claims remain gated until WP01 and WP02 pass review.

---

## 16. Final claim boundary

The strongest supported statement is:

> The MATH-PROGRAMME now has a source-normalized, machine-locked, encoding-explicit, reduction-disciplined, and barrier-aware specification of the classical P-versus-NP problem.

The universal class equality or separation remains open.