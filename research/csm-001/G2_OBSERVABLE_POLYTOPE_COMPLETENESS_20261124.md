# CSM-G2-WP10 — complete finite predictive-polytope witnesses and positive realization

**Status:** internally proved candidate equivalence for positive exponential conditional regularity, with exact rational implementation and balanced overlapping example. Originality UNADJUDICATED; no MATHCERT or independent mathematical certification. Continues WP07–WP09.

## 1. Minimal predictive coordinates

Let a stationary full-support finite-alphabet process have rational finite nonnegative transfer data. Write $p(u)$ for its cylinder probabilities. The WP04 actual-word Hankel construction produces a minimal rational linear representation $p(w)=\ell M_w r$ of dimension $d$. Choose actual future probes $v_0=\varnothing,v_1,\ldots,v_{d-1}$ whose Hankel columns on the reachable row span are independent, and actual independent left probes $u_i$. In these predictive coordinates the terminal column is $r=e_0$ and the stationary row has first coordinate 1. For every finite history $u$ the normalized row is

$$
x_u=\ell M_u/p(u),\qquad
(x_u)_j=p(uv_j)/p(u).
$$

The coordinate matrices are computed by the exact linear systems $HM_a=H_a$ with $H(i,j)=p(u_i v_j)$ and $H_a(i,j)=p(u_i a v_j)$. The intertwining holds on the entire reachable span because the probes separate its observable quotient. In particular signed entries in $M_a$ are allowed; no microscopic nonnegativity claim is made for the coordinate matrices.

Let $e_0$ be the first coordinate column, and put $Q_*=\sum_a M_a$. Stationarity and cylinder consistency imply $\ell Q_*=\ell$ and $Q_*e_0=e_0$, by minimality. Work on the affine plane $X=\{x:x_0=1\}$ with the maximum norm on the remaining coordinates. For a matrix $A$ let

$$
F_A(x)=\frac{xA}{(xA)_0}.
$$

If the denominator is positive on a convex hull, the image of that hull is the convex hull of the normalized vertex images: the barycentric weights are reweighted by the positive denominators. This identity also holds for signed matrices.

## 2. Finite rational certificate

Supply a rational full-dimensional polytope $P=\mathrm{conv}(V)$ in $X$, containing $\ell$, and a positive integer block length $s$. Require one-symbol non-nullness on the entire vertex set:

$$
c=\min_{v\in V,a}(vM_a)_0>0.
$$

For every word $w$ of length $s$ set $A=M_w$ and require

$$
d_A=\min_{v\in V}(vA)_0>0,\qquad
F_A(v)\in P\quad(v\in V).
$$

Finally compute the finite secant bound

$$
L_A=
\frac{1}{d_A}
\max_{v\in V}\max_{j\ge1}
\sum_{i\ge1}|A_{ij}-A_{i0}F_A(v)_j|,
\qquad
\eta=\max_{|w|=s}L_{M_w}<1.
\tag{1}
$$

In dimension one the tangent norm and maximum are zero. Every check is exact rational arithmetic: convex membership can be verified by rational barycentric coefficients, or determined by finite enumeration of affinely independent subsets of at most $d$ vertices (Caratheodory). No eigenvalue approximation or assumed positivity of the reduced matrices is required.

The identity

$$
F_A(x)-F_A(y)
=\frac{(x-y)A-((x-y)A)_0 F_A(y)}{(xA)_0}
$$

proves the Lipschitz bound $L_A$ on the entire polytope. Indeed $x-y$ has zero first coordinate, the absolute column-sum expression is the induced tangent maximum-norm bound, and the convexity of that expression in $F_A(y)$ bounds it by its largest value at a normalized vertex image. Thus (1) is an all-state bound, not a sampling estimate.

### Sufficiency and explicit rate

Complete-block invariance implies all normalized states at lengths divisible by $s$ belong to $P$. For a word $u$ of arbitrary length, pad its left side by a length $t$ so $|u|+t$ is divisible by $s$. Stationarity gives

$$
x_u=\sum_{|v|=t}\frac{p(vu)}{p(u)}x_{vu}.
$$

This convex combination belongs to $P$. Hence every finite conditional likelihood $p(ua)/p(u)$ is at least $c$.

