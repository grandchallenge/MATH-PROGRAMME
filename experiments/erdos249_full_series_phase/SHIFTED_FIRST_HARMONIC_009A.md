# Erdős #249 — WP09-A: signed shifted-totient contrast and a first-harmonic saving

**Scientific issue:** [MATH-PROGRAMME #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500).  
**Source lock:** Will Cook, *The Binary Totient Series* (2026, revised October 2026), [exact source](https://github.com/wcook04/plectis-erdos/blob/main/paper/249/erdos-249-binary-totient-series.tex), section *An exponential-sum question*.  
**State:** BOUNDED MATHEMATICAL RESULT; NOT A PROOF OF IRRATIONALITY. Original Erdős #249 OPEN; MATHCERT NOT_SUBMITTED.

## 1. Target: Cook's actual first harmonic, not a surrogate

Let $h\ge1$ be fixed, and let $\varphi$ be the actual Euler totient. Cook defines

$$
D_{h,N,L}=\sum_{j=1}^L2^{L-j}
\bigl(\varphi(N+h+j)-\varphi(N+j)\bigr),
\qquad E_{h,N,L}=\exp(2\pi iD_{h,N,L}/2^L).
$$

His sufficient target, for every fixed $h$ on arbitrarily large blocks at a common admissible depth, is

$$
\mathrm{Re}\sum_{N=X}^{2X-1}E_{h,N,L}\le\frac9{10}X,
\qquad 2^L\ge16(2X+h+L+2).
\tag{C}
$$

Cook's source-locked four-term decomposition isolates a *weighted first-harmonic correlation* still unproved at the required $14X/25$ scale; unweighted prime-cofactor means do not control it. This WP establishes a genuinely unconditional **strict but small** saving for the **whole actual harmonic** at the admissible depth. It does NOT establish the required $10\%$ saving, the difficult weighted correlation, or the original irrationality.

The arithmetic input is a quantitative variant of shifted-totient sign contrasts. Such order phenomena have antecedents in G. Martin (2006), cited by Cook. **No novelty or priority claim** is made for the general strategy, CRT, or the classical mean of $\varphi(n)/n$.

## 2. A fixed arithmetic progression that forces large contrasts of both signs

Fix any integer $h\ge1$. Choose a squarefree integer $M=M_h\ge2$, relatively prime to $h$, such that

$$
\eta_M=\prod_{p\mid M}(1-1/p)\le\frac{29}{50}.
\tag{1}
$$

Such $M$ exists for every fixed $h$: take an increasing finite product of primes not dividing $h$. The classical divergence of $\sum_p1/p$ implies the product of their factors $(1-1/p)$ tends to zero. No prime number theorem or independence assumption is needed.

Set $\tau=3/5$ and

$$
C_M=\prod_{p\nmid M}(1-1/p^2)
=\frac{6/\pi^2}{\prod_{p\mid M}(1-1/p^2)}
\ge\frac6{\pi^2}>\tau.
\tag{2}
$$

**Lemma A (conditional totient mean, with proof).** For every residue $a$ coprime to $M$ and every consecutive integer interval $I$ of length $X+O(1)$ contained in $[X/2,4X]$, with $M$ fixed,

$$
\sum_{\substack{n\in I\\n\equiv a\pmod M}}
\frac{\varphi(n)}n
=\frac{C_M}{M}X+O_M(\log X).
\tag{3}
$$

**Proof.** Use the exact divisor identity

$$
\frac{\varphi(n)}n=\sum_{d\mid n}\frac{\mu(d)}d.
$$

If $n\equiv a\pmod M$ with $(a,M)=1$, then only $d$ coprime to $M$ may divide $n$. For such $d$, the CRT identifies a unique residue class modulo $Md$ satisfying $n\equiv a\pmod M$ and $d\mid n$, containing $X/(Md)+O(1)$ integers in $I$. Interchange the finite sums. The main term is $(X/M)\sum_{(d,M)=1}\mu(d)/d^2=(X/M)C_M$; the sum of weighted $O(1)$ errors is $O(\sum_{d\le4X}1/d)=O(\log X)$, and the omitted absolutely convergent main tail contributes $O_M(1)$. QED.

**Lemma B (positive-density signed contrasts).** Define

$$
\kappa=\frac{6/\pi^2-3/5}{2/5}=\frac{15}{\pi^2}-\frac32>0.
$$

For any interval $I_X=[X+L+1,2X+L-1]$ with $L=O(\log X)$ and fixed $M,h$, there are at least

$$
\frac{\kappa X}{M}-O_{M,h}(\log X)
\tag{4}
$$

indices in **each** of the two disjoint sets

$$
\begin{aligned}
\mathcal N_-&=\{n\in I_X:n\equiv-h\pmod M,\quad\varphi(n)/n\ge3/5\},\\
\mathcal N_+&=\{n\in I_X:n\equiv0\pmod M,\quad\varphi(n+h)/(n+h)\ge3/5\}.
\end{aligned}
\tag{5}
$$

For sufficiently large $X$ (in particular $X\ge58h$), they satisfy, respectively,

$$
\boxed{
\varphi(n+h)-\varphi(n)\le-\frac X{100}
\quad(n\in\mathcal N_-),\qquad
\varphi(n+h)-\varphi(n)\ge\frac X{50}
\quad(n\in\mathcal N_+).
}
\tag{6}
$$

**Proof.** In the first class, $(n,M)=1$ because $(h,M)=1$; apply Lemma A. If $B=X/M+O(1)$ integers lie in the class and $g$ have ratio $\ge\tau$, the total ratio is at most $\tau B+(1-\tau)g$. Since the actual mean is $C_MX/M+O_M(\log X)$, this forces $g\ge[(C_M-\tau)/(1-\tau)]X/M-O_M(\log X)$, which is at least (4). For the second class apply Lemma A to $n+h\equiv h\pmod M$ in the shifted interval, preserving its length. The classes are disjoint because $M\nmid h$.

For $n\in\mathcal N_-$, $M\mid(n+h)$ and the exact Euler product gives $\varphi(n+h)\le\eta_M(n+h)$; whereas $\varphi(n)\ge\tau n$. Thus the difference is at most

$$
-(\tau-\eta_M)n+\eta_M h
\le-\frac n{50}+\frac{29h}{50}\le-\frac X{100}
$$

when $n\ge X\ge58h$. For $n\in\mathcal N_+$, the analogous inequalities give $\varphi(n)\le\eta_Mn$ and $\varphi(n+h)\ge\tau(n+h)$, so the difference is at least $n/50\ge X/50$. QED.

The two signs are not a heuristic fluctuation: each is forced on a positive, explicit proportion depending on $M$ of every sufficiently large dyadic interval. The modulus may be large when $h$ contains many small prime factors; no uniform lower bound independent of $h$ is claimed.

## 3. Exact sliding recurrence for Cook's shifted phase

Let $Q=2^L$, and set $d_h(n)=\varphi(n+h)-\varphi(n)$. Direct index shifting gives

$$
D_{h,N+1,L}=2D_{h,N,L}-Qd_h(N+1)+d_h(N+L+1).
$$

Writing $r_N=\mathrm{cen}_Q(D_{h,N,L})$ for the centered integer residue, we obtain the **exact** modular recurrence

$$
\boxed{r_{N+1}-2r_N\equiv d_h(N+L+1)\pmod Q.}
\tag{7}
$$

Assume the depth is *Cook admissible*,

$$
Q\ge16(2X+h+L+2)>32X.
\tag{8}
$$

For every large $X$ also satisfying $h+L+1\le X$, the coefficient difference at any $n\in I_X$ has magnitude less than $n+h<3X$. When $|d_h(n)|\ge X/100$, it is **impossible** for both neighboring centered residues to have magnitude $<X/300$: otherwise $z=r_{N+1}-2r_N$ has $|z|<X/100$, so $z-d_h(n)$ is a nonzero multiple of $Q$ of absolute value less than $X/100+3X<Q$. Thus

$$
\boxed{\max(|r_N|,|r_{N+1}|)\ge X/300}
\tag{9}
$$

for every signed-contrast endpoint $n=N+L+1$ from Lemma B.

Each starting index belongs to at most two adjacent pairs, and the two sets of contrast endpoints are disjoint. Equations (4)–(9) therefore prove the **quantitative first-harmonic nonconcentration**

$$
\boxed{
\#\left\{N\in[X,2X):
\mathrm{dist}(D_{h,N,L}/Q,\mathbb Z)\ge\frac{X}{300Q}
\right\}
\ge\frac{\kappa X}{M}-O_{M,h}(\log X).
}
\tag{10}
$$

Unlike WP08-A/B, this is for Cook's **actual shifted difference** $D_{h,N,L}$, not for the unshifted totient tail or its comparison with a rational approximation.

## 4. Theorem C — an unconditional strict first-harmonic saving

For each fixed $h$, take $L=L_h(X)$ to be the **least** integer satisfying (8). For all sufficiently large $X$, this $L$ is at least $h+26$, is $O_h(\log X)$, and satisfies $h+L+1\le X$. Minimality gives

$$
Q=2^L<32(2X+h+L+1)\le96X.
\tag{11}
$$

Consequently the lower bound in (10) yields a **fixed fractional distance**, at least $1/28800$, for at least $\kappa X/(2M)$ starts once $X$ is sufficiently large. Let

$$
c_h=
\frac{\kappa}{2M_h}
\left(1-\cos\left(\frac{2\pi}{28800}\right)\right)>0.
\tag{12}
$$

**Theorem C (strict but quantitatively insufficient Cook-harmonic saving).** For **every fixed integer $h\ge1$**, every sufficiently large integer $X$ and its least Cook-admissible depth $L=L_h(X)$,

$$
\boxed{
\mathrm{Re}\sum_{N=X}^{2X-1}
\exp\left(\frac{2\pi iD_{h,N,L}}{2^L}\right)
\le(1-c_h)X.
}
\tag{13}
$$

**Proof.** For each of the at least $\kappa X/(2M)$ exceptional starting positions, the fractional distance of $D/Q$ to the nearest integer is at least $1/28800$. Hence the real part of its unit phase is at most $\cos(2\pi/28800)$. For every other position it is at most one. Sum the two upper bounds and substitute (12). QED.

The theorem gives a rigorously proved **positive cancellation deficit** at the exact object, scale, and quantifier order of Cook's first-harmonic route. It uses only CRT, Euler's product, the elementary conditional totient mean, and the exact phase recurrence. No prime number theorem, independence model, or conjectural correlation estimate is needed.

But the saving is far below Cook's required $1/10$; at the universal parameter choice of (1), its explicit lower estimate is of order $10^{-10}/M_h$, not $10^{-1}$. Taking the depth larger does **not** bridge the gap by itself: the phase separation forced by (9) scales as $X/Q$, while Cook's discarded-tail error scales as $X/Q$. The ratio of these two scales is independent of depth.

## 5. Theorem D — an exact multiplicative cocycle across arbitrary shifts

A further exact identity gives the right form of the *next* correlation problem. For any integer coefficient sequence $a(n)$, define $D^a_{h,N,L}$ using the same shifted binary-window formula. Then for any fixed positive shifts $h,k$ and **the same depth** $L$,

$$
\boxed{
D^a_{h+k,N,L}=D^a_{h,N,L}+D^a_{k,N+h,L}.
}
\tag{14}
$$

**Proof.** Term by term in the finite sum, write

$$
a(N+h+k+j)-a(N+j)
=
[a(N+h+k+j)-a(N+h+j)]
+[a(N+h+j)-a(N+j)].
$$

Multiply by $2^{L-j}$ and sum over $1\le j\le L$. QED.

For the exact unit phases this yields the **multiplicative cocycle identity**

$$
\boxed{
E^a_{h+k,N,L}=E^a_{h,N,L}E^a_{k,N+h,L},
\qquad
E^a_{h,N,L}=\prod_{r=0}^{h-1}E^a_{1,N+r,L}.
}
\tag{15}
$$

This is not an independence or mixing assertion. It states that Cook's all-shift target is precisely a family of *higher-order consecutive correlations* of the same first-shift phase process, rather than $h$ unrelated frequency tests.

**Hostile elementary correlation counterexample.** Take the abstract unit-phase sequence $u_N=i(-1)^N$. Its one-point mean is exactly zero on every even-length interval, yet $u_Nu_{N+1}=1$ at every position. Thus even perfect first-harmonic cancellation for shift one is **not** sufficient, without a correlation estimate, to guarantee saving for shift two. This is a logical phase-sequence counterexample, **not** a claim that these $u_N$ equal the actual totient phases or satisfy their arithmetic recurrence.

The exact source test suite independently verifies both the integer cocycle and the unit-phase obstruction. A productive amplification must therefore establish actual-totient correlation or mixing of the products in (15), uniform across each **fixed** $h$ on sufficiently late blocks. The small one-point saving $c_1$ of Theorem C cannot simply be multiplied across $h$.

## 6. Hostile rational model and limit of the theorem

For a **fixed** shift $h$, choose an integer $M\ge3$ coprime to $h$ (so $-h,0,h$ are distinct modulo $M$) and define the integer sequence

$$
a_n=
\begin{cases}
n,&n\equiv-h\pmod M,\\
0,&n\equiv0\pmod M,\\
n,&n\equiv h\pmod M,\\
\lfloor n/2\rfloor,&\text{otherwise}.
\end{cases}
$$

Because $n\mapsto a_n$ is a *degree-one quasipolynomial* with period $M$, its entire binary series $\sum_{n\ge1}a_n2^{-n}$ is exactly rational (a finite sum of rational generating functions over residue classes).

Nevertheless $d_h(n)=a_{n+h}-a_n$ is at most $-n$ for $n\equiv-h\pmod M$ and at least $n+h$ for $n\equiv0\pmod M$; the same signed-contrast and local modular harmonic arguments apply. Thus **even qualitative positive-density signed differences and a strict harmonic saving for a particular $h$ are compatible with a rational full series**. A rational sequence has a (possibly different) period relevant to its denominator; our fixed chosen $h$ is not guaranteed to be that period. This hostile model does not refute the original totient-specific sufficient criterion, which demands a $10\%$ saving **for every hypothetical period $h$**.

The additional obstruction is quantitative: a bounded-coefficient, one-step residue recurrence cannot force a centered residue larger than the actual omitted-tail uncertainty $B\sim2X$ merely from a coefficient difference of magnitude at most $O(X)$. The $1/10$ saving remains a substantive arithmetic mixing problem. Cook's open **weighted first-harmonic** term has not been proved or replaced by this weak result.

## 7. Claim ledger and successor

| Claim | Status |
| --- | --- |
| A: conditional mean of $\varphi(n)/n$ on an invertible fixed progression, with $O_M(\log X)$ error | Elementary proof |
| B: every fixed $h$ has both positive-density $\Omega_h(X)$ and negative-density $\Omega_h(X)$ linear shifted-totient contrasts | Elementary CRT and totient mean proof; related earlier sign-contrast literature |
| B2: at the actual Cook-admissible depth, positive-density shifted finite phases are at a fixed distance from integers | Exact centered-residue recurrence proof |
| C: for each $h$ an explicit $c_h>0$ gives $\mathrm{Re}\sum E\le(1-c_h)X$ for all large blocks | Unconditional elementary proof, **far weaker** than Cook's needed $0.1X$ |
| D: exact shifted integer and unit-phase multiplicative cocycle for any coefficient sequence; harmonic for all $h$ is a consecutive correlation of shift-one phases | Elementary telescoping proof; no mixing asserted |
| Strong Cook weighted correlation / $0.9X$ whole harmonic / denominator-uniform complete-tail exclusion | **OPEN** |
| Original full binary totient-series irrationality, novelty, independent proof certification | **OPEN / NOT_CLAIMED / MATHCERT NOT_SUBMITTED** |

**Next substantive target:** Establish an arithmetic **amplification** of Cook's first-harmonic saving from the current tiny $c_h$ to a constant exceeding $0.1$, by controlling overlap of shifted totient values inside the residual weights $w_N$ **or** proving the actual-totient consecutive phase-product correlation in (15), rather than merely exhibiting large individual shifts. Any future amplification must survive the rational quasipolynomial comparator above and WP07-E exact near-log rational imitation.

The executable witness engine is [shifted_first_harmonic.py](shifted_first_harmonic.py) and the hostile tests extend the **existing governed** [test_erdos249_full_series_phase.py](../../tests/test_erdos249_full_series_phase.py); they do not change protected policy, routes or workflows. The finite experiments validate exact arithmetic identities and counts, not the infinite asymptotics. Qualified same-agent logical review is not independent authentication.

**Governance:** Bounded mathematical source review and protected admission only. Preserve issue #3500 as OPEN / Project #2 In Progress, original Erdős #249 OPEN, parent #3201 OPEN and MATHCERT NOT_SUBMITTED.
