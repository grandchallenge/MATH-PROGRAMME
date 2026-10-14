# EC-BULK-007 critical sample — Erdős #1084 (review incomplete)

- Deterministic critical sample: #1084 is one of the precommitted 20 problems.
- Review disposition: **PENDING_PRIMARY_PROOF_AND_FORMAL_STATUS**. Do not count as completed.
- Original source return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2355#issuecomment-6160843432
- Unaccepted draft: governance/erdos_compendium/editorial/1084.md
- Formal snapshot: google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020, FormalConjectures/ErdosProblems/1084.lean

## Source and theorem interface

The maintained Erdős catalogue (#1084, last edited February 8, 2026)
reports the parent problem OPEN, but separately attributes to Harborth
(1974) the exact planar theorem

$$
f_2(N)=\lfloor3N-\sqrt{12N-3}\rfloor,\quad N\ge2.
$$

The frozen Lean source labels its planar triangular-lattice optimality
theorem as research open and the proof body has an unproved placeholder.
That annotation conflicts with the published planar theorem according
to the catalogue and independent modern circle-packing literature.
Neither the general open problem nor the published planar theorem may
be relabeled by inference from the annotation alone.

## Independently replayable bounded evidence

The phase-seven finite program verifies hexagonal triangular-lattice
witnesses for radii 1,2,3,4 with point counts 7,19,37,61 and exactly
12,42,90,156 contacts, respectively. Integer arithmetic checks all
pairwise distances are >=1. These establish only four finite LOWER
WITNESSES, not Harborth's universal optimality proof.

## Outstanding checks for a completed critical review

1. Obtain and hash the original Harborth 1974 paper and read its
   theorem/proof pages directly.
2. Verify upper-bound proof hypotheses, separation/contact conventions,
   floor rounding, and boundary cases N=0,1.
3. Compare to the independent published sphere-packing account.
4. Correct the frozen formal-status inconsistency by an authorized
   upstream change, without implying a kernel proof exists.
5. Perform a genuine second-pass critical article review and record
   acceptance or revision against original pages.

No critical sample certification, source-fidelity approval, protected
publication, or novel theorem is claimed.
