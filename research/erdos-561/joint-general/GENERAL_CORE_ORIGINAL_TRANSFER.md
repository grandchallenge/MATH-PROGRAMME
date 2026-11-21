# Erdős #561 — sharp-residual core transfer and parity-free ORIGINAL families

**Research date:** 2026-11-21. **Status:** paper-level mathematical proofs UNDER_REVIEW; one exact finite graph classification CHECKED. **Scope:** original size-Ramsey equalities over arbitrary finite simple host graphs for the stated families. This is NOT a proof of unrestricted Erdős #561 or the still-open unrestricted joint-residual hypothesis #3490.

Let $n=(n_1,\ldots,n_s)$ and $m=(m_1,\ldots,m_t)$ be nonincreasing positive star edge counts, $s,t\ge3$, and let $F(n)$ be the vertex-disjoint union of the corresponding stars. All embeddings are ordinary, non-induced subgraphs. Set

$$
w_k=\max_{i+j=k}(n_i+m_j-1),\quad
W=\sum_{k=2}^{s+t}w_k,\quad
J=W-w_2,\quad D=n_1+m_1-2.
$$

Assume $n_1,m_1\ge2$ and that the **sharp simultaneous residual inequality** is already proved for the selected pair: any finite simple $Q$ satisfying both

$$
Q\to(F(n_2,\ldots,n_s),F(m)),
\qquad
Q\to(F(n),F(m_2,\ldots,m_t))
$$

has at least $J$ edges. We do not assume this for all pairs.

## Theorem A — a general degree-core transfer beyond even caps

Under these hypotheses, the original Erdős size-Ramsey formula

$$
\widehat r(F(n),F(m))=W
$$

holds whenever **any** of the following conditions holds:

1. Both leading sizes $n_1,m_1$ are odd.
2. **Any parity:** $W\le D(D+1)/2$.
3. **At least one leading size odd:** $W\le D(D+1)$.
4. **Opposite parity leading sizes:** $2W<2D^2+R$, where $R=\max(\sum_i n_i+s,\sum_jm_j+t)$.

The third condition includes the first when the stated numerical inequality holds; the first is unconditional. The fourth uses the forest-vertex budget and can be stronger than the third when $R$ is sufficiently large.

### Proof

The canonical antidiagonal disjoint-star forest has $W$ edges and arrows the original pair by the elementary greedy star-host criterion, so it suffices to exclude an original-arrowing $G$ with $e(G)\le W-1$.

For **every** vertex $v$, original arrowing implies both residual arrowings in $G-v$: colour all edges at $v$ red to transport the red-largest-star-deleted relation, or blue for the blue-largest-star-deleted relation. At most one vertex-disjoint target component can meet $v$, and the remaining components dominate the relevant deleted-largest forest. Consequently

$$
e(G-v)\ge J,\qquad d_G(v)\le(W-1)-J=D.
$$

Put the proposed red and blue maximum-degree caps $\alpha=n_1-1$ and $\beta=m_1-1$, so $\alpha+\beta=D$. If $G$ admits an $(\alpha,\beta)$ edge partition, that colouring contains no full original target in either colour, a contradiction. Therefore $G$ has **no** capped partition.

We use two independently source-locked classical consequences of the **ordinary Lovász $(g,f)$-factor theorem**:

- The degree-core necessity theorem in \`research/erdos-561/formal-graph/LOVASZ_CAP_PARTITION_BRIDGE.md\`: failure of a capped partition with $\Delta(G)\le D$ forces a connected degree $D$ core of at least $D+1$ vertices.
- The sharp $2D+1$ uniqueness theorem in \`research/erdos-561/unique-core/GENERAL_SATURATED_CORE_UNIQUENESS_THEOREM.md\`: if at most $2D+1$ vertices have degree $D$, capped-partition failure can occur **only when both caps are odd**, in which case there is an isolated odd-order connected degree $D$ regular component. The statement is a paper proof dependent on the ordinary factor theorem, not a complete Lean formalization.

Let $k$ count vertices of degree $D$. The first theorem forces $k\ge D+1$, and the degree handshake gives $2e(G)\ge kD\ge D(D+1)$. This contradicts $e(G)\le W-1$ under condition 2.

If both $n_1,m_1$ are odd, then $\alpha,\beta$ are both **even**. The classical even-cap factorization theorem already source-locked in \`research/erdos-561/even-caps/EVEN_CAP_DEGREE_SPLITTING_THEOREM.md\` gives the partition unconditionally, proving condition 1.

If **at least one** $n_1,m_1$ is odd, at least one cap is even, so the $2D+1$ uniqueness theorem shows that a non-partitionable graph must have $k\ge2D+2$. Hence

$$
2e(G)\ge Dk\ge2D(D+1),
\qquad e(G)\ge D(D+1).
$$

This contradicts $e(G)<W$ under condition 3. This supplies a useful general lower edge bound for any degree-capped obstruction when the caps are not both odd.

For the stronger vertex-budget variant, original arrowing implies $G$ contains each original forest in its all-red and all-blue colourings, hence its number of nonisolated vertices obeys $v_+(G)\ge R$. The handshake gives

$$
2e(G)\ge Dk+(v_+(G)-k)\ge R+(D-1)k.
$$

For non-partitionability with opposite-parity leading sizes, the same $k\ge2D+2$ is necessary, so

$$
2e(G)\ge R+(D-1)(2D+2)=R+2D^2-2.
$$

But $e(G)\le W-1$ gives $2e(G)\le2W-2$, contradicting condition 4, namely $2W<2D^2+R$. Thus every proposed original counterexample is impossible in all four cases. QED.

Theorem A is an implication, not a proof of the unrestricted joint residual inequality; applying it without a previously established $J$ would be invalid.

## Theorem B — three full parity-free infinite families

The *parent joint-residual lower bounds* are already proved on paper for arbitrary finite simple hosts in the protected GCL source. The present proof restores **all leading parities** and obtains original size-Ramsey equalities.

### B1. Three versus four stars, including the final degree-two boundary

For **all** integers $a\ge2$, $1\le c\le a$, and $b\ge a+c-1$,

$$
\boxed{\widehat r(F(a,1,1),F(b,c,1,1))=3b+2a+1.}
$$

The earlier general peeling theorem (claim 003) gives the exact joint residual lower $J=2b+a+2$; direct antidiagonal arithmetic gives $W=3b+2a+1$.

For $a\ge4$, since $b\ge a+c-1\ge a$, put $T=(a+b-2)(a+b-1)/2$. At $b=a$,

$$
T-W=(a-1)(2a-1)-(5a+1)=2a(a-4)\ge0.
$$

Increasing $b$ by one increases $T$ by $D+1=a+b-1\ge7$ but increases $W$ by three, so condition 2 of Theorem A continues to hold.

For $a=3$, $b$ odd gives condition 1. If $b$ even, the hypotheses imply $b\ge4$, and $D=b+1$, $W=3b+7\le(b+1)(b+2)=D(D+1)$, giving condition 3.

For $a=2$, the only possible values of $c$ are one and two. The cases split exhaustively as follows:

- If $b\ge5$ is odd, then $W=3b+5\le b(b+1)=D(D+1)$, giving condition 3.
- If $b\ge8$ is even, then $W=3b+5\le b(b+1)/2=D(D+1)/2$, giving condition 2.
- The remaining even cases $b=4,6$, with either permitted $c$, are settled by the *isolated-regular-core* exclusion proved immediately below.
- For $b=3$, with $c=1$ or two, the specialized **nine-cubic-vertex matching lemma** below supplies the forbidden degree split.
- The single remaining case is $(a,b,c)=(2,2,1)$, proved by the **complete 106-class** path-and-cycle certificate below.

**Even boundary $b=4,6$.** Suppose an original-arrowing graph has at most $W-1$ edges. The residual lower bound gives $\Delta\le D=b$. The required original blue forest has at least $R_m=b+c+6$ nonisolated vertices. If $k\ge2D+2$, then $2e\ge R_m+(D-1)(2D+2)$, which is impossible at $b=4$ since $2e\le32$ but the right side is at least $11+30=41$, or at $b=6$ since $2e\le44$ but the right side is at least $13+70=83$. Hence $k\le2D+1$.

Both caps $1,b-1$ are odd. By the uniqueness theorem, failure of their capped partition forces an isolated connected odd-order degree $b$ regular component $C$, with $|C|\ge b+1$ and $b|C|/2\le W-1$.

For $b=4$, the only odd possible core orders are five and seven. At order five, the complement has at most $16-10=6$ edges. Colour $C$ red and its complement blue. The red forest $F(2,1,1)$ needs seven vertices, more than five; the blue forest $F(4,c,1,1)$ needs $6+c\ge7$ edges, more than the complement has. At order seven, the complement has at most $16-14=2$ edges. Colour $C$ blue and the complement red: the blue target needs at least $4+c+6>7$ vertices, and the red target needs four edges, more than the complement. Both choices avoid both targets, contradiction.

For $b=6$, the only feasible odd core order is seven: its 21 edges leave at most one exterior edge in the $W-1=22$ budget; order nine would require 27. Colour the core blue and the exterior red. The blue target needs $6+c+6>7$ vertices, and the red target needs four edges; neither appears. This completes the $b=4,6$ exclusions.

**Nine-cubic-vertex matching lemma (new sharpening).** Every finite simple graph of maximum degree at most three with **at most nine degree-three vertices** has a matching covering every degree-three vertex. Equivalently it admits a red degree-one / blue degree-two edge partition.

*Proof.* Apply the ordinary Lovász $(g,f)$ theorem with $g(v)=\max(0,d(v)-2)$, $f(v)=\min(1,d(v))$. If there is no such factor, some disjoint $S,T$ have a violated integer cut $0\le A<q$, with $3A\ge2e(S)+4e(T)+e(S,U)+2e(T,U)$. Every component counted by $q$ consists of degree-three vertices and has odd $|C|+e(C,T)$; degree-zero components never count.

For a counted component of size $r\le3$, its outgoing boundary has at least $r(4-r)\ge3$ edges, hence its weighted boundary $e(C,S)+2e(C,T)$ is at least three. For $r=4$, the outgoing boundary has even size because $3r=12$ is even, while the parity condition forces $e(C,T)$ odd and at least one; therefore the boundary has at least two edges and its weighted boundary is at least $2+1=3$. Thus **every counted component of order at most four pays at least three**.

With at most nine cubic vertices, there can be at most one counted component of order five or more. If there is none, $3A\ge3q$ contradicts $A\le q-1$. Otherwise the other $q-1$ components pay at least $3(q-1)$, so the large component must have **zero** outgoing boundary. It is isolated and cubic. The handshake lemma forces its order even, while the counted parity condition becomes $|C|$ odd. Contradiction. Hence the $(g,f)$ factor exists. QED.

For $b=3$, the predicted $W$ is fourteen, so a smaller original-arrowing $G$ has $e\le13$ and $\Delta\le D=3$. The original blue forest $F(3,c,1,1)$ requires $9+c$ nonisolated vertices. With $k$ cubic vertices,

$$
26\ge2e(G)\ge3k+((9+c)-k)=9+c+2k.
$$

Consequently $k\le8$ for $c=1$, and $k\le7$ for $c=2$. The nine-cubic matching lemma provides the forbidden $(1,2)$ partition, contradicting original arrowing.

**Final boundary $(a,b,c)=(2,2,1)$.** Here $J=8$, $W=11$ and $D=2$. A hypothetical original Ramsey host with at most ten edges must have $\Delta\le2$ by vertex deletion. Add disjoint single edges until it has exactly ten edges; arrowing and the degree bound are preserved.

Up to isolates, every ten-edge graph of maximum degree at most two is a disjoint union of nontrivial path components with positive edge counts and cycle components with at least three edges. Classify by the unordered multiset of typed component edge counts, totaling ten. There are exactly **106** nonisomorphic types: 42 acyclic, 45 with one cycle, 17 with two cycles and two with three cycles.

The standard-library deterministic source \`verify_d2_original_211_2111.py\` exhausts all 106 types and **all $106\cdot2^{10}=108{,}544$ red/blue colourings**, comparing two *independent* non-induced, vertex-disjoint star-forest embedding tests for each colouring: (i) explicit two-edge-star-plus-disjoint-matching search, and (ii) general edge-mask embedding enumeration with upward-closure subset DP. The two methods agree in all classes. Each class has at least one colouring with neither red $F(2,1,1)$ nor blue $F(2,1,1,1)$. The deterministic 106-witness JSON-content digest is SHA-256 \`2840d4d0a16690272b3052a33e21d8b487ce717e982879899735af3577680aaf\`. The script actually constructs the witnesses; this is a **complete finite proof** after the universal maximum-degree reduction, not a random search or claim of a universal lemma verified on samples. It is not Lean kernel certification.

No ten-edge host arrows the original pair. Thus its size-Ramsey number equals the canonical eleven-edge upper bound. Every B1 case has now been proved.

### B2. Nonuniform equal-leading three-versus-four original family

For all integers $a\ge4$,

$$
\boxed{\widehat r(F(a,2,1),F(a,1,1,1))=5a+3.}
$$

The previously proved exact joint residual minimum is $J=3a+4$, hence $W=5a+3$. For $a\ge5$,

$$
D(D+1)/2-W=(a-1)(2a-1)-(5a+3)
=2(a^2-4a-1)>0.
$$

Apply Theorem A(2). Only $a=4$ requires a separate argument.

For $a=4$, $D=6$, $W=23$, and a smaller original Ramsey host has at most 22 edges, maximum degree at most six and at least eleven nonisolated vertices (from its all-blue copy of $F(4,1,1,1)$). If $k\ge14$ vertices had degree six, then $2e\ge11+5k\ge81>44$, contradiction. Hence $k\le13$. The caps are $(3,3)$, both odd, so a failed split forces an isolated odd-order degree-six regular component $C$. It must contain at least seven vertices and at most 22 edges total, so $3|C|\le22$ forces $|C|=7$. The exterior has at most one edge. Colour the core red, exterior blue. Red $F(4,2,1)$ needs ten vertices, exceeding seven; blue $F(4,1,1,1)$ needs seven edges, exceeding one. Contradiction. The canonical 23-edge upper host attains the prediction.

### B3. Sharp unequal-profile two-parameter original family

For **all** integers $a\ge3$ and $b\ge2a-2$, with no parity restrictions,

$$
\boxed{\widehat r(F(a,1,1),F(b,a-1,2,1))=3b+2a+2.}
$$

The source-locked residual-profile mismatch theorem gives $J=2b+a+3$, and direct antidiagonal arithmetic gives $W=3b+2a+2$.

For $a\ge4$, at minimal $b=2a-2$ the degree threshold is $D=3a-4$ and

$$
D(D+1)/2-W=(9a^2-37a+20)/2>0.
$$

This is positive at $a=4$ and increases thereafter. Increasing $b$ increases the quadratic threshold by $D+1$ and $W$ by three; since $D\ge8$, condition 2 persists for every larger $b$.

For $a=3$, the admissible $b$ begin at four. At $b=4$, $D=5$ and $W=20\le D(D+1)=30$, and the leading sizes have opposite parity: condition 3 applies. At $b=5$ the leading sizes are both odd, so condition 1 applies. For $b\ge6$, $D=b+1$ and

$$
D(D+1)/2-W=(b^2-3b-14)/2\ge0,
$$

so condition 2 applies. This completes every parity.

## Further original fixed cases inherited without a new graph census

The admitted monotone plateau theorem proves $J=15$ for original red $n=(3,2,1)$ and all five blue profiles $m=(4,c,d,1)$ with $1\le c\le3$ and $1\le d\le\min(c,2)$. In all five cases $W=21$ and $D=5$, so the mixed-parity criterion $W\le D(D+1)=30$ proves

$$
\widehat r(F(3,2,1),F(4,c,d,1))=21
$$

for all five profiles. These fixed original deductions use the same proven parent $J=15$; no redundant fourteen-edge host search is needed.

## Evidence and unresolved boundary

\`verify_core_original_transfer.py\` independently recomputes all original and residual antidiagonal sums with two index conventions and tests **8,749** exact parameter instances from the three infinite families and the five plateau cases, checking the precise qualifying analytic gates or the explicit boundary cases. These are bounded arithmetic corroborations, **not a numerical proof of the all-host graph theorems**.

\`verify_d2_original_211_2111.py\` is the **complete** independent-oracle 106-class finite graph proof specifically for the one forced degree-two equality boundary. This finite proof depends only on the universal degree bound from an earlier sharp residual theorem, which remains paper-level UNDER_REVIEW.

All unbounded graph deductions rely on already source-locked published ordinary Lovász factor theory and previous protected GCL sharp-residual proofs. They remain UNDER_REVIEW until substantive mathematical adjudication. Unrestricted joint residual issue #3490 and original Erdős #561 remain **OPEN/PARTIAL**. Neither result is claimed as MATHCERT/public certification.
