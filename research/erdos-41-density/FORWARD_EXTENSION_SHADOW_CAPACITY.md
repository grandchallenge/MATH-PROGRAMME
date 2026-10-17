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

$$
K(J)=[2j_0-j_1,\ 2j_1-j_0]\cap\mathbb Z
\quad\text{with }|K(J)|=3L+1.
$$

For a B3 prefix P disjoint from J, set

$$
\boxed{
\Phi(P;J)=|K(J)\setminus T(P)|
=(3L+1)-|T(P)\cap K(J)|.
}\tag{EXACT-SHADOW-POTENTIAL}
$$

**Theorem A2 (monotone extension potential, full strength).**

1. Every actual B3 extension X subset J of P satisfies

$$
\boxed{f(|X|)\le\Phi(P;J),\quad C(P,J)\le F(\Phi(P;J)).}\tag{SHADOW-ENVELOPE}
$$

2. For any B3 prefix chain P_0 subset P_1 subset ... subset P_r with all prefixes disjoint from the **same** J,

$$
\boxed{
\Phi(P_0;J)-\Phi(P_r;J)
=\sum_{i=1}^r
|(T(P_i)\setminus T(P_{i-1}))\cap K(J)|.
}\tag{EXACT-TELESCOPING}
$$

Each new shadow position has exactly one owner, its **first** prefix appearance. Thus the tax is genuinely monotone, nonnegative, and neither duplicated across prefix stages nor dependent on an arbitrary block partition.

**Proof.** For disjoint P,X with P union X B3, T(P) and T(X) cannot intersect: an equality a+b-c=x+y-z would give a+b+z=x+y+c, with two P and one X points on the left, and two X and one P points on the right, contradicting B3. Since T(X) is wholly within K(J) and has f(|X|) points, all its values are in K(J)\T(P), proving (1). Part (2) follows from the nestedness of T(P_i): the successive new shadow differences are disjoint and their union is T(P_r)\T(P_0). QED.

