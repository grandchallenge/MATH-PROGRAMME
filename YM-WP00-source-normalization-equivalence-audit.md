# YM-WP00 — Source, Normalization, and Equivalence Audit

**Artifact ID:** `YM-WP00-source-normalization-equivalence-audit`  
**Challenge:** Yang–Mills Existence and Mass Gap  
**Programme lane:** MATHSOLVE  
**Status:** `INTERNAL REVIEW COMPLETE — PROMOTION ELIGIBLE`  
**Version:** 0.1.0  
**Audit date:** 2026-07-24  
**Promotion authority:** Referee  
**Claim class:** `SOURCE-NORMALIZED / NON-SOLUTION ARTIFACT`

---

## 0. Executive disposition

This Work Package fixes the statement, normalization conventions, implication graph, and claim boundary for the Yang–Mills Existence and Mass Gap challenge.

It does **not** claim:

- construction of a four-dimensional quantum Yang–Mills theory;
- proof of a continuum or physical mass gap;
- proof of confinement;
- proof of an area law;
- proof that any presently known lattice, perturbative, numerical, stochastic, or gauge-fixed construction solves the Clay problem.

The artifact is promotion-eligible as a **problem-definition and equivalence-control dossier only**. No theorem-strengthening, mechanism-generation, or numerical work is authorized by this status.

---

## 1. Object in view

For every compact simple gauge group \(G\), construct a nontrivial quantum Yang–Mills theory on four-dimensional spacetime and prove a strictly positive finite mass gap.

The canonical theorem target is:

> For every compact simple gauge group \(G\), there exists a nontrivial quantum Yang–Mills theory on \(\mathbb R^4\), satisfying axiomatic properties at least as strong as the Wightman and Osterwalder–Schrader schemes cited by Jaffe and Witten, whose physical Hamiltonian \(H\) has a vacuum \(\Omega\) and some \(\Delta>0\) such that
> \[
> H\Omega=0,
> \qquad
> \operatorname{spec}(H)\cap(0,\Delta)=\varnothing,
> \]
> with the supremal admissible gap finite.

The theorem has two inseparable trunks:

- **YM-E — Existence:** construct and identify the nontrivial interacting continuum theory with the required axiomatic, local, spectral, and ultraviolet properties.
- **YM-M — Mass gap:** prove a strictly positive gap in the physical Hamiltonian spectrum above the vacuum.

Neither trunk is accepted as a substitute for the other.

---

## 2. Obstruction in focus

The central obstruction is not a single estimate. It is the simultaneous control of:

1. ultraviolet regulator removal;
2. infinite-volume passage;
3. gauge invariance and the physical observable sector;
4. positivity sufficient to reconstruct a physical Hilbert space;
5. locality and Poincaré covariance;
6. nontriviality of the limiting theory;
7. asymptotically free short-distance behaviour;
8. a positive infrared spectral scale that survives all regulator limits.

A proof route that controls only one regime or one representation of the theory remains incomplete unless the interfaces to all other obligations are proved.

---

## 3. Binding sources

### 3.1 Normative source ledger

| ID | Source | Role | Binding content used here |
|---|---|---|---|
| `SRC-YM-00` | Arthur Jaffe and Edward Witten, *Quantum Yang–Mills Theory*, official Clay problem description: <https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf> | Normative problem statement | Quantification over compact simple \(G\); nontrivial theory on \(\mathbb R^4\); mass-gap definition; axiomatic floor; local gauge-invariant observables; short-distance asymptotic-freedom requirements; clustering consequence; finite-volume warning. |
| `SRC-YM-01` | Clay Mathematics Institute, *Yang–Mills & the Mass Gap*: <https://www.claymath.org/millennium/yang-mills-the-maths-gap/> | Current institutional status and overview | The problem remains listed as unsolved; physical and computational evidence is not a mathematical construction or proof. |
| `SRC-AX-00` | R. Streater and A. Wightman, *PCT, Spin and Statistics, and All That*, W. A. Benjamin, 1964; cited as [45] by Jaffe–Witten | Minkowski axiomatic floor | Positive-energy Hilbert-space formulation, vacuum, covariance, locality, and operator-valued-distribution framework. |
| `SRC-AX-01` | K. Osterwalder and R. Schrader, “Axioms for Euclidean Green’s Functions,” *Commun. Math. Phys.* 31 (1973), 83–112, DOI 10.1007/BF01645738 | Euclidean reconstruction source | Euclidean axiom scheme and reflection-positivity route toward a physical Hilbert-space theory. |
| `SRC-AX-02` | K. Osterwalder and R. Schrader, “Axioms for Euclidean Green’s Functions II,” *Commun. Math. Phys.* 42 (1975), 281–305, DOI 10.1007/BF01608978 | Euclidean reconstruction correction/completion | Reconstruction and analytic-continuation hypotheses must be read with the corrected/completed formulation. |

