# Erdős #41 — Joint-window integer sixth-defect forcing and the residue-refinement hierarchy

**23 October 2026 | Candidate mathematics, not a solution.** GCL #2789; Tracks A #2790, B #2791, D #2793; independent critic #2792. The preceding modular-single-window research is open on PR #2824. This manuscript is independent and fully states the prerequisite identities, so review is not dependent on treating PR #2824 as certified or merged.

## 1. Exact weighted collision energy

Throughout, B3 means uniqueness of sums of unordered three-element multisets, **allowing repeated elements**. For a finite integer set E of n elements, let

$$
F_E(\theta)=\sum_{e\in E}e^{2\pi i e\theta},
\qquad
\mathfrak d_6(E)=\int_0^1|F_E(\theta)|^6\,d\theta-(6n^3-9n^2+4n).
$$

Every distinct unordered three-term multiset of equal integer sum contributes a positive term to this nonnegative integer defect. In particular, if X,Y,Z are pairwise disjoint and X union Y is B3, put Q=X+Y, whose |X||Y| cross pair sums are all distinct. For the actual mixed triple representation function

$$
r(s)=|\{(q,z)\in Q\times Z:q+z=s\}|,
$$

the exact contribution from **pairs of different unordered triples with one entry in each colour** is

$$
\boxed{
\mathfrak d_{XYZ}=36\sum_s r(s)(r(s)-1)\le\mathfrak d_6(X\cup Y\cup Z).
}\tag{COLOUR-LEDGER}
$$

The factor 36 is six orderings per distinct-colour triple, squared. The nonnegative integer summands cannot cancel.

## 2. Any number of forced future windows: a shared integer capacity system

Let X,Y be disjoint nonempty finite sets with X union Y B3. Write Q=X+Y. Let

$$
J_i=[L_i,U_i]\cap\mathbb Z,\qquad i=1,\ldots,b,
$$

be mutually disjoint finite future windows, also disjoint from X union Y. Let $Z_i\subseteq J_i$ be unknown occupied batches, with required populations $|Z_i|\ge k_i$ for prescribed nonnegative integers $k_i$. Write $Z=\bigcup_iZ_i$.

The **joint** possible mixed-triple support is

$$
\mathcal U=\bigcup_{i=1}^b(Q+J_i),
$$

NOT the sum of separate capacities $|Q+J_i|$. Choose modulus $h\ge1$ and put

$$
a_r=|\{q\in Q:q\equiv r\pmod h\}|,\qquad
j_{i,r}=|\{u\in J_i:u\equiv r\pmod h\}|,
$$

$$
c_t=|\{u\in\mathcal U:u\equiv t\pmod h\}|.
$$

For any actual batches, let $z_{i,r}=|\{z\in Z_i:z\equiv r\pmod h\}|$. Their **joint** mixed-three-colour residue loads are

$$
N_t=\sum_{i=1}^b\sum_{r\bmod h}a_rz_{i,t-r}.
$$

**Theorem A (exact joint-window necessary integer system).** Every genuine B3-compatible selection must satisfy

$$
\boxed{
z_{i,r}\in\mathbb Z_{\ge0},\quad
z_{i,r}\le j_{i,r},\quad
\sum_r z_{i,r}\ge k_i,\quad
N_t\le c_t\quad(\forall t\bmod h).
}\tag{JOINT-INTEGER-CAPACITY}
$$

Thus a proof of integer infeasibility of this finite system is a **rigorous universal collision certificate** for all choices of actual points meeting the stated per-window population requirements. Crucially, individually feasible systems for each $J_i$ do not imply feasibility of the joint system: the translated sum supports can overlap and share exact integer capacity.

**Proof.** Each pair $(q,z)$ identifies a distinct unordered mixed triple $(x,y,z)$ because X union Y is B2 and the three colours are disjoint. Under B3 all resulting sums are distinct. The number of those sums in residue class t is exactly $N_t$, and all lie in the $c_t$ available positions of $\mathcal U$ in that residue. The remaining inequalities express literal integer occupancy within the windows. QED.

