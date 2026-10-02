# Gate 8 Review Packet - Volume III RC1

## Reviewer-facing rule

Review the exact camera-ready RC1 of **Volume III - PROOF / PROGRAM: Logic Becomes Executable**. The supplied camera-ready manuscript PDF is the primary review object. **Compilation of the TeX is not required.**

The exact source archive is supplied as a secondary verification and source-inspection surface. A reviewer may inspect or rebuild it when useful, but source reconstruction and compilation are not preconditions for mathematical review.

## Exact target identity

- source archive filename: `GCL_Type_Theory_Volume_III_PROOF_PROGRAM_RC1_Source.zip`
- source archive SHA-256: `70c9ffedefa795cf40e2536c45db8a7f3fb0223719d4c6cf24f921e7637d7a62`
- source archive size: `106349` bytes
- protected admission commit: `69fe9e649ea59c5bc1c27f816bb65f52c2627d79`
- protected admission release tree: `fd8ad170e47ef68ae4745d12b27a4200cc1e6be8`
- review tracking issue: `#871`

Camera-ready PDF identities:

- `01_PROOF_PROGRAM_RC1.pdf`: `caf12162ff052db869356c8c0d0fa96dce77b8c40de3bf576e61a2fce30574f3`
- `02_SOLUTIONS_COMPANION_RC1.pdf`: `2e1eae3596f7cb386dc2c93064bcc3d1c85f9511f46f49431ed9ede62836677e`
- `03_PLATE_FOLIO_RC1.pdf`: `ae718ef486fbee4a89fe5d498a48228d5499100d9e84d04bf67517fb520a0de0`

A materially changed mathematical or claim-scope revision is a new review target. A convenience-copy or rebuild that does not match the recorded identity must not be represented as this RC1.

## Identity check

Before substantive review, verify at minimum that the manuscript PDF you are reading matches the recorded manuscript SHA-256, or that it came directly from the protected reviewer-assets directory bound by the protected docket.

If you inspect the source archive, verify its SHA-256 before relying on it. If you rebuild the PDFs, record the environment and output hashes. Rebuild output may differ at the byte level because TeX can embed timestamps; visual/content equivalence is a separate reproducibility question.

A failed identity check blocks a Gate 8 disposition for this exact target.

## Independence requirement

The reviewer must be genuinely independent of the composing process. Candidate audits, laboratories, CI, regression evidence, and the theorem matrix are navigation/evidence inputs only. Their conclusions must not be adopted without independent checking.

The reviewer may use proof assistants, symbolic tools, scripts, or literature searches. The final judgment must be attributable to a distinct reviewer and contain an explicit independence/conflict declaration.

## Primary mathematical scope

Review every named target in `THEOREM_REVIEW_MATRIX.json`, including locally proved results, imported results used by the manuscript, architectural propositions, finite computational claims, and explicit non-results whose boundaries must remain intact.

Mandatory surface includes:

- `CH-0` implication term assignment, weakening, capture-avoiding substitution, and principal beta preservation;
- implication detour/beta correspondence;
- product/sum term assignment, canonical forms, and principal preservation;
- canonical forms, progress, and preservation for the stated `CH-0` teaching evaluator;
- imported strong normalization for pure `CH-0`, including calculus/hypothesis matching;
- natural-deduction normalization versus term reduction and their scoped correspondence;
- `CHD-1` Pi/Sigma rule correspondence without transferring dependent normalization or upgrading Volume II's review state;
- bounded `LJ-0` principal cut reduction versus imported general cut admissibility;
- the Kripke countermodel plus imported soundness route used for excluded-middle non-derivability;
- restricted `CHC-1` CPS typing preservation without arbitrary-control normalization/extraction claims;
- relevance/erasure and selected witness-extraction claims in their toy/finite scopes;
- the imported relational-parametricity dependency used only as a `CHF-1` preview and the separate finite relational fixture;
- the toy elaborator/kernel rechecking boundary;
- the Chapter 14 separation between closed normalization and protocol correctness.

For every target, determine whether the statement, hypotheses, dependencies, proof/proof sketch, imported theorem, and cited evidence support exactly the claim made.

## Claim-boundary audit

Check independently that the manuscript preserves these distinctions:

- natural-deduction derivations vs proof terms;
- structural correspondence vs literal/universal identity;
- operational one-step reduction vs definitional/equational equality;
- definitional equality vs propositional equality;
- proof relevance vs proof irrelevance;
- intuitionistic construction vs classical/control interpretations;
- normalization vs progress/canonical forms;
- ND normalization vs beta reduction vs sequent cut elimination;
- locally proved principal cases vs imported general metatheorems;
- finite executable evidence vs mathematical proof;
- propositions-as-types vs the false claim that all types are truth values;
- closed proof/program evaluation vs open interaction/protocol correctness.

## Explicit non-results to police

The exact RC1 does not claim to establish:

- unrestricted dependent normalization;
- normalization or extraction for arbitrary continuation/control calculi;
- global proof irrelevance;
- constructive excluded middle;
- a universal Curry-Howard identity across all logics/languages;
- arbitrary-sequent cut elimination beyond the stated/imported calculus;
- general Coq/Lean/Agda or industrial extraction correctness;
- a full implemented System F parametricity proof;
- protocol fidelity, deadlock-freedom, liveness, fairness, or distributed-system correctness;
- the monograph's complete metatheory merely from laboratory success.

If any argument silently requires one of these, record a defect.

## Imported-result audit

For each imported result, verify that the cited theorem exists, its hypotheses/calculus match the use made here (or a valid translation is supplied), the manuscript does not over-promote the result, and the attribution is sufficient to locate the source. This applies especially to pure `CH-0` strong normalization, Prawitz-style normalization, Gentzen cut admissibility, Kripke soundness, and Reynolds-style relational parametricity.

## Secondary scope

Sample exercises/solutions, cited laboratories, plate notation, and bibliography entries where they bear on mathematical claims. Gate 8 is mathematical review, not a full cosmetic copyedit.

## Defect taxonomy

Classify findings as `MATHEMATICAL`, `SCOPE`, `EVIDENTIARY`, or `EDITORIAL_NONMATERIAL`; assign severity `BLOCKER`, `MAJOR`, `MINOR`, or `NOTE`. Any blocker, unresolved major defect, or required change to mathematical meaning/claim scope requires `REVISE_AND_REREVIEW` and a new exact target.

## Required disposition

Use exactly one: `PASS`, `PASS_WITH_NONMATERIAL_NOTES`, `REVISE_AND_REREVIEW`, or `FAIL`. A passing Gate 8 review may support a separate transition to `RC_REVIEW_QUALIFIED`; it does not grant publication authority.

## Required durable output

Return a completed copy of `REVIEW_RECORD_TEMPLATE.yaml` bound to this exact target. It must record reviewer identity, independence/conflicts, identity verification, materials examined, methods/tools/sources, per-target findings, claim-boundary/non-result checks, defects/limitations, final disposition, date, and attestation.