### 3.2 Source hierarchy

For this campaign:

1. `SRC-YM-00` fixes the challenge statement.
2. `SRC-AX-00`–`SRC-AX-02` fix the cited axiomatic floor.
3. Later literature may sharpen implementation choices but may not silently weaken the target.
4. Numerical, perturbative, physical, or heuristic sources are evidence classes, not theorem authorities.

### 3.3 Source-language control

Jaffe–Witten use both mandatory and programmatic language. This audit normalizes it as follows:

| Source language | Normalized status |
|---|---|
| “Prove that …” | Mandatory theorem obligation. |
| “Existence includes … at least as strong as …” | Mandatory axiomatic lower bound; alternative axiom systems require a proved strength comparison. |
| “one should define …” | Part of the official intended meaning of existence and therefore a required acceptance item unless a formally equivalent substitute is proved. |
| “should agree at short distances …” | Required ultraviolet-concordance obligation; the exact topology and observable class must be stated by a proposed solution. |
| “an important consequence … is clustering” | Direction explicitly supported: physical mass gap implies exponential clustering for suitable centred local observables. The converse is not granted without reconstruction and spectral hypotheses. |
| “may play a fundamental role” | Strategic observation, not part of the theorem statement. |

---

## 4. Canonical theorem specification

### 4.1 Quantifiers

The target is universally quantified:

\[
\forall G\;\bigl(G\text{ compact and simple}\bigr)
\Longrightarrow
\exists\,\mathcal Q_G,\Delta_G>0
\]

such that \(\mathcal Q_G\) is a nontrivial four-dimensional pure quantum Yang–Mills theory satisfying the accepted axiomatic profile and possessing physical gap \(\Delta_G\).

The theorem does **not** merely ask for one selected group, one rank, or one asymptotic family. A reduction to a canonical subfamily is admissible only if the reduction theorem is proved.

### 4.2 Spacetime and signature

- The physical target is a theory on Minkowski \(\mathbb R^{1,3}\).
- The official notation “on \(\mathbb R^4\)” permits a Euclidean constructive route.
- A Euclidean construction counts only after the relevant Osterwalder–Schrader hypotheses and reconstruction are established.
- A compact torus, finite lattice, finite box, or infrared-cutoff space is an approximation domain, not the terminal target.

### 4.3 Field content

The target is **pure** Yang–Mills theory for compact simple \(G\), absent matter or Higgs fields unless an exact reduction removes the added sector without changing the target theory.

### 4.4 Physical observable sector

The construction must identify local quantum observables corresponding, with the required renormalization qualifications, to gauge-invariant local polynomials in the curvature \(F\) and its covariant derivatives.

A gauge potential \(A\) in a fixed gauge is not itself sufficient to identify the physical observable algebra.

### 4.5 Nontriviality

“Nontrivial” is not normalized as merely “nonzero partition function” or “nonempty Hilbert space.” A candidate solution must provide a criterion excluding a Gaussian/free or otherwise degenerate limit. Acceptable criteria may include a proved non-Gaussian Schwinger hierarchy, nonvanishing connected observables, or nontrivial scattering/interaction structure, provided the criterion is tied to the reconstructed physical theory.

### 4.6 Vacuum and Hamiltonian

The reconstructed physical theory must include:

- a positive-definite Hilbert space \(\mathcal H\);
- a strongly continuous positive-energy representation of translations;
- a self-adjoint Hamiltonian \(H\ge 0\);
- a Poincaré-invariant vacuum \(\Omega\), unique up to phase under the adopted axiom profile;
- \(H\Omega=0\).

### 4.7 Mass gap

A physical mass gap exists when there is \(\Delta>0\) with

\[
\operatorname{spec}(H)\cap(0,\Delta)=\varnothing.
\]

Following the official statement, the supremum of admissible \(\Delta\) is required to be finite. This prevents the empty-excitation or otherwise degenerate interpretation from satisfying the words vacuously.

