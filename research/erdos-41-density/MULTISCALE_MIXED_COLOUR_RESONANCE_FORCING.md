# Erdős #41 — Multiscale three-colour resonance forcing, with exact sixth-defect supersaturation

**21 October 2026; GCL Track A / D.** This note proves a quantitative **finite** multiscale theorem for genuinely occupied integer windows, using both their populations and their actual locations. It identifies an exact *mixed old-old pair-sum* resonance missed by pairwise block tests, and proves a no-cancellation Hall-to-sixth-defect inequality for unions of any selected three-colour types. **It does not prove these local overload conditions must occur in every hypothetically c-persistent infinite B3 set. Erdős #41 remains OPEN.** No novelty assertion or independent mathematical certification is claimed.

## 1. Tripartite collisions are sixth-order resonances

Let $X,Y,Z$ be pairwise disjoint nonempty finite subsets of the integers. They are *colour classes*: their absolute positions and spacing are arbitrary. Put

$$
a=|X|,\qquad b=|Y|,\qquad c=|Z|,
\qquad
S_{XYZ}=\mathrm{diam}(X)+\mathrm{diam}(Y)+\mathrm{diam}(Z)+1.
$$

Define the tripartite representation function

$$
r_{XYZ}(s)=|\{(x,y,z)\in X\times Y\times Z:x+y+z=s\}|,
\qquad M_{XYZ}=abc.
$$

Every triple with one element of each colour has six orderings. Its entire *within-colour-type* contribution to the exact sixth defect is

$$
\boxed{
\mathfrak d_{XYZ}
=36\left(\sum_s r_{XYZ}(s)^2-abc\right)
\ge 36\left(\frac{(abc)^2}{S_{XYZ}}-abc\right)_+.
}
\tag{TRIPARTITE-RESONANCE-PRESSURE}
$$

Here the notation $u_+=\max(u,0)$ is used. Since $\mathfrak d_6(X\cup Y\cup Z)$ contains this nonnegative summand,

$$
\boxed{
\mathfrak d_6(X\cup Y\cup Z)\ge\mathfrak d_{XYZ}.
}
$$

**Proof.** Every distinct $(x,y,z)$ is a distinct unordered triple of the global set because the colours are disjoint. Its sum lies in an integer interval containing at most $S_{XYZ}$ points, regardless of the gaps between the original three blocks. As established in the exact sixth-defect ledger, the within-type collision contribution is 36 times the number of *ordered pairs of unequal coloured triples with equal sum*. That number is $\sum_s r(s)^2-abc$. Cauchy–Schwarz on the at most $S_{XYZ}$ available sum positions gives $\sum_s r(s)^2\ge(abc)^2/S_{XYZ}$. All other triple-type collisions are nonnegative, proving both inequalities. QED.

**Immediate forcing criterion:** if $abc>S_{XYZ}$, the global set is NOT B3 and its integer sixth defect is positive. More precisely, $abc$ is the number of genuinely different mixed-colour triples, not an entropy surrogate. No assumption of regular spacing, field-code factors, or separation of the block locations enters the result.

## 2. Exact mixed-pair-sum difference resonance

Assume additionally that $X\cup Y$ is B2 (in particular, B3). Then the $ab$ cross pair sums $x+y$ are all distinct. For every $d>0$ define

