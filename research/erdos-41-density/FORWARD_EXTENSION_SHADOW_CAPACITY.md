# Erdős #41 — forward extension capacity through the cubic-shadow tax

**17 October 2026. Research status:** exact finite and conditional persistent-density theorems PROVED below; the universal true-batch extension loss and Erdős #41 remain OPEN. This work prioritizes future extension capacity over residue-complexity hypotheses.

## 1. Distinguish actual capacity from singleton availability

For a finite repeated-summand B3 set P and a future integer interval J disjoint from P, let

$$
C(P,J)=\max\{|X|:X\subseteq J,\ P\cup X\text{ is }B_3\}.
$$

Let S(P,J) count the integers z in J such that P union {z} is B3. Both C and S are nonincreasing when a legitimate new block is added to P outside J. Their decrements telescope for any nested prefix chain with fixed J. **A decrease in S does not, by itself, imply any decrease in C.**

## 2. Exact cubic-shadow and mixed-shadow theorem

For any finite B3 X of size ell>=1, set T(X)=X+X-X with the two positive terms an unordered pair allowing repetitions. Then

$$
\boxed{|T(X)|=f(\ell)=\frac{\ell^3-\ell^2+2\ell}{2}.}\tag{SHADOW}
$$

**Proof.** All elements of X occur. For each c in X and each unordered pair a<=b from X excluding c, the number a+b-c is outside X by B2. It is distinct from all other such nontrivial representations by the B3 equality a+b+c'=a'+b'+c: as c is excluded from a,b and c' from a',b', equality of unordered triples forces c=c' and {a,b}={a',b'}. The count is ell+ell*binom(ell,2), as displayed.

For disjoint nonempty P,Y inside one genuine B3 carrier let n=|P|, m=|Y| and define

