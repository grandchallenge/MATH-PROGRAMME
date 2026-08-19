# Amanuensis continuity record — MP-DOC-VISUAL-PEDAGOGY-001

Status: proposed final bounded-pilot continuity record under issue #410. It becomes protected pilot-closure evidence only after independent review, protected merge, and terminal post-merge readback.

## Authority chain

- Parent docket: #377, `MP-DOC-VISUAL-PEDAGOGY-001`.
- Governing Council disposition: `VISUAL_PEDAGOGY_REFORM_APPROVED_FOR_BOUNDED_PILOT`.
- Governance/contract protected merge: PR #380 → `3b79b35fadc6805775246c03124deb3e1425ef86`.
- Corrective successor operation: #386 / PR #389.
- Final reviewed representation-repair head: `603a0df8f40797dbf0ec75c53ac4144b70458eba`.
- Protected successor merge: `50f2b4d975b96ab34e26b14192ff635045170cf0`.

No item in this chain authorizes programme-wide visual migration or promotes a mathematical claim.

## Review history preserved without erasure

The first SVG-only corrective realization failed independent review. Review `4901258988` returned `CHANGES_REQUESTED` with the finding that the SVG plates did not carry sufficient pedagogical detail. The review was submitted against commit `9a569bc935e9002436818ee06ffb106907fcc786`; superseded freeze comment `5240440397` separately preserves the earlier `ad38c4352121c2e7170d56eb02f1bf52356e19d3` freeze record. Neither record is rewritten or dismissed.

The response was a representation-layer repair, not an SVG-detail patch. PR #389 then froze exact head `603a0df8f40797dbf0ec75c53ac4144b70458eba` in comment `5248330492`. Reviewer `jimsteeg` recorded the reservation that pedagogy should continue to improve in review `4901948990`, and subsequently submitted exact-head `APPROVED` review `4902525377` against `603a0df8f40797dbf0ec75c53ac4144b70458eba`.

Human Steward exact-head merge authorization was posted as comment `5248393712`. Protected merge execution produced `50f2b4d975b96ab34e26b14192ff635045170cf0`, followed by terminal protected post-merge validation. The historical rejection remains part of the accepted provenance of the final pilot.

## Eight-case identity continuity

| Plate | Audit disposition | Protected predecessor/control identity | Reviewed bounded-pilot realization |
|---|---|---|---|
| `PC-RICCI-FLOW-PLATE-II` | `REPLACE` | `docs/assets/documentaries/poincare/plate_geometry.svg` — git blob `d02d5650b002a2f5d47290f579f980a026462160` | `review_candidates/poincare/plate_geometry_successor.png` — sha256 `593cb7d7ef7fc31239cb19eb7991c6d0baf499101c2f89f5d672aa14cb23399a` |
| `PC-SURGERY-PLATE-III` | `REPLACE` | `docs/assets/documentaries/poincare/plate_surgery.svg` — git blob `b2eba493adf6fb8c976be088f06526718ec2a008` | primary sha256 `7c394188cdee145bf7d61f11185971ed958909a46115eb9adb320f9afbab5ece`; print sha256 `22a80c58cf43d67121b11502b0d587c9ddc94e9f7bf345b57cfc50697626f37f` |
| `RH-CRITICAL-STRIP-PLATE-II` | `REPLACE` | `docs/assets/documentaries/riemann/strip.svg` — git blob `6684dbd8281e2768e42084e8ef04c05eef794d15` | `review_candidates/riemann/critical_strip_successor.png` — sha256 `1231d3667a88e2f6c6473c50a1e255310c7345e65e91aba41cc5e9908ae52e8b` |
| `NS-VORTICITY-PLATE-II` | `REPLACE` | `docs/assets/documentaries/navier_stokes/vorticity.svg` — git blob `6391ea8cb891c2119fbc9c34d227e6debd9b87fb` | `review_candidates/navier_stokes/vorticity_stretching_successor.png` — sha256 `715c8dceec5b9ffbcaa615c83efbd8c1f3cb3bd83ae1fcf1cc4c70337abe316a` |
| `BSD-CURVE-PLATE-I` | `REDRAW` | `docs/assets/documentaries/bsd/plate_curve.svg` — git blob `88b010f956744a4303dfbfd04b9f95062dbdfe04` | `review_candidates/bsd/plate_curve_successor.png` — sha256 `971106fe6dba55335e707d4cb5c49a6ef32414ccd8d3ea2ffbe64c9e87cca13f` |
| `HC-CYCLE-CLASS-PLATE-III` | `REDRAW` | `docs/assets/documentaries/hodge/cycles.svg` — git blob `a89e4851b30ec7ac858da9f999328abed168eb90` | `review_candidates/hodge/cycle_class_successor.png` — sha256 `17c4d75f11f090220f4ee6caad3661cfbe28c60b3b3caa846c6d9e6b77d67245` |
| `PNP-REDUCTION-PLATE-II` | `KEEP` | `docs/assets/documentaries/p_vs_np/reduction.svg` — git blob `e351902a073e9fdb41d0953400992d1732fd0fd4` | same protected exact-SVG control |
| `EUCLID-ANTHYPHAIRESIS-PLATE-I` | `KEEP` | `docs/assets/documentaries/euclid_book_vii/plate_anthyphairesis.svg` — git blob `6bcddb97bcd31d99575cfbbe1f6698b9c6eb3cd1` | same protected exact-SVG control |

The canonical identity/digest authority for generated review candidates remains `governance/visual_pedagogy/representation_repair_manifest.json` and the individual plate contracts. This table is a continuity index, not an alternate authority source.

## Integration boundary

PR #389 deliberately admitted reviewed candidates and provenance machinery without silently replacing live documentary predecessors. The two exact SVG controls demonstrate that representation-first governance is not a rasterization rule. The six corrective cases demonstrate that geometric, analytic, dynamical, and arithmetic pedagogy may require 3D, raster, or hybrid representation.

Every plate retains `visual_is_evidence: false`. Rendering reproducibility, reviewer approval, and documentary promotion do not establish theorem truth, proof validity, numerical completeness, or certification authority.

## Pilot conclusion

The evidence supports broader use of the visual-pedagogy standard, but not an indiscriminate library rewrite. The recorded recommendation is:

`BROADER_VISUAL_PEDAGOGY_PROPAGATION_RECOMMENDED_AS_STAGED_GOVERNED_MIGRATION_WITH_RESERVATIONS`

The reservation is substantive: the reviewer explicitly asked that pedagogy continue to improve, and the pilot itself demonstrated that a semantically safe but representationally weak medium can fail. Any propagation operation should therefore preserve per-plate representation choice, independent review, provenance, accessibility, predecessor continuity, and claim-control gates.

This recommendation is not migration authority. A separate governed propagation operation and Human Steward disposition are required before changes extend beyond the bounded pilot.
