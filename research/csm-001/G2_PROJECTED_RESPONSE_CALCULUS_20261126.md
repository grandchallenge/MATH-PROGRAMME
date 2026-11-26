# CSM-G2-WP19 — conserved-subspace response and conditional transport

Internally derived candidate; originality UNADJUDICATED, no MATHCERT. Protected predecessor WP17 #3773; WP18 #3787 exact candidate 2b2739dc8766b9ae98c1fdf3a69cd32c5915189c queued at preparation. Independent proof uses only canonical sectors and local bonds, not WP18's unadmitted theorem. Scope finite graphs, finite observation histories and hard phase control.

## 1. Response and conservation gauge

On a finite Markov path in a fixed count sector K, let arbitrary positive slice likelihoods L_t weight its law. Additional log-fields h_t multiply these by exp(h_t dot X_t). Finite differentiation of the normalizer gives

$$
C_{ts}=\nabla_{h_s}\mathbb E_h X_t=\mathrm{Cov}_h(X_t,X_s).
$$

The entire space-time response is a symmetric positive semidefinite Hessian, not necessarily each cross-time block. Conservation gives C_ts 1=0 and 1^T C_ts=0. With Pi=I-11^T/N, C_ts=Pi C_ts Pi. Adding a multiple of 1 to each field leaves the posterior unchanged. More generally for fixed linear charges A^T X_t=c use projection to ker(A^T), also for dependent charges. Sector mixtures differ: total covariance is expected within-sector covariance plus covariance of sector-conditional means, using posterior sector weights. The latter can persist and include projected directions, not just the constant mode.

Finite log-field changes integrate the covariance along a straight interpolation. Derivatives of nonlinear target tests similarly give covariances. At fixed K, oscillation of a dot x is the sum of the K largest coefficients minus the sum of the K smallest; by Cauchy-Schwarz it is at most sqrt(2 min(K,N-K)) times the Euclidean norm of its projected coefficients.

## 2. Actual physical local exchange with multiple clamps

Use random-scan heat bath on a connected N-site graph with E edges and positive site and symmetric pair factors. Suppose either placement on any active bond has probability at least eta>0; e.g. site ratio R, B=max_i product of max(lambda_ij,1/lambda_ij) give eta=1/(1+R B^2). Time-dependent factors with uniform eta also allowed.

Any two configurations in the same sector are connected by at most m=N(N-1)/2 adjacent swaps: fix a spanning-tree leaf to its desired bit by moving the nearest needed particle or hole along the tree, then remove that leaf. Counts on the remaining tree agree. Each stage takes at most the number of remaining edges. Self loops have probability at least eta, so pad to m. Desired swaps have probability at least eta/E; hence every m-step kernel entry is at least (eta/E)^m. Singleton sectors have zero response.

Write B_{s,t}(x,y) for transfer product of physical kernels and likelihoods (including t, not s), and R_v=max L_v/min L_v on the sector. For t-s=m,

$$
(\eta/E)^m L_t(y)\prod_{s<v<t}\min L_v
\le B_{s,t}(x,y)\le
L_t(y)\prod_{s<v<t}\max L_v.
$$

Lower bound uses one padded path, upper bound total transition probability one. Future observations enter a positive backward message b_t(y). Posterior conditional block kernel is B(x,y)b_t(y) divided by its row sum, by finite Markov factorization. It has a common minorizing probability measure of mass at least

$$
\delta_{s,t}=(\eta/E)^m\prod_{s<v<t}R_v^{-1}.
$$

Indeed B(x,y)>=delta U_y for column maxima U_y, and the row normalizer is at most sum_y U_y b_t(y). Reference measure proportional to U_y b_t(y) works. Thus Dobrushin oscillation contraction <=1-delta independently of endpoint likelihood and all future messages. A sharper exact small-block option computes min_y min_x B(x,y)/max_x B(x,y), omitting zero columns. Zero lower bound is undecided, not an obstruction. Compose blocks and leftover steps (nonexpansive). With gamma the product of block contraction bounds,

$$
|\mathrm{Cov}_h(f(X_t),g(X_s))|
\le \tfrac14\,\mathrm{osc}(f)\,\mathrm{osc}(g)\,\gamma.
$$

