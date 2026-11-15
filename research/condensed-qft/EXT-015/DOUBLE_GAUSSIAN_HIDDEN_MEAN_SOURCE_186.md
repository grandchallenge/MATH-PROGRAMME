# EXT-015 REACH / 186 — two independent hidden Gaussian edges, effective-mean cones, and source typing

**Primary disposition: AN EXACT LEGAL DOUBLE-BRIDGE REDUCTION, AN EFFECTIVE-CONE COUNTEREXAMPLE, AND A CONDITIONAL MODULO-RAPID NEGATIVE THEOREM.** Two genuine Gaussian edges ending at the same retained output coordinate admit an exact Gaussian product/mean-coordinate factorization, with no arbitrary upstream heat inverse. Original permitted R1 inputs can produce an **effective forbidden diagonal conormal** after forgetting distinct hidden vertices; this destroys an unqualified use of the effective-R1 hypothesis in protected 180/183. The exhibited effective-conormal contribution is regulator-flat in a fixed rapid stage. Conversely, if the remaining scalar multiplier and original R1 coefficient are graph-regular through zero, the entire double-bridge class cannot represent the first anchored Green core even modulo the existing uniform rapid ideal. No conclusion is made about arbitrary 105 scalar stages with singular zero-scale profiles, partition jets, or universal 150.L.

## 1. Exact source contract and new question

The original sources are 105 Gaussian/Wick scalar heat normal form (Git blob a8ce66ff0edec33e2aff299550fca2089d671033), 108 finite completed mixed histories, fixed cone, rapid ideal and legal maps (587c15fd6e24f6e6b14de574ff878221cdbd5cb6), 126 source-controlled parameter rows (5b05c6147d237ca1d22e4dcbce9262b0f038c163), 165 joint Green core (24b82716d41d309438fcb7a97bbacab0b724afde), 174 single hidden bridge (7c470ba092d917dc434a8883e5afaff7bce1dfc6), 180 compact Gaussian-width independence (fac58764ac29e518ac522e0451a9c9829e86720b), and 183 polynomial retained-coordinate normal ordering (e1d6473ac075b0e17eb354603b25b94d1208be19). Primary180 was protected in PR3344 at 28d978e788c9a1930a00056a0044ae3f4a124469; critical181 and ledger182 in PR3346 at 68fb8a8adc4e672f2284179e5fdb94426ab30351; primary183 in PR3348 at 2af279aff16578031a8cd41aeb05b6e875a265e9; and the nonterminal checkpoint CP193 in PR3349 at 030344a264a16e8ab465c997981cfb99a281c521. Exact source183 and checkpoint blobs were read back protected main. Logical critical184 and ledger185 are separately pending protected admission in PR3350 at the time of this source lock.

The unproved first Green core is

$$
A_\epsilon(x,z)=f(x)\rho(z)\kappa_\epsilon(z),\qquad
f(x)=\chi(x)|x|/2,\qquad
\kappa_\sigma(t)=
\frac{1}{\sqrt{2\pi}\sigma}e^{-t^2/(2\sigma^2)},
\tag{186.1}
$$

with fixed smooth compact $\chi,\rho$, $\chi=1$ near zero and $\rho(0)\ne0$. The 165/168 reductions make this exact source question decisive for the remaining labelled and symmetric primitive. The present target is not another arbitrary terminal factorization: it is the **genuine existing 108.7 subclass with two different hidden endpoints**.

Retain physical output variables $(x,z)$, two forgotten vertices $(y,h)$, and proper compact support. Choose finite positive width ratios $a,b$ and an original compact R1 distribution $T(x,y,h)$ (extended trivially and smoothly in retained $z$), or a family continuously extending in one fixed R1 graph stage when specified. Set

$$
S_\epsilon(x,z)
=\rho(z)\iint
\kappa_{a\epsilon}(z-y)\kappa_{b\epsilon}(z-h)
\,m_\epsilon(x,z,y,h)\,T(x,y,h)\,dy\,dh.
\tag{186.2}
$$

Here the product is understood as the original legal multiplication of smooth positive-regulator scalar factors with the R1 distribution, followed by the proper forgetting map. For the unconditional exact algebraic identity below take $m_\epsilon\equiv1$ on a fixed common support patch; fixed cutoffs can be inserted and retained literally. For the graph-regular rapid theorem, take $m_\epsilon$ smooth in all physical variables and extending to zero with all derivatives on a fixed support, with fixed compatible 126 parameter rows if parameters are used. We do **not** assume arbitrary positive-regulator-smooth multipliers are accepted scalar stages.

