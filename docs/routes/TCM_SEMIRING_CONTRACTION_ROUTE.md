# TCM Semiring-Contraction Route

## Programme placement

Tropical Contraction Machines are a MATHSOLVE route class for finite proof obligations whose search space can be represented as a semiring tensor network.

They are not a fourth pillar and not a trusted theorem prover.

```text
MATHFORGE  -> identify finite/discretizable proof debt and emit problem cards
MATHSOLVE  -> run TCM search and emit artifacts
MATHCERT   -> replay certificates and decide claim status
```

Binding doctrine:

> Search tropical; certify formally.

## Route status

| Field | Value |
| --- | --- |
| Route family | `SEMIRING-CONTRACTION/TCM` |
| Pillar owner | MATHSOLVE |
| Certification owner | MATHCERT |
| Intake owner | MATHFORGE |
| Trusted base | external checker, Lean import, or small replay checker |
| Forbidden claim | TCM proves theorems |
| Allowed claim | TCM emits checkable finite artifacts |

## Eligible obligations

MATHFORGE may route a problem card to TCM when the obligation is finite, bounded, or faithfully discretized and has one of these shapes:

- SAT / MaxSAT / pseudo-Boolean / QUBO;
- finite-domain CSP;
- graph optimization;
- bounded counterexample search;
- finite model or witness search;
- exact counting or degeneracy audit;
- route-selection as a finite optimization problem.

The semantic correspondence between the mathematical subclaim and the finite encoding must be separately recorded. Encoding is a mathematical act, not an implementation detail.

## Trust rule

TCM outputs are evidence until checked.

| Output | Status before MATHCERT | Promotion condition |
| --- | --- | --- |
| witness | candidate | direct replay/check |
| counterexample | candidate | direct replay/check |
| exact contraction trace | evidence | replay by small checker |
| OPB/PB certificate | artifact | PB checker accepts |
| soft tropical gradient | heuristic | never proof-relevant alone |
| visual audit | pedagogy | never proof-relevant alone |

## Fixture ladder

Fixture 006 is the first certificate-interchange milestone for the route.

- MATHSOLVE owns the executable artifact emitter.
- MATHCERT owns the PB replay checker.
- MATHFORGE owns the finite-obligation intake pattern.
- MATH-PROGRAMME owns this route doctrine and ledger.
