# Mathematical typography: GitHub and MkDocs compatibility

This page describes the repository-wide mathematical typography audit. The public record is the [machine-readable audit inventory](https://grandchallenge.github.io/MATH-PROGRAMME/math-typography-audit.json), generated from the exact protected documentation build. That inventory enumerates file paths, line numbers, diagnostic classes, and short source excerpts. It is an *audit*, not a claim that every historical file has been repaired.

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
