# Elementary proofs of the three analytic inputs for FFKPY Lemma 3.2

Companion to LEMMA32_CORRELATION_RECONSTRUCTION_001.md. The earlier conditional argument is retained as a dependency ledger; all three dependencies are discharged below by general proofs. This is an alternative elementary reconstruction of the published Lemma 3.2, not a claim of novelty, a replay of the cited Halberstam–Richert text, or a reconstruction of full Theorem B.

## 1. Uniform upper-bound sieve (H1)

For real x>=1, Q>=2 define F_Q(x) as the number of positive integers <=x with no prime divisor <=Q, including 1. If x<Q, F_Q(x)=1. Suppose x>=Q and let D=floor(min(Q,x^(1/4)))>=1. We prove

F_Q(x) <= x/G(D)+D^2, where G(D)=sum_{k<=D} mu(k)^2/phi(k).

Here mu is the Mobius function and phi the Euler totient. The weights are explicitly finite; no asymptotic sieve theorem is imported. Put y_k=mu(k)/(phi(k)G(D)), and define

lambda_d/d = sum_{k<=D,d|k} mu(k/d)y_k   (1<=d<=D).

Finite Mobius inversion gives y_k=sum_{d<=D,k|d} lambda_d/d and lambda_1=sum mu(k)y_k=1. Inversion follows by interchanging the finite sums and using sum_{a|n}mu(a)=1 for n=1 and 0 otherwise. The latter is the expansion of (1-1)^r over the distinct primes of n. The elementary identity sum_{a|n}phi(a)=n follows by classifying 1<=j<=n by gcd(j,n).

If d is not squarefree, lambda_d=0 since every k divisible by d has mu(k)=0. For squarefree d, multiplicativity of mu and phi gives

lambda_d = mu(d) d/phi(d) * G_d(D/d)/G(D),
G_d(T)=sum_{m<=T,gcd(m,d)=1} mu(m)^2/phi(m).

For each squarefree m counted in G_d(D/d) and each k|d, km<=D and km is squarefree. The products km are distinct, because gcd(km,d)=k, and phi(km)=phi(k)phi(m). Summing their positive contributions gives
G(D) >= G_d(D/d) sum_{k|d}1/phi(k) = G_d(D/d) d/phi(d).
The final product identity uses squarefreeness of d: each local sum is 1+1/(p-1)=p/(p-1). Therefore |lambda_d|<=1.

For every counted rough n, no d>1 with d<=D can divide n (any such divisor has a prime factor <=D<=Q). Hence the sum of lambda_d over divisors d<=D of n equals 1; for any other n its square is nonnegative. Summing yields

F_Q(x) <= sum_{n<=x}(sum_{d<=D,d|n}lambda_d)^2
       = sum_{d,e<=D}lambda_d lambda_e floor(x/lcm(d,e)).

Replace each floor by x/lcm(d,e) with absolute total error <=(sum|lambda_d|)^2<=D^2, valid even for signed weights. The exact quadratic form equals

sum_{d,e<=D}lambda_d lambda_e/lcm(d,e)
 = sum_{k<=D}phi(k)(sum_{d<=D,k|d}lambda_d/d)^2
 = sum_{k<=D}phi(k)y_k^2
 = 1/G(D),

using 1/lcm(d,e)=gcd(d,e)/(de) and the divisor-sum identity above. This proves the finite sieve inequality.

To bound G(D), write each positive integer t uniquely as a squarefree a times b^2. The harmonic sum H_D=sum_{t<=D}1/t is at most
(sum_{b>=1}1/b^2) sum_{a<=D,squarefree}1/a <= 2G(D),
because phi(a)<=a and the convergent square sum is <=2 by integral comparison. Thus G(D)>=log(D+1)/2. Since x>=Q, D+1>min(Q,x^(1/4))>=Q^(1/4); hence G(D)>=(log Q)/8. Also D^2<=sqrt(x)<=x/log Q: log Q<=log x<=sqrt(x) for x>=1 (the minimum of sqrt(x)-log x occurs at x=4 and is positive).

Therefore F_Q(x)<=9x/log Q when x>=Q, and F_Q(x)<=9x/log Q+1 for every x>=1,Q>=2. This explicitly proves H1, with a uniform constant, including the small-x case.

