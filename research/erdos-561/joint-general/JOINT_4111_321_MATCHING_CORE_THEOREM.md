# Erdős #561: 15-edge four-by-three joint residual by a matching-core proof

**Date:** 2026-11-24. **Status:** mathematical paper UNDER_REVIEW, bounded checks separately CHECKED after exact-head replay. **Scope:** finite simple arbitrary hosts, ordinary non-induced, vertex-disjoint positive star forests. No MATHCERT, all-profile proof or priority claim.

## Statement

Let $F(a_1,\ldots,a_r)$ denote the vertex-disjoint union of $K_{1,a_i}$; $G\to(R,B)$ means every red/blue edge colouring contains red $R$ or blue $B$.

**Theorem.** For every finite simple graph $Q$, simultaneous

$$
Q\to(3K_2,F(3,2,1))
\quad\text{and}\quad
Q\to(F(4,1,1,1),F(2,1))
$$

implies $e(Q)\ge15$; equality holds at $Q=F(5,4,3,2,1)$. These are exactly the JOINT residual relations for original red $(4,1,1,1)$ and blue $(3,2,1)$. The canonical original weights are $(6,5,4,3,2,1)$, so the JOINT tail is $5+4+3+2+1=15$. The separate residual minima are 12 and 14, giving switching surplus one.

## Lower bound

Suppose $e(Q)\le14$. Let $N$ be the number of nonisolated vertices.

**First deletion.** For any two distinct vertices $u,v$, colour every edge meeting $\{u,v\}$ RED and all other edges BLUE. The red edges have vertex cover at most two, hence cannot contain $3K_2$. The first arrow forces

$$
Q-\{u,v\}\supseteq F(3,2,1),\quad e(Q-\{u,v\})\ge6.
$$

**Second deletion.** For any vertex $u$, colour all edges meeting $u$ BLUE and all other edges RED. The blue graph has matching number at most one; it cannot contain $F(2,1)$. Hence $Q-u$ contains RED $F(4,1,1,1)$, with eleven distinct vertices and a star centre $v\ne u$ of degree at least four within $Q-u$. Combining the deletions gives

$$
e(Q)=d_Q(u)+d_{Q-u}(v)+e(Q-\{u,v\})
\ge d_Q(u)+4+6.
$$

Thus $\Delta(Q)\le4$. Choosing a nonisolated $u$ for the second deletion also yields $N\ge12$.

Let $X$ be the vertices of degree four and $k=|X|$. If a matching covered every vertex of $X$, colouring its edges BLUE and all other edges RED would avoid the second arrowing pair: blue maximum degree at most one excludes $F(2,1)$, and red maximum degree at most three excludes $F(4,1,1,1)$. Consequently **no matching covers $X$**.

**Matching-cover lemma.** In a simple graph of maximum degree at most four, if at most four vertices have degree four, then a matching covers them all.

Proof. The classical specified-vertex Tutte matching criterion states that a matching covering $X$ exists if and only if, for every $S\subseteq V$, the number $q_X(S)$ of odd connected components of $G-S$ wholly contained in $X$ is at most $|S|$. For each such component $C$, let $r=|C|$; then $1\le r\le4$ and every vertex of $C$ has degree four. All exiting edges lead into $S$, and simplicity gives

$$
e(C,S)=4r-2e(C)\ge4r-r(r-1)=r(5-r)\ge4.
$$

Counted components are disjoint and vertices of $S$ have degree at most four. Consequently $4q_X(S)\le e(S,V\setminus S)\le4|S|$. The Tutte criterion holds. QED. Source: the Akiyama–Kano specified-vertex formulation referenced in the protected designated-matching research; an independent lecture statement appears at https://www.cs.mcgill.ca/~mdresc/graphtheory.pdf (Theorem 9).

By the lemma, $k\ge5$. The degree sum now gives

$$
2e(Q)\ge 4k+(N-k)=N+3k\ge12+15=27.
$$

Since $e(Q)\le14$, necessarily $e(Q)=14$ and $k=5$ (else $28\ge12+3k$ fails). Thus the five degree-four vertices have degree sum 20 and the remaining nonisolated vertices have total degree 8. Set $Y=V(Q)\setminus X$.

**Five-vertex core.** Define $q=10-e(Q[X])$, the number of missing edges of the potential complete graph on the five degree-four vertices. The crossing-edge count is

$$
e(X,Y)=20-2e(Q[X])=2q.
$$

Since all positive-degree vertices of $Y$ have total degree eight, $0\le q\le4$.

If $q=0$, the five degree-four vertices form an isolated $K_5$, and $Q-X$ has exactly four edges. Colour all edges of $K_5$ RED; colour two other edges RED and the other two BLUE. Red $F(4,1,1,1)$ cannot appear: a red four-star must lie inside the isolated $K_5$, consuming all five of its vertices, and only two red edges remain outside. Blue $F(2,1)$ needs three edges but only two are blue. Contradiction.

