# CSM-G2-WP11 — effective suffix-grid witness synthesis and quantitative complexity

**Status:** internally proved candidate quantitative synthesis theorem, exact reference implementation and sharp obstruction family. Originality UNADJUDICATED. No MATHCERT, independent mathematical certification or public claim promotion. Continues WP10, PR #3694, merged at bf29fae53929610b6b19f8e939cf64b3dab24ba2; three unchanged artifacts read back at protected base 785b184ede403ade37863752eb131fa8150c213b.

## 1. Structured certificate language

Use WP10's exact minimal predictive quotient, dimension $d$, alphabet size $m$, terminal column $e_0$, stationary row $\ell$, rational labelled matrices $M_a$. Let $k=d-1$. Actual normalized predictive states have first coordinate one and remaining coordinates in $[0,1]$:

$$
x_u=\frac{\ell M_u}{p(u)},\qquad (x_u)_i=\frac{p(uv_i)}{p(u)}.
$$

Write $F_A(x)=xA/(xA)_0$ when the denominator is positive. Assume full support. For fixed positive block length $s$ and dyadic radius $\delta=2^{-j}$, integer $j\ge2$, round each free coordinate of each suffix state $x_w$, for words of length $s$, down to the nearest multiple of $\delta/2$, obtaining $z_w$. Let $B$ be the unit tangent cube in maximum norm. Form

$$
P(s,\delta)=\mathrm{conv}\bigcup_{|w|=s}(z_w+\delta B).
$$

The generating set $V$ consists of deduplicated rational box corners. In one free dimension retain the hull endpoints; in zero free dimensions retain the unique normalized point. No numerical hull approximation is required.

Every $x_w$ belongs to its box because rounding error is at most $\delta/2$. Stationarity yields $\ell=\sum_{|w|=s}p(w)x_w$, hence $\ell\in P$. For each vertex, check positive one-letter likelihoods and positive block denominators; compute the WP10 secant bound $L_{M_w}$ and require it strictly below one. Also require each block vertex image to lie strictly inside its own box:

$$
\max_{i\ge1}|F_{M_w}(v)_i-(z_w)_i|<\delta .
\tag{1}
$$

For $k=0$ the maximum is zero. By the positive-denominator convex-image identity, the entire convex hull maps into the corresponding box, hence into $P$. This is a WP10 witness: positive Hölder conditionals and an exponentially summable two-sided Gibbs interaction follow. These are finite rational inequalities, not extrapolation from a sampled trajectory. The witness can be replayed using only the two integers $s,j$ and the exact model identity.

## 2. Quantitative existence and termination

Assume the uniform WP07 regularity bounds in predictive coordinates:

$$
p(uv)\ge b\,p(u)p(v),\quad 0<b\le1,
$$

$$
\max_{i,j}|(M_w)_{ij}|\le Jp(w),
$$

$$
\max_{i,j,k,l}|(M_w)_{ik}(M_w)_{jl}-(M_w)_{il}(M_w)_{jk}|
\le Hp(w)^2\theta^{|w|},\quad 0<\theta<1 .
$$

Here $J>0,H\ge0$; the minor bound is needed only for nonempty words. These are hypotheses of the conditional resource theorem, not estimates inferred from finitely many words. They exist for every positive Hölder finite-state law by WP07. One constant is directly computable: take the invertible Hankel slice $G$ for independent left probes and the fixed predictive probes. Each entry of $G M_w$ is $p(u_iwv_j)\le p(w)$ by cylinder inclusion and stationarity. Therefore $J=\|G^{-1}\|_\infty$ is a valid uniform entry bound, computed by exact Gaussian elimination. The remaining constants need not be known in advance.

Let $K$ be the closed convex hull of all reachable normalized rows and $K_t=K+tB$. It is compact since free predictive coordinates lie in $[0,1]$. Since the rounding error is at most $\delta/2$ and the box radius is $\delta$, we have $P(s,\delta)\subset K_{2\delta}$. For $k\ge1$ choose the least integer $j\ge2$ such that

$$
\delta=2^{-j}\le\min(1/4,b/(8kJ)).
\tag{2}
$$

