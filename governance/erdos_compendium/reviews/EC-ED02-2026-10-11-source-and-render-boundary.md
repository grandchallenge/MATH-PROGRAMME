# EC-ED02 — Erdős #7: non-authoring source and publication-boundary assessment

Date: 2026-10-11. Scope: the authored manuscript at
`governance/erdos_compendium/editorial/0007.md` and its linked evidence.
Disposition: **SOURCE_CLAIMS_BOUNDED_PASS; PUBLIC_HTML_UNVERIFIED; EDITORIAL_ACCEPTANCE_WITHHELD**.

This review is a distinct **read-only logical critical pass**, not an independent
external academic identity, a protected GitHub approval, a replay of the deep
proofs, or GCL mathematical certification. The authoring and checking work
use the same available operational identity. Review observations are
documentary evidence only; a separate protected admission decision is required.

## Primary-source claim concordance

1. **Object and quantifiers**: finite family of congruences, pairwise distinct
   odd moduli greater than one; union equals all integers. The open
   [Erdős #7 catalogue entry](https://www.erdosproblems.com/history/7)
   and [source audit #1276](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1276)
   match. A YES has an exact finite periodic certificate. This does not
   imply an algorithm terminating on every NO instance. PASS.
2. **Hough–Nielsen (2019)**:
   [authors' full text](https://www.math.stonybrook.edu/~rdhough/covering_restricted.pdf),
   Theorem 1, printed page 2, states that every distinct covering system has
   a modulus divisible by 2 or 3. With only odd moduli, a modulus divisible
   by 3 is necessary. The deep proof was not replayed. PASS source interface.
3. **Balister–Bollobás–Morris–Sahasrabudhe–Tiba (2021)**:
   [authors' preprint](https://arxiv.org/pdf/1901.11465), Theorem 1.1,
   printed page 2, proves that every covering by distinct square-free
   moduli has an even modulus. Hence no covering exists using only distinct
   odd square-free moduli. It does **not** rule out nonsquarefree odd moduli.
   PASS source interface.
4. **Balister et al., Inventiones 228 (2022)**:
   [arXiv:1811.03547](https://arxiv.org/pdf/1811.03547), Theorem 1.4,
   printed page 4 of publicly accessible version 1, states
   $\,2\mid L\ \lor\ 9\mid L\ \lor\ 15\mid L\,$ for a distinct covering
   with $L$ the lcm of its moduli. With every modulus odd, this becomes
   $9\mid L$ or $15\mid L$. The authors explicitly caution that
   $15\mid L$ does *not* establish $15\mid m_i$ for one modulus.
   This resolves the **theorem-location obligation left open** in the
   EC-ED02 original RESULT/1; this is a preprint-to-journal theorem
   interface check, **not a full proof replay**. PASS with version qualifier.
5. **Bispels et al., Discrete Mathematics 349 (2026), 115013**:
   [publisher abstract](https://doi.org/10.1016/j.disc.2026.115013)
   explicitly studies one modulus permitted to repeat. This is not
   the all-distinct odd covering question. PASS variant distinction.
6. **Mian–Siddique 2026**:
   [arXiv:2607.25628](https://arxiv.org/abs/2607.25628) reports
   kernel-checked finite exclusion through lcm 10,000, not an unrestricted
   impossibility theorem. We did **not** fetch/replay their Lean files or
   recheck kernel axioms. PASS cautious attribution only.

## Independent elementary replay

Pure integer enumeration over the full lcm period:

- For $(m_i,a_i)=((3,0),(5,1),(7,2))$: lcm $105$;
  uncovered $48$, covered $57$. CRT gives $2\cdot4\cdot6=48$;
  $n=4$ is an explicit uncovered residue.
- For $(2,0),(3,0),(4,1),(6,5),(12,7)$: lcm $12$;
  uncovered $0$, covered $12$, but not an all-odd example.

These checks verify the pedagogical fixtures, **not** the main conjecture.

## GitHub/MkDocs/HTML/authority boundary

- The source manuscript merged in [PR #2577](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2577)
  at head `0b5897bbbf0de699f59ae312586bbcd662b24873`.
- Worker [RESULT/1](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2556#issuecomment-6108695648)
  was transported to Project **RETURNED** by
  [Council Clerk #38139713290](https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/38139713290),
  with [parent readback](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2552#issuecomment-6109065121).
- [MkDocs Pages deployment #38137356772](https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/38137356772)
  completed successfully against merger commit
  `2a6b6de70229f760f924270ab03387b2d16ae461`.
- **Direct public page HTML, rendered MathJax/KaTeX formula glyphs, internal
  links, accessibility and actual GitHub rich Markdown were not observed
  from this review runtime**; the public website URL returned no accessible
  page body. A successful deployment job is not equivalent to a
  page-specific HTML/rendering acceptance record.
- The generator previously promoted *any* merged manuscript automatically.
  The associated corrective PR replaces that with exact-hash, evidence-linked
  editorial admissions; legacy exemplars #1–#3 remain expressly qualified.
  As of this review, #4 and #7 remain pending separate acceptance.

## Follow-up

1. Protected gate PR CI and non-author approval; no required-check shortcut.
2. Verify direct public URL
   `https://grandchallenge.github.io/MATH-PROGRAMME/erdos/problems/0007/`
   against expected source and mathematics after corrected deploy;
   capture a durable issue-comment receipt with rendered formula checks.
3. Provide a distinct *logical* non-authoring acceptance review of the amended
   exact SHA (identity independence is not implied).
4. Only after proof of these editorial predicates, append a source-hash-bound
   record to `EDITORIAL_ADMISSIONS.json` through a separate protected PR.
5. The original conjecture is still open and no Solve/Cert authority changes.

