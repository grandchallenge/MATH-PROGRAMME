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