For $x\in K_{2\delta}$, comparison to a point of $K$ within distance $2\delta$ gives

$$
(xM_w)_0\ge (b-2\delta kJ)p(w)\ge (b/2)p(w)
$$

for every word. Also $\sum_i|x_i|\le1+2k$. Using the WP10 identity for $A=M_w$,

$$
A_{ij}-A_{i0}F_A(y)_j=
\frac{\sum_l y_l(A_{ij}A_{l0}-A_{i0}A_{lj})}{(yA)_0},
$$

each numerator is bounded by $(1+2k)Hp(w)^2\theta^{|w|}$. The inner denominator and outer secant denominator are each at least $(b/2)p(w)$. Summing over $k$ tangent coordinates gives

$$
L_{M_w}\le D\theta^{|w|},\qquad D=4k(1+2k)H/b^2.
$$

This bound holds uniformly in the generated polytope. Choose any positive integer $s$ with

$$
D\theta^s<\delta/4.
\tag{3}
$$

If $D=0$ take $s=1$; otherwise one sufficient integer is

$$
\max\left(1,1+\left\lfloor
\frac{\log(4D/\delta)}{-\log\theta}
\right\rfloor\right).
$$

The implementation uses exact rational comparisons rather than floating logarithms. Since $\ell\in P$ and every vertex is within distance at most $1+2\delta\le2$ of $\ell$,

$$
\|F_{M_w}(v)-x_w\|_\infty
\le L_{M_w}\|v-\ell\|_\infty<\delta/2.
$$

Adding rounding error at most $\delta/2$ proves (1) strictly. All likelihood and contraction inequalities also pass. Dimension one is immediate: the law is iid, with positive symbol probabilities and zero tangent contraction.

**Theorem:** Every rational finite-state full-support positive Hölder law admits a structured suffix-grid witness with these explicit sufficient bounds. Conversely every passing witness proves positive Hölder regularity by WP10. This is a complete positive-certificate language, without arbitrary polytope enumeration, conditional on WP07/WP10's internally proved candidate results. No independent certification is asserted.

## 3. Vertex, word and bit complexity

There are at most $m^s$ block words, each contributing at most $2^k$ corners. Rounded coordinate indices run from 0 to $2/\delta$; corners shift indices by 2. Hence

$$
|V|\le\min\{2^k m^s,(2/\delta+5)^k\}.
\tag{4}
$$

The bound applies also to the actual number of extreme vertices. Grid coordinates use bit length $O(j+1)$. Dependence on observable dimension replaces dependence on microscopic lift dimension.

Maintain exact distinct normalized products $\widetilde M_w=M_w/p(w)$. If two agree, they have identical projective maps, secant bounds and suffix centers, and their one-letter extensions remain equal after normalization. Keep one representative per matrix and extend each representative by every label. A zero denominator yields a concrete zero-probability word; negative mass is an invalid-realization error, not a forbidden-word certificate. Induction gives complete enumeration of distinct products. No approximate merging is used.

Write $W_s$ for the number of distinct normalized products. A dense extension step costs $O(mW_{s-1}d^3)$ rational operations plus exact hashing. A candidate radius generates at most $2^kW_s$ corners. After deduplication, positivity, secant and box checks cost $O(m|V|d+W_s|V|d^2)$ rational operations, plus corner generation and sorting. No general convex-hull membership solver is needed in the synthesis loop. Current products, vertices and representative words occupy $O(W_s d^2+|V|d+sW_s)$ entries, with previous-level storage temporarily also needed. This excludes quotient construction. Worst case $W_s=m^s$.

Clear denominators in the fixed matrices by a common integer and similarly in $\ell$. If resulting numerators and denominators use at most $B_0$ bits, dense integer products of length $s$ have entry bit length $O(s(B_0+\log d))$. Dividing by the exact stationary word weight gives normalized entries of bit length $O((s+1)(B_0+\log d))$, regardless of the small raw word probability. The grid coordinate bit cost is $O(j+1)$. Each rational arithmetic operation and the finite secant calculations therefore have polynomial bit cost in $d,s,B_0,j$; the word and vertex counts can still be exponential. This is not a polynomial-time bound in the input model description.

