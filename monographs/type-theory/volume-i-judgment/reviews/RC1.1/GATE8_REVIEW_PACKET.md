# Gate 8 Review Packet — Volume I RC1.1

## Review object

Review the exact durably admitted RC1.1 of **Volume I — JUDGMENT: The Grammar of Computation**.

Identity:

- rebuild-core SHA-256: `013fd6b5f78a8bb45711bb9e167321f7ca58324b7a0ae3f0c7e594ba63a96e3b`
- exact `main.tex` SHA-256: `ceb02e6c84011615c7557c9bf4bba391290f43d6d54d9c5033dab9215af14d01`
- protected source-admission commit: `0b18341a7536d021b6ab007c033a72b32e3ff7e1`
- protected release tree: `3a7dbb5d0990b75ce15c70daa91b232138b3a9a0`
- durable-state record commit: `c2911113beaf58c17e2d88a908021d66dcf9a7bf`
- release directory: `monographs/type-theory/volume-i-judgment/releases/RC1.1`
- review tracking issue: `#859`

Do not review a later working copy, regenerated archive, or locally edited manuscript as though it were this target. A material change to mathematical meaning or claim scope defines a new review target.

## Independence requirement

The reviewer must be independent of the composing process. The internal publication audit, executable regressions, CI, and any prior machine-assisted proof audit are navigation/evidence inputs only; they are not independent review and their conclusions must not be adopted without checking.

The reviewer may use proof assistants, symbolic tools, scripts, or literature searches. The completed review must be attributable to a distinct reviewer and contain an explicit independence/conflict declaration.

## Reconstruction and identity check

Before substantive review:

1. Obtain the protected files under `releases/RC1.1/`.
2. Inspect `SOURCE_TRANSPORT_MANIFEST.json`.
3. Run `RECONSTRUCT_SOURCE.py` in that directory.
4. Verify that reconstruction reports:
   - Base64 length: `179956` characters;
   - decoded archive size: `134967` bytes;
   - SHA-256: `013fd6b5f78a8bb45711bb9e167321f7ca58324b7a0ae3f0c7e594ba63a96e3b`.
5. Verify `main.tex` SHA-256 is `ceb02e6c84011615c7557c9bf4bba391290f43d6d54d9c5033dab9215af14d01`.
6. Review only the verified reconstructed source tree.

A failed identity check blocks Gate 8.

## Primary mathematical scope

The reviewer must examine **all 19 named results** in the exact admitted `main.tex`; sampling is not permitted. `THEOREM_REVIEW_MATRIX.json` contains their exact source locations and statement fingerprints.

The mandatory result set is:

1. Inversion for natural-number constructors.
2. Weakening for the simple core.
3. Free-variable adequacy.
4. Substitution for the simple core.
5. Beta preservation.
6. Uniqueness of synthesized types.
7. Typing stability under fundamental function computation.
8. Canonical forms for products and sums.
9. Nat-rec iteration along numeral structure.
10. Conditional normalization decision procedure for reduction-generated definitional equality.
11. Non-typability of the usual `Omega` in finite STLC.
12. Canonical forms for closed TinyTT values.
13. Preservation for the TinyTT core.
14. Progress for closed TinyTT terms.
15. No stuck closed well-typed states.
16. Implication detour elimination as beta reduction under Curry–Howard.
17. Independent checking localizes trust for the core judgment.
18. Soundness of the TinyTT bidirectional checker.
19. The simple-arrow grammar cannot bind a term in its codomain.

For every result, determine whether the statement, hypotheses, proof/proof sketch, dependencies, and surrounding prose support exactly the claimed conclusion.

## High-risk cross-cutting checks

The reviewer must explicitly address these pressure points:

- generalized substitution carries a trailing context and handles binder cases without silently dropping context;
- weakening uses fresh declarations/distinct formal names, while implementation shadowing is only a convenience;
- nat-rec iteration is stated in reduction-generated definitional equality/congruence closure, not as a false literal call-by-value trace for open terms;
- declarative preservation is distinct from algorithmic re-synthesis after evaluation erases annotations;
- progress proves an immediate step/value dichotomy and does not assume normalization;
- the definitional-equality decision theorem is conditional on strong normalization, confluence, decidable alpha-equivalence, and the stated generated equality;
- the manuscript does not pretend to prove strong normalization for the whole TinyTT core;
- the `Omega` proof depends on finite simple types and must not be generalized to recursive-type systems;
- the kernel/localized-trust proposition is conditional on an independently implemented sound kernel and does not establish surface-intent preservation;
- the Volume-I dependent threshold is a grammar limitation, not a proof of the dependent theory developed in Volume II.