Condition f on X_s and use contraction, Cauchy-Schwarz, variance <=osc^2/4. Reverse order by transposition. For linear tests the projected operator norm is at most min(K,N-K) gamma/2. Source-only perturbation integrates with the same certificate, which is independent of the source likelihood. Multiple times integrate using uniform intermediate ratios along interpolation. This is a finite-volume temporal multi-clamp bound for genuinely interacting physical exchange; rate can be extremely poor and is not uniform hydrodynamic scaling, spatial quasilocality or an infinite-volume result. Coarse bound requires no state tensor; exact small-block option enumerates states.

For a 4-cycle, K=2, alternating site weights 1 and 2, pair factor 17/16, and successive local likelihood ratios 2, the six-step column ratio is 1298683449634385525/5608074338365162367 (>0.2315); the coarse lower bound is below 4e-9. Both bound the actual conditioned kernel independently of future messages. This quantifies the cost of the crude physical-path certificate.

## 3. Exact composition and missing modes

For s<u<t the posterior path remains Markov. Let F=E[X_t-E X_t|X_u] and G=E[X_s-E X_s|X_u]. With covariance pseudoinverse at u, the orthogonal least-squares projections onto the centered linear occupation span are F_lin=C_tu C_uu^+ (X_u-E X_u) and G_lin=C_su C_uu^+ (X_u-E X_u). Conditional independence of endpoints and residual orthogonality give

$$
C_{ts}=C_{tu} C_{uu}^{+} C_{us}
+\mathbb E[(F-F_{\rm lin})(G-G_{\rm lin})^T].
$$

Each bilinear residual is bounded by the product of its residual L2 norms. It vanishes if either conditional endpoint mean is affine in X_u; no invertibility on the entire projected space is needed. On full centered L2 spaces conditional-expectation maps compose exactly and are contractions by Jensen. The linear occupation projection is not in general a closed subsystem.

Counterexample: 4-cycle, K=2, uniform stationary exchange, endpoints 0 and 2 both reweighted by 2 to the power X_0 (site 0), middle unweighted. Given middle state x, both endpoint means at site 0 equal g(x)=2p/(1+p), where p=(P x)_0, P=I-Laplacian/8. Complementary middle states give p=7/8 and 1/8, or 3/4 and 1/4. Their g sums are 52/45 and 44/35 respectively. An affine function on the sector has a constant complement sum, so g is not affine. All middle states have positive posterior mass. The scalar closure defect for the two endpoint site-0 observables is exactly the strictly positive residual variance. Exact rational replay gives scalar defect 512/1058501, compared with total endpoint covariance 4224/51529. Projection alone cannot justify closed diffusion even with noninteracting physical dynamics. Without clamps uniform exclusion linear expectations are closed and the projected heat kernel formula is recovered.

## 4. Collective order control distinct from charge

On even cycles of size at least four impose hard nearest-neighbor exclusion at half filling. Exactly two alternating configurations remain; both have the same count. Every physical bond exchange is frozen. The equal mixture has covariance vv^T/4, with v_i=(-1)^i orthogonal to the charge; its staggered eigenvalue is N/4. This mode persists in time and survives projection. This hard disconnected example is outside the positive-bond theorem.

On the infinite line the two alternating phases are limits of the finite-sector laws. Observe each bit independently with P(+|1)=2/3 and P(+|0)=1/3. Every finite observed assignment has positive probability; the two observation phases are mutually singular on the exterior of any site by the strong law on even sites. Target plus conditional probability is 2/3 or 1/3 according to inferred phase. Every finite exterior cylinder has positive probability in both phases, so any a.s. version has essential oscillation at least 1/3 in every such neighborhood. No quasilocal version exists. This is a genuine observable conditional phase obstruction at the same density, not sector mixing or failed gain. No positive-temperature phase theorem follows.

## 5. Prior art and frontier

Exponential-family covariance identities, conditional-expectation projection and finite HMM smoothing/minorization are classical; see Douc, Fort, Moulines, Priouret (2009), https://arxiv.org/abs/math/0703836, and Cappe, Moulines, Ryden (2005), filtering and smoothing recursions, https://people.bordeaux.inria.fr/pierre.delmoral/hmm-cappe-moulines-ryden.pdf (Chapter 2). This is a bounded synthesis, not an originality claim. Next: scale-sensitive interacting conditioned transport on local graphs, control nonlinear closure defects in hydrodynamic regimes, and separate soft positive-temperature phases from hard controls. No G3 promotion.
