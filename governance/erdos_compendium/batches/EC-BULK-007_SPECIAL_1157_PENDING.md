# EC-BULK-007 — #1157 Brown–Erdős–Sós parameter/notation fidelity

**SOURCE_NORMALIZATION_PENDING**, not a proof of the open hypergraph problem.

The current catalogue at https://www.erdosproblems.com/1157 introduces parameters $t,k,r\ge2$, but immediately defines a family of $r$-uniform hypergraphs with $k$ vertices and $s$ edges. Variable **$s$ is unbound** in the introducing quantification, while **$t$ is unused** in the primary $\mathrm{ex}_r(n,\mathcal F)$ quantity. The text later uses a different **$t$-uniform** Brown–Erdős–Sós conjecture involving both $r$ and $t$. These must not be merged.

Original issue return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2428#issuecomment-6184851029
Primary original mathematical reference: Brown, Erdős, Sós (1973), BES73; Vardi (1999) §3.64.

## Bounded confirmation

For $r=2,k=3,s=3$, forbidden family is a triangle and exact enumeration gives $\mathrm{ex}_2(5,K_3)=6$; Mantel's theorem independently gives the same. For $r=3,k=4,s=2$ on four vertices, any two triples lie on those four points, hence $\mathrm{ex}_3(4,\mathcal F)=1$. Neither proves the general sharp hypergraph theory or interprets an unbound parameter.

## Source correction boundary

Read BES73 and Vardi99 exact theorem and variable domains, including whether $s\le\binom kr$, whether the $k$ vertices must be distinct even when isolated, whether forbidden hypergraphs use induced or ordinary embeddings, and whether $\gg_{k,s}$ in the maintained bound suppresses dependence on $r$. Correct only after primary source text matches the normalized statement. Preserve the original frozen issue SHA. No independent reviewer approval has occurred.
