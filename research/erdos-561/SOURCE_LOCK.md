# External mathematical source and evidence lock — 2026-11-18

## Fixed inputs

- Formal conjecture scaffold: `google-deepmind/formal-conjectures@2f91d251c07f/FormalConjectures/ErdosProblems/561.lean`. Theorem `Erdos561.erdos_561` has `by sorry`: **statement only, not proof**.
- October 2026 two-component paper: arXiv:2610.25958v1, downloaded PDF SHA256 `2ec8aebcc738c66a0cdc36ba181bbf1f64326d6e814641072f525b482b8efc3a`. Earlier proof audit #3475 is **not** a proof of unrestricted #561.

## New dependency closure: 1994 full text no longer needed

## Pinned constructive source for Vizing's adjacency lemma

P. M. D. Woodall, *Edge-Colourings of Simple Graphs*, postgraduate lecture notes (2006/07), pp. 1-4, Theorem 3 (p. 4), with an explicit proof from fan sequences and Lemmas 2.1/3.1. https://www.maths.nottingham.ac.uk/plp/pmadw/PG/edgecol.pdf . CHAD source-lock 2026-11-18: HTTP 200, application/pdf, **78,683 bytes**, SHA-256 **`8aaf86605054ed8ebc78a29a44f960b29fe9e9864a373f79db8e9e1b59622ae1`**. This is a full written proof of the classical theorem invoked in `CRITICAL5_REPLACEMENT_PROOF.md`; it is not a copy of Vizing's original 1965 publication. The exact graph6 finite datasets and source hashes are pinned below.


The proof now uses `CRITICAL5_REPLACEMENT_PROOF.md`: a direct derivation of `e(C)>=2|V(C)|` from Vizing's adjacency lemma and a complete seven/eight-vertex classification. This proves the *only critical-graph bound actually needed* for the fixed 24-edge theorem without relying on a full 1994 Kayathri proof. Original 1994 provenance below is retained for historical reference; its unavailability is **not** a mathematical dependency blocker for this revised proof.

- McKay `graph7.g6` SHA256 `5a878f1a46606da4733df250bf9a412d6ae0b3c73c2112e25d66ba00ae565b56`, 1,044 classes.
- McKay `graph8.g6` SHA256 `546a249902101c97d3aa590f93e53366854bd0a6f405aa59bdb32d25c57f845a`, 12,346 classes.
- Upstream https://users.cecs.anu.edu.au/~bdm/data/graphs.html, data files CC BY 4.0. Exact copies stored under `fixtures/`; all contents and schema are checked on replay.

## Historical critical-degree theorem provenance (superseded for this proof)

External hypothesis: every simple edge-5-critical graph C on n vertices satisfies `2e(C)>=4n+3`. `edge-5-critical` means maximum degree five, edge chromatic number six, and every proper subgraph five-edge-colourable.

- **Primary original attribution:** K. Kayathri, *On the size of edge-chromatic critical graphs*, Graphs and Combinatorics **10** (1994), 139–144. DOI `10.1007/BF02986658`. Publisher page https://doi.org/10.1007/BF02986658 . The full primary 1994 text has **NOT** been acquired or replayed here (attempted download returned HTML). This is a review blocker, not an inferred proof lock.
- **Later published attestation:** R. Luo and C.-Q. Zhang, *Edge coloring of graphs with small average degrees*, Discrete Mathematics **275** (2004), 207–218, DOI `10.1016/S0012-365X(03)00107-9`, page 208, Conjecture 1.1 and statement that it is verified for `Δ<=5`, citing [1,4,5,13] including Kayathri 1994.
- **Authors' corroborating manuscript:** Y. Cao and G. Chen, *On the average degree of edge chromatic critical graphs*, https://math.gsu.edu/gchen/files/2018/CaoChen2018-1.pdf , retrieved HTTP 200 as PDF 2026-11-18, SHA256 `ae95b0f2fa1cb6db18ba75c356828839d28db7bbf94f0a8c56c97dd84c35b25b`, introduction p.2 explicitly says the conjecture is verified for `Δ<=6`.

The accessible published 2004 source and later author manuscript corroborate the exact contract used by the 24-edge proof; **neither constitutes a locked copy of Kayathri's original proof.** The replacement proof is now supplied; the original 1994 text remains an optional historical source-verification task. Do not state that its bytes were retrieved.

## Internal reproducibility

- The included 11,197-case finite classification has two programs, one Python and one C++17. Their agreement is *algorithmic cross-checking*, not independent proof assessment.
- The 24-edge original result is a **fixed-parameter, computer-assisted paper proof candidate**, NOT protected certification or public priority.
- The full Erdős #561 conjecture remains **OPEN**. The joint residual research issue #3490 likewise remains **OPEN** outside its resolved subfamilies.
