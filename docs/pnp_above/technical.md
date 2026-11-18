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

For its substantive completeness and soundness conclusions, the *input verifier* must also be nine-level normal form and bounded by the parameter $\lambda$, and $n\ge C_0$ for a universal threshold specified existentially by the theorem.

Writing $N=2^n$, the theorem transfers existence of a perfect PCC strategy. A **source-level discrepancy** affects the stated quantitative factor. The printed **statement** of Theorem 12.1 gives

$$
\mathcal E(V_n^{\mathrm{compr}},1/2)\geq
\max\left\{
\frac12\mathcal E(V_N,1/2),\,
2^{N^\lambda-1}
\right\}.
$$

But Table 2 and the displayed conclusion of the **proof** on printed page 189 yield only

$$
\mathcal E(V_n^{\mathrm{compr}},1/2)\geq
\frac12\max\left\{
\mathcal E(V_N,1/2),\,
2^{N^\lambda-1}
\right\}.
$$

The earlier edition incorrectly labelled the proof-backed form the exact theorem statement. We use the weaker inequality conservatively, pending reconciliation of the factor of two in the second branch. [Read the dated source erratum and WP01 findings](wp01_erratum.md).

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
L_G=\{1^n:\mathrm{val}^{*}(G_n)=1\}.
$$

The source completeness clause ensures every sufficiently large unary index is positive. Thus $L_G$ is cofinite and lies in $\mathsf P$ (a finite exception table can be hardcoded existentially). This is **not** a uniform algorithm for deciding game value from arbitrary game encodings. It does not provide an effective numerical $C_0$ or execute the full compressor.

Source: [protected input note](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/PNP-ABOVE/WP00_NINE_LEVEL_INPUT_AND_TRANSFER.md) and [Python emulator](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/PNP-ABOVE/WP00_NINE_LEVEL_INPUT_EMULATOR.py).

## Original-source nine-level verifier and unconditional diagonal no-gap

By 18 November 2026, WP08–WP14 had gone beyond the original finite emulator: the source-native `MIPRE.Cost.Prog` identity decider, an interpreter soundness/completeness chain, a typed parser theorem, and an actual original `Verifier 9` with bounded conditional stages were replayed with their pinned upstream. These are **real source-native formal results**, not a completed quantum compressor.

However, the paired source sampler is of the form `(L(z),L(z))`, so its question law has **zero off-diagonal mass**. The WP15 actual game accepts fixed empty answers, yielding exact value 1 across the original synchronous, tensor-product quantum and commuting models. WP16 proves the diagonal distribution directly from original `MIPRE.CL.clDist`. WP17 proves a stronger general theorem: for *any* original finite synchronous game with nonempty answers and diagonal-only question support, define

$$
m(G)=\sum_x \mu(x,x)\,\mathbf{1}[\exists a,\ D(x,x,a,a)].
$$

Then the original model's three optimal values satisfy

$$
\omega_{\mathrm{sync}}(G)=\omega_{\mathrm{quantum}}(G)=\omega_{\mathrm{commuting}}(G)=m(G).
$$

The common value may be **below one** when some sampled diagonals are unwinnable. This is proved by an original one-dimensional question-dependent deterministic strategy attaining `m(G)` and separate native Born-rule and commuting-tracial upper bounds. It does **not** assert that arbitrary non-synchronous games have equal values, nor that the next sampler/decider or a positive gap has been built. It proves that **changing only the decision predicate with WP14's question law cannot create a quantum advantage**.

See [WP17 source/receipts](coverage.md#status-of-the-source-native-theorem-chain), the [evidence register](evidence.md) and the original-source [MATHSOLVE proof](https://github.com/grandchallenge/MATHSOLVE/blob/d741a85572cd99a1f8e206d1211543ef72445da2/research/PNP-ABOVE/WP17_UnconditionalDiagonalNoGap.lean).

## A proved restricted SAT transfer — and its limitation

For finite explicitly tabulated two-prover games, existence of a perfect deterministic classical local strategy is equivalent to satisfiability of an explicitly constructed CNF formula. If SAT is polynomial-time decidable, self-reduction then produces the strategy in polynomial time in the **explicit table size**, with at most one SAT query per Boolean variable plus an initial feasibility query. This establishes a valid restricted classical strategy-extraction transfer.

The magic-square game shows why a perfect entangled strategy does not entail satisfiability of the *classical* strategy CNF. And a succinct compressed verifier may have an exponentially large explicit game table, so this theorem does not give polynomial runtime in the compressed description length.

A further sharp but restricted result says that outputting a uniform m-bit string using at most r fair random bits on the verifier side incurs total variation distance at least $1-2^{r-m}$. This applies to *local output sampling*, not the source's prover-assisted quantum introspection.

The [WP01 erratum and results](wp01_erratum.md) provide proofs, test quantities and exact model restrictions.

## The missing lower-bound transfer

Define an actual classical cost invariant $\mathcal C_{\mathcal A}(G_n)$, including the allowed strategy class $\mathcal A$, randomness, uniformity, communication, circuit representation, promises and errors.

To prove P differs from NP using an independently established lower bound, one must also establish an implication of the form

$$
\mathrm{SAT}\in\mathsf P
\quad\Longrightarrow\quad
\mathcal C_{\mathcal A}(G_n)\leq n^{O(1)}
$$

with exact construction and overhead accounting. No such transfer is presently proved. A Schmidt-rank bound cannot be inserted in place of a classical strategy cost without demonstrating how a putative SAT solver produces a forbidden strategy.

The required additional audit includes relativization, natural proofs and algebrization, with their precise hypotheses. Neither quantum entanglement nor self-reference automatically bypasses those barriers.

## Exact next obligations (updated 18 November 2026)

1. Construct a **source-native, non-diagonal/player-asymmetric conditional-linear sampler** with genuine positive probability on unequal questions, all original query-interface conditions and uniform source execution/size bounds. The existing shared-map reference is mathematically incapable of giving the target value gap.
2. Implement an **answer-sensitive executable original `Cost.Prog` decider**, establish its typed-input/malformed-data semantics and worst-case source bounds, and prove a bounded `Verifier` for the new sampled game.
3. Prove a quantitative, nonzero **quantum/classical value or soundness gap** using the original source strategy models and independent upper/lower bounds; source compilation or positive off-diagonal mass alone does not suffice.
4. Only after that, execute the positive-parameter introspection, answer-reduction and repetition stages on an evidenced input, quantify `\lambda` and `C_0`, and resolve Theorem 12.1's printed statement/proof discrepancy.
5. Independently establish or refute the **uniform succinct SAT-to-classical-resource transfer** with fixed machine/encoding, or expose a counterexample. Keep the separate PNP-001 Formal Conjectures model, NP-verifier and endpoint bridges open.

**What remains open:** the hard-game gap, source-effective full compressor, general classical transfer and P versus NP itself. Continue to [GCL documentary coverage](coverage.md) and [Evidence and status](evidence.md).
