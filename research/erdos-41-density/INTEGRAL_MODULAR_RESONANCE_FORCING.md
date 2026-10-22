# Erdős #41 — Integral residue-capacity certificates for actual-support multiscale resonance

**22 October 2026.** Research candidate; Track A/B/D crossover, coordination #2789; review #2792. This note proves exact **finite** modular and actual-support forcing tests for genuinely occupied B3 windows. Unlike the earlier interval-envelope Hall bounds, these tests retain old cross-pair-sum arithmetic and integer future residue occupancy. This is **not** a proof that the tests inevitably trigger under persistent positive critical density. Erdős #41 remains OPEN.

## 1. Arithmetic-support rather than whole-envelope capacity

Let X and Y be two disjoint nonempty finite integer sets with X union Y repetition-permitted B3. Then the $m=|X||Y|$ mixed pair sums

$$
Q=X+Y=\{x+y:x\in X,\ y\in Y\}
$$

are distinct, by B2 uniqueness. Let $J=[L,L+W-1]\cap\mathbb Z$ be any future interval, disjoint from X and Y, and let $Z\subseteq J$ be a candidate future B3 batch. Define the **actual old-support available positions**

$$
U=Q+J=\bigcup_{q\in Q}[q+L,q+L+W-1]\cap\mathbb Z.
$$

**Theorem A (mixed-support capacity).** If X union Y union Z is B3, then

$$
\boxed{
|X||Y||Z|\le|Q+J|
=W+\sum_{i=1}^{m-1}\min(W,q_{i+1}-q_i),
}\tag{GAP-CAPACITY}
$$

where $q_1<\cdots<q_m$ are the *actual* sorted cross pair sums. This bound uses intrinsic gaps of X+Y and the true window width, not only the diameter of X+Y. It is invariant under independent whole-block translations of X, Y, and J.

**Proof.** B3 uniqueness forces all $m|Z|$ mixed triple sums $(x+y)+z$ to be distinct. They lie in U, proving the first inequality. Each consecutive translated width-W interval contributes exactly $\min(W,q_{i+1}-q_i)$ new integer positions to their ordered union, proving the exact gap formula. QED.

For a c-persistent hypothetical infinite B3 set, an actual populated Z of at least k elements in a fixed future interval therefore requires $|Q+J|\ge mk$. The unresolved issue is showing that **some necessarily occupied choice** of X,Y,J violates this condition, regardless of how X,Y are arranged; the theorem itself does not force that conclusion.

## 2. An exact integer modular obstruction stronger than scalar Hall

Fix a positive modulus $h$. Let $\mathbb Z_h$ be its residue classes. Define

$$
a_r=|\{q\in Q:q\equiv r\pmod h\}|,\qquad
z_r=|\{z\in Z:z\equiv r\pmod h\}|,
$$

and

$$
C_t=|\{u\in U:u\equiv t\pmod h\}|,\qquad
J_r=|\{j\in J:j\equiv r\pmod h\}|.
$$

**Theorem B (integer modular capacity and positive sixth-defect pressure).** Every B3-compatible Z must satisfy the INTEGER convolution system

$$
\boxed{
0\le z_r\le J_r,\quad \sum_r z_r=|Z|,
\qquad
N_t:=\sum_{r\in\mathbb Z_h}a_rz_{t-r}\le C_t
\quad(\forall t\in\mathbb Z_h).
}\tag{INTEGRAL-MODULAR-HALL}
$$

For arbitrary Z (not necessarily B3), its exact three-colour contribution to the nonnegative sixth collision defect satisfies

$$
\boxed{
\mathfrak d_{XYZ}
\ge
36\sum_{\substack{t\in\mathbb Z_h\\C_t>0}}
\left(\frac{N_t^2}{C_t}-N_t\right)_+.
}\tag{MODULAR-SIXTH-DEFECT}
$$

If $C_t=0$ but $N_t>0$, the data contradicts $Z\subseteq J$ and the definitions, hence cannot arise. The positive part is $v_+=\max(v,0)$.

**Proof.** Let $r_{XYZ}(s)$ count labelled triples $(x,y,z)$ with sum s. It has total mass $m|Z|$ and, for each residue t, mass $N_t$ in the at most $C_t$ admissible actual-support positions. The type-specific sixth defect is the exact positive integer

$$
\mathfrak d_{XYZ}=36\sum_s\bigl(r_{XYZ}(s)^2-r_{XYZ}(s)\bigr).
$$

Cauchy–Schwarz separately within each residue class gives $\sum_{s\equiv t}r(s)^2\ge N_t^2/C_t$. Since every summand $r(s)^2-r(s)$ is nonnegative, one can take the positive parts *independently* and sum. If B3 holds, $\mathfrak d_{XYZ}=0$; each $r(s)$ is either zero or one, hence $N_t\le C_t$. The position upper bounds $z_r\le J_r$ are immediate. QED.

Define the **integer modular extension ceiling**

$$
\boxed{
K_h(Q,J)=
\max\left\{\sum_r v_r:
v_r\in\mathbb Z_{\ge0},\ 
v_r\le J_r,\
\sum_r a_rv_{t-r}\le C_t\text{ for all }t
\right\}.
}\tag{INTEGRAL-CAPACITY-CEILING}
$$

It is a finite integer optimization problem, not a prediction of valid B3 extensions. Every true B3-compatible Z obeys

$$
|Z|\le K_h(Q,J)\le\left\lfloor\frac{|Q+J|}{|Q|}\right\rfloor.
$$

The second bound follows by summing the modular constraints. The **integrality** of $v_r$ is indispensable: allowing fractional residue populations can admit false candidate batches.

