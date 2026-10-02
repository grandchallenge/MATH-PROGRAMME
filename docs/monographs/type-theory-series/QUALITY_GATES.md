# QUALITY GATES

These gates assess different kinds of closure. Passing a later internal composition gate does not retroactively create durable admission, independent review, or publication authority. `PUBLICATION_STATE_MODEL.md` controls the status vocabulary.

## Gate 0 — Preflight

Pass when `VOLUME_PLAN.md` names the calculus, semantics, intended metatheorems, chapter/lab plan, initial plate burdens, exercise ecology, bibliography plan, next-volume threshold, and thesis pressure points.

## Gate 1 — Minimal executable tranche

Pass when Chapters 1–2 compile; the first lab runs; the first plate tranche is visually inspected; exercises have solutions/rubrics; notation is registered.

## Gate 2 — Formal closure

Pass when:
- every named theorem has explicit scope;
- theorem dependencies are recorded in `THEOREM_AUDIT.md`;
- no proof uses a stronger induction hypothesis than the theorem states;
- operational and equational claims are separated;
- imported results are cited;
- regression tests cover representative executable claims.

## Gate 3 — Pedagogical closure

Pass when:
- all teaching chapters have worked examples and failure modes;
- all exercises are keyed in the solutions companion;
- difficulty outliers are calibrated;
- labs match the APIs and calculi described in prose.

## Gate 4 — Visual closure

Pass when:
- every registered plate is embedded;
- every plate has a pedagogical burden and scope/analogy-limit caption;
- grayscale remains intelligible;
- color is nonessential;
- no arrows/connectors obscure text at folio or manuscript scale;
- computed visuals retain executable provenance where applicable.

## Gate 5 — Scholarship closure

Pass when:
- historical attributions have sources;
- foundational priority/date claims have primary-source support where feasible;
- bibliography includes both original sources and modern expository references;
- no literature-dependent novelty claim is made without an explicit search/audit.

## Gate 6 — Notation/index closure

Pass when:
- new symbols are registered;
- overloaded symbols have an explicit policy;
- no cross-volume symbol changes meaning silently;
- index coverage includes the main concepts, formal rules, metatheorems, and computational techniques.

## Gate 7 — Camera-ready composition RC

Pass when:
- clean LuaLaTeX rebuild succeeds from a fresh auxiliary state;
- index rebuild succeeds;
- no unresolved references;
- no overfull boxes requiring manual judgment remain;
- no missing glyph warnings;
- PDFs open and are unencrypted/non-scanned;
- all page contact sheets are visually inspected;
- affected pages receive full-resolution spot checks;
- release manifest/checksums are written.

Passing Gate 7 permits the status `RC_COMPOSITION_COMPLETE`. It does **not** mean that the comprehensive RC is canonical on protected GitHub.

## Gate 7A — Durable RC admission

Pass when:
- the exact RC source/rebuild identity and release checksum identity are durably present in protected repository state;
- the required claim boundaries, audit state, and unresolved review obligations are present in the same durable continuity record or are referenced exactly;
- applicable repository checks pass;
- protected merge/admission succeeds under current doctrine;
- protected readback confirms the exact admitted identity.

Passing Gate 7A permits `RC_DURABLY_ADMITTED`. It is a persistence/institutional-state gate, not a mathematical truth or certification gate.

## Gate 8 — External mathematical review

Required before claiming `RC_REVIEW_QUALIFIED` or “externally refereed.” The review must bind to the exact admitted revision and state what was checked, what was established, and what remains outside scope. A self-audit, regression suite, or second pass by the same composing process is not an independent referee.

Before soliciting the reviewer, satisfy the reviewer-delivery readiness requirements in `REVIEWER_DELIVERY_STANDARD.md`: provide one protected PDF-first landing page, direct manuscript/solutions/folio PDFs, the exact admitted source archive, the review packet/matrix/template, optional build instructions, a checksum-bound deterministic reviewer bundle, and a one-click Gate-8 issue entry point. Source reconstruction or TeX compilation must not be a prerequisite for beginning mathematical review. Reviewer-delivery readiness is logistics only and creates no publication-state transition.

Passing Gate 8 does not itself create publication authority.

## Gate 9 — Publication authority

Required before claiming `PUBLISHED_AUTHORITATIVE_EDITION`. Pass only when an explicit governing authority disposition applies to the exact review-qualified revision and states the permitted representation/use.

A PDF release, public URL, Git tag, repository presence, or polished presentation does not satisfy Gate 9 by itself.