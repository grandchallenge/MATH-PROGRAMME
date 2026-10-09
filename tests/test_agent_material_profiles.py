from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from agent_material_profiles import (  # noqa: E402
    MaterialAdmissionError, classify_text, load_registry, validate_registry,
)
from agent_routine_review import (  # noqa: E402
    REPOSITORY, RoutineReviewError, delegated_classification, review_body,
)


class DelegatedMaterialProfilesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry()

    def classify(self, old: str, new: str, path: str = "docs/ORIENTATION.md") -> dict:
        return classify_text(path, old.encode(), new.encode(), self.registry)

    def test_registry_contract_is_valid(self) -> None:
        validate_registry(self.registry)

    def test_final_newline_admitted(self) -> None:
        out = self.classify("# Orientation\n\nThis page explains ordinary routing.",
                            "# Orientation\n\nThis page explains ordinary routing.\n")
        self.assertEqual(out["profile_id"], "DOC-FINAL-NEWLINE-001")
        self.assertEqual(out["disposition"], "ROUTINE_BOUNDED")
        self.assertEqual([x["role"] for x in out["logical_passes"]],
                         ["Verifier", "Adversary"])
        self.assertFalse(out["authority"]["scientific_certification"])

    def test_single_trailing_space_admitted(self) -> None:
        out = self.classify("# Intro\n\nRoutine housekeeping. \nNext paragraph.\n",
                            "# Intro\n\nRoutine housekeeping.\nNext paragraph.\n")
        self.assertEqual(out["profile_id"], "DOC-TRAILING-SPACE-001")
        self.assertEqual(out["changed_lines"], 1)

    def test_redundant_blank_run_admitted(self) -> None:
        out = self.classify("# Intro\n\n\n\nBody.\n", "# Intro\n\n\nBody.\n")
        self.assertEqual(out["profile_id"], "DOC-REDUNDANT-BLANKS-001")

    def test_no_semantic_claim_insertion(self) -> None:
        with self.assertRaises(MaterialAdmissionError):
            self.classify("A bounded note.\n", "A bounded note.\nCM4 is proven.\n")

    def test_claim_and_whitespace_mixed_rejected(self) -> None:
        with self.assertRaises(MaterialAdmissionError):
            self.classify("Some prose. \n", "Some other prose.\n")

    def test_double_space_markdown_hard_break_not_removed(self) -> None:
        with self.assertRaises(MaterialAdmissionError):
            self.classify("Markdown line.  \nNext line.\n",
                          "Markdown line.\nNext line.\n")

    def test_protected_governance_paths_excluded(self) -> None:
        for path in ("docs/governance/AUTHORITY.md", "fixtures/formal/CM4.lean",
                     "ci/policy.py", ".github/workflows/a.yml", "docs/../../AGENTS.md"):
            with self.subTest(path=path), self.assertRaises(MaterialAdmissionError):
                self.classify("Prose. \n", "Prose.\n", path)

    def test_code_and_math_documents_not_whitespace_admitted(self) -> None:
        for fragment in ("```lean\nexample : True := trivial\n```",
                         "$$x^2+y^2=z^2$$", "\\begin{theorem}", "<!-- governed -->"):
            with self.subTest(fragment=fragment), self.assertRaises(MaterialAdmissionError):
                self.classify("# Note\n" + fragment + "\nText. \n",
                              "# Note\n" + fragment + "\nText.\n")

    def test_crlf_and_tab_fails_closed(self) -> None:
        for text in (b"Doc\r\n", b"Doc\t\n"):
            with self.assertRaises(MaterialAdmissionError):
                classify_text("docs/Intro.md", text, b"Doc\n", self.registry)

    def test_oversized_file_fails_closed(self) -> None:
        with self.assertRaises(MaterialAdmissionError):
            classify_text("docs/Intro.md", b"x" * 250001, b"x\n", self.registry)

    def test_profile_substitution_rejected(self) -> None:
        data = copy.deepcopy(self.registry)
        data["profiles"][0]["operation"] = "unrestricted_docs_change"
        with self.assertRaises(MaterialAdmissionError):
            validate_registry(data)

    def test_authority_bit_flip_rejected(self) -> None:
        data = copy.deepcopy(self.registry)
        data["boundaries"]["mathematical_certification"] = True
        with self.assertRaises(MaterialAdmissionError):
            validate_registry(data)

    def test_missing_review_role_rejected(self) -> None:
        data = copy.deepcopy(self.registry)
        data["profiles"][0]["review_roles"] = ["Verifier"]
        with self.assertRaises(MaterialAdmissionError):
            validate_registry(data)

    def test_no_changes_no_approval(self) -> None:
        with self.assertRaises(MaterialAdmissionError):
            self.classify("Same line.\n", "Same line.\n")

    def test_more_than_twelve_changes_rejected(self) -> None:
        a = "# Intro\n" + "Ordinary text. \n" * 13
        b = "# Intro\n" + "Ordinary text.\n" * 13
        with self.assertRaises(MaterialAdmissionError):
            self.classify(a, b)

    def test_executable_controller_uses_only_pinned_bytes(self) -> None:
        head, base = "a" * 40, "b" * 40
        pr = {
            "state": "open", "draft": False, "changed_files": 1,
            "head": {"sha": head, "repo": {"full_name": REPOSITORY}},
            "base": {"ref": "main", "sha": base}, "user": {"login": "fyremael"},
        }
        after = b"Safe narrative.\n"
        before = b"Safe narrative."
        changed = [{"filename": "docs/Intro.md", "status": "modified", "sha": "c" * 40}]
        with patch("agent_routine_review.fetch_exact_file",
                   side_effect=[(before, "d" * 40), (after, "c" * 40)]):
            out = delegated_classification(pr, changed, head, token="dummy",
                                           prefix=f"/repos/{REPOSITORY}")
        self.assertEqual(out["profile_id"], "DOC-FINAL-NEWLINE-001")
        body = review_body(head, out)
        self.assertIn("logical audit passes", body)
        self.assertIn("scientific_certification", body)

    def test_stale_or_mismatched_blob_never_approved(self) -> None:
        head, base = "a" * 40, "b" * 40
        pr = {
            "state": "open", "draft": False, "changed_files": 1,
            "head": {"sha": head, "repo": {"full_name": REPOSITORY}},
            "base": {"ref": "main", "sha": base}, "user": {"login": "fyremael"},
        }
        changed = [{"filename": "docs/Intro.md", "status": "modified", "sha": "c" * 40}]
        with patch("agent_routine_review.fetch_exact_file",
                   side_effect=[(b"Safe text.", "d" * 40), (b"Safe text.\n", "e" * 40)]):
            with self.assertRaisesRegex(RoutineReviewError, "blob"):
                delegated_classification(pr, changed, head, token="dummy",
                                         prefix=f"/repos/{REPOSITORY}")

    def test_multifile_candidate_never_approved(self) -> None:
        pr = {"state": "open", "draft": False, "changed_files": 2,
              "head": {"sha": "a" * 40, "repo": {"full_name": REPOSITORY}},
              "base": {"ref": "main", "sha": "b" * 40},
              "user": {"login": "fyremael"}}
        with self.assertRaises(RoutineReviewError):
            delegated_classification(pr, [], "a" * 40, token="dummy",
                                     prefix=f"/repos/{REPOSITORY}")


if __name__ == "__main__":
    unittest.main()
