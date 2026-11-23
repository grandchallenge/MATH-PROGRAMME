# CSM-G2-WP05 — weight-sensitive posterior envelopes with permanent structural zeros

**Programme:** CSM-001. **Status:** self-contained finite-state convexity and exact-rational certificate, plus a classical Birkhoff-based all-scale example. Internal reconstruction and native CI pending; **no originality or MATHCERT certification claimed**. The main result is an explicit, source-auditable computational criterion; its mathematical mechanism is established hidden-Markov smoothing and projective contraction, not a claim to have invented filter stability.

## 1. The genuine gap after WP04

The exact observable-subspace checker in WP04 decides **finite** Markov memory. It cannot conclude that a stationary output with **infinite** memory fails to be Gibbsian.

Conversely, G2-WP02 used strictly positive labelled transfer matrices, which excludes natural presentations with persistent structural zeros.

This work introduces a **posterior diameter** that is computed by rational arithmetic from the original labelled matrices, remains meaningful when they have zero entries, and bounds the conditional sensitivity to *every* possible future continuation. A second exact identity makes this diameter monotone with respect to observed-prefix length. A separate all-scale contraction proof, not finite test extrapolation, establishes an infinite-memory Gibbsian example despite a globally reducible, permanently zero-filled presentation.

## 2. Probability-conserving posterior columns

Let $A$ be a finite output alphabet and let nonnegative rational matrices $T_a$, indexed by $a\in A$, sum to a stochastic transition matrix $Q$. Assume there is a strictly positive stationary probability row $\pi$ with $\pi Q=\pi$, and the observed process has full word support. This is the same well-typed linear representation as WP04.

For a finite future word $u$, define the nonnegative row vectors

$$
r_u=\pi T_u,\qquad
r_{a,u}=\pi T_a T_u.
$$

Because stationarity implies $\sum_a\pi T_a=\pi$, we have the exact identity

$$
\sum_{a\in A}r_{a,u}=r_u.
$$

Also, whenever the coordinate indexed by $j$ of $r_u$ is zero, every corresponding numerator coordinate $r_{a,u}(j)$ is zero. On the positive support

$$
J_u=\{j:r_u(j)>0\},
$$

therefore define a probability vector for each terminal hidden state:

$$
\rho_{u,j}(a)=\frac{r_{a,u}(j)}{r_u(j)}.
$$

Every coordinate is nonnegative and $\sum_a\rho_{u,j}(a)=1$. These are conditional laws for the present output symbol, given the observed future prefix and the hidden state at the **end** of that prefix (with the time-index alignment supplied by stationarity).

Define their exact total-variation diameter:

$$
D(u)=\max_{i,j\in J_u}
\frac12\sum_{a\in A}
|\rho_{u,i}(a)-\rho_{u,j}(a)|,
\qquad
\Delta_k=\max_{u\in A^k}D(u).
$$

Every $D(u)$ and $\Delta_k$ is a finite **rational** number computable from the matrices and stationary row, without sampling or floating-point thresholds.

## 3. Exact theorem: posterior convexity, monotonicity, and non-nullness

**Theorem (elementary posterior-envelope inequalities).**

(a) For every future prefix $u$ and any two finite continuation words $v,w$, the conditional output laws satisfy

$$
\left\|
\nu(Y_0=\cdot\mid Y_1\ldots Y_{|uv|}=uv)
-
\nu(Y_0=\cdot\mid Y_1\ldots Y_{|uw|}=uw)
\right\|_{\mathrm{TV}}
\le D(u).
$$

(b) For every output letter $z$, one has

$$
D(uz)\le D(u),
\qquad
\Delta_{k+1}\le\Delta_k.
$$

(c) Let

$$
c_0=\min_{a\in A,j}
\frac{(\pi T_a)_j}{\pi_j}.
$$

If $c_0>0$, then **all** posterior columns at every prefix have all output probabilities at least $c_0$. Consequently every finite-future conditional of each output letter is uniformly at least $c_0$.

**Proof.** For any tail $v$, set $b_v=T_v\mathbf1$. The conditional law is

$$
q(a\mid uv)=
\frac{r_{a,u}b_v}{r_u b_v}
=
\sum_{j\in J_u}
\frac{r_u(j)b_v(j)}{r_u b_v}\,
\rho_{u,j}(a).
$$

By full word support the denominator is positive. The coefficients are nonnegative and sum to one, so every such conditional is in the convex hull of the terminal posterior columns. The total-variation diameter of a convex hull equals the diameter of its generating points. This proves (a).

For extension by one observed letter $z$, direct matrix multiplication gives

$$
\rho_{uz,j}(a)=
\sum_{i\in J_u}
\frac{r_u(i)T_z(i,j)}{r_uT_z(:,j)}\,
\rho_{u,i}(a)
$$

for every $j\in J_{uz}$. Hence **each new posterior column is a convex combination of old posterior columns**. Taking convex hulls cannot increase their total-variation diameter: $D(uz)\le D(u)$. Maximizing over words proves (b).

