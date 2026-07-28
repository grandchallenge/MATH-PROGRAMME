# PNP-WP02 — Composition Rules

A proposed proof route may compose ledger records only under the following rules.

## 1. Exact object identity

The language, promise, circuit model, proof system, algebraic family, or meta-complexity problem must match the cited theorem. Similar notation is not identity.

## 2. Hypothesis closure

Every hypothesis and residual hypothesis must be discharged by a named theorem, certificate, or explicit assumption. A transfer theorem does not prove its premise.

## 3. Quantifier preservation

Do not exchange:

- worst case and average case;
- every input and almost every input;
- unrestricted formulas and fixed-width formulas;
- uniform algorithms and nonuniform circuits;
- a named proof system and all proof systems;
- a restricted circuit class and unrestricted circuits;
- a higher complexity class and NP;
- finite verification and asymptotic truth.

## 4. Resource preservation

Runtime is measured in the WP00 bit model. Charge parsing, memory, output, arithmetic bit growth, precision, preprocessing, advice, expansion, and all branches.

## 5. Direction preservation

One-way implications remain one-way. In particular:

- `P = NP` implies `NP = coNP`;
- `NP != coNP` implies `P != NP`;
- a qualifying SAT algorithm can imply a circuit lower bound under theorem-specific conditions;
- a circuit lower bound does not automatically yield the qualifying SAT algorithm;
- avoiding relativization, naturalness, or algebrization is not a proof.

## 6. Source maturity

A current preprint may support an accurately scoped frontier record. It cannot be described as a settled unrestricted theorem. Re-audit the source before promotion.

## 7. Terminal firewall

Only `PNP-T-130` represents the terminal challenge. Its state must remain `OPEN_TERMINAL` until a complete proof package supplies one of the two WP00 terminal certificates.
