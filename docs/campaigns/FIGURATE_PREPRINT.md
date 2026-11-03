# FIGURATE: A Unified Experimental Framework for Figurate Diophantine Tuples

**Research preprint, version 0.1, 3 November 2026.**

**Grand Challenge Labs — FIGURATE-PILOT-001**

**Claim status:** Programme methods paper and bounded computational report. **No novel unbounded theorem is claimed.** It is not a submitted or accepted arXiv article, a formally verified proof, or an independently certified mathematical result.

## Abstract

We introduce a common computational and expository framework for three different families of figurate Diophantine tuples: tuples whose entries are polygonal numbers and whose shifted pairwise products are squares; tuples whose shifted pairwise products are polygonal; and tuples satisfying both constraints. A discriminant and congruence membership test reduces polygonal membership to exact integer arithmetic, and a pair-compatibility graph turns bounded tuple enumeration into clique search. We report a reproducible 270-parameter survey of entry-bounded tuples with maximum entry 60, polygonal orders 3–12, additive offsets −1, 0 and +1, and cardinalities 2–4. We distinguish computational observations from theorems, and reconcile recent Type A and Type B results, including the 2026 construction of all-triangular quadruples for infinitely many nonunit square offsets. The contribution of this edition is the explicit taxonomy, machine-readable bounded baseline, and research-question normalization, **not** proof of a new structural result.

**Keywords:** Diophantine tuples; polygonal numbers; triangular numbers; exact computation; Pell equations; finite enumeration.

## 1. Introduction

Classical Diophantine tuples are sets of distinct positive integers such that every product of distinct elements, increased by one, is a perfect square. Variations replace the additive constant, restrict entries to special sequences, or change the pairwise target from squares to triangular or higher polygonal numbers.

A recurrent ambiguity is the phrase *triangular Diophantine tuple*. It can mean a classical square-output tuple made only of triangular entries, or a tuple in which every shifted pairwise product is triangular. Recent literature contains both notions, with different theorems and different permissible offsets [1–5]. We therefore distinguish three versions before comparing computations or proposing a theorem.

## 2. Definitions and exact membership

For integers $k\geq3$ and $t\geq1$, define

$$
P_k(t)=\frac{(k-2)t^2-(k-4)t}{2}.
$$

We consider tuples of distinct positive integers, always with a declared polygonal order and additive offset.

**Type A.** Each entry is a polygonal number and each shifted pairwise product is a square:

$$
a_i=P_k(t_i), \qquad a_i a_j+n=x_{ij}^2 \quad (i<j).
$$

**Type B.** Each shifted pairwise product is a polygonal number:

$$
a_i a_j+c=P_k(t_{ij}) \quad (i<j).
$$

**Type C.** Both the entry condition and the polygonal-output condition hold, using the explicitly declared orders and offsets. The initial computational implementation uses the same polygonal order for both.

**Elementary membership lemma (algebraic identity, not a novelty claim).** An integer $z\geq1$ is of the form $P_k(t)$ for some integer $t\geq1$ exactly when

$$
D=(k-4)^2+8(k-2)z
$$

is the square of a nonnegative integer $r$ and the integer candidate

$$
t=\frac{r+(k-4)}{2(k-2)}
$$

is integral and at least one. Equivalently, the numerator is divisible by $2(k-2)$, its quotient is positive, and substitution gives $P_k(t)=z$.

*Explanation.* Multiplying the definition by $8(k-2)$ and completing the square yields

$$
\bigl(2(k-2)t-(k-4)\bigr)^2=(k-4)^2+8(k-2)P_k(t).
$$

For $k\geq3$ and $t\geq1$, the expression inside the square on the left is positive. Hence the positive square root recovers the candidate formula; direct substitution certifies sufficiency. Merely detecting a square discriminant without integral-index and positivity checks can generate spurious solutions.

For Type A, the pairwise membership test is simply the exact integer-square test for $a_i a_j+n$. All tests use integer arithmetic, not floating-point tolerance.