### 4.8 Ultraviolet concordance

The local correlation functions must have the required short-distance relation to asymptotic freedom and perturbative renormalization, including the prescribed local singularity structure. A proposed solution must state:

- the renormalized observable family;
- the scale and scheme conventions;
- the topology or distributional mode of convergence;
- the theorem connecting the nonperturbative construction to the perturbative asymptotics.

Formal beta-function calculations alone do not discharge this item.

---

## 5. Theorem-obligation ledger

### 5.1 YM-E — Existence trunk

| ID | Obligation | Acceptance condition | Status |
|---|---|---|---|
| `YM-E01` | Regulated definition | Finite regulator theory is mathematically defined with all parameters and measures/operators specified. | Open |
| `YM-E02` | Gauge control | Gauge redundancy is quotiented, fixed, or encoded without losing the physical observable sector. | Open |
| `YM-E03` | Ultraviolet limit | Cutoff/lattice-spacing removal is proved in a stated topology. | Open |
| `YM-E04` | Infinite-volume limit | Thermodynamic limit on \(\mathbb R^4\) is proved and identified. | Open |
| `YM-E05` | Euclidean axioms | Euclidean invariance, symmetry, regularity, clustering/ergodicity as required, and reflection positivity are proved for the limiting Schwinger functions. | Open |
| `YM-E06` | Reconstruction | A positive physical Hilbert space, vacuum, translations, Hamiltonian, locality, and covariance are reconstructed. | Open |
| `YM-E07` | Local observables | Gauge-invariant local quantum fields corresponding to curvature polynomials and covariant derivatives are constructed with renormalization control. | Open |
| `YM-E08` | Nontriviality | The continuum theory is proved interacting/non-Gaussian under an explicit criterion. | Open |
| `YM-E09` | UV concordance | Short-distance correlations are proved consistent with asymptotic freedom and perturbative renormalization. | Open |
| `YM-E10` | Universality in \(G\) | All compact simple \(G\), or a proved reduction covering them, are treated. | Open |

### 5.2 YM-M — Mass-gap trunk

| ID | Obligation | Acceptance condition | Status |
|---|---|---|---|
| `YM-M01` | Physical Hamiltonian | Gap is stated for the reconstructed physical \(H\), not merely a gauge-fixed auxiliary operator. | Open |
| `YM-M02` | Positive lower bound | Some \(\Delta_G>0\) excludes physical spectrum in \((0,\Delta_G)\). | Open |
| `YM-M03` | Finite gap scale | Supremal gap is finite as required by the official formulation. | Open |
| `YM-M04` | Volume uniformity | Any finite-volume lower bound is uniform enough to survive the infinite-volume limit. | Open |
| `YM-M05` | Cutoff uniformity | Any regulated lower bound survives continuum scaling in physical units. | Open |
| `YM-M06` | Observable-sector linkage | Correlation-decay evidence is linked to a dense or separating physical observable class sufficient for the spectral conclusion. | Open |
| `YM-M07` | Vacuum control | Vacuum sector and possible degeneracy/superselection issues are explicitly treated. | Open |
| `YM-M08` | Universality in \(G\) | Gap result covers each compact simple \(G\), or follows through a proved reduction. | Open |

---

## 6. Typed support route

Every claim in later Yang–Mills work must carry one of these support types:

| Type | Meaning |
|---|---|
| `SRC` | Directly fixed by a cited authoritative source. |
| `DEF` | Definition introduced for the campaign. |
| `THM` | Proved theorem with hypotheses and dependency route. |
| `LEM` | Proved intermediate lemma. |
| `EQV` | Proved equivalence, with both directions and hypotheses. |
| `IMP` | Proved one-way implication. |
| `NUM` | Numerical evidence only. |
| `PERT` | Perturbative or formal expansion evidence only. |
| `HEUR` | Physical or mathematical heuristic. |
| `OBS` | Open proof obligation. |
| `EXC` | Explicit non-equivalence or excluded inference. |

No `NUM`, `PERT`, or `HEUR` item may be promoted directly to `THM`, `IMP`, or `EQV` without a separately checked proof artifact.

---

## 7. Equivalence and implication graph

### 7.1 Core route

```text
regulated gauge model
        |
        |  continuum + thermodynamic limits, identification
        v
Euclidean Schwinger hierarchy
        |
        |  Osterwalder–Schrader hypotheses and reconstruction
        v
physical Hilbert-space QFT
        |
        |  translation generators and positive energy
        v
self-adjoint physical Hamiltonian H
        |
        |  uniform nonzero spectral lower bound
        v
physical mass gap
```

