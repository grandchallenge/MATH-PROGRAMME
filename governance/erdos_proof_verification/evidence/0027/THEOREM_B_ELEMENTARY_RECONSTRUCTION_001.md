# Erdős 27: Lemmas 3.3, 3.4, 4.1 and Theorem B

Supplementary research reconstruction; no second Phase C RESULT/1 and no promotion of the C formal scope. Source: FFKPY, Sieving by large integers and covering systems of congruences, 21 December 2006 manuscript, DOI 10.1090/S0894-0347-06-00549-2, https://ford126.web.illinois.edu/wwwpapers/coverings.pdf. Visually rechecked printed pp. 12–14, 19–20; original source lock SHA256 aabca6f856644c89826e9f9c8c46f03a92c9f3e46c41ee443b4d6670463014e9 reused, no fresh byte acquisition claimed. Uses the already admitted finite Lemmas 2.1, 3.1 and elementary reconstruction of 3.2. Here we independently reconstruct the distinct-modulus Theorem B directly, not the full multiplicity generalization Theorem 4.

## Lemma 3.3: geometric mean

Write C for the finite set of residue pairs (n,r), alpha(C)=product over pairs (1-1/n), and delta(C) for uncovered density. Split each modulus n=a*b into its Q-smooth part a and Q-rough part b; M=lcm of the smooth parts. Let C_h be the set of pairs (b,r) with h=r mod a, as in Lemma 3.1. The smooth-only subsystem C' consists of pairs with b=1. Let G be the set of h mod M for which no projected modulus is 1, let g=|G|, and d=g/M=delta(C')>0. For h outside G alpha(C_h)=0, and for h in G every projected modulus exceeds Q.

Set lambda=1+1/Q. For b>Q>=2, log(1-1/b)>=-lambda/b: indeed for x=1/b<=1/2 the power series tail sum_{j>=2}x^j/j<=x^2/(2(1-x))<=x^2. Therefore AM-GM on the g positive factors gives
mean_h alpha(C_h) >= d exp(-lambda/g * sum_{h in G} sum_{(b,r) in C_h}1/b).
Every original pair activates in exactly M/a fibres. Projected deduplication can only reduce the sum of positive weights. Hence the sum over ALL fibres is at most M sum_{(n,r) in C}1/n. Each bad fibre contributes at least 1 to that sum, so the good-fibre sum is at most M (S-1+d), where S=sum_C 1/n. Consequently
mean alpha >= d exp(lambda(1-d)/d) exp(-lambda S/d).
The first two factors have product >=1: with t=1/d>=1, t-1>=log t, and lambda>=1. Finally alpha(C)<=exp(-S), from log(1-x)<=-x. (Under d>0 the original modulus 1 cannot occur.) Thus
mean alpha(C_h) >= alpha(C)^(lambda/d).
This proves Lemma 3.3, including the empty family case. The restriction d>0 is indispensable, not just a division-by-zero convention.

## Lemma 3.4: synthesis

