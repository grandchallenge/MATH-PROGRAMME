# Erdős #561 — bounded proof evidence (research only)

**Proof claim:** `rhat(F(4,2,2),F(4,3,1))=24` for finite simple graphs, where `F` is the vertex-disjoint union of the stated stars. This is one fixed, asymmetric, three-star-versus-three-star instance; the unrestricted conjecture is open.

This directory makes the evidence from [GCL research #3490](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3490) and [certification gate #3502](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3502) reproducible **without** merging a mathematical acceptance into protected main.

## Contents

- `ERDOS_561_FULL_422_431_PROOF.md` — original fixed 24-edge proof reconstruction.
- `EXACT_JOINT_422_431_PROOF.md` — exact 17-edge coupled residual proof.
- `exact_degree5_residual.py` — standard-library Python 11,197-case classifier (historical hardcoded output removed for portability).
- `exact_degree5_cpp_replay.cpp` — independently implemented standard C++17 classification.
- `exact_joint_upper.py`, `exact_original_upper.py` — exhaustive 630- and 5,040-case upper host checks.
- `K_APEX_THEOREM.md`, `k_apex_colouring.py` — new general independent-`k`-apex colouring theorem and stdlib-only constructive tests.
- `CRITICAL5_REPLACEMENT_PROOF.md`, `critical5_atlas_verify.py` — replacement for the unavailable 1994 density-proof dependency; Vizing adjacency lemma plus exact seven/eight-vertex atlas census.
- `fixtures/graph7.g6`, `fixtures/graph8.g6` — original McKay complete unlabeled graph catalogues, CC BY 4.0 with attribution and fail-closed source hashes.
- `SOURCE_LOCK.md` — precise external input contract and historically open but mathematically superseded 1994 source-lock gap.
- `claim_ledger.json` — schema 1.1.0 source- and scope-aware claims, not a certification stamp.

## Reproducibility

```bash
cd research/erdos-561
bash run_certificates.sh
```

Expected: the Python and C++ classifiers each test 11,197 extensions, finding two labelled isomorphic survivors; upper-host checks pass 630 and 5,040 assignments; `k_apex_colouring.py` passes 3,000 deterministic cases for `k=1..4`.

The replay is deliberately a research-directory script rather than a new GitHub Actions workflow: additional workflows require protected GH-OS routing registration and cannot be introduced by this ordinary research PR. The run can be executed in existing runner environments, including CHAD, without GitHub Actions configuration changes.

## Promotion restrictions

These scripts contain exact finite computations and a paper-level reduction using a Vizing's adjacency lemma and the pinned finite critical-graph census. There is **no** Lean proof, external second-author review, proof of the superseded original Kayathri 1994 text (no longer required), or proof of the unrestricted conjecture. Follow `CERTIFICATION_LADDER.md` and the protected review gates before substantive mathematical acceptance.