The two scalar factors are **actual relative Gaussian edges**, not unproved Gaussian anchoring to an external absolute zero. They are separately admitted by 105.4 and their finite product, positive scale rescalings, fixed cutoffs and proper projection by 105.3–105.6 and 108.7. For every finite $a,b$ this has one fixed scalar face-index stage and one fixed permitted compact R1 cone; it is an explicit finite simple-tensor 108.6 source. All positive-regulator identities retain physical Lebesgue test-pairing densities. Legal original source membership requires this precise construction, not just the right to multiply two arbitrary distributional counterterms.

## 2. Exact two-edge Gaussian factorization

Put

$$
d=\sqrt{a^2+b^2},\qquad
c=\frac{ab}{d},\qquad
\alpha=\frac{a^2}{a^2+b^2},\qquad
\beta=\frac{b^2}{a^2+b^2},
\quad \alpha+\beta=1.
\tag{186.3}
$$

Use the linear hidden-coordinate change

$$
u=\beta y+\alpha h,\qquad
v=y-h,\qquad
y=u+\alpha v,\quad h=u-\beta v.
\tag{186.4}
$$

The absolute value of the physical Jacobian is one. Completing the square gives the **normalized exact identity**

$$
\kappa_{a\epsilon}(z-y)\kappa_{b\epsilon}(z-h)
=\kappa_{c\epsilon}(z-u)\kappa_{d\epsilon}(v)
\quad\text{for every }\epsilon>0.
\tag{186.5}
$$

For $m_\epsilon=1$ define the compact effective distribution

$$
V_\epsilon(x,u)
=\int\kappa_{d\epsilon}(v)\,
T(x,u+\alpha v,u-\beta v)\,dv.
\tag{186.6}
$$

The integral denotes proper distributional pushforward, using the determinant-one coordinate change; the Gaussian multiplier is smooth at every positive regulator and the original $T$ is compact. The exact output is

$$
S_\epsilon(x,z)
=\rho(z)\left[
\kappa_{c\epsilon}*_{u}V_\epsilon
\right](x,z).
\tag{186.7}
$$

For general smooth $m_\epsilon$ depending on retained $z$, its transformed factor remains inside the integral and cannot in general be pulled into an effective $V_\epsilon$ independent of $z$. This is a **real nonterminal output-scalar effect**; (186.7) is not asserted for such a coefficient. However the weak-limit theorem in Section 4 applies to this larger smooth-through-zero scalar subclass.

Equation (186.5) is an exact source-controlled Gaussian identity, not an assertion that an arbitrary compact $V_\epsilon$ is itself an allowed original R1 input. In fact, the next section proves that this would be false.

**Parallel-edge corollary.** If $y=h$ is imposed by an admissible *source-jet insertion*, the product reduces to the single-width $c$ Gaussian times the explicit factor $\kappa_{d\epsilon}(0)=1/(\sqrt{2\pi}d\epsilon)$ and the actual source-jet density. One must retain that density and Laurent shift. A collision inclusion is legal only when its input trace is noncharacteristic under the original R1 cone; this algebra does not authorize an arbitrary delta self-restriction.

## 3. A legal original R1 source with a forbidden effective diagonal cone

The tempting assertion that original R1 on $(x,y,h)$ forces the effective $V_\epsilon(x,u)$ to avoid the conormal of $x=u$ is **false even for a single legal finite double bridge**.

Take $a=b=\sqrt2$, so $c=1$, $d=2$, $\alpha=\beta=1/2$. Choose a compact interval inside the physical open $U$, smooth compact $g(x)\ne0$, and a smooth nonnegative $\psi(v)\not\equiv0$ with

$$
\mathrm{supp}\psi
\Subset\{v:\delta<|v|<2\delta\}
\quad\text{for some }\delta>0,
\tag{186.8}
$$

with $\delta$ small enough that every physical coordinate stays in the original compact patch. Choose fixed cutoffs in $u$ equal to one on $\mathrm{supp}g$. On $(x,u,v)$ define the compact distribution

$$
T(x,u,v)=g(x)\psi(v)\delta(x-u).
\tag{186.9}
$$

Return to the original $(x,y,h)$ coordinates using $u=(y+h)/2$, $v=y-h$. On the singular support $x=u$ and $v\ne0$, the three physical vertex coordinates are **pairwise distinct**:

