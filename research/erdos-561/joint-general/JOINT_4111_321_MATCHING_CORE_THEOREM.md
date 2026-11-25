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

## Reproducibility, scope and next boundary

The standard-library verifier checks all $6\cdot5\cdot4\cdot3\cdot2=720$ red count vectors on the canonical star host, all $2^{15}=32768$ individual edge colours, and all $\sum_{q=1}^4\binom{10}{q}=385$ missing-core patterns, including construction of each required five-core covering matching. These are corroborative *finite* checks. The lower theorem uses the universally quantified classical specified-vertex Tutte condition, not extrapolation from the finite checks.

**Mathematical disposition:** sharp new fixed JOINT theorem, paper UNDER_REVIEW; no protected mathematical or external MATHCERT certification. The full $s,t\ge3$ residual hypothesis #3490 and unrestricted ORIGINAL Erdős #561 remain OPEN/PARTIAL. The sharp ORIGINAL $(4,1,1,1)$ versus $(3,2,1)$ value is **not** inferred without a separate valid original-transfer proof.
