# CSM-G2-1D — positive-channel Gibbs preservation with a computable certificate

**Programme:** CSM-001. **Stage:** internally reconstructed mathematical **proof candidate**, with independent exact finite replay. **Novelty:** expressly **NOT CLAIMED**. The positive finite-state hidden-Markov/Gibbs phenomenon and projective-metric contraction are prior mathematics; see G0 audit S05/S06 and classical Birkhoff contraction. **Certification:** none; no MATHCERT admission or external validation. **Scope:** stationary one-dimensional finite hidden Markov chains, not arbitrary DLR specifications, higher-dimensional decimation, or all coarse-graining maps.

## 1. The exact theorem under audit

Let $S$ and $Y$ be nonempty finite sets. Let $P$ be a strictly positive **row-stochastic** $S$ transition matrix. Let $\pi$ be its strictly positive stationary probability vector, and let $E$ be a nonnegative row-stochastic observation channel from $S$ to $Y$. We allow zero entries of $E$, but require every observed symbol to occur with positive marginal mass:

$$
p_a=\sum_{s\in S}\pi(s)E(s,a)>0,\qquad a\in Y.
$$

The stationary hidden chain emits $Y_i$ from $S_i$ using $E$ independently across times conditional on the hidden path. Write $\nu$ for the observed bi-infinite stationary law. Define finite-cylinder conditionals

$$
q_m(a\mid y_1,\ldots,y_m)
=\frac{\nu(Y_0=a,Y_1=y_1,\ldots,Y_m=y_m)}
{\nu(Y_1=y_1,\ldots,Y_m=y_m)}.
$$

All denominators are positive. Put $p_{\min}=\min_{s,t}P(s,t)$, $p_{\max}=\max_{s,t}P(s,t)$ and the checkable quantities

$$
R=p_{\max}/p_{\min},\qquad
\kappa=(R-1)/(R+1)<1.
$$

**Reconstructed preservation certificate (candidate statement).**

1. The limit $g(a\mid y_1y_2\ldots)=\lim_{m\to\infty}q_m(a\mid y_1,\ldots,y_m)$ exists **uniformly** on all infinite observed futures.
2. It is normalized and uniformly non-null: $g(a\mid y^+)\ge p_a/R>0$.
3. If two observed futures share their first $k\ge1$ symbols, then for every $a\in Y$,

$$
|\log g(a\mid y^+)-\log g(a\mid z^+)|
\le 2\log R\,\kappa^{k-1}.
$$

For $R=1$, interpret this as zero variation: the observed process is independent across time.

4. Consequently $\nu$ has a **quasilocal, uniformly non-null specification** and an absolutely summable one-dimensional interaction obtained by telescoping the logarithm of $g$. In fact the interval-interaction norms decay geometrically.
5. The constants $R,\kappa$ are **independent of the emission entries**. If two stochastic observation channels are composed in sequence at every site and all final output symbols have positive mass, the same $R,\kappa$ certify the composite. This is *one-site channel composition*, not an assertion about overlapping-block coarse-graining.

This theorem covers arbitrary zeros in $E$ under the stated observability assumption. The hypotheses **do not** include a general hidden Gibbs phase, a transition with structural zero entries, or a spin-block operation involving overlapping hidden neighborhoods. None of those cases is asserted.

## 2. Proof: exact transfer semantics

Let $D_a$ denote the diagonal matrix with entries $E(s,a)$. Define the strictly positive future message

$$
b_m(y_1,\ldots,y_m)
=P D_{y_1}P D_{y_2}\cdots P D_{y_m}\mathbf 1.
$$

For any nonnegative nonzero $v$, $Pv$ is strictly positive because $P>0$. Each $D_a v$ has at least one positive coordinate whenever $v>0$, since $p_a>0$ and $\pi>0$. Hence each displayed message is strictly positive. Exact matrix expansion gives

$$
q_m(a\mid y_1,\ldots,y_m)
=\frac{\pi D_a b_m}{\pi b_m}.
$$

