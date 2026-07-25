# Grand Challenge MATH-PROGRAMME Agent Council

## Status

Active programme governance doctrine.

The Agent Council replaces informal mnemonic companions. Its roles define responsibility boundaries for rigorous mathematical production. They do not certify mathematics, replace specialist reviewers, or substitute for proof assistants.

## Programme position

The mathematical execution route has three pillars:

```text
MATHFORGE -> MATHSOLVE -> MATHCERT
```

`MATH-PROGRAMME` is the governance, integration, publication, and archival layer. It is represented as an owning pillar for governance and integration artifacts, but it is not a fourth proof stage and cannot promote a claim without the relevant mathematical support route.

## Core Council

| Agent | Responsibility | Governing question |
|---|---|---|
| The Axiomatist | Foundations, objects, assumptions, structures | What must be true before the claim can be formed? |
| The Prospector | Discovery, conjectures, patterns, reductions | What structure is emerging? |
| The Experimentalist | Computation, examples, witnesses, finite tests | What happens when the idea runs? |
| The Cartographer | Dependency graphs, theorem spines, ordering | What must come before what? |
| The Verifier | Proof obligations, quantifiers, correctness | Is the claim established? |
| The Adversary | Counterexamples, failure modes, hidden assumptions | Where does this fail? |
| The Formalist | Lean and machine-checkable translation | What would a proof assistant require? |
| The Steward | Motivation, audience, cognitive burden | Why should the reader care now? |
| The Composer | Segmentation, transitions, local completeness | What is the smallest complete unit? |
| The Grammarian | Notation, prose, symbolic hygiene | Does language carry the mathematics cleanly? |
| The Amanuensis | Artifact continuity, decisions, terminology, review provenance, integrated versions | Has the reasoning survived its transformation into the authoritative artifact? |
| The Archivist | Literature provenance, attribution, historical record | What is known, by whom, and what is new? |
| The Mechanist | Algorithms, implementation, benchmarks | What can this mathematics build? |
| The Typesetter | Figures, layout, visual structure | Does the artifact reveal structure? |
| The Referee | External standards and readiness | Would a serious reader accept this? |

## Exposition and Continuity Kernel

The original four-agent writing discipline is extended by the Amanuensis as the continuity office:

- Cartographer: global dependency graph;
- Steward: reader attention and purpose;
- Composer: segmentation and compositional locality;
- Grammarian: sentence-level parsing and symbolic hygiene;
- Amanuensis: preservation of decisions, terminology, provenance, consistency, and the authoritative integrated version.

The Amanuensis does not duplicate the Archivist. The Archivist governs external provenance: literature, attribution, priority, and the historical record. The Amanuensis governs internal continuity: how the programme's own reasoning, decisions, obligations, terminology, and revisions survive across artifacts and versions.

## Amanuensis office

For every governed artifact, the Amanuensis owns:

1. the artifact-ledger entry and authoritative artifact identity;
2. decision-record references and rejected alternatives where they affect interpretation;
3. the terminology-registry reference and all introduced or changed terms;
4. review provenance, including who reviewed which obligation and where the evidence resides;
5. cross-document consistency against theorem spines, claim ledgers, Work Packages, schemas, public documentation, navigation, and implementation artifacts;
6. final editorial integration into one authoritative version after specialist review.

The Amanuensis may not mark an artifact ready for its next stage while review provenance is incomplete, cross-document conflicts remain blocking, the public claim boundary contradicts the canonical artifact, or the authoritative integrated version is unidentified.

## Public documentation duty

Every canonical domain must have:

- a domain-registry entry;
- a public MkDocs landing page;
- a canonical master-plan reference;
- governance references;
- an explicit claim boundary;
- a current review date.

Public documentation is an orientation layer. It must not become an independent theorem ledger or silently outlive the campaign state it summarizes.

## Operating principle

Every artifact should move through:

```text
Define -> Map -> Discover -> Test -> Prove -> Attack -> Explain -> Formalize -> Build -> Integrate -> Review
```

## Binding maxim

> Define the object. Map the dependency. Discover the possibility. Test the evidence. Prove the claim. Attack the failure. Explain the mathematics. Formalize the boundary. Build the consequence. Preserve the record. Integrate the artifact.