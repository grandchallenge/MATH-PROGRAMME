# EC-ED02 — documentary acceptance evidence dossier for Erdős #7

State at submission: **CANDIDATE EDITORIAL ADMISSION**. This dossier is source and
rendering evidence, not a final acceptance, independent-login review or
mathematical proof certification. The ledger decision is effective only if
admitted by the independently approved, protected PR.

## Bounded mathematical subject

[Erdős Problem #7](https://www.erdosproblems.com/7) is the open
Erdős–Selfridge question: can finitely many *pairwise distinct odd moduli
greater than 1*, with selected residues, cover every integer? Existence is
semidecidable by a finite yes certificate; no global no certificate or
undecidability theorem is claimed.

The authored manuscript has six substantive sections and portable GitHub and
MkDocs mathematical delimiters. The source review checks exact mathematical
interfaces, **not** deep proof reconstruction:

- Hough–Nielsen (2019) necessary presence of a modulus divisible by 2 or 3.
- Balister–Bollobás–Morris–Sahasrabudhe–Tiba (2021) exclusion only of
  distinct **odd square-free** covering systems.
- Balister et al. (2022), Theorem 1.4 in
  [arXiv:1811.03547v1](https://arxiv.org/abs/1811.03547), page 4: for a
  distinct covering with least common multiple $L$, either $2\mid L$,
  $9\mid L$, or $15\mid L$. Odd requires 9 or 15 to divide the lcm; one individual
  modulus need **not** be divisible by 15.
- Bispels et al. 2026 is a repeated-modulus variant, not the all-distinct
  problem. Mian–Siddique 2026's lcm ≤ 10,000 formal exclusion remains an
  **author-reported** finite Lean result, without GCL kernel replay.

Finite examples independently count 57 covered and 48 uncovered among
105 residues for (3,5,7), residues (0,1,2), and 12 covered among 12 for
the mixed-parity (2,3,4,6,12) control.

Source documentation:
- [Exact GCL provider/source audit](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1276#issuecomment-6103364800)
- [Read-only critical review, source reconciliation and limits](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2556#issuecomment-6115648569)
- [Exact-manuscript source and rendering review](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2556#issuecomment-6118086838)

## Exact-source binding

Path: `governance/erdos_compendium/editorial/0007.md`.

Protected source checked at `f9a77a0772c2485b06ba3dcc3c4a6362707cbe30`,
Git blob `61eea384213a19d9d233116b6a7419ea6ae1e787`.

**SHA-256 of stripped UTF-8 text (the exact generator contract):**

`a559fac0a350f5d487509d980a9257dfdaa662bc11f67d0ae930557a0d14acc2`

A change to the manuscript bytes must invalidate the admission until a new
critical review and separate protected amendment.

## Actual deployed mathematical rendering and caveats

- [Successful exact protected Pages deployment](https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/38204827132)
- [Successful trust-scoped Chromium HTML/MathML run](https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/38204869030),
  artifact `11726986418`, preserved `readback.json` and screenshots.
- [Authenticated Council Clerk readback receipt](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2556#issuecomment-6117889968).
  The original receipt has a **display-only GitHub count defect**:
  `github_render.observed.renderedMath` is absent, printed as null;
  actual JSON records `github_render.renderedMath=51` and
  `github_render.renderer=native_mathml`.
- MkDocs DOM: 51 input expressions, 51 rendered MathJax CHTML nodes, with
  source/theorem/example, draft-warning, alt-text and JavaScript checks PASS.
- GitHub exact-head rich Markdown: 51 visible native MathML elements, no
  unprocessed maths, all substantive markers PASS; page screenshot captured.
- The protected probe used **actual browser DOM** on both surfaces rather than
  merely assuming success from a MkDocs build. This is a bounded presentation
  check; it is **not** an exhaustive WCAG compliance audit.

## Authority and acceptance boundary

- Worker `RESULT/1` on
  [EC-ED02 #2556](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2556#issuecomment-6108695648)
  was projected operationally to RETURNED by
  [protected Council Clerk run #38139713290](https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/38139713290).
- Corrective PRs [#2582](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2582)
  and [#2584](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2584)
  were protected-merged; #2582 received recorded non-author approval.
- Earlier same-identity read-only analysis does **not** impersonate a different
  editorial reviewer. The **ledger-admission PR requires an actual
  authorization by a non-author**, independent of the authored critique.
- The live-probe transition for a reviewed page (distinct from draft warning)
  is addressed separately in
  [PR #2586](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2586).
  That compatibility correction **must be protected-admitted before this
  admission PR is merged**. Otherwise the next trusted Pages verification
  would reject a valid accepted page.
- The ledger admission changes *documentary coverage only*. It does **not**
  close the Erdős conjecture, accept a mathematical proof, issue a MathCert
  certificate, forge a second login, or mark the editorial worker issue DONE.
  Issue/Project closure is a distinct authorized operation.

## Acceptance review instructions

Verify the exact SHA-256 and all seven ledger fields; independently check the
linked source, critical and DOM evidence. Check #2586 is already merged and
that the current branch's generator, hostile replay tests, and complete
required Programme policy checks pass. Approve through normal protected
non-author review and merge queue; **do not bypass the requirement or approve
based only on well-formed link syntax**. Once the ledger PR actually merges,
verify the post-merge strict MkDocs site reports reviewed=1, pending=1,
legacy=3, catalogue=1221, and that the post-merge browser check passes for
the **reviewed** (not draft) page.

