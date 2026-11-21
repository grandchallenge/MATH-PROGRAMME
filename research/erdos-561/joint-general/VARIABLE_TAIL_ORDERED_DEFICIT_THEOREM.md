# Erdős #561 — ordered-deficit joint residual theorem for unequal blue tails

**Status:** mathematical proof UNDER_REVIEW; finite corroboration CHECKED. Every graph below is an arbitrary finite simple host; embeddings of star forests are ordinary and vertex-disjoint. This neither resolves the unrestricted joint residual conjecture in issue #3490 nor certifies the original unrestricted Erdős #561 problem.

Let $a\ge2$, $k\ge3$, and $b\ge c_1\ge\cdots\ge c_k\ge1$. The original targets are

$$
n=(a,1,1),\qquad m=(b,c_1,\ldots,c_k).
$$

Let $\mathcal J(n,m)$ be the minimum edge count of a graph satisfying BOTH residual relations:

$$
G\to(F(1,1),F(b,c_1,\ldots,c_k)),
\qquad
G\to(F(a,1,1),F(c_1,\ldots,c_k)).
$$

Define

$$
r=a-1,\quad C=\sum_{j=1}^k c_j,\quad d_j=\max(0,c_j-r),\quad
L=\sum_{i=1}^{k-2}\max(0,c_{i+2}-d_i).
$$

## Theorem A: unrestricted-host ordered-deficit lower bound

For all the stated parameters,

$$
\boxed{\mathcal J(n,m)\ge 2b+C+L.}
$$

### Rearrangement lemma

If $p_1\ge\cdots\ge p_s\ge0$ and $d_1\ge\cdots\ge d_N\ge0$, with $s\le N$, then any injection $\sigma:\{1,\ldots,s\}\hookrightarrow\{1,\ldots,N\}$ satisfies

$$
\sum_{i=1}^s(p_i-d_{\sigma(i)})_+
\ge\sum_{i=1}^s(p_i-d_i)_+,\qquad x_+:=\max(0,x).
$$

Indeed, increasing an assigned capacity cannot increase its deficit, so the best assignment uses the largest $s$ capacities. For $x\ge y$ and $u\ge v$, the function $(x-z)_+-(y-z)_+$ is nonincreasing in $z$, hence

$$
(x-u)_++(y-v)_+\le(x-v)_++(y-u)_+.
$$

Repeatedly exchange inverted pairs to match largest demand with largest capacity. Each exchange weakly reduces total deficit. This proves the lemma.

### Proof of Theorem A

The first residual relation applied to an all-blue colouring forces the forest $H=F(b,c_1,\ldots,c_k)$ inside $G$, so some vertex $v$ has degree at least $b$. Colour every edge at $v$ red and every other edge blue. The red graph is a single star and has no red $F(1,1)$, so the first residual relation forces an entire copy of $H$ in $G-v$.

Fix this particular copy of $H$; it has $h=b+C$ edges. Let $q=e(G-v)-h$ count all edges in $G-v$ outside that copy. Colour exactly $\min(r,c_j)$ edges of secondary star $j$ in the fixed $H$ red, for every $1\le j\le k$, and every other edge of $G$ blue, including all edges incident to $v$.

The red graph consists of vertex-disjoint stars with maximum degree at most $r=a-1$. Thus red contains no $F(a,1,1)$. The second residual relation requires a blue $F(c_1,\ldots,c_k)$.

Suppose such a blue forest occurs. Its $k$ component stars are vertex-disjoint. At most **one** uses vertex $v$. At most **one other** uses an edge of the fixed primary star of size $b$, because every edge of that primary star has a common centre. Choose any $k-2$ of its component stars that avoid both exceptions. Let their required edge counts in descending order be $p_1,\ldots,p_{k-2}$. Since they are obtained by deleting at most two elements of the full descending target list,

$$
p_i\ge c_{i+2}\quad(1\le i\le k-2).
$$

Every selected blue star avoids $v$ and every primary-star edge. If it uses any edge of the fixed secondary stars, all such edges belong to ONE secondary component: all its selected edges meet at its own centre, while the fixed secondary components are vertex-disjoint. Two distinct selected blue stars cannot both use edges of the same fixed secondary component, since all edges in a host star share the host centre. Assign each selected target star to its used secondary component, or to an arbitrary unused secondary component if it uses no secondary-copy edge. This is an injection.

