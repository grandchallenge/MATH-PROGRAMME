# PNP-WP01 — Executable False-Proof Atlas

**Artifact ID:** `PNP-WP01`  
**Campaign:** `PNP-001`  
**Pillar:** MATHFORGE  
**Status:** `INTERNAL REVIEW COMPLETE — REPOSITORY GATE PENDING`  
**Audit date:** 2026-07-28  
**Claim class:** `ELIMINATIVE / NON-SOLUTION ARTIFACT`

## Purpose

This package converts the semantic and resource failures identified in WP00 into deterministic rejection fixtures.

The atlas contains **46 fixtures**. Each fixture states:

- an invalid inference;
- the exact missing obligation;
- a minimal witness or scope counterexample;
- a bounded decision, `REJECT` or `NARROW`;
- a remediation route;
- the WP02 theorem interfaces needed to assess that remediation.

The fixtures cover algorithmic hidden cost, uniformity, encoding, total correctness, quantifier drift, restricted models, circuit explicitness, proof complexity, relativization, natural proofs, algebrization, conditional transfers, meta-complexity, algebraic analogues, source maturity, analog precision, succinct representations, and learned-solver overreach.

## Execution

```bash
python campaigns/p_vs_np/WP01_FALSE_PROOF_ATLAS/replay.py
python campaigns/p_vs_np/validate_wp01_wp02.py
python campaigns/p_vs_np/tests/test_validate_wp01_wp02.py
```

A passing replay means only that the fixture package is internally complete and its links resolve. It does not prove that P equals NP, that P differs from NP, or that every possible proof route fails.

## Files

- `01_ATLAS.json` — machine-readable fixture ledger.
- `02_REPLAY_CONTRACT.md` — interpretation and mutation contract.
- `replay.py` — deterministic structural replay.
- `../validate_wp01_wp02.py` — cross-package validation against WP02.
- `../tests/test_validate_wp01_wp02.py` — adversarial mutation tests.

## Promotion boundary

WP01 may be promoted only after repository review and merge. Passing every fixture is an intake condition for a proposed argument, not a proof certificate.