For histories with a shared suffix $w$ of length $n$, absorb the initial remainder of that suffix into the preceding histories, then apply its complete blocks. The normalized states differ by at most

$$
\mathrm{diam}(P)\eta^{\lfloor n/s\rfloor}.
$$

Each one-symbol likelihood is linear on $X$ with maximum-norm Lipschitz constant at most $J=\max_a\sum_{i\ge1}|M_a(i,0)|$. Therefore the log-conditional oscillation is bounded by

$$
\frac{J\,\mathrm{diam}(P)}{c}\eta^{\lfloor n/s\rfloor}.
\tag{2}
$$

This yields a uniform limit of forward conditional probabilities on all infinite pasts, positive by the bound $c$; martingale convergence identifies the conditional version. For $\eta=0$ interpret the bound as zero after one full block and the finite constant for shorter suffixes. WP07's relative factorization characterization applied in reversed time gives its all-word quasi-Bernoulli and relative factorization bounds for the original law as well (reverse words and exchange the two exterior contexts). Thus the reverse conditionals are also positive Hölder, and WP07's direct interval construction gives a two-sided exponentially summable Gibbs interaction.

This proof does not require a common microscopic pivot, strict positivity of any original transfer, invertibility, or concentration in a rare history. It does require the full observable quotient; treating an arbitrary nonminimal hidden representation as minimal may introduce permanent invisible noncontracting directions.

## 3. Completeness of finite witnesses

**Theorem.** For every rational stationary finite-state full-support law, positive exponentially regular conditional probabilities are equivalent to existence of the finite rational certificate above. In fact the certificate can be chosen so every complete-block image is strictly inside $P$ relative to $X$. In addition the law admits an equivalent strictly positive rational labelled-transfer representation, on the original alphabet, without grouping the output into blocks.

We prove the necessity of the witness first. By WP07 positive exponential conditional regularity gives constants $b>0$, $J_0,J_1<\infty$, $0<\theta<1$ with

$$
p(uv)\ge b p(u)p(v),\qquad
\|M_w\|\le J_0 p(w),\qquad
\|\bigwedge^2 M_w\|\le J_1p(w)^2\theta^{|w|}.
\tag{3}
$$

These are in the minimal representation; all finite-dimensional norms are equivalent. The middle bound follows from the actual-word Hankel slice and is independent of positivity in these coordinates. The same assumptions hold if one begins with forward conditionals, by reversal.

Let $K$ be the closed convex hull of all $x_u$. It is compact since the predictive coordinates are probabilities. Minimality ensures its affine span is $X$; linear independence of reachable rows implies affine independence of their normalized versions. The quasi-Bernoulli bound and linearity give

$$
xM_we_0\ge b p(w)\qquad(x\in K).
$$

Each map $F_{M_w}$ preserves $K$, by the reachable-state update, normalized convexity, and continuity at positive denominators. There is a fixed $\delta>0$ such that all word denominators remain at least $(b/2)p(w)$ throughout the closed convex neighborhood $K_\delta=K+\delta B$, where $B$ is the unit tangent maximum-norm ball. Indeed, the middle inequality of (3) bounds perturbation of the denominator by a constant times $\delta p(w)$ uniformly in all words.

We now bound the actual finite expression (1) uniformly for every finite vertex set inside $K_\delta$. For $y\in K_\delta$, write

$$
A_{ij}-A_{i0}F_A(y)_j
=\frac{\sum_k y_k(A_{ij}A_{k0}-A_{i0}A_{kj})}{(yA)_0},
\qquad A=M_w.
$$

Every expression in parentheses is zero or, up to sign, a two-by-two minor. The last bound of (3), the uniform denominator lower bound, and boundedness of $y$ imply that each numerator entry after division is bounded by a fixed constant times $p(w)\theta^{|w|}$. Dividing by $d_A\ge (b/2)p(w)$ and summing the finitely many tangent coordinates gives

$$
L_{M_w}\le D\theta^{|w|}
\tag{4}
$$

with $D$ independent of the word and the chosen vertices in $K_\delta$. The secant argument also gives the same estimate (with a fixed constant) for the Lipschitz norm on the entire $K_\delta$.

