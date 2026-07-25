# BSD-WP00 — Foundation, source, normalization, status, and equivalence audit

## Metadata

- Domain: arithmetic of elliptic curves over \(\mathbb Q\)
- Campaign: `BSD-001`
- Work Package: `BSD-WP00`
- Canonical tracker: `MATH-PROGRAMME#66`
- Primary type: source audit, normalization registry, statement lattice, and proof-obligation map
- Global theorem-spine nodes advanced: `BSD-B000` through `BSD-B090`
- Incoming dependencies: Mordell–Weil; modularity; Hasse–Weil \(L\)-functions; Selmer groups; Gross–Zagier; Kolyvagin systems; Iwasawa theory
- Claim status: WP00 source and semantic audit promoted; universal conjecture open
- Certification target: human audit, machine validation of ledgers, selective Lean formalization
- Foundational profile: present
- Promotion state: promoted

## 1. Result-status box

| Field | Value |
|---|---|
| Result status | `WP00 PROMOTED / OPEN PROBLEM` |
| Conditional on | standard definitions of elliptic curves, Galois cohomology, local conditions, modular \(L\)-functions, and Néron–Tate heights |
| Strongest supported claim | the rank, \(\Sha\)-finiteness, and leading-term statements are distinct; the low analytic-rank \(0/1\) bridge is known; the universal higher-rank and strong formulas remain open; all converse and \(p\)-part results require exact hypotheses |
| Not claimed | a proof of BSD, a new reduction, universal finiteness of \(\Sha\), a universal converse, or promotion of finite/family evidence |
| Support-route class | `PRIMARY_SOURCE_AUDIT`, `SEMANTIC_CORRESPONDENCE_AUDIT`, `NORMALIZATION_AUDIT`, `LOGICAL_DECOMPOSITION` |
| Foundational profile | arithmetic geometry over \(\mathbb Q\); high normalization and imported-theorem risk |
| Certification state | human audit promoted; formal certification pending |
| First executable step | run WP01 false-proof atlas and WP02 theorem ledger in parallel |

## 2. Foundational profile

```yaml
foundational_profile:
  carrier_type: arithmetic_geometric
  ambient_structure:
    - schemes
    - elliptic_curves
    - number_fields
    - local_fields
    - Galois_cohomology
    - finitely_generated_abelian_groups
    - complex_L_functions
    - p_adic_L_functions
    - height_pairings
  regularity:
    - smooth_projective_genus_one_curve_with_rational_origin
    - global_minimal_Neron_model
  axiom_profile:
    base: classical_algebra_number_theory_and_analysis
    choice_usage: standard_algebra_and_cohomology
    excluded_middle: used
    large_cardinal_usage: none
    determinacy_usage: none
  witness_policy:
    existence_claim: theorem_or_explicit_curve_certificate
    witness_location: source_theorem_database_or_formal_object
  certification_target:
    - human_audit
    - schema_validation
    - Lean
  pathology_risk:
    level: high
    notes: Normalization drift, hidden local conditions, Selmer-versus-rank conflation, unproved Sha finiteness, exceptional-zero phenomena, and family-to-universal inference are principal risks.
```

## 3. Lay executive companion

### The object

An elliptic curve has two independent-looking measurements of complexity.

- The arithmetic measurement counts independent rational points.
- The analytic measurement counts how many derivatives of its \(L\)-function vanish at the central point.

BSD asserts that these counts are identical.

### The obstruction

The \(L\)-function sees global prime-by-prime data. Rational points are discrete geometric objects. Selmer groups mediate between them, but a Selmer group also contains the hidden contribution of the Tate–Shafarevich group. The bridge is therefore not a direct equality of two easily compared dimensions.

### The restricted theorem frontier

The bridge is known when the analytic rank is \(0\) or \(1\). Higher rank requires mechanisms capable of controlling several independent global classes and a determinant of height pairings, not merely one distinguished Heegner point or one Euler-system direction.

### What this package achieved

