# Erdős #249 — WP05: cofinal finite-prime congruences and a one-depth obstruction

**Research record:** ERDOS-249-S-WP05/1  
**Date:** 2026-11-18 UTC  
**Authoring/review status:** manuscript-level arithmetic; explicit same-agent adversarial review required  
**Original problem:** OPEN. No Lean proof or MATHCERT certification of the full series  
**Source locks:** GCL proof-verification manifest 0249; completed auxiliary-T issue #3205; signed-tail WP04 issue #3473; parent #3201

## Source and prior-art lock

The original open Erdős #249 problem asks whether

$$
S=\sum_{n=1}^{\infty}\frac{\varphi(n)}{2^n}
$$

is irrational. The corresponding scaled tail is

$$
U_N=\sum_{j=1}^{\infty}\frac{\varphi(N+j)}{2^j}.
$$

For a positive shift $H$, the exact difference is

$$
V_{H,N}=U_{N+H}-U_N
=\sum_{j\ge1}\frac{\varphi(N+H+j)-\varphi(N+j)}{2^j}.
$$

Will Cook's *The Binary Totient Series*, revised 1 October 2026, already proves a cofinal prime-position modulo-four totient pulse (Proposition 6.91), a high-two-adic prime construction (Proposition 6.92), and the directed residue criterion (Proposition 6.69). Proposition 6.70 supplies a **conditional** prime-pulse irrationality route. The associated condition on every candidate period is still open. The cited paper is the source of the CRT–Dirichlet construction and the earlier high-divisibility witness. This work **does not** claim novelty or priority for that method.

Source: https://wcook04.github.io/plectis/maths/papers/erdos249-totient-reasoning-surface--chapter-b5c5789c9d0d.html

Previously protected GCL full-series investigations include Fourier phase, sparse irrational orbit, Farey denominator exclusion, and WP04 signed Möbius-tail and reduced-denominator isolation. None proved irrationality of $S$.

## A. Simultaneous cofinal forward-pulse theorem

**Theorem A.** Let $\mathcal H$ be a nonempty finite set of positive integers. For every positive $L,K$, every bound $B\ge0$, and $K_0=\max(K,2)$, there is a prime $p>B$ satisfying

$$
p\equiv3\pmod4
$$

and, **simultaneously for every** $h\in\mathcal H$,

$$
2^{K_0}\mid\varphi(p+4h),
\qquad
\varphi(p+4h)-\varphi(p)\equiv2\pmod4,
$$

and for every integer $1\le j\le L$,

$$
2^{K_0}\mid\varphi(p+j),
\qquad
2^{K_0}\mid\varphi(p+4h+j).
$$

Indeed, infinitely many such primes exist.

**Proof.** Form the finite set of distinct positive offsets

$$
\mathcal T=
\{4h:h\in\mathcal H\}
\cup\{1,\ldots,L\}
\cup\{4h+j:h\in\mathcal H,\ 1\le j\le L\}.
$$

For each $t\in\mathcal T$ choose a **distinct** prime $q_t>\max\mathcal T$ satisfying

$$
q_t\equiv1\pmod{2^{K_0}}.
$$

Dirichlet's theorem supplies infinitely many eligible auxiliary primes. The pairwise coprime congruences

$$
p\equiv3\pmod4,
\qquad
p\equiv-t\pmod{q_t}\quad(t\in\mathcal T)
$$

have a unique common residue class modulo $4\prod_tq_t$ by the Chinese remainder theorem. This class is reduced: it is odd modulo four and nonzero modulo every $q_t$, because $0<t<q_t$. Dirichlet therefore supplies infinitely many primes $p$ in this class, arbitrarily far beyond $B$.

For each such prime, $q_t\mid p+t$, and the totient prime-factor formula gives $q_t-1\mid\varphi(p+t)$. Hence $2^{K_0}\mid\varphi(p+t)$. Meanwhile $\varphi(p)=p-1\equiv2\pmod4$ because $p$ is prime congruent to three modulo four. These facts give every required congruence. QED.

**Corollary A.1.** If $K\ge L$, then for every $h$ in the prescribed finite family the truncated shifted-tail difference

$$
V_{4h,p,L}=
\sum_{j=1}^{L}
\frac{\varphi(p+4h+j)-\varphi(p+j)}{2^j}
$$

is an integer divisible by $2^{K-L}$. Equivalently, the exact integer residue

$$
D(4h,p,L)=
\sum_{j=1}^{L}2^{L-j}
\bigl(\varphi(p+4h+j)-\varphi(p+j)\bigr)
$$

satisfies

$$
D(4h,p,L)\equiv0\pmod{2^L}.
$$

The proof is termwise divisibility by $2^K$. Thus for **any fixed finite family of shifts and any fixed depth** there exist arbitrarily large prime positions on which that finite residue test cannot certify nonintegrality. This is not a theorem about the untruncated infinite difference.

## B. The omitted infinite tail is not certified small

The exact discarded difference is

$$
V_{4h,p}-V_{4h,p,L}
=
\sum_{j>L}\frac{\varphi(p+4h+j)-\varphi(p+j)}{2^j}.
$$

