# Pedagogical Style Guide

## Purpose

Grand Challenge pedagogy is not simplification. It is structural revelation
and mathematical control.

The goal is to let a serious reader see what the object is, why it resists
proof, which claims are supported, where the proof debt sits, and what exact
action should happen next.

The binding campaign pattern is the
[Chaidez Pedagogical Protocol](CHAIDEZ_PEDAGOGICAL_PROTOCOL.md).

## Voice

Use a voice that is:

- lucid;
- exact;
- generous to the reader;
- severe with unsupported claims;
- comfortable with partial and negative results;
- explicit about proof debt;
- allergic to performance.

Avoid marketing, mysticism, vague difficulty claims, and victory language
before certification.

## Start with status

Every serious artifact begins with a compact result-status box:

- result status;
- conditional hypotheses;
- strongest supported claim;
- claims explicitly not made;
- computation class;
- certification state;
- first executable step.

The reader should not need to infer whether the headline is proved,
conditional, computational, or open.

## The eight-move exposition pattern

### 1. Plain object

Begin with the object in ordinary mathematical language. Do not begin with
machinery unless the machinery is the object.

Answer:

> What are we actually trying to understand?

### 2. Exact obstruction

Give a small calculation, toy model, counterexample, or failed mechanism that
shows why the naive route breaks.

Answer:

> What specifically prevents the obvious argument from working?

### 3. Working model

Give an example, picture, finite enumeration, or local model. The reader should
be able to touch the object before encountering the full abstraction.

### 4. Restricted claim

State the strongest claim the package is actually equipped to investigate.
Name every condition. Do not let the programme-wide conjecture stand in for
the local target.

### 5. Formal spine

Introduce definitions, propositions, lemmas, and exact hypotheses. Every item
must state its role in the global theorem spine and its dependencies.

A lemma without a role is a loose gear. A theorem list without a dependency
graph is not a campaign.

### 6. Proof, computation, or negative result

Present the mathematical action. Classify each computation as exploratory
evidence, regression audit, exact finite verification, or continuum proof.

### 7. Debt and claim boundary

Separate:

- what is proved;
- what is checked;
- what remains open;
- what requires external verification.

Link unresolved steps to the proof-debt register and state what would discharge
them.

### 8. First executable step

End with one bounded action with named input, output, and completion test.
"Continue research" is not an executable step.

## Required explanatory moves

A serious Work Package must explain:

- why this definition is the right definition;
- what examples it admits and excludes;
- what invariant is being preserved;
- where naive approaches fail;
- which spine node the package advances;
- which dependencies are consumed;
- which finite computations are checks rather than proof;
- which proof debt is created or discharged;
- what formalization would require;
- what would change the claim status;
- why the next step is the correct local move.

## Negative-result discipline

Negative results teach when they identify an exact obstruction. Record:

1. the attempted route;
2. why it was plausible;
3. the smallest exact failure;
4. what the failure rules out;
5. what it leaves viable;
6. the next restricted problem.

Do not conclude only that an approach failed.

## Decorative discipline

Decoration is welcome when it teaches. Diagrams, tables, callouts, analogies,
and names are useful if they compress structure.

Decoration is harmful when it hides uncertainty or substitutes atmosphere for
content.

Use ornament as a lantern, not a curtain.

## Sentence-level guidance

Prefer:

> This computation is an exact finite verification for families of size at
> most 4. It does not establish the unrestricted claim.

Avoid:

> This computation provides strong evidence for the conjecture.

Prefer:

> The obstruction is not enumeration; it is the lack of a monotone quantity
> that survives arbitrary unions.

Avoid:

> The problem is challenging and important.

Prefer:

> This lemma discharges debt item `PD-07` by converting the singleton argument
> into an injective counting statement.

Avoid:

> We prove a useful lemma.

## Final paragraph test

The final paragraph of every Work Package must answer:

1. What did we clarify?
2. What remains unproved?
3. What proof debt blocks the next spine node?
4. What is the first executable step?
5. What would promote the strongest claim in the ledger?
