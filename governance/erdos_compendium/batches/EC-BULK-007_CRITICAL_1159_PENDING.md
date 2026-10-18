# EC-BULK-007 — Mandatory independent critical sample #1159

**State: PRIMARY_SOURCE_AND_INDEPENDENT_CRITICAL_REVIEW_PENDING.** The source article and finite evidence are not independent editorial approval, a resolution of the universal plane problem, or Lean certification.

- Original catalogue: https://www.erdosproblems.com/1159
- Authenticated frozen issue return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2430#issuecomment-6184857288
- Draft article: governance/erdos_compendium/editorial/1159.md
- Primary background as reported: Erdős (1981); Erdős–Silverman–Stein (1983), ESS83; Vardi (1999), §4.70; stronger #664
- Programme: ci/erdos_compendium_007_phase18_checks.py; finite receipt governance/erdos_compendium/batches/EC-BULK-007_FINITE_CHECKS_PHASE18.json

## Exact critical statement

For **every** finite projective plane of order $q$ and of **arbitrary coordinatizability**, find a set of points $S$ such that each projective line $\ell$ has

$$
1\le |S\cap\ell|\le C,
$$

where a SINGLE numerical $C>1$ is independent of $q$ and the particular projective plane.

The stated condition allows selecting a whole line when its size is small; some definitions of proper blocking sets forbid this and cannot silently replace the actual problem. A plane of order $q$ has $q^2+q+1$ points and lines; each line has $q+1$ points and any two lines meet in one point. Not every finite projective plane is assumed Desarguesian; testing $\mathrm{PG}(2,q)$ is not all planes.

## Mathematical fixture, exactly verified

The program constructs all normalized 1-dimensional projective classes of nonzero triples over $\mathbb F_q$ for prime $q=2,3$. Lines use dot-product-zero incidence. It verifies $q^2+q+1$ points and lines, $q+1$ points per line, and every pair of distinct lines meeting in exactly one point. It enumerates all $2^{q^2+q+1}$ subsets.

- Fano $\mathrm{PG}(2,2)$: **no subset can hit each line in only 1 or 2 points**; exhaustive optimal maximum line intersection is $C_{\min}=3$. A whole projective line meets itself in 3 and each other line in 1.
- $\mathrm{PG}(2,3)$: the same **$C_{\min}=3$**; a 6-point witness set attains it. Stored witness point indices and all feasible subset histograms are in the phase-18 receipt.

These results are finite exact enumerations only. They **cannot** show that a single $C=3$ or any finite $C$ suffices for all finite projective planes.

## Exact prior theorem and gap

Erdős–Silverman–Stein (1983) reportedly provide $1\le|S\cap\ell|\ll\log q$ for every line. This is **not** a constant independent of $q$. Independently source-review the probability construction and constants in ESS83; avoid reporting $O(\log q)$ as a solution.

## Independent critic obligations

1. Source-lock and read ESS83 and original Erdős 1981, check treatment of all finite planes and design generalization.
2. Independently verify the finite enumerator, geometry normalization, and exhaustive search (separate implementation or mathematical certificate).
3. Audit proof that Fano $C=2$ is impossible (can use the elementary Fano non-2-colourability theorem, with proof), and compare $q=3$ witness.
4. Examine asymptotic $O(\log q)$ proof and its allowed zero/whole-line/definition conventions, and state precisely what is not known for constant $C$.
5. Independent **non-author** mathematical review required under cohort deterministic sampling. Record signed source citations, reviewer identity and APPROVE/REVISE; do not count this sample as complete on the basis of writing this dossier.

**Current sample approval:** PENDING. **Cohort independent deterministic critical samples approved:** 0/20.
