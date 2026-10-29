# EXT-015 REACH / M4 / 094 — new-input audit of the actual weighted liquid Hom systems

**Disposition: structural audit; no new sufficient mechanism for original R3.** The weighted Hom groups have the exact Fréchet-null-sequence/operator-matrix description proved below. Their auxiliary topology, dense transition maps, countable weight absorption and product-index cofinality can also be proved in ZFC. None supplies global normalization (84.19), an actual nonlifting morphism in (85.14), or a realizable infinite family of nonzero classes in (85.16). No new opposed proof/counterexample construction is started. Original R3 remains open, independently of the field-theoretic M1–M3 track.

**Role and dependency disclosure:** this auditor authored 082. Its earlier acceptance of the actual 067 presentation/injectivity is a shared dependency, not a new independent certification. The present task is a separate non-author new-input audit within the same Codex system. It is neither external certification nor a claim of institutional independence. Only this file is authored; sources, checkpoints, trackers, Git history and protected state are unchanged.

## 1. Exact inputs, category and unchanged target question

The read local source cut is `1452f5b9e982f30bcb43e640a9361c168ce8a599`, on ordinary branch `research/reach-m1-liquid-bridge-20261029`, in `F:\_codex\MATH\_worktrees\reach-reassessment-20261027`. The parent supplies the protected protocol custody: PR #2896, native merge `e06b00010c080663461488f23fea819a24d91063`, with its six-blob readback complete. The reported merge parents are `c534d2dc31e877590e0bea05237ab320883ffefe` and candidate `eac5ab8e89088e170c09658031672aa593ac7584`; the local source cut descends from that candidate through progress metadata. The remote merge commit is not present in this checkout's object database; this audit binds the actual locally read inputs by the following Git blobs rather than claiming a second read of that remote commit.

Paths in this table are relative to this directory unless marked otherwise.