1. Fixed the complete complex \(L\)-function normalization.
2. Reconciled it with Wiles's incomplete official-problem notation.
3. Separated rank BSD, \(\Sha\) finiteness, strong BSD, \(p\)-converses, \(p\)-parts, parity, family results, and finite computation.
4. Audited the Selmer exact sequence and its logical consequences.
5. Recorded the low-rank theorem frontier and restricted converse terrain.
6. Built the implication ledger, dependency DAG, proof-debt register, and certification handoff.
7. Promoted WP01 and WP02 as the only admissible next mathematical stages.

### What this package did not achieve

It did not prove a new theorem. It did not establish any universal higher-rank bridge, any universal finiteness theorem for \(\Sha\), or any missing leading-term identity.

## 4. Formal problem statement

For every elliptic curve \(E/\mathbb Q\), prove

\[
\operatorname{rank}_{\mathbb Z}E(\mathbb Q)
=
\operatorname{ord}_{s=1}L(E,s).
\]

The refined campaign separately asks for finiteness of

\[
\Sha(E/\mathbb Q)
=
\ker\!\left(H^1(\mathbb Q,E)\to\prod_v H^1(\mathbb Q_v,E)\right)
\]

and the leading-term formula fixed in `07_NORMALIZATION_REGISTRY.yaml`.

## 5. Object and obstruction

The exact Kummer/Selmer sequence is

\[
0\to E(\mathbb Q)\otimes\mathbb Q_p/\mathbb Z_p
\to\operatorname{Sel}_{p^\infty}(E/\mathbb Q)
\to\Sha(E/\mathbb Q)[p^\infty]\to0.
\]

Thus

\[
\operatorname{corank}\operatorname{Sel}_{p^\infty}
=
\operatorname{rank}E(\mathbb Q)
+
\operatorname{corank}\Sha[p^\infty].
\]

This one line is the smallest exact obstruction to treating “Selmer rank” as “Mordell–Weil rank.”

## 6. Known terrain and source audit

The authoritative audit is `04_SOURCE_NORMALIZATION_EQUIVALENCE_AUDIT.md`.

| Terrain | Supported determination |
|---|---|
| official status | unsolved as of `2026-07-24` |
| analytic existence | modularity gives continuation and functional equation for all \(E/\mathbb Q\) |
| analytic rank \(0/1\) | rank equality and finite \(\Sha\) known |
| parity | \(p\)-Selmer parity equals analytic parity for all \(E/\mathbb Q\) and all \(p\) |
| converse | substantial restricted theorems; no universal bridge |
| leading term | many restricted \(p\)-parts and families; no universal formula |
| computation | can prove individual finite cases; cannot discharge the universal quantifier |

## 7. Claim ledger and trust quartet

### Claim summary

| Claim ID | Statement | State |
|---|---|---|
| `BSD-C001` | the official rank conjecture is the equality of algebraic and analytic rank | audited |
| `BSD-C002` | modularity makes \(r_{\mathrm{an}}\) defined for every \(E/\mathbb Q\) | audited theorem |
| `BSD-C003` | analytic rank \(0/1\) gives matching rank and finite \(\Sha\) | audited theorem terrain |
| `BSD-C004` | Selmer corank contains both rank and \(\Sha[p^\infty]\) | checked exact sequence |
| `BSD-C005` | \(p\)-Selmer parity agrees with analytic parity | audited theorem |
| `BSD-C006` | rank, finiteness, and leading coefficient are distinct obligations | checked semantic decomposition |
| `BSD-C007` | converse and \(p\)-part theorems are hypothesis-sensitive | audited |
| `BSD-C008` | universal BSD remains open | current-status audited |
| `BSD-C009` | family and finite computational results do not imply universal BSD | checked logical boundary |

### What is proved?

Only standard logical and normalization consequences are reconstructed in this package: the local-factor convention, equality of orders for \(L\) and \(\Lambda\), the Selmer-corank decomposition, and the implication/non-implication lattice.

