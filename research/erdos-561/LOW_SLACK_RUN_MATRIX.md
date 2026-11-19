# Run matrix

| Gate | Verification | Exact expected result |
| --- | --- | --- |
| GRA-01 | `verify_core_isolation.py` | 77 eligible graph atlas classes; 172 cap tests; 20 isolated-clique odd/odd failures |
| TRI-01 | `verify_three_star_low_slack.py` | 4,566 small ordered pairs; 851 baseline; 316 new exclusions; 535 retained |
| TRI-02 | `verify_three_star_independent.py` | Same 316 exact ordered pairs with sorted-set SHA-256 `d2d741b5432bacce00fc5fc2a7394b54f966c66c9478dcbcb0e4e6b5e33df91b` |
| PRO-01 | Independent mathematical proof audit | Lovász factor cut parity, degree-sum bound, exact D+1 saturated classification, leaf-colouring inequality and upstream joint-residual dependency |
| GOV-01 | Protected review policy | Claim remains `UNDER_REVIEW`, draft PR only; no protected certification, full #561 remains OPEN |