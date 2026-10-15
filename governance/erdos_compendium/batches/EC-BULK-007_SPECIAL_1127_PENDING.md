# EC-BULK-007 — Erdős #1127 source-fidelity and logical status exception

**Status: PRIMARY_LOGICAL_INDEPENDENCE_PROOF_PENDING.** This is not a completed critical review, a proof of independence, or a protected admission.

- Maintained source: https://www.erdosproblems.com/1127 (INDEPENDENT).
- Authenticated return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2398#issuecomment-6180698900 (STATUS_CONFLICT for insufficient displayed countable-negative evidence).
- Unaccepted article: governance/erdos_compendium/editorial/1127.md
- Source-verified bibliography: Kenneth Kunen, *Partitioning Euclidean space*, Math. Proc. Camb. Phil. Soc. **102** (1987), 379–383. DOI: https://doi.org/10.1017/S0305004100067426 .
- Earlier n=1 and n=2: Erdős–Kakutani (1943), Davies (1972).

## Statement fidelity

For fixed finite dimension n, partition R^n into COUNTABLY MANY subsets each having all distances between distinct UNORDERED pairs distinct. This is stronger than forbidding isosceles triangles in each subset; repeated distance between disjoint pairs must also be excluded.

Under CH, the cited original results report affirmative partitions in n=1,2 and all finite n. A Q-linearly-independent set of reals has unique unordered pair distances by elementary sign algebra; the complete countable partition and its assumptions are externally sourced rather than reproduced here.

The site classifies the original statement as **INDEPENDENT of ZFC**, but the negative justification displayed describes non-CH obstruction to FINITELY many colour classes. A finite-colour impossibility alone does NOT imply countable-colour impossibility. Reviewers must not treat this mismatch as proof the source's status is false; it is an explicit missing source step.

## Required source-and-logic review

1. Obtain and hash original Erdős–Kakutani (1943), Davies (1972), Kunen (1987), plus Erdős–Hajnal negative source.
2. Record exact positive CH theorem including n, classes, Q-independence versus unique Euclidean distances.
3. Locate a NO-COUNTABLE-PARTITION theorem in a model of ZFC + not-CH, with the actual cardinal assumptions and every finite n claimed; do not replace by NO-FINITE.
4. If a negative countable theorem exists, cite its numbered theorem/page and proof assumptions; if not, record precise unresolved statement and propose upstream catalogue correction.
5. Independently adjudicate semantic equivalence, then permit editorial source-fidelity review. Do not change ZFC/CH status labels until mathematically justified.

## Reproducible bounded evidence

ci/erdos_compendium_007_phase14_checks.py checks {0,1,3} has distances {1,2,3}, whereas {0,1,2} repeats distance 1. Neither experiment certifies a continuum cardinal theorem.

**Do not mark #1127 source-fidelity approved or call a new theorem/Lean result certified.**
