# EXT-015C / Fixed Fréchet source — countable-directed obstruction theorem 018

**Disposition:** PROVED a new conditional-on-source-presentation *localization theorem* in the actual real-liquid category, with its set-theoretic hypotheses and remaining categorical obstruction explicitly separated. **The required surjectivity or non-surjectivity of the original Ext¹ target-stage comparison remains OPEN.** Nothing in this note is a second human approval or a numerical proof.

**Guiding question:** Can an extension carry genuinely global analytic information that no compact-support stage can capture?

**Protected predecessors:** [agent mathematical review 016](AGENT_CRITICAL_REVIEW_AB_016.md), [scalar phantom decomposition 017](SCALAR_PHANTOM_ESCAPE_017.md), [EXT-015 specification](SPEC.md), and [LFO-013](../LFO3_SURJECTIVITY_THEOREM_013.md).

## 1. Exact fixed source and the mathematical provenance

Take the actual primary source $H=\underline{\mathcal D_{[-1,1]}(\mathbb R)}$ in $\mathcal A_p=\mathrm{Liq}_p(\mathbb R)$, $0<p\le1$. By the Valdivia–Vogt representation of compact-support test functions on a compact set with nonempty interior, the Fréchet space $\mathcal D_{[-1,1]}(\mathbb R)$ is isomorphic to the rapidly decreasing sequence Fréchet space $s$. Its liquid realization is therefore isomorphic to $\underline s$. The original source for this representation is M. Valdivia, *A representation of the space D(K)*, J. reine angew. Math. **320** (1980), 97–98; see also the explicit statement in [the sequence-space discussion](https://mathoverflow.net/questions/321160/extension-of-valdivia-vogt-isomorphism-from-mathscrdk-to-mathscrek).

For a positive rapidly decreasing weight $r=(r_n)_{n\ge1}$, let

$$
T_r=r\cdot\mathcal M_{<p}(\mathbb N)
\hookrightarrow\underline s.
\tag{18.1}
$$

The weight order $r\preceq r'$ means $r_n\le C r'_n$ for some constant $C$ and all $n$. The poset $\mathscr R$ of equivalence classes of such weights is **countably directed**: every countable family has an upper bound. The measure-stage presentation

$$
\underline s\cong\varinjlim_{r\in\mathscr R} T_r
\tag{18.2}
$$

and the description of scalar morphisms as weighted spaces of type $c_0$ are worked out in Grisha Taroyan's [August 2026 construction](https://mathoverflow.net/questions/510488/operatornameext1s-mathbb-r-in-the-category-of-liquid-vector-spaces/514158). For the present use, (18.2) can also be checked on every profinite plot: the image is compact in $s$, so the supremum of the absolute value of its coordinates indexed by $n$ decreases faster than any polynomial; choosing a positive rapid weight larger than the square root of this supremum bounds the image in one measure stage and gives continuous factorization. The countable-direction property follows by diagonal domination of countably many rapid weights. Neither assertion requires the Continuum Hypothesis.

A source precision: the free liquid measure objects $\mathcal M_{<p}(S)$ are **projective when $S$ is extremally disconnected** (Scholze, *Lectures on Analytic Geometry*, Theorem 6.5). The one-point compactification $\mathbb N\cup\{\infty\}$ is not extremally disconnected. **Do not assert its free measure object is projective.** What is needed below is only abelian-category compactness, not projectivity.

## 2. A ZFC inverse-limit lemma

**Lemma 18.1 (countably directed finite-coordinate support).** Let $I$ be a nonempty countably directed partially ordered set. For each $n\ge1$, let $W_n$ be a vector space, and let $(V_{i,n})_{i\in I}$ be a reverse system of linear subspaces of $W_n$ such that $V_{j,n}\subseteq V_{i,n}$ whenever $i\le j$. Put

$$
V_i=\bigoplus_{n\ge1}V_{i,n},
\qquad
W=\bigoplus_{n\ge1}W_n.
$$

Then for inverse systems of ordinary vector spaces

$$
\varprojlim_i{}^{1} V_i
\cong
\bigoplus_{n\ge1}\varprojlim_i{}^{1} V_{i,n}.
\tag{18.3}
$$

The assertion holds in ZFC for arbitrary such nested systems; it is **not** an assertion that first-derived inverse limits commute with arbitrary sums over arbitrary index categories.

**Proof.** For every $i$ there is an exact sequence

$$
0\longrightarrow V_i\longrightarrow W
\longrightarrow
\bigoplus_n(W_n/V_{i,n})\longrightarrow0.
\tag{18.4}
$$

The middle inverse system is constant, hence its positive derived inverse limits vanish on a nonempty directed index category (its category nerve is contractible). Its long exact derived-limit sequence yields

$$
\varprojlim\nolimits_i^{1}V_i
\cong
\mathrm{coker}
\left[
W\longrightarrow
\varprojlim_i\bigoplus_n(W_n/V_{i,n})
\right].
\tag{18.5}
$$

The key countably directed observation is

$$
\varprojlim_i\bigoplus_n X_{i,n}
\cong
\bigoplus_n\varprojlim_i X_{i,n}
\tag{18.6}
$$

for **any** family of inverse systems with coordinatewise transition maps indexed by such $I$. Indeed, if a compatible family had infinitely many nonzero coordinate families, choose one index $i_n$ where each of those coordinates is nonzero. A common upper bound $j$ of the countably many $i_n$ would force the representative at $j$ to have infinitely many nonzero coordinates, contradicting its membership in the direct sum. Conversely any finite family of compatible coordinate systems defines a compatible direct-sum family. Applying (18.6) to the quotients in (18.5), and the same derived-limit exact sequence for each $n$, gives (18.3). $\square$

**Fatal scope warning.** Ordinary countable inverse towers are not countably directed in this sense: a countable unbounded set of natural-number stages has no upper bound. The uncountable, countably directed weight poset is the crucial hypothesis, not a decorative feature.

## 3. Apply the lemma to the exact liquid scalar-sum target

Retain the actual scalar summand of test-function output from [017](SCALAR_PHANTOM_ESCAPE_017.md):

$$
\mathsf S=\bigoplus_{n\ge1}\underline{\mathbb R},
\qquad
\mathsf P=\prod_{n\ge1}\underline{\mathbb R},
\qquad
\mathsf Q=\mathsf P/\mathsf S.
\tag{18.7}
$$

**Compactness of the weight stages.** Let $S_\infty=\mathbb N\cup\{\infty\}$ with its convergent-sequence profinite topology. The standard split exact sequence

$$
0\longrightarrow
\mathcal M_{<p}(\mathbb N)
\longrightarrow
\mathcal M_{<p}(S_\infty)
\longrightarrow
\mathcal M_{<p}(*)\longrightarrow0
\tag{18.8}
$$

has a section induced by the point $\infty$, so $\mathcal M_{<p}(\mathbb N)$ is a direct summand of $\mathcal M_{<p}(S_\infty)$. The latter is a **compact object** in the liquid abelian category: its Hom functor represents evaluation on the profinite $S_\infty$, and filtered colimits of liquid modules are computed sectionwise. Hence each abstractly isomorphic scaled object $T_r$ is compact. This is **not** a proof that $T_r$ is projective.

Consequently, for each $r$ the canonical comparison is an isomorphism

$$
\mathrm{Hom}_{\mathcal A_p}(T_r,\mathsf S)
\cong
\bigoplus_n\mathrm{Hom}_{\mathcal A_p}
(T_r,\underline{\mathbb R}).
\tag{18.9}
$$

The scalar groups on the right can be identified with nested linear subspaces of the same sequence space $W_0=\mathbb R^{\mathbb N}$:

$$
V_r=
\left\{a\in\mathbb R^{\mathbb N}:
r_n a_n\longrightarrow0\right\}
\subseteq W_0,
\qquad
r\preceq r'\implies V_{r'}\subseteq V_r.
\tag{18.10}
$$

