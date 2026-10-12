# Erdős 41 finite Lean check — Colab computational lane

Computational-only research evidence, not an accepted theorem about the infinite Erdős #41 problem.

Pinned Lean: `leanprover/lean4:v4.29.1` (the version used in MATHCERT's `lean-toolchain` at design time). The lock is explicit; the remote worker must attest the actual `lean --version` output.

Run locally from the folder containing `lean-toolchain`:

```bash
elan run leanprover/lean4:v4.29.1 lean Erdos41Finite.lean
```

The theorems check the exact finite equality `1+1+3 = 1+2+2` and distinction between triples. This does not prove any infinite statement, historical semantics, or publication-ready mathematics.

Control flow: Codex reasons and writes proof files → authenticated GCL host validates queue and immutable task → Colab executes fixed Lean command with an exact toolchain and time budget → host verifies process exit code, source digest, toolchain and signed/hashed logs → existing authenticated GCL intake captures provisional evidence. Do not install an unpinned model or claim independent MATHCERT approval.
