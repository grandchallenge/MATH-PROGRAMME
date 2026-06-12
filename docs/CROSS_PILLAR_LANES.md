# Cross-Pillar Lanes

## Why lanes exist

Some kinds of mathematical work recur across domains. A lane is a reusable route through the three pillars: discovery, campaign, certification.

A lane should state:

- what kind of mathematical obligation it handles;
- what MATHFORGE emits;
- what MATHSOLVE decides;
- what MATHCERT checks;
- what status words are allowed before certification.

## Lane 01: algebraic witness to certificate

This lane covers polynomial identities, Gröbner-style normal forms, ideal membership, ideal equality, elimination, radical membership, and finite truncations of algebraic systems.

```text
MATHFORGE
  external CAS / exact search / symbolic exploration
  -> algebraic witness JSON

MATHSOLVE
  recognize algebraic subproblem
  -> invoke tactic or request witness
  -> prepare certification handoff

MATHCERT
  replay or Lean-check certificate
  -> promote only checked claims
```

### MATHFORGE responsibility

MATHFORGE may call SageMath, SymPy, Singular, Magma, or custom exact routines. Its artifact is a candidate witness with provenance, not a proof.

Allowed pre-certification statuses:

- `external_output_only`;
- `external_witness_recorded`;
- `script_replayed`;
- `ready_for_mathcert`.

### MATHSOLVE responsibility

MATHSOLVE decides whether the local proof obligation is genuinely algebraic and whether a Gröbner-style tactic is appropriate.

Allowed tactical statuses:

- `candidate`;
- `witness_requested`;
- `witness_available`;
- `sent_to_mathcert`;
- `rejected`.

Only after MATHCERT accepts the artifact may the status become `certified_by_mathcert`.

### MATHCERT responsibility

MATHCERT owns the proof boundary. It may accept:

- a checked Lean theorem;
- an independently replayed exact certificate;
- a formalized reduction plus exact replay;
- another explicitly trusted proof-producing route.

External CAS output alone is never certification.

## How to add a new lane

A new lane should include:

1. a human doctrine document;
2. an input schema;
3. an output or handoff schema;
4. a toy fixture;
5. allowed statuses;
6. a rejection policy;
7. a promotion route into MATHCERT.

The first question is not "Can a tool do this?" The first question is "Where is the proof boundary?"
