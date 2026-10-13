# QFT-COND-005 / LFO-013 — Exact verification matrix

**Artifact:** [LFO3_SURJECTIVITY_THEOREM_013.md](LFO3_SURJECTIVITY_THEOREM_013.md). This is a written mathematical proof, **not** a finite numerical validation of an infinite statement.

| Obligation | Evidence | Result | Limit |
| --- | --- | --- | --- |
| Real liquid category preserves filtered colimits in condensed modules | Clausen–Scholze, *Condensed Mathematics and Complex Geometry*, Theorem 3.11 | SOURCE-BACKED | Fixed $0<p\le1$ |
| Stage $G_b=\mathcal D_{L_b}(V)$ is nuclear Fréchet | Classical test-function topology; support restrictions are closed in $C^\infty(V)$ | SOURCE-BACKED | Euclidean open $V$, compact $L_b$ |
| Stage inclusions are closed embeddings | $\bigcap_{x\notin L_b}\ker\mathrm{ev}_x$ inside $G_c$ | PROVED | Required for plots upgrade |
| Filtered colimits of condensed modules evaluated on profinite plots | Sheaf condition with finite covers and filtered colimits commuting with finite limits | PROVED | Applies to filtered diagrams, not arbitrary inverse limits |
| Scalar point evaluations on $H$ continuous | Full faithfulness of Fréchet condensed realization; $H$ metrizable | PROVED | Does not assert source compactness |
| Uniform compact support for all global images | Increasing sequence of closed subspaces $H_b$, Baire theorem | PROVED | Fixed Fréchet source $H$ |
| Factorization of every $S$-plot through chosen $G_{b_0}$ | Stagewise factorization of filtered colimit plots plus closed embedding | PROVED | Cannot infer from global points alone |
| LFO3 surjectivity | Previous two rows | PROVED | Underived Hom sets |
| LFO3 injectivity | Monic stage maps into filtered colimit | PROVED | Underived Hom sets |
| $A_p(V)\cong\underline{\mathcal D(V)}$ | Strict LF bounded-set regularity; compact image of profinite plot lies in stage | PROVED | Specific strict LF sequence, not arbitrary LF |
| Independence from source support | Identity map $\mathcal D(\mathbb R)\to\mathcal D(\mathbb R)$ | COUNTEREXAMPLE to interchanging outer source limits | Does not contradict fixed-source LFO3 |
| Higher $\operatorname{RHom}$ and $\operatorname{Ext}^i$ | No proof supplied | OPEN | Must not be inferred from LFO3 |
| Pro-cochain mapping enrichment | No equivalence proof supplied | OPEN | Must not be inferred from LFO3 |
| Mathematical novelty | Classical ingredients; explicit adapted proof | NOT CLAIMED | No external priority claim |
| Numerical fixture | Not applicable to Baire/profinite categorical proof | NOT RUN | Do not report finite tests as proof |
| Protected GitHub admission | PR status to be checked against exact head | PENDING | No merge claim here |

## Typographic review

All mathematical display expressions in the associated proof use Markdown-compatible blank-line-separated display math fences and inline dollar delimiters. No raw HTML or unsupported LaTeX delimiters are required. Actual MkDocs build/render remains a repository CI obligation.

## Review focus

1. Verify that filtered colimits in real $p$-liquid modules are computed in condensed modules and that profinite section evaluation commutes with these filtered colimits.
2. Ensure the plot factorization uses **closed** support stages rather than incorrectly treating pointwise equality as sufficient for arbitrary condensed objects.
3. Verify classical **strict LF** regularity and topology inheritance, not properties of arbitrary LF systems.
4. Confirm that no derived conclusion is made from underived Hom bijectivity.
