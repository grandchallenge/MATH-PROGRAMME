# Erdős #561 — independent bounded factor-gate reconstruction

**Task:** `ERDOS-PV-0561-B`; **source issue:** [#1832](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1832), source-body SHA-256 `040d064d6aa382dbc832b449e8d0869378c145523bf99e795b185997c49751b4`. **Source lock:** `teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89:data/problems.yaml` (Git blob `4e60263a80af6207aca494d2e1388e44fa372889`), historical status **open**. **2026 paper revision:** Chunlin You, *Size Ramsey numbers of star forests with two components on one side*, [arXiv:2610.25958v1](https://arxiv.org/html/2610.25958v1), posted 19 October 2026. The exact HTML response captured by CHAD was 433,901 bytes, SHA-256 `abcf3930c1b8d77578286b701d9317b63e7ea3832dcf10c627ef1220a32f04f7`. This locks a retrieved HTML rendering, not the original LaTeX source bytes or the 1978/2002 primary papers.

**Verification scope:** an ordinary, independently reconstructed and finite-tested **conditional graph-factor bridge** corresponding to the paper's Corollary 2.6 and final Claim 3.10. The classical Lovász factor theorem is cited as a known external theorem, not independently proved here. The structural reductions in the paper's Claims 3.2–3.8 are treated as *premises*, not as checked results. No full-paper verification, Lean kernel proof, novel theorem priority or MATHCERT certification.

## Original problem and normalization

For finite simple graphs, $G\to(F,H)$ means that every red/blue colouring of the edges of $G$ has a red (not necessarily induced) $F$ or a blue $H$. The asymmetric size Ramsey number is the minimum number of **host edges** over such $G$.

For non-increasing, strictly positive leaf-count sequences $n_1,\ldots,n_s$ and $m_1,\ldots,m_t$, let $F=\bigsqcup_i K_{1,n_i}$ and $H=\bigsqcup_j K_{1,m_j}$. Problem #561 asks whether the two-target size Ramsey number equals the sum of the anti-diagonal maxima $\ell_k=\max_{i+j=k}(n_i+m_j-1)$, from $k=2$ to $k=s+t$. The **general $s,t\geq3$ problem remains open in the October 2026 source**; the newer paper claims a special result when one forest has exactly two components.

The source's Theorem 1.2 gives, for $a\geq b\geq1$ and $n_1\geq\cdots\geq n_q\geq1$,

$$
\widehat r\left(K_{1,a}\sqcup K_{1,b},\bigsqcup_{i=1}^qK_{1,n_i}\right)
=(a+n_1-1)+\sum_{i=1}^{q-1}\max\{a+n_{i+1}-1,b+n_i-1\}+(b+n_q-1).
$$

The previous source-audit return independently normalized this formula and checked 19,383 parameter tuples. That work was **statement-level** only, not an independent proof of Theorem 1.2.

## Exact conditional theorem verified here

Let $G$ be a finite simple undirected graph and let $\alpha\geq2$ and $\beta\geq2(\alpha+1)$ be integers. Put $D=\alpha+\beta$ and suppose:

1. $\Delta(G)\leq D$.
2. There is an **edge-disjoint partition** into $\alpha$ matchings $M_1,\ldots,M_\alpha$, a subgraph $H_0$ consisting of **vertex-disjoint nonempty stars**, and a residual subgraph $R$. Empty matchings are allowed; their union and $H_0$ and $R$ partition $E(G)$ exactly once.
3. **Every** vertex of degree $D$ in $G$ is a center of one of the star components of $H_0$.
4. $e(R)\leq\beta-1$.

**Conclusion:** $G$ has an edge-disjoint decomposition $E(G)=E(J)\sqcup E(K)$ with $\Delta(J)\leq\alpha$ and $\Delta(K)\leq\beta$.

This is not an independent claim about all bounded-degree graphs. It assumes the crucial center localization and near-exact star-plus-matchings decomposition supplied earlier in You's counterexample analysis.

### Step 1: exact Lovász factor specialization

For $v\in V(G)$ set

$$
g(v)=\max\{0,d_G(v)-\beta\},\qquad f(v)=\alpha.
$$

The hypothesis $d_G(v)\leq\alpha+\beta$ gives $0\leq g(v)\leq f(v)$. A spanning $(g,f)$ factor $J$ has $g(v)\leq d_J(v)\leq\alpha$ and its edge complement $K$ has $d_K(v)=d_G(v)-d_J(v)\leq\beta$. Conversely any edge partition with these degree bounds satisfies the factor inequalities, including vertices where $d_G(v)<\beta$.

For disjoint $S,T\subseteq V(G)$ and $Y=V(G)\setminus(S\cup T)$ set

$$
A(S,T)=\alpha|S|+\sum_{v\in T}\min\{d_G(v),\beta\}-e_G(S,T).
$$

The non-parity portion of Lovász's $(g,f)$ criterion equals $A$, since $d-g=\min\{d,\beta\}$. Because $\alpha>0$, the equality $g(v)=f(v)$ holds **if and only if** $d_G(v)=D$. Thus the parity obstruction counts exactly the components $C$ of $G[Y]$ for which all vertices have ambient degree $D$ and

$$
\alpha|V(C)|+e_G(V(C),T)\quad\text{is odd}.
$$

Write their number as $q_D(S,T)$. The original theorem therefore specializes to the exact biconditional

$$
\exists\,E(G)=E(J)\sqcup E(K),\Delta(J)\leq\alpha,\ \Delta(K)\leq\beta
\quad\Longleftrightarrow\quad
\forall S\cap T=\varnothing,\ A(S,T)\geq q_D(S,T).
$$

The parity term for edges incident with $T$ must **not** be deleted. The original Lovász theorem remains a cited dependency; the specialization, parity identification, and both implication directions are reconstructed here.

### Step 2: graph-independent weighted boundary estimate

Write $e(S)=e(G[S])$ and $e(S,Y),e(T,Y)$ for the respective crossing edges. Since $0\leq d_G(v)\leq D$,

$$
D\min\{d_G(v),\beta\}\geq\beta d_G(v).
$$

The degree sums give

$$
D|S|\geq2e(S)+e(S,T)+e(S,Y),
$$

$$
\sum_{v\in T}d_G(v)=2e(T)+e(S,T)+e(T,Y).
$$

Substitute them in $D A(S,T)$ to get the exact strengthened bound

$$
D A(S,T)\geq
2\alpha e(S)+2\beta e(T)+\alpha e(S,Y)+\beta e(T,Y)
\geq\alpha e(S,Y)+\beta e(T,Y)\geq0.
$$

Thus $A\geq0$ and, since $\beta\geq\alpha$,

$$
e(S,Y)+e(T,Y)\leq\frac D\alpha A(S,T).
$$

All quantities in the original integer cut certificate are integral, including $A$ and $q_D$; division is used only in a real inequality after that fact has been recorded.

### Step 3: suppose a forbidden cut exists

Assume the desired edge partition does not exist. By the exact Lovász specialization, there are disjoint $S,T$ with

$$
A(S,T)<r:=q_D(S,T).
$$

By Step 2, $A\geq0$. Since $A$ and $r$ are integers, $r\geq1$ and $A\leq r-1$. Writing $Y=V(G)\setminus(S\cup T)$ and $B=e(S,Y)+e(T,Y)$, we have

$$
0\leq B\leq\frac D\alpha(r-1).
$$

Let $C_1,\ldots,C_r$ denote **the counted components**, which are pairwise vertex disjoint within $G[Y]$. Every vertex of every $C_i$ has ambient degree exactly $D$.

If all $r$ counted components have $m=|C_i|\leq D$ vertices, then, by simplicity of $G$,

$$
e_G(C_i,S\cup T)
=Dm-2e(C_i)
\geq m(D-m+1)
=D+(m-1)(D-m)\geq D.
$$

There are no edges between distinct components of the induced graph $G[Y]$, so summing these cut edges gives $B\geq rD$. This contradicts $B\leq D(r-1)/\alpha$ for $r\geq1$ and $\alpha\geq2$.

Therefore at least one counted component has **at least $D+1$ vertices**. Each of the other $r-1$ counted components is nonempty, so at least $D+r$ vertices of $Y$ belong to counted components and have ambient degree $D$.

### Step 4: the star-center localization forces a large boundary

By hypothesis 3, each of these at least $D+r$ vertices is a center $c$ of a component of $H_0$, with star size $n(c)\geq1$. **Every leaf of this star lies in $S\cup T$.** Otherwise, a leaf in $Y$ would be connected to its center by an edge of $G[Y]$ and would lie in the same counted component. It would then have degree $D$ and would have to be a center of $H_0$, impossible because the components of $H_0$ are vertex disjoint.

For each selected center $c$, the decomposition into $\alpha$ matchings, $H_0$, and $R$ yields

$$
D=d_G(c)\leq\alpha+n(c)+d_R(c),
\qquad n(c)\geq\beta-d_R(c).
$$

The chosen star edges are distinct because $H_0$ is an edge-disjoint union of vertex-disjoint stars. They all cross the cut $(Y,S\cup T)$, so summing over the selected centers and observing $\sum_c d_R(c)\leq2e(R)$ gives

$$
B\geq\beta(D+r)-2e(R)
\geq\beta(D+r-2)+2.
$$

The second inequality uses the **stated residual bound** $e(R)\leq\beta-1$. As $D\geq1$,

$$
\beta(D+r-2)+2>\beta(r-1).
$$

On the other hand, $\alpha\geq2$ and $\beta\geq2(\alpha+1)\geq6$ give

$$
\frac D\alpha=1+\frac\beta\alpha
\leq1+\frac\beta2<\beta.
$$

Hence the forbidden cut satisfies $B\leq D(r-1)/\alpha\leq\beta(r-1)$, even when $r=1$, contradicting the strict lower bound. No forbidden cut exists. The Lovász criterion then supplies the required edge partition. **QED, conditional on the four stated graph hypotheses and the cited Lovász theorem.**

## Precise interface with You's Claim 3.10

The paper first reduces a hypothetical counterexample to $b=1$, $a\geq3$, $q\geq3$, $n_q=1$, $D=a+n_1-2$ and $\Delta(G)=D$. In the proof above, substitute

$$
\alpha=a-1,\qquad\beta=n_1-1,\qquad D=\alpha+\beta.
$$

- Claim 3.6 supplies the $a-1=\alpha$ matchings, a vertex-disjoint copy $H_0$ of the target blue star forest, and $e(R)\leq\rho-k$, where $k\geq1$.
- Claim 3.7 supplies at least two jumps $n_i-n_{i+1}\geq a$. With $n_q=1$ this implies $\beta=n_1-1\geq2a=2(\alpha+1)$.
- Since $\rho=\sum_i\max\{n_i-n_{i+1}-a+1,0\}\leq n_1-n_q=\beta$, the residual bound becomes $e(R)\leq\beta-1$.
- Claim 3.8 states that every vertex with ambient degree $D$ of $G$ is an $H_0$ center, exactly the localization used in Step 4.
- The paper's Corollary 2.6 is the special case of Lovász's theorem derived in Step 1.

**These bullet points identify required source-premise dependencies, not independently checked proofs of Claims 3.2–3.8.** In particular, showing that every putative counterexample satisfies those premises is substantive, uncompleted Phase B work. A copy-count, finite regression, or independent reconstruction of the conditional gate must **not** be reported as an independent validation of Theorem 1.2.

## Falsification and finite checks

Two separately implemented finite procedures were compared: one enumerates all $3^{|V|}$ disjoint ordered cuts and their **parity-sensitive** Lovász obstructions; the other assigns actual edges to two sets by independent backtracking and checks degrees. The finite tests cover all 76 labelled graphs on 0–4 vertices, providing 661 graph/budget comparisons and 46,935 independent cut certificates, with positive budgets in $\{1,2,3\}$ and $\Delta\leq\alpha+\beta$, all 253 five-vertex simple graphs of maximum degree at most two at $(\alpha,\beta)=(1,1)$, and 90 seeded five-vertex comparisons. The weighted cut estimate was tested over the complete 0–4-vertex census. Further checks use four constructed stars-plus-matchings graphs satisfying the paper's reduced-case parameter relation, each tested against 3,000 seeded disjoint cuts, and 12,331 exact-integer parameter inequalities. In total, the two independent algorithms agreed on 1,004 admissible graph/budget comparisons (661 + 253 + 90).

**Negative controls:**
- $K_3$ with $(\alpha,\beta)=(1,1)$ and $K_5$ with $(\alpha,\beta)=(1,3)$ have no feasible degree-bounded edge partition. The **empty** $S=T=\varnothing$ cuts detect $q_D=1>A=0$ from an odd regular component; any implementation omitting the parity obstruction falsely accepts them.
- In the $K_3$ cut $S=\{2\}$, $T=\{1\}$, $Y=\{0\}$, the parity of $\alpha|C|+e(C,T)$ is **even**, despite $\alpha|C|$ being odd. This detects omission of the parity term for edges incident with $T$.
- The general code rejects nonpositive degree budgets, repeated/loop edges and overlapping cut sets.
- The conclusion is **not** assumed from $\Delta(G)\leq D$ alone; the center-localization, small residual, and edge-disjoint matchings must be checked or explicitly retained as hypotheses.

Executable sources: `ci/erdos_pv_0561_factor_gate.py` and `ci/test_erdos_pv_0561_factor_gate.py`. Tests use the Python standard library and a fixed random seed. No Lean provider statement for #561 is present in the protected frozen source snapshot. The oracle is a regression, **not** a proof certificate.

## Scope-qualified disposition and next action

**Bounded conclusion:** `VERIFIED_CONDITIONAL_FACTOR_GATE__PRECURSOR_REDUCTIONS_UNVERIFIED`. We independently reconstructed the parity-bearing Lovász specialization and supplied a complete *ordinary mathematical* proof of its conditional final contradiction, with separate finite brute-force and adversarial tests. We rely on the classical Lovász theorem and the paper's claimed earlier structural hypotheses.

**First open obligation:** independently reconstruct and challenge the bridge from the full paper's induction hypotheses to the structural premises above, especially Claim 3.2 (maximum-degree/edge-count forcing and nonpartition obstruction) and Claims 3.6–3.8 (matching-star-residual decomposition and center localization). Revisit the exact 1978 paper and the 2002 strict/nonstrict hypothesis discrepancy in a separate source-lock step. Phase C must not advertise the whole Theorem 1.2 as kernel checked unless the entire statement and proof are actually in a source-typed Lean environment. Original Erdős #561 for general $s,t\geq3$ remains open; MATHCERT remains `NOT_SUBMITTED`.

A further deliberately **false strengthening** is to remove the star-center hypothesis while keeping the paper's numerical budget. For $\alpha=3$, $\beta=9$, $D=12$, the complete graph $K_{13}$ has ambient maximum degree $D$ and satisfies $\beta\geq2(\alpha+1)$. Any desired partition would force a spanning factor of degree $3$ on thirteen vertices, contradicting the handshaking lemma because $13\cdot3$ is odd. The empty cut independently produces $A=0$, $q_D=1$. This graph **cannot** satisfy the localization premise: thirteen vertices of ambient degree $D$ would all have to be centers of disjoint nonempty stars, requiring at least twenty-six vertices. The counterexample does not invalidate the conditional theorem; it falsifies an overbroad formulation that discards the structural reduction.
