# Gate 8 Review Packet — Volume II RC1

## Review object

Review the exact durably admitted RC1 of **Volume II — COMPREHENSION: How Computational Worlds Are Built**.

Identity:

- source archive SHA-256: `1e1f4ae917e50514dc0a74fa706d30ad0d1c3dbf9ac2f45d7c8ad2445f3fd95a`
- protected admission commit: `3615be3114ea3aceec14e02231e3a1647faa44b4`
- protected release tree: `8fae441820506bb6902e36c048cc475dc56242d5`
- release directory: `monographs/type-theory/volume-ii-comprehension/releases/RC1`
- review tracking issue: `#853`

Do not review a later working copy, regenerated archive, or locally edited manuscript as though it were this target. Any materially changed mathematical or claim-scope bytes define a new review target.

## Independence requirement

The reviewer must be independent of the composing process. The internal `THEOREM_AUDIT.md`, executable laboratories, regression evidence, and CI are navigation/evidence inputs only; they are not independent review and their conclusions must not be adopted without checking.

The reviewer may use proof assistants, symbolic tools, scripts, or literature searches. The completed review must nevertheless be attributable to a distinct reviewer and contain an explicit independence/conflict declaration.

## Reconstruction and identity check

Before substantive review:

1. Obtain the protected files under `releases/RC1/`.
2. Inspect `SOURCE_TRANSPORT_MANIFEST.json`.
3. Run `RECONSTRUCT_SOURCE.py` in that directory.
4. Verify that reconstruction reports:
   - Base64 length: `189472` characters;
   - decoded archive size: `142104` bytes;
   - SHA-256: `1e1f4ae917e50514dc0a74fa706d30ad0d1c3dbf9ac2f45d7c8ad2445f3fd95a`.
5. Review only the verified reconstructed source tree.

A failed identity check blocks Gate 8.

## Primary mathematical scope

The reviewer must examine every named formal result in the exact admitted RC1, not merely a sample. The mandatory result set is encoded in `THEOREM_REVIEW_MATRIX.json` and includes:

- weakening under dependency;
- generalized dependent substitution through trailing dependent declarations;
- binder-free substitution composition in its stated COMP-0 scope;
- Π formation/introduction/elimination and dependent application;
- principal Π-beta subject reduction;
- Σ formation/introduction/projections;
- principal Σ projection preservation;
- conditional adjacent exchange under mutual non-dependence and suffix re-formation;
- canonical-forms/inversion claims for the selected `Fin` family;
- canonical-forms/inversion claims for the selected `Vec` family;
- exclusion of the nil case for `Vec(A,succ(n))`;
- restricted bidirectional algorithmic soundness;
- termination of the concrete teaching checker only;
- the elaborator/kernel trust-boundary proposition;
- totality of the finite external toy code decoder.

For each item, determine whether the statement, hypotheses, proof/proof sketch, and dependencies support exactly the claimed result.

## Claim-boundary audit

The reviewer must independently check that the manuscript keeps the following distinctions intact:

- syntax vs metasyntax;
- definitional equality vs propositional equality;
- operational reduction vs equational closure;
- declarative typing vs algorithmic checking;
- normalization vs progress/canonicity;
- type-family indexing vs arbitrary semantic truth;
- universe coding preview vs a proved internal universe hierarchy;
- categorical comprehension as semantic organization vs literal syntactic/category identity;
- executable evidence vs mathematical proof.

The review must explicitly determine whether any proof or explanatory argument silently relies on a result that the manuscript lists as unestablished.

## Explicit non-results to police

The exact RC1 does **not** claim to establish:

- strong normalization for the full pedagogical union of fragments;
- global canonicity without a proved/cited normalization route;
- decidability or completeness of arbitrary dependent definitional equality;
- general strict-positivity or termination checking for user-defined inductive families;
- consistency of a full internal universe hierarchy;
- identity types, propositional equality, `J`, or general transport;
- completeness of elaboration or higher-order unification.

If any theorem, exercise solution, plate caption, worked example, or later argument requires one of these as an unstated premise, record a defect.

## Secondary scope

The reviewer should also sample the following for mathematical consistency with the formal core:

- exercises and keyed solutions, especially proof-workshop and challenge items that reuse named theorems;
- laboratories whose outputs are cited as support for finite examples;
- mathematical notation in plates where it could change the meaning of a formal claim;
- bibliography entries used to import or historically attribute mathematical results.

This secondary review need not constitute a full copyedit or typography review. Gate 8 is mathematical, not cosmetic.

## Defect taxonomy

Classify each finding with one primary class:

- `MATHEMATICAL`: false result, missing hypothesis, invalid proof step, circular dependency, misuse of imported theorem, or incorrect formal example;
- `SCOPE`: wording or theorem scope is stronger than the argument supports, or an analogy is presented as equivalence;
- `EVIDENTIARY`: computational or cited evidence does not support the claim attributed to it;
- `EDITORIAL_NONMATERIAL`: notation, prose, or local presentation issue that does not change mathematical meaning or claim scope.

Also assign severity: `BLOCKER`, `MAJOR`, `MINOR`, or `NOTE`.

Any `BLOCKER`, any unresolved `MAJOR`, or any correction that changes mathematical meaning or claim scope requires `REVISE_AND_REREVIEW` and a new exact review target.

## Required disposition

Use one of exactly four dispositions:

- `PASS` — the exact admitted RC1 is mathematically review-qualified within the stated scope;
- `PASS_WITH_NONMATERIAL_NOTES` — only clearly nonmaterial notes remain, with no change to mathematical meaning or claim scope;
- `REVISE_AND_REREVIEW` — one or more material changes are required;
- `FAIL` — the candidate is not supportable in its present mathematical architecture.

A `PASS` or justified `PASS_WITH_NONMATERIAL_NOTES` may support a separate institutional state transition to `RC_REVIEW_QUALIFIED`. The review itself does not create publication authority.

## Required durable output

Submit a completed copy of `REVIEW_RECORD_TEMPLATE.yaml` under this review directory through protected repository controls. The record must include:

- reviewer identity;
- independence/conflict declaration;
- exact target identity;
- materials actually examined;
- method/depth;
- per-result findings;
- claim-boundary and non-result checks;
- defects and limitations;
- disposition;
- date and attestation.

Do not modify `WORKSET_STATE.json` to `RC_REVIEW_QUALIFIED` in the same transaction unless the governing workflow explicitly permits that transition and the admitted review record is already fixed and inspectable.