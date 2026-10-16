# Erdős #41 — residue-resolved avoidance and multiplicative density cost

**Stage B research note, 2026-10-16. Status: finite theorems PROVED; density-forced collision and Erdős #41 remain OPEN.** This is a successor to the complete-pair dilation programme in PR #2696 and popular-distance/residue-LP work in PR #2713. It does not depend on either PR being merged. It is not a MATHCERT claim.

## 1. The exact arithmetic question

Let U,W be disjoint finite subsets of a repetition-permitted B3 set A, with U<W. Let P be the **complete** set of unordered positive pair sums from U, including repetitions. For integer h set

$$
r_U(h)=\#\{(p,p')\in P^2:p-p'=2h\},
\qquad r_U(-h)=r_U(h).
$$

The true, nonduplicated cross-correlation is

$$
\mathcal M(U,W)=\sum_{\{x,y\}\subset W}r_U(y-x)
=\frac12\sum_{\substack{x,y\in W\\x\ne y}}r_U(y-x).
$$

The first sum orders each two-element subset so y>x. B3 implies B2, hence **every nonzero ordered difference in W occurs just once**. This distinct-difference property is the indispensable extra input for the next theorem: it is false for arbitrary independent subsets of the forbidden-distance graph. We do **not** claim an independence bound for all graph-independent sets.

Fix a candidate interval I of integer span L>=1 containing W, and a modulus Q>=1. For each residue s modulo Q let b_s=# {w in W:w=s mod Q}. For each residue d put

$$
K_d=\sum_{s\bmod Q}b_s b_{s+d}-|W|\mathbf1_{d=0}.
$$

These are the numbers of **ordered distinct** pairs (x,y) in W with y-x=d modulo Q. Their sum is exactly |W|(|W|-1), with no representation or shell-cut duplication.

For d modulo Q, form the finite list of weights

$$
\Omega_d(U;L,Q)=
\left\{r_U(h):
0<|h|\le L,\quad h\equiv d\pmod Q\right\}
$$

with **one entry for each eligible signed integer h**. Sort its entries nondecreasingly as $\omega_{d,1}\le\dots\le\omega_{d,N_d}$. Define $F_d(k)=\sum_{j=1}^k\omega_{d,j}$, with F_d(0)=0. Only k<=N_d is allowed.

## 2. Theorem A: weighted residue-order-statistic inverse

For any such actual B3 outer set W,

$$
\boxed{
2\mathcal M(U,W)\ge\sum_{d\bmod Q}F_d(K_d).
}\tag{WEIGHTED-INVERSE}
$$

**Proof.** Fix a residue class d. The K_d ordered nonzero differences realized by W are **different integers**, each in the candidate range (-L,L) and congruent to d modulo Q. The total r_U weight of those K_d differences cannot be smaller than the sum of the K_d smallest weights available in that residue class. Sum over d. The left sum counts each undirected outer pair twice. QED.

This theorem uses the **actual** complete U pair-sum spectrum and the **actual** residue profile of W; it does not infer spectral mixing, independence, or uniformity from cardinality.

For an integer threshold t>=1 define the number of low-weight eligible differences in class d:

$$
Z_{d,t}=\#\{0<|h|\le L:
h\equiv d\pmod Q,\ r_U(h)<t\}.
$$

A direct consequence, useful for exact integer-programming certificates, is

$$
\boxed{
2\mathcal M(U,W)
\ge t\sum_{d\bmod Q}(K_d-Z_{d,t})_+.
}\tag{THRESHOLD-INVERSE}
$$

In particular if W is graph-independent at threshold t, so every realized nonzero difference has r_U(h)<t, the **quadratic residue profile restrictions** are

$$
\boxed{
\sum_s b_s b_{s+d}-m\mathbf1_{d=0}
\le Z_{d,t},\quad m=|W|,\quad \text{for every }d\bmod Q.
}\tag{AVOID-Q}
$$

