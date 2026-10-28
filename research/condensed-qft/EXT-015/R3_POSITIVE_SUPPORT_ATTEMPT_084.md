# EXT-015 REACH-R3 / 084 — positive support normalization attempt

**Result: incomplete.** This is one positive construction, followed by one correction pass. It reduces the original degree-two question to an explicit first-cocycle normalization for the actual rapid-weight quotient systems. It supplies local acyclicity proofs and a chain-comparison recipe back to the actual evaluated cover of 067. The quotient-cocycle normalization remains unproved. Consequently this note produces neither a solution of (67.14) for every cocycle nor a counterexample. Original R3 remains open.

The opposing attempt 085 and other future attempt drafts were not read. No argument was requested from another agent. Fresh-context scrutiny within one Codex system is not external mathematical certification.

## 1. Exact inputs and fixed objects

The audited source cut is `afb5a6873562a9050b8a1fb65dee42f399db9967`; the original protected mathematical cut is `9cc483334648d94ea6226a76874151a3eabd33b1`. The files below were read at the audited cut. Their Git blob identities are part of the mathematical data, not a claim of a new protected admission.

| Source | Git blob |
| --- | --- |
| [018, rapid-weight presentation](FIXED_SOURCE_WEIGHT_LOCALIZATION_018.md) | `a6c5670d10d35a7acc761f60c6273c2034cc82a3` |
| [019, degree-one support theorem](FIXED_SOURCE_EXT1_ISOMORPHISM_019.md) | `6b0fb373b8bde1434b3b443f16274c626e0d954c` |
| [037, actual singleton splitting](R3_ALL_SINGLETON_LINEAR_RELATIONS_037.md) | `68b92dfca0bdd51707f409ff79f2770a310fc4e0` |
| [067, actual evaluated relation cover](R3_EVALUATED_RELATION_COVER_067.md) | `7069938ce1e75f946e2f4ff70fcabb2f073065e9` |
| [081, bounded reassessment protocol](REACH_REASSESSMENT_081.md) | `128ad967100e73f6ea91581a7835f6809daebaee` |
| [082, completed fresh audit](REASSESSMENT_FRESH_AUDIT_082.md) | `b596a671ec62ec1dfed4343a834d5ac7343e19cb` |

Work throughout in $\mathcal A_p=\mathrm{Liq}_p(\mathbb R)$ for fixed $0<p\le1$, in the same small condensed universe as 067. Retain exactly

$$
H=\underline{\mathcal D_{[-1,1]}(\mathbb R)},\qquad
G_b=\underline{\mathcal D_{[-b,b]}(\mathbb R)},\qquad
G=\varinjlim_bG_b.
\tag{84.1}
$$

In particular, $K$ and $K_1$ below are liquid kernels, with no assigned Fréchet topology. The source presentation and the real strict-LF realization are the explicit hypotheses retained by 018/019 and the audit:

$$
H\simeq\underline s\simeq\varinjlim_{r\in\mathscr R}T_r,
\qquad
T_r=r\mathcal M_{<p}(\mathbb N),
\qquad
G\simeq E=\bigoplus_{n\ge1}B_n,
\quad B_n=\underline s.
\tag{84.2}
$$

The poset $\mathscr R$ is countably directed; its arrows are the actual scaled-measure inclusions. Each $T_r$ is isomorphic to the retract $\mathcal M_{<p}(\mathbb N)$ of $\mathcal M_{<p}(S_\infty)$, where $S_\infty=\mathbb N\cup\{\infty\}$. This retract uses the collapse to $*$ and its section at $\infty$. It does not make $S_\infty$ extremally disconnected or its free liquid module projective.

