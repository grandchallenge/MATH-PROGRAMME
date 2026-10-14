# EC-BULK-007 — Erdős #1115 predetermined critical sample

**Disposition: PRIMARY-COMPLEX-ANALYSIS-AND-INDEPENDENT-CRITICAL-REVIEW-PENDING.** Not an accepted mathematical article or completed sample review.

Maintained catalogue: https://www.erdosproblems.com/1115 (SOLVED by a negative counterexample, Dec 2025).
Authenticated source return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2386#issuecomment-6168872310
Unaccepted draft: governance/erdos_compendium/editorial/1115.md

## Exact assertion and published counterexample interface

For an entire finite-order f, can one ALWAYS find an unbounded rectifiable path Gamma with |f(z)|->infinity and arc length ell(r)=O(r) inside disk |z|<r? The universal assertion is externally reported DISPROVED by Gol'dberg–Eremenko (1979), who construct counterexamples with log M(r) << phi(r)(log r)^2 for ANY phi(r)->infinity, even with arbitrary prescribed finite order.

Beware distinguishing:
- existence of some f with a short escape path vs all finite-order f;
- f(z)->infinity vs |f(z)|->infinity;
- rectifiable globally vs locally rectifiable unbounded escape path;
- a growth upper bound on log M(r) vs a lower bound on minimal path length;
- any prescribed finite order, including zero, vs merely some finite order.

Source must settle these conventions, not an editor's inference.

## Independently verified bounded elementary interface

For f(z)=exp(z) and Gamma(t)=t>=0, M(r)=exp(r), ell(r)=r, |f(Gamma(t))|=exp(t)->infinity, and f has finite order one. This positive example illustrates that a short path can exist in special cases; it does not prove the universal theorem and does not construct a Gol'dberg–Eremenko obstruction.

Reproducible script: ci/erdos_compendium_007_phase12_checks.py

## Required before approving critical sample

1. Locate, hash and read Hayman's 1960 result and 1974 Problem 2.41 original context, with attribution provenance.
2. Read Gol'dberg–Eremenko 1979 actual counterexample proof and extract all quantifiers, finite-order construction and path definition.
3. Verify every reported phi/log M upper bound and absence-of-O(r)-escape-path conclusion at theorem level; distinguish order zero.
4. Conduct independent mathematical/expository critical review, explicitly confirming no claim of novel theorem or Lean kernel certification.
5. Only then record APPROVE or REVISE and update the deterministic sample count.

Status remains REVIEW_PENDING. No protected manuscript admission or public cohort deployment claimed.
