# GRAND_CHALLENGE_PEDAGOGY_STANDARD.md

## Purpose

Pedagogy is not decoration. It is the discipline of making mathematical structure visible without falsifying it. Every Grand Challenge artifact must teach the reader what is being studied, what obstructs progress, what has changed, and what remains unresolved.

## Three readings

Every serious artifact should support three readings.

### Lay reading

For an intelligent non-specialist. The reader should learn the object, the motivation, the result boundary, and the next step.

### Research reading

For a mathematically trained reader. The reader should see definitions, theorem spine, known results, proof strategy, computations, and failure modes.

### Certification reading

For a formalization or verification worker. The reader should see Lean/equivalent targets, certificate formats, dependencies, and blockers.

## Five questions

Every Work Package must answer:

1. What is the object?
2. What is the obstruction?
3. What is the reduction or attack?
4. What has actually been proved or checked?
5. What is the next sharp move?

## Tone

The tone should be lucid, serious, generous, and exact. Avoid hype. Avoid corporate abstractions. Avoid mystical phrasing. Avoid fake humility. The reader should feel invited into the structure, not impressed from outside it.

## Diagrams and examples

Use examples whenever they expose structure. For Union-Closed Sets, show small families, frequency counts, the role of the top union, and why the half bound is sharp for a full powerset.

## Failure pedagogy

A failed proof attempt should be written when it teaches something. Describe why the route was tempting and what obstruction broke it. Do not include dead ends as filler.

## Certification pedagogy

Every Lean/equivalent file should include a human-facing companion:

```text
Human statement
Formal statement
Informal meaning
Dependencies
What is checked
What remains unchecked
Connection to Work Package claim ledger
```

## Pedagogical anti-patterns

Reject text that:

- says a problem is important without explaining why;
- uses technical definitions without examples;
- reports a computation without saying what it proves;
- reports a proof without saying what it means;
- lists citations without a status map;
- hides what remains unknown.

## Binding maxim

> The reader should leave knowing more mathematics, not merely believing that mathematics was done.
