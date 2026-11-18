# Erdős #249 — WP07-B: a rational series with all-position near-logarithmic finite-tail integrality

**Research record:** ERDOS-249-S-WP07-B/1  
**Parent workstream:** [#3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500)  
**Status:** elementary manuscript theorem and exact deterministic hostile controls; **not an irrationality proof**  
**Original full-series problem:** OPEN. **MATHCERT:** NOT_SUBMITTED  
**Date:** 2026-11-18 UTC

## 1. Provenance, scope and source relationship

The original Erdős #249 asks whether

$$
S=\sum_{n\ge1}\frac{\varphi(n)}{2^n}
$$

is irrational. Our earlier [WP07-A](MOVING_LOGLOG_INTEGRALITY_007.md) establishes, using the classical Selberg–Delange moment estimate, that a shallow truncation of the *actual totient tail* is integral for almost every start even at depths proportional to $\log\log X$. This new work package studies a different, synthetic integer-coefficient sequence; it does **not** assert the same deep divisibility statement for the actual Euler totient.

The purpose is to falsify a tempting generic inference: that all-position integer finite tails at almost logarithmic analytic depth, positive coefficients of linear magnitude, and increasing two-adic coefficient valuations would suffice to make the complete binary sum irrational. They do not.

The generic dyadic coboundary mechanism is elementary and was also used in GCL's [WP06](COBOUNDARY_TWO_SCALE_006.md) prime-pulse rational comparator. Will Cook, *The Binary Totient Series* (2026, revised 1 October 2026), already provides stronger, **totient-specific** conditional irrationality criteria and rational countercontrols. The construction here is a bounded methodological control; mathematical novelty, historical priority, independent review, and formal certification are not asserted.

## 2. Construction

For every positive integer $n$, put

$$
c_n=\left\lfloor\frac n2\right\rfloor,
\qquad
M_n=2^{\max(0,\lfloor\log_2 n\rfloor-5)}.
$$

Define integers $b_0=0$ and, recursively,

$$
0\le b_n<M_n,\qquad
b_n\equiv c_n+2b_{n-1}\pmod{M_n}.
$$

The residue is chosen canonically in $[0,M_n)$; thus the sequence is defined deterministically, without a search for any target real number. Finally define

$$
\boxed{
a_n=c_n+2b_{n-1}-b_n.
}
\tag{1}
$$

The divisibility is built in: since $b_n$ is the residue modulo $M_n$ of $c_n+2b_{n-1}$,

$$
\boxed{M_n\mid a_n.}
\tag{2}
$$

The values $M_n$ are nondecreasing powers of two, and $M_n\le n/32$ whenever $n\ge64$.

## 3. Theorem A — rational sum and linear coefficient bounds

**Theorem A.** The sequence $(a_n)_{n\ge1}$ defined above consists of integers satisfying

$$
a_1=0,\qquad
\boxed{\frac n4\le a_n\le n\quad(n\ge2),}
$$

and the *full infinite sum* is the exact rational value

$$
\boxed{\sum_{n=1}^{\infty}\frac{a_n}{2^n}=\frac23.}
$$

**Proof of bounds.** If $n<64$, $M_n=1$ and thus $b_n=0$. Therefore $a_n=\lfloor n/2\rfloor$. This satisfies $n/4\le a_n\le n$ for $n\ge2$ and gives $a_1=0$.

For $n\ge64$, the facts $M_{n-1}\le M_n\le n/32$, $0\le b_n<M_n$ and $0\le b_{n-1}<M_{n-1}$ yield

$$
\left\lfloor\frac n2\right\rfloor-(M_n-1)
\le a_n
\le\left\lfloor\frac n2\right\rfloor+2(M_{n-1}-1).
$$

Consequently

$$
a_n\ge\frac n2-\frac12-\frac n{32}+1>\frac n4
$$

and

$$
a_n<\frac n2+\frac n{16}<n.
$$

Both bounds are uniform across the jumps of the power-of-two modulus.

**Proof of exact sum.** The coboundary has an exact telescoping identity at every finite depth $N$:

$$
\begin{aligned}
\sum_{n=1}^{N}\frac{2b_{n-1}-b_n}{2^n}
&=\sum_{n=0}^{N-1}\frac{b_n}{2^n}
-\sum_{n=1}^{N}\frac{b_n}{2^n}\\
&=-\frac{b_N}{2^N},
\end{aligned}
$$

as $b_0=0$. Since $0\le b_N<M_N\le\max(1,N/32)$ for all sufficiently large $N$, the right-hand side tends to zero. The series on the left is absolutely convergent because $b_n=O(n)$.

Separately, the ordinary generating function of $c_n$ is

$$
\sum_{n\ge1}\left\lfloor\frac n2\right\rfloor x^n
=\frac{x^2(1+x)}{(1-x^2)^2}.
$$

At $x=1/2$ this equals $2/3$. Equation (1) and the vanishing coboundary then give the displayed rational full sum. QED.

**Important limitation:** Even though the full value is rational, the binary coefficient sequence need not be eventually periodic: the coefficients are not binary digits. In particular, no reasoning about eventual periodicity of the coefficients or the integer portion of a scaled tail is valid without further hypotheses.

## 4. Theorem B — all-position near-logarithmic integrality

**Theorem B.** For *every* integer $N\ge64$, choose

$$
L_N=\lfloor\log_2N\rfloor-5\ge1.
$$

Then

$$
\boxed{
U^a_{N,L_N}
=\sum_{j=1}^{L_N}\frac{a_{N+j}}{2^j}
\in\mathbb Z.
}
\tag{3}
$$

Nevertheless its **true positive omitted tail** is at least four:

$$
\boxed{
U^a_N-U^a_{N,L_N}
=\sum_{j>L_N}\frac{a_{N+j}}{2^j}\ge4.
}
\tag{4}
$$

Finally, the fractional part of this omitted infinite tail is never zero; it equals

$$
\boxed{
\left\{U^a_N-U^a_{N,L_N}\right\}=
\begin{cases}
2/3 & N\text{ even},\\
1/3 & N\text{ odd}.
\end{cases}
}
\tag{5}
$$

**Proof of (3).** The modulus $M_n$ is nondecreasing. If $1\le j\le L_N$, then $N+j>N$, so

$$
M_{N+j}\ge M_N=2^{L_N}\ge2^j.
$$

Combining this with $M_{N+j}\mid a_{N+j}$ proves that every term $a_{N+j}/2^j$ is individually an integer, not just that the truncated sum is integral.

**Proof of (4).** All $a_n$ are nonnegative, and the first omitted term suffices:

$$
U^a_N-U^a_{N,L_N}
\ge\frac{a_{N+L_N+1}}{2^{L_N+1}}
\ge\frac{N+L_N+1}{4\cdot2^{L_N+1}}.
$$

If $k=\lfloor\log_2N\rfloor$, then $L_N=k-5$ and

$$
2^{L_N+1}=2^{k-4}\le\frac N{16}.
$$

Therefore the displayed lower bound is at least $4(1+(L_N+1)/N)>4$, and the weaker bound $\ge4$ holds as stated.

**Proof of (5).** Write the entire rational sum as $A=2/3$. The scaled full tail is

$$
U^a_N=2^N A
-\sum_{n=1}^{N}a_n2^{N-n}.
$$

The second term is an integer. The truncated tail (3) is also an integer. Therefore their subtraction does not change the fractional part, and

$$
\{U^a_N-U^a_{N,L_N}\}
=\left\{\frac{2^{N+1}}3\right\}.
$$

The residue $2^{N+1}\bmod3$ is two for even $N$, one for odd $N$. This proves (5). QED.

## 5. Why the stronger countermodel matters and what it does not say

The scale $L_N=\log_2N+O(1)$ is within a fixed additive offset of the depth at which the standard **upper** estimate for a linear-size tail can become small. Unlike WP07-A's genuine-totient theorem at $\alpha\log\log X$, this rational control exhibits integrality of each finite summand for **every** sufficiently large starting index at the deeper logarithmic scale. Its positive omitted tail is provably large, with a nonzero periodic fractional part.

Thus the implication

> High two-adic divisibility of coefficients through a moving window, plus positive linear coefficient growth, plus the resulting all-position near-logarithmic finite-tail integrality, forces irrationality of the full binary sum

is **false** without a further arithmetic hypothesis specific to the Euler totient function.

It does **not** follow that the actual totient series has this near-logarithmic integrality property, or that a rational sequence could satisfy Cook's full good-base harmonic-saving hypothesis. The latter is a quantitatively stronger, cofinal, *totient-specific* statement. Existing GCL irrational lacunary orbit controls provide a separate counterexample to generic Fourier cancellation.

## 6. Executable evidence and claim ledger

Implementation: [nearlog_rational_coboundary.py](nearlog_rational_coboundary.py).  
Tests: [test_erdos249_rational_pulse_coboundary.py](../../tests/test_erdos249_rational_pulse_coboundary.py), extending the **already governed** WP06 rational-control test suite without a new CI route. Code uses only standard-library exact integer arithmetic and fractions.

Hostile tests independently check the modulus jumps, congruence condition, coefficient inequalities for thousands of indices, telescoping at several modulus boundaries, rational generating function, simultaneous integrality for every start in a large finite interval, true first-omitted-term lower bound, exact alternating fractional parts, receipt invariants, and malformed inputs. **Finite tests are supplementary checks**; the universal and infinite statements follow from the manuscript proofs, not from numerical exhaustion.

| Claim | Grounding | Claim scope |
| --- | --- | --- |
| WP07-B-A | Bounded deterministic variable-modulus carries yield integer $n/4\le a_n\le n$ and full value $2/3$ | Elementary proved manuscript theorem |
| WP07-B-B | For all $N\ge64$, the $L_N$ finite tail is integral | Exact divisibility argument |
| WP07-B-C | The omitted positive tail exceeds four, while its fractional part alternates $2/3$, $1/3$ | First-term lower bound and exact scaled rational full sum |
| WP07-OPEN | Genuine totient-specific cofinal harmonic or residue separation at analytic depth | **UNPROVED** |
| ORIGINAL-249 | Irrationality of $S$ | **OPEN** |

**Next positive mathematical obligation.** Seek a condition on **the actual coefficients $\varphi(n)$** that cannot be reproduced by rational-coboundary controls. A promising candidate must force a nontrivial cofinal lower bound on the distance of a moving-depth totient residue to the nearest integer, at depths that make the *actual infinite-tail error* smaller than that distance, for every hypothetical denominator period. Any attempted generic argument from linear growth, coefficient valuations, finite integrality or finite prime pulses must be rejected by the WP06 and WP07-B controls. Cook's existing equivalent/sufficient criteria are the source-locked starting point; restating them is not progress.

**Certification boundary:** No GCL result here certifies irrationality of the original full totient series, and no independent human mathematical review, Lean proof, or novelty priority is asserted.