Every arrow is a theorem obligation. No arrow is definitional by default.

### 7.2 Edge ledger

| Edge | Type | Required hypotheses | What is not licensed |
|---|---|---|---|
| Regulated lattice/continuum-cutoff model \(\to\) limiting Schwinger functions | `IMP`, open in target theory | Tightness or stronger compactness; uniqueness or controlled subsequences; uniform renormalized bounds; regulator removal; infinite-volume control; identification of observables. | A formal path integral or an unidentified weak limit is not a constructed QFT. |
| Limiting Schwinger functions \(\to\) Minkowski/physical QFT | `IMP` under OS hypotheses | Euclidean covariance, symmetry, reflection positivity, regularity/growth, cluster or vacuum conditions, and the precise OS reconstruction assumptions. | Euclidean invariance alone does not create a positive physical Hilbert space. |
| Minkowski Wightman theory \(\to\) Euclidean functions | `IMP` under spectral/analytic hypotheses | Positive energy, temperedness/regularity, locality and analytic continuation conditions. | A gauge-fixed indefinite-metric field theory does not automatically yield the required physical Wightman theory. |
| Physical spectral gap \(\to\) exponential clustering | `IMP` | Physical Hilbert space, centred suitable local observables, locality/spectral representation, and \(C<\Delta\). | This direction does not by itself prove the converse. |
| Exponential decay of selected Euclidean correlators \(\to\) physical spectral gap | `IMP` only after additional theorems | OS reconstruction; correct transfer semigroup; decay uniformity; observable class sufficiently rich to detect the bottom of the physical spectrum; vacuum-sector control. | Decay of one operator, one channel, or one regulator value is not the full mass-gap theorem. |
| Fixed-lattice transfer-matrix gap \(\to\) continuum physical gap | `OBS`, not an equivalence | Reflection positivity/transfer construction; volume-uniform lower bound; conversion to physical units; cutoff-uniform scaling; convergence of the reconstructed generators/spectra. | A positive dimensionless lattice gap may vanish after multiplication by the inverse physical correlation length or after \(a\to0\). |
| Finite-volume gap \(\to\) infinite-volume gap | `OBS`, not automatic | Lower bound uniform in volume and convergence preserving the relevant spectral exclusion. | Discrete finite-volume spectrum is generic and does not establish a thermodynamic mass gap. |
| Area law \(\leftrightarrow\) confinement | Model- and definition-dependent | Precise Wilson-loop, charge-sector, and limit definitions. | Neither phrase may be substituted for the Clay spectral-gap theorem. |
| Confinement \(\to\) mass gap | `EXC` as a general unqualified inference | Additional model-specific hypotheses would be required. | Confinement and mass gap are distinct official objectives. |
| Isolated one-particle state \(\to\) mass gap | `IMP` only with vacuum separation and positive particle mass | Physical particle state, isolation, lower spectral control. | The Clay problem does not require proof of an isolated one-particle pole; Jaffe–Witten list it as an extension. |
| Perturbative asymptotic freedom \(\to\) nonperturbative existence | `EXC` | No general implication. | Renormalized perturbation theory alone does not construct the full theory. |

### 7.3 Non-circularity rule

A route is circular if it uses, explicitly or through an imported theorem, any of the following to prove the gap while those same statements depend on an already established gap:

- exponential clustering with a rate already identified as a spectral mass;
- thermodynamic uniqueness proved using a uniform transfer-matrix gap;
- reconstruction estimates whose constants presuppose infrared exponential decay;
- a continuum scaling limit selected by fixing a correlation length whose positivity is the desired conclusion.

Every later Work Package must publish a dependency graph sufficient to expose such cycles.

---

## 8. Mass-gap normalization ledger

The symbol “gap” is reserved only with a qualifier until physical reconstruction is complete.

