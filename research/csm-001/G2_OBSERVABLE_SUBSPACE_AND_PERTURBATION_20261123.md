# CSM-G2-WP04 — exact observable-subspace certificates with structural zeros

**Programme:** CSM-001; **tracker:** [#3136](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3136). **Status:** self-contained finite-word proof reconstruction and executable rational certificates; exact-head CI and protected admission required. **Novelty:** NOT CLAIMED. Finite-rank rational-series algorithms, hidden-Markov order tests, and the global finite-order cutoff already exist; see Béal et al. (2026), Theorems 4.4 and 5.1. **Certification:** no MATHCERT proof certificate and no public original-theorem promotion.

## 1. Goal and sharp claim boundary

The previous G2-WP02 used **strict positivity** of all labelled transfer matrices to certify exponentially continuous conditionals. G2-WP03 proved that the zero/nonzero pattern alone cannot classify Gibbsianity.

This work supplies a different, exact **weight-sensitive** certificate. It decides whether a finite-state output process has a nominated **finite reverse Markov order**, even when every labelled transfer matrix has zeros. It then uses a clearly identified *external theorem* to decide whether **any finite Markov order** exists. It is not a general Gibbs/non-Gibbs classifier: continuous infinite-memory Gibbs processes can fail the finite-memory test.

## 2. Transfer model and full-support check

Let the output alphabet $A$ be finite. Let $T_a$ be a nonnegative rational square matrix of order $d$ for each output letter $a\in A$. Assume their sum

$$
Q=\sum_{a\in A}T_a
$$

is stochastic and has a strictly positive stationary probability row $\pi$, so $\pi Q=\pi$. Define the stationary word probabilities

$$
\nu(w)=\pi T_w\mathbf1,
\qquad
T_{a_1\cdots a_m}=T_{a_1}\cdots T_{a_m},
\qquad T_{\varnothing}=I.
$$

The output has **full shift support** precisely if all word probabilities are positive.

A finite support-domain check does not use the actual weights: start with all hidden states, evolve the set of reachable states under each letter by the positive-entry graph of $T_a$, and perform breadth-first search on the finite state-set automaton. If the empty set is reached, the corresponding output word is forbidden; otherwise every word is possible. At most $2^d$ distinct subsets need examination. This Boolean test establishes the **domain** of the subsequent algebraic proof, not Gibbsianity.

## 3. Finite-window cutoff theorem

For an integer $k\ge0$, say the output has *reverse memory at most* $k$ when for every output letter $a$, every future prefix of length $k$ $u$, and every further finite future word $v$,

$$
\nu(a u v)\nu(u)=\nu(a u)\nu(u v).
\tag{1}
$$

For full-support words, (1) says that the conditional probability of the present symbol given an arbitrarily long future depends only on its first $k$ symbols.

**Theorem (exact finite-window reduction).** Under the preceding rational, stationarity and full-support hypotheses, (1) holds for **all** future tails $v$ if and only if it holds for tails of length at most $d-1$.

**Proof.** Define the future-message space

$$
W=\mathrm{span}_{\mathbb Q}\{T_v\mathbf1:v\in A^*\}
\subseteq\mathbb Q^d,
$$

and its finite-depth approximation

$$
W_\ell=\mathrm{span}_{\mathbb Q}\{T_v\mathbf1:|v|\le\ell\}.
$$

We have $W_0=\mathrm{span}\{\mathbf1\}$, of dimension one, and

$$
W_{\ell+1}=W_\ell+\sum_{a\in A}T_aW_\ell.
$$

Whenever $W_{\ell+1}=W_\ell$, this space is invariant under every $T_a$ and therefore equals $W$. Otherwise its dimension increases by at least one. Since the ambient dimension is $d$, stabilization occurs no later than $\ell=d-1$:

$$
W=W_{d-1}.
$$

For fixed $a,u$ define the rational row functional

$$
L_{a,u}
=\nu(u)\pi T_aT_u-\nu(a u)\pi T_u.
$$

Its evaluation on the actual future message is exactly

$$
L_{a,u}(T_v\mathbf1)
=\nu(a u v)\nu(u)-\nu(a u)\nu(u v).
$$

Thus (1) for all words $v$ is equivalent to $L_{a,u}$ annihilating $W$, which is equivalent to its annihilating the finite generating family with $|v|\le d-1$. This proves both directions. QED.

**Constructive witness:** Build a basis of $W$ from actual word-labelled messages, adding a vector only when its exact rational rank increases. The construction uses at most $d$ basis vectors, each tagged by a tail of length at most $d-1$. A failure produces a concrete word triple $(a,u,v)$ with two **different exact rational conditionals**, not merely a floating-point score.

The same technique builds the left row span from $\pi T_u$. The rank of their bilinear pairing gives the minimal linear-representation dimension $n\le d$. The algorithm uses exact Gaussian elimination, not singular-value thresholds.

## 4. Physical interpretation and the prior-art cutoff

If (1) holds for a finite $k$, the stationary observed process is reverse Markov of order $k$; equivalently, the time-reversed stationary process has Markov order $k$. With full shift support, all corresponding finite conditional probabilities are positive. The familiar reverse-chain factorization supplies a **finite-range one-dimensional Gibbs interaction** on intervals of length at most $k+1$, with a term such as

$$
-\log\frac{\nu(a u)}{\nu(u)}
$$

for a present letter $a$ and the next $k$ future letters $u$. This is classical finite-order Markov/Gibbs equivalence, not an original theorem.

**Global finite-order decision uses known mathematics.** In Béal, Gilburg, Jugé, Mairesse and Perrin, [*Sofic measures*, arXiv:2604.11212v2](https://arxiv.org/html/2604.11212v2) (19 October 2026), Theorem 4.4 recalls Holland's minimal-representation rank-one criterion for order $k$; **Theorem 5.1** proves that if a stationary sofic measure of minimal linear dimension $n$ has any finite Markov order, it already has order at most $\binom{n}{2}$.

Therefore, after computing the exact minimal dimension $n$, testing all integers

$$
k=0,1,\ldots,\binom{n}{2}
$$

decides the existence of a finite Markov order. A negative result depends on **that external published theorem**, not just on the finite-window reduction above. No independent source-proof replay is asserted.

**Complexity:** the full-support domain check visits at most $2^d$ subsets, spanning a rational message basis adds at most $d$ generators, and each fixed-order decision inspects at most $|A|^k$ prefixes with at most $d$ short tail witnesses. This is a correctness-first exact algorithm, not a guarantee of tractability for large $d$ or $k$.

## 5. Genuine two-layer overlapping composition with zeros

Take iid binary microscopic spins with parameter $p\in(0,1)$; first form overlapping XOR observations

$$
Y_i=X_i\oplus X_{i+1};
$$

then apply a **second overlapping XOR layer**

$$
Z_i=Y_i\oplus Y_{i+1}=X_i\oplus X_{i+2}.
$$

Unlike the positive-channel theorem, **both channels are deterministic** and have structural zeros. The exact Markov lift uses $V_i=(X_{i+1},Y_i)$, four stationary hidden states, and labelled nonnegative matrices $T_z$. No product $T_w$ is a strictly positive four-by-four matrix: the model retains deterministic constraints for every output word.

Both the fair and biased systems have exactly the **same Boolean transfer supports** for all output labels and all labelled products. Nevertheless, exact rational linear algebra yields:

| Microscopic parameter | Lift dimension | Minimal linear dimension | Exact output-memory result |
| --- | ---: | ---: | --- |
| $p=1/2$ | 4 | 1 | Output is iid; order 0 is certified |
| $p=3/4$ | 4 | 4 | All orders 0 through 6 fail; external cutoff excludes every finite order |

For the biased system a particularly short exact witness is

$$
\nu(Z_0=0)=\frac58,\qquad
\nu(Z_0=0\mid Z_1=0,Z_2=0)=\frac7{10}.
$$

The independent microscopic check enumerates all underlying $X_0,\ldots,X_{m+1}$ for each output word of length $m$. The transfer results agree exactly.

The same biased example is **not Gibbsian**, for an independent reason stronger than failure of finite memory. The even-indexed final observations are the overlapping XOR image of the iid even microscopic subsequence; the odd observations are an independent copy from the odd microscopic subsequence. For biased microscopic spins, either copy has the essential-discontinuity obstruction already source-matched to Kari–Taati Example 32. Conditioning an even central site on finite exterior observations in both parities leaves its bad even-parity conditional unchanged; the odd-parity data are independent. The two finite even-boundary cylinder families force the central conditional toward zero and one within every cylinder neighborhood of the all-one even exterior. Thus the interleaved two-layer output has no quasilocal two-sided specification. For $p=1/2$, both parity copies are iid fair, and so is the whole final output.

This is a **known-example corollary** and a compositional regression, not a new statistical-mechanics result.

## 6. Why approximate weight matching is insufficient

A separate elementary obstruction comes from two permanently disconnected hidden phases. For fixed $0<p<1$ and sufficiently small $\delta>0$, put

$$
\nu_\delta
=\frac12\mathrm{Ber}(p+\delta)^{\otimes\mathbb Z}
+\frac12\mathrm{Ber}(p-\delta)^{\otimes\mathbb Z}.
$$

Its two hidden sectors have diagonal labelled matrices

$$
T_1=\mathrm{diag}(p+\delta,p-\delta),\qquad
T_0=\mathrm{diag}(1-p-\delta,1-p+\delta).
$$

All these matrices have the same supports for every $\delta$ in the allowed interval. For $\delta=0$, the image is an iid Gibbs measure. For every $\delta>0$, it is **not quasilocal**.

**Elementary proof of non-quasilocality.** Condition on any fixed finite exterior cylinder, with $r$ observed ones and $s$ zeros. The posterior odds of the two hidden phases are positive and finite. Add, arbitrarily far outside that fixed cylinder, $N$ additional observed ones. These multiply the odds in favor of the phase having larger $p$ by

$$
\left(\frac{p+\delta}{p-\delta}\right)^N,
$$

forcing the central conditional probability of one toward $p+\delta$. Alternatively add $N$ distant zeros; the posterior odds then force the conditional toward $p-\delta$. Both finite events have positive probability and agree on the entire fixed central cylinder. A continuous conditional would have uniformly small oscillation in a sufficiently small cylinder neighborhood; these separated limiting values contradict continuity. Hence there is no quasilocal specification. QED.

Yet every finite observation horizon can be misleadingly close to the Gibbsian model. For any $m$,

$$
\left\|(\nu_\delta)_{[1,m]}
-\mathrm{Ber}(p)^{\otimes m}\right\|_{\mathrm{TV}}
\le m\delta.
$$

This follows by coupling each Bernoulli coordinate so that its mismatch probability is $\delta$, applying a union bound over $m$ coordinates, and then averaging over the two phases.

**Consequence:** no fixed finite empirical horizon and tolerance can, by proximity alone, certify a robust Gibbs-preservation claim across this reducible class. Quantitative posterior synchronization requires a structural hypothesis excluding persistent hidden phases, not merely a small observed discrepancy. This is an elementary instance of established nonquasilocal mixture phenomena and is **not claimed original**.

## 7. Source and replay record

The executable exact reference is `research/csm-001/observable_memory_certificate.py`, tested independently by `tests/test_csm_observable_memory_certificate.py`. It checks zero-tolerant two-layer lifts, exact stationarity, full-support rejection, Gaussian rational spans, finite witness equivalence, minimal dimension, all seven cutoff orders in the biased four-state model, independent hidden-path enumeration, a non-iid one-step Markov case, and arbitrarily small perturbation examples.

**Preliminary exact local replay:** 9/9 tests passed on candidate `40355defb6cd34cded8fb93337cad566f293ceef`, authenticated CHAD capture `ae212db04aa54272993e07cacbab39c9`; independent execution attested=false. Final CI must replay the exact final candidate head.

**Prior-art source lock:** Béal, Gilburg, Jugé, Mairesse, Perrin, *Sofic measures*, arXiv:2604.11212v2, HTML Theorems 4.4 and 5.1; exact [PDF](https://arxiv.org/pdf/2604.11212v2) 402865 bytes, SHA-256 `ac30dc52a667075cbd0fd6ddc73021ab2cc57828ef726859b3a0e44f094ed75d`. The local source-byte acquisition receipt is GCL_CONTROL_BASH_RESULT/1 `b39ec3ad0af34b36bb7c3b6116a5b2dd` with independent attestation=false. The version is materially newer than the legacy CSM source register.

The theorem-level prior-art comparison also includes [Kari–Taati Example 32](https://arxiv.org/abs/1311.2319) for XOR and established work on nonquasilocal mixtures. No public novelty verdict is asserted for the independent *implementation details*; no original mathematical theorem is claimed here.

## 8. Next substantive mathematical boundary

The finite-order problem has an exact answer in this class. The genuine original G2 target is **not** another finite-word Markov-order test. It is a *weight-sensitive, verifiable asymptotic posterior-contraction criterion* for structurally zero overlapping compositions with **infinite but summably continuous memory**, distinguishing them from the biased-XOR and persistent-phase non-Gibbsian cases.

An acceptable result must produce an actual quantitative variation modulus for every observed future, establish a two-sided Gibbs specification under its precise hypotheses, and prove novelty against the classical projective-contraction, fiber-mixing, sofic-measure and posterior-metric sources. Without such a proof, `CSM-G2_ORIGINAL_WEIGHT_SENSITIVE_POSTERIOR_CONTRACTION_OPEN` is the honest boundary.