## 3. Integral convexity sharpens Cauchy–Schwarz and bounds the sixth defect

For nonnegative integers N,C with C>0, write $N=Cv+w$, $0\le w<C$, and define

$$
\boxed{
\Phi(N,C)=C\,v(v-1)+2vw.
}\tag{EXACT-INTEGER-FIBRE-PRESSURE}
$$

Set $\Phi(0,0)=0$. A state with $N>0$ and $C=0$ is impossible for correctly formed actual supports.

**Lemma B (sharp integer collision lower bound).** If N labelled objects occupy at most C distinct integer positions, then

$$
\sum_{s=1}^C r_s(r_s-1)\ge\Phi(N,C),
\qquad \sum_s r_s=N,
$$

with equality for the most even integer occupancy, namely C−w positions occupied v times and w positions occupied v+1 times. This inequality is SHARP given only N and C; it makes no claim that every such occupancy pattern is arithmetically realizable by old pair sums and future elements.

**Proof.** For $r_u\ge r_v+2$, moving one object from position u to v changes $\sum r_s(r_s-1)$ by $-2(r_u-r_v-1)<0$. Repeating makes all occupation numbers differ by at most one; division with remainder then yields the claimed formula. QED.

**Theorem C (joint modular integer sixth-defect bound).** In Theorem A's notation, for any actual sets $Z_i$,

$$
\boxed{
\mathfrak d_6(X\cup Y\cup Z)
\ge36\sum_{t\bmod h}\Phi(N_t,c_t).
}\tag{JOINT-SIXTH-INTEGER-DEFECT}
$$

Further, let $\mathcal A_h(k_1,\ldots,k_b)$ be the finite set of integer vectors $(z_{i,r})$ satisfying only the window upper bounds and per-window lower populations, **without** imposing $N_t\le c_t$. Define

$$
\Gamma_h(Q;J_1,\ldots,J_b;k_1,\ldots,k_b)
=36\min_{z\in\mathcal A_h(k)}
\sum_{t\bmod h}\Phi\left(
\sum_{i,r}a_r z_{i,t-r},c_t\right).
$$

For actual compatible populations the set $\mathcal A_h(k)$ is nonempty, and

$$
\boxed{
\mathfrak d_6(X\cup Y\cup Z)\ge\Gamma_h.
}\tag{UNIFORM-FORCED-DEFECT}
$$

If $\Gamma_h>0$, **no B3 set can populate every prescribed window to its required minimum**. The minimization can be restricted to $\sum_rz_{i,r}=k_i$: deleting surplus elements cannot increase any $N_t$, and $\Phi$ is monotone in N.

**Proof.** Split the mixed triple representation function from §1 into its h residue fibres. Fibre t has exactly $N_t$ ordered-by-colour triples and at most $c_t$ integer sum positions. Apply Lemma B to each fibre, multiply by the exact sixth-defect factor 36 and minimize over literal integer residue populations. Extra global triple-colour collisions are nonnegative. QED.

This corrects the loss incurred by the earlier real-valued Cauchy lower bound. For instance, a residue fibre with $N=4$ and $C=3$ has $\Phi(4,3)=2$, while $N^2/C-N=4/3$; the exact sixth-defect penalty is 72 instead of 48.

## 4. Residue refinement is monotone

**Theorem D (divisibility monotonicity).** If $h$ divides $H$, then for the same *actual* fixed Q, windows and batch populations,

$$
\boxed{
\sum_{t\bmod H}\Phi(N_t,c_t)\ge
\sum_{u\bmod h}\Phi\left(
\sum_{t\equiv u\pmod h}N_t,\,
\sum_{t\equiv u\pmod h}c_t\right).
}\tag{MODULUS-REFINEMENT}
$$

Consequently the jointly optimized forced lower bounds also satisfy $\Gamma_H\ge\Gamma_h$.

**Proof.** The residue fibres modulo $H$ partition every residue fibre modulo $h$. The minimum possible integer collision count subject to the finer prescribed loads cannot be below the unconstrained optimum obtained by aggregating all positions and loads in their common coarser fibre, by Lemma B. For the optimized statement, every integer H-residue allocation projects to an h-residue allocation with the same per-window totals; the finer cost is at least that projected coarser cost, which is in turn at least the coarser minimum. QED.