$$
H(P,Y)=\{y+y'-p:y,y'\in Y,\ y\le y',\ p\in P\}.
$$

**Theorem A:**

$$
\boxed{|H(P,Y)|=n\binom{m+1}{2}.}\tag{FORWARD-TAX}
$$

Proof: equality y+y'-p=z+z'-p' gives the two triple sums y+y'+p'=z+z'+p. B3 and the separation of P,Y force p=p' and identical unordered Y-pairs. Every h in H outside P union Y is forbidden as a new B3 member because h+p=y+y' violates B2.

If a third nonempty block X is disjoint from P,Y and P union Y union X is B3, then

$$
\boxed{H(P,Y)\cap T(X)=\varnothing.}\tag{MIXED-SHADOW-DISJOINTNESS}
$$

Indeed y+y'-p=x+x'-x'' would give a collision y+y'+x''=x+x'+p; the left has two Y and one X members, the right two X and one P, so the unordered triples cannot be the same.

## 2A. The right potential: exact remaining future *shadow capacity*

The previously defined true batch capacity C(P,J) is difficult to compute directly. A **canonical monotone upper-budget potential** nevertheless exists without choosing a residue modulus or assuming mixing.

For a nonempty integer interval J=[j0,j1] of diameter L, define its entire affine-shadow arena

$
K(J)=[2j_0-j_1,\ 2j_1-j_0]\cap\mathbb Z
\quad\text{with }|K(J)|=3L+1.
$

For a B3 prefix P disjoint from J, set

$
\boxed{
\Phi(P;J)=|K(J)\setminus T(P)|
=(3L+1)-|T(P)\cap K(J)|.
}\tag{EXACT-SHADOW-POTENTIAL}
$

**Theorem A2 (monotone extension potential, full strength).**

1. Every actual B3 extension X subset J of P satisfies

$
\boxed{f(|X|)\le\Phi(P;J),\quad C(P,J)\le F(\Phi(P;J)).}\tag{SHADOW-ENVELOPE}
$

2. For any B3 prefix chain P_0 subset P_1 subset ... subset P_r with all prefixes disjoint from the **same** J,

$
\boxed{
\Phi(P_0;J)-\Phi(P_r;J)
=\sum_{i=1}^r
|(T(P_i)\setminus T(P_{i-1}))\cap K(J)|.
}\tag{EXACT-TELESCOPING}
$

Each new shadow position has exactly one owner, its **first** prefix appearance. Thus the tax is genuinely monotone, nonnegative, and neither duplicated across prefix stages nor dependent on an arbitrary block partition.

**Proof.** For disjoint P,X with P union X B3, T(P) and T(X) cannot intersect: an equality a+b-c=x+y-z would give a+b+z=x+y+c, with two P and one X points on the left, and two X and one P points on the right, contradicting B3. Since T(X) is wholly within K(J) and has f(|X|) points, all its values are in K(J)\T(P), proving (1). Part (2) follows from the nestedness of T(P_i): the successive new shadow differences are disjoint and their union is T(P_r)\T(P_0). QED.

**Forward-shadow strengthening.** Under the geometry of the next section, the exact mixed shadow H(P,Y) lies in K(J) but is disjoint from T(P) (otherwise y+y'-p=a+b-c yields a forbidden B3 triple equality with two Y elements versus none). Hence

$
\boxed{
\Phi(P;J)-\Phi(P\cup Y;J)
\ge|H(P,Y)|=n\binom{m+1}{2}.
}\tag{POTENTIAL-TAX}
$

This is a **real lower bound on a bona fide monotone future-extension potential**, not merely an improvement obtained by comparing two unrelated upper bounds. The potential also controls **every** joint future B3 batch, via (SHADOW-ENVELOPE). It still does not imply an actual decrease in C(P,J), since the upper bound F(Phi) may be slack.

## 3. A genuine future charge and a bound on true batch capacity

Suppose P subset [1,R], and Y subset [a,b], for integer endpoints a>2R and b<2a-R, with P union Y genuinely B3. Put p_min=min P and

$$
\boxed{
J=[2a-R,\ 2b-p_{\min}]\cap\mathbb Z,\qquad
L=2(b-a)+R-p_{\min}.
}\tag{FUTURE-WINDOW}
$$

The mixed shadow H(P,Y) is contained in J. Moreover J starts after 3R, and it starts after b. **Every z in J is individually admissible before Y:** any three-term sum of P is <=3R; the sums with one z, two z, or three z are internally unique and lie in successive disjoint ranges once z>3R.

For the new prefix P'=P union Y (or the entire actual chronological B3 prefix up to b), the actual singleton tax therefore satisfies

$$
\boxed{
S(P,J)=|J|,\quad
S(P,J)-S(P',J)\ge n\binom{m+1}{2}.
}\tag{SINGLETON-CONSUMPTION}
$$

**Theorem B (future batch shadow-capacity envelope).** Every X subset J for which P' union X is B3, with ell=|X|, satisfies

$$
\boxed{
f(\ell)+n\binom{m+1}{2}\le3L+1.
}\tag{BATCH-SHADOW-CAPACITY}
$$

**Proof.** If J=[j0,j1], its affine shadow T(X) is contained in [2j0-j1,2j1-j0], a common interval of exactly 3L+1 integers. H(P,Y) is contained in J and therefore in the same larger interval. Those two exact cardinality shadows are disjoint by Theorem A. Count their occupied integer positions. QED.

Define F(B)=max{ell>=0:f(ell)<=B}, taking f(0)=0. Thus the TRUE maximum batch capacity obeys

$$
\boxed{
C(P',J)\le F\left(3L+1-n\binom{m+1}{2}\right).
}\tag{BATCH-UPPER-BOUND}
$$

This is strictly stronger than the ordinary cubic-shadow upper *envelope* F(3L+1) at the real-valued volume level; the integer-valued ceilings may coincide for small windows. The lost budget is exactly n*binom(m+1,2) occupied future shadow positions, not necessarily the numerical decrement of C.

An exact conditional certified lower bound on the actual capacity decrement is

$$
\boxed{
C(P,J)-C(P',J)\ge
\left[
C(P,J)-F\left(3L+1-n\binom{m+1}{2}\right)
\right]_+.
}\tag{IF-NEAR-CAPACITY}
$$

The right-hand side can vanish when C(P,J) is far below its ordinary shadow envelope. This failure cannot be suppressed: see the finite hostile example.

## 3A. A second, nonredundant tax: blocked translations of any fixed future shape

The forward shadow imposes a quantified restriction on **where a proposed future batch shape can be placed**, even without measuring its optimum cardinality. Let X_0 be any nonempty finite B3 *template*, of ell points, and let t range over all integer translations for which X_0+t would be disjoint from P union Y. Its centered shadow translates exactly:

$$
T(X_0+t)=T(X_0)+t.
$$

Whenever t belongs to the integer difference set H(P,Y)-T(X_0), one of the forbidden early/middle shadow positions coincides with a shadow of X_0+t. If X_0+t is disjoint from P union Y, the full union **cannot** be B3. If it overlaps P or Y, the translate is already inadmissible as a *disjoint future extension*; the shadow collision alone is not claimed to prove that the set-theoretic union fails B3.

**Theorem B2 (fixed-shape extension-placement tax).** There are at least

$$
\boxed{
|H(P,Y)-T(X_0)|
\ge |H(P,Y)|+|T(X_0)|-1
=n\binom{m+1}{2}+f(\ell)-1
}\tag{BLOCKED-TRANSLATIONS}
$$

different integer shifts prohibited by this particular shadow collision. The second inequality is the elementary sumset inequality |E-F|>=|E|+|F|-1 for finite nonempty integer sets: ordering their elements constructs |E|+|F|-1 distinct extreme differences.

For a template X_0 supported in an interval of diameter d, the entire set of these excluded shifts lies inside an interval of length at most L+3d+1, because H subset J has span at most L and T(X_0) has span at most 3d. Hence in that **full translation arena**, at least the fraction

$$
\boxed{
\frac{n\binom{m+1}{2}+f(\ell)-1}{L+3d+1}
}\tag{TRANSLATION-FRACTION}
$$

of shifts are blocked by forward-shadow competition. At critical-scale n,m,ell of order R^(1/3), with L,d=O(R), this can be a fixed positive fraction of the possible translates.

**Important limitation:** some shifts in the full arena may not place X_0 wholly into the predetermined future interval J; the fraction is a property of the full translate-support arena, **not** a lower bound on blocked admissible placements *inside J*. Different prospective future B3 batches may change shape, so this fixed-template exclusion does not imply a decrease in the optimum true capacity C(P,J). This theorem captures a rigorously quantified entropy tax, not the still-open universal batch tax.

## 4. Conditional persistent density: O(R) forced future tax at every large scale

Assume HYPOTHETICALLY an infinite B3 set A obeys A(N)>=c N^(1/3) for all sufficiently large N, where 0<c<=1. The ordinary three-sum bound gives A(t)^3<=18t.

Fix the integer constants

$$
\Lambda=\lceil(16/c)^3\rceil,\qquad
K=\left\lceil\log_{3/2}(\Lambda/3)\right\rceil.
$$

At every sufficiently large integer R, the earlier actual prefix P=A intersect [1,R] contains n>=c R^(1/3) elements. The middle annulus satisfies

$$
|A\cap(3R,\Lambda R]|
\ge c(\Lambda R)^{1/3}-(54R)^{1/3}
>12R^{1/3}.
$$

Partition that annulus into K consecutive geometric bins of ratio at most 3/2, truncated at Lambda R. One bin contains a selected Y of m>=12R^(1/3)/K points. Write a=min Y and b=max Y. Since the bin lies above 3R and its upper endpoint is at most 3/2 times its lower endpoint, a>3R and b<3a/2<2a-R. Thus J from (FUTURE-WINDOW) is after b, all its sites are individually admissible to P, and the entire true chronological prefix P'=A intersect [1,b] blocks at least the mixed shadow H(P,Y).

**Theorem C (density-forced forward consumption):** at EVERY sufficiently large R,

$$
\boxed{
S(P,J)-S(P',J)
\ge n\binom{m+1}{2}
\ge\frac{72c}{K^2}R.
}\tag{DENSITY-FORCED-SINGLETON-TAX}
$$

Since L=2(b-a)+R-p_min<=(Lambda+1)R, set

$$
\delta_c=\frac{18c}{K^2(\Lambda+1)}>0.
$$

Then the true future batch capacity satisfies the explicit STRONGER-THAN-STANDARD upper bound

$$
\boxed{
C(P',J)\le F\bigl((1-\delta_c)(3L+1)\bigr).
}\tag{DENSITY-FORCED-ENVELOPE}
$$

The charged future shadow positions form a positive c-dependent fraction of the full 3L+1 cubic-shadow arena. Because f(ell)~ell^3/2, this is a strict c-dependent reduction in the ordinary asymptotic critical-size **upper envelope**, of ratio at most (1-delta_c)^(1/3).

**The capacity-envelope loss is genuinely of critical order, not merely nonzero.** The shadow formula gives f(n)>=n^3/4 for every integer n>=1. Since T(P) fits into an interval of 3 diam(P)+1 positions, 3L+1>=3 diam(P)+1>=n^3/4>=c^3 R/4. Hence L grows proportionally to R in this construction. As B tends to infinity, the explicitly invertible cubic satisfies F(B)=(2B)^(1/3)+O(1). Therefore

$$
\boxed{
F(3L+1)-F((1-\delta_c)(3L+1))
=\bigl[1-(1-\delta_c)^{1/3}\bigr](2(3L+1))^{1/3}+O(1)
=\Omega_c(R^{1/3}).
}\tag{CRITICAL-ENVELOPE-TAX}
$$

This lower-bounds the decrease of the **universal cubic-shadow capacity ceiling**, not the difference of the actual maxima C(P,J)-C(P',J). The independent finite no-batch-tax example shows why the distinction cannot be dropped.

No modular residues or Fourier mixing were assumed. **However this still does not assert that C(P,J)-C(P',J)>0, or that normalized counting density decays across scales.** The ordinary and improved budgets are both order R, and even a linear site loss can coexist with no decrease in maximum future batch size.

## 5. Independently verifiable hostile and positive finite controls

Let P={1,2,5}, Y={14}; P union Y is a genuine repeated-summand B3 set and H(P,Y)={23,26,27}.

**Hostile to the false bridge singleton loss => batch-capacity loss.** On J=[25,33] two initially admissible singleton positions (26,27) become forbidden. Exact enumeration over every future subset nevertheless gives

$$
\boxed{
C(P,[25,33])=1=C(P\cup Y,[25,33]).
}\tag{NO-BATCH-DECREMENT}
$$

One optimal old extension is {25}; one optimal new extension is {33}. A positive singleton tax cannot be promoted to a universal numerical tax on C.

**Positive actual batch-capacity tax at canonical window.** Taking R=5 and a=b=14 gives J=[23,27]. Exact enumeration gives

$$
\boxed{
C(P,[23,27])=1,\qquad
C(P\cup Y,[23,27])=0.
}\tag{POSITIVE-BATCH-DECREMENT}
$$

Here the exact forward shadow tax is 3 of 5 future sites, and the BATCH-SHADOW-CAPACITY bound is verified for every admissible future subset.

For larger geometrically separated genuine B3 blocks, tests verify shadow cardinalities, nonoverlap, the cubic future budget, and the ability of added early/middle elements to forbid linearly many future singleton positions. Scaling finite examples does not establish a fixed positive infinite density.

## 6. The sharply isolated remaining lemma

**Unproved bridge:** show that a hypothetical c-persistent B3 chain repeatedly approaches its available future *batch* capacity closely enough that the proved cubic-shadow budget charges force a decreasing scale-normalized potential. One possible precise sufficient statement is an asymptotic lower bound on C(P,J) near F(3L+1) for appropriately selected windows, or a new full-hypergraph dual certificate that controls how the optimal future batch re-routes around blocked shadow sites.

This is the mathematically consequential difference from the old modular inverse programme: we HAVE proved a positive density-sensitive forward shadow consumption theorem, but we have NOT proved that the consumption is forced to accumulate against true critical-density extensions. New work must address that bridge, not restate the singleton tax or sum geometric windows as if they share one global capacity budget.

The exact finite-window base-eight valley criterion remains the final target; Erdős #41 is OPEN (https://www.erdosproblems.com/41). The result is bounded GCL research and not externally certified novelty.