The algorithm searches successive block lengths and dyadic radii with explicit block, grid-bit, product and vertex budgets. It returns a certified witness, a forbidden word, or undecided with the exhausted boundary. Rejected candidates and budget exhaustion never imply non-Gibbsianness. Dovetailing increasing all budgets terminates for every positive Hölder rational law by (2)–(4). A successful witness needs no advance knowledge of $b,H,\theta$. The conditional resource theorem provides a sufficient budget when valid constants are known.

## 4. Sharp fixed-dimension block obstruction

For integer $N\ge1$ put $\varepsilon=1/(1+2^N)$ and take

$$
A=\begin{pmatrix}1/2&0\\0&1/4\end{pmatrix},\quad
B=\frac14\begin{pmatrix}\varepsilon&1-\varepsilon\\
\varepsilon&1-\varepsilon\end{pmatrix},\quad
C=\begin{pmatrix}1/8&1/8\\1/4&1/4\end{pmatrix}.
$$

Their sum is positive stochastic with stationary row $(2(1+\varepsilon)/5,(3-2\varepsilon)/5)$. All words have positive mass; reachable and observable spaces have dimension two since the resets give distinct rows and the $A$ likelihood distinguishes columns. The normalized hidden posterior is $(t,1-t)$. Observing $B$ resets $t$ to $\varepsilon$; observing $C$ resets it to $1/2$. The initial and reachable $t$ values lie in $[\varepsilon,1]$, and observing $A$ increases $t$. Every one-symbol likelihood on this interval is at least $1/4$.

Every word containing either reset has constant projective map. For $s$ copies of $A$ the derivative is

$$
\frac{dF_{A^s}(t)}{dt}=\frac{2^s}{(1+(2^s-1)t)^2}.
\tag{5}
$$

On the invariant interval the supremum is at $\varepsilon$ and decays exponentially in $s$; WP10 sufficiency implies positive Hölder regularity. The minimal predictive coordinate for probe $A$ is $(1+t)/4$, an invertible affine rescaling preserving the scalar Lipschitz constant.

Every WP10 witness contains all reachable states by stationarity padding, including the two post-reset states and the segment joining them. Its block Lipschitz bound must be at least the one-sided derivative in (5) at $\varepsilon$. This derivative is at least 1 exactly when $2^{s/2}\le2^N$ for $s>0$. No strict contraction is possible for $s\le2N$. For $s=2N+1$, the interval $[\varepsilon,1]$ has positive likelihoods, block invariance and strict secant contraction: in one dimension the WP10 bound equals determinant magnitude divided by squared minimum denominator, the supremum derivative. Reset blocks have zero bound. Thus the optimum block length over WP10 witnesses is **exactly $2N+1$**. To obtain strict interior invariance, slightly enlarge both endpoints rationally; continuity preserves strict contraction and positivity, and both reset points and the fixed point 1 then lie in the interior.

Dimension and alphabet remain 2 and 3 while the optimum diverges with $N$ and coefficients have bit length $O(N)$. This is a linear-in-bit-length obstruction for the particular secant norm, not a complexity lower bound for all algorithms for Gibbs regularity or for the number of vertices. Two vertices suffice for the optimal witness. The structured grid search is more conservative.

## 5. Exact synthesis evidence

No supplied vertices are used. The prior WP10 verifier checks the synthesized witnesses in the regression suite.

| Model | Observable dimension | Block | Radius | Generating vertices | Exact contraction |
| --- | ---: | ---: | ---: | ---: | --- |
| WP10 balanced coupled overlap | 2 | 3 | 1/16 | 2 | 243/256 |
| Balanced three-state coupled overlap | 3 | 4 | 1/128 | 20 | 11019472/11236473 |
| WP09 length-three parity, iid input probability 1/256 | 4 | 2 | 1/16 | 8 | 68300012320775/273825722925056 |
| Slow reset, N=2 | 2 | 7 | 1/64 | 2 | 8192/18225 |
| Slow reset, N=4 | 2 | 11 | 1/256 | 2 | 33554432/107391769 |
| Fair iid | 1 | 1 | 1/4 | 1 | 0 |