Choose a rational full-dimensional polytope with $K_{\delta/2}\subset P\subset K_\delta$. Existence follows by taking the convex hull of the corners of finitely many sufficiently small rational grid boxes meeting the inner neighborhood. The entire hull lies in the outer convex neighborhood. This works in the affine plane $X$ with its free rational coordinates. For dimension one take the singleton. The stationary state belongs to $K$, and one-letter likelihoods on $P$ have the required uniform lower bound. Choose $s$ large enough that the right side of (4), and the corresponding Lipschitz bound on $K_\delta$, are below $1/4$. For any $x\in P$, choose $y\in K$ within distance $\delta$. Its block image lies in $K$, and the image of $x$ lies within distance $\delta/4$ of that image. All complete-block images therefore lie in $K_{\delta/4}$, strictly inside $P$. The finite tests succeed. QED.

This is an existential completeness theorem for exact witnesses, not a universal runtime bound. Rational polytopes and block lengths can be enumerated, and verification terminates for each candidate. Dovetailing therefore semidecides the positive class, but is not claimed to terminate for negative instances. No decision procedure for arbitrary slower-decay Gibbs interactions follows. The necessity proof also applies over real coefficients with real certificates, but the algorithmic exactness claim here concerns rational data.

## 4. Strictly positive rational realization on the original alphabet

The following proof strengthens the conclusion beyond the positive realization of a blocked process. Let $P_0=P$ be a full-dimensional rational polytope from Section 3, all length-$s$ images of which lie strictly inside $P_0$. Every word denominator is positive on $P_0$ by the proof above.

For $1\le j\le s$ let

$$
C_j=\mathrm{conv}\bigcup_{|v|=j}F_{M_v}(P_0).
$$

These sets are compact, and $C_s$ lies strictly inside $P_0$. Every one-letter denominator is positive on $C_j$ for $j<s$: on $F_{M_v}(P_0)$ it is the ratio of two positive word denominators, and on the convex hull it is linear. The normalized convex-image identity gives $F_{M_a}(C_j)\subset C_{j+1}$.

Choose rational polytopes $P_{s-1},P_{s-2},\ldots,P_1$ in that backward order, each containing the corresponding $C_j$ strictly inside it and sufficiently close to it that all one-letter denominators remain positive and each $F_{M_a}(P_j)$ lies strictly inside $P_{j+1}$, where $P_s=P_0$. This is possible by compactness, continuity and the strict interior inclusion of $C_{j+1}$ in the already selected polytope. The original $P_0$ satisfies $F_{M_a}(P_0)\subset C_1\subset\mathrm{int}(P_1)$. If $s=1$, use $P_0$ directly.

Take $P_*=\mathrm{conv}\bigcup_{j=0}^{s-1}P_j$. All one-letter denominators are positive on it. Normalized convexity implies every one-letter map carries $P_*$ strictly inside itself: each image is a convex combination of points lying in the relative interior of $P_*$. The initial row remains in $P_*$. This resolves the apparent obstruction from one-letter expansion of the original block witness.

Let $v_i$ be the finitely many rational generating vertices of $P_*$. Since $F_{M_a}(v_i)$ lies in the relative interior, it admits strictly positive rational barycentric weights $\lambda_{iaj}$ on **all** vertices. To see this, let $\bar v$ be the average of the vertices and take sufficiently small positive rational $t$; the adjusted point $(F_{M_a}(v_i)-t\bar v)/(1-t)$ is still in the polytope, has rational nonnegative weights by the rational linear system, and adding $t$ times the uniform weights makes every coefficient positive.

Define a new labelled matrix on the vertex states by

$$
T'_a(i,j)=(v_iM_a)_0\lambda_{iaj}.
$$

Every entry is strictly positive and rational. With $V_*$ the matrix whose rows are $v_i$,

$$
T'_a V_*=V_* M_a,\qquad V_*e_0=\mathbf1.
$$

The sum $Q'=\sum_a T'_a$ is positive row-stochastic because $Q_*e_0=e_0$. Let $\pi'$ be its unique stationary row, positive and rational by finite linear equations. Choose a convex weight row $\mu$ with $\mu V_*=\ell$. Since $\ell Q_*=\ell$, for every $n$ we have $\mu(Q')^n V_*=\ell$. Positivity of $Q'$ gives convergence to $\pi'$, so $\pi' V_*=\ell$. Intertwining now yields $\pi' T'_w\mathbf1=p(w)$ for every word. This proves strict positive realization on the original alphabet.