## 3. Compatibility graph and finite enumeration

Fix a condition family, polygonal order, offset, entry bound and tuple size. Form a finite graph whose vertices are the admissible positive entries no greater than the bound. Connect two distinct vertices exactly when their pairwise condition passes the appropriate membership test.

**Elementary correspondence.** A tuple of the prescribed cardinality satisfies all pairwise conditions if and only if its vertices form a clique of that cardinality. This is immediate because both predicates quantify over exactly the unordered distinct pairs. Restricting recursion to strictly increasing candidates prevents duplicate tuples.

The public implementation records each tuple's pairwise integer witnesses. The test harness uses direct combination enumeration on smaller cases as an algorithmically distinct check against mistakes in graph construction or search order. A recorded zero asserts completeness **only for the exact finite vertex set**.

The algorithm's worst-case output is necessarily proportional to the number of tuples produced. No claim of improved asymptotic complexity is made. Large-number and runtime scaling are deferred.

## 4. Computational protocol

The archived panel fixes:

| Parameter | Declared values |
| --- | --- |
| Families | A, B, C |
| Polygonal order | 3 through 12 inclusive |
| Additive offset | −1, 0, +1 |
| Tuple cardinality | 2, 3, 4 |
| Maximum entry | 60 |
| Number of parameter combinations | 270 |
| Arithmetic | Exact integer square root and divisibility |

The [dataset](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_census_2026_11_03_L60.csv) has one row per parameter combination and contains the count and lexicographically first witness. A [replay harness](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_census_replay.py) regenerates the values from the [reference search program](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_census.py). Independent small-case regressions are archived alongside them.

The totals in Table 1 are sums across the different order/offset choices. They are not counts of distinct tuples after deduplicating across parameter settings.

**Table 1. Bounded, summed tuple counts.**

| Family | Pairs | Triples | Quadruples |
| --- | ---: | ---: | ---: |
| A | 42 | 35 | 35 |
| B | 1312 | 137 | 41 |
| C | 65 | 38 | 35 |

Every four-element solution observed in this panel occurs at square order with zero offset. This is an elementary control regime, because a product of square entries is again square. No general upper bound on tuple cardinality or global nonexistence can be inferred.

For Type B with triangular outputs and unit offset, the smallest observed triple is $\{1,2,27\}$: the three outputs are 3, 28 and 55, all triangular. Its special role is already present in earlier published work [3]. At pentagonal order and offset −1, the bounded panel includes the triple $\{2,3,59\}$; this is a computational example and is not asserted new.

## 5. Prior art and the novelty boundary

Bagchi and Zhou-Zheng [1] prove nonexistence of all-triangular classical $D(1)$ quadruples and construct an infinite family of all-triangular $D(1)$ triples. Their conjecture that this constructed family is complete is not resolved by the present work. Radić [2] studies other square offsets and constructs all-triangular quadruples for infinitely many such offsets. These two papers do not conflict: they address different additive constants.

Filipin and Szalay [3] prove that no triangular-output unit-offset quadruple contains both 1 and 2. Filipin, Jurasić and Togbé [4] study nonextension for specified offset-dependent pairs. Rayaguru, Panda and Togbé [5] discuss unshifted triangular-product tuples, so even the zero-offset case has identifiable prior literature. Further restricted negative-offset results appear in Jukić Bokun and Soldo [6].

Consequently, a productive theorem programme must pin precise conditions, not merely ask whether triangular quadruples exist. Classical square-output quintuple nonexistence was settled in 2019 by He, Togbé and Ziegler [7]. The expanded citation catalogue documents these distinctions and links the sources.

### An explicit published Type B quadruple

The original 2023 Filipin–Szalay paper supplies the triangular-output quadruple with entries 14, 31, 135 and 3510, in which all six shifted products are triangular. Thus a universal Type B offset-one quadruple nonexistence claim is **false**. The nonextension theorem in that paper concerns the prescribed pair 1 and 2. Our entry-bound-60 census does not include the published quadruple and cannot be used to infer global absence.

