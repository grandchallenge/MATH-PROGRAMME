# Erdős #561 — exact all-component-count uniform star forests by Euler defect budgeting

**Research date:** 2026-11-21. **Status:** new paper theorem UNDER_REVIEW, bounded arithmetic checks CHECKED. All hosts are arbitrary finite simple graphs; forest copies are ordinary, non-induced, and vertex-disjoint. This establishes an infinite class with **both component counts unbounded and every star nontrivial**, but NOT the unrestricted Erdős #561 conjecture for heterogeneous original star sizes. It is independent of the public 2026-10-21 three-component proposed proof and uses only the published pinned two-component result (Chunlin You, arXiv:2610.25958v1) plus the existing protected even-cap splitting theorem for odd arm sizes. The equal-even-arm case has an elementary Euler-tour proof given in full below.

Write $F(u^p)$ for $p$ vertex-disjoint copies of a star having $u$ edges. Let $s,t\ge3$ and $a,b\ge2$. Put

$$
R=a+b-1,\qquad D=R-1=a+b-2.
$$

The canonical antidiagonal weights for original $n=(a^s)$ and $m=(b^t)$ are all equal to $R$, with $s+t-1$ original diagonals and $s+t-2$ joint-residual diagonals.

## Theorem A — exact arbitrary-host all-length uniform families

Assume **either** of these independent conditions:

1. $a$ and $b$ are both odd, not necessarily equal; **or**
2. $a=b$ is even.

Then **for all integers $s,t\ge3$**, and for arbitrary finite simple graph hosts,

$$
\boxed{\mathcal J((a^s),(b^t))=(s+t-2)(a+b-1)}
$$

and

$$
\boxed{\widehat r(F(a^s),F(b^t))=(s+t-1)(a+b-1).}
$$

In particular, for EVERY integer $u\ge2$, whether even or odd,

$$
\boxed{
\mathcal J((u^s),(u^t))=(s+t-2)(2u-1),\qquad
\widehat r(F(u^s),F(u^t))=(s+t-1)(2u-1).
}
$$

This is a full solution of the **uniform equal-arm** family for arbitrary component counts, not a claim that arbitrary nonuniform forests are solved.

### Lemma B — an elementary Euler-tour bounded-edge defect theorem

Fix an **even** integer $u\ge2$ and write $D=2u-2$, $R=D+1=2u-1$. Let $p,q\ge1$ and let $G$ be any finite simple graph with

$$
\Delta(G)\le D,\qquad e(G)<(p+q-1)R.
$$

Then there exists a red/blue edge colouring of $G$ containing neither red $F(u^p)$ nor blue $F(u^q)$.

**Proof.** Work independently inside each nontrivial connected component $C$ of $G$.

**Case 1: $C$ contains at least one vertex of odd degree.** Add one auxiliary vertex $z$ and an auxiliary edge from $z$ to **each odd-degree vertex** of $C$. The number of odd-degree vertices is even, so the augmented connected multigraph has all degrees even and an Euler circuit based at $z$. Colour its successive edges alternating red and blue along the Euler traversal, then discard the auxiliary edges. Every original even-degree vertex is exactly balanced between red and blue, because each incoming/outgoing Euler pair has opposite colours; at each original odd-degree vertex the removal of its one auxiliary edge leaves colour degrees differing by one. The only possible alternate-colouring defect at the start/end of an odd-length Euler circuit occurs at the **auxiliary** vertex $z$, not in $G$. Consequently every original vertex has red and blue degrees at most $\lceil d_C(v)/2\rceil\le u-1$, because $d_C(v)\le2u-2$.

**Case 2: $C$ has only even-degree vertices.** Choose an Euler circuit of $C$ and colour its successive edges alternately. If the Euler circuit has even edge count, every vertex is exactly balanced, with both colour degrees $d_C(v)/2\le u-1$.

