#!/usr/bin/env python3
"""Check that manuscript presence and GitHub merges cannot self-authorize coverage."""
from __future__ import annotations
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from erdos_compendium import ACCEPTANCE, EDITORIAL, build, load_admissions, load_batch_admissions, manuscript
from erdos_compendium_public_html_readback import publication_state_matches

REPO = "https://github.com/grandchallenge/MATH-PROGRAMME"

class EditorialGateTests(unittest.TestCase):
    def _build(self, admissions):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            manifest = root / "admissions.json"
            manifest.write_text(json.dumps({
                "record_type": "ERDOS_COMPENDIUM_EDITORIAL_ADMISSIONS/1",
                "admissions": admissions,
            }), encoding="utf-8")
            site = root / "erdos"
            counts = build(output=site, admissions_path=manifest)
            pages = {n: (site / "problems" / f"{n:04d}.md").read_text(encoding="utf-8")
                     for n in (1, 4, 7)}
            index = (site / "catalogue" / "index.md").read_text(encoding="utf-8")
            return counts, pages, index

    def _admission(self, n, sha):
        return {
            "problem_id": n,
            "source_sha256": sha,
            "source_check": REPO + "/issues/2556#issuecomment-6108695648",
            "critical_review": REPO + "/pull/2577#issuecomment-6108689695",
            "protected_admission": REPO + "/pull/2577",
            "mkdocs_run": REPO + "/actions/runs/38137356772",
            "public_html_readback": REPO + "/issues/2552#issuecomment-6109065121",
        }

    def _v2(self, entries, batch_id="EC-BULK-0001"):
        return {"record_type": "ERDOS_COMPENDIUM_EDITORIAL_ADMISSIONS/2",
                "admissions": [], "batches": [{
                    "batch_id": batch_id,
                    "critical_review": REPO + "/pull/2588#issuecomment-6108689695",
                    "protected_admission": REPO + "/pull/2588",
                    "mkdocs_run": REPO + "/actions/runs/38204827132",
                    "public_html_readback": REPO + "/issues/2556#issuecomment-6117889968",
                    "entries": entries,
                }]}

    def test_active_v2_ledger_preserves_exact_legacy_admission(self):
        """V1→V2 migration must preserve identity and all six evidence fields."""
        import copy
        actual = load_batch_admissions(ACCEPTANCE)
        self.assertEqual(set(actual), {7}, "Migration must not silently admit draft articles")
        row = copy.deepcopy(actual[7])
        self.assertEqual(row.pop("batch_id"), "EC-LEGACY-0007")
        self.assertEqual(row, {
            "problem_id": 7,
            "source_sha256": "a559fac0a350f5d487509d980a9257dfdaa662bc11f67d0ae930557a0d14acc2",
            "source_check": REPO + "/issues/1276#issuecomment-6103364800",
            "critical_review": REPO + "/issues/2556#issuecomment-6118086838",
            "protected_admission": REPO + "/pull/2587",
            "mkdocs_run": REPO + "/actions/runs/38204827132",
            "public_html_readback": REPO + "/issues/2556#issuecomment-6117889968",
        })
        self.assertEqual(row["source_sha256"],
                         hashlib.sha256(manuscript(7).encode("utf-8")).hexdigest())
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            counts = build(output=root / "site", admissions_path=ACCEPTANCE)
            self.assertEqual(counts["reviewed"], 1)
            self.assertEqual(counts["pending"],
                             counts["editorial"] - counts["legacy"] - 1)
            accepted_page = (root / "site" / "problems" / "0007.md").read_text(encoding="utf-8")
            self.assertIn("Reviewed explanatory article", accepted_page)
            self.assertNotIn("UNACCEPTED DRAFT", accepted_page)

    def test_v2_rejects_cross_version_duplicate_admission(self):
        sha = hashlib.sha256(manuscript(7).encode("utf-8")).hexdigest()
        data = self._v2([{
            "problem_id": 7, "source_sha256": sha,
            "source_check": REPO + "/issues/1276#issuecomment-6103364800",
        }])
        data["admissions"].append(self._admission(7, sha))
        with tempfile.TemporaryDirectory() as root:
            f = Path(root) / "manifest.json"
            f.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicated"):
                load_batch_admissions(f)

    def test_batch_v2_source_hash_and_shared_evidence(self):
        good_sha = hashlib.sha256(manuscript(7).encode("utf-8")).hexdigest()
        row = {"problem_id": 7, "source_sha256": good_sha,
               "source_check": REPO + "/issues/1276#issuecomment-6103364800"}
        with tempfile.TemporaryDirectory() as root:
            manifest = Path(root) / "admissions.json"
            def save(data):
                manifest.write_text(json.dumps(data), encoding="utf-8")
            save(self._v2([row]))
            self.assertEqual(set(load_batch_admissions(manifest)), {7})
            counts = build(output=Path(root)/"site", admissions_path=manifest)
            self.assertEqual(counts["reviewed"], 1)
            save(self._v2([row, row]))
            with self.assertRaisesRegex(ValueError, "duplicated"):
                load_batch_admissions(manifest)
            save(self._v2([{**row, "source_sha256": "0"*64}]))
            with self.assertRaisesRegex(ValueError, "changed without re-review"):
                build(output=Path(root)/"site", admissions_path=manifest)
            bad = self._v2([row]); bad["batches"][0]["mkdocs_run"] = "https://example.com/fake"
            save(bad)
            with self.assertRaisesRegex(ValueError, "Invalid batch mkdocs_run"):
                load_batch_admissions(manifest)
            bad = self._v2([row]); bad["batches"][0]["entries"][0].pop("source_check")
            save(bad)
            with self.assertRaisesRegex(ValueError, "Invalid per-article"):
                load_batch_admissions(manifest)
            bad = self._v2([row] * 251)
            save(bad)
            with self.assertRaisesRegex(ValueError, "batch size"):
                load_batch_admissions(manifest)

    def test_merged_drafts_do_not_auto_promote(self):
        counts, pages, index = self._build([])
        self.assertEqual(counts["problems"], 1221)
        self.assertEqual(counts["reviewed"], 0)
        self.assertEqual(counts["legacy"], 3)
        self.assertEqual(counts["editorial"], sum(manuscript(n) is not None for n in range(1, 1222)))
        self.assertEqual(counts["pending"], counts["editorial"] - counts["legacy"])
        self.assertIn("Legacy authored exemplar", pages[1])
        for n in (4, 7):
            self.assertIn("UNACCEPTED DRAFT", pages[n])
            self.assertIn("NOT editorially accepted", pages[n])
            self.assertIn("## The question in plain language", pages[n])
            self.assertIn("## A small example", pages[n])
        self.assertIn("0 separately admitted explanations", index)
        self.assertIn(f"{counts['pending']} manuscripts pending acceptance", index)

    def test_exact_source_and_evidence_can_admit_only_bounded_article(self):
        text = manuscript(7)
        good_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        counts, pages, _ = self._build([self._admission(7, good_sha)])
        self.assertEqual(counts["reviewed"], 1)
        self.assertEqual(counts["pending"], counts["editorial"] - counts["legacy"] - 1)
        self.assertIn("## What is known", pages[7])
        self.assertIn("A **covering system**", pages[7])
        self.assertIn("UNACCEPTED DRAFT", pages[4])
        self.assertNotIn("UNACCEPTED DRAFT", pages[7])

    def test_new_manuscript_rejects_nonportable_github_math_fences(self):
        # Legacy authored sources have a documented, bounded exception;
        # new articles must render correctly on GitHub *and* on MkDocs.
        source = manuscript(7)
        self.assertNotIn(r"\(", source)
        self.assertNotIn(r"\[", source)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "0009.md"
            path.write_text(source + chr(10) + r"\(x\)" + chr(10), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "nonportable GitHub mathematical delimiters"):
                manuscript(9, base=Path(temp))
            path.write_text(source, encoding="utf-8")
            self.assertEqual(manuscript(9, base=Path(temp)), source)

    def test_live_publication_state_is_ledger_bound_and_fail_closed(self):
        draft = {"draft": True, "reviewed": False, "notCertified": True}
        accepted = {"draft": False, "reviewed": True, "notCertified": False}
        mixed = {"draft": True, "reviewed": True, "notCertified": True}
        self.assertTrue(publication_state_matches(draft, False))
        self.assertTrue(publication_state_matches(accepted, True))
        self.assertFalse(publication_state_matches(draft, True))
        self.assertFalse(publication_state_matches(accepted, False))
        self.assertFalse(publication_state_matches(mixed, True))
        self.assertFalse(publication_state_matches(mixed, False))

    def test_stale_evidence_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "changed without re-review"):
            self._build([self._admission(7, "0"*64)])

    def test_invalid_evidence_and_duplicate_or_legacy_fail(self):
        sha = hashlib.sha256(manuscript(7).encode("utf-8")).hexdigest()
        bad = self._admission(7, sha)
        bad["public_html_readback"] = "https://example.com/unverified"
        with self.assertRaisesRegex(ValueError, "Invalid public_html_readback"):
            self._build([bad])
        with self.assertRaisesRegex(ValueError, "duplicated"):
            self._build([self._admission(7, sha)] * 2)
        with self.assertRaisesRegex(ValueError, "legacy"):
            self._build([self._admission(1, "a"*64)])

if __name__ == "__main__":
    unittest.main()
