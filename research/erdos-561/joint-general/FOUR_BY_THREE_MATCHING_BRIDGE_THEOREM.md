# Erdős #561: exact heterogeneous FOUR-by-THREE joint residual with unbounded switching surplus

**Date:** 2026-11-22. **Claim status:** mathematical paper UNDER_REVIEW; bounded arithmetic and explicit graph-colouring checks are separate evidence. **Scope:** arbitrary finite simple host graphs and ordinary, non-induced, vertex-disjoint positive star forests. This is an original bounded extension beyond the previously reconstructed three-by-three joint residual result; historical priority is not asserted without a further literature audit. **The full all-profile Erdős #561 conjecture and the unrestricted joint-residual hypothesis in issue #3490 remain OPEN.** No MATHCERT certification is implied by a source merge.

## 1. Notation and an exact algebraic defect identity

For a nonincreasing positive list $x$, let $F(x)$ denote the disjoint union of stars having the listed edge sizes. For original lists $n=(n_1,\ldots,n_s)$ and $m=(m_1,\ldots,m_t)$ put

$$
w_k(n,m)=\max_{i+j=k}(n_i+m_j-1),\qquad
W(n,m)=\sum_{k=2}^{s+t}w_k,\qquad
J_{\rm can}(n,m)=\sum_{k=3}^{s+t}w_k.
$$

Indices are one-based. The source-locked canonical antidiagonal star-host criterion supplies an arbitrary-host **upper bound** of $J_{\rm can}$ for the simultaneous residual problem and of $W$ for the original problem. A genuine arbitrary-host lower bound is still needed.

Say that a graph $Q$ is a *joint residual host* for $(n,m)$ when

$$
Q\to(F(n_2,\ldots,n_s),F(m)),
\qquad
Q\to(F(n),F(m_2,\ldots,m_t)).
$$

Take

$$
n=(a,b,c,1),\qquad m=(d,e,1),
\quad a\ge b\ge c\ge2,\quad d\ge e\ge1.
$$

Set $T=\max(b,c+e-1)$. Direct expansion gives

$$
\begin{aligned}
w_3&=\max(a+e-1,b+d-1),\\
w_4&=\max(a,b+e-1,c+d-1),\\
w_5&=\max(b,c+e-1,d)=\max(T,d),\\
w_6&=\max(c,e),\qquad w_7=1.
\end{aligned}
$$

The source-proved exact *three-by-three* joint residual for the shortened red list $n'=(a-1,b-1,c-1)$ and unchanged blue list $m$ is

