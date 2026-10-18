# GitHub mathematical source readers

These seven text-first pages are deterministically generated from the **canonical HTML documentary manuscripts**. They allow GitHub's Markdown renderer to typeset equations that GitHub does not parse inside the original elaborate HTML monographs. They are not separate authorships, theorem corrections, replacements for illustrated editions, mathematical certification or final publication approval.

The original files remain canonical. Each original links to its corresponding GitHub reader outside the HTML wrapper; the reader links back to the original.

| Documentary | Original formula bodies | MkDocs reader wrappers | Canonical browser math nodes | Reader browser math nodes |
| --- | ---: | ---: | ---: | ---: |
| Birch and Swinnerton–Dyer | 91 | 91 | 182 | 182 |
| Riemann Hypothesis | 19 | 19 | 38 | 38 |
| Hodge Conjecture | 25 | 25 | 50 | 50 |
| Navier–Stokes | 22 | 22 | 44 | 44 |
| Poincaré Conjecture | 12 | 12 | 24 | 24 |
| P versus NP | 23 | 23 | 46 | 46 |
| Yang–Mills | 14 | 14 | 28 | 28 |
| **Total** | **206** | **206** | **412** | **412** |

## Reproduction

- Generator: python3 ci/generate_documentary_github_math.py
- Source/reader parity check: python3 ci/generate_documentary_github_math.py --check
- Unit regressions: python3 -m unittest tests.test_documentary_github_math -v
- Mathematical Markdown preflight: python3 ci/math_markdown_gate.py --file PATH
- Full site: mkdocs build --strict --site-dir /tmp/gcl-documentary-review
- Rendered validation: python3 ci/validate_rendered_docs.py --site-dir /tmp/gcl-documentary-review
- GitHub parser: POST the generated source to the GitHub Markdown API in GFM mode, then verify genuine math-renderer output.
- Real browser: inspect all canonical and reader pages in Chromium; compare genuinely visible mathematics, headings, image and source links, and JavaScript page errors.

The generator checks every mathematical TeX body in its original order. The only permitted presentation changes are converting legacy delimiters to GitHub dollar delimiters, representing the same named operators in Roman math-op style, and adding invisible word boundaries around mathematical compounds. Mathematical source bodies and claim status are not rewritten. Figure captions, alt descriptions, source links and explanatory text are extracted from the canonical articles.

Initial protected source baseline: 32636637d87f6df70bbaaf256da1dad956cabfee (2026-10-18).
Original [cross-render verifier #1263](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1263), [implementation issue #2757](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2757).

The generator uses Python standard-library HTMLParser and adds no third-party parser dependency. This matrix records local browser acceptance, not a public deployment or independent mathematical certification.
