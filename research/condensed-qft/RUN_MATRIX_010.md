# QFT-COND-005 / LFO-010 — Verification matrix

| Control | Method | Outcome | Interpretation |
| --- | --- | --- | --- |
| Strict-LF-output mixed support-stage Hom description | Written Grothendieck-factorization proof and source audit | PROVED under strict LF/nuclear Fréchet hypotheses | Underived smooth multilinear mapping sets only |
| Grothendieck support-stage factorization | Smirnov Lemma 1 and strict LF stage regularity | SOURCE-BACKED | Not simulated by finite Python |
| Identity map no uniform target support | Direct proof and finite support-stage adversary | PASS | Counterexample to swapping outer limit and inner colimit |
| Nuclear Fréchet/liquid Hom at each fixed support stage | Existing Clausen–Scholze and fully faithful Fréchet realization | SOURCE-BACKED | Does not prove unrestricted LF-output liquid Hom formula |
| Borel full jet surjection and finite jet sections | Classical Borel theorem plus explicit polynomial sections | PROVED | Every finite jet map splits continuously linearly |
| Infinite jet no continuous linear section | Product-topology seminorm argument | PROVED | Nonzero strict nuclear Fréchet Yoneda extension |
| Finite exact jet matrices | Python `fractions.Fraction`, N up to 24 | PASS | Regression control; not an infinite proof |
| Finite LF identity support/adversarial bilinear kernel | Python rational model | PASS | Regression control; not a proof of topology theorem |
| Python compilation | Python 3 `py_compile` | PASS | Syntax verified |
| GitHub math-rendering source gate analogue | Native inline dollar and blank-line display delimiter checks | PASS | Actual MkDocs rendering not asserted |
| Relative liquid Hom–filtered-colimit property LFO3 | Open mathematical hypothesis | UNPROVED | Needed for full LF-output liquid Hom comparison |
| Strict Frechet Ext class transfer to derived liquid | Exactness/Ext comparison not checked | UNPROVED | Not claimed |
| Smooth-enriched Costello–Gwilliam B.6 equivalence | Not established | UNPROVED | Remains QFT-COND-004/005 research gate |
| Protected GitHub merge | No verified admission | NOT CLAIMED | Local files only |

**Source audit:** Smirnov, *On kernel theorems for (LF)-spaces*, Lemma 1; Costello–Gwilliam, *Factorization Algebras in QFT* Vol. 1, B.6.1.1 and C.1.0.5–C.1.0.6; classical Borel theorem and the infinite-jet non-splitting argument; Clausen–Scholze liquid nuclear Fréchet tensor theorem.

The strict Fréchet Yoneda extension class is a theorem in that exact category only. Do not export it to the derived liquid category without a separate exactness proof.