# CSM-G2-WP02 — quantitative two-layer overlapping-channel certificate

**Programme:** CSM-001; **status:** exact finite-state proof reconstruction, locally executed regression suite, pending protected CI and mathematical source-semantic review. **Originality:** NOT ESTABLISHED and NOT CLAIMED. Classical Birkhoff–Hopf contraction and the one-dimensional summable-variation-to-Gibbs bridge supply the principal mathematical ingredients. **No MATHCERT or public external certification.**

## 1. Why a naive single-site composition is invalid

Let $S$, $Y$, and $Z$ be nonempty finite alphabets. The stationary hidden chain $S_i$ has strictly positive stochastic transition $P(s,t)$ and strictly positive stationary distribution $\pi$. Given the entire hidden chain, generate independent first-layer outputs with strictly positive stochastic channel

$$
K(y\mid s,t)>0,\qquad
Y_i\sim K(\cdot\mid S_i,S_{i+1}).
$$

Then independently given the entire first layer, generate outputs using a second strictly positive stochastic channel

$$
H(z\mid y,w)>0,\qquad
Z_i\sim H(\cdot\mid Y_i,Y_{i+1}).
$$

Both channels are *overlapping*: consecutive outputs share inputs. In general neither product of one-site stochastic kernels nor pointwise normalization of weighted factor networks equals the law of the final observed process. The following lift retains all shared-variable dependencies.

## 2. Exact Markov lift and transfer formula

Set $V_i=(S_{i+1},Y_i)$, taking values in $S\times Y$. Then $V_i$ is a stationary Markov chain with

$$
Q((s,y),(t,w))=P(s,t)K(w\mid s,t).
$$

Its strictly positive invariant distribution is

$$
\lambda(s,y)=\sum_{u\in S}\pi(u)P(u,s)K(y\mid u,s).
$$

Indeed the transition sums to one, and using $\pi P=\pi$ gives $\lambda Q=\lambda$ exactly. Strict positivity of $P$ and $K$ gives $Q>0$. The second-layer output $Z_i$ depends on adjacent lift states $V_i=(s,y)$ and $V_{i+1}=(t,w)$ through $H(z\mid y,w)$.

For each final output symbol $z$, define a strictly positive square transfer matrix

