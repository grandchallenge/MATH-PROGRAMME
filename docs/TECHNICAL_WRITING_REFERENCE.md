# Grand Challenge Technical Writing Reference

## Purpose

This is the programme-wide entry point for technical writing and research exposition at Grand Challenge Labs.

The governing idea is that **technical communication is part of the research instrument**. A consequential claim is not ready for institutional use merely because the prose is polished or the artifact is complete. Its scope, evidence, limitations, provenance, review state, and permitted authority must remain inspectable.

This reference does not replace the underlying instruments. It tells authors and composing agents which instruments to read and how they fit together.

## Reference hierarchy

### 1. Institutional communication contract — GCL-TCS-00

Primary source:

- `docs/council/submissions/GCL-TCS-00/GCL-TCS-00.policy.yaml`
- source parts under `council_submissions/GCL-TCS-00/parts/`

**GCL-TCS-00 — Technical Communication Charter and Conformance Model**, version 0.1.0, defines the programme communication hierarchy, conformance profiles, metadata, claim/evidence controls, review gates, exception handling, and fail-closed promotion model.

Its current authority is bounded: the candidate version is admitted for `bounded_candidate_pilot` use by `docs/council/submissions/GCL-TCS-00_GCL-POS-01_AUTHORITY_DECISION.json`. That decision does not promote it to a general version-1 authoritative standard, and current protected MATH-PROGRAMME doctrine controls any conflict.

### 2. Institutional position — GCL-POS-01

Primary source:

- `council_submissions/GCL-POS-01/GCL-POS-01.md`
- conformance/review records under `docs/council/submissions/GCL-POS-01/`

**GCL-POS-01 — Technical Communication Is Part of the Research Instrument**, version 0.1.0, supplies the programme's conceptual writing position. It establishes the working discipline that presentation may reveal authority but cannot create it; public exposition must inherit the material boundaries of the source claim; negative evidence remains visible; and promotion is an explicit state transition over a fixed revision.

GCL-POS-01 is admitted as the `bounded_institutional_position_accompanying_pilot` by the same protected authority decision. Its claims remain bounded exactly as recorded there.

### 3. Prose clarity baseline — ASD-STE100

ASD-STE100 Issue 9 is the preferred controlled-language baseline where its rules are appropriate to the artifact class. Use its discipline for controlled terms, direct sentences, stable keywords, active voice, and explicit procedures.

Do **not** claim formal ASD-STE100 compliance unless a separately governed conformance record establishes that status. Mathematical notation, theorem statements, code, schemas, and exact quotations are not to be distorted merely to imitate controlled-language syntax.

### 4. Mathematics-specific exposition companions

For mathematical and research-facing writing, also read:

- `docs/GRAND_CHALLENGE_PEDAGOGY_STANDARD.md` — programme-wide teaching and exposition standard;
- `docs/PEDAGOGICAL_STYLE_GUIDE.md` — sentence- and artifact-level mathematical exposition;
- `docs/ACCESSIBLE_RESEARCH_GUIDE_STANDARD.md` — prerequisites, examples, fixtures, challenge ladders, certification paths, and continuation graphs;
- `docs/CHAIDEZ_PEDAGOGICAL_PROTOCOL.md` — theorem-spine campaign structure;
- `docs/CLAIM_BOUNDARY_DOCTRINE.md` — claim-scope discipline;
- `docs/FOUNDATION_AWARE_MATH_PROGRAMME.md` — foundation and semantic-profile discipline.

These companions specialize the communication contract; they do not weaken its claim, provenance, review, or authority requirements.

## Writing invariants

Unless a controlling profile explicitly says otherwise, consequential technical writing should preserve these invariants:

1. **Object identity.** Use one canonical technical object across prose, equations, code, data, and schemas. Record aliases when interpretation depends on them.
2. **Claim identity.** Distinguish definitions, assumptions, observations, hypotheses, results, interpretations, recommendations, and speculation.
3. **Bounded evidence.** Evidence supports only the scope actually tested, derived, replayed, or proved. Preserve negative evidence.
4. **Visible limitations.** State material assumptions, unresolved uncertainty, falsifiers, proof debt, and excluded scope.
5. **Provenance.** Preserve revision identity, source identity, methods, versions, hashes, and dependency lineage where consequential.
6. **Review specificity.** State what each review checked and what it did not establish. Machine-assisted self-review is not independent review.
7. **Authority separation.** A clean PDF, passing CI, reproducible experiment, citation count, or public release does not create institutional authority.
8. **Public inheritance.** Summaries and public explanations may simplify language and structure but may not strengthen the source claim or remove material uncertainty.
9. **Analogy discipline.** Label analogy as analogy. Do not write equivalence unless an explicit correspondence supports it.
10. **Fail closed.** Missing required evidence, review, provenance, or authority records block the applicable promotion transition.

## Recommended explanatory order

For serious research exposition, default to:

`status -> object -> obstruction -> working example/picture -> exact claim -> formal structure -> evidence/support route -> limitations/debt -> next executable step`

For the Type Theory monograph collection, the series-specific chapter rhythm in `docs/monographs/type-theory-series/SERIES_STYLE_CONTRACT.md` refines this order without overriding it.

## Authority and revision rule

This reference is a navigation and integration document. It does not itself enlarge the authority of GCL-TCS-00, GCL-POS-01, ASD-STE100, or any mathematical claim.

When the underlying communication instruments are superseded, update this reference by protected revision. Do not silently reinterpret an older artifact under a newer writing standard without preserving the historical revision context.
