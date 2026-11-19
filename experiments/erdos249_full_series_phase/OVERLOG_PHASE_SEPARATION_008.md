# Erdős #249 — WP08-A: positive-density over-logarithmic finite-tail phase separation

**Research workstream:** [MATH-PROGRAMME #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500)  
**Record:** ERDOS-249-S-WP08-A/1  
**Date:** 2026-11-18 (Pacific), November 19 UTC  
**Status:** noncertifying mathematics manuscript, exact hostile source tests; original Erdős #249 **OPEN**, MATHCERT **NOT_SUBMITTED**

## 1. Scientific question, provenance, and claim firewall

The protected WP07-A–E results showed that near-logarithmic finite-tail integrality and Fourier-phase information do not, by themselves, settle the irrationality of

$$
S=\sum_{n\ge1}\varphi(n)2^{-n}.
$$

WP07-E proved an exact rational interpolation theorem for **every** bounded target sequence at depths below $\lfloor\log_2 N\rfloor$ by a fixed deficit. A positive research target is to establish what genuinely follows for the *actual* totient at a depth **above** that threshold, where the ordinary infinite-tail estimate becomes numerically small.

Here we establish unconditional **positive-density finite-tail nonconcentration by a fixed fractional distance from the integers** at depth $L=\lfloor\log_2 X\rfloor+4$. We also establish a multiplicative totient-specific separation from the rational baseline $c_n=\lfloor n/2\rfloor$, an exact rigidity theorem for any pair of linearly bounded sequences, and two independent hostile *rational* examples that meet the same finite-phase conclusions. The positive theorem is stronger than a bare nonintegrality count but is **not the full irrationality proof**.

Relevant antecedents: Will Cook, *The Binary Totient Series* (2026, revised October 1), for the original full-tail residue and first-harmonic problem; GCL protected WP07-C/D for exact sliding recurrences; GCL WP07-E for the universal rational finite-phase mimic. The elementary mean identity for $\varphi(n)/n$ and the modular doubling recurrence are standard; **no mathematical novelty or priority is claimed without dedicated literature review**.

## 2. Exact finite-tail recurrence

Let $X$ be a positive integer tending to infinity, set

$$
k=\lfloor\log_2 X\rfloor,\qquad
L=k+4,\qquad Q=2^L.
$$

For $X\ge64$ we have

$$
8X<Q\le16X,\qquad L+1\le X.
\tag{1}
$$

For any integer-valued coefficient sequence $a_n$, set

$$
A^a_N=\sum_{j=1}^L2^{L-j}a_{N+j},
\qquad
U^a_N=A^a_N/Q.
$$

Let $\operatorname{cen}_Q(m)$ denote a centered representative of an integer $m$ modulo $Q$, chosen in the interval $[-Q/2,Q/2]$. The choice at the two tied endpoints does not affect absolute values, and

$$
\left\|U^a_N\right\|_{\mathbb R/\mathbb Z}
=\frac{|\operatorname{cen}_Q(A^a_N)|}{Q}.
$$

The exact integer recurrence is

$$
\boxed{
A^a_{N+1}=2A^a_N-Qa_{N+1}+a_{N+L+1}.
}
\tag{2}
$$

In particular, setting $r^a_N=\operatorname{cen}_Q(A^a_N)$,

$$
\boxed{r^a_{N+1}\equiv2r^a_N+a_{N+L+1}\pmod Q.}
\tag{3}
$$

The same recurrence holds for the difference of two coefficient sequences.

## 3. Theorem A — actual-totient nonconcentration beyond the logarithmic threshold

**Theorem A.** For the actual Euler totient $\varphi(n)$ and every sufficiently large integer $X$, define

$$
\mathcal H_X=
\left\{
N\in[X,2X)\cap\mathbb Z:
\left\|\sum_{j=1}^{L}\frac{\varphi(N+j)}{2^j}\right\|_{\mathbb R/\mathbb Z}
\ge\frac1{96}
\right\}.
$$

Then

$$
\boxed{
\#\mathcal H_X\ge
\left(\frac6{\pi^2}-\frac12\right)X-O(\log X).
}
\tag{A}
$$

The leading constant is strictly positive, approximately $0.1079$. In particular, **a positive proportion** of actual totient finite tails at over-logarithmic depth are separated by a **fixed nonvanishing amount** from every integer. This is not merely a nonzero dyadic residue whose separation shrinks as $X$ grows.

**Proof, Step 1: the mean totient ratio.** The standard divisor identity

$$
\frac{\varphi(n)}n=\sum_{d\mid n}\frac{\mu(d)}d
$$

and absolute convergence of $\sum_{d\ge1}\mu(d)d^{-2}=1/\zeta(2)=6/\pi^2$ give the completely elementary summatory estimate

$$
\begin{aligned}
\sum_{n\le Y}\frac{\varphi(n)}n
&=\sum_{d\le Y}\frac{\mu(d)}d\left\lfloor\frac Yd\right\rfloor\\
&=\frac6{\pi^2}Y+O(\log Y).
\end{aligned}
\tag{4}
$$

Consider the $X-1$ consecutive integers

$$
I_X=[X+L+1,\,2X+L-1]\cap\mathbb Z.
$$

By subtracting (4) at the two endpoints and using $L=O(\log X)$, we obtain

$$
\sum_{n\in I_X}\frac{\varphi(n)}n
=\frac6{\pi^2}X+O(\log X).
\tag{5}
$$

Let $G_X=\{n\in I_X:\varphi(n)\ge n/2\}$, and write $g_X=\#G_X$. Since every totient ratio is at most one, while ratios outside $G_X$ are strictly less than $1/2$,

$$
\frac6{\pi^2}X+O(\log X)
\le g_X+\frac12(X-1-g_X).
$$

Consequently,

$$
\boxed{g_X\ge\left(\frac{12}{\pi^2}-1\right)X-O(\log X).}
\tag{6}
$$

**Step 2: no two neighboring centered residues can both be small.** Take any $n\in G_X$ and set $N=n-L-1$, so $X\le N\le2X-2$ and $N+1\in[X,2X)$. Because $\varphi(n)\ge n/2\ge X/2$ and $\varphi(n)\le n<3X$, the congruence (3) reads

$$
r^\varphi_{N+1}-2r^\varphi_N\equiv\varphi(n)\pmod Q.
$$

Suppose both $|r^\varphi_N|<X/6$ and $|r^\varphi_{N+1}|<X/6$. Their linear combination $z=r^\varphi_{N+1}-2r^\varphi_N$ has $|z|<X/2$. Thus

$$
0<\varphi(n)-z<3X+X/2<Q,
$$

yet $\varphi(n)-z$ is a multiple of $Q$, a contradiction. Hence at least one of the two adjacent starts satisfies

$$
\boxed{\max(|r^\varphi_N|,|r^\varphi_{N+1}|)\ge X/6.}
\tag{7}
$$

By (1), for that start the fractional distance is at least $X/(6Q)\ge1/96$.

**Step 3: count qualifying starts.** Each start belongs to at most two of the adjacent pairs produced by the $g_X$ good integers $n$, so at least $g_X/2$ **distinct** starts satisfy (7). Inserting (6) proves (A). QED.

**Source boundary.** This theorem depends only on the classical mean of $\varphi(n)/n$, its bound $0\le\varphi(n)\le n$, and the exact recurrence. It does not use prime-factor independence, conjectural distribution of totients, or a numerical Fourier probe.

## 4. Theorem B — a separate totient-specific modular separation

The first theorem only needs a mean coefficient ratio above $1/2$ and so is not uniquely characteristic of Euler's totient. We can also exploit an exact consequence of its multiplicative prime-factor formula: if $6\mid n$, then

$$
\varphi(n)\le n(1-1/2)(1-1/3)=n/3.
$$

Let $c_n=\lfloor n/2\rfloor$, and define the centered numerator for the **difference** of the two complete finite tails,

$$
s_N=\operatorname{cen}_Q(A^\varphi_N-A^c_N).
$$

**Theorem B.** At the same $L=k+4$ and every integer $X\ge64$,

$$
\boxed{
\#\left\{N\in[X,2X):
\|U^\varphi_N-U^c_N\|_{\mathbb R/\mathbb Z}\ge\frac1{288}\right\}
\ge\frac X6-O(1).
}
\tag{B}
$$

**Proof.** Put $\delta_n=\varphi(n)-c_n$. For every multiple of six, $\delta_n\le-n/6<0$ and $|\delta_n|\le n/2<3X/2$ for $n\in I_X$. The difference recurrence gives

$$
s_{N+1}-2s_N\equiv\delta_{N+L+1}\pmod Q.
$$

If $n=N+L+1\in I_X$ is divisible by six and both $|s_N|<X/18$ and $|s_{N+1}|<X/18$, then $|s_{N+1}-2s_N|<X/6$, while $\delta_n\le-X/6$ and $|\delta_n|<3X/2$. Their difference is a nonzero integer with absolute value less than $2X<Q$, contradicting the congruence. Hence one of the two neighboring starts has $|s|\ge X/18$, giving fractional separation at least $X/(18Q)\ge1/288$.

The relevant multiples of six have density one-sixth in $I_X$ and are spaced six apart; their adjacent two-start pairs are disjoint. Thus they produce $X/6-O(1)$ **distinct** starts. QED.

## 5. Theorem C — exact over-logarithmic phase rigidity

**Theorem C (rigidity for linearly bounded coefficient sequences).** Let $(a_n)$ and $(t_n)$ be integer sequences with $0\le a_n,t_n\le n$. Fix $X\ge64$ and $L=\lfloor\log_2X\rfloor+4$. If their **whole finite tails have identical fractional parts at both** $N$ and $N+1$, where $X\le N\le2X-2$, then

$$
\boxed{a_{N+L+1}=t_{N+L+1}.}
\tag{C}
$$

Consequently, if the phases agree at **every** start in $[X,2X)$, the two sequences coincide at all indices in $I_X$.

**Proof.** Let $\Delta_N=A^a_N-A^t_N$. Fractional equality is exactly $Q\mid\Delta_N$ and $Q\mid\Delta_{N+1}$. Subtracting their recurrence gives

$$
a_{N+L+1}-t_{N+L+1}\equiv0\pmod Q.
$$

But the absolute difference is at most $N+L+1<3X<Q$, so it must be zero. QED.

**Interpretation:** WP07-E's universal rational phase interpolation works at a fixed deficit *below* logarithmic depth. Theorem C demonstrates an explicit rigidity barrier *above* logarithmic depth under the same linear coefficient envelope. For arbitrary targets with genuinely different coefficients, universal all-position matching cannot persist through this deeper scale without abandoning the envelope. This is a structural threshold theorem, **not** irrationality of the target binary series.

## 6. Hostile rational controls — the conclusions are not irrationality criteria

**Control R1: positive-density direct separation with rational full sum.** Let

$$
u_n=\lfloor3n/4\rfloor,\qquad
\sum_{n\ge1}\frac{u_n}{2^n}=\frac{14}{15}.
$$

The infinite identity follows by writing $u_n=(3n-r_n)/4$ where $r_n=3n\bmod4$ has period four $(3,2,1,0)$. Indeed $\sum n2^{-n}=2$ and

$$
\sum_{n\ge1}r_n2^{-n}
=\frac{3/2+2/4+1/8}{1-2^{-4}}=\frac{34}{15}.
$$

The average of $u_n/n$ tends to $3/4>1/2$, and $0\le u_n\le n$. Thus the **same** recurrence-and-mean proof as Theorem A gives a positive-density fixed fractional gap from integers at the same over-log depth, despite the full series being rational $14/15$.

**Control R2: the multiple-of-six separation also occurs for a rational series.** Define

$$
v_n=
\begin{cases}
\lfloor n/2\rfloor-n/6,&6\mid n,\\
\lfloor n/2\rfloor,&6\nmid n.
\end{cases}
$$

It is an integer sequence with $0\le v_n\le n$. Its complete binary sum is

$$
\sum_{n\ge1}\frac{v_n}{2^n}
=\frac23-\sum_{m\ge1}\frac m{2^{6m}}
=\frac23-\frac{64}{3969}
=\boxed{\frac{2582}{3969}}.
$$

For every multiple of six, $v_n-\lfloor n/2\rfloor=-n/6$, so the **entire** elementary proof of Theorem B remains valid for this rational comparison sequence. This demonstrates that even a highly visible arithmetic-progression inequality does not suffice to prove the original irrationality statement.

Neither R1 nor R2 asserts equality with Euler's totient coefficients. They are adversarial controls for unsupported inference, not approximations to the unknown full value.

## 7. Why these proven bounds still do not settle Erdős #249

The exact positive omitted tail obeys

$$
0<
\sum_{j>L}\frac{\varphi(N+j)}{2^j}
<
\frac{N+L+2}{2^L}
=\frac{N+L+2}{Q}.
\tag{8}
$$

Theorem A proves a centered fractional distance at least $X/(6Q)$ for a positive proportion of starts, while (8) permits an omitted correction of size up to $(2X+L+2)/Q$. The proven lower bound is **too small** to prevent an integer crossing. Moreover a rationality contradiction requires handling an arbitrary hypothetical denominator, not just a comparison to integer zero; the signed one-sided residue requirements are more demanding.

Theorems A–C therefore establish **over-logarithmic finite arithmetic phase separation and rigidity**, but **not** a cofinal full-series residue gap. Controls R1 and R2 prove that their core generic mechanisms are compatible with rational infinite sums. An actual proof of irrationality must exploit arithmetic structure not present in these rational controls, or strengthen the residue-versus-remainder inequality beyond the present constants.

The successor mathematical target remains the problem-specific **totient multiplicative correlation needed for a denominator-uniform, one-sided, over-logarithmic finite residue gap**—the kind of unproved input already isolated by Cook's cofinal tests. No additional finite sweep alone can settle it.

## 8. Claim ledger and exact evidence

| Claim | Disposition |
| --- | --- |
| WP08-A-A: positive-density actual totient whole finite tails at over-log depth have fixed fractional distance at least $1/96$ | Complete elementary manuscript proof using classical totient mean |
| WP08-A-B: at least $X/6-O(1)$ full finite totient phases differ from the rational baseline by at least $1/288$ | Complete elementary proof using exact $6\mid n$ totient inequality |
| WP08-A-C: identical neighboring deep finite phases force equal last coefficient for linearly bounded sequences | Exact recurrence and magnitude rigidity |
| WP08-A-R1/R2: both separation phenomena can also occur with **rational complete binary sums** | Exact generating-function constructions |
| WP08-A-FULL: original full Euler-totient binary series irrational | **OPEN, NOT CLAIMED** |
| External novelty, independent theorem referee, Lean checking, MATHCERT | **NOT CLAIMED / NOT_SUBMITTED** |

The standard-library implementation is [overlog_phase_separation.py](overlog_phase_separation.py), with exact hostile tests appended to the existing governed [full-series test module](../../tests/test_erdos249_full_series_phase.py), without modifying routing or protected policy. The finite tests supplement, rather than substitute for, the full all-$X$ manuscript derivations.

**Continuity:** Record a bounded protected admission receipt in [#3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500) only after native merge queue admission, exact protected head / five-file blob readback and required merge-group checks. Keep issue #3500 **OPEN/In Progress**, parent #3201 and original Erdős #249 **OPEN**, MATHCERT **NOT_SUBMITTED**.
