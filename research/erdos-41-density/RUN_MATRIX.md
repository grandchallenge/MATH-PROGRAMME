# E041 density transfer: bounded run matrix

The present programme separates mathematical proof, computer checking, and conjectural exploration. Code changes are admitted only under protected GitHub checks; proof evidence is not MATHCERT certification.

| Track | Method | Acceptance | State |
| --- | --- | --- | --- |
| E3 two-term padding | Lean 4.29.1 with pinned mathlib | Compiler exit 0; source SHA-256; no admitted holes | Kernel checked |
| Source-index affine H3 | Lean 4.29.1 with pinned mathlib | Compiler exit 0; source SHA-256; no admitted holes | Kernel checked |
| Affine cubic growth | Lean 4.29.1 core | Compiler exit 0; source SHA-256; no admitted holes | Kernel checked |
| Actual image H3 | Full written proof | Inverse of injective affine image and sum/card identity | Written proof; not a separate kernel theorem |
| Counting liminf equivalence | Full written proof | Ordered enumeration and counting growth equivalence | Written proof; not a separate kernel theorem |
| Finite adversarial replays | Python standard-library unittest | Exact E3-to-H3 prefixes, count identity, M3 countercase | Four tests passed |
| Multiscale M3 packing | Elementary written proof | Number of three-term multisets fits into sum range | Proved elementary lemma |
| Dyadic shell-energy deficit | OPEN new claim | Independent proof or counterexample | Unresolved; no solution promotion |

The source-locked proof files use Lean 4.29.1; mathlib git commit 5e932f97dd25535344f80f9dd8da3aab83df0fe6. Colab is not used to certify this mathematical result; the local authenticated CHAD Lean compiler supplies verification and provenance. A new Colab job would need explicit protected registration and an authorized issue, rather than reusing the previous finite #41 one-shot receipt.

## Shell-energy adversarial audit, October 2026

| Task | Evidence | Disposition |
| --- | --- | --- |
| Finite cubic convolution inequality | [SHELL_HARDY_AUDIT.md](SHELL_HARDY_AUDIT.md), rational arithmetic tests | Written proof, Lean 4.29.1 checks the cubic two-term identity with exit 0, plus 5 exact Python test methods |
| Critical-density shell/cesaro equivalence | Quantitative constants 1/288 and 1 in finite inequality (2) | Proved for any nonnegative shell occupancies |
| Packing-only hostile profile | Rare empty dyadic-shell gaps, limit 7/12 for shell energy | Refutes derivation from ordinary cubic packing plus density dips, **not** an M3 counterexample |
| Exact M3 finite-window valleys | Equivalent statement (V), powered by uniformly bounded u_k | Proved, conditional on the standard packing bound |
| Original M3 shell-energy deficit | Docket #2622, multiscale gate | OPEN, stronger target |

This audit does not certify the full Erdős conjecture or authorize a new worker task without queue governance.

## Cross-pattern Hall method audit

| Bound | Status |
| --- | --- |
| Generic shell-pattern Hall injection | Elementary written proof; all patterns including repeated shell labels |
| Two-adjacent-shell mixed-pattern inequality | Elementary written proof, arithmetic Lean certificate and hostile x=y=7 fixture |
| Universal-Hall counterprofiles, gapped and ungapped | Written infinite proof; seven new deterministic tests of numeric and actual finite M3 fixtures |
| Original finite-window valley for actual M3 | OPEN: range-only Hall constraints are insufficient |

Consult [CROSS_PATTERN_HALL.md](CROSS_PATTERN_HALL.md). A feasible shell-occupancy profile need not be an M3 set.
