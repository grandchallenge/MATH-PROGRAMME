# EC-BULK-004 — Erdős #464 critical documentary review

Receipt: EC-BULK-004-CRIT-EXCEPTIONS-012  
Review date: 2026-10-13  
Authenticated accountable GitHub identity: fyremael  
Function: logically distinct adversarial source and mathematical scrutiny after manuscript drafting. **Not** an independent human identity, GCL mathematical certification or V2 editorial admission.

## Primary source and formalization comparison

The original Erdős–Graham monograph (1980), printed p. 92, PDF zero-based page 87, uses fractional parts $\{\alpha a_k-\lfloor\alpha a_k\rfloor\}$ and explicitly requires an **irrational** multiplier $\alpha$. The ratio assumption is $a_{k+1}/a_k\ge c>1$. The maintained #464 prose can be misread as nondensity of *nearest-integer distances* $\|\alpha a_k\|$ in $[0,1]$, an assertion that is vacuous because all those distances belong to $[0,1/2]$. The manuscript does not propagate that vacuous statement as the original theorem.

Peres–Schlag, arXiv:0706.0223v1, printed p. 2, Theorem 1.1, independently inspected, gives $\inf_k\|\theta a_k\|>C\varepsilon/|\log\varepsilon|$ under $a_{k+1}/a_k\ge1+\varepsilon$ and $0<\varepsilon<1/4$ for some **real** $\theta\in(0,1)$. Section 3, Theorem 3.1, uses a Lovász-local-lemma argument. The explicitly displayed Theorem 1.1 does **not** require $\theta$ irrational, so it is not alone a syntactic proof of that qualifier. Pollington's cited 1979 Hausdorff-dimensional exceptional-multiplier result supplies a separate historical bridge, but the complete five-page Pollington primary proof has **not** been independently checked by GCL.

Pinned google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020 FormalConjectures/ErdosProblems/464.lean, Git blob 8f5c8f5e6d5cd150a7e4ca87a1525957651ac302, has Irrational theta and modulo-one nondensity in AddCircle, but its theorem remains an unproved placeholder. External Jayyhk/erdos-lean@110d489ed5c07e5b216453e092e9113127c98c9a problems/464/Erdos464.lean, blob cb00a923ad490adf6c0963e38655b4191b198bd7, has source proof declarations solution_uncountable, deMathan_not_dense, erdos_464 and no visible active proof holes in fetched text. GCL **did not compile or independently replay** it. Neither source is GCL MathCert.

## Mathematical adversarial check

The illustrative binary multiplier uses complementary digit pairs: pair j is 10 if j is a perfect square and 01 otherwise. Every triple of consecutive digits contains a full complementary pair and cannot be 000 or 111. Multiplication by $2^k$ shifts the expansion, giving $1/8\le\{2^k\theta\}\le7/8$ for every k. The even-position digits are exactly the square indicator, with infinitely many 1s and unbounded gaps, so the infinite word is not eventually periodic. Its real number is irrational. This proves the **example**, not the universal lacunary theorem.

Three exact standalone mathematical fixtures were independently executed in the local Python runtime: complementarity through 10,000 pairs; forbidden triples and exact rational 28-bit bounds through 10,000 shifts; and nearest-integer distances always $\le1/2$. All passed. The finite tests supplement, but do not replace, the all-index pairing argument. **Full CHAD pytest and MkDocs were not executed at this head**: shell requests currently report INVALID_ARGUMENT. No CI or public rendering success is asserted.

## Hash and provenance custody

- Authenticated original issue return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/1734#issuecomment-6157166081, SOURCE_LOCK_READY documentary disposition. SHA-256 of normalized LF source comment: 5d7093458a3b22905a031819b9e99bc0e73c62a781d709d9d982135a22e3aabe.
- Manuscript: governance/erdos_compendium/editorial/0464.md; SHA-256 stripped UTF-8 text 9a7e13e083441b8bf53be2b7a33c60bce1cb1dca37418466e7b4294044adeb60; raw UTF-8 SHA-256 392832c9ec7d9ffe9fab107ab436a3c95256e106ddeef3683c623222f0c7779d.
- Six canonical headings each occur exactly once; dollar-delimited math markers are paired.
- Protected production merge, V2 admission and actual public browser MathJax readback: NONE.

## Editorial disposition

CRITICAL_DRAFT_PASS_PENDING_FULL_BUILD_AND_HISTORICAL_SOURCE_CHECK. The source and semantic boundaries are sufficiently grounded for a **non-admitted documentary draft**. Historical Pollington full proof and external Lean should be checked independently for stronger assurance. Mandatory deterministic final sample and all mathematical exceptions remain distinct obligations. The statement is an established solved problem, not a new GCL theorem or independent formal certification.
