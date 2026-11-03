# FIGURATE: source-critical bibliography and novelty boundaries

**FIGURATE-SRC-001.** Documentary edition: 3 November 2026. **Status:** primary abstract/metadata assertions checked against author, arXiv or publisher pages; proof-level source-semantic and exhaustive novelty reviews remain **open**. This is an evidence catalogue, not independent mathematical certification.

## Controlled mathematical taxonomy

Let the polygonal number of order $k$ be

$$
P_k(t)=\frac{(k-2)t^2-(k-4)t}{2}.
$$

Our **Type A** studies classical square-output Diophantine tuples whose *entries* are polygonal; the defining relations are $a_i=P_k(t_i)$ and $a_i a_j+n=x_{ij}^2$.

Our **Type B** studies tuples whose *pairwise outputs* are polygonal; their relations are $a_i a_j+c=P_k(t_{ij})$.

Our **Type C** requires polygonal entries and polygonal pairwise outputs. In each case the entries are distinct positive integers and the order, offset and allowed indices are part of the problem statement. The expression *triangular Diophantine tuple* has been applied to more than one of these definitions; indexing by the phrase alone causes semantic mistakes.

## Source register

| Key | Primary source | Specific source-supported statement | Classification and caution |
| --- | --- | --- | --- |
| F01 | [Bagchi and Zhou-Zheng, *Diophantine m-tuples of Triangular Numbers*, arXiv:2608.27697 (posted 27 August 2026)](https://arxiv.org/abs/2608.27697) | No all-triangular classical $D(1)$ quadruple; infinite constructed family of all-triangular $D(1)$ triples, conjectured complete; no all-triangular $D(n)$ pair when $n$ is 2 or 5 mod 9; generalized-Pell test with stated complexity bound. | **A, triangular.** Family completeness is a **conjecture**, not a theorem. The absence of $D(1)$ quadruples is not absence of all $D(n)$ quadruples. |
| F02 | [Radić, *On some D(u²) triples and quadruples of triangular numbers*, arXiv:2609.28018 (posted 23 September 2026)](https://arxiv.org/abs/2609.28018) | Classifies certain all-triangular $D(u^2)$ triples with prescribed smallest entry, and constructs all-triangular quadruples for infinitely many positive $u$. | **A, triangular with variable square offset.** Refutes any overbroad paraphrase extending F01's $D(1)$ nonexistence to all square offsets. |
| F03 | [Filipin, Jurasić and Togbé, *A note on the extension of some triangular Diophantine sets*, Ann. Sci. Univ. Ovidius Constanţa Ser. Mat. 34(2), July 2026, DOI:10.2478/auom-2026-0018](https://doi.org/10.2478/auom-2026-0018) | For the specifically studied triangular $D(k)$ pairs $\{k,2k\}$ at $k=10,28$, no extension to a quadruple. | **B, triangular outputs.** The $k$ in that paper denotes an offset, **not** the polygonal order of our $P_k$. No general nonexistence is inferred. |
| F04 | [Filipin and Szalay, *Triangular Diophantine tuples from {1, 2}*, Rad HAZU Matematičke znanosti 27 (2023), 55–70, DOI:10.21857/ygjwrcp48y](https://doi.org/10.21857/ygjwrcp48y) | No triangular-output $D(1)$ quadruple containing both 1 and 2. | **B.** For instance, the bounded triple $\{1,2,27\}$ is not new, and cannot be extended to a quadruple containing these entries. |
| F05 | [Jukić Bokun and Soldo, *Triangular D(−1)-tuples*, Bulletin mathématique de la Société des Sciences Mathématiques de Roumanie 69 (2024), 233–239](https://www.croris.hr/crosbi/publikacija/prilog-casopis/852811) | Classifies certain triples of form $\{1,2,c\}$ with a prime-power restriction on $c$ and proves nonextension of the listed cases. | **B, offset −1.** Restricted shape; do not generalize to all triangular-output tuples. Metadata/abstract in institutional registry, not independently replayed proof. |
| F06 | [Rayaguru, Panda and Togbé, *On Diophantine, pronic and triangular triples of balancing numbers*, Mathematical Communications 25 (2020), 137–155](https://www.mathos.unios.hr/mc/index.php/mc/article/view/3475) | Defines triangular tuples using **unshifted** pairwise triangular products and studies balancing-number instances. | **B, offset 0** with special balancing-number constructions. Offset 0 is legitimate established prior art, not a new FIGURATE definition. |
| F07 | [He, Togbé and Ziegler, *There is no Diophantine quintuple*, Trans. Amer. Math. Soc. 371 (2019), 6665–6709](https://doi.org/10.1090/tran/7573) | Classical $D(1)$ positive-integer quintuple nonexistence theorem. | Classical square-output background. Any new claim about $D(1)$ quintuples must respect this global result. |
| F08 | [Dujella, *On the size of Diophantine m-tuples*, Mathematical Proceedings of the Cambridge Philosophical Society 132 (2002), 23–33](https://doi.org/10.1017/S0305004101005515) | Formal definition of $D(n)$ and historical context, including Fermat's $\{1,3,8,120\}$. | Classical D(n) background; source abstract partly historical and may predate later resolved conjectures. |
| F09 | [Dujella, continuously maintained Diophantine m-tuples bibliography](https://dujella.github.io/ref.html) | Literature-discovery index, including 2026 triangular-number work and related developments. | **Index only.** A reference list does not itself certify theorem statements or comprehensive novelty. |

### Chronology and semantic reconciliation

F01 is about **triangular entries** with square pairwise outputs and offset 1. F02 subsequently shows that all-triangular quadruples **do** exist for infinitely many other offsets of the form square parameters. These findings are compatible because their offsets differ.

F03 and F04 instead impose **triangular pairwise outputs**, so their nonextension results apply to Type B rather than to Type A.

F05 covers the negative offset case. F06 already studies unshifted triangular pairwise products. All should be compared before proposing any uniform extension criterion.

In particular, our L60 computational rows with zero quadruples cannot be promoted into global nonexistence, and the positive square-order offset-zero counts mostly expose the elementary fact that products of squares are squares.

## Novelty ledger and research targets

| Candidate claim or question | Status on 3 November 2026 | Requirement before promotion |
| --- | --- | --- |
| Complete classification of all triangular-entry $D(1)$ triples | **F01 conjecture; not a GCL discovery** | Compare any proposed classification with F01's exact constructed family and hypotheses |
| All-triangular $D(1)$ quadruple nonexistence | **Known theorem F01** | No rediscovery claim |
| All-triangular $D(u^2)$ quadruple nonexistence for variable $u$ | **False in general by F02** | Avoid as a programme target |
| No triangular-output $D(1)$ quadruple containing 1 and 2 | **Known theorem F04** | No rediscovery claim |
| Triangular-output $D(k)$ nonextension for studied $\{k,2k\}$ at 10 and 28 | **Known theorem F03** | Do not extrapolate without proof |
| Polygonal-order-uniform modular obstruction for Type B | **Research direction, no new proof** | Specify domain, modulus, residue classes, offsets; prove necessity and compare all sources |
| Parameterized computational sieve and asymptotic cost bound | **Research direction, no measured speed-up** | Reproducible implementation and rigorous complexity or verified benchmark comparison |
| Exhaustive absence within fixed entry bound | **Finite computation only** | Exact solver replay, independent witness/coverage check, machine-readable configuration |

## Source audit method and limitations

The register verifies identities, publication metadata, terminology and the **narrowest stated conclusions** available from the primary publisher, author bibliography, and arXiv abstract pages. It does **not** independently inspect or certify every lemma and proof in these papers, and cannot prove a global literature search complete. Treat the F01 completeness conjecture as *apparently open in the inspected 2026 sources*, rather than a claim about all possible unpublished work.

On any new theorem submission, freeze source versions, inspect full primary proofs, record theorem numbers, compare exact parameter domains, and submit the novelty and claim-semantics assessment to the appropriate mathematical adjudication lane. This catalogue is enough to prevent the important known misclassifications; it is not a mathematical originality certificate.

## Continuity

Parent: [FIGURATE-PILOT-001](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3093). Method and finite evidence: [MATHSOLVE census archive](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/FIGURATE_CENSUS_README.md). Reader introduction: [FIGURATE primer](FIGURATE_PILOT_001.md). Documentary bibliography complete at **registered-primary-source level**; proof-level semantic verification and future novelty assessment remain open research controls.
