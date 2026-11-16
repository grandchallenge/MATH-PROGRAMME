# Documentation renderer succession — MkDocs Material to Zensical

Status: **MIGRATION CANDIDATE; PRODUCTION SWITCH NOT AUTHORIZED** (2026-11-15)

## Upstream facts

- Material for MkDocs enters final critical maintenance through **2027-05-05**, then reaches end of life.
- Existing production dependencies are pinned in `requirements/docs.txt`: `mkdocs==1.6.1`, `mkdocs-material==9.7.7`, `pymdown-extensions==11.0.1`, `PyYAML==6.0.3`.
- Zensical reads `mkdocs.yml` and supports parallel `zensical build`; however its migration guide explicitly lists `hooks` as unsupported. Its plugin documentation also states that unknown plugins can be silently ignored.
- The existing GCL `mkdocs.yml` uses two required hooks: `ci/erdos_compendium_hook.py` and `ci/oai26_compendium_hook.py`. These produce governed public compendium content. A successful Zensical exit status *without those generated pages* is **not** publication parity.

References:
- https://squidfunk.github.io/mkdocs-material/changelog/
- https://zensical.org/docs/compatibility/mkdocs/migration/
- https://zensical.org/docs/compatibility/mkdocs/plugins/

## Migration work package (bounded)

1. Freeze baseline: exact protected head, dependency lock, MkDocs build artifact digest, count and URLs of generated pages, all relevant index, search and math assets.
2. Separate generator-independent, policy-validated publication data from the two MkDocs hook adapters. The new generator must consume exactly the same validated input and output pages, or an independently checked equivalent. Retain source hashes and claim-status authority.
3. Build a pinned Zensical candidate into a **different** output directory in an isolated environment; do not modify production `site_dir` or Pages workflow.
4. Compare routes and substantive output: Erdős and OAI26 generated chapter inventories, CM4/CM5 pages, math display, navigation, search, custom CSS/JS, accessibility, canonical URLs and sitemap. Require zero lost canonical routes and no silent drop of governed content.
5. Perform independent review and exact-head replay of the production deployment custody chain. Only then propose a separate production-switch PR; retain MkDocs baseline for rollback until readback passes.

## Explicit release gates

| Gate | Required evidence |
| --- | --- |
| G0 | Current exact-head MkDocs baseline and accepted content manifest |
| G1 | Equivalent generation of both custom compendia without MkDocs hook dependency |
| G2 | Zensical build and complete page/route parity report |
| G3 | Browser checks: equations, search, CSS, JS, links and accessibility |
| G4 | Protected review and preserved artifact-digest provenance |
| G5 | Live-path readback and tested rollback |

**Current verified blocker:** G1, because Zensical explicitly does not support `hooks`. No claim of compatibility or migration completion is permitted from a build command alone.

## Domain interaction

Treat `grandchallenge.ai` cutover and renderer migration as independent change sets. Verify `/MATH-PROGRAMME/` on the new domain before changing `site_url`. Do not conflate an address migration with a renderer switch.
