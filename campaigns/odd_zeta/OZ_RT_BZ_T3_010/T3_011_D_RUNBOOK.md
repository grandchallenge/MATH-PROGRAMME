# T3-011-D replay

Governed replay entrypoints:

```text
python3 campaigns/odd_zeta/OZ_RT_BZ_T3_010/t3_011_d.py
python3 campaigns/odd_zeta/OZ_RT_BZ_T3_010/verify_t3_011_d.py
python3 tests/test_oz_rt_bz_t3_011_d.py
```

The producer reconstructs the frozen predecessor candidate order and base cokernel witness, then changes only `x_c` to `x_c^2`. It evaluates `(x_c+h_c)^2 S_c(G)-x_c^2 G` and stops at the first exact nonzero cokernel pairing.

The verifier independently reconstructs `x_c^2 Delta_c(G)+(2h_c x_c+h_c^2)S_c(G)`, compares it under the exact T3-011-C rational-function semantic normal form, independently reconstructs the normalized cokernel witness, and verifies the canonical tested prefix and first-nonzero stop rule.

If no independent candidate has nonzero pairing, the 110 `l1` mirrors of the frozen `k1` bank are checked. A negative terminal is valid only after all 311 independent candidates and all 110 mirror-derived checks remain cokernel-invisible.

Do not widen another structural dimension under issue #498, regardless of terminal outcome.