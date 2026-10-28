# EXT-015 REACH-R3 / 085 — diagonal counterexample attempt and its boundary obstruction

**Verdict: INCONCLUSIVE; no counterexample to (67.14).** One primary construction and one correction pass are complete. The primary construction is an actual liquid map out of the exact second kernel, with no bounded output stage. It is nevertheless an explicit projective boundary. The correction constructs an actual nonzero, pointwise-invisible quotient morphism on the first kernel. It has an explicit product lift, so it too gives zero in the degree-two phantom channel. Neither construction survives the required boundary test. Sections 4–5 isolate the additional existence/nonvanishing statements that would be needed for either negative channel.

This is a fresh-context, negative mathematical attempt within the same Codex system. It is not external certification. No opposing R3 attempt or future attempt draft was read. No source theorem, checkpoint, tracker, commit, pull request, or protected state was changed by this pass.

## 1. Fixed objects, custody, and source transfer

The original protected mathematical input is `9cc483334648d94ea6226a76874151a3eabd33b1`; the reconciled audit input is `afb5a6873562a9050b8a1fb65dee42f399db9967`. All source blobs below are read at the latter commit. Paths are relative to this directory except for the marked prerequisite.

| Source | Git blob |
| --- | --- |
| `REACH_REASSESSMENT_081.md` | `128ad967100e73f6ea91581a7835f6809daebaee` |
| `REASSESSMENT_FRESH_AUDIT_082.md` | `b596a671ec62ec1dfed4343a834d5ac7343e19cb` |
| `R3_EVALUATED_RELATION_COVER_067.md` | `7069938ce1e75f946e2f4ff70fcabb2f073065e9` |
| `R3_ALL_SINGLETON_LINEAR_RELATIONS_037.md` | `68b92dfca0bdd51707f409ff79f2770a310fc4e0` |
| `FIXED_SOURCE_WEIGHT_LOCALIZATION_018.md` | `a6c5670d10d35a7acc761f60c6273c2034cc82a3` |
| `FIXED_SOURCE_EXT1_ISOMORPHISM_019.md` | `6b0fb373b8bde1434b3b443f16274c626e0d954c` |
| `AGENT_CRITICAL_REVIEW_AB_016.md` | `74fee0606b392460c90c32af85a1d86039597f74` |
| `../LFO3_SURJECTIVITY_THEOREM_013.md` | `ad974987c2ef9ae1f24c93b521cd59d8f764e0c0` |

Fix $0<p\le1$ and work throughout in $\mathcal A_p=\mathrm{Liq}_p(\mathbb R)$. The original objects are

$$
H=\underline{\mathcal D_{[-1,1]}(\mathbb R)},\qquad
G_b=\underline{\mathcal D_{[-b,b]}(\mathbb R)},\qquad
G=\underline{\mathcal D(\mathbb R)}.
$$

Retain the *actual* fixed covers of 037/067:

$$
0\longrightarrow K\overset{i}{\longrightarrow}P_{\mathrm{red}}
\overset{\varepsilon}{\longrightarrow}H\longrightarrow0,
\qquad
0\longrightarrow K_1\overset{j}{\longrightarrow}P_1
\overset{q}{\longrightarrow}K\longrightarrow0.
\tag{85.1}
$$

In particular, $P_1$ has its summand $\mathcal M_{<p}(S)$ for every actual relation morphism $r:\mathcal M_{<p}(S)\to P_{\mathrm{red}}$ in (67.2). No convenient topology on either kernel is introduced.

The category input was checked directly in Scholze's [*Lectures on Analytic Geometry*, Theorem 6.5](https://people.mpim-bonn.mpg.de/scholze/Analytic.pdf#page=35): free-liquid extension of profinite plots, closure under kernels/cokernels/extensions, compact projective generators on extremally disconnected sets, and fully faithful derived inclusion. Only those assertions are used below. In particular, no projectivity of the free module on a general profinite set is inferred.

Fix the admitted coefficient isomorphism from 018/019,

