# CSM-G2-WP17 — conserved-sector exchange and observation comparison

Internally derived candidate, originality UNADJUDICATED, no MATHCERT. Continues WP16 protected merge ec2c99a2c0be024d0134fbdc98655b763061b687. Scope: fixed-time equilibrium of binary conservative exchange, not full space-time PCA smoothing.

## Sector and exchange coupling

For N sites and fixed particle count K use the canonical law

$$
\mu_{K,w}(x)=Z^{-1}\mathbf1_{\sum_i x_i=K}\prod_i w_i^{x_i},\qquad 0<a\le w_i\le b,\quad R=b/a.
$$

A bond heat bath leaves 00 and 11 unchanged and selects 10 or 01 with probabilities proportional to the positive site weights. Detailed balance follows from conditional resampling. On any connected finite graph adjacent transpositions generate all permutations, so the chain is irreducible within each count sector; individual-site heat baths are identity kernels. Distinct sectors never communicate.

On the complete graph choose unordered bonds uniformly. Use half-Hamming distance d. For states at distance one differing at i,j, couple the second bond selection by interchanging i,j. On bond {i,j} the conditional law is identical, so coalesce. For each other site l exactly one of the two bonds involving l and i,j permits coalescence when both chains swap (the other has equal bits in both). Use a common uniform random variable to couple swap probabilities. Both swap with probability at least 1/(1+R) on the coalescing-capable bond; if only one or neither swaps, distance remains one. Bonds avoiding i,j leave distance one under identical resampling. Thus for M=N(N-1)/2,

$$
\mathbb E d(X',Y')\le 1-\alpha,\qquad
\alpha=\frac{1+(N-2)/(1+R)}{M}.
$$

For arbitrary pairs connect them by a shortest swap path and glue the adjacent couplings by finite conditional disintegration. The triangle inequality yields expected distance at most (1-alpha)d; iteration gives Wasserstein contraction and TV at most min(K,N-K)(1-alpha)^t for arbitrary starting laws in the same sector. This auxiliary complete-graph chain is not a uniform mixing claim for local physical exchange.

## Canonical covariance bound

Write e_r for elementary symmetric polynomials, with e_0=1 and out-of-range terms zero. Excluding i,j, direct expansion of Z gives

$$
-\mathrm{Cov}(X_i,X_j)=\frac{w_iw_j}{Z^2}(e_{K-1}^2-e_{K-2}e_K).
$$

Nonnegativity follows from Newton's inequalities. To compare j and l, delete i,j,l and write A=e_(K-1), B=e_(K-2), C=e_(K-3), D=e_K on the remaining sites. The bracket after adding weight t is

$$
P(t)=(A^2-BD)+t(AB-CD)+t^2(B^2-AC).
$$

All coefficients are nonnegative: the first and last by log concavity; the middle by consecutive ratio inequalities, or by inspecting the zero endpoints of the contiguous positive degree range. Hence for t,u in [a,b], P(t)<=R^2 P(u). Including the outside weight gives a factor R^3 comparing any two off-diagonal entries in the same row. For N=2 the row has only one such entry. Conservation implies

$$
\sum_{j\ne i}-\mathrm{Cov}(X_i,X_j)=\mathrm{Var}(X_i)\le 1/4.
$$

Every off-diagonal negative covariance is therefore at most R^3/[4(N-1)] for N>=2. Trivial sectors have zero covariance.

## Observation comparison

A positive local likelihood L multiplies the local weight by L(1)/L(0). Multiple likelihoods may be combined provided resulting weights stay in [a,b]. Changing only w_j by ratio r gives

$$
p'_i-p_i=\frac{(r-1)\mathrm{Cov}(X_i,X_j)}{1+(r-1)p_j}.
$$

The absolute prefactor is at most R-1 (also for r<1). Telescoping m changes outside a target of s sites bounds target marginal TV by

$$
\min\left(1,\frac{sm(R-1)R^3}{4(N-s)}\right),\qquad 1\le s<N.
$$

Expose target coordinates sequentially, coupling their Bernoulli conditionals maximally while prefixes agree. On a common feasible prefix of length h the remaining law is canonical with N-h sites and remaining count reduced by the prefix count. Both laws have the same support. The single-site denominator N-h-1 is at least N-s. Union bound on first disagreement proves the claim. Stochastic output channels contract TV; insertion functions in [0,1] inherit it. Positive target likelihood with minimum c implies log discrepancy at most TV/c. The normalizer and moments are computed by elementary-symmetric dynamic programming in O(NK) rational operations per deleted set, without enumerating sectors; not a constant-bit-cost claim.

## Sharp qualitative limits

At uniform weights covariance is exactly -K(N-K)/(N^2(N-1)), so inverse-volume order is sharp at nondegenerate density.

For even N, K=N/2, target weight one and every other weight r, its inclusion probability is 1/(1+r), by binomial ratios. Use a binary channel with L_+(1)=2/3, L_+(0)=1/3 and complementary minus. All plus clamps give r=2 and target probability 1/3; minus gives r=1/2 and 2/3. Leave a common wildcard neighborhood of o(N) sites around the target. The comparison bound shows these probabilities still tend to 1/3 and 2/3; target plus insertion tends to 4/9 and 5/9, gap 1/9, despite every likelihood being at least 1/3. Thus uniform finite-volume distance decay over extensive clamps is false even within one sector. This is an order-of-limits obstruction, not non-Gibbsianness of the infinite-volume observed law: for K/N tending to rho, fixed finite marginals of the unweighted canonical law converge to iid Bernoulli(rho) by the hypergeometric formula. The limiting single-time observation field is iid. An extensive clamp changes the reservoir.

For mixtures of sectors, couple posterior counts maximally first; target TV is bounded by the mismatch probability plus the sum of common count masses times within-sector bounds. No decay across sector mixtures: all-empty and all-full give permanent observable distinction.

On an N-cycle at uniform weights a uniformly chosen bond heat bath changes the expected occupation vector by the discrete Laplacian divided by 2N. The nonconstant Fourier density mode has eigenvalue 1-(1-cos(2pi/N))/N in every nontrivial sector; it bounds the per-bond spectral gap above by order N^-3, or N^-2 per sweep. Uniform positive per-sweep gap is impossible. Auxiliary complete-graph exchange is not a replacement physical dynamics.

## Prior art and boundary

Conditioned Bernoulli/rejective sampling, negative correlation, Newton inequalities, path coupling and ensemble equivalence are classical. Relevant source comparison: Ruetz and Schnass, Non-asymptotic bounds for inclusion probabilities in rejective sampling (https://www.uibk.ac.at/media/filer_public/4b/59/4b59f460-a2f2-4a58-baa8-a9a73c80f3c7/22_rusc_rejective_sampling.pdf), abstract and model; conservative canonical stationary distributions, https://doi.org/10.1088/1751-8121/aadc6e. No priority claim from this limited comparison.

Next: interacting canonical Gibbs measures and genuine time-dependent observation conditioning under local exchange, distinguishing diffusive conserved modes from conditional phase coexistence. No unrestricted interacting or stationary space-time quasilocality claim.