**Forward-shadow strengthening.** Under the geometry of the next section, the exact mixed shadow H(P,Y) lies in K(J) but is disjoint from T(P) (otherwise y+y'-p=a+b-c yields a forbidden B3 triple equality with two Y elements versus none). Hence

$$
\boxed{
\Phi(P;J)-\Phi(P\cup Y;J)
\ge|H(P,Y)|=n\binom{m+1}{2}.
}\tag{POTENTIAL-TAX}
$$

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

## 3B. Stronger one-anchor theorem: a cubic singleton loss needs no dense middle block

The mixed shadow H(P,Y) is a **batch-shadow** obstruction. A stronger *singleton* obstruction arises from the reflected **internal** cubic shadow of the early prefix. Crucially, it requires only **one** new later B3 element, not a dense later block.

Let P be a finite B3 set of n>=1 elements contained in [1,R], with p_min=min P, p_max=max P. Define its internal shadow

$$
I(P)=T(P)\cap[p_{\min},p_{\max}].
$$

**Theorem D (internal cubic shadow):**

$$
\boxed{|I(P)|\ge n+\binom n3.}\tag{INTERNAL-CUBIC}
$$

**Proof.** All n elements of P belong to I(P). For each **distinct** ordered triple a<b<c of P, the signed sum a+c-b lies strictly between a and c and hence in [p_min,p_max]. It cannot belong to P, for then a+c=b+z is a forbidden nontrivial two-term sum collision. These binom(n,3) signed sums are mutually distinct: they are nontrivial affine-shadow values of P, whose representations are unique by B3 (see section 2). Therefore the stated count holds.

Now choose just **one** new anchor y>2R with P union {y} still B3. Define

$$
\boxed{J_y=[2y-R,\ 2y-p_{\min}]\cap\mathbb Z.}\tag{ONE-ANCHOR-WINDOW}
$$

**Theorem E (uniform cubic single-anchor tax):**

$$
\boxed{
S(P,J_y)=|J_y|,\qquad
S(P,J_y)-S(P\cup\{y\},J_y)
\ge |I(P)|\ge n+\binom n3.
}\tag{CUBIC-SINGLETON-TAX}
$$

**Proof.** Every z in J_y exceeds 3R (because y>2R), so adjoining z to P preserves B3 by separation of the three possible multiplicities of z in triple sums. For every t=a+b-c in I(P), the reflected future integer z=2y-t belongs to J_y, is greater than y, and satisfies the forbidden equality

$$
z+a+b=2y+c.
$$

The left triple contains one future z and two earlier P members, whereas the right triple contains two copies of y and one earlier P member; they cannot be the same unordered triple. Thus all the distinct reflected I(P) values are newly forbidden singleton sites. QED.

**Density-sensitive corollary without annular pigeonhole.** If the hypothetical persistent B3 lower bound A(R)>=cR^(1/3) holds for all large R, take P=A intersect [1,R] and ANY actual later anchor y in A with y>2R. For n=|P|>=6 one has binom(n,3)>=n³/12. Hence for all sufficiently large R,

$$
\boxed{
S(P,J_y)-S(P\cup\{y\},J_y)
\ge\frac{c^3}{12}R,
\qquad
\frac{S(P,J_y)-S(P\cup\{y\},J_y)}{|J_y|}
\ge\frac{c^3}{12}.
}\tag{ONE-ANCHOR-DENSITY-TAX}
$$

The entire future interval has |J_y|=R-p_min+1<=R. No density of the chosen middle anchor is needed. It is always possible to select an actual later anchor in an infinite A, and it can be chosen at distance O_c(R) using the same standard prefix counting bounds as section 4.

**A rigorous entropy bound on future candidate batches.** Let N_ell(P',J) count the true ell-element B3 extensions X subset J of prefix P'. Since every X after adjoining y must avoid the B=|I(P)| newly forbidden sites,

$$
\boxed{
N_{\ell}(P\cup\{y\},J_y)
\le\binom{|J_y|-B}{\ell}
\le e^{-B\ell/|J_y|}\binom{|J_y|}{\ell}.
}\tag{RAW-EXTENSION-ENTROPY}
$$

Under persistent density, a prospective future batch of ell>=eta R^(1/3) has a suppression factor at most exp(-c³ eta R^(1/3)/12) **relative to all raw ell-subsets**, not relative to the already much smaller collection of B3-compatible completions for P. The inequality is exact and follows by the product formula for binomial coefficients.

**A robust within-window translation obstruction, not merely a full-arena claim.** Take an arbitrary finite B3 template X0 of diameter d, translated so min X0=0. Among all integer shifts t for which X0+t subset J_y (a range of |J_y|-d shifts), at least

$$
\boxed{\bigl[|I(P)|-d\bigr]_+}\tag{INTERIOR-TRANSLATION-TAX}
$$

are forbidden by the reflected internal shadow alone: each blocked future singleton site z=2y-h not in the last d positions of J_y is an eligible shift t=z, since 0 belongs to X0. In particular if d<=|I(P)|/2, at least |I(P)|/2 **genuinely eligible placements** of every fixed future template are lost. These are placements, not independent future batches; a shape-changing optimizer can still evade them.

**Critical limitation (proved by the next hostile example):** Even an overwhelming cubic loss of legal singleton sites and exponentially fewer raw ell-subsets does **not** imply a strict loss of the *true* optimal future batch size C(P,J). The missing bridge remains a constraint on every rerouted complete batch, not just on its possible locations.

### An exact counterexample in the canonical one-anchor window

Let

$$
P=\{1,2,5,14\},\quad R=14,\quad y=34,\quad J_y=[54,67].
$$

P union {y} is genuinely B3. Exact enumeration gives

$$
\boxed{
|I(P)|=12,\quad |J_y|=14,\quad
S(P,J_y)=14,\quad
S(P\cup\{34\},J_y)=1,
}\tag{CUBIC-HOSTILE}
$$

so **13 of 14** individually legal sites disappear (12 already certified by the internal shadow). Nevertheless the true complete-B3 batch capacities are

$$
\boxed{
C(P,J_y)=1=C(P\cup\{34\},J_y).
}\tag{CANONICAL-NO-BATCH-LOSS}
$$

Thus no universal lemma can equate a large *fractional* loss of legal singleton positions with a positive *numerical* decline in true batch capacity, even for the canonical interval after a valid B3 one-anchor extension. This test directly refutes a natural but false proposed bridge. It is not a counterexample to the infinite Erdős problem.

## 3C. Exact reoptimization model: reflect the future batch back into the old prefix interval

The remaining bridge concerns actual **optimal batches**, not individual future sites. A sufficiently distant one-anchor future window admits a surprisingly small and exact reformulation as a **two-colour signed-sum packing problem entirely inside the original scale**.

Let P subset [1,R] be a finite repeated-summand B3 set, let y>6R, and define the canonical J_y=[2y-R,2y-p_min]. Every X subset J_y corresponds bijectively to a reflected finite set

$$
\boxed{T=\{2y-x:x\in X\}\subseteq[p_{\min},R].}\tag{REFLECT}
$$

For any two finite sets P,T define the two *coloured signed-word injectivity* properties

$$
\begin{aligned}
(\mathrm{PP-T}):&\quad
(a,b,t)\longmapsto a+b-t
&& (a,b\in P,\ a\le b,\ t\in T),\\
(\mathrm{P-TT}):&\quad
(p,t,u)\longmapsto p-t-u
&& (p\in P,\ t,u\in T,\ t\le u).
\end{aligned}
$$

Here "injective" means no two **different** displayed unordered-positive word labels yield equal integers. It does not demand that either image avoid the other, because they are *different digit levels* in the original unanchored B3 problem.

**Theorem F (complete, exact reflected capacity characterization).** For y>6R and X=2y−T,

$$
\boxed{
P\cup X\text{ is }B_3
\Longleftrightarrow
\begin{cases}
T\text{ is }B_3,\\
\mathrm{PP-T}\text{ is injective},\\
\mathrm{P-TT}\text{ is injective}.
\end{cases}
}\tag{UNANCHORED-REFLECTION}
$$

Furthermore,

$$
\boxed{
P\cup\{y\}\cup X\text{ is }B_3
\Longleftrightarrow
\begin{cases}
T\text{ is }B_3,\\
\mathrm{PP-T}\text{ and }\mathrm{P-TT}\text{ are injective},\\
T\cap T(P)=\varnothing,\\
P\cap T(T)=\varnothing.
\end{cases}
}\tag{ANCHORED-REFLECTION}
$$

All statements include repeated summands. Here T(P)=P+P−P and T(T)=T+T−T are full cubic shadows, not their internal restrictions.

**Proof.** Distinguish each selected value in P (digit level 0), the anchor y (level 1), and each future x=2y−t (level 2). In a three-term sum, the total digit level k lies in {0,...,6}, and the remaining offset is bounded in absolute value by 3R. As y>6R, sums from distinct levels cannot collide. Without the anchor the only available levels are 0,2,4,6. Their offsets are respectively sums PPP, values PP−T, values P−TT, and negatives of unordered triple sums TTT. Triple-sum uniqueness is therefore equivalent to the displayed three conditions.

With the anchor, odd levels appear: level 1 gives ordinary unordered pair sums PP (unique by B3), level 3 gives offset 0 (yyy) and the differences P−T (y+x+p), and level 5 gives negatives of unordered pair sums TT (unique by T B3). Injectivity of P−T follows from PP−T injectivity by fixing any p0∈P and comparing p+p0−t; 0 is excluded exactly when T∩P is empty. That follows from T∩T(P)=empty since P subset T(P).

At level 2 there is additionally the type yy+p, offset p. It cannot collide with PP−T precisely when P∩(P+P−T)=empty, equivalently T∩T(P)=empty. At level 4 there is additionally yy+x, offset −t. It cannot collide with P−TT precisely when (−T)∩(P−T−T)=empty, equivalently P∩T(T)=empty. Every other within-level uniqueness condition was already included. This proves both directions. QED.

**Exact consequence for the true maximum capacities, independent of y once y>6R:**

$$
\boxed{
\begin{aligned}
C(P,J_y)&=\max_{T\subseteq[p_{\min},R]}
\{|T|:T\text{ satisfies UNANCHORED-REFLECTION}\},\\
C(P\cup\{y\},J_y)&=\max_{T\subseteq[p_{\min},R]}
\{|T|:T\text{ satisfies ANCHORED-REFLECTION}\}.
\end{aligned}
}\tag{REFLECTED-TRUE-CAPACITY}
$$

The reoptimization loophole is now *completely specified*: future batches can change their reflected shape T to evade both mutual cubic-shadow exclusions. Merely deleting many eligible t values in T(P) does not control the maximum T that also satisfies the two signed-word injectivity conditions and reciprocal shadow avoidance. This reframes the remaining proof obstacle without residue assumptions and without any appeal to generic pseudorandom mixing.

The two reciprocal exclusions are independently meaningful. The first is the strong cubic singleton tax already proved; the second is a genuinely **batch-dependent** obstruction that can only be seen after selecting the full reflected T, namely P∩T(T)=empty. This identifies a precise next gate: show that for critically dense P no T of the required critical size can satisfy *both* signed-word injectivities and the two reciprocal shadow exclusions across a sustained chain of scales.

**Hostile control, even in the exact reflected setting.** With P={1,2,5,14}, R=14 and y=100, J_y=[186,199]. The anchored and unanchored true capacities both equal 1, despite more than half the future singleton positions being removed. Hence even the exact reciprocal-shadow characterization does not automatically yield a positive single-step batch decrement.

## 3D. Three successive colours: an exact seven-layer survival theorem

The one-anchor signed-code theorem extends to an **entire middle cohort**, and the resulting constraints bind the size of any reoptimized future batch without fixing its shape.

Let R be a positive integer. Let P and T be subsets of [0,R] and D subset [0,R]. Write n=|P|, m=|D|, ell=|T|. For a sufficiently separated integer y>6R consider the *physical* set

$$
\boxed{\mathcal A=P\ \cup\ (y+D)\ \cup\ (2y-T).}\tag{THREE-COLOUR}
$$

The three sets are disjoint. The middle offsets D need not be nonnegative original A-elements; the formulation allows any translated actual middle cohort in a short interval, as long as the displayed offset windows have width at most R.

Every unordered triple from mathcal A has a uniquely defined **digit level** in {0,1,...,6}, the sum of its three block levels 0,1,2. Its remaining integer offset lies in the following exact word families. Within each family the positive repeated pair is unordered and all multiplicities are retained.

| Digit level | Required offset word families |
| --- | --- |
| 0 | PPP |
| 1 | PP+D |
| 2 | P+D+D **and** P+P−T |
| 3 | D+D+D **and** P+D−T |
| 4 | D+D−T **and** P−T−T |
| 5 | D−T−T |
| 6 | −T−T−T |

**Theorem G (seven-layer exact survival):** If y>6R, the physical union mathcal A is B3 **if and only if** within each of the seven displayed levels, **all** the offset words (including the two different word types at levels 2, 3, and 4) yield mutually distinct integers. No comparison is required between *different* levels.

**Proof.** All terms in P,D,T lie between 0 and R, so each three-term offset lies between −3R and 3R. Different digit levels produce sums differing by at least y−6R>0 and thus cannot collide. A collision of two distinct unordered physical triples with the same digit level is exactly an equality between two distinct offset words listed for that level. This includes repeated points, mixed blocks, and both cross-type comparisons. Thus uniqueness of all three-term sums is equivalent to injectivity within each level. QED.

This theorem includes the one-anchor reflected characterization as the special case D={0}. It also completely characterizes the compatibility of an **arbitrarily structured middle B3 cohort** with an optimally selected future reflected batch.

**Theorem H (shape-independent cardinality competition).** If mathcal A is B3 then

$$
\boxed{
\begin{aligned}
\binom{n+2}{3}&\le 3R+1,\\
m\binom{n+1}{2}&\le 3R+1,\\
n\binom{m+1}{2}+\ell\binom{n+1}{2}&\le 4R+1,\\
\binom{m+2}{3}+nm\ell&\le 4R+1,\\
\ell\binom{m+1}{2}+n\binom{\ell+1}{2}&\le 4R+1,\\
m\binom{\ell+1}{2}&\le 3R+1,\\
\binom{\ell+2}{3}&\le 3R+1.
\end{aligned}
}\tag{SEVEN-LAYER-PACKING}
$$

**Proof.** In each level count the number of distinct required unordered colour words; the counts are shown on the left. For levels 0,1,5,6 all offsets occupy an interval of at most 3R+1 integers. The union offset ranges at levels 2,3,4 occupy intervals of at most 4R+1 integers: respectively [−R,3R], [−R,3R], and [−2R,2R]. Exact injectivity from Theorem G forces the counts not to exceed the available integer positions. QED.

Theorem H gives a **fully batch-shape-independent** upper bound, for example

$$
\boxed{
\ell\le
\left\lfloor\frac{4R+1-\binom{m+2}{3}}{nm}\right\rfloor
\quad(nm>0).
}\tag{LEVEL-THREE-FUTURE-CAP}
$$

It also gives coupled quadratic bounds from the levels 2 and 4. These are stricter *joint cardinality restrictions* on a three-cohort extension than the ordinary separate cubic-shadow range count. In contrast with the single-anchor singleton loss, they cannot be evaded by rearranging future T without lowering its cardinality.

### Localized Hall refinement (proved; no distribution hypothesis)

The crude right sides 4R+1 can be reduced to the *actual geometric union* of the two competing word-type intervals. Let P,D,T have respective minimum and maximum values (p_-,p_+), (d_-,d_+), (t_-,t_+), with all three sets nonempty. Define

$$
\begin{aligned}
I_2^{(1)}&=[p_-+2d_-,\ p_++2d_+],&
I_2^{(2)}&=[2p_--t_+,\ 2p_+-t_-],\\
I_3^{(1)}&=[3d_-,\ 3d_+],&
I_3^{(2)}&=[p_-+d_--t_+,\ p_++d_+-t_-],\\
I_4^{(1)}&=[2d_--t_+,\ 2d_+-t_-],&
I_4^{(2)}&=[p_--2t_+,\ p_+-2t_-].
\end{aligned}
$$

Every admissible reflected three-cohort extension satisfies

$$
\boxed{
\begin{aligned}
n\binom{m+1}{2}+\ell\binom{n+1}{2}
&\le|I_2^{(1)}\cup I_2^{(2)}|,\\
\binom{m+2}{3}+nm\ell
&\le|I_3^{(1)}\cup I_3^{(2)}|,\\
\ell\binom{m+1}{2}+n\binom{\ell+1}{2}
&\le|I_4^{(1)}\cup I_4^{(2)}|.
\end{aligned}
}\tag{LOCALIZED-THREE-COLOUR-HALL}
$$

The proof is direct: distinct triple sums in the same level must fit into the union of the **two actual** integer ranges they occupy. The constraints become stronger when one cohort is narrowly located, and they retain their force even if every actual future batch changes shape.

**Critical limitation about real persistent density.** To use these bounds with n,m,ell all of order R^(1/3), one must first prove that actual hypothetical c-persistent B3 sets provide **three appropriately located and sufficiently populated cohorts simultaneously**. A lower counting bound A(N)>=cN^(1/3) at all large N guarantees density in suitably chosen annuli, but not arbitrary prescribed triplets of short windows at positions y and 2y. It would be invalid to assert such localization without an additional extraction theorem.

**Precise limitation.** In the critical regime n,m,ell all proportional to R^(1/3), every term in (SEVEN-LAYER-PACKING) is order R. With a sufficiently small hypothetical density coefficient c, all seven inequalities can have slack. No fixed collection of these inequalities forces a contradiction for **every** c>0, and there is no independently proved recurrence showing their costs become superlinear over growing numbers of scale-owned cohorts. Therefore Theorems G and H are a genuine finite-batch step towards the multiscale obligation, **not** its completion.

**Next exact mathematical gate:** For a c-persistent B3 set, select a family of overlapping consecutive three-cohort windows at growing scales in which the *same actual elements* appear with consistent digit-level roles, then prove a comparison of the unused capacities in levels 2–4 that cannot be discharged by adjusting T. Such an inequality must count each actual sum once at its first owning window; simply repeating (SEVEN-LAYER-PACKING) over many windows cannot make the slack accumulate.

## 3E. The exact surviving-site graph and its reciprocal difference condition

The complete reflected theorem has a compact formulation that **does** account for shape-changing optimizers, rather than merely deleting a fraction of future singletons.

Let P be a finite B3 set in [1,R], y>6R, and

$$
Q_P=\{p+p':p,p'\in P,\ p\le p'\},\quad
V_P=([p_{\min},R]\cap\mathbb Z)\setminus T(P).
$$

On the vertex set V_P, define the **complete pair-sum difference graph** G_P, joining distinct t,u precisely when

$$
t-u\in Q_P-Q_P.
$$

Differences are understood with both orientations, so the edge definition is symmetric. Let Q_T be the unordered pair-sum set of a proposed T and let $\Delta_P=P-P$, $\Delta_{Q_P}=Q_P-Q_P$.

**Theorem I (exact survivor graph + dual packing characterization).** The individual reflected sites admissible after adding y are **exactly** V_P. Moreover the true future optimal batch capacity is

$$
\boxed{
C(P\cup\{y\},J_y)
=
\max\{|T|:\ T\subseteq V_P,\quad
T\text{ is }B_3,\quad
(T-T)\cap\Delta_{Q_P}=\{0\},\quad
(Q_T-Q_T)\cap\Delta_P=\{0\},\quad
P\cap T(T)=\varnothing
\}.
}\tag{DUAL-SIGNED-CODE}
$$

Consequently the completely **shape-independent** graph bound is

$$
\boxed{
C(P\cup\{y\},J_y)\le\alpha(G_P[V_P]).
}\tag{SURVIVOR-INDEPENDENCE}
$$

**Proof.** Theorem F says a reflected T is admissible with the anchor iff T is B3, T∩T(P)=empty, P∩T(T)=empty, and the PP−T and P−TT maps are injective.

The first shadow condition is exactly T subset V_P. Each nonzero collision of two PP−T words is an equality q−t=q'−u, equivalent to t−u=q−q' with t!=u, which is prohibited exactly by $(T-T)\cap(Q_P-Q_P)=\{0\}$; the internal uniqueness of q follows from B2. Similarly the P−TT map is injective precisely when the nonzero pair-sum differences from Q_T avoid the nonzero differences of P, namely $(Q_T-Q_T)\cap(P-P)=\{0\}$, because T is B2 and hence Q_T has distinct labelled unordered pair representations. If |T|=1, those maps are automatically injective and T(T)=T; since P subset T(P), each t∈V_P yields a legal singleton. This proves the claimed exact characterization and upper bound. QED.

**The remaining decisive graph problem is now different from the old Stage B one.** It is the independence number of the graph induced by the **surviving reflected singleton sites** after deleting the actual cubic shadow, with *all* differences of the unordered inner pair-sum set forbidden, and a **reciprocal** difference-spectrum condition for Q_T against P-P. The older forbidden-distance graph used only the doubled outer differences and did not impose this coupled, bidirectional signed-code packing problem.

**Concrete complete-batch decrement, without a near-saturation assumption.** Let P={1,2,5}, R=14, y=100, and D={0,11}. Both the old P and the intermediate genuine B3 prefix P union {100,111} are valid. The future reflected interval is J_y=[186,199]. Exact enumeration of **all** 2^14 reflected future sets yields

$$
\boxed{
C(P,J_y)=2,\qquad
C(P\cup\{100,111\},J_y)=1.
}\tag{REAL-MIDDLE-BATCH-TAX}
$$

For the new middle prefix, the reflected **singleton** survivors are precisely T={7,10,11,14}. Any two of these have a difference in Q_P−Q_P, so they form a **clique** in the old pair-sum difference graph. This gives a human-checkable certificate of the upper bound one without rerunning the complete three-sum search. At least one of these singleton T's remains admissible, proving equality. The old prefix admits, for example, T={1,10} as a two-element batch, showing the before-bound of two is achieved. The full two-colour constraints and the direct B3 enumeration confirm both optima.

**Limitation:** the example demonstrates a genuine *numerical* batch capacity loss caused by a populated middle cohort and the surviving-site graph. It does not show a positive capacity drop on **every** step (the earlier canonical counterexample shows the opposite), nor any uniform lower bound on the drop under infinite persistent density. At small critical density, V_P can remain a positive fraction of the old interval and its graph may have critical-order independent sets. The multiscale obstruction must bound the survival of these **coupled** signed-code independent sets across linked cohorts.

## 3F. A genuine many-cohort theorem: critical-density blocks cannot form arbitrarily long arithmetic runs

The seven-layer result is the three-cohort case of a stronger **multicoherence obstruction**. The following theorem rules out long translated runs of dense B3 blocks **independently of the separation between their centres**.

Let r>=4, R>=1, and q>=R be integers, and choose B large enough that all positions below are positive. Suppose a B3 set contains **2r+1 pairwise disjoint blocks**

$
A_i\subseteq[B+iq,\ B+iq+R-1]\quad(-r\le i\le r),
$

each containing at least m>=1 elements.

**Theorem J (arithmetic-run extension exhaustion).** With s=floor(r/2),

$
\boxed{
\binom{s}{2}m^3\le3R-2.
}\tag{ARITHMETIC-RUN}
$

In particular if m>=cR^(1/3), for a fixed c>0, then

$
\boxed{
\binom{\lfloor r/2\rfloor}{2}<\frac{3}{c^3},
\quad\text{hence}\quad r=O(c^{-3/2}).
}\tag{NO-LONG-DENSE-AP-RUN}
$

**Proof.** For each pair of indices 1<=i<j<=s, the third index k=−i−j lies in [−r,−3]. These are all **three distinct indices** and their sum is zero. Choose one actual B3 element from each of A_i,A_j,A_k; each pattern creates at least m³ distinct unordered three-element triples. Patterns for different i,j use different block-index multisets and cannot select the same element triple. All resulting sums belong to

$
[3B,\ 3B+3(R-1)]\cap\mathbb Z,
$

which contains 3R−2 integers, since iq+jq+kq=0. The original B3 property makes every selected triple sum distinct. Thus binom(s,2)m³<=3R−2. Under the fixed critical block coefficient c, substitute m³>=c³R and rearrange. QED.

The bound is **independent of q**. Choosing farther-apart block centres cannot relieve the collision pressure once their centres have the same additive relation. The theorem is a genuinely multiblock and density-sensitive obstruction: after O(c^(-3/2)) equally spaced, critically populated cohorts, extension is impossible.

**Essential limitation (no hidden density extraction).** Hypothetical persistent lower density A(N)>=cN^(1/3) does **not** imply the existence of 2r+1 populated, nearly equally spaced, short blocks of critical **local** density. Concentrating points into geometrically separated islands may satisfy cardinal lower bounds while avoiding these particular centre configurations; whether the full B3 property prohibits that avoidance is exactly the open arithmetic alignment/inverse question. Theorem J solves the aligned-run case, **not** the general Erdős #41 case.

**A stronger exact coarse-bin formulation.** For a partition into integer blocks I_i=[iR,(i+1)R−1] and occupancies m_i, define for each index-sum s the number of actual unordered three-element selections of each bin-index pattern:

$
w(i,j,k)=
\begin{cases}
m_im_jm_k,&i<j<k,\\
\binom{m_i+1}{2}m_k,&i=j<k,\\
m_i\binom{m_j+1}{2},&i<j=k,\\
\binom{m_i+2}{3},&i=j=k.
\end{cases}
$

Then the full B3 property implies the exact **multiwindow sum-capacity inequality**

$
\boxed{
\sum_{\substack{i\le j\le k\\i+j+k=s}}w(i,j,k)\le3R-2
\qquad\text{for every integer }s.
}\tag{COARSE-TRIPLE-CAPACITY}
$

Each selected actual triple has one unique unordered bin-index pattern and its sum belongs to the integer interval [sR,sR+3R−3]. Therefore the bound has neither multiplicity omissions nor double-counting across index patterns. This controls **any** family of equal-width bins, not only an aligned arithmetic run, though the set of coarse capacity inequalities is not by itself known to imply a critical-density dip.

### A decisive negative test for count-only multiscale packing

The exact coarse index-sum inequalities are **still not enough**, by themselves, to force the finite-window density dip. The following theorem gives explicit critical-density *integer occupancy profiles* meeting **all** of them at arbitrarily many coarse checkpoints. These are **not asserted to be realizable by any B3 set**.

For an arbitrary integer M>=1, put

$
L=(20M)^3,\qquad
m_i=\left\lfloor\frac{4M}{(i+1)^{2/3}}\right\rfloor
\quad(0\le i<M).
$

**Theorem K (sharp limitation of scalar multiscale Hall capacity).**

1. At **every** coarse prefix length 1<=h<=M, the vector has critical lower density:

$
\boxed{
\sum_{i=0}^{h-1}m_i
\ge\frac3{20}(hL)^{1/3}.
}\tag{COARSE-CRITICAL-COUNTERMODEL}
$

2. The full, repetition-permitting scalar triple-pattern capacity (COARSE-TRIPLE-CAPACITY), with this occupancy vector, holds for **every** integer index sum s:

$
\boxed{
\sum_{i\le j\le k,\ i+j+k=s}w(i,j,k)
\le 3L-2.
}\tag{COUNTERMODEL-PASSES-ALL-HALL}
$

**Proof.** Since each summand (i+1)^(-2/3)>=h^(-2/3) for i<h, the partial sum is at least h^(1/3). Using floor(x)>=x-1 gives \(\sum_{i<h}m_i\ge4Mh^{1/3}-h\ge3Mh^{1/3}=(3/20)(hL)^{1/3}\), because h<=M.

For the triple-capacity statement let a_i=(i+1)^(-2/3) for i>=0, and set a_i=0 outside [0,M-1]. Splitting each convolution at its midpoint and comparing power sums with integrals proves

$
\sum_{i+j=s}a_ia_j\le10(s+1)^{-1/3},
\qquad
\boxed{\sum_{i+j+k=s}a_ia_ja_k\le100}\quad(s\ge0).
$

Each m_i>=floor(4M^(1/3))>=4, so m_i+2<=2m_i<=(2/5)L^(1/3)a_i. For each index pattern i<=j<=k, write v for the number of distinct permutations of (i,j,k): respectively v=6,3,1 when all three indices are distinct, exactly two coincide, or all three coincide. Its multiset weight w(i,j,k) is at most (v/6)(m_i+2)(m_j+2)(m_k+2). Indeed the three cases reduce to m_i m_j m_k<=b_i b_j b_k, binom(m_i+1,2)m_k<=b_i²b_k/2, and binom(m_i+2,3)<=b_i³/6. Therefore the sum of pattern weights at index sum s is bounded by **one sixth of the full ordered triple convolution** of b_i=m_i+2. Thus

$
\sum_{i\le j\le k,\ i+j+k=s}w(i,j,k)
\le\frac16\left(\frac25\right)^3 L\cdot100
=\frac{16}{15}L<3L-2
$

for L>=8. The last inequality holds because L=(20M)^3>=8000. QED.

**Interpretation.** At arbitrarily long but finite collections of coarse checkpoints, a numerical occupancy profile can remain at positive normalized critical density while respecting *every one* of the cubic bin-index sum-packing constraints. This rules out proving Erdős #41 from these **cardinality-only** inequalities plus prefix counts, without an additional position-sensitive arithmetic compatibility theorem. The profile is a hostile **scalar relaxation**, not an actual B3 construction; it does not disprove the conjecture or the exact seven-layer and reciprocal shadow conditions.

This is why the preferred Stage B object remains **true future extension capacity and reciprocal signed-code compatibility**, rather than scalar block counts or unowned multiscale sums.

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

**Unproved bridge, after the stronger one-anchor and reflection audits:** show that a hypothetical c-persistent B3 chain cannot indefinitely sustain the four *simultaneous* reflected signed-code conditions (both signed-word injections and both reciprocal shadow avoidances) in the future windows that are required by its actual counting function. An adequate theorem must compare several successive, uniquely owned geometric windows or certify finite-horizon impossibility at every c>0. A one-window loss of the singleton or cubic-shadow ceiling is not enough: in a genuine B3 countercontrol 13 of 14 initially legal future sites vanish but the true batch capacity remains 1. Near-envelope rigidity can serve as a sufficient auxiliary hypothesis only if proved independently; it must not be assumed. A collision-hypergraph dual certificate with all optimally rerouted future batch shapes is another admissible route.

This is the mathematically consequential difference from the old modular inverse programme: we HAVE proved a positive density-sensitive forward shadow consumption theorem, but we have NOT proved that the consumption is forced to accumulate against true critical-density extensions. New work must address that bridge, not restate the singleton tax or sum geometric windows as if they share one global capacity budget.

The exact finite-window base-eight valley criterion remains the final target; Erdős #41 is OPEN (https://www.erdosproblems.com/41). The result is bounded GCL research and not externally certified novelty.
