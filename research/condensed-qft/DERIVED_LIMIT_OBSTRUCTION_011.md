# QFT-COND-005 / DLI-011: A derived inverse-limit obstruction in nuclear Fréchet spaces

**Disposition:** Exact counterexample in the underlying algebraic category of real vector spaces; source-backed nuclearity of the example. This is **not** a calculation of derived liquid inverse limits, nor a counterexample to Costello–Gwilliam Appendix B.6. Tracker: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2603.

## Theorem DLI-1: nuclear Fréchet tower with a nonzero first derived limit

Let

$$
s=\{a=(a_k)_{k\geq0}:p_m(a)=\sup_{k\geq0}(1+k)^m|a_k|<\infty\text{ for all }m\geq0\}.
$$

This rapidly decreasing sequence space is a nuclear Fréchet space. Let $S:s\to s$ be the continuous injective right shift, $S(a_0,a_1,\ldots)=(0,a_0,a_1,\ldots)$. Consider the inverse system $V_n=s$ with transition $S:V_{n+1}\to V_n$. On the underlying vector spaces, the standard countable Roos differential is

$$
\Delta:\prod_{n\geq0}s\longrightarrow\prod_{n\geq0}s,\qquad
\Delta(y)_n=y_n-Sy_{n+1}.
$$

**Claim:** $\varprojlim V_n=0$, while $\varprojlim^1 V_n=\operatorname{coker}\Delta\neq0$, with $\varprojlim^1$ calculated in the category of real vector spaces.

**Proof of the ordinary-limit assertion.** A compatible element obeys $y_0=S^ny_n$ for all $n$. Hence the first $n$ coordinates of $y_0$ vanish for all $n$, so $y_0=0$. The same reasoning applies to any $y_j$, proving the assertion.

**Proof of nonvanishing.** Let $x_n=e_0=(1,0,0,\ldots)$ for every $n$. If $x=\Delta(y)$, then $y_n=e_0+Sy_{n+1}$. Thus $(y_n)_0=1$ and $(y_n)_k=(y_{n+1})_{k-1}$ for $k>0$. Iterating forces $(y_0)_k=1$ for every $k$. This sequence is not rapidly decreasing, a contradiction. Hence $[x]\neq0$ in $\operatorname{coker}\Delta$. $\square$

**Derived consequence with declared ambient category.** In $D(\mathrm{Vect}_{\mathbb R})$, the homotopy inverse limit of the tower of degree-zero underlying vector spaces is represented by $\operatorname{Cone}(\Delta)[-1]$ (cohomological conventions). It has $H^0=\ker\Delta=0$ and $H^1=\operatorname{coker}\Delta\neq0$. The ordinary inverse limit misses this class.

## Theorem DLI-2: every fixed coordinate truncation loses the obstruction

For $N\geq1$, let $P_N=\mathbb R^N$ and $S_N:P_N\to P_N$ be the truncated right shift. Then $S_N^N=0$. The differential on $\prod_nP_N$ is surjective, with explicit right inverse

$$
y_n=\sum_{j=0}^{N-1}S_N^j x_{n+j}.
$$

Indeed, $y_n-S_Ny_{n+1}=x_n-S_N^Nx_{n+N}=x_n$. Consequently $\varprojlim^1(P_N,S_N)=0$ at every fixed $N$, even though $\varprojlim^1(s,S)\neq0$.

**Completion warning.** $s$ embeds densely in $\mathbb R^{\mathbb N_0}$ for the weaker product topology; $s$ itself is already complete in its **own** nuclear Fréchet topology. Replacing $s$ with its product-topology closure changes the coefficient object. Under that change, the formal solution with all coordinates equal to one exists. No assertion of ordinary Fréchet completion of $s$ is intended.

## Implications for QFT-COND-005

The example makes one necessary gate explicit: stagewise nuclearity and vanishing higher cohomology do not imply that inverse-limit formation is underived. A derived comparison for quantum-weight towers or differentiable pro-cochains must specify the ambient stable category, the functor realizing these nuclear Fréchet spaces, and whether the relevant tower is derived-limit acyclic (for example, by an appropriately formulated Mittag–Leffler or fibrancy hypothesis).

This result **does not establish** the relative target-support liquid Hom colimit property (LFO3). Nor does it prove that this nonzero vector-space $\varprojlim^1$ persists in derived $p$-liquid modules or in the exact category of strict nuclear Fréchet sequences. Both require a separate comparison theorem. A physical BV observable complex realizing this tower has not been constructed.

**Next mathematical gates:** (1) determine if $\underline{s}$ and $S$ preserve this Roos obstruction under the selected exact derived-liquid realization; (2) prove or refute LFO3 on the actual compact-support source stages; (3) implement a differentiable pro-cochain mapping-object comparison, including filtered differentials and Weiss descent.

## Reproducibility and evidence

The finite rational test verifies, for $N=1,\ldots,24$, the telescoping identity $y_n-S_Ny_{n+1}=x_n$ on nontrivial generated data. It is a **finite regression check only**; the infinite contradiction above is the proof.

Source context: [rapidly decreasing sequence space](https://link.springer.com/article/10.1007/s00605-015-0758-z); [Vogt, Subspaces and Quotient Spaces of (s)](https://www.sciencedirect.com/science/article/pii/S0304020808705310). Standard countable derived-limit Roos construction is used algebraically, not as a topological or liquid exactness theorem.

**Novelty:** no independent priority claim. This is an explicit diagnostic example within the QFT-COND research programme.
