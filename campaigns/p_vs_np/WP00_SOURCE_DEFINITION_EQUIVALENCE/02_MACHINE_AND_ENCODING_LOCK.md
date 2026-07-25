# PNP-WP00 — Machine and Encoding Lock

**Artifact ID:** `PNP-WP00-02-MACHINE-ENCODING-LOCK`  
**Campaign:** `PNP-001`  
**Challenge:** P versus NP  
**Work Package:** `PNP-WP00`  
**Status:** `LOCKED FOR WP00`  
**Version:** 0.1.0  
**Audit date:** 2026-07-24  
**Claim class:** `MODEL-AND-REPRESENTATION CONTROL / NON-SOLUTION ARTIFACT`

---

## 1. Purpose

Complexity claims are statements about a computational model acting on an encoded object. A proof that suppresses either component can hide the entire cost of the computation.

This document fixes the canonical machine, uniformity, cost, encoding, and malformed-input conventions for `PNP-WP00` and all descendant work unless a later artifact proves an explicit polynomial-equivalence bridge.

## 2. Canonical machine model

### 2.1 Normative model

The normative definition follows Cook’s official Clay problem description: deterministic and nondeterministic Turing machines operating on finite strings.

### 2.2 Working baseline

For implementation-level descriptions, the programme uses a deterministic multitape Turing machine with:

- a read-only input tape;
- finitely many work tapes;
- a finite tape alphabet;
- one transition per machine step;
- a designated accepting state and rejecting state; and
- mandatory halting on every input for a decider.

This working model is admitted because standard single-tape and multitape Turing machines simulate one another with polynomial overhead. The class `P` is therefore unchanged.

A proposed proof may use another standard model only when the package states and proves, or cites and instantiates, a polynomial-time simulation into the locked model.

## 3. Uniformity lock

Algorithms are uniform finite descriptions.

The following are not available unless explicitly introduced and charged:

- one independently chosen circuit or algorithm for each input length;
- arbitrary advice strings;
- an infinite table of precomputed answers;
- a noncomputable real constant encoding answers;
- an oracle;
- preprocessing depending on the eventual input rather than only on a fixed public problem specification.

A circuit-family argument must distinguish:

```text
uniform polynomial-time computation
from
nonuniform polynomial-size circuit computation (P/poly).
```

The implication `P subseteq P/poly` is available. The converse is not.

## 4. Cost model

### 4.1 Primary measure

The primary resource is the number of Turing-machine steps in the worst case over all strings of encoded length `n`.

A polynomial-time claim must have the form

```math
\exists k,c,n_0\;\forall n\ge n_0\;\forall x\in\{0,1\}^n,
\quad T_M(x)\le c n^k.
```

Equivalent harmless variants such as `n^k+k` are accepted.

### 4.2 Bit complexity

Arithmetic cost is bit cost.

For integers, rationals, finite-field elements, algebraic data, probabilities, weights, and coefficients, the package must track:

- representation length;
- growth of intermediate values;
- cost of arithmetic operations as a function of operand length;
- cost of comparisons and zero tests;
- cost of copying, indexing, and memory addressing when not constant in the Turing model.

A unit-cost arithmetic model does not establish membership in `P` without a polynomial simulation and polynomial bounds on word or coefficient size.

### 4.3 Precision

Approximate numerical computation must state:

- precision requested;
- rounding model;
- conditioning or separation assumptions;
- number of bits required for a correct decision;
- cost of obtaining those bits.

An algorithm whose required precision can grow exponentially has not been shown polynomial-time merely because it uses polynomially many arithmetic operations.

### 4.4 Randomness and quantum computation

Random and quantum operations are not part of the locked deterministic model.

A randomized or quantum algorithm may be studied in a neighboring lane, but it proves `L in P` only after a deterministic polynomial-time simulation or derandomization theorem with all hypotheses discharged.

## 5. Alphabet and canonical binary coding

The normative source allows any fixed finite alphabet of size at least two. The programme canonicalizes all inputs to binary strings.

For every admitted problem representation there must be polynomial-time maps

```math
\operatorname{enc}:\mathcal I\to\{0,1\}^*,
\qquad
\operatorname{dec}:\{0,1\}^*\to \mathcal I\cup\{\bot\},
```

such that:

1. `dec(enc(I)) = I`;
2. well-formedness is decidable in polynomial time;
3. encoding and decoding are polynomial-time;
4. equivalent standard encodings have polynomially related lengths; and
5. no semantic information is stored in an uncharged external naming convention.

The size of an instance is

```math
|I| := |\operatorname{enc}(I)|.
```

## 6. Malformed-input convention

A decision language is defined on all binary strings.

For each canonical problem:

```text
malformed encoding -> NO
```

unless the language definition explicitly chooses a different total convention.

The parser and well-formedness check are part of the running time.

A promise that inputs are well formed may simplify exposition but cannot remove the need for a total polynomial-time decider when making a claim about `P` or `NP` as language classes.

## 7. Numeric encoding lock

Integers are encoded in signed binary with a self-delimiting length convention when concatenated.

Consequences:

- an integer of magnitude `N` contributes `Theta(log(N+1))` bits;
- iterating `N` times is exponential in the input length when `N` is given in binary;
- changing binary input to unary changes the problem and must be recorded as a distinct language;
- pseudo-polynomial running time is not polynomial in the locked bit-length unless the numeric magnitudes are polynomially bounded by the encoded length.

## 8. Boolean formula encoding

A propositional formula is encoded as a syntax tree or a topologically ordered syntax DAG with:

- gate or connective tags from a fixed alphabet;
- variable identifiers encoded as binary integers;
- explicit child references;
- an explicit output node;
- a polynomial-time acyclicity and reference-range check.

The canonical `SAT` language contains exactly the encodings of well-formed satisfiable propositional formulas.

Formula size counts the complete binary representation, including variable identifiers, gate tags, separators, and pointers.

Claims that transform formulas must bound the full output encoding length, not only the number of logical connectives.

## 9. CNF and 3-CNF encoding

A CNF instance contains:

- a declared variable count;
- an ordered list of clauses;
- each literal represented by a sign bit and variable identifier;
- self-delimiting clause boundaries.

For `3-SAT`, each clause contains at most three literals under the canonical convention. Exactly-three-literal variants are polynomially interreducible but must state their padding convention.

Duplicate literals, tautological clauses, repeated clauses, and unused variables are permitted unless a restricted language explicitly excludes them.

The input length includes all literal occurrences and identifier bits.

## 10. Boolean circuit encoding

A Boolean circuit is encoded as a topologically ordered finite acyclic directed graph with:

- input nodes;
- constant nodes when admitted;
- gates from a fixed finite basis, canonically `{AND, OR, NOT}` with fan-in at most two except for `NOT`;
- binary child indices pointing to earlier nodes;
- one designated output gate.

The canonical `CIRCUIT-SAT` language contains encodings of circuits for which some Boolean assignment to the input nodes makes the output gate `1`.

Circuit size is the length of the complete encoding. Gate count may be used as a secondary measure only after proving polynomial equivalence to encoding length for the representation in use.

Unbounded fan-in, threshold, arithmetic, oracle, real-weight, or nonstandard gates define different circuit models and require separate transfer theorems.

## 11. Certificate encoding

A certificate is a binary string `y` whose length is bounded by a fixed polynomial in `|x|`.

The verifier receives the pair `(x,y)` through a self-delimiting pairing function with polynomial-time encode/decode and length

```math
|\langle x,y\rangle| = O(|x|+|y|+\log|x|+\log|y|).
```

The verifier must reject malformed pairs and malformed certificates in polynomial time.

A certificate may not be:

- exponentially long;
- accessible only through a succinct object whose expansion is exponential unless the verifier operates on that succinct representation in polynomial time;
- a real number requiring unbounded precision;
- an interactive transcript unless reduced to the locked static certificate model;
- an advice string shared across inputs without being included and charged.

## 12. Reduction lock

The default completeness reduction is a deterministic polynomial-time many-one reduction.

For languages `A` and `B`,

```math
A \le_m^p B
```

means that there exists a total deterministic polynomial-time function `f` such that

```math
x\in A \iff f(x)\in B
```

for every binary string `x`.

The reduction package must prove:

1. totality on malformed as well as well-formed strings;
2. polynomial running time in `|x|`;
3. polynomial output length;
4. YES/NO preservation in both directions; and
5. compatibility with the canonical encodings.

Polynomial-time Turing reductions, randomized reductions, nonuniform reductions, approximation-preserving reductions, parameterized reductions, and promise-preserving reductions are separately typed and may not be substituted silently.

## 13. Preprocessing and parameter lock

Preprocessing is charged unless it depends only on a fixed finite public specification and has constant description size.

For a parameterized algorithm with running time

```math
f(k)\,n^c,
```

membership in `P` follows only when `k` is fixed as part of the language definition or when `f(k)` is polynomially bounded in the total encoded input length.

A proof for every fixed `k` is not automatically one uniform polynomial-time algorithm when `k` is part of the input.

## 14. Output and search accounting

The canonical target is decision. Search procedures must include the cost of writing their output.

A search-to-decision reduction is accepted only when:

- the witness length is polynomially bounded;
- each query is to the locked decision language or a proved polynomial-time equivalent language;
- the number and size of queries are polynomial;
- malformed and NO instances are handled;
- the constructed witness is checked before return.

## 15. Representation-change gate

A later artifact may introduce a new representation only by supplying a representation certificate with:

| Field | Required content |
|---|---|
| Source representation | Exact syntax and size measure |
| Target representation | Exact syntax and size measure |
| Forward map | Total polynomial-time encoder |
| Reverse or semantic map | Decoder or equivalence theorem |
| Size bound | Explicit polynomial relation |
| Correctness | Preservation of language membership |
| Hidden resources | Advice, randomness, precision, oracle, preprocessing |
| Scope | Exact languages and malformed-input convention covered |

Without this certificate, complexity statements remain representation-local.

## 16. Rejection tests

A proposed polynomial-time algorithm is rejected at WP00 review if any of the following occurs:

1. it measures time in the numeric value of a binary input rather than its bit-length;
2. it assumes constant-cost arithmetic on exponentially long operands;
3. it stores exponentially many states under a symbolic label without polynomial-time operations on that label;
4. it uses an exponentially large precomputed table;
5. it fixes a parameter separately for every input family without one uniform machine;
6. it proves expected or average running time but claims worst-case `P` membership;
7. it uses randomness or quantum operations without deterministic simulation;
8. it omits parsing, copying, output, or precision costs;
9. it changes the formula, circuit, graph, or numeric encoding without a size-preserving bridge;
10. it solves a promise version while claiming a total language result;
11. it gives a polynomial number of operations whose operands have uncontrolled bit-length;
12. it relies on a heuristic, learned model, SAT solver, or empirical benchmark as an asymptotic proof.

## 17. Claim boundary

This lock establishes the model under which later algorithmic and lower-bound claims will be judged. It does not establish any new upper bound, lower bound, completeness theorem, class collapse, or class separation.