### What is checked?

The official statement, current status, modularity consequence, low-rank theorem frontier, parity theorem, selected converse statements, and selected \(p\)-part statements.

### What remains open?

The universal rank equality, universal finiteness of \(\Sha\), universal leading-term formula, and every unrestricted higher-rank analytic–arithmetic bridge.

### What requires external verification?

Exact theorem-number and hypothesis extraction for the complete WP02 ledger, especially Kolyvagin variants, Kato/Rubin interfaces, exceptional primes, and the full modern \(p\)-adic normalization taxonomy.

## 8. Theorem-spine slice and dependency DAG

See `06_DEPENDENCY_DAG.json`. The central chain is

```text
modularity -> analytic continuation and functional equation -> analytic rank
Mordell-Weil + Kummer theory -> Selmer exact sequence
analytic rank 0/1 -> rank equality and finite Sha
restricted Iwasawa/Euler-system hypotheses -> selected converses and p-parts
missing universal higher-rank bridge -> BSD-RANK-Q remains open
missing universal Sha and leading-term control -> BSD-SHA-Q and BSD-LEAD-Q remain open
```

## 9. Proofs and classified computations

WP00 uses no curve computation.

- normalization reconciliation: `SEMANTIC_CORRESPONDENCE_AUDIT`;
- Selmer exact-sequence consequences: `ALGEBRAIC_DERIVATION`;
- current status and theorem frontier: `PRIMARY_SOURCE_AUDIT`;
- statement lattice and non-implications: `LOGICAL_DECOMPOSITION`.

## 10. Failure and negative-result analysis

### Rejected shortcut

The functional equation sign gives the parity of analytic rank, not its exact value.

### Rejected arithmetic shortcut

A Selmer corank is not a Mordell–Weil rank unless the divisible \(p\)-primary contribution of \(\Sha\) is controlled.

### Rejected refinement shortcut

A theorem for the \(p\)-part of a formula does not prove the formula at every prime or its archimedean normalization.

### Rejected quantifier shortcut

A positive proportion, an infinite twist family, or every curve below a conductor bound does not imply every elliptic curve.

### Viable next work

WP01 should encode these failures as fixtures. WP02 should extract exact hypotheses and theorem numbers for all admitted imported interfaces.

## 11. Proof-debt register

See `09_PROOF_DEBT.json`. No unresolved mathematical source item changes the canonical open-status determination. Repository policy checks and independent Referee review passed; the remaining debt is nonblocking for WP01/WP02 progression.

## 12. Certification boundary and MATHCERT handoff

The first formal targets are:

1. the logical separation of rank, finiteness, and leading-term statements;
2. the corank consequence of the Selmer exact sequence;
3. complete versus incomplete Euler-factor conversion records;
4. root-number parity as a statement interface;
5. machine validation of source, implication, and claim ledgers.

Imported deep theorems remain provenance-bearing assumptions. BSD itself must not be encoded as an axiom.

## 13. First executable step

- Input: the WP00 audit bundle.
- Operation: run WP01 false-proof atlas and WP02 source-normalized theorem ledger in parallel.
- Output: falsification fixtures and a theorem-by-theorem hypothesis matrix.
- Completion test: no imported result is cited only by theorem name; every route records curve class, prime, reduction, direction, and exact conclusion.
- Spine nodes advanced: `BSD-B080` and `BSD-B090`.

## 14. Escalation gate

- [x] Canonical problem and refined obligations are separated.
- [x] Complex \(L\)-function normalization is fixed.
- [x] Official incomplete notation is reconciled.
- [x] Selmer-to-rank correspondence is audited.
- [x] Low-rank theorem frontier is recorded.
- [x] Universal and restricted quantifiers are separated.
- [x] Claim and proof-debt ledgers are present.
- [x] Certification boundary is explicit.
- [x] Repository CI has passed (`Programme policy checks` run `30083374165`).
- [x] Independent Referee promotion has been recorded.
