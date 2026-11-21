# Erdős #561 — exact multi-arm flat-tail joint residual by recolouring budget

**Research date:** 2026-11-21. **Scope:** arbitrary finite simple host graphs with ordinary, non-induced, vertex-disjoint star-forest embeddings. **Mathematical status:** paper-level theorem \`UNDER_REVIEW\`, bounded deterministic corroboration \`CHECKED\`. The general joint-residual inequality (issue #3490) and unrestricted original Erdős #561 conjecture remain OPEN; no MATHCERT certificate is claimed.

Write $F(x_1,\ldots,x_s)$ for disjoint positive-edge stars, and $G\to(R,B)$ for ordinary two-colour Ramsey arrowing. For nonincreasing original lists $n,m$, denote by $\mathcal J(n,m)$ the **minimum number of edges in any finite simple graph jointly satisfying** the two residual relations

$$
G\to(F(n_2,\ldots,n_s),F(m)),
\qquad
G\to(F(n),F(m_2,\ldots,m_t)).
$$

The conjectured value is the sum of the non-leading original antidiagonal maxima; this manuscript establishes that value for a new infinite flat-tail family, including the formerly open one-edge-slack five-blue-star case.

## Theorem A — universal multi-arm recolouring lower bound

Let $t\ge4$, $a\ge2$, $c\ge1$, and $b\ge c$. Set

$$
n=(a,1,1),\quad m=(b,\underbrace{c,\ldots,c}_{t-1}),\quad
r=\min\{a-1,c\},\quad h=b+(t-1)c.
$$

**Any finite simple graph** jointly arrowing the two residual pairs has at least

$$
\boxed{\mathcal J(n,m)\ge 2b+(t-1)c+(t-3)\min\{a-1,c\}.}
$$

No graph-topology restriction, parity assumption, connectedness assumption, source-dependent finite search, or unproved universal residual conjecture is used.

### Proof — copy, recolour, charge disjoint blue stars

Suppose $G$ satisfies both residual relations. In the all-blue colouring, the *first* relation forces a copy of $H=F(b,c^{t-1})$ in $G$, so there exists a vertex $v$ with $\deg_G(v)\ge b$.

Colour every edge incident to $v$ red and every other edge blue. All red edges share $v$, so the red graph contains no two disjoint edges and in particular no red $F(1,1)$. Therefore the *first* residual relation forces a blue copy of $H$ in $G-v$.

Fix such a copy of $H$ in $G-v$. It uses exactly $h$ edges, partitioned into one primary blue star of $b$ edges and $t-1$ vertex-disjoint secondary stars, each with $c$ edges. Write

$$
q=e(G-v)-h\ge0
$$

for the number of *extra edges* outside this particular fixed copy.

Construct a new red/blue colouring of **all** $G$ as follows: in each of the $t-1$ secondary $c$-stars, colour exactly $r$ of its edges red; colour every other edge of $G$ blue, including those incident to $v$, the primary $b$-star edges, and the $q$ extra edges. This is an actual edge colouring: the stars in the fixed forest copy are edge-disjoint and vertex-disjoint.

The red graph is a disjoint union of stars of size exactly $r$ (plus isolates), so its maximum red degree is $r\le a-1$. It therefore **cannot** contain a red $F(a,1,1)$, the red target in the *second* residual relation.

Suppose nevertheless that this colouring contains a blue copy of $F(c^{t-1})$. Its $t-1$ stars are vertex-disjoint. At most **one** of these stars uses vertex $v$. At most **one other** of the remaining stars uses an edge of the primary $b$-star: any two edges of that primary star meet at its centre, so two vertex-disjoint blue stars cannot both use its edges.

Therefore **at least $t-3$** of the vertex-disjoint blue $c$-stars both avoid $v$ and use **no primary-star edge**. For each such blue star, the only available edges from the fixed forest copy are in its secondary components, and after recolouring those have maximum degree at most $c-r$. A $c$-edge star has one centre with $c$ incident selected blue edges. **At least $r$ of those edges must therefore be outside the fixed copy**, belonging to the $q$ extra edges. Because the selected blue stars are vertex-disjoint, the extra edges they use are all distinct. Consequently

$$
q\ge r(t-3).
$$

We have constructed a colouring without red $F(a,1,1)$; the *second* residual arrowing relation therefore requires blue $F(c^{t-1})$. The preceding inequality is thus necessary:

$$
e(G)=\deg_G(v)+h+q
\ge b+[b+(t-1)c]+r(t-3).
$$

This is the claimed lower bound. QED.

The counting principle is exact: **one** blue target star may use $v$, **one** may consume the primary large star, and **each of the other $t-3$ disjoint blue target stars must consume at least $r$ extra edges**. There is no assumption that the blue target stars must be centred at the original host star centres. The argument counts incident *edges at any possible centre*, including centres introduced by extra edges.

## Theorem B — exact unrestricted-host flat-tail family (all t, multi-arm)

Suppose in addition that

$$
\boxed{c\ge a-1,\qquad b\ge a+c-1.}
$$

Then for **every** $t\ge4$, $a\ge2$, $c\ge a-1$, $b\ge a+c-1$,

$$
\boxed{\mathcal J\big((a,1,1),(b,c^{t-1})\big)
=2b+(t-3)(a+c-1)+2c.}
$$

This includes mixed parity and arbitrary graph hosts, not merely disjoint-star host optimum.

**Proof.** Theorem A has $r=a-1$, giving the lower bound

$$
2b+(t-1)c+(t-3)(a-1)
=2b+(t-3)(a+c-1)+2c.
$$

For the matching upper bound, take the **explicit canonical disjoint-star host**

$$
U=F\big(b,b,\underbrace{a+c-1,\ldots,a+c-1}_{t-3},c,c\big).
$$

Its size is precisely the claimed bound. We check directly why it simultaneously arrows both residual pairs, using the already source-proved exact star-host antidiagonal criterion (\`JOINT_RESIDUAL_ITERATED_PEELING_THEOREM.md\`, Theorem A).

The first residual pair $(F(1,1),F(b,c^{t-1}))$ has canonical antidiagonal list

$$
A=(b,b,\underbrace{c,\ldots,c}_{t-1}).
$$

The second pair $(F(a,1,1),F(c^{t-1}))$ has list

$$
B=(\underbrace{a+c-1,\ldots,a+c-1}_{t-1},c,c).
$$

These lists have the same length $t+1$. Under $b\ge a+c-1$, their coordinatewise maximum equals exactly the star-size list of $U$. By the star-host criterion, $U$ arrows both residual pairs. Thus $\mathcal J\le e(U)$, matching Theorem A's lower bound. QED.

### Previously open five-blue-star benchmark: exact closure

Set $a=2$ and $t=5$ (red original $F(2,1,1)$, blue original $F(b,c,c,c,c)$). The hypotheses simplify to $c\ge1$, $b\ge c+1$. Then the exact result becomes

$$
\boxed{\mathcal J((2,1,1),(b,c,c,c,c))=2b+4c+2.}
$$

The earlier issue #3490 result was the one-edge interval $2b+4c+1\le\mathcal J\le2b+4c+2$. Theorem A now excludes the entire lower edge count for **all** such pairs, and Theorem B gives the upper. The formerly proposed difficult **one-edge-slack rigidity classification is unnecessary**: the simple recolouring-budget argument proves the sharp result directly for arbitrary hosts.

This is also sharper than the old peeling bound for $c>1$. For $a=2$ and $t=5$, the older two-hub theorem yields $e(G)\ge2b+6$, while the present exact theorem gives $e(G)\ge2b+4c+2$. The improvement is $4(c-1)$ edges. For $a\ge3$ the gain likewise grows with the secondary star size and with $t$.

### General original size-Ramsey corollary where the core transfer applies

For these same lists, the **original** antidiagonal edge budget is

$$
W=\mathcal J+(a+b-1)
=3b+(t-3)(a+c-1)+2c+a-1.
$$

Let $D=a+b-2$. The original full size-Ramsey equality follows from the separately source-locked core transfer in \`GENERAL_CORE_ORIGINAL_TRANSFER.md\` whenever any of the following sufficient conditions holds:

- Both $a$ and $b$ are odd.
- $W\le D(D+1)/2$ (regardless of parity).
- At least one of $a,b$ is odd and $W\le D(D+1)$.
- Opposite parity and the corresponding vertex-budget inequality from that source.

No claim is made here that these inequalities cover *all* admissible original parameters; the new unconditional exact theorem concerns the **joint residual**, and the original corollary uses an independently source-proved transfer implication.

## A reusable exclusion bound outside the exact upper regime

Theorem A holds also for $c<a-1$ and for $b<a+c-1$ (provided $b\ge c$). In these ranges it yields the unconditional arbitrary-host lower

$$
\mathcal J\ge 2b+(t-1)c+(t-3)\min(a-1,c).
$$

This is an additional safe bound, **not** a claim that the general antidiagonal candidate equals it. In particular, for $c=1$, $a>2$, the older independent peeling theorem may be stronger. The open issue is not silently closed outside the explicitly proved regime.

## Finite verification and provenance

\`verify_flat_tail_multiarm.py\` independently recomputes original and residual antidiagonal maxima with distinct zero- and one-based formulas. It verifies the algebraic equalities and the precise lower-bound budget for **4,662** parameter instances, including **2,772** exact-family instances and **1,890** general lower-only instances. It also tests **complete red-arm allocations** of a small declared collection of canonical star hosts, separately checking both residual arrowing properties. The verifier uses the standard library and is fully deterministic. These bounded checks corroborate formulas and upper hosts; the **all-host lower proof is the mathematical counting argument above, not the finite grid**.

The source of the previously known exact canonical disjoint-star-host criterion and old two-hub peeling lower is \`JOINT_RESIDUAL_ITERATED_PEELING_THEOREM.md\`; the new budget proof does not assume its unproved general conjecture. This is new claim 018, \`UNDER_REVIEW\`, with finite corroboration claim 019 \`CHECKED\`. Substantive mathematical review must examine both the "one primary star" exception and the $r$-extra-edge charge, and validate the antidiagonal coordinatewise maximum independently.

**Outstanding boundary for unrestricted Erdős #561:** extending this recolouring charge beyond flat equal tails and $(a,1,1)$ red profiles without assuming a uniform per-target-star deficit, and the remaining general asymmetric joint residual inequality. The special $(a,1,1)$ / $(b,c^{t-1})$ joint theorem stated here is complete on paper; the unrestricted conjecture is not.