The isomorphism to $E$ is used only as a coefficient isomorphism. Finite prefixes $E_N=\bigoplus_{n\le N}B_n$ and actual $G_b$ factor through one another as in 067. Thus a finite-prefix result returns to some actual support stage. The primary [Taroyan source](https://mathoverflow.net/questions/510488/operatornameext1s-mathbb-r-in-the-category-of-liquid-vector-spaces/514158) was inspected for the weight presentation and countable-direction calculation. Its separate assertion of projectivity for arbitrary profinite measure objects is not used, nor is its CH-dependent scalar conclusion.

Write the exact sequences from 067 as

$$
0\longrightarrow K\overset{i}{\longrightarrow}P_{\mathrm{red}}
\longrightarrow H\longrightarrow0,
\qquad
0\longrightarrow K_1\overset{j}{\longrightarrow}P_1
\overset{q}{\longrightarrow}K\longrightarrow0.
\tag{84.3}
$$

Here $P_{\mathrm{red}}$ retains the Hamel-basis singleton coproduct and every original nonsingleton profinite summand; $P_1$ is the evaluated sum over all actual relation plots (67.2). No cover is replaced by a topological surrogate. For an arbitrary actual $f:K_1\to E$, the desired construction is

$$
f=\iota_Nf_N+\psi j,
\qquad f_N:K_1\to E_N,\quad\psi:P_1\to E.
\tag{84.4}
$$

## 2. Local step: controlled primitives at the actual weight stages

The local statement needed by this attempt is stronger than the degree-one argument of 019:

$$
\mathrm{Ext}^m(T_r,B_n)=0,
\qquad
\mathrm{Ext}^m(T_r,E)=0
\quad(r\in\mathscr R,\ n\ge1,\ m>0).
\tag{84.5}
$$

Here is a proof with the extra analytic input made explicit. In the stable May 2026 version of Scholze's [Lectures on Analytic Geometry](https://people.mpim-bonn.mpg.de/scholze/Analytic.pdf), Theorem 6.5(2)–(3), printed p. 35, gives derived full faithfulness and the derived free-measure identity. Proposition 10.1 and its following real-base-change paragraph, printed p. 69, explicitly identify the derived liquidification of $\mathbb R[S]$ with $\mathcal M_{<p}(S)$ in degree zero, also for compact Hausdorff $S$. These statements imply, for any profinite $S$ and liquid coefficient $V$,

$$
R\mathrm{Hom}_{\mathcal A_p}(\mathcal M_{<p}(S),V)
\simeq R\Gamma(S,V).
\tag{84.6}
$$

Equivalently, apply Theorem 6.5(3) for every $p'<p$ and pass from $\mathcal M_{p'}(S)$ to their filtered colimit. The compatible derived Hom diagrams on the right are constant. This is derived liquidification, not an unsupported application of an ordinary left adjoint to an exact complex.

