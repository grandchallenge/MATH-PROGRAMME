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
        for n in ("001", "002", "003", "004", "005", "006", "007", "008", "342", "376"):
            draft = (c.EDITORIAL / (n + ".md")).read_text(encoding="utf-8")
            c.validate_draft(draft, n)
            with self.assertRaises(ValueError):
                c.validate_draft(draft.replace(c.SECTIONS[1], ""), n)

    def test_admission_fail_closed(self):
        j = json.loads(c.ADMISSIONS.read_text(encoding="utf-8"))
        admitted = c.load_admissions()
        self.assertEqual(set(admitted), {"001", "002", "003", "004", "005", "006"})
        self.assertEqual(admitted["001"]["manuscript_sha256"],
                         "fead8152dee7a70a702fb217166f27d1c7e5cea40183f5580e3a47bfd21092a8")
        self.assertEqual(admitted["002"]["manuscript_sha256"],
                         "30cb8d56240dcaf234cdfe3e05cfc21fda94f65bf53e0d4e55ddaa551161b5c2")
        self.assertEqual(admitted["003"]["manuscript_sha256"],
                         "6db924e9084e5a6df2ef2fca34438c87178cd348de8aefbcdf017b35f9e27b2b")
        self.assertEqual(admitted["004"]["manuscript_sha256"],
                         "d5c23e0a128d6836bd3de392ce861864c8afef44f6843593bc8a17354c9d9629")
        self.assertEqual(admitted["005"]["manuscript_sha256"],
                         "972871081d0ba1f686b79e044fb10aa9d3406156e712571bc06eb0a925a60d8e")
        self.assertEqual(admitted["006"]["manuscript_sha256"],
                         "84badb815c57a21a3a93386a9c99599b988401de7b441b7c39c6289f72da54cb")
        row = dict(family_id="007", manuscript_sha256="0"*64,
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
                                         editorial_drafts=4, editorially_admitted=6,
                                         reference_only=362, generated_pages=373))
            self.assertEqual(len(list((out / "families").glob("*.md"))), 372)
            self.assertTrue((out / "families/377.md").exists())
            admitted_page = (out / "families/001.md").read_text(encoding="utf-8")
            self.assertIn("EDITORIALLY_ADMITTED", admitted_page)
            self.assertIn("NO_CERTIFICATION", admitted_page)
            second_page = (out / "families/002.md").read_text(encoding="utf-8")
            self.assertIn("EDITORIALLY_ADMITTED", second_page)
            self.assertIn("NO_CERTIFICATION", second_page)
            third_page = (out / "families/003.md").read_text(encoding="utf-8")
            self.assertIn("EDITORIALLY_ADMITTED", third_page)
            self.assertIn("NO_CERTIFICATION", third_page)
            fourth_page = (out / "families/004.md").read_text(encoding="utf-8")
            self.assertIn("EDITORIALLY_ADMITTED", fourth_page)
            self.assertIn("NO_CERTIFICATION", fourth_page)
            fifth_page = (out / "families/005.md").read_text(encoding="utf-8")
            self.assertIn("EDITORIALLY_ADMITTED", fifth_page)
            self.assertIn("NO_CERTIFICATION", fifth_page)
            sixth_page = (out / "families/006.md").read_text(encoding="utf-8")
            self.assertIn("EDITORIALLY_ADMITTED", sixth_page)
            self.assertIn("NO_CERTIFICATION", sixth_page)
            for n in ("007", "008", "342", "376"):
                page = (out / "families" / (n+".md")).read_text(encoding="utf-8")
                self.assertIn("DRAFT_UNACCEPTED", page)
                self.assertIn("NO_CERTIFICATION", page)
            ref = (out / "families/009.md").read_text(encoding="utf-8")
            self.assertIn("REFERENCE_ONLY", ref)
            self.assertIn("FAMILY_SEMANTICS_UNREVIEWED", ref)
            self.assertIn("NO_CERTIFICATION", ref)
            c.clean(out)
            self.assertFalse((out / "catalogue.md").exists())
            self.assertFalse((out / "families").exists())


if __name__ == "__main__":
    unittest.main()
