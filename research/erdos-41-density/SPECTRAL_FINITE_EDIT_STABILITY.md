# Erdős #41 — A finite-edit stability barrier for normalized Fourier sixth moments

**21 October 2026. Research status:** exact finite-edit theorem and an infinite *sequence of finite hostile witnesses*. This is a **bounded negative result about spectral observables**, not an infinite B3 counterexample, density-valley proof, or independent mathematical certification.

The prior protected note \`research/erdos-41-density/FOUR_ROUTE_FIRST_FALSIFICATION.md\` showed that weak empirical measures of critical-order finite B3 sets and nearby non-B3 sets can become indistinguishable. Here we strengthen the obstruction: even supplementing the weak measure with the **leading normalized sixth Fourier moment** does not recover the exact B3 property.

## 1. Exact representation function and repeated-summand convention

Let E be any n-point subset of the integers. Define its ordered three-sum representation function and sixth energy by

$$
r_E(s)=|\{(a,b,c)\in E^3:a+b+c=s\}|,
\qquad
\mathcal E_6(E)=\sum_s r_E(s)^2
=\int_0^1\left|\sum_{a\in E}e^{2\pi ia\theta}\right|^6d\theta.
$$

If E is repetition-permitted B3, every unordered triple has a unique sum, and the three order multiplicities are 6 (all distinct), 3 (exactly two equal), and 1 (all equal). Hence

$$
\mathcal E_6(E)
=36\binom n3+9n(n-1)+n
=6n^3-9n^2+4n.
$$

A non-B3 set has strictly larger sixth energy, but the *normalized* excess may be small.

## 2. Uniform finite-edit energy stability theorem

**Theorem A (fixed-edit spectral nonidentifiability).** Let A and B be finite integer sets with the same cardinality n, with A repetition-permitted B3. Suppose their common intersection C=A∩B has cardinality n−r, where 0≤r≤n. Then

$$
\boxed{
0\le \mathcal E_6(B)-\mathcal E_6(A)
\le
6r\bigl(12+6r+3r^2+r^3\bigr)n^2.
}\tag{FINITE-EDIT-SIXTH-ENERGY}
$$

The lower bound is valid for every B because the B3 sixth-energy value is the minimum for an n-point set. The upper bound depends only on the number of edited elements, not their magnitudes, the ambient interval, or the location of integer sums.

**Proof.** Let \(r_C\) be the ordered triple-sum representation function of C, and write

$$
r_A=r_C+u,\qquad r_B=r_C+v.
$$

All of u,v are nonnegative integer functions. They count ordered triples containing at least one of the r special elements in A\C or B\C. Consequently,

$$
\sum_s u(s)=\sum_s v(s)=n^3-(n-r)^3\le3rn^2.
$$

Because C⊂A is B3, its **unordered pair sums are all distinct**, including equal summands. For any prescribed integer sum s, the ordered triples with exactly one special element have at most \(3\cdot r\cdot2=6r\) possibilities: choose its position and value; at most one unordered pair from C has the required complementary sum, with at most two orders. Those with exactly two special elements contribute at most \(3r^2\) possibilities: choose the position of the single C value and the two ordered special values, which uniquely determine it. Those with all three special contribute at most \(r^3\). Therefore, for all s,

$$
0\le u(s),v(s)\le M_r:=6r+3r^2+r^3.
$$

Also B3 uniqueness yields \(0\le r_C(s)\le6\). Subtracting the energies gives

$$
\begin{aligned}
|\mathcal E_6(B)-\mathcal E_6(A)|
&=
\left|\sum_s(2r_C(s)(v(s)-u(s))+v(s)^2-u(s)^2)\right|\\
&\le(12+M_r)\sum_s(u(s)+v(s))\\
&=2(12+M_r)(n^3-(n-r)^3)\\
&\le6r(12+M_r)n^2.
\end{aligned}
$$

Since A is B3, its energy is minimal, establishing the displayed two-sided bound. QED.

**Corollary.** For a sequence of n-point B3 sets A_n with n→∞, and any B_n obtained by a fixed number r of point replacements,

$$
\boxed{
\frac{\mathcal E_6(B_n)}{n^3}
-
\frac{\mathcal E_6(A_n)}{n^3}
=O_r(1/n)\longrightarrow0,
\quad
\frac{\mathcal E_6(A_n)}{n^3}\longrightarrow6.
}\tag{NORMALIZED-MOMENT-NO-GO}
$$

If the two sets are placed in any common integer interval of width W_n, their normalized empirical probability measures differ in total variation by at most r/n, and all their rescaled Fourier modes by at most 2r/n. Hence **weak empirical measures together with normalized sixth energies still cannot distinguish B3 from non-B3**.

This does NOT say the exact sixth moment is insensitive. The exact nonnegative integer defect \(\mathcal E_6(B)-(6n^3-9n^2+4n)\) detects all B3 violations and must be retained if this particular spectral route is pursued.

## 3. Explicit arbitrary-size critical-order hostile witnesses

For each prime p>3 take the p-point finite-field moment-code B3 set

$$
T_p=\left\{
1+i+(3p+1)(i^2\bmod p)+(3p+1)^2(i^3\bmod p)
:0\le i<p\right\}
\subseteq[1,W_p]
$$

with \(W_p=p(1+(3p+1)+(3p+1)^2)+1<12p^3\). No-carry base expansion and Newton's identities establish that \(T_p\) is B3 including repeated summands.

Let

$$
T'_p=\{1,2,3\}\cup\{e_i:3\le i<p\}.
$$

Both sets have exactly p distinct elements and meet the same critical endpoint-order lower count

$$
|T_p|=|T'_p|=p>(W_p/12)^{1/3}.
$$

But \(T'_p\) is **not B3**, because the distinct unordered triples (1,1,3) and (1,2,2) both sum to 5. The two sets differ at no more than three points each way (r≤3). Theorem A gives

$$
0<
\frac{\mathcal E_6(T'_p)-(6p^3-9p^2+4p)}{p^3}
\le\frac{1512}{p}
\longrightarrow0.
$$

Every empirical Fourier mode on the rescaled width simultaneously differs by at most \(6/p\). Thus the hostile example persists even when the state includes the weak rescaled empirical measure AND the leading sixth-energy coefficient.

**Logical limits.** These are finite sets whose *endpoint populations* have critical order; neither family satisfies a positive normalized lower bound for all large N as a single infinite set. The theorem does not rule out exact unnormalized spectral defects, full integer-frequency Fourier data, or a nonstationary transfer inequality that amplifies the subleading O(n²) discrepancy across infinitely many scales.

## 4. Mathematical research next step for Track D

The mathematical observable cannot simply be a weak limit of \(\mu_n\) plus \(\mathcal E_6(E_n)/n^3\). The following exact integer defect remains faithful for finite configurations:

$$
\boxed{
\mathfrak d_6(E)=\mathcal E_6(E)-(6|E|^3-9|E|^2+4|E|)\in\mathbb Z_{\ge0},
\qquad
\mathfrak d_6(E)=0\Longleftrightarrow E\text{ is B3}.
}
$$

For an actual B3 prefix, \(\mathfrak d_6=0\) at EVERY stage, while all cross-scale shell choices must preserve that exact zero. A useful new Fourier approach needs a *transfer obstruction* showing that maintaining these infinitely many exact zero conditions together with positive critical density is impossible. Merely enforcing a limiting density and limiting sixth moment is insufficient.

The source programme remains issue #2789; Track D #2793 and critical audit Track C #2792. No independent role has yet submitted authenticated RESULT/1 for this candidate.
