# CSM-G2-WP25 — gradient transport and finite-range observed phase

Internal candidate, originality UNADJUDICATED, no MATHCERT. Continues WP24 protected merge dae3f109581774c7d7405f3c86d9845060f114d3. Two bounded theorems: uniform-in-time dilute transport for fixed genuine nearest-neighbor interaction, and essential conditional discontinuity for an independently erased noisy observation of subsequential finite-range bilayer limits. Neither is a general positive-density hydrodynamic theorem or a theorem for all observation channels.

## 1. Exact gradient identity for physical heat bath

On an N>=5 ring let the canonical weight be lambda^(sum_i x_i x_{i+1}), with fixed 0<lambda<infinity and count K. All bonds have rate-one clocks; a selected bond resamples its occupations from the Gibbs conditional. Write j_i(x) for the instantaneous signed particle flux from i to i+1. Set c=(1-lambda)/(2(1+lambda)) and define psi_i as the indicator of at least two occupied sites among i-1,i,i+1. Then

$$
j_i=h_i-h_{i+1},\qquad h_i=x_i/2+c\psi_i.
$$

Indeed write (a,x,y,b) for the four consecutive bits around the bond. The swap odds when x=1,y=0 are lambda^(b-a), and the reverse odds for x=0,y=1 are lambda^(a-b). Thus j_i=(x-y)/2+c(a-b)(x-y)^2. Expand psi_i=a x+a y+x y-2 a x y and subtract its translate; the difference is (a-b)(x+y-2xy). This is an exact gradient identity with genuinely nonzero interaction. G x_i=j_{i-1}-j_i is the discrete Laplacian of h_i.

For a real first Fourier coefficient a_i=cos(2 pi i/N), let F=sum_i a_i x_i, Z=sum_i a_i psi_i, omega=1-cos(2 pi/N). Both means vanish by translation invariance. Then GF=-omega F-2 omega c Z. Duhamel and L2 contractivity of the reversible semigroup give for every T>=0

$$
\|e^{TG}F-e^{-\omega T}F\|_2
\le 2|c|(1-e^{-\omega T})\|Z\|_2 .
$$

No spectral diagonalization, scheduled equilibration or accumulation proportional to microscopic bond count is needed.

## 2. Scale-uniform dilute certificate

Let R=max(lambda,1/lambda)^K. The total occupied-bond count is between 0 and K, so the canonical density relative to uniform fixed-count law lies in [1/R,R]. Pointwise C=sum_i psi_i<=3K, since each occupied site occurs in three triples (a sharper bound is possible). By the union bound over three possible occupied pairs, E C<=3R K(K-1)/(N-1). Since |Z|<=C, E Z^2<=9R K^2(K-1)/(N-1). Uniform fixed-count variance of F is K(N-K)/(2(N-1)), using the uniform canonical covariance and sum a_i=0, sum a_i^2=N/2. The actual variance is at least this divided by R. Thus for 1<=K<N,

$$
\frac{\|e^{TG}F-e^{-\omega T}F\|_2}{\|F\|_2}
\le 6|c|R\sqrt{\frac{2K(K-1)}{N-K}} .
$$

This tends to zero uniformly over T>=0 at fixed K>=2 and fixed lambda not equal to one (K=1 is exact). More generally sufficient is R^2 K(K-1)/(N-K)->0. At T=sN^2 the normalized equilibrium F autocorrelation converges to exp(-2 pi^2 s). This is a genuine fixed-interaction dilute family, not positive-density transport: the interaction correction is small because occupied triples become rare, not because the energy parameter vanishes. At positive density the displayed estimate fails to prove convergence. The gradient identity identifies the next required finite-density replacement: replace the local nonlinear psi by its equilibrium density response, with control of the time-integrated remainder. No such replacement theorem is assumed here.

## 3. Finite-range observed conditional discontinuity

Use WP24's even square torus bilayer at sufficiently low fixed beta in the imported periodic Ising surface-order theorem's range. Its common transformed layer magnetization M has symmetric canonical law and P(|M|<=a_0 L^2)->0 for a fixed a_0>0. Let mu_L^+ and mu_L^- be the laws conditioned on M>0 and M<0. They are translation invariant, related by layer exchange, and the upper spin's mean is respectively at least a_0-o(1) and at most -a_0+o(1), by translation invariance. Compactness of finite-alphabet product measures gives a joint subsequence of their periodic extensions with local weak limits mu^+,mu^-. The unconditioned limit is their equal mixture mu; the omitted M=0 weight vanishes. The limiting upper spin means differ by at least 2a_0. We do not assume the limits are pure, DLR, or mutually singular.

Observe upper-layer spins through an independent channel at each cell: erase with probability r in (0,1); otherwise output plus with probability 2/3 for spin +1 and 1/3 for spin -1, minus otherwise. Erasure flags are independent of the hidden field and all nonerased noise. Let nu^+,nu^- be the resulting stationary observed laws, nu their equal mixture. The expected indicator of output plus differs by at least (1-r)a_0/3 between these components (since conditional plus probability is (1-r)(1/2+sigma/6)).

Let A be the limit of square spatial averages of the plus indicator, given almost surely by the multiparameter pointwise ergodic theorem for stationary Z^2 fields. It is invariant and measurable from the exterior of the origin; removing any finite set does not change the limit. Under each observed component E A equals its plus mean. Therefore the essential range of A under nu has diameter at least (1-r)a_0/3. No assumption of pure phases is needed. For any invariant event E in the sigma field of A, stationarity gives E[1_{Y_0=+} 1_E]=E[A 1_E] (average over translates and bounded convergence).