$$
\chi:G\overset{\sim}{\longrightarrow}E=\bigoplus_{n\ge1}B_n,
\qquad B_n=\underline s,\qquad E_N=\bigoplus_{n\le N}B_n.
\tag{85.2}
$$

The strict-LF realization and two-way stage factorization are hypotheses inherited exactly from those sources and the reconciled audit. They identify finite-prefix and original support-stage classes as in 067. All maps to $E$ constructed below are transported to the requested $G$ by $\chi^{-1}$; the source and cover are never changed.

A potentially tempting primary-source transfer is unavailable: Clausen–Scholze's [*Condensed Mathematics and Complex Geometry*, Theorem 8.15 proof](https://people.mpim-bonn.mpg.de/scholze/Complex.pdf#page=85) uses higher Ext vanishing for a **DNF source** represented as a sequential colimit of compact projectives. This pass has no such representation for the nuclear Fréchet $H$, $K$, or $K_1$. Dualizing that assertion or applying it merely because the word “nuclear” occurs would not be a valid transfer. The degree-one statements of 018/019 likewise supply no such representation for $K$.

## 2. Primary construction: an infinite diagonal on genuine relations of relations

This construction works inside the given evaluated cover; it does not add generators to it.

The original non-singleton plot index includes the zero plot on a two-point extremally disconnected set. Its summand

$$
D=\mathcal M_{<p}(\{0,1\})\cong\underline{\mathbb R}^2
\quad\subset P_{\mathrm{red}}
$$

is killed by $\varepsilon$, and hence lies in $K$. Choose a nonzero coordinate vector, viewed as a liquid map $v:\underline{\mathbb R}\to K$. The composition $iv$ is nonzero. This uses a retained non-singleton summand; the Hamel-singleton reduction of 037 does not remove it.

Choose any nonempty extremally disconnected $S_0$ in the fixed generating family used by 067 and put $L=\mathcal M_{<p}(S_0)$. Choose a point of $S_0$. The collapse and that point give actual liquid maps

$$
m:L\longrightarrow\underline{\mathbb R},\qquad
\delta:\underline{\mathbb R}\longrightarrow L,\qquad m\delta=1.
$$

For every integer $n\ge1$ the morphism

$$
r_n=n\,ivm:L\longrightarrow P_{\mathrm{red}}
\tag{85.3}
$$

is a relation in (67.2). They are distinct, since $iv\ne0$ and $m\delta=1$. Let $t_n:L\to P_1$ denote the corresponding, already present, coproduct summand. Its defining equation is

$$
qt_n=n\,vm.
$$

For $n\ge2$, the morphism $t_n\delta-n t_1\delta$ is annihilated by $q$. It therefore factors uniquely through a liquid map $z_n:\underline{\mathbb R}\to K_1$ with

$$
jz_n=t_n\delta-n t_1\delta.
\tag{85.4}
$$

Fix $0\ne h\in s$ and let $h_n:\underline{\mathbb R}\to B_n$ send $1$ to $h$. Define a single liquid morphism $\Psi:P_1\to E$ by its restrictions to the coproduct summands:

$$
\Psi t_n=\iota_n h_n m\quad(n\ge2),\qquad
\Psi t_1=0,
\qquad
\Psi=0\text{ on every other summand}.
\tag{85.5}
$$

The coproduct universal property makes this a morphism in $\mathcal A_p$, with no convergence or countable-sum topology assumption. Define

$$
f_0=\Psi j:K_1\longrightarrow E.
\tag{85.6}
$$

Its values on the actual maps (85.4) are

$$
f_0z_n=\iota_n h_n\ne0\quad(n\ge2).
\tag{85.7}
$$

Thus $f_0$ factors through no finite $E_N$. Consequently $\chi^{-1}f_0$ factors through no actual $G_b$: any such factorization would, by the admitted factorization of $G_b\to E$, contradict (85.7).

There is also an actual split projective subobject behind this diagonal. Put $Z=\bigoplus_{n\ge2}\underline{\mathbb R}$. The $z_n$ assemble to $z:Z\to K_1$. Define $\lambda:P_1\to Z$ on $t_n$ for $n\ge2$ by the mass map $m$ into coordinate $n$, and define it to be zero on $t_1$ and all other summands. Then

