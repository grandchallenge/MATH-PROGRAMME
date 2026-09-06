# Gate 8 Review Packet — Volume III RC1

## Review object

Review the exact durably admitted RC1 of **Volume III — PROOF / PROGRAM: Logic Becomes Executable**.

Identity:

- source archive filename: `GCL_Type_Theory_Volume_III_PROOF_PROGRAM_RC1_Source.zip`
- source archive SHA-256: `70c9ffedefa795cf40e2536c45db8a7f3fb0223719d4c6cf24f921e7637d7a62`
- decoded archive size: `106349` bytes
- protected admission commit: `69fe9e649ea59c5bc1c27f816bb65f52c2627d79`
- protected admission release tree: `fd8ad170e47ef68ae4745d12b27a4200cc1e6be8`
- release directory: `monographs/type-theory/volume-iii-proof-program/releases/RC1`
- review tracking issue: `#871`

Do not review a later working copy, regenerated archive, or locally edited manuscript as though it were this target. Any material change to mathematical meaning or claim scope defines a new review target.

## Independence requirement

The reviewer must be independent of the composing process. `THEOREM_AUDIT.md`, `CLAIMS_LEDGER.md`, laboratories, CI, rendered inspection, and regression evidence are navigation/evidence inputs only. Their conclusions must not be adopted without independent checking.

The reviewer may use proof assistants, symbolic tools, scripts, or literature searches. The completed review must nevertheless be attributable to a distinct reviewer and contain an explicit independence/conflict declaration.

## Reconstruction and identity check

Before substantive review:

1. Obtain the protected files under `releases/RC1/`.
2. Inspect `SOURCE_TRANSPORT_MANIFEST.json`.
3. Run `RECONSTRUCT_SOURCE.py` in that directory.
4. Verify that reconstruction reports:
   - Base64 length: `141800` characters;
   - decoded archive size: `106349` bytes;
   - SHA-256: `70c9ffedefa795cf40e2536c45db8a7f3fb0223719d4c6cf24f921e7637d7a62`.
5. Review only the verified reconstructed source tree.

A failed identity check blocks Gate 8.

## Primary mathematical scope

The reviewer must examine every named target in `THEOREM_REVIEW_MATRIX.json`, including local proofs, imported results on which the manuscript relies, architectural propositions, finite computational claims, and explicit non-results whose boundary must remain intact.

The mandatory surface includes:

- `CH-0` implication term assignment, weakening, capture-avoiding substitution, and principal beta preservation;
- the selected implication detour/beta correspondence;
- product and sum term assignments, canonical forms, and principal preservation cases;
- canonical forms, progress, and preservation for the full stated `CH-0` teaching evaluator;
- the standard strong-normalization theorem imported for pure `CH-0`, including whether its hypotheses match the manuscript calculus;
- the scoped natural-deduction-normalization correspondence without collapsing derivation reduction into term reduction;
- `CHD-1` Π/Σ rule correspondence, while preserving Volume II's independently unreviewed status and making no dependent-normalization transfer;
- bounded `LJ-0` principal implication cut reduction versus the separately imported general cut-admissibility theorem;
- the two-world Kripke countermodel and the imported soundness step used to obtain non-derivability of excluded middle;
- restricted `CHC-1` CPS typing preservation without claiming arbitrary-control normalization, extraction, contextual equivalence, or general control metatheory;
- toy relevance/erasure and selected existential witness-preservation claims;
- the imported relational-parametricity theorem used only as a `CHF-1` conceptual preview and the separate finite relational fixture;
- the toy elaborator/kernel rechecking boundary;
- the finite Chapter-14 separation result showing that closed normalization does not imply protocol correctness.

For every target, determine whether the statement, hypotheses, dependencies, proof/proof sketch, imported result, and cited evidence support exactly the manuscript's claim.

## Claim-boundary audit

The reviewer must independently check that the manuscript preserves these distinctions:

- natural-deduction derivations vs proof terms;
- structural correspondence vs literal or universal identity;
- operational one-step reduction vs definitional/equational equality;
- definitional equality vs propositional equality;
- proof relevance vs proof irrelevance;
- intuitionistic construction vs classical principles/control interpretations;
- normalization vs progress/canonical forms;
- natural-deduction normalization vs beta reduction vs sequent cut elimination;
- locally proved principal cases vs imported general metatheorems;
- finite executable evidence vs mathematical proof;
- propositions-as-types vs the false assertion that all types are truth values;
- closed proof/program evaluation vs open interaction and protocol correctness.

The review must explicitly determine whether any proof, exercise solution, plate, caption, worked example, or later argument silently uses a result listed as unestablished.

## Explicit non-results to police

The exact RC1 does **not** claim to establish:

- unrestricted dependent normalization;
- normalization or extraction for arbitrary continuation/control calculi;
- global proof irrelevance;
- constructive excluded middle;
- a universal Curry–Howard identity across all logics or programming languages;
- arbitrary-sequent cut elimination beyond the stated/imported calculus;
- general Coq/Lean/Agda or industrial proof-assistant extraction correctness;
- a full implemented-System-F parametricity proof;
- protocol fidelity, deadlock-freedom, liveness, fairness, or distributed-system correctness;
- the monograph's complete metatheory merely from executable laboratory success.

If any argument requires one of these as an unstated premise, record a defect.

## Imported-result audit

Imported theorems are not exempt from review. For each imported dependency, verify at minimum:

- the theorem actually exists in the cited literature;
- its calculus/hypotheses match the use made here or a valid translation/reduction is supplied;
- the manuscript does not promote an imported theorem beyond the imported scope;
- the dependency is sufficiently attributed for a reader to locate and inspect it.

This applies especially to pure `CH-0` strong normalization, the Prawitz-style normalization context, Gentzen cut admissibility, Kripke soundness, and Reynolds-style relational parametricity.

## Secondary scope

Also sample for mathematical consistency with the formal core:

- exercises and keyed solutions, especially proof-workshop and challenge items using named theorems;
- laboratories cited as support for finite examples;
- plate notation where it could alter a formal claim;
- bibliography entries used to import or historically attribute mathematical results.

This secondary review is mathematical, not a full copyedit or typography review.

## Defect taxonomy

Assign each finding one primary class:

- `MATHEMATICAL`: false result, missing hypothesis, invalid proof step, circular dependency, misuse of imported theorem, or incorrect formal example;
- `SCOPE`: wording/theorem scope stronger than supported, or analogy/correspondence presented as unrestricted identity;
- `EVIDENTIARY`: computational or cited evidence does not support the claim attributed to it;
- `EDITORIAL_NONMATERIAL`: notation, prose, or presentation issue that does not change mathematical meaning or claim scope.

Also assign severity: `BLOCKER`, `MAJOR`, `MINOR`, or `NOTE`.

Any `BLOCKER`, any unresolved `MAJOR`, or any required change to mathematical meaning or claim scope requires `REVISE_AND_REREVIEW` and a new exact review target.

## Required disposition

Use one of exactly four dispositions:

- `PASS` — the exact admitted RC1 is mathematically review-qualified within the stated scope;
- `PASS_WITH_NONMATERIAL_NOTES` — only clearly nonmaterial notes remain;
- `REVISE_AND_REREVIEW` — one or more material corrections are required;
- `FAIL` — the candidate is not supportable in its present mathematical architecture.

A `PASS` or justified `PASS_WITH_NONMATERIAL_NOTES` may support a separate transition to `RC_REVIEW_QUALIFIED`. The review itself creates no publication authority.

## Required durable output

Submit a completed copy of `REVIEW_RECORD_TEMPLATE.yaml` under this review directory through protected repository controls. It must include:

- reviewer identity;
- independence/conflict declaration;
- exact target identity and identity-verification result;
- materials actually examined;
- method/depth and external sources/tools used;
- per-target findings;
- claim-boundary and explicit-non-result checks;
- defects, limitations, and excluded scope;
- final disposition, date, and reviewer attestation.

Do not change `WORKSET_STATE.json` to `RC_REVIEW_QUALIFIED` in the same transaction unless the governing workflow explicitly permits that transition and the independent review record is already protected, fixed, and inspectable.
