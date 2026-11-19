# Erdős #561 low-degree run matrix

| Gate | Command or check | Expected |
| --- | --- | --- |
| Strict mathematics | `python3 ci/math_markdown_gate.py --file LOW_DEGREE_CLOSURE_THEOREMS.md` | PASS |
| Exact C++ compilation | `c++ -std=c++17 -O2 -Wall -Wextra -Werror -o /tmp/erdos561_d2 verify_degree2_exhaustive.cpp` | Zero warnings/errors |
| Complete D2 C++ search | `/tmp/erdos561_d2` | Six target pairs, 1,356 graph types, zero arrowing hosts |
| Independent D2 Python search | `python3 verify_degree2_independent.py` | Same 1,356 graph types, zero arrowing hosts |
| Sharp D3 obstruction | `python3 verify_cubic_sharpness.py` | 16 edges, ten saturated vertices; matching cover impossible, A=1<q=2 |
| Upstream-gated exact case audit | `python3 verify_lowdegree_ledger.py` | 75 input; 25 new-method; 12 published; 1 overlap; 39 residual, 20 unordered |
| Protected content integrity | `sha256sum -c SHA256SUMS.txt` | All files match |
| Canonical ledger schema | Validate `CLAIM_LEDGER.json` against `schemas/claim_ledger.schema.json` | All claims scoped and no unrestricted certification |

For a complete standalone runtime, invoke `bash run_all.sh` after setting the upstream certificate path if not running in the repository layout. The Python independent exhaustive search may take tens of seconds on a CPU; there is no GPU dependency. No repeated dynamic GitHub calls occur inside the tests.
