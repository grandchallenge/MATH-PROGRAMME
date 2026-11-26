# CSM-G2-WP18 — local energetic response and global conservation

Internally derived candidate; originality UNADJUDICATED, no MATHCERT. Continues WP17 protected merge 782f113fc8881927b4aba48aa93e49d1573a0cac. Scope: interacting fixed-time binary canonical Gibbs law, and a separate exact single-observation response for uniform conservative dynamics.

## 1. Local certificate

On N>=3 sites, fixed count K, take positive weights w_i and symmetric positive pair factors lambda_ij (one for absent edges). The mass is proportional to the product of occupied site weights and pair factors for doubly occupied edges. Both compared laws have the same interactions and count, and weights in [a,b]. Set R=b/a. Define symmetric nonnegative kappa_ij >= |log lambda_ij|/4, diagonal zero, L=max row sum kappa, and B=max_i product_j max(lambda_ij,1/lambda_ij). Put Q=R B^2, eta=1/(1+Q), M=N(N-1)/2,

$$
A_0=1+(N-2)\eta,\qquad A=A_0-2(N-3)L.
$$

Require A>0. A positive uniform margin follows from eta>2L, but the finite condition is sufficient. All constants can be checked rationally by choosing kappa_ij=(max(lambda_ij,1/lambda_ij)-1)/4. Every complete-graph pair heat bath is a genuine conditional; local physical bond exchanges on any connected graph are also irreducible in a sector. The complete graph is an auxiliary proof device, not the physical transport graph.

## 2. Coupling and global response

For states x,y at swap distance one, differing at i,j, use WP17's bond permutation coupling. On {i,j} coalesce because their exterior agrees. For each l outside the difference pair, one of the two paired bonds permits simultaneous swaps and coalescence; the other has equal bits in each chain. Both swap with probability at least eta: the conditional odds between two placements are bounded between 1/Q and Q because the pair factor itself does not contribute when exactly one endpoint is occupied. A one-sided swap moves one disagreement but does not increase distance. For a bond {u,v} avoiding i,j, if the bond is active, conditional log odds differ by at most four times kappa_ui+kappa_uj+kappa_vi+kappa_vj; the derivative of the logistic function is at most 1/4. Common-uniform coupling therefore adds at most this sum of kappas to expected swap distance. Summing outside bonds gives at most 2(N-3)L. Consequently expected distance is at most 1-A/M. Glue along shortest swap paths to extend the contraction to every pair.

For two fields w,w', set tau_i >= |log(w'_i/w_i)|/4, T=sum tau_i. On the same input configuration a common-bond maximal coupling of the two kernels has swap disagreement probability at most tau_u+tau_v. Thus its expected distance is at most (N-1)T/M. Compose this coupling with the same-model contraction via finite conditional disintegration. A stationary coupling exists by finiteness; the marginal invariant laws are unique within the sector. Writing e_i for coordinate mismatch probabilities and D=sum e_i/2, stationarity yields

$$
D\le (N-1)T/A.
$$

This is uniform over K, including singleton sectors, and gives an average response of order T/N for uniform positive gain. No sign condition on interactions is imposed.

## 3. Local versus reservoir response

For the adjacent pair x,y of Section 2, a disagreement at k in {i,j} survives with probability at most 1-A_0/M (all guaranteed coalescences remove both). If k is outside {i,j}, its possible new mismatch arises from one paired coalescing-capable bond with probability at most 1/M, and outside bonds containing k. Summing their logistic bounds yields at most

$$
\frac{1+2L+(N-3)(\kappa_{ki}+\kappa_{kj})}{M}.
$$

Indeed each term involving k occurs N-3 times, and the sum of remaining terms is at most 2L. Glue the same adjacent couplings along a shortest swap path; each initially discrepant coordinate appears exactly once, and the mismatch indicator obeys the triangle inequality. For any pair, the resulting coupling has coordinate mismatch bound given by summing these estimates. For the field-change coupling on a common state, the coordinate source at k is bounded by ((N-2)tau_k+T)/M, summing the N-1 incident bonds. The two couplings can be glued simultaneously, so the stationary coupling used for the global bound also satisfies

