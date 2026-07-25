# Agent Council Terminology Registry

## Status

Active programme register.

**Owner:** The Amanuensis.

This registry preserves the canonical meaning of governance terms used across Agent Council documents, schemas, Work Packages, review records, and integrated artifacts. It prevents silent synonym drift and records distinctions that materially affect responsibility boundaries.

## Canonical terms

| Term | Canonical meaning | Boundary and exclusions |
|---|---|---|
| Amanuensis | The council office responsible for internal artifact continuity, decision records, terminology, review provenance, cross-document consistency, and final editorial integration. | Does not certify mathematical truth and does not own external literature provenance. |
| Archivist | The council office responsible for literature provenance, attribution, priority, and the external historical record. | Does not own the programme's internal revision continuity or integrated artifact state. |
| Artifact ledger | The canonical register that identifies each governed artifact and its authoritative integrated version. | Not a claim ledger and not a certificate registry. |
| Decision record | A stable record of a governance or integration choice, its context, alternatives, consequences, and affected artifacts. Each ADR has one canonical file under `docs/decisions/`. | Not a proof, not a substitute for source provenance, and not duplicated authoritatively in the decision index. |
| Decision-record index | `docs/AGENT_COUNCIL_DECISION_RECORDS.md`, the canonical navigation and contract index for dedicated ADR files. | Does not contain authoritative duplicate ADR bodies. |
| Terminology registry | The canonical record of defined governance terms and material term changes. | Not a general mathematical glossary unless a term affects governance or cross-artifact interpretation. |
| Review provenance | Evidence identifying who or what reviewed an obligation, when the review occurred, and where its findings are recorded. | A review reference does not imply that the reviewed claim is proved or certified. |
| Schema-bound Agent Council review record | A review record that conforms to `schemas/agent_review.schema.json` and is explicitly registered in `SCHEMA_BOUND_AGENT_REVIEWS` for CI validation. | A committed legacy review is not schema-bound until migrated and registered. |
| Artifact lifecycle status | The stable machine-readable phase in `artifact.status`: `draft`, `active`, `blocked`, `ready_for_next_stage`, `ready_for_certification`, `certified`, `completed`, `selected`, `published`, or `archived`. | Does not encode campaign-specific Referee qualifications or theorem-strength descriptions. |
| Artifact disposition | An optional human-readable, campaign-specific qualification recorded separately from lifecycle status. | Must not be used to silently create a new machine lifecycle token. |
| Cross-document consistency | A recorded comparison of an artifact against relevant theorem spines, claim ledgers, Work Packages, schemas, documentation, implementation artifacts, and navigation entries. | Consistency does not establish correctness; it establishes that known representations do not silently conflict. |
| Final editorial integration | The controlled incorporation of specialist reviews, resolved obligations, terminology, and decision records into one authoritative artifact. | Not merely copy-editing and not equivalent to Composer or Grammarian review. |
| Authoritative integrated artifact | The version designated by the artifact ledger as the current complete representation of the reviewed work. | Drafts, review fragments, and superseded versions are not authoritative. |
| Exposition and Continuity Kernel | The Cartographer, Steward, Composer, Grammarian, and Amanuensis acting together to preserve dependency, purpose, composition, language, and continuity. | Does not replace the full Agent Council or mathematical certification. |
| Amanuensis continuity state | The recorded state `pending`, `reviewed`, or `blocked` for continuity-related checks. | Must not be interpreted as a mathematical claim status. |
| BSD-RANK-Q | The universal equality of Mordell–Weil rank and complex analytic rank for every elliptic curve over `Q`. | Excludes `Sha` finiteness, leading-term values, parity-only statements, family results, and finite computation unless separately stated. |
| BSD-SHA-Q | The universal assertion that `Sha(E/Q)` is finite for every elliptic curve over `Q`. | Not implied merely by rank equality or control of one `p`-primary component. |
| BSD-LEAD-Q | The universal strong complex leading-term formula in the campaign normalization. | Requires explicit period, regulator, Tamagawa, torsion, `Sha`, Euler-factor, and quantifier conventions; a one-prime or `p`-adic formula is not identical. |
| Solved-problem reconstruction campaign | A governed campaign whose target theorem is already established and whose purpose is source normalization, dependency reconstruction, adversarial audit, pedagogy, or selective certification. | Must not be presented as an open-problem attack, novelty claim, or independent proof unless the corresponding obligations are discharged. |
| Finite-extinction route | The Poincaré-specific route from Ricci flow with surgery and finite extinction, through explicit surgery-topology bookkeeping, to terminal connected-sum and fundamental-group discharge. | Finite extinction alone is insufficient; the term includes the provenance-bearing surgery and topology interfaces. |
| Adversarial guard | A named false-proof fixture attached to a theorem interface to prevent a known hypothesis deletion, scope expansion, circular inference, source drift, or certification overclaim. | Passing all attached guards is not a proof of the guarded theorem. |
| Theorem-interface reconstruction level | A reconstruction state in which exact theorem roles, operational hypotheses, conclusions, sources, corrections, parameters, dependencies, consumers, and claim boundaries are recorded. | Does not assert independent proof, quotation-level source completeness, or formal verification of the imported theorem. |
| Source correction ledger | A versioned record of statements corrected, withdrawn, deferred, or reformulated across primary and reconstruction sources, together with the governing replacement and downstream disposition. | Not a general errata list; only corrections affecting campaign theorem interfaces and claims belong here. |
| Topology event contract | A provenance-bearing interface specifying the permitted topological consequence of one surgery transition: active-component changes, separating or nonseparating sphere cuts, caps, discards, ancestry, and backward connected-sum equations. | Does not certify that the geometric hypotheses for the event occur or that the analytic surgery construction is valid. |
| Surgery-history certificate | A finite source-bound record whose event order, active sets, ancestry, reconstruction equations, factor normalization, local-finiteness/extinction evidence, and terminal discharge have been validated. | Certifies consequences of the imported event contract, not existence of the Ricci flow or correctness of its analytic estimates. |
| Imported event relation | The explicit formal interface asserting that a source-certified event satisfies its recorded finite factor-expression equation. | It is an assumption supplied to the evaluator, not a theorem that a Ricci-flow surgery event exists or is analytically valid. |
| Bounded evaluator certificate | A kernel-checked certificate for a finite evaluator and its structural correctness under explicit imported relations, with its finite input corpus replayed under repository policy. | Does not certify the imported mathematical relations, manifold-level semantics, analytic existence, or the full target theorem. |
| Campaign-critical source concordance | Agreement in theorem role, hypothesis direction, consumer relation, correction discipline, and route relevance across the primary and governing reconstruction sources needed by the selected proof route. | Does not imply sentence-by-sentence identity, exact parameter equivalence, quotation completeness, or independent verification. |
| Qualified solved-problem archive | A versioned archival dossier for an established theorem whose sources, dependencies, adversarial guards, certificates, retained debt, and public claim boundary are explicit. | Not a new proof, open-problem result, full formal certificate, novelty claim, or assertion that every source-level proof step has been independently checked. |

## Change rule

A term is added or changed only when:

1. the change has an associated decision record;
2. affected artifacts are identified;
3. cross-document consistency is checked;
4. the authoritative integrated artifacts are updated;
5. the artifact ledger records the new integrated state.

The decision-record storage, schema-bound review, lifecycle-status, and disposition terms were normalized by `ADR-0007`.
