# CSM-G2-WP22 — homogeneous conservative dynamics: memory and mode augmentation

Internal candidate; originality UNADJUDICATED, no MATHCERT. Continues WP21 protected merge 3e20ef3c18ac6697ef87c435541ffd60e45b96de. Finite positive canonical Gibbs law, continuous-time physical bond heat bath with every bond clock rate one (no scheduled equilibration). Exact obstruction on diffusive horizons, a residual certificate and a soft finite phase control; not a general hydrodynamic limit.

## 1. Exact projected memory, without artificial scheduling

Let L=sum_e (H_e-I), where H_e is conditional expectation given exterior and the bond count, and pi the canonical equilibrium. L is self-adjoint nonpositive in L2(pi). For block count algebra let P be conditional expectation onto counts, Q=I-P. More generally use any orthogonal projection P containing constants. On the two spaces set A=PLP, D=QLQ, B=QLP; adjoints taken in equilibrium L2. For f in range P, y(t)=P exp(tL)f and z(t)=Q exp(tL)f satisfy y'=Ay+B* z, z'=By+Dz, y(0)=f,z(0)=0. Variation of constants gives the exact Mori-Zwanzig equation

$$
y'(t)=Ay(t)+\int_0^t B^*e^{(t-s)D}B y(s)\,ds.
$$

The memory kernel is positive semidefinite at each time by self-adjointness of D, but the convolution applied to a changing y is not necessarily positive in every component. If -D>=g I for g>0, its norm is at most ||B||^2 exp(-gt), and the integrated kernel is B*(-D)^{-1}B. The zero-frequency Schur complement is A+B*(-D)^{-1}B, nonpositive by minimizing the quadratic form of -L over Q corrections. No identification of this zero-frequency operator with the full time evolution is asserted.

The count-fiber Poincare inequality from WP21 supplies an explicit g for the genuine homogeneous process: the internal-bond part is the sum of physical bond Dirichlet forms, and cross-block terms are nonnegative. On each count fiber use WP21's g_k for one uniform block/internal-bond step; the sum dominates its Dirichlet form, so g=min_k g_k is valid on Q. Uniform lower placement probabilities and q<1 from WP21 give a common bound without enumerating counts. Singleton fibers have Q=0 there. This is only a lower bound on the orthogonal gap, not an assumed separation of global time scales.

## 2. A posterior-compatible a posteriori certificate

For a retained target f, put v(t)=exp(tA)f and w(t)=exp(tL)f-v(t). Then w'=Lw+Bv and w(0)=0. Using the Dirichlet lower bound on the discarded subspace,

$$
\frac12\frac{d}{dt}\|w\|_2^2
\le -g\|Qw\|_2^2+\|Qw\|_2\|Bv\|_2
\le \frac{\|Bv\|_2^2}{4g}.
$$

Consequently ||w(T)||_2^2 <= (1/(2g)) integral_0^T ||B exp(tA)f||_2^2 dt. It remains valid for a time-dependent differentiable retained approximation v with an additional retained residual; the displayed formula is for exact retained evolution only. This certificate uses actual boundary flux leakage and is often sharper than the uniform ||B|| bound. It may be vacuous; a small orthogonal time scale alone does not ensure a small integral. At equilibrium, any test h has correlation error bounded by ||h||_2 times this norm bound.

For a count algebra P, A is the true averaged count generator, a Markov generator with equilibrium count law (no scheduled fast resets). Multiplication by positive count likelihood L_j preserves the algebra and has norm <=M_j=max L_j; m_j=min L_j>0. For a word of H physical intervals t_j with such likelihoods, both exact and reduced transfers have L2 norm <=M_j. Let epsilon_j bound ||(exp(t_j L)-exp(t_j A))P|| by the certificate (embedding the coarse operator in microscopic space). Telescoping the operator products on a retained target gives unnormalized error <=||p/pi||_2 ||f||_2 (product M_j) sum epsilon_j, for initial density p/pi in L2. Apply also to evidence f=1. Both evidences are >=product m_j. For 0<=f<=1 the normalized terminal error is therefore <=min(1,2||p/pi||_2 (product M_j/m_j) sum epsilon_j). The inequality follows by writing the difference of ratios as a numerator difference plus a denominator difference times the reduced normalized target. This is an explicit multi-clamp sufficient certificate for the actual unscheduled dynamics; not uniform over arbitrarily strong observations, and it controls terminal tests, not all coarse histories. For endpoint conditional predictions, a uniform pointwise residual would follow from the L2 bound divided by sqrt(pi_min); this is volume dependent, so no uniform conditional phase result follows.

## 3. Diffusive-scale obstruction to instantaneous count closure

Take uniform symmetric exclusion on the N-cycle, N=M ell with fixed block length ell>=2, M>=3, and any nontrivial fixed count. Each bond has rate one and heat bath swaps unequal bits with probability 1/2. On linear occupation observables L acts as half the discrete Laplacian. Let a_i=exp(2 pi i i/N) (the first i in the exponent denotes the imaginary unit), and let b_i=exp(2 pi i floor(i/ell)/M). Use centered linear observables f_a, f_b with these coefficients. Both coefficient sums vanish. The uniform canonical covariance inner product on zero-sum coefficients is a common scalar times Euclidean inner product, namely rho(1-rho) N/(N-1). Therefore normalized correlation of f_a is exactly exp(-t(1-cos(2 pi/N))). Also ||f_a-f_b||/||f_b||<=2 pi ell/N by the elementary Lipschitz bound for complex exponentials, and their norms agree. Contractivity gives a difference of normalized equilibrium autocorrelations at most 4 pi ell/N for every t. Complex observables here mean the paired real sine and cosine tests with the usual Hermitian covariance.