This creates a genuine hierarchy of rigorous collision lower bounds. It is NOT a monotone-in-time potential for legal B3 prefixes: every such prefix has zero exact defect, and there is still no theorem that some modulus must eventually force $\Gamma_h>0$ under persistent critical density.

## 4A. Finite completeness at a sufficiently fine modulus

**Theorem E (exactness threshold for one selected mixed-colour family).** Put

$$
D=\max\mathcal U-\min\mathcal U,\qquad H>D.
$$

For this finite candidate-window problem, every nonzero residue class modulo H contains **at most one integer of** $\mathcal U$, and each admissible window position is also uniquely specified by its residue modulo H. Consequently,

$$
\boxed{
\Gamma_H
=
\min_{\substack{Z_i\subseteq J_i\\|Z_i|\ge k_i}}
36\sum_s r_{Q,Z}(s)(r_{Q,Z}(s)-1)
=
\min_{\substack{Z_i\subseteq J_i\\|Z_i|=k_i}}
\mathfrak d_{XYZ}.
}\tag{FINITE-ARITHMETIC-COMPLETENESS}
$$

Here $r_{Q,Z}(s)=|\{(q,z)\in Q\times\bigcup_iZ_i:q+z=s\}|$ and $\mathfrak d_{XYZ}$ denotes the **selected mixed-colour contribution only**. In particular, $\Gamma_H=0$ if and only if there is an actual selection meeting every required window population whose selected mixed three-colour sums $Q+Z$ are all different.

**Proof.** Fix some $q_0\in Q$. The translated subset $q_0+\bigcup_iJ_i$ lies inside $\mathcal U$, so the map from all candidate future positions to residues modulo H is injective: any two distinct such positions have integer separation at most D, less than H. The same holds for Q by fixing an arbitrary future candidate position. Every integer vector $z_{i,r}$ satisfying the literal per-window capacity constraints is therefore exactly the residue description of a unique collection of selected actual integers $Z_i$. Moreover, distinct positions $s\in\mathcal U$ occupy distinct H-residues and their capacities $c_t$ are either zero or one. For $c_t=1$, the integer-fibre minimum is identically $\Phi(N_t,1)=N_t(N_t-1)$; $N_t$ is exactly the representation multiplicity at its unique actual integer sum. Thus the modular lower bound is equality for EVERY candidate collection. Minimizing over the equal-population allocations gives the rightmost expression. The minimum under $\ge k_i$ agrees because removal of any surplus future element cannot create a collision and the chosen minima are feasible whenever the population lower bounds are. QED.

**Limits and complexity.** This theorem is a finite **completeness result for a chosen collision type**, not for all possible B3 triple-colour types. Avoidance of mixed collisions of type $(X,Y,\bigcup Z_i)$ may coexist with illegal $(X,X,Z)$, $(X,Z,Z)$ or other triple equalities. The exactness modulus H can grow with the full window span; it does NOT give a bounded or uniformly efficient modular certificate, nor establish eventual overload in a c-persistent infinite B3 configuration. For a useful density theorem the challenge is obtaining a forcing statement at a controlled collection of windows/moduli without merely exhaustively restating finite extension feasibility.

## 4B. Cumulative-prefix constraints: the exact form supplied by persistent lower density

A cumulative lower-density hypothesis does **not** prescribe a positive cardinality for every individual future window. The finite forcing formalism admits exactly the weaker constraints it actually supplies.

Let $P=A\cap[1,R]$ be a complete prefix of a hypothetical infinite B3 set, with older disjoint cohorts $X,Y\subseteq P$. Let consecutive integer windows $J_1,\ldots,J_b$ **partition** $(R,N_b]\cap\mathbb Z$, with endpoints $N_j=\max J_j$. Fix $c>0$ and suppose $A(N)\ge cN^{1/3}$ for every $N\ge R$.

Write $z_{i,r}$ for integer future populations in residue class r modulo h and $z_i=\sum_rz_{i,r}$. At every chosen endpoint the *necessary* demand is

