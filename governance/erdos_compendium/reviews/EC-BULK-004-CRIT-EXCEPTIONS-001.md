# EC-BULK-004 — early exception-driven critical editorial review

Record: `EC-BULK-004-CRIT-EXCEPTIONS-001`  
Observed: 2026-10-13  
Logical role: `NONAUTHORING_READ_ONLY_ADVERSARIAL_EDITORIAL_PASS`  
Accountable GitHub identity: `fyremael`  
Review authority: routine documentary editorial judgment only; **not mathematical certification**.  
Relation to production sampling: three additional exception reviews, **not** a replacement for the separate deterministic minimum sample of 20 across all 200 articles.

## Exact review scope and verdict

The three source-backed draft files examined on `editorial/ec-bulk-004-200` are:

| Problem | Authenticated source return | Normalized SHA-256 | Editorial critical outcome |
| --- | --- | --- | --- |
| 448 | [#1718 RESULT/1](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1718#issuecomment-6142995429) | `dec0bcd3f3803cec6406c2f0ab40779acbb738225be55c32ae6400bd79924cac` | PASS as unaccepted documentary draft |
| 449 | [#1719 original PARTIAL](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1719#issuecomment-6143008498), [critical supplement](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1719#issuecomment-6143318025) | `8202f25b5bf0d69eff49f49fe7ab640b5b5777629c6643c262d0ab8cbdfd1862` | PASS with mandatory secondary-source correction documented |
| 451 | [#1721 RESULT/1](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1721#issuecomment-6143054330) | `e46f77a8d2d9d394a77cdbc34f6493aaaa8bae7a67ef24d7c79c8bf4af139453` | PASS as unaccepted documentary draft |

Each review was conducted separately from the drafting action, against the immutable issue-bound source evidence and the generated manuscript. The same authenticated account was used for the accountable editorial role; physical agent/account independence is **not** claimed.

## 448: mathematical and primary-source challenge

- Original source: Erdős–Graham (1980), printed p. 89, inspected at https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf#page=85.
- Original resolving theorem: Erdős–Tenenbaum, *Ann. Inst. Fourier* **31** (1981), printed pp. 18–19, https://www.numdam.org/item/10.5802/aif.815.pdf#page=4, Theorem 1. The quantifiers `∀η>0 ∃Cη>0 ∀0<α≤1` and the upper-density versus strict/nonstrict predicate were checked.
- The manuscript correctly distinguishes a published quantitative theorem from the logically elementary deduction of a negative answer; `τ⁺(12)=4`, `τ(12)=6`, `τ⁺(6)=3`, `τ(6)=4` independently rechecked.
- Protected FormalConjectures provider at `85f863718beeec7b58a3a1926ee92e3472bc2020` still contains `sorry` for the main theorem. The manuscript does **not** count an external link or reported Lean proof as GCL certification.
- Verdict: no source/quantifier blocker for documentary exposition; **independent formal proof replay remains out of scope**.

## 449: adversarial reproduction and proof challenge

- Original Erdős–Graham printed p. 89 asks about `r(n)<ετ(n)` for almost all n. The secondary maintained entry reports a disproof but claims `r(n)+τ(n)≥τ(n)^2/τ⁺(n)`.
- The claimed intermediate inequality is **refuted exactly** at n=6, where `τ=4,τ⁺=3,r=1`: `5<16/3`. Do not propagate it.
- Correct dyadic-pair Cauchy–Schwarz inequality: `2r+τ≥τ²/τ⁺`. The proof uses `r≥Σ_j binom(a_j,2)`, `Σ a_j=τ`, `Σ a_j²≥τ²/τ⁺`; all signs, factor 2, open endpoints, and pair multiplicities checked.
- Stronger positive-lower-density statement reconstructed: put `m=6^h`. Then `τ(m)=(h+1)^2`, `τ⁺(m)≤3h+1`, so `r(m)/τ(m)≥½((h+1)^2/(3h+1)-1)→∞`. Fix h with ratio>K. For n=mt, gcd(t,6)=1, unique coprime divisor factorization injects the close pairs from each divisor of t, yielding `r(n)≥r(m)τ(t)>Kτ(n)`. The set of such n has natural density `1/(3m)>0`. Checked uniqueness and the exact positive density, not merely infinitude.
- The result was already reported in the literature; the construction is a self-contained expository reconstruction, **not a GCL novelty/MathCert claim**.
- The 1988 Hall–Tenenbaum §4.6 book passage was not accessible, so no exact book theorem is imputed to that source. **Correct the maintained-site explanation** independently of this manuscript's eventual admission.
- Verdict: source-fidelity concern about the main published status is resolved by a transparent reconstruction using the original question. Original immutable `PARTIAL` source return remains preserved; the supplemental critical record provides the new evidence.

## 451: publication-date, asymptotic and computation challenge

- Original source: Erdős–Graham p. 89. New primary preprint: van Doorn–Tang, arXiv:2606.19863v1, 18 June 2026, abstract and Theorem 1.1, https://arxiv.org/pdf/2606.19863.
- The lower bound `n_k>exp(log²k/(20 log log k))` for sufficiently large k implies `n_k>k^d` for every fixed d because `log²k/(20 log log k) / log k→∞`. It **does not** establish the separate upper conjecture or the full growth estimate, so the article correctly remains OPEN.
- The Theorem 1.1 interval `(k,k+3k^θ)` with θ=21/40 sits in `(k,2k)` for sufficiently large k, a necessary bridge explicitly included in the article.
- Construction `M_k=∏_{k<p<2k}p` and least multiple of `M_k` greater than 2k was checked, including the **small-k exception** to an unqualified `n_k≤M_k` bound. Finite cases `n_2=6,n_3=9,n_4=20,n_5=13` independently checked.
- Authors' external Lean/research-provenance declarations have no GCL proof-certification effect.
- Verdict: suitable documentary explanation of a dated partial theorem, pending protected production admission and public rendering.

## Mechanical QA receipts and restrictions

- At source head `1a2fbc8d81426b05d2604a892be2ca4084000ccb`, `python3 -m pytest -q ci/test_ec_bulk_004_math_fixtures.py ci/test_erdos_compendium_*.py` returned **51 passed, 3 subtests passed**.
- All three manuscript files at the later content head `472160546e7d27a879606b9c5144d0e549f11423` have the prescribed six headings exactly once and balanced dollar-delimited math. Normalized hashes appear above and are independently measured as `SHA256(UTF8(article_text.strip()))`.
- A strict `mkdocs build --strict --quiet` was run at the article-bearing head, exit code 0. It reported `editorial=65`, `reviewed=50`, `pending=12` **across the whole repository**, not as EC-BULK-004 acceptance.
- The local MkDocs output marks new manuscripts as **unaccepted**. **No protected production merge, deployed public HTML readback, actual browser math rendering, or V2 admission is claimed.**
- The mandated deterministic sample of at least 20 articles still has zero completed reviews; these three reviewed exceptions do not replace those 20.
- Final batch QA and formal mathematical certification gates remain separate from this early editorial pass.
