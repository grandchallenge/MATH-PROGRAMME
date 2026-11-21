# Erdős #561 — exact ALL uniform star forests via one spare Vizing class

**Research date:** 2026-11-21. **Status:** independently reconstructed **KNOWN uniform-family theorem**, paper-level proof UNDER_REVIEW, bounded checks CHECKED, NOT MATHCERT. All original host graphs are finite simple, and star forests have ordinary non-induced, vertex-disjoint component embeddings. This source establishes a concise independent proof route, **NOT mathematical novelty or priority for the uniform formula**. Explicit published precedence: Pingting Fu, Zhidan Luo, Zhenyu Ni, *Size Ramsey minimal graphs for uniform star forests*, arXiv:2606.04439v3 (2026-07-04), https://arxiv.org/abs/2606.04439v3 , and prior uniform results cited therein. The base two-component case is Chunlin You, *Size Ramsey numbers of star forests with two components on one side*, arXiv:2610.25958v1 (2026-10-19), https://arxiv.org/abs/2610.25958v1 . Our proof is an additional self-contained **Vizing smallest-class** argument reducing the higher-component case to that pinned base. The full heterogeneous Erdős #561 conjecture remains OPEN.

## Theorem 0 — EVERY pair of uniform positive star sizes, all component counts

Let $a,b\ge1$ and $s,t\ge3$ be arbitrary integers. Let $F(a^s)$ denote $s$ vertex-disjoint stars, each with exactly $a$ edges. Write

$$
R=a+b-1.
$$

Then for **all** such parameter values, with no parity, equality, or graph topology restriction,

$$
\boxed{
\mathcal J((a^s),(b^t))=(s+t-2)R,
\qquad
\widehat r(F(a^s),F(b^t))=(s+t-1)R.
}
$$

This is exactly the established uniform-star-forest formula, together with a sharp simultaneous joint-residual statement. Below is an independent constructive proof for arbitrary simple host graphs.

### Lemma 0.A — universal smallest-spare-matching degree gate

Let $a,b\ge1$, $A=a-1$, $B=b-1$, $D=A+B$, and $R=D+1=a+b-1$. For any $p,q\ge1$, any finite simple graph $G$ with

$$
\Delta(G)\le D,
\qquad
e(G)<(p+q-1)R,
$$

admits a red/blue edge colouring containing **neither** red $F(a^p)$ nor blue $F(b^q)$.

**Proof.** Vizing's edge-colouring theorem gives a proper edge colouring of $G$ with at most $\Delta(G)+1\le D+1=R$ classes. Adjoin empty classes if necessary to obtain **exactly $R$ named matching classes**. Select a **smallest** class $M$ and reserve it as the *spare class*. Since the $R$ classes partition the edges,

$$
|M|\le\frac{e(G)}{R}<p+q-1
\quad\Longrightarrow\quad
|M|\le p+q-2.
$$

Arbitrarily divide the remaining $D=A+B$ matching classes into $A$ **RED base classes** and $B$ **BLUE base classes**. This base colouring has red degree at most $A$ and blue degree at most $B$ at EVERY vertex.

Consider a spare edge $xy\in M$. Because $M$ is a matching, no other spare edge touches either endpoint. At either endpoint $v\in\{x,y\}$, the original graph has at most $D$ incident edges and one belongs to $M$. Thus at most $D-1$ of the $D$ base matching classes occur at $v$. **At least one base class is missing.** Therefore $v$ has at least ONE *safe spare colour*: colour $xy$ red if it is missing a red base class (red degree stays at most $A$), or blue if it is missing a blue base class (blue degree stays at most $B$). When $A=0$ or $B=0$, the corresponding empty group cannot be missing, but the nonempty group necessarily supplies a safe colour whenever a spare edge exists; the same reasoning applies.

If the two endpoints share a safe colour, assign it to $xy$ and create **no cap violation**.

Otherwise their safe-colour sets are disjoint: one endpoint permits only RED safely and the other only BLUE. We may choose either colour for $xy$:
- Colouring it RED exceeds the red cap at exactly ONE endpoint, by one (red degree becomes $A+1=a$), while staying below the blue cap everywhere.
- Colouring it BLUE exceeds the blue cap at exactly ONE endpoint, by one (blue degree becomes $B+1=b$), while staying below the red cap everywhere.

Each *conflicting* spare edge therefore produces **at most one forbidden-size star centre in a freely chosen colour**, and distinct spare edges have no common endpoints. There are at most $|M|\le p+q-2$ such independently assignable defects.

Assign their chosen colours so that **at most $p-1$ centres have red degree $a$** and **at most $q-1$ centres have blue degree $b$**. This is always possible because the sum of these two capacities is $p+q-2$. Every other vertex has red degree at most $a-1$ and blue degree at most $b-1$.

