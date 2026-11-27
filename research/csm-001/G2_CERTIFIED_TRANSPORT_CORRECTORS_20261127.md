# CSM-G2-WP23 — certified transport correctors and fixed-temperature phase augmentation

Internal candidate; originality UNADJUDICATED, no MATHCERT. Continues protected WP22 merge 487d1aa6ce888582c819e3b53fdd3bd77b90171d. Two distinct results: finite interacting homogeneous exchange resolvent correctors with exact residual certificates, and a fixed-temperature mean-field antiferromagnetic model with physical nearest-neighbor exchange and a count-invisible collective phase. Neither is a general short-range interacting hydrodynamic or fixed-temperature phase theorem.

## 1. Variational corrector without spectral decomposition

Use WP22's reversible generator L, equilibrium inner product, count projection P, Q=I-P, A=PLP, D=QLQ and B=QLP. For z>0 define the positive operator H_z=zI-D on range Q, and b=Bf for any retained f. The exact transport correction at Laplace frequency z is

$$
m_z(f)=\langle b,H_z^{-1}b\rangle.
$$

It is the Laplace transform of the quadratic memory kernel. By completing the square,

$$
m_z(f)=\sup_{v\in Q}\{2\langle b,v\rangle-\langle v,H_zv\rangle\}.
$$

For any trial v in Q define J(v) as the expression in braces and r=b-H_zv. The exact identity m_z-J(v)=<r,H_z^{-1}r> gives the certified interval

$$
J(v)\le m_z(f)\le J(v)+\|r\|^2/(z+g),
$$

whenever -D>=gI on Q; g=0 is always safe. A finite trial basis gives a positive definite Gram system, solved using generator actions and equilibrium inner products only. Redundant vectors are removed. Use projected local occupation monomials, projected boundary currents, or the Krylov sequence b,H_z b,... . Ritz maxima increase monotonically for nested spaces; Krylov reaches the exact solution after finitely many independent vectors (invariant span when the next vector is dependent). Residual upper bounds need not decrease monotonically; intersect successive intervals. This does not require diagonalizing L and is a certificate even for genuinely interacting bond heat baths. It is not a complexity bound: equilibrium inner products and Q may themselves require expensive computation. Finite-state reference tests deliberately enumerate small sectors. To avoid a spurious local claim, Q of a cylinder function is generally not a cylinder function.

For a common trial space V subset Q and each retained f, solve its Gram system; the solution T_V f is linear. Define M_V by <f,M_V f>=J(T_V f) and the residual map R_V=B-H_z T_V. Then in Loewner order

$$
0\le M_z-M_V\le R_V^*R_V/(z+g).
$$

The exact Schur complement C_z=zI-A-M_z is positive definite: minimize the form of zI-L over the discarded coordinate, giving C_z>=zI. Block Gaussian elimination yields P(zI-L)^(-1)P=C_z^(-1) on range P. The reduced C_V=zI-A-M_V is an upper bound on C_z. If a residual form certificate R_V^*R_V/(z+g)<=eta C_V holds for eta<1, then

$$
C_V^{-1}\le P(zI-L)^{-1}P\le (1-\eta)^{-1}C_V^{-1}.
$$

Thus the tolerance is relative to the actual corrected low-frequency operator, not the size of the discarded state space. z can be chosen of order N^-2 on a diffusive horizon. A computable sufficient eta is the trace of C_V inverse times the residual quadratic-form matrix divided by z+g in any retained basis. Indeed after conjugating the residual form by the positive square root of the inverse C_V, the resulting positive semidefinite operator has largest eigenvalue at most its trace. The basis need not be orthonormal when both matrices represent bilinear forms. A scalar test of the residual form on just one f does not certify this operator inequality. A separate target-specific interval follows by solving (zI-L)u=f variationally in P+V, with residual divided by z; this is the full integrated autocorrelation certificate. Bounds concern Laplace-weighted equilibrium response, not pointwise time or arbitrary conditioned paths. Exact memory or additional estimates are required to turn them into such claims.

For an interacting finite specimen we use six-site half-filled local ring heat bath with nearest-neighbor pair factor 3/2 and adjacent two-site count blocks. The rational reference uses a retained centered block count, projected local features and Krylov directions. It checks residual intervals for z=1/N^2, exact solution as a small-sector oracle only, monotonic Ritz lower bounds, and correction positivity. No artificially scheduled relaxation is used.

## 2. Fixed-temperature collective phase with local physical exchanges

Take N divisible by four, K=N/2, alternating signs v_i=(-1)^i, and S=N^{-1} sum_i v_i(2x_i-1). Use Gibbs law proportional to exp(beta N S^2) at a fixed beta>0, with nearest-neighbor ring bond heat baths of rate one. The energy is extensive and pairwise mean-field (expanding the square); physical moves are local, the Hamiltonian is not short-range. All sector configurations have positive weight. No zero-temperature limit or N-dependent beta is taken.

Pair adjacent even and odd sites. Swapping both sites of every pair preserves every pair count and sends S to -S. The Gibbs weight is invariant. Hence the conditional mean of every odd function of S given the count vector is zero. In particular the staggered density and f=sign(S), with sign(0)=0, are exactly invisible to the entire count algebra, not just to its linear span.