For clarity, an actual liquid resolution computing (84.6) can be chosen as follows. Choose an extremally disconnected profinite hypercover $S_\bullet\to S$, by taking an extremally disconnected cover of each finite matching object and retaining degeneracies. Matching objects are compact profinite. Every level can therefore be compact profinite and extremally disconnected. The augmented free-sheaf complex is a resolution by hypercover acyclicity; see [Stacks, Section 25.4](https://stacks.math.columbia.edu/tag/01GA). Apply derived liquidification. Its terms are $\mathcal M_{<p}(S_k)$, compact projective by Theorem 6.5, and its augmentation is $\mathcal M_{<p}(S)$ by the identity just cited. Thus

$$
\cdots\longrightarrow\mathcal M_{<p}(S_2)
\longrightarrow\mathcal M_{<p}(S_1)
\longrightarrow\mathcal M_{<p}(S_0)
\longrightarrow\mathcal M_{<p}(S)\longrightarrow0
\tag{84.7}
$$

is an actual projective resolution in $\mathcal A_p$. Normalization, if used, replaces its terms by projective direct summands. The alternating face maps give the differential. Applying Hom into $V$ gives the cochain complex $V(S_k)$.

**Controlled scalar primitive.** Scholze's Proposition 8.19, printed p. 54, applies to any profinite hypercover and a complete normed module. Its last assertion supplies primitives with supremum norm at most $(1+\epsilon)$ times the cocycle norm, in every positive cochain degree. For the present application take the complete normed real line and let the formal variable $T$ act by multiplication by a fixed $0<\lambda<1$. It is a module over $\mathbb Z[T^{\pm1}]$ whose norm scales by $\lambda$ under $T$, as required in that proposition. Taking $\epsilon=1$ gives, for every scalar cocycle $z\in\mathrm{Cont}(S_m,\mathbb R)$ with $m>0$, a continuous $y:S_{m-1}\to\mathbb R$ such that

$$
dy=z,\qquad \|y\|_\infty\le2\|z\|_\infty.
\tag{84.8}
$$

**Rapid-coordinate primitive.** Let $z:S_m\to s$ be a continuous cocycle and write its scalar coordinates as $z_k$. Compactness of $S_m$ gives

$$
\sup_{t\in S_m,\ k\ge1}(1+k)^a|z_k(t)|<\infty
\qquad(a\ge0).
\tag{84.9}
$$

Apply (84.8) separately to each $z_k$, obtaining $y_k$ with the same constant $2$. The family $y=(y_k)$ takes values in $s$. It is continuous into its Fréchet topology: in seminorm $a$, its finite-coordinate truncations converge uniformly because their tails are bounded by $2/(1+N)$ times the bound (84.9) for $a+1$. Coordinate continuity plus this uniform convergence proves continuity. Its differential is $z$ coordinatewise. This proves $H^m(S,\underline s)=0$ for every $m>0$ using the actual resolution (84.7).

**Strict-LF primitive without support growth.** If $z\in E(S_m)$ is a cocycle, the admitted strict-LF realization and compactness of $S_m$ put its entire plot in one $E_N$. Its differential already vanishes there because $E_N\to E$ is monic. Apply the preceding argument in each of the finitely many $s$ summands. It gives a primitive in the same $E_N$. Thus $H^m(S,E)=0$ for $m>0$. Equation (84.6), followed by the retract for $T_r$, proves (84.5). The same proof or exact products gives acyclicity against $P=\prod_nB_n$; the coefficient exact sequence then gives it against $Q=P/E$.

No global Ext vanishing follows: these assertions concern free modules on compact profinite sets and their specified retracts, not $H$, $K$, or $K_1$. In particular they do not identify any liquid syzygy with $s$.

## 3. Normalize the original cocycle into one explicit higher-limit problem

Set

$$
V_{r,n}=\mathrm{Hom}_{\mathcal A_p}(T_r,B_n)
\subseteq W_n=s^{\mathbb N},\qquad
V_r=\bigoplus_nV_{r,n},\qquad W=\bigoplus_nW_n.
\tag{84.10}
$$

The common-coordinate embedding and its injectivity are exactly those of 018: compose with continuous scalar functionals on $s$ and use the weighted $c_0$ scalar description. Transition maps are inclusions $V_{s,n}\subseteq V_{r,n}$ when $r\preceq s$. Ordinary Hom into $E$ is $V_r$ by compact-plot factorization and the retract above.

Choose functorial evaluated-generator projective resolutions $L_{r,\bullet}\to T_r$. Their simplicial replacement has projective terms

$$
D_{a,b}=\bigoplus_{r_0\preceq\cdots\preceq r_a}L_{r_0,b}.
\tag{84.11}
$$

Its total complex $D_\bullet$ resolves the actual filtered colimit $H$; filtered colimits are exact here, as checked on the compact projective generators. The horizontal differential is the source bar differential; the vertical one is the resolution differential with the usual total sign. On applying Hom into $E$, write

$$
C^{a,b}=\prod_{r_0\preceq\cdots\preceq r_a}
\mathrm{Hom}(L_{r_0,b},E),\qquad
D=\delta+(-1)^a d.
\tag{84.12}
$$

For an inverse-system cochain $x$, the first Roos differential is

$$
(\delta x)_{r,s}=x_s|_{T_r}-x_r,
\qquad
(\delta x)_{r,s,t}=x_{s,t}|_{T_r}-x_{r,t}+x_{r,s}.
\tag{84.13}
$$

A total degree-two cocycle is a triple $(a,b,c)$ of bidegrees $(0,2),(1,1),(2,0)$ with

$$
da=0,\qquad \delta a-db=0,\qquad
\delta b+dc=0,\qquad\delta c=0.
\tag{84.14}
$$

A degree-one cochain $(u,v)$ changes it by the actual boundary

$$
D(u,v)=(du,\ \delta u-dv,\ \delta v).
\tag{84.15}
$$

Using (84.5), choose $u$ with $du=a$. Then $b'=b-\delta u$ satisfies $db'=0$. Choose $w$ with $dw=b'$ and subtract $D(0,-w)$. The resulting triple is $(0,0,c+\delta w)$, with its last component in $\prod_{r\preceq s\preceq t}V_r$. Products of real vector spaces are exact, so these choices can be made componentwise. We have thereby constructed the source-specific isomorphisms

$$
\mathrm{Ext}^m(H,E)\simeq\varprojlim_r{}^m V_r,
\qquad
\mathrm{Ext}^m(H,B_n)\simeq\varprojlim_r{}^mV_{r,n}.
\tag{84.16}
$$

This normalization does not control the support of $u$ or $w$ uniformly over all weights and strings. No such assertion is needed to obtain (84.16).

**The attempted final step.** For a normalized $c\in C^2(V)$, choose $a\in C^1(W)$ with $\delta a=c$. This is possible because the constant inverse system $W$ has no positive derived limits over the nonempty directed poset. Put

$$
X_{r,n}=W_n/V_{r,n},\qquad X_r=\bigoplus_nX_{r,n},
\qquad \alpha_{r,s}=a_{r,s}\bmod V_r.
\tag{84.17}
$$

Then

$$
\alpha_{r,t}=\alpha_{r,s}+\alpha_{s,t}|_r.
\tag{84.18}
$$

To finish the positive construction one needs a finite set $F\subseteq\mathbb N$ and $\beta_r\in X_r$, finite-supported separately for each $r$, such that

$$
\alpha_{r,s}-(\beta_s|_r-\beta_r)
\in\bigoplus_{n\in F}X_{r,n}
\qquad\text{for every }r\preceq s.
\tag{84.19}
$$

This is the **exact unresolved inference of the attempt**, for the specific weighted Hom subspaces with values in $s$ in (84.10). It is not supplied by the existing degree-one theorem. Indeed the constant-system exact sequences give

$$
\varprojlim{}^2V\simeq\varprojlim{}^1X,
\qquad
\varprojlim{}^2V_{\bullet,n}\simeq\varprojlim{}^1X_{\bullet,n}.
\tag{84.20}
$$

Lemma 18.1 controls $\varprojlim{}^1V$ because $V$ consists of nested subspaces of a constant space. It does not control $\varprojlim{}^1X$: these are quotient systems with surjective transition maps, and they have not been embedded as the requisite nested subspaces. Substituting $X$ for $V$ in that lemma would discard its central hypothesis.

If (84.19) were proved, choose finite-coordinate lifts $\widetilde\beta_r\in W$ and set $a'=a-\delta\widetilde\beta$. The tail $a'_{F^c}$ is then a legitimate 1-cochain with values in $V$, and $c-\delta a'_{F^c}$ has coefficients in $\bigoplus_{n\in F}V_{r,n}$. This is the desired finite-coordinate degree-two class. This paragraph is a proved implication, not an assertion that the required $\beta$ has been constructed.

## 4. Return a successful normalization to the actual equation (67.14)

Here are the maps needed to avoid replacing the actual cocycle by a different source problem. Extend the fixed resolution (84.3) by an actual projective epimorphism $\pi_2:P_2\twoheadrightarrow K_1$ and continue it. Call the resulting resolution $R_\bullet$, with $R_0=P_{\mathrm{red}}$, $R_1=P_1$ and $d_2=j\pi_2$. The original cocycle is precisely

$$
\widehat f=f\pi_2:P_2\to E,
\qquad \widehat f d_3=0,
\qquad \text{boundaries are }\psi d_2.
\tag{84.21}
$$

Choose comparison chain maps $u:D_\bullet\to R_\bullet$ and $v:R_\bullet\to D_\bullet$ over $H$. Projectivity constructs these by successive lifting. Choose a chain homotopy $h$ with $uv-1=dh+hd$. Normalize the pulled-back cocycle $\widehat f u_2$ by (84.14)–(84.17). If (84.19) supplied a finite-prefix cocycle $\zeta:D_2\to E_N$ and degree-one cochain $\eta:D_1\to E$ satisfying

$$
\widehat f u_2-\iota_N\zeta=\eta d^D_2,
\tag{84.22}
$$

then $\zeta v_2$ kills $\mathrm{im}(d_3)=\ker\pi_2$ and therefore factors uniquely as $f_N\pi_2$ for $f_N:K_1\to E_N$. Direct substitution gives

$$
\widehat f-\iota_N f_N\pi_2
=(\eta v_1-\widehat f h_1)d_2.
\tag{84.23}
$$

Since $\pi_2$ is epic, (84.4) follows with $\psi=\eta v_1-\widehat f h_1$. Finally factor $E_N\to G$ through an actual $G_b$ and transport $f_N$. This is the precise conditional recipe for $b,f_b,\psi$ in (67.14). Its missing input is (84.19), not an unnamed comparison or an assumed Fréchet property of $K_1$.

## 5. Both residual channels, in the same construction

By the local acyclicity in Section 2 and the exact target coefficient sequence, put

$$
Y_r=\prod_nV_{r,n},\qquad U_r=Y_r/V_r
=\mathrm{Hom}(T_r,Q).
\tag{84.24}
$$

The equality on the right uses actual surjectivity $\mathrm{Hom}(T_r,P)\to\mathrm{Hom}(T_r,Q)$, since $\mathrm{Ext}^1(T_r,E)=0$. Thus (67.12) becomes

$$
\mathrm{Ph}^2\simeq
\mathrm{coker}\left[\varprojlim{}^1Y_r
\longrightarrow\varprojlim{}^1U_r\right],
\tag{84.25}
$$

and its infinitely coordinate-visible residual is

$$
\frac{\mathrm{im}\left[\varprojlim{}^2V_r
\longrightarrow\prod_n\varprojlim{}^2V_{r,n}\right]}
{\bigoplus_n\varprojlim{}^2V_{r,n}}.
\tag{84.26}
$$

Normalization (84.19) would kill both: it would make every global class finite-coordinate, and coordinate retractions make a finite-coordinate phantom zero. Conversely, local lifting at every $T_r$ proves neither the surjectivity in (84.25) nor finite support in (84.26). All degree-two classes in (84.16) restrict to zero at every $T_r$ by (84.5), including any possibly nonzero coordinate classes. Thus the degree-one technique of choosing a stage where each nonzero coordinate remains nonzero has no such witnesses here.

There is also an exact description directly in the fixed cover. If $[f]$ is a phantom, choose $\psi_n:P_1\to B_n$ with $f_n=\psi_nj$. Their product is $\Psi:P_1\to P$ with $\Psi j=\iota f$. Consequently $\pi\Psi$ descends to an actual $h:K\to Q$. If $h$ lifts to $\ell:K\to P$, then $\Psi-\ell q$ lands in $E$ and its restriction to $K_1$ is $f$. It is the required boundary. The failure to construct such a lift for every actual $h$ is precisely the phantom compatibility issue. Projectivity of $P_1$ gives the individual coordinate primitives, not a compatible liquid-linear lift out of $K$.

For the visible channel, proving that the tail coordinate classes vanish would first give a product-valued primitive on $P_1$ for that tail. Its defect would again descend to $K\to Q$ and require the same lifting step. This is why killing one channel alone cannot finish (67.14).

## 6. One correction pass and hostile controls

The primary construction attempted to diagonalize the supports of the quotient 1-cocycle $\alpha$. The correction pass retains the local proofs but rejects the inference that countable direction alone makes this diagonalization work.

1. **Compatible sections versus coherent cochains.** Lemma 18.1 bounds supports of a compatible 0-family. Equation (84.18) allows cancellations among three different values. A common upper bound for countably many indices does not turn those values into a single representative with all selected coordinates nonzero.
2. **Explicit cancellation control in ZFC.** On the countably directed ordinal $\omega_1$, use the constant inverse system $A=\bigoplus_{n\ge0}\mathbb R e_n$. Write each ordinal uniquely as $\omega\gamma+m$ with $m<\omega$ and set $\beta_\alpha=e_m$. Then $\alpha_{\mu,\nu}=\beta_\nu-\beta_\mu$ is a 1-cocycle whose union of coordinate supports is infinite. At the common upper bound $\omega$ of the finite ordinals, $\alpha_{n,\omega}=e_0-e_n$; every value still has finite support. This cocycle is a boundary. The control refutes bounding a representative's support by this diagonal argument; it proves neither failure nor success of (84.19).
3. **Actual support-escaping boundary.** The infinite projective-source control in 067 still applies. A map to $E$ can use every coordinate and nevertheless represent zero Ext. Neither the Roos control nor an unbounded choice of the $\psi_n$ above is a negative liquid Ext witness.
4. **No false projectivity or ordinary-adjoint exactness.** The hypercover levels in (84.7) are extremally disconnected. Its augmentation is justified by derived liquidification, not merely preservation of a coequalizer. $S_\infty$ and its measure retract are used only after the coefficient-specific acyclicity proof. The proof of (84.8) is invoked for precisely the complete normed real line, and the rapid-coordinate argument proves the needed continuity for $s$ in every positive degree.
5. **No sum/product exchange hidden in normalization.** Roos cochains are products over weight strings of direct sums over output coordinates. A cochain can have an unbounded union of output supports across those strings. This product is not replaced by a direct sum of Roos complexes. Equations (84.19)–(84.20) name the missing exchange modulo boundaries explicitly.
6. **Literature control.** [Bannister–Bergfalk–Moore–Todorcevic, Theorem 8.4](https://ems.press/content/serial-article-files/51446), printed pp. 5026–5027, proves derived-limit additivity under a specific partition/cofinality hypothesis. That hypothesis concerns products of the coordinate posets and a cofinal-map homogeneity property. No such property has been proved here for the actual weighted Hom systems with values in $s$. This theorem is a control against asserting unconditional additivity, not a theorem that our normalization is independent or false. No CH, OCA, forcing axiom or independence claim is assumed.

No new approach was started after this correction. The outcome is a positive reduction with one precise remaining normalization, not a positive R3 verdict.

## 7. Replay, environment and final boundary

The work was written on CHAD in Windows PowerShell. No fixture was added: the missing normalization quantifies over the entire actual weight poset, so a finite linear-algebra model cannot establish it. The existing 067 fixture is retained as a control for actual relation/boundary typing and finite presentation comparison.

Validation on 2026-10-27 used the isolated evidence interpreter `F:\_codex\MATH\_evidence\reach-completion-20261027\.venv\Scripts\python.exe`. Readback reported CPython 3.12.12, its distinct virtual-environment prefix, and base prefix `C:\Users\jamie\AppData\Roaming\uv\python\cpython-3.12-windows-x86_64-none`. The spawned process explicitly set `UV_CACHE_DIR=C:\Users\jamie\AppData\Local\GCL\uv` and `PYTHONPYCACHEPREFIX=C:\Users\jamie\AppData\Local\GCL\PythonBytecodeCache`. Readback found neither a root `uv.lock` nor root `pyproject.toml`; the evidence environment is **unpinned**. No dependency installation, lock resolution, system-Python shortcut or hosted compute was used.

- `fixtures/check_evaluated_relation_cover_067.py`, unchanged Git blob `7d77ae56a6655b82cbc8357a68903037ce6d3bac`: PASS, including 81 projective-generator lifts, relation kernels, comparison modulo boundaries, coefficient retractions and support-escaping boundaries. These are its finite controls only.
- `ci/math_markdown_gate.py --file research/condensed-qft/EXT-015/R3_POSITIVE_SUPPORT_ATTEMPT_084.md`, gate Git blob `71356dcb861bb2eb4fb7cb93ee3075f787e2c065`: PASS after correcting five delimiter/prose adjacency defects. This was an editorial correction, not a new mathematical approach.
- `git diff --check`: PASS. The source gate was repeated after adding this replay record; the final artifact blob is returned separately to avoid a self-referential hash.

**Final mathematical boundary:** candidate proofs of the controlled local primitive statement (84.5), the actual-cover chain recipe (84.21)–(84.23), and the reduction to (84.19) are supplied for separate scrutiny. These additions were not part of the frozen 082 audit. A proof of (84.19) for the specific systems (84.10), or a genuine actual liquid obstruction surviving every boundary, is still absent. Neither original degree-two surjectivity nor its failure is established. This note does not change trackers, checkpoints, protected state or claim authority.
