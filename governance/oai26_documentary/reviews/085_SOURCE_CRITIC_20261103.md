# OAI26 Family 085 — bounded primary-source critic

**Pinned revision:** `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`.

The primary evidence inspected is the introduction of `preprints/An-Endpoint-Gradient-Bound-for-the-Centered-Disk-Maximal-Operator-September-26-2026/article.pdf` and its `build/sections/introduction.tex`, together with the publisher's `lean/docs/085.md`.

## Claim and limits

The source theorem concerns **real-valued** inhomogeneous W^{1,1} functions on the **Euclidean plane** and all positive radii of **centered disks**. It claims local W^{1,1} regularity of the maximal average of absolute values and a global L1 gradient bound with one absolute constant. It does not claim global L1 integrability of the maximal function, the sharp constant, higher dimensions, different shapes, or a BV extension.

The signed finite-band auxiliary estimate concerns signed disk averages of smooth compactly supported data, with a constant independent of the dyadic radius-band depth. This is distinct from an unsigned maximum. The proof roadmap emphasizes disk moment and shell concentration, scalar cancellation prices, vector direction-path costs and cancellation of differentiated transition rows; the absolute-continuity argument removing singular derivative mass is crucial.

## Critical proof frontier

Independently verify every local shell and moment identity, the uniform finite-band summation, support and mass conservation in scalar cancellation, vector particle birth and refinement, spatial label transition gradient costs, radius-endpoint cancellation, signed cutoff and local mean subtraction, Sobolev approximation and elimination of the singular derivative part. The publisher's Lean scope names SignedFiniteBand and DiskMaximal comparators but does not establish exact formal replay, axiom audit, nonvacuity, or mathematical certification.

**Editorial verdict: SOURCE_SCOPE_REVIEWED_WITH_LIMITS; NO_CERTIFICATION.** Admit only with matching article digest, compendium checks, documentation build, protected CI, merge and main readback.
