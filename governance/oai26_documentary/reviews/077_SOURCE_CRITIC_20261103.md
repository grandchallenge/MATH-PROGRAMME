# OAI-26 Family 077 — bounded primary-source critical review

**Source pin:** `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`.

The two manuscript identities are (1) `preprints/Elliptic-capacity-propagation-and-Fourier-restriction-to-the-sphere-September-24-2026/Elliptic-capacity-propagation-and-Fourier-restriction-to-the-sphere-September-24-2026.pdf` and (2) `preprints/Diagonal-Fourier-extension-for-positively-curved-surfaces-in-three-dimensions-September-24-2026/Diagonal-Fourier-extension-for-positively-curved-surfaces-in-three-dimensions-September-24-2026.pdf`.

**Inspected:** exact-pinned primary TeX introductions, displayed main theorems and extended methodological overviews for both manuscripts. Not inspected: complete proof bodies, all dependent results, numerical constants, or any formal dependency closure. No claim of independent validation is justified.

**Source-bound claim 1:** the sphere manuscript asserts a bounded-input Fourier extension bound for every exponent strictly above three, with no endpoint assertion. The constant-input example demonstrates divergence at or below three. The stated sphere-specific factorization and Kakeya maximal consequences are separate deductions, not automatic general-surface claims.

**Source-bound claim 2:** the companion manuscript asserts a diagonal bound with equal finite-power input and output norms for all compact smooth positively curved surfaces in three dimensions, including smooth boundaries, for each finite exponent above three. Its stated proof uses both the packet propagation result and a separately established Kakeya maximal theorem; the latter is not proved merely by the bounded-input sphere theorem. Its Schrödinger local smoothing and oscillatory-integral corollaries require additional hypotheses and should not be generalized.

**Critical checks still required:** independently replay the elliptic-capacity propagation and hairbrush bounds; frame normalization and masking for arbitrary finite complex arrays; geometric-to-analytic conversions; strength and compatibility of the Kakeya input; chart continuations, boundary charts, sparse-ball epsilon removal, and exponent-dependent loss accounting. The pinned introductions establish statement and method fidelity only.

**Verdict:** SOURCE_SCOPE_REVIEWED_WITH_LIMITS; NO_CERTIFICATION. Editorial admission depends on exact digest, regenerated compendium, strict rendering and protected exact-head merge; mathematical certification is not claimed.
