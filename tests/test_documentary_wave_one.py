from __future__ import annotations

import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCUMENTARIES = DOCS / "documentaries"

WAVE_ONE = {
    "navier_stokes": {"campaign": "NS-CI-001", "domain": "Domain 02"},
    "p_vs_np": {"campaign": "PNP-001", "domain": "Domain 07"},
    "hodge": {"campaign": "HC-001", "domain": "Domain 03"},
    "yang_mills": {"campaign": "YM-001", "domain": "Domain 06"},
    "riemann": {"campaign": "RH-001", "domain": "Domain 08"},
}
REQUIRED_BOXES = ('class="definition-box"','class="theorem-box"','class="conjecture-box"','class="imported-box"','class="warning-box"')

class DocumentaryWaveOneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema=json.loads((DOCUMENTARIES/"documentary_web.schema.json").read_text(encoding="utf-8"))
        cls.manifest=json.loads((DOCUMENTARIES/"ARTIFACT_MANIFEST.json").read_text(encoding="utf-8"))
        cls.volumes={volume["slug"]:volume for volume in cls.manifest["volumes"]}
        cls.reader_css=(DOCS/"stylesheets/documentary.css").read_text(encoding="utf-8")
        cls.status_css=(DOCS/"stylesheets/documentary-status.css").read_text(encoding="utf-8")
    def load(self,slug:str)->tuple[dict,str,dict]:
        edition=json.loads((DOCUMENTARIES/f"{slug}.edition.json").read_text(encoding="utf-8"))
        page=(DOCUMENTARIES/f"{slug}.md").read_text(encoding="utf-8")
        return edition,page,self.volumes[slug]
    def test_every_wave_one_edition_is_schema_valid(self)->None:
        validator=Draft202012Validator(self.schema,format_checker=FormatChecker())
        for slug in WAVE_ONE:
            with self.subTest(slug=slug):
                edition,_,_=self.load(slug)
                errors=sorted(validator.iter_errors(edition),key=lambda item:list(item.path))
                self.assertEqual([],[f"{error.json_path}: {error.message}" for error in errors])
                self.assertEqual(slug,edition["volume_id"]);self.assertEqual("1.1.0",edition["schema_version"]);self.assertEqual("docs_root",edition["asset_base"])
    def test_open_status_and_exact_claim_boundaries(self)->None:
        for slug,crosswalk in WAVE_ONE.items():
            with self.subTest(slug=slug):
                edition,page,_=self.load(slug)
                self.assertIn("Open Millennium Prize Problem",edition["status"])
                self.assertGreaterEqual(page.count("Open Millennium Prize Problem"),2)
                self.assertIn(edition["claim_boundary"],page);self.assertIn(crosswalk["campaign"],page);self.assertIn(crosswalk["domain"],page)
                for forbidden in ("problem is solved","new proof of","we prove P = NP","we prove P ≠ NP","proves the Riemann Hypothesis"):
                    self.assertNotIn(forbidden,page)
    def test_semantic_reader_accessibility_and_status_surfaces(self)->None:
        for slug in WAVE_ONE:
            with self.subTest(slug=slug):
                _,page,_=self.load(slug)
                required=(f'data-gcl-reader="{slug}"','data-edition="1.1.0"','<article class="monograph-body"','id="monograph-start" tabindex="-1"','href="#monograph-start"',"documentary-status.css","source TeX remain",'aria-live="polite"','data-plate-dialog')+REQUIRED_BOXES
                for marker in required:self.assertIn(marker,page)
                self.assertNotIn('<main class="monograph-body"',page)
    def test_plate_assets_are_accessible_and_pedagogical(self)->None:
        for slug in WAVE_ONE:
            edition,page,_=self.load(slug);self.assertGreaterEqual(len(edition["plates"]),5)
            for plate in edition["plates"]:
                with self.subTest(slug=slug,plate=plate["id"]):
                    self.assertEqual("pedagogical_orientation_only",plate["authority"]);self.assertGreaterEqual(len(plate["alt"]),20)
                    asset=DOCS/plate["asset"];self.assertTrue(asset.is_file(),plate["asset"]);self.assertIn(plate["asset"],page)
                    root=ET.parse(asset).getroot();ns={"svg":"http://www.w3.org/2000/svg"};self.assertIsNotNone(root.find("svg:title",ns));self.assertIsNotNone(root.find("svg:desc",ns))
    def test_sections_and_sources_are_rendered(self)->None:
        for slug in WAVE_ONE:
            edition,page,_=self.load(slug);sections=edition["chapters"]+edition["appendices"];ids=[section["id"] for section in sections];self.assertEqual(len(ids),len(set(ids)))
            for section_id in ids:self.assertIn(f'id="{section_id}"',page);self.assertIn(f'href="#{section_id}"',page)
            for source in edition["sources"]:self.assertIn(source,page)
    def test_mathjax_mobile_reduced_motion_and_print_contracts(self)->None:
        for marker in ("@media(max-width:680px)","prefers-reduced-motion","@media print",":focus-visible"):self.assertIn(marker,self.reader_css)
        for slug in WAVE_ONE:
            edition,page,_=self.load(slug);self.assertIn(f'.gcl-monograph[data-gcl-reader="{slug}"]',self.status_css);self.assertIn(edition["math_rendering"]["script_url"],page)
            for marker in ('crossorigin="anonymous"','referrerpolicy="no-referrer"','data-archival-role="enhancement-only"'):self.assertIn(marker,page)
        self.assertIn("@media(max-width:680px)",self.status_css);self.assertIn("@media print",self.status_css)
    def test_source_authority_and_release_identities_are_preserved(self)->None:
        for slug in WAVE_ONE:
            _,page,volume=self.load(slug);self.assertIn("source record",page.lower());self.assertIn("authoritative source artifact",page.lower())
            for key in ("rendered_pdf","latex_source","authoritative_source_bundle"):
                artifact=volume[key];self.assertIn(f"{artifact['bytes']:,}",page);self.assertIn(artifact["sha256"],page);self.assertIn(artifact["availability"],page)

if __name__=="__main__":unittest.main()