$$
\lambda jz=1_Z.
\tag{85.8}
$$

So the constructed support escape is carried entirely by a genuine projective retract of $K_1$ whose retraction extends to $P_1$.

**Hostile boundary verdict.** The proposed counterexample fails exactly, without a finite approximation: (85.6) already exhibits the allowed boundary. In (67.14) take any $b$, take $f_b=0$, and take $\psi=\chi^{-1}\Psi$. Its class in $\mathrm{Ext}^2(H,G)$ is zero. Every output coordinate in (85.7) is nonzero as a map but zero as an Ext class. Neither singleton reduction nor escape of all support stages changes that verdict.

## 3. One correction pass: replace pointwise support escape by a quotient ghost

The correction attempts to force a phantom class using the actual liquid quotient

$$
0\longrightarrow E\overset{\iota}{\longrightarrow}
P=\prod_{n\ge1}B_n\overset{\pi}{\longrightarrow}Q\longrightarrow0.
\tag{85.9}
$$

The quotient in (85.9) is categorical in $\mathcal A_p$. It is not replaced by the ordinary algebraic quotient of point sets or a chosen non-Hausdorff vector-space topology.

Let $S_\infty=\mathbb N\cup\{\infty\}$ be the profinite convergent sequence, and define the continuous plot

$$
u:S_\infty\longrightarrow\prod_n s,
\qquad u(n)=\iota_n h,\qquad u(\infty)=0.
\tag{85.10}
$$

Continuity is coordinatewise. Its image $\overline u\in Q(S_\infty)$ is nonzero: otherwise exactness at $P(S_\infty)$ would place $u$ in $E(S_\infty)$, whereas the admitted strict-LF realization would then put the entire plot in one $E_N$, contradicting (85.10). Nevertheless $\overline u$ restricts to zero on every singleton, since each $u(n)$ belongs to one finite summand. This is a genuine sectionwise ghost.

There is a continuous surjection $\tau:\beta\mathbb N\to S_\infty$ sending $n$ to $n$ and the remainder to $\infty$. The space $\beta\mathbb N$ is extremally disconnected and has weight at most $2^{\aleph_0}$. Hence, up to the fixed representative in 016, the original cover contains its zero-plot summand

$$
J=\mathcal M_{<p}(\beta\mathbb N)\subset P_{\mathrm{red}}.
$$

Because its plot is zero in $H$, its inclusion factors through $s_J:J\to K$. Projection onto that summand restricts to $e_J:K\to J$, with $e_Js_J=1_J$. No new summand is adjoined to the exact cover.

The plot $u\tau$ extends by the free-liquid universal property to $\widehat u:J\to P$. Its image $\pi\widehat u$ is nonzero: the restriction map $Q(S_\infty)\to Q(\beta\mathbb N)$ is injective by the sheaf axiom for the surjection $\tau$, and $\overline u\ne0$. We have therefore constructed an actual nonzero liquid morphism

$$
h_K=(\pi\widehat u)e_J:K\longrightarrow Q.
\tag{85.11}
$$

**Correction failure: the ghost has a global product lift.** The explicit lift is

$$
g_K=\widehat u e_J:K\longrightarrow P,\qquad \pi g_K=h_K.
\tag{85.12}
$$

To test the degree-two class in the actual evaluated resolution, choose any lift $a:P_1\to P$ of $h_Kq$; such a lift exists by projectivity of $P_1$. Since $\pi a j=0$, there is a unique $f_a:K_1\to E$ with $\iota f_a=aj$. Equations (85.11)–(85.12) give

$$
\pi(a-g_Kq)=0.
$$

Consequently $a-g_Kq=\iota\psi$ for an actual liquid $\psi:P_1\to E$, and

$$
\iota f_a=aj=(a-g_Kq)j=\iota\psi j,
\qquad f_a=\psi j.
\tag{85.13}
$$