If the circuit has **odd** edge count, every vertex except the starting vertex is exactly balanced. At the starting vertex one colour has degree $d_C(v)/2+1$, and the other $d_C(v)/2-1$. If any vertex of $C$ has degree strictly below $D$, choose it as the start; since all degrees are even, it has degree at most $D-2$ and the larger colour degree remains at most $(D-2)/2+1=u-1$.

The only remaining **exceptional component** is therefore a connected graph in which every vertex has degree exactly $D$, and the number of edges is odd. Because $G$ is simple, such a component has at least $D+1=R$ vertices and hence at least

$$
\frac{D(D+1)}2=(u-1)R
$$

edges. In such a component, choose any Euler start vertex and alternate the colours: **exactly one vertex** has monochromatic degree $u$ (red OR blue, at our choice by reversing the initial colour), and every other vertex has both colour degrees at most $u-1$. The other colour at the exceptional vertex has degree $u-2$.

Let $k$ be the number of exceptional components. They are edge-disjoint and each costs at least $(u-1)R\ge R$ edges, so

$$
kR\le e(G)<(p+q-1)R,\qquad k\le p+q-2.
$$

Assign the exceptional colours independently among these components so that at most $p-1$ exceptional vertices have red degree $u$ and at most $q-1$ have blue degree $u$. This is possible because $(p-1)+(q-1)\ge k$.

Every vertex outside these exceptional centres has **both** red and blue degrees at most $u-1$. Hence every red $u$-edge star must be centred at a red exceptional centre, of which there are fewer than $p$, while every blue $u$-edge star must be centred at a blue exceptional centre, of which there are fewer than $q$. Neither target forest can occur. QED.

The lemma makes no assumption of connectedness, absence of bridges, bipartiteness, factor criticality, or existence of a proper $D$-edge-colouring. **Odd cycles for $u=2$ are the simplest exceptional components**; for higher even $u$, the proof automatically charges an odd-sized saturated $D$-regular component at least $(u-1)R$ edges.

### Lemma C — a uniform leading-degree gate

Under either condition of Theorem A, a graph $G$ of fewer than $(p+q-1)R$ edges satisfying

$$
G\to(F(a^p),F(b^q))
$$

must have a vertex of degree at least $R=a+b-1$.