If $c_0>0$, all initial columns at the empty prefix have every output probability at least $c_0$. Part (b)'s convex-combination recursion preserves this lower bound at every subsequent prefix; part (a) passes it to every future conditional. QED.

**Logical caveat:** Observing $\Delta_k$ decrease over some finite set of lengths **does not prove** that it tends to zero or has a summable tail. The all-scale asymptotic hypothesis must be justified independently.

## 4. An explicitly sufficient regularity theorem

Suppose $c_0>0$ and an independently established bound shows, for all integers $k\ge0$,

$$
\Delta_k\le C\theta^k,
\qquad
0\le\theta<1.
$$

Then all finite-future conditional laws form a uniformly Cauchy family as the common prefix grows: their total-variation distance is at most $\Delta_k$. They converge to a strictly positive continuous function $g$ on infinite observed futures. For futures agreeing in their first $k$ symbols, every log-conditional variation is bounded by

$$
|\log g(a\mid u)-\log g(a\mid v)|
\le\frac{C}{c_0}\theta^k.
$$

Choose a reference output letter and telescope the logarithm of $g$ along finite prefixes. The interval interaction term of length $k+1$ has norm at most a constant times $\theta^{k-1}$ for $k\ge2$. Since

$$
\sum_{k\ge0}(k+1)\theta^k<\infty,
$$

this gives a translation-invariant, **uniformly absolutely summable** interval interaction. The standard right-to-left cylinder-ratio reconstruction supplies a positive quasilocal two-sided DLR specification for the stationary observed law.

The same argument works with the stronger general hypothesis

$$
\sum_{k\ge0}(k+1)\Delta_k<\infty
$$

and $c_0>0$. The extra factor $k+1$ explicitly accounts for the number of translated intervals of that size that contain the origin. Merely showing $\Delta_k\to0$ is **not enough** to certify a Gibbs interaction.

This is a sufficient **weights-sensitive** criterion; it is **not asserted necessary**, nor is there a claim that checking finitely many $\Delta_k$ values certifies the unbounded tail.

## 5. All-scale exact rational bound from a positive observable sector

For a stationary sector with **strictly positive** labelled transfer matrices $A_z$, define the finite rational maximum

$$
C_{\mathrm{cross}}
=
\max_{z,i,j,s,t}
\frac{A_z(i,s)A_z(j,t)}
{A_z(i,t)A_z(j,s)},
\qquad
\kappa=\frac{C_{\mathrm{cross}}-1}{C_{\mathrm{cross}}+1}<1.
$$

Write $\rho_{\varnothing,j}(a)$ for the initial posterior columns and define

$$
R_0=\max_{a,i,j}
\frac{\rho_{\varnothing,i}(a)}
{\rho_{\varnothing,j}(a)}\ge1.
$$

Classical Birkhoff projective contraction, applied **to the positive row vectors on the right by $A_z$**, gives

$$
d_H(\pi A_a A_u,\pi A_u)
\le\kappa^{|u|}
d_H(\pi A_a,\pi)
\le\kappa^{|u|}\log R_0.
$$

Hence posterior columns' coordinate ratios are at most $R_0^{\kappa^{|u|}}$. Using the elementary convexity inequality

$$
R_0^t\le1+t(R_0-1),\qquad 0\le t\le1,
$$

and the fact that each posterior coordinate is at most one yields the **entirely rational** all-scale total-variation bound

$$
\Delta_k\le
\frac{|A|}{2}(R_0-1)\kappa^k.
\tag{2}
$$

This is an analytic theorem derived from an explicitly recorded source lemma, **not a forecast extrapolated from computed prefixes**.

## 6. Structurally zero, infinite-memory, Gibbsian specimen

Let $P$ and $\pi$ be

$$
P=
\begin{pmatrix}
4/5&1/5\\
1/3&2/3
\end{pmatrix},
\qquad
\pi=(5/8,3/8).
$$

Emit binary outputs from the current hidden state with positive probabilities

$$
\Pr(Y_i=1\mid S_i=0)=1/4,\qquad
\Pr(Y_i=1\mid S_i=1)=3/4.
$$

The two positive sector matrices are

$$
A_z(s,t)=P(s,t)\Pr(Y_i=z\mid S_i=s).
$$

An exact WP04 rank/Hankel check finds minimal dimension **2** and rejects reverse Markov orders **0 and 1**. Therefore, by the explicitly attributed Béal et al. (2026) minimal-order bound, the observed law has **infinite** Markov memory. It is nevertheless Gibbsian by the positive-sector contraction proof.

Now construct a four-state presentation consisting of two **noncommunicating** hidden sectors: one has the $A_z$ matrices, the other has the same model after permuting its two hidden-state labels. The full labelled matrices are block diagonal, hence contain structural zeros **in every product of every word length**. A finite exact rational-series equality test proves that the two sectors have identical output-cylinder probabilities for **all** finite words: construct the joint block transfer, generate its future-message basis, and check that the signed difference of the two stationary rows annihilates the entire basis. No finite-window extrapolation is involved.

