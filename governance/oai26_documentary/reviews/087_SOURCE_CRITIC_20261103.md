# OAI26 Family 087 — bounded source critic

**Source lock:** `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`.
Inspected three pinned preprint introductions: `The-symmetric-Mahler-conjecture-and-its-equality-cases-September-22-2026`, `The-Mahler-Conjecture-for-General-Convex-Bodies-September-22-2026`, and `Symplectic-Balls-in-Symmetric-Polar-Products-September-22-2026`; also `lean/docs/087.md`.

## Three distinct mathematical claims

The symmetric manuscript claims the inequality at constant 4^n/n! for origin-symmetric bodies, with equality precisely at linear Hanner bodies. The general manuscript instead uses the polar centered at the Santaló point and claims constant (n+1)^(n+1)/(n!)^2 with simplex equality for all convex bodies. The symplectic manuscript claims Gromov width four for the interior of a symmetric body times its polar, with smooth embeddings at all *strictly smaller* capacities; the width result implies a symmetric Mahler lower bound through volume, not Hanner equality.

## Exclusions and independent audit obligations

No functional Mahler or entropy-transport corollary is covered by the selected comparator descriptions. The symplectic source does not assert an embedding at exact capacity four. Source existence and publisher Lean scope are not proof certificates. Review of the symmetric holomorphic mass and feasible-simplex normalization, metric-median equality reduction, general Gaussian matrix layer and scalar inequalities, and symplectic holomorphic ball and uniform boundary-slice arguments remains outstanding. Each comparator requires exact hypotheses, dependency/nonvacuity audit, and independent replay.

**Editorial verdict: SOURCE_SCOPE_REVIEWED_WITH_LIMITS; NO_CERTIFICATION.** Protected documentary admission requires exact article hash, compendium regression, strict rendering, CI and main readback.