## 2. Elementary prime count (H2)

Let theta(t)=sum_{p<=t}log p. For each integer m>=1, the product of primes m<p<=2m divides binomial(2m,m): these primes occur in the numerator product (m+1)...(2m) but not in m!. Thus theta(2m)-theta(m)<=log binomial(2m,m)<=2m log 2. Sum for m=1,2,4,...,2^(k-1) and choose k minimal with x<=2^k. For x>=2, theta(x)<=theta(2^k)<2^(k+1)log 2<=4x log 2. Every prime p>sqrt(x) contributes at least (log x)/2 to theta(x), while at most sqrt(x) positive integers lie below sqrt(x). Thus

pi(x)<=sqrt(x)+2 theta(x)/log x <= (1+8 log 2)x/log x,

using log x<=sqrt(x). This proves H2 for all x>=2. The dyadic prime-square-tail argument in the companion file then applies.

## 3. Elementary prime product upper bound (H3)

For Q>=2 let sigma=1+1/log Q and P_t(Q)=product_{p<=Q}(1-p^(-t))^-1. The finite product expansion has nonnegative terms, all corresponding to positive integers (unique prime factorization), so

P_sigma(Q)<=sum_{n>=1}n^-sigma<=1+1/(sigma-1)=1+log Q.

By convergent logarithmic series (finite number of primes), and 1-exp(-u)<=u for u>=0,

log P_1(Q)-log P_sigma(Q)
 = sum_{p<=Q}sum_{k>=1}(p^-k-p^(-k sigma))/k
 <= (sigma-1) sum_{p<=Q}log p/(p-1).

Since p>=2, the last prime sum is <=2 sum_{p<=Q}log p/p. Partial summation and the theta bound of Section 2 imply

sum_{p<=Q}log p/p = theta(Q)/Q + integral_1^Q theta(t)/t^2 dt
 <= 4 log 2 (1+log Q).

Multiplying by sigma-1 bounds the log product difference by the absolute constant 8 log 2 (1+1/log 2). Consequently P_1(Q)<=C log Q for an absolute C, using 1+log Q <=(1+1/log 2)log Q. This proves precisely H3; no full Mertens theorem, prime number theorem, or analytic sieve black box is needed.

## 4. Scope and adversarial review

Sections 1–3 establish the three premises of the companion proof. Substitution gives the unconditional uniform Lemma 3.2 bound O(s^2 log^2(QK)/Q), where the constant is independent of the finite family, N>0, K>1, Q>=2 and multiplicity s. The exact finite reduction additionally retains the residue compatibility indicator. This is ordinary mathematical reconstruction of known results using elementary number theory, not kernel verification or a new theorem.

Separate role-scoped critical pass: the sign of lambda_d is not assumed nonnegative; the floor error uses absolute values. The choice D<=Q is essential for the rough-number majorant; the x<Q branch must not be dropped. Mobius inversion requires all multiples through D, not only primes; the squarefree restriction is a consequence of the formula. The distinctness of products km in the weight bound follows from gcd(km,d)=k, not from arbitrary factorization. The estimate for H3 uses the *upper* bound on the finite Euler product by the full Dirichlet series, not equality. The same accountable operator performed both roles; no externally independent referee or toolchain certification is claimed.

Exact local test: check_elementary_sieve.py, 64 weight domains D=1..64, 448 counting cases, exact rational inversion, closed-form weights, |lambda|<=1, quadratic identity, squarefree harmonic lower bound and floor-error majorant, with independent rough count and direct n-sum on small D. PASS, digest 4da08daa56939464cba50181c5893de3eed034047b02aece0e836469f5d4abe9, CHAD capture 078d647ee32c4956b9682c28540a6ae3. These tests support the algebra; the general proofs carry the analytic claims. The external Halberstam–Richert citation is not independently replayed, but is no longer a logical premise of this alternative derivation.

Remaining original-proof work: Lemma 3.3 geometric mean, Lemma 3.4 synthesis, Lemma 4.1 smooth-number reciprocal tail (different from rough sieve H1), and the final parameter selections in Theorem B. Formal kernel verification remains separate.
