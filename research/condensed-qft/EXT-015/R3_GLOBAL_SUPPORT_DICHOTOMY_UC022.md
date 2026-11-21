# EXT-015 REACH / R3 / UC022 — opposite verdicts for the original global support comparison

**Candidate theorem.** For the original real liquid degree-two support comparison, the continuum hypothesis implies failure through a nonzero class invisible in every output coordinate. The partition hypothesis $\mathrm{PH}_1$ of Bannister, Bergfalk, Moore and Todorcevic implies success. Both conclusions use the source, targets and boundary equation of 067. The relative independence conclusion requires the stated consistency assumptions.

## 1. Scope and plan

Work in the real liquid heart with fixed exponent $0<p\leq 1$ and the universe of [067](R3_EVALUATED_RELATION_COVER_067.md). Retain its actual projective presentation with second kernel $j:K_1\to P_1$, its source $H$, and its coefficient $G$ with compact-support stages $G_b$. The target is

$$
\forall f:K_1\to G,\quad
f=\iota_b f_b+\psi j
\quad\text{for some }b,\ f_b:K_1\to G_b,\ \psi:P_1\to G.
$$

Retain the coefficient realization in [084](R3_POSITIVE_SUPPORT_ATTEMPT_084.md) and [094](R3_NEW_INPUT_AUDIT_094.md). Write $G\simeq E=\bigoplus_{n\in\mathbb N} B_n$, $B_n=\underline{s}$, with finite prefixes of $E$ and actual stages of $G$ factoring through one another. Let $\mathscr R$ be the poset of positive rapid weights modulo mutual domination. Write $r\preceq t$ when $r_i\leq C t_i$ for all $i$ and some $C<\infty$. Set

$$
W_n=s^{\mathbb N},\qquad
V_{r,n}=\{a\in W_n:r_i q_k(a_i)\longrightarrow 0\text{ for every }k\},\qquad
X_{r,n}=W_n/V_{r,n},\qquad X_r=\bigoplus_n X_{r,n}.
$$

The $q_k$ are the increasing seminorms of $s$ in (94.4). The transition $X_{t,n}\to X_{r,n}$ takes a representative to the same representative. Derived limits below are of ordinary abelian-group diagrams. The admitted computations (84.16), (84.20), (94.14) identify $\mathrm{Ext}^2(H,E)$ with $\lim^1_{\mathscr R}X_r$, naturally in finite coordinate projections and inclusions. The same computation applies to individual $B_n$. Finite prefixes give exactly the image of the compact-support stage comparison by 067. Surjectivity asks for (84.19), with separately finite-supported corrections and one finite set of output coordinates for the entire cochain.

First patch countable systems in one coordinate, then test additivity across infinitely many coordinates. Next check the published partition argument against the concrete rapid-weight order and use the genuine projective comparison to return both results to the liquid category. Finally freeze the candidate for distinct review of the two residual channels and the foundations.

## 2. Countable lifting in the actual quotients

**Lemma.** For any increasing sequence $(r^{(m)})_{m\geq 1}$ in $\mathscr R$, the natural map $W_n\to\lim_m X_{r^{(m)},n}$ is surjective.

Take compatible classes with representatives $a^{(m)}$. Compatibility says $a^{(m)}-a^{(j)}\in V_{r^{(j)},n}$ for $j\leq m$. Choose strictly increasing integer cutoffs $N_m$ so that for all $i\geq N_m$, $j\leq m$ and $k\leq m$,

$$
r^{(j)}_i q_k(a^{(m)}_i-a^{(j)}_i)\leq 1/m .
$$

Define $a_i=a^{(m)}_i$ on $N_m\leq i<N_{m+1}$ and choose arbitrary initial columns. For fixed $j,k$ the bound gives the required limit, so $a-a^{(j)}\in V_{r^{(j)},n}$. Each column belongs to $s$, which is all the ambient $W_n$ requires. On a countable ordinal segment without a last element, lift on an increasing cofinal sequence, then use compatibility to recover the other values. On a segment with a last element, choose a representative there. The empty segment has zero limit.

## 3. Under CH the original comparison has a nonzero phantom class

