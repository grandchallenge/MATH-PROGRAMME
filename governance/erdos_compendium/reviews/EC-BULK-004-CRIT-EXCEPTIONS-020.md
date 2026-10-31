# EC-BULK-004 — critical mathematical and source review of Erdős #481

Receipt: EC-BULK-004-CRIT-EXCEPTIONS-020  
Observed: 2026-10-14  
Authenticated accountable identity: fyremael  
Scope: mathematical adversarial review following initial authoring; no independently distinct human reviewer, no kernel-checked Lean MathCert, no V2 editorial admission.

## Original-vs-modern parameter semantics

The directly inspected original Erdős–Graham (1980), printed p.96, PDF zero-based p.91, https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf#page=92 , says “given integers” a_i,b_i and asks about repeated application of the affine list operator and an additional cutoff B; it does **not explicitly restrict** them to positive a_i and nonnegative b_i on that page. The maintained https://www.erdosproblems.com/481 (last edited 2025-12-03) instead uses a_i,b_i∈ℕ, reciprocal hypothesis Σ1/a_i>1 and repeated elements in some list A_k. The latter is a precise *positive/nonnegative domain normalization* but the unrestricted signed interpretation of the 1980 wording has NOT been source-locked as equivalent. The current documentary return is therefore PARTIAL; the modern theorem remains **PROVED**.

Source attribution independently checked from the full original primary A. Kolpakov and A. Talambutsa, “On free semigroups of affine maps on the real line,” *Proc. Amer. Math. Soc.* **150** (2022), 2301–2307, https://arxiv.org/pdf/2105.09387v2 , preprint p.2 Theorem 3, full proof pp.5–6. Its theorem requires positive integer multipliers a_i, **rational offsets** b_i, and Σ1/a_i>1; it yields non-freeness of the generated AFFINE-MAP semigroup. Its proof groups same-length words by multiplier, then counts rational affine constant terms, so gives equal-LENGTH function words. Evaluation at x=1 yields a collision in a single generation of the current problem. Reverse implication (equal at x=1 → equal as functions) is false.

Klarner's original D. A. Klarner, *J. Algebra* 74 (1982), 140–148, DOI 10.1016/0021-8693(82)90010-2, Theorem 1.1 is identified from the actual 2022 proof and bibliography, but its full journal pages have NOT been independently read. The 2022 source flags that Klarner's proof relies on an unpublished Rivest argument for a special case, a genuine provenance caution, not grounds to deny the corrected 2022 full proof.

## Independent algebraic proof check

For nonnegative b_i and positive a_i, a self-contained harmonic-weighted proof was reconstructed and checked:

Under assumed no collisions, S_k=Σ_{x∈A_k}1/x and m_k=min A_k. Let C=Σ1/a_i>1 and D=Σ b_i/a_i²≥0. If f_i=id and r≥2, compositions f_i∘f_j and f_j∘f_i are different **labelled** words of length two with the same value at 1, so a collision occurs in A_3. Thus, under the no-collision assumption, there is no identity. For x≥1 every remaining affine map f_i(x)=a_ix+b_i≥x+1. Hence m_k≥k.

The elementary identity

$$

\frac1{a_ix+b_i}=\frac1{a_i x}-
\frac{b_i}{a_ix(a_ix+b_i)}

$$

implies S_{k+1}≥C S_k−DΣ 1/x²≥(C−D/k)S_k. For all sufficiently large k choose q>1 with C−D/k≥q. Thus S_k≥S_Kq^{k−K}. But if all r^{k−1} entries are distinct positive integers then S_k≤H_{r^{k−1}}≤1+(k−1)log r, contradiction. This proves the normalized problem independent of the external 2022 theorem but is **established mathematics** and not new GCL work.

Crucial adversarial **identity exception**: a=(1,2),b=(0,0) has C=3/2>1 yet m_k=1 for EVERY k, so an unqualified assertion m_k≥k is false. It nevertheless collides in A_3 by commuting id and doubling. The proof and article explicitly split this case before invoking minimum growth.

## Exact arithmetic replay and provenance

The committed tests/test_erdos_compendium_0481_affine.py checks five cases exactly using integer and Fraction arithmetic. All **5 PASSED** on source head f20bd819e9f9ce533cdc82317f24133080c31ac0:
1. a=(2,2,3),b=(0,1,1), C=4/3, A_2=(2,3,4), distinct length-two words (0,2) and (1,1) yield A_3 value 7.
2. a=(1,2),b=(0,0) identity exception and level-three collision.
3. Minimum-growth and reciprocal-sum recurrence checked at unique early generations.
4. a=(2,3,6),b=(0,1,1) has C=1 and still collides: theorem criterion sufficient, NOT necessary.
5. a=(2,2),b=(0,0) already collides in A_2, showing that silently taking a set instead of a list discards the witness.

Authenticated original issue RESULT/1 return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/1751#issuecomment-6168823640; author fyremael, LF-normalized SHA-256 **2732492750767103ee0ada41e0947eda66a805d4ef77891f0ad0aad2878328ec**, PARTIAL (historical sign domain).

Six-section manuscript: governance/erdos_compendium/editorial/0481.md, stripped UTF-8 SHA-256 **b2f51c5ddea6f57434ea67652923fef027c863b9aa5cad0e8699ef72c4a5d407**, raw bytes SHA-256 **f86a8cbecfdc43cb1aec64c164742dd054016999ddce30269d732888ba72b894**. All six required headings appear once; balanced dollar-sign math delimiters.

## Formalization boundary and acceptance

GCL's pinned google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020 contains **no** FormalConjectures/ErdosProblems/481.lean (GitHub 404; protected manifest agrees). New upstream unpinned file blob **474c191091eae1f259da24da6769a3b645c6937f** declares List.Nodup under positive a_i and natural b_i but theorem body is \`by sorry\`. The maintained heading “PROVED (LEAN)” and contradictory formalized-statement metadata do not substitute for a trusted GCL Lean proof. No kernel replay/axiom closure reported.

Disposition: **CRITICAL_DRAFT_PASS_WITH_ORIGINAL_SIGN_DOMAIN_SOURCE_EXCEPTION_UNACCEPTED**. Credible and rigorous six-section exposition of the established modern theorem, but do not upgrade original historical signed-parameter source fidelity or certify the upstream Lean file. Bounded next task: compare original 1980 signs and B quantifiers with actual Klarner 1982 text, then independently formalize the self-contained harmonic proof (identity branch, minimum growth, reciprocal bounds) with zero proof holes. Full cohort pytest, strict MkDocs, browser MathJax and protected PR gates require separate exact-head receipts. This review is not the fixed deterministic 20-article sample and makes no novelty claim.
