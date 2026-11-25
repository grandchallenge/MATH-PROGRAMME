# OpenAI Mathematics 2026 — documentary compendium

<p class="page-deck">A source-linked guide to 372 mathematical problem families in OpenAI's 2026 collection. Read the questions, examine the original manuscripts, and distinguish what formal tools have replayed from what the mathematics actually establishes.</p>

[**Browse all 372 families**](https://grandchallenge.github.io/MATH-PROGRAMME/oai26/catalogue/)

## What this collection contains

The pinned [OpenAI mathematics source collection](https://github.com/openai/math/tree/1581d4cbdd69a0faf34b2089614fe2a814316a6a) lists **372 numbered families** and **719 distinct manuscript PDF paths**. Its formalization index lists **200 declarations**, while the publisher separately reports **300 formalized top-line results**. These figures count different objects and are not interchangeable.

Every numbered family has a bibliographic reference page with links to its exact original manuscript paths. Some families also have longer six-section explanatory drafts; those remain visibly marked until editorially accepted. A catalogue entry is **not** an independently verified theorem.

## How to read a family page

An article explains the question in plain language, offers a small checkable example, describes known results and uncertainties, reports GCL's present evidence, identifies the next mathematical obligations, and links primary sources.

Four distinctions matter:

- **Source indexed:** a manuscript is present at a pinned path; no truth or validity is inferred.
- **Lean build and axiom audit:** a named declaration compiled in a particular toolchain, subject to an exact axiom check. This does not establish manuscript equivalence.
- **Proposition or semantic concordance:** the statement, assumptions, definitions and source edition must actually correspond, rather than merely sharing a title.
- **Mathematical assessment and certification:** independent mathematical criticism and any subsequent MATHCERT process are separate gates.

## Recent verification-backed explanations

- [Family 003: Quasi-Riemann hypothesis and exceptional real zeros](https://grandchallenge.github.io/MATH-PROGRAMME/oai26/families/003/) — four original Lean and hardened comparator passes; explanation of both proof strategies, with full Hecke correspondence limitations.
- [Family 008: Deligne–Drinfeld conjecture](https://grandchallenge.github.io/MATH-PROGRAMME/oai26/families/008/) — verified within explicit scope; free odd-weight generators, completion and the characteristic-two dimension argument.
- [Family 011: Prime predecessors and totient fibers](https://grandchallenge.github.io/MATH-PROGRAMME/oai26/families/011/) — checked statement bridges and qualified local external-proof replay, distinct from the unresolved companion claims.

The [live catalogue](https://grandchallenge.github.io/MATH-PROGRAMME/oai26/catalogue/) distinguishes admitted articles, unadmitted drafts and reference-only pages. Editorial admission is not mathematical certification. Additional examples of unadmitted explanations include [Family 342](https://grandchallenge.github.io/MATH-PROGRAMME/oai26/families/342/) and [Family 376](https://grandchallenge.github.io/MATH-PROGRAMME/oai26/families/376/).

The [protected comparator evidence index](https://github.com/grandchallenge/MATHFORGE/blob/a1b62de5ae52debe981a2f2855407a0078016e25/sources/OPENAI-MATH-2026/WP01_COMPARATOR_200_PROTECTED_RECEIPT_INDEX.json) records 200 of 200 indexed comparator acceptances. This does not imply 200 verified manuscripts or 372 verified families. Article updates reuse that evidence where relevant and report its exact scope.

## Evidence and editorial accountability

The authoritative [OAI-26 programme tracker](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2850) links the six verification work packages. The [compendium editorial protocol](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/governance/oai26_documentary/EDITORIAL_PROTOCOL.md) defines source-locked manuscripts, mechanical checks, critical reading, protected admission, and independent mathematical certification as separate steps.

The manuscript source is fixed to `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`. Revisions are not silently substituted for the pinned edition. Historical withdrawals and corrections are reported by exact edition, not treated as an automatically valid proof.