Conversely a strictly positive labelled-transfer representation has positive exponential conditional regularity by the established positive-transfer theorem (WP01). Thus for the scoped rational full-shift laws we have an equivalence between positive Hölder conditionals, finite observable polytope witnesses, and existence of an equivalent strictly positive labelled-transfer realization. The previously proposed search for a positive-Hölder Gibbs law with no equivalent strictly positive labelled representation is therefore refuted within this scope, subject to specialist proof review. This does not exclude non-Hölder Gibbs laws or constrain realization dimension. A strictly positive labelled transfer is an edge-emission representation, not necessarily a state-emission HMM in a prescribed dimension.

### Consequence for composition

For every specified finite-range stochastic kernel of WP09 whose output has full support, construct its exact finite history lift and then this minimal quotient. If the output is positive Hölder, some finite polytope witness exists; if a witness passes, the output is positive Hölder. This provides a complete positive certificate language for the exponential class, regardless of the input's rare-history statistics. It is not unconditional Gibbs preservation, an efficient uniform synthesis algorithm, or a certificate for all kernels without inspecting the composition. The earlier XOR obstruction still applies.

## 5. Balanced genuinely overlapping example with persistent invisible modes

Take a binary Markov input with stationary law $(1/2,1/2)$ and transition

$$
Q=\begin{pmatrix}3/4&1/4\\1/4&3/4\end{pmatrix}.
$$

Every adjacent pair has mass at least $1/8$; the source is non-iid. Realize it microscopically on states $(a,i)$, where $a$ is the observed bit and $i$ is an internal parity bit. Update the parity bit by a flip exactly on transition 11, leaving it unchanged otherwise. The transition probabilities for the observed bit are those of $Q$ independent of the internal bit. The four-state chain has uniform stationary row, is irreducible (the 11 transition can flip the parity and either bit can be reached), and has self-loops. Thus it is primitive; the additional bit is not a disconnected phase.

Apply the two-site overlapping stochastic readout with zero-output probabilities

$$
H(0\mid00)=3/4,\qquad H(0\mid11)=1/4,
\qquad H(0\mid01)=H(0\mid10)=0,
$$

and complementary probabilities for output one. Adjacent output windows share one input bit. This is a coupled single-track adjacent readout, not a sitewise mixture or independent staggered tracks.

After exact history lift and removal of zero-stationary states, there are four microscopic states. The output is non-iid. Along all-zero words, the two states with observed bit zero each have a self-loop of weight $9/16$ and do not communicate. The other two states have a weighted flip of weight $3/16$. Hence the two largest singular values of every zero-word microscopic transfer are equal: the raw exterior-square spectral ratio cannot decay at all.

Nevertheless the actual-word Hankel quotient has dimension two, with probes the empty word and symbol zero. Exact matrices in these coordinates are

$$
\ell=(1,3/8),\quad
M_0=\begin{pmatrix}0&-27/256\\1&3/4\end{pmatrix},
\qquad
M_1=\begin{pmatrix}1&75/256\\-1&-1/4\end{pmatrix}.
$$

Use the rational interval $P=\{(1,x):3/10\le x\le9/16\}$. The four length-two matrices preserve this interval with positive denominators. All one-letter likelihoods are at least $3/10$. The exact finite secant expression (1) gives

$$
\eta=225/289,\qquad
\mathrm{diam}(P)=21/80,\qquad J=1.
$$

Therefore the forward log-conditional variation bound at shared suffix length $n$ is

$$
\frac78(225/289)^{\lfloor n/2\rfloor}.
$$

The one-step contraction test fails for this interval, but the two-step test succeeds. Both quotient generators are invertible; thus no word has rank one in any equivalent representation by the observable Hankel slice rank argument of WP07. The source-concentration criterion of WP09 cannot apply: for a retained anchor, each unlabelled lifted state has stationary mass $1/4$, hence the sum of maximum nonanchor column entries of any stochastic block power is at least $3/4$. The pivot lower bound is at most 1, so $e\ge3/4$. This violates the required $e<1/2$ for every length and every anchor.

