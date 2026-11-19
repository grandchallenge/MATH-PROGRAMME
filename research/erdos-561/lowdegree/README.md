# Erdős #561 — low-degree closure and source-version correction

**Research date:** 2026-11-19. This is mathematical research evidence, not an unrestricted solution to Erdős #561.

The general paper theorem: a finite simple graph with maximum degree at most 3 and at most 15 edges **always** admits a red/blue edge split with maximum red degree at most 1 and blue at most 2. A constructed 16-edge graph shows sharpness. The proof uses the audited ordinary Lovász factor theorem for the stronger 9-saturated-vertex core bound, plus Tutte's perfect matching theorem for the 10-vertex cubic case.

A separate **complete bounded exhaustive enumeration** establishes that every graph of maximum degree at most 2 with `W−1` edges for any two three-star targets having largest star of size 2 admits an avoiding red/blue colouring, for all six unordered target pairs. Both a C++17 verifier and an **independent Python verifier** agree on all 1,356 nonisomorphic graph types.

When applied to the already admitted but *not publicly certified* joint 3×3 residual theorem, the new methods cover 25 of the former 75 ordered method-survivors. A strict source/assumption audit finds 12 already settled in 1978/2025 (one overlapping with the 25). Hence **39 remain unaccounted for by these specific arguments**, or 20 unordered under swapping red and blue. These are method-survivors, not necessarily genuine open problems.

**Important literature correction:** arXiv:2606.04439 v1 had an overbroad abstract claiming to resolve the unrestricted star-forest conjecture. Its current July 2026 v3 narrows the paper to size-Ramsey minimal graphs for **uniform** star forests. The current v3 cannot be cited as a full solution to Erdős #561. The exact Theorem 2.6 from Davoodi et al. 2025 requires every component on the nonuniform side to have size at least **2**; this package enforces that premise when counting published prior coverage.

Files:
- `LOW_DEGREE_CLOSURE_THEOREMS.md`: mathematical proof, finite model-class exhaustiveness and source audit.
- `verify_degree2_exhaustive.cpp`: deterministic full C++17 verification over all labelled red/blue edge colourings of each graph type.
- `verify_degree2_independent.py`: independent full enumeration using vertex-disjoint star-embedding masks.
- `verify_cubic_sharpness.py`: exact 16-edge, 10-saturated-vertex obstruction; all edge subsets exhaustively checked as candidate matching sets.
- `verify_lowdegree_ledger.py`: classifies all 75 input entries with strict literature hypotheses and derives 39/20 residual counts.
- `LOWDEGREE_75_CASE_LEDGER.json`: exact pairwise evidence and remaining case list.
- `RUN_MATRIX.md`, `EXECUTION_EVIDENCE.json`, `CLAIM_LEDGER.json`, `SHA256SUMS.txt`, `run_all.sh`: reproducibility and governance records.

**Dependency:** `verify_lowdegree_ledger.py` reads the previously protected-source-locked input `../unique-core/GENERAL_CORE_PARAMETER_CERTIFICATE.json` (use environment variable `UPSTREAM_561_CERTIFICATE` to override this in standalone tests). It does not replicate the 52-kB upstream JSON source in the repository.

**Claim scope:** The finite D2 enumeration is machine exhaustive for its declared bounded domain. The mixed-cap 16-edge theorem is a complete paper deduction from standard graph theory but not full Lean formalization. Its use to determine original three-star size-Ramsey values is **conditional** on the existing, unpromoted joint-residual theorem. All substantive original problem claims remain `UNDER_REVIEW`. The unrestricted conjecture remains OPEN.