A red copy of $F(a^p)$ would need $p$ distinct centres having at least $a$ red incident edges; a blue copy of $F(b^q)$ would need $q$ distinct centres having at least $b$ blue incident edges. Both are excluded. This constructs the required avoiding colouring of the original arbitrary simple graph. QED.

**Key invariant:** the smallest proper-colour class costs at most $e(G)/(a+b-1)$ edges; each spare edge can create at most ONE dangerous degree-cap violation, and its colour is independently selectable. This removes **every parity obstruction**, even in nonbipartite class-two graphs.

### Corollary 0.B — necessary large degree below the canonical budget

Under the preceding hypotheses, if $G\to(F(a^p),F(b^q))$ and $e(G)<(p+q-1)R$, then necessarily

$$
\boxed{\Delta(G)\ge R=a+b-1.}
$$

Otherwise Lemma 0.A supplies a colouring avoiding both target forests, contradicting arrowing.

### Proof of sharp JOINT residual for all uniform lengths

The canonical joint host is $s+t-2$ disjoint stars, each with $R$ edges. Its arrowing is established by the ordinary antidiagonal star-host criterion, and its edge count provides the upper bound.

For the lower bound, induct on $s\ge3$ with **arbitrary fixed $t\ge3$**. The base case $s=3$ follows directly from Chunlin You's pinned **two-component** theorem: the first residual relation is

$$
Q\to(F(a^2),F(b^t)),
$$

whose size Ramsey lower bound is $(t+1)R=(s+t-2)R$. Thus the joint statement is already sharp for $s=3$, independently of any proposed full three-component proof.

Now suppose $s\ge4$ and $Q$ jointly arrows the residuals of $(a^s),(b^t)$. Write $J=(s+t-2)R$. Assume for contradiction that $e(Q)<J$. The **first** residual arrows red $F(a^{s-1})$ against blue $F(b^t)$, so Lemma 0.B with $p=s-1,q=t$ forces a vertex $v$ of degree at least $R$.

For either of the two residual relations, colour all edges touching $v$ red in a hypothetical extension of a colouring of $Q-v$. Any red copy of the relevant forest contains at most one component meeting $v$, so the remaining red components yield the corresponding smaller residual target entirely within $Q-v$. Blue cannot use an edge touching $v$. Consequently

$$
Q-v\to(F(a^{s-2}),F(b^t)),
\qquad
Q-v\to(F(a^{s-1}),F(b^{t-1})).
$$

These are precisely the two residual relations for uniform original lengths $(s-1,t)$. Induction gives $e(Q-v)\ge(s+t-3)R$. Therefore

$$
e(Q)=d_Q(v)+e(Q-v)\ge R+(s+t-3)R=J,
$$

a contradiction. The joint residual theorem is proved for every $s,t$.

### Proof of the ORIGINAL uniform formula

Let $G$ arrow the ORIGINAL pair $F(a^s),F(b^t)$, and put $W=(s+t-1)R$. If $e(G)<W$, Lemma 0.B applied with $p=s,q=t$ forces a vertex $v$ of degree at least $R$. Every one-vertex deletion of an ORIGINAL Ramsey host arrows BOTH residual pairs (extend a violating residual colouring by colouring all edges at $v$ red or blue; a putative original copy loses at most one component). Hence $G-v$ satisfies the newly proved sharp joint residual and has at least $(s+t-2)R$ edges. Thus

$$
e(G)=d_G(v)+e(G-v)\ge R+(s+t-2)R=W,
$$

contradiction. The canonical original host of $s+t-1$ disjoint $R$-edge stars supplies the matching upper bound. QED.

## Alternative structural proofs for equal and same-parity arm sizes

The elementary Euler-tour and two-factor/Hall constructions in the remainder are additional **independent degree-defect budget arguments** for the narrower same-parity subfamilies. They are not needed for the general uniform theorem above. They remain useful as explicit structural explanations of what proper edge-colour class defects measure in saturated regular components.

Write $F(u^p)$ for $p$ vertex-disjoint copies of a star having $u$ edges. Let $s,t\ge3$ and $a,b\ge2$. Put

$$
R=a+b-1,\qquad D=R-1=a+b-2.
$$

The canonical antidiagonal weights for original $n=(a^s)$ and $m=(b^t)$ are all equal to $R$, with $s+t-1$ original diagonals and $s+t-2$ joint-residual diagonals.

## Theorem A — alternative exact same-parity uniform families

Assume **either** of these independent conditions:

1. $a$ and $b$ are both odd, not necessarily equal; **or**
2. $a$ and $b$ are both even, **not necessarily equal**.

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

Every vertex outside these exceptional centres has **both** red and blue degrees at most $u-1$. Hence every red star with $u$ edges must be centred at a red exceptional centre, of which there are fewer than $p$, while every blue star with $u$ edges must be centred at a blue exceptional centre, of which there are fewer than $q$. Neither target forest can occur. QED.

