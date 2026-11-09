# CMDG CM4 — targeted independent-specialist review execution

**Operation:** CMDG-CM4-EXTERNAL-REVIEW-OUTREACH-001. **Status:** REVIEWER SHORTLIST AND HANDOFF READY; NO OUTREACH SENT, NO REVIEW ACCEPTED. The external mathematical disposition remains open exclusively at [MATH-PROGRAMME #1222](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1222).

## Scope and independence

Request an **independent mathematical appraisal**, not an administrative approval or a check that Lean reports success. CM4 is internally protected-closed; the review addresses mathematical soundness, semantic match to integer-coefficient free solid condensed groups, proof noncircularity and suitability for a human-supervised upstream port. It does **not** reopen ordinary GCL internal work or make CM5 dependent on a reviewer.

The existing canonical materials already suffice for a first approach:

- [External mathematical review packet](../../docs/CMDG-CM4-EXTERNAL-MATHEMATICAL-REVIEW.md).
- [Standalone mathematical note](../../docs/CMDG_CM4_MATHEMATICAL_NOTE.md).
- [Reproducibility protocol](../../docs/CMDG_CM4_REPRODUCIBILITY.md).
- [Exact terminal Lean wrapper](../../fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4Blocker.lean).
- [External review issue #1222](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1222).

Frozen replay checkout: `7a0f33588aa8d1add4d941c9b4681b6910644bf1`; terminal source blob `8ab0051746507099f7321460fe091e56a84b57bb`, proof module blob `d3ef22a2ad2d9c0af6982773d0a24b715e61f5a7`; Lean `v4.33.0-rc1`, mathlib `79d0395a1825a6264ad5d269e35e60537518955e`. Reproducing the theorem is not a review disposition.

## Publicly identified potential reviewers

This is a **candidate contact list**, not endorsement or agreement. Confirm current availability, conflicts and appropriate contact method before an approach.

| Candidate | Domain-specific fit | Public evidence | Caveat |
| --- | --- | --- | --- |
| Dagur Ásgeirsson | Formalized condensed mathematics and solid modules; thesis *Towards a formalized theory of solid modules*, Nöbeling in Lean; source author of mathlib's `Solid.lean` | [Professional page](https://www.dagur.org/) | Strong fit for semantic comparison but disclose authorship of the upstream interface; independent of GCL proof **only if confirmed** |
| Johan Commelin | Condensed mathematics formalization and Liquid Tensor Experiment, Mathlib Initiative | [Professional page](https://math.commelin.net/) | Confirm independence from any GCL proof production and suitable scope |
| Riccardo Brasca | Formal condensed mathematics, Lean/mathlib maintainer, Liquid Tensor Experiment contributor | [Professional page](https://riccardobrasca.github.io/) | Confirm no conflict and whether a mathematical rather than solely implementation review is available |

**Sequence:** contact one qualified candidate with a bounded review brief and a reasonable offer of compensated consulting if appropriate; approach another only on nonresponse or declined scope. Do not solicit blanket endorsement or mass-email multiple researchers. An upstream mathlib maintainer could advise on portability, but that discussion is not itself independent peer review of this proof.

## Minimal proposed review commission

**Requested result:** a dated, attributable, written referee report answering:

1. Does the terminal Lean statement correspond to the intended module-level integer-coefficient solidity result, with all universe and category qualifications?
2. Is the Point-functional argument noncircular at its five critical proof joints (zero reflection, weighted reconstruction, kernel annihilation, scalar-to-morphism faithfulness, terminal solidity)?
3. Does the proof rely on additional substantive assumptions beyond the recorded `[propext, Classical.choice, Quot.sound]` footprint or on a semantically inappropriate definition?
4. Can the reviewer reproduce the pinned theorem, or otherwise identify exactly which part could not be independently checked?
5. What is the smallest repair or caveat needed, if any?

Require the referee to choose **exactly one** disposition from #1222: `MATHEMATICALLY_SOUND__UPSTREAM_PORT_JUSTIFIED`, `SOUND_WITH_REQUIRED_CLARIFICATIONS`, `GAP_FOUND`, `TARGET_MISIDENTIFIED`, or `REVIEW_INCONCLUSIVE`. Record specific mathematical reasoning, file/lemma locators, reproducibility identity, reviewer's stated independence, date and permission to preserve the report.

## Reviewer-facing first contact (candidate wording)

> We have a Lean-checked, source-pinned proof of the module-level integer-coefficient solidity of the free solid condensed module on a profinite set. It uses an underived Point-functional route, rather than the standard derived-Hom argument. Would you be interested in undertaking a bounded independent mathematical review of its semantic match and five critical proof joints, potentially as a paid consultancy? The mathematical note, reproducibility protocol and exact theorem sources are publicly available at the links above. We do not seek endorsement based on compilation alone and would welcome a precise critical finding or an inconclusive report. We can supply a concise review remit and agree on scope before work begins.

**Communication boundary:** this text has **not** been sent. GCL must establish an appropriate sender, consent to any commercial terms, and a direct legitimate communication channel before solicitation. No GCL account or identity should represent a reviewer as retained until acceptance is recorded.

## Upstream-specific guard

Mathlib's current [contribution policy](https://mathlib.org/contribute/index.html) requires human understanding and supervision of AI-assisted work, disclosure of AI use, and expressly disallows LLM-written GitHub/Zulip comments. A GCL agent must **not** submit an AI-authored mathlib comment/PR or treat this document as upstream permission. The human-supervised upstream-port issue remains [#1223](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1223); it is separable from #1222.

## State and next transition

Current state: `REVIEWER_SHORTLIST_READY__NO_CONTACT`. The next external step is actual respectful one-to-one solicitation through an authorized sender; then preserve invitation/response, reviewer independence, the exact frozen material and written returned disposition on #1222. Do not mark the review closed because of internal documentation, PR merge, formal replay, or a candidate's general expertise.
