# OAI-26 documentary compendium: editorial protocol

This compendium follows the Erdős six-section manuscript standard. The primary source lock is `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`. Bibliographic identity is imported without edits from the protected MATHFORGE `MANUSCRIPT_INDEX.json` Git blob `7a0b00eb9bfdeb59b157a98ee6522fc685580152`. It represents **372 families and 719 unique manuscript paths**. An index entry is not an independent mathematical claim.

## Three distinct coverage dimensions

1. **Catalogue presence:** every family has a public source-linked reference page, searchable by its stable 3-digit family ID. These generated reference pages must visibly say `REFERENCE_ONLY`, must not invent a precise theorem statement or a worked example, and do not qualify as reviewed articles.
2. **Authored explanation:** `docs/oai26/editorial/NNN.md` is an exact-source, six-section manuscript. Every draft must clearly distinguish literature context, a independently checked small example, what the source asserts, GCL proof replay, proposition-level inspection, semantic equivalence and mathematical correctness. Until admitted, it appears as `DRAFT_UNACCEPTED` and must not count as a reviewed article.
3. **Editorial admission:** occurs only after a dated source audit, non-author role-scoped critical read, normalized hypotheses, correct example, exact file SHA-256, strict MkDocs build and browser/MathJax inspection, protected PR admission and readback. The protected `EDITORIAL_ADMISSIONS.json` must name the manuscript digest, source audit, critic evidence, and protected admission. No independent physical GitHub login is required for routine logical roles. This is not mathematical certification.

## Required article headings

- The question in plain language
- A small example
- What is known
- GCL verification state
- What remains
- Sources and claim boundaries

Source history and repairs must be edition-bound. The three withdrawn publisher titles must be excluded from active acceptance; dependency reuse requires explicit source checks. The 14 repaired manuscripts and 13 citation editions must not be presented as individually reconciled until each edition is witnessed. Family 342 and Family 376 are required revision-risk regression fixtures.

## Deterministic controls and next editorial wave

Run `python3 ci/oai26_compendium.py check` and `python3 -m unittest tests.test_oai26_compendium -q`. The site build invokes `ci/oai26_compendium_hook.py`, generates the source pages only in a temporary build lifecycle, verifies rendered sentinels, and removes marked generated Markdown. Use `mkdocs build --strict` and follow it with actual site/browser inspection before claiming public publication. Independently verify article math rendering and any external manuscript links.

First substantive wave: the original pilot 001–012, with a separate revision-risk wave for 342 and 376. Three seeded explanatory drafts (003, 342, 376) are deliberately **unaccepted** until their source and editorial reviews are complete. Continue in bounded cohorts, report counts of reference pages, unaccepted drafts, reviewed articles, Lean evidence and mathematically certified claims separately. Neither site generation nor a successful CI run promotes a theorem.