A selected target star assigned to component $j$ has at most $d_j=\max(0,c_j-r)$ available blue edges from that component. Every other selected edge must be one of the $q$ extra edges. Thus that target star uses at least $(p-d_j)_+$ extra edges. Different selected target stars are vertex-disjoint, so these extra edges cannot be shared. By the rearrangement lemma and the order-statistic bound,

$$
q\ge\sum_{i=1}^{k-2}(p_i-d_i)_+
\ge\sum_{i=1}^{k-2}(c_{i+2}-d_i)_+=L.
$$

Counting edges at $v$, fixed copy $H$, and remaining edges separately gives

$$
e(G)=d_G(v)+h+q\ge b+(b+C)+L.
$$

The proof does not assume that selected target stars are centred at the fixed host-star centres, and it makes no graph-topology restriction. QED.

## Theorem B: exact variable-tail family

Assume additionally

$$
\boxed{b\ge a+c_1-1,\qquad c_{k-2}\ge a-1.}
$$

The latter means all secondary sizes except possibly the final two are at least $a-1$. Then the unrestricted-host exact joint residual is

$$
\boxed{\mathcal J((a,1,1),(b,c_1,\ldots,c_k))
=2b+C+\sum_{i=1}^{k-2}(a-1+c_{i+2}-c_i)_+.}
$$

An attaining canonical star host is

$$
U=F\big(
b,b,\max(c_1,a+c_3-1),\ldots,
\max(c_{k-2},a+c_k-1),c_{k-1},c_k\big).
$$

**Proof.** For every $i\le k-2$ the extra hypothesis gives $c_i\ge a-1$, so $d_i=c_i-(a-1)$. Theorem A now yields exactly the claimed lower expression.

The first residual antidiagonal star-size list is $A=(b,b,c_1,\ldots,c_k)$. The second residual list comes from $(a,1,1)$ versus $(c_1,\ldots,c_k)$. At its position $i+2$ for $1\le i\le k-2$, its entries can only be $a+c_{i+2}-1$, $c_{i+1}$ or $c_i$. Hence the coordinatewise maximum with $A$ has entry $\max(c_i,a+c_{i+2}-1)$. At the first two positions, $b\ge a+c_1-1$ dominates the second residual list. The final two positions give $c_{k-1},c_k$. Thus the maximum is exactly the star list defining $U$.

By the source-proved exact antidiagonal criterion for disjoint-star hosts, $U$ arrows both residual pairs. Its edge count is

$$
e(U)=2b+C+\sum_{i=1}^{k-2}(a-1+c_{i+2}-c_i)_+.
$$

This matches Theorem A for every arbitrary finite simple host. QED.

### Examples and downstream original size-Ramsey values

The flat-tail theorem from the immediately preceding research package is the special case $c_1=\cdots=c_k=c\ge a-1$, where every summand equals $a-1$. Theorem B now permits **unequal** tails and zero or positive deficits in different positions.

A concrete nonuniform example: $a=4$, $b=8$, $k=5$ and $(c_1,\ldots,c_5)=(5,4,3,2,1)$. The exact joint residual is **34**, attained by $F(8,8,6,5,4,2,1)$.

The original predicted antidiagonal value is $W=J+(a+b-1)$. The already source-locked general core transfer in GENERAL_CORE_ORIGINAL_TRANSFER.md proves the *original* unrestricted-host size-Ramsey equality for this family whenever both leading sizes $a,b$ are odd, or whenever an applicable even-cap/core-density condition from that source holds. This is a valid conditional transfer with an individually proved $J$, not a claim that all original parameters are settled.

### A safe bound beyond the exact regime

Theorem A holds also when $c_{k-2}<a-1$ or $b<a+c_1-1$, provided the blue target remains nonincreasing ($b\ge c_1$). In these cases it supplies a proved but not necessarily sharp lower bound. The full joint-residual conjecture is OPEN/PARTIAL; no extension of the exact equality beyond its stated hypotheses is claimed.

### Evidence and governance

The standard-library verifier verify_variable_tail_deficit.py independently recomputes original and both residual antidiagonal lists with zero- and one-based formulas, checks **24,500** bounded exact-family instances and **19,305** lower-only cases, and examines every one of **147,188** red-arm allocations across six nonuniform canonical star hosts, checking both residual relations. These tests corroborate the arithmetic and finite host upper bounds; the unbounded arbitrary-host lower bound is the injection/rearrangement proof above.

Source claim 020 is UNDER_REVIEW; finite exact-check claim 021 is CHECKED. Neither source admission, local execution nor finite numerical corroboration is MATHCERT certification.
