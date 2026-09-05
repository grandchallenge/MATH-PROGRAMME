# Type Theory Monograph Series — Durable Composition Handoff

Canonical GitHub location for the composition contract governing Volumes II–X of **TYPE THEORY — The Grand Unified Theory of Computation**.

Entry point: `SERIES_HANDOFF.md`.

This package is designed so a future composing agent can reconstruct the series contract without relying on chat history.

Key files:
- `SERIES_HANDOFF.md` — operating instructions and read order.
- `HANDOFF_PROMPT.md` — compact paste-ready takeover pointer.
- `SERIES_MANIFEST.json` — canonical volume identities/questions.
- `VOLUME_BLUEPRINTS.md` — intellectual spines for Volumes II–X.
- `SERIES_STYLE_CONTRACT.md` — typography/pedagogy/visual conventions.
- `QUALITY_GATES.md` — development and publication gates.
- `NOTATION_REGISTRY.json` — cross-volume notation contract.
- `REFERENCE_BASELINE.json` — checksummed Volume I reference baseline.
- `bootstrap_volume.py` — instantiate a volume workspace.
- `validate_volume.py` — static consistency checks.
- `templates/` — shared LaTeX style/macros and plate template.
- `ARTIFACT_RECORD.md` — durable continuity and claim-boundary record.

Example:

```bash
python bootstrap_volume.py II ./volume_II_comprehension
python validate_volume.py ./volume_II_comprehension
```

Before a release candidate:

```bash
python validate_volume.py ./volume_II_comprehension --rc --compile
```

The reconciled Volume I RC1.1 reference is a 146-page publication-pass manuscript with the cosmetic plate cleanup applied. It supersedes the earlier 139-page cosmetic-only RC1.1 build as a series baseline.

The binary Volume I release artifacts are not required for this control package to function: `REFERENCE_BASELINE.json` pins their identities and the shared templates preserve the series construction contract. When exact Volume I artifacts are available, verify them against those checksums before treating them as the reference bytes.