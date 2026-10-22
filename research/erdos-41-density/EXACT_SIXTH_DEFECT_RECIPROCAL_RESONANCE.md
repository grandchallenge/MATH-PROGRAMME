# Erdős #41 — Exact sixth-moment defect and reciprocal two-block resonance

**21 October 2026.** Track D / A crossover. Candidate exact integer theorem and source-first tests; **not an Erdős #41 solution**, novel priority claim, specialist RESULT/1, or mathematical certification.

## 1. The defect is an exact nonnegative collision ledger

For any finite integer set $E$ with $n=|E|$, let $\mathcal T(E)$ be the set of unordered three-element multisets drawn from E, allowing repetitions. Each $\tau\in\mathcal T(E)$ has integer sum $\sigma(\tau)$ and its number of distinct orderings $w(\tau)\in\{1,3,6\}$. Put

$$
F_E(\theta)=\sum_{a\in E}e^{2\pi ia\theta},
\qquad
\mathcal E_6(E)=\int_0^1|F_E(\theta)|^6\,d\theta.
$$

**Theorem A (exact defect/collision ledger).** The nonnegative integer

$$
\boxed{
\mathfrak d_6(E)
=\mathcal E_6(E)-(6n^3-9n^2+4n)
=2\sum_{\substack{\{\tau,\upsilon\}\subseteq\mathcal T(E)\\
\tau\ne\upsilon,\ \sigma(\tau)=\sigma(\upsilon)}}
w(\tau)w(\upsilon).
}
\tag{EXACT-DEFECT-LEDGER}
$$

In particular $\mathfrak d_6(E)=0$ if and only if E is a repetition-permitted B3 set. If $E\subseteq E'$, then $\mathfrak d_6(E)\le\mathfrak d_6(E')$. The latter is **monotonicity of the defect as an integer ledger**, not a decay of normalized counting density.

**Proof.** Fourier orthogonality gives $\mathcal E_6(E)=\sum_s r_E(s)^2$, where $r_E(s)=\sum_{\sigma(\tau)=s}w(\tau)$. Expanding each square produces the diagonal $\sum_\tau w(\tau)^2=36\binom n3+9n(n-1)+n=6n^3-9n^2+4n$ and the doubled positive off-diagonal products. Under inclusion all existing unordered triple pairs and their sums persist, so no prior defect contribution can disappear. QED.

**Important limitation.** Along a genuine B3 extension history, $\mathfrak d_6$ is IDENTICALLY ZERO, so a proof using only this nonnegative scalar has no density-drift mechanism. The content must come from showing that some future populated batch makes a positive new ledger entry unavoidable.

## 2. The far-field defect has an exact, translation-invariant factorization

Let P and T be two finite B3 sets of positive integers. Set $U=\max P$, $V=\max T$, and $W=\max(U,V)$. For the unordered pair sums of S define

$$
Q(S)=\{a+b:a,b\in S,\ a\le b\},
\quad
\omega_S(a+b)=
\begin{cases}
1,&a=b,\\
2,&a<b.
\end{cases}
$$

The value $\omega_S(q)$ is well-defined because B3 implies B2, so unordered pair sums are unique.

Define two **positive-distance correlation counts**, for each integer $d>0$:

$$
H_S(d)=\sum_{\substack{q,q'\in Q(S)\\q-q'=d}}
\omega_S(q)\omega_S(q'),
\qquad
G_S(d)=|\{(s,s')\in S^2:s-s'=d\}|.
$$

Both are nonnegative integers. We use $G_S(d)=0$ for positive distances absent from $S-S$.

**Theorem B (exact two-block far-field resonance).** For any integer shift $L>3W$,

$$
\boxed{
\mathfrak d_6(P\cup(L+T))
=
18\sum_{d>0}\bigl(H_P(d)G_T(d)+H_T(d)G_P(d)\bigr).
}
\tag{FAR-FIELD-RESONANCE}
$$

The right side is translation invariant in L and nonnegative. It vanishes exactly when both support intersections $D(Q(P))\cap D(T)$ and $D(Q(T))\cap D(P)$ are empty, where D denotes the set of positive differences.

**Proof.** Group unordered triples in the union by the number $j=0,1,2,3$ of elements belonging to $L+T$. All their sums lie within $jL+[3,3W]$, so the four groups have disjoint sum supports for $L>3W$. Because P and T are individually B3, the all-P and all-T groups contain no internal collisions. In the type with two P elements and one T element, the unordered triple indexed by $(q,t)\in Q(P)\times T$ has ordering weight $3\omega_P(q)$ and sum $L+q+t$. Distinct such triples coincide precisely when $q-q'=t'-t\ne0$. Counting each *unordered* colliding pair once, positive distances $d>0$ contribute $H_P(d)G_T(d)$ weighted pair products; the defect doubles the products, giving $2\cdot3^2=18$. The analogous type with one P and two T elements contributes $18\sum H_T(d)G_P(d)$. No other collisions occur. QED.

**Corollary (distance obstruction is exact at sixth order).** For any $L>3W$ the full union is B3 if and only if its two reciprocal correlation sums vanish. This is strictly a characterization of *a fixed two-block extension with a sufficiently separated location*: it does NOT imply every occupied future block lies in the far-field regime of every past block, nor that the right side must be positive for all critically populated future blocks.

## 3. Pairwise lower bound for any number of blocks, with no spacing assumption

**Theorem C (noncancelling many-block lower bound).** Let $B_1,\ldots,B_h$ be pairwise disjoint finite B3 subsets of the integers, and let $E=\bigcup_iB_i$. No assumption is made about their locations or diameters. Then

$$
\boxed{
\mathfrak d_6(E)\ge
18\sum_{1\le i<j\le h}\sum_{d>0}
\bigl(H_{B_i}(d)G_{B_j}(d)+H_{B_j}(d)G_{B_i}(d)\bigr).
}
\tag{MULTIBLOCK-POSITIVE-RESONANCE}
$$

**Proof.** Fix a pair of blocks $B_i,B_j$. A positive-distance overlap in $Q(B_i)-Q(B_i)$ and $B_j-B_j$ produces a collision between two distinct triple multisets of colour type $(2B_i,1B_j)$, with defect contribution 18 times the relevant pair-ordering weights. The reciprocal term produces collisions of type $(1B_i,2B_j)$. This logic holds irrespective of block positions: translating one block shifts every sum within that type by the same amount. Each colour type belongs to a **unique unordered block pair and orientation**, so its colliding unordered-triple pairs cannot be charged to any other $i,j$. All contributions are nonnegative summands already present in Theorem A. The global defect may include additional collisions, which only increase its value. QED.

For a globally B3 set E this bound has zero on both sides. It therefore proves an exact **noncancellation constraint**, but **not** a positive drift along legal extensions. It is a convenient source-locked baseline for testing any purported cross-scale "defect pressure" theorem: such a theorem must lower-bound one of these correlations for *unavoidably populated* future blocks, not just count possible forbidden distances.

## 4. Genuine hostile examples and the higher-order gap

Take $P=\{1,2,5,14\}$ and $T=\{1,2,5,14\}$. Both sets are B3 individually. For sufficiently large L, their union is not B3, with

$$
\sum_{d>0}H_P(d)G_T(d)
=
\sum_{d>0}H_T(d)G_P(d)=72,
$$

and the exact defect is $18(72+72)=2592$.

For $P=\{1,2,5,14\}$ and $T=\{33,72,125,219\}$, the two reciprocal correlations are zero, so a sufficiently distant translate of T yields a B3 union. At a *smaller* separation such as $L=100$, the defect can be positive (12) from collisions BETWEEN the four different colour-count classes even though the intrinsic pairwise resonances vanish. Thus equality in Theorem B requires the explicit separation hypothesis; Theorem C remains a valid lower bound without it.

Finally, the **genuine eight-element B3 carrier**

$$
P=\{1,2,5,14\},
\qquad
Y=\{1033,1072,1125,1219\}
$$

has nontrivial mixed four-sum overlap $\Xi_4(P,Y)=11$, yet **all its sixth-moment reciprocal resonance terms are zero**. This confirms that permitted fourth-order overlap is not itself a positive B3 collision defect. Any useful Xi4-to-future-pressure theorem must add a *third* genuinely constrained future cohort or another nontrivial mechanism.

## 5. Next mathematical gate

The sixth-moment defect is an exact *zero-or-positive* feasibility certificate, not a scalar potential that drifts along valid B3 prefixes. The falsifiable next obligation is to prove a density-dependent theorem of the form:

> For every hypothetical infinite B3 set with $A(N)\ge cN^{1/3}$ at all sufficiently large N, the genuinely occupied windows at selected scales force a positive sixth-order reciprocal resonance, or an independently quantified collision among distinct colour types.

That assertion would yield a contradiction because a genuine B3 history has identically zero defect. It is presently **UNPROVED** and is essentially the original difficulty in a more faithful arithmetic representation.

The claims in this note are bounded finite combinatorial identities, with no claim of novelty relative to the additive-energy literature. They require Track C #2792 logical audit before substantive mathematical certification; coordination #2789 and Track D #2793 remain open.
