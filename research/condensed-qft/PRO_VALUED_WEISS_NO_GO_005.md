# PRO-001 — A pro-valued Weiss counterexample for completed quantum BV observables

**Disposition:** **Negative theorem** for the naive quantum-weight tower as a pro-valued Weiss cosheaf; **positive narrower result** retained for the tower as a pro-object *in the category of Weiss factorization algebras*. Not a claim of mathematical priority, Lean certification, or a new interacting-QFT result.

**Tracker:** [QFT-COND-004](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2603).  
**Input:** [QW-001: quantum-weight tower](QUANTUM_WEIGHT_PRO_COMPLETION_004.md), [smooth polynomial free-field factorization](COMPACT_SUPPORT_FACTORISATION_003.md).

> **CF-001 successor:** [The completed filtered liquid construction](COMPLETE_FILTERED_LIQUID_WEISS_006.md) passes Weiss descent using weightwise/completed Cech colimits. PRO-1 below remains true for the different pro-category Cech colimit; the full differentiable pro-cochain comparison remains open.

## 1. The missing distinction

Work over the real derived liquid category

$$
\mathcal C_p=D(\mathrm{Liq}_p(\mathbb R)),
\qquad 0<p\le1.
$$

For an open set $U$ let $E_p(U)$ be the compact-support free massive scalar BV generator complex, with elliptic kinetic operator $P=-\partial_x^2+m^2$ for $m>0$. Let $D=d+\hbar\Delta_{\mathrm{BV}}$. The quantum weight $w=r+2k$ is preserved by $D$, where $r$ counts symmetric generators and $k$ counts powers of $\hbar$.

Following QW-001 set

$$
W_w(U)=
\bigoplus_{\substack{r,k\ge0\\r+2k=w}}
\hbar^k\mathrm{Sym}^r E_p(U),
\qquad
T_N(U)=\bigoplus_{0\le w<N}W_w(U).
$$

Each finite $T_N$ satisfies Weiss descent and has compatible disjoint-open factorization maps. Their tower is an object of

$$
\mathrm{Pro}\bigl(\mathrm{Fact}_{\mathrm{Weiss}}(\mathcal C_p)\bigr).
\tag{1}
$$

This **does not** imply that the evaluated assignment

$$
U\longmapsto \mathbf T(U):=\{T_N(U)\}_N
\tag{2}
$$

is a Weiss cosheaf *valued in* $\mathrm{Pro}(\mathcal C_p)$. The latter axiom requires computing the Čech homotopy colimit in the pro-category, and a new proof.

For a constant target $R\in\mathcal C_p$, the established mapping formula is

$$
\mathrm{Map}_{\mathrm{Pro}(\mathcal C_p)}
(\mathbf T(U),\mathrm{const}(R))
\simeq
\mathrm{colim}_N\mathrm{Map}_{\mathcal C_p}(T_N(U),R).
\tag{3}
$$

Thus maps into a constant pro-object **must factor through some finite quantum-weight stage**. This is Barnea–Harpaz–Horel, *Pro-categories in homotopy theory*, §5.1.

## 2. Main theorem: quantum pro-valued descent fails

**Theorem PRO-1.** On a genuine Weiss cover for a free massive scalar, the assignment (2) fails Weiss descent with values in $\mathrm{Pro}(\mathcal C_p)$. The obstruction is a compatible family of local quantum BV maps to a constant coefficient object that cannot arise from any globally bounded weight cutoff.

**Proof.** Fix disconnected Euclidean open intervals and their finite unions:

$$
I_j=(3j,3j+1),\qquad
U=\coprod_{j\ge1}I_j,\qquad
U_k=\coprod_{1\le j\le k}I_j.
$$

The increasing collection $\{U_k\}$ is a Weiss cover because every finite collection of points of $U$ lies in some $U_k$. Its Čech homotopy colimit, when defined, agrees with the filtered colimit of the directed diagram.

For $j\ge1$ define the moment functional on compact-support test functions by

$$
\ell_j(f)=\int_{I_j} e^{mx}f(x)\,dx.
$$

It is continuous on nuclear Fréchet support stages and therefore defines a liquid morphism. Since $P(e^{mx})=0$, integration by parts gives $\ell_j(Pg)=0$. As established in QW-001, the induced cochain map

$$
\lambda_j:W_j(U)\longrightarrow \underline{\mathbb R}[0]
$$

projects onto the degree-zero-power-of- $\hbar$ component and applies the $j$ -fold symmetric tensor of $\ell_j$. It kills *both* the kinetic boundaries and the contributions of $\hbar\Delta_{\mathrm{BV}}$, so it is a morphism for the **full quantum differential**. Choose a compactly supported bump $f_j$ inside $I_j$ normalized by $\ell_j(f_j)=1$. The class

$$
z_j=x_{f_j}^{\,j}\in W_j(U)^0,
\qquad \lambda_j(z_j)=1,
$$

is a nontrivial degree-zero quantum BV cohomology class. For $j>k$, the entire functional $\lambda_j$ vanishes upon restriction to $W_j(U_k)$.

Construct a compatible family of **local pro-morphisms**

$$
a_k:\mathbf T(U_k)\longrightarrow
\mathrm{const}(\underline{\mathbb R}[0])
$$

represented at cutoff $N=k+1$ by the finite sum

$$
T_{k+1}(U_k)\longrightarrow \underline{\mathbb R}[0],
\quad
(t_0,\dots,t_k)\longmapsto \sum_{j=1}^{k}\lambda_j(t_j).
\tag{4}
$$

These are honest quantum cochain maps. For $l\le k$, the restriction of $a_k$ along the inclusion $U_l\subset U_k$ equals $a_l$: terms with $j>l$ vanish on $U_l$. Hence the maps form a coherent compatible cone on the directed local diagram with values in the constant real unit.

