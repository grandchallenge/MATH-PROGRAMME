# VGSE-001 Accessible Research Guide

!!! info "Research surface authority"
    **LIVE:** [VGSE-001 canonical tracker #170](https://github.com/grandchallenge/MATH-PROGRAMME/issues/170).  
    **AUTHORITY:** `governance/vgse_bounded_admission_decision.json` and `governance/vgse_post_repin_closure.json`.  
    **EXPOSITION:** this guide explains the bounded successor route; it does not create certification authority.

## 1. Status

VGSE-001 has completed bounded Programme admission and downstream synchronization. The route remains active as `active_bounded_pending_cert_evidence`; MATHCERT is registered but cannot adjudicate because qualifying evidence is not yet protected.

## 2. Plain object

VGSE converts broad reconstruction questions into bounded successor mandates with explicit inputs, outputs, replay conditions, and claim boundaries.

## 3. Exact obstruction

The protected authority chain establishes route admission and synchronization, not the substantive target theorem. Certification remains blocked on new evidence satisfying the route contract.

## 4. Working model

Subsequent mechanical-semantics and identifiability-aware work must consume the protected bounded-admission state without inferring theorem truth from engineering completion.

## 5. Theorem-spine location

Authority:
- `governance/vgse_bounded_admission_decision.json`
- `governance/vgse_post_repin_closure.json`

LIVE coordination begins at tracker #170 and continues through the current successor issues named by the Programme route.

## 6. Debt audit

Open debt is evidence, not route activation: prove or falsify the bounded successor claims, preserve exact semantic interfaces, and produce a certification-ready evidence packet before adjudication.

## 7. Claim boundary

No substantive theorem or certification result is admitted by route activation, issue closure, or this guide.

## 8. First executable step

Read the latest protected successor record downstream of the post-repin closure, then execute the smallest active bounded mandate.

## Reader entry and prerequisites

**Status:** bounded route activated; substantive certification pending evidence. **Audience:** graduate geometry/engineering readers and verification contributors. **Time to first example:** 10 minutes. **Time to first fixture:** 10 minutes.

| Level | Concepts |
| --- | --- |
| Required | Two-dimensional coordinates, determinants, affine transformations |
| Helpful | Inverse problems, identifiability, constraint systems |
| Deferred | VGSE five-root geometry, mechanism semantics and protected formal interfaces |

## Core bridge and first examples by hand

A generic inverse problem asks whether measurements determine hidden parameters. The following affine-geometry toy models *identifiability*, not a VGSE theorem.

**Friendly example:** three source points \((0,0),(1,0),(0,1)\) determine an affine map from their three target images because they are not collinear.

**Failure example:** three collinear points \((0,0),(1,0),(2,0)\) leave the map's action in the vertical direction undetermined. This is exact non-identifiability. It makes no claim about five-root constructions, foldability, or mechanical feasibility.

Bridge: measured landmark positions → constraint matrix → rank → inverse uniqueness or ambiguity → specified protected successor target.

## First computation or fixture

Python 3 integer oriented-area determinant:

```python
def area2(p,q,r):
    return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
print(area2((0,0),(1,0),(0,1)))
print(area2((0,0),(1,0),(2,0)))
# Expected: 1 and 0, on separate lines
```

Inputs are the two landmark triples; operation computes twice signed triangle area. **Support route:** exact finite determinant regression. **Limitation:** not a simulation or proof of the protected VGSE mechanism.

## First theorem or local proposition

**Affine uniqueness lemma.** An affine map \(T(x)=Ax+b\) on \(\mathbb R^2\) is determined by its values on three noncollinear points: subtract the first image from the others; the two independent displacement vectors span \(\mathbb R^2\), determining \(A\), then \(b\). If the points are collinear, this argument fails. This is ordinary linear algebra.

## Challenge ladder

| Stage | Duty | Completion test |
| --- | --- | --- |
| Exercise | Compute the first determinant | 1 |
| Exploration | Change third point to \((2,0)\) | Determinant 0 |
| Fixture | Replay determinant script | Outputs 1 and 0 |
| Lemma candidate | Prove affine uniqueness | Use invertibility of two-vector basis |
| Open direction | Read current protected identifiability mandate | Name actual state variables, observation map and residual |

## Certification path and continuation graph

Toy affine uniqueness is directly provable. For VGSE, a certificate requires the real successor contract, supported geometry/semantics and an independently checked witness or theorem. Route activation and mechanical tests alone confer no certification.

`affine determinant fixture → inverse uniqueness lemma → exact VGSE state/observation mapping → source-specific injectivity or obstruction [OPEN] → Solve/Cert boundary`

## Trust quartet

**Proved:** affine uniqueness under noncollinearity. **Checked:** two determinants. **Open:** the substantive VGSE geometry/semantics and evidence for certification. **External verification:** protected successor mapping and any imported mechanical interpretation.

## Bibliography and source audit

| Source | Role | Audit state |
| --- | --- | --- |
| `governance/vgse_bounded_admission_decision.json` | Bounded admission contract | Protected operational authority |
| `governance/vgse_post_repin_closure.json` | Post-repin route consistency | Protected operational authority |
| [VGSE mechanical semantics mandate](../VGSE_MECHANICAL_SEMANTICS_MANDATE.md) | Successor learning/read-through | Not itself a geometric certificate |

**First executable step / completion test:** Replay both determinants, then extract from the protected successor one actual observation map, one identified ambiguity (if any), and its exact admissibility tests; return a bounded theorem, replay, or source-verified obstruction.

