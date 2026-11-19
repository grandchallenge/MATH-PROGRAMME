# Erdős #561 graph-level Lean run matrix

| Gate | Operation | Expected result |
| --- | --- | --- |
| ENV | `lean --version` | Lean `4.33.0-rc1`, commit `62eed1db4d67327ec8120be05f1a1b0847d74561` |
| GRAPH | `lean Erdos561GraphHandshake.lean` | Graph handshake, saturated edge/vertex budgets, low-slack exact-core theorem; only standard Lean axioms |
| SEMANTIC | `lean Erdos561FourVertexCore.lean` | Exhaustive four-vertex canary, 64 graph masks; triangle obstruction |
| SOURCE | `sha256sum -c SHA256SUMS.txt` | Entire pinned file set matches |
| LEDGER | Canonical JSON Schema | Three narrow formal statements plus one separate under-review paper theorem |
| MATH-MD | `python3 ci/math_markdown_gate.py --file FORMAL_SCOPE.md` | Source safe for mathematical rendering |

| LEAN-FACTOR-ARITH | `lean Erdos561FactorCut.lean` | Six general Nat lemmas; source-level #print axioms only `propext`, `Quot.sound` |
| FACTOR-VERIFY | `bash run_bridge.sh` | 33,866 graphs, 91,727 cap splits, 273 obstructions, 2,809 exact factor criteria comparisons |
| FACTOR-MANUSCRIPT | `python3 ci/math_markdown_gate.py --file LOVASZ_CAP_PARTITION_BRIDGE.md` | Renderer-safe complete paper proof; cites ordinary Lovász factor theorem |

Compiler success does not prove the ordinary Lovász `(g,f)` factor theorem or the full three-star Ramsey theorem. The manuscript proves the bridge on paper, using the published theorem.
