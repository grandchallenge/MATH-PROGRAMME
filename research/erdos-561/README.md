# Erdős #561 — bounded proof evidence (research only)

**Proof claim:** `rhat(F(4,2,2),F(4,3,1))=24` for finite simple graphs, where `F` is the vertex-disjoint union of the stated stars. This is one fixed, asymmetric, three-star-versus-three-star instance; the unrestricted conjecture is open.

This directory makes the evidence from [GCL research #3490](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3490) and [certification gate #3502](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3502) reproducible **without** merging a mathematical acceptance into protected main.

## Contents

- `ERDOS_561_FULL_422_431_PROOF.md` — original fixed 24-edge proof reconstruction.
- `EXACT_JOINT_422_431_PROOF.md` — exact 17-edge coupled residual proof.
- `exact_degree5_residual.py` — exact Python 11,197-case classifier (historical hardcoded output removed for portability).
- `exact_degree5_cpp_replay.cpp` — independently implemented standard C++17 classification.
- `exact_joint_upper.py`, `exact_original_upper.py` — exhaustive 630- and 5,040-case upper host checks.
- `K_APEX_THEOREM.md`, `k_apex_colouring.py` — new general independent-`k`-apex colouring theorem and stdlib-only constructive tests.
- `SOURCE_LOCK.md` — precise external input contract and **still open** primary source-lock gap.
- `claim_ledger.json` — schema 1.1.0 source- and scope-aware claims, not a certification stamp.

## Reproducibility

```bash
cd research/erdos-561
python3 exact_degree5_residual.py
c++ -std=c++17 -O2 -o /tmp/erdos561-cpp exact_degree5_cpp_replay.cpp
/tmp/erdos561-cpp
python3 exact_joint_upper.py
python3 exact_original_upper.py
python3 k_apex_colouring.py
```

Expected: the Python and C++ classifiers each test 11,197 extensions, finding two labelled isomorphic survivors; upper-host checks pass 630 and 5,040 assignments; `k_apex_colouring.py` passes 3,000 deterministic cases for `k=1..4`.

## Promotion restrictions

These scripts contain exact finite computations and a paper-level reduction using a published edge-critical graph theorem. There is **no** Lean proof, external second-author review, proof of original Kayathri source in this PR, or proof of the unrestricted conjecture. Follow `CERTIFICATION_LADDER.md` and the protected review gates before substantive mathematical acceptance.