This is the weighted $c_0$ dual description from the cited measure-stage representation. Equations (18.3), (18.9) and (18.10) therefore prove

$$
\varprojlim\nolimits_r^{1}
\mathrm{Hom}_{\mathcal A_p}(T_r,\mathsf S)
\cong
\bigoplus_n
\varprojlim\nolimits_r^{1}
\mathrm{Hom}_{\mathcal A_p}(T_r,\underline{\mathbb R}).
\tag{18.11}
$$

**Theorem 18.2 (stagewise-split scalar extensions cannot escape).** Suppose a genuine liquid class

$$
\xi\in\mathrm{Ext}^1_{\mathcal A_p}(\underline s,\mathsf S)
$$

pulls back to **zero** in $\mathrm{Ext}^1_{\mathcal A_p}(T_r,\mathsf S)$ for every weight $r$. Then $\xi$ comes from a finite scalar prefix $\mathsf S_{\le b}$.

**Proof.** The derived mapping property of a filtered colimit (18.2) gives

$$
R\mathrm{Hom}(\underline s,\mathsf S)
\simeq
R\varprojlim_r R\mathrm{Hom}(T_r,\mathsf S).
\tag{18.12}
$$

The low-degree edge of its hyper-derived-limit spectral sequence is the exact sequence

$$
0\longrightarrow
\varprojlim\nolimits_r^{1}\mathrm{Hom}(T_r,\mathsf S)
\longrightarrow
\mathrm{Ext}^1(\underline s,\mathsf S)
\longrightarrow
\varprojlim_r\mathrm{Ext}^1(T_r,\mathsf S).
\tag{18.13}
$$

