# 9. Conformance profiles

## 9.1 General profile rules

Each governed artifact MUST declare one primary profile. It MAY declare secondary profiles.

The primary profile controls the artifact's main structure and audience. The complete obligation set is the union of the primary and secondary profile requirements.

When profile requirements conflict, the stricter requirement applies unless it changes technical meaning. A meaning-preserving exception MAY resolve the conflict.

## 9.2 GCL-TCS-P01 - Operational and procedural communication

Use this profile for procedures, runbooks, installation instructions, maintenance instructions, incident response, and safety instructions.

Mandatory emphasis:

- direct imperative steps;
- one main action per numbered step;
- explicit prerequisites and completion conditions;
- warnings before the action that creates the hazard;
- named agents and responsibilities;
- controlled vocabulary and units;
- tested step order;
- rollback or recovery instructions when applicable.

Language requirements are strict. Mathematical notation and code can appear when necessary, but the surrounding procedure MUST remain explicit.

Mandatory dimensions: L, T, S, C, E, P, V, G. Dimension R is mandatory when the procedure can be repeated or tested.

## 9.3 GCL-TCS-P02 - Research communication

Use this profile for research reports, work packages, literature audits, technical memoranda, preprints, and research programme records.

Mandatory emphasis:

- canonical question and scope;
- source and normalization locks;
- explicit assumptions and exclusions;
- claim ledger;
- evidence and counterevidence;
- comparison with alternatives;
- limitations and falsifiers;
- separation of results from interpretation;
- review provenance.

Mandatory dimensions: all dimensions. Dimension R can be marked not applicable only for a fully non-computational artifact with an explicit reason.

## 9.4 GCL-TCS-P03 - Mathematical and formal communication

Use this profile for definitions, conjectures, lemmas, theorems, proofs, proof audits, formal specifications, and proof-assistant interfaces.

Mandatory emphasis:

- ambient objects and domains;
- quantifier order;
- regularity, normalization, sign, and unit conventions;
- dependency and implication structure;
- exact statement versions;
- imported result provenance;
- proof obligations and unresolved proof debt;
- counterexample and boundary-case review;
- formalized and informal boundaries.

Formal notation MAY exceed ordinary language limits. A logically atomic definition or theorem statement SHOULD remain intact when splitting it would obscure scope.

Mandatory dimensions: T, S, C, E, P, V, G. Dimension L is mandatory for explanatory prose. Dimension R is conditional on computation, mechanized proof, or executable checking.

## 9.5 GCL-TCS-P04 - Experimental and computational communication

Use this profile for experiments, simulations, benchmarks, notebooks, computational proofs, data analyses, and visual results.

Mandatory emphasis:

- primary hypothesis and alternatives;
- target observable;
- intervention and controls;
- data and model versions;
- seeds and environment;
- stopping and exclusion rules;
- primary and secondary metrics;
- uncertainty and sensitivity;
- negative and null results;
- exact execution path;
- plot provenance and interpretation limits.

Mandatory dimensions: all dimensions.

## 9.6 GCL-TCS-P05 - Software, API, and notebook communication

Use this profile for repositories, packages, APIs, schemas, command-line tools, notebooks, and implementation documentation.

Mandatory emphasis:

- input and output contracts;
- types, shapes, units, and valid ranges;
- preconditions and postconditions;
- deterministic and nondeterministic behaviour;
- failure and error semantics;
- compatibility and version support;
- security and trust boundaries;
- executable examples;
- tests linked to documented guarantees;
- self-containment for teaching notebooks unless an external dependency is part of the lesson.

Mandatory dimensions: L, T, S, C, E, R, P, V, G.

## 9.7 GCL-TCS-P06 - Public technical exposition

Use this profile for web editions, public summaries, release pages, explanatory articles, and technical announcements.

Mandatory emphasis:

- audience-appropriate explanations;
- preserved claim status and limitations;
- links to authoritative sources;
- no promotion by paraphrase;
- accessible figures and equations;
- clear distinction between analogy and mechanism;
- disclosure of material uncertainty.

This profile MUST inherit claim status from authoritative source artifacts. It MUST NOT create a stronger technical claim than its sources support.

Mandatory dimensions: L, T, S, C, E, P, V, G. Reproducibility MAY be inherited through linked source artifacts.

## 9.8 GCL-TCS-P07 - Governance and documentary records

Use this profile for standards, charters, decision records, manifests, source registries, claim ledgers, terminology registries, and review records.

Mandatory emphasis:

- machine-readable status;
- explicit authority and ownership;
- fail-closed discovery and registration;
- stable identifiers;
- complete supersession links;
- no orphan governed records;
- atomic admission of related artifacts;
- review provenance.

Mandatory dimensions: all dimensions except R. Reproducibility becomes mandatory when a governance process includes executable validation.