| Term | Definition | Evidentiary status |
|---|---|---|
| **Fixed-lattice transfer gap** | Separation in the spectrum of a transfer operator at fixed lattice spacing \(a\) and specified spatial volume. | Regulated evidence only. |
| **Finite-volume Hamiltonian gap** | Difference between vacuum and first excitation for a Hamiltonian in a finite box/torus. | Insufficient without volume uniformity. |
| **Volume-uniform regulated gap** | Lower bound independent of spatial volume at fixed regulator. | Potential input to infinite-volume construction; not yet continuum gap. |
| **Cutoff-uniform physical gap** | Lower bound, expressed in fixed physical units, that persists as ultraviolet regulator is removed. | Candidate bridge to physical theorem. |
| **Euclidean inverse correlation length** | Exponential decay rate for specified connected Euclidean correlators. | Operator- and channel-dependent until reconstruction and completeness are proved. |
| **Physical Hamiltonian mass gap** | \(\operatorname{spec}(H)\cap(0,\Delta)=\varnothing\) in the reconstructed physical Hilbert space. | Required target. |
| **Isolated one-particle mass** | Isolated mass-shell or spectral eigenvalue above the vacuum. | Stronger/different adjacent target; not required by the base problem. |

### 8.1 Scaling warning

For a lattice spacing \(a\), a dimensionless transfer gap \(\delta(a)\) does not yield a positive continuum mass merely because \(\delta(a)>0\) for every \(a>0\). One needs a physical normalization and a proved limit or lower bound such as

\[
\inf_{a\le a_0}\frac{\delta(a)}{a}>0
\]

in the relevant convention, together with all reconstruction and volume hypotheses. The exact scaling formula depends on the transfer normalization; it must be derived, not assumed.

---

## 9. Exclusion ledger

The following are explicitly insufficient as standalone solutions:

| ID | Excluded substitution | Reason |
|---|---|---|
| `YM-X01` | Classical Yang–Mills global existence or regularity | The challenge concerns an interacting quantum field theory. |
| `YM-X02` | Perturbative renormalizability or beta-function calculation | Formal/asymptotic expansions do not construct the nonperturbative theory. |
| `YM-X03` | A formal Euclidean path integral | Measure existence, regulator removal, positivity, locality, and reconstruction remain unproved. |
| `YM-X04` | A positive gap at one lattice spacing | It may vanish under continuum scaling. |
| `YM-X05` | A finite-volume spectral gap | Finite boxes generally have discrete spectra; the bound may collapse as volume grows. |
| `YM-X06` | Strong-coupling cluster expansion alone | The physical continuum limit lies at a critical scaling regime; continuation and uniform estimates require proof. |
| `YM-X07` | Numerical glueball masses or Monte Carlo exponential decay | Numerical evidence does not prove exact existence, OS reconstruction, or a universal spectral exclusion. |
| `YM-X08` | Gauge-fixed construction in an indefinite metric | Physical positivity and the gauge-invariant Hilbert-space sector must be recovered. |
| `YM-X09` | Confinement or Wilson-loop area-law heuristic | Confinement and spectral mass gap are distinct claims. |
| `YM-X10` | Large-\(N\), supersymmetric, lower-dimensional, or Abelian analogue | Such models may guide mechanism discovery but do not solve the universally quantified four-dimensional pure non-Abelian problem. |
| `YM-X11` | Weak compactness plus an unidentified subsequential limit | The limit must be identified, nontrivial, axiomatic, and gapped. |
| `YM-X12` | Mass gap for a selected observable channel | The physical spectral bottom must be excluded across the complete observable sector. |

---

## 10. Semantic hazard register

The campaign treats these distinctions as binding:

\[
\text{classical existence}\ne\text{quantum existence},
\]

\[
\text{perturbative renormalizability}\ne\text{nonperturbative construction},
\]

\[
\text{finite-lattice gap}\ne\text{continuum physical mass gap},
\]

\[
\text{confinement}\ne\text{mass gap},
\]

\[
\text{gauge-fixed auxiliary positivity}\ne\text{physical Hilbert-space positivity},
\]

\[
\text{exponential decay in one channel}\ne\text{full spectral exclusion}.
\]

Any document that suppresses one of these distinctions incurs claim-boundary debt and cannot be promoted.

---

## 11. Formal proposition schemas

These schemas are not proofs. They define the shape of later formal obligations.

### 11.1 Reconstruction schema

Let \(\mathcal S=\{S_n\}_{n\ge0}\) be a hierarchy of gauge-invariant Euclidean Schwinger distributions. A reconstruction artifact must state and prove:

```text
OSProfile(S)
  -> exists (H, Omega, U, Phi)
       PhysicalQFT(H, Omega, U, Phi)
       and Reconstructs(Phi, S).
```

`OSProfile` must expand into explicit axioms rather than remain an opaque imported predicate.

