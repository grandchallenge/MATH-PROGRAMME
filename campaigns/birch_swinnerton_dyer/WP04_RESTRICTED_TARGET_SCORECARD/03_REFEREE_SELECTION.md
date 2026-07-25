# BSD-WP04 — Referee target-selection decision

## Decision

Select `BSD-R2-A1` as the first theorem-grade restricted research target for campaign `BSD-001`.

The selected statement is the exact \(2\)-primary valuation identity in the rank-one BSD formula for semistable odd-conductor elliptic curves over \(\mathbb Q\) with good ordinary reduction at \(2\) and irreducible \(E[2]\).

## Status semantics

`SELECTED_RESEARCH_TARGET_UNPROVED` means:

- the statement, curve class, quantifiers, and normalization are fixed;
- the current bounded source delta did not locate an exact general theorem for the class;
- the proof-obligation DAG and adversarial gates are explicit;
- the statement is not proved, certified, or claimed novel;
- universal rank equality, universal \(\Sha\)-finiteness, and the universal leading-term formula remain open.

## Scorecard

Scores are 0–5. Execution cost is subtracted.

| Dimension | R2-A1 | R2-A0 | PC2-1 | ADD-1 | HR2-1 |
|---|---:|---:|---:|---:|---:|
| leverage | 5 | 4 | 4 | 4 | 5 |
| non-circularity | 5 | 5 | 4 | 4 | 2 |
| audited open gap | 5 | 5 | 4 | 3 | 4 |
| proof tractability | 2 | 3 | 2 | 1 | 1 |
| formalizability | 4 | 4 | 4 | 3 | 2 |
| falsifiability | 5 | 5 | 4 | 3 | 3 |
| full-problem relevance | 5 | 4 | 4 | 4 | 5 |
| information value if false | 5 | 4 | 4 | 4 | 5 |
| interface readiness | 4 | 4 | 3 | 1 | 1 |
| execution cost | 4 | 3 | 4 | 5 | 5 |
| **adjusted score** | **36** | **35** | **29** | **22** | **23** |

## Referee reconstruction

### Exact source boundary

Odd-prime rank-one \(p\)-parts include good and multiplicative reduction theorems, and newer good-ordinary and Eisenstein work expands that terrain. Those general interfaces retain \(p>2\). Audited \(2\)-primary results are CM-specific, family-specific, or modulo-squares transport statements rather than the exact general valuation identity selected here.

This is a bounded source-audit conclusion. It is not a novelty or priority determination.

### Non-vacuity

LMFDB curve `53.a1` belongs to the selected class: it is semistable of odd conductor \(53\), has analytic rank one and trivial rational torsion, and is ordinary at \(2\). Trivial rational torsion implies \(E(\mathbb Q)[2]=0\), hence irreducibility of the two-dimensional \(\mathbb F_2\)-representation. This establishes only that the class is nonempty.

### Non-circularity

The analytic-rank-one hypothesis invokes the established low-rank theorem to make rank, regulator, and finite \(\Sha\) legitimate inputs. The selected conclusion is not used to generate those inputs.

### Bounded conclusion

The result would establish only an \(\operatorname{ord}_2\) equality. It would not determine odd-prime valuations, the sign of the rational quotient, or the full leading-term formula.

### Adversarial value

The target forces exact treatment of \(2\)-adic local conditions, integrality and exceptional factors, complete versus incomplete \(L\)-functions, period and isogeny normalization, and Selmer-to-\(\Sha[2^\infty]\) comparison.

## Other dispositions

- `BSD-R2-A0` remains the fallback target if rank-one reciprocity proves inessentially harder than the \(2\)-primary arithmetic itself.
- `BSD-PC2-1` remains a separate converse candidate but is not authorized.
- `BSD-ADD-1` may re-enter only after exact local normalization.
- `BSD-HR2-1` is rejected unless independent height nondegeneracy is proved.

## Validation

The pre-promotion target-scorecard replay `30140379838` and Programme policy workflow `30140379827` passed. Independent Referee reconstruction found no blocking source, semantic, or proof-architecture defect.

## Gate

Selection does not authorize mechanism generation. `BSD-WP05` may reconstruct the exact \(2\)-adic source interfaces and sharpen the DAG only after separate authorization.
