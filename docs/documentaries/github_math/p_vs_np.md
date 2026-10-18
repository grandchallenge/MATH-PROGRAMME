# The Shape of Computational Truth

**Source status:** Open Millennium Prize Problem · PNP-001 · No solution claimed.

> **GitHub equation reader; automatically generated from the original manuscript.**
> The [illustrated documentary](../p_vs_np.md) has the canonical layout, figures and reader controls.
> This is not independent mathematical or publication certification.

A note to the reader

## How to Read the Machine

Complexity theory asks not merely whether a problem can be solved, but how resources grow with encoded input length. The labyrinths and gates in this edition are metaphors. Machine models, encodings, reduction direction, worst-case quantifiers, and uniformity govern the mathematics.

**Edition status:**

Open Millennium Prize Problem; machine-normalized documentary; no algorithm or lower-bound claim.

**Open problem**

Determine whether every language in $\mathsf{NP}$ is in $\mathsf{P}$. Since $\mathsf{P}\subseteq\mathsf{NP}$, the question is whether the inclusion is equality.

**Claim boundary**

A fast heuristic, a quantum speedup, a restricted lower bound, an oracle separation, or success on a finite benchmark does not settle the uniform worst-case machine-level question.

> **Plate I.** Plate I Finding and checking Pedagogical orientation only. The verifier definition governs the claim. [Illustration](../../assets/documentaries/p_vs_np/verification.svg). *Alt text:* A maze contrasts discovering a path with rapidly verifying a supplied path certificate.

Chapter I

## Finding and Checking

A supplied Sudoku grid, Hamiltonian cycle, or satisfying assignment may be rapidly checked even when discovering it appears difficult.

**Definition**

A language $L$ lies in $\mathsf{NP}$ when a polynomial-time verifier $V$ and polynomial $p$ satisfy: $x\in L$ exactly when some certificate $y$, with $|y|\le p(|x|)$, has $V(x,y)=1$.

**Established inclusion**

$\mathsf{P}\subseteq\mathsf{NP}$: a deterministic polynomial-time algorithm supplies a verifier that simply runs the algorithm.

Chapter II

## The Classes P and NP

$$
\mathsf{P}\subseteq\mathsf{NP},\qquad \mathsf{P}\stackrel{?}{=}\mathsf{NP}.
$$

Polynomial time is robust across standard reasonable machine models only after encoding costs and uniformity are fixed. Unary and binary encodings can assign radically different input lengths to the same numerical value.

**Encoding guardrail**

An algorithm polynomial in a numerical magnitude may be exponential in its bit length. Every complexity claim must state the representation and count the resources used to read, transform, and verify it.

> **Plate II.** Plate II The grammar of reduction Pedagogical orientation only. Reduction direction is theorem-critical. [Illustration](../../assets/documentaries/p_vs_np/reduction.svg). *Alt text:* Directed gateways map one decision problem into another while preserving yes and no instances.

Chapter III

## Reductions Preserve Difficulty

A polynomial-time many-one reduction satisfies $x\in A\Longleftrightarrow f(x)\in B$. If $A\le_p B$, an efficient solver for $B$ yields one for $A$; the direction cannot be reversed by rhetoric.

**Definition**

A language is NP-hard when every language in $\mathsf{NP}$ reduces to it. It is NP-complete when it is NP-hard and itself belongs to $\mathsf{NP}$.

> **Plate III.** Plate III The complete problems Pedagogical orientation only. Exact reduction chains govern completeness. [Illustration](../../assets/documentaries/p_vs_np/complete.svg). *Alt text:* SAT sits at a hub linked to graph, scheduling, routing, and packing problems by polynomial reductions.

Chapter IV

## The Complete Problems

**Imported established theorem · Cook–Levin**

Boolean satisfiability is NP-complete. A polynomial-time algorithm for SAT would place every language in $\mathsf{NP}$ inside $\mathsf{P}$.

Computation tableaux encode accepting machine histories as Boolean formulas. Thousands of graph, scheduling, routing, packing, algebraic, and logical problems are complete through explicit reduction chains. Decision, search, optimization, and counting remain distinct contracts unless an interreduction is proved.

> **Plate IV.** Plate IV The walls around the frontier Pedagogical orientation only. Barriers constrain technique families; they do not settle the problem. [Illustration](../../assets/documentaries/p_vs_np/barriers.svg). *Alt text:* Relativization, natural proofs, and algebrization form distinct barriers around the unresolved central question.

Chapter V

## The Frontier and Its Barriers

### Relativization

Oracles exist relative to which P equals NP and others relative to which they differ.

### Natural proofs