$$
\boxed{
\sum_{i=1}^{j}z_i\ge
K_j(c):=\max\{0,\lceil cN_j^{1/3}\rceil-|P|\}
\qquad (1\le j\le b).
}\tag{TRUE-CUMULATIVE-DEMAND}
$$

Here no individual window is assigned an artificial positive lower bound, and no uncounted gaps may be omitted from the partition. Define $\widetilde\Gamma_h$ by minimizing the same integral fibre-pressure functional of §3 over **all integer** allocations obeying these cumulative demands and the literal capacity $0\le z_{i,r}\le j_{i,r}$.

**Theorem F (sound cumulative-density defect certificate).** For any genuine B3 extension meeting the stated lower counting hypothesis,

$$
\boxed{
0=\mathfrak d_6(A\cap[1,N_b])
\ge
\widetilde\Gamma_h(Q;J_1,\ldots,J_b;K_1(c),\ldots,K_b(c)).
}\tag{CUMULATIVE-DENSITY-CERTIFICATE}
$$

In particular, $\widetilde\Gamma_h>0$ is an exact contradiction. The modulus-refinement inequality from Theorem D holds for these cumulative constraints too. At any modulus exceeding $\mathrm{diam}(\mathcal U)$ the optimized value equals the true minimum **selected mixed-colour** collision defect under these cumulative demands.

**Proof.** All elements of $A$ above R and at most $N_b$ belong to precisely one of the partition windows. The assumed counting lower bound therefore yields the displayed cumulative inequalities with no additional population hypothesis. Their actual residue allocations form an admissible integer vector for the minimization; by Theorem C its objective cannot exceed the true global defect. For refinement and finite exactness, use the same projection and injectivity arguments as Theorems D and E; the prefix cumulative sums are invariant under residue coarsening, and at sufficiently large modulus every permitted integer position has its own residue. QED.

**Illustration, not a critical-density instance:** In §5, neither window needs to be individually forced if the only constraint is the *combined* demand $z_1+z_2\ge2$. Its integer modular minimum still obeys $\widetilde\Gamma_1=0$ and $\widetilde\Gamma_3=72$. This distinguishes logically sound cumulative forcing from unwarranted claims of local population. The arbitrary demand two in this small example is not asserted to follow from a particular $cN^{1/3}$ inequality.

**Remaining unsolved problem.** A hypothetical positive lower critical density gives real cumulative demands but places no simple independent lower bound on the size or residue distribution of each narrow window. The central missing step is to prove that for *every* such globally compatible evolving B3 prefix P, some finite downstream partition and modulus force $\widetilde\Gamma_h>0$. No such universal theorem has been established. The prefix inequalities and exactness of the finite optimizer alone are not a proof of Erdős #41.

## 4C. All old pair sums: a full-prefix necessary condition stronger than selected old colour pairs

The selected old-colour cross pair sums $X+Y$ may omit the very old-old pair-sum difference that forbids a new batch. One can preserve **all** the old prefix's two-summand structure without assuming any regular distribution of its elements.

Let $P$ be an arbitrary finite repetition-permitted B3 set of size $n$, and let $Z$ be disjoint from P. Define

