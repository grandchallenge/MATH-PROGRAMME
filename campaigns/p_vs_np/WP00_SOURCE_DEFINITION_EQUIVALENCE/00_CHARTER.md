# PNP-WP00 — Charter

**Artifact ID:** `PNP-WP00-00-CHARTER`  
**Campaign:** `PNP-001`  
**Challenge:** P versus NP  
**Work Package:** `PNP-WP00`  
**Status:** `LOCKED FOR WP00`  
**Version:** 0.1.0  
**Audit date:** 2026-07-24  
**Claim class:** `SOURCE-NORMALIZED / NON-SOLUTION ARTIFACT`

---

## 1. Binding proposition

Determine whether

```math
\mathbf P = \mathbf{NP}.
```

The programme fixes the proposition in the following language form.

Let `Sigma` be a finite alphabet with at least two symbols, and let `Sigma*` be the set of finite strings over `Sigma`.

A language `L subseteq Sigma*` lies in `P` when there exists a deterministic Turing machine `M` and a constant `k` such that:

1. `M` halts on every input `x`;
2. `M` accepts exactly the strings in `L`; and
3. the worst-case running time satisfies

```math
T_M(n) \le n^k + k
```

for every input length `n`.

A language `L subseteq Sigma*` lies in `NP` when there exist a deterministic polynomial-time verifier `V` and a polynomial `p` such that

```math
x \in L
\quad\Longleftrightarrow\quad
\exists y\in\{0,1\}^*,\ |y|\le p(|x|),\ V(x,y)=1.
```

The challenge asks whether every language with polynomially bounded, polynomial-time verifiable certificates also has a deterministic polynomial-time decider.

The inclusion `P subseteq NP` is immediate. The unresolved direction is

```math
\mathbf{NP} \stackrel{?}{\subseteq} \mathbf P.
```

## 2. Normative source authority

The binding problem statement is Stephen Cook, *The P versus NP Problem*, the official Clay Mathematics Institute problem description:

- <https://www.claymath.org/wp-content/uploads/2022/06/pvsnp.pdf>

Current institutional status is taken from:

- <https://www.claymath.org/millennium/p-vs-np/>

Historical and structural sources used by this Work Package include:

- Stephen Cook, “The Complexity of Theorem-Proving Procedures,” STOC 1971, DOI `10.1145/800157.805047`;
- Richard Karp, “Reducibility Among Combinatorial Problems,” 1972;
- Theodore Baker, John Gill, and Robert Solovay, “Relativizations of the P =? NP Question,” *SIAM Journal on Computing* 4(4), 1975, DOI `10.1137/0204037`;
- Stephen Cook and Robert Reckhow, “The Relative Efficiency of Propositional Proof Systems,” *Journal of Symbolic Logic* 44, 1979;
- Alexander Razborov and Steven Rudich, “Natural Proofs,” *Journal of Computer and System Sciences* 55, 1997, DOI `10.1006/jcss.1997.1494`;
- Scott Aaronson and Avi Wigderson, “Algebrization: A New Barrier in Complexity Theory,” STOC 2008; journal version in *ACM Transactions on Computation Theory* 1(1), 2009.

Later literature may refine strategy, known restricted lower bounds, algorithms, or meta-complexity routes. It may not silently change the target proposition.

## 3. Object and quantifier lock

The primary objects are **decision languages over finite strings**.

The theorem quantifies over algorithms, inputs, and input lengths:

```math
L\in\mathbf P
\iff
\exists M\,\exists k\,\forall x\,
\bigl[M(x)\text{ halts and decides }L\bigr]
\land
T_M(|x|)\le |x|^k+k.
```

The `NP` certificate definition quantifies as follows:

```math
L\in\mathbf{NP}
\iff
\exists V\,\exists p\,\forall x\,
\left[
 x\in L
 \iff
 \exists y\,(|y|\le p(|x|)\land V(x,y)=1)
\right].
```

The following are binding:

- running time is worst-case asymptotic time;
- input size is encoded bit-length;
- the algorithm is uniform;
- the machine halts on every input;
- the verifier is deterministic and polynomial-time;
- certificates have polynomially bounded length;
- malformed strings are part of the language model and must be handled in polynomial time;
- polynomial constants and exponents are fixed independently of the input.

## 4. Admissible terminal outcomes

### 4.1 Equality outcome

A valid equality proof may establish that one fixed NP-complete language belongs to `P`, provided the package contains:

1. a fully specified deterministic uniform algorithm;
2. a proof that it decides every encoded instance correctly;
3. a worst-case polynomial bit-complexity bound;
4. an audited reduction certificate showing that the chosen language is NP-complete under the locked reduction notion; and
5. no uncharged advice, preprocessing, precision, oracle, randomness, or parameter dependence.

Canonical representatives are:

- `CIRCUIT-SAT`;
- `SAT`;
- `3-SAT`.

Thus, under the reduction lock,

```math
\mathrm{SAT}\in\mathbf P
\iff
\mathrm{3SAT}\in\mathbf P
\iff
\mathrm{CIRCUIT\text{-}SAT}\in\mathbf P
\iff
\mathbf P=\mathbf{NP}.
```

### 4.2 Separation outcome

A valid separation proof may establish that one NP-complete language is not in `P`:

```math
\mathrm{SAT}\notin\mathbf P
\quad\Longrightarrow\quad
\mathbf P\ne\mathbf{NP}.
```

A lower bound against a restricted algorithm family, circuit family, proof system, parameter range, distribution, or representation is not a terminal separation unless an explicit theorem transfers that lower bound to all deterministic polynomial-time Turing machines.

## 5. Scope exclusions

The following are distinct objects until connected by an explicit theorem:

- function and search classes such as `FP` and `FNP`;
- optimization and approximation problems;
- counting classes such as `#P`;
- promise problems;
- average-case complexity;
- randomized classes such as `BPP` and `RP`;
- quantum classes such as `BQP` and `QMA`;
- nonuniform classes such as `P/poly`;
- parameterized classes such as `FPT` and `W[1]`;
- algebraic models such as `VP` versus `VNP` or `P_C` versus `NP_C`;
- real- or complex-number unit-cost machine models;
- interactive, probabilistic, cryptographic, or heuristic verification notions;
- finite-instance performance and empirical scaling.

These lanes may support strategy. They do not inherit equivalence to the canonical target by resemblance.

## 6. Claim boundary

This charter claims only that the challenge statement, quantifiers, admissible terminal outcomes, and exclusion boundaries have been fixed for `PNP-WP00`.

It does **not** claim:

- `P = NP`;
- `P != NP`;
- a new algorithm for an NP-complete problem;
- a new lower bound;
- a new barrier theorem;
- a collapse or separation of any neighboring complexity classes;
- a novelty result.

## 7. Authorization rule

No proposed proof route may enter mechanism generation or theorem promotion until it states:

1. its machine model;
2. its input encoding and size measure;
3. its uniformity status;
4. its exact target language or class statement;
5. its reduction notion;
6. its worst-case resource bound;
7. any advice, preprocessing, randomness, precision, approximation, or promise assumptions;
8. the barrier profile it is expected to cross; and
9. the exact theorem that connects its local result to `P` versus `NP`.

The companion machine-and-encoding lock is authoritative for items 1–7.