For the averaged count generator A, the mean net count drift of each block is the discrete block Laplacian of k divided by 2 ell: average boundary occupations are k_A/ell. Thus f_b is exactly an eigenfunction of A with decay rate (1-cos(2 pi/M))/ell. At t=s N^2 for any fixed s>0, the actual normalized f_b autocorrelation tends to exp(-2 pi^2 s), whereas instantaneous count closure gives exp(-2 pi^2 ell s). They differ by a strictly positive constant. This disproves the inference that a locally equilibrated count algebra has the correct instantaneous coarse generator on diffusive scales, even without interactions or observations. Equilibration of omitted modes alone is insufficient. Conversely the physical smooth density mode gives an explicit corrected prediction for f_b with uniform error at most 4 pi ell/N; no inserted fast schedule. This is a positive scale-dependent retained-mode certificate for an equilibrium two-time test, not a Markov model for arbitrary count histories.

## 4. Soft finite-temperature phase augmentation

Let N even >=4, K=N/2, ring Gibbs weight lambda raised to the number of adjacent occupied pairs, with 0<lambda<1. There are precisely two alternating states with zero adjacent pairs; all others have at least one. Each bond heat bath in an alternating state creates exactly one occupied pair if it swaps. Exit rate from either alternating state is a=N lambda/(1+lambda). Equilibrium mass m of the two alternating states satisfies m>=2/(2+(binomial(N,K)-2)lambda). All states retain positive probability, and the physical chain is irreducible.

Let f be +1 on one alternating state, -1 on the other, zero otherwise. For adjacent two-site count blocks the two alternating states share the all-one count vector and equal weight. Thus Pf=0 exactly. Its mean is zero, norm squared m and Dirichlet energy a m (the two states are not directly connected). Spectral Jensen for the self-adjoint semigroup gives

$$
\langle f,e^{tL}f\rangle\ge m e^{-at}.
$$

Also the physically local aggregate staggered density s(x)=N^{-1} sum_i (-1)^i (2x_i-1) agrees with f on the alternating states and differs by at most one elsewhere. By particle-hole complement symmetry at half filling on the ring, its conditional expectation on the all-one count fiber vanishes (the number of occupied adjacent pairs equals the number of empty adjacent pairs). In particular ||Qs||^2>=m. Its autocorrelation (with the staggered density already divided by N) differs from that of f by at most 2 sqrt(1-m), using contraction and norms <=1. Therefore positive-temperature finite systems can contain a slow collective direction completely absent from count observables. An augmented algebra retaining the sign phase f contains this obstruction exactly; it is not asserted to be sufficient for all other observables. A general necessary condition for a discarded-space gap g is g<=a in this specimen, by testing f. This bound can be small at low temperature even though total count is fixed. For volume-dependent lambda with binomial(N,K) lambda ->0 and t N lambda ->0, the phase is persistent on that time scale; this is not a fixed-positive-temperature thermodynamic phase transition in one dimension.

## 5. Reference replay

The sparse Fourier formula for the normalized block-step mode is a sum over ell aliases k=1+l M, with weights given by squared moduli of the within-block Fourier average. At N=4096 and t=N^2/20 the actual correlations for ell=2,4,8 are 0.3727076917, 0.3727068147, 0.3727033067; the naive count model gives 0.1389113482, 0.0192965419, 0.0003723842. The smooth density prediction is 0.3727079110 in all three cases. These values are floating-point evaluations of analytic formulas, not sampling estimates or rigorous interval enclosures. Exact small-sector rational replay checks reversibility, count projection, the second derivative memory identity and the phase Rayleigh quotient. Additional bounded numerical semigroup replay checks the two-clamp residual and the Fourier formula against the microscopic generator. For N=8 and lambda=1/10000 the alternating mass lower bound is 5000/5017 and exit rate 8/10001.

## 6. Prior art and remaining boundary

Mori-Zwanzig memory, Schur complements, Dirichlet forms, spectral Jensen and symmetric exclusion duality are classical. See On the generalized Langevin equation and the Mori projection operator technique, https://arxiv.org/abs/2503.20457, orthogonal semigroup and projection formula; A priori estimation of memory effects in reduced-order models of nonlinear systems using the Mori-Zwanzig formalism, https://pmc.ncbi.nlm.nih.gov/articles/PMC5627381/; and hydrodynamic exclusion homogenization https://doi.org/10.1007/s00440-022-01163-8. Bounded CSM synthesis: count-fiber Poincare control of orthogonal generator, energy residual for conditioned transfer words, explicit diffusive-scale failure of instantaneous count averaging, and a soft finite phase diagnostic. Next: constructive transport correctors under genuinely interacting homogeneous exchange, and fixed-temperature collective phase augmentation with a scale-uniform certificate. No G3 promotion.