For t=1, zero correlation forces these inequalities. The class capacities N_d always bound K_d automatically, but the smaller **allowed** capacities Z_d depend on the genuine forbidden spectrum. Under arbitrary positive M, the weighted lower bound measures precisely the unavoidable cost of exceeding them.

These are necessary finite conditions, not sufficient to realize a B3 outer set. They can be imposed alongside the already proved linear residue capacity constraints for P+W and P+2W. Unlike those linear constraints, the new inequalities use outer **B2 difference uniqueness** and are quadratic in the outer residue occupancies.

## 2A. Explicit finite bound on B2-independent outer carriers

For an interval I of L+1 integers and modulus Q, let I_s count candidate outer positions in residue s. For each integer threshold t>=1, define the feasible nonnegative integer vectors b=(b_s) by

$
0\le b_s\le I_s,\quad m=\sum_s b_s,\quad
\sum_s b_s b_{s+d}-m\mathbf1_{d=0}\le Z_{d,t}
\quad(d\bmod Q).
$

Let OPT_(Q,t)(U,I) be the maximum m among these vectors. **Corollary (genuine B2-independent capacity):** if W is a B2 subset of I with r_U(y-x)<t at all distinct center pairs, then

$
\boxed{|W|\le \mathrm{OPT}_{Q,t}(U,I).}\tag{B2-ALPHA}
$

This is a finite integer-*quadratic* optimization, not a general forbidden-graph independence theorem. Actual B3 outer W qualify since B3 implies B2. For Q=1 it reduces to the explicit formula

$
\boxed{
m(m-1)\le Z_{0,t},\qquad
m\le\left\lfloor\frac{1+\sqrt{1+4Z_{0,t}}}{2}\right\rfloor .
}\tag{ONE-CLASS}
$

For example, U={1,2,5}, I=[20,28], and t=1: r_U(h)>0 precisely for h=1,2,3,4, while h=5,6,7,8 are allowed. Thus Z_(0,1)=8 signed allowed differences. Every *B2*-independent W in I has m(m-1)<=8 and hence m<=3. The ordinary doubled-sum injectivity bound only gives m<=4. The original **B3 mixed-triple** packing already gives m<=2 in this tiny example; therefore the new corollary does not improve the known B3 extremal bound there. Its purpose is to retain residue-by-residue arithmetic exclusions for actual W.

The integer programme can be combined with the existing **linear** residue sum-capacity system for P+W and P+2W, and the per-residue cubic-shadow B3 size restrictions. A finite infeasibility receipt rules out that finite candidate, not the infinite conjecture. Coarse Q=1 alone cannot prove a critical-density deficit because the number of allowed differences is typically order L while m^2 is only order L^(2/3).

## 3A. Sharpening: localized *oriented* cross-bin inverse

The signed full-outer-set theorem uses every candidate difference with absolute value at most the total outer diameter. The actual Stage B construction uses much shorter positive-difference windows from two separated fine outer bins.

Let Y,Z be two nonempty, disjoint B3 subsets of the actual outer carrier with every y in Y below every z in Z. Let

$$
J=[\min Z-\max Y,\ \max Z-\min Y]\cap\mathbb Z,
\qquad |J|=\mathrm{diam}(Y)+\mathrm{diam}(Z)+1.
$$

Let $b_s=\#\{y\in Y:y\equiv s\pmod Q\}$ and $c_s=\#\{z\in Z:z\equiv s\pmod Q\}$. For each d modulo Q define

$$
K^{Y,Z}_d=\sum_{s\bmod Q}b_s c_{s+d}.
$$

Then sum_d K^{Y,Z}_d=|Y||Z|. The B2 property makes all positive cross-bin differences z-y distinct, so each K_d picks out K_d **distinct** integers h in J with h=d modulo Q.