Consequently, every stationary mixture of these two observationally equivalent sectors has the **same observed process** as either positive sector. Its block-diagonal hidden representation never becomes positive, but its output is an **infinite-memory Gibbs measure**.

For these specifically permuted sectors the posterior-column distributions are the same up to permutation, so the complete four-state posterior diameter equals that of the base sector at every prefix. Exact calculations yield

| Quantity | Value |
| --- | --- |
| Full lifted dimension | 4 |
| Minimal observable dimension | 2 |
| Positive-sector cross-ratio $C_{\mathrm{cross}}$ | 8 |
| Conservative rational $\kappa$ | $7/9$ |
| Initial ratio $R_0$ | $5/3$ |
| Uniform output non-null lower bound $c_0$ | $7/20$ |
| Exact $\Delta_0$ | $7/30$ |
| Exact $\Delta_1$ | $1/10$ |

In particular, the proved bound for **all** $k$ is

$$
\boxed{\Delta_k\le\frac23\left(\frac79\right)^k.}
$$

This certifies Gibbsian regularity in a globally reducible hidden presentation, *without* declaring its permanently zero transfer entries positive. The positive observational sector and its exact word-law equivalence are the additional mathematical evidence.

## 7. Hostile counterexamples and logical limits

The exact one-step posterior recursion also explains the known non-Gibbsian examples.

- **Two-layer XOR with fair iid spins:** every posterior column is the fair coin law. Its exact diameter is $\Delta_k=0$ for all $k$.
- **Two-layer XOR with biased parameter $p=3/4$:** every labelled transfer acts as a positive-weight permutation. The posterior columns are permuted, not mixed, at each observation. Thus the diameter remains $\Delta_k=1/2$ for **every** $k$, consistent with the earlier Kari–Taati obstruction.
- **Two disconnected Bernoulli phases with parameters $49/100$ and $51/100$:** each labelled matrix is diagonal. No posterior column mixes with the other, and $\Delta_k=1/50$ for **every** $k$. The measured diameter correctly identifies persistent phase uncertainty.

A diagnostic that ignores statistical weights would assign the same graph to the fair and biased XOR systems and miss this distinction. Conversely, a diagnostic that merely requires the *original matrices* to become positive would incorrectly reject the reducible, observationally equivalent Gibbsian specimen.

**Limits:** The posterior envelope uses all hidden terminal coordinates, so it can be conservative when some hidden directions are observationally invisible. An observationally equivalent positive quotient is a sufficient route to a Gibbs conclusion; it is not necessary. The criterion is neither a universal decision algorithm for Gibbsianity nor proof of originality. No general finite-time algorithm for deciding an infinite-horizon $\Delta_k$ decay rate is claimed.

## 8. Evidence and source posture

- `research/csm-001/posterior_envelope.py` computes exact posterior columns, total-variation diameters, finite word-law equivalence witnesses and rational Birkhoff constants.
- `tests/test_csm_posterior_envelope.py` checks posterior barycentric identities against independently evaluated word probabilities, per-prefix and uniform monotonicity, structural-zero vs infinite-memory Gibbs positive control, the exact rational rate, small perturbation inequality witnesses, full-support rejection and three negative controls.
- Local replay on exact candidate `d574590dc5adb290fbac2dfcfa0e9896e24af553` passed 7/7 tests; authenticated OS capture `46d64b4e51d34e45a15a20503c665dd4`; independent execution attested=false. Protected CI must replay the final exact head.

**Prior mathematical sources:** Birkhoff–Hopf projective contraction and positive matrix products; classical HMM filter/smoother forgetting; [Exponential stability of filters and smoothers for hidden Markov models](https://openresearch-repository.anu.edu.au/entities/publication/c4ff39c7-5166-4278-b17f-371d6bc861e1); [Exponential filter stability via Dobrushin's coefficient](https://arxiv.org/abs/1910.08463); [Béal et al., Sofic measures (2026), Theorems 4.4 and 5.1](https://arxiv.org/html/2604.11212v2). These are existing theorem classes; the precise GCL formulation, calculations and implementation are **not promoted as a novel theorem** until stronger source comparison and independent specialist review.

## 9. Frontier and claim boundary

**Completed mathematical reconstruction target:** A true finite-state, weight-sensitive, nonnegative-matrix posterior envelope with an exact monotonicity identity, an explicit all-scale contraction bridge, and a rigorously Gibbsian **infinite-memory** example whose original transfer matrices have permanent zeros.

**Original G2 target still open:** Establish a provably new **weights-sensitive** sufficient/necessary condition for non-quasilocal versus Gibbsian behavior **without** an equivalent positive sector, strict block positivity, or already-known fiber/posterior stability hypotheses. Compare that claim at theorem level against existing HMM, sofic, Dobrushin and relative-pressure results before any promotion or certification.

**Named boundary:** `CSM-G2_NEW_IRREDUCIBLE_STRUCTURAL_ZERO_POSTERIOR_CONTRACTION_OPEN`.