No vanishing of $\mathrm{Ext}^1(T_r,\mathsf S)$ is assumed here. The hypothesis says precisely that $\xi$ lies in the image of the first arrow of (18.13). By (18.11), its preimage uses only finitely many scalar coordinates. Naturality of the edge homomorphism with respect to the finite-summand target inclusions proves that $\xi$ comes from the corresponding finite scalar prefix. $\square$

**Corollary 18.3 (where an actual negative witness must live).** If $\xi\in\mathrm{Ext}^1(\underline s,\mathsf S)$ escapes every finite prefix, then there exists at least one $r$ for which

$$
\xi|_{T_r}\ne0
\quad\text{in}\quad
\mathrm{Ext}^1_{\mathcal A_p}(T_r,\mathsf S).
\tag{18.14}
$$

Thus a transfinite derived-limit obstruction built **only** from stagewise splittings, however nonzero, cannot produce the sought scalar support escape.

**Corollary 18.4 (phantom-map localization).** If every morphism $f:T_r\to\mathsf Q$ lifts to $\mathsf P$ at every weight stage $T_r$, then every morphism $\underline s\to\mathsf Q$ also lifts to $\mathsf P$. In fact, for a global morphism $f$ let $\delta(f)\in\mathrm{Ext}^1(\underline s,\mathsf S)$ be its boundary. Every stage restriction of this boundary is zero by the assumption, so Theorem 18.2 makes $\delta(f)$ finite-prefix. But $\delta(f)$ maps to zero in $\mathrm{Ext}^1(\underline s,\mathsf P)$ by exactness, whereas finite-prefix Ext¹ embeds into product-target Ext¹ by coordinate retractions. Thus $\delta(f)=0$, and exactness gives a global lift. $\square$

This is an **agent-proved conditional lifting theorem**, with a named checkable local criterion, not a claim that the local criterion has already been proved.

### Single-space local lifting gate

Let $S_\infty=\mathbb N\cup\{\infty\}$ as in (18.8). A sufficient condition for the global phantom channel to vanish is the **specific** surjectivity

$$
\mathsf P(S_\infty)\longrightarrow\mathsf Q(S_\infty).
\tag{18.15}
$$

If every section of $\mathsf Q$ on this one profinite test space lifts to $\mathsf P$, the universal free-measure property and the retract $T_r\subset\mathcal M_{<p}(S_\infty)$ imply that every $T_r\to\mathsf Q$ lifts. Corollary 18.4 then gives a lift for every $\underline s\to\mathsf Q$. This is a **conditional** statement: the map in (18.15) has not been proved surjective. Surjectivity of the liquid quotient morphism as a sheaf is insufficient, since $S_\infty$ is not extremally disconnected.

A related explicit control shows why checking point values cannot replace a sectionwise argument. The continuous map $u:S_\infty\to\mathbb R^{\mathbb N}$ given by $u(n)=e_n$ and $u(\infty)=0$ defines a section whose image in $\mathsf Q(S_\infty)$ is **nonzero**, although it vanishes on every singleton point: $e_n$ belongs to the finite-coordinate sum for each $n$, but no **uniform finite prefix** contains all $e_n$. This ghost section **does lift** (by $u$), so it is not a counterexample to (18.15). It is a proof that singleton tests alone cannot decide the missing lifting gate.

