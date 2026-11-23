# CSM-G2-WP03 — zero-pattern-only Gibbs classification is impossible

**Status:** internally proved elementary no-go corollary from the *already published* biased-Bernoulli XOR example. **Originality:** NOT CLAIMED. **No MATHCERT certification.** This note is about the limits of a proposed GCL proof strategy, not a new physical phase transition.

## 1. Formal statement

Let a finite-state stationary hidden Markov process have strictly positive stationary law $\pi$, and let $\{T_z\}_{z\in Z}$ be its nonnegative output-labelled transfer matrices, summing to a stochastic transition. A **support-only criterion** is one whose input consists solely of the Boolean matrices

$$
B_z(i,j)=\mathbf1_{\{T_z(i,j)>0\}}.
$$

Such a criterion may perform arbitrary exact finite or infinite Boolean-matrix operations and inspect the supports of all labelled products, but it has no access to the magnitudes of positive transition weights.

**No-go proposition.** There is no support-only condition that is both necessary and sufficient, over all stationary finite-state hidden Markov presentations, for the observed measure to be Gibbsian for a uniformly absolutely summable interaction on the binary full shift.

## 2. Exact proof

Fix $0<p<1$. Let hidden spins $X_i$ be iid Bernoulli with parameter $p$, and define the deterministic overlapping factor

$$
Y_i=X_i\oplus X_{i+1}.
$$

Write $q=1-p$. Because the hidden transition matrix has rows $(q,p)$, the two labelled transfer matrices in hidden-state order $(0,1)$ are

$$
T_0(p)=
\begin{pmatrix}
q&0\\0&p
\end{pmatrix},
\qquad
T_1(p)=
\begin{pmatrix}
0&p\\q&0
\end{pmatrix}.
$$

For every parameter in the entire interval $0<p<1$, their support matrices are exactly

$$
B_0=
\begin{pmatrix}
1&0\\0&1
\end{pmatrix},
\qquad
B_1=
\begin{pmatrix}
0&1\\1&0
\end{pmatrix}.
$$

All supports of labelled products are therefore parameter independent as well: Boolean multiplication depends only on the two fixed generators. Moreover every finite output word has positive probability, because each XOR word has exactly two compatible hidden words and every hidden word has positive product probability.

At $p=1/2$, every output word of length $m$ has two hidden preimages of probability $2^{-(m+1)}$, hence observed probability $2^{-m}$. The observed law is iid fair Bernoulli and Gibbsian for the zero interaction.

For $p\ne1/2$, the same map produces a measure with an essentially discontinuous two-sided single-site conditional at the all-one exterior configuration. This has an explicit independent finite-cylinder proof in GCL's G2_XOR_OVERLAP_NONQUASILOCALITY_20261123.md, and the non-Gibbsian example was established earlier in Kari–Taati, *Statistical Mechanics of Surjective Cellular Automata*, Example 32 (including prior credit to van den Berg). Therefore it is not Gibbsian for an absolutely summable interaction.

The two parameters $p=1/2$ and $p=3/4$ yield **identical inputs to every support-only criterion but opposite Gibbs classifications**. That contradicts necessary-and-sufficient classification and proves the proposition. QED.

## 3. What the proposition does and does not rule out

- **Ruled out:** exact if-and-only-if Gibbs characterization using only the zero/nonzero matrices, their finite Boolean products, allowable-word language, or any other invariant determined exclusively by these supports.
- **Not ruled out:** support-only **sufficient** certificates. Uniformly positive products of all words of some length give a conventional Hilbert contraction guarantee, but their failure is not evidence of non-Gibbsianness.
- **Required for any complete criterion:** numerical positive weights, posterior ratios, or an equivalent measure-sensitive invariant. The same labelled graph may support both Gibbsian and non-Gibbsian outputs.
- **Existing literature:** this elementary logical corollary follows immediately from the already established Kari–Taati example. Its purpose is to exclude an unsound GCL research direction, not to assert an original theorem.

## 4. Next original research obligation

Seek a **weights-sensitive** compositional characterization beyond classical positive-matrix contraction, fiber-mixing, almost-additive relative pressure and posterior-Dobrushin criteria. Candidate scope: a finite, efficiently checkable weighted posterior-stability condition for structurally zero overlapping transformations, whose quantitative conclusion is strictly stronger than the known corresponding theorems.

Before labeling any such statement original, compare the exact theorem and condition against Külske–Opoku (2008), Chazottes–Ugalde, Kari–Taati, Piraino/Yoo fiber mixing and Yayama's **arXiv:2402.10199v2**, especially Definition 4.1, Proposition 4.1 and Theorem 4.2 under Setting (C). That 2025 revision has an expanded classification absent from the 2024 v1 source.

**Current substantive boundary:** CSM-G2_ORIGINAL_WEIGHT_SENSITIVE_OVERLAP_CRITERION_UNPROVED. The no-go proof itself is complete as an elementary corollary; its novelty is negative.
