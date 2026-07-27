from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCUMENTARIES = DOCS / "documentaries"


class BSDWebEditionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(
            (DOCUMENTARIES / "documentary_web.schema.json").read_text(encoding="utf-8")
        )
        cls.edition = json.loads(
            (DOCUMENTARIES / "bsd.edition.json").read_text(encoding="utf-8")
        )
        cls.page = (DOCUMENTARIES / "bsd.md").read_text(encoding="utf-8")
        cls.manifest = json.loads(
            (DOCUMENTARIES / "ARTIFACT_MANIFEST.json").read_text(encoding="utf-8")
        )
        cls.volume = next(
            volume for volume in cls.manifest["volumes"] if volume["slug"] == "bsd"
        )

    def test_edition_is_schema_valid(self) -> None:
        validator = Draft202012Validator(self.schema, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(self.edition), key=lambda item: list(item.path))
        self.assertEqual([], [f"{error.json_path}: {error.message}" for error in errors])
        self.assertEqual("bsd", self.edition["volume_id"])
        self.assertEqual("1.1.0", self.edition["schema_version"])

    def test_claim_boundary_and_open_status_are_explicit(self) -> None:
        self.assertIn("Open Millennium Prize Problem", self.edition["status"])
        self.assertGreaterEqual(self.page.count("Open Millennium Prize Problem"), 2)
        presentation_normalized = self.page.replace("$p$-adic", "p-adic")
        self.assertIn(self.edition["claim_boundary"], presentation_normalized)
        for phrase in (
            "does not prove BSD",
            "Rank equality, finiteness",
            "Numerical agreement, parity, Selmer bounds",
            "no proof claim",
        ):
            self.assertIn(phrase, self.page)
        for forbidden in (
            "BSD is proved",
            "proves the Birch and Swinnerton",
            "new proof of BSD",
        ):
            self.assertNotIn(forbidden, self.page)

    def test_semantic_reader_and_status_vocabulary(self) -> None:
        required = (
            'data-gcl-reader="bsd"',
            'data-edition="1.1.0"',
            '<article class="monograph-body"',
            'id="monograph-start" tabindex="-1"',
            'href="#monograph-start"',
            'class="definition-box"',
            'class="theorem-box"',
            'class="conjecture-box"',
            'class="warning-box"',
            'class="imported-box"',
            "documentary-status.css",
            "source TeX remain",
        )
        for marker in required:
            self.assertIn(marker, self.page)
        self.assertNotIn('<main class="monograph-body"', self.page)

    def test_plate_contract_and_assets(self) -> None:
        self.assertGreaterEqual(len(self.edition["plates"]), 6)
        for plate in self.edition["plates"]:
            self.assertEqual("pedagogical_orientation_only", plate["authority"])
            asset = DOCS / plate["asset"]
            self.assertTrue(asset.is_file(), plate["asset"])
            self.assertIn(plate["asset"], self.page)
            self.assertGreaterEqual(len(plate["alt"]), 20)
            if asset.suffix == ".svg":
                text = asset.read_text(encoding="utf-8")
                self.assertIn("<title", text)
                self.assertIn("<desc", text)

    def test_section_schema_matches_rendered_page(self) -> None:
        sections = self.edition["chapters"] + self.edition["appendices"]
        ids = [section["id"] for section in sections]
        self.assertEqual(len(ids), len(set(ids)))
        for section_id in ids:
            self.assertIn(f'id="{section_id}"', self.page)
            self.assertIn(f'href="#{section_id}"', self.page)

    def test_mathjax_and_responsive_print_contracts(self) -> None:
        math = self.edition["math_rendering"]
        self.assertIn(math["script_url"], self.page)
        for marker in (
            'crossorigin="anonymous"',
            'referrerpolicy="no-referrer"',
            'data-archival-role="enhancement-only"',
        ):
            self.assertIn(marker, self.page)
        reader_css = (DOCS / "stylesheets/documentary.css").read_text(encoding="utf-8")
        status_css = (DOCS / "stylesheets/documentary-status.css").read_text(encoding="utf-8")
        for marker in ("@media(max-width:680px)", "prefers-reduced-motion", "@media print", ":focus-visible"):
            self.assertIn(marker, reader_css)
        self.assertIn('@media(max-width:680px)', status_css)
        self.assertIn('@media print', status_css)

    def test_source_crosswalk_and_release_identities_are_preserved(self) -> None:
        self.assertIn("BSD-001", self.page)
        self.assertIn("Domain 04", self.page)
        self.assertIn("source record", self.page.lower())
        self.assertIn("authoritative source artifact", self.page.lower())
        for key in ("rendered_pdf", "latex_source", "authoritative_source_bundle"):
            artifact = self.volume[key]
            self.assertIn(f"{artifact['bytes']:,}", self.page)
            self.assertIn(artifact["sha256"], self.page)
            self.assertIn(artifact["availability"], self.page)

    def test_equation_and_guardrail_spine_is_present(self) -> None:
        normalized = re.sub(r"\s+", " ", self.page)
        for marker in (
            r"\operatorname{rank}E(\mathbb{Q})",
            r"\operatorname{ord}_{s=1}L(E,s)",
            r"\operatorname{Reg}(E/\mathbb{Q})",
            r"\operatorname{Sel}_n(E/\mathbb{Q})",
            r"\operatorname{Sha}(E/\mathbb{Q})",
        ):
            self.assertIn(marker, normalized)


if __name__ == "__main__":
    unittest.main()
