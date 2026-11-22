# Erdős #249 — WP09-G: a rational obstruction and an actual two-prime Cook-phase discriminator

**Research:** [MATH-PROGRAMME #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500).  
**Previous protected theorem:** WP09-F [PR #3621](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3621), protected merge 7105da0f786623e96d57db08161cebf4e2aecc9d.  
**Primary source lock:** Will Cook, *The Binary Totient Series*, [revision 3368d1e69467aec111eb3244843ad3542171ff96](https://github.com/wcook04/plectis-erdos/blob/3368d1e69467aec111eb3244843ad3542171ff96/paper/249/erdos-249-binary-totient-series.tex), Git blob 547ed9ed83500181a2e55047ce5df569b7cb49ac, section *An exponential-sum question*.  
**Claim status:** two bounded mathematical theorems. The first is a strict **no-free-amplification counterexample** for the inputs of WP09-F. The second proves a **positive actual Euler-totient two-prime conditional Cook cocycle Fourier contrast** not shared by that comparator. Original Erdős #249 OPEN. Cook's 10% first harmonic OPEN. MATHCERT NOT_SUBMITTED.

## 1. Why another single-prime energy estimate cannot close the problem

For any nonnegative integer sequence $a(n)\le n$ define the complete finite Cook numerator and phase for a fixed shift h:

$$
D^a_{h,N,L}=\sum_{j=1}^L2^{L-j}[a(N+h+j)-a(N+j)],
\qquad
E^a_{h,N,L}=\exp(2\pi i D^a_{h,N,L}/2^L).
\tag{1}
$$

Cook's sufficient irrationality criterion for **the actual totient**, not arbitrary a, requires for each h arbitrarily late blocks with

$$
2^L\ge16(2X+h+L+2),
\qquad
\mathrm{Re}\sum_{N=X}^{2X-1} E^\varphi_{h,N,L}\le\frac9{10}X.
\tag{2}
$$

WP09-F proves strict but small saving using a signed fixed-prime first moment for $d_h(n)=\varphi(n+h)-\varphi(n)$ and the exact phase cocycle. The following exact example proves that those ingredients **alone**, even together with parity, positivity, integer coefficients, the size envelope and **all** multistep phase recurrences, cannot imply the required ten-percent saving.

## 2. Theorem A: an even-valued rational hostile with *strong* WP09-F source bias

For $k\ge1$ define periodic base-four digits

$$
b_1=1,\qquad
b_{3m+2}=0,\quad b_{3m+3}=1,\quad b_{3m+4}=3
\quad(m\ge0).
\tag{3}
$$

Define the explicit nonnegative integer sequence

$$
\boxed{
a(2k+1)=2k,\qquad
a(2k)=2b_k\quad(k\ge1),
\qquad a(1)=0.
}
\tag{4}
$$

This definition of odd positions also covers k=0. For every n, $a(n)$ is **even** and $0\le a(n)\le n$. In particular it respects the elementary parity property of $\varphi(n)$ for n≥3, while not claiming to match the totient's multiplicative structure or lower envelope.

**Theorem A (unconditional parity-compatible rational countermodel).** The complete binary series of (4) is **exactly one**:

$$
\boxed{\sum_{n=1}^{\infty}\frac{a(n)}{2^n}=1.}
\tag{5}
$$

For the shift $h=1$, terminal offset $s=L+1$, prime $p=2$ and every $X\ge32$ with $s+1\le X$, the sequence has the **same directions of signed fixed-prime source bounds** used in WP09-F, with at least its stated magnitudes:

$$
\boxed{
\begin{aligned}
\sum_{\substack{X\le N<2X\\N+s\equiv0\pmod2}}
 [a(N+s+1)-a(N+s)]&\ge X^2/8,\\
\sum_{\substack{X\le N<2X\\N+s\equiv1\pmod2}}
 [a(N+s+1)-a(N+s)]&\le-X^2/8,\\
\left|\sum_{\substack{X\le N\le2X-2\\N+s\equiv r\pmod2}}
 [a(N+s+1)-a(N+s)]\right|&\ge X^2/16,\\
\sum_{\substack{X\le N\le2X-2\\N+s\equiv r\pmod2}}
 [a(N+s+1)-a(N+s)]^2&\ge X^3/256
\end{aligned}}
\tag{6}
$$

for either parity $r=0,1$. Nevertheless, for **EVERY** h≥1 and every Cook-admissible pair $(X,L)$,

$$
\boxed{
\mathrm{Re}\,E^a_{h,N,L}
>\cos(\pi/8)>9/10
\quad\text{for EVERY }X\le N<2X.
}
\tag{7}
$$

Therefore the full first harmonic of this *rational comparison sequence* is **always greater than $0.9X$**, despite source first moments far stronger than WP09-F requires for h=1. The failure is not restricted to selected blocks or a fixed depth.

### Exact geometric-series proof of the rational identity

The odd-position contribution is

$$
\sum_{k=0}^\infty\frac{2k}{2^{2k+1}}
=\sum_{k=0}^\infty \frac{k}{4^k}=\frac49.
$$

The base-four digits in (3) satisfy

$$
\sum_{k=1}^\infty\frac{b_k}{4^k}
=\frac14+\frac{4^{-3}+3\cdot4^{-4}}{1-4^{-3}}
=\frac14+\frac1{36}=\frac5{18}.
$$

Since the even-position coefficient is $2b_k$, its entire contribution is $2(5/18)=5/9$. Adding gives $4/9+5/9=1$; this is an **exact infinite identity**, not a numerical truncation or finite-precision test.

The base-four digits are at most three. The only early potentially tight positions are $k=1,2,3,4$, where $2b_k$ equals $2,0,2,6$ respectively and never exceeds $2k$; for $k\ge4$, $2b_k\le6\le2k$. All coefficients are nonnegative even integers, proving the envelope and parity.

### Exact strong arithmetic source

Write $d^a_1(n)=a(n+1)-a(n)$. For even n, $a(n+1)=n$ and $a(n)\le6$, so $d^a_1(n)\ge n-6$. For odd n, $a(n)=n-1$ and $a(n+1)\le6$, hence $d^a_1(n)\le7-n$. Thus

$$
\boxed{
(-1)^n d^a_1(n)\ge n-7.
}
\tag{8}
$$

For $n=N+s$ on $X\le N<2X$ this is at least $X-7\ge X/2$ when $X\ge32$. Both parity classes have at least $X/3$ members on the full block and on the source-truncated block $X\le N\le2X-2$ for $X\ge32$. Consequently the source signed sums have magnitude at least $X^2/6$, and source energy at least $X^3/12$. These are **strictly stronger** than all the corresponding bounds in (6). No totient-specific Möbius identity is ascribed to a.

### Why every Cook phase remains near one

Because the complete binary sum of a is the integer one, for every N≥0 and h≥1 the **infinite** shifted-difference tail

$$
S^a_{h,N}=\sum_{j=1}^\infty
\frac{a(N+h+j)-a(N+j)}{2^j}
\tag{9}
$$

is an integer: each shifted single-series tail equals a power of two times the complete integer sum, minus a finite integer prefix.

Now use the envelope $0\le a(n)\le n$ to obtain

$$
\left|
S^a_{h,N}-\frac{D^a_{h,N,L}}{2^L}
\right|
\le\sum_{j>L}\frac{N+h+j}{2^j}
=\frac{N+h+L+2}{2^L}.
\tag{10}
$$

At a Cook-admissible depth and $N<2X$, the right-hand side is **strictly smaller than $1/16$**. Since $S^a_{h,N}$ is integral,

$$
\mathrm{Re}\,E^a_{h,N,L}
=\cos\!\left(2\pi\left[\frac{D^a_{h,N,L}}{2^L}-S^a_{h,N}\right]\right)
>\cos(\pi/8)>\frac9{10}.
$$

Finally, every sequence of integer coefficients, including a, obeys the *full* k-step Cook recurrence modulo $Q=2^L$:

$$
\boxed{
E^a_{N+k}\,\overline{E^a_N}^{\,2^k}
=\exp\left(
\frac{2\pi i}{Q}
\sum_{i=0}^{k-1}2^{k-1-i}d^a_h(N+L+1+i)
\right)
}
\tag{11}
$$

whenever both phases are defined. Equation (11), the h=1 fixed-prime source biases, parity, and the envelope therefore **cannot together force ten-percent cancellation**. This is a rigorous restriction on a proof strategy, not a counterexample to the real totient or its irrationality.

## 3. Theorem B: genuine two-prime arithmetic difference for the actual totient

The countermodel concentrates essentially all its large values on odd integers. The **actual** totient has further, independent structure from odd primes. We now prove a specific new conditional invariant for the actual source using the simultaneous primes 2 and 3.

Fix shift h=1, positive X and L, $s=L+1$, $Q=2^L$, and let

$$
E_X^*=3+\mathrm{bitlength}(3X).
$$

We require

$$
\boxed{
X\ge1024E_X^*,\qquad
8(s+1)\le X,\qquad
Q\ge64X,\qquad
Q\ge16(2X+L+3).
}
\tag{12}
$$

For $j\in\{0,2\}$ define the complete and recurrence-ready terminal-index subsets

$$
\begin{aligned}
I_j&=\{X\le N<2X:N+s\equiv j\pmod6\},\\
S_j&=\{X\le N\le2X-2:N+s\equiv j\pmod6\}.
\end{aligned}
\tag{13}
$$

Let $d(n)=\varphi(n+1)-\varphi(n)$ and let E_N be **Cook's original actual full phase** for h=1.

**Theorem B (actual two-prime arithmetic and modulo-one cocycle contrast).** Under (12),

$$
\boxed{
\begin{aligned}
\Delta_{\rm full}
&=\sum_{N\in I_0}d(N+s)-\sum_{N\in I_2}d(N+s)
\ge\frac{X^2}{32},\\
\Delta_{\rm source}
&=\sum_{N\in S_0}d(N+s)-\sum_{N\in S_2}d(N+s)
\ge\frac{X^2}{64}.
\end{aligned}}
\tag{14}
$$

And the **genuine modulo-one imaginary Cook cocycle contrast** satisfies

$$
\boxed{
\begin{aligned}
U_{X,L}
&=\mathrm{Im}
\left[
 \sum_{N\in S_0} E_{N+1}\overline{E_N}^{\,2}
-\sum_{N\in S_2} E_{N+1}\overline{E_N}^{\,2}
\right]\\
&\ge\frac{\pi X^2}{64Q}>0.
\end{aligned}}
\tag{15}
$$

The theorem is valid for $L=L_1(X)+1$, one greater than Cook's **least** admissible depth, at every sufficiently large X. For this legal depth $Q<256X$, and consequently

$$
\boxed{U_{X,L}\ge\frac{\pi X}{16384}.}
\tag{16}
$$

Unlike WP09-F, this is a **two-prime conditional Fourier signature** that the even-valued rational comparator in Theorem A does not reproduce. It still does **not** bound the complete real Cook first harmonic by $0.9X$; an imaginary contrast between selected cocycle sums is not that statement.

## 4. Proof of the actual two-prime arithmetic contrast

First prove an actual-totient arithmetic progression lemma for the **composite modulus six**; it is not an independence heuristic.

For any $k\in[0,s+1]$, any $r\bmod6$, put $f(n)=\varphi(n)/n$,

$$
W=\sum_{N=X}^{2X-1}(N+s),\quad
g_6(u)=\left(1-\frac12\mathbf1_{\{2\mid u\}}\right)
       \left(1-\frac13\mathbf1_{\{3\mid u\}}\right),
\quad
\mu_6=\prod_{\substack{q\ {\rm prime}\\q\nmid6}}(1-q^{-2}).
\tag{17}
$$

The exact conditional first moment is

$$
\boxed{
\left|
\sum_{\substack{X\le N<2X\\N\equiv r\pmod6}}
(N+s)f(N+k)
-\frac W6\,\mu_6\,g_6(r+k)
\right|\le5XE_X^*.
}
\tag{18}
$$

**Proof of (18).** Expand the true ratio via
$f(n)=\sum_{d\mid n}\mu(d)/d$.
Only squarefree d contribute. Split $d=d_0d_1$, with $d_0\mid6$ and $\gcd(d_1,6)=1$; this is an exact unique decomposition for squarefree d. The simultaneous congruences $N\equiv r\pmod6$ and $d\mid N+k$ are possible precisely when $d_0\mid r+k$. They then select **one** residue class modulo $6d_1$.

For a single residue progression in $[X,2X)$, prefix counting has discrepancy of at most one. Partial summation against the increasing weight $N+s$ shows its weighted sum differs from its density $W/(6d_1)$ by at most $4X$. Summing these errors with coefficients $|\mu(d)|/d$ for $d\le M=2X+s+1\le3X$ costs at most $4X(1+\log M)$. Completing the absolutely convergent main series beyond M costs at most $W\sum_{d>M}d^{-2}\le X$. Since $E_X^*>1+\log(3X)$, the total is bounded by $5XE_X^*$.

The Euler factors of the complete main sum are **exact**:

$$
\frac W6
\prod_{q\nmid6}(1-q^{-2})
\prod_{\substack{q\mid6\\q\mid r+k}}(1-q^{-1}),
$$

which is precisely $W\mu_6g_6(r+k)/6$. Thus (18) follows.

The elementary product inequality and a sum over ALL integers n≥5 give

$$
\mu_6\ge1-\sum_{n\ge5}n^{-2}
\ge1-\frac1{25}-\frac15
=\frac{19}{25}>\frac34.
\tag{19}
$$

For the terminal indices $N+s\equiv0\bmod6$, the exact local ratio difference is

$$
g_6(1)-g_6(0)=1-\frac13=\frac23.
$$

For $N+s\equiv2\bmod6$, it is

$$
g_6(3)-g_6(2)=\frac23-\frac12=\frac16.
$$

Thus their difference is exactly $1/2$. Apply (18) for the two shifts k=s and k=s+1, and use the identity

$$
d(N+s)=(N+s)[f(N+s+1)-f(N+s)]+f(N+s+1).
$$

Each arithmetic progression's difference has error at most $10XE_X^*$ plus a remainder bounded by X (because $0\le f\le1$). Taking the **difference of the two residue classes**, we get

$$
\boxed{
\Delta_{\rm full}
=\frac{\mu_6 W}{12}
+R_X,\qquad
|R_X|\le20XE_X^*+2X.
}
\tag{20}
$$

Since $W\ge X^2$, $\mu_6>3/4$, and $X\ge1024E_X^*$,

$$
\frac{\mu_6W}{12}\ge\frac{X^2}{16},\qquad
20XE_X^*+2X\le22XE_X^*
\le\frac{22}{1024}X^2<\frac{X^2}{32}.
$$

Therefore $\Delta_{\rm full}\ge X^2/32$. Each terminal-index set loses at most one index when truncated from $I_j$ to $S_j$. Since the two residue classes are disjoint, at most two contributions can be removed; each $|d(N+s)|\le3X$. Hence

$$
\Delta_{\rm source}\ge\frac{X^2}{32}-6X
\ge\frac{X^2}{64}
$$

as $X\ge1024E_X^*\ge384$. This proves (14).

## 5. Proof of the actual modulo-one Fourier contrast

The full exact Cook recurrence at h=1 is

$$
E_{N+1}\overline{E_N}^{\,2}
=\exp(2\pi i d(N+L+1)/Q)
=\exp(2\pi i d(N+s)/Q).
\tag{21}
$$

Therefore the imaginary contrast in (15) is **exactly**

$$
U_{X,L}=\sum_{N\in S_0}\sin(2\pi d(N+s)/Q)
-\sum_{N\in S_2}\sin(2\pi d(N+s)/Q).
\tag{22}
$$

For every real t the elementary Taylor remainder satisfies

$$
|\sin t-t|\le |t|^3/6.
$$

Hypothesis $8(s+1)\le X$ gives the elementary uniform bound

$$
|d(N+s)|\le N+s+1\le17X/8
\quad(N\in S_0\cup S_2).
$$

There are at most $X/3+2\le3X/8$ such indices. Hence, without any probabilistic or cancellation assumption,

$$
\boxed{
\left|U_{X,L}
-\frac{2\pi}{Q}\Delta_{\rm source}\right|
\le \frac{1}{6}\left(\frac{2\pi}{Q}\right)^3
  \frac{3X}{8}\left(\frac{17X}{8}\right)^3
<\frac{5\pi^3X^4}{Q^3}.
}
\tag{23}
$$

Substitute $\Delta_{\rm source}\ge X^2/64$:

$$
U_{X,L}\ge\frac{\pi X^2}{32Q}
-\frac{5\pi^3X^4}{Q^3}.
$$

Since $Q\ge64X$ and $\pi^2<10$, the error is **less than half** the positive main term: its ratio to that main term is at most

$$
160\pi^2\frac{X^2}{Q^2}
\le\frac{1600}{4096}<\frac12.
$$

Thus $U_{X,L}\ge\pi X^2/(64Q)$, proving (15).

For each fixed h=1, Cook's least depth $L_1(X)=O(\log X)$ grows, so $L=L_1(X)+1$ eventually meets all conditions in (12), and the increment gives $Q>64X$. Minimality gives $2^{L_1(X)}<32(2X+L_1(X)+2)$; doubling once shows
$Q<128X+64(L_1(X)+2)<256X$
for sufficiently large X. Equation (16) follows. QED.

## 6. The same second-prime witness *rejects* the rational parity comparator

For every sufficiently large even n, the comparator from (4) has

$$
a(n)=
\begin{cases}
2,&n\equiv0\pmod6,\\
6,&n\equiv2\pmod6,\\
0,&n\equiv4\pmod6.
\end{cases}
$$

Since $a(n+1)=n$ for even n, its h=1 source is

$$
d_1^a(n)=
\begin{cases}
n-2,&n\equiv0\pmod6,\\
n-6,&n\equiv2\pmod6.
\end{cases}
\tag{24}
$$

Pair successive indices $n=6k$ and $n+2=6k+2$ inside the same interval of terminal arguments. In each complete pair the arithmetic difference is **exactly two**:
$(n-2)-[(n+2)-6]=2$.
There can be at most one unpaired entry at each end; the terms there are bounded by $3X$. Hence, for $X\ge32$,

$$
\boxed{
\left|
\sum_{N\in I_0}d_1^a(N+s)
-\sum_{N\in I_2}d_1^a(N+s)
\right|\le8X.
}
\tag{25}
$$

The corresponding comparator **imaginary cocycle contrast** is bounded absolutely by **three**, uniformly for $Q\ge64X$:

$$
\boxed{|U_{X,L}^a|<3.}
\tag{26}
$$

Indeed, each complete pair has sources differing by only two, so the sine Lipschitz inequality bounds their difference by $4\pi/Q$; at most two unpaired sine terms contribute a total of two. With no more than $X/6+1$ pairs, the total is at most

$$
2+\frac{4\pi}{Q}\left(\frac X6+1\right)<3
$$

for $X\ge32$, $Q\ge64X$.

In contrast, the **actual totient** has $U_{X,L}\ge\pi X^2/(64Q)$, which is $\Omega(X)$ for $L=L_1(X)+1$.

This is a **precise new point of discrimination**: the single-prime signed bias, all-step cocycle and Euler-totient-style coefficient parity admit a rational false model, but the added **odd-prime conditional imaginary Fourier contrast** distinguishes it quantitatively. The distinction still does not establish how often original phase arguments fall far enough from integers to yield Cook's required global ten-percent saving.

## 7. Evidence, computation and the remaining theorem gap

The exact rational identity (5), all-coefficient parity/envelope, strong WP09-F style source bounds, modular Cook recurrence, and centered-tail obstruction are independently checked by the bounded source verifier [two_prime_phase_discriminator.py](two_prime_phase_discriminator.py). The actual totient composite-modulus arithmetic contrast is checked as an **integer inequality**, and the full Cook numerator is reconstructed by the WP09-E exact rolling algorithm. Sine evaluations on finite blocks are **diagnostic only**. The all-X inequality (15) is established by the analytic proof, not by float samples.

For the actual Euler totient at $X=32768$, $h=1$, and legal depth $L=L_1(X)+1=22$, an independent bounded source calculation gave:

- True exact source two-prime difference $\Delta_{\rm full}=122446838$, compared with $X^2/32=33554432$.
- Actual imaginary cocycle contrast $U_{X,L}\approx183.3423$, versus its proved lower bound $\pi X^2/(64Q)=4\pi\approx12.5664$.
- Rational parity comparator full-source contrast $-21864=O(X)$; imaginary cocycle contrast $\approx0.0653$, consistent with its uniform bound of three.
- At the legal *least* Cook depth $L_1(4096)=18$, the comparator full real phase average is approximately 0.998745, whereas the actual totient's is approximately 0.0050011. These are finite observations only, **not** proofs of an asymptotic real harmonic bound.

**Research disposition:** Theorem A is a genuine obstruction to amplification from only the existing single-prime inputs. Theorem B is a bounded positive new **two-prime** actual-totient modulo-one phase signal, cofinal in X. Neither settles Cook's weighted prime/cofactor bound nor the required **real** ten-percent full harmonic. No MATHCERT, theorem-priority claim, Lean proof or independent external certification.

**Next substantive obligation:** transfer simultaneous two-prime and higher-prime conditional source information to the **distribution of the original Cook phases**; controlling only the imaginary one-step cocycle is still insufficient. A serious next candidate is a multi-prime, multi-time *weighted* characteristic or large-sieve estimate for Cook's actual overlapping totient windows; it must quantify cancellation of the cofactor-dependent weights, rather than assume them independent.

Same-agent separate logical hostile review: [WP09_G_CRITICAL_REVIEW.md](WP09_G_CRITICAL_REVIEW.md). Test coverage appends to the existing policy-routed [tests/test_erdos249_full_series_phase.py](../../tests/test_erdos249_full_series_phase.py). Original Erdős #249 and research issue #3500 remain **OPEN**, MATHCERT NOT_SUBMITTED.