Let a be the number of occupied even sites. Then S=4a/N-1 and multiplicity is binomial(N/2,a)^2. The probability mass exponent per site converges uniformly, up to O(log N/N), to

$$
\Phi_\beta(s)=H((1+s)/2)+\beta s^2,
$$

where H(p)=-p log p-(1-p) log(1-p) with continuous endpoint values. This follows from the elementary entropy bounds exp(n H(p))/(n+1)<=binomial(n,np)<=exp(n H(p)); the lower bound uses that np is a mode of Binomial(n,p). For beta>1/2 the two global maximizers are +/-s_beta, where s_beta in (0,1) solves atanh(s_beta)=2 beta s_beta: atanh(s)/s strictly increases from 1 to infinity. For beta<=1/2 the unique maximizer is zero. The multiplicities and the strict gap of Phi away from its maximizers imply concentration there, with equal weights by reflection symmetry. Thus ||S||_2^2 -> s_beta^2 and ||f||_2^2 ->1 at fixed beta>1/2.

A local bond move changes S by at most 4/N. Therefore f can change only from states in the central band |S|<=4/N. Let b_N be its equilibrium probability. The preceding strict entropy gap implies b_N<= exp(-c_beta N) for all sufficiently large N, for some c_beta>0. More explicitly for beta>log 2 use Z>=2 exp(beta N) and at most 2^N states to obtain

$$
b_N\le \tfrac12\exp[-N(\beta-\log 2)+16\beta/N].
$$

With N bonds of rate one, squared sign increment at most four, Dirichlet energy E(f,f)<=2N b_N. Spectral Jensen yields <f,exp(tL)f> >= ||f||^2 exp(-2N b_N t/||f||^2); ||f||^2>=1-b_N. This gives an exponentially slow projected collective mode at fixed positive temperature even with local physical exchange and fixed particle count. Any count-only discarded gap satisfies g<=2N b_N/(1-b_N) when b_N<1. On all polynomial time horizons the sign autocorrelation tends to one. Moreover ||S-s_beta f||_2->0, so the staggered density autocorrelation tends to s_beta^2 on those horizons. Adding S or its sign as an observable removes the identified invisible direction (S as an algebra generator includes sign), but no uniform gap for the remainder is claimed.

For fixed beta=log 4, N>=8, the explicit band bound is <=2^(3-N) using 32/N<=4. The probability |S|<=1/2 is <=2^(-1-N/2). These are exact rational upper bounds; exponential energy and actual probabilities can be evaluated by log-sum-exp over only N/2+1 count values. This is a scale-uniform phase obstruction for mean-field energy, not for finite-range Hamiltonians.

The infinite-volume single-time limit is the equal mixture of two independent alternating Bernoulli fields: conditional on a, even and odd sets are independently uniform fixed-count configurations, whose finite marginals tend by hypergeometric ratios to product laws with respective densities (1+s_beta)/2 and (1-s_beta)/2 (reversed in the other phase). Pass to the mixture using concentration and boundedness. Under independent noisy binary observations with plus probabilities 2/3 when occupied and 1/3 when vacant, the two observed phases have even-site plus probabilities 1/2 +/- s_beta/6. They are mutually singular on any exterior by the strong law; every finite cylinder has positive probability in both. Hence any version of the target plus conditional has essential oscillation >=s_beta/3 on every finite exterior cylinder. No quasilocal version exists. This is a genuine same-density observed phase obstruction for the mean-field limit; not a local-Gibbs theorem.

## 3. Exact reference replay

In the interacting six-site ring with lambda=3/2 and z=1/36, the scalar corrector using b alone has rational interval with endpoints approximately 0.070035191120319 and 0.072603764038333. Adding H_z b produces the exact value 0.070071775066952 (rounded). The common retained-space correction requires more: block Krylov dimensions 6, 12, 13 yield trace upper bounds eta approximately 6.0099675, 0.01037049, 0 respectively. The first two do not certify a 1% tolerance, the third is exact. The small-sector full linear solve is an oracle, not the proposed scalable algorithm. Exact tests also cover repulsion lambda=2/3, projected local trials, all-retained form inversion, invalid inputs, and the N=8 mean-field Gibbs mass, local-bond phase energy and count projection. For beta=log 4 the rational phase gap bounds at N=16,64,256 are approximately 3.907e-3, 5.552e-17, 3.538e-74 (rounded upward); the multiplicity-based numerical second moments of S are approximately 0.99826, 0.99733, 0.99237. The exact rational bounds, not the floating evaluations, support the persistence theorem.

## 4. Prior art and scope

Corrector/resolvent variational methods for reversible Markov transport are classical (Kipnis-Varadhan framework; see https://numdam.org/item/10.1016/S0246-0203%2802%2900016-X.pdf and https://www.mathematik.uni-marburg.de/~stochastik/publikationen/holzmann/31.pdf). Memory-based Galerkin approximation: https://pmc.ncbi.nlm.nih.gov/articles/PMC10898919/. Curie-Weiss entropy and symmetry breaking are classical. The bounded CSM synthesis is the relative Schur residual certificate, projected generator-selected augmentation, and the explicit canonical mean-field phase mode invisible to every adjacent-pair count. No originality or certification claim. Next: genuinely local finite-range fixed-temperature phase obstruction and certified interacting transport correctors with local equilibrium inner-product computation and controlled diffusive-time, rather than merely Laplace-frequency, error.
