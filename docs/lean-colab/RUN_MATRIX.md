# Lean/Colab skill execution matrix

| Mode | Entry | Expected | Authority |
| --- | --- | --- | --- |
| discover | python3 ci/gcl_lean_colab_jobs.py list | Registered bounded jobs | offline |
| lock | python3 ci/gcl_lean_colab_jobs.py verify | Exact source and worker digests | offline |
| selftest | python3 ci/gcl_lean_colab_jobs.py selftest --job ERDOS-041-FINITE-001 | No allocation, hostile host tests | offline |
| preflight | python3 ci/gcl_lean_colab_jobs.py preflight --job ERDOS-041-FINITE-001 | Live Project AVAILABLE and source custody | authenticated read |
| execute | python3 ci/gcl_lean_colab_jobs.py execute --job ERDOS-041-FINITE-001 | Pinned Lean, exact receipt, stop | protected main and authenticated Colab |
| 248 selftest | python3 ci/gcl_lean_colab_jobs.py selftest --job ERDOS-0248-LEAN-REPLAY-001 | 17 hostile/contract checks, pinned upstream patch locks; no Colab allocation | offline |
| 248 preflight | python3 ci/gcl_lean_colab_jobs.py preflight --job ERDOS-0248-LEAN-REPLAY-001 | Authenticated Project #2 open/available and pinned source/host/worker digests | authenticated read |
| 248 execute | python3 ci/gcl_lean_colab_jobs.py execute --job ERDOS-0248-LEAN-REPLAY-001 | Pinned provider + declared post_update compatibility patches; full compiler/axiom/log receipt and teardown | clean exact protected main, Colab OAuth |
| mutation | Change registered source or worker | fail closed | offline |
| failure | Wrong Lean, failed download, RED/forged receipt | no claim, preserved one-shot ticket | host |

Codex authors the mathematical claim. A computational GREEN means only the exact compiler invocation succeeded; historical source-semantic review remains separate.

The first #248 run (PR #3406 worker) exited RED in two unpatched BoundedGaps modules. The next worker revision must use the provider-declared, hash-locked Lake post_update patches before building. The original RED receipt and complete archived logs are preserved under governance/erdos_proof_verification/evidence/0248/LEAN_REPLAY_RED_001.*. Never delete the first attempt ticket or report a patched run as an unmodified dependency tree. A replacement worker has a distinct hash and therefore a distinct guarded attempt identity.
