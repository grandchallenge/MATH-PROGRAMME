# SERIES HANDOFF — Type Theory: The Grand Unified Theory of Computation

## Purpose

This file is the durable entry point for composing Volumes II–X of the Grand Challenge monograph collection **TYPE THEORY — The Grand Unified Theory of Computation**.

Treat the series title as a **research thesis** to be tested, not a doctrine to be repeated. The collection asks whether type theory can serve as a sufficiently general grammar of computational possibility. Each volume must strengthen, delimit, or falsify parts of that thesis.

Volume I, **JUDGMENT — The Grammar of Computation**, is the reference implementation for pedagogy, visual language, metatheoretic discipline, exercises, laboratories, bibliography, audit practice, and release production.

## Canonical read order

Before writing a new volume, read in this order:

1. `SERIES_HANDOFF.md` — this operating contract.
2. `SERIES_MANIFEST.json` — canonical volume identities, questions, and thresholds.
3. `SERIES_STYLE_CONTRACT.md` — typography, pedagogy, visual grammar, notation and prose invariants.
4. `VOLUME_BLUEPRINTS.md` — volume-specific intellectual arcs.
5. `QUALITY_GATES.md` — audit and release requirements.
6. `PUBLICATION_STATE_MODEL.md` — the non-collapsible states composition complete, durably admitted, independently reviewed, and published authoritative edition.
7. `NOTATION_REGISTRY.json` — symbols already claimed or reserved by the series.
8. `REFERENCE_BASELINE.json` — the exact Volume I reference state and checksums.
9. For implementation, run `bootstrap_volume.py` and then `validate_volume.py`.

Do not begin drafting chapters before the preflight contract below is written into the new volume's `VOLUME_PLAN.md`.

## Preflight contract for every new volume

The composing agent must first state, in the volume workspace:

- volume number, title, subtitle and governing question;
- what is inherited from prior volumes and what is reintroduced for self-containment;
- the exact formal calculus or family of calculi in scope;
- operational/equational semantics in scope;
- metatheorems intended to be proved, assumed, cited, or explicitly postponed;
- major conceptual distinctions that must not be collapsed;
- the intended chapter count and chapter-to-lab mapping;
- the initial plate register with one pedagogical burden per plate;
- the exercise ecology and solution-companion plan;
- the bibliography/historical attribution plan;
- the transition theorem/question that forces the next volume;
- known pressure points against the grand-unification thesis.

Then identify the **smallest safe executable tranche**: normally Chapters 1–2 + their formal interludes + laboratories + 4–6 plates + exercises. Build and preflight that tranche before scaling.

## Series invariants

The following are controlled invariants unless a volume explicitly records a justified exception.

### 1. Pedagogy

Formalism arrives after the problem it solves is visible. The default explanatory rhythm is:

`ordinary problem → picture → intuition → notation → rules → worked example → computation/lab → proof obligation → exercises → failure mode`

Each chapter should contain at least one place where the theory is deliberately broken or a tempting false inference is exhibited.

### 2. Formal scope honesty

Every named theorem must identify the calculus to which it applies. Do not write “type theory proves…” when the result is only for a specific fragment. Separate:

- syntax from metasyntax;
- definitional equality from propositional equality;
- operational reduction from equational closure;
- declarative typing from algorithmic checking;
- normalization from progress;
- type safety from liveness/deadlock freedom;
- model validity from syntactic derivability;
- analogy from equivalence.

Long standard proofs may be structured proof sketches only when the induction measure, critical cases, and imported theorem are explicit.

### 3. Computational companions

If a plate or prose claim describes a finite graph, search, trace, reduction, enumeration, optimization, or quantitative phenomenon, prefer deriving it from executable evidence. Retain the producing program and machine-readable evidence under `labs/` or `evidence/`.

Wolfram is encouraged when it materially determines the mathematical visual structure (graph layouts, exact combinatorics, symbolic identities, phase portraits, state spaces, etc.). It is not required for decorative diagrams. If unavailable, use an auditable local computation and say so; never imitate a Wolfram-derived result without provenance.

### 4. Illustration discipline

Plates are explanatory arguments, not ornaments. Every plate must have:

- a unique pedagogical burden;
- a caption that states the limit of its analogy where relevant;
- grayscale legibility;
- no semantic dependence on color alone;
- no introduced notation that the adjacent text has not earned;
- no arrow shaft, arrowhead, connector or brace crossing readable text unless semantically intentional;
- visual preflight at actual manuscript scale, not folio scale only.

Use the shared `gclplate` TikZ style and `gcllabel` text shield. Prefer rerouting connectors before shrinking labels.

### 5. Exercise ecology

Default per teaching chapter: 12 exercises.

- 3 Checkpoint — one-star recall/translation/local calculation.
- 3 Core — two-star construction.
- 2 Synthesis — three-star cross-viewpoint explanation.
- 2 Proof Workshop — three-star formal argument.
- 1 Design Clinic — four-star language/system engineering.
- 1 Challenge — four-to-five-star extension or research reading.

Every exercise must have either a worked solution or an explicit rubric in the complete solutions companion. Open problems must not be disguised as deterministic exercises.

### 6. Historical scholarship

Historical names and priority claims require sources. Prefer primary sources for foundational events and modern standard references for exposition. Distinguish circulation date, lecture-note date, and publication date where historically relevant.

### 7. Cross-volume continuity

Each volume must:

- state what it inherits from earlier volumes;
- avoid silently changing notation or semantics;
- add new symbols to `NOTATION_REGISTRY.json`;
- include a “Do not confuse” boundary for the central new idea;
- end with a threshold that makes the next volume necessary rather than merely advertised;
- include a final series-atlas plate locating the current volume within the ten-volume argument.

### 8. Publication-state honesty

The series uses the state model in `PUBLICATION_STATE_MODEL.md`. The following transitions are independent and must not be collapsed:

`RC_COMPOSITION_COMPLETE → RC_DURABLY_ADMITTED → RC_REVIEW_QUALIFIED → PUBLISHED_AUTHORITATIVE_EDITION`.

A clean PDF, complete manuscript, release checksum, successful self-audit, or executable regression suite may establish internal composition evidence. None by itself establishes durable admission, independent review, or publication authority.

Every late-stage `WORKSET_STATE.json` should carry separate `composition_status`, `durable_admission_status`, `independent_review_status`, and `publication_authority_status` fields. A later volume must inherit a prior volume at the institutional state actually achieved, not silently upgrade it.

## Composition stages

### Stage A — Intellectual contract

Produce `VOLUME_PLAN.md`, `CLAIMS_LEDGER.md`, initial `ILLUSTRATION_REGISTER.md`, and `BIBLIOGRAPHY_PLAN.md`. No large prose expansion yet.

### Stage B — Minimal teaching kernel

Write the first 1–2 chapters, implement the smallest executable calculus/example system, produce the first 4–6 plates, and establish the exercise style. Compile early.

### Stage C — Full manuscript spine

Complete 12–15 teaching chapters. Maintain one formal interlude and one laboratory per teaching chapter unless a documented reason says otherwise. Keep proofs and code aligned with the exact calculus.

### Stage D — Visual closure

Finish the canonical plate set. Default target is 42; acceptable range is 36–48. Never pad to hit a number. Maintain `ILLUSTRATION_REGISTER.md` and `plates_folio.tex`.

### Stage E — Monograph-development pass

Deepen theorem/proof layer; add worked examples; complete exercises; build solutions companion; reconcile laboratories and prose APIs.

### Stage F — Publication pass / internal RC composition

Run the theorem/proof audit, exercise/solution completeness audit, bibliography/history audit, notation/index audit, copyedit, camera-ready typography, PDF preflight and rendered-page inspection. Produce `PUBLICATION_AUDIT_RC1.md` and release checksums. Passing this stage permits `RC_COMPOSITION_COMPLETE`; it does not by itself mean the exact RC has been durably admitted.

### Stage F.5 — Durable RC admission

Admit the exact checksummed RC source/rebuild identity and required continuity records to protected repository state through the applicable controls. Read the exact state back from protected state. Only then may the exact RC be called `RC_DURABLY_ADMITTED` or canonical on protected GitHub.

### Stage G — External review gate

Do not call the work an externally refereed final edition until a genuinely independent mathematical reader has checked the exact admitted formal claims. A self-audit, regression suite, or second pass by the same composing process is not independent review. Successful review permits `RC_REVIEW_QUALIFIED`, subject to the review record's stated scope.

### Stage H — Publication authority

A review-qualified RC becomes a `PUBLISHED_AUTHORITATIVE_EDITION` only through an explicit authority disposition over the exact revision. Public availability, a PDF release, a Git tag, or polished presentation does not create authority.

## Stop conditions

Routine bounded editorial work proceeds autonomously. Stop and explicitly surface the issue when any of the following occurs:

- the volume requires changing the series thesis rather than testing/refining it;
- a theorem needed for the central argument cannot be proved under the stated calculus;
- a claimed equivalence turns out to be only an analogy or requires materially stronger hypotheses;
- the notation registry would need an incompatible redefinition of a series-wide symbol;
- a computational experiment contradicts the prose claim;
- a publication claim depends on external mathematical sign-off that has not occurred;
- an institutional-state claim would represent composition, persistence, review, or publication authority more strongly than the exact durable records permit.

## Required release artifacts per volume

At minimum:

- `main.tex` and rendered `main.pdf`;
- `solutions_companion.tex` and PDF;
- `series_style.tex` and `series_macros.tex`;
- `VOLUME_PLAN.md`;
- `CLAIMS_LEDGER.md`;
- `THEOREM_AUDIT.md`;
- `ILLUSTRATION_REGISTER.md`;
- `plates/` and `plates_folio.tex`;
- `labs/` and/or `evidence/` for executable claims;
- `BIBLIOGRAPHY_AUDIT.md`;
- `EXERCISE_AUDIT.json`;
- `PUBLICATION_AUDIT_RC1.md`;
- `RELEASE_MANIFEST_SHA256.txt`;
- a source archive containing everything needed to rebuild;
- a `WORKSET_STATE.json` whose institutional-state fields do not conflate composition, durable admission, independent review, and publication authority.

## Definition of consistency

Series consistency does **not** mean making every volume visually or mathematically identical. It means preserving the same epistemic contract:

- the reader always knows what is formal, what is intuitive, what is computed, what is cited, and what is conjectural;
- pictures carry explanatory burden and announce their limits;
- proofs are scoped to the calculus actually taught;
- executable companions test the claims they are said to test;
- later abstractions arise because earlier machinery reaches a visible boundary;
- the grand-unification thesis is continuously earned rather than repeated;
- institutional state is explicit: internally complete, durably admitted, independently reviewed, and published authoritative are separate claims.