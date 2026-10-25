# Erdős #41: a strict coupled PPZ–PZZ gap obstruction

**24 October 2026 | Research candidate | GCL Track A/B/D.** This is a **finite, exact** theorem for repetition-permitted B3 sets, with a genuinely strict coupling of two independent obstruction families and a useful gap-transfer necessary condition. It is **not** an infinite positive-density refutation or a proof of Erdős #41. Source and tests require independent Track C scrutiny.

## 1. Exact two-sided constraints

For a finite integer set S define

$$
Q(S)=\{s+s':s,s'\in S,\ s\le s'\},
\qquad
\Delta_1(S)=\{s-s':s,s'\in S,\ s>s'\},
$$

$$
\Delta_2(S)=\{q-q':q,q'\in Q(S),\ q>q'\}.
$$

B3 means uniqueness of all three-summand unordered multisets, **including repetitions**; in particular B3 implies B2.

**Theorem A (two distinct forbidden structures).** Suppose P is a genuine B3 set and Z is a disjoint future candidate set.

* If $P\cup Z$ is B3, then every two distinct future points u,v must satisfy $|u-v|\notin\Delta_2(P)$. This is the old-old-new (**PPZ**) forbidden-distance graph.
* If $P\cup Z$ is B3, then $\Delta_1(P)\cap\Delta_2(Z)=\varnothing$. This is the old-new-new (**PZZ**) obstruction. It includes hyperedges supported on up to four different future points, because distinct unordered future pairs may reuse some points.
* Z must itself be B3.

In particular, for any future triple $x<y<z$ with successive gaps

$$
a=y-x,\qquad b=z-y,
$$

its **necessary** conditions are

$$
\boxed{
a,b,a+b\notin\Delta_2(P),
\qquad
|a-b|\notin\Delta_1(P)\cup\{0\}.
}\tag{COUPLED-GAP-TRANSITION}
$$

**Proof.** If $q+u=q'+v$ for distinct $q,q'\in Q(P)$, then the two distinct old-old-new three-summand multisets collide; hence no future pair distance lies in $\Delta_2(P)$. Likewise if $p+q_Z=p'+q'_Z$ for $p\ne p'\in P$ and distinct unordered future pair sums $q_Z,q'_Z$, then distinct old-new-new triples collide. If the two future pair sums are equal, Z already fails B2 and thus B3. For the chosen x,y,z, the two future pair sums $2y$ and $x+z$ differ by $|a-b|$; equality is a forbidden three-point arithmetic progression and any nonzero difference in $\Delta_1(P)$ is PZZ collision. The three pairwise distances of the future triple are a,b,a+b, which must avoid PPZ. QED.

These are necessary for any global B3 union without a separation assumption. At **far translation** of an individually B3 future block, the two reciprocal conditions are together sufficient because triple groups containing 0/1/2/3 future elements have disjoint sum bands. A selected PPZ constraint on its own is never sufficient to certify the whole union.

## 2. Strict joint obstruction: each separate channel admits three, both together admit only two

Fix the old genuine B3 prefix $P=\{1,2\}$ and let $J=[100,107]\cap\mathbb Z$, a future window of **eight** integer positions.

The spectra are exact:

$$
Q(P)=\{2,3,4\},\quad\Delta_1(P)=\{1\},
\quad\Delta_2(P)=\{1,2\}.
$$

**Theorem B (strictly submultiplicative joint capacity).** Every genuine B3 extension satisfies

$$
\boxed{
|Z|\le2\quad\text{for all }Z\subseteq J
\text{ such that }P\cup Z\text{ is B3}.
}\tag{STRICT-COUPLED-WINDOW-CAPACITY}
$$

The bound is sharp. In contrast,

$$
\begin{aligned}
\max\{|Z|:Z\subseteq J,\ Z\text{ B3},\ \Delta_1(Z)\cap\Delta_2(P)=\varnothing\}&=3,\\
\max\{|Z|:Z\subseteq J,\ Z\text{ B3},\ \Delta_2(Z)\cap\Delta_1(P)=\varnothing\}&=3.
\end{aligned}
$$

Thus the joint maximum 2 is **strictly smaller than the minimum of the separate maxima** (3). This shows a genuine joint restriction, not merely another formulation of the existing PPZ-only distance-graph bound.

**Elementary proof.** Suppose x<y<z in J are three globally compatible future elements. PPZ forbids distances 1 and 2, so their consecutive gaps a,b are each at least 3. Since the window has diameter 7, $a+b\le7$. Hence the only possibilities are

$$
(a,b)\in\{(3,3),(3,4),(4,3)\}.
$$

The pair (3,3) is an arithmetic progression, so Z is not B3. Each of (3,4) and (4,3) has $|a-b|=1\in\Delta_1(P)$, and yields a PZZ collision using the future pair sums 2y and x+z. This excludes every three-point Z. Adding further elements cannot repair a collision. Conversely $Z=\{100,103\}$ gives a genuine five-element B3 union P∪Z, proving the upper bound sharp.

**Independent-feasibility controls.** The *PPZ-only plus internal B3* demand of three points is met by

$$
Z_{\mathrm{PPZ}}=\{100,103,107\};
$$

it fails only PZZ, because $|2\cdot103-(100+107)|=1$. The *PZZ-only plus internal B3* demand of three points is met by

$$
Z_{\mathrm{PZZ}}=\{100,102,107\};
$$

it fails PPZ, because $102-100=2\in\Delta_2(P)$. Both future three-point sets are genuinely B3 individually, and both have all old/new triple-count sum bands far-separated from one another. Exhaustive exact enumeration yields two such three-point witnesses for each separate channel but **zero** for their intersection.

In fact every $Z\subseteq J$ with $|Z|\ge3$ creates a positive sixth-moment collision defect in $P\cup Z$. The sharp finite minimum at $|Z|=3$ is **18**, attained at $Z=\{100,102,107\}$. This number is an exact finite defect, not an asymptotic density loss.

## 3. A reusable gap-transition packing lemma

**Theorem C (short-block exclusion from any adjacent old pair).** Let P be **any** genuine B3 prefix containing two consecutive integers p,p+1. Let J be **any** eight-consecutive-integer interval disjoint from P. Then every B3-compatible Z⊂J has $|Z|\le2$. No far separation is required.

**Proof.** The old pair creates $1\in\Delta_1(P)$ and $1,2\in\Delta_2(P)$, since $Q(P)$ includes $2p,2p+1,2p+2$. The same three-gap classification as Theorem B applies to any three future elements within diameter 7. Therefore no triple is compatible. QED.

The window length eight is **sharp as a universal exclusion statement**: for $P=\{1,2\}$ and $Z=\{100,103,108\}$, a future interval of nine consecutive integers contains three points and the complete union is genuinely B3.

An equivalent dynamic necessary condition emerges for successive gaps of *any* legal future tail Z={z_1<...<z_k} after such a prefix. Writing $g_i=z_{i+1}-z_i$, every legal B3 extension must satisfy

$$
\boxed{g_i\ge3,\qquad |g_{i+1}-g_i|\ge2.}\tag{GAP-TRANSFER}
$$

Pairwise sums of adjacent gaps are therefore each at least 8; the span of k future points obeys the exact necessary lower bound

$$
\boxed{
z_k-z_1\ge
8\left\lfloor\frac{k-1}{2}\right\rfloor
+
3((k-1)\bmod2).
}\tag{LOCAL-GAP-PACKING}
$$

**Proof.** Every gap is a future pair distance, so PPZ excludes 1 and 2. Any two adjacent gaps must be different because a three-point arithmetic progression violates B2; they also cannot differ by exactly 1 because this generates a PZZ collision with old difference 1. Pair adjacent successive gaps into $\lfloor(k-1)/2\rfloor$ disjoint pairs, each summing to at least 8; an odd residual gap is at least 3. QED.

**Important sharpness qualification.** The numerical lower bound is optimal for the **stated local gap inequalities** (alternating gaps 3 and 5), but for k≥4 those alternating-gap configurations may violate other B3 constraints. It is therefore a *necessary* lower bound, not a formula for the true optimal global B3 packing number.

## 4. Exact coupled conflict hypergraph and the next analytical target

For a given finite prefix P and finite candidate future window J, construct:

1. A **PPZ graph** with vertex set J and edges at distances in $\Delta_2(P)$.
2. A **PZZ hypergraph** containing the support of every pair of distinct unordered two-multisets of elements of J whose pair sums differ by an element of $\Delta_1(P)$. These hyperedges have size 2, 3, or 4 (when the old difference is nonzero).
3. A **new-block B3 obstruction hypergraph** containing supports of distinct unordered three-multisets of elements of J with the same sum; these have size at most 6.

A chosen future set Z obeys each corresponding channel exactly when it contains no hyperedge from that channel. For sufficiently remote J (separating old/new triple-count classes), their **joint** hypergraph independence is equivalent to full B3 compatibility. For near-field J, additional cross-colour-count collisions can occur; this exact equivalence is not claimed without separation.

Theorem B shows why replacing all three obstruction channels by independent scalar capacity estimates fails: each individual independence number can permit population k, while their **intersection** forbids it. A genuine nontrivial multiscale forcing theorem would have to use evolving **joint** graph-hypergraph occupancy and the *cumulative* lower counting demands, not the separate margins.

**Boundary:** Although the local gap-transition bound is exact and strict for eight-position windows, it gives only linear-length packing information. It cannot by itself improve the critical normalized $N^{1/3}$ density behavior. Fixed finite B3 prefixes still admit remote scaled finite B3 extensions at prefix-dependent scales. To settle Erdős #41 one must prove a global, c-uniform, growing-prefix incompatibility or find a demonstrably stronger invariant.

**Governance:** candidate mathematical research for coordinator #2789; substantive Tracks A #2790, B #2791, D #2793; request independent source-locked adversarial audit in Track C #2792. No specialist RESULT/1, MathCert, or theorem admission claimed.
