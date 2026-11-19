# Erdős #561 graph-level Lean run matrix

| Gate | Operation | Expected result |
| --- | --- | --- |
| ENV | `lean --version` | Lean `4.33.0-rc1`, commit `62eed1db4d67327ec8120be05f1a1b0847d74561` |
| GRAPH | `lean Erdos561GraphHandshake.lean` | Graph handshake, saturated edge/vertex budgets, low-slack exact-core theorem; only standard Lean axioms |
| SEMANTIC | `lean Erdos561FourVertexCore.lean` | Exhaustive four-vertex canary, 64 graph masks; triangle obstruction |
| SOURCE | `sha256sum -c SHA256SUMS.txt` | Entire pinned file set matches |
| LEDGER | Canonical JSON Schema | Exactly two narrow formal statements |
| MATH-MD | `python3 ci/math_markdown_gate.py --file FORMAL_SCOPE.md` | Source safe for mathematical rendering |

Compiler success does not prove the Lovász-factor implication or full three-star Ramsey theorem.
