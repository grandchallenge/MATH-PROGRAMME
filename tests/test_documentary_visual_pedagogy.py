from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))
from validate_documentary_visual_pedagogy import AUDIT_PATH, SCHEMA_PATH, audit_inventory, git_blob_sha, load_json, visual_pedagogy_errors  # noqa: E402

class DocumentaryVisualPedagogyTests(unittest.TestCase):
    def test_live_visual_pedagogy_contract_is_closed(self): self.assertEqual([], visual_pedagogy_errors(ROOT))
    def test_audit_counts_and_positive_controls(self):
        audit=load_json(ROOT/AUDIT_PATH); inventory=audit_inventory(audit)
        self.assertEqual(45,len(inventory)); self.assertEqual(8,len(audit["reference_pilot"]["selected"]))
        dispositions={x["disposition"] for x in audit["reference_pilot"]["selected"]}
        self.assertIn("KEEP",dispositions); self.assertTrue({"REDRAW","REPLACE"}&dispositions)
    def test_predecessor_git_identity_is_bound(self):
        audit=load_json(ROOT/AUDIT_PATH); inv={x["asset"]:x for x in audit_inventory(audit)}; rel="docs/assets/documentaries/p_vs_np/reduction.svg"
        self.assertEqual(inv[rel]["blob_sha"],git_blob_sha(ROOT/rel))
    def test_schema_rejects_visual_evidence_promotion(self):
        v=Draft202012Validator(load_json(ROOT/SCHEMA_PATH)); c=load_json(ROOT/"governance/visual_pedagogy/plates/PNP-REDUCTION-PLATE-II.json"); m=copy.deepcopy(c); m["claim_boundary"]["visual_is_evidence"]=True; self.assertTrue(list(v.iter_errors(m)))
    def test_all_pilot_contracts_bind_completed_independent_review(self):
        audit=load_json(ROOT/AUDIT_PATH); selected={x["asset"] for x in audit["reference_pilot"]["selected"]}; bound={}
        for p in (ROOT/"governance/visual_pedagogy/plates").glob("*.json"):
            c=load_json(p); paths={d["path"] for d in c.get("derivatives",[]) if d.get("path")}; predecessor=c.get("predecessor")
            if predecessor: paths.add(predecessor)
            matched=paths&selected
            self.assertLessEqual(len(matched),1,p.name)
            if matched: bound[next(iter(matched))]=c
        self.assertEqual(selected,set(bound)); self.assertEqual(8,len(bound)); self.assertTrue(all(c["independent_review"]["status"]=="reviewed" and c["independent_review"]["evidence_refs"] for c in bound.values()))
    def test_rejected_svg_candidate_git_blobs_remain_historical(self):
        m=load_json(ROOT/"governance/visual_pedagogy/successor_render_manifest.json")
        for o in m["outputs"]:
            self.assertEqual(o["git_blob"],git_blob_sha(ROOT/o["path"]),o["path"])
            if "print_path" in o: self.assertEqual(o["print_git_blob"],git_blob_sha(ROOT/o["print_path"]))
    def test_rejected_bsd_svg_renderer_still_reproduces_historical_candidate(self):
        renderer=ROOT/"tools/render_visual_pedagogy_successors.py"
        compile(renderer.read_text(encoding="utf-8"),str(renderer),"exec")
        with tempfile.TemporaryDirectory() as td:
            subprocess.run([sys.executable,str(renderer)],cwd=td,check=True)
            made=Path(td)/"governance/visual_pedagogy/review_candidates/bsd/plate_curve_successor.svg"
            expected=ROOT/"governance/visual_pedagogy/review_candidates/bsd/plate_curve_successor.svg"
            self.assertEqual(expected.read_bytes(),made.read_bytes())
            self.assertEqual("ec72146f47f9d9356d3a697440bedb73a1f7c1692d79e29aea41e653e3aee6ed",hashlib.sha256(made.read_bytes()).hexdigest())
    def test_review_candidates_are_not_live_documentary_assets(self):
        repair=load_json(ROOT/"governance/visual_pedagogy/representation_repair_manifest.json")
        for o in repair["outputs"]:
            for d in o["derivatives"]: self.assertTrue(d["path"].startswith("governance/visual_pedagogy/review_candidates/"))
        forbidden=[ROOT/"docs/assets/documentaries/poincare/plate_geometry_successor.png",ROOT/"docs/assets/documentaries/poincare/plate_surgery_successor.png",ROOT/"docs/assets/documentaries/riemann/critical_strip_successor.png",ROOT/"docs/assets/documentaries/navier_stokes/vorticity_stretching_successor.png",ROOT/"docs/assets/documentaries/bsd/plate_curve_successor.png",ROOT/"docs/assets/documentaries/hodge/cycle_class_successor.png"]
        self.assertTrue(all(not p.exists() for p in forbidden))
    def test_pc001_quality_reference_is_bound_and_non_authoritative(self):
        q=load_json(ROOT/"governance/visual_pedagogy/quality_reference_pc001.json")
        self.assertEqual("0e1499ee13a6966a3b190b850b6acd2db647952826c54b3abc575d607a2f6ea4",q["repository_identity"]["rendered_pdf_sha256"]); self.assertFalse(q["authority_boundary"]["reference_is_proof_authority"]); self.assertEqual({f"VQ-{i:02d}" for i in range(1,9)},{x["id"] for x in q["binding_quality_principles"]})
    def test_representation_repair_manifest_binds_current_pngs(self):
        m=load_json(ROOT/"governance/visual_pedagogy/representation_repair_manifest.json")
        self.assertEqual("REJECTED_REPRESENTATION_LAYER_INADEQUATE",m["review_rejection"]["disposition"])
        self.assertFalse(m["authority_boundary"]["visual_is_evidence"])
        self.assertEqual(6,len(m["outputs"]))
        refs=[m["review_entry"]]+[d for o in m["outputs"] for d in o["derivatives"]]
        self.assertEqual(8,len(refs))
        for item in refs:
            p=ROOT/item["path"]
            self.assertTrue(p.is_file(),item["path"])
            self.assertEqual(item["sha256"],hashlib.sha256(p.read_bytes()).hexdigest(),item["path"])
    def test_current_corrective_contracts_use_raster_derivatives(self):
        plate_ids={"PC-RICCI-FLOW-PLATE-II","PC-SURGERY-PLATE-III","RH-CRITICAL-STRIP-PLATE-II","NS-VORTICITY-PLATE-II","BSD-CURVE-PLATE-I","HC-CYCLE-CLASS-PLATE-III"}
        contracts={c["plate_id"]:c for c in [load_json(p) for p in (ROOT/"governance/visual_pedagogy/plates").glob("*.json")]}
        for pid in plate_ids:
            c=contracts[pid]
            self.assertTrue(all(d["format"]=="png" for d in c["derivatives"]),pid)
            self.assertTrue(all(d["path"].endswith(".png") for d in c["derivatives"]),pid)
            self.assertTrue(c["renderer"]["reproducible"],pid)
            self.assertEqual("governance/visual_pedagogy/representation_repair_manifest.json",c["renderer"]["parameters_ref"])
        self.assertEqual("data-derived",contracts["RH-CRITICAL-STRIP-PLATE-II"]["representation_class"])
    def test_review_gallery_points_to_representation_repair_pngs(self):
        gallery=(ROOT/"governance/visual_pedagogy/review_candidates/README.md").read_text(encoding="utf-8")
        self.assertIn("contact_sheet.png",gallery)
        self.assertIn("plate_geometry_successor.png",gallery)
        self.assertIn("critical_strip_successor.png",gallery)
        self.assertNotIn("![Ricci-flow geometry candidate](poincare/plate_geometry_successor.svg)",gallery)
    def test_raster_renderer_source_is_syntactically_valid(self):
        renderer=ROOT/"tools/render_visual_pedagogy_raster_successors.py"
        compile(renderer.read_text(encoding="utf-8"),str(renderer),"exec")

if __name__ == "__main__": unittest.main()