$$
x=u,\qquad y=u+v/2,\qquad h=u-v/2.
\tag{186.10}
$$

Thus the support of its nonzero wavefront avoids every proper partial-partition equality locus for these three vertices. After extending by a smooth compact retained-coordinate $z$ cutoff, any additional possible partition equality involving $z$ has a conormal with a nonzero $z$ component or requires one of the already absent equalities; the original wavefront has zero $z$ component. Hence the input belongs to a fixed compact permitted R1 normal cone, including the full four-vertex partition test. This is a **legal original R1 input**, not an artificially enlarged source.

Integrating $v$ in (186.6) gives

$$
V_\epsilon(x,u)
=C_\epsilon g(x)\delta(x-u),\qquad
C_\epsilon=\int\kappa_{2\epsilon}(v)\psi(v)\,dv>0.
\tag{186.11}
$$

For every positive regulator the effective input contains a nonzero conormal $(\tau,-\tau)$ to $x=u$ at points with $g(x)\ne0$. This is exactly the conormal forbidden to an original two-vertex R1 input. Nevertheless the complete four-vertex source (186.2) is lawful. Its output is

$$
S_\epsilon(x,z)=\rho(z)C_\epsilon g(x)
\,\kappa_\epsilon(z-x).
\tag{186.12}
$$

Since $\psi$ has a fixed positive separation from $v=0$, every fixed regulator derivative obeys a polynomial-times-Gaussian estimate

$$
|\partial_\epsilon^kC_\epsilon|
\le C_k\epsilon^{-N_k}
\exp(-\delta^2/(8\epsilon^2)).
\tag{186.13}
$$

The harmless numerical exponent is conservative for $d=2$. The spatial and regulator derivatives of the remaining Gaussian have finite inverse powers of $\epsilon$ in every fixed Sobolev or compact test seminorm. Thus the output (186.12) is **uniformly rapid** in one fixed finite spatial negative-order stage for each prescribed regulator derivative: it belongs to the original rapid ideal $\mathcal I^{\mathrm{rap}}$. The forbidden effective conormal survives at every positive $\epsilon$ but has zero class in $\mathcal Z_2$.

**Proposition 186.1.** Original R1-conormal exclusion does **not** automatically descend to the exact positive-regulator effective input of the two-hidden-Gaussian mean map. The counterexample occurs in an actual finite legal 105/108 source. It is regulator-flat and cannot, by itself, represent $A$ or contradict any quotient-level conormal statement. In particular the target-width R1 condition in 180/183 must remain an independently verified hypothesis for a nonidentity mean-map source.

## 4. Bounded no-go for graph-regular double bridges, including modulo rapid

**Theorem 186.2 (regular double-bridge source obstruction).** Consider a finite sum of legal double-hidden-bridge sources (186.2), each with fixed finite Gaussian widths, compact support, the **identity partition** (no nonidentity source-jet inclusion), no additional Wick/Green scalar singularity, only fixed finite physical differential decorations, and a coefficient $m_\epsilon T_\epsilon$ that extends continuously to regulator zero in one fixed original permitted R1 normal graph stage after multiplication by smooth physical multipliers. The scalar $m_\epsilon$ and all its fixed parameter rows extend smoothly through zero on the same physical compact stage, with no negative Laurent pole or other singular heat front factor beyond the **two displayed Gaussian edges**. Then no such finite sum can equal $A$ **even modulo the unchanged original uniform finite-order rapid ideal**.

**Proof.** First work with one source. For every test supported in a compact physical patch, the pair of normalized Gaussian kernels in (186.2) is an approximate identity in the two normal directions $(y-z,h-z)$. The original R1 cone excludes the conormal to $y=h$ and the triple vertex partition, so the trace

$$
\mathrm{Diag}^*T_0(x,z)=T_0(x,z,z)
\tag{186.14}
$$

is a well-defined original noncharacteristic R1 restriction. The fixed normal-graph extension ensures the trace varies continuously with the coefficient. More precisely use (186.4): the graph restriction to $v=0$ exists, and the transformed coefficient is smooth as a distribution-valued function of the normal variable $v$ near zero. Pairing with the normalized $\kappa_{d\epsilon}(v)$ converges to that trace. The remaining $\kappa_{c\epsilon}$ is an ordinary approximate identity in $u$, yielding the weak distribution limit

