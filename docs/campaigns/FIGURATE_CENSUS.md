# FIGURATE: bounded computational census and reproducibility

**FIGURATE-DATA-001, 3 November 2026.** Status: *reproducible finite computations, without a new mathematical theorem or claimed certification*.

## The bounded experiment

The first archived survey fixes a maximum tuple entry value of 60. It enumerates three distinct condition classes for polygonal orders 3–12, offsets −1, 0 and +1, and tuple sizes 2, 3 and 4. There are exactly 270 parameter cases.

- **A:** every entry is polygonal, and every pairwise product plus the offset is a square.
- **B:** entries are arbitrary distinct positive integers, and every pairwise product plus the offset is polygonal.
- **C:** every entry and every pairwise output is polygonal.

The additive offset is interpreted differently for Type A (square outputs) versus Type B or C (polygonal outputs). The polygonal order applies to entries for A, pairwise outputs for B, and both for C.

The canonical machine-readable [270-row CSV](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_census_2026_11_03_L60.csv) records the order, offset, tuple size, entry limit, exact count and lexicographically first witness, or an empty witness for a bounded zero.

The [producer](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_census.py), [archive replay](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_census_replay.py), [independent test cases](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_census_archive.py) and [technical runbook](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/FIGURATE_CENSUS_README.md) are versioned in MATHSOLVE.

## Observed aggregate counts

| Family | Number of pairs | Number of triples | Number of quadruples |
| --- | ---: | ---: | ---: |
| A | 42 | 35 | 35 |
| B | 1312 | 137 | 41 |
| C | 65 | 38 | 35 |

Each column sums counts across 30 order-and-offset choices. Thus these numbers are **not** unique tuple counts across all parameter families; one tuple may contribute to more than one choice.

Some notable finite observations:

- With triangular outputs and offset +1, Type B has **11 triples** below the bound, beginning with the known example $\{1,2,27\}$.
- With pentagonal outputs and offset −1, Type B has **one triple**, beginning with $\{2,3,59\}$.
- All **size-four** solutions in this particular finite parameter panel occur for square order and offset zero. This is expected to be a structurally trivial family: products of perfect squares are perfect squares. It does **not** imply quadruple nonexistence outside the bound.

The zero-offset square cases should be removed from comparative performance and theorem-discovery dashboards, or reported separately as a trivial control class.

## Reproduce the exact counts

Run the following from the MATHSOLVE repository root.

```sh
python3 -m research.figurate_census_replay
python3 -m unittest discover -s tests -p test_figurate_census_archive.py
python3 -m unittest discover -s tests -p test_figurate_census.py
python3 -m research.figurate_census --kind B --k 3 --offset 1 --limit 60 --size 3
```

The replay checks 270 archived parameter rows by recomputing them with the exact-integer census source, checking the first tuple with the independent witness validator, and verifying the expected row grid. The regression tests also enumerate selected cases independently with direct combinations and polygonal-number membership. During snapshot generation, a separate direct-combination implementation cross-checked 135 parameter rows. Only the committed replay and regression program provides a durable method to repeat these checks.

A bounded enumeration does not prove an unbounded nonexistence claim. Nor does an exact computational result automatically establish a novel mathematical theorem. No runtime benchmark or complexity improvement is reported from this dataset. The first survey is deliberately small and intended to catch discrepancies in subsequent searches.

## Known mathematics versus FIGURATE evidence

The fact that no Type A, triangular, offset +1 quadruple occurs in a bound-60 survey is consistent with a **published global theorem**, not a GCL discovery. Other offsets can behave differently: the 2026 Radić work constructs infinitely many square offsets admitting all-triangular quadruples.

Read the [source-critical bibliography](FIGURATE_SOURCES.md) before inferring anything about maximum tuple sizes or general extension. An experimental positive tuple is only a witness; an experimental zero only concerns the declared finite domain.

## Full-paper counterexample outside the census bound

The [original 2023 Filipin–Szalay paper](https://hrcak.srce.hr/en/file/443905) records the **Type B triangular-output, offset +1** quadruple with entries 14, 31, 135 and 3510. Each pair product plus one is triangular, at indices 29, 61, 313, 91, 466 and 973 respectively. This example is excluded from the L60 experiment solely because the larger entries exceed 60.

The paper's nonextension theorem applies specifically to quadruples **containing both 1 and 2**; it is not a global nonexistence result. A regression for the published quadruple is in [MATHSOLVE](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_published_type_b_quadruple.py). This should be retained as a high-value external witness for future search benchmarks.

## Claim and continuity record

**Established:** machine-readable bounded archive, exact source implementation, runbook, and executable verification route.

**Not established:** a global classification, a generalized obstruction, a formal Lean certificate, any independent mathematical certification, a performance advantage, or exhaustive prior-art originality. Those remain scientific work packages rather than documentary defects.

Programme tracker: [FIGURATE-PILOT-001](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3093). Technical implementation: [MATHSOLVE PR #1176](https://github.com/grandchallenge/MATHSOLVE/pull/1176). Companion manuscript: [FIGURATE research preprint](FIGURATE_PREPRINT.md).