The raw labelled representation retains structural zeros and invisible peripheral modes. This demonstrates actual benefit from quotienting, not just recoding a positive model in its original hidden coordinates. It does not establish absence of a positive realization; the theorem explicitly constructs one.

For example use the enlarged predictive interval $9/32\le x\le21/32$, whose one-letter images lie strictly inside it. Exact rational synthesis from its two vertices produces

$$
\pi'=(3/4,1/4),\quad
T'_0=\frac1{128}\begin{pmatrix}27&9\\15&69\end{pmatrix},
\qquad
T'_1=\frac1{128}\begin{pmatrix}85&7\\33&11\end{pmatrix}.
$$

The exact intertwiner and stationary-row identities are verified; word probabilities are therefore identical at all lengths, independently of finite regression comparisons. All entries are positive. This supplies a concrete strictly positive presentation of a coupled model whose original microscopic representation cannot satisfy full-state spectral separation.

## 6. Evidence and prior-art boundary

Code: observable_polytope_certificate.py. Tests: tests/test_csm_observable_polytope_certificate.py. The implementation constructs the exact minimal quotient from actual-word bases, checks the intertwining on all spanning rows, computes finite vertex secant bounds, and tests convex membership with exact rational linear equations. A supplied strictly invariant one-step polytope can also be converted to a positive realization by bounded rational barycentric search; failure of a supplied witness or budget is not a negative realizability result. The general existence theorem is not implemented as an unbounded search.

Seven local tests passed at exact candidate bc0bf2fc18b24d7613eea6b96a4c5d56645416f8, local capture eaf2842725b84a00a7492220686f8ee6 (independent attestation false). They cover independent microscopic overlapping cylinder sums, signed minimal quotient, all-word rank checks at finite replay lengths plus analytic invertibility, exact two-block constants, suffix bounds, failed one-step and concentration checks, singular obstruction and iid controls, rational hull membership, positive realization and exact intertwiner, and finite cylinder agreement through length seven. Final source gate and native CI must bind the final candidate.

**Close prior art:** Heller's invariant polyhedral cone theorem, Jaeger's observable operator models, and the positive-realization literature already establish finite Hankel-space realization and invariant-cone mechanisms. In particular M. Vidyasagar, [The Complete Realization Problem for Hidden Markov Models: A Survey and Some New Results, manuscript dated 23 March 2009](https://personal.utdallas.edu/~mxv091000/Research/hmm-full.pdf), Definition 6, Lemma 9.4, Theorem 9.2 and Lemma 9.5 are directly relevant. Definition 6 uses a uniform conditional-independence error with a fixed-length probe; Lemma 9.4 obtains rank-one approximation of normalized word matrices. Theorem 9.2 and Lemma 9.5 use additional finite-cluster-point/interior conditions in their realization results. Their normalized rank-one approximation and polyhedral-cone construction are close predecessors, not GCL discoveries. Our stronger exponential and quasi-Bernoulli hypotheses give a uniform thickened convex set, avoiding a finite-cluster-point assumption for this scoped class. Whether the finite secant witness equivalence and strictly positive edge realization theorem are already established elsewhere is **unadjudicated**; published-edition concordance and independent source-proof replay remain open. PDF extracted theorem text was inspected; the web screenshot service returned cache misses. Do not claim visual page verification. Birkhoff positivity, actual-word minimality, and barycentric realization are established mathematics.

**Disposition:** exact finite witness criterion on the observable quotient, existential completeness for positive Hölder full-shift rational finite-state laws, strictly positive rational realization equivalence, and genuinely overlapping balanced non-iid example, internally proved. Novelty remains UNADJUDICATED. No public claim promotion.

**Next boundary:** CSM-G2_EFFECTIVE_WITNESS_SYNTHESIS_AND_COMPLEXITY_OPEN. Determine quantitative bounds for witness size and block length, develop an effective finite-budget synthesis algorithm beyond supplied polytopes, and audit the precise positive-realization equivalence against earlier realization theory. Unrestricted negative-instance decision and the slower-decay quasilocal class remain open. Keep canonical issue #3136 open.
