# YM-001 Accessible Research Guide

!!! info "Research surface authority"
    **LIVE:** [YM-001 canonical tracker #164](https://github.com/grandchallenge/MATH-PROGRAMME/issues/164), with historical, **closed** contribution returns [MATHSOLVE #716](https://github.com/grandchallenge/MATHSOLVE/issues/716), [#717](https://github.com/grandchallenge/MATHSOLVE/issues/717), and [#718](https://github.com/grandchallenge/MATHSOLVE/issues/718). These returns are not active child controllers.  
    **AUTHORITY:** `YM-WP00-source-normalization-equivalence-audit.md` and `governance/governed_campaign_registry.json`.  
    **EXPOSITION:** this guide explains protected state; it does not promote or certify mathematics.

## 1. Status

Yang–Mills existence and mass gap remain open. GCL has a promoted source-normalized baseline, an executable false-proof layer, a theorem/dependency ledger, and bounded source-completeness work. No protected record constructs the full four-dimensional theory or proves the physical mass gap.

## 2. Plain object

The theorem has two inseparable trunks: construct the interacting four-dimensional continuum theory with the required axiomatic/reconstruction properties, and prove a strictly positive finite spectral gap above the vacuum.

## 3. Current obstruction

The present residual is not merely ultraviolet control. Protected work recognizes bounded four-dimensional UV/large-field input, but the route still requires infrared/infinite-volume removal, uniqueness or full continuum identification, complete Osterwalder–Schrader reconstruction, and physical scale identification before a mass-gap theorem can be claimed.

## 4. Working model

Programme state is routed through the exact theorem/dependency obligations rather than broad mechanism generation. The D003 line has been narrowed by source reconstruction and adversarial proof-completeness review; downstream work must state the function-space/topological framework, convergence domain, uniformity, Slavnov-identity passage, and regulator/IR interpretation needed by the intended theorem.

## 5. Restricted claim

Protected records may be used as bounded source and theorem-interface inputs only. They do not establish Yang–Mills existence, a mass gap, confinement, an area law, or regulator-independent continuum control.

## 6. Theorem-spine location

Programme authority:
- `YM-WP00-source-normalization-equivalence-audit.md`
- `governance/governed_campaign_registry.json`

LIVE coordination:
- Programme #164 (canonical campaign mirror; current open-theorem work must be read from the protected Solve handoff)
- MATHSOLVE #716–#718 (closed historical D003 contribution returns; not new active work)

## 7. Debt audit

Open debt includes the full continuum/reconstruction bridge, theorem-grade convergence on the downstream-required domain, uniformity sufficient for a Schwinger hierarchy, preservation of Slavnov identities in the limit, and the physical mass-gap implication.

## 8. Claim boundary

Issue closure, source discovery, replay, numerical evidence, or this guide cannot create mathematical or certification authority. MATHCERT remains the certification surface.

## 9. First executable step

Read #164, then re-fetch the current protected Solve handoff for the smallest surviving D003 proof-completeness node. Work only against protected source locks and return an exact theorem, falsification, or blocker.

## Reader entry and prerequisites

**Status:** open existence-and-mass-gap target, protected source/theorem interfaces only. **Audience:** graduate mathematical physics readers, source auditors, and proof-completeness reviewers. **Time to first example:** 10 minutes. **Time to first fixture:** 10 minutes.

| Level | Concepts |
| --- | --- |
| Required | Matrices, eigenvalues, limits of real sequences |
| Helpful | Hilbert spaces, spectra, positive operators |
| Deferred | Gauge fields, constructive QFT, Osterwalder–Schrader reconstruction and Slavnov identities |

## Core bridge and first examples by hand

**Friendly example:** the finite Hermitian matrix \(H=\operatorname{diag}(0,2)\) has vacuum energy 0 and first excited energy 2. Its finite spectral gap is exactly 2.

**Obstruction example:** the sequence \(H_n=\operatorname{diag}(0,1/n)\) has a positive gap for each finite \(n\), but the gaps tend to zero. Thus showing positivity **at every regulator** does not establish a strictly positive limiting physical gap. Neither matrix is a model of the actual four-dimensional Yang–Mills theory.

Bridge: finite spectrum → regulator-dependent gap → absence of uniform lower bound → continuum/OS reconstruction and positive physical gap as separate theorem obligations.

## First computation or fixture

Python 3 exact rational toy gap experiment:

```python
from fractions import Fraction
for n in (1, 2, 5, 10):
    gap = Fraction(1, n)
    print(n, gap)
# Expected: (1,1), (2,1/2), (5,1/5), (10,1/10), printed as separate rows
```

Input \(n\); operation reads the nonzero eigenvalue of a two-dimensional diagonal matrix; output is exact rational arithmetic. **Support route:** elementary regression fixture. **Limitation:** no continuum, interacting QFT or Yang–Mills evidence.

## First theorem or local proposition

**Vanishing-gap lemma.** For \(H_n=\operatorname{diag}(0,1/n)\), every finite \(H_n\) has positive spectral gap but \(\inf_n\operatorname{gap}(H_n)=0\). Proof: for any \(\varepsilon>0\), choose an integer \(n>1/\varepsilon\). This demonstrates why a regulator-independent bound is a separate analytic requirement; it cannot substitute for the full theory existence axioms.

## Challenge ladder

| Stage | Duty | Completion test |
| --- | --- | --- |
| Exercise | Find the eigenvalues of \(H=\operatorname{diag}(0,2)\) | 0 and 2 |
| Exploration | Derive the finite \(H_n\) gaps | \(1/n\) |
| Fixture | Execute rational checker | Match all four values |
| Lemma candidate | Prove vanishing-gap lemma | Quantified \(\varepsilon\) argument |
| Open direction | Trace one D003 theorem-grade convergence dependency | Name topology/domain/uniformity needed by actual downstream statement |

## Certification path and continuation graph

The finite-matrix lemma is independently provable but not a YM certificate. Native Solve proof-completeness work must source-lock the actual continuum/OS/Slavnov statements and preserve its function-space, IR, regulator and uniformity conditions before any Cert handoff.

`matrix fixture → uniform-gap obstruction → exact D003 source theorem → continuum/OS convergence bridge [OPEN] → physical-spectrum construction → Cert [not yet eligible]`

## Trust quartet

**Proved:** elementary vanishing-gap lemma, and only bounded source claims protected by GCL. **Checked:** rational matrix fixture and closed historical D003 returns. **Open:** construction, full reconstruction, spectral gap. **External verification:** convergence and reconstruction in actual primary sources, not the finite toy model.

## Bibliography and source audit

| Source | Role | Audit state |
| --- | --- | --- |
| [YM WP00 source audit](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/YM-WP00-source-normalization-equivalence-audit.md) | Canonical Clay target and axiomatic floor | Protected Programme authority |
| [D003 UV/large-field supplement](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/campaigns/yang_mills/YM_D003_UV_LARGE_FIELD_SUPPLEMENT.json) | Bounded source context | Protected, not terminal bridge |
| Jaffe–Witten; Osterwalder–Schrader; Balaban / MRS sources (locked in protected ledger) | Imported theorem dependencies | Exact source scope and proof completeness remain controlling |

**First executable step / completion test:** Reproduce the finite counterexample and identify one actual missing D003 implication with named domain, topology, uniformity estimate and source identity; do not infer a physical mass gap from the toy sequence.

