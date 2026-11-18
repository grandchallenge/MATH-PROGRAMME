# Erdős #249 — WP04 signed Möbius tails and prime-window denominator isolation

**Record:** ERDOS-249-S-WP04/1  
**Issue:** [MATH-PROGRAMME #3473](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3473)  
**Date:** 2026-11-18 UTC  
**Claim class:** exact mathematical manuscript arguments and deterministic computational checks; no external mathematical certification  
**Full problem:** OPEN  
**Source authority:** pinned GCL [0249 manifest](../../governance/erdos_proof_verification/manifests/0249.json); source audit [#1518](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1518)  
**Reused bounded theorem:** irrational lacunary subseries $T$, closed as [#3205](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3205); not a proof of the original $S$

## 1. Exact mathematical object and prior art

The Erdős #249 question concerns

$$
S=\sum_{n=1}^{\infty}\frac{\varphi(n)}{2^n}.
$$

By the standard Möbius inversion identity for Euler's totient and the geometric derivative,

$$
\varphi(n)=n\sum_{d\mid n}\frac{\mu(d)}{d},
\qquad
S=\sum_{d=1}^{\infty}\mu(d)a_d,
\qquad
a_d=\frac{2^d}{(2^d-1)^2}.
$$

Both sides converge absolutely: $a_d=O(2^{-d})$. Define the *rational* finite truncation

$$
R_D=\sum_{d=1}^{D}\mu(d)a_d=\frac{A_D}{q_D}
$$

with $q_D\ge1$ and $\gcd(A_D,q_D)=1$.

The Möbius/squared-Lambert representation, finite denominator obstructions, phase criteria and rational countermodels **precede this packet**. Primary related research: Will Cook, *The Binary Totient Series* (July 2026, revised 1 October 2026), [full record](https://wcook04.github.io/practical-formal-verification/maths/papers/erdos249-totient-reasoning-surface--chapter-024ee725701b.html), [short paper](https://wcook04.github.io/practical-formal-verification/maths/papers/erdos-249-binary-totient-series.html). In particular, Cook's separate reduced-denominator bounds for LCM-based tail contributions are an antecedent to the prime-isolation mechanism below. This packet asserts **no novelty or priority**. GCL's own earlier full-series Fourier, sparse-orbit, and Farey experiments remain [in the same experiment directory](README.md).

## 2. WP04-A — strict weighted-tail domination (proved manuscript)

**Lemma A.1.** For every integer $m\ge1$,

$$
a_m-\sum_{d=m+1}^{\infty}a_d
=
\sum_{k=2}^{\infty} k\,2^{-km}
\left(1-\frac{1}{2^k-1}\right)
>
\frac{4}{3\cdot4^m}.
$$

**Proof.** The absolutely convergent geometric derivative gives

$$
a_d=\frac{2^{-d}}{(1-2^{-d})^2}
=\sum_{k=1}^{\infty}k\,2^{-dk}.
$$

Every term is nonnegative, so Tonelli's theorem for series permits the interchange

$$
\sum_{d=m+1}^{\infty}a_d
=\sum_{k=1}^{\infty}\frac{k\,2^{-km}}{2^k-1}.
$$

Subtract. The $k=1$ coefficient vanishes. Every $k\ge2$ coefficient is positive; the $k=2$ term is exactly $4/(3\cdot4^m)$. All $k\ge3$ terms are positive, yielding the strict inequality. No hypothesis on the Möbius sequence was used. QED.

**Theorem A.2 (first nonzero signed-tail term).** Let $D\ge1$ and let $m>D$ be the least integer with $\mu(m)\ne0$ (it exists because primes are squarefree). Then

$$
\mathrm{sgn}(S-R_D)=\mu(m)
$$

and

$$
|S-R_D|>
\frac{4}{3\cdot4^m}.
$$

**Proof.** For $D<d<m$, $\mu(d)=0$. Thus

$$
S-R_D=\mu(m)a_m+\sum_{d>m}\mu(d)a_d.
$$

Since $|\mu(d)|\le1$, the absolute value of the second sum is at most $\sum_{d>m}a_d$, which is strictly smaller than $a_m$ by Lemma A.1. The first term determines the sign. Reverse triangle inequality and Lemma A.1 give the strict lower bound. QED.

**Upper enclosure.** For $d\ge D+1$, the factor $(1-2^{-d})^{-2}$ decreases with $d$. Hence

$$
0<|S-R_D|
\le\sum_{d>D}a_d
<
\frac{2^{D+2}}{(2^{D+1}-1)^2}.
$$

The strict upper bound is valid because infinitely many coefficients $\mu(d)$ vanish at non-squarefree indices (and, independently, the factor inequality is strict for $d>D+1$). The tested function \`absolute_tail_upper(D)\` returns the displayed rational bound. The sign and strict lower enclosure together yield two-sided rational intervals enclosing $S$ on a known side of every $R_D$.

**Consequences.** Prime indices $m=p$ with $D=p-1$ give $\mu(p)=-1$, hence $S<R_{p-1}$. Indices $m=2p$ with $p$ an odd prime and $D=2p-1$ give $\mu(2p)=1$, hence $S>R_{2p-1}$. Both occur at arbitrarily large depths, since there are infinitely many primes. This is a bracket property, not irrationality.

## 3. WP04-B — exact reduced-denominator prime isolation (proved manuscript)

**Theorem B.1.** For every integer $D\ge2$, define

$$
\mathcal P_D=\{p:p\text{ prime},\ D/2<p\le D\}.
$$

Then the reduced denominator $q_D$ of $R_D$ is divisible by

$$
\boxed{
\prod_{p\in\mathcal P_D}(2^p-1)^2.
}
$$

**Proof.** Fix $p\in\mathcal P_D$. The summand with index $p$ is

$$
\mu(p)a_p=-\frac{2^p}{(2^p-1)^2}.
$$

Its numerator is coprime to its denominator. If $d\le D$ and $d\ne p$, then $p\nmid d$ because $D<2p$. Since $p$ is prime, $\gcd(p,d)=1$. The standard Mersenne gcd identity gives

$$
\gcd(2^p-1,2^d-1)=2^{\gcd(p,d)}-1=1.
$$

Thus every other summand has reduced denominator coprime to $2^p-1$. Adding them to the isolated index $p$ summand cannot cancel any prime-power factor of $(2^p-1)^2$ in the reduced denominator. This holds simultaneously for every $p\in\mathcal P_D$; distinct $p$ have pairwise coprime $(2^p-1)$. Their squared product therefore divides $q_D$. QED.

**Conditional dependency on a standard external theorem, not new.** The prime number theorem implies

$$
\sum_{D/2<p\le D}p
\sim\frac{3D^2}{8\log D}.
$$

Consequently Theorem B.1 implies

$$
\log q_D\ge
\left(\frac34+o(1)\right)
(\log2)\frac{D^2}{\log D}.
$$

Along the infinite subsequence $D=p-1$ for primes $p$, Theorem A.2 supplies

$$
|S-R_D|>\frac{4}{3\cdot4^{D+1}},
$$

and hence $q_D|S-R_D|\to\infty$ on that subsequence. The manuscript supplies the derivation conditional **only on the accepted prime number theorem**, not a self-contained proof of PNT. The unbounded product is not a denominator bound for $S$ itself.

## 4. What these results do *not* establish

If hypothetically $S=a/b$ were rational in lowest terms, then

$$
bq_D(S-R_D)=a q_D-bA_D
$$

would be a nonzero integer by Theorem A.2. An irrationality contradiction would require $0<bq_D|S-R_D|<1$ for some $D$. These natural Möbius truncations have **very large reduced denominators**, while their errors have definite sign and are not suppressed at a comparable rate. The elementary upper enclosure cannot give the required small-denominator contradiction. On the prime-index subsequence the PNT-dependent lower bound actually forces $q_D|S-R_D|\to\infty$.

This excludes **the naive use of $R_D$ as a vanishing-height rational-approximation certificate on that subsequence**. It does not exclude different approximants, signed combinations, engineered cancellation, Diophantine arguments, or the original irrationality.

**Hostile rational comparator:** The weights $w_n=2^{-n}+4^{-n}$ satisfy the same strict term-tail domination, because

$$
w_n-\sum_{d>n}w_d=\frac{2}{3\cdot4^n}>0,
$$

yet their all-positive series has the *rational* sum

$$
\sum_{n\ge1}w_n=1+\frac13=\frac43.
$$

Thus tail domination and infinitely many sign-controlled rational approximants are not, in isolation, irrationality criteria.

## 5. Reproduction and hostile test matrix

Module: [\`mobius_prime_denominators.py\`](mobius_prime_denominators.py).  
Tests: [\`test_erdos249_mobius_prime_denominators.py\`](../../tests/test_erdos249_mobius_prime_denominators.py).

Run from the repository root with standard-library Python:

\`\`\`bash
python3 -m unittest discover -s tests -p 'test_erdos249_mobius_prime_denominators.py' -v
python3 -c 'from experiments.erdos249_full_series_phase.mobius_prime_denominators import reduced_denominator_receipt; print(reduced_denominator_receipt(24))'
python3 ci/math_markdown_gate.py --file experiments/erdos249_full_series_phase/MOBIUS_SIGNED_TAIL_DENOMINATOR_004.md
\`\`\`

The ten tests check: (1) sieve $\mu$ against independent trial division; (2) exact geometric identity; (3) term dominance with a rigorously enclosed discarded tail; (4) tail sign/lower bound with rigorous remaining-tail error; (5) squared prime-window factors in the reduced denominator; (6) removal of the isolated prime term to falsify the denominator mechanism; (7) strict upper/lower inequality; (8) a rational countermodel to the unsupported implication; (9) independent coprime-enumeration reconciliation of the full totient series with the Möbius representation and explicit analytic error enclosures; (10) receipt claim boundary and exact integer factorization. All computational comparisons are exact \`fractions.Fraction\` arithmetic, not floating-point claims.

**Status at drafting:** proofs are elementary manuscript arguments; code and tests await execution/CI and protected exact-head readback. They are **not Lean-checked**, **not externally independently reviewed**, **not MATHCERT-certified**, and **not a novelty claim**. Update execution and admission status using actual run receipts; never infer them from this prose.

## 6. Claim ledger and deterministic successor

| ID | Claim | Evidence | Authority |
| --- | --- | --- | --- |
| WP04-A | First nonzero $\mu$ fixes signed truncation error and strict lower gap | Lemma A.1 and Theorem A.2; executable hostile tests | Manuscript proof; needs independent critical pass |
| WP04-B | Prime-window squared factors divide the reduced $q_D$ | Theorem B.1; exact-fraction divisibility and prime-omission tests | Manuscript proof; needs independent critical pass |
| WP04-C | Along $D=p-1$, $q_D|S-R_D|\to\infty$ | A.2 + B.1 + classical PNT | Known-theorem dependent deduction |
| WP04-N | These approximants and signed domination do **not** establish irrationality | Explicit denominator barrier and rational comparator | Negative route assessment |
| ORIGINAL-249 | $S\notin\mathbb Q$ | **No proof** | **OPEN** |

**Next substantive work:** seek a *totient-specific cofinal arithmetic separation* that escapes both (i) the rational comparator and (ii) the height barrier for raw $R_D$; in particular test denominator-clearing combinations with a provable reduction in height relative to the tail error, or prove one of Cook's existing cofinal phase/residue conditions. Before launching any further finite sweep, formulate the exact new inequality, prove why it would imply the original statement, and identify a plausible independent number-theoretic input. Existing GCL Fourier and Farey explorations and Cook's longer research record are mandatory antecedents. Retain original problem OPEN and certification NOT_SUBMITTED.
