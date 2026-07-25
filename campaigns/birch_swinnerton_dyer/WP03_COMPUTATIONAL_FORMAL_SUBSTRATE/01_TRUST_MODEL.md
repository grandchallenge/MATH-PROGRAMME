# WP03 trust model

## 1. Three noninterchangeable trust classes

### `individual_curve_certificate`

An artifact may certify only the exact claims named in its manifest and only for the exact curve identifier and model recorded there. A certificate must bind:

- a canonical curve identifier and explicit Weierstrass coefficients;
- the exact target claim;
- source-normalized theorem interfaces imported from WP02;
- complete computational provenance;
- proof-producing or rigorously bounded evidence;
- normalization and local-factor conventions;
- a negative claim boundary.

Floating-point output, high precision, agreement between programs, or database membership is not by itself a certificate.

### `finite_database_experiment`

An experiment binds a finite immutable snapshot, a reproducible selection query, the exact number of selected records, software provenance, and descriptive outputs. It may:

- find counterexamples to an auxiliary finite-scope assertion;
- test implementation consistency;
- generate hypotheses;
- measure finite-population frequencies.

It may not prove a universal theorem or certify an individual curve unless a separate certificate packet is constructed.

### `formal_interface`

A formal interface exposes a bounded algebraic or logical statement suitable for theorem-prover certification. It must list every imported assumption. It may not encode BSD, universal \(\Sha\)-finiteness, a universal converse, or a leading-term identity as an axiom.

## 2. Trust lattice

```text
numerical observation
      |
      v
finite experiment ----------------------+
      |                                 |
      | no theorem promotion            | no universal promotion
      v                                 v
individual certificate candidate   hypothesis only

formal interface --proof replay--> certified interface
```

There is no edge from finite experiment to universal theorem. There is no edge from certified interface to BSD unless a separately reviewed proof supplies all missing mathematical obligations.

## 3. Required language

Permitted:

- “verified for the finite snapshot recorded in the manifest”;
- “candidate individual-curve certificate”;
- “formally certified algebraic interface”;
- “no counterexample found in the stated finite population.”

Prohibited:

- “therefore BSD holds”;
- “verified for all elliptic curves”;
- “the data proves the conjecture”;
- “the formalization proves BSD” when it only proves an interface lemma.
