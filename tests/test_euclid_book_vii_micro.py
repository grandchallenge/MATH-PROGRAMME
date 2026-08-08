#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import euclid_book_vii_micro as validator


class EuclidBookVIIMicroTests(unittest.TestCase):
    def test_protected_candidate_validates(self) -> None:
        self.assertEqual(validator.validate(), [])

    def _mutated_json(self, original: Path, mutate) -> Path:
        data = json.loads(original.read_text(encoding="utf-8"))
        mutate(data)
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", encoding="utf-8", delete=False)
        json.dump(data, tmp)
        tmp.close()
        self.addCleanup(lambda: Path(tmp.name).unlink(missing_ok=True))
        return Path(tmp.name)

    def test_schema_rejects_extra_edition_property(self) -> None:
        data = json.loads(validator.EDITION.read_text(encoding="utf-8"))
        data["authority_surprise"] = True
        schema = json.loads(validator.SCHEMA.read_text(encoding="utf-8"))
        self.assertTrue(list(validator.Draft202012Validator(schema).iter_errors(data)))

    def test_source_lock_substitution_rejected(self) -> None:
        mutated = self._mutated_json(validator.SOURCE, lambda d: d.__setitem__("source_lock_merge", "0" * 40))
        with patch.object(validator, "SOURCE", mutated):
            self.assertIn("source-lock merge drift", validator.validate())

    def test_source_sha_drift_rejected(self) -> None:
        mutated = self._mutated_json(validator.SOURCE, lambda d: d["transcription"].__setitem__("sha256", "0" * 64))
        with patch.object(validator, "SOURCE", mutated):
            self.assertIn("transcription identity drift", validator.validate())

    def test_locus_insertion_rejected(self) -> None:
        mutated = self._mutated_json(validator.SOURCE, lambda d: d["admitted_loci"].append("VII.3"))
        with patch.object(validator, "SOURCE", mutated):
            self.assertTrue(any("locus membership" in e for e in validator.validate()))

    def test_locus_deletion_rejected(self) -> None:
        mutated = self._mutated_json(validator.EDITION, lambda d: d["admitted_loci"].pop())
        with patch.object(validator, "EDITION", mutated):
            self.assertTrue(validator.validate())

    def test_historical_quote_mutation_rejected(self) -> None:
        text = validator.PAGE.read_text(encoding="utf-8").replace(validator.EXACT_STATEMENTS["VII.def.2"], "A number is anything countable.")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", encoding="utf-8", delete=False) as tmp:
            tmp.write(text); path = Path(tmp.name)
        self.addCleanup(lambda: path.unlink(missing_ok=True))
        with patch.object(validator, "PAGE", path):
            self.assertTrue(any("VII.def.2" in e for e in validator.validate()))

    def test_authority_inflation_rejected(self) -> None:
        mutated = self._mutated_json(validator.EDITION, lambda d: d["authority_flags"].__setitem__("bezout_verbatim_euclid", True))
        with patch.object(validator, "EDITION", mutated):
            self.assertTrue(validator.validate())

    def test_plate_authority_inflation_rejected(self) -> None:
        mutated = self._mutated_json(validator.EDITION, lambda d: d["plates"][0].__setitem__("authority", "proof_authority"))
        with patch.object(validator, "EDITION", mutated):
            self.assertTrue(validator.validate())

    def test_missing_plate_accessibility_rejected(self) -> None:
        text = validator.PLATES[0].read_text(encoding="utf-8").replace("<desc id=\"desc\">", "<metadata>", 1)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".svg", encoding="utf-8", delete=False) as tmp:
            tmp.write(text); path = Path(tmp.name)
        self.addCleanup(lambda: path.unlink(missing_ok=True))
        with patch.object(validator, "PLATES", [path, validator.PLATES[1]]):
            self.assertTrue(any("<desc" in e for e in validator.validate()))

    def test_manifest_membership_deletion_rejected(self) -> None:
        mutated = self._mutated_json(validator.MANIFEST, lambda d: d.__setitem__("volumes", [v for v in d["volumes"] if v.get("slug") != "euclid_book_vii_micro"]))
        with patch.object(validator, "MANIFEST", mutated):
            self.assertTrue(any("manifest" in e for e in validator.validate()))

    def test_navigation_deletion_rejected(self) -> None:
        text = validator.MKDOCS.read_text(encoding="utf-8").replace("          - Euclid, Book VII: Measure and Common Measure: documentaries/euclid_book_vii_micro.md\n", "")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", encoding="utf-8", delete=False) as tmp:
            tmp.write(text); path = Path(tmp.name)
        self.addCleanup(lambda: path.unlink(missing_ok=True))
        with patch.object(validator, "MKDOCS", path):
            self.assertIn("MkDocs navigation admission missing", validator.validate())

    def test_partial_atomic_member_rejected(self) -> None:
        mutated = self._mutated_json(validator.ADMISSION, lambda d: d["atomic_members"].remove("docs/documentaries/euclid_book_vii_micro.edition.json"))
        with patch.object(validator, "ADMISSION", mutated):
            self.assertTrue(any("atomic admission member missing" in e for e in validator.validate()))

    def test_modern_authority_insertion_rejected(self) -> None:
        mutated = self._mutated_json(validator.ADMISSION, lambda d: d.__setitem__("mathcert_authority_created", True))
        with patch.object(validator, "ADMISSION", mutated):
            self.assertIn("admission authority inflation: mathcert_authority_created", validator.validate())

    def test_print_contract_rejected_if_removed(self) -> None:
        text = validator.CSS.read_text(encoding="utf-8").replace("@media print", "@media screen")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".css", encoding="utf-8", delete=False) as tmp:
            tmp.write(text); path = Path(tmp.name)
        self.addCleanup(lambda: path.unlink(missing_ok=True))
        with patch.object(validator, "CSS", path):
            self.assertTrue(any("@media print" in e for e in validator.validate()))


if __name__ == "__main__":
    unittest.main()