The new balanced three-state Markov source has uniform stationary row and transition diagonal entries 1/2, off-diagonal entries 1/4. Every adjacent input pair has probability at least 1/12. Binary output-zero probabilities on ordered adjacent input pairs are

$$
\begin{pmatrix}3/4&1/4&1/2\\1/2&3/4&1/4\\1/4&1/2&1/4\end{pmatrix}.
$$

A nonzero minor proves non-product pair likelihood; adjacent windows share an input symbol. The output is non-iid with minimal dimension three. Direct source-window summation independently checks lifted cylinder probabilities. The witness has five grid centers, 20 generating corners, strictly positive slack and likelihood lower bound 7/16.

For the slow family with $N=4$, length 11 uses only 109 normalized products instead of 177147 raw words. The optimum unrestricted block is 9, so the grid result is not optimal. With $N=2$, 44 products replace 2187 words at length 7. The singular-gap hostile control returned undecided through block 6 and grid bit 6, as appropriate for a positive semidecision. An alternating deterministic control returned an exact zero cylinder. The WP09 non-iid rare parity model of minimal dimension five was **not certified within block 6, grid bit 8, product budget 4096 and vertex budget 512**. WP09 proves it regular by a different witness; this is a practical limitation of the current coordinate/grid search, not a mathematical obstruction.

Preliminary exact parameter captures: 7ad0edfecb38402b87c6edffc4c51ab0 at d2efdf944cfb0f6a7f707c56fe91ebe71c9b635c; 659a9939d67f474cb3f703b5a26cebd1 at edd5c212e209e19442a323611aaabb38c96bc92c. Seven exact tests passed at 62fa0d38c1d087259ab1e4c8f18aca5ca4f1ca1c, local capture 44b6e3c2d4ac45b5a1ba21d541812172. Final strengthened replay required. Independent execution attestation flags are false.

## 6. Prior art and scope

Invariant polyhedral cones are established realization theory. Brian D. O. Anderson, [Realization problem for hidden Markov models](https://doi.org/10.1007/pl00009846), Mathematics of Control, Signals and Systems 12 (1999), 80–120, develops cone existence and construction algorithms (institutional abstract checked; full paper replay open). M. Vidyasagar, [The Realization Problem for Hidden Markov Models: The Complete Realization Problem](https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc05/pdffiles/papers/0862.pdf), CDC-ECC 2005, Section V, Definition 2, Theorem 5, Lemma 2, gives ultra-mixing and Hankel-based realization criteria with additional cluster-point assumptions. Extracted primary text inspected; PDF screenshot cache missed. This closely precedes WP10's realization mechanism. Guglielmi and Protasov, [Invariant polytopes of linear operators](https://arxiv.org/abs/1502.01192), develops invariant polytope algorithms for joint spectral radius and regularity. These concern norms for linear products rather than directly normalized probability projective maps; full comparison remains required. Their 2024 Computing the spectral gap of a family of matrices abstract describes a joint spectral radius/second Lyapunov exponent quantity, not WP07's uniform wordwise relative singular gap.

The specific result is a constructive consequence of the WP07/WP10 candidate regularity equivalence: explicit grid witness size and block bounds conditional on observable margins, replayable rational synthesis with exact product-equivalence reduction, and a sharp fixed-dimension block obstruction. Grid approximation, stationarity, exterior estimates and invariant polytope methods are established tools. Originality of the combination remains UNADJUDICATED; no new general realization algorithm, general decidability, computational tractability or independent formal verification is claimed.

**Next boundary:** CSM-G2_EFFECTIVE_MARGIN_DISCOVERY_AND_ADAPTIVE_SYNTHESIS_OPEN. Obtain efficiently verifiable quantitative margins from input models, improve poorly conditioned predictive coordinates and replace uniform grid/word enumeration with certified adaptive covers. Seek bounds in terms of input bit size and lower bounds beyond the particular secant norm. Negative-instance decision and slower-decay Gibbs regularity remain open. Canonical tracker #3136 stays open.