$$
T_z(v,v')=Q(v,v')H(z\mid y(v),y(v')).
$$

Then $\sum_z T_z=Q$, and the final process has exact finite-cylinder probabilities

$$
\nu(Z_0=z_0,\ldots,Z_{m-1}=z_{m-1})
=\lambda^\top T_{z_0}\cdots T_{z_{m-1}}\mathbf1.
$$

This is a **precise compositional semantics** for two overlapping stochastic layers, not a false reduction to independent single-site channels.

## 3. Computable quantitative preservation theorem

For any family of strictly positive matrices $T_z$ summing to a stochastic matrix $Q$, with $\lambda^\top Q=\lambda^\top>0$, define the projective cross-ratio bound

$$
C=\max_{z,i,j,k,\ell}
\frac{T_z(i,k)T_z(j,\ell)}
{T_z(i,\ell)T_z(j,k)}\ge1.
$$

This is a **finite rational maximum** when all input probabilities are rational. Put

$$
\widehat\kappa=\frac{C-1}{C+1}<1.
$$

For each symbol, define another finite, exact lower bound

$$
c_z=\min_j\frac{(\lambda^\top T_z)_j}{\lambda_j}>0.
$$

**Theorem (internally reconstructed, classical mechanism).** The limiting future-conditional probabilities

$$
g(z\mid u_1u_2\ldots)
=\lim_{m\to\infty}
\frac{\lambda^\top T_zT_{u_1}\cdots T_{u_m}\mathbf1}
{\lambda^\top T_{u_1}\cdots T_{u_m}\mathbf1}
$$

exist uniformly over all infinite future strings; are stochastic and satisfy $g(z\mid u)\ge c_z$; and obey the explicit continuity estimate

$$
\left|\log g(z\mid u)-\log g(z\mid v)\right|
\le(\log C)\widehat\kappa^{k-1}
$$

whenever $u,v$ share their first $k\ge1$ observed symbols. For $C=1$, interpret the right side as zero. Consequently the final stationary output measure is Gibbsian for a one-dimensional absolutely summable interval interaction, with exponentially decaying interaction norms.

**Proof.** For positive column vectors $a,b$, let

$$
d_H(a,b)=\log\frac{\max_i a_i/b_i}{\min_i a_i/b_i}
$$

be the Hilbert projective metric. The Birkhoff–Hopf theorem gives projective diameter at most $\log C$ for each $T_z$, and contraction factor at most

$$
\tanh\left(\frac{\log C}{4}\right)
=\frac{\sqrt C-1}{\sqrt C+1}
\le\widehat\kappa.
$$

Hence two positive transfer messages with a common first $k$ symbols are separated by at most $(\log C)\widehat\kappa^{k-1}$. For any nonzero nonnegative row vectors $r,s$, the difference between the logarithms of $(ra)/(sa)$ and $(rb)/(sb)$ is bounded by $d_H(a,b)$: each positive linear functional ratio lies between the minimum and maximum componentwise ratios. Use $r=\lambda^\top T_z$ and $s=\lambda^\top$. This proves the same log-conditional difference bound for finite future words sharing a prefix. Comparing a word to any extension gives uniform convergence to $g$.

Also the conditional is a convex combination of the positive numbers $(\lambda^\top T_z)_j/\lambda_j$, with weights proportional to $\lambda_j$ times the future message. Thus it is at least $c_z$. Normalization follows from $\sum_z T_z=Q$ and $\lambda^\top Q=\lambda^\top$.

To obtain a Gibbs interaction, choose a reference symbol $o$ and telescope $A(z,u)=\log g(z\mid u)$ along finite prefixes terminated by $o^\infty$. Denote the incremental interval term of length $j+1$ by $\psi_j$. The first two terms are uniformly bounded by non-nullness. For $j\ge2$, the two future strings used to define $\psi_j$ agree in their first $j-1$ symbols, so

$$
\|\psi_j\|_\infty
\le(\log C)\widehat\kappa^{j-2}.
$$

Their norms are summable; the resulting interval interaction is absolutely summable. The standard one-dimensional cylinder-ratio argument shows that the conditioned finite-volume ratios converge uniformly to a strictly positive quasilocal DLR specification and agree with this telescoped interaction. This is the established *summable one-sided variation implies a two-sided Gibbs description* bridge, not an independent new general theorem. QED, subject to mathematical review of the cited classical inputs.

**Scope:** It is a sufficient condition, not an if-and-only-if theorem. The condition fails to cover structural-zero lifted transitions, deterministic overlapping transformations, infinite alphabets, higher dimensions, or arbitrary many-layer networks. Replacing them with positive matrices by fiat would invalidate the result.

## 4. Exact two-layer specimen

Use a two-state hidden chain and positive first and second overlapping channels:

$$
P=
\begin{pmatrix}
4/5&1/5\\1/3&2/3
\end{pmatrix},
\quad\pi=(5/8,3/8).
$$

Let the first-layer probability of symbol one at hidden pair $(s,t)$ and the second-layer probability of symbol one at observed pair $(y,w)$ be, respectively,

$$
K(1\mid s,t)=
\begin{pmatrix}
1/5&2/5\\3/5&4/5
\end{pmatrix},
\quad
H(1\mid y,w)=
\begin{pmatrix}
1/6&1/3\\2/3&5/6
\end{pmatrix}.
$$

The zero-symbol probabilities are complements. Exact computation gives

$$
\lambda=(9/20,7/40,1/8,1/4),\quad
C=256/5,\quad
\widehat\kappa=251/261
$$

and lower bounds $c_0=93/250$, $c_1=443/1350$. The certificate is conservative; its value is that **every parameter and inequality can be replayed exactly**. Direct enumeration of both hidden layers independently matches all final-word probabilities tested.

## 5. Sharp noise-restoration comparison with the XOR obstruction

For iid hidden Bernoulli spins with parameter $p\in(0,1)$, let the output be noisy XOR:

$$
Z_i=X_i\oplus X_{i+1}\oplus N_i,
\qquad
N_i\overset{\mathrm{iid}}{\sim}\mathrm{Bernoulli}(\varepsilon).
$$

For every $\varepsilon\in(0,1)$ the edge-labelled transfer matrices on the original binary hidden state are strictly positive:

$$
T_z(s,t)=\pi(t)
\begin{cases}
1-\varepsilon,&s\oplus t=z,\\
\varepsilon,&s\oplus t\ne z.
\end{cases}
$$

The exact projective cross ratio is

$$
C=\left(\frac{\max(\varepsilon,1-\varepsilon)}
{\min(\varepsilon,1-\varepsilon)}\right)^2.
$$

In this case the **sharper, exact** Birkhoff coefficient is $|1-2\varepsilon|$, and the Gibbs log-variation bound becomes

$$
\operatorname{var}_k(\log g)
\le2\left|\log\frac{1-\varepsilon}{\varepsilon}\right|
|1-2\varepsilon|^{k-1}.
$$

At $\varepsilon=1/2$, the output is iid fair Bernoulli. The constants remain finite for every strictly positive noise level, but the contraction degenerates as noise approaches zero or one. At $\varepsilon=0$ or $1$ with biased hidden spins, the known Kari–Taati overlapping-XOR non-Gibbsian obstruction reappears (up to complementing the output).

This is a **quantitative regularization calibration**, not a novel claim about noisy Gibbs transforms.

## 6. Exact replay and implementation boundary

The finite rational implementation is overlapping_transfer_certificate.py; its independent regression is tests/test_csm_overlapping_transfer_certificate.py. The test suite includes:

1. Separate full hidden-path enumeration, including both layers and every shared variable, for words up to length four.
2. Exact stationarity, cylinder probabilities, conditional ratios, cross ratios and positive lower bounds.
3. Log-variation upper bounds over different futures sharing fixed prefixes.
4. Noisy XOR direct microscopic enumeration for five positive noise levels and the fair channel.
5. Rejection of zero/noise-one parameters, nonstationary hidden laws, and structurally zero channels.

A CHAD exact-head local replay at candidate commit 57448f5fe17639627369c040e15e85b0c216f0a4 passed 7 tests. Receipt GCL_CONTROL_BASH_RESULT/1 6f4ee30fd5574466a8e4e290410d668a; independent execution attested=false. Protected CI and final source review must still bind to the **final** candidate head.

The direct certificate uses $d=|S||Y|$ lifted states, $|Z|$ matrices, $O(|Z|d^4)$ exact cross-ratio comparisons and $O(|Z|d^2)$ matrix storage. This is an exact reference evaluator, not a large-scale optimized contraction engine.

## 7. Prior-art/novelty adjudication

- **Külske–Opoku (2008):** posterior metric and Dobrushin methods already provide transformed-Gibbs regularity criteria; a new theorem cannot simply restate uniform posterior uniqueness. [Original arXiv abstract](https://arxiv.org/abs/0711.3764).
- **Chazottes–Ugalde / Fernández–Maillard:** one-dimensional hidden Markov and one-sided-to-two-sided Gibbs bridges are classical; see G0 source register.
- **Kari–Taati (2014):** deterministic overlapping XOR image non-Gibbsianness for biased Bernoulli input is a known exact counterexample. [arXiv original](https://arxiv.org/abs/1311.2319).
- **Yayama (2026, ETDS 46):** necessary-and-sufficient Gibbs image criteria for special factor maps are in scope and require theorem-level concordance, not abstract-only extrapolation. [Published article](https://doi.org/10.1017/etds.2025.10262).

**Novelty verdict for this WP02 theorem:** the principal transfer contraction and Gibbs conclusion are **known mathematics**; the precise two-layer finite certificate is a GCL implementation/reconstruction. An original G2 criterion remains OPEN. A fruitful next test is whether a compositional **non-strict, support-aware block-contraction** rule can be both decidable from the typed network and quantitatively sharper than the full labelled-matrix semigroup criteria already studied. Establish a source-grounded theorem gap before proceeding to public originality or certification.
