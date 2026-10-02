# Publication Audit RC1 — Composition Complete

Volume IV — **PROTOCOL: Computation as Communication** has completed the internal camera-ready composition pass for RC1. This audit records internal composition evidence only. It is not Gate 8 independent mathematical review, mathematical certification, or publication authority.

## Gate dispositions

- Gate 0 preflight: PASS.
- Gate 1 minimal executable tranche: PASS_PROTECTED_ADMISSION_AND_READBACK under `WORKSET_STATE.json`.
- Gate 2 formal closure: PASS in `THEOREM_AUDIT.md`; theorem and non-result boundaries remain as recorded there.
- Gate 3 pedagogical closure: PASS; 14 chapters, 168 exercises, 168 keyed solutions/rubrics, and 14 retained laboratory source files.
- Gate 4 visual closure: PASS. The 77-page manuscript, 34-page solutions companion, and 10-page 42-plate folio were rendered and inspected. All page contact sheets were visually inspected; affected and warning-associated pages were checked at full resolution. All 42 canonical plates were inspected in the folio, and grayscale inspection confirmed legibility. No clipping, overlap, broken glyph, or arrow/text collision remained.
- Gate 5 scholarship closure: PASS in `BIBLIOGRAPHY_AUDIT.md`.
- Gate 6 notation/index closure: PASS; the publication build produced 58 index entries.
- Gate 7 camera-ready composition RC: PASS for built source `9e7d817daf388e020ceb2b4d83bb7543d8c57f12` under exact-head workflow run `34170916991`. The canonical RC validator reports 42 plates, zero errors, and zero warnings. All 14 laboratories pass. Clean indexed LuaLaTeX builds of all three publication targets pass. Final diagnostics report no fatal errors, unresolved references or citations, duplicate labels, missing glyphs, or overfull boxes. The retained 25 warning lines are underfull/package notices and were covered by rendered inspection.
- Gate 7A durable RC admission: PENDING protected merge and protected readback.
- Gate 8 independent mathematical review: PENDING_EXTERNAL_MATHEMATICAL_REVIEW after durable RC admission.
- Gate 9 publication authority: NOT_GRANTED.

## Repair evidence

Gate-7 inspection found and corrected two concrete defects before this disposition: canonical plate labels were added to all 42 plate sources; a duplicate physical inclusion of Plate 22 was removed from Chapter 4. A subsequent visual check corrected the Chapter 4 forward wording so it names canonical Plate 22 rather than exposing chapter-local figure numbering. The final correction changed only manuscript page 29 relative to the previously inspected build; the solutions companion and plate folio were raster-identical. Page 29 was re-inspected at full resolution and passed.

## Distribution build identities

- built source commit: `9e7d817daf388e020ceb2b4d83bb7543d8c57f12`;
- Gate-7 run: `34170916991`;
- main PDF SHA-256: `bb1c4ef217f7487a8e4a9f93fb2f1e7e7ecce3fef3f426485e7e8f2d5c1a12b7`;
- solutions PDF SHA-256: `d5a1bfa752c57f90a3461ea24d663523dc35c7bb9a127116d32e4d05ae57cdd4`;
- plates folio SHA-256: `6e5fb07bc67f88230895fca2a4e60354ec452d7e4dec9871dd47c806b3c84fe0`;
- exact source archive SHA-256: `48e2d1f32b1cbf8349ddd3a0f5a807781c6e75b50a411fba8a8f8f038302508e`.

This evidence record is staged in a later administrative commit than the built source above. Its Gate-7 disposition becomes operative only after the containing exact head receives a fresh clean replay confirming that the evidence/release additions did not alter the publication outputs materially.

## Claim boundary

`RC_COMPOSITION_COMPLETE` means that the internal composition/publication gates are closed for this RC1 source. It does not mean that RC1 is durably admitted on protected `main`, independently refereed, mathematically certified as a whole, or publication-authorized. The next permitted transition is Gate 7A exact durable admission and protected readback.