### Theorem 18.7 — the local lifting gate actually holds

For **every** profinite test space $K$, the canonical map

$$
\mathsf P(K)\longrightarrow\mathsf Q(K)
\tag{18.17}
$$

is surjective. In particular, the map (18.15) for the convergent-sequence space $S_\infty$ is surjective.

**Proof by effective descent.** Write $\mathsf S=\varinjlim_m\underline{\mathbb R^m}$ and $\mathsf P=\prod_n\underline{\mathbb R}$. Let $v\in\mathsf Q(K)$. Since $\mathsf Q$ is the sheaf cokernel of $\mathsf S\hookrightarrow\mathsf P$, there is a finite jointly surjective profinite covering, combined into a surjective map $\pi:T\to K$, and a section $a\in\mathsf P(T)$ whose image is $\pi^*v$. Consider $T\times_K T$, also profinite. The two pullbacks of $a$ have the same image in $\mathsf Q(T\times_K T)$, so their difference lies in the **sheaf kernel** $\mathsf S(T\times_K T)$. Filtered colimits of condensed sections are computed sectionwise. Consequently **one integer $m$** exists such that for all pairs $(t,t')$ with $\pi(t)=\pi(t')$ and every output coordinate $n>m$,

$$
a_n(t)=a_n(t').
\tag{18.18}
$$

Every $a_n:T\to\mathbb R$ with $n>m$ therefore descends to a continuous function $b_n:K\to\mathbb R$, because the surjection $\pi$ from compact Hausdorff $T$ to Hausdorff $K$ is a topological quotient. Define $b_n=0$ for $n\le m$. All coordinates $b_n$ are continuous, hence $b=(b_n)_n$ defines a section in $\mathsf P(K)=\mathrm{Cont}(K,\mathbb R^{\mathbb N})$. Over $T$ the difference $a-\pi^*b$ has only its first $m$ coordinates possibly nonzero, so is an element of $\mathsf S(T)$. Thus $q(b)$ and $v$ have the same restriction to the jointly surjective cover $T\to K$; by sheaf descent they are equal on $K$. This proves (18.17). $\square$

**Corollary 18.8 (fixed Fréchet phantom channel vanishes in ZFC).** For the source $\underline s\cong\underline{\mathcal D_{[-1,1]}(\mathbb R)}$,

$$
\mathrm{Hom}(\underline s,\mathsf P)
\twoheadrightarrow
\mathrm{Hom}(\underline s,\mathsf Q),
\qquad
K(\underline s)=0.
\tag{18.19}
$$

Indeed, Theorem 18.7 applies to $S_\infty$, and the universal free-measure property lifts every morphism from $\mathcal M_{<p}(S_\infty)$ to $\mathsf Q$ through $\mathsf P$. The retract (18.8) lifts every stage morphism $T_r\to\mathsf Q$. Corollary 18.4 then lifts any morphism $\underline s\to\mathsf Q$. Therefore the entire **scalar-invisible phantom channel** of (17.14) is absent for this fixed Fréchet source.

**Limits of the result.** The surjectivity (18.17) is for sections on profinite test objects, not a claim that the epimorphism $\mathsf P\to\mathsf Q$ admits a global **liquid-linear section** $\mathsf Q\to\mathsf P$. The non-split extension (17.2) for source $\mathsf Q$ remains valid. The ghost plot in (18.16) likewise remains nonzero but has a global lift. Equation (18.19) does not settle the infinitely coordinate-visible scalar Ext channel or the non-scalar part of the genuine test-function output.

## 4. What the 2026 scalar Ext literature does and does not yield

Grisha Taroyan's [August 2026 MathOverflow argument](https://mathoverflow.net/questions/510488/operatornameext1s-mathbb-r-in-the-category-of-liquid-vector-spaces/514158) establishes, under **ZFC + the Continuum Hypothesis**, a nonzero class in $\mathrm{Ext}^1_{\mathcal A_p}(\underline s,\underline{\mathbb R})$ through a derived inverse limit of the weighted spaces $V_r$. Peter Scholze's [response and comments](https://mathoverflow.net/questions/510488/operatornameext1s-mathbb-r-in-the-category-of-liquid-vector-spaces) support the nature of this argument and caution that unconditional behaviour is subtle. Neither the Continuum Hypothesis nor the Open Colouring Axiom may be silently assumed for EXT-015.

A nonzero scalar Ext¹ class under CH lies in one scalar-output component. Theorem 18.2 shows something stronger: **all classes supplied solely by the stagewise-split derived-limit edge for $\mathsf S$ have finite scalar output support**, regardless of whether scalar Ext¹ vanishes or not. The familiar CH $\varprojlim^1$ phenomenon is therefore **not, by itself, a negative answer to EXT-015C**.

## 5. Honest boundary: original test-function target

By [017](SCALAR_PHANTOM_ESCAPE_017.md), $\mathsf S$ is a split liquid subobject of the actual output

$$
G=\varinjlim_b\underline{\mathcal D_{[-b,b]}(\mathbb R)}
$$

and the scalar-sum comparison cokernel injects into the target-stage comparison cokernel. Theorem 18.2 implies: **any scalar-summand escaping extension for the prescribed fixed source must already be nonsplit over some weight stage $T_r$**. The nonliftable scalar phantom route is ruled out entirely by Theorem 18.8; only stage-local coordinate-visible scalar classes could still escape.

This is **not** a proof that no such local-stage obstruction exists. It also does **not** classify all classes in $\mathrm{Ext}^1(H,G)$; the complementary test-function output can carry other extensions.

The remaining two sharply bounded mathematical possibilities are:

1. **Scalar local-stage obstruction:** exhibit or rule out a nonzero image in $\mathrm{Ext}^1(T_r,\mathsf S)$ that can extend coherently to the full fixed Fréchet source, and survives every finite output prefix. Proving $\mathrm{Ext}^1(T_r,\mathsf S)=0$ for every $r$ is a sufficient, **not yet established**, scalar positive result. Do not confuse compactness of $T_r$ with projectivity or with derived compactness.
2. **Full test-function obstruction:** even if scalar local-stage escape is excluded, determine whether the non-scalar complement of $G$ supports a genuine class not arising from any compact stage. Use the corrected first-syzygy quotient from [review 016](AGENT_CRITICAL_REVIEW_AB_016.md) and check all liquid boundaries.

**Finite-dimensional warning:** $\underline{\mathbb R^m}$ is projective in $\mathcal A_p$, so all degree-one liquid Ext classes restrict to zero on finite-dimensional coordinate truncations of the Fréchet source. Finite-dimensional computations cannot settle either possibility, even in principle.

## 6. Verification ledger and status

| Obligation | Mathematical verdict |
| --- | --- |
| Valdivia–Vogt source identification $H\cong\underline s$ | SOURCE GROUNDED for $K=[-1,1]$ |
| Countably directed inverse-system lemma (18.3) | PROVED in ZFC |
| Measure-stage compactness and scalar Hom direct-sum factorization (18.8–18.10) | PROVED from free-measure universal property and scalar projectivity, with source-stage presentation |
| Stagewise-split classes in $\mathrm{Ext}^1(H,\mathsf S)$ have finite support (18.13) | PROVED conditional on the source-backed measure-stage presentation (18.2) |
| CH implies existence of some scalar $\mathrm{Ext}^1(s,\mathbb R)$ classes | EXTERNAL CONDITIONAL RESULT, not GCL independent theorem, and not target escape |
| Every $\mathrm{Hom}(T_r,\mathsf Q)$ map lifts to $\mathsf P$ | PROVED (18.17), by finite-coordinate effective descent |
| Every $\mathrm{Ext}^1(T_r,\mathsf S)$ vanishes | OPEN; stronger sufficient gate, requiring scalar stage acyclicity |
| Fixed-source phantom group $K(\underline s)$ | ZERO: PROVED IN ZFC (18.19) |
| Full fixed-source target-stage $\mathrm{Ext}^1$ comparison is surjective or not | OPEN |

**Research discipline:** Preserve the full exact-category distinctions and original source hypotheses. Do not report an auxiliary non-Fréchet-source result or a set-theoretically conditional scalar result as a proof of the original comparison. GCL agents, not the Human Steward, own subsequent mathematical investigations and critical checks.
