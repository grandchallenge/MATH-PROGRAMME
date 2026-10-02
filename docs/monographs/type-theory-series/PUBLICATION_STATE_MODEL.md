# Publication State Model — Type Theory Monograph Series

## Purpose

This file separates four states that must never be collapsed across the **TYPE THEORY — The Grand Unified Theory of Computation** monograph series:

1. **composition complete** — the manuscript, solutions, plates, laboratories, audits, and release artifacts satisfy the internal composition/publication gates for an exact candidate revision;
2. **durably admitted** — that exact candidate revision, or an exact checksummed rebuildable representation of it, has been admitted to protected repository state and read back from that state;
3. **independently reviewed** — the exact admitted revision has received the required independent mathematical review, with the reviewer record stating what was and was not established;
4. **published authoritative edition** — an explicit authority decision permits the exact reviewed revision to be represented as the published authoritative edition.

These are distinct state transitions. Passing one does not imply the next.

## Controlling principle

A technically polished artifact does not acquire authority from appearance, completeness, or self-consistency alone. Claim scope, evidence, limitations, provenance, review state, and permitted use must remain inspectable.

This series-level state model is consistent with the bounded institutional position represented by `GCL-POS-01` version `0.1.0`, as admitted for bounded pilot use by `docs/council/submissions/GCL-TCS-00_GCL-POS-01_AUTHORITY_DECISION.json`. Current protected MATH-PROGRAMME doctrine controls any conflict. This file does not promote `GCL-POS-01` beyond its recorded authority or create new mathematical authority.

## State machine

```text
DRAFT / DEVELOPMENT
        |
        | internal composition and publication gates
        v
RC_COMPOSITION_COMPLETE
        |
        | exact-revision durable admission + protected readback
        v
RC_DURABLY_ADMITTED
        |
        | independent mathematical review of that exact revision
        v
RC_REVIEW_QUALIFIED
        |
        | explicit publication/authority disposition
        v
PUBLISHED_AUTHORITATIVE_EDITION
```

A superseding revision returns to the appropriate earlier state. Review does not automatically transfer to materially changed bytes.

## Required meanings

### RC_COMPOSITION_COMPLETE

May be used when the candidate satisfies the internal Stage F / camera-ready gates, including theorem/proof audit, exercise/solution completeness, bibliography/history audit, notation/index audit, copyedit, PDF preflight, rendered-page inspection, and release checksums.

It means **internally complete candidate**. It does not mean protected admission, independent review, mathematical certification, or publication authority.

### RC_DURABLY_ADMITTED

May be used only after the exact candidate identity is present on protected repository state and protected readback confirms that identity. The durable record must preserve the source/rebuild identity, release manifest/checksum identity, claim boundaries, and unresolved review obligations.

Durable admission is an institutional persistence state. It does not establish the truth of mathematical claims.

### RC_REVIEW_QUALIFIED

May be used only when the applicable independent mathematical reader/referee has reviewed the exact admitted candidate and the review record identifies its scope, findings, limitations, and revision identity.

Machine-assisted self-audit, regression testing, or a second pass by the same composing process does not satisfy this state by itself.

### PUBLISHED_AUTHORITATIVE_EDITION

Reserved for an explicit authority decision over the exact review-qualified revision. The decision must state the permitted representation/use. Publication layout, a release PDF, a Git tag, or public availability alone does not create this state.

## Machine-readable status axes

Each active volume `WORKSET_STATE.json` SHOULD carry these independent fields once it reaches late development:

```json
{
  "composition_status": "...",
  "durable_admission_status": "...",
  "independent_review_status": "...",
  "publication_authority_status": "..."
}
```

Recommended values are descriptive strings rather than a single overloaded `status` field. A volume may be composition-complete while durable admission remains pending.

## Release-language rules

Allowed before durable admission:

- “internally complete RC1”;
- “composition-complete release candidate”;
- “external mathematical review pending.”

Not allowed before durable admission:

- “canonical RC1 on protected main”;
- “institutionally admitted RC1.”

Not allowed before independent review:

- “externally refereed”;
- “independently verified” when referring to the manuscript as a whole.

Not allowed before explicit authority disposition:

- “published authoritative edition”;
- any wording that converts an RC or review artifact into institutional authority by implication.

## Exact-revision rule

Review and authority attach to an exact revision identity. Cosmetic or editorial changes may be judged non-material only under the controlling review/authority instrument. Substantive mathematical, semantic, evidentiary, or claim-scope changes require rebinding review and authority to the new revision.

## Volume-transition rule

A later volume may cite or inherit a prior volume's **formal content** at the status actually achieved by that prior volume. It must not silently upgrade the prior volume's institutional state. For example, a later volume may build pedagogically on an internally complete RC while still stating that independent review remains open.

## Volume II reconciliation

For Volume II — **COMPREHENSION**, the exact comprehensive RC1 is presently classified as:

- composition: `RC_COMPOSITION_COMPLETE`;
- durable admission: `RC_DURABLY_ADMITTED`;
- independent mathematical review: `PENDING_EXTERNAL_MATHEMATICAL_REVIEW`;
- publication authority: `NOT_GRANTED`.

The exact admitted review target is bound to source archive SHA-256 `1e1f4ae917e50514dc0a74fa706d30ad0d1c3dbf9ac2f45d7c8ad2445f3fd95a`, protected admission commit `3615be3114ea3aceec14e02231e3a1647faa44b4`, and protected release tree `8fae441820506bb6902e36c048cc475dc56242d5`.

Gate 8 is tracked by issue `#853`. Its durable review packet is under `monographs/type-theory/volume-ii-comprehension/reviews/RC1/`. The next legitimate transition is genuinely independent mathematical review of that exact admitted revision. No self-audit, regression suite, CI run, or second pass by the composing process may substitute for the required independent reviewer record. Passing Gate 8 would permit `RC_REVIEW_QUALIFIED` only; publication authority remains a separate Gate 9 disposition.