### 11.2 Gap schema

```text
PhysicalQFT(H, Omega, U, Phi)
  and VacuumGroundState(H, Omega)
  and SpectrumExcluded(H, 0, Delta)
  and Delta > 0
  and Delta < infinity
  -> PhysicalMassGap(H, Omega, Delta).
```

### 11.3 Regulator-survival schema

For regulated Hamiltonians \(H_{a,L}\):

```text
UniformGapPhysicalUnits(H_{a,L}, Delta0)
  and ThermodynamicConvergence(H_{a,L}, H_a)
  and ContinuumConvergence(H_a, H)
  and SpectralExclusionStableUnderLimits(...)
  -> SpectrumExcluded(H, 0, Delta0).
```

Each convergence predicate must specify topology and domain control. Strong-resolvent convergence alone, for example, does not automatically preserve every desired spectral gap without additional hypotheses.

---

## 12. Claim-level trust matrix

| Claim | Type | Support | Trust state |
|---|---|---|---|
| The official target quantifies over every compact simple \(G\). | `SRC` | `SRC-YM-00`, §4 | Verified |
| The target requires a nontrivial theory on \(\mathbb R^4\). | `SRC` | `SRC-YM-00`, §4 | Verified |
| The mass gap is a spectral exclusion for the physical Hamiltonian above the vacuum. | `SRC` | `SRC-YM-00`, §4 | Verified |
| The axiomatic floor is at least as strong as the cited Wightman and OS schemes. | `SRC` | `SRC-YM-00`, §§3–4 and refs. [35], [45] | Verified |
| Local gauge-invariant curvature observables and UV concordance belong to the intended existence obligation. | `SRC` | `SRC-YM-00`, §4 | Verified |
| A mass gap implies exponential clustering for suitable centred local observables. | `IMP` | `SRC-YM-00`, §5 | Verified in stated direction |
| Exponential decay of arbitrary selected correlators is equivalent to the full physical mass gap. | `EQV` | No unconditional source route | Rejected |
| A finite-volume or fixed-lattice gap solves YM-M. | `IMP` | No valid route | Rejected |
| Confinement is identical to the mass-gap statement. | `EQV` | Contradicted by official separation of objectives | Rejected |
| The challenge is currently solved. | `SRC` | `SRC-YM-01` | Rejected; remains open |

---

## 13. Eight-role internal review

This is a documented **internal adversarial review by role**, not an external peer review and not a substitute for repository maintainers or independent experts.

### 13.1 Axiomatist

**Question:** Does the artifact preserve the cited axiomatic floor and distinguish Euclidean construction from physical reconstruction?

**Finding A1 — major, resolved:** An early formulation risked treating reflection positivity as the whole OS package. The text now requires the complete reconstruction profile, including regularity, covariance, symmetry, vacuum/cluster conditions, and the corrected OS formulation.

**Finding A2 — major, resolved:** Gauge-fixed fields could have been mistaken for physical fields. The physical gauge-invariant observable sector and positive Hilbert space are now explicit.

**Verdict:** `PASS`.

### 13.2 Cartographer

**Question:** Are all representation changes and limiting operations exposed as typed arrows?

**Finding C1 — major, resolved:** “Lattice theory → Yang–Mills theory” was too coarse. It is now decomposed into regulator limits, Schwinger-hierarchy identification, OS reconstruction, Hamiltonian generation, and spectral exclusion.

**Finding C2 — minor, resolved:** The route now distinguishes one-way implications from equivalences and exclusions.

**Verdict:** `PASS`.

### 13.3 Grammarian

**Question:** Are quantifiers, modality, and overloaded terms controlled?

**Finding G1 — major, resolved:** “For compact simple \(G\)” is normalized as universal quantification, not selection of a convenient example.

**Finding G2 — minor, resolved:** “Gap” is prohibited without a qualifier before physical reconstruction.

**Finding G3 — minor, resolved:** “Should” clauses in the official description are classified rather than silently discarded.

**Verdict:** `PASS`.

### 13.4 Verifier

**Question:** Are source-dependent claims traceable to exact authoritative locations?

**Finding V1 — major, resolved:** The theorem, gap definition, local-observable requirement, clustering statement, and finite-volume warning now point to Jaffe–Witten §§4–5.

**Finding V2 — minor, resolved:** The two Osterwalder–Schrader papers are recorded separately with verified volume, pages, year, and DOI.

