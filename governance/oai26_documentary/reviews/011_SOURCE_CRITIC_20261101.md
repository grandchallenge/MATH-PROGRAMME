# OAI-26 Family 011 — pinned three-PDF source audit and editorial critic

Record: GCL_OAI26_ED01_F011_SOURCE_CRITIC/1. Source lock openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a.

The three PDFs were fetched by exact Git blobs and opening theorem statements inspected:

1. Weighted dilation graphs, smooth shifted primes and totient fibers (Sept 24), blob 3acecffeba75121b28efd194c4c2b266a9f6d77b, 802390 bytes, 68 pages. Theorem 1.1: for every epsilon>0 infinitely many n have totient fibers g(n)>n^(1-epsilon). Theorem 1.2: for fixed 0<delta<1/4 at least x^(1-o(1)) primes 2x<p<=5x have P+(p-1)<=x^delta. Neither positive limiting proportion nor uniformity in delta is claimed.
2. The Poisson-Dirichlet law for prime predecessors (Sept 24), blob c46ae43eabf76a9c1cc53655414567ba4e5b60ae, 795971 bytes, 74 pages. Abstract: the decreasing prime factors of p-1, counted with multiplicity, normalized by log(p-1), converge in finite joint distribution to Poisson-Dirichlet(1). The limiting law is a distinct assertion from simple smoothness abundance.
3. Prime Predecessors with an Even Number of Prime Factors (Sept 17), blob 73d9d9f5ed478e1c0ba049fa00a55fafea4b48a5, 599500 bytes, 45 pages. Theorem 1.1: infinitely many primes have squarefree p-1 and even Omega(p-1), equivalently mu(p-1)=1. The paper cites the first paper's unsigned dilation-graph machinery but requires additional signed, parity-sensitive work. Smoothness alone does not imply this theorem.

Editorial critic: ACCEPTED_EXPOSITION_WITH_LIMITS. The six-section article distinguishes maximal prime factors, full ranked factor-size distribution, and parity of the factor count; it preserves quantitative counting intervals and conventions, scope and the absence of mathematical certification. This is statement-level fidelity review, NOT a proof audit of 187 pages. The central analytic graph, uniformity and spectral estimates, distribution-limit derivations, Type II parity estimates and all external dependencies have not been independently validated. No GCL formal Lean mapping, Comparator verdict or MATHCERT certificate is asserted.

Exact manuscript hash and HTML validation must be checked on the candidate head before protected editorial admission. Parent issue #2901 remains open.
