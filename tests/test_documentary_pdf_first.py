"""The public PDF menu may link only to released copies of governed PDFs."""
from pathlib import Path
import copy,json,sys,unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"ci"))
from validate_documentaries import pdf_release_contract_errors

class DocumentaryPdfFirstTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=json.loads((ROOT/"docs/documentaries/ARTIFACT_MANIFEST.json").read_text())
        cls.record=json.loads((ROOT/"docs/documentaries/PDF_RELEASES.json").read_text())
        cls.index=(ROOT/"docs/documentaries/index.md").read_text()

    def test_exact_public_pdf_identities(self):
        self.assertEqual(pdf_release_contract_errors(self.manifest,self.record,self.index),[])
        self.assertEqual(len(self.record["pdfs"]),8)
        self.assertEqual(len(self.manifest["volumes"]),9)

    def test_corrupt_pdf_hash_rejected(self):
        modified=copy.deepcopy(self.record)
        modified["pdfs"][0]["sha256"]="0"*64
        self.assertTrue(any("wrong sha256" in error for error in
                            pdf_release_contract_errors(self.manifest,modified,self.index)))

    def test_missing_and_fake_downloads_rejected(self):
        self.assertTrue(pdf_release_contract_errors(self.manifest,self.record,self.index.replace(
            self.record["pdfs"][0]["download_url"],"https://example.com/fake.pdf")))
        modified=copy.deepcopy(self.record)
        modified["pdfs"].pop()
        self.assertTrue(pdf_release_contract_errors(self.manifest,modified,self.index))

    def test_all_web_editions_archived_not_featured(self):
        nav=(ROOT/"mkdocs.yml").read_text()
        archive=(ROOT/"docs/archives/publications.md").read_text()
        self.assertIn("      - Documentary Library: documentaries/index.md",nav)
        for row in self.manifest["volumes"]:
            path="documentaries/"+row["web_page"]
            self.assertNotIn(path,nav)
            self.assertIn("../"+path,archive)

    def test_release_tag_is_anchored_and_micro_has_no_imagined_pdf(self):
        self.assertEqual(self.record["release_target_protected_commit"],
                         "1b6e1897a24ea7d4d898a2f0b90b22ee2e435399")
        self.assertEqual(self.record["no_pdf"]["slug"],"euclid_book_vii_micro")
        self.assertNotIn("euclid_book_vii_micro.pdf",self.index)

if __name__=="__main__":unittest.main()