**Finding V3 — retained note:** Any later claim about a modern theorem, numerical result, or constructive partial result requires a new primary-source audit; this WP00 does not inventory the entire post-2000 literature.

**Verdict:** `PASS` for source normalization; literature atlas deferred to a later authorized Work Package.

### 13.5 Adversary

**Question:** Can a false solution pass by exploiting semantic shortcuts?

**Finding D1 — critical, resolved:** A positive finite-lattice gap can collapse in physical units as \(a\to0\). The cutoff-uniform scaling obligation is explicit.

**Finding D2 — critical, resolved:** Finite-volume discreteness can masquerade as a mass gap. Volume uniformity is explicit.

**Finding D3 — major, resolved:** Confinement, area law, glueball numerics, and one-channel exponential decay are blocked as substitutes.

**Finding D4 — major, resolved:** Weak subsequential existence without identification, nontriviality, axioms, and gap is excluded.

**Verdict:** `PASS`.

### 13.6 Formalist

**Question:** Can the obligation structure be translated into checkable propositions without hidden predicates?

**Finding F1 — major, resolved:** Reconstruction, mass-gap, and regulator-survival proposition schemas have been added.

**Finding F2 — retained obligation:** No theorem prover encoding is attempted at WP00. Future formalization must expand `OSProfile`, convergence modes, domains, and spectral-stability hypotheses.

**Verdict:** `PASS` for formalizability audit; no certification claim.

### 13.7 Amanuensis

**Question:** Are terminology, source IDs, claim types, and review provenance internally consistent?

**Finding M1 — minor, resolved:** Source and obligation IDs are unique and stable.

**Finding M2 — minor, resolved:** “Minkowski \(\mathbb R^{1,3}\)” and Euclidean \(\mathbb R^4\) are distinguished while respecting the official statement’s notation.

**Finding M3 — retained note:** Version 0.1.0 should remain immutable after promotion; corrections should increment the version and append a change record.

**Verdict:** `PASS`.

### 13.8 Referee

**Question:** Is the artifact complete enough to govern subsequent Yang–Mills work without overstating mathematical progress?

**Assessment:**

- object: explicit;
- obstruction: explicit;
- claim boundary: explicit;
- next move: explicit;
- source route: authoritative and traceable;
- equivalence graph: typed;
- principal false inferences: blocked;
- open theorem obligations: not disguised as results;
- internal review provenance: recorded.

**Referee verdict:** `PROMOTION ELIGIBLE AS YM-WP00`.

This verdict promotes only the source-normalization and equivalence-control artifact. It does not promote any existence theorem, gap theorem, or mechanism claim.

---

## 14. Promotion conditions

Promotion of this artifact requires all of the following:

- [x] Canonical Clay/Jaffe–Witten statement recorded.
- [x] Wightman and Osterwalder–Schrader source floor identified.
- [x] Quantifiers, spacetime, field content, observables, vacuum, and gap normalized.
- [x] Existence and mass-gap trunks separated but jointly required.
- [x] Regulator, reconstruction, and spectral arrows typed.
- [x] Finite-volume and fixed-lattice gaps distinguished from the physical gap.
- [x] Exclusion ledger published.
- [x] Claim-level trust matrix published.
- [x] Axiomatist review passed.
- [x] Cartographer review passed.
- [x] Grammarian review passed.
- [x] Verifier review passed.
- [x] Adversary review passed.
- [x] Formalist review passed.
- [x] Amanuensis review passed.
- [x] Referee issued a bounded promotion verdict.
- [ ] Repository review completed and artifact merged to the protected branch.

Until the final repository condition is satisfied, status remains `PROMOTION ELIGIBLE`, not `PROMOTED`.

---

## 15. Next move

The next eligible work may be authorized only after repository promotion of WP00.

The natural successors are:

- **YM-WP01 — False-proof atlas:** catalogue recurrent invalid routes, hidden circularities, regulator-limit failures, gauge-positivity failures, and confinement/gap conflations.
- **YM-WP02 — Source-normalized theorem ledger:** inventory rigorous partial results by dimension, gauge group, regulator, volume, coupling regime, axiom profile, and gap notion.

These may proceed in parallel after WP00 promotion. Mechanism generation, numerical experimentation, and restricted-target selection remain gated until their source and theorem ledgers exist.

---

## 16. Change record

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-24 | Initial source, normalization, equivalence, exclusion, trust-matrix, and eight-role review artifact. |