By the finite CRT density identity and Lemma 2.1, delta(C)>=mean alpha(C_h)-mean beta(C_h). Apply Lemma 3.3 and the uniform correlation bound in the protected companion documents to obtain
delta(C)>=alpha(C)^((1+1/Q)/delta(C'))-A s^2 log^2(QK)/Q,
with an absolute A, for multiplicity at most s and all moduli in (N,KN]. This is the precise one-sided interpretation of the source's signed O-term.

## Lemma 4.1: independent elementary smooth reciprocal tail

Let Q>=2, Q<N<=exp(sqrt(Q)), u=log N/log Q>1. Define P_t(Q)=product_{p<=Q}(1-p^(-t))^-1 for t>0. We use only the elementary estimates already proved in LEMMA32_ELEMENTARY_ANALYTIC_INPUTS_001.md: theta(x)=sum_{p<=x}log p<=A0 x for x>=1, and P_1(Q)<=A1 log Q. We prove the full required tail
sum_{n>N, P(n)<=Q}1/n <= A2(log Q) u^(-u),
where A2 is absolute.

For 0<=z<=1/2, differentiating the finite product logarithm gives derivative sum_{p<=Q} log p/(p^(1-z)-1) <= C sum_{p<=Q}(log p)p^(z-1), since p^(1-z)>=sqrt(2). By partial summation using theta(x)<=A0 x, for z>0,
sum_{p<=Q}(log p)p^(z-1) <= A0[Q^z+(Q^z-1)/z].
The z=0 case follows by continuity. Integrate from 0 to t<=1/2 and set v=t log Q>=1:
log(P_(1-t)(Q)/P_1(Q)) <= C'[(exp(v)-1)/log Q + integral_0^v (exp(w)-1)/w dw] <= C'' exp(v)/v.
For the final inequality, log Q>=2v. On [0,v/2], (exp(w)-1)/w<=exp(w), so its integral <=exp(v/2); on [v/2,v], 1/w<=2/v, so the integral <=2exp(v)/v. The first term is bounded by a constant times exp(v)/v since v exp(-v/2) is bounded. All constants are absolute.

For Q>=exp(e), choose v=log u+1 and t=v/log Q. The upper hypothesis u<=sqrt(Q)/log Q gives v<=0.5 log Q because log log Q>=1. Thus t<=1/2. Rankin's inequality, using unique prime factorization and absolute convergence of the finite Euler product, yields
sum_{n>N,smooth}1/n <= N^(-t) P_(1-t)(Q)
 <= A1 log Q * exp(-u(log u+1)+C'' e*u/(log u+1)).
For all sufficiently large u (absolute threshold), the last positive term is <=u, proving the desired estimate. For 1<u below that threshold, u^u is bounded and the trivial bound P_1(Q) suffices after enlarging A2. For 2<=Q<exp(e), u is also bounded by sqrt(Q)/log Q, and the same trivial bound applies. This handles the full uniform domain of Lemma 4.1. No de Bruijn distribution theorem or prime number theorem is imported.

## Theorem B: direct parameter selection for multiplicity one

Fix 0<c<1/2. Let N tend to infinity and 1<K<=exp(c T), T=log N * log log log N / log log N. For a finite set S of distinct integers in (N,KN], choose arbitrary residues. Write L=log N, l=log L, m=log l, so T=L m/l. Choose d0=(c+1/2)/2 strictly between c and 1/2, Q=exp(d0 T). For large N, Q>=2, Q<N<=exp(sqrt Q), and u=L/log Q=l/(d0 m). As N grows,
u log u = (l/d0)(1-(log m+log d0)/m) = (1/d0+o(1)) l.
By the union bound and Lemma 4.1, e0=1-delta(C') <= C(log Q)exp(-u log u) = O(L^(1-1/d0+o(1))). Since d0<1/2, e0 L=o(1). In particular delta(C')>0 eventually. Set E=(1+1/Q)/delta(C'); then E-1=O(e0+1/Q).

The product alpha(S) is bounded below by the full-interval telescoping product floor(N)/floor(KN) (empty interval product 1). This is >=(1-1/N)/K. Hence 0<=-log alpha<=log K+O(1/N)<=cT+O(1/N)=O(L), uniformly in K and S. Therefore alpha^E/alpha=exp((E-1)log alpha)=1-o(1), uniformly in both.

The additive error in Lemma 3.4, divided by alpha, is at most
C' K log^2(QK)/Q <= exp(-(d0-c)T+O(log L))=o(1),
since T/log L tends to infinity. Thus every residue assignment has delta(C)>=(1-o(1))alpha(S), uniformly over K and S. For the matching upper bound, start with all integers and successively choose a residue class modulo each n that removes at least 1/n of the remaining density, by partition and averaging on a common period. Each step multiplies the residual density by at most 1-1/n. This constructs a choice with delta(C)<=alpha(S). Taking the minimum over finitely many choices proves delta^-(S)=(1+o(1))alpha(S), with error controlled only by c. This is precisely the distinct-modulus Theorem B (not Theorem A, the general multiplicity theorem, or the historical minimum-modulus question).

## Role-scoped critical audit

The proof uses a positive good-fibre count and never takes logs of zero; the subtraction of at least one weight per bad fibre is essential to cancel the AM-GM prefactor. Deduplicated projected pairs give a one-sided inequality, not equality. Prime product differentiation is only on t>=1/2 in its exponent, so no singular factor is encountered; the integration variable z is distinct from that exponent. The Rankin product counts all smooth positive integers, including 1, but the left tail excludes 1. The small-Q and bounded-u regimes are covered by absolute constants, not extrapolation of a large-u estimate. Both parameter margins c<d0 and d0<1/2 are required for this proof; at c=1/2 there is no such d0. The proof is uniform over all real K in the allowed range, even if the interval contains no integers. The upper bound requires a choice of residues, not every assignment. Prior admitted Lemmas 2.1, 3.1 and 3.2 carry their existing scope; no kernel formalization of the analytic chain is claimed. The same accountable operator performed author and logical critic roles. This is a reconstruction of the already published result, not new mathematics, independent external review, MATHCERT or a new closure status. Finite regression separately checks the good-fibre bound and synthesis; tests do not replace the analytic proof.
