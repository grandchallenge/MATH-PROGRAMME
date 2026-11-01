# EC-BULK-004 — Erdős #479 source and formal-domain critical review

Review: EC-BULK-004-CRIT-EXCEPTIONS-018  
Observed: 2026-10-14  
Accountable authenticated reviewer: fyremael (logically separate post-draft review, NOT independent-person mathematical certification).  
Outcome: **CRITICAL_DRAFT_PASS_WITH_PINNED_FORMAL_SEMANTIC_EXCEPTION**; selected deterministic sample **not yet full pass** until semantic-equivalence resolution.

## Direct primary source and exact statement

Original P. Erdős and R. L. Graham (1980), printed p.96, visually inspected from https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf#page=92: asks **for every fixed integer k≠1** whether infinitely many n satisfy $2^n\equiv k\pmod n$. Reported established cases k=$2^i$ (i≥1) and k=−1 are attributed to Graham, D. H. Lehmer and Emma Lehmer, reference [Gr-Leh-Leh(xx)] which is listed as unpublished. The historic k=3 solution n=4700063497=19·47·5263229 is arithmetically checked here; its 1980 “smallest known” status is a dated computational report, not independently exhaustive current fact.

An ORIGINAL author manuscript, not a secondary summary, was downloaded and source-read: Q. Tang, *A Note on Erdős Problem #479: Infinitude of the Sets A(2^i) and Related Results* (2025-12-02), https://github.com/QuanyuTang/Erdos-Problem-479-Note/blob/main/A_note_on_Erdos_Problem_479.pdf . Six PDF pages; independently fetched SHA-256 **7054c3f9598d29299c9a50878036d0bb0219c73713fd166e3cbb9c809ccac3ac**. Page 1 reports historical manuscript missing; p.3 §2.2 inventories k=0,−1,−2 and $2^i$; pp.4–5 Theorem 3.1 proves $A(2^i)$ infinite using Fermat, multiplicative orders and Dirichlet. The note expressly disclaims novelty and is author-posted, not GCL MathCert.

## Pinned formal source: material domain mismatch

Protected google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020 file FormalConjectures/ErdosProblems/479.lean, Git blob 97e2765e0ef6c068d7b871a8c157e52b2e420e11, expresses `∀ᵉ (k > 1), { n | 2 ^ n ≡ k [MOD n]}.Infinite`, with an unresolved proof placeholder. The historical problem includes k=0 and **all negative** integers k, while this binder only quantifies k>1. Thus the provider snapshot is NOT a faithful formal statement of the full original. The ordinary integer-domain restriction to k>1 cannot be substituted for k≠1, and adding a theorem for all positive k would leave negative cases unproved.

Upstream `main` blob 77d7d378e7761aa771ff7e9af8a691047286610c instead writes `∀ᵉ (k : ℤ) (k ≠ 1)` and `[ZMOD (n : ℤ)]`; it corrects the domain but is NOT the protected source lock and still has an unresolved `sorry`. Explicit governance reconciliation and independently compiled statement-level equivalence are required before any mathematical formalization is considered source matched. No open conjecture is Lean-replayed or GCL certified.

## Independent mathematical audit

For each i≥1, factor i=2^s∏q_j^{e_j}. Define d_j=ord_{q_j^{e_j}}(2), $L=\mathrm{lcm}_j[d_j/\gcd(d_j,i)]$ (L=1 if no odd q). Choose odd primes p≡1 mod L with p∤i. Then Fermat shows p|$2^{ip}-2^i$, and the order conditions plus 2^s|2^i show i divides the same difference. Since gcd(i,p)=1, ip divides it. Dirichlet yields infinitely many such p. All steps were independently checked against Tang pp.4–5 and finite test implementations. This proves the historically established partial result, not the universal conjecture.

Independent elementary obstruction k=1: for even n>1, 2^n not congruent1 mod2. For odd n>1 let p be its smallest prime divisor. The multiplicative order of 2 modulo p divides n and p−1, hence if nontrivial would have a prime factor of n smaller than p, contradiction. Order 1 is impossible; therefore A(1)={1}.

Authenticated original result: https://github.com/grandchallenge/MATH-PROGRAMME/issues/1749#issuecomment-6167988790 , author fyremael, LF-normalized UTF-8 SHA256 **83f76ebf9fddb1ea211d3fd9a2a2314b4b044d87cc28a21c084bdd5132af0c4e**; six substantive RESULT/1 sections, disposition SOURCE_LOCK_READY for documentary original and known partial result.

Manuscript governance/erdos_compendium/editorial/0479.md stripped UTF-8 SHA256 **6455accc92cc48d1cd902081ef4889a6161cb65882499afbd8c3a9c130f2032b**, raw SHA256 **2f9679479206d8b61d11c78ed00e4b5b0b4e3b9ca80485b6e4a6193590870b1b**. All six canonical headings occur once, dollar-delimited mathematics balanced.

Exact finite test tests/test_erdos_compendium_0479_congruences.py: **4 PASS** at commit c1b6f0356fde96d737d4e34ef7ec679f8bf5b628. Tests derive L independently from trial-division prime powers and repeated multiplication orders, check ten i values and distinct p for each, reproduce $n=4700063497$ modular identity for k=3 (NOT historic minimality), k=0 and k=−1 special cases, k=1 n≤2499 obstruction, and two exact CRT extension witnesses. These tests do NOT prove any open instance beyond the known power-of-two family, nor do they replace Dirichlet's theorem.

## Bounded successor and disposition

EC004-0479-PINNED-SEMANTICS: freeze both formal blobs; exhibit k=−1 and k=0 as excluded by the older binder; inspect actual Lean elaboration; prove equivalence of the newer integer ZMOD clause with the historical statement on positive n and any integer k; do not promote to protected source without required governance. Continue source review of unpublished Graham–Lehmer–Lehmer citation, and optionally replay Tang's proof in formal Lean with separately attributed Dirichlet dependence.

For cohort QA this is an additional critical review, not completed final deterministic 20-sample adjudication: **sample entry #479 stays blocked on the pinned formal statement mismatch**. The documentary manuscript may remain UNACCEPTED_DRAFT as it accurately labels the exception. Full tests, strict MkDocs and source reconciliation must be run on exact final register head, and protected production/V2 merge/public browser MathJax remain absent.
