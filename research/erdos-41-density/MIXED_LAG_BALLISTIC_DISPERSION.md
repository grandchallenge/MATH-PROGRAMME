# Erdős #41 — forced two-sided mixed-lag dispersion and exact moments

**Status:** finite B3 theorem and rigorous consequence under a *hypothetical* persistent positive lower density. These results do not imply the requested cross-scale matching overload. The original conjecture remains open.

## 1. Scope and representation conventions

A B3 set A has unique unordered three-term sums, repetitions permitted. For disjoint nonempty X,Y subsets of a common B3 set, write x=|X|, y=|Y| and m=x+y. For any unordered positive pair {a,b} and center c consider d=a+b-2c. Give the representation *support weight* 2 when a≠b, and 1 when a=b. Equivalently, weighted sums over unordered pairs equal unweighted sums over all **ordered** triples (a,b,c).

Let w_mix(d) be the support weight of the representations involving both colors. Define its first and second moments in the usual integer variable d.

## 2. Exact mixed-lag first and second moments

Let $\mu_X,\mu_Y$ be block means, and let $v_X,v_Y$ be **population** variances. Put $\Delta=\mu_Y-\mu_X$.

**Theorem 1.** For every finite disjoint X,Y in a common B3 set,

$$
\boxed{\sum_dw_{\mathrm{mix}}(d)=3xym,\qquad
\sum_dd\,w_{\mathrm{mix}}(d)=0,}\tag{M0}
$$

$$
\boxed{\sum_dd^2w_{\mathrm{mix}}(d)
=6xy\Big[(2x+y)v_X+(x+2y)v_Y+m\Delta^2\Big].}\tag{M2}
$$

Consequently, the root-mean-square lag under the weighted mixed distribution satisfies

$$
\boxed{\frac{\sum_dd^2w_{\mathrm{mix}}(d)}{\sum_dw_{\mathrm{mix}}(d)}
=2\Big[\frac{2x+y}{m}v_X+\frac{x+2y}{m}v_Y+\Delta^2\Big]
\ge2\Delta^2.}\tag{RMS}
$$

**Proof.** For any finite block Z of size s, let its ordered triples (a,b,c) range freely over Z³. The signed quantity d=a+b−2c has total first moment zero by symmetry and coefficient sum 1+1−2=0. Treating a,b,c as independent uniform choices in Z, its second moment equals $6s^3v_Z$ because Var(a+b−2c)=(1+1+4)v_Z=6v_Z. The mixed representation sums are obtained by subtracting the all-X and all-Y totals from the full (X∪Y) total. Thus

$$
\sum_{\mathrm{mixed}}d^2=6[m^3v_{X\cup Y}-x^3v_X-y^3v_Y].
$$

The population variance of the union obeys

$$
v_{X\cup Y}=\frac{xv_X+yv_Y}{m}+\frac{xy}{m^2}\Delta^2.
$$

Substitution and expansion yield (M2). The weighted total is $m^3-x^3-y^3=3xym$. Dividing gives (RMS). These identities are pure arithmetic and hold even without B3; B3 matters for the matching conclusions below and for excluding nontrivial zero lags.

## 3. Two-sided ballistic tail-support theorem

**Theorem 2.** Assume additionally that every element of X is smaller than every element of Y. Let

$$
g=\min Y-\max X>0.
$$

Define the negative and positive *extreme-type* mixed-lag sets

$$
S_-=\{a+b-2c:a,b\in X,\ c\in Y\},\quad
S_+=\{a+b-2c:a,b\in Y,\ c\in X\}.
$$

Then

$$
\boxed{S_-\subseteq(-\infty,-2g],\quad S_+\subseteq[2g,\infty),}
$$

and

$$
\boxed{|S_-|\ge xy,\qquad|S_+|\ge xy.}\tag{TAIL}
$$

**Proof.** The signs and distance from zero follow from a,b≤max X and c≥min Y in S_-, and symmetrically in S_+. The weighted numbers of extreme-type representations are x²y and y²x, because the positive pairs are ordered by their weights, and there are x² (respectively y²) possibilities for positive entries for each center.

Fix a nonzero lag d. By the B3 centered-fiber matching theorem, distinct representations at d have positive pairs with pairwise disjoint supports. For extreme type XX|Y, those supports lie in X, so their total positive-pair support weight is at most x, *not* the full x+y. Hence there must be at least (x²y)/x=xy different negative extreme-type lags. Analogously, YY|X requires at least (y²x)/y=xy different positive lags. The two sets are disjoint by opposite signs. No probabilistic or smoothness assumption enters.

