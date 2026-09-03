# GHOS estate membership sentinel — GCL-TCS candidate pilot

**Artifact:** `GHOS_ESTATE_MEMBERSHIP_SENTINEL`  
**Operation:** `GCL-TCS-PILOT-INSTITUTIONALIZATION-001`  
**Tracker:** `grandchallenge/MATH-PROGRAMME#788`  
**Primary profile:** `GCL-TCS-P05`  
**Secondary profile:** `GCL-TCS-P07`  
**Impact class:** `IC-2`  
**Authority status:** candidate  
**Promotion status:** in review

This package evaluates the protected detect-only GHOS estate-membership classifier against GCL-TCS-00. It does not change the classifier, admit a repository, modify terminal GHOS evidence, create a controller, change workflows/routing/protection, or authorize mathematical, certification, canonical-claim, publication, or external-claim state.

## Fixed source identity

- source: `ci/ghos_material_state_sentinel.py`
- protected source commit: `5bb3a91cca92b99bd97e60101934390a91f96103`
- source git blob: `ae860565d8b1769e0072bcebd9b0b92b2a3e8549`
- test source: `tests/test_ghos_material_state_sentinel.py`
- test git blob: `d6a1ffb0ee2f61fc43a4399b79864a580c9900a0`

## Candidate package

- `SOFTWARE_CONTRACT.md` — user-facing input/output, failure, compatibility, and trust boundary.
- `GHOS_ESTATE_MEMBERSHIP_SENTINEL.conformance.yaml` — candidate conformance declaration.
- `registries/TERMINOLOGY.yaml` — controlled terms/status tokens.
- `registers/CLAIMS.yaml` — bounded software communication claims and exclusions.
- `registers/EVIDENCE.yaml` — exact evidence links.
- `reviews/INTERNAL_G0_G7.yaml` — machine-assisted G0-G7 internal checks; explicitly not independent G8 review.
- `reviews/DEFERRED_G8_G9.yaml` — explicit deferred promotion/admission gates.
- `PILOT_OBSERVATIONS.yaml` — observed benefit, failure modes, burden, and ambiguity.

## Promotion boundary

G0-G7 internal checks do not create `CHECKED` or `ASSURED` conformance and do not satisfy G8 independence. Promotion requires a genuine non-author Referee disposition against the exact candidate material closure. G9 remains a separate atomic protected admission step after any valid G8 PASS.
