# CSM-G2-XOR — sharp one-dimensional overlap obstruction from an iid source

**Programme:** CSM-001. **Status:** independently reconstructed proof candidate and exact-rational finite-cylinder tests; mathematical result **KNOWN / NOT NOVEL** by Kari–Taati Example 32; GCL internal proof review and independent replay remain open. **Do not describe as an original theorem, mathematically certified, or externally validated.** This is distinct from the positive **single-site channel** preservation reconstruction in [G2 positive-channel certificate](G2_POSITIVE_CHANNEL_CERTIFICATE_20261123.md).

## Statement

Let $(X_i)_{i\in\mathbb Z}$ be independent Bernoulli random variables with common parameter $0<p<1$. Let the deterministic translation-equivariant, overlapping, two-site block transformation be

$$
Y_i=X_i\oplus X_{i+1},
$$

where addition is modulo two. Denote the observed stationary measure on binary configurations by $\nu_p$.

**Proposition, proof candidate:**

1. For every $p$, $\nu_p$ is translation invariant, has full support on the binary full shift, and is **one-dependent**: variables indexed by two sets at separation at least two are independent.
2. At $p=1/2$, $\nu_p$ is exactly the independent fair Bernoulli product measure and hence Gibbsian.
3. At every $p\ne1/2$ in $(0,1)$, $\nu_p$ has an **essential discontinuity of the two-sided single-site conditional** at the exterior configuration whose spins are all one. It admits **no quasilocal specification**, and therefore is not Gibbsian for any uniformly absolutely summable one-dimensional interaction.

Here "one-dependent" is a statement about unconditional correlations. "Quasilocal" requires continuity of conditional probabilities under *all* exterior configurations, including exceptional zero-probability infinite boundary patterns. These are different requirements.

## Exact finite-cylinder conditionals

For positive integers $L,R$ and integer $K\ge0$, consider an exterior cylinder event $A_{L,R,K}$ in which the observed coordinates immediately to the left of site zero are a run of length $L$ of ones, preceded by $K$ zeros; and to the right are a run of length $R$ of ones, followed by $K$ zeros. Coordinates outside these four finite runs are unrestricted.

Explicitly:

$$
\begin{array}{ll}
Y_{-L-K},\ldots,Y_{-L-1}=0,
&Y_{-L},\ldots,Y_{-1}=1,\\
Y_1,\ldots,Y_R=1,
&Y_{R+1},\ldots,Y_{R+K}=0.
\end{array}
$$

Every $A_{L,R,K}$ has positive $\nu_p$ probability. The hidden variables constrained by the left and right observed runs are disjoint: respectively from $X_{-L-K}$ through $X_0$, and from $X_1$ through $X_{R+K+1}$. Thus these two hidden segments remain independent conditioned on the exterior cylinder.

Each hidden segment compatible with its observed XOR word has **exactly two** possible hidden configurations, specified by one endpoint spin. Write their Bernoulli product weights as $w_L(0),w_L(1)$ and $w_R(0),w_R(1)$, with the left endpoint understood as $X_0$ and the right endpoint as $X_1$. Then the exact conditional probability of the central observed spin is

$$
q_{L,R,K}
=\nu_p(Y_0=1\mid A_{L,R,K})
=\frac{w_L(0)w_R(1)+w_L(1)w_R(0)}
{(w_L(0)+w_L(1))(w_R(0)+w_R(1))}.
$$

This expression is rational when $p$ is rational; it does not invoke limiting probabilities or approximate simulation.

## Boundary pinning lemma

Fix $p\ne1/2$ and put

$$
T=\max\!\left(\frac p{1-p},\frac{1-p}p\right)>1,
\qquad
\varepsilon_K=\frac1{1+T^{K-1}}.
$$

Let $b$ be the preferred hidden value, equal to one if $p>1/2$ and zero if $p<1/2$.

For a left segment with $K$ consecutive observed zeros followed by $L$ observed ones, all $K+1$ spins in its zero run agree. Its Bernoulli weight favors the value $b$ for these repeated spins. The two hidden configurations are complements; within the remaining alternating segment the difference between the numbers of zeros and ones is at most one. Therefore the **unfavored-to-favored** ratio is bounded by $T^{-(K-1)}$, and the probability of the unfavored phase is at most $\varepsilon_K$.

Crossing the run of $L$ observed ones toggles the hidden spin $L$ times. Consequently, conditional on the observed left run, $X_0$ differs from $b\oplus (L\bmod 2)$ with probability at most $\varepsilon_K$. Similarly, conditional on the observed right run, $X_1$ differs from $b\oplus(R\bmod2)$ with probability at most $\varepsilon_K$.

Because the constrained left and right segments are independent, the union bound yields

