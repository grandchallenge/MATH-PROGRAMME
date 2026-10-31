# OAI-26 Family 001 — pinned-primary-PDF source audit

Record type: `GCL_OAI26_ED01_F001_SOURCE_AUDIT/1`

## Identities

- Work package: [OAI26-ED-01, #2901](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2901).
- Source: `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`, 36-page October 7, 2026 *Milne's rationality conjecture for abelian varieties* PDF, Git blob `3780abc1f47a23e546f28190bd3db7b24419f1f9`.
- The PDF was fetched through the authenticated GitHub Git-blob API (595,267 bytes) and independently checked with `git hash-object`; output matched the above blob. Source extraction was performed by `pypdf`.
- Target authored editorial manuscript: `governance/oai26_documentary/editorial/001.md`, Git blob `c9aed1b647f3c65a2315ed44b23ed6aa06e8d443`, already protected by [PR #2940](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2940).
- Separate bounded critical-review evidence: [PR #2945](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2945), protected merge `28540da0b8d07081778e642b7a576b519d193cf1`.

## Primary-PDF passage concordance

| PDF pages | Exact source object | Editorial article's treatment | Disposition |
| --- | --- | --- | --- |
| 1–2 | Theorem 1.1: fixed prime and place, dimension d, 0 <= r <= d, any complementary Cartier divisor list, common q in Q across all prime-to-p and crystalline traces | Describes the same per-class/per-list quantifiers; no across-place comparison | SOURCE_FIDELITY_PASS |
| 2–5 | Origins, absolute-Hodge and comparison inputs, two auxiliary constructions, proof overview, Figure 1 | Correctly distinguishes CM auxiliary from separately prescribed-filtration auxiliary; no claimed map between their generic fibers | SOURCE_FIDELITY_PASS |
| 17 | Corollary 3.4: CM auxiliary and a single special-fiber rational quasi-isogeny with equality in all stated realizations | Correctly identifies special-fiber transport | SOURCE_FIDELITY_PASS |
| 17–23 | Theorem 4.1: constrained weak-admissible filtration and local-field descent | Accurately summarized as a claimed construction, not independently verified | SOURCE_FIDELITY_PASS_WITH_QUALIFICATION |
| 24–28 | Proposition 5.2: zero Lefschetz pairings without invertible u, or a simultaneous rational Lefschetz class with invertible u | Reports both branches and divisor identity, without asserting proof certification | SOURCE_FIDELITY_PASS |
| 29–31 | Lemma 6.1: rational-idempotent CM reduction, rational-span descent; Theorem 1.1 proof on p. 31 | Preserves the proof roadmap and rational-pullback limitation | SOURCE_FIDELITY_PASS |
| 31–33 | Corollary 6.3: membership in one fixed good theory | Explicitly not algebraic-cycle representation | SOURCE_FIDELITY_PASS |
| 33 | Corollary 6.4: algebraic cycle on special fiber under an additional CM Hodge theorem [OAI26, Theorem 1.1] | Distinguishes conditional algebraicity from Theorem 1.1 | SOURCE_FIDELITY_PASS |

## Source-critical determination

The exact authored explanatory article is **faithful to the checked claims and qualifications** of the pinned primary PDF. The elementary elliptic-curve example is illustrative only. The PDF claims the results; this source audit neither confirms the underlying mathematical truth nor assigns a Lean/Comparator or MATHCERT outcome.

**Unresolved external mathematical dependencies:** the exact applicability of Kisin–Zhou, Pappas–Rapoport, GLX integral-uniformization and characteristic-two hypotheses; rational normalization details and finite local-field descent; separately cited CM Hodge theorem. These are substantive proof-verification obligations and must not be silently classified as verified.

**Coverage limit:** A bounded theorem/dependency/passages source audit, **not** line-by-line fidelity checking of every page of the 36-page PDF or every cited external paper. The editorial article makes no claim of that broader coverage. The reviewed passage concordance is sufficient to support the *bounded descriptive claims* of the current six-section article, subject to the separate editorial-admission process; it does not establish an external theorem certificate.

## Result

`SOURCE_AUDIT_BOUNDED_PASS / CRITIC_EVIDENCE_SEPARATELY_PROTECTED / EDITORIAL_ADMISSION_NOT_YET_GRANTED / NO_CERTIFICATION`.

The companion strict-site/HTML evidence is [PR #2944](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2944), with local strict build successful; deployed browser MathJax was not independently visually checked. Keep the parent #2901 open for remaining families.
