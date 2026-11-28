# CSM-G2-WP24 — finite-range phase obstruction and time-domain transport certificates

Internal candidate; originality UNADJUDICATED, no MATHCERT. Continues protected WP23 merge 13f82abe12810c37a72fef060cdcf322ec3f9c29. The phase theorem below imports an explicitly identified classical Ising surface-order theorem; the conservative canonical transfer and observable obstruction are derived here. No generic hydrodynamic limit or general observed nonquasilocality claim.

## 1. Short-range bilayer with a single conserved charge

Let Lambda be an even L by L square torus, L>=4, m=L^2. At each cell there are two occupations x_i,y_i in {0,1}. The physical graph comprises nearest-neighbor edges in both layers and vertical rungs, all with rate-one bond heat bath. Set sigma_i=2x_i-1 and tau_i=1-2y_i. On the globally half-filled sector sum_i(x_i+y_i)=m, use weight

$$
\exp\left[\beta\sum_{\langle i,j\rangle}(\sigma_i\sigma_j+\tau_i\tau_j)\right].
$$

This is finite-range, bounded degree and fixed positive temperature, with no hard constraints except the one total count. The graph is connected and every active swap has positive rate, so the sector chain is irreducible (tree swaps). Layer counts can change at rungs; cell counts can change along layers. No additional count invariant is assumed.

Let M=sum sigma_i, M'=sum tau_i. Half filling is exactly M=M'. If p_a is the zero-field periodic one-layer Ising magnetization distribution, the canonical common magnetization law is

$$
\mathbb P(M=a)=p_a^2/\sum_b p_b^2.
$$

The conditioning event has probability sum p_b^2 >=1/(m+1) by Cauchy-Schwarz, since there are m+1 values. Thus for any set U, the canonical probability M in U is at most (m+1) times the one-layer probability. Also the canonical law is symmetric. The layer-exchange involution (x,y)->(y,x) preserves every vertical-pair count k_i=x_i+y_i and the energy, and sends (sigma,tau)->(-tau,-sigma). On the sector it sends M to -M. Hence every odd function of M has conditional mean zero given the entire pair-count vector. In particular the sign f=sign(M) (zero at zero) and the bounded staggered layer-density difference S=M/m are orthogonal to the entire count algebra, not only the linear count span.

## 2. Transfer of the finite-temperature phase theorem

External input: Bodineau, Ioffe and Velenik, Rigorous probabilistic analysis of equilibrium crystal shapes, J. Math. Phys. 41 (2000), 3886–3931, https://www.unige.ch/~velenik/papers/BIV00.pdf , Theorem 2.1.1, printed page 22 of the supplied preprint. The periodic Ising surface-order large deviation statement applies in its specified coarse-graining temperature range; the remark includes sufficiently low fixed temperatures. Choose a fixed beta in this range, sufficiently large, and a fixed positive a_0 strictly between its lower magnetization threshold (or zero if larger) and spontaneous magnetization m_star(beta). The theorem gives a strictly positive surface cost for the nontrivial phase fraction and hence constants c>0,L_0 with one-layer probability |M|<=a_0 m at most exp(-c L) for L>=L_0. We use only this upper bound, not the precise Wulff shape. This is an imported theorem, not an independent derivation of surface tension; no numerical value of c is inferred from it.

Thus b_L=P_canonical(|M|<=2) <= (m+1) exp(-c L) for all sufficiently large L. Intralayer swaps preserve M and only a rung can change it by two. The sign can change only from the central band |M|<=2. There are m rung clocks of rate one and squared sign jump <=4. With reversible generator G, the Dirichlet energy obeys

$$
\mathcal E(f,f)\le 2m b_L,\qquad
\|f\|_2^2\ge1-b_L.
$$

Any lower spectral bound g on the count-orthogonal restriction of -G must therefore satisfy g<=2m b_L/(1-b_L) when b_L<1. The spectral Jensen inequality gives

$$
\langle f,e^{tG}f\rangle
\ge (1-b_L)\exp[-2m b_L t/(1-b_L)].
$$

Consequently the sign autocorrelation tends to one on every polynomial time horizon at this fixed positive temperature, with fixed total density 1/2 and finite-range physical interactions. Also E S^2 >= a_0^2 [1-(m+1) exp(-cL)], so the bounded local-density aggregate has nonvanishing omitted variance. This establishes a finite-range collective phase obstruction. Adding S as an algebra generator includes its sign and removes this particular hidden direction. It is not shown that the remaining discarded directions have a uniform gap. Nor is a noisy observation nonquasilocality theorem inferred merely from phase coexistence: that requires a separate conditional-discontinuity argument. The two-layer construction is a specified short-range model, not a proof for every canonical antiferromagnet.

## 3. From frequency-domain to time-domain certificates

Let G be any finite reversible nonpositive generator in equilibrium L2, and U a trial space containing the target f. Use orthogonal projection P_U and the compressed generator G_U=P_U G P_U on U. For T>0, integer n>=2 and h=T/n, set u_0=f and solve within U successively

