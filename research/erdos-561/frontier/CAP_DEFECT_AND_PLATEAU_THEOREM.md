# Erdős #561: quantitative cap defect and frontier plateau obstruction

**Date:** 2026-11-25. **Scope:** finite simple graphs; vertex-disjoint noninduced positive star forests. PAPER UNDER_REVIEW; no MATHCERT, priority claim, or full conjecture closure. Continuation of [#3490 frontier reformulation](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3490#issuecomment-7157314480). Prior source: ../unique-core/GENERAL_SATURATED_CORE_UNIQUENESS_THEOREM.md; compare the spare Vizing class in ../joint-general/UNIFORM_ALL_COMPONENTS_EULER_DEFECT_THEOREM.md. The present bound charges exceptional edges to saturated vertices, not the total edge budget.

## 1. Quantitative cap repair (unconditional)

Let $G$ have maximum degree at most $D=\alpha+\beta$, with positive integer caps $\alpha,\beta$. Write $p=|\{v:d(v)=D\}|$. There is an exceptional edge set $Z$ with

$$
|Z|\le \lfloor p/(D+1)\rfloor
$$

such that $G-Z$ has a red/blue edge colouring with maximum red degree at most $\alpha$ and maximum blue degree at most $\beta$.

Define $g(v)=\max(0,d(v)-\beta)$ and $f(v)=\min(\alpha,d(v))$. For disjoint $S,T$, put $U=V(G)\setminus(S\cup T)$ and

$$
A=f(S)+\sum_{t\in T}(d(t)-g(t))-e(S,T).
$$

By the ordinary Lovász $(g,f)$ factor theorem (Kano and Saito, [Theorem 1](https://gorogoro.cis.ibaraki.ac.jp/web/papers/newKanoSaitoFactor1984.pdf)), the required red factor exists iff $A\ge q$, where $q$ counts components $C$ of $G[U]$ entirely tight ($g=f$) with $f(C)+e(C,T)$ odd. Counted components consist entirely of degree-$D$ vertices: the only other tight vertices are isolates, which cannot contribute odd parity.

The proportional bounds $Df(v)\ge\alpha d(v)$ and $D(d(v)-g(v))\ge\beta d(v)$ give

$$
DA\ge 2\alpha e(S)+2\beta e(T)+\alpha e(S,U)+\beta e(T,U).
$$

In particular $A\ge0$. Every counted component of order $r\le D$ sends at least $r(D-r+1)\ge D$ edges to $S\cup T$. These edges are disjoint between components, and their weights are at least one. Thus $A\ge q_{\rm small}$, so $q-A\le q_{\rm large}\le\lfloor p/(D+1)\rfloor$. Here large means order at least $D+1$.

Set $h=\max_{S,T}(q-A)$, nonnegative by choosing $S=T=\varnothing$. If $h=0$, the factor theorem already supplies a split. Otherwise adjoin one new vertex $z$ adjacent once to every original vertex, with $g(z)=0,f(z)=h$, leaving all original bounds unchanged. These bounds remain admissible because $1\le h\le |V(G)|$. Verify the ordinary factor theorem on the augmented graph:
- $z\in S'$: write $S=S'\setminus\{z\}$ and $T=T'$. The cut value is $A+h$, because the added degrees of vertices of $T$ cancel their new edges to $S'$. The counted components and parity are unchanged, so $A+h\ge q$.
- $z\in T'$: write $S=S'$ and $T=T'\setminus\{z\}$. The cut value is $A+|T|+|V(G)|-|S|$, at least $|U|$. The augmented odd count is at most $|U|$ regardless of changed parity.
- $z\notin S'\cup T'$: $z$ joins every remaining original vertex and is not tight, so the odd count is zero. The cut value is $A+|T|\ge0$.

The augmented factor exists. Restrict its red edges to $G$. Red degrees remain at most $\alpha$; complement blue degrees exceed $\beta$ by total at most $h$, since at most $h$ factor edges met $z$. Repeatedly remove a blue edge incident with any vertex exceeding its cap. Each step reduces the total positive blue excess by at least one; no excess increases. After at most $h$ removals the remaining colouring is capped. This proves the stronger $|Z|\le h\le\lfloor p/(D+1)\rfloor$ without any unproved Ramsey assumption. The construction need not make $Z$ a matching.

Sharpness: for even $D$ and odd positive caps summing to $D$, take a disjoint union of $j$ copies of $K_{D+1}$. Each clique requires at least one exceptional edge, by the odd sum of forced red degrees. The theorem gives at most $j$, hence exactly $j$.

## 2. Frontier consequence

For decreasing positive profiles $n,m$ of lengths $s,t$, set $w_\ell=\max_{i+j=\ell}(n_i+m_j-1)$, $W_k=\sum_{\ell=k}^{s+t}w_\ell$, and $L=s+t-k+1$. A frontier host arrows the two suffix forests for every valid pair $i+j=k$.

Use the minimal-counterexample deductions in #3490: choose least $L$ across failures; then $e(H)=W_k-1$, $\Delta(H)=D=w_k-1\ge2$, and the nonisolated count $N\ge L+M_k$, where $M_k$ is the maximum suffix arm sum on this frontier. In every maximizing pair both leading arms are at least two. If a leading arm were one, the monochromatic colouring in the opposite colour, of max degree $D$, would avoid both targets.

Let $P$ be the length of the initial constant plateau of $w_k,w_{k+1},\ldots$. For a maximizing pair let $u$ and $v$ count the repetitions of its leading red and blue arm sizes in their suffixes. Then

$$
P=\max_{\text{maximizing }(i,j)}(u+v-1).
$$

Indeed each such pair can advance by up to $(u-1)+(v-1)$ steps without reducing its sum. Conversely a later maximizing pair with the same sum has an ancestor on frontier $k$ by decreasing its indices; monotonicity forces both ancestor arm sizes equal to the later ones. The ancestor's constant runs permit all those steps.

Take a maximizing pair attaining $P$, with $\alpha=n_i-1,\beta=m_j-1$. If its cap repair needed at most $P-1=u+v-2$ exceptions, assign at most $u-1$ of them red and at most $v-1$ blue. Every red leading star must use an exceptional red edge; pairwise vertex-disjoint leading stars use distinct such edges. The analogous statement holds for blue. Thus neither forest appears, contradiction. In particular the cut deficiency $h\ge P$. Consequently

$$
p\ge P(D+1),\qquad
2(W_k-1)\ge L+M_k+P(D^2-1),\qquad PD<2L.
$$

The last inequality follows from $pD\le2(W_k-1)<2L(D+1)$. These necessary conditions strengthen the old single-core guard when $P>1$. No minimal obstruction can have a completely flat frontier ($P=L$, $D\ge2$).

## 3. Exact threshold and multiple-component cut

A cut attaining $h\ge P$ has at least $P$ large counted components. If it has exactly $P$, the weighted boundary inequality implies $A=q_{\rm small}$ and the total weighted boundary of all large components is zero. Each is therefore an isolated connected $D$-regular component; its parity requires odd order and odd $\alpha$ (hence odd $\beta$, $D$ even).

Thus if $p<(P+1)(D+1)$, the cut exhibits exactly $P$ such isolated odd regular components. Each has order at most $2D+1$ and the exterior has fewer than $D+1$ saturated vertices. The prior unique-core theorem gives a capped split of the exterior. Deleting any one edge of each isolated core destroys its only possible isolated $D$-regular obstruction: every component of the edge-deleted connected core contains an endpoint of the deleted edge if disconnected, and otherwise both endpoints. Apply the same theorem to each core. Precisely $P$ exceptional edges suffice and at least $P$ are necessary by parity. At $p=P(D+1)$ every core is a clique $K_{D+1}$. If either cap is even, or no isolated odd $D$-regular component exists, there must instead be at least $P+1$ large counted components, hence $p\ge(P+1)(D+1)$.

More generally, for $b=q_{\rm large}\ge P$ choose $r\le\min(L,b(D+1))$ saturated vertices spread as evenly as possible among $b$ large components. Write $r=bq_0+t_0$ with $0\le t_0<b$. They have at most $b\binom{q_0}{2}+t_0q_0$ induced edges, since no edges join counted components in $G[U]$. The previous frontier multi-vertex deletion inequality implies the necessary condition

$$
\sum_{\ell=1}^{r-1}(D-w_{k+\ell})\le b\binom{q_0}{2}+t_0q_0.
$$

This is applicable to arbitrary near-flat profiles, not only a fixed number of components.

## 4. Critical isolated-core colouring and tail-packing gate

In the exact-$P$ isolated-core branch of Section 3, write $a=\alpha+1$, $b=\beta+1$, let $c_1,\ldots,c_P$ be the core orders and $C=\sum c_j$. Let $T_{\rm ext}$ be the exterior edge count and fix a capped split of the exterior with $R_{\rm ext}$ red edges and $B_{\rm ext}$ blue edges.

Delete one edge in each core and cap-colour the remainder as above. All non-endpoints have exactly $\alpha$ red and $\beta$ blue incident edges. Each endpoint is deficient by precisely one in one colour. Since $\alpha c_j$ is odd and red degree sum is even, exactly one endpoint is red-deficient, the other blue-deficient. Restoring the edge in red therefore creates exactly one red degree-$a$ vertex, with all other vertices red degree $\alpha$; blue has no degree-$b$ vertex. Restoring it blue interchanges these roles. Thus each core is a switch with a single over-cap vertex and no other leading-star centre.

Let $u,v$ be the leading multiplicities of the selected maximizing pair attaining $P=u+v-1$. Choose exactly $u$ cores to be red switches and the other $v-1$ blue. Blue is automatically defeated. If red occurs, all its $u$ leading stars must be centred at the $u$ unique red over-cap vertices, with all their incident red edges forced. Those stars lie in different cores. Their vertex sets each have size $a+1$ and red degree sum $a^2$, so removing each set removes at least $\lceil a^2/2\rceil$ red edges. Total red edges inside the cores before deletion are $(\alpha C+2u-P)/2$. The red tail must therefore satisfy

$$
\sum_{\ell=i+u}^{s} n_\ell
\le R_{\rm ext}+\frac{\alpha C+2u-P}{2}
-u\left\lceil\frac{a^2}{2}\right\rceil .
$$

Symmetrically, choose exactly $v$ blue switches and $u-1$ red. The same exterior colouring can be used, and the blue tail must satisfy

$$
\sum_{\ell=j+v}^{t} m_\ell
\le B_{\rm ext}+\frac{\beta C+2v-P}{2}
-v\left\lceil\frac{b^2}{2}\right\rceil .
$$

Both inequalities must hold for **every** capped exterior split. Adding, using $R_{\rm ext}+B_{\rm ext}=T_{\rm ext}$, $u+v=P+1$ and $e(H)=DC/2+T_{\rm ext}$, gives the additional necessary tail-edge gate

$$
\sum_{\ell=i+u}^{s}n_\ell+\sum_{\ell=j+v}^{t}m_\ell
\le e(H)+1-u\left\lceil a^2/2\right\rceil
-v\left\lceil b^2/2\right\rceil .
$$

The bound is necessary, not sufficient: the remaining tails still need vertex-disjoint embeddings. For $D=2$, the isolated cores are odd cycles; the repaired colour on each switch consists of one forced two-star and disjoint single edges, and the non-switch colour is a matching.

## 5. A matching-budget component removal gate

Suppose an isolated subgraph $C$ (union of components) has the following property for an integer $r\le L$: for every pair of nonnegative integers $x+y=r$, it admits a colouring whose red matching number is at most $x$ and blue matching number at most $y$. Then $H-V(C)$ satisfies frontier $k+r$ (if nonempty). Indeed each pair at that frontier has an ancestor at frontier $k$, with index differences $x,y$ summing to $r$. Extend an arbitrary exterior colouring by the corresponding matching-budget colouring of $C$. A monochromatic disjoint star forest can lose at most $x$ red components or $y$ blue components inside $C$. It follows that the appropriate suffix survives in the exterior. This uses isolation, not an assumption that optimal embeddings are connected across components. For $r=L$ the successor bound is just zero. Minimality therefore forces

$$
e(C)\le\sum_{\ell=k}^{k+r-1}w_\ell-1.
$$

A triangle has the property with $r=1$ (colour all three edges in the chosen colour), hence a minimal obstruction with $D=2$, $w_k=3$, cannot contain an isolated triangle. Since every triangle in a graph of maximum degree two is isolated, all odd cycles now have length at least five. The $(1,1)$ cap defect is exactly the number of odd cycles: a path or even cycle alternates, an odd cycle needs and suffices with one exceptional edge. The preceding plateau argument forces at least $P$ odd cycles, so the sharper necessary conditions are $e(H)\ge5P$ and $p\ge5P$.

For an even cycle of order $2q$, the matching-budget property holds with $r=q$: use consecutive blocks of $2x$ and $2y$ edges, or a monochromatic cycle at the endpoints of the allocation. For an odd cycle of order $2q+1$, it holds with $r=q+1$: for positive $x,y$, consecutive blocks of $2x-1$ and $2y$ edges have matching numbers $x,y$; monochromatic endpoints again work. These give further explicit component-removal tests in the degree-two regime.

## 6. Boundary

The exceptional-edge count eliminates the one-core branch whenever $P\ge2$; it forces more large components as the plateau grows. At $P=1$ the previous isolated-core obstruction can still survive; at larger $P$ the exactly-$P$ isolated-core branch can survive. The unresolved task is to use smaller target arms and their vertex-disjoint packing requirements to exclude these critical colourings (or construct a true counterexample). The proof does not establish the full frontier conjecture. Bounded checks in the accompanying verifier are corroboration, not general proof.
