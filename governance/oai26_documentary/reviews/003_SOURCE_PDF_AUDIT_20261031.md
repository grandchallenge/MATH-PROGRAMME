# OAI-26 Family 003 — source-pinned PDF audit

Record type: `GCL_OAI26_F003_SOURCE_AUDIT/1`; editorial source-fidelity only.

Pinned revision: `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`. All three PDF objects were retrieved from the GitHub Git-blob API and text inspected with pypdf.

| Source | Git blob | Size | Pages | Exact examined statement |
| --- | --- | ---: | ---: | --- |
| September 30, *Quasi-Riemann Hypothesis: a zero-free half-plane Re s > 7/8* | `8132b77eeb270a70b25df8d6609f008e83e65d91` | 1,588,969 | 199 | Abstract p. 1 and introduction p. 4: claims finite-order Hecke L-functions of Q(sqrt(-3)) and all Dirichlet L-functions, including zeta, are zero-free on Re s > 7/8; principal pole at s=1 is allowed |
| October 5, *Quasi-Riemann Hypothesis* (alternate proof) | `3ea94d87ffdee8db02c6ef1e563e6d166021ad2f` | 784,503 | 49 | Theorem 1.1, PDF p. 2: claims the **weaker** region Re s > 11/12 for the same classes of L-functions; points to the September 30 source for the stronger 7/8 region |
| October 1, *Uniform exclusion of Landau–Siegel zeros* | `e31b1a244f251439b01d930c906f4e0c91dfc3a8` | 404,812 | 9 | Theorem 1, PDF p. 1: an absolute c>0 with (1-beta) log q >= c for real zeros beta in (0,1) of primitive nonprincipal real Dirichlet L-functions of conductor q>=3 |

The authored `editorial/003.md` correctly attributes the 7/8 statement to an upstream paper, explains it is not RH, notes the classical Re s > 1 result, and expressly withholds independent proof certification. Its Dirichlet-exception caveat is consistent with the principal-character pole at 1; it does not inadvertently claim a zero at that pole.

**Editorial precision note:** the alternate 11/12 statement is mathematically weaker, not a second independent derivation of 7/8. The separate nine-page Landau–Siegel paper states a conductor-logarithmic exclusion condition. Neither may be silently represented as an independently verified proof of the stronger theorem.

**Coverage limit:** checked source introduction and displayed main theorem/abstract, not all pages of 199+49+9 or their proof dependencies, imported Lean definitions, or a global comparison/certification. Existing MATHFORGE WP03 proposition alignment remains partial and a deliberate `sorry` placeholder does not establish a proof.

Verdict: `PINNED_THEOREM_STATEMENT_FIDELITY_PASS / PROOF_NOT_CERTIFIED`. Exact authored article Git blob: `f9fc5050ad0544268f003531f33c5dfc178976ea`.