$$
J_3(n',m)=w_3+w_4+T+c-4.
$$

Consequently the following is an **exact identity**, not an inequality or a conjecture:

$$
\boxed{
J_{\rm can}(n,m)
=5+J_3(n',m)
 +(d-T)_+ +(e-c)_+,
}
$$

where $(x)_+=\max(0,x)$.

The two explicit positive-part terms measure exactly the failure of a single five-edge matching deletion to recover the complete four-by-three canonical tail.

## 2. Five-edge matching theorem for an arbitrary host

**Lemma A (the decisive graph obstruction).** Let $a\ge b\ge c\ge2$, $f\ge1$ with $c\ge f$, and $e\ge1$. If an arbitrary finite simple graph $Q$ satisfies even the **single** residual relation

$$
Q\to(F(a,b,c,f),F(e,1)),
$$

then its matching number satisfies $\nu(Q)\ge5$.

**Proof.** Colour every edge incident with an arbitrary vertex $v$ BLUE, and all other edges RED. The blue graph has vertex cover $\{v\}$, hence every blue matching has size at most one. The blue target $F(e,1)$ requires a matching of size two and is therefore absent. Arrowing forces a red copy of $F(a,b,c,f)$ wholly inside $Q-v$, for every vertex $v$. Thus

$$
\nu(Q-v)\ge4\quad\text{for every }v,\qquad \nu(Q)\ge4.
$$

Assume for contradiction $\nu(Q)=4$. Then $\nu(Q-v)=4$ for EVERY vertex $v$. Apply the classical Gallai matching-stability/factor-critical characterization componentwise: every nontrivial connected component $C$ of $Q$ has odd order $|C|=2\nu(C)+1$ and admits a maximum matching after deletion of any vertex. The total matching number is four, so at most four nontrivial components exist and the total number of nonisolated vertices is at most

$$
\sum_C(2\nu(C)+1)\le2\cdot4+4=12.
$$

The required full red forest $F(a,b,c,f)$ has at least

$$
(a+1)+(b+1)+(c+1)+(f+1)\ge3+3+3+2=11
$$

distinct nonisolated vertices. Since it must fit in $Q-v$ for **every** nonisolated $v$, $Q$ must have at least twelve nonisolated vertices. Equality is forced throughout. Therefore there are exactly FOUR nontrivial factor-critical components, each of matching number one and order three. A connected factor-critical simple graph on three vertices is $K_3$, so $Q$ is exactly $4K_3$ up to isolated vertices.

But colour all edges of three triangles RED, and all edges of the fourth triangle BLUE. The red graph is supported on only nine vertices, fewer than the eleven required by $F(a,b,c,f)$. The blue graph is supported on only three vertices, fewer than the $e+3\ge4$ vertices required by the disjoint positive stars $F(e,1)$. Neither target occurs, contradicting the assumed arrow. Hence $\nu(Q)\ge5$. QED.

The lemma is an **unrestricted-host** assertion, not a reduction to star-only graphs. The sole possible matching-four exceptional topology is eliminated by an explicit red/blue colouring.

## 3. The exact four-by-three theorem and quantitative nonsharp case

**Theorem B (sharp four-by-three).** Let

$$
n=(a,b,c,f),\quad m=(d,e,1),
\qquad
a\ge b\ge c\ge f\ge1,\quad d\ge e\ge1,
$$

and define the reduced three-leading-arm values

$$
A=a-f+1,\qquad B=b-f+1,\qquad C=c-f+1.
$$

Assume $C\ge2$. Define the **exact matching-deletion deficit**

$$
P(n,m)=\bigl(d-\max(B,C+e-1)\bigr)_+
       +(e-C)_+.
$$

Then for **every** finite simple joint residual host $Q$,

$$
\boxed{
e(Q)\ge J_{\rm can}(n,m)-P(n,m).
}
$$

In particular, whenever

$$
\boxed{
e\le C,\qquad
d\le\max(B,C+e-1),
}
$$

the deficit vanishes and the exact unrestricted-host JOINT residual minimum equals

$$
\boxed{\mathcal J(n,m)=J_{\rm can}(n,m).}
$$

**Proof.** First take $f=1$, so $A=a,B=b,C=c$. By Lemma A applied to the SECOND residual relation

$$
Q\to(F(a,b,c,1),F(e,1)),
$$

there is a matching $M$ with at least five edges. Remove **all** edges in $M$. To see precisely what the remaining graph arrows, colour every removed matching edge RED in any two-colouring. A red star in the original colouring uses at most ONE edge of $M$, because its centre would otherwise meet two distinct edges of a matching. Thus removing $M$ reduces the sizes of the red star components by at most one. Any red copy of $F(a,b,c,1)$ in the extended graph leaves at least a red copy of $F(a-1,b-1,c-1)$ after discarding the final one-edge component; similarly, any red $F(b,c,1)$ leaves $F(b-1,c-1)$. Blue edges are unchanged. Therefore $Q-M$ satisfies BOTH relations

$$
Q-M\to(F(b-1,c-1),F(d,e,1)),
$$

$$
Q-M\to(F(a-1,b-1,c-1),F(e,1)).
$$

These are exactly the joint residual relations for original **three-by-three** lists $n'=(a-1,b-1,c-1)$ and $m=(d,e,1)$. The source-proved full three-by-three joint result gives

$$
e(Q-M)\ge J_3(n',m).
$$

Accounting for the distinct removed matching edges gives

$$
e(Q)\ge |M|+J_3(n',m)\ge5+J_3(n',m)
       =J_{\rm can}(n,m)-P(n,m),
$$

by the algebraic identity in Section 1. If $P=0$, the canonical joint star host matches this lower bound.

Now let $f\ge2$ and assume the result already for the red list $n^-=(a-1,b-1,c-1,f-1)$, whose reduced values $(A,B,C)$ are **unchanged**, so the deficit $P$ is also unchanged. Lemma A again gives a matching $M$ of size at least five. Colour removed matching edges red, as above. Since every original red arm is at least two, $Q-M$ jointly arrows precisely the two residual relations for $(n^-,m)$. The inductive lower bound yields

$$
e(Q-M)\ge J_{\rm can}(n^-,m)-P.
$$

Each of the FIVE non-leading original antidiagonal weights decreases by exactly one when all four red sizes decrease by one, so

$$
J_{\rm can}(n^-,m)=J_{\rm can}(n,m)-5.
$$

Adding $|M|\ge5$ yields the asserted lower bound. Induction closes for every $f\ge1$ with $C\ge2$. QED.

**Important distinction.** Where $P>0$, we have proved the **quantified lower bound** $J_{\rm can}-P$, NOT equality with the canonical joint minimum. We do not silently discard this deficit or assert the unrestricted all-profile joint conjecture.

## 4. Complementary exact regime and the precise remaining coupled deficit

For ANY positive ordered four-star list $n$ and three-star list $m$, define the two separately known exact original size-Ramsey values

$$
S_1=\widehat r(F(n_2,n_3,n_4),F(m))
     =\sum_k w_k(n_{2:},m),
$$

$$
S_2=\widehat r(F(n),F(m_2,m_3))
     =\sum_k w_k(n,m_{2:}).
$$

Here $S_1$ is the **complete source-reconstructed three-by-three ORIGINAL theorem**, while $S_2$ is the **pinned published two-component size-Ramsey theorem**, with the two-component forest on the BLUE side and colour symmetry. Both are unrestricted-host results.

The exact source-proved antidiagonal switching identity says

$$
\sigma(n,m)=J_{\rm can}(n,m)-\max(S_1,S_2)\ge0.
$$

Any joint residual graph arrows both separate targets, so $e(Q)\ge\max(S_1,S_2)=J_{\rm can}-\sigma$. Thus the JOINT residual is automatically **exact** for EVERY four-by-three profile with $\sigma=0$, even where the matching-deletion deficit $P$ above is positive.

For the profile domain of Theorem B, combining this independent bound with the five-edge matching transfer yields the stronger **coupled-deficit theorem**

$$
\boxed{
J_{\rm can}(n,m)-\min\{P(n,m),\sigma(n,m)\}
\ \le\ \mathcal J(n,m)\ \le\ J_{\rm can}(n,m).
}
$$

Hence **either** $P=0$ **or** $\sigma=0$ suffices for sharp joint equality. The two-method positive-deficit region is further reduced by the DUAL BLUE matching bridge in Section 5; see its three-way minimum. These are explicit, computable integer inequalities, not a vague claim of a missing proof. They also preserve the sharp original-transfer conclusions wherever the actual joint minimum is established.

## 5. DUAL blue-matching bridge to the two-component joint theorem

The preceding bound uses the red matching-colour extension. The opposite extension supplies a genuinely different sharp theorem.

Assume the blue second-largest star size satisfies $e\ge2$. For the reduced red values $(A,B,C)$ from Theorem B put

$$
X=\max(B+e-1,C+d-1),\qquad Z=\max(C+e-1,d)
$$

and define the **blue matching-deletion deficit**

$$
\boxed{
P_{\mathrm B}(n,m)
=(A-X)_+ +(B-Z)_+ +(C-e)_+.
}
$$

**Theorem C (dual joint reduction).** Under the exact sorted-positive hypotheses of Theorem B, with $e\ge2$, EVERY arbitrary finite simple joint residual host satisfies

$$
\boxed{e(Q)\ge J_{\rm can}(n,m)-P_{\mathrm B}(n,m).}
$$

In particular the full canonical joint formula is **exact** whenever

$$
A\le\max(B+e-1,C+d-1),\quad
B\le\max(C+e-1,d),\quad
C\le e.
$$

**Proof, base $f=1$.** Lemma A already proves $\nu(Q)\ge5$. Choose a maximum matching $M$ and this time colour every edge in $M$ **BLUE**, rather than red. The two original residual relations imply that $Q-M$ satisfies

$$
Q-M\to(F(b,c,1),F(d-1,e-1)),
$$

$$
Q-M\to(F(a,b,c,1),F(e-1)).
$$

The first follows from the original first residual by deleting its blue final single-edge component and decrementing the other two blue stars; the second follows in exactly the same way from the original second residual. Every blue original star loses at most one edge from the removed matching, while all red edges are unchanged.

These are the two JOINT residual relations for original lists **red** $n=(a,b,c,1)$ and **blue** $m'=(d-1,e-1)$, of lengths four and two. The source-proved two-component residual bridge in \`THREE_BY_THREE_JOINT_RECONSTRUCTION.md\`, Lemma 1, applies after exchanging the colours. It proves an unrestricted-host lower

$$
e(Q-M)\ge J_{\rm can}(n,(d-1,e-1)).
$$

The relevant original five joint antidiagonal entries for $(n,(d,e,1))$ are

$$
\begin{aligned}
w_3&=\max(a+e-1,b+d-1),\\
w_4&=\max(a,b+e-1,c+d-1)=\max(a,X),\\
w_5&=\max(b,c+e-1,d)=\max(b,Z),\\
w_6&=\max(c,e),\qquad w_7=1.
\end{aligned}
$$

The FOUR joint antidiagonal entries for the shortened blue pair $(d-1,e-1)$ are

$$
(w_3-1,\ X-1,\ Z-1,\ e-1).
$$

Summing them proves the **exact dual algebraic identity**

$$
\boxed{
J_{\rm can}(n,m)
=5+J_{\rm can}(n,(d-1,e-1))
 +(a-X)_+ +(b-Z)_+ +(c-e)_+.
}
$$

Hence $e(Q)\ge |M|+e(Q-M)\ge5+J_{\rm can}(n,m')=J_{\rm can}(n,m)-P_{\mathrm B}$.

**For $f>1$**, colour and delete a five-or-more-edge matching RED, as in Theorem B, to obtain a smaller four-by-three JOINT host with all four red sizes decremented by one. Repeat until the final red arm becomes one. This takes $f-1$ steps, subtracting exactly five from the canonical joint tail at each step. The final red profile is $(A,B,C,1)$ with the **same** $(d,e,1)$ blue list, to which the dual base proof just established applies. Since $P_{\mathrm B}$ depends only on $A,B,C,d,e$, it is unchanged during this red decrement sequence. Summing the distinct edges removed proves the exact claimed bound for arbitrary $f$. QED.

### The three-way coupled deficit

Retain $P_{\mathrm R}=P$ from Theorem B and the switching surplus $\sigma$ from Section 4. For $e\ge2$ define

$$
\boxed{
\Delta_{\rm joint}=\min(P_{\mathrm R},P_{\mathrm B},\sigma).
}
$$

For $e=1$ omit the blue reduction and define $\Delta_{\rm joint}=\min(P_{\mathrm R},\sigma)$.

The sharpest combined lower bound established by these three independent methods is now

$$
\boxed{
J_{\rm can}(n,m)-\Delta_{\rm joint}
\ \le\ \mathcal J(n,m)\ \le\ J_{\rm can}(n,m).
}
$$

Thus if **ANY** of the explicitly computable quantities $P_{\mathrm R}$, $P_{\mathrm B}$ (when legal), or $\sigma$ vanishes, we have proved the full JOINT equality for arbitrary graph hosts. In the declared exact 14,520-parameter base grid, this additional BLUE reduction resolves **838** profiles that survived the previous RED matching and individual-residual bounds; **458** base profiles remain open under all three routes. These counts are FINITE arithmetic classification within the declared grid, not a claim about all integer parameters.

### A second genuinely heterogeneous family with unbounded switching surplus, closed by BLUE matching

For every $h\ge1$, take

$$
\widetilde n_h=(4h,2h,2h,1),\qquad
\widetilde m_h=(4h,3h,1).
$$

The original antidiagonal weights are

$$
(8h-1,\,7h-1,\,6h-1,\,5h-1,\,3h,\,1).
$$

The direct RED matching bridge loses $P_{\mathrm R}=h$ edges, and each separate residual bound also loses $\sigma=h$ edges. **Nevertheless the BLUE matching deficit is exactly zero** for every $h$:

$$
P_{\mathrm B}=0.
$$

Theorem C therefore establishes the full unrestricted-host JOINT value

$$
\boxed{\mathcal J(\widetilde n_h,\widetilde m_h)=21h-2,}
$$

although each separate residual value is only $20h-2$.

The ORIGINAL canonical size is $W=29h-3$. For $h\ge2$, the protected degree-core transfer applies with $D=8h-2$, because

$$
D(D+1)-2(W-1)=64h^2-82h+10>0
\qquad (h\ge2).
$$

Therefore

$$
\boxed{
\widehat r(F(4h,2h,2h,1),F(4h,3h,1))=29h-3
\quad\text{for all }h\ge2.
}
$$

The JOINT formula is proved also for $h=1$; **the ORIGINAL $h=1$ value is not promoted by this particular transfer**. This is a second unbounded-switching, genuinely nonuniform four-versus-three family, complementary to the RED bridge family in Section 7.

## 6. ORIGINAL size-Ramsey transfer, with no extra induction

Write $W=W(n,m)$, $J=J_{\rm can}(n,m)$, and $D=a+d-2$. In the parameter range of Theorem B with $P=0$, the existing protected \`GENERAL_CORE_ORIGINAL_TRANSFER.md\` proves the ORIGINAL equality under any of its independent sufficient conditions. In particular, for $a,d\ge2$,

$$
\boxed{W\le D(D+1)/2
\quad\Longrightarrow\quad
\widehat r(F(n),F(m))=W.}
$$

A convenient unrestricted parameter criterion is $a+d\ge14$, because here the original list lengths are four and three, so there are SIX original antidiagonal weights, each at most $D+1$; thus $W\le6(D+1)\le D(D+1)/2$ whenever $D\ge12$. Also, if both leading values $a,d$ are odd, the protected even-cap splitting argument transfers joint sharpness without the numerical criterion.

For clarity, the degree-core argument is this. A hypothetical original-arrowing host with $E\le W-1$ has every one-vertex deletion jointly arrowing the two residual relations. Sharp joint lower $e(G-v)\ge J$ therefore gives $d_G(v)\le E-J\le D$. If a red/blue partition with degree caps $(a-1,d-1)$ existed, the colouring would avoid both leading stars. The protected degree-cap splitting theorem ensures that **failure** of such a partition requires at least $D+1$ vertices of degree $D$. Handshaking forces $2E\ge D(D+1)$, contradicting $E\le W-1$ whenever $W\le D(D+1)/2$. Canonical original star host gives the upper bound. For blue leading $d=1$, the complete matching-side original formula already applies separately and no use of a positive blue degree cap is needed.

## 7. A genuinely heterogeneous four-by-three infinite family with UNBOUNDED switching surplus

For every integer $h\ge1$, take the original lists

$$
n_h=(6h,4h,4h,1),\qquad m_h=(4h,3h,1).
$$

They satisfy $C=4h\ge2$, $e=3h\le4h$, and

$$
d=4h\le\max(4h,4h+3h-1).
$$

Theorem B therefore proves the sharp JOINT residual lower for **arbitrary finite simple hosts**.

The six original antidiagonal weights are

$$
(w_2,w_3,w_4,w_5,w_6,w_7)
=(10h-1,\,9h-1,\,8h-1,\,7h-1,\,4h,\,1).
$$

Consequently

$$
\boxed{\mathcal J(n_h,m_h)=28h-2.}
$$

**Both separately necessary residual size bounds are strictly smaller:**

$$
\sum_k w_k(n_{h,2:},m_h)
=\sum_k w_k(n_h,m_{h,2:})=27h-2.
$$

Hence the exact **switching surplus** is

$$
\boxed{\sigma_h=h,}
$$

unbounded as $h$ grows. The proof recovers this otherwise missing surplus with a single five-edge matching transfer to sharp three-by-three joint residuals.

The ORIGINAL canonical value is $W=38h-3$. Here $D=10h-2$ and

$$
D(D+1)-2(W-1)
=(10h-2)(10h-1)-2(38h-4)
=(h-1)(100h-6)+4>0.
$$

Thus the degree-core criterion is satisfied for **every** $h\ge1$, including the smallest case. Therefore

$$
\boxed{
\widehat r(F(6h,4h,4h,1),F(4h,3h,1))=38h-3
\quad\text{for all }h\ge1.
}
$$

This is an **unbounded, nonuniform FOUR-BY-THREE original Ramsey family** with proven switching surplus increasing linearly. It is not an all-profile theorem.

## 8. BLUE-minimum induction: remove the one-edge-tail restriction from the four-by-three theorem

The preceding RED and BLUE matching bridges were stated with smallest blue arm equal to one. This restriction is unnecessary for the **joint-residual inequality** and all of its sharp-parameter consequences.

**Theorem D (general BLUE terminal arm).** Let original red and blue profiles be

$
n=(a,b,c,f),\qquad m=(d,e,g),
$

with both lists positive and nonincreasing, $c\ge f+1$ and $d\ge e\ge g\ge1$. Define the **reduced blue list**

$
m^{\flat}=(d-g+1,e-g+1,1).
$

Form the old RED and BLUE matching deficits $P_{\mathrm R}(n,m^{\flat})$, $P_{\mathrm B}(n,m^{\flat})$ (when $e-g+1\ge2$), and the exact separate-residual switching surplus $\sigma(n,m^{\flat})$ as in Sections 4–5. Set

$
\Delta^{\flat}=
\begin{cases}
\min(P_{\mathrm R},P_{\mathrm B},\sigma),& e-g+1\ge2,\\
\min(P_{\mathrm R},\sigma),& e-g+1=1.
\end{cases}
$

Then for every finite simple **joint residual** host $Q$ for $(n,m)$,

$
\boxed{e(Q)\ge J_{\rm can}(n,m)-\Delta^{\flat}.}
$

In particular, if **any** of the reduced-profile deficits is zero, the exact full antidiagonal JOINT formula holds even when **all three blue arms are at least two**. No assumption is placed on the topology of $Q$.

**Proof by induction on the smallest blue arm $g$.** The base $g=1$ is Theorems B/C together with the separate-residual lower in Sections 3–5.

Assume $g\ge2$. The SECOND joint-residual arrowing relation reads

$
Q\to(F(a,b,c,f),F(e,g)).
$

Colour all edges at an arbitrary vertex $v$ blue and all others red. The blue graph has a vertex cover of size one, while the blue target has TWO vertex-disjoint positive stars and therefore a matching of size two. Consequently every $Q-v$ contains the entire red original four-star forest $F(n)$, implying $\nu(Q-v)\ge4$. If $\nu(Q)=4$, Gallai's matching-stability theorem again bounds the nonisolated vertex count by twelve. Since $c\ge f+1\ge2$, the red forest requires at least eleven distinct vertices after every nonisolated vertex deletion; exactly as in Lemma A, the only possible graph is $4K_3$, up to isolates. Colour three triangles wholly red and one wholly blue. The red support has only nine vertices, and the blue support only three; $F(e,g)$ needs at least four vertices, so this colouring avoids BOTH targets. This contradiction proves

$
\boxed{\nu(Q)\ge5\quad\text{also for every }g\ge2.}
$

Remove a maximum matching $M$ of at least five edges and colour every removed edge BLUE. For any two-colouring of $Q-M$, a blue star in a copy of either residual target uses at most one matching edge, so removing $M$ reduces each blue star size by at most one. The red targets are unchanged. Thus the two arrowing relations for $Q$ imply exactly the two residual relations for the same original red $n$ and the shortened blue list

$
m^-=(d-1,e-1,g-1).
$

All three blue arm sizes remain positive because $g\ge2$. Therefore $Q-M$ is a JOINT host for $(n,m^-)$, to which the induction hypothesis applies. Its reduced blue list is unchanged:

$
(d-1-(g-1)+1,\ e-1-(g-1)+1,\ 1)
=m^{\flat}.
$

Hence the deficit $\Delta^{\flat}$ is the SAME at each step. Each of the five non-leading original antidiagonal weights drops by exactly one under a uniform decrement of all blue sizes, so

$
J_{\rm can}(n,m^-)=J_{\rm can}(n,m)-5.
$

It follows that

$
e(Q)\ge |M|+e(Q-M)
\ge5+[J_{\rm can}(n,m)-5-\Delta^{\flat}]
=J_{\rm can}(n,m)-\Delta^{\flat}.
$

Induction proves the theorem for all $g\ge1$. Canonical joint disjoint-star hosts give the matching upper bound in every zero-deficit case. QED.

### New three-parameter ORIGINAL family with NO one-edge components on either side

For integers $h\ge1$, $r,k\ge0$, let

$
n_{h,r}=(6h+r,4h+r,4h+r,1+r),
\qquad
m_{h,k}=(4h+k,3h+k,1+k).
$

Uniform RED increments of all four arms by $r$ and uniform BLUE increments of all three arms by $k$ preserve the reduced-profile penalties and the exact switching surplus $\sigma=h$. The red bridge remains sharp after red lifting by Theorem B, and Theorem D propagates sharpness through all blue lifts. The five JOINT weights each increase by $r+k$, and the six ORIGINAL weights each increase by $r+k$. Therefore, for all $h\ge1,r,k\ge0$,

$
\boxed{
\mathcal J(n_{h,r},m_{h,k})
=28h-2+5(r+k),\qquad
W_{\rm can}=38h-3+6(r+k),\qquad
\sigma=h.
}
$

For the original size-Ramsey equality, put $x=r+k$ and $D=10h+x-2$. The exact degree-core excess is

$
\begin{aligned}
D(D+1)-2(W_{\rm can}-1)
&=(h-1)(100h-6)+4\\
&\quad +(20h-15)x+x^2>0.
\end{aligned}
$

This is strictly positive for **every** $h\ge1,r,k\ge0$. The source-locked original degree-core transfer therefore proves

$
\boxed{
\widehat r\big(F(n_{h,r}),F(m_{h,k})\big)
=38h-3+6(r+k)
\quad \text{for ALL }h\ge1,r,k\ge0.
}
$

If $r,k\ge1$, **every original star component on BOTH sides has at least two edges**. Thus this is an exact genuinely nonuniform four-versus-three family with neither forest having a one-edge terminal component and with arbitrarily large switching surplus. It is a strict structural extension of the previous one-edge-tail examples.

### Dual-BLUE-switching family, also with all-positive shifts

For $h\ge1,r,k\ge0$, let

$
\widetilde n_{h,r}=(4h+r,2h+r,2h+r,1+r),
\qquad
\widetilde m_{h,k}=(4h+k,3h+k,1+k).
$

The BLUE bridge has zero reduced deficit. The joint result and canonical original value become

$
\boxed{
\mathcal J(\widetilde n_{h,r},\widetilde m_{h,k})
=21h-2+5(r+k),\qquad
\widetilde W_{\rm can}=29h-3+6(r+k),\qquad
\sigma=h.
}
$

Here $D=8h+r+k-2$ and $x=r+k$ give

$
D(D+1)-2(\widetilde W_{\rm can}-1)
=64h^2-82h+10+(16h-15)x+x^2.
$

The ORIGINAL formula is therefore proved when $h\ge2$ (all $r,k\ge0$), or when $h=1$ and $r+k\ge3$. In those regimes,

$
\widehat r\big(F(\widetilde n_{h,r}),F(\widetilde m_{h,k})\big)
=29h-3+6(r+k).
$

The original $h=1,r+k\le2$ cases are NOT claimed sharp from this degree-core argument, although the full JOINT formula is established there.

## 9. NEW equal-bottom-RED extension: two smallest red arms may coincide

The previous four-by-three matching bridge assumed $c\ge f+1$, because its RED matching deletion eventually required a positive three-star target $(a-1,b-1,c-1)$. That condition is **not necessary for the BLUE matching bridge**. When the last two red arms are equal, a different matching guarantee supplies the induction.

### Lemma E.1 — a five-edge matching from eleven red support vertices

Let $n=(a,b,c,f)$ be any nonincreasing positive four-star list with

$
V(n):=a+b+c+f+4\ge11.
$

Let $y,z\ge1$. If a finite simple graph $Q$ arrows

$
Q\to(F(n),F(y,z)),
$

then $\nu(Q)\ge5$, regardless of its topology.

**Proof.** Colour all edges at an arbitrary vertex $v$ BLUE. The blue subgraph has matching number at most one and cannot contain two vertex-disjoint nonempty stars. Thus every $Q-v$ contains a red $F(n)$, implying $\nu(Q-v)\ge4$ for every vertex $v$. If $\nu(Q)=4$, Gallai matching stability says each nontrivial connected component is factor-critical, with $2\nu(C)+1$ nonisolated vertices. Since the matching number sums to four and each nontrivial component has matching number at least one, their total nonisolated vertex number $N$ is at most twelve.

Choose any nonisolated $v$. The red forest surviving in $Q-v$ requires at least $V(n)\ge11$ nonisolated vertices, so $N\ge V(n)+1\ge12$. Consequently $N=12$ and $V(n)=11$; moreover, equality in the factor-critical vertex budget forces exactly four components of matching number one, each a triangle. Hence $Q$ has nontrivial part $4K_3$. Colour three triangles entirely RED and the fourth entirely BLUE. The red graph is supported on only nine vertices, less than $V(n)\ge11$; the blue graph is supported on only three vertices, less than the four required by $F(y,z)$ for positive $y,z$. This avoids both targets, a contradiction. Thus $\nu(Q)\ge5$. QED.

Unlike the previous form of Lemma A, this lemma also applies to **red $(A,B,1,1)$**, provided $A+B\ge5$ (because $V=A+B+6\ge11$).

### Theorem E.2 — full JOINT lower bound with equal final RED arms

Let

$
n=(a,b,f,f),\quad a\ge b\ge f\ge1,
\qquad
m=(d,e,g),\quad d\ge e\ge g\ge1.
$

Put

$
A=a-f+1,\quad B=b-f+1,\qquad
D=d-g+1,\quad E=e-g+1.
$

Assume

$
A+B\ge5,\qquad E\ge2.
$

Then every arbitrary finite simple joint residual host $Q$ for $(n,m)$ satisfies

$
\boxed{
e(Q)\ge J_{\rm can}(n,m)-P_{\rm tie},
}
$

where the **new exact tied-tail BLUE deficit** is

$
\boxed{
P_{\rm tie}
=(A-\max(B+E-1,D))_+ +(B-D)_+.
}
$

Moreover, the exact separately proved original residual lower bounds give

$
\boxed{
J_{\rm can}(n,m)-\min(P_{\rm tie},\sigma(n,m))
\ \le\ \mathcal J(n,m)\ \le\ J_{\rm can}(n,m).
}
$

Therefore if either $P_{\rm tie}=0$ **or** the antidiagonal switching surplus $\sigma(n,m)=0$, then the canonical four-by-three JOINT residual formula is **sharp for all finite simple host graphs**. In particular $P_{\rm tie}=0$ whenever

$
A\le\max(B+E-1,D),\qquad B\le D.
$

**Proof.** First reduce BOTH terminal red and blue arm sizes by uniformly decrementing their entire respective profiles, using five-edge matchings.

A joint host $Q$ satisfies the second residual arrowing condition against blue $F(e,g)$; this has TWO positive stars. At each stage of the RED and BLUE decrements, the current four-star red profile has at least eleven total vertices: the minimal profile reached is $(A,B,1,1)$, with $A+B+6\ge11$. Therefore Lemma E.1 supplies a matching with at least five edges for each intermediate joint host.

If the smallest RED size is $f'>1$, remove any five-or-more-edge matching and colour all its edges RED when extending a colouring. Because a matching meets each vertex at most once, every red star loses at most one edge when its edges are deleted. The result jointly arrows the original RED list with all four arms decremented by one and unchanged blue list. Every one of the five nonleading original antidiagonal weights decreases by exactly one. Induct until the red list becomes $(A,B,1,1)$.

Likewise, if the smallest BLUE size is $g'>1$, remove another matching and colour it BLUE, reducing all three blue sizes uniformly by one while preserving both joint residual arrowing conditions and dropping five nonleading weights by one each. Induct until the blue list becomes $(D,E,1)$.

It suffices to bound the final JOINT host $Q_0$ for

$
n_0=(A,B,1,1),\qquad m_0=(D,E,1).
$

Since $E\ge2$, Lemma E.1 supplies a further matching $M$ of at least five edges. Colour this matching BLUE, and remove it. The result jointly arrows the original RED four-star list $(A,B,1,1)$ against the blue TWO-component list $(D-1,E-1)$, whose entries are strictly positive. The source-proved *two-component JOINT residual bridge* (Lemma 1 in \`THREE_BY_THREE_JOINT_RECONSTRUCTION.md\`, with the colours exchanged) yields

$
e(Q_0-M)\ge J_{\rm can}((A,B,1,1),(D-1,E-1)).
$

The exact four-by-three antidiagonal expansion gives

$
\begin{aligned}
J_{\rm can}((A,B,1,1),(D,E,1))
&=5+J_{\rm can}((A,B,1,1),(D-1,E-1))\\
&\quad +(A-\max(B+E-1,D))_+ +(B-D)_+.
\end{aligned}
$

Thus $e(Q_0)\ge J_{\rm can}(n_0,m_0)-P_{\rm tie}$. Adding at least five removed edges for each uniform decrement gives the same deficit for the original $(n,m)$, because each decrement changes the canonical joint total by exactly five. The independent exact first and second **ORIGINAL** residual theorems give a simultaneous lower $J_{\rm can}-\sigma$; combining the two yields the stated minimum. The canonical joint disjoint-star host supplies the upper bound. QED.

**Boundary discipline:** This proof does **not** claim the RED matching reduction to three-by-three when $c=f$, because that would produce a zero-sized star. It uses only the legal BLUE matching reduction and the established two-component residual result, with the support-size matching lemma carefully re-established for the tied-tail case.

### A third UNBOUNDED switching family, with two equal smallest RED arms

For every integer $h\ge1$ and increments $r,k\ge0$, define

$
n_{h,r}=(4h+r,h+r,1+r,1+r),
\qquad
m_{h,k}=(4h+k,2h+k,1+k).
$

Here the reduced values are $A=4h$, $B=h$, $D=4h$, $E=2h$. We have $A+B=5h\ge5$, $E\ge2$, and

$
P_{\rm tie}
=(4h-\max(3h-1,4h))_+ +(h-4h)_+
=0.
$

The exact six original antidiagonal weights for $r=k=0$ are

$
(8h-1,\ 6h-1,\ 4h,\ 4h,\ 2h,\ 1).
$

Thus for **ALL** $h\ge1,r,k\ge0$, Theorem E.2 proves

$
\boxed{
\mathcal J(n_{h,r},m_{h,k})=16h+5(r+k),
\quad W_{\rm can}=24h-1+6(r+k),
\quad \sigma=h.
}
$

The positive switching surplus grows without bound and the red profile has **two equal trailing arms**, outside the strict-gap condition $c\ge f+1$ of Theorem D.

For the ORIGINAL size-Ramsey number put $x=r+k$ and $D_{\rm lead}=8h+x-2$. The protected general degree-core transfer requires $W_{\rm can}\le D_{\rm lead}(D_{\rm lead}+1)/2$, equivalently

$
D_{\rm lead}(D_{\rm lead}+1)-2W_{\rm can}
=64h^2-72h+4+(16h-15)x+x^2\ge0.
$

This inequality holds for every $h\ge2$, any $x\ge0$, and for $h=1$, every $x\ge2$. Therefore

$
\boxed{
\widehat r(F(n_{h,r}),F(m_{h,k}))
=24h-1+6(r+k)
}
$

for all $h\ge2$ and $r,k\ge0$, **or** $h=1$ and $r+k\ge2$.

In particular, choosing $r,k\ge1$ makes **every star on both sides have at least two edges** and proves sharp ORIGINAL and JOINT formulas for **all** $h\ge1$. The unshifted original case $h=1,r=k=0$ and single-shift original cases $h=1,r+k=1$ are **not promoted** by this degree-core proof, although their JOINT values are sharp.

## 10. Reproducibility and independent-review requirements

The deterministic checker \`verify_four_by_three_matching_bridge.py\` independently computes both original and residual antidiagonal arrays in two indexing conventions; checks the EXACT positive-part deficit for every declared bounded base profile; checks the five-edge red decrement for all declared lifted profiles; validates the sharp parameter region and original core gate; tests $\sigma_h=h$ and all closed forms for a scale grid; and checks a concrete avoiding colouring of the unique matching-four factor-critical candidate $4K_3$ against the **minimal** target forests using a separate exact ordinary, vertex-disjoint star-embedding oracle. The arithmetic and explicit colouring are CHECKED only after replay of the exact committed candidate head.

The all-host proof uses the **classical Gallai factor-critical matching-stability theorem**, the three-by-three JOINT paper reconstruction in \`THREE_BY_THREE_JOINT_RECONSTRUCTION.md\`, the source-locked \`GENERAL_CORE_ORIGINAL_TRANSFER.md\`, and canonical antidiagonal star-host upper results. These dependencies and precise ordinary/non-induced semantics require mathematical review before certification. A passing CI/merging source package is NOT independent mathematical adjudication or MATHCERT.

**Next remaining boundary:** for four red stars and three blue stars outside the vanishing-deficit region, the matching bridge leaves exactly $P>0$ unaccounted edges. A sharper coupled residual lemma must recover these edges or exhibit a genuine counterexample. For general $s,t\ge4$, a corresponding large-matching guarantee beyond the four-by-three geometry is also unresolved. The BLUE-terminal lifting and NEW tied-bottom-red BLUE matching theorem above remove the unit blue-tail limitation and cover red lists with their last two arms EQUAL, under the stated red vertex-support threshold. The positive coupled deficits and unrestricted arbitrary-length conjecture remain open.