A practical falsifiable gate for a forced future window is now precise: if a prior compatible X,Y and a guaranteed future population k satisfy $K_h(Q,J)<k$ for even one modulus h, the purported whole B3 configuration cannot exist. The gap from Erdős #41 is proving that some such forcing certificate must occur under *only* its cumulative critical-density hypothesis.

## 3. A hostile certificate: all pairwise B3, scalar capacity passes, modular integrality forces failure

Consider the genuine pairwise compatible configuration

$$
X=\{1,2\},\quad Y=\{1000,1003\},\quad
J=[10000,10004]\cap\mathbb Z.
$$

The old cross pair sums and their actual window support are

$$
Q=\{1001,1002,1004,1005\},\qquad
U=Q+J=[11001,11009]\cap\mathbb Z.
$$

The scalar Hall bound allows $|Z|=2$, since $|Q||Z|=8\le9=|U|$. But for modulus h=3, the Q residue populations are $a_0=a_2=2$, $a_1=0$, and each target residue has exactly $C_0=C_1=C_2=3$ available positions.

A future point of residue u contributes TWO triples to each of the residues u and u+2, modulo 3. Two future points, irrespective of their residues, must overload at least one of the three boxes by four triples against capacity three, because **any two two-element subsets of a three-element universe intersect**. Therefore

$$
\boxed{K_3(Q,J)=1<2=\left\lfloor|U|/|Q|\right\rfloor.}
$$

The *fractional relaxation* falsely allows two points: assign $v_0=v_1=v_2=2/3$. This meets the true window residue capacities $(J_0,J_1,J_2)=(1,2,2)$ and all three inequalities $N_t=8/3\le3$, with $\sum_rv_r=2$. There is nevertheless **no integer** allocation of total two. The example is an explicit integrality gap between a continuous Fourier/residue linear relaxation and the correct finite arithmetic population constraint.\n\nThis is a rigorous **arrangement-independent** obstruction to a two-point future batch in J. Indeed take $Z=\{10000,10004\}$. All THREE pairwise unions X∪Y, X∪Z, Y∪Z are repetition-permitted B3, but

$$
1+1000+10004=2+1003+10000=11005.
$$

For this Z the type-specific sixth defect is exactly 72, whereas the modulus-three bound already certifies at least 48. The older *whole-envelope* bound $M=8\le|U|=9$ gives zero pressure, and the even coarser diameter bound also gives none. This demonstrates that an **integer residue certificate can force cross-three-block resonance when both ordinary Hall bounds remain silent**.

The configuration is a finite hostile test, not an infinite-density contradiction. It is possible that later blocks adopt other residue patterns and avoid every comparable test; the universal inference is still OPEN.

## 4. Any number of actual old-colour pairs and genuinely located future windows

Let $B_0,\ldots,B_{s-1}$ be disjoint actual finite integer blocks. Choose a family $\mathcal F$ of three-DISTINCT-colour index types $(i,j,k)$, with i<j<k. For each type, retain the *actual* old pair sumset $Q_{ij}=B_i+B_j$ and only the declared future window $J_k\supseteq B_k$. Set

$$
U_{\mathcal F}=\bigcup_{(i,j,k)\in\mathcal F}(Q_{ij}+J_k).
$$

For a modulus h, let $C_t$ count positions of $U_{\mathcal F}$ of residue t and $N_t$ count all actual coloured triples from F of that residue (convolving the actual $B_i,B_j,B_k$ residue populations). Put $M=\sum_tN_t$.

**Theorem C (actual-support multiscale forcing).** Regardless of the positions, cardinalities, and arithmetic patterns of the B_i, the global sixth collision defect obeys

$$
\boxed{
\mathfrak d_6\left(\bigcup_iB_i\right)
\ge36\sum_{\substack{t\bmod h\\C_t>0}}
\left(\frac{N_t^2}{C_t}-N_t\right)_+.
}\tag{MULTISCALE-INTEGER-RESIDUE-PRESSURE}
$$

If the blocks are a partition of a genuine B3 set, then every $N_t\le C_t$ for every possible choice of $\mathcal F$ and h. The theorem allows envelopes of **different colour types to overlap** and counts their demands collectively; its exact actual-support union can be substantially smaller than the coarse sum-of-window envelopes. It can incorporate multiple nonuniform future windows and distinct Q_(ij) without any assumption that the locations form a regular progression.

**Proof.** The selected triple-colour types are disjoint families of unordered triples with ordering weight six. Sum their integer representations and apply the nonnegative sixth-defect ledger, then Cauchy–Schwarz within each residue class on the actual union U_F. No selected coloured triple is duplicated, and other types contribute further nonnegative terms. QED.

This is a **necessary condition and finite certificate framework**. It becomes a proof of a strict normalized-density loss only if one proves that the census of actually populated future windows required by $A(N)\ge cN^{1/3}$ must cause a modular-support overload *for every possible B3 arithmetic organization*. Such a theorem has **not** been proved.

## 5. Next noncircular mathematical obligation

Rather than searching for an arbitrary overlap in a known illegal configuration, the next serious target is an **integer infeasibility theorem over all admissible future residue allocations**, uniformly over changing prefixes and scales:

1. Extract a finite set of actually required future windows from the cumulative density assumption, keeping exact locations and cardinality lower bounds.
2. Construct the prior mixed-pair sumsets Q_(ij) from actual earlier B3 blocks, preserving their residue histograms and integer support gaps.
3. Prove that for at least one bounded or scale-dependent modulus h, the simultaneous integer modular-capacity constraints of Theorem B/C are infeasible for every possible required future batch allocation.
4. Test hostile finite-field and tagged B3 constructions; do not replace integer occupancy by a continuous LP and declare infeasibility without an integer proof.

This explicit integer-residue pressure is a new *approach*, not a demonstrated universal forcing argument. No independent mathematical specialist has certified these notes; verification and protected admission remain governed separately.
