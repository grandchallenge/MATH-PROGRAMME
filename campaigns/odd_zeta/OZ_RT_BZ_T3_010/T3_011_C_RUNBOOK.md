# T3-011-C replay

Governed replay entrypoints:

```text
python3 campaigns/odd_zeta/OZ_RT_BZ_T3_010/t3_011_c.py
python3 campaigns/odd_zeta/OZ_RT_BZ_T3_010/verify_t3_011_c.py
python3 tests/test_oz_rt_bz_t3_011_c.py
```

The producer's direct path reconstructs raw shifted expressions without using either T3-011-B lifted response generator as authority. The verifier rebuilds the candidate bank through the reverse T3-010-C path, independently evaluates the raw finite difference, checks source-level helper separation, and replays all 311 independent plus 110 mirror-derived response comparisons.

A mismatch is terminal for this audit. Do not repair it by widening the candidate class or rerunning the mathematical search under issue #494.