[WP05 primary-source matrix](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP05_PRIMARY_SOURCE_MATRIX_002.md) records theorem numbers and argument dependencies where original full papers have been inspected, while keeping inaccessible original proofs distinctly unverified.

## 6. Research questions

The pilot's first substantive mathematical questions are:

**Uniform local obstructions.** For a fixed polygonal order, can one characterize residue classes of offsets that prohibit any Type B pair, or prohibit extension of a specified pair, by explicit congruence arguments? Such a result must retain integral-index conditions after discriminant reduction.

**Beyond the triangular case.** Can simultaneous Pell-type equations for higher polygonal targets yield new nonextension criteria, particularly outside the offset-zero square control class? The target must be checked against the prior source catalogue.

**Proven algorithmic benefit.** Can residue filters or lifted congruence restrictions reduce the search space with a rigorous correctness proof and a documented complexity or measured-performance advantage? No such speedup is claimed here.

**Formal checking.** Can a bounded search's completeness assertion be translated to a small trusted checker or Lean theorem, rather than relying on a single enumeration implementation? This is a future obligation, not something already demonstrated.

## 7. Limitations and conclusion

The finite data establish neither mathematical novelty nor an asymptotic law. The survey's entry bound is intentionally modest. The primary bibliography is checked at source-abstract and publisher-metadata level, not through independently reconstructed proofs. There is no formalized Lean statement, no external certification, no nontrivial new theorem, and no claim of an arXiv submission.

The result of this edition is a durable, precise baseline from which a focused theorem attempt can proceed without confusing incompatible notions of figurate Diophantine tuples or rediscovering known restricted nonextension theorems.

## References

1. S. Bagchi and C. Zhou-Zheng, *Diophantine m-tuples of Triangular Numbers*, [arXiv:2608.27697](https://arxiv.org/abs/2608.27697), 2026.
2. P. Radić, *On some D(u²)-triples and quadruples of triangular numbers*, [arXiv:2609.28018](https://arxiv.org/abs/2609.28018), 2026.
3. A. Filipin and L. Szalay, *Triangular Diophantine tuples from {1, 2}*, Rad HAZU Matematičke znanosti 27 (2023), 55–70, [DOI](https://doi.org/10.21857/ygjwrcp48y).
4. A. Filipin, A. Jurasić and A. Togbé, *A note on the extension of some triangular Diophantine sets*, Ann. Sci. Univ. Ovidius Constanţa Ser. Mat. 34(2) (2026), [DOI](https://doi.org/10.2478/auom-2026-0018).
5. S. G. Rayaguru, G. K. Panda and A. Togbé, *On Diophantine, pronic and triangular triples of balancing numbers*, Mathematical Communications 25 (2020), 137–155, [journal](https://www.mathos.unios.hr/mc/index.php/mc/article/view/3475).
6. M. Jukić Bokun and I. Soldo, *Triangular D(−1)-tuples*, Bulletin mathématique de la Société des Sciences Mathématiques de Roumanie 69 (2024), 233–239, [institutional record](https://www.croris.hr/crosbi/publikacija/prilog-casopis/852811).
7. B. He, A. Togbé and V. Ziegler, *There is no Diophantine quintuple*, Trans. Amer. Math. Soc. 371 (2019), 6665–6709, [DOI](https://doi.org/10.1090/tran/7573).
8. A. Dujella, [Diophantine m-tuples bibliography](https://dujella.github.io/ref.html), continuously updated.

## Research reproducibility and governance

[FIGURATE source catalogue](FIGURATE_SOURCES.md) · [Bounded census](FIGURATE_CENSUS.md) · [Research primer](FIGURATE_PILOT_001.md) · [Programme charter](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3093) · [MATHSOLVE research baseline](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_PILOT_001.md).

**Next required promotion boundary:** a proposed new theorem requires exact source-version pinning, full-proof semantics review, independently checked mathematical reasoning and governed certification. This manuscript's *draft* status must not be confused with an external publication.