The lemma makes no assumption of connectedness, absence of bridges, bipartiteness, factor criticality, or existence of a proper edge colouring with $D$ colours. **Odd cycles for $u=2$ are the simplest exceptional components**; for higher even $u$, the proof automatically charges an odd-sized saturated regular component of degree $D$ at least $(u-1)R$ edges.

### Lemma C — unequal EVEN star sizes by two-factor defect budgeting

Let $a,b\ge2$ be **arbitrary even integers**, possibly unequal, and write

$$
A=a-1,\quad B=b-1,\quad D=A+B,\quad R=D+1=a+b-1.
$$

Then for any positive integers $p,q$ and **any finite simple graph** $G$ satisfying

$$
\Delta(G)\le D,\qquad e(G)<(p+q-1)R,
$$

there is a red/blue edge colouring avoiding red $F(a^p)$ and blue $F(b^q)$.

**Proof (fully constructive).**

Because $a,b$ are even, $A$ and $B$ are positive **odd** integers, so $D$ is even. Form a loopless **regular multigraph completion** $\widetilde G$ by taking two disjoint copies of $G$ and adding exactly $D-d_G(v)$ parallel edges between corresponding vertices $v$ and $v'$ across the two copies. Every vertex of $\widetilde G$ has degree exactly $D$, and **each vertex of the first copy of $G$ with original degree below $D$ is incident to at least one added completion edge**. Vertices originally saturated at degree $D$ have no completion edges.

A regular multigraph of even degree $D$ decomposes into exactly $D/2$ spanning two-factors. For completeness, orient the edges of each connected component along Euler circuits. Every vertex then has indegree and outdegree $D/2$. Replace vertex $v$ by a left and right copy; represent each directed edge $v\to w$ by a bipartite edge $v_L w_R$. This is a regular bipartite multigraph of degree $D/2$, which decomposes into $D/2$ perfect matchings by Hall's theorem. Each matching corresponds to a directed cycle cover and therefore a spanning two-factor of $\widetilde G$. Two-cycles made of parallel edges are permitted and are **even**, so they cause no parity exception.

Colour every edge in $(A-1)/2$ of these two-factors RED and every edge in $(B-1)/2$ other two-factors BLUE. Exactly ONE spanning two-factor remains uncoloured. Each of its components is a cycle. Along **each** leftover cycle, colour its edges alternately red and blue:

- On an even cycle, every vertex receives one additional red and one additional blue edge. Its degrees in the complete multigraph are exactly $(A,B)$.
- On an odd cycle, choose any vertex of that cycle as an exception and begin the alternation there. Every other vertex receives one additional edge of each colour and has full multigraph degrees $(A,B)$. At the exceptional vertex the full degrees are **either** $(A+1,B-1)$ **or** $(A-1,B+1)$, at our independent choice by reversing the alternating colours.

We now choose the exception for each odd cycle so that, after deleting all completion edges and the entire second copy, only a small number of potentially forbidden star centres remain in the original $G$.

If the odd leftover cycle visits a vertex of the **second copy**, select such a vertex as its exception. It does not matter that this vertex may exceed a colour cap, because we ultimately restrict the colouring to the first copy.

Otherwise, if the odd cycle visits an **unsaturated original vertex** $v$ with $d_G(v)<D$, choose $v$ as the exception. This vertex has at least one incident completion edge. If one such edge belongs to a previously red or blue two-factor, choose the **same colour** for the exception: the full degree surplus of one in that colour disappears when the completion edge is removed. If all its completion edges lie in the leftover cycle, choose either exception colour; both leftover cycle edges at the exception are coloured with that selected colour, and at least one is removed. Consequently the restricted original colour degrees at $v$ are at most $(A,B)$.

Only odd leftover cycles whose **every vertex lies in the first copy and was saturated at degree $D$ in $G$** remain unabsorbed. Such an odd cycle has **at least three vertices**, because $G$ is simple and has neither loops nor parallel edges in its original first copy. Different cycles of one two-factor are vertex-disjoint. Therefore, if $k$ is the number of unabsorbed odd cycles and $Z$ is the set of vertices of degree $D$ in the original graph,

$$
|Z|\ge3k.
$$

The original degree sum yields

$$
2e(G)\ge D|Z|\ge3Dk,
$$

hence

$$
e(G)\ge \frac{3D}{2}k\ge(D+1)k=Rk,
$$

since $D\ge2$ gives $3D/2\ge D+1$. Using the assumed strict edge budget,

$$
kR\le e(G)<(p+q-1)R,
\qquad k\le p+q-2.
$$

