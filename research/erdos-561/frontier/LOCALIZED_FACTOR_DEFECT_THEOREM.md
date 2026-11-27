# Erdős #561: exact localized factor-defect apportionment

**2026-11-26. Status:** paper proof UNDER_REVIEW; bounded exhaustive evidence CHECKED separately. All graphs finite and simple; all star forests have positive, vertex-disjoint components, ordinary subgraph containment. No novelty-priority or MATHCERT claim. Full conjecture OPEN.

**Dependencies:** ordinary Lovász (g,f)-factor theorem as source-locked in CAP_DEFECT_AND_PLATEAU_THEOREM.md (protected blob 84f65a064d0de9bf34697da152b802f09dfdc4b9; PR #3748); frontier reduction recorded in #3490. The result below strengthens the previous exceptional-edge bound to an exact two-colour vertex-defect theorem with independently prescribed supports. It does not assume the unresolved frontier inequality.

## 1. Exact localization theorem

Let $d(v)\le D=\alpha+\beta$, with positive integer caps $\alpha,\beta$, and $X=\{v:d(v)=D\}$. Define $g(v)=\max(0,d(v)-\beta)$ and $f(v)=\min(\alpha,d(v))$. For disjoint $S,T$ with $U=V(G)\setminus(S\cup T)$, put

$$
a(S,T)=f(S)+\sum_{v\in T}(d(v)-g(v))-e(S,T).
$$

Here $q(S,T)$ counts components $C$ of $G[U]$ all of whose vertices satisfy $g=f$ and with $f(C)+e(C,T)$ odd. Such counted components consist entirely of saturated vertices; degree-zero isolates cannot contribute. Let

$$
h=\max_{S,T}(q(S,T)-a(S,T)).
$$

As in the prior proof, $a\ge0$, $h\ge0$, and $h\le\lfloor |X|/(D+1)\rfloor$.

**Theorem.** Let $A,B\subseteq X$ be any two dominating sets of $G[X]$, not necessarily equal or independent. For nonnegative integers $r,b$, a colouring exists with all red excess vertices in $A$, all blue excess vertices in $B$, at most $r$ red excess vertices and $b$ blue excess vertices, each exceeding its own cap by exactly one, if and only if $r+b\ge h$. All other vertices respect both caps. At equality the actual numbers are exactly $r,b$ (when their sum is $h$).

In fact the proof needs only the following cut-covering property for each of $A$ and $B$: for every disjoint $S,T$, the number $q_0(A)$ of originally counted components avoiding $A$ is at most $a(S,T)$, and similarly for $B$.

### The cut-covering property

The proportional degree inequalities from #3748 give

$$
Da(S,T)\ge 2\alpha e(S)+2\beta e(T)+\alpha e(S,U)+\beta e(T,U).
$$

Any counted component of order $c\le D$ sends at least $c(D-c+1)\ge D$ edges to $S\cup T$. Any counted component avoiding a dominating set and of order $c>D$ has every vertex adjacent to that set outside the component, necessarily in $S\cup T$; hence its boundary has at least $c>D$ edges. The respective edge contributions are disjoint and have weights at least one. Therefore $q_0(A)\le a$, likewise for $B$. Also $q-a\le q-q_0(A)\le |A|$, so $h\le |A|$ and $h\le |B|$. Budgets can be clipped to these sizes without losing $r+b\ge h$.

### Necessity and exact equality

For a full colouring with red subgraph $F$, set

$$
a_F=d_F(S)+\sum_{v\in T}(d(v)-d_F(v))-e(S,T).
$$

It equals $2e_F(S)+2e_{\bar F}(T)+e_F(S,U)+e_{\bar F}(T,U)$. A counted component containing no defect has odd $d_F(C)+e(C,T)$, hence sends at least one red edge to $S$ or blue edge to $T$. Different components pay distinct edges. Thus $q\le a_F+c_*$, where $c_*$ is the number of counted components containing a defect. Moreover $a_F-a\le |X_R\cap S|+|X_B\cap T|$ where $X_R,X_B$ are the actual sets of red and blue excess vertices. Therefore

$$
q-a\le |X_R\cap S|+|X_B\cap T|+c_*
\le |X_R|+|X_B|\le r+b.
$$

Taking the maximum proves necessity. If $r+b=h$, each inequality is tight for every maximizing cut: each defect belongs either to the red defects in $S$, the blue defects in $T$, or to a counted component, with at most one defect per such component. Each defect-free counted component pays exactly one red-to-$S$ or blue-to-$T$ boundary edge, and there are no other contributions to $a_F$. The actual colour budgets are attained.

### Sufficiency: two auxiliary vertices

The case $h=0$ follows from the factor theorem. Assume positive budgets first. Set $m=|A|$, $n=|B|$. Add vertex $y$ adjacent exactly to $A$, with bounds $g'(y)=m-r$, $f'(y)=m$; add vertex $z$ adjacent exactly to $B$, with bounds $g'(z)=0$, $f'(z)=b$. There is no $yz$ edge. On original vertices set

$$
g'(v)=g(v)+1_A(v),\qquad f'(v)=f(v)+1_A(v).
$$

All bounds are admissible. Both auxiliaries are non-tight. In a red factor of the augmented graph, the omission of a $y$ edge permits one red excess at its original endpoint; the inclusion of a $z$ edge permits one blue excess. Restricting to the original graph therefore has the claimed properties, with separate prescribed supports $A,B$.

It remains to verify every augmented factor cut. Write $s_A=|S\cap A|$, $t_A=|T\cap A|$, $u_A=|U\cap A|$ and analogously for $B$. Remove the auxiliaries from the cut to obtain original $S,T$. Let O denote the remaining vertex set of the augmented cut. The exact increment of the cut capacity $a'$ over $a$ is given by this table (row is location of $y$, column location of $z$):

| | S | T | O |
|---|---|---|---|
| S | $2s_A+u_A+b$ | $2s_A+u_A+2t_B+u_B$ | $2s_A+u_A+t_B$ |
| T | $r+b$ | $2t_B+u_B+r$ | $r+t_B$ |
| O | $s_A+b$ | $s_A+2t_B+u_B$ | $s_A+t_B$ |

Indeed each original vertex in $A\cap S$ adds one to the upper-bound sum, each original vertex in $B\cap T$ adds one to the degree-minus-lower-bound sum, and each auxiliary contributes its own term minus its cut edges. Original tightness is unchanged. A component containing an auxiliary in O is non-tight. Among the other components, parity changes only by the number of vertices in $A$ when $y$ is in S, or in $B$ when $z$ is in T. If $y$ is in T its parity effect cancels its shift in $f$; if it is in O, every remaining counted component avoids $A$. If $z$ is in O, every remaining counted component avoids $B$.

In the (T,S) cell parity is unchanged, $q'=q$, and $a'=a+r+b\ge q$. In each cell with a parity change, the number of counted components is bounded by $q_0(A)+u_A$, $q_0(B)+u_B$, or $q_0(A\cup B)+u_A+u_B$, according to the indicated changed sets. The table supplies at least the corresponding increment, and the cut-covering property pays $q_0$. In the remaining cells with an auxiliary in O and no parity change, at most $q_0(A)$ or $q_0(B)$ components count, and $a'\ge a$. Thus every cut satisfies the ordinary factor theorem.

If $r=0<b$, add only $z$ at $B$ with bounds $0,b$ and leave original bounds unchanged. For $z$ in S, capacity increments by $b$ with unchanged parity; in T it increments by $2t_B+u_B$ with possible parity change only on components meeting $B$; in O it increments by $t_B$, with counted components avoiding $B$. This proves the one-sided statement. For $b=0<r$, exchange colours and use $A$. The deficit $h$ is invariant under colour exchange and interchange of $S,T$: capacity is identical, and counted parity changes by $D|C|+e(C,S)+e(C,T)$, an even integer by the degree sum on $C$. This completes all cases. QED.

## 2. Consequences for a minimal frontier obstruction

Keep the established notation $w=w_k=D+1$, $L=s+t-k+1$, $W_k=\sum_{\ell=k}^{s+t}w_\ell$, $e(H)=W_k-1$, and initial plateau length $P$. Select a maximizing frontier pair with $u$ equal leading red stars of size $\alpha+1$ and $v$ equal leading blue stars of size $\beta+1$, with $P=u+v-1$. The earlier plateau identity and avoiding-colouring argument give $h\ge P$.

**Universal packing constraints on prescribed supports.** For any dominating set $A$ of the saturated graph, $H$ must contain $u$ vertex-disjoint stars of size $\alpha+1$ centred in $A$. Otherwise choose a defect colouring with at most $v-1$ blue excess vertices and all red excess vertices in $A$ (take a sufficiently large red budget). Blue cannot contain its leading multiplicity; red cannot pack its leading multiplicity inside $A$. Symmetrically every dominating set $B$ must support $v$ vertex-disjoint stars of size $\beta+1$ centred in $B$. These necessary constraints hold even when $h>P$.

**Critical defect case $h=P$.** For any independently chosen dominating sets $A,B$, take budgets $(u,v-1)$, then $(u-1,v)$. In the first colouring all $u$ red excess vertices must centre the $u$ leading red stars, since blue cannot occur; in the second all $v$ blue excess vertices must centre the leading blue stars. Every such leading star consists of exactly the incident edges of its colour at its centre, so the smaller stars must pack outside the union of these forced closed star neighbourhoods. The exact maximizing-cut equality in Section 1 also localizes the defects to distinct odd components or to the specified sides of the cut. This extends the previous isolated-core switch construction to arbitrary factor-obstruction cuts. It does not by itself prove the required tail-packing contradiction.

**Unit-drop two-layer gate.** Suppose the initial $P$ weights $D+1$ are followed by $Q>0$ weights $D$. Let $A$ now be any maximal independent set in $H[X]$, with $r=|A|$. It dominates $X$, so $r\ge h\ge P$. Deleting it removes $rD$ edges and advances the frontier by $r$ steps. All surviving degrees are at most $D-1$. If $P\le r<P+Q$, the successor has leading weight $D$ and plateau length $P+Q-r$. For $D=2$ this is impossible (a maximizing pair has one leading arm one and the other two, defeated by a monochromatic colouring of maximum degree one). For $D\ge3$, its two caps must be positive and sum to $D-1$, else the same monochromatic argument defeats it. The earlier plateau bound, which needs only the maximum-degree cap and frontier arrowing, then forces at least $D(P+Q-r)$ vertices of degree $D-1$ in $H-A$.

Write $Y=\{v:d_H(v)=D-1\}$. The actual count gives a new exact necessary condition for **every** such independent dominating set in this range:

$$
|\{x\in X\setminus A:|N_H(x)\cap A|=1\}|
+|\{y\in Y:N_H(y)\cap A=\varnothing\}|
\ge D(P+Q-r).
$$

The first layer of degree saturation is therefore coupled to the second layer of the graph, not merely to total edge count. This is a structural constraint, not yet an elimination of all unit-drop profiles.

## 3. Bounded checks and scope

The accompanying independent verifier uses exact full-colouring enumeration, independently enumerated original factor cuts, every dominating subset, and every ordered pair of dominating subsets for positive-deficit cases. It does not implement the two-auxiliary factor construction. Exact finite tests corroborate the proof but are not the unbounded argument. No claim that the unrestricted conjecture has been proved. Next obligation: use the independently localizable forced stars and the two-layer saturation constraint to exclude a unit-drop least-frontier obstruction or construct a genuine counterexample.
