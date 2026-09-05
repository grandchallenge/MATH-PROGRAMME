# QUALITY GATES

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

## Gate 7 — Camera-ready RC

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

## Gate 8 — External mathematical review

Required before claiming “externally refereed final edition.” A self-audit, regression suite, or second pass by the same composing process is not an independent referee.