# OAI26-ED-01 Family 001 — exact-protected-head publication-rendering readback

Record type: `GCL_OAI26_FAMILY001_HTML_READBACK/1`

## Immutable input identities

- Repository: `grandchallenge/MATH-PROGRAMME`
- Protected `main` checked out at `73cac49c368e43ba09f566e68d1ee7a1929d485e`, PR #2940 merge
- Reviewed manuscript: `governance/oai26_documentary/editorial/001.md`
- Manuscript Git blob: `c9aed1b647f3c65a2315ed44b23ed6aa06e8d443`
- Primary PDF: `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`, Git blob `3780abc1f47a23e546f28190bd3db7b24419f1f9`

## Exact-head validation

An isolated detached worktree at `73cac49` ran the following checks, all with exit code zero:

1. `python3 ci/math_markdown_gate.py --file governance/oai26_documentary/editorial/001.md` — PASS.
2. `python3 -m unittest tests.test_oai26_compendium -q` — 7/7 PASS.
3. `python3 ci/oai26_compendium.py check` — 372 families and 719 source manuscript paths, PASS.
4. `mkdocs build --strict -d /tmp/gcl-ed01-2940-site` — exit code zero, entire site generated.
5. Generated `oai26/families/001/index.html` inspected using a separate read-only check: HTML file exists, 43,248 bytes; contains `DRAFT_UNACCEPTED` (twice), `NO_CERTIFICATION` (twice), `PINNED_PDF_SELECTED_PASSAGES_FIDELITY_REVIEWED` (once), two `arithmatex` markers and a pinned Family 001 PDF hyperlink.

The full-site build emitted informational messages about unrelated preexisting navigation exclusions and seven unrecognized legacy `documentaries/github_math/*` links. These did not fail `--strict`; this record does not certify those unrelated links.

GCL CONTROL execution IDs and local receipt digests:

- Source and unit replay: `75f82c9877104392bed9a8fc98597ebc`, receipt SHA-256 `bc0c591821119b792005ed3066b4e29046b2665bc9da126d3dac6c22b0ce67b7`
- Strict site build: `01e9ea44958c478392e28432db38f463`, receipt SHA-256 `8cf6b38042360172531b6601b94f3b851cd1bc7c48201e60533acbc210048426`
- Family 001 HTML readback: `bcfcd624f74a4114916ab15447ffb7c7`, receipt SHA-256 `61c7c60a4f12eb830ebf5b6f463fcaf9031775caeed7967212d9fc7c8f6bc9af`

## Deliberate nonclaims and successors

This evidence closes **local full-site strict build and generated HTML structure checks** for the exact protected article. It is not a live deployment check, browser MathJax glyph inspection, mathematical proof certification, or independent verification of the primary manuscript's external source dependencies.

The editorial admission registry was unmodified and its earlier state was `NO_EDITORIAL_ADMISSIONS_YET`. Family 001 is deliberately still `DRAFT_UNACCEPTED`. Before a separate exact-hash editorial admission, reconcile substantive source-dependency review findings and obtain any required public deployment/browser checks. Do not close ED-01 parent #2901, which includes another 15 families.
