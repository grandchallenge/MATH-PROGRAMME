# Source-locked Lean/Colab worker skill

**Owner:** MATH-PROGRAMME. **Computational authority:** unadjudicated evidence only.

The local Codex skill is at .agents/skills/gcl-lean-colab/SKILL.md. The protected job discovery API is ci/gcl_lean_colab_jobs.py, driven by governance/lean_colab/JOBS.json. New jobs require an exact source digest, worker digest, CPU budget, Lean toolchain pin, authenticated queue binding, concrete worker adapter, and tests. Generic untrusted payload execution is not allowed.

For live work the dispatcher enforces a clean checkout at the actual remote protected main head. Each registered adapter independently enforces authenticated Project queue readiness, one-shot attempt tickets, pinned runtime, receipt validation and teardown. Neither the skill nor Colab confers reviewer independence, source acceptance, Solve authority, Cert authority or publication authority.

Initial registered job ERDOS-041-FINITE-001 provides a pinned Lean 4.29.1 CPU arithmetic canary, with elan v4.2.4 release archive SHA-256 attestation. Mathlib-intensive proofs need a separate pinned environment and reviewed adapter; the initial arithmetic canary must not be misrepresented as an unrestricted mathlib runner.
