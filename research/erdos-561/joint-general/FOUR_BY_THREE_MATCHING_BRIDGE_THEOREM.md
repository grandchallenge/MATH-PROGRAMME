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

## 4. ORIGINAL size-Ramsey transfer, with no extra induction

Write $W=W(n,m)$, $J=J_{\rm can}(n,m)$, and $D=a+d-2$. In the parameter range of Theorem B with $P=0$, the existing protected \`GENERAL_CORE_ORIGINAL_TRANSFER.md\` proves the ORIGINAL equality under any of its independent sufficient conditions. In particular, for $a,d\ge2$,

$$
\boxed{W\le D(D+1)/2
\quad\Longrightarrow\quad
\widehat r(F(n),F(m))=W.}
$$

A convenient unrestricted parameter criterion is $a+d\ge14$, because here the original list lengths are four and three, so there are SIX original antidiagonal weights, each at most $D+1$; thus $W\le6(D+1)\le D(D+1)/2$ whenever $D\ge12$. Also, if both leading values $a,d$ are odd, the protected even-cap splitting argument transfers joint sharpness without the numerical criterion.

For clarity, the degree-core argument is this. A hypothetical original-arrowing host with $E\le W-1$ has every one-vertex deletion jointly arrowing the two residual relations. Sharp joint lower $e(G-v)\ge J$ therefore gives $d_G(v)\le E-J\le D$. If a degree-$(a-1,d-1)$ red/blue partition existed, the colouring would avoid both leading stars. The protected degree-cap splitting theorem ensures that **failure** of such a partition requires at least $D+1$ vertices of degree $D$. Handshaking forces $2E\ge D(D+1)$, contradicting $E\le W-1$ whenever $W\le D(D+1)/2$. Canonical original star host gives the upper bound. For blue leading $d=1$, the complete matching-side original formula already applies separately and no use of a positive blue degree cap is needed.

## 5. A genuinely heterogeneous four-by-three infinite family with UNBOUNDED switching surplus

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

## 6. Reproducibility and independent-review requirements

The deterministic checker \`verify_four_by_three_matching_bridge.py\` independently computes both original and residual antidiagonal arrays in two indexing conventions; checks the EXACT positive-part deficit for every declared bounded base profile; checks the five-edge red decrement for all declared lifted profiles; validates the sharp parameter region and original core gate; tests $\sigma_h=h$ and all closed forms for a scale grid; and checks a concrete avoiding colouring of the unique matching-four factor-critical candidate $4K_3$ against the **minimal** target forests using a separate exact ordinary, vertex-disjoint star-embedding oracle. The arithmetic and explicit colouring are CHECKED only after replay of the exact committed candidate head.

The all-host proof uses the **classical Gallai factor-critical matching-stability theorem**, the three-by-three JOINT paper reconstruction in \`THREE_BY_THREE_JOINT_RECONSTRUCTION.md\`, the source-locked \`GENERAL_CORE_ORIGINAL_TRANSFER.md\`, and canonical antidiagonal star-host upper results. These dependencies and precise ordinary/non-induced semantics require mathematical review before certification. A passing CI/merging source package is NOT independent mathematical adjudication or MATHCERT.

**Next remaining boundary:** for four red stars and three blue stars outside the vanishing-deficit region, the matching bridge leaves exactly $P>0$ unaccounted edges. A sharper coupled residual lemma must recover these edges or exhibit a genuine counterexample. For general $s,t\ge4$, a corresponding large-matching guarantee beyond the four-by-three geometry is also unresolved.
