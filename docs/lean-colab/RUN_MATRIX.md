# Lean/Colab skill execution matrix

| Mode | Entry | Expected | Authority |
| --- | --- | --- | --- |
| discover | python3 ci/gcl_lean_colab_jobs.py list | Registered bounded jobs | offline |
| lock | python3 ci/gcl_lean_colab_jobs.py verify | Exact source and worker digests | offline |
| selftest | python3 ci/gcl_lean_colab_jobs.py selftest --job ERDOS-041-FINITE-001 | No allocation, hostile host tests | offline |
| preflight | python3 ci/gcl_lean_colab_jobs.py preflight --job ERDOS-041-FINITE-001 | Live Project AVAILABLE and source custody | authenticated read |
| execute | python3 ci/gcl_lean_colab_jobs.py execute --job ERDOS-041-FINITE-001 | Pinned Lean, exact receipt, stop | protected main and authenticated Colab |
| mutation | Change registered source or worker | fail closed | offline |
| failure | Wrong Lean, failed download, RED/forged receipt | no claim, preserved one-shot ticket | host |

Codex authors the mathematical claim. A computational GREEN means only the exact compiler invocation succeeded; historical source-semantic review remains separate.
