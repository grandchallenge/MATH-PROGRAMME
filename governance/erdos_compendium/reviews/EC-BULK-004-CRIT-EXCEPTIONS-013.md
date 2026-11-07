# EC-BULK-004 — Erdős #466 adversarial source and mathematical review

Receipt: EC-BULK-004-CRIT-EXCEPTIONS-013  
Observed: 2026-10-14  
Accountable GitHub identity: fyremael  
Authority: documentary editorial scrutiny after initial drafting, not independent-person review, new theorem certification, or protected editorial admission.

## Primary-source and semantic audit

The exact original Erdős–Graham monograph (1980), **printed pp. 92–93** (PDF zero-based pp. 87–88), was inspected visually: source https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf#page=89 . The distance rule is nearest-integer norm of the **Euclidean distance** and points lie in a radius-X circular region, not necessarily on the circumference. The original question is $\exists\delta>0:\lim_{X\to\infty}N(X,\delta)=\infty$; no changing $\delta$ with the target point count is allowed.

The original p.93 explicitly reports Graham's $N(X,1/10)>(\log X)/10$ and Sárközy's $N(X,\delta)>X^{1/2-\varepsilon}$ when $\delta\le\delta(\varepsilon)$ and X is sufficiently large. These are accepted historical *published-source claims*, not independent GCL replication of either quantitative proof.

Primary Goenka–Moore arXiv:2605.06621v1, first printed page, introduction, equation (1.1), directly inspected, corroborates the planar historical lower and upper quantitative rates. Its own Theorems 1.2/1.3 concern higher dimensions and are not confused with solving #466. Konyagin's $O_\delta(X^{1/2})$ upper theorem concerns neighboring #465.

The maintained page reports an explicit $1/2-\delta^{1/7}$ exponent; the inspected 1980 page has only $\delta(\varepsilon)$. Full Sárközy 1976 proof is not independently read, so explicit exponent stays a **source-fidelity exception**, not a source-locked historical theorem.

## Adversarial mathematical checks

- Four rational-coordinate square vertices $(\pm3/4,\pm3/4)$ lie inside a disk of radius 2. Four pairwise distances are $3/2$, two are $3\sqrt2/2$. Exact rational squaring gives $(21/10)^2<9/2<(5/2)^2$, so the diagonal nearest-integer distance exceeds $1/10$; edges have gap $1/2$. Hence $N(2,1/10)\ge4$, independent of floating-point calculations.
- The manuscript's separate **nonquantitative** qualitative proof uses existence of configurations with rationally independent pairwise distances. Challenge: why can no nonzero rational linear combination of the planar distance functions vanish identically? Holding all other points separated and letting one selected pair collide gives a cusp for its selected distance, while all others extend differentiably. Thus any identically vanishing combination has every coefficient zero. Nonzero real-analytic functions on connected distinct-point configuration space have measure-zero zero sets; countably many rational relations leave a generic configuration with rationally independent distances.
- For those finitely many independent distances, the classical real-time Kronecker density theorem gives a *single* positive scale t making **every** distance's fractional part lie in $(1/4,3/4)$. This yields $N(X,1/4)\ge n$ for all X≥t for arbitrary fixed n. This is a reconstruction using established genericity/Kronecker mathematics and does not recreate Graham's *effective* logarithmic bound.
- A finite square example by itself does not imply the limit, a point often mishandled in elementary summaries. The manuscript separately supplies the uniform fixed‑$\delta$ quantifiers and derives the limit from the classical theorem.

## Reproducibility and hash custody

Authenticated original issue RESULT/1: https://github.com/grandchallenge/MATH-PROGRAMME/issues/1736#issuecomment-6166375563, author fyremael, comment LF-normalized SHA-256 **162e872cd1b5382b13ab601f5cb5589b7e4c18e65c04e7fdfb7cceecbc93d13f**. Disposition SOURCE_LOCK_READY documentary; cannot imply formal GCL proof certification.

Manuscript: governance/erdos_compendium/editorial/0466.md; SHA-256 of stripped UTF-8 **ef27bd7d3245feb880fbeb4abe273ba8089e59bc8ba06b8783bd9e77d937ce9f**, raw file SHA-256 **5f7e2711f1bbd7930d2ce31ff25eeb793ce99d5dc6b5fb61fd77c02c8dbef384**. Six required heading names appear exactly once, math-dollar pairs are balanced.

Finite exact fixture: tests/test_erdos_compendium_0466_square.py; 3 tests passed. Full Compendium run on exact branch head 4743a4bec5097f0d7f924c9240ac0460536d5af7: **108 tests + 517 subtests passed**, receipt 6cd8bfffbd09466a9e48f6b10d7dd415. **Strict MkDocs build succeeded** on that head, receipt 876fbfd5341944af8fbf8606ea155d68. This is a local build, **not** browser MathJax verified public deployment.

## Editorial decision

CRITICAL_DRAFT_PASS_PENDING_PROTECTED_BATCH_ADMISSION. The nontrivial exact original question is reported PROVED, with appropriate source attribution and unresolved *proof provenance* of original quantitative sources. Do not claim source audit of complete 1976 Sárközy paper, a new theorem, novelty, independent-person mathematical review, Lean replay or MathCert.

This is an additional exception review, **not a substitute** for the mandatory final deterministic 20-article sample. Protected full-200 cohort production PR, public browser formula verification, and V2 admission remain pending.
