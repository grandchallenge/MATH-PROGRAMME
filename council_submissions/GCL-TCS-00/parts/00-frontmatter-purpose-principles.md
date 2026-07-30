---
title: "GCL-TCS-00: Technical Communication Charter and Conformance Model"
subtitle: "Candidate Standard 0.1.0"
author: "Grand Challenge Labs"
date: "2026-07-27"
lang: en-CA
geometry: margin=24mm
fontsize: 10.5pt
header-includes:
  - |
    \usepackage{longtable,booktabs,array}
  - |
    \usepackage{microtype}
  - |
    \usepackage{enumitem}
  - |
    \setlist{nosep}
---

# Document control

| Field | Value |
|---|---|
| Standard identifier | GCL-TCS-00 |
| Title | Technical Communication Charter and Conformance Model |
| Version | 0.1.0 |
| Status | Candidate standard |
| Date | 2026-07-27 |
| Authority | Grand Challenge Labs |
| Language | Canadian English |
| Supersedes | None |
| Normative scope | All governed GCL technical communication artifacts |
| Baseline language reference | ASD-STE100 Simplified Technical English, Issue 9, January 2025 |

# 1. Purpose

GCL-TCS-00 defines the governance system for technical communication at Grand Challenge Labs. It establishes the standards hierarchy, conformance profiles, mandatory metadata, exception rules, and promotion gates.

This charter does not replace domain standards. It defines how domain standards are selected, combined, checked, and recorded.

The charter has five purposes:

1. Preserve technical correctness and claim boundaries.
2. Make each important statement traceable to evidence and authority.
3. Make research artifacts reproducible when reproduction is applicable.
4. Keep terminology and notation stable across documents, code, data, and public explanations.
5. Prevent incomplete or unreviewed artifacts from acquiring authority through presentation quality alone.

# 2. Scope

This charter applies to technical artifacts that GCL creates, maintains, reviews, promotes, or publishes. These artifacts include:

- research reports and work packages;
- mathematical statements, proofs, and proof audits;
- experimental protocols, notebooks, datasets, and plots;
- software repositories, APIs, schemas, and implementation notes;
- procedures, runbooks, and safety instructions;
- governance records, claim ledgers, source records, and review records;
- public web editions, explanatory articles, and release notes.

This charter applies to human-authored and machine-assisted content. The use of a language model does not change the required evidence, review, or authority.

Private scratch notes are outside the formal promotion system until a project registers them as governed artifacts. A promoted document must not depend on an unregistered scratch note as its only source of authority.

# 3. Normative language

The following words have special meanings in this standard:

- **MUST** identifies a mandatory requirement.
- **MUST NOT** identifies a prohibition.
- **SHOULD** identifies a strong default. A deviation requires a reason.
- **SHOULD NOT** identifies a practice that normally creates unacceptable risk.
- **MAY** identifies a permitted choice.

A statement marked MUST or MUST NOT is normative. Examples and explanatory notes are informative unless the text states otherwise.

# 4. Governing principles

## 4.1 Correctness before style

A writing rule MUST NOT change the technical meaning of a statement. A shorter sentence is not better when it removes a quantifier, condition, exception, uncertainty, or causal distinction.

When clarity and precision appear to conflict, the author MUST first try a structural solution. The author can use a definition, equation, table, list, diagram, or sequence of short statements. If precision still requires a more complex construction, the author MAY use it and record an exception when the applicable profile requires one.

## 4.2 Claim boundaries before persuasion

A document MUST distinguish established results from hypotheses, interpretations, recommendations, and speculation. Presentation quality MUST NOT raise the status of a claim.

A public explanation MUST preserve the claim status, scope, assumptions, and important limitations of its authoritative source.

## 4.3 Evidence before promotion

A consequential claim MUST link to evidence or to an accepted derivation. The evidence MUST be sufficient for the declared claim type and impact class.

A missing evidence record is not a neutral omission. It is a failed promotion condition.

## 4.4 Reproducibility before authority

An empirical or computational result MUST provide enough information to repeat the relevant procedure. When full reproduction is not possible, the artifact MUST state why and provide the strongest available substitute.

## 4.5 Stable terminology before stylistic variation

A technical object SHOULD have one canonical name in a project. Synonyms MAY appear for teaching or search, but the document MUST identify the canonical term.

Notation, code identifiers, schema fields, and prose terms SHOULD map to one another through a terminology or notation registry.

## 4.6 Explicit uncertainty before apparent completeness

An artifact MUST state material uncertainty, unresolved proof debt, missing controls, unsupported assumptions, and known failure cases.

An artifact MUST NOT use silence to imply that an unresolved question has been settled.

## 4.7 Fail-closed governance

The promotion system MUST fail closed. Missing mandatory metadata, ledgers, reviews, hashes, or exception records MUST block the applicable gate.

A tool MUST NOT infer a promotion state from display text. Machine-readable status fields are authoritative.

# 5. Relationship to Simplified Technical English

ASD-STE100 Issue 9 is the baseline language reference for ordinary technical prose. GCL adopts its central clarity practices, including controlled terminology, short and direct sentences, active voice when the agent is known, stable key terms, topic-bounded paragraphs, and explicit procedural steps.

GCL does not claim that all artifacts are formally ASD-STE100 compliant. Formal STE compliance also depends on its approved dictionary and full rule set.

GCL applies STE principles through profiles:

- The operational profile applies them most strictly.
- The research and public profiles apply them strongly to explanatory prose.
- The mathematical and software profiles permit defined notation, code syntax, formal grammar, identifiers, and logically atomic constructions.
- Exact quotations and source-locked text remain exact.

The detailed controlled-language module will be GCL-TCS-01. Until that module is adopted, this charter supplies the minimum language requirements in Section 11.

