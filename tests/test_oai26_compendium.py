"""OAI-26 source/claim-boundary checks (no theorem validation)."""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))
import oai26_compendium as c


class DocumentaryCatalogueTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogue = c.load_catalogue()

    def test_exact_source_coverage_and_noncontiguous_ids(self):
        f = self.catalogue["families"]
        self.assertEqual(len(f), 372)
        self.assertEqual(sum(len(x["manuscripts"]) for x in f), 719)
        ids = {x["family_id"] for x in f}
        self.assertEqual(f[0]["family_id"], "001")
        self.assertEqual(f[-1]["family_id"], "377")
        self.assertEqual({f"{n:03d}" for n in range(1, 378)} - ids,
                         {"045", "061", "070", "123", "163"})

    def test_source_lock_stale_rejected(self):
        j = copy.deepcopy(self.catalogue)
        j["source_lock"] = "0"*40
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "catalogue.json"
            p.write_text(json.dumps(j), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "source revision drift"):
                c.load_catalogue(p)

    def test_duplicate_path_rejected(self):
        j = copy.deepcopy(self.catalogue)
        j["families"][1]["manuscripts"][0]["pdf_path"] = j["families"][0]["manuscripts"][0]["pdf_path"]
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "catalogue.json"
            p.write_text(json.dumps(j), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unique paths"):
                c.load_catalogue(p)

    def test_missing_family_and_unsafe_path_rejected(self):
        j = copy.deepcopy(self.catalogue)
        j["families"][1]["family_id"] = j["families"][0]["family_id"]
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "catalogue.json"
            p.write_text(json.dumps(j), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicated"):
                c.load_catalogue(p)
        j = copy.deepcopy(self.catalogue)
        j["families"][0]["manuscripts"][0]["pdf_path"] = "preprints/../else.pdf"
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "catalogue.json"
            p.write_text(json.dumps(j), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unsafe"):
                c.load_catalogue(p)

    def test_authored_drafts_have_six_sections(self):
        for n in ("001", "003", "342", "376"):
            draft = (c.EDITORIAL / (n + ".md")).read_text(encoding="utf-8")
            c.validate_draft(draft, n)
            with self.assertRaises(ValueError):
                c.validate_draft(draft.replace(c.SECTIONS[1], ""), n)

    def test_admission_fail_closed(self):
        j = json.loads(c.ADMISSIONS.read_text(encoding="utf-8"))
        self.assertEqual(j["admissions"], [])
        row = dict(family_id="003", manuscript_sha256="0"*64,
                   source_audit_url="https://github.com/grandchallenge/MATHFORGE/issues/332",
                   critic_evidence_url="https://github.com/grandchallenge/MATHFORGE/issues/333",
                   protected_admission_url="https://github.com/grandchallenge/MATH-PROGRAMME/issues/2850")
        j["admissions"].append(row)
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "admissions.json"
            p.write_text(json.dumps(j), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "stale editorial manuscript hash"):
                c.build(output_dir=Path(td)/"oai26", admissions_path=p)

    def test_complete_generation_and_cleanup(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "oai26"
            stats = c.build(output_dir=out)
            self.assertEqual(stats, dict(families=372, manuscript_paths=719,
                                         editorial_drafts=4, editorially_admitted=0,
                                         reference_only=368, generated_pages=373))
            self.assertEqual(len(list((out / "families").glob("*.md"))), 372)
            self.assertTrue((out / "families/377.md").exists())
            for n in ("003", "342", "376"):
                page = (out / "families" / (n+".md")).read_text(encoding="utf-8")
                self.assertIn("DRAFT_UNACCEPTED", page)
                self.assertIn("NO_CERTIFICATION", page)
            ref = (out / "families/002.md").read_text(encoding="utf-8")
            self.assertIn("REFERENCE_ONLY", ref)
            self.assertIn("FAMILY_SEMANTICS_UNREVIEWED", ref)
            self.assertIn("NO_CERTIFICATION", ref)
            c.clean(out)
            self.assertFalse((out / "catalogue.md").exists())
            self.assertFalse((out / "families").exists())


if __name__ == "__main__":
    unittest.main()
