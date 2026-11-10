# OAI26 Family 019 — bounded review of two pinned original papers

**Scope:** Primary-source *statement fidelity* only. This review does not check the full proofs, the cited mathematical literature, any Lean equivalence, or MATHCERT certification.

Source lock: `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`.

Both original PDFs were downloaded at the pinned revision and raw-byte Git blob hashes matched the authenticated GitHub metadata:

- `preprints/Etale-covers-with-a-prescribed-exterior-sheet-September-24-2026/main.pdf`: 7 pages, 319,576 bytes, Git blob `7d753179e1b93b742dd3640b2bc7e1e9704f2afd`, SHA-256 `713430a73f1530f5d89cd38050c45a6bc2ccc458878a191917bb37b451b2f26a`.
- `preprints/The-p-adic-section-conjecture-October-6-2026/main.pdf`: 24 pages, 491,950 bytes, Git blob `5d83521ccc50a2c7f990474b14841a982f1bcefc`, SHA-256 `f3c8d6f784d6bae48305f6959c44c7cc337f9c2b6078d93a5595d317b3a82f40`.

## Principal statements and qualifications

*Exterior-sheet paper*, page 1, Theorem 1.1: Fix a prime p, finite extension k/Q_p, algebraic closure and its completion Omega. For a **smooth proper connected hyperbolic curve over the algebraic closure**, choose disjoint coordinate disks and strictly smaller specified open disks V_i. Require that the compact exterior U after removing the V_i is nonempty and contains an Omega-rational point. The paper asserts a **single connected finite étale cover** for which one connected component above U maps isomorphically onto U, while **every connected component** above **each specified** V_i has degree divisible by p. It does **not** replace the prescribed V_i by smaller disks in the conclusion. This is a simultaneous cover construction, **not** a section-conjecture statement. The proof description invokes resolution of nonsingularities, semistable skeleta, graph characters, and a stabilizer quotient. The cited Mochizuki–Tsujimura resolution input was not independently reviewed.

*Section-conjecture paper*, page 2, Theorem 1.1: For **every prime p** and **every finite extension k/Q_p**, if X/k is smooth, proper, geometrically connected and of genus at least two, the map from X(k) to **continuous sections of the full arithmetic étale fundamental-group exact sequence modulo conjugacy by the full geometric étale fundamental group** is bijective. It claims both surjectivity and injectivity; sections of a quotient group or birational Galois sections are not a substitute. Page 3, Theorem 1.2 is a separate **rank-one valuation completion** theorem used in the claimed proof. Its statement requires chosen copies of the fields in one completion; mere abstract embedding is weaker. Pages 17–18 describe valuations and the point-section reduction.

The local theorem alone does **not** establish the section conjecture for arbitrary number-field curves. The source introduces modified adelic localization and a finite-cover descent locus, then gives Theorem 8.2 on page 20: equality of that locus with diagonal rational points is a sufficient additional hypothesis for global bijectivity. Page 21, Corollary 8.5 applies published Stoll finite-descent results with corrections to claim the global section conjecture for smooth projective modular curves **X_0(N) and X_1(N) over Q of genus at least two**. The claimed modular result is not a theorem for every curve over Q; its descent dependency remains a distinct mathematical obligation.

The revised six-section article reflects these scopes and avoids treating the exterior-sheet covering theorem as a direct proof of the local conjecture, or local point-theoreticity as sufficient for every global case.

**Verdict: ACCEPTED_EXPOSITION_WITH_LIMITS.** Checked against original primary statements: geometric covering hypotheses and disk-level quantifiers, full arithmetic and geometric group conjugacy, local theorem genus and field scope, and the modular-curve corollary's descent dependency. Not checked: completeness of either PDF's proof, the essential non-Archimedean analytic patching and completion claims, independent Pop–Stix / Mochizuki–Tsujimura / Koenigsmann / Harari–Stix / Stoll references, source-to-Lean mapping, Comparator replay, or independent mathematical correctness.

**Claim boundary:** Editorial source fidelity only; NO_CERTIFICATION. Protected admission requires exact revised article SHA-256, mathematical Markdown and compendium tests, generated HTML verification, and protected merge/readback.
