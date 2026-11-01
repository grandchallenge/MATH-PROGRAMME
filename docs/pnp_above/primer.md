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

## What would count as progress?

The programme's missing bridge is a new, explicitly **classical** cost measure together with a proof that a hypothetical polynomial-time SAT solver would produce a cheap implementation of the measured structure. Only then could a matching classical lower bound lead toward P versus NP.

An equally useful outcome would be a rigorous counterexample showing that a proposed transfer cannot work. Such negative results eliminate false routes before they become alleged proofs.

For exact definitions and equations see the [technical spine](technical.md). For source identities, evidence grades and open work, see [evidence](evidence.md). For the scholarly paper see the [preprint record](preprint.md).
