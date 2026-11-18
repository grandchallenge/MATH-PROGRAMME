# External mathematical source and evidence lock — 2026-11-18

## Fixed inputs

- Formal conjecture scaffold: `google-deepmind/formal-conjectures@2f91d251c07f/FormalConjectures/ErdosProblems/561.lean`. Theorem `Erdos561.erdos_561` has `by sorry`: **statement only, not proof**.
- October 2026 two-component paper: arXiv:2610.25958v1, downloaded PDF SHA256 `2ec8aebcc738c66a0cdc36ba181bbf1f64326d6e814641072f525b482b8efc3a`. Earlier proof audit #3475 is **not** a proof of unrestricted #561.

## Critical-degree external input to the fixed 24-edge claim

External hypothesis: every simple edge-5-critical graph C on n vertices satisfies `2e(C)>=4n+3`. `edge-5-critical` means maximum degree five, edge chromatic number six, and every proper subgraph five-edge-colourable.

- **Primary original attribution:** K. Kayathri, *On the size of edge-chromatic critical graphs*, Graphs and Combinatorics **10** (1994), 139–144. DOI `10.1007/BF02986658`. Publisher page https://doi.org/10.1007/BF02986658 . The full primary 1994 text has **NOT** been acquired or replayed here (attempted download returned HTML). This is a review blocker, not an inferred proof lock.
- **Later published attestation:** R. Luo and C.-Q. Zhang, *Edge coloring of graphs with small average degrees*, Discrete Mathematics **275** (2004), 207–218, DOI `10.1016/S0012-365X(03)00107-9`, page 208, Conjecture 1.1 and statement that it is verified for `Δ<=5`, citing [1,4,5,13] including Kayathri 1994.
- **Authors' corroborating manuscript:** Y. Cao and G. Chen, *On the average degree of edge chromatic critical graphs*, https://math.gsu.edu/gchen/files/2018/CaoChen2018-1.pdf , retrieved HTTP 200 as PDF 2026-11-18, SHA256 `ae95b0f2fa1cb6db18ba75c356828839d28db7bbf94f0a8c56c97dd84c35b25b`, introduction p.2 explicitly says the conjecture is verified for `Δ<=6`.

The accessible published 2004 source and later author manuscript corroborate the exact contract used by the 24-edge proof; **neither constitutes a locked copy of Kayathri's original proof.** Keep this gap in #3502 until primary-source verification or a self-contained replacement proof is obtained.

## Internal reproducibility

- The included 11,197-case finite classification has two programs, one Python and one C++17. Their agreement is *algorithmic cross-checking*, not independent proof assessment.
- The 24-edge original result is a **fixed-parameter, computer-assisted paper proof candidate**, NOT protected certification or public priority.
- The full Erdős #561 conjecture remains **OPEN**. The joint residual research issue #3490 likewise remains **OPEN** outside its resolved subfamilies.
