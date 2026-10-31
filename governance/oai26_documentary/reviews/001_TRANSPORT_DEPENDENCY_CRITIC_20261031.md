# OAI-26 Family 001 — transport and source-dependency editorial critic

Record type: `GCL_OAI26_ED01_F001_DEPENDENCY_CRITIC/1`

## Identity and disposition

- Work package: [OAI26-ED-01, Programme #2901](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2901).
- Exact reviewed article: `governance/oai26_documentary/editorial/001.md`, Git blob `c9aed1b647f3c65a2315ed44b23ed6aa06e8d443`, protected predecessor `8f630df438e5a0d501b73b805cf99a8fc92d2df2`.
- Primary paper: `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`, 36-page PDF Git blob `3780abc1f47a23e546f28190bd3db7b24419f1f9` (retrieved from the GitHub blob API; `git hash-object` agreed).
- Review role: logically distinct source-dependency and mathematical-editorial critic; **not** an independent external mathematics certificate.
- **Disposition: EDITORIAL_CLAIM_BOUNDARIES_PASS; EXTERNAL_DEPENDENCY_PROOF_AUDIT_UNRESOLVED; NO_CERTIFICATION.** This review supplies critic evidence, not standalone authority to set `EDITORIALLY_ADMITTED`.

## Claim and proof-chain check (source-faithfulness)

1. **Theorem 1.1, PDF pp. 1–2.** The premise is an abelian variety over the algebraic closure of the rationals with good reduction at a fixed chosen p-adic place, and a rational Hodge class of codimension `0 <= r <= d`. For *each* chosen complementary list of Cartier divisors on the special fiber, a single `q in Q` gives the normalized trace in all prime-to-p ell-adic realizations and the crystalline realization at p. It does **not** assert one q independent of divisor choices or comparison between different reduction places. The article accurately retains these restrictions.
2. **CM transport, Corollary 3.4, p. 17.** The simultaneous equality of specializations uses the *same rational special-fiber quasi-isogeny* and a CM auxiliary class. The article accurately avoids alleging an actual generic-fiber map. Critical input chain to check if seeking a mathematical correctness verdict: Proposition 3.1, especially its local Shimura integral-uniformization and rational normalization; cf. the strongly admissible construction described on PDF p. 9 and the uniformization/Dieudonne-lattice and special-fiber marking on pp. 13–14.
3. **Balanced Weil route, Proposition 5.2, pp. 24–28.** The alternative without an invertible Rosati-symmetric conjugate-linear endomorphism yields zero pairings (Lemma 5.3, pp. 24–25); the invertible case constructs a divisor, constrained weakly admissible filtration (Theorem 4.1, pp. 17–23), and rational divisor identity via Lemma 5.4. In the source, Proposition 3.1 then realizes a local auxiliary lift while preserving the marked first summand (pp. 27–28). The article correctly identifies these as assertions of the manuscript, not verified theorems of GCL.
4. **CM reduction and main proof, Lemma 6.1 and Theorem 1.1 proof, pp. 29–31.** Rational idempotents of powers and descent of the *rational span* of determinant classes are essential. The reduction does not require each individual eigenspace component to descend to Q; the source explicitly makes this distinction (p. 31). The article's summary is accurate but does not itself establish the descent argument.
5. **The two corollaries, pp. 31–33.** Corollary 6.3 asserts membership of all specialized rational Hodge classes in one *fixed good theory* of rational Tate classes, and expressly says this does not yield an algebraic cycle. Corollary 6.4 invokes the additional claimed CM Hodge theorem `[OAI26, Theorem 1.1]` to obtain one rational algebraic cycle on the **special fiber**; the source explicitly disclaims algebraicity on the original generic fiber and uniqueness of the cycle up to rational equivalence. The article keeps the two conclusions distinct.

## Dependency critique and open tests

The central *potential* proof-sensitive points are not demonstrated errors. They are precisely the external statements whose applicability requires a separate source-level verification before anyone asserts an independent theorem-proof verdict:

- **Strongly admissible integral-model inputs, including residue characteristic two:** PDF pp. 9–14 depend on Kisin–Zhou, Pappas–Rapoport and GLX uniformization hypotheses. Audit the exact editions, the full-stabilizer/connected-special-fiber and root-system assumptions, framed point existence above a prescribed period, and integral special-fiber marking.
- **Finite local-field descent and realization of a prescribed weakly admissible filtration:** PDF pp. 17–23 and 27–28 use filtered isocrystal/subobject inequalities and local-model realization; check that the auxiliary field and tensors descend together. A rational class being compatible in each realization does not automatically establish one common rational normalization without the stated divisor-ratio argument.
- **Endomorphism and divisor lifting:** PDF pp. 24–28 require faithful rational actions, Rosati relations, specialized projectors and injectivity of specialization. A rational divisor identity on the auxiliary lift must be transported back with coefficients independent of realization.
- **Conditional algebraicity:** The referenced CM Hodge theorem is additional and not checked in this review. Do not imply Corollary 6.4 follows from Theorem 1.1 without it.

## Editorial determination

For a **documentary exposition**, the six-section article accurately attributes claims to the source and withholds independent proof/certification. No contradiction with the inspected primary-PDF passages was found. The elliptic curve degree example is explicitly heuristic and cannot serve as evidence of the general theorem.

**Accepted editorial scope of this critic:** correctness of the article's bounded theorem statement, special-fiber transport distinction, proof roadmap, conditional corollary distinction and noncertification boundaries, at the exact article blob above.

**Not accepted by this critic:** mathematical truth of the external uniformization inputs; full line-by-line verification of all 36 pages and all bibliography; exact Lean correspondence or Comparator verdict; MATHCERT; browser-level deployed MathJax; permission to promote by this record alone.

Supporting protected rendering record: `governance/oai26_documentary/reviews/001_HTML_READBACK_20261030.md` (PR #2944). The public-editorial admission remains a separate exact-article-hash protected transaction, with explicit `source_audit_url`, `critic_evidence_url`, `protected_admission_url` and a valid SHA-256; do not close parent #2901 for this one family.
