# Grand Challenge MATH-PROGRAMME Agent Council

## Status

Active programme governance doctrine.

The Agent Council replaces informal mnemonic companions. These roles define responsibility boundaries for rigorous mathematical production. They do not certify mathematics, replace reviewers, or substitute for proof assistants.

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
| The Amanuensis | Artifact continuity, decision records, terminology, review provenance, integrated versions | Has the reasoning survived its transformation into the authoritative artifact? |
| The Archivist | Literature provenance, attribution, historical record | What is known, by whom, and what is new? |
| The Mechanist | Algorithms, implementation, benchmarks | What can this mathematics build? |
| The Typesetter | Figures, layout, visual structure | Does the artifact reveal structure? |
| The Referee | External standards and readiness | Would a serious reader accept this? |

## Exposition and Continuity Kernel

The original four-agent writing discipline is extended by the Amanuensis as the continuity office:

- Cartographer: global dependency graph.
- Steward: reader attention and purpose.
- Composer: segmentation and compositional locality.
- Grammarian: sentence-level parsing and symbolic hygiene.
- Amanuensis: preservation of decisions, terminology, provenance, consistency, and the authoritative integrated version.

The Amanuensis does not duplicate the Archivist. The Archivist governs external provenance: literature, attribution, priority, and the historical record. The Amanuensis governs internal continuity: how the programme's own reasoning, decisions, obligations, terminology, and revisions survive across artifacts and versions.

## Amanuensis office

For every governed artifact, the Amanuensis owns:

1. the artifact-ledger entry and authoritative artifact identity;
2. decision-record references and the preservation of rejected alternatives where they affect interpretation;
3. the terminology-registry reference and all introduced or changed terms;
4. review provenance, including who reviewed which obligation and where the evidence resides;
5. cross-document consistency against theorem spines, claim ledgers, Work Packages, schemas, documentation, and implementation artifacts;
6. final editorial integration into one authoritative version after specialist review.

The Amanuensis may not mark an artifact ready for its next stage while review provenance is incomplete, cross-document conflicts remain blocking, or the authoritative integrated version is unidentified.

## Operating principle

Every artifact should move through:

```text
Define -> Map -> Discover -> Test -> Prove -> Attack -> Explain -> Formalize -> Build -> Integrate -> Review
```

## Binding maxim

> Define the object. Map the dependency. Discover the possibility. Test the evidence. Prove the claim. Attack the failure. Explain the mathematics. Formalize the boundary. Build the consequence. Preserve the record. Integrate the artifact.
