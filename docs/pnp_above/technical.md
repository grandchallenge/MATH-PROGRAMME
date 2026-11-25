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

## WP18: escaping diagonal support without producing hardness

The original source-pinned WP18 construction lets Alice retain the full conditional nine-stage map and Bob use a full-depth unconditional nine-stage singleton-register map. At seed (0,1,0,...,0), the original conditional-linear outputs differ. A kernel-checked source theorem establishes **positive original CL distribution mass on that unequal question pair**, with every native query-interface proof, raw-input halting and verifier runtime bound. The complete original Sampler 9 and Verifier 9 records are formally compiled; the latter has polynomial-bound parameter **145469**.

This **does not** give a value gap. The unchanged original identity decider accepts empty answers on every positive-index question pair. A dimension-one deterministic strategy wins perfectly, and the original synchronous, tensor-product quantum and commuting values are all exactly 1. The support of the newly asymmetric law is also a sparse star centered on the all-zero Alice question when the first seed bit vanishes, plus diagonal pairs when it does not; WP19 now proves the stronger obstruction: **no synchronous predicate on this exact support can produce a quantum advantage at all**.

The two proven no-go results are complementary: WP17 eliminates *predicate-only* changes on a diagonal question law; WP18 eliminates *sampler-only* changes with an always-winning predicate. The next candidate must construct a genuinely coupled sampling/answer-sensitive verification system and **prove** a nonzero original-model game gap. [Source-locked WP18 and detailed limits](evidence.md#wp18-native-asymmetric-nine-stage-cl-sampler-and-second-no-gap-control-18-november-2026).

## WP19: the original WP18 sampler cannot become quantum-hard under any decider

In the original source-native `CL.clDist` model, WP19 proves the exact two-player mapping for each uniformly chosen nine-bit seed `z`:

$$
L^{\mathsf A}(z)=
\begin{cases}
z, & z_0=1, \\
0, & z_0=0,
\end{cases}
\qquad L^{\mathsf B}(z)=z.
$$

Thus the sampled question law has precisely **512 support pairs**, each with probability `1/512`, forming a 256-edge star and 256 isolated diagonal pairs. [The original-source exact probability theorem](https://github.com/grandchallenge/MATHSOLVE/blob/0780909e5a31c8fb7ff882a25b1ccad5bf31dd51/research/PNP-ABOVE/WP19_ExactOriginalQuestionProbability.lean) is proved symbolically for every seed and pair.

The stronger theorem concerns a *general* finite synchronous game supported on such a star and disjoint diagonal matching. Each no-signalling correlation with nonnegative normalized probabilities is bounded by a convex combination of actual dimension-one deterministic strategies: first select a center answer, then optimize each spoke conditionally, and optimize each isolated diagonal separately. Original tensor-product Born probabilities and tracial commuting probabilities satisfy this bound as proved in Lean.

For **every** synchronous replacement predicate `D` on WP18's original question distribution, including predicates with unsatisfiable sampled pairs,

$$
\omega_{\mathrm{sync}}(G_D)
=\omega_{\mathrm{quantum}}(G_D)
=\omega_{\mathrm{commuting}}(G_D).
$$

This equal optimum need **not be one**. The arbitrary replacement predicate is quantified mathematically, not claimed to be a compiled original `Cost.Prog`. Hence WP19 rules out *any decider-only repair of WP18*. A new source-native sampler with interacting two-sided question choices is required before a quantum gap is even possible. The [full theorem statement and scope](evidence.md#wp19-universal-star-support-no-quantum-advantage-19-november-2026) do not claim a hard game, quantum compression or P-versus-NP separation.

## A proved restricted SAT transfer — and its limitation

For finite explicitly tabulated two-prover games, existence of a perfect deterministic classical local strategy is equivalent to satisfiability of an explicitly constructed CNF formula. If SAT is polynomial-time decidable, self-reduction then produces the strategy in polynomial time in the **explicit table size**, with at most one SAT query per Boolean variable plus an initial feasibility query. This establishes a valid restricted classical strategy-extraction transfer.

The magic-square game shows why a perfect entangled strategy does not entail satisfiability of the *classical* strategy CNF. And a succinct compressed verifier may have an exponentially large explicit game table, so this theorem does not give polynomial runtime in the compressed description length.

A further sharp but restricted result says that outputting a uniform m-bit string using at most r fair random bits on the verifier side incurs total variation distance at least $1-2^{r-m}$. This applies to *local output sampling*, not the source's prover-assisted quantum introspection.

The [WP01 erratum and results](wp01_erratum.md) provide proofs, test quantities and exact model restrictions.

## The native decision–search equivalence (WP34–WP38)

Use the original MIPRE source model, with encoded size `esize` and actual `Cost.PolyTimeFun` programs. Fix a compression object $G$, a source universal machine $U$ and a verifier boundedness parameter $\lambda$ satisfying WP34's explicit boundedness hypothesis. Define $D$ as existence of a total source-polynomial solver correct on encoded formulas; $C$ as existence of a total source-polynomial solver of the valid compressed promise; $W$ as existence of a total source-polynomial witness program correct on all satisfiable formulas; and $L$ as the analogous canonical witness program.

WP34 and WP38B establish

$$
C \iff D \iff W \iff L.
$$

For valid indices the original input is the binary formula index $k$, above the fixed threshold, with the compressed verifier interpreting SAT by perfect PCC completeness and unsatisfiability by quantum value at most $1/2$. This is not a decision claim for arbitrary numeric indices. PCC is the source strategy condition, not an efficient deterministic local strategy. The verifier bound polynomial in the *numeric* index $k$ is not automatically polynomial in the binary index length. WP31 exposes this encoding barrier; WP32–WP35 control padding, variable scope and dense support.

For a fixed formula $f$, let $S(f)$ be WP35's ordered list of distinct active identifiers, and $R(f,b)$ its verified dense witness relation. The precise search proposition is

$$
W=\exists A\in\mathrm{PTF}\ \forall f,\quad
\mathrm{SAT}(f)\Longrightarrow R(f,A(f)).
$$

Here PTF denotes original native polynomial-time functions, not abstract oracle access. The relation is sound on all inputs and complete with a witness of length $|S(f)|\leq f.\mathrm{size}$. WP38A constructs a source program that successively tests $f_j\land x_j$ and then sets $f_{j+1}=f_j\land x_j$ on YES, or $f_j\land\neg x_j$ on NO. On a satisfiable prefix this preserves feasibility; the resulting bits form the lexicographically greatest restriction of a satisfying assignment to the ordered identifiers. Each fold step increases encoded state size by at most $\mathrm{esize}(i)+27$ for identifier $i$. The original fold combinator provides an actual polynomial execution certificate. WP38B composes this with the support scanner and constructs the reverse decision program by total source parsing and verified witness evaluation. No correctness condition is imposed on witness outputs for unsatisfiable inputs, but total polynomial runtime is required there too.

The exact theorems `valid_promise_iff_witness`, `valid_promise_iff_canonical` and their negated forms are in [WP38B](https://github.com/grandchallenge/MATHSOLVE/pull/1298); [WP38A](https://github.com/grandchallenge/MATHSOLVE/pull/1297) proves the greedy compiler, lexicographic property and parser. This is standard self-reducibility formalized with actual native runtime accounting, not a novel general complexity separation.

## What the lower bounds actually establish

WP36A–B prove a worst-case quadratic lower bound over fixed correct native programs on genuine valid-index instances with empty variable support. It arises from the native charged-copy representation. WP37 proves a support-width obstruction for binary semantic refutations: for a complete ordered-pair parity construction on $N$ vertices, every refutation in the specified system must exceed width $\lfloor N/3\rfloor^2$ for $N\geq3$. Arbitrary predicates are allowed on lines; inference arity and support are restricted. Adding the parity equations gives an algebraic shortcut. Neither result excludes polynomial-time algorithms of arbitrary degree and form.

## Open obligations (24 November 2026)

The negated equivalence $\neg C\iff\neg W\iff\neg L$ gives a search-side target. Prove that every total polynomial-time native candidate fails to produce a satisfying witness on some satisfiable formula, or equivalently exclude every total polynomial-time canonical witness constructor. One may seek a hard satisfiable subfamily; restricting to unique witnesses is a research choice, not a proved equivalence with the general unique-SAT promise. Non-affinity and logical expansion alone are not hardness proofs. Any proposed measure must control unrestricted algorithmic transformations, not only a prescribed proof calculus or greedy search.

General SAT-to-classical *strategy resource* transfer and a superpolynomial bound remain open. The restricted decision equivalence does not turn quantum-state rank into classical runtime. The full effective numerical compressor execution and printed theorem discrepancy are separate from the abstract source promise results. The PNP-001 standard-machine, NP-verifier and endpoint concordance remains a separate incomplete lane, with later reverse-simulation progress. Relevant relativization, natural-proofs and algebrization barriers must be respected.

**P versus NP remains open.** Continue to the [source coverage](coverage.md) and [evidence ledger](evidence.md).