This identity retains the weight normalization correctly. It is **not** the result of normalizing every unnormalized tensor separately.

## 3. Proof: projective contraction and uniform continuity

For strictly positive vectors $u,v$, define Hilbert's projective distance

$$
d_H(u,v)=\log\left(
\frac{\max_i(u_i/v_i)}{\min_i(u_i/v_i)}
\right).
$$

A positive matrix $P$ contracts this metric by the classical Birkhoff coefficient. If the maximal cross-ratio of four entries of $P$ is $\Xi$, its coefficient is $\tanh((\log\Xi)/4)$. Since $\Xi\le R^2$, the coefficient is at most $\kappa$. Diagonal multiplication by $D_a$, even with zero columns, does not expand the projective distance on the **common nonzero support**, and the following multiplication by $P>0$ returns to the strictly positive cone. Thus each $P D_a$ contracts positive-vector projective distances by at most $\kappa$. This application uses the Birkhoff-Hopf lemma as established prior art, not as a CSM discovery.

Also, for arbitrary nonzero nonnegative vectors $u,v$,

$$
d_H(Pu,Pv)\le 2\log R.
$$

Indeed every coordinate of $Pu$ lies between $p_{\min}\sum u$ and $p_{\max}\sum u$; the same applies to $Pv$. Therefore, if two observation words agree in their first $k\ge1$ symbols but differ arbitrarily afterwards, their messages obey

$$
d_H(b_{\text{word}},b_{\text{other}})
\le 2\log R\,\kappa^{k-1}.
$$

For two strictly positive message vectors $u,v$, and two fixed nonzero nonnegative row vectors $r,s$, every ratio $(ru)/(rv)$ lies between the smallest and largest coordinate ratios $u_i/v_i$. Consequently

$$
\left|\log\frac{ru}{su}-\log\frac{rv}{sv}\right|
\le d_H(u,v).
$$

Apply this to $r=\pi D_a$ and $s=\pi$, obtaining the displayed log-conditional variation bound for $q_m$ whenever the observation words have a common prefix of length $k$. Comparing a word with any extension proves uniform Cauchy convergence as $m\to\infty$; the same variation bound passes to $g$.

For every nonempty future word, $b_m$ has largest-to-smallest component ratio at most $R$. Thus

$$
q_m(a\mid y_1,\ldots,y_m)
=\frac{\pi D_a b_m}{\pi b_m}
\ge \frac{p_a}{R}.
$$

For $m=0$, $q_0(a)=p_a$. Taking limits completes assertions 1–3.

## 4. Proof: explicit one-dimensional Gibbs reconstruction

Fix a reference output symbol $o$. For an infinite future $u=u_1u_2\ldots$, write $A(a,u)=\log g(a\mid u)$. Define interval functions

$$
\psi_0(a)=A(a,o^\infty)
$$

and for $k\ge1$,

$$
\psi_k(a,u_1,\ldots,u_k)
=A(a,u_1\ldots u_k o^\infty)
-A(a,u_1\ldots u_{k-1}o^\infty).
$$

Uniform continuity shows $A(a,u)=\sum_{k\ge0}\psi_k(a,u_1,\ldots,u_k)$, with uniform absolute convergence. The norms of $\psi_0,\psi_1$ are finite by uniform non-nullness. For $k\ge2$ the two arguments of the difference share $k-1$ initial symbols, hence

$$
\|\psi_k\|_\infty
\le 2\log R\,\kappa^{k-2}.
$$

Thus $\sum_k\|\psi_k\|_\infty<\infty$. Associate $\psi_k$ to the interval $[i,i+k]$ in the bi-infinite lattice (the conventional Hamiltonian uses the negative of these log weights).