Choose the independent exception colours of these $k$ unabsorbed odd cycles so that **at most $p-1$ are red exceptions** and **at most $q-1$ are blue exceptions**. Every other original vertex has red degree at most $A=a-1$ and blue degree at most $B=b-1$. Each unabsorbed red exception is the **only possible centre of a red star with $a$ edges in its leftover odd cycle**, and each blue exception similarly the only possible centre of a blue star with $b$ edges. With fewer than $p$ red eligible centres and fewer than $q$ blue eligible centres, neither requested vertex-disjoint star forest can exist. This proves the avoiding colouring on the arbitrary original simple graph $G$. QED.

This strengthens the equal-even Euler argument of Lemma B: the odd-cycle exceptions in the last two-factor need not correspond to entire regular connected components, but **each surviving exception is charged to three vertices of degree $D$ and costs at least $R$ distinct original edge incidences in the handshake bound**. The completion's second copy is a proof device; no parallel edge is introduced into the original host or either Ramsey target.

### Lemma D — a uniform leading-degree gate

Under either condition of Theorem A, a graph $G$ of fewer than $(p+q-1)R$ edges satisfying

$$
G\to(F(a^p),F(b^q))
$$

must have a vertex of degree at least $R=a+b-1$.

**If both $a,b$ are odd:** the two positive degree caps $a-1$ and $b-1$ are even, with sum $D$. The previously protected universal even-cap splitting theorem, \`EVEN_CAP_DEGREE_SPLITTING_THEOREM.md\`, partitions the edges of EVERY graph of maximum degree at most $D$ into red degree at most $a-1$ and blue degree at most $b-1$. Such a colouring avoids BOTH leading star sizes, regardless of edge count. Therefore any arrowing graph must have degree at least $D+1=R$.

**If both $a,b$ are even:** a graph with degree at most $D=a+b-2$ and fewer than $(p+q-1)R$ edges admits the avoiding colouring constructed in Lemma C. This includes the earlier equal-even Lemma B as a special case. Therefore any arrowing graph with fewer edges has degree at least $R$.

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

Apply Lemma D with $p=s-1$, $q=t$ and threshold $(p+q-1)R=(s+t-2)R=J$. Since $e(Q)<J$, there exists a vertex $v$ of degree at least $R$.

For *every* vertex $v$, the two residual arrowing relations survive deletion in the appropriate form when all edges at $v$ are coloured RED: the first red target of $s-1$ disjoint stars of size $a$ loses at most one component, leaving at least $s-2$ red stars of size $a$ in $Q-v$, while the second red target of $s$ such stars leaves at least $s-1$. Thus

$$
Q-v\to(F(a^{s-2}),F(b^t)),
\qquad
Q-v\to(F(a^{s-1}),F(b^{t-1})).
$$

These are precisely the two joint residual relations for original lengths $(s-1,t)$. By induction,

$$
e(Q-v)\ge(s+t-3)R.
$$

Adding the at least $R$ distinct edges incident to $v$ gives $e(Q)\ge(s+t-2)R=J$, a contradiction. Hence the lower is proved for all $s$. The canonical antidiagonal star host of $s+t-2$ disjoint stars of size $R$ arrows both residuals and supplies the upper. QED.

### ORIGINAL size Ramsey proof

Take any $G\to(F(a^s),F(b^t))$, and put $W=(s+t-1)R$. Suppose $e(G)<W$. Lemma D with $p=s,q=t$ forces $\Delta(G)\ge R$. Pick a vertex $v$ of degree at least $R$.

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

This theorem proves complete original and joint formulas for **arbitrarily large, genuinely nonmatching star forests on BOTH sides**, including **all same-parity uniform arm pairs**: identical or unequal, even-even or odd-odd. For equal even arms, the new mechanism is a *budgeted Euler-tour one-defect cap splitter*. For unequal even arms, a two-factorization of an even-regular multigraph completion charges each unabsorbable odd-cycle defect to at least three saturated original vertices, recovering the same leading-weight edge budget. It converts a local degree-cap obstruction into an explicit global edge lower bound and then into a component-count induction.

The verifier \`verify_uniform_star_erdos561.py\` independently computes all original/joint antidiagonal sums over a declared broad grid in $s,t,a,b$, validates the exact inductive thresholds and exceptional component cost inequalities, and exhausts complete red-arm allocations for several small canonical original and joint star hosts. A separate bounded graph-atlas audit checks the Euler defect splitter on all simple graphs of at most six vertices with maximum degree at most $2u-2$, and checks its exceptional-core count prediction, using a standard-library exhaustive simple-graph enumerator. These checks are corroborative of the proof, not a finite substitute for its graph-theoretic universal quantifier.

**Paper theorem claim UNDER_REVIEW; finite source checks CHECKED.** Original all-component-count Erdős #561 for arbitrary nonuniform star lists remains unresolved, as do the mixed-parity uniform families not explicitly included here. No MATHCERT certificate or external novelty claim is issued.