$$
\begin{aligned}
q_{L,R,K}&\le 2\varepsilon_K
&&\text{when $L\equiv R\pmod2$},\\
q_{L,R,K}&\ge1-2\varepsilon_K
&&\text{when $L\not\equiv R\pmod2$}.
\end{aligned}
$$

These inequalities are uniform in $L$ and $R$.

## Proof of essential discontinuity and non-Gibbsianness

Fix arbitrary $n\ge1$. Both events $A_{n,n,K}$ and $A_{n,n+1,K}$ constrain all coordinates $Y_{-n},\ldots,Y_{-1}$ and $Y_1,\ldots,Y_n$ to equal one. They therefore lie inside **the same arbitrary cylinder neighborhood** of the all-one exterior configuration. Yet, as $K\to\infty$, the preceding bounds show

$$
\nu_p(Y_0=1\mid A_{n,n,K})\longrightarrow0
$$

and

$$
\nu_p(Y_0=1\mid A_{n,n+1,K})\longrightarrow1.
$$

Suppose a continuous two-sided single-site conditional kernel $\gamma_0(1\mid\cdot)$ existed for $\nu_p$. By continuity at the all-one exterior configuration, for a sufficiently large $n$ its value would differ by less than $1/4$ from its value at that configuration throughout this central cylinder. The DLR consistency property and the tower rule imply that its average over either positive-probability sub-cylinder $A_{n,n,K}$ or $A_{n,n+1,K}$ equals the corresponding finite conditional $q$. Therefore both finite conditionals would have to lie within $1/4$ of the same number. Choosing $K$ so that the first is below $1/8$ and the second above $7/8$ makes that impossible.

Thus no continuous version of the single-site exterior conditional can exist, and no quasilocal specification is compatible with $\nu_p$. In particular a Gibbs representation by a uniformly absolutely summable interaction is impossible. This completes part 3 of the statement.

For part 1, each finite observed word has exactly two compatible hidden bit strings, each of strictly positive product weight, proving full support; stationarity is immediate from translation-equivariance. Observed groups with index separation at least two depend on disjoint sets of independent $X$ variables, proving one-dependence. For part 2, if $p=1/2$, the two compatible hidden strings each have mass $2^{-(m+1)}$ for an observed word of length $m$, giving observed mass $2^{-m}$ for every word. Therefore the observed process is iid fair Bernoulli.

## Explicit rational replay

For $p=3/4$, two exact finite cylinders give

$$
q_{2,2,2}=\frac{27}{392},
\qquad
q_{2,3,2}=\frac{61}{70}.
$$

The same exterior with longer distant zeros forces the first probability toward zero and the second toward one. See `research/csm-001/xor_block_obstruction.py` for rational endpoint weights, and `tests/test_csm_xor_block_obstruction.py` for independent complete hidden-state enumeration and hostile/fair-coin boundary checks. The direct evaluator costs $O(L+R+K)$ rational operations; the independent exhaustive replay is exponential by design.

**Scientific interpretation:** This exhibits the fragility of locality under *overlapping deterministic gluing*. Even an independent microscopic state, and even an observed process with strictly finite dependence range and full finite-cylinder support, can have singular conditional behavior. Unconditional finite-range decorrelation does **not** imply quasilocality.

## Definitive source comparison

Kari and Taati, [*Statistical Mechanics of Surjective Cellular Automata*](https://arxiv.org/pdf/1311.2319v2) (2014), **Example 32**, proves exactly that the image of a biased Bernoulli measure under this overlapping binary XOR map fails to be a regular Gibbs measure unless the source is fair. **Proposition 33** describes an invariant-measure collapse obstruction; **Example 34** extends XOR analysis to its iterates. The source also identifies an earlier suggestion by van den Berg. Thus the XOR preservation/obstruction conclusion above is **established prior art; novelty verdict NEGATIVE**. Our independent finite-cylinder pinning argument and exact arithmetic tests are retained strictly as a reconstructive calibration/checking fixture. No originality of that alternative proof is claimed pending a source-level audit of the van den Berg predecessor.

## Novelty and authority boundary

The result is an **already published example**. The present note adds a proposed independently readable cylinder-ratio proof and exact-rational fixture. These must be reviewed and replayed as mathematical reconstruction; G2 novelty must instead seek a theorem with demonstrably different hypotheses or conclusion and check it against the Kari–Taati and van den Berg predecessor class.

The positive single-site-channel preservation theorem is not contradicted: the XOR image observes **two overlapping hidden sites**, and its lifted hidden-state transition has structural zeros, so the strict-positivity hypothesis used for uniform projective contraction is lost. This is the intended sharp boundary diagnostic.

**Status:** FINITE EXACT CERTIFICATE + PROOF CANDIDATE; novelty **NEGATIVE (KNOWN RESULT)**, mathematical certification NOT ISSUED. G0 source equivalence and comprehensive G2 novelty gate remain open; no G3 general theorem is inferred.