For completeness, the DLR compatibility argument can be obtained by cylinder ratios. The chain rule from right to left says that any finite observed word has probability equal to its rightmost one-symbol marginal times the product of the relevant finite-future conditionals $q_m$. Compare two assignments on a fixed interval $[a,b]$ while holding the observations outside it fixed inside a larger window $[-L,R']$. Factors to the right of $b$ cancel. Replace each remaining $q_m$ by $g$: the sum of replacement errors is bounded by a geometric tail in $R'-b$, uniformly in $L$. The contributions from indices strictly to the left of $a$ converge uniformly as $L$ increases, because those differences of log $g$ decay geometrically with distance from $[a,b]$. The resulting finite set of normalized conditional ratios therefore converges uniformly over exterior configurations. It defines strictly positive, continuous conditional kernels; their compatibility and consistency with $\nu$ follow by taking limits of the finite conditional probabilities. Expanding the terms in log $g$ using the $\psi_k$ telescoping series identifies these kernels as the Gibbs specification for the absolutely summable interval interaction. This proves assertion 4 without presupposing that a finite-volume partition function can itself determine a thermodynamic limit.

Finally, at each site the composite of observation kernels $E_1:S\to Z$ and $E_2:Z\to Y$ is the stochastic matrix $E=E_1E_2$. Independence of the intermediate local symbols conditional on the hidden states shows equality of *all* observed cylinder probabilities. Since $P$ and hence $R,\kappa$ are unchanged, the same certificate applies to the composite whenever its output symbols have positive marginal mass. This proves assertion 5.

**Boundary of this argument:** The Hilbert contraction and the implication from summable one-sided continuity to Gibbs reconstruction are established techniques. The above is an explicit, finite-state reconstruction for GCL's composition conventions, **not a novelty claim**. Specialist review should recheck the passage from cylinder ratios to a two-sided specification before mathematical certification.

## 5. Exact-arithmetic specimen and independent replay

`research/csm-001/hidden_markov_certificate.py` implements:

- hypothesis rejection for nonpositive $P$, nonstationary $\pi$, nonstochastic channels and an impossible observed symbol;
- exact transfer messages and conditional probabilities $q_m$;
- a checkable rational $R,\kappa$ and positive lower bound $p_a/R$;
- channel composition and exact observed-word probabilities;
- an independently enumerated hidden-path formula.

`tests/test_csm_hidden_markov_certificate.py` checks the transfer formula against direct enumeration, the probability-ratio identity, the non-null bound, geometric log-variation bounds over many different futures, composition, the rank-one transition boundary and invalid hypotheses.

For the fully specified two-hidden-state example,

$$
P=\begin{pmatrix}
4/5&1/5\\
1/3&2/3
\end{pmatrix},
\quad
\pi=(5/8,3/8),
\quad
E=\begin{pmatrix}
1&0\\
1/4&3/4
\end{pmatrix},
$$

the exact output masses are $(23/32,9/32)$, and the conservative **rational** certificate is $R=4$, $\kappa=3/5$. The observed emission channel has a zero entry, so this tests more than the trivial all-entries-positive case.

## 6. Advancement boundary and next nontrivial mathematical route

**Positive 1D finite-state channel preservation: reconstructed as prior mathematics.** Do **not** treat this as a new G2 theorem.

An actual G2 novelty target must move beyond already known Hölder-factor and one-dimensional specification results. Candidate direction: establish a **uniform local-to-global preservation criterion** for a compositional class of overlapping-block transformations in higher-dimensional Gibbs specifications, including an explicitly checkable condition that rules out hidden phase transitions in constrained fibers and an obstruction when those fibers undergo a phase transition. This is a research target, *not* a proved theorem. First compare it against van Enter–Fernández–Sokal and later Dobrushin/Shlosman and hidden-phase-transition criteria; otherwise the likely outcome is another negative novelty verdict.

**Gates:** G0 remains partial (full source-byte locks and theorem comparison outstanding). G2 remains **open** for a new theorem. G3 infinite-volume source-family and exact DLR hypotheses remain open. No authorization to activate G4 follows.