| Input | Exact read Git blob |
| --- | --- |
| [090, authoritative full REACH protocol](REACH_CONDENSED_RENORMALIZATION_PLAN_090.md) | `6b642bf10c3328bb64d37474e290810fb45cbca1` |
| [018, rapid-weight and target realization inputs](FIXED_SOURCE_WEIGHT_LOCALIZATION_018.md) | `a6c5670d10d35a7acc761f60c6273c2034cc82a3` |
| [019, original degree-one theorem](FIXED_SOURCE_EXT1_ISOMORPHISM_019.md) | `6b0fb373b8bde1434b3b443f16274c626e0d954c` |
| [037, actual singleton-reduced cover](R3_ALL_SINGLETON_LINEAR_RELATIONS_037.md) | `68b92dfca0bdd51707f409ff79f2770a310fc4e0` |
| [067, actual evaluated cover and stage injectivity](R3_EVALUATED_RELATION_COVER_067.md) | `7069938ce1e75f946e2f4ff70fcabb2f073065e9` |
| [082, this auditor's earlier source audit](REASSESSMENT_FRESH_AUDIT_082.md) | `b596a671ec62ec1dfed4343a834d5ac7343e19cb` |
| [084, completed positive attempt and exact unresolved normalization](R3_POSITIVE_SUPPORT_ATTEMPT_084.md) | `932be6cc3445182a8423b23cc4840fe7ad685ced` |
| [085, completed negative attempt and boundary/product controls](R3_COUNTEREXAMPLE_ATTEMPT_085.md) | `9f4463bc17cb723043f27965ebfbbef0bf2f657a` |
| [086, source-bound reassessment critique](AGENT_CRITICAL_REVIEW_REASSESSMENT_086.md) | `8934ec118e2b6a62a7d4ff5730dc815d7b9f66f8` |
| `../LFO3_SURJECTIVITY_THEOREM_013.md` | `ad974987c2ef9ae1f24c93b521cd59d8f764e0c0` |
| Root `AGENTS.md` | `68c5ece274011cd53682e90a27c990c8ab7b6923` |
| Root `ci/math_markdown_gate.py` | `71356dcb861bb2eb4fb7cb93ee3075f787e2c065` |

Fix $0<p\le1$ and work in the real abelian category $\mathcal A_p=\mathrm{Liq}_p(\mathbb R)$, in the same small condensed universe as 067. All unqualified arguments here are in ZFC. Retain the actual objects and covers:

$$
\begin{gathered}
H=\underline{\mathcal D_{[-1,1]}(\mathbb R)}\simeq\underline s,
\qquad G=\underline{\mathcal D(\mathbb R)}\simeq E=\bigoplus_{n\ge1}B_n,
\qquad B_n=\underline s,\\
0\longrightarrow K\longrightarrow P_{\mathrm{red}}\longrightarrow H\longrightarrow0,
\qquad
0\longrightarrow K_1\overset{j}{\longrightarrow}P_1\overset{q}{\longrightarrow}K\longrightarrow0.
\end{gathered}
\tag{94.1}
$$

The real strict-LF/liquid realizations and two-way factorization of finite prefixes $E_N$ with actual compact-support stages $G_b$ are the admitted hypotheses of 018/019/067. Neither $K$ nor $K_1$ is assigned a Fréchet or bornological topology. The remaining equation is still, for every actual liquid $f:K_1\to G$,

$$
f=\iota_b f_b+\psi j
\quad\text{for some }b,\ f_b:K_1\to G_b,\ \psi:P_1\to G.
\tag{94.2}
$$

The stage-comparison injection of 067 is retained. Nothing below turns that injection into surjectivity.

## 2. Genuine liquid Hom gives an exact null-sequence description

Write $S_\infty=\mathbb N\cup\{\infty\}$ with its convergent-sequence profinite topology and put $M(S)=\mathcal M_{<p}(S)$. The collapse to a point and its section at $\infty$ split the actual liquid object:

$$
D=\ker\bigl(M(S_\infty)\longrightarrow M(*)\bigr),
\qquad M(S_\infty)\simeq M(*)\oplus D.
\tag{94.3}
$$

Here $D$ is the $\mathcal M_{<p}(\mathbb N)$ of 018/084. This notation denotes this retract, not a free object on a noncompact profinite set. Its distinguished generators are $g_i=\delta_i-\delta_\infty$.

Let $r=(r_i)$ be a positive rapid weight. Under the actual identification $T_r=rD\subset\underline s$, the distinguished element $g_i$ maps to $r_i e_i$. Thus the physical coordinate vector $e_i$ belongs to $T_r$ as $g_i/r_i$. Put $W_n=s^{\mathbb N}$, with columns $a_i\in s$, and use the usual seminorms

$$
q_k(x)=\sup_{j\ge1}(1+j)^k|x_j|,
\qquad k\ge0.
\tag{94.4}
$$

**Lemma 94.1 — actual Hom, not a vector-space shadow.** Evaluation at the physical $e_i$ identifies the ordinary real vector space of liquid morphisms with

$$
\boxed{
V_{r,n}=\mathrm{Hom}_{\mathcal A_p}(T_r,B_n)
=\left\{(a_i)\in s^{\mathbb N}:\ r_i a_i\longrightarrow0\text{ in }s\right\}.
}
\tag{94.5}
$$

Equivalently, writing $a_{ji}$ for the matrix with source index $i$ and target-sequence index $j$,

$$
\boxed{
\forall k\ge0,\qquad
\lim_{i\to\infty}r_i\sup_{j\ge1}(1+j)^k|a_{ji}|=0.
}
\tag{94.6}
$$

Every column is required to lie in $s$. The limit is uniform in the internal target index $j$ for each fixed seminorm. The external target-summand index is $n$ and is distinct from both $i$ and $j$.

**Proof.** The free-liquid universal property gives

$$
\mathrm{Hom}_{\mathcal A_p}(M(S_\infty),\underline s)
=\mathrm{Cont}(S_\infty,s).
$$

Restriction to the direct summand $D$ identifies its Hom group with continuous plots taking value zero at $\infty$: extend a map out of $D$ by zero on the summand $M(*)$, or restrict such a plot. A plot is therefore exactly a null sequence $b_i\to0$ in $s$, and its values on $g_i$ determine the morphism uniquely. For $T_r$, those values are $b_i=f(r_i e_i)=r_i f(e_i)=r_i a_i$. This proves both necessity and sufficiency in (94.5), as actual liquid morphisms. Equation (94.6) is the definition of Fréchet convergence through (94.4). No projectivity of $M(S_\infty)$ is used. $\square$

This identification holds for each fixed admitted $p$. Its displayed ordinary Hom subspace does not acquire a different condition when $p$ changes. No assertion of higher-Ext invariance in $p$ is inferred.

### Auxiliary operator formulation and its category boundary

The same data determine an auxiliary continuous linear operator

$$
L_{r,a}:\ell^1\longrightarrow s,
\qquad L_{r,a}(x)=\sum_i x_i r_i a_i.
\tag{94.7}
$$

For $a\in V_{r,n}$, the sum converges in the complete Fréchet space $s$ because $\sup_i q_k(r_i a_i)<\infty$ for every $k$. If $P_N$ is coordinate truncation on $\ell^1$, then

$$
\sup_{\|x\|_1\le1}q_k\bigl(L_{r,a}(1-P_N)x\bigr)
=\sup_{i>N}q_k(r_i a_i)\longrightarrow0.
\tag{94.8}
$$

The upper bound is the triangle inequality; a single signed basis vector gives the reverse supremum bound. Conversely, an operator with columns $r_i a_i$ satisfying (94.8) supplies the null sequence and hence the genuine liquid morphism of Lemma 94.1. Thus this is an exact operator-matrix encoding of those Hom groups. It is **not** an identification of $T_r$ with $\ell^1$, an identification of a liquid internal Hom with an operator topology, or a comparison between bornological and liquid Ext.

## 3. The inverse systems and their quotient topology trap

For $r\preceq t$, meaning $\sup_i r_i/t_i<\infty$, the actual source inclusion induces the common-coordinate inclusion $V_{t,n}\subseteq V_{r,n}$. Indeed $r_i a_i=(r_i/t_i)(t_i a_i)$, so (94.6) is preserved. Equivalent representatives of the weight class give the same subspace.

There is a useful auxiliary Fréchet topology on $V_{r,n}$, with seminorms

$$
\|a\|_{r,k}=\sup_i r_i q_k(a_i).
\tag{94.9}
$$

Multiplication by $r_i$ identifies it with $c_0(\mathbb N,s)$ equipped with the uniform seminorms. Completeness follows by taking the limit in the complete space $s$ in each column of a Cauchy sequence; uniform Cauchy control in each seminorm preserves the null tails. The inclusion from $t$ to $r$ is continuous with bound $\|a\|_{r,k}\le C\|a\|_{t,k}$. It has dense image: finite-source-column truncations belong to every $V_{t,n}$ and converge to $a$ in every seminorm (94.9) when $a\in V_{r,n}$.

These are auxiliary topological facts about ordinary Hom vector spaces. The Roos and quotient systems of 084 are still the ordinary inverse systems

$$
\begin{gathered}
X_{r,n}=W_n/V_{r,n},\qquad
V_r=\bigoplus_nV_{r,n},\qquad X_r=\bigoplus_nX_{r,n},\\
Y_r=\prod_nV_{r,n},\qquad U_r=Y_r/V_r.
\end{gathered}
\tag{94.10}
$$

The maps $X_{t,n}\to X_{r,n}$ are the algebraic quotient maps and are surjective. They are not proved to have coherent splittings. Surjectivity of transition maps on an uncountable directed set is not the sequential Mittag–Leffler theorem.

**Hostile quotient control.** Give $W_n=s^{\mathbb N}$ its product Fréchet topology. Its finite-source-column sequences lie in $V_{r,n}$ and are dense in $W_n$. But $V_{r,n}$ is proper: take $a_i=r_i^{-1}h$ for fixed nonzero $h\in s$. Then $r_i a_i=h$ is not null. Thus $X_{r,n}$ is a nonzero algebraic quotient by a dense proper subspace. Its Hausdorff topological quotient is zero. Substituting that Hausdorff quotient would delete precisely the algebraic data under study. Neither $X_{r,n}$ nor a naive condensed realization of this non-Hausdorff quotient is the categorical coefficient $Q=P/E$.

## 4. Cofinality and countable controls in ZFC

The exact matrix description permits bounded structural controls. They clarify the quantifiers but do not normalize the global cocycle.

### Upper bounds and absence of a sequential cofinal replacement

For countably many positive rapid weights $r^{(m)}$, put

$$
D_m=1+\sum_{k=0}^m q_k\bigl(\sqrt{r^{(m)}}\bigr),
\qquad
t_i=\sum_{m\ge1}\frac{2^{-m}\sqrt{r_i^{(m)}}}{D_m}.
\tag{94.11}
$$

Every square-root weight is rapid. For fixed $k$, the tail with $m\ge k$ has $q_k$ bounded by $\sum_m2^{-m}$, and the finitely many earlier terms are rapid. Thus $t$ is positive and rapid. The summand indexed by $m$ gives $r_i^{(m)}/t_i\le2^mD_m\sqrt{r_i^{(m)}}$, so $r^{(m)}\preceq t$, even with ratio tending to zero. This proves countable direction without CH.

There is no largest weight class: $\sqrt r$ is rapid and is not dominated by $r$, since $r_i\to0$. Consequently there is **no countable cofinal subset**. Otherwise its countable upper bound would dominate every weight, contradicting this example. Replacing the actual weight system by one countable inverse tower is therefore unjustified.

Under **the additional hypothesis CH**, one can enumerate all rapid weights in length $\omega_1$ and recursively choose upper bounds at each countable stage, obtaining a cofinal chain indexed by $\omega_1$. This is a conditional indexing statement only. It proves neither (84.19) nor a degree-two class, and CH is not assumed by this audit.

### Countable product-index reformulation

The diagonal $\mathscr R\to\mathscr R^{\mathbb N}$ is monotone and cofinal for the coordinatewise product order: every tuple has a common upper bound by (94.11). The category of such upper bounds is nonempty and directed, hence has contractible nerve. Thus the usual derived cofinal restriction applies to systems on that product. One may write

$$
\widetilde V_{(r_n)}=\bigoplus_nV_{r_n,n},
\qquad
\widetilde X_{(r_n)}=\bigoplus_nX_{r_n,n},
\tag{94.12}
$$

and recover the derived limits of (94.10) by diagonal restriction. This places an additivity theorem's possible product-index hypothesis on the correct objects. It does **not** prove the additional partition property needed by such a theorem.

### A bounded absorption lemma, with the opposite quantifier from normalization

**Lemma 94.2.** Given a fixed positive rapid weight $r^0$ and any countable list $a^{(m)}\in s^{\mathbb N}$, there is a positive rapid $t$ with $t\preceq r^0$ and $a^{(m)}\in V_{t,n}$ for every prescribed matrix, identifying the copies of $s$.

**Proof.** Set

$$
t_i=\min\left\{r_i^0,
\frac{(1+i)^{-i}}{1+\max_{1\le m\le i,\ 0\le k\le i}q_k(a_i^{(m)})}\right\}.
\tag{94.13}
$$

This is positive and rapid and satisfies $t_i\le r_i^0$. For fixed $m,k$ and $i\ge\max(m,k)$, the product $t_iq_k(a_i^{(m)})$ is at most $(1+i)^{-i}$ and hence tends to zero. Lemma 94.1 proves the claim. $\square$

The lemma absorbs a prescribed countable set after moving **downward** to a smaller weight. A smaller-weight set is not a cofinal upper tail of the original directed source presentation. It does not choose finite-supported $\beta_r$ simultaneously for every weight and every edge of an arbitrary Roos cocycle. There is also no one weight absorbing every matrix: the fixed non-null example after (94.10) defeats that assertion at each chosen weight. This is a structural lemma, not sufficient progress on (84.19).

## 5. The exact global inference still missing

Retain the actual-cover comparison and coefficient-specific local acyclicity from 084/086. Their derived computation is

$$
\mathrm{Ext}^2(H,E)\simeq\varprojlim{}^2V_r
\simeq\varprojlim{}^1X_r,
\qquad
\mathrm{Ext}^2(H,B_n)\simeq\varprojlim{}^1X_{r,n}.
\tag{94.14}
$$

The acyclicity of each $T_r$ against these coefficients is supported by the primary-source uniform hypercover primitive argument, not by projectivity of an arbitrary profinite measure object. It makes degree-two classes restrict to zero at every $T_r$; it does not make the global groups vanish.

To express (84.19) using actual matrices, let $A_{r,t,n}\in W_n$ be finite-supported in $n$ separately for each edge $r\preceq t$ and represent a quotient 1-cocycle. Its cocycle identity is modulo the subspaces (94.6). One must find one finite set $F$ and matrices $B_{r,n}\in W_n$, finite-supported in $n$ separately for each $r$, such that

$$
\boxed{
\forall r\preceq t,\ n\notin F,\ k\ge0,\qquad
\lim_{i\to\infty}r_iq_k\bigl(A_{r,t,n,i}-B_{t,n,i}+B_{r,n,i}\bigr)=0.
}
\tag{94.15}
$$

The source-index restriction is the identity on the common matrix coordinates; its quotient at $r$ explains the factor $r_i$ in this formula. Changing representatives by $V_{r,n}$ does not change the condition. Equation (94.15) is exactly (84.19), with its missing global finite support and boundary adjustment visible. It is a characterization of the unresolved problem, not a solution obtained from (94.6).

The auxiliary null-sequence norms supply no bound or measurability hypothesis on the arbitrary family $A_{r,t,n}$ over its uncountably many weight strings. Finite-rank approximation in (94.8), countable absorption in (94.13), and dense transition maps therefore do not construct those $B_r$ or the single $F$. The countably directed nested-subspace lemma 18.1 is about first derived limits of $V$, not first derived limits of the quotient system $X$. Applying it to $X$ remains invalid.

## 6. Both residual channels retain their original tests

Put $P=\prod_nB_n$ and $Q=P/E$ in the liquid category. The exact residuals of 067/084/085 are unchanged:

$$
\begin{aligned}
\mathrm{Ph}^2
&=\ker\left[\mathrm{Ext}^2(H,E)\longrightarrow\prod_n\mathrm{Ext}^2(H,B_n)\right]\\
&\simeq\mathrm{coker}\left[\varprojlim{}^1Y_r\longrightarrow\varprojlim{}^1U_r\right]\\
&\simeq\frac{\mathrm{Hom}_{\mathcal A_p}(K,Q)}
{\pi\mathrm{Hom}_{\mathcal A_p}(K,P)},
\end{aligned}
\tag{94.16}
$$

and

$$
0\longrightarrow\mathrm{Ph}^2
\longrightarrow\mathrm{coker}(\theta_H^2)
\longrightarrow
\frac{\mathrm{im}[\varprojlim{}^2V_r\longrightarrow\prod_n\varprojlim{}^2V_{r,n}]}
{\bigoplus_n\varprojlim{}^2V_{r,n}}
\longrightarrow0.
\tag{94.17}
$$

| Channel | Sufficient new mathematical input | What this audit supplies |
| --- | --- | --- |
| Coordinate-invisible, (67.12)/(84.25)/(85.14) | A compatible liquid-linear lift for every actual $K\to Q$, or an actual morphism that has no such lift | Neither; the matrix description controls maps out of $T_r$, not a linear lift on the whole syzygy |
| Infinitely coordinate-visible, (67.13)/(84.26)/(85.16) | Global finite support of every realizable family modulo projective boundaries, or an infinite family with exact plotwise finite support and infinitely many nonzero coordinate Ext classes | Neither; no nonzero degree-two coordinate class or realizing family is constructed |
| Both simultaneously | Uniform quotient-cocycle normalization (94.15), with its actual-cover chain transfer from 084 | An exact concrete description of its coefficients and unchanged missing quantifier; no normalization mechanism |

The sharpened phantom quotient in (94.16) accounts for **all** boundaries because maps $P_{\mathrm{red}}\to Q$ lift through $P$ by projectivity and their restrictions are already in the displayed denominator. For the visible channel, a family $\phi_n:K_1\to B_n$ must vanish in all but finitely many coordinates after precomposition with each compact projective relation plot. This is exact zero, not rapid numerical decay. Infinitely many resulting classes must also remain nonzero modulo every restriction from $P_1$.

### Hostile boundary and product controls

- In 085, $f_0=\Psi j$ has unbounded output support but is one explicit global boundary. Reusing its support escape cannot provide a new class.
- The nonzero ghost $h_K$ in (85.11) has the actual product lift (85.12). Formula (85.13) proves that every lift choice gives a boundary. A nonzero quotient section alone is not a phantom Ext class.
- In matrix language, fix nonzero $h\in s$ and put $a_i^{(n)}=r_i^{-1}\delta_{in}h$. Each fixed $n$ belongs to $V_{r,n}$, so the full family is in $Y_r$. Its unscaled null-sequence plot is $i\mapsto\iota_i h$ in the product. It has no uniform finite target prefix and is not in $V_r$. This restates the product/ghost control, with its explicit lift; it is not a new counterexample construction.
- Checking each fixed matrix row is insufficient. With $a_i=r_i^{-1}e_i$, each fixed internal coordinate of $r_i a_i$ is eventually zero, but $q_0(r_i a_i)=1$. Thus scalar coordinate checks alone do not establish a liquid Hom into $s$.
- Multiplying external target coordinates by nonzero rapidly decreasing scalars cannot turn infinitely many nonzero composites into the eventually exact-zero composites needed for a map into $E$. Nor can Hausdorff completion of the quotients in section 3 preserve their algebraic obstruction data.

## 7. Primary-literature and hypothesis audit

Only primary mathematical sources were consulted. The following uses are distinguished from unproved transfers:

| Source inspected directly | Applicable input | Excluded inference |
| --- | --- | --- |
| Scholze, [Analytic Geometry](https://people.mpim-bonn.mpg.de/scholze/Analytic.pdf), Theorem 6.5 | Universal extension of profinite plots and compact projective generators on extremally disconnected sets; this proves Lemma 94.1 through the split retract | Projectivity of every profinite measure object |
| Same source, Proposition 8.19 and Proposition 10.1 with its real-base-change paragraph | Uniform scalar primitives and degree-zero derived free liquidification support 084's coefficient-specific local computation | Global acyclicity of $H$, $K$ or $K_1$ |
| Taroyan, [primary MathOverflow answer 514158 to question 510488](https://mathoverflow.net/questions/510488/operatornameext1s-mathbb-r-in-the-category-of-liquid-vector-spaces/514158) | Rapid-weight presentation and countable-direction construction; the relevant elementary weight facts were checked above | The answer's arbitrary-profinite projectivity sentence is not valid as stated. Its scalar first-degree CH conclusion and suggested independence extension are not original R3 verdicts |
| Bannister–Bergfalk–Moore–Todorcevic, [A descriptive approach to higher derived limits](https://ems.press/content/serial-article-files/51446), Theorem 8.4 and Definition 8.3 | Additivity under the stated product-poset coloring/cofinal-homogeneity hypothesis; (94.12) identifies the relevant product indexing | No such partition premise has been proved for these weighted systems in ZFC; an analytic description of the coefficients does not establish it or make arbitrary cochains Borel |
| Clausen–Scholze, [Condensed Mathematics and Complex Geometry](https://arxiv.org/pdf/2605.11731), Theorem 4.11/Remark 4.12 | Flatness and completed tensor calculations under the stated summability/nuclear Fréchet hypotheses | Exactness of Hom from $H$, projectivity, a lift out of $K$, or higher-Ext/additivity conclusions |

The source representation retains the real-liquid rather than merely a bornological interpretation. A result about a different exact category would require an exact comparison that preserves the relevant extensions, boundaries and realizability condition. None is supplied by tensor flatness. The direct free-liquid proof of (94.5) avoids relying on any such comparison.

The local proof in 084 does not need the erroneous projectivity sentence in the primary MathOverflow answer: it uses the derived free identity and coefficient-specific hypercover primitives from Scholze. A conditional scalar degree-one nonvanishing result, even if fully repaired, has neither the degree nor the target needed for (94.16)–(94.17). No CH, OCA, forcing axiom or independence claim for original R3 is admitted here.

## 8. One correction pass, validation and exact disposition

The primary audit delivered its conclusion to the parent before this final file: actual weighted null-sequence structure is available, but no new sufficient normalization or nonlifting mechanism has been found. This is the appropriate **new-input audit return**, not an unsuccessful new opposed construction and not an impossibility theorem for original R3.

The single correction pass checks the actual liquid universal property, all Fréchet seminorms in the matrix condition, physical-coordinate scaling, direction of source and quotient maps, product-diagonal cofinality, downward absorption versus an upper cofinal tail, exact support versus convergence, and both existing boundary controls. No new construction route or new set-theoretic premise is introduced in that pass.

Execution is CHAD Windows PowerShell. The existing isolated interpreter `F:\_codex\MATH\_evidence\reach-completion-20261027\.venv\Scripts\python.exe` reported CPython 3.12.12 and its distinct virtual-environment prefix. No root `uv.lock` or root Python project is admitted; this evidence environment is **unpinned**. The Python process explicitly sets `UV_CACHE_DIR=C:\Users\jamie\AppData\Local\GCL\uv` and `PYTHONPYCACHEPREFIX=C:\Users\jamie\AppData\Local\GCL\PythonBytecodeCache`. There are no dependency installations, lock resolutions, system-Python shortcuts, hosted allocations, numerical fixtures or finite tests purporting to settle infinite cohomology.

Validation on 2026-10-29: the mathematical Markdown source preflight passed. Its first run identified three delimiter/prose adjacency defects; these were corrected editorially, without changing the mathematical argument. A direct check of this untracked file found no trailing whitespace and confirmed its final newline; the path-scoped `git diff --check` also passed. The source gate is repeated after this validation record. The non-self-referential final Git blob is returned to the parent separately. No finite cohomology fixture was added or replayed.

**Final M4 boundary:** Lemmas 94.1–94.2 and the cofinality/topology controls are bounded structural results proved here as source-bound candidates, without a mathematical priority claim or an assertion that this audit supplies their separate protected admission. They do not meet protocol 090's new-input threshold for reopening an opposed degree-two construction. Equation (94.15), equivalently the original (84.19)/(67.14), remains unresolved. No actual nonlifting $K\to Q$ or simultaneously realizable infinite family of nonzero coordinate degree-two classes has been found. Original R3 remains open; M1's field-theoretic tensor statement cannot discharge it.
