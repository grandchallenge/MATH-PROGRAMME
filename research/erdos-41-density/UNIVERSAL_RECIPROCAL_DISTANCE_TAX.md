# Erdős #41 — Universal cubic difference tax across reconfigured scales

**20 October 2026. Mathematical status:** A rigorous universal, nonduplicated **cumulative reciprocal compatibility cost** is proved for every repeated-summand B3 set along a separated-anchor sequence. Under a *hypothetical* persistent critical lower-density condition the anchors can be chosen with bounded multiplicative gaps and the absolute tax is linear in each preceding scale. **The cost does not exceed the available difference budget; no critical-density contradiction and no solution of Erdős #41 is claimed.** This result does not assume fixed residue patterns, a shared finite-field alphabet, or arithmetic alignment.

## 1. Exact one-anchor creation of new reciprocal forbidden distances

Let P be any nonempty finite B3 set in [1,R] and let n=|P|. Let

$$
Q(P)=\{a+b:a,b\in P,\ a\le b\}
$$

denote the unordered pair-sum set, and let its positive difference spectrum be

$$
D(P)=\{q-q':q,q'\in Q(P),\ q>q'\}.
$$

For each B3 set P, two exact cardinality formulae hold:

$$
|Q(P)|=\binom{n+1}{2},
\qquad
|T(P)|=\left|P+P-P\right|
=\frac{n^3-n^2+2n}{2}.
$$

The first is B2 uniqueness (which follows from B3). To prove the second, note that the n original members of P belong to T(P). Every triple consisting of a denominator c in P and an unordered positive pair a<=b from P excluding c produces a+b−c outside P, by B2 uniqueness. Two such signed words cannot coincide: equality a+b−c=a'+b'−c' would give a+b+c'=a'+b'+c, and B3 uniqueness forces c=c' and identical unordered positive pairs. Each denominator has binom(n,2) eligible repeated-positive unordered pairs. Therefore |T(P)|=n+n*binom(n,2).

**Theorem A (exact decomposition of ALL new pair-sum distances).** If y>4R is an integer, then P'=P union {y} is B3 and

$$
\boxed{
|D(P')\setminus D(P)|
\ =\
\frac{n^3+3n}{2}.
}\tag{UNIVERSAL-CUBIC-DISTANCE-TAX}
$$

More precisely, two **disjoint** subsets of genuinely new positive distances are

$$
\boxed{
B_1=y-T(P),\qquad B_2=2y-Q(P).
}\tag{UNIQUE-NEW-DISTANCE-BANDS}
$$

These bands have respective sizes (n^3−n^2+2n)/2 and n(n+1)/2 and lie strictly ABOVE all old distances D(P).

**Proof.** The three classes of new unordered pair sums are Q(P), y+P, and {2y}; by B2 they are disjoint. For any p,a,b in P, the difference (y+p)−(a+b)=y−(a+b−p) belongs to D(P'), so B1 subset D(P'). Similarly 2y−(a+b) belongs to D(P'), so B2 subset D(P').

Every old pair sum lies in [2,2R], whence D(P) subset [1,2R−2]. Since T(P) subset [2−R,2R−1], the first band satisfies B1 subset [y−2R+1,y+R−2], which is above 2R−2 when y>4R. The second band lies in [2y−2R,2y−2], and its minimum exceeds the maximum of the first when y>3R−2. Thus B1,B2 are mutually disjoint and avoid D(P). Their exact cardinalities add to (n^3+3n)/2, as claimed. The separation y>4R also makes P' B3 by separating triple-sum classes with zero, one, two or three copies of y. QED.

**Exhaustiveness audit (strengthens Theorem A from a lower bound to equality).** Every pair of unordered sums in the enlarged set $Q(P')=Q(P)\,\dot\cup\,(y+P)\,\dot\cup\,\{2y\}$ falls into exactly one of six type pairs. Differences within $Q(P)$ are $D(P)$; differences within $y+P$ are positive differences $P-P\subset D(P)$, because for fixed $t\in P$, $(p+t)-(p'+t)=p-p'$. Differences between $y+P$ and $Q(P)$ are exactly $y-T(P)$. Differences between $\{2y\}$ and $Q(P)$ are exactly $2y-Q(P)$. Finally differences between $\{2y\}$ and $y+P$ are $y-P\subseteq y-T(P)$ because $P\subseteq T(P)$. Thus there are **no other types of new difference** and

$
\boxed{
D(P\cup\{y\})=
D(P)\;\dot\cup\;(y-T(P))\;\dot\cup\;(2y-Q(P)).
}\tag{COMPLETE-DIFFERENCE-DECOMPOSITION}
$

The three pieces are pairwise disjoint for $y>4R$. This exact identity establishes that the cubic increment $(n^3+3n)/2$ is **the whole one-anchor contribution**, not a conservative estimate with missing hidden differences.

**Short-window invisibility.** Both new bands consist of distances strictly greater than $2R-2$. Therefore **neither new band prohibits two points lying in the same interval of at most $2R-1$ consecutive integers**: their mutual difference is at most $2R-2$. These distances can still obstruct pairs drawn from *different* future intervals; no claim of global independence is made. This locates the genuinely missing interaction: an already charged band must be proved to hit cross-window differences of the actual populated future elements.

**Interpretation.** D(P') is the forbidden-distance spectrum for every later batch: any two later elements whose difference belongs to D(P') cannot jointly extend P' to a B3 set, because the distinct PPX triple sums collide. Therefore the new bands are **new reciprocal constraints**, not just numerical representations. They cannot be avoided by changing the structure of P or the placement of subsequent elements.

## 2. Universal telescoping across arbitrarily reconfigured prefixes

Let A be an infinite B3 set. Start with any sufficiently large integer R_0. Define recursively

$$
R_{j+1}=\min\{a\in A:a>4R_j\},
\qquad P_j=A\cap[1,R_j],
\qquad n_j=|P_j|.
$$

Every R_(j+1) exists since A is infinite, and R_(j+1)>4R_j. Although A may contain other points between R_j and R_(j+1), Theorem A applies to the B3 subset P_j union {R_(j+1)}. Its two new distance bands lie above the old full D(P_j), and hence are also contained in D(P_(j+1)) minus D(P_j).

**Theorem B (fully nonduplicated cumulative reciprocal cost).** For every h>=1,

$$
\boxed{
|D(P_h)|-|D(P_0)|
\ \ge\
\frac12\sum_{j=0}^{h-1}(n_j^3+3n_j).
}\tag{CUMULATIVE-DISTANCE-COST}
$$

Every newly charged distance has one unique owner: the first stage at which it appears in the monotonically growing pair-sum difference spectrum. No fixed alphabet, digit tags, block alignment, mixing, or probabilistic rounding is assumed. The telescope remains valid under arbitrary changes in arithmetic organization between the stages.

## 3. Hypothetical persistent critical density: bounded scale ratios and linear stage taxes

Assume HYPOTHETICALLY that one infinite B3 set A obeys

$$
A(N)\ge cN^{1/3}
\quad\text{for all sufficiently large integers }N,
\qquad 0<c\le1.
$$

The elementary upper bound from counting distinct three-term sums is A(N)<= (18N)^(1/3). Choose the fixed integer

$$
K_c=\left\lceil(5/c)^3\right\rceil.
$$

For all sufficiently large R we have

$$
A(K_cR)\ge cK_c^{1/3}R^{1/3}\ge5R^{1/3}
>(72R)^{1/3}\ge A(4R).
$$

Consequently the first actual A-point after 4R lies at most K_c R. In the sequence from Theorem B, for all sufficiently large j,

$$
\boxed{4R_j<R_{j+1}\le K_c R_j.}\tag{BOUNDED-ANCHOR-RATIOS}
$$

Moreover n_j>=c R_j^(1/3), so the **new genuinely forbidden distance count** at every stage satisfies

$$
\boxed{
|D(P_{j+1})\setminus D(P_j)|
\ge\frac{c^3}{2}R_j.
}\tag{LINEAR-PER-STAGE-COST}
$$

Thus the cumulative cost obeys

$$
\boxed{
|D(P_h)|-|D(P_0)|
\ge\frac{c^3}{2}\sum_{j<h} R_j.
}\tag{DENSITY-DEPENDENT-CUMULATIVE-COST}
$$

Because R_(j+1)>4R_j, the geometric bound is

$$
\sum_{j<h}R_j<\frac13 R_h.
$$

Also all positive pair-sum differences of P_h lie below 2R_h; therefore the **available distance spectrum has capacity at most 2R_h−2**. The forced cost is *linear* in the scale, but the available budget is ALSO linear in the scale. This argument does not show the forced cost exceeds capacity, even after arbitrarily many stages.

The bounded-gap property K_c is necessary for hypothetical persistent density, but it does not fix the difficulty: a fixed fraction of each newly enlarged arithmetic arena can pay for these nonduplicated distance constraints indefinitely, so long as no additional *superlinear* or *mutually competing* shadow deficit is proved.

## 4A. A rigorous scalar non-overload model: why the exact charge cannot prove a valley by itself

The universal distance increment can now be audited against its entire scalar ambient capacity, rather than extrapolated. The following is a **countermodel to a proposed inference from inequalities**, not a new B3 construction.

**Proposition C (critical-order occupancy and all charged distance volumes remain compatible).** Fix any $0<c\le 1/2$ and integer $R_0\ge\max(10,\lceil c^{-3}\rceil)$. For all $j\ge0$ define the abstract numerical sequences

$
R_j=5^j R_0,\qquad
n_j=\lceil cR_j^{1/3}\rceil,\qquad
d_0=0,\qquad
d_h=\frac12\sum_{j<h}(n_j^3+3n_j).
$

Then, for **every** $h\ge1$ simultaneously,

$
\boxed{
n_j\ge cR_j^{1/3},\qquad
4R_j<R_{j+1}\le K_cR_j,\qquad
d_h<2R_h-2.
}\tag{SCALAR-NO-OVERLOAD}
$

Moreover $d_{j+1}-d_j=(n_j^3+3n_j)/2$ is precisely the **exact** charge from one distant anchor. Thus the numerical inequalities in Theorem B, the persistent-density lower bound, the bounded-ratio requirement, and the $O(R_h)$ capacity upper bound are all jointly feasible indefinitely at the scalar level.

**Proof.** Since $R_j\ge c^{-3}$, the ceiling gives $n_j\le2cR_j^{1/3}$. Then

$
\frac{n_j^3+3n_j}{2}
\le 4c^3R_j+3cR_j^{1/3}
\le7c^3R_j.
$

The last bound follows from $R_j^{2/3}\ge c^{-2}$. Summing a geometric series,

$
d_h\le7c^3\sum_{j<h}R_j
<\frac{7c^3}{4}R_h
\le\frac7{32}R_h<2R_h-2.
$

Here $R_h\ge50$, so the final inequality is immediate. Also $R_{j+1}=5R_j$ and $K_c=\lceil(5/c)^3\rceil\ge125>5$. QED.

**Logical scope is essential.** The sequences $(R_j,n_j,d_j)$ are **numbers**, not the counting function and difference spectra of one actual infinite B3 set. In particular the growth of $n_j$ requires many actual intermediate elements, which might create **additional coupled differences** not included in the one-anchor charge. Those uncounted joint contributions are precisely where a real density contradiction could arise. The proposition proves only that the *universal one-anchor charges plus scalar ambient capacity* are not enough to deduce such a contradiction. It does NOT rule out a stronger theorem exploiting all actual intermediate elements and their cross-scale signed-sum compatibility.

### Concrete missing interaction

Let $Y$ be any later B3 block jointly compatible with P. Its pair differences $Y-Y$ must avoid $D(P)\setminus\{0\}$ by PPY triple uniqueness. This statement is independent of the position of $Y$, but it does not guarantee $Y-Y$ meets any of the newly created long-distance bands of $D(P\cup\{y\})$. In fact the two exact new bands from Theorem A cannot themselves intersect differences internal to a length-R interval. Their **cross-window** interaction, including the forced occupation of several future windows under hypothetical persistence, must therefore be quantified before a cardinality deficit can be inferred.

This is a narrow, testable research target: find a c-dependent lower bound for conflict *between actual differently positioned future cohorts*, not just for the total number of forbidden distances. A viable bound must detect the many intermediate elements omitted by the scalar relaxation.

### Relation to known conditional progress

The full odd-order B3 density-valley conjecture remains open. Táfula's 2026 work on zero-sum linear forms proves substantial density restrictions under explicit gap-regularity hypotheses (published in *Monatshefte für Mathematik*, DOI: https://doi.org/10.1007/s00605-026-02211-4). Helm's *On the Distribution of B3-Sequences* (1996, DOI: https://doi.org/10.1006/jnth.1996.0069) rules out the regular asymptotic law $A(N)\sim\alpha N^{1/3}$. These are **external established conditional results**, not achievements of the present note. Their existence reinforces the need to control genuinely irregular multiscale reconfigurations rather than presuppose smooth growth.

## 4. An explicit reason not to infer the conjecture

Every finite B3 prefix can be extended indefinitely by adjoining sufficiently rapidly growing new elements: choose each y_j>4 max P_j. Theorem B proves that such a resulting infinite B3 set incurs a **strictly growing cubic reciprocal distance tax at each stage**, even as its normalized counting density has arbitrarily deep valleys. Thus 'indefinitely extendible' by itself does not demand positive normalized density. Conversely the exact distance-tax lower bound does not eliminate a hypothetical positive critical lower density.

A proof of Erdős #41 therefore requires an additional quantitative **cost-to-capacity gap** that forces the occupied distance spectrum or a stronger reciprocal resource to grow faster than its expanding ambient range. Any claim that the positive stage tax *alone* settles the problem would be false. Public status: https://www.erdosproblems.com/41 (OPEN).

**Next precise objective:** using the new exact distance bands B1 and B2 as uniquely owned witnesses, prove that in every c-persistent B3 history they conflict with the future occupied batches in a way that consumes more than the available O(R) pair-difference resource, or establish a mutually incompatible cross-scale collection of signed-code constraints that forces the future batch cardinality below eta_c R^(1/3). No such general result is proved here.

GCL research issue #2622; bounded note for independent specialist review.