$$
S_\epsilon\longrightarrow
\rho(z)\,
\bigl[m_0(x,z,z,z)\,T_0(x,z,z)\bigr]
\qquad(\epsilon\downarrow0).
\tag{186.15}
$$

All densities are the physical ones; the determinant-one change of variables and normalized Gaussian masses give no missing constant. If $m_\epsilon$ has retained-coordinate $z$ dependence, keep it inside the integral before passing to the limit; smooth-through-zero bounds give the same (186.15), without needing the exact terminal factorization (186.7).

By the original R1 restriction-cone property in 108 Section 4, the distribution $T_0(x,z,z)$ excludes the nonzero $x=z$ conormal. Multiplication by the smooth $m_0$ and $\rho$ cannot add wavefront directions. Hence the right side of (186.15) has **no nonzero diagonal conormal $(\tau,-\tau)$** at $(0,0)$. This remains true for finite sums and any fixed finite physical derivatives taken within the same graph-regular **identity-partition** class. It does not cover a normal jet inserted by a nonidentity partition map.

On the other hand, the target has weak limit

$$
A_\epsilon\longrightarrow
\rho(0)f(x)\delta_0(z).
\tag{186.16}
$$

Because $\rho(0)\ne0$ and $f(x)=\chi(x)|x|/2$, the tensor-product wavefront of (186.16) at $(x,z)=(0,0)$ contains every nonzero $(\tau,-\tau)$. These two limits cannot agree. Every uniformly rapid difference in the **original fixed-order 108.3 ideal** converges weakly to zero, so the same contradiction excludes equality modulo rapid. This argument only uses the zero-limit map under the *additional stated graph-regularity and smooth-scalar hypotheses*, not the false positive-regulator effective cone preservation refuted by Proposition186.1. $\square$

A rapidly flat coefficient such as (186.11) is compatible with the theorem: its output limit is zero and it creates no nonzero source class despite its forbidden effective conormal at each positive regulator. The graph-regular hypothesis is not asserted for every admissible 105 scalar face stage; for instance a heat-smoothed Green cusp in protected 168 has a nonsmooth zero-scale limit and needs its own scalar source proof. Thus Theorem186.2 does **not** exclude an original history combining a Wick/Green scalar, nonzero negative Laurent orders, or a nonidentity partition source insertion.

## 5. What this changes, and exact next obligation

| Problem | 186 disposition |
| --- | --- |
| Two independent terminal Gaussian edges with distinct hidden endpoints | **ACTUAL legal finite 108.7 histories**, fixed scalar heat stages and proper densities |
| Gaussian product and mean-coordinate transformation | **EXACT** with correctly normalized physical Jacobian |
| Original R1 cone always descends to effective target-width R1 cone | **FALSE**, legal example (186.9)–(186.12) |
| Effective diagonal conormal counterexample survives in the original rapid quotient | **NO**; this particular counterexample is regulator-flat |
| Finite graph-regular identity-partition double bridges with scalar factor smooth through zero | **EXCLUDED for $A$ even modulo rapid** |
| Arbitrary nonpolynomial retained-output scalar stages, negative Laurent/source boundary singularities, nonidentity partition jets | **OPEN** |
| Full original 108.7 $A$ source status, universal 150.L, residual $W$ acyclicity, original R3, full126.14, higher weights, actual lifting, M5/R4 | **OPEN** |

This study supplies a concrete correction to the research attack surface: the source-induced **hidden mean map itself**, even with the identity partition, can produce a forbidden *effective* diagonal conormal. Any general argument must therefore work on the original 108 source and full boundary, not assume a preserved effective cone at every fixed regulator.

**Successor 189 after source-locked critical187 and ledger188:** extend the double-bridge test to a genuine singular scalar stage (the admitted Wick-smoothed Green cusp or another 105 polyhomogeneous stage), and analyze the leading all-corner coefficient and original 126 rows under general hidden-mean and nonidentity partition-jet maps. Either construct one actual complete source of $A$ or establish an invariant across all allowed 108 histories and their uniform rapid classes. The current bounded theorem is not source membership, universal Lemma150.L, residual $W$ cohomology or R3.

A competent adversarial review must check particularly the full four-vertex R1 cone for (186.9), the Gaussian normalization and Jacobian in (186.5), the strict rapid estimate, and the noncharacteristic diagonal trace invoked in Theorem186.2. Code/CI and same-account logical criticism do not constitute external mathematical certification.