$$
Q(P)=\{p+p':p,p'\in P,\ p\le p'\},
\qquad
\omega(p+p')=
\begin{cases}1,&p=p',\\2,&p<p'.\end{cases}
$$

The B3 condition on P implies its unordered pair sums are all distinct, so the weights are well-defined. Write

$$
r_{PPZ}(s)=\sum_{\substack{q\in Q(P),z\in Z\\q+z=s}}\omega(q),
\qquad
u_{PPZ}(s)=|\{(q,z)\in Q(P)\times Z:q+z=s\}|.
$$

**Theorem G (complete old-pair/future collision ledger).** The contribution of collisions between distinct unordered triples containing **two old entries and one new entry** to the global sixth-moment defect is exactly

$$
\boxed{
\mathfrak d_{PPZ}
=
9\left[
\sum_s r_{PPZ}(s)^2
-
(2n^2-n)|Z|
\right]
\ge
9\sum_su_{PPZ}(s)\bigl(u_{PPZ}(s)-1\bigr)
\ge0.
}\tag{FULL-PREFIX-RESONANCE}
$$

It vanishes if and only if the map $(q,z)\mapsto q+z$ on $Q(P)\times Z$ is injective.

**Proof.** Each unordered triple $(p,p',z)$ has exactly $3\omega(p+p')$ orderings. Squaring the weighted representation counts and subtracting its diagonal contributions yields the first equality, since $\sum_{q\in Q(P)}\omega(q)^2=n+4\binom n2=2n^2-n$. Every collision between *distinct* unordered triples has exact defect contribution $2(3\omega(q))(3\omega(q'))\ge18$, while every colliding unordered pair of $(q,z)$ inputs contributes two units to $\sum_s u(s)(u(s)-1)$. Both vanish precisely under injectivity. These triples belong to a single distinguished colour type (old,old,new), so their positive contributions are included in the full defect without cancellation. QED.

**Theorem H (full-prefix joint modular integer bound).** Use the future windows and cumulative checkpoint constraints of Theorem F, but replace the selected old mixed pair sums $X+Y$ by $Q(P)$. Let $a_r$ count the **unweighted** $Q(P)$ residues modulo h, $c_t$ the exact support $(Q(P)+\bigcup_iJ_i)$ residue capacities, and $N_t$ their convolutions with the integer future histogram allocations. Then every B3 extension satisfies the same necessary integer system $N_t\le c_t$. Moreover,

$$
\boxed{
\mathfrak d_6(P\cup Z)
\ge
\mathfrak d_{PPZ}
\ge9\sum_{t\bmod h}\Phi(N_t,c_t).
}\tag{FULL-PREFIX-INTEGER-DEFECT}
$$

Minimizing the rightmost expression over the literal future-window integer allocations, with either per-window or cumulative checkpoint population demands, produces a universal finite B3 impossibility certificate. This is **strictly more comprehensive** than checking one selected $X+Y$ because it includes all old repeated and mixed pair sums. Its numerical lower-bound coefficient is 9 rather than 36 because diagonally repeated old pairs have only three permutations.

**Proof.** Theorem G gives a lower bound of nine times the unweighted collision-pair count among $Q(P)+Z$. Split those unweighted representations into residues and apply the sharp integer fibre Lemma B, then minimize as in Theorems C and F. No assumption about the older arithmetic organization is made beyond the actual B3 property of P. QED.

**Exact hostile witness of the difference from selected cohorts.** Take

$$
P=\{1,2,5,14\},\qquad
J_1=\{1000,1001\},\qquad
J_2=\{1002,1003\}.
$$

All singleton extensions of P using any point of these windows are B3 (the new element is greater than four times the old maximum). Every choice of **two** future elements, one from each window, creates a PPZ collision because their difference is 1, 2 or 3 and the actual full pair-sum set Q(P) has each of these differences. The scalar full-prefix count does **not** detect the forced collision: $|Q(P)|=10$ and the union $Q(P)+(J_1\cup J_2)$ has 24 positions, enough for the twenty mixed sums of two future points.

However, modulo 6 the actual-support capacity vector is $(3,4,5,4,4,4)$ and the four possible future choices all overload some residue; thus the full-prefix cumulative integer system with combined required population 2 is impossible. The selected earlier old colour partition $X=\{1,2\}$, $Y=\{5,14\}$ **misses** the collision for $Z=\{1000,1002\}$, because the four sums in $X+Y=\{6,7,15,16\}$ have no difference 2. The full Q(P) certificate detects it.

For the cumulative total-two demand in this example, the **correct all-old-pair lower-bound factor is 9**. The modulus-6 optimized unweighted bound is $18$, and the sufficiently fine modulus-50 unweighted bound is $36$, while the exact minimum **weighted** PPZ sixth defect over all six two-element future subsets is $54$. Thus a fine modulus recovers the full unweighted pair-sum collision count, but not the diagonal/offdiagonal pair multiplicity weights unless those weights are explicitly retained in the integer optimization. The earlier factor 36 applies ONLY to triples with three distinct old/new colours, not to all old-old-new triples. The all-prefix certificate is nonetheless sound and forces a positive collision for every selection.

The family is a genuine finite illustration of why **retaining the entire evolving prefix** matters. It is neither a proof that critical lower density forces such windows nor a construction of an infinite B3 set.

## 4D. Weighted integral pressure: recovering the **exact** old-old-new defect

The full-prefix bound in Theorem H is deliberately conservative: each unordered old pair has a weight $\omega(q)\in\{1,2\}$, and counting all old pairs as weight one preserves positivity but loses the multiplicity of colliding off-diagonal pairs. The weights can be retained without abandoning integer residue optimization.

For a fixed modulus h and actual future selections Z, and for each residue class t, define the **number**, **weighted mass**, and **diagonal squared mass** of labelled $(q,z)$ inputs:

$
N_t=\sum_{q,z:\,q+z\equiv t\pmod h}1,\qquad
W_t=\sum_{q,z:\,q+z\equiv t\pmod h}\omega(q),\qquad
B_t=\sum_{q,z:\,q+z\equiv t\pmod h}\omega(q)^2.
$

Here q ranges over $Q(P)$ and z over Z. These are exact integer convolutions of the old-pair residue histograms (separated into diagonal and off-diagonal weights) against the future-window integer residue populations.

For $C>0$ and $W=Cv+w$, $0\le w<C$, put

$
\Psi(W,C)=(C-w)v^2+w(v+1)^2.
$

This is the minimum $\sum_{j=1}^C a_j^2$ over all **nonnegative integers** $a_j$ totalling W. It allows the weight-two contributions to split into separate unit masses, so it is a relaxation, never an overestimate of the actual weighted squared energy. Let $c_t$ be the number of available integer sums in $(Q(P)+\bigcup_iJ_i)$ congruent to t modulo h.

**Theorem I (weighted full-prefix modular collision certificate).** For every genuine old B3 prefix P and arbitrary future set Z contained in the declared windows,

$
\boxed{
\mathfrak d_6(P\cup Z)
\ge \mathfrak d_{PPZ}
\ge 9\sum_{t\bmod h}
\max\!\left\{
\Phi(N_t,c_t),\
\Psi(W_t,c_t)-B_t,\
0
\right\}.
}\tag{WEIGHTED-INTEGER-DEFECT}
$

A term with $c_t=0$ necessarily has $N_t=W_t=B_t=0$ for a correctly formed support. The bound is exact for every actual Z when

$
h>\max(Q(P)+\textstyle\bigcup_iJ_i)
-\min(Q(P)+\textstyle\bigcup_iJ_i).
$

Under that finite-modulus condition each occupied residue contains at most one actual integer sum, so $c_t\in\{0,1\}$ and $\Psi(W_t,1)=W_t^2$. Thus the rightmost sum **equals the full weighted** $\mathfrak d_{PPZ}$, rather than just the weaker unweighted collision count.

**Proof.** In residue t, the actual weighted representation $R(s)=\sum_{q+z=s}\omega(q)$ is a nonnegative integer, with total mass $W_t$ on at most $c_t$ sites. By integer convexity $\sum_{s\equiv t}R(s)^2\ge\Psi(W_t,c_t)$. Subtracting the exact diagonal $\sum_{s\equiv t}\sum_{q+z=s}\omega(q)^2=B_t$ yields the second lower bound. Separately, each pair of distinct inputs $(q,z)$ and $(q',z')$ whose sums collide has weight product at least one, so the weighted collision contribution is at least $\Phi(N_t,c_t)$. Both inequalities hold for each nonnegative fibre contribution, hence their maximum remains a lower bound. Summing fibres and multiplying by the exact factor 9 proves the formula. At the stated fine modulus every possible integer sum occupies its own residue, and its weighted squared contribution is exactly $W_t^2$; equality follows. QED.

Optimizing this weighted expression over the **integer** future-window histograms subject to Theorem F's cumulative checkpoint requirements gives a stronger finite forcing functional $\Gamma_h^{\mathrm{weighted}}$. It is nondecreasing on any divisibility chain of moduli, by the same refinement argument for the two convex lower bounds, and is exactly the minimum actual $\mathfrak d_{PPZ}$ over future selections when the modulus exceeds the full mixed-sum span. The optimization does **not** certify the absence of PZZ, ZZZ or other types of B3 collisions; it concerns PPZ only.

**Corrected numeric calibration.** For $P=\{1,2,5,14\}$ and two future elements anywhere in $J_1=\{1000,1001\}, J_2=\{1002,1003\}$, the minimum exact weighted PPZ defect is $54$. The earlier unweighted factor-nine fine-modulus relaxation yields only $36$; the new weighted fine-modulus functional gives exactly $54$. This calibrates the difference between a rigorous positive certificate and full **selected-type** completeness, without suggesting that either forces universal critical-density loss.

## 5. Concrete simultaneous-window obstruction missed by separate windows and total capacity

Take

$$
X=\{1,2\},\qquad Y=\{1000,1003\},
$$

with $Q=X+Y=\{1001,1002,1004,1005\}$, and two disjoint future windows

$$
J_1=\{10000,10001\},\qquad
J_2=\{10003,10004\},\qquad
k_1=k_2=1.
$$

Every individual point in either window can be added to X union Y while preserving B3; both separately occupied windows pass all individual single-point arithmetic tests.

The separate supports each have **six** available positions,

$$
|Q+J_1|=|Q+J_2|=6,
$$

so each single-point demand four fits. Their shared actual support is

$$
\mathcal U=(Q+J_1)\cup(Q+J_2)=[11001,11009]\cap\mathbb Z,
$$

containing nine positions. **Even the combined unpartitioned scalar Hall count passes:** $4(k_1+k_2)=8\le9$.

Modulo 3, however, the old pair-sum histogram is $a=(2,0,2)$ and the joint support has capacity $c=(3,3,3)$. Both windows admit only residues 1 or 2. Each selected future point therefore requires two units in each of two out of three target residue classes. Any two such two-class demands **overlap somewhere**, forcing a load of at least four against capacity three.

Therefore the joint integer system has NO solution with one future element in each window, and

$$
\boxed{
\Gamma_1=0,\qquad \Gamma_3=72.
}\tag{TWO-WINDOW-INTEGRAL-OBSTRUCTION}
$$

The two-point combination $Z=\{10000,10004\}$ attains the lower bound EXACTLY:

$$
1+1000+10004=2+1003+10000=11005,
\qquad
\mathfrak d_6(X\cup Y\cup Z)=72.
$$

All three pairwise unions (X union Y, X union Z, and Y union Z) are genuine repetition-permitted B3. Thus this is a real three-colour obstruction, not a defect of either individual window or pairwise union.

The example also defeats a family of naive separate-window extension arguments: locally legal choices, individually feasible residue allocations, and spare combined total sum positions still need not admit one jointly legal selection. Its certificate is **integral and simultaneous**.

## 6. Relation to the unresolved global density problem

Theorems A–D are unconditional finite mathematical results for specified X,Y and necessarily occupied future windows. They do not imply that a hypothetically c-persistent infinite B3 set will furnish older cohorts and forced windows for which any $\Gamma_h$ is positive.

A full positive-density contradiction would need an additional, genuinely new theorem: for every c>0 and every sufficiently large B3 prefix compatible with persistent cumulative count $A(N)\ge cN^{1/3}$, there must exist a finite family of actual (possibly irregular) future windows with the guaranteed populations, and a modulus h, such that $\Gamma_h>0$ despite all possible changes in their arithmetic organization. No such universal transport/forcing statement is proved here.

Finite-field moment codes, tagged separated-block examples, and the geometric-shell occupancy no-go must remain hostile controls; modular infeasibility cannot be inferred from an ordinary continuous LP when integer feasibility remains an independent requirement.

**Disposition: FINITE THEOREM plus exact integrality supersaturation and an explicit noncancelling joint-window certificate; universal cross-scale density step OPEN.** Independent source-locked critical mathematical audit required before theorem certification.