Since both totient values are nonnegative and no larger than their arguments,

$$
\left|V_{4h,p}-V_{4h,p,L}\right|
\le
\sum_{j>L}\frac{p+4h+j}{2^j}
=
\frac{p+4h+L+2}{2^L}.
$$

For a **fixed** depth $L$ this valid **upper bound** diverges along the cofinal prime progression. This observation means only that the bound cannot certify a small omitted tail. It does **not** prove that the actual omitted difference diverges, is nonintegral, or has any specified sign. No interchange of fixed-depth and moving-depth limits is justified.

A finite-prefix rational polynomial can match every totient value used in a **single** constructed window and therefore match its finite congruences. This is a negative control, not a claim that one rational comparator matches an entire cofinal family. Cook's more sophisticated rational controls must remain part of any later full-series argument.

## C. Same-depth no-go theorem for Cook's high-divisibility witnesses

This analyzes an already published result, Cook Proposition 6.92, rather than presenting its midpoint formula as new. Fix integers $K\ge2$ and $H>K$. Suppose a prime $p>H+K$ satisfies the conditions used in that proposition:

$$
p\equiv1+2^{K-1}\pmod{2^K},
\qquad
2^K\mid\varphi(p+H),
$$

and for each $1\le j<K$,

$$
2^K\mid\varphi(p-j),
\qquad
2^K\mid\varphi(p-j+H).
$$

Set $N=p-K$. Cook's source obtains the midpoint residue

$$
D(H,N,K)\equiv2^{K-1}\pmod{2^K}.
$$

**Theorem B (one-depth certificate obstruction).** Under these hypotheses, **no** residue modulo $2^K$ at this start $N$ can pass the standard directed nonintegrality certificate at depth $K$.

**Proof.** Cook's directed certificate requires the residue to satisfy, as its necessary lower inequality,

$$
N+K+2\le D(H,N,K)\bmod 2^K.
$$

The left side is $p+2$. But $K\ge2$ permits $j=1$ in the high-divisibility hypotheses, so the **positive** integer $\varphi(p-1)$ is divisible by $2^K$. Consequently

$$
2^K\le\varphi(p-1)\le p-1,
\qquad
p+2\ge2^K+3.
$$

Every residue modulo $2^K$ lies between zero and $2^K-1$. Thus the necessary inequality fails for **every** residue, not merely for Cook's midpoint residue. QED.

Even the weaker residue-class restriction $p\equiv1+2^{K-1}\pmod{2^K}$ implies $p+2>2^{K-1}$, already excluding the displayed midpoint at this depth. The totient valuation makes the obstruction uniform across all possible residues.

**Interpretation:** Cook's Proposition 6.92 remains mathematically valid, and this theorem does **not** disprove its source or eliminate all finite-residue arguments. It proves a narrow incompatibility between its prescribed high-power divisibility at one depth and the *same-depth standard tail-error certificate*. A successful argument must use a larger analytic depth, a sharper error estimate, or an independent new source of actual nonintegrality.

## D. Verification, claim ledger, and research successor

Reproducible standard-library Python is in the prime-pulse library, with an independent hostile test module. The executable checks reconstruct Euler's totient from factorization and coprime counting, verify reduced CRT progression identities and primality of finite witnesses, prove their two-adic congruences in exact arithmetic, test a finite family of shifts simultaneously, reproduce the backward midpoint residue, and verify that its certificate threshold fails. The computer's finite prime scan **does not** prove the Dirichlet infinitude assertion; that step is supplied by the named classical theorem.

| ID | Claim | Grounding | Status |
| --- | --- | --- | --- |
| WP05-A | Simultaneous forward congruences at infinitely many prime positions | CRT + Dirichlet + totient formula; finite exact tests | Manuscript theorem |
| WP05-A1 | Finite front integral at depth $L\le K$ | Exact divisibility; dyadic tests | Manuscript corollary |
| WP05-B | Cook 6.92 witnesses cannot pass the standard **same-depth** directed residue certificate | Size constraint $2^K\mid\varphi(p-1)$; source criterion | Manuscript negative theorem |
| WP05-N | Local congruence does not settle actual infinite-tail integrality | Explicit error bound and rational finite-prefix control | Established scope firewall |
| ERDOS-249 | Irrationality of the full sum $S$ | **No proof** | **OPEN** |

**Next substantive obligation (WP06):** A *two-scale* arithmetic-and-analytic producer. Distinguish the congruence-forcing exponent $K$ from the final certification depth $L>K$. Prove a nontrivial bound or construct residues guaranteeing that for every hypothetical rational period $H$ (or on the source-locked LCM diagonal), some arbitrarily large $N$ and depth $L$ satisfy the complete directed nonintegrality interval. A finite prime scan, a fixed-depth CRT witness, an unbounded **upper bound** on its error, or another unrelated lacunary subseries cannot meet that obligation.

**Provenance boundary:** No claim of new priority, independent human review, Lean replay, theorem certification, original irrationality proof, or external promotion. Preserve any separate review/CI/merge state as evidence rather than assuming completion from this manuscript.
