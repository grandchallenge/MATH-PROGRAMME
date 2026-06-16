# Fixture Ledger: TCM Fixture 006

## Identifier

`TCM-FIXTURE-006`

## Title

External Checker Round-Trip for a Pseudo-Boolean Assignment Certificate

## Purpose

Fixture 006 demonstrates the first cross-pillar certificate-interchange path for Tropical Contraction Machines.

The fixture is deliberately small, but it exercises the full status boundary:

```text
finite PB obligation
  -> exact max-plus/count TCM search
  -> OPB + primal witness + dual certificate
  -> MATHCERT replay checker
  -> checked or rejected result card
```

## Claim under audit

A 5x5 max-weight assignment OPB instance has optimum value `85` and a unique optimum.

This is not a new mathematical theorem. It is a prover-component fixture.

## Pillar ownership

| Artifact | Owner repo | Status |
| --- | --- | --- |
| Route doctrine | `grandchallenge/MATH-PROGRAMME` | this ledger |
| Artifact emitter | `grandchallenge/MATHSOLVE` | companion PR |
| PB replay checker | `grandchallenge/MATHCERT` | companion PR |
| Intake pattern | `grandchallenge/MATHFORGE` | companion PR |

## Promotion criteria

The fixture is promoted from `artifact_emitted` to `checked` only when MATHCERT replays:

1. the OPB objective;
2. the primal witness objective;
3. the row/column dual upper bound;
4. equality of lower and upper bounds;
5. agreement with the result card.

## Trust boundary

- The TCM search trace is untrusted evidence.
- The OPB instance, witness, and dual certificate are durable artifacts.
- The MATHCERT checker transcript is the certification boundary for this fixture.
- The Lean stub is an import scaffold, not a completed proof.

## Failure modes

- malformed OPB artifact;
- infeasible witness;
- invalid dual inequality;
- primal/dual mismatch;
- result-card mismatch;
- overclaiming external certification when only local artifact emission occurred.

## Grand Challenge reading

Fixture 006 should be read as a route maturity test, not as a solver benchmark. The key achievement is not the numerical optimum. The key achievement is a clean handoff from tropical search to exact replay.