Sort the actual weights r_U(h) over all h in J with h=d modulo Q as $v_{d,1}\le v_{d,2}\le\dots$. Define $G_d(k)=\sum_{j=1}^k v_{d,j}$ and $Z^{Y,Z}_{d,t}=\#\{h\in J:h\equiv d\pmod Q,\ r_U(h)<t\}$.

**Theorem B (oriented localized weighted inverse):**

$$
\boxed{
\begin{aligned}
\mathcal M_{Y,Z}(U)
&:=\sum_{y\in Y}\sum_{z\in Z}r_U(z-y)\\
&\ge\sum_{d\bmod Q}G_d(K^{Y,Z}_d)\\
&\ge t\sum_{d\bmod Q}(K^{Y,Z}_d-Z^{Y,Z}_{d,t})_+ .
\end{aligned}
}\tag{LOCAL-INVERSE}
$$

**Proof.** Every ordered center pair (y,z) has z-y>0 and determines a unique positive difference because the actual B3 carrier is Sidon. For each residue class d, its K_d differences are K_d *distinct* members of J. Their total weight is at least the sum of the K_d smallest possible weights there. At most Z_{d,t} of them can have weight below t, giving the threshold bound. Sum over d. No pair is charged at more than one bin pair or scale when the center-bin partition has a unique owner. QED.

**Zero-correlation inverse.** If M_{Y,Z}(U)=0, then for every residue class d,

$$
\boxed{\sum_s b_s c_{s+d}\le Z^{Y,Z}_{d,1}.}\tag{LOCAL-AVOID}
$$

The candidate difference range has only diam(Y)+diam(Z)+1 slots, **not** the full outer-center span. Accordingly this version can provide a stronger finite exclusion than the global theorem when the two outer bins are narrow and separated.

For Q>|J|-1 each residue occurs at most once in J; the order-statistic bound becomes an exact equality for the given Y,Z. For smaller Q it is a computable, potentially nontrivial *coarsened* arithmetic certificate. This equality at large Q is a verification feature, not an asymptotic density advance.

**Falsifiable Stage B target:** choose bin pairs by a predeclared density-window partition, compute (LOCAL-AVOID) at a bounded collection of moduli, and attempt to show that every outer B3 pair profile with |Y|,|Z| on the hypothesized critical scale violates at least one constraint. If the inequalities remain feasible across long windows, seek an independent arithmetic inverse theorem that forces a CRT deficit as described below. Neither universal finite-window exclusion nor its multiscale consequence has been proved.

## 3. A quantitative inverse structural theorem on multiple coprime moduli

An exact *density cost* arises independently from the B3 cubic-shadow inequality. Let X be any finite B3 set with n>=2 and diameter D>0. For each integer modulus q with 1<=q<=D, let t_q(X) be the number of occupied residue classes. The established modular dispersion inequality is

$$
\boxed{\frac{n}{D^{1/3}}
\le12^{1/3}\frac{t_q(X)}{q^{1/3}}.}\tag{SINGLE-MODULUS}
$$

**Proof of the single-modulus bound (included to avoid an unmerged dependency).** Let t=t_q(X). Some occupied residue class has s>=n/t points. If s=1 then t=n and the claimed estimate follows from q<=D. If s>=2, subtract its residue and divide its elements by q. The resulting s-element set is still B3, of diameter at most D/q. Its exact cubic shadow has size (s^3-s^2+2s)/2 and lies in at most 3D/q+1 integers. Hence s^3-s^2+2s<=6D/q+2. Since s^3-s^2+2s-2>=s^3/2 for all integers s>=2, we obtain q s^3<=12D. Finally s>=n/t gives q n^3<=12D t^3. This establishes (SINGLE-MODULUS) without assumptions about graph independence.

Let q_1,...,q_s be **pairwise coprime** positive moduli whose product Q=prod_j q_j satisfies Q<=D. Write t_j=t_{q_j}(X). By the Chinese remainder theorem, the number t_Q(X) of occupied classes modulo Q is at most prod_j t_j. Apply (SINGLE-MODULUS) at Q:

$$
\boxed{
\frac{n}{D^{1/3}}
\le12^{1/3}\prod_{j=1}^s\frac{t_j}{q_j^{1/3}}.
}\tag{CRT-DENSITY-COST}
$$

This is a **proved multiplicative inverse-density law**. It is equally valid for an actual outer B3 subset W, independently of its forbidden-graph independence. If for a sequence of candidate B3 outer blocks X_N there are sets of pairwise coprime moduli q_{N,j} with product <=diam(X_N) and

$$
\prod_j\frac{t_{q_{N,j}}(X_N)}{q_{N,j}^{1/3}}\longrightarrow0,
$$

then |X_N|/diam(X_N)^(1/3) -> 0. In particular, if each of s(N)->infinity moduli has t_j<=q_j^(1/3)(1-epsilon) for a fixed epsilon>0, and their product stays within the diameter, critical lower density is impossible along those windows.

**Scope limitation:** deficits on different moduli must be realized by the **same actual block X_N** at a given scale; multiplying certificates from unrelated blocks or overlapping scale cuts is invalid. A structural theorem showing that large graph-independent B3 outer sets *necessarily* have this accumulated modular deficit has **not** been proved. For some q_j, t_j/q_j^(1/3)>1 and can offset deficits at others. Do not infer a density drop from an unspecified collection of residue patterns.

This criterion strengthens the usable *form* of the earlier single-modulus cost: one need not exhibit an extreme t_q=o(q^(1/3)) at a single modest modulus, provided an accumulated joint CRT deficit exists. For Q=prod q_j it is still a consequence of the original cubic-shadow packing inequality, not a new general B3 density theorem.

## 4. Independent-set and adversarial boundaries

The graph with edges at h where r_U(h)>=t can have independent vertex sets that are **not B2**; then many different ordered vertex pairs can reuse the same allowed integer difference, invalidating both (WEIGHTED-INVERSE) and (AVOID-Q). Apply them to actual outer B3 sets, or other sets whose nonzero ordered differences are independently certified distinct. The full graph independence number alpha_t is **not** bounded by these inequalities without that extra hypothesis.

The popular forbidden-distance theorem provides many large r_U weights inside short magnitude ranges, but the known actual outer difference reservoir has only O(N^(2/3)) members inside an order-N interval. It is sparse in relative terms. Neither the global popular-distance density nor (AVOID-Q) alone gives a collision for a positive critical density coefficient.

For short finite intervals and Q, (AVOID-Q) is an exact **falsification certificate**: if no nonnegative integer vector b satisfying candidate residue capacities, outer B3 per-class bounds, (AVOID-Q), and the original triple-sum capacities can reach the density-required |W|, then the proposed persistent-density finite configuration is impossible. This is a bounded finite consequence, **not** proof that all sufficiently large windows fail.

An honest next inverse theorem must show that sustained avoidance across nested, uniquely owned density windows forces a **quantified accumulation of CRT residue deficits** or some other rigorously costed gap structure. At present this implication is OPEN. Test it against complete Sidon-digit lifts (where large residue class counts can defeat the CRT deficit), sparse infinite base-16 B3 examples, genuine finite B3 prefixes, and non-B3 repeated-difference hostile controls.

## 5. Acceptance and provenance

- Written exact proofs of the weighted order-statistic bound, thresholded residue capacity, and CRT multiplicative density cost above.
- Replay exact profiles of real finite B3 fixtures with integer weights, including M=0 and M>0. Verify all moduli and thresholds, and compare the result to the actual sum over W pairs.
- Verify that a non-B2 independent outer control is explicitly rejected, rather than silently granted a false bound.
- Keep substantive Erdős #41, large-scale alpha_t improvement, and the general avoidance-to-density implication OPEN.
- GCL research docket: issue #2622. Related unmerged research PRs #2696 and #2713; no dependency on their protected admission.

No mathematical certification, external priority, or resolution is asserted.