**If both $a,b$ are odd:** the two positive degree caps $a-1$ and $b-1$ are even, with sum $D$. The previously protected universal even-cap splitting theorem, \`EVEN_CAP_DEGREE_SPLITTING_THEOREM.md\`, partitions the edges of EVERY graph of maximum degree at most $D$ into red degree at most $a-1$ and blue degree at most $b-1$. Such a colouring avoids BOTH leading star sizes, regardless of edge count. Therefore any arrowing graph must have degree at least $D+1=R$.

**If $a=b=u$ is even:** a graph with degree at most $D=2u-2$ and fewer than $(p+q-1)R$ edges admits the avoiding colouring constructed in Lemma B. Therefore any arrowing graph with fewer edges has degree at least $R$.

This is a **strictly scoped degree gate**. In particular, for even equal star arms, we do not claim that a general bounded-degree graph at a much larger edge count admits such a partition: sufficiently many exceptional odd regular components can force the coloured star-forest property.

### Base case — two-component published theorem, no unverified 3x3 dependency

For $s=3$ and **arbitrary $t\ge3$**, the *first* joint residual relation is

$$
Q\to(F(a^2),F(b^t)).
$$

Chunlin You's pinned exact two-component size Ramsey theorem (arXiv:2610.25958v1) implies immediately

$$
e(Q)\ge(t+1)(a+b-1)=(3+t-2)R.
$$

The canonical antidiagonal joint host has exactly $(t+1)R$ edges, so the joint theorem holds for $s=3$ without any need to import or assume the public October 2026 general 3×3 proposal.

### Inductive JOINT proof for all s,t

Fix any $t\ge3$ and induct on $s\ge3$, using the preceding base $s=3$.

For the induction step, suppose $s\ge4$ and $Q$ jointly arrows original red $F(a^s)$ and blue $F(b^t)$. Let the proposed value be $J=(s+t-2)R$. If $e(Q)\ge J$, the lower bound is proved, so assume instead that $e(Q)<J$.

The **first residual** arrowing relation is

$$
Q\to(F(a^{s-1}),F(b^t)).
$$

Apply Lemma C with $p=s-1$, $q=t$ and threshold $(p+q-1)R=(s+t-2)R=J$. Since $e(Q)<J$, there exists a vertex $v$ of degree at least $R$.

For *every* vertex $v$, the two residual arrowing relations survive deletion in the appropriate form when all edges at $v$ are coloured RED: the first red target of $s-1$ disjoint $a$-stars loses at most one component, leaving at least $s-2$ red $a$-stars in $Q-v$, while the second red target of $s$ such stars leaves at least $s-1$. Thus

$$
Q-v\to(F(a^{s-2}),F(b^t)),
\qquad
Q-v\to(F(a^{s-1}),F(b^{t-1})).
$$

These are precisely the two joint residual relations for original lengths $(s-1,t)$. By induction,

$$
e(Q-v)\ge(s+t-3)R.
$$

Adding the at least $R$ distinct edges incident to $v$ gives $e(Q)\ge(s+t-2)R=J$, a contradiction. Hence the lower is proved for all $s$. The canonical antidiagonal star host of $s+t-2$ disjoint $R$-edge stars arrows both residuals and supplies the upper. QED.

### ORIGINAL size Ramsey proof

Take any $G\to(F(a^s),F(b^t))$, and put $W=(s+t-1)R$. Suppose $e(G)<W$. Lemma C with $p=s,q=t$ forces $\Delta(G)\ge R$. Pick a vertex $v$ of degree at least $R$.

The standard all-incident-edge monochromatic extension argument shows **every** one-vertex deletion of an original Ramsey graph arrows both residual relations for the original lists $(a^s),(b^t)$: an original red/blue forest copy meeting $v$ loses at most one component, and the remaining vertices contain the corresponding residual forest. Our sharp JOINT theorem, already proved for these lengths, therefore gives

$$
e(G-v)\ge(s+t-2)R.
$$

Consequently

$$
e(G)=d_G(v)+e(G-v)\ge R+(s+t-2)R=W,
$$

contradicting the assumed smaller edge count. The canonical original disjoint-star forest of $s+t-1$ copies of $K_{1,R}$ arrows both targets, attaining the lower bound. QED.

## Relevance, checks and exact boundary

This theorem proves complete original and joint formulas for **arbitrarily large, genuinely nonmatching star forests on BOTH sides**, including every pair of identical uniform arm sizes and also **unequal odd uniform sizes**. The new mechanism is a *budgeted Euler-tour one-defect cap splitter*: each exceptional odd saturated regular component contributes at most one centre of a potentially forbidden monochromatic star, and costs at least the full canonical leading weight in edges. It converts a local degree-cap obstruction into an explicit global edge lower bound and then into a component-count induction.

The verifier \`verify_uniform_star_erdos561.py\` independently computes all original/joint antidiagonal sums over a declared broad grid in $s,t,a,b$, validates the exact inductive thresholds and exceptional component cost inequalities, and exhausts complete red-arm allocations for several small canonical original and joint star hosts. A separate bounded graph-atlas audit checks the Euler defect splitter on all simple graphs of at most six vertices with maximum degree at most $2u-2$, and checks its exceptional-core count prediction, using a standard-library exhaustive simple-graph enumerator. These checks are corroborative of the proof, not a finite substitute for its graph-theoretic universal quantifier.

**Paper theorem claim UNDER_REVIEW; finite source checks CHECKED.** Original all-component-count Erdős #561 for arbitrary nonuniform star lists remains unresolved, as do the parity-mixed uniform and unequal-even-uniform families not explicitly included here. No MATHCERT certificate or external novelty claim is issued.
