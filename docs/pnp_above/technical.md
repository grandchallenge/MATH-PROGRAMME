# Technical spine: theorem interfaces and classical transfer

<p class="page-deck">The precise mathematical meaning, assumptions, and limitations of the MIP*-motivated PNP-ABOVE programme.</p>

!!! warning "Mathematical provenance"
    The compression theorem is externally established mathematics, not a GCL theorem. The finite emulator is a bounded GCL construction, not a reimplementation of the paper's compression procedure. No SAT lower-bound claim follows without an additional transfer theorem.

## The classical target

PNP-001 concerns uniformly encoded binary decision languages. SAT is NP-complete under polynomial-time many-one reductions, and the main target is deciding whether $\mathsf P=\mathsf{NP}$.

An unrestricted proof must respect the parent's [machine and encoding lock](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/campaigns/p_vs_np/WP00_SOURCE_DEFINITION_EQUIVALENCE/02_MACHINE_AND_ENCODING_LOCK.md). The existing formal-statement concordance obligation remains open.

## What the source theorem actually measures

For a nonlocal game $G$ and winning threshold $\nu$, Definition 5.12 of Ji et al., [arXiv:2001.04383v4](https://arxiv.org/pdf/2001.04383v4), introduces

$$
\mathcal E(G,\nu)=
\min\{\text{Schmidt rank of a qualifying finite-dimensional strategy winning with probability at least }\nu\}.
$$

The value is taken to be infinity when no such strategy exists.

The objects being counted are quantum-state components across a bipartition. This resource is **not** circuit size, deterministic Turing running time, NP witness size, or a lower bound on a language's decision complexity.

## Theorem 12.1: gap-preserving compression

Given a verifier $V=(S,D)$ and positive integer $\lambda$, the published compression constructor produces a nine-level normal-form verifier $V^{\mathrm{compr}}$ with sampler and decider time polynomial in the compressed index $n$ and in $\lambda$.

For its substantive completeness and soundness conclusions, the *input verifier* must also be nine-level normal form and $\lambda$-bounded, and $n\ge C_0$ for a universal threshold specified existentially by the theorem.

Writing $N=2^n$, the theorem transfers existence of a perfect PCC strategy and establishes

$$
\mathcal E(V_n^{\mathrm{compr}},1/2)\geq
\frac12\max\left\{
\mathcal E(V_N,1/2),\,
2^{N^\lambda-1}
\right\}.
$$

Here PCC denotes the source's projective, consistent and commuting strategy condition. The bound says nothing by itself about a polynomial-time SAT decider or a polynomial-size Boolean circuit family. It should not be interpreted as a game-value algorithm for arbitrary explicitly described games.

## Construction stages and resource bounds

The proof builds the compressor using the following published transformations:

| Transformation | Verifier level | Sampler time | Decider time |
| --- | ---: | --- | --- |
| Introspection (Thm. 8.3) | 5 | Polynomial in $n,\lambda$ | Polynomial in $2^{n\lambda}$ |
| Answer reduction (Thm. 10.30) | 7 | Polynomial in $n,\lambda$ | Polynomial in $n,\lambda$ |
| Anchored repetition (Thm. 11.4) | 9 | Polynomial in $n,\lambda$ | Polynomial in $n,\lambda$ |

The [protected WP00 symbolic ledger](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/PNP-ABOVE/WP00_COMPRESSION_PARAMETER_LEDGER.md) records the parameters $a_1,a_2,b_1,b_2,\sigma,\mu,\tau,C_0$ and the source equation chain (182)–(192).

Two exact leading-error substitutions are

$$
a_1(\lambda n)^{a_1}\epsilon_1^{b_1}=\frac18
$$

and

$$
\sigma^{a_2}(\lambda n)^{a_2\mu}\epsilon_2^{b_2}=\frac{\epsilon_1}{3}.
$$

Their algebraic verification does not independently establish the three published transformation theorems. The ledger does not supply certified numerical values for all universal constants.

## First finite calibration: magic square

Alice must return an even-parity row of a $3\times3$ array; Bob must return a column of the specified parity, odd only in the final column. Their entries at the intersection must agree.

A deterministic strategy winning every pair would assign all nine bits consistently, contradicting the parity sum. Every deterministic classical strategy therefore loses at least one of nine uniform pairs, and the bound is attained:

$$
\omega_{\rm C}=\frac89.
$$

The standard entangled Pauli-observable strategy wins perfectly, giving $\omega_{\rm Q}=1$. Yet the global parity system is an efficiently decidable linear system over $\mathbb F_2$. This is an elementary counterexample to interpreting a quantum–classical *strategy gap* as a classical *decision lower bound*.

Source: [finite calibration record](https://github.com/grandchallenge/MATHSOLVE/pull/1137).

## Second finite calibration: an explicit nine-level input

Let $W=\mathbb F_2^9$ and let each player's conditionally linear function be $L(z)=z$, decomposed into the nine coordinate factors. For each $z\in W$, the sampler emits the diagonal pair $(z,z)$ with probability $2^{-9}$. The finite source-level emulator checks all 512 vectors, both players and all nine stages. The decider accepts valid questions exactly when each answer is empty.

This input has a perfect rank-one PCC strategy. For any faithful encoded implementation satisfying the source theorem's input promises, the compressed family $G_n$ obeys the conditional theorem-derived bound

$$
\mathcal E(G_n,1/2)\geq 2^{2^{\lambda n}-2}
\qquad(n\ge C_0).
$$

Now define the *unary indexed* language

$$
L_G=\{1^n:\operatorname{val}^{*}(G_n)=1\}.
$$

The source completeness clause ensures every sufficiently large unary index is positive. Thus $L_G$ is cofinite and lies in $\mathsf P$ (a finite exception table can be hardcoded existentially). This is **not** a uniform algorithm for deciding game value from arbitrary game encodings. It does not provide an effective numerical $C_0$ or execute the full compressor.

Source: [protected input note](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/PNP-ABOVE/WP00_NINE_LEVEL_INPUT_AND_TRANSFER.md) and [Python emulator](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/PNP-ABOVE/WP00_NINE_LEVEL_INPUT_EMULATOR.py).

## The missing lower-bound transfer

Define an actual classical cost invariant $\mathcal C_{\mathcal A}(G_n)$, including the allowed strategy class $\mathcal A$, randomness, uniformity, communication, circuit representation, promises and errors.

To prove P differs from NP using an independently established lower bound, one must also establish an implication of the form

$$
\operatorname{SAT}\in\mathsf P
\quad\Longrightarrow\quad
\mathcal C_{\mathcal A}(G_n)\leq n^{O(1)}
$$

with exact construction and overhead accounting. No such transfer is presently proved. A Schmidt-rank bound cannot be inserted in place of a classical strategy cost without demonstrating how a putative SAT solver produces a forbidden strategy.

The required additional audit includes relativization, natural proofs and algebrization, with their precise hypotheses. Neither quantum entanglement nor self-reference automatically bypasses those barriers.

## Exact next obligations

1. Produce the paper-faithful encoded Turing machines for the nine-level input and establish their worst-case step and description-length bounds.
2. Determine the source-effective numerical values of $\lambda$ and $C_0$, or isolate the exact nonconstructive obstacle.
3. Identify a nontrivial *classical* finite game-cost invariant and a corresponding ordinary classical decision predicate.
4. Prove a restricted lower bound or furnish a counterexample; do not extrapolate from sampled game sizes.
5. Formulate and test a uniform classical transfer lemma with explicit SAT reduction and strategy-construction directions.

**What remains open:** the classical bridge and P versus NP itself. Continue to [Evidence and status](evidence.md).
