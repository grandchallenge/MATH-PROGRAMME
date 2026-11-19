# GCL Erdős #561: unique large saturated core research tranche

**Material date:** 2026-11-19. **Claim boundary:** This contains a new paper-level theorem about capped edge-colouring obstructions; the finite three-star consequences rely on the paper-level joint three-star residual theorem already recorded in MATH-PROGRAMME. It is not a complete solution to Erdős #561 and does not newly certify that upstream theorem.

## Main result

For a finite simple graph with degree bound `D=alpha+beta` (both caps positive), if at most `2D+1` vertices have degree exactly `D`, then a degree-capped red/blue partition fails **exactly** when both caps are odd and an isolated connected odd-order `D`-regular component exists. A component of this kind need not be a clique: e.g. `K_(D+3)` minus a Hamilton cycle when `D` is even.

The new three-star integer filter removes 186 of the 339 prior method-surviving ordered small-parameter pairs, leaving 153 candidates for other arguments. This classification is conditional on the existing three-star paper theorem, and the 153 candidates are not necessarily new open problems.

## Evidence and integrity

- `GENERAL_SATURATED_CORE_UNIQUENESS_THEOREM.md`: complete derivation from the ordinary Lovász `(g,f)` factor theorem, including the exact tight-component parity criterion and the explicit avoiding edge-colouring.
- `Erdos561UniqueLargeCore.lean`: 4 source-level kernel-checked general Nat lemmas. `#print axioms` reports only Lean's standard `propext`, `Quot.sound`, and `Classical.choice` as used by classical contradiction; no `sorry`, `admit`, added axioms or `native_decide`. Does not formalize the full ordinary factor theorem.
- `verify_general_core.cpp`: independent C++17 exact graph-colouring and component test on all labelled graphs of 2..6 vertices, plus the connected odd-regular `K_(D+3)` minus cycle family. Compile with `-Werror`.
- `verify_parameter_gate.py`: independent exact integer parameter audit from fresh loops and antidiagonal weights, not importing the previous verifier.
- `GENERAL_CORE_PARAMETER_CERTIFICATE.json`: 186 excluded and 153 remaining ordered cases with exact lists and SHA-256 digest.
- `RUN_MATRIX.md`, `EXECUTION_EVIDENCE.json`, `CLAIM_LEDGER.json` and `SHA256SUMS.txt`: run protocol, local execution evidence, canonical scoped claims and content lock.

## Governance

This is a research-evidence package. The new general graph classification and downstream Ramsey corollary remain paper-level `UNDER_REVIEW` until substantive mathematical admission. No new approval ceremony is needed merely to store reproducible research in protected main under delegated policy; do not relabel these claims MATHCERT or publicly certified. The general Erdős #561 conjecture is still OPEN.
