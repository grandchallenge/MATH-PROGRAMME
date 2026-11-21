# Erdős #561 — saturated-top matching-versus-star-forest exact joint residual

**Research date:** 2026-11-21. **Status:** paper-level unrestricted-host theorem UNDER_REVIEW; deterministic finite corroboration CHECKED; full Erdős #561 and all-profiles joint issue #3490 remain OPEN/PARTIAL. No MATHCERT certification.

Let $s,t\ge3$ with $s-1\le t$, and let

$$
n=(\underbrace{1,\ldots,1}_{s}),\qquad
m=(m_1,\ldots,m_t),\quad m_1\ge\cdots\ge m_t\ge1.
$$

Write $F(n)$ for the vertex-disjoint union of ordinary positive-edge stars and $G\to(R,B)$ for ordinary non-induced Ramsey arrowing under every red/blue edge colouring. The **joint residual** relations for this pair are

$$
\mathrm{R1}:\quad
G\to(F(1^{s-1}),F(m_1,\ldots,m_t)),
$$

$$
\mathrm{R2}:\quad
G\to(F(1^{s}),F(m_2,\ldots,m_t)).
$$

All graphs may be arbitrary finite simple graphs, not necessarily disjoint unions of stars.

## Theorem A — arbitrary-profile matching prefix lower bound

If G satisfies R1 and R2, then

$$
\boxed{
e(G)\ge m_1+\sum_{j=1}^{t}m_j+\sum_{j=3}^{s-1}m_j.
}
$$

The final sum is zero when $s=3$.

### Proof

R1 in the all-blue colouring forces a blue copy of $F(m)$, so there exists a vertex $v$ with $d_G(v)\ge m_1$.

Colour every edge incident to $v$ red and every other edge blue. All red edges meet $v$, so red has matching number at most one; because $s-1\ge2$, it cannot contain $F(1^{s-1})$. By R1, the remainder $G-v$ contains a copy of the full blue forest $H=F(m_1,\ldots,m_t)$.

Fix a particular such $H$. Let $M=\sum_{j=1}^t m_j$ and $q=e(G-v)-M\ge0$ be the extra edge count outside the fixed H copy. Its components are vertex-disjoint stars, with the given sorted arm sizes.

Construct a **new** colouring: colour every edge in the **first $s-1$ largest component stars of H** red; colour every other edge of G blue, including all edges incident with $v$. The red graph consists of at most $s-1$ nontrivial star components and has matching number at most $s-1$. Thus it avoids the red $F(1^s)$ of R2, forcing a blue copy of $F(m_2,\ldots,m_t)$.

This blue target uses exactly $M-m_1$ edges. Its star components are vertex-disjoint, so at most ONE of them contains vertex $v$. Because the largest star in this target has $m_2$ edges, the copy has at most $m_2$ of its edges incident with $v$. Therefore at least

$$
(M-m_1)-m_2
$$

edges of the blue target lie in $G-v$.

But in $G-v$ the only blue edges are the $q$ extra edges and the edges of the *unrecoloured* tail H-stars numbered $s$ through $t$, of total size $M-\sum_{j=1}^{s-1}m_j$. Thus

$$
M-m_1-m_2
\le q+M-\sum_{j=1}^{s-1}m_j,
$$

equivalently

$$
q\ge\sum_{j=3}^{s-1}m_j.
$$

Add disjoint contributions: the edges incident to $v$, the fixed H edges, and the remaining q edges:

$$
e(G)=d_G(v)+M+q
\ge m_1+M+\sum_{j=3}^{s-1}m_j.
$$

This is a completely unrestricted-host proof. It uses only the two residual Ramsey properties, elementary matching number, and edge-disjoint accounting. QED.

## Theorem B — exact family with saturated maximal blue tier

Suppose additionally that

$$
m_1=m_2=\cdots=m_{s-1}=b
$$

for an integer $b\ge1$, and let the remaining blue tail $(c_1,\ldots,c_L)$, where $L=t-s+1\ge0$, have **arbitrary** positive nonincreasing values at most $b$. (For $s=3$, assume $L\ge1$ so $t\ge3$.)

Then the joint residual minimum over **all finite simple graph hosts** is EXACTLY

$$
\boxed{
\mathcal J((1^s),(b^{s-1},c_1,\ldots,c_L))
=(2s-3)b+\sum_{\ell=1}^{L}c_\ell.
}
$$

The canonical disjoint-star upper host is

$$
U=F(\underbrace{b,\ldots,b}_{2s-3},c_1,\ldots,c_L).
$$

**Proof of the lower bound.** Theorem A gives

$$
e(G)\ge b+\big((s-1)b+\sum_\ell c_\ell\big)
+\underbrace{\sum_{j=3}^{s-1}b}_{(s-3)b}
=(2s-3)b+\sum_\ell c_\ell.
$$

**Proof of the upper bound.** Because the red original target is a matching of size $s$, every original antidiagonal size is simply the largest blue arm size in the corresponding sliding window of $s$ entries. Since the blue sizes are nonincreasing, the original antidiagonal list is

$$
(\underbrace{m_1,\ldots,m_1}_{s},m_2,\ldots,m_t).
$$

Removing its first entry gives the canonical **joint-residual** star-host list

$$
(\underbrace{m_1,\ldots,m_1}_{s-1},m_2,\ldots,m_t).
$$

For our saturated maximal prefix, this list equals $(b^{2s-3},c_1,\ldots,c_L)$, whose sum is exactly the lower bound above. The source-proved antidiagonal star-host Ramsey criterion (`JOINT_RESIDUAL_ITERATED_PEELING_THEOREM.md`, Theorem A) shows the canonical host simultaneously arrows R1 and R2. Hence its edge count is attained, proving equality. QED.

