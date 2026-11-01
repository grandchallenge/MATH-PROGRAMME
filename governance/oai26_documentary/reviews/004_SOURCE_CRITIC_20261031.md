# Family 004 — source and editorial-critical disposition

Record: `GCL_OAI26_F004_SOURCE_CRITIC/1`. Source lock `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`.

## Evidence chain

Main PDF `b75dddd5e05503cc04a156e94bb15d6fadf8158e` (62 pages) and companion PDF `1d35e83ccc541890903bfa978c1f0f73972843ca` (91 pages), with verified repository Git blob identities. Original source examination is preserved in [ED-01 issue #2901](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2901): main Theorem 1.1 physical p. 3, §1.2 p. 5, Corollary 7.1 p. 56, and §§3.3–3.4 pp. 21–24; companion Theorem 1.1 introductory pages. Relevant source-audit comment identifiers: `6532469600`, `6533518886`, `6542630207`, `6542717565`, `6542811338`, `6549723358`, `6550741822`.

## Separate critical questions

- **Claim and scope:** The main paper asserts undecidability of rational solvability for arbitrary integer-coefficient polynomials with variable count. A corollary claims restricted forms and Turing degree `0'`. The six-section article attributes, but does not endorse, these claims.
- **Companion dependence:** Pointwise 2-converse requires rational 2-torsion and full two-power Selmer corank at most one. The article reports it as a claimed input and does not conflate the result with full BSD.
- **Local proof chain:** At the constructed elliptic curve, the arithmetic of a 3-dimensional 2-Selmer group and 2-dimensional rational 2-torsion gives `rank + dim_F2 Sha[2] = 1`. Conditional on full Selmer-corank eligibility and the companion's finiteness conclusion, perfect alternating Cassels–Tate pairing implies `Sha[2]=0`, so the selected Selmer class comes from a rational point. The source pp. 23–24 contains this step.
- **Unverified antecedents:** The matrix-rank hypothesis (3.11), support-prime existence, all local Kummer equalities including (3.15), and the global undecidability reduction were not independently established. Earlier finite-field identity (3.8)–(3.10) was checked and (3.11) expressly remained a hypothesis; a conditional proof is not an unconditional certificate.
- **No false certification:** The new draft explicitly states `DRAFT_UNACCEPTED` and `NO_CERTIFICATION`; it neither claims Lean correspondence nor a MATHCERT verdict.

**Critic verdict:** `ACCEPTED_EXPOSITION_WITH_LIMITS` for a bounded, publisher-attributed, source-faithful description of the claim and specific Lemma 3.4 proof route. The record is **not** an independent full-page proof audit of 62+91 pages, nor a correctness verdict on Hilbert's tenth problem over the rationals. The accepted scope is explanatory and conditional, not mathematical certification. This finding supports consideration of exact-manuscript-hash editorial admission after validation and protected readback.

Article: `governance/oai26_documentary/editorial/004.md` on the same candidate branch; tie admission to exact content SHA-256 measured after writing. Parent #2901 remains open for Families 005–016.