The proof uses a cofinal family of rapid weights of cardinality at most $\aleph_1$. CH supplies one since a rapid weight is a sequence of reals. Enumerate a cofinal family as $(u_\xi)_{\xi<\omega_1}$. By countable direction (94.11), take an upper bound $w_\xi$ of $u_\xi$ and the previously chosen $r_\eta$, and set $r_\xi=\sqrt{w_\xi}$. This is cofinal and for every $\eta<\xi$ satisfies $r_{\eta,i}/r_{\xi,i}\to0$, since $r_{\eta,i}\leq C_\eta w_{\xi,i}$ and $w_{\xi,i}\to0$. Each comparison in the chain is strict by the reciprocal ratio. At any weight the ordinal tail of stages above it is nonempty and directed. Cofinal restriction therefore computes the same derived limits, naturally for the sum and each coordinate.

Identify the copies of $W_n$ by their copies of $s$. On the chain let $L_\xi$ denote the common one-coordinate quotient $X_{r_\xi,n}$. By the lemma and the quotient map from $W_n$, the map $L_\xi\to\lim_{\eta<\xi}L_\eta$ is onto. Write $J_\xi$ for its kernel. For fixed nonzero $h\in s$, the matrix $a_i=h/r_{\xi,i}$ gives a nonzero class $v_\xi\in J_\xi$. At $\xi$ the weighted sequence is constantly $h$. At every earlier stage it tends to zero in every seminorm by the ratio condition.

Choose a linear section of each surjection $L_\xi\to\lim_{\eta<\xi}L_\eta$. Transfinite recursion gives an isomorphism of inverse systems

$$
L_\xi\simeq\prod_{\eta\leq\xi}J_\eta
$$

with truncation maps. The earlier decompositions identify the target of the surjection with $\prod_{\eta<\xi}J_\eta$. The new section splits off that product and projection to every earlier stage is truncation. This is an algebraic decomposition. Use the same decomposition for each $n$.

Each one-coordinate chain 1-cocycle $\gamma$ is a boundary. In the $\eta$ component at stage $\xi\geq\eta$, set $\beta_\xi(\eta)=\gamma_{\eta,\xi}(\eta)$. Its difference with the value at an earlier stage is the required component of $\gamma$ by the cocycle identity based at $\eta$. Hence $\lim^1_\xi L_\xi=0$ and every finite prefix has zero first derived limit.

**Coherent family.** There are finite-to-one maps $e_\xi:\xi+1\to\mathbb N$ such that $e_\zeta|_{\xi+1}$ and $e_\xi$ disagree at only finitely many arguments for $\xi<\zeta$. Construct them by recursion. Start with any value at zero. At a successor extend the previous map by one value. At a nonzero countable limit $\zeta$, take an increasing sequence $\xi_m<\zeta$ cofinal in $\zeta$. Use $e_{\xi_0}$ through $\xi_0$. On each interval $(\xi_m,\xi_{m+1}]$ use $e_{\xi_{m+1}}$, changing the finitely many values below $m$ to values at least $m$. Choose any value at $\zeta$. A given fiber is finite since it meets only finitely many intervals and is finite in each. On any segment through $\xi_j$ there are only finitely many intervals. Inductive coherence and the finite changes give agreement up to finitely many arguments there, and hence on every smaller initial segment.

Use the product decompositions to define $y_\xi\in\prod_n L_\xi$ with entries, for $\eta\leq\xi$,

$$
y_\xi(\eta,n)=
\begin{cases}
v_\eta,& e_\xi(\eta)=n,\\
0,& e_\xi(\eta)\ne n.
\end{cases}
$$

For $\xi\leq\zeta$ set $\alpha_{\xi,\zeta}=y_\zeta|_\xi-y_\xi$. The finite set of changed ordinal arguments affects only finitely many output coordinates. Thus $\alpha_{\xi,\zeta}$ belongs to $\bigoplus_n L_\xi$. The differences satisfy the 1-cocycle identity. For each coordinate individually $y$ is a primitive.