Broad constructive circuit arguments conflict with strong pseudorandom functions.

≠

### Algebrization

Even arithmetized relativizing methods meet oracle-style limits.

### Meaning

These are barriers to methods, not evidence of undecidability.

Quantum computation, interactive proofs, PCPs, approximation, parameterization, and average-case theory reveal nearby structure without deciding equality.

A reduction is a bridge of obligation: solve the destination, and every source problem may cross.

Technical appendix A

## Machines, Encodings, and Clocks

A deterministic Turing machine decides a language in polynomial time when its worst-case step count is $n^{O(1)}$. A nondeterministic machine accepts if at least one polynomially bounded branch accepts. The verifier and nondeterministic definitions of NP are equivalent. Uniformity excludes an unrelated advice circuit for each input length.

Technical appendix B

## Decision, Search, Optimization, and Counting

Self-reduction recovers a SAT witness from polynomially many decision queries. This theorem does not automatically transfer to every search problem. Approximation changes the output contract; a heuristic or approximation ratio is not an exact polynomial-time algorithm for the NP-complete decision problem.

Technical appendix C

## Circuits and Proof Complexity

Strong lower bounds are known for restricted circuits and proof systems. The unrestricted lower bounds needed for P versus NP remain open. Cryptographic consequences are conditional: P = NP would undermine standard one-way-function assumptions, while P ≠ NP alone does not guarantee secure cryptography.

Technical appendix D

## Claim-Level Trust Matrix

| Claim | Trust class | Qualification |
| --- | --- | --- |
| $\mathsf{P}\subseteq\mathsf{NP}$ | established | direct verifier construction |
| SAT is NP-complete | imported established | Cook–Levin |
| Restricted circuit/proof lower bounds | established in model | no unrestricted separation |
| Relativization, natural proofs, algebrization | imported established | barriers to method families |
| P = NP or P ≠ NP | open | neither direction proved |
| Quantum advantage | model-specific | no known NP-complete polynomial-time algorithm |
| AI benchmark success | empirical | not worst-case classification |
| Illuminated plates | pedagogical | never authoritative machine proofs |

**Final claim boundary**

This edition supplies no new algorithm, reduction, circuit lower bound, proof-system lower bound, oracle theorem, or cryptographic construction that settles P versus NP.

Sources and programme crosswalk

## Governing literature and campaign record

[Clay Mathematics Institute: P versus NP](https://www.claymath.org/millennium/p-vs-np/).

[Stephen Cook, official problem description](https://www.claymath.org/wp-content/uploads/2022/06/pvsnp.pdf).

[Cook–Levin foundations](https://doi.org/10.1145/800157.805047).

[Baker, Gill, and Solovay: relativization](https://doi.org/10.1137/0204037).

[Razborov and Rudich: natural proofs](https://doi.org/10.1145/237814.237866).

[Aaronson and Wigderson: algebrization](https://doi.org/10.1145/780542.780545).

Programme links: [Domain 07](../../domains/p_vs_np/) · [claim-authority record](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/PNP-WP00-source-definition-equivalence-audit.md) · [campaign artifacts](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/p_vs_np) · [review records](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/reviews/p_vs_np)

## Edition record

This browser-native edition uses the immutable Poincaré reference contract and shared open-problem status vocabulary. Native SVG diagrams are pedagogical; semantic HTML carries the machine definitions and reductions.

The committed pointer is a source record; the checksum-locked complete illustrated source bundle is the authoritative source artifact. MathJax 3.2.2 is a version-pinned network enhancement, and the source TeX remains present when unavailable.

**Web claim boundary:** Browser-native, source-normalized exposition of the machine-and-encoding question P versus NP. Fast heuristics, finite experiments, average-case success, quantum algorithms, oracle separations, special-case algorithms, restricted circuit lower bounds, and proof-complexity results are not promoted to P = NP or P ≠ NP.

[Web-edition data](../p_vs_np.edition.json)[Reusable schema](../documentary_web.schema.json)[Source record](../sources/the_shape_of_computational_truth.tex)[Artifact manifest](../ARTIFACT_MANIFEST.json)

Rendered PDF

19,050,413 bytes ·

`2bde341f24383dbaa66c326488bc01355990a8c676f7a5ac2e518905b75097a9`

·

`metadata_only`

Complete LaTeX source

66,883 bytes ·

`166497cf0b5b4dfc8124c002b6dd510816779907864df0611328a8172ab9729f`

·

`metadata_only`

Authoritative complete illustrated source bundle

37,547,668 bytes ·

`f7afac36f2381738bd6b850519df151f48a9c2983a7e8fcee78c2442ff2c5a2a`

·

`metadata_only`
