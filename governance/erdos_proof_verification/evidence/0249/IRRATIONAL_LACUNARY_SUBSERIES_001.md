# Erdős #249: independently checked irrational lacunary subseries

**Work item:** [ERDOS-PV-0249-S01](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3205)  
**Disposition:** BOUNDED_MATHEMATICAL_LEMMA_PROVED; FULL_ERDOS_249_OPEN; LEAN_REPLAY_NOT_RUN; MATHCERT_NOT_SUBMITTED

## Exact claim

Let $\varphi$ denote Euler's totient function, and define

$$
T=\sum_{m=1}^{\infty}\frac{\varphi(2^m)}{2^{2^m}}.
$$

Then **$T$ is irrational**. This does **not** establish irrationality of the original Erdős #249 series

$$
S=\sum_{n=1}^{\infty}\frac{\varphi(n)}{2^n}.
$$

The source-catalogue lock is `teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89:data/problems.yaml`, entry 249 (Git blob `4e60263a80af6207aca494d2e1388e44fa372889`). The pinned statement provider is `google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020:FormalConjectures/ErdosProblems/249.lean`, blob `ed4650c870f58a7cbfbc9ec8c4bc4c35175b074a`. Its statement concerns the *full* $S$ and contains `answer(sorry)` and `by sorry`, not a completed proof. Original source discussion: Erdős–Graham (1980), p. 61; Erdős (1988), p. 102, DOI 10.1017/CBO9780511897184.009.

## Proof by dyadic rational separation

For every integer $m\geq1$, exactly half of the integers from 1 to $2^m$ are odd. Therefore,

$$
\varphi(2^m)=2^{m-1}.
$$

Set $e_m=2^m-m+1$. The subseries becomes

$$
T=\sum_{m=1}^{\infty}2^{-e_m},
\qquad
e_{m+1}-e_m=2^m-1\geq1.
$$

In particular the exponents $e_m$ are positive, strictly increasing integers and the series converges. Its partial sum through index $N$ is a dyadic rational

$$
T_N=\sum_{m=1}^{N}2^{-e_m}
=\frac{A_N}{2^{e_N}}
$$

for an integer $A_N>0$. Every tail is strictly positive. Since the successive exponents beyond $e_{N+1}$ are separated by **at least one**, comparison with the geometric series gives

$$
0<T-T_N\leq
\sum_{j=0}^{\infty}2^{-(e_{N+1}+j)}
=2^{1-e_{N+1}}.
$$

Suppose for a contradiction that $T=a/b$ for integers $a$ and $b>0$. Then

$$
b\,2^{e_N}(T-T_N)
=a\,2^{e_N}-bA_N
$$

is a strictly positive **integer**, so it is at least 1. But the proven tail bound yields

$$
0<b\,2^{e_N}(T-T_N)
\leq b\,2^{1+e_N-e_{N+1}}
=b\,2^{2-2^N}.
$$

For sufficiently large $N$, $2^{2^N-2}>b$, and thus the last upper bound is **strictly smaller than 1**. This contradicts positive integrality. Hence $T$ is irrational.

This proof is elementary and complete as a mathematical argument. Unlike the alternative binary-periodicity proof, it requires no choice of binary expansion and no argument about dyadic double representations.

## Adverse checks and finite fixtures

The first exponent values are $e_m=2,3,6,13,28$ for $m=1,2,3,4,5$. Thus

$$
T_4=\frac14+\frac18+\frac1{64}+\frac1{8192}
=\frac{3201}{8192}.
$$

The proof's critical conditions are independently explicit: the exponent gap is **$2^m-1$**, not $2^m$; the discarded tail is **strictly positive**; and for a hypothetical rational $a/b$ the denominator $b$ is fixed independently of $N$. The geometric tail bound holds because subsequent gaps are at least 1, regardless of occasional adjacent binary 1-digits at the start. The contradiction uses no assumption that $T_N$ is in lowest terms.

**Non-implication boundary:** irrationality of a positive subseries does not imply irrationality of the full sum. The omitted terms can change the rationality of $S$, so the original Erdős #249 conjecture remains open. No statement of the full series was proved here.

## Verification and custody limits

The displayed proof was independently reconstructed as a dyadic-denominator argument; it is not a Lean-checked theorem, independent human review, or MATHCERT certification. The registered full-conjecture Lean statement remains `by sorry`. The bounded formal successor is to prove the totient power-of-two identity, the gap and tail inequalities, and the dyadic rational separation argument in Lean with pinned toolchain and an actual successful kernel replay; then conduct a separate role-scoped adversarial check. Do not close issue #3205 or classify the full $S$ as irrational before its own proper acceptance.