$$
A_0 e_k\le (N-3)\sum_l\kappa_{kl}e_l+(1+2L)D+(N-2)\tau_k+T.
$$

Let G=(N-3)kappa/A_0, q=(N-3)L/A_0<1 (indeed A>0 implies q<1/2 when N>3), and let r_k be graph distance to the support of tau in the graph of positive kappa entries (the interaction graph for the stated rational choice). The stationary inequality and the convergent nonnegative Neumann series give

$$
e_k\le \frac{T[1+(1+2L)(N-1)/A]}{A_0(1-q)}
+\frac{(N-2)\max_i\tau_i}{A_0(1-q)}q^{r_k}.
$$

For disconnected sites the second term is zero; use 0^0=1 for a source when q=0. The bound also holds if tau vanishes identically, with both terms zero. The first term is an inverse-volume reservoir term for fixed T and uniform margins; the second is exponentially decaying energetic response. Target TV for a finite set is at most the sum of its coordinate bounds, capped at one. Positive local observation likelihoods are field multipliers; stochastic channels contract TV. For an insertion function bounded below by c>0, log discrepancy is at most target TV/c. This does not establish uniform decay for extensive clamps or arbitrary time histories. It is a sufficient high-temperature certificate, not necessary; failure is undecided.

## 4. Exact sparse specimen

For a ring with pair factor 17/16, all initial weights one, and a single changed weight 9/8, exact rational certificate evaluation gives far-field bounds below 0.002559, 0.000325 and 0.00004069 for N=128, 1024 and 8192, respectively (rounded upward). The q values are below 0.077. These are certificate bounds, not estimates of actual observed correlations. No sector enumeration occurs in the sparse producer. Small exact enumeration tests cover attractive and repulsive factors, every particle count for sizes 4 through 8, adjacent coupling inequalities, and time-dependent response.

## 5. Exact time-dependent observation control

For uniform fields and unit interactions, use the actual nearest-neighbor random-scan bond heat bath on a finite connected graph with E edges. On occupation expectations its linear operator is P=I-Laplacian/(2E). In the uniform K sector let rho=K/N. Exchangeability gives same-time covariance matrix rho(1-rho)N/(N-1) times (I-ones/N). Conditional expectation of the future occupation vector is P^t x; hence

$$
\mathrm{Cov}(X_i(t),X_j(0))=\rho(1-\rho)\frac{N}{N-1}\left((P^t)_{ij}-\frac1N\right).
$$

A single strictly positive observation at j,time 0 with likelihood ratio h reweights the path law by h to the power X_j(0). Exact target occupation response at i,time t equals this covariance times (h-1)/(1+(h-1)rho). A binary target observation with likelihood values L(0),L(1) multiplies the response by L(1)-L(0). This is actual time-dependent observation conditioning, but only one source observation on uniform exclusion, not arbitrary conditioned interacting trajectories. By reversibility it also holds backward in time. On the cycle the Fourier eigenvalues are 1-(1-cos(2pi k/N))/N. The zero mode is removed exactly by the fixed count; nonzero modes diffuse. This does not imply an infinite-volume conditional phase obstruction.

## 6. Prior art and frontier

Canonical ensemble comparisons, conservative mixing and exclusion duality are established mathematics. Cancrini, Martinelli and Roberto, The logarithmic Sobolev constant of Kawasaki dynamics under a mixing condition revisited (2002), https://doi.org/10.1016/S0246-0203(01)01096-2, abstract, study canonical lattice gas exchange under high-temperature mixing; no equivalence or improvement over their assumptions is claimed. Liggett, Stochastic models for large interacting systems and related correlation inequalities (2010), https://pmc.ncbi.nlm.nih.gov/articles/PMC2944758/, discusses exclusion and duality. The local certificate and reservoir/energetic decomposition above are bounded CSM synthesis; priority unadjudicated. Next: genuinely interacting time-dependent posterior under multiple observation clamps, on the physical graph; compare transport kernels without assuming a uniform spectral gap. No full G2/G3 promotion.
