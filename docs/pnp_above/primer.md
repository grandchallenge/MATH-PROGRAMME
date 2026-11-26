# Reader's primer: verifying is not computing

<p class="page-deck">An introduction to the mathematical motivation of PNP-ABOVE, suitable for readers without graduate training in complexity theory or quantum information.</p>

## A puzzle, a certificate, and a decision

Imagine assembling a jigsaw puzzle. Checking a completed picture can be much easier than finding the correct placement of pieces. For a Boolean satisfiability problem, a proposed assignment of true or false values is easy to check: evaluate each clause. But nobody knows whether there is a polynomial-time algorithm that always decides whether a satisfying assignment exists.

The classes $\mathsf P$ and $\mathsf{NP}$ formalize this distinction for decision problems on finite strings. A problem is in $\mathsf P$ if a deterministic algorithm decides it in polynomial time. It is in $\mathsf{NP}$ if every yes instance has a polynomial-length classical certificate verifiable in polynomial time. The question is whether the two classes coincide.

**Important:** an apparent difficulty in finding an answer is not a mathematical proof of hardness.

## A referee who can ask questions

In an interactive proof, an efficient referee interrogates one or more much more powerful provers. Two provers can be prevented from communicating after receiving their questions. The verifier can therefore ask related questions and test whether the responses fit one consistent account.

The referee's computational cost can be small even though the mathematical object being checked is enormous. But the computational resources of the provers remain part of the model.

With classical noncommunicating provers, the resulting language class is $\mathsf{MIP}=\mathsf{NEXP}$. With entangled quantum provers the class is $\mathsf{MIP}^{*}$. Ji and collaborators proved the remarkable result

$$
\mathsf{MIP}^{*}=\mathsf{RE}.
$$

The class $\mathsf{RE}$ contains languages whose positive instances can eventually be recognized, even when negative inputs might never halt. The theorem does **not** say a polynomial-time classical algorithm can solve undecidable problems. Instead it characterizes what an efficient verifier can test in this enlarged interaction model.

## A tiny description of a huge verifier

The source proof uses recursive verification compression. An informal analogy is an audit of an immense archive: instead of reading every page, a referee asks precise consistency questions that collectively enforce a complicated condition.

The published construction takes a verifier indexed by a huge parameter $N=2^n$ and constructs a smaller indexed verification description at $n$. It uses three distinct steps: introspection, answer reduction and parallel repetition. These preserve carefully quantified completeness and soundness properties, but do not magically execute the enormous underlying computation in polynomial time.

The distinction matters:

- **Verification compression:** the checks can be represented efficiently.
- **Computational compression:** the answer itself can be computed efficiently.

The first does not imply the second.

## What an entanglement lower bound measures

Theorem 12.1 uses a measure denoted $\mathcal E(G,\nu)$: the minimum Schmidt rank of a shared bipartite quantum state allowing a strategy to win a game with probability at least $\nu$. Informally, Schmidt rank measures the independent paired components required by the entangled state.

It is not an NP certificate length. It is not a Boolean circuit size. It is not the running time of a SAT solver.

The theorem can force this quantum strategy resource to grow fantastically quickly. That does not by itself establish classical decision hardness.

## The magic-square calibration

Consider a $3\times3$ grid of bits. Require all three row parities to be even; require the first two column parities to be even and the third odd. No single classical grid satisfies all conditions, because summing the row equations gives even total parity and summing the column equations gives odd total parity.

In a game where separate provers receive a row and column, the best classical noncommunicating strategy wins eight of nine equally likely pairs:

$$
\omega_{\mathrm{classical}}=\frac89.
$$

Quantum provers sharing entanglement can win every round:

$$
\omega_{\mathrm{entangled}}=1.
$$

