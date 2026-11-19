# EC-BULK-004 — Erdős #453 source and manuscript QA checkpoint

Record: `EC-BULK-004-0453-DRAFT-QA`
Date: 2026-10-13
Authority: local accountable-editor source and consistency check; **not independent identity, formal proof certification, or editorial admission**.

## Source comparison

- Original: Erdős–Graham (1980), printed p. 90, states that Pomerance disproved the eventual prime-product inequality. The adjacent density-zero speculation is separate.
- Primary: Pomerance, *The Prime Number Graph* (1979), printed p. 399 equation (1.1) and p. 400 Theorem 2.2 and corollary. Theorem hypotheses are strictly increasing positive $a_n$ with $a_n/n\to0$; conclusion is **infinitely many** $n$ satisfying the strict midpoint $>$ inequality for **all** positive $i<n$. The substitution $a_n=\log p_n$ preserves the hypotheses.
- Formal provider: `google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020`, `FormalConjectures/ErdosProblems/453.lean`, blob `a4313b258228fddfae8e925cd88783ce4a906d7d`. `Nat.nth Nat.Prime` is zero-indexed; the theorem body is `sorry` at this source lock.
- Exact issue: `ERDOS-CATALOGUE-0453-S01`, https://github.com/grandchallenge/MATH-PROGRAMME/issues/1723 . A complete six-section `RESULT/1` is staged in `governance/erdos_compendium/batches/EC-BULK-004_0453_UNPOSTED_RESULT.md`. **It has not been posted.** GitHub comment write attempts returned runtime safety blocks; no authenticated return or source-fidelity clearance is claimed.

## Reproduction and review boundary

- `ci/test_ec_bulk_004_math_fixtures.py` checks $n=3,5$ as good indices, $n=2,4$ as non-good indices, the first ten good indices up to 20, and the exact identity $(n+1)^2-(n-i+1)(n+i+1)=i^2$ for finite sample values. This is not an asymptotic proof.
- The draft has the six required expository sections and dollar-delimited mathematical expressions.
- Manuscript: `governance/erdos_compendium/editorial/0453.md`. Its SHA-256 after stripping leading/trailing whitespace is `c7fbb70aae19a38ca53280adc99b50aefaadcf9e83284d579af4519636f03061`.
- Local `pytest` and strict MkDocs pass; the generated page is unaccepted. No live-browser MathJax readback or protected V2 admission is claimed.
- This QA checkpoint does **not** satisfy the separate deterministic 20-article critical-review sample. Source-return posting and an independently executed critical pass remain outstanding.
