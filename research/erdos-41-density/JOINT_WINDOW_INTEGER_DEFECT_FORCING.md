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

$
D=\max\mathcal U-\min\mathcal U,\qquad H>D.
$

For this finite candidate-window problem, every nonzero residue class modulo H contains **at most one integer of** $\mathcal U$, and each admissible window position is also uniquely specified by its residue modulo H. Consequently,

$
\boxed{
\Gamma_H
=
\min_{\substack{Z_i\subseteq J_i\\|Z_i|\ge k_i}}
36\sum_s r_{Q,Z}(s)(r_{Q,Z}(s)-1)
=
\min_{\substack{Z_i\subseteq J_i\\|Z_i|=k_i}}
\mathfrak d_{XYZ}.
}\tag{FINITE-ARITHMETIC-COMPLETENESS}
$

Here $r_{Q,Z}(s)=|\{(q,z)\in Q\times\bigcup_iZ_i:q+z=s\}|$ and $\mathfrak d_{XYZ}$ denotes the **selected mixed-colour contribution only**. In particular, $\Gamma_H=0$ if and only if there is an actual selection meeting every required window population whose selected mixed three-colour sums $Q+Z$ are all different.

**Proof.** Fix some $q_0\in Q$. The translated subset $q_0+\bigcup_iJ_i$ lies inside $\mathcal U$, so the map from all candidate future positions to residues modulo H is injective: any two distinct such positions have integer separation at most D, less than H. The same holds for Q by fixing an arbitrary future candidate position. Every integer vector $z_{i,r}$ satisfying the literal per-window capacity constraints is therefore exactly the residue description of a unique collection of selected actual integers $Z_i$. Moreover, distinct positions $s\in\mathcal U$ occupy distinct H-residues and their capacities $c_t$ are either zero or one. For $c_t=1$, the integer-fibre minimum is identically $\Phi(N_t,1)=N_t(N_t-1)$; $N_t$ is exactly the representation multiplicity at its unique actual integer sum. Thus the modular lower bound is equality for EVERY candidate collection. Minimizing over the equal-population allocations gives the rightmost expression. The minimum under $\ge k_i$ agrees because removal of any surplus future element cannot create a collision and the chosen minima are feasible whenever the population lower bounds are. QED.

**Limits and complexity.** This theorem is a finite **completeness result for a chosen collision type**, not for all possible B3 triple-colour types. Avoidance of $(X,Y,\bigcup Z_i)$-mixed collisions may coexist with illegal $(X,X,Z)$, $(X,Z,Z)$ or other triple equalities. The exactness modulus H can grow with the full window span; it does NOT give a bounded or uniformly efficient modular certificate, nor establish eventual overload in a c-persistent infinite B3 configuration. For a useful density theorem the challenge is obtaining a forcing statement at a controlled collection of windows/moduli without merely exhaustively restating finite extension feasibility.

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