This excludes a nonzero phantom class for **every** choice of projective lift $a$, not just the convenient lift $g_Kq$. For example $a=g_Kq+\iota\Psi$ gives exactly the support-escaping map $f_0$ of section 2. The correction produces a nonzero ghost on $K$ but no nonzero cohomology class.

More generally, any $K\to Q$ factoring through a projective retract of $K$ lifts to $P$, since (85.9) is epic and the retract is projective. Thus merely replacing the zero-plot summand with a different projective summand cannot repair this attempted mechanism. No further replacement search is undertaken.

## 4. Exact phantom-channel obstruction, including every boundary

For this fixed first cover there is a useful sharpened form of (67.12):

$$
\mathrm{Ph}^2\cong
\frac{\mathrm{Hom}(K,Q)}
{\pi\,\mathrm{Hom}(K,P)}.
\tag{85.14}
$$

Indeed dimension shifting expresses $\mathrm{Ext}^1(H,V)$ as $\mathrm{Hom}(K,V)$ modulo restrictions from $P_{\mathrm{red}}$. In the cokernel of the map from coefficients $P$ to coefficients $Q$, any additional restriction from $\mathrm{Hom}(P_{\mathrm{red}},Q)$ already belongs to $\pi\mathrm{Hom}(K,P)$: projectivity of $P_{\mathrm{red}}$ lifts it through $P\to Q$, and one then restricts the lift to $K$. This proves (85.14) from (67.12) in the actual category.

Equivalently, start with any actual $h:K\to Q$, lift $hq$ to $a:P_1\to P$, and form $f_a$ as in section 3. Then

$$
[f_a]=0\text{ in }\mathrm{Ext}^2(H,E)
\quad\Longleftrightarrow\quad
h\text{ has a liquid-linear lift }K\to P.
\tag{85.15}
$$

The reverse implication is (85.13). For the forward implication, write $f_a=\psi j$. The map $a-\iota\psi$ annihilates $j$ and therefore descends through its cokernel $q$ to $g:K\to P$. The equation $\pi g=h$ follows after precomposition with the epimorphism $q$. This also proves that a different choice of $a$ cannot change the verdict.

Furthermore $[f_a]$ is coordinate-invisible, since $\iota f_a=aj$ makes its image with coefficient $P$ a boundary. By (67.13) and the finite-prefix coordinate retractions, a phantom class cannot be a nonzero finite-stage class. Thus a nonlifting $h$ in (85.15) would violate the full (67.14), including all finite-stage corrections, rather than merely be nonzero in a chosen representative.

**Exact missing step for this channel:** construct an actual $h:K\to Q$ with no liquid-linear lift to $P$. The nonzero section (85.10) and the nonzero morphism (85.11) do not meet that condition. Sectionwise lifting of $P\to Q$ on profinite tests, as proved in 018, neither provides such an $h$ nor proves that every $K\to Q$ lifts: that would need a compatible linear lift on the whole kernel. The attempted $h_K$ has such a lift for the explicit reason (85.12).

## 5. Coordinate-visible channel: realizability and nonvanishing are separate tests

The other channel in (67.13) requires a family of actual liquid maps

$$
\phi_n:K_1\longrightarrow B_n
$$

meeting **both** of the following conditions.

1. For every compact projective generator $L'$ of the fixed family and every actual $w:L'\to K_1$, only finitely many composites $\phi_nw$ are nonzero.
2. For infinitely many $n$, the class of $\phi_n$ in

$$
\frac{\mathrm{Hom}(K_1,B_n)}
{\{\eta j:\eta:P_1\to B_n\}}
\cong\mathrm{Ext}^2(H,B_n)
\tag{85.16}
$$

is nonzero.

Condition 1 is exactly the realizability test for the family to define a morphism $f:K_1\to E$. Necessity follows from compactness of the generators and the coproduct $E$. For sufficiency, form the product map $\overline f:K_1\to P$. For each $w$ its coordinates have finite support, so $\overline f w$ factors through $E$ and $\pi\overline f w=0$. The generators detect zero morphisms, hence $\pi\overline f=0$. The kernel property in (85.9) supplies the unique liquid map $f$.

