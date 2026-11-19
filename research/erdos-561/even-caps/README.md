# GCL Erdős #561: even-degree cap partition theorem

**2026-11-19.** Elementary, classical graph-factor construction, included here because it eliminates **three** further ordered small three-star cases from the exact source-locked candidate list. The standalone edge-partition theorem does **not** depend on Erdős #561 or the upstream joint residual result.

For **any** even positive degree caps `alpha,beta`, every finite simple graph with maximum degree at most `alpha+beta` can divide its edges into red and blue parts satisfying the two caps. The proof completes a graph to an even regular multigraph, orients Euler circuits, decomposes the resulting regular bipartite graph into matchings, and removes the artificial edges. This is a direct consequence of classical factorization results, not presented as a novel theorem.

For degree four and caps `(2,2)` we implement the construction directly in `verify_even_caps_constructive.py`, checking **685 graph-atlas classes** of at most 7 vertices with degree at most four and **200 larger** seeded random graphs. This is corroborating finite verification, not a replacement for the general proof.

The source-locked parameter audit in `verify_even_cap_parameters.py` reads the preceding exact 25-case certificate from `../unique16/SIXTEEN_TO_EIGHTEEN_PARAMETER_CERTIFICATE.json` (PR #3568, head `afe38d6158a11b8b256d91d6a65d437cdff4dd64`, SHA256 `1ee51aed0080c4b10e5460835dd6a9ec209a45a511dd558d796ce1c64ed51f80`). It removes precisely three `(2,2)`-cap cases, leaving **22 ordered / 11 unordered** method-survivors, all with caps `(1,3)` in some order.

**Boundary:** The universal even-cap graph theorem is unconditional; original size-Ramsey corollaries remain dependent on the unpromoted paper-level joint three-star residual reduction. The unrestricted Erdős #561 conjecture is OPEN.

Files: `EVEN_CAP_DEGREE_SPLITTING_THEOREM.md` (proof), `verify_even_caps_constructive.py` (algorithm and tests), `verify_even_cap_parameters.py` (exact shortlist audit), `EVEN_CAP_PARAMETER_CERTIFICATE.json` (case list), `RUN_MATRIX.md` (replay), `CLAIM_LEDGER.json` (claim scope), `EXECUTION_EVIDENCE.json` (provenance), `SHA256SUMS.txt` (source lock), `run_all.sh` (replay script).