This is substantially stronger than simply knowing the complete mixed support has size ≥3xy: it identifies two separated intervals that individually must contain at least xy distinct mixed lags. In fact, the negative extreme type contributes precisely $x^2y$ weighted representations and the positive extreme type precisely $xy^2$. Hence **at least one third** of the total mixed weighted mass $3xym$ occurs at lags of absolute value at least $2g$:

$$
\boxed{\sum_{|d|\ge2g}w_{\mathrm{mix}}(d)\ge xym=\frac13\sum_dw_{\mathrm{mix}}(d).}\tag{TAIL-MASS}
$$

This is a *mass* constraint, independent of the second-moment argument. It rules out concentrating more than two thirds of the mixed mass into the open central interval $(-2g,2g)$.


## 4. Consequence of persistent positive lower B3 density

Suppose an infinite B3 A obeys

$$
A(t)\ge c\,t^{1/3}\quad\text{for every sufficiently large }t,\qquad 0<c\le1.
$$

Let $R=(6/c)^3$, $X=A\cap[1,N/R^2]$, and $Y=A\cap(N/R,N]$. The previous [density-forced audit](DENSITY_FORCED_MIXED_BUDGET.md) proves, for all sufficiently large N,

$$
x\ge\frac{c^3}{36}N^{1/3},\qquad
y\ge\frac c2N^{1/3},\qquad
g\ge\left(\frac1R-\frac1{R^2}\right)N.
$$

Therefore (TAIL) gives the following **density-sensitive, two-sided arithmetic restriction**:

$$
\boxed{
\left|S_{\mathrm{mix}}\cap\left(-\infty,-2\Big(\frac1R-\frac1{R^2}\Big)N\right]\right|
\ge\frac{c^4}{72}N^{2/3},}\tag{NEG}
$$

$$
\boxed{
\left|S_{\mathrm{mix}}\cap\left[2\Big(\frac1R-\frac1{R^2}\Big)N,\infty\right)\right|
\ge\frac{c^4}{72}N^{2/3}.}\tag{POS}
$$

In addition, because $\Delta=\mu_Y-\mu_X\ge g$, the exact mixed second moment forces a weighted root-mean-square lag at least $\sqrt2\,g$, a *macroscopic* fraction of N depending only on c.

**Interpretation:** persistent lower density does not merely force many mixed representations. It forces at least order N^(2/3) **distinct** lag values in *each* of two widely separated sign regions, and a nontrivial macroscopic mixed second moment. Therefore **no proposed localization theorem concentrating all mixed lags into a sublinear-width neighborhood of the origin can be valid under the positive-density hypothesis.** This does not refute a theorem asserting few discrete occupied locations inside large intervals: radius localization and *cardinality* localization are different obligations.

## 5. Why this does not prove Erdős #41

The entire global centered-lag interval of A∩[1,N] has length O(N), whereas (NEG)/(POS) require only Ω_c(N^(2/3)) occupied lag locations in each tail. Even though these regions are far from zero, each can still contain O(N) available integers. The extreme-type support estimates therefore do not force more than the available matching budget.

The genuine 29-element B3 fixture from the prior tests illustrates this distinction: its mixed representations spread over thousands of lags, with each individual lag far below the permitted matching cap. This is a finite benchmark, not a claimed infinite counterexample.

The paper by C. Táfula, *Infinite Sidon-type sets for zero-sum linear forms* (Monatsh. Math. 211 (2026), 315–327, DOI 10.1007/s00605-026-02211-4), explicitly identifies the odd-order B_h density problem as open and obtains zero-sum density statements under additional consecutive-gap hypotheses. The representation conventions differ: its variables are ordered and pairwise distinct, whereas the current calculation includes diagonals and B3 uniqueness with repetition. Those hypotheses and counts must not be transferred without conversion.

**Bounded conclusion:** Theorem 1 gives exact weighted mixed first and second moments. Theorem 2 plus persistent density gives two separated sets of at least c^4 N^(2/3)/72 lag positions each. This **rules out small-radius localization** as a shortcut, but does not give the requested *upper* support of o(N^(2/3)) or eventual weighted matching overload. Obtaining one of those would be a genuine resolution of Erdős #41; no such proof is claimed. The next nontrivial input must constrain **overlap between different scales inside the widely separated lag regions**, beyond these moment and capacity identities.
