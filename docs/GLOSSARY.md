# Glossary

## Agent Council

The programme review-governance system that assigns explicit responsibility for foundations, discovery, experiments, dependency structure, verification, adversarial review, formalization, exposition, provenance, implementation, continuity, and Referee readiness.

## Amanuensis

The Agent Council office responsible for internal artifact continuity: authoritative identity, decision records, terminology, review provenance, cross-document consistency, and final editorial integration. The Amanuensis does not certify mathematical truth.

## Artifact disposition

A human-readable campaign qualification such as `selected_unproved` or `referee_promoted_conditional`. Disposition explains an artifact's campaign state without creating a new machine lifecycle token.

## Artifact lifecycle status

The machine-readable phase of a governed artifact: `draft`, `active`, `blocked`, `ready_for_next_stage`, `ready_for_certification`, `certified`, `completed`, `selected`, `published`, or `archived`. Lifecycle status does not directly state whether a conjecture is proved.

## Assay office

The MATHCERT role. It tests whether a claim survives a trusted proof or replay boundary.

## Campaign promotion register

The current documentary register that records when repository review and merge conditions have been discharged for an immutable campaign artifact whose text preserves its pre-merge status snapshot. It does not promote a theorem, novelty claim, or certification state.

## Candidate ore

A promising mathematical object, problem, pattern, or computational signal produced by MATHFORGE before disciplined Work Package treatment.

## Certification handoff

A packet from MATHSOLVE to MATHCERT containing a precise claim, formal statement, assumptions, dependencies, source trail, and expected proof or replay route.

## Claim boundary

The line separating what is proved or certified from what is heuristic, conjectural, literature-derived, or merely computed under finite assumptions.

## Claim ledger

A machine- and human-readable record of claims, support types, statuses, assumptions, artifacts, and promotion conditions.

## Exact screen

A reproducible finite or symbolic computation used to verify a finite statement, search for counterexamples, sanity-check definitions, or produce a certificate candidate.

## Foundry

The MATHFORGE role. It gathers source material, runs reconnaissance, generates examples, and produces candidate artifacts.

## Governed root campaign artifact

An integrated root-level `*-WP00-*.md` source-normalized non-solution dossier with an artifact ID, challenge identity, and explicit claim class. Documentation CI requires it to be registered as a canonical programme domain entry. Registration does not strengthen its mathematical claims.

## Grand Challenge Work Package

A bounded mathematical campaign artifact with lay companion, formal problem statement, source audit, claim ledger, theorem spine, proof/computation/failure analysis, next target, and certification handoff.

## MATH-PROGRAMME

The governance, integration, publication, and archival layer. It may own governed artifacts in the review schema, but it is not a fourth mathematical execution or proof stage.

## MATHCERT

The certification pillar. It owns Lean or equivalent formalization, exact replay, interval certificates, SAT/SMT artifacts, CI gates, and claim-status enforcement.

## MATHFORGE

The discovery pillar. It owns intake, source reconstruction, reconnaissance computation, conjecture mining, and candidate witness generation.

## MATHSOLVE

The campaign pillar. It owns Work Packages, theorem spines, reductions, exact screens, failed-attempt accounting, synthesis, and MATHCERT handoffs.

## Normal form

A reformulation that reduces ambiguity and exposes the essential structure of a problem without changing its content.

## Pedagogical companion

The explanatory layer that teaches the object, obstruction, claim boundary, and next target to a serious reader.

## Programme domain

A governed mathematical campaign with a stable domain ID, campaign ID, canonical repository entry, public landing page, foundational profile, review date, and explicit claim boundary in `DOMAIN_REGISTRY.yaml`.

## Promotion condition

The specific action required for a claim or artifact to move to a stronger status. Mathematical promotion requires the declared support route; documentary promotion may instead require review, integration, CI, or repository merge. The two must not be confused.

## Qualified solved-problem archive

A governed reconstruction dossier for an established theorem whose sources, dependencies, adversarial guards, certificates, retained debt, and public claim boundary are explicit. It is not automatically a new proof or complete formalization.

## Schema-bound review record

An Agent Council review record that conforms to the current schema and is explicitly registered for CI validation. Legacy review files are governed evidence but are not schema-bound until migrated and registered.

## Status spine

A structured account of what is known, unknown, solved, refuted, stale, or specialist-dependent in a problem domain.

## Theorem spine

The chain of definitions, propositions, lemmas, corollaries, examples, and counterexamples that makes a Work Package mathematically auditable.

## Terminology authority

The [Agent Council Terminology Registry](AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md) governs terms that materially affect review, lifecycle, continuity, and cross-artifact interpretation. The [Programme Status Taxonomy](STATUS_TAXONOMY.md) gives the public mapping among claim status, artifact lifecycle, and campaign disposition.