**Test against every finite-support correction.** Suppose (84.19) holds for this $\alpha$ with some finite $F$ and corrections $\beta_\xi$. Outside $F$, the family $y_\xi-\beta_\xi$ is compatible. Let $z(\eta,n)$ be its global array on those coordinates, assigning zero on $F$. For each $\xi$ there is a finite $F_\xi$ such that $z(\eta,n)=y_\xi(\eta,n)$ for all $\eta\leq\xi$ and $n\notin F_\xi$. Take $F_\xi$ to contain $F$ and the stagewise support of $\beta_\xi$.

Only finitely many global columns can have infinite support. Otherwise choose countably many such columns and countably many nonzero entries in each. The union lies in one countable initial segment by regularity of $\omega_1$. Each chosen column must be in that segment's $F_\xi$, since the corresponding column of $y_\xi$ has finite support. This contradicts finiteness of $F_\xi$. Replace the finitely many infinite columns by zero. The property with finite $F_\xi$ persists. Now on each initial segment $z$ and $y_\xi$ differ in only finitely many entries, since finitely many columns can differ and their supports there are finite. Every row of $y_\xi$ has exactly one nonzero entry. Thus only finitely many global rows can fail this property, since a countable subset of bad rows would lie in one initial segment. Each remaining row lies in the support of some column, and each column has finite global support. Their countable union cannot cover all but finitely many ordinals below $\omega_1$. This excludes every $F$ and every allowed correction.

By cofinal restriction choose a full-poset representative of the constructed class. Lift it edgewise with finite support to $\bigoplus_n W_n$. Its Roos coboundary is a degree-two cocycle in $V$. Insert it by augmentation in bidegree $(2,0)$ of the actual projective total resolution $D$ of (84.11)–(84.16). This gives a map $\zeta:D_2\to E$ killing $d_3^D$. With the comparison map $v:R_\bullet\to D_\bullet$ of §4 in 084, $\zeta v_2$ descends along $\pi_2:P_2\twoheadrightarrow K_1$ to a genuine liquid $f:K_1\to E$. Naturality identifies its class with the constructed quotient class. If $f$ were the sum of a bounded-stage map and an actual boundary, the quotient class would satisfy (84.19). The contradiction includes $F=\varnothing$. Formula (94.16) consequently gives a genuine nonlifting map $K\to Q$ modulo product lifts. The infinitely coordinate-visible channel has zero target here because each single-coordinate degree-two group vanishes.

## 4. Under PH1 the original comparison is an isomorphism

