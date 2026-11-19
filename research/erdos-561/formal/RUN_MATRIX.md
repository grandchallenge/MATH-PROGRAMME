# Run matrix: Erdős #561 formal subclaims

| Gate | Command | Expected result | What it does NOT establish |
| --- | --- | --- | --- |
| LEAN-ENV | `lean --version` | Lean 4.33.0-rc1 / commit 62eed1db | Proof semantics |
| LEAN-ARITH | `lean Erdos561CoreArithmetic.lean` | Four closed universally quantified arithmetic lemmas | Lovász factor or graph handshake |
| LEAN-FINITE | `lean Erdos561Finite.lean` | 84 triples; all 7,056 ordered pairs; 82=74+8 finite gate; no axioms for finite closed theorems | Ramsey reduction to arithmetic |
| SRC-LOCK | `sha256sum -c SHA256SUMS.txt` | All listed bytes match (run without writing result files to source tree) | Independent mathematical review |
| REFEREE | GitHub PR #3523 requested reviewer `jimsteeg` | Authenticated non-author review disposition, pending | Not satisfied by dispatch alone |

From the directory run `bash run_lean.sh`. The script checks the pinned compiler release, forbids common proof placeholders and runs both modules; its output logs are local evidence, not mathematical certification.
