# GCL Erdős #561 even-cap degree splitting run matrix

| Check | Procedure | Expected |
| --- | --- | --- |
| General mathematical proof | Inspect `EVEN_CAP_DEGREE_SPLITTING_THEOREM.md` | Even regular completion, Euler orientation, bipartite factorization, delete fake edges |
| Constructive degree-four replay | `python3 verify_even_caps_constructive.py` | 685 graph atlas classes + 200 larger seeded examples, zero cap failures |
| Exact three-star parameter audit | `python3 verify_even_cap_parameters.py` | 25 prior entries, three even-cap exclusions, 22 ordered / 11 unordered remaining |
| Even-cap transfer of four infinite ORIGINAL star-forest families | `python3 verify_even_cap_original_transfer.py` | Two antidiagonal index conventions and exact arithmetic for four finite parameter grids; universal transfer analytic, upstream residual proofs retain UNDER_REVIEW |
| Complete replay | `bash run_all.sh` | `EVEN_CAPS_RESEARCH_REPLAY_PASS` |
| Mathematical Markdown preflight | `python3 ci/math_markdown_gate.py --file EVEN_CAP_DEGREE_SPLITTING_THEOREM.md` | PASS |
| Canonical claim ledger | Validate `CLAIM_LEDGER.json` with `schemas/claim_ledger.schema.json` | Exact computation CHECKED; broad graph theorem and conditional Ramsey implications scoped |
| Source hashes | `sha256sum -c SHA256SUMS.txt` | Every file matches |

`verify_even_cap_parameters.py` reads the protected upstream certificate by default at `../unique16/SIXTEEN_TO_EIGHTEEN_PARAMETER_CERTIFICATE.json`. When running before the prerequisite PR merges, override with `UPSTREAM_561_UNIQUE16_CERTIFICATE=/path/to/pinned-input.json`. `verify_even_caps_constructive.py` uses NetworkX 3.4.2 for graph enumeration/Euler/matching operations; Python 3.10+ is sufficient.
