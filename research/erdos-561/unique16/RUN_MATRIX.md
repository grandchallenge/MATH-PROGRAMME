# Erdős #561 — 16-edge uniqueness run matrix

| Check | Command | Expected |
| --- | --- | --- |
| Source proof Markdown | `python3 ci/math_markdown_gate.py --file UNIQUE_16EDGE_SUBCUBIC_OBSTRUCTION.md` | PASS |
| Finite cut-pattern classification | `python3 verify_cut_profiles.py` | Exactly 72 profiles, only `(5,5)` with weighted boundary one each |
| Five-vertex block uniqueness | `python3 verify_five_vertex_block.py` | All 1,024 labelled five-vertex graphs checked, 30 degree-profile matches, one isomorphism type |
| Explicit motif/target avoidance | `python3 verify_motif_colorings.py` | Graph has 16 edges; each colour support has 6 vertices; four ordered cases excluded |
| Input provenance | SHA-256 of `../lowdegree/LOWDEGREE_75_CASE_LEDGER.json` | `eb9fee1ee3472b2ae7490b0b104e4a896a2be41914055057aff36db59c7201f0` |
| All computations | `bash run_all.sh` | `ERDOS561_UNIQUE16_SOURCE_REPLAY_PASS` |
| Canonical claim ledger | Validate `CLAIM_LEDGER.json` with `schemas/claim_ledger.schema.json` | Narrow finite calculation CHECKED; general paper theorem UNDER_REVIEW |
| SHA-256 manifest | `sha256sum -c SHA256SUMS.txt` | Every source file byte-identical |

This does not formally prove the ordinary Lovász theorem or promote unrestricted Erdős #561.
