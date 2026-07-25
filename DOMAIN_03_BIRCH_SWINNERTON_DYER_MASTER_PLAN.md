# DOMAIN 03 — Birch–Swinnerton-Dyer Master Plan

## 1. Campaign identity

- Campaign ID: `BSD-001`
- Canonical tracker: `MATH-PROGRAMME#66`
- Primary domain: elliptic curves over `\(\mathbb Q\)`
- Primary target: equality of Mordell–Weil rank and analytic rank
- Refined targets: finiteness of the Tate–Shafarevich group and the leading-term formula
- Current state: `WP03_REFEREE_PROMOTED / OPEN_PROBLEM`
- Claim boundary: no proof, reduction, novelty, mechanism, restricted target, universal converse, or certified curve instance is claimed

## 2. Canonical problem

Let \(E/\mathbb Q\) be an elliptic curve. Mordell–Weil gives

\[
E(\mathbb Q)\cong \mathbb Z^{r_{\mathrm{alg}}}\oplus E(\mathbb Q)_{\mathrm{tors}}.
\]

Let \(L(E,s)\) be the complete Hasse–Weil \(L\)-function with all finite Euler factors, and define

\[
r_{\mathrm{an}}=\operatorname{ord}_{s=1}L(E,s).
\]

The rank form of the Birch–Swinnerton-Dyer conjecture is

\[
\boxed{r_{\mathrm{alg}}=r_{\mathrm{an}}.}
\]

The strong formula, in the normalization fixed by `WP00/07_NORMALIZATION_REGISTRY.yaml`, is

\[
\frac{L^{(r)}(E,1)}{r!}
=
\frac{\Omega_E\,\operatorname{Reg}_E\,\#\Sha(E/\mathbb Q)\,\prod_\ell c_\ell}
{\#E(\mathbb Q)_{\mathrm{tors}}^2},
\qquad r=r_{\mathrm{alg}}=r_{\mathrm{an}}.
\]

The campaign treats the rank equality, finiteness of \(\Sha\), and the leading-term identity as separate obligations.

## 3. Named lanes

| Lane | Exact target | Status |
|---|---|---|
| `BSD-RANK-Q` | \(r_{\mathrm{alg}}=r_{\mathrm{an}}\) for every \(E/\mathbb Q\) | open |
| `BSD-SHA-Q` | \(\Sha(E/\mathbb Q)\) is finite for every \(E/\mathbb Q\) | open |
| `BSD-LEAD-Q` | the complete leading-term formula for every \(E/\mathbb Q\) | open |
| `BSD-LOW-RANK` | rank and finiteness consequences when \(r_{\mathrm{an}}\le 1\) | theorem terrain |
| `BSD-P-CONVERSE` | Selmer-to-complex-analytic converse statements at a prime \(p\) | theorem terrain with hypotheses |
| `BSD-P-LEAD` | \(p\)-parts or \(p\)-adic leading-term formulas | theorem terrain with normalization branches |
| `BSD-FAMILY` | density, average, twist-family, or explicit-family theorems | theorem terrain; not universal |
| `BSD-COMPUTE` | rigorous verification for individual finite sets of curves | evidence/certification lane; not universal |

## 4. Theorem spine

| Node | Statement | Status |
|---|---|---|
| `BSD-B000` | elliptic-curve, local-factor, and height definitions | standard |
| `BSD-B010` | Mordell–Weil finite generation | theorem |
| `BSD-B020` | modularity of every elliptic curve over \(\mathbb Q\) | theorem |
| `BSD-B030` | analytic continuation and functional equation of \(L(E,s)\) | theorem via modularity |
| `BSD-B040` | Kummer/Selmer exact sequence | theorem |
| `BSD-B050` | \(\operatorname{corank}\mathrm{Sel}_{p^\infty}=\operatorname{rank}E(\mathbb Q)+\operatorname{corank}\Sha[p^\infty]\) | theorem |
| `BSD-B060` | analytic rank \(0\) or \(1\) implies matching algebraic rank and finite \(\Sha\) | theorem |
| `BSD-B070` | \(p\)-Selmer parity equals analytic parity over \(\mathbb Q\) | theorem |
| `BSD-B080` | selected \(p\)-converses under explicit hypotheses | theorem terrain |
| `BSD-B090` | selected \(p\)-parts of the leading-term formula | theorem terrain |
| `BSD-O100` | universal rank equality | open |
| `BSD-O110` | universal finiteness of \(\Sha\) | open |
| `BSD-O120` | universal leading-term formula | open |

## 5. Work-package sequence

### `BSD-WP00` — Source, normalization, status, and equivalence audit

Promoted on 2026-07-24 after independent Referee review and successful Programme policy checks. The package delivers the canonical source corpus, normalization registry, statement lattice, implication ledger, theorem DAG, claim ledger, proof debt, and certification boundary.

### `BSD-WP01` — False-proof atlas

Referee-promoted on 2026-07-24. The package contains eighteen executable semantic fixtures for parity-to-rank, numerical vanishing, Selmer/rank, hidden-\(\Sha\), one-prime, \(p\)-adic/complex, normalization, higher-rank extrapolation, family, finite-database, height, local-condition, and circularity failures. A triggered fixture rejects or narrows an inference; passing the atlas is not a proof certificate.

### `BSD-WP02` — Source-normalized theorem ledger

Referee-promoted on 2026-07-24. Sixteen theorem interfaces record curve class, direction, rank range, prime and reduction profile, residual hypotheses, Selmer structure, normalization, conclusion, source locator, and composition state. Kato and modern zeta-element source pointers remain noncomposable until theorem-level extraction. Family, finite-database, and individual-curve statements remain below the universal quantifier.

### `BSD-WP03` — Computational and formal substrate

Referee-promoted on 2026-07-24. It separates individual-curve certificate candidates, finite database experiments, and formal interfaces. The package includes certificate and experiment schemas, five bounded formal-interface specifications, exact coupling to WP02 composition states, a claim-promotion graph firewall, three positive and five adversarial cases, deterministic replay, proof debt, and a handoff gate. It contains no certified curve result and no theorem-prover-certified BSD interface yet.

### `BSD-WP04` — Restricted-target scorecard

Next eligible stage, but not authorized. It may select exactly one theorem-grade target only after separate authorization. A target must be narrower than BSD, not a restatement through Selmer notation or finite data, and must have a falsifiable proof-obligation DAG.

## 6. Governing restrictions

1. `rank BSD`, `Sha finiteness`, and `strong BSD` are not synonyms.
2. The complex \(L\)-function and every \(p\)-adic \(L\)-function retain separate normalization records.
3. The root number determines only analytic parity, not exact analytic rank.
4. Selmer groups include both Mordell–Weil and Tate–Shafarevich contributions.
5. A theorem for one prime, one reduction type, one twist family, or one density class remains restricted.
6. Numerical vanishing must be replaced by certified analytic-rank bounds before it can support an individual-curve theorem.
7. The universal conjecture must never be encoded as an axiom in a formal artifact.
8. Mechanism generation, novelty claims, and restricted-target selection remain closed until separately authorized.
9. WP03 structural fixtures are not mathematical certificates and may not be described as verified BSD instances.