Suppose instead $1\le q\le4$. Form the graph $M$ of missing core edges and pick $x\in X$ of largest missing-edge degree $h\ge1$. If $h\ge2$, the graph $M-x$ has at most $q-h\le2$ edges. If $h=1$, all missing core edges form a matching, so $q\le2$ and $M-x$ has at most one edge. Therefore $Q[X\setminus\{x\}]$ is $K_4$ with at most two missing edges. The three pairwise edge-disjoint perfect matchings of $K_4$ guarantee that an intact two-edge perfect matching remains. Because $x$ misses at least one core neighbour but still has degree four, $x$ has a neighbour $y\in Y$. The edge $xy$ together with the intact perfect matching of the four other core vertices gives a three-edge matching covering all of $X$.

Colour that matching BLUE and all other edges RED. The BLUE maximum degree is at most one and the RED maximum degree is at most three, avoiding the second arrowing pair; contradiction.

Both cases contradict the existence of a 14-edge JOINT host. This proves the lower bound for **arbitrary finite simple graphs**. QED.

## Upper bound

Take $H=F(5,4,3,2,1)$, containing exactly 15 edges. All edges of an individual host star meet its centre, so any two vertex-disjoint positive target stars must be placed in distinct host components.

For the **first** arrowing relation, if red $3K_2$ is absent, red edges occur in at most two of the five host-star components. At least three components are wholly blue; their descending sizes dominate $(3,2,1)$. Thus blue $F(3,2,1)$ occurs.

For the **second** relation, suppose blue $F(2,1)$ is absent. If blue edges occur in at most one host component, at least four host components are entirely red, with one of size at least four; these contain red $F(4,1,1,1)$. If blue edges occur in two or more host components, absence of blue $F(2,1)$ forces every blue-active host component to contain at most one blue edge. Red counts in the five components are at least $(4,3,2,1,0)$. The first yields a red four-star and the next three provide its required disjoint red single edges. Therefore red $F(4,1,1,1)$ occurs. This proves the upper bound. QED.

## Infinite-family extension: all larger leading RED stars

**Theorem (unbounded, original size-Ramsey for every $a\\ge5$).** For any integer $a\\ge4$, original red $n=(a,1,1,1)$ and blue $m=(3,2,1)$ have exact JOINT residual minimum

$$
\\boxed{\\mathcal J(n,m)=2a+7.}
$$

Furthermore, for every $a\\ge5$ the ORIGINAL asymmetric size Ramsey number over arbitrary finite simple hosts is

$$
\\boxed{\\widehat r(F(a,1,1,1),F(3,2,1))=3a+9.}
$$

For $a=4$, the original equality 21 is proved separately below using the prior source-locked sharp $D+2$ saturated-core capped-partition theorem; no extension to all Erdős #561 parameter profiles is intended.

**Proof of JOINT when $a\\ge5$.** Let $Q$ satisfy the two residual arrows

$$
Q\\to(3K_2,F(3,2,1)),\\quad
Q\\to(F(a,1,1,1),F(2,1)).
$$

The canonical upper host is $F(a+1,a,3,2,1)$, totaling $2a+7$ edges. Its upper arrowing proof is exactly the preceding two-case host-star argument with $(5,4)$ replaced by $(a+1,a)$; all inequalities hold for $a\\ge4$.

Suppose $e(Q)\\le2a+6$. The same independent two-vertex and one-vertex deletion colourings used above give, for each vertex $u$, an appropriate different $v$ with

$$
e(Q)\\ge d_Q(u)+a+6;
$$

therefore $\\Delta(Q)\\le a$. The red forest in $Q-u$ has $a+7$ nonisolated vertices, so $N=|V_+(Q)|\\ge a+8$.

If a matching covers all degree $a$ vertices $X$, colouring it BLUE and all other edges RED avoids the second relation: red degrees are at most $a-1$ and blue degrees at most one. Thus no matching covers $X$. Exactly the same specified-vertex Tutte boundary proof as above, now with $D=a$, proves the general lemma: if a graph has maximum degree at most $a$ and $|X|\\le a$, a matching covers $X$. Indeed a counted component of $r\\le a$ saturated vertices sends at least $r(a-r+1)\\ge a$ edges to $S$, and each vertex of $S$ receives at most $a$. Hence $k=|X|\\ge a+1$. The handshake bound gives

$$
2e(Q)\\ge N+(a-1)k\\ge(a+8)+(a-1)(a+1)=a^2+a+7.
$$

But the assumed edge budget gives $2e(Q)\\le4a+12$. Since $a^2-3a-5>0$ for every integer $a\\ge5$, these inequalities conflict. Hence $e(Q)\\ge2a+7$, proving sharp JOINT for all $a\\ge5$; the $a=4$ boundary is the explicit five-core argument above.

**Proof of ORIGINAL when $a\\ge5$.** The canonical original host $F(a+2,a+1,a,3,2,1)$ has $W=3a+9$ edges and arrows the original pair by the source-proved canonical star-host criterion. Suppose $G$ arrows the pair with $e(G)\\le W-1=3a+8$. Standard single-vertex Ramsey deletion forces $G-u$ to satisfy BOTH proved JOINT relations for each $u$. Their sharpness gives

