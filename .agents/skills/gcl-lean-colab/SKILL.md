---
name: gcl-lean-colab
description: Submit frozen Lean proofs and bounded computational jobs to authenticated CPU Colab, retaining exact GCL provenance. Never use model inference or claim mathematical certification.
---

# GCL Lean/Colab computational worker

Codex does mathematical research, writes Lean, and performs adversarial reasoning. Colab runs Lean and CPU horsework. GitHub governs job allocation and evidence.

The protected dispatcher is ci/gcl_lean_colab_jobs.py. From an authenticated GitHub operator in MATH-PROGRAMME:

1. python3 ci/gcl_lean_colab_jobs.py list
2. python3 ci/gcl_lean_colab_jobs.py verify
3. python3 ci/gcl_lean_colab_jobs.py selftest --job ERDOS-041-FINITE-001
4. python3 ci/gcl_lean_colab_jobs.py preflight --job ERDOS-041-FINITE-001
5. Only from exact clean protected main, with verified queue and Colab OAuth: python3 ci/gcl_lean_colab_jobs.py execute --job ERDOS-041-FINITE-001

Do not upload provider tokens or run language models in Colab. The job adapter must record exact source and worker SHA-256, Lean pin, process exit, receipt, CPU usage and clean teardown. A RED result reserves its one-shot attempt; create a protected successor rather than retrying silently.

To extend the skill, add an explicit protected entry to governance/lean_colab/JOBS.json, a bounded adapter and worker, exact hash and queue lock, and hostile CI tests. Do not point live execution at arbitrary user files.

See docs/lean-colab/SPEC.md and docs/lean-colab/RUN_MATRIX.md. A passing compiler result does not certify historic semantics, solve Erdős problems or authorize MATHCERT.
