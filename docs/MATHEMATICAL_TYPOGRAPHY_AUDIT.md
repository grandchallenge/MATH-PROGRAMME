# Mathematical typography: GitHub and MkDocs compatibility

This page describes the repository-wide mathematical typography audit. The public record is the [machine-readable audit inventory](https://grandchallenge.github.io/MATH-PROGRAMME/math-typography-audit.json), generated from the exact protected documentation build. That inventory enumerates file paths, line numbers, diagnostic classes, and short source excerpts. It is an *audit*, not a claim that every historical file has been repaired.

## Source-first mathematical Markdown contract

**Binding rule for new work:** Mathematical Markdown must be correctly typeset in its first committed source. Do not defer repairs until after protected merge. The required classifier runs `ci/math_markdown_gate.py` across **all added or modified Markdown files**, including research notes outside the public docs directory. It compares candidate markup to the exact protected-base source, allowing unchanged historical defects but rejecting every new defect.

A valid inline expression has paired single-dollar delimiters on the same line. A display expression has two standalone double-dollar delimiter lines, a nonempty TeX body, and blank lines separating it from prose. Inline math cannot touch words or hyphens. Unmatched/legacy math delimiters and unsupported operator macros fail this source gate. Code fences and inline code remain literal.

**Before opening a PR:** `python3 ci/math_markdown_gate.py --file path/to/note.md`. The repository classifier runs the equivalent diff-bound check automatically on PR and push transitions.

For public reading editions the strict MkDocs build and rendered-Arithmatex check additionally verify that the manuscript's equations reached the HTML math renderer. Such checks do not prove actual browser-side MathJax glyph painting, which remains a separate acceptance step. This contract does not change mathematical certification boundaries.

## What is checked

- **Repository Markdown source (GitHub compatibility):** every Markdown file outside generated/build directories is examined for legacy math delimiters, disallowed operator macros, math attached to prose, and suspicious unpaired dollar delimiters. Inline code and fenced code blocks are excluded. Findings inside HTML are labelled separately from ordinary Markdown.
- **MkDocs rendering:** every documentation page containing standard dollar-delimited mathematics is checked against the actual built HTML. The audit counts Arithmatex wrappers and reports missing pages or fewer rendered math wrappers than source formulas.
- **Enforced regression boundary:** the [CM4 mathematical note](CMDG_CM4_MATHEMATICAL_NOTE.md) and [Condensed Mathematics for the Perplexed](CONDENSED_MATHEMATICS_FOR_THE_PERPLEXED.md) must pass both source-compatibility and rendered-wrapper checks. Other historical findings remain visible in the inventory for systematic triage.

## Authoring conventions

Use dollar-delimited math in ordinary Markdown shared between GitHub and MkDocs. Inline math uses $x+y$; display math uses matching double-dollar delimiters on separate lines, with blank lines around the display. Leave mathematical commands inside the delimiters and ordinary punctuation and hyphenation outside them. Prefer explicit prose, such as “derived Hom ($\mathrm{RHom}$)”, to a hyphen adjoining a math delimiter. Use \mathrm for identifiers where the GitHub renderer rejects the operator macro; do not mechanically replace genuine operator semantics without checking meaning.

Code examples use fenced code blocks; mathematical and Lean source names appearing as literal code use inline code formatting. Do not convert mathematical syntax inside verbatim source files, quoted records, or intentionally hand-authored HTML without examining the owning renderer.

Documentary/monograph pages sometimes contain hand-authored HTML and an independent pinned MathJax loader. Those occurrences are **reported separately**. They cannot safely be bulk-rewritten as though they were ordinary Markdown.

## How to reproduce

The docs policy shard executes the audit after a strict MkDocs build. The script can also be run independently:

```sh
python3 ci/audit_math_typography.py --root . --site-dir site --output site/math-typography-audit.json --gate
```

The inventory is generated on each successful protected build and becomes part of the published documentation artifact.

**Limitations:** a source syntax check cannot prove that GitHub's browser-side MathJax renderer accepts every mathematical command. Arithmatex-wrapper inspection proves that Markdown reached the math rendering layer, not that browser-side JavaScript painted every glyph correctly. Those are distinct tests and require live-renderer/browser validation. The audit preserves that distinction instead of claiming visual correctness from a successful build.

---

## ED07 — Public mathematical-typography remainder ledger

**Campaign:** [MATH-TYPOGRAPHY-REMEDIATION-001, issue #1255](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1255).  
**Assignment:** [MP-MATH-TYPO-ED07, issue #1262](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1262).  
**Original protected source lock:** `afa10e54ced2dd88f9ce07e38246641c1162d7cf`.  
**Scope:** every `docs/**/*.md` file, excluding the specific files assigned to ED01–ED06, the two protected CM4/condensed flagships, and all non-`docs` archives, campaigns, records, and research.

#### Method and denominator

The protected tree contains **192** public Markdown files. All 192 were fetched and examined using the same exclusions and source-diagnostic logic as `ci/audit_math_typography.py`: fenced/inline code excluded; script/style bodies excluded; raw HTML distinguished from ordinary Markdown; legacy inline and display delimiters, `\\operatorname`, math/prose adjacency, and unpaired dollar markers recorded with exact original line numbers. The full repository audit is a separate, larger denominator.

On this protected snapshot the public pages contained **177 line-level audit diagnostics**: **129** in files explicitly assigned to ED01–ED06 (tracked separately below) and **48** in the **nine** files eligible for ED07. Duplicate kinds on one source line count as distinct findings; each eligible path was deduplicated for editing.

| Category within ED07 | Original findings | Candidate action | Candidate source findings |
|---|---:|---|---:|
| Six ordinary public guides/mandate documents: old math delimiters | 29 | Convert `\\(...\\)` into `$...$` without changing the TeX body | 0 |
| Two documentary HTML editions: valid pinned MathJax forms | 18 | Leave TeX untouched; repair independently confirmed raw Markdown headings/tables | 18 |
| Erdős-024 governance note: unescaped dollar currency | 1 | Escape the literal currency dollar to prevent a false mathematical opening delimiter | 0 |
| **ED07 subtotal** | **48** | **Nine substantive files, plus this ledger** | **18 (intentional documentary forms)** |

**Critical semantic exception:** the Euclid guide's original line 87 wrapped a literal protected Git commit identifier in math delimiters. This was not a mathematical formula. The candidate now shows the *unchanged* identifier as parenthesized inline code, avoiding an accidental double-dollar display interpretation when Markdown strips code spans. Of the six guides' 58 originally delimited spans, **57 genuine TeX formula bodies remain byte-identical** and this one source identifier is corrected as code. No mathematical claim or source SHA is changed.

#### Original line-by-line public-page finding inventory

Every line number in this table is from the locked protected base above. The line numbers in the new candidate may shift after converting HTML tables. A set of numbers refers to audit **diagnostics**; line 36 of the Yang–Mills documentary has two separate diagnostics.

| File (prefix `docs/` omitted) | Original line numbers | Findings | Triage and disposition |
|---|---|---:|---|
| `EUCLID_GCD_E2E_001_RESEARCH_GUIDE.md` | 28, 30, 55, 80, 87, 104 | 6 | Ordinary Markdown / confirmed GitHub source compatibility: repaired |
| `POINCARE_RECONSTRUCTION_RESEARCH_GUIDE.md` | 28, 30, 52, 81 | 4 | Ordinary Markdown / confirmed GitHub source compatibility: repaired |
| `VGSE_GEOMETRY_QUOTIENT_COUPLING_MANDATE.md` | 19, 50, 51, 52, 58, 76, 77 | 7 | Ordinary Markdown / confirmed GitHub source compatibility: repaired |
| `campaigns/VGSE_001_RESEARCH_GUIDE.md` | 38, 40, 60, 83 | 4 | Ordinary Markdown / confirmed GitHub source compatibility: repaired |
| `domains/PNP_001_RESEARCH_GUIDE.md` | 36, 38, 77, 91 | 4 | Ordinary Markdown / confirmed GitHub source compatibility: repaired |
| `domains/UC_001_RESEARCH_GUIDE.md` | 38, 40, 61, 80 | 4 | Ordinary Markdown / confirmed GitHub source compatibility: repaired |
| `documentaries/p_vs_np.md` | 13, 18, 21, 27, 28, 32, 42, 53 | 8 | Intentional documentary raw HTML/MathJax input; leave original TeX intact. The separate, confirmed HTML/Markdown leak is repaired |
| `documentaries/yang_mills.md` | 10, 14, 15, 20, 26, 30, 35, 36 (twice), 42 | 10 | Intentional documentary raw HTML/MathJax input; leave original TeX intact. The separate, confirmed HTML/Markdown leak is repaired |
| `governance/ERDOS_024_FORGE_COPILOT_PILOT.md` | 17 | 1 | False positive as *mathematics*: the original notation means USD 0.30, not inline math. Escape the currency dollar in ordinary Markdown |
| **Total** | | **48** | |

#### Documentary structural corrections (distinct from math diagnostics)

Both remaining documentary editions hand-author HTML and use a separately pinned documentary MathJax bootstrap that explicitly supports their delimiter forms. The protected MkDocs config does **not** enable `md_in_html`. Thus raw `##` headings and pipe tables nested in their hand-authored HTML can leak literally into the built page. This is a **confirmed MkDocs presentation/semantic markup defect**, distinct from the 18 valid MathJax source findings.

- P versus NP: 11 literal headings, one Markdown trust table with eight data rows, one raw bold status label. Replaced with native accessible `h2`/`table`/`strong` elements without altering any math or status cell.
- Yang–Mills: 11 literal headings, one Markdown trust table with nine data rows, one raw bold status label. Same semantic HTML repair, retaining the exact statements and trust statuses.
- Source MathJax warning diagnostics stay at eight and ten respectively. A GitHub *browser-side glyph check* remains **unverified**; local compatibility of a TeX expression is not proof that a remote client displayed it.

#### Protected boundary: findings excluded from ED07

The following **129** source diagnostics exist in pages assigned to other editorial packets on the locked protected base; none are silently counted as an ED07 repair. Earlier workers filed separate candidate PRs, which may still be awaiting protected admission.

| Existing owner | File(s) and diagnostic counts | Total |
|---|---|---:|
| [ED01 #1256](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1256) | `domains/BSD_001_RESEARCH_GUIDE.md` (12); `domains/HC_001_RESEARCH_GUIDE.md` (8) | 20 |
| [ED02 #1257](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1257) | `domains/NS_CI_001_RESEARCH_GUIDE.md` (11); `domains/YM_001_RESEARCH_GUIDE.md` (11) | 22 |
| [ED03 #1258](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1258) | `campaigns/OZ_001_RESEARCH_GUIDE.md` (12); `campaigns/OZ_001_STATUS.md` (0) | 12 |
| [ED04 #1259](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1259) | `documentaries/bsd.md` (25); `documentaries/riemann.md` (13) | 38 |
| [ED05 #1260](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1260) | `documentaries/hodge.md` (16); `documentaries/navier_stokes.md` (15) | 31 |
| [ED06 #1261](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1261) | `documentaries/poincare.md` (2); `documentaries/union_closed.md` (4) | 6 |
| **Excluded prior assignments** | | **129** |

Both flagship pages, `docs/CMDG_CM4_MATHEMATICAL_NOTE.md` and `docs/CONDENSED_MATHEMATICS_FOR_THE_PERPLEXED.md`, had zero source findings on the base and were not edited.

#### Deterministic unresolved remainder, next owners

1. **ED07's 18 intentional documentary syntax diagnostics:** `docs/documentaries/p_vs_np.md` lines 13, 18, 21, 27, 28, 32, 42, 53 and `docs/documentaries/yang_mills.md` lines 10, 14, 15, 20, 26, 30, 35, 36 (two kinds), 42. **Classification:** intentional MathJax input and/or unsupported direct GitHub static-file renderer; keep source unless independent browser rendering demonstrates a failure. **Next owner:** [ED08 #1263](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1263), critical live GitHub + MkDocs browser review.
2. **Other owners' 129 baseline diagnostics:** listed in the preceding ownership table. **Next owners:** ED01–ED06 PR protected admission and ED08 verification, not ED07 rewrites.
3. **Non-public repository files:** all warning occurrences outside `docs/` are outside this work packet; process archival and historical materials through the separately governed ED09 [#1264](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1264) or source-owning process. The whole-repository count must not be mistaken for 48 remaining public-facing defects.

#### Acceptance and replay instructions

Use `ci/audit_math_typography.py` and the built-site `site/math-typography-audit.json` to verify this lock, with `mkdocs build --strict`, `python3 ci/validate_rendered_docs.py`, and policy CI at the exact PR candidate. Check that the **nine edited public pages' before/after source diagnostics change from 48 to 18** and that the generated MkDocs HTML contains the intended article headings and tables. Confirm the 18 retained warnings occur solely in the two documentary pages, not ordinary Markdown guides.

**Evidence boundary:** the source audit is GitHub *syntax compatibility* evidence; the MkDocs HTML audit checks Arithmatex wrappers and documentary script presence, not the final browser MathJax glyphs. Browser-side visual verification and independent non-author protected PR review are required. This ledger is editorial evidence, not a mathematical certificate or admission authority.