Condition 2 would control **all** projective boundaries: if $f=f_N+\psi j$ with $f_N$ valued in $E_N$, projection to any $n>N$ would give $\phi_n=(\mathrm{pr}_n\psi)j$, contradicting the infinitely many nonzero classes in (85.16). By the admitted two-way stage factorization, this also excludes all original $G_b$ corrections.

The primary construction satisfies Condition 1 but fails Condition 2 in every coordinate:

$$
\phi_n=\mathrm{pr}_n\Psi j,
\qquad [\phi_n]=0\quad\text{for every }n.
\tag{85.17}
$$

The ghost correction produces the same failure by (85.13). Choosing independently nonzero classes in (85.16), even if such choices were available, would not prove Condition 1. They could define only a product-valued cocycle. Multiplying coordinates by nonzero rapidly decreasing scalars does not fix that problem: Condition 1 requires eventual **exact zero** on each relation plot, and nonzero scalar multiplication preserves whether a composite vanishes. Thus convergence in the product cannot replace realizability in the admitted strict-LF coproduct.

**Exact missing step for this channel:** exhibit an infinite family satisfying Conditions 1 and 2 simultaneously. This attempt proves no nonzero member of (85.16), and supplies no coherent family of them with the required plotwise finite support. Known or conditional first-Ext information for scalar coefficients has the wrong degree and does not provide that family. No CH/OCA hypothesis, independence assertion, or scalar-to-degree-two transfer is made.

## 6. Bounded disposition and replay

The substantive constructed objects are the exact relation maps (85.3), the actual relations of relations (85.4), the unbounded liquid cocycle (85.6), and the nonzero quotient ghost (85.11). Their decisive hostile tests are the explicit global boundary (85.5) and the explicit global product lift (85.12), with the all-lifts calculation (85.13). These are categorical calculations for the original infinite objects, not finite-dimensional fixtures.

The result is therefore an unsuccessful negative attempt, not a negative theorem about possible future constructions. The one correction pass is exhausted. Original degree-two surjectivity remains open; so does existence of a counterexample. There is no basis here for a feasibility verdict, an impossibility verdict, or completion of R3/R4/REACH.

Validation uses Windows, not WSL, and the existing isolated evidence environment at `F:\_codex\MATH\_evidence\reach-completion-20261027\.venv\Scripts\python.exe`. The expected runtime is CPython 3.12.12. There is no admitted `uv.lock` for this evidence environment, so it is **not pinned**. No package installation, dependency resolution, or lockfile change is needed. The validation process explicitly sets owner-private external caches:

```powershell
$env:UV_CACHE_DIR = 'C:\Users\jamie\AppData\Local\GCL\uv'
$env:PYTHONPYCACHEPREFIX = 'C:\Users\jamie\AppData\Local\GCL\PythonBytecodeCache'
& 'F:\_codex\MATH\_evidence\reach-completion-20261027\.venv\Scripts\python.exe' --version
& 'F:\_codex\MATH\_evidence\reach-completion-20261027\.venv\Scripts\python.exe' ci/math_markdown_gate.py --file research/condensed-qft/EXT-015/R3_COUNTEREXAMPLE_ATTEMPT_085.md
git diff --check -- research/condensed-qft/EXT-015/R3_COUNTEREXAMPLE_ATTEMPT_085.md
git hash-object research/condensed-qft/EXT-015/R3_COUNTEREXAMPLE_ATTEMPT_085.md
```

Run from `F:\_codex\MATH\_worktrees\reach-reassessment-20261027`. Execution on 2026-10-27 reported CPython 3.12.12; the mathematical Markdown source gate passed, and the path-scoped `git diff --check` passed. The working copies of all eight source artifacts in the custody table matched their listed frozen blobs. The source preflight checks mathematical delimiter structure, not the arguments or a live browser paint. The final non-self-referential blob identity is returned to the parent separately. No finite fixture is added because the decisive issue is the existence of a nonlifting morphism or a simultaneously realizable nonzero Ext family, and no finite-rank calculation can establish either.