### Concrete families, including the formerly two-tier case

For $s=4$ and any $t\ge3$, original red is a four-edge matching, original blue can be **three largest stars of size $b$ followed by any sorted positive tail**; the exact joint minimum is

$$
\mathcal J((1,1,1,1),(b,b,b,c_1,\ldots,c_L))=5b+\sum_\ell c_\ell.
$$

This strictly extends the special $(b,b,b,1)$ case from the prior turn. For arbitrary $3\le s\le t$ and $m=(b^{t-1},1)$, the exact value is $(s+t-3)b+1$, as obtained by taking $c_1,\ldots,c_L$ to consist of $t-s$ further copies of $b$ followed by one edge. More generally, the saturated first $s-1$ maximal stars need not be followed by a uniform or two-level tail: the tail can be completely nonuniform.

Theorem A also gives a valid new partial lower bound for **any** nonincreasing blue target (even when the first $s-1$ blue sizes differ). Its exactness under a saturated maximal tier is proved here, but it does not assert all arbitrary-profile cases.

## Theorem C — automatic transfer to the ORIGINAL problem when either original forest is a matching

Let $n,m$ be arbitrary nonincreasing positive lists of lengths $s,t\ge3$, and suppose that the **individual sharp joint residual inequality** has already been established:

$$
G\to(F(n_2,\ldots,n_s),F(m)),
\quad
G\to(F(n),F(m_2,\ldots,m_t))
\quad\Longrightarrow\quad
e(G)\ge J,
$$

where $W=\sum_{k=2}^{s+t}w_k(n,m)$ is the canonical original antidiagonal edge budget and $J=W-(n_1+m_1-1)$. If **either** $n_1=1$ or $m_1=1$, then

$$
\boxed{\widehat r(F(n),F(m))=W.}
$$

This transfer holds over arbitrary finite simple graph hosts. It needs no Lovász factor theorem, parity restriction, bounded enumeration, or assumption of the unrestricted joint residual hypothesis.

### Proof of Theorem C

As usual, the canonical disjoint-star host of $W$ edges arrows the original pair, so only the lower bound is at issue. Suppose an original-arrowing graph $G$ has $e(G)\le W-1$.

**First, every vertex deletion produces both residual arrowing relations.** Fix an arbitrary vertex $v$. If $G-v$ admitted a colouring avoiding red $F(n_2,\ldots,n_s)$ and blue $F(m)$, extend it by colouring all edges at $v$ red. A blue copy of $F(m)$ is then impossible. A red copy of $F(n)$ is also impossible: if such a vertex-disjoint forest exists, at most one of its components meets $v$. Discarding that component leaves $s-1$ red stars entirely in $G-v$, whose sorted sizes necessarily dominate the list $(n_2,\ldots,n_s)$, because deleting any one entry from a nonincreasing list leaves a coordinatewise larger sequence than deleting its largest entry. This contradicts the chosen red-residual-avoiding colouring. Thus $G-v$ arrows the first residual pair. Interchanging the two colours and recolouring all edges at $v$ blue proves the second residual arrowing relation in exactly the same way.

By the individually proved sharp joint residual inequality, $e(G-v)\ge J$. Hence every vertex satisfies

$$
d_G(v)=e(G)-e(G-v)\le W-1-J=n_1+m_1-2.
$$

If $n_1=1$, then $n$ is a matching and the bound becomes $\Delta(G)\le m_1-1$. But original arrowing applied to the all-blue colouring forces a blue copy of $F(m)$, which contains a star of degree $m_1$ and therefore requires $\Delta(G)\ge m_1$. Contradiction.

If the leading blue star size is one, then the blue target is a matching. The displayed degree bound makes the maximum degree of G at most the leading red star size minus one. But the all-red colouring must contain the original red forest, including a star of that leading size. This is impossible. Thus the canonical host of W edges is optimal. QED.

### New parity-free ORIGINAL infinite family

Combine Theorem C with the exact individual joint residual in Theorem B. For all $s\ge3$, all $L\ge0$ with $t=s-1+L\ge3$, all $b\ge1$, and all arbitrary positive nonincreasing tail lists $b\ge c_1\ge\cdots\ge c_L$,

$$
\boxed{
\widehat r\big(F(1^s),F(b^{s-1},c_1,\ldots,c_L)\big)
=(2s-2)b+\sum_{\ell=1}^{L}c_\ell.
}
$$

The exact original antidiagonal list has $s$ initial copies of $b$, followed by the remaining $s-2$ copies of $b$ and the arbitrary tail; its sum is the displayed value. The case $L=0$ is permitted whenever $s\ge4$ so $t\ge3$. In particular, for every $b\ge1$ and $1\le c\le b$,

$$
\widehat r(F(1,1,1,1),F(b,b,b,c))=6b+c.
$$

These are exact over unrestricted finite simple hosts, but the source-level mathematical status remains UNDER_REVIEW, not MATHCERT certification.

## Verification and exact mathematical boundary

The deterministic verifier `verify_saturated_matching_joint.py` independently computes the complete original and both residual antidiagonals using zero- and one-based conventions; it checks **14,203** bounded matching-versus-blue-profile cases, including **3,385** saturated-prefix exact-family instances, and exhaustive all-arm red/blue allocations across seven specified canonical hosts (**116,386** allocations). The finite checks corroborate the separate analytical proof; no finite graph-topology census proves the theorem.

New unbounded claim 022 remains UNDER_REVIEW; the distinct general matching-leading original transfer and its original infinite-family consequence are source claim 024 UNDER_REVIEW. Bounded exact arithmetic/arm-class claim 023 is CHECKED. This does not promote unrestricted Erdős #561, issue #3490, or MATHCERT.