Suppose a *global* pro-morphism $a:\mathbf T(U)\to\mathrm{const}(\underline{\mathbb R}[0])$ induced this cone. By formula (3), some finite $N$ and cochain map $T_N(U)\to\underline{\mathbb R}[0]$ represent $a$. Its restriction to each $U_k$ is blind to weights $j\ge N$. Choose $k\ge N$. But $a_k(z_k)=1$ for the genuine degree-zero class of weight $k$. After passing to a common truncation $T_M(U_k)$ with $M>k$, the restriction of the putative global map gives $0$ on $z_k$, while $a_k$ gives $1$. They are therefore distinct even in the derived pro-mapping space, contradiction.

Thus the restriction map

$$
\pi_0\mathrm{Map}_{\mathrm{Pro}(\mathcal C_p)}
(\mathbf T(U),\mathrm{const}(\underline{\mathbb R}))
\longrightarrow
\pi_0\mathrm{holim}_k
\mathrm{Map}_{\mathrm{Pro}(\mathcal C_p)}
(\mathbf T(U_k),\mathrm{const}(\underline{\mathbb R}))
$$

does not hit the explicitly compatible family $(a_k)$. If the Čech colimit of the local pro-objects were equivalent to $\mathbf T(U)$, the mapping-space universal property would contradict this fact. Therefore the pro-valued Weiss comparison is not an equivalence. $\square$

This is **stronger than the earlier inverse-limit counterexample**: no ordinary product $\mathrm{holim}_N T_N$ is formed before detecting the failure, and compactness of the liquid real unit is **not needed**. What fails is the assumption that the finite truncation bound for a global pro-morphism can grow without bound as a local cover is enlarged.

## 3. General obstruction and a valid meaning of completion

For an increasing Weiss cover with every $T_N$ Weiss-local, pro-valued descent would imply that for each constant target $R$ the canonical comparison

$$
\mathrm{colim}_N\mathrm{holim}_k
\mathrm{Map}_{\mathcal C_p}(T_N(U_k),R)
\longrightarrow
\mathrm{holim}_k\mathrm{colim}_N
\mathrm{Map}_{\mathcal C_p}(T_N(U_k),R)
\tag{5}
$$

is an equivalence. PRO-1 gives a nonzero witness to the failure of this interchange. A **uniform cutoff condition** for compatible local probes is therefore necessary for pro-valued descent. It is not, by itself, sufficient: other targets and higher homotopy groups must also be checked.

The existing tower remains a mathematically legitimate completion **in the weaker target category**

$$
\mathrm{Pro}\bigl(\mathrm{Fact}_{\mathrm{Weiss}}(\mathcal C_p)\bigr).
$$

Each stage is a genuine local factorization algebra, with a compatible free quantum differential and operations. But no canonical equivalence is asserted between this category and factorization algebras *valued in* $\mathrm{Pro}(\mathcal C_p)$.

A positive successor must construct an explicit localization or completion functor, state the actual target category, explain how it removes the unbounded-cutoff obstruction, and verify quantum differential, disjoint-open multiplication and Weiss descent **in that target**. It must then be compared to the differentiable pro-cochain/bornological models of Costello–Gwilliam or Gwilliam–Rejzner. The latter comparison is still open.

## 4. Finite adversarial replay

Run

~~~sh
python3 research/condensed-qft/fixtures/pro_valued_weiss.py
~~~

The fixture uses exact rational linear functionals and finite truncation matrices. It verifies that the local maps represented at stage $k+1$ restrict compatibly to every earlier cover stage; that every fixed global cutoff $N$ fails at $k\ge N$; and that all witnesses are nonzero in the degree-zero quantum cohomological moment model. The **infinite theorem** is proved by the categorical map formula and the unbounded-cutoff argument, not by finite enumeration.

## 5. Evidence and claim boundaries

| Claim | Status | Basis |
| --- | --- | --- |
| Quantum-weight stages and factorization properties | Source-backed proved predecessor | QW-001; Costello–Gwilliam |
| Pro-morphism formula to a constant object | Established mathematics | Barnea–Harpaz–Horel §5.1 |
| Compatible local moment maps (4) | Direct proof | Massive field equation and finite-stage liquid maps |
| PRO-1: no global pro-morphism, hence no pro-valued Weiss descent | Direct mathematical proof | (3), (4), classes $z_k$ |
| Naive ordinary inverse-limit realization fails Weiss descent | Previously proved | QW-001 |
| All pro-/bornological/renormalized completions fail | **NOT PROVED** | Different completions and colimits require their own arguments |
| Comparison with differentiable pro-cochain free quantum observables | **OPEN** | Requires typed analytic equivalence |
| Independent mathematical priority and Lean formalization | **NOT CERTIFIED** | Explicit GCL derivation and checkable prior-art constraints |

Primary sources: [Barnea–Harpaz–Horel, *Pro-categories in homotopy theory*](https://arxiv.org/abs/1507.01564), §5.1; [Scholze, *Lectures on Analytic Geometry*](https://people.mpim-bonn.mpg.de/scholze/Analytic.pdf), Theorem 6.5; [Gwilliam–Rejzner, *Relating Nets and Factorization Algebras: Free Field Theories*](https://link.springer.com/article/10.1007/s00220-019-03652-9), Definitions 2.29–2.33; GCL's QFT-COND-003 and QW-001 source notes.

**Research decision:** Do not promote the stagewise-local quantum-weight tower to a pro-valued Weiss cosheaf. The concrete new requirement is a *uniform finite-cutoff/localization theorem* (or a new completion category where this demand is appropriately reformulated) and an exact comparison with the established completed free-field constructions.