$$
K_{XY}(d)=|\{(q,q')\in(X+Y)^2:q-q'=d\}|,
\qquad
G_Z(d)=|\{(z,z')\in Z^2:z-z'=d\}|.
$$

**Theorem A (exact three-colour resonance identity).**

$$
\boxed{
\mathfrak d_{XYZ}
=72\sum_{d>0}K_{XY}(d)G_Z(d).
}
\tag{MIXED-PAIR-RESONANCE}
$$

The right side is invariant under **independent translations** of X, Y and Z: every $(x+y+z)$ changes by the same total translation, and both positive difference profiles are unchanged.

**Proof.** An equality between two different coloured triples is equivalent to $q+z=q'+z'$, where $q=x+y$ and $q'=x'+y'$ are **uniquely** represented cross pair sums. If $q=q'$ then $z=z'$, hence the coloured triples coincide. Otherwise exactly one ordering has $q-q'=d>0$ and $z'-z=d$. The number of *unordered* colliding pairs of coloured triples is therefore $\sum_{d>0}K_{XY}(d)G_Z(d)$. Each has two different unordered triples of weight six, giving sixth-defect contribution $2\cdot6^2=72$. QED.

The previous *individual-block* reciprocal correlations $H_XG_Z$, $H_YG_Z$ and $H_ZG_X$, $H_ZG_Y$ can all vanish while this **mixed-pair** resonance is strictly positive. Thus any forcing programme that examines only pairwise compatibility of original occupied containers is incomplete.

## 3. Minimal genuinely B3-compatible-pairs hostile example

Set

$$
X=\{2,18\},\qquad
Y=\{20,35\},\qquad
Z=\{43,44\}.
$$

Each of X, Y, Z and each *pairwise union* is genuinely repetition-permitted B3. All two-block reciprocal sixth-order resonance terms vanish, yet the full union is not B3:

$$
2+35+44=18+20+43=81.
$$

Here $K_{XY}(1)G_Z(1)>0$. The within-XYZ sixth defect is exactly $72$; the complete union has sixth defect $174$, owing to additional cross-colour-type collisions. This demonstrates an authentic three-block obstruction that cannot be inferred from any one of the three pairwise B3 checks.

The obstruction persists under independent whole-block translations, provided the resulting blocks remain disjoint: the equality of two triples containing exactly one element of each block survives every translation.

## 4. A family of three-colour types: location-aware sixth-order Hall pressure

Let $B_0,\dots,B_{h-1}$ be **pairwise disjoint** nonempty integer blocks, with

$$
B_i\subseteq[\ell_i,u_i]\cap\mathbb Z,\qquad m_i=|B_i|.
$$

For a triple of distinct colour indices $\alpha=\{i,j,k\}$, define its sum-support envelope

$$
I_\alpha=[\ell_i+\ell_j+\ell_k,\ u_i+u_j+u_k]\cap\mathbb Z
$$

and its number of unordered coloured triples $M_\alpha=m_im_jm_k$.

For an arbitrary nonempty collection $\mathcal F$ of such index triples, put

$$
M_{\mathcal F}=\sum_{\alpha\in\mathcal F}M_\alpha,\qquad
S_{\mathcal F}=\left|\bigcup_{\alpha\in\mathcal F}I_\alpha\right|.
$$

**Theorem B (multiscale aggregate Hall-to-defect forcing).** For ANY blocks, positions, sizes and collection $\mathcal F$,

$$
\boxed{
\mathfrak d_6\left(\bigcup_iB_i\right)
\ \ge\
36\left(\frac{M_{\mathcal F}^2}{S_{\mathcal F}}-M_{\mathcal F}\right)_+.
}
\tag{MULTISCALE-COLOUR-HALL-DEFECT}
$$

In particular, if $M_{\mathcal F}>S_{\mathcal F}$, **at least one forbidden three-sum collision is inevitable**; no change of arithmetic organization inside the occupied windows can avoid it. The proof needs no separate B3 assumption on any block.

**Proof.** Define $r_{\mathcal F}(s)$ to count all unordered triples of pairwise distinct colours with colour index set $\alpha\in\mathcal F$ and total sum s. These are distinct unordered triples, all of permutation weight six. They have total mass $M_{\mathcal F}$ and all their sums lie in the union of the envelopes, whose number of integer positions is $S_{\mathcal F}$. As in §1, the contribution of colliding pairs *within this chosen triple family* to the global defect is exactly $36(\sum_s r_{\mathcal F}(s)^2-M_{\mathcal F})$. Cauchy–Schwarz gives the inequality. Every other collision term in the full sixth-defect ledger is nonnegative. QED.

The theorem improves on separate interval-Hall tests in one precise way: **overlapping support envelopes from different three-colour types are charged jointly**, so individually feasible types may be jointly impossible. It also makes the required *positive excess* quantitative, rather than merely labelling a Hall failure.

If several families $\mathcal F_j$ are *pairwise disjoint in their sets of triple-colour types*, their corresponding within-family collision contributions are disjoint and the right sides can be summed without double counting. Overlapping families must NOT be added in this fashion.

## 5. Conditional forcing in many comparable occupied windows

Suppose $h\ge3$ disjoint nonempty B3 blocks occupy consecutive width-R windows inside an interval of total diameter at most $hR-1$, and each contains at least m elements. Take $\mathcal F$ to be **all** index triples with distinct colours. Then

$$
M_{\mathcal F}\ge\binom h3m^3,\qquad S_{\mathcal F}\le3hR.
$$

Consequently,

$$
\boxed{
\mathfrak d_6\left(\bigcup_iB_i\right)
\ge
36\left(
\frac{\binom h3^2m^6}{3hR}
-\binom h3m^3
\right)_+
}
\tag{REGULAR-WINDOW-OVERLOAD}
$$

**CAUTION:** the boxed quantitative bound as written requires a proof of monotonicity in M beyond the threshold. For $M\ge\binom h3m^3>3hR$, the function $f(M)=M^2/(3hR)-M$ is increasing, and then the inequality is valid. When the threshold is not passed, the RHS is declared zero and valid. Therefore the implication **whenever** $\binom h3m^3>3hR$ is unconditional.

With $m\ge cR^{1/3}$ this yields a genuine finite forcing criterion:

$$
\boxed{
\binom h3c^3>3h
\quad\Longrightarrow\quad
\text{such }h\text{ occupied windows cannot coexist in a B3 set}.
}
\tag{CONDITIONAL-REGULARITY-OBSTRUCTION}
$$

For every fixed c>0, this holds for sufficiently many comparable, individually populated adjacent windows (roughly $h>\sqrt{18}\,c^{-3/2}$).

**This does not prove Erdős #41:** the assumption that *every one of h adjacent width-R windows* holds $cR^{1/3}$ elements does NOT follow from the persistent cumulative bound $A(N)\ge cN^{1/3}$. Such a cumulative bound can be carried by uneven, migrating occupied windows. The aggregate Hall pressure also cannot be assumed to exceed its support capacity for the sparse geometric windows selected by earlier mandatory-window extraction.

Moreover, the regular-window forcing is comparable to the elementary global three-sum packing bound; it is **not** advertised as a breakthrough on the unresolved odd-order density valley. The genuine contribution here is the precise triple-colour defect decomposition and independently translatable mixed-pair resonance, plus a falsifiable, location-sensitive pressure criterion.

## 6. The exact next open mathematical bridge

For hypothetical positive lower critical density, choose actual occupied windows (possibly of different widths) by the proven annular extraction. Their populations are known from below, but their **sum-support envelopes need not collide tightly enough** to force $M_\mathcal F>S_\mathcal F$.

The decisive missing implication is a new *occupation-versus-sum-support concentration theorem*:

> Show that some collection of necessarily occupied, possibly irregular multiscale windows has $\sum_{\alpha\in\mathcal F}\prod_{i\in\alpha}|B_i|$ exceeding the size of the union of the three-colour sum-support envelopes, OR force a different exact six-variable correlation to be positive.

Neither statement has been proved for all hypothetical c-persistent B3 sets. A proof of this implication would essentially solve Erdős #41. Track A #2790 should focus on adaptive selection of the colour-type family $\mathcal F$ and its arithmetic support; Track B #2791 should test whether the support-deficit quantity transports under changing windows; independent audit is Track C #2792; coordination #2789. This is candidate author mathematics only.