$$
(I-hG_U)u_j=u_{j-1},\qquad
r_j=u_{j-1}-(I-hG)u_j=h(I-P_U)Gu_j .
$$

The residuals are directly computable from generator actions and equilibrium inner products. With J=(I-hG)^(-1), ||J||<=1 and J u_{j-1}-u_j=J r_j. Telescoping gives ||J^n f-u_n||<=sum_j ||r_j||. For x>=0, putting a=n log(1+x/n) gives x-a<=a^2 exp(a/n)/(2n), by Taylor's formula. Consequently

$$
0\le (1+x/n)^{-n}-e^{-x}
\le e^{-a}(x-a)\le 2/n,
$$

since n>=2 and sup_{a>=0} a^2 e^{-a/2}=16/e^2. Spectral calculus now yields the time-domain certificate

$$
\|e^{TG}f-u_n\|_2\le (2/n)\|f\|_2+\sum_{j=1}^n\|r_j\|_2 .
$$

The bound is independent of ||G|| and applies at T proportional to L^2 with no artificial fast reset. It does not assert residual smallness at that horizon: the trial space must achieve it. All quantities can be enclosed rationally (including square roots by upward rational rounding). Equilibrium correlations follow by Cauchy-Schwarz. For general U the compressed generator need not be a Markov generator; neither positivity nor normalized posterior-path closure is claimed. Nested trial spaces or generator Krylov enrichment may improve the result but residual monotonicity is not assumed. Finite invariant Krylov spaces yield zero residual. This is a constructive a posteriori criterion, not a proof of efficient scale-uniform hydrodynamic closure.

## 4. Local equilibrium inner products without enumerating sectors

For a one-dimensional ring with positive rational site factors w_i and nearest-neighbor pair factors lambda_i, weight(x)=prod_i w_i^{x_i} lambda_i^{x_i x_{i+1}}. The partition function at fixed K, including arbitrary prescribed bits on a set of sites, can be evaluated by a transfer recurrence keeping first bit, last bit and accumulated count. Append bit b with factor w_i^b lambda_{i-1}^{a b} where a is previous bit; forbid prescribed mismatches; close with lambda_{N-1}^{last*first}. Sum terminal entries at count K. There are O(N K) arithmetic operations, ignoring integer bit complexity. For a local cylinder function of support size s, sum its values against the exact marginal probabilities from these prescribed-bit partition functions, O(2^s N K) operations. Products require only the union of their supports. G applied to a cylinder function sums only physical bonds meeting its support; the swap rates depend only on the endpoints and their nearest neighbors. Hence each local term extends support by at most two lattice steps and can be evaluated from a finite truth table. Finite sums of local cylinder functions allow Gram and residual inner products by pairwise summation, without constructing the global configuration space. This provides an exact one-dimensional interacting equilibrium route to the time certificate. It does not bound the size of the selected basis or support growth at long times, or solve two-dimensional local marginal computation. The reference implementation uses this transfer recursion and rational local generator actions; small-sector enumeration is used solely as a verification oracle.

## 5. Exact reference replay

At L=4 and beta=log 4 (aligned-bond factor 16), a single-layer row transfer computes the magnetization distribution with exact integers, checked against independent enumeration of the 65536 single-layer states. Squaring the probabilities and renormalizing evaluates the 32-site canonical bilayer without enumerating its half-filled sector. The collision probability is approximately 0.4997540, central band mass 1.743506e-18, and discarded Rayleigh upper bound 5.579218e-17 (rounded upward for the last two); these are finite-size evaluations of exact rational bounds, not fitted asymptotics. An independent connected eight-site bilayer tests count invisibility, nonconservation of individual layer and cell counts, and the sign energy inequality.

A six-site interacting ring (pair factor 3/2) has 20 half-filled microstates. Its centered adjacent-pair count generates a three-dimensional invariant Krylov space. For T=36 and 64 implicit Euler steps the exact accumulated residual is zero and the certified absolute L2 error is below 0.020911 (not a relative error certificate for the small remaining correlation). Exact rational full-sector implicit Euler agrees with the reduced result. This small invariant-space example is not a scaling theorem. Independently, local cylinder Gram, stiffness and leakage forms for a nonuniform interacting ring match the full generator oracle; a 64-site half-filled ring with pair factor 3/2 gives exact rational nearest-neighbor joint occupancy probability approximately 0.2712791 by transfer without sector enumeration. Six regression groups cover these results and invalid input rejection.

## 6. Remaining boundaries

Classical ingredients: Ising surface-order large deviations (cited theorem), reversible Dirichlet forms and spectral Jensen, implicit Euler rational approximation and Galerkin residuals, transfer matrices. The CSM synthesis is the canonical collision conditioning and count-preserving phase symmetry in a connected finite-range particle model, plus a constructive time residual with exact local inner-product route in one dimension. Remaining: uniform diffusive residual certificates for nontrivial interacting families, finite-range noisy observation conditional discontinuity, and sufficiency of phase-augmented algebra. No G3 promotion.