Use $\mathrm{PH}_1$ as in [Bannister, Bergfalk, Moore and Todorcevic, Definition 3.2](https://ems.press/content/serial-article-files/51446). For a coloring of ordered pairs from the set $\Omega$ of strictly increasing functions $\mathbb N\to\mathbb N$, the hypothesis gives values on singletons and pairs, ordered by eventual domination under face inclusion, with singleton values eventually dominating their inputs. The colors of the two singleton-to-pair edges are constant across all pairs. We use distinct lifts for distinct vertices and handle degenerate pairs by the singleton choice.

For any $g:\mathbb N\to\mathbb N$, define

$$
d_g(i)=\max(\{0\}\cup\{k:1\leq k\leq i,\ g(k)\leq i\}),\qquad
\rho_g(i)=(1+i)^{-d_g(i)} .
$$

The exponents tend to infinity, so these are positive rapid weights. If $g\leq^* h$, then for sufficiently large $i$ the index realizing $d_h(i)$ lies beyond the finitely many exceptions. It satisfies $g(k)\leq i$, so $d_g(i)\geq d_h(i)$ eventually and $\rho_g\preceq\rho_h$. Given any rapid $r$, choose $g(k)$ with $r_i\leq(1+i)^{-k}$ for $i\geq g(k)$ and $k\geq1$. Then $r\preceq\rho_g$. In the finitely many places with zero exponent one can enlarge the domination constant. Any pointwise larger threshold function also works.

Fix a bijection $\mathbb N\times\mathbb N\to\mathbb N$. Decode each increasing function into rows $g_n$ and send it to $(\rho_{g_n})_n$. This map from eventual domination on $\Omega$ to the coordinatewise order on $\mathscr R^{\mathbb N}$ is monotone. A finite set of exceptions in the flattened arguments leaves only finitely many exceptions in each row, which its weight map absorbs. The map is cofinal. Flatten a tuple of thresholds and choose a strictly increasing pointwise majorant. Every tuple has continuum many such majorants, so lifts of distinct tuples can be chosen distinct by transfinite recursion, since there are at most continuum many tuples.

Pull back a coloring of pairs of tuples by this map, apply PH1, then push the singleton and pair values forward on the chosen lifts. Domination of singletons and all face inequalities hold in the full coordinatewise order. The two induced singleton-to-pair edges have the common color. These are the hypotheses of Theorem 8.4 with derived degree one, $P_i=\mathscr R$ and exceptional set empty. Apply it to $X_{r,n}$. The coordinate projections and the diagonal in $\mathscr R^{\mathbb N}$ are cofinal, the latter by countable direction in (94.12). In both cases the upper-bound categories are nonempty and directed. Cofinal restriction gives

$$
\bigoplus_n \lim\nolimits^1_{\mathscr R} X_{r,n}
\ \simeq\
\lim\nolimits^1_{\mathscr R}\bigoplus_n X_{r,n}.
$$

The corrections can also be read directly from the cocycle. Use the single-row map $\Omega\to\mathscr R$, monotone and cofinal by the same proof. Color a comparable pair of weights by a finite-prefix bound on the support of its cocycle value, assigning a default color on incomparable pairs. Pull back the coloring and apply PH1 as above. For $r\prec t$ the induced $F_r\succeq r$, $F_{r,t}\succeq F_r,F_t$ have a single support bound on $(F_r,F_{r,t})$ and $(F_t,F_{r,t})$. Set $\beta_r=-\alpha_{r,F_r}$. The cocycle identity gives

$$
\alpha_{r,t}-(\beta_t|_r-\beta_r)=
\alpha_{F_r,F_{r,t}}|_r-\alpha_{F_t,F_{r,t}}|_r .
$$

This holds trivially for $r=t$, where the difference is zero. The right side has the same finite-prefix bound everywhere, and each correction has finite support as a single cocycle value. This proves (84.19). Equations (84.22)–(84.23) give the actual boundary $\psi:P_1\to G$ and factor the corrected cocycle through some $G_b$. Together with 067 injectivity this proves the original comparison under PH1, accounting for both residual channels.

## 5. Foundations, hostile controls and custody

Countable patching and the cofinal encoding are ZFC arguments. The negative direction uses the cofinal chain supplied by CH. The positive direction uses PH1 for arbitrary colorings. Theorem 6.1 of the cited paper gives PH1 in the indicated Hechler extension of a model with a weakly compact cardinal. Gödel's constructibility theorem supplies the relative consistency of CH. With those consistency assumptions and the admitted source results valid in each model, the original R3 comparison has opposite verdicts in models of ZFC. The base programme works in ZFC.

Every edge of the negative construction has exact finite support and every coordinate has a primitive. The global failure holds after arbitrary separately finite-supported boundary corrections and after removing any fixed finite set. The class returns through the actual fixed projective cover. The one-coordinate patching estimates control all Fréchet seminorms. The positive proof controls the full weight poset by cofinality. These checks distinguish the construction from a product-valued substitute, a sequence of local scalar primitives and a support-escaping boundary.

Frozen input is commit 1540ed6bc7c40c8f73a2866ea3440905d62136ce, retained ref research/reach-r3-uniformization-input-20261121. CP255 was bound at 894fd2cae8345003c093f3d9d98bc62a33a1965d. The consumed 067, 084, 094 and [UC021](R3_CECH_INPUT_ACCEPTANCE_UC021.md) blobs are respectively 7069938ce1e75f946e2f4ff70fcabb2f073065e9, 932be6cc3445182a8423b23cc4840fe7ad685ced, f0732cb96a27f540a2209a54d43ced97abb94503, and c20cde6a0c0ec64a1be5ab0ba39df121ac5adf43. This is the root-authored candidate for distinct nonauthor review. Scientific checks are mathematical proofs and hostile controls. Source validation uses the existing unpinned isolated Windows Python with external GCL caches. General Gaussian/Wick source closure and final integration remain open.