## Claim-boundary audit

Independently check that the manuscript keeps the following distinctions intact:

- syntax vs metasyntax;
- derivability vs semantic truth/model validity;
- operational reduction vs definitional/equational closure;
- definitional equality vs richer propositional equality;
- declarative typing vs algorithmic bidirectional checking;
- preservation/progress/type safety vs normalization;
- type safety vs correctness, security, termination in richer languages, liveness, or resource guarantees;
- proof/program correspondence vs unrestricted identity of logic and computation;
- context-as-interface analogy vs temporal/protocol semantics;
- executable evidence vs mathematical proof;
- analogy vs formal equivalence;
- simple type grammar vs dependent type formation.

The review must state whether any result, exercise solution, or explanatory argument silently relies on a theorem the manuscript explicitly postpones or merely assumes.

## Explicit non-results to police

Volume I RC1.1 does **not** establish, merely by its own theorem layer:

- strong normalization for the entire TinyTT core;
- confluence for every reduction/equality extension a reader might add;
- decidability of arbitrary definitional equality without the stated normalization/confluence hypotheses;
- semantic soundness/completeness in a fully developed model theory;
- dependent products, dependent sums, identity types, universes, session fidelity, effect safety, or other later-volume metatheory;
- general program correctness, security, liveness, deadlock freedom, resource bounds, or user-intent satisfaction;
- production-grade proof-assistant/kernel correctness merely from the TinyTT teaching implementation;
- publication authority or mathematical certification from executable tests.

If any theorem, solution, plate, or prose passage requires one of these as an unstated premise, record a defect.

## Secondary scope

The reviewer should sample for mathematical consistency:

- proof-workshop and challenge solutions that reuse named results;
- plate notation when it could change the meaning of a formal claim;
- historical/bibliographic claims used to import mathematical facts;
- any separately available computational evidence cited for finite traces, searches, or checker behavior.

The exact durably admitted rebuild core does not duplicate all historical audit/evidence files. If those are unavailable to the reviewer, record that limitation explicitly. Do not infer a successful evidentiary audit from its pinned hash alone.

## Defect taxonomy

Classify each finding with one primary class:

- `MATHEMATICAL`: false result, missing hypothesis, invalid proof step, circular dependency, misuse of imported theorem, or incorrect formal example;
- `SCOPE`: wording/result scope stronger than the argument supports, or analogy presented as equivalence;
- `EVIDENTIARY`: computational/cited evidence does not support the claim attributed to it;
- `EDITORIAL_NONMATERIAL`: notation, prose, or local presentation issue that does not change mathematical meaning or claim scope.

Also assign severity: `BLOCKER`, `MAJOR`, `MINOR`, or `NOTE`.

Any `BLOCKER`, unresolved `MAJOR`, or correction changing mathematical meaning or claim scope requires `REVISE_AND_REREVIEW` against a new exact revision.

## Required disposition

Use exactly one:

- `PASS`
- `PASS_WITH_NONMATERIAL_NOTES`
- `REVISE_AND_REREVIEW`
- `FAIL`

A `PASS` or justified `PASS_WITH_NONMATERIAL_NOTES` may support a separate institutional transition to `RC_REVIEW_QUALIFIED`. The review itself does not create publication authority.

## Required durable output

Submit a completed copy of `REVIEW_RECORD_TEMPLATE.yaml` through protected repository controls. It must include:

- reviewer identity;
- independence/conflict declaration;
- exact target identity and successful identity check;
- materials actually examined and materials not examined;
- methods/depth;
- findings for every T01–T19 result;
- cross-cutting and claim-boundary checks;
- defects, limitations, and excluded scope;
- final disposition;
- date and attestation.

Do not change `WORKSET_STATE.json` to `RC_REVIEW_QUALIFIED` until a completed independent review record is itself fixed, admitted, and inspectable under the governing transition.