Let C_F denote the event that every observation in finite exterior set F is erased. It has probability r^|F| and is independent of the pair (Y_0,A): A can be calculated from outside F, the flags in F are independent of the hidden field and all other channel randomness. Consequently E[1_{Y_0=+}|E,C_F]=E[A|E] whenever P(E)>0. For any version g of the exterior conditional probability of Y_0=+, the tower property forces its essential oscillation on C_F to be at least the essential range diameter of A: choose E near each endpoint of that range, both with positive probability inside C_F. Thus every finite exterior neighborhood of the all-erasure configuration has conditional oscillation at least (1-r)a_0/3. The observed law has full support since every channel output has a uniformly positive conditional probability. No quasilocal version exists. This is an essential discontinuity for a specified finite-range hidden model and erasure-plus-noise channel, not a claim for ordinary binary noise alone.

## 4. What sufficiency means here

The dilute theorem gives asymptotic sufficiency of the smooth first density mode for its unconditioned equilibrium two-time prediction, not a closed posterior algebra. The observed-phase theorem provides a concrete necessary tail statistic A, in the sense that conditional averages distinguish its different invariant ranges; adding a phase label may not determine the complete conditional law. In particular two-time correctness and observed conditional continuity are logically different requirements. No general sufficiency of conservation+transport+phase augmentation is claimed.

Prior art: reversible gradient systems and hydrodynamic replacement, Duhamel, canonical combinatorics, multiparameter ergodic theorem and hidden-field non-Gibbs phenomena are classical. WP24 identifies the imported surface-order theorem and its temperature boundary. The CSM contribution here is the explicit gradient dilute residual and the erasure-cylinder argument without assuming pure phase limits. Next: finite-density gradient replacement with a quantitative equilibrium norm estimate, and conditional closure within the phase-resolved observed system.

## 5. Positive-density bridge: exact static coefficient, explicit dynamic obligation

For the infinite one-dimensional grand-canonical nearest-neighbor law at density rho in (0,1), the stationary two-state Markov chain has joint probabilities p_11=q, p_10=p_01=rho-q, p_00=1-2rho+q. The positive transfer matrix gives the odds-ratio identity

$$
q(1-2\rho+q)=\lambda(\rho-q)^2.
$$

Conversely this equation has a unique solution strictly between max(0,2rho-1) and rho: the odds ratio increases strictly from zero to infinity. The positive Markov transition p_ab/p_a has precisely the prescribed nearest-neighbor factor, since the odds ratio of its transfer weights is lambda (one-site factors absorb the remaining terms). Thus the equilibrium mean of psi is the explicit function

$$
\Psi(\rho)=2q-q^2/\rho+(\rho-q)^2/(1-\rho).
$$

This follows by adding the four triple probabilities 110,101,011,111 using conditional independence of the outer bits given the middle bit. At half filling, put s=sqrt(lambda). Then q=s/[2(1+s)] and q'=1 by particle-hole symmetry q(1-rho)=1-2rho+q(rho). Differentiation gives Psi'(1/2)=1+2/(1+s)^2. The resulting static gradient diffusion candidate is

$$
D_*=\tfrac12+c\Psi'(1/2)=\frac{2}{(1+s)(1+s^2)}.
$$

This coefficient is exact as a static derivative, not yet a proven finite-density dynamic diffusivity in this work package. For the half-filled even finite ring, let W=Z-Psi'(1/2)F. The exact generator identity gives GF=-2 omega D_* F-2 omega c W. Since D_*>0, the same Duhamel formula and spectral calculus yield

$$
\|e^{TG}F-e^{-2\omega D_*T}F\|_2
\le 2|c|\omega\sqrt{T}\,\|W\|_{-1},
$$

where the squared negative Sobolev norm is <W,(-G)^(-1)W> on mean-zero functions (connected sector). In the spectral representation the scalar convolution is at most min(T,1/alpha) at eigenvalue -alpha, whose square is at most T/alpha. The exact finite-density obligation on diffusive horizons is therefore ||W||_{-1}/||F||=o(N); no estimate of this size is claimed here. This explicitly identifies the nonlinear remainder whose time-integrated influence must vanish to prove density closure at positive density. Static derivative alone cannot certify it.

## 6. Reference checks

Exact rational truth tables cover four interaction strengths and every local four-bit environment. Independent full microscopic generators for N=5,6,7 check the gradient identity; rational moment tests and floating first-Fourier comparisons check the residual structure. At K=2, lambda=3/2 the uniform normalized error bounds rounded upward are 0.240536, 0.084458, 0.029835, 0.010548 for N=128,1024,8192,65536. These are bounds, not measured errors. The finite erasure control uses two overlapping nonpure mixtures; it checks invariance of mixture weights under arbitrary finite erasure cylinders and their conditional mean separation, not the infinite-volume theorem itself. The latter rests on the imported Ising surface estimate, compactness and the pointwise ergodic theorem. The external Ising theorem was rechecked on printed page 22 of https://www.unige.ch/~velenik/papers/BIV00.pdf (Theorem 2.1.1). For context on the classical dynamic replacement principle see Ayala, Carinci and Redig, Quantitative Boltzmann-Gibbs Principles via Orthogonal Polynomial Duality, https://doi.org/10.1007/s10955-018-2060-7; its duality results are not imported as a proof for this interacting model.