This is a genuine quantum advantage. Yet deciding the underlying classical parity system is easy with Gaussian elimination over the two-element field. Therefore a gap in *game-winning ability* does not automatically establish a hard *decision problem*. This finite example is documented in [MATHSOLVE PR #1137](https://github.com/grandchallenge/MATHSOLVE/pull/1137).

## The nine-level finite input

GCL's WP00 work also constructs an input verifier with nine binary coordinates. Its sampler is the identity on $\mathbb F_2^9$, and the question pairs have uniform support on the 512 diagonal pairs $(z,z)$. The decider accepts two empty answers, so the input game has a trivial perfect strategy.

The [finite emulator](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/PNP-ABOVE/WP00_NINE_LEVEL_INPUT_EMULATOR.py) checks the nine-level identities and all 512 vectors. It is not the full published compression program.

For a properly encoded input satisfying the published theorem's hypotheses, the compressed family has an enormous entanglement-rank lower bound and also has a perfect strategy for every sufficiently large index. The set of positive unary indices is therefore **cofinite**, so it belongs to $\mathsf P$ in the standard complexity-theoretic sense. This existence statement does not supply the numerical threshold or the finite exceptional membership table.

Again, deciding a selected indexed proposition can be easy even when successfully performing the corresponding interactive task requires an enormous resource.

## Why diagonal and star-shaped question patterns cannot give quantum advantage

The more recent GCL formalization provides a useful negative lesson. Imagine a referee who **always gives both provers exactly the same question**. For a *synchronous* game, they win on that question only when they give the same acceptable answer. If a winning answer exists, the provers can agree in advance what to return for each question. Sharing entanglement cannot improve that best possible response. If no acceptable answer exists for a sampled question, neither classical nor quantum provers can win it.

WP16 proves that the current nine-stage conditional reference sampler **really does send identical questions**. WP17 then proves in the original MIP* formal game model that for *every* finite synchronous game supported only on equal questions, the best deterministic, tensor-product quantum and commuting strategies have **the same winning probability**. This remains true when some questions are impossible to answer correctly. It does not imply that all quantum games are classically easy: the magic-square game above deliberately sends the two players different, related questions and has a real quantum advantage.

Consequently simply modifying the verifier's acceptance test while leaving that **diagonal** sampler unchanged cannot create the required quantum/classical value gap. WP18 has now built and proved an original source-native non-diagonal two-player sampler, so that first necessary condition is no longer missing. But the **old referee still accepts empty answers to every question**. Changing the questions alone also does not help: the optimal classical, quantum and commuting winning probabilities remain one.

An intuition is that handing two students different exam questions does not make the exam difficult if every question is marked correct when the students leave their answer sheets blank. For genuine quantum advantage, the *questions and the consistency checks on their answers* must jointly create a classical impossibility that quantum resources can overcome. WP19 now **proves those limitations**, not merely suspects them. Imagine the referee always giving Alice one central question, while Bob may receive one of 256 different leaf questions. The players can agree in advance on Alice's answer and independently choose Bob's optimal reply for each leaf. The other 256 question pairs involve separate identical questions and can likewise be answered independently. There is no network of mutually competing consistency checks that might give quantum correlations an advantage. The original source proof shows that this reasoning holds for **every synchronous acceptance rule**, even if some questions are impossible to win. Therefore a new *joint question distribution* is required; changing only WP18's marking rules cannot work. At WP19 a hard game had not been established. The WP20–WP22 successor closes that particular construction obstacle, not the P-versus-NP question. See the [source coverage](coverage.md) and [proof grades](evidence.md).

## From knowing that a solution exists to finding it

Suppose a machine can answer, quickly and correctly, whether any Boolean formula has a satisfying assignment. Could we use it to find an actual assignment? Yes. This is the standard **self-reducibility of SAT**, now implemented and formally verified in our native source model by [WP38A](https://github.com/grandchallenge/MATHSOLVE/pull/1297) and [WP38B](https://github.com/grandchallenge/MATHSOLVE/pull/1298).

Try this small puzzle with three switches, ordered $x,y,z$:

$$
(x\lor y)\land(\neg x\lor z)\land(\neg y\lor\neg z).
$$

Ask whether each proposed choice can still be completed into a solution. Prefer 1 whenever possible.

| Question asked | Answer | Choice retained |
| --- | --- | --- |
| Can the puzzle be solved with $x=1$? | Yes | $x=1$ |
| With $x=1$, can $y=1$ also work? | No | $y=0$ |
| With $x=1,y=0$, can $z=1$ work? | Yes | $z=1$ |

The resulting assignment $(1,0,1)$ satisfies all three clauses. It is also the lexicographically greatest solution in the chosen order: the other solution is $(0,1,0)$. Each answer preserves the existence of a completion. There is no need to explore a failed subtree.

For a formula with $d$ distinct occurring variables, this procedure needs only $d$ feasibility questions on a satisfiable input (counting logical queries, not low-level calls of the implementation). Each adds just one constraint to the running formula. The verified source implementation also controls actual storage and execution costs, including binary variable names. WP35 ensures that only occurring variables need be represented.

The converse is equally important. Suppose a fast program finds a satisfying assignment whenever one exists. Run it and check the returned assignment. On a satisfiable formula the check must succeed; on an unsatisfiable formula no assignment can pass. The search program must still halt within its polynomial time bound on *all* inputs, but its output need not be meaningful on unsatisfiable ones.

Thus a fast SAT decision algorithm exists exactly when a fast witness constructor exists (and exactly when a fast canonical witness constructor exists). A canonical witness means the largest bit string in a fixed variable order, not a solution invariant under every possible relabelling.

## Why complicated relationships are not yet a lower bound

Imagine a network of switches joined by parity rules. Each rule says whether an even or odd number of nearby switches must be on. If the constraints overlap extensively, a proof that combines two statements at a time may have to keep track of many switches simultaneously. [WP37](https://github.com/grandchallenge/MATHSOLVE/pull/1293) proves such a width lower bound for an explicit family, even when each proof line is allowed to be an arbitrary Boolean predicate.

But an ordinary computer can add parity equations modulo two. In that same family, adding all the equations exposes the contradiction. Gaussian elimination solves general linear parity systems in polynomial time. A large proof width is therefore not a large running time for every algorithm.

The important distinction is between ruling out a particular way of reasoning and ruling out every possible way of computing. WP36 likewise proves a quadratic native input-access cost; its hard inputs have no active variables. That is a real theorem about the representation, not the intrinsic difficulty of solving interconnected logical constraints.

## What would count as progress now?

The earlier WP19 sampler obstruction was overcome by later source constructions. WP34–WP35 establish the precise restricted native compressed-promise/SAT decision equivalence and short dense witnesses; WP38 adds the exact search equivalence. The conditional compressor promises have a genuine SAT interpretation. They do not themselves force a classical solver to use the quantum strategy or pay its entanglement cost.

The remaining target is to prove that no total deterministic polynomial-time algorithm can always construct a satisfying assignment on satisfiable formulas. We may concentrate on that positive-input obligation, without asking the constructor to explain why an impossible puzzle has no solution. We must nevertheless cover arbitrary algorithms, not only the illustrative greedy procedure, brute-force enumeration, local search or a narrow proof system.

Nonlinear constraints and uniquely solvable puzzles are possible research specimens, not established hard families. Uniqueness alone proves no hardness; an efficient algorithm for just the unique-solution promise is not known to imply a general deterministic SAT solver. A superpolynomial lower bound for a subfamily of satisfiable formulas would suffice if it genuinely excludes all relevant polynomial-time witness constructors.

**What has changed:** a source-verified, equivalent search-side target is available. **What has not changed:** the unrestricted lower bound, the separate standard-machine concordance and the P-versus-NP question remain open.

For exact definitions and equations see the [technical spine](technical.md). For source identities, evidence grades and open work, see [evidence](evidence.md). For the scholarly paper see the [preprint record](preprint.md).

## Structural Capacity Calculus: why relationships resist compression

**Status (25 November 2026): exploratory, not certified.** [SCC-001 live research tracker](https://github.com/grandchallenge/MATHSOLVE/issues/1309). The [evidence register](evidence.md) remains the authority for admitted PNP-ABOVE claims.

Imagine two rows of eight switches. All 64 cross-row pairings can be realized jointly by one multiplication of the two row parities:

$$
F=\left(\sum_i x_i\right)\left(\sum_j y_j\right).
$$

Contrast the eight independent pairings:

$$
G=\sum_i x_i y_i.
$$

Over the binary field, with affine operations free, the first takes one multiplication and the second exactly eight. For the lower bound, restrict one affine operand of each successive gate to a constant on the current affine subspace. Each gate costs at most one dimension; the final output is affine on the remaining subspace. The inner product has a nondegenerate polar form in 16 dimensions, so such a subspace has dimension at most eight. This covers arbitrary nonlinear intermediate reuse. More relationships can therefore mean less work.

**Research question:** Can we discover a conservation law for logical structure that every classical computation must obey?

### A calculus of reuse

In the Boolean function ring over the binary field on $n$ input bits, let $V$ contain the input coordinates and constant one. A charged multiplication adds $g=uv$ for $u,v\in V$, producing $V'=V+\langle g\rangle$. This is the unrestricted multiplicative-complexity model. Polynomial-size Boolean circuits and polynomial multiplicative complexity agree up to polynomial overhead. A superpolynomial bound for total encoded SAT would imply NP is not contained in P/poly, stronger than P versus NP.

Let $F_r$ be the span of products of at most $r$ elements of $V$, with $F_0$ the constants and negative grades zero. Write $A_r=F_r/F_{r-1}$ and use primes for the new state.

**Candidate theorem (author proof):** for $r\geq1$,

$$
F'_r=F_r+gF_{r-1}.
$$

Expansion proves this identity: all positive powers of $g$ equal $g$. The reverse inclusion follows from the definition. In particular, $F_r\subseteq F'_r\subseteq F_{r+1}$.

Let $q$ be the symbol of $g$ in $A_2$. The identity map induces an exact sequence:

$$
0\longrightarrow qA_{r-2}\longrightarrow A_r
\longrightarrow A'_r\longrightarrow qA_{r-1}
\longrightarrow 0.
$$

The kernel is $F'_{r-1}/F_{r-1}=qA_{r-2}$, and the cokernel is $F'_r/F_r=qA_{r-1}$. Set $H_r=\dim A_r$ and $R_j=\dim(qA_j)$. Then

$$
H'_r=H_r-R_{r-2}+R_{r-1}.
$$

A target of relative degree $d\geq1$ drops one degree exactly when its leading symbol lies in $qA_{d-2}$. It cannot drop further in one step. A family of leading symbols in degree $d$ is jointly promoted exactly when its span lies in that same image.

### Why counting promoted relationships fails

At the initial affine state, the graded algebra is the exterior algebra on the coordinate symbols, whose squares vanish. For the one gate $g=x_1x_2$, multiplication by its symbol maps each monomial avoiding those two coordinates to a distinct monomial containing both, and annihilates the others. For $n\geq2$,

$$
R_j=\binom{n-2}{j}.
$$

Exactly $2^{n-2}$ independent monomial directions move down one degree. With three input bits there are two such directions; with ten there are 256. All share the same computed factor. Counting these directions without accounting for reuse cannot yield a polynomial one-gate capacity bound.

### Evidence and next step

The theorem route is Boolean semantics, filtration update, graded exact sequence, joint symbol promotion, then the open conservation law. The carrier is finite Boolean functions with ordinary finite-dimensional linear algebra; no additional foundational axioms are needed.

Support: direct author proof and finite regression of 720 transitions, 3,168 grade checks and 71,640 target checks. These cover every ordered affine operand pair for one through three inputs and 64 seeded six-gate histories on four inputs. This is not formal verification or novelty certification. Replay-source preservation, specialist audit and Lean checking remain debt.

The next bounded task is to preserve the replay and formalize the exact sequence, then test joint leading-symbol subspaces against all decomposable $q$ and subsequent reuse. The missing result is an independently characterized target-specific potential with polynomial change per gate and superpolynomial demand on SAT. The restricted PNP-ABOVE transfer and standard-machine concordance remain open. Follow the [SCC-001 tracker](https://github.com/grandchallenge/MATHSOLVE/issues/1309).
