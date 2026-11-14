# EC-BULK-004 — Erdős #485 critical proof-source and formalization review

Receipt: EC-BULK-004-CRIT-EXCEPTIONS-022  
Date: 2026-10-14  
Authenticated editorial identity: fyremael. This is a distinct post-draft reasoning pass by the SAME operator, not independent-person peer review, new mathematical certification or V2 admission.  
Disposition: **SOURCE_AND_DRAFT_PASS_WITH_1987_LEMMA_IMAGE_AND_EXTERNAL_LEAN_BLOCKERS**.

## Historical and mathematical problem identity

Directly inspected original P. Erdős, *Some unsolved problems* (1961), printed p.234, I.23, https://users.renyi.hu/~p_erdos/1961-22.pdf#page=14 . Let f(k)=min τ(P²) over all rational k-term P, where τ counts distinct NONZERO coefficients after all cancellations. Erdős and Rényi conjectured f(k)→∞. Erdős's earlier construction f(k)<k^(1−c) for some c>0 is an UPPER witness; it cannot refute unbounded lower growth. The original 1947/1949 papers and Hayman 1974 Problem 4.4 have NOT been read in full during this review; attribution is directly present in the 1961 page and 2009 resolving paper.

The first solution is Schinzel, *Acta Arithmetica* 49 (1987), 55–70, DOI 10.4064/aa-49-1-55-70. The exact scanned original archive PDF was downloaded from https://www.impan.pl/shop/en/publication/transaction/download/product/105207, PDF SHA256 **b2dc9ffd681efe84581cb39a20449605a9b5946f8371dd5123c86dd7513c5401** (9 PDF pages, original journal pagination 55–70); its content is an image-only scan and ORIGINAL 1987 LEMMA PAGES WERE NOT VISUALLY REPLAYED. Source provenance and status still stand, but do not claim first-proof independent audit.

## Complete inspected stronger primary

DIRECTLY READ original publisher four-page PDF Schinzel–Zannier, *Rendiconti Lincei Matematica e Applicazioni* 20 (2009), 95–98, https://ems.press/content/serial-article-files/39657, downloaded PDF SHA256 **47a3272cd0575ff17900f7cb59e52037ebe6388532f6e36990e55ff3f6524f27**. Theorem 1 printed p.95 says for field F, P∈F[x] with T≥2 terms, integer l≥1, t=τ(P^l), assuming char F=0 OR char F>l·deg P:

$$

t\ge2+\frac{\log(T-1)}{\log(4l)}.

$$

For F=ℚ,l=2,T=k≥2, this gives f(k)≥2+log(k−1)/log8→∞. No restriction on degrees over ℚ. The 2009 Theorem 2 p.96 has separate positive-characteristic assumptions that cannot be silently dropped.

The complete paper's p.96 Lemmas 1–2 and p.97 proof explicitly depend on Schinzel 1987 pp.60–63. The core 2009 argument assumes a minimal-degree counterexample, uses Diophantine approximation of exponent ratios, a two-variable polynomial decomposition and lower-degree substitution contradicting minimality. The mathematical theorem is publication-proven; an independent GCL proof reconstruction of the original 1987 auxiliary lemmas and all 2009 algebraic steps has NOT occurred. Its characteristic and degree hypotheses are visibly retained in the six-section manuscript.

## Adversarial arithmetic and logical checks

The exact example P(x)=1+x−x²/2 gives P²=1+2x−x³+x⁴/4 (FOUR terms). This falsifies the naive assertion τ(P²)≥2τ(P)−1 for all polynomials; cancellations are essential. For G_k(x)=1+x+⋯+x^(k−1), τ(G_k²)=2k−1 because coefficients of degrees 0..2k−2 are all strictly positive: an upper witness, NOT an all-P lower theorem.

For a binomial ax^r+bx^s, r<s,ab≠0, characteristic zero ensures τ(P²)=3; f(1)=1 and f(2)=3. These edge cases do not alter the large-k question. For all d≥1, r≥0, nonzero c, define Q(x)=cx^rP(x^d); then τ(Q)=τ(P), τ(Q²)=τ(P²). Unbounded polynomial DEGREE cannot be replaced by a bounded finite search over exponents to prove the all-k theorem.

Five tests/test_erdos_compendium_0485_sparse_squares.py exact rational polynomial arithmetic checks passed at source commit c17ef87cc7be6442d75b681f7f5957abce69ab1d: cancellation/normalization, all two-term supports with exponents r<s<9, dense positive geometric sums for k≤29, monomial-shift/dilation invariance up to d=97 and r=100, and the 2009 published inequality for bounded examples. Rational Fraction arithmetic avoids floating-point coefficient cancellation. Tests DO NOT prove the universal 2009 theorem, nor characterize exact f(3).

## Formalization and admission boundary

GCL pinned google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020 has NO 485.lean file. Unpinned current main blob **dbd3d40adee5e88b044bcb256d345288db32f6e8** declares f(k) using `sInf` over ℚ[X] support-cardinality sets and asks `Tendsto f atTop atTop`, but its main theorem body is `by sorry`. The metadata cites an external Lean purported proof plby/lean-proofs@8822f7ddef30fadbd92e1c6ab4ed897af356af5e, `src/latest/ErdosProblems/Erdos485.lean`. The external proof was NOT independently built or axiom-reviewed by GCL in this pass. Site metadata “Formalised statement? No” conflicts with the pinned source packet's assertion “yes”; this is editorial metadata drift, not evidence of mathematical uncertainty.

The authenticated original issue research return https://github.com/grandchallenge/MATH-PROGRAMME/issues/1755#issuecomment-6180254764 has six substantive RESULT/1 sections, disposition SOURCE_LOCK_READY for original question and 2009 theorem, author fyremael, LF-normalized body SHA256 **29963f4dd3fcfeb08f9412dd81169969438e7ff8289b2b5195cfa9ea933abcd0**.

Six-heading accessible article governance/erdos_compendium/editorial/0485.md has balanced dollar-sign math delimiters, normalized stripped UTF-8 SHA256 **47d76e8b5e81fd7117873a6e2f344af480b3a19da7b863a6c5feca92ec325a42**, raw byte SHA256 **681be5bf46dc14130c62a7621468b62d48d626161c51afdca3baab362dd55f0b**.

## Result and bounded successor

**CRITICAL_DRAFT_PASS_WITH_1987_PAGE_AND_EXTERNAL_FORMAL_EXCEPTION**. Appropriate source-grounded scholarly exposition; original 1961 and complete 2009 theorem are directly read. Remaining bounded task: visually review Schinzel 1987 original Lemmas 1–2 (pp.60–63) as page images, reconstruct their exact hypothesis match to the 2009 theorem, then separately compile the pinned external Lean project with transitive trust/axiom output and a formal binder statement-equivalence check; exact rational regression fixtures provide limited arithmetic confidence only. Falsification hooks: confuse log(4l) with l·log4; omit characteristic; replace T−1 with T; treat upper construction as lower; or treat incomplete Lean theorem as kernel-checked. Stop at any explicit missing original lemma or proof artifact rather than fabricate MathCert. The article is UNACCEPTED_DRAFT, no protected production PR/merge, public browser MathJax readback, independent-person proof certificate or V2 admission claimed. This is an additional source critical review, not a substitute for the cohort's fixed deterministic 20-sample gate.