$$
d_G(u)=e(G)-e(G-u)\\le(3a+8)-(2a+7)=a+1.
$$

Write $D=a+1=(a-1)+2$. If $\\Delta(G)\\le a$, Vizing's edge-colouring theorem decomposes its edges into at most $a+1$ matchings. Colour $a-1$ matching classes RED and two BLUE. This yields red maximum degree at most $a-1$ and blue maximum degree at most two, contradicting original arrowing. Thus $\\Delta(G)=D$.

A RED/BLUE capped edge partition with respective caps $a-1$ and $2$ also avoids both original leading stars. Therefore the source-proved ordinary Lovász $(g,f)$ maximum-degree-core lemma gives at least $D+1=a+2$ vertices of degree $D$. The all-RED colouring forces a copy of $F(a,1,1,1)$ and so $N=|V_+(G)|\\ge a+7$. Handshake now yields

$$
2e(G)\\ge N+(D-1)(D+1)
\\ge a+7+a(a+2)=a^2+3a+7.
$$

However, $2e(G)\\le6a+16$, and $a^2-3a-9>0$ for every integer $a\\ge5$. Contradiction. Thus $e(G)\\ge3a+9$, matched by the canonical upper host. QED.

**The $a=4$ ORIGINAL boundary.** The original edge target is $W=21$. Suppose an arbitrary finite simple $G$ arrows $(F(4,1,1,1),F(3,2,1))$ with $e(G)\le20$. The now-proved sharp JOINT bound $J=15$ and vertex deletion give $\Delta(G)\le20-15=5$. If $\Delta(G)\le4$, Vizing gives at most five matching colours, split three RED plus two BLUE to avoid both targets. Thus $\Delta(G)=D=5$.

The capped split with $(\alpha,\beta)=(3,2)$ must fail, or it would itself avoid both original leading stars. The source-proved **sharp $D+2$ saturated-core partition theorem** (see `research/erdos-561/DPLUS2_SATURATED_CORE_THEOREM.md`, section 1) asserts that a graph with $\Delta\le D=\alpha+\beta$ and at most $D+2$ degree $D$ vertices admits such a capped partition whenever $D$ is odd. It is an ordinary paper derivation from the general Lovász $(g,f)$ theorem, not a finite-graph assumption.

The all-RED colouring requires $G$ to contain $F(4,1,1,1)$, so $N=|V_+(G)|\ge11$. If $k$ vertices have degree five, degree sum yields

$$
2e(G)\ge5k+(N-k)\ge4k+11.
$$

As $2e(G)\le40$, this forces $k\le\lfloor29/4\rfloor=7=D+2$. Since $D=5$ is odd, the cited sharp partition theorem supplies a $(3,2)$ capped edge split. This contradicts original arrowing. Thus no at-most-20-edge original-arrowing graph exists. The canonical 21-edge star host $F(6,5,4,3,2,1)$ attains the upper bound; consequently

$$
\boxed{\widehat r(F(4,1,1,1),F(3,2,1))=21.}
$$

This is a complete *paper-level original theorem*, conditional only on the published Lovász and Vizing classical results and the independently checkable graph and deletion deductions. In particular, it does not rely on an unproved general JOINT hypothesis.

**Dependencies and sharp boundary.** The JOINT infinite family requires the standard specified-vertex matching theorem but not the general joint-residual hypothesis. The ORIGINAL family uses the already documented and paper-proved ordinary Lovász factor/degree-core theorem, and at $a=4$ the stronger sharp $D+2$ cap theorem (the relevant sources include `research/erdos-561/formal-graph/LOVASZ_CAP_PARTITION_BRIDGE.md`), Vizing's edge-colouring theorem and standard Ramsey vertex deletion. Neither is a Lean kernel proof. No claim for other BLUE profiles or unrestricted $s,t$ is implied.

## Reproducibility, scope and next boundary

The standard-library verifier checks all $6\cdot5\cdot4\cdot3\cdot2=720$ red count vectors on the canonical star host, all $2^{15}=32768$ individual edge colours, and all $\sum_{q=1}^4\binom{10}{q}=385$ missing-core patterns, including construction of each required five-core covering matching. These are corroborative *finite* checks. The lower theorem uses the universally quantified classical specified-vertex Tutte condition, not extrapolation from the finite checks.

**Mathematical disposition:** sharp new fixed JOINT theorem, paper UNDER_REVIEW; no protected mathematical or external MATHCERT certification. The full $s,t\ge3$ residual hypothesis #3490 and unrestricted ORIGINAL Erdős #561 remain OPEN/PARTIAL. The sharp ORIGINAL $(4,1,1,1)$ versus $(3,2,1)$ value $21$ is established separately by the source-proved odd $D$ $D+2$ cap classification, as shown in the infinite-family extension.
