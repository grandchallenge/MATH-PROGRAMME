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
from erdos_compendium import ACCEPTANCE, EDITORIAL, ROOT, build, load_admissions, load_batch_admissions, load_registry, manuscript
from erdos_compendium_public_html_readback import protected_editorial_state, publication_state_matches

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

    def test_browser_readback_reads_active_v2_batch_ledger(self):
        """V2 browser verifier accepts original #7 and protected new #8."""
        for n in (7, 8):
            self.assertTrue(protected_editorial_state(n))
            self.assertTrue(publication_state_matches(
                {"reviewed": True, "draft": False, "notCertified": False},
                admitted=protected_editorial_state(n)))

    def test_active_v2_ledger_preserves_exact_legacy_admission(self):
        """V1→V2 migration must preserve identity and all six evidence fields."""
        import copy
        actual = load_batch_admissions(ACCEPTANCE)
        cohort = json.loads((ROOT / "governance/erdos_compendium/batches/EC-BULK-001.json").read_text(encoding="utf-8"))
        expected_ids = {x["problem_id"] for x in cohort["items"]}
        self.assertEqual(len(expected_ids), 50)
        new_ids = {n for n in range(246, 447) if n != 390}
        self.assertEqual(set(actual), expected_ids | new_ids,
                         "Only the two exact protected editorial cohorts may be admitted")
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
            self.assertEqual(counts["reviewed"], 250)
            self.assertEqual(counts["pending"], counts["editorial"] - counts["legacy"] - counts["reviewed"])
            accepted_page = (root / "site" / "problems" / "0007.md").read_text(encoding="utf-8")
            self.assertIn("Reviewed explanatory article", accepted_page)
            self.assertNotIn("UNACCEPTED DRAFT", accepted_page)

    def test_bulk_001_protected_admission_evidence_and_exact_source(self):
        """Full-batch admission must bind every manuscript and all shared receipts."""
        proposal = json.loads((ROOT / "governance/erdos_compendium/batches/EC-BULK-001_ADMISSION_PROPOSAL.json").read_text(encoding="utf-8"))
        ledger = json.loads(ACCEPTANCE.read_text(encoding="utf-8"))
        self.assertEqual(proposal["record_type"], "ERDOS_COMPENDIUM_BATCH_ADMISSION_PROPOSAL/1")
        self.assertEqual(proposal["cohort_id"], "EC-BULK-001")
        self.assertEqual(proposal["new_admission_count"], 49)
        self.assertEqual(len(ledger["batches"]), 3)
        batch = ledger["batches"][1]
        self.assertEqual(batch["batch_id"], "EC-BULK-001")
        self.assertEqual(batch["protected_admission"], REPO + "/pull/2608")
        for field in ("critical_review", "mkdocs_run", "public_html_readback"):
            self.assertEqual(batch[field], proposal[field])
        expected = {r["problem_id"]: r for r in proposal["entries"]}
        actual = {r["problem_id"]: r for r in batch["entries"]}
        self.assertEqual(len(expected), 49)
        self.assertEqual(actual, expected)
        self.assertNotIn(7, actual)
        for n, row in expected.items():
            self.assertEqual(hashlib.sha256(manuscript(n).encode("utf-8")).hexdigest(),
                             row["source_sha256"], f"Stale source in admitted article #{n}")
            self.assertIn(row["source_check"], manuscript(n),
                          f"No exact issue-source link in article #{n}")
        self.assertEqual(proposal["public_browser_digest"],
                         "9a47a82c4c449439cbf3acd651a6d2a529939c562c2b30a2fa96361547d0bf89")
        self.assertIn("NOT_MATHEMATICAL_CERTIFICATION", proposal["disposition"])

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

    def test_bulk_001_002_boundary_is_contiguous_and_nonoverlapping(self):
        """Every registered #4–#245 belongs to exactly one intake cohort."""
        _, rows = load_registry()
        issue_by_id = {row["problem_id"]: row["issue_number"] for row in rows}
        required = set(range(4, 246))
        self.assertTrue(required <= issue_by_id.keys(),
                        "Canonical registry has a missing #4–#245 identity")
        selected_001 = set(range(4, 42)) | {99, 101, 138, 241}
        selected_002 = set(range(42, 246)) - {99, 101, 138, 241}
        expected_001_outliers = {390, 470, 522, 550, 593, 595, 1052, 1112}
        owners = {}
        for cohort, expected_size, expected_in_range in (
            ("EC-BULK-001", 50, selected_001),
            ("EC-BULK-002", 200, selected_002),
        ):
            path = (ROOT / "governance/erdos_compendium/batches" /
                    f"{cohort}.json")
            manifest = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["cohort_id"], cohort)
            self.assertEqual(manifest["target_count"], expected_size)
            items = manifest["items"]
            ids = [item["problem_id"] for item in items]
            self.assertEqual(len(ids), expected_size)
            self.assertEqual(len(set(ids)), len(ids),
                             f"Duplicate within {cohort}")
            self.assertEqual(set(ids) & required, expected_in_range,
                             f"Wrong #4–#245 membership in {cohort}")
            if cohort == "EC-BULK-001":
                self.assertEqual(set(ids) - required, expected_001_outliers)
            else:
                self.assertFalse(set(ids) - required)
            for item in items:
                n = item["problem_id"]
                self.assertIn(n, issue_by_id,
                              f"Unknown registered problem #{n}")
                self.assertEqual(item["audit_issue"], issue_by_id[n],
                                 f"Wrong canonical issue for #{n}")
                if n in required:
                    self.assertNotIn(n, owners,
                                     f"Problem #{n} assigned twice")
                    owners[n] = cohort
        self.assertEqual(set(owners), required,
                         f"Missing/extra #4–#245 assignments: "
                         f"{sorted(required ^ set(owners))}")
        self.assertEqual(len(owners), 242)

    def test_full_1221_catalogue_ownership(self):
        """All registry IDs have one owner; staged owners are not admissions."""
        _, rows = load_registry()
        by_id = {row["problem_id"]: row for row in rows}
        universe = set(range(1, 1222))
        self.assertEqual(len(rows), 1221)
        self.assertEqual(set(by_id), universe)
        raw = (ROOT / "governance/erdos_catalogue/REGISTRY.json").read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() +
                            b"\\0" + raw).hexdigest()
        self.assertEqual(blob, "90f6499cfbaca8c8a9e1ac4c6beb468ca09127a5")
        # Each tuple: cohort, inclusive range, omitted IDs, additional IDs,
        # manifest expected on protected main, exact cohort cardinality.
        partitions = (
            ("EC-BULK-001", 4, 41, (), (99, 101, 138, 241, 390, 470, 522,
                                        550, 593, 595, 1052, 1112), True, 50),
            ("EC-BULK-002", 42, 245, (99, 101, 138, 241), (), True, 200),
            ("EC-BULK-003", 246, 446, (390,), (), True, 200),
            ("EC-BULK-004", 447, 651, (470, 522, 550, 593, 595),
             (), False, 200),
            ("EC-BULK-005", 652, 851, (), (), False, 200),
            ("EC-BULK-006", 852, 1051, (), (), False, 200),
            ("EC-BULK-007", 1053, 1221, (1112,), (), False, 168),
        )
        owners = {n: "LEGACY" for n in (1, 2, 3)}
        for n in (1, 2, 3):
            self.assertIsNotNone(manuscript(n))
        for cohort, low, high, omit, extra, required_on_main, expected_n in partitions:
            expected = set(range(low, high + 1)).difference(omit).union(extra)
            self.assertEqual(len(expected), expected_n, cohort)
            for n in expected:
                self.assertIn(n, universe)
                self.assertNotIn(n, owners,
                                 f"Duplicate #{n}: {owners.get(n)} and {cohort}")
                owners[n] = cohort
            path = ROOT / "governance/erdos_compendium/batches" / f"{cohort}.json"
            if not path.exists():
                self.assertFalse(required_on_main,
                                 f"Missing protected manifest: {cohort}")
                continue  # staged reservation, not documentary admission
            record = json.loads(path.read_text(encoding="utf-8"))
            items = record["items"]
            ids = [item["problem_id"] for item in items]
            self.assertEqual(record["cohort_id"], cohort)
            self.assertEqual(record["target_count"], expected_n)
            self.assertEqual(record["source_registry_blob"], blob)
            self.assertEqual(len(ids), expected_n)
            self.assertEqual(len(set(ids)), expected_n)
            self.assertEqual(set(ids), expected,
                             f"Wrong issue ownership in {cohort}")
            for item in items:
                n = item["problem_id"]
                row = by_id[n]
                self.assertEqual(item["audit_issue"], row["issue_number"])
                if item.get("source_return"):
                    self.assertRegex(
                        item["source_return"],
                        r"^https://github[.]com/grandchallenge/MATH-PROGRAMME/"
                        r"issues/" + str(row["issue_number"]) +
                        r"#issuecomment-[0-9]+$")
                if "original_issue_body_sha256" in item:
                    self.assertEqual(item["original_issue_body_sha256"],
                                     row["issue_body_sha256"])
        self.assertEqual(set(owners), universe)
        self.assertEqual(len(owners), 1221)
        admitted = load_batch_admissions(ACCEPTANCE)
        self.assertFalse(set(admitted) - universe)
        self.assertFalse(set(admitted) & {1, 2, 3})

    def test_bulk_002_200_existing_issue_slots_and_authentic_returns(self):
        """200 original queue jobs, not invented articles or accepted entries."""
        manifest_path = ROOT / "governance/erdos_compendium/batches/EC-BULK-002.json"
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(data["record_type"], "ERDOS_COMPENDIUM_BULK_INTAKE/1")
        self.assertEqual((data["cohort_id"], data["target_count"]), ("EC-BULK-002", 200))
        self.assertEqual(len(data["items"]), 200)
        self.assertTrue(data["source_queue_readback"]["all_200_open_available"])
        self.assertEqual(data["source_queue_readback"]["baseline_source_return_count"], 0)
        registry, rows = load_registry()
        source = ROOT / "governance/erdos_catalogue/REGISTRY.json"
        binary = source.read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(binary)).encode() + b"\0" + binary).hexdigest()
        self.assertEqual(data["source_registry_blob"], blob)
        ids = [x["problem_id"] for x in data["items"]]
        expected = sorted(x["problem_id"] for x in rows
                          if 42 <= x["problem_id"] <= 245
                          and x["problem_id"] not in {99, 101, 138, 241})
        self.assertEqual(ids, expected)
        issues = {r["problem_id"]: r["issue_number"] for r in rows}
        ready = 0
        for item in data["items"]:
            self.assertEqual(set(item), {
                "problem_id", "audit_issue", "source_return", "evidence_state"})
            n = item["problem_id"]
            self.assertEqual(item["audit_issue"], issues[n])
            if item["evidence_state"] == "RESULT_PRESENT_UNADJUDICATED":
                ready += 1
                self.assertRegex(
                    item["source_return"],
                    r"^https://github[.]com/grandchallenge/MATH-PROGRAMME/issues/" +
                    str(issues[n]) + r"#issuecomment-[0-9]+$")
                article = manuscript(n)
                self.assertIsNotNone(article, f"Source-ready #{n} has no manuscript yet")
                self.assertIn(item["source_return"], article)
            elif item["evidence_state"] == "NO_RESULT_AT_READBACK":
                self.assertIsNone(item["source_return"])
            else:
                self.fail("Unknown source state in 200-slot batch")
        self.assertGreaterEqual(ready, 3)
        self.assertNotIn(42, load_batch_admissions(ACCEPTANCE),
                         "Cohort source evidence is not an acceptance")

    def test_bulk_002_source_return_parser_rejects_forgeries(self):
        from erdos_compendium_source_reconcile import valid_return
        item = {"problem_id": 42, "audit_issue": 1311}
        comment = {
            "user": {"login": "review-worker"},
            "body": "\n".join([
                "RESULT/1", "ASSIGNMENT_ID: ERDOS-CATALOGUE-0042-S01",
                "PROBLEM_ID: 42", "DISPOSITION: STATUS_CONFLICT",
                "CONTEXT_CLASS: ZERO_CONTEXT", "TIMEBOX_OBSERVED: NO",
                "## Exact statement and normalization",
                "## Dated status and primary evidence",
                "## Strongest verified interface",
                "## Proposed bounded successor task",
                "## Prerequisites and blocker",
                "## Reuse and claim boundary",
            ]),
        }
        self.assertTrue(valid_return(item, comment))
        self.assertFalse(valid_return(item, {**comment, "user": {}}))
        self.assertFalse(valid_return(item, {**comment,
                         "body": comment["body"].replace("PROBLEM_ID: 42",
                                                         "PROBLEM_ID: 43")}))
        self.assertFalse(valid_return(item, {**comment,
                         "body": "Note: " + comment["body"]}))
        self.assertFalse(valid_return(item, {**comment,
                         "body": comment["body"].replace(
                             "## Prerequisites and blocker", "## Not reviewed")}))

    def test_bulk_001_source_return_is_not_acceptance(self):
        """Fail closed on mismatched registry identities or fabricated source readiness."""
        manifest = ROOT / "governance/erdos_compendium/batches/EC-BULK-001.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertEqual(data["record_type"], "ERDOS_COMPENDIUM_BULK_INTAKE/1")
        self.assertEqual(data["cohort_id"], "EC-BULK-001")
        self.assertEqual(data["observed_date"], "2026-10-12")
        self.assertEqual(data["target_count"], 50)
        self.assertEqual(len(data["items"]), 50)
        catalogue, rows = load_registry()
        by_id = {r["problem_id"]: r["issue_number"] for r in rows}
        ids = [r["problem_id"] for r in data["items"]]
        self.assertEqual(ids, sorted(set(ids)))
        self.assertFalse({1, 2, 3} & set(ids), "Legacy exemplars must not enter new admissions")
        registry_bytes = (ROOT / "governance/erdos_catalogue/REGISTRY.json").read_bytes()
        git_blob = hashlib.sha1(b"blob " + str(len(registry_bytes)).encode() +
                                b"\0" + registry_bytes).hexdigest()
        self.assertEqual(data["source_registry_blob"], git_blob)
        returned = 0
        missing = 0
        for item in data["items"]:
            self.assertEqual(set(item), {"problem_id", "audit_issue",
                                         "source_return", "evidence_state"})
            self.assertEqual(by_id[item["problem_id"]], item["audit_issue"])
            if item["evidence_state"] == "RESULT_PRESENT_UNADJUDICATED":
                self.assertRegex(item["source_return"],
                    r"^https://github[.]com/grandchallenge/MATH-PROGRAMME/issues/" +
                    str(item["audit_issue"]) + r"#issuecomment-[0-9]+$")
                returned += 1
            elif item["evidence_state"] == "NO_RESULT_AT_READBACK":
                self.assertIsNone(item["source_return"])
                missing += 1
            else:
                self.fail("Unknown source evidence state")
        self.assertEqual((returned, missing), (50, 0))
        self.assertIn("NOT accepted", data["status_semantics"])

    def test_bulk_001_six_new_source_boundaries(self):
        """Check finite constructions without conflating them with deep claims."""
        from math import log, isqrt
        from itertools import combinations

        # #5: ratio of the two normalizations is a finite identity.
        for n, p, next_p in [(3, 5, 7), (4, 7, 11), (5, 11, 13)]:
            self.assertAlmostEqual(
                (next_p-p) / log(n),
                ((next_p-p) / log(p)) * (log(p) / log(n)))
        # #8: singleton residue classes of modulus >1 do not cover a cycle.
        for m in range(2, 20):
            self.assertTrue(all(
                any(x % m != r for x in range(m))
                for r in range(m)))
        # #13: lower construction with b=c allowed is forbidden-triple-free.
        for N in range(1, 51):
            A = list(range((2*N)//3 + 1, N+1))
            for a in A:
                for b in A:
                    for c in A:
                        if a < min(b, c):
                            self.assertNotEqual((b+c) % a, 0)
        # #16: any odd prime plus 1 has prime=2, and then n=3.
        def prime(n):
            return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))
        self.assertEqual([p+1 for p in range(2, 200)
                          if prime(p) and (p+1) % 2], [3])
        # #21: f(2)=3, witnessed by a triangle; <=2 edges have a hit.
        edges = [frozenset((1, 2)), frozenset((1, 3)),
                 frozenset((2, 3))]
        self.assertTrue(all(a & b for a, b in combinations(edges, 2)))
        self.assertFalse(any(all(v in edge for edge in edges)
                             for v in (1, 2, 3)))
        self.assertTrue(any(
            all(set(hit) & edge for edge in edges)
            for hit in combinations((1,2,3), 2)))
        # #22: C4 is K4-free and has independence number 2, not o(4).
        C4 = {frozenset(e) for e in ((0,1),(1,2),(2,3),(3,0))}
        self.assertEqual(len(C4), 4)
        self.assertGreaterEqual(len(C4), 4*4/8)
        self.assertTrue(any(all(
            frozenset(pair) not in C4
            for pair in combinations(vertices, 2))
            for vertices in combinations(range(4), 2)))
        self.assertFalse(any(all(
            frozenset(pair) not in C4
            for pair in combinations(vertices, 2))
            for vertices in combinations(range(4), 3)))

    def test_bulk_001_four_graph_and_set_examples(self):
        """#19/#20/#23/#24 exact finite models: no asymptotic claim."""
        from itertools import combinations, permutations

        # #19 n=2: two distinct graph edges yield a 2-colourable forest.
        for e1, e2 in combinations(list(combinations(range(4), 2)), 2):
            edges = {frozenset(e1), frozenset(e2)}
            self.assertTrue(any(
                all((int(u in left) != int(v in left)) for e in edges
                    for u,v in [tuple(e)])
                for mask in range(1 << 4)
                for left in [{i for i in range(4) if (mask >> i) & 1}]))
        # #20: common core for three-petal example, not for triangle of pairs.
        good = [{1,2},{1,3},{1,4}]
        bad = [{1,2},{2,3},{1,3}]
        pair_intersections = lambda fam: [a & b for a,b in combinations(fam,2)]
        self.assertTrue(all(x == {1} for x in pair_intersections(good)))
        self.assertEqual(len({frozenset(x) for x in pair_intersections(bad)}), 3)
        # #23, #24: 2-fold blown-up pentagon.
        n = 2
        vertices = tuple(range(5*n))
        edges = {
            frozenset((5*a+i, 5*b+j))
            for a in range(n) for b in range(n)
            for i in range(5) for j in range(5)
            if (j-i) % 5 in (1,4)
        }
        # Note class encoding: vertex=(copy index)*5+cycle position.
        self.assertEqual(len(edges), 5*n*n)
        self.assertFalse(any(
            all(frozenset(e) in edges for e in combinations(t, 2))
            for t in combinations(vertices, 3)))
        max_cut = max(sum(bool((mask>>u)&1) != bool((mask>>v)&1)
                          for edge in edges for u,v in [tuple(edge)])
                      for mask in range(1 << len(vertices)))
        self.assertEqual(max_cut, 4*n*n)
        self.assertEqual(len(edges)-max_cut, n*n)
        # Every 5-cycle counted once up to rotation and reversal.
        cycles = set()
        for cyc in permutations(vertices, 5):
            if all(frozenset((cyc[i], cyc[(i+1)%5])) in edges for i in range(5)):
                rotations = [cyc[i:]+cyc[:i] for i in range(5)]
                rev = cyc[::-1]
                rotations += [rev[i:]+rev[:i] for i in range(5)]
                cycles.add(min(rotations))
        self.assertEqual(len(cycles), n**5)

    def test_bulk_001_quality_sample_exact_and_full_manuscript_coverage(self):
        import random
        qa = json.loads((ROOT / "governance/erdos_compendium/batches/EC-BULK-001_QA.json").read_text(encoding="utf-8"))
        intake = json.loads((ROOT / "governance/erdos_compendium/batches/EC-BULK-001.json").read_text(encoding="utf-8"))
        self.assertEqual(qa["record_type"], "ERDOS_COMPENDIUM_BATCH_EDITORIAL_QA/1")
        self.assertEqual(qa["cohort_id"], intake["cohort_id"])
        self.assertEqual(qa["source_registry_blob"], intake["source_registry_blob"])
        self.assertIn("SELF_REVIEW", qa["review_kind"])
        ids = sorted(x["problem_id"] for x in intake["items"])
        self.assertEqual(len(ids), 50)
        self.assertEqual(
            qa["sample_problem_ids"],
            sorted(random.Random(int(hashlib.sha256(qa["sample_seed"].encode("utf-8")).hexdigest(),16)).sample(ids,10)))
        exceptions = set(qa["exception_problem_ids"])
        self.assertEqual(exceptions, {12, 15, 19, 23, 26, 38, 41, 522, 1112})
        selected = set(qa["sample_problem_ids"]) | exceptions
        self.assertEqual(selected, {x["problem_id"] for x in qa["reviewed"]})
        links = {x["problem_id"]: x["source_return"] for x in intake["items"]}
        for row in qa["reviewed"]:
            self.assertEqual(row["source_return"], links[row["problem_id"]])
            self.assertEqual(row["editorial_check"], "SOURCE_BOUNDED_PASS_WITH_DISCLOSED_LIMITS")
            self.assertGreaterEqual(len(row["finding"]), 30)
            if row["problem_id"] in exceptions:
                self.assertIn("EXCEPTION", row["selection"])
        for n in ids:
            # Verifies section contract + supported mathematical syntax for
            # ALL 50 articles, not just the sample or the 38 new sources.
            content = manuscript(n)
            self.assertIn("## The question in plain language", content)
            self.assertIn("## A small example", content)
            self.assertIn("## Sources and claim boundaries", content)
            self.assertIn(links[n], content,
                          f"Missing exact issue-comment source attribution for #{n}")
        self.assertIn("NO_MATH_CERTIFICATION", qa["disposition"])
        self.assertIn("Await protected PR merge", qa["publication_gate"])

    def test_bulk_001_exact_finite_examples(self):
        """Batch-level mathematical replay, not certification of asymptotic claims."""
        import itertools
        from fractions import Fraction
        from math import isqrt

        def prime(n):
            return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))

        def squarefree(n):
            return n > 0 and all(n % (p*p) for p in range(2, isqrt(n) + 1)
                                 if prime(p))

        # #6: four consecutive primes give three strictly increasing gaps.
        primes = [p for p in range(2, 102) if prime(p)]
        i = primes.index(17)
        self.assertEqual(primes[i:i+4], [17, 19, 23, 29])
        self.assertEqual([primes[j+1]-primes[j] for j in range(i, i+3)], [2, 4, 6])
        # #11: positive and zero-exponent witness semantics.
        self.assertTrue(squarefree(11-4))
        self.assertFalse(squarefree(11-2))
        self.assertTrue(squarefree(11-1))
        # #12: finite check for 88 points in historical/formal predicate countermodel.
        sq_primes = [p for p in range(5, 998) if prime(p) and p % 4 == 3]
        source = [3, 6] + [p*p for p in sq_primes]
        self.assertEqual((len(sq_primes), len(source)), (86, 88))
        bad = [(a,b,c) for a in source for j,b in enumerate(source)
               if a < b for c in source[j:] if a < c and (b+c) % a == 0]
        self.assertEqual(bad, [(3, 6, 6)])
        # #14, #30, #39: strict unordered sums, diagonal pairs included.
        def pair_sums(items):
            return [a+b for i,a in enumerate(items) for b in items[i:]]
        self.assertEqual(pair_sums([1,2,4]), [2,3,5,4,6,8])
        self.assertEqual(len(set(pair_sums([1,2,4]))), 6)
        self.assertEqual(len(set(pair_sums([1,2,4,8]))), 10)
        self.assertEqual(1+3, 2+2)  # #39 collision when diagonal is permitted
        # #15: adjacent prime-pair identity in exact rational arithmetic.
        self.assertEqual(-Fraction(1,2)+Fraction(2,3), Fraction(1,6))
        self.assertEqual(-Fraction(3,5)+Fraction(4,7), -Fraction(1,35))
        # #17: all primes up to 101 except 97 satisfy bounded cluster condition.
        noncluster = {}
        for p in primes:
            missing = [d for d in range(0, p-2, 2) if not
                       any(q+d <= p and prime(q+d) for q in primes if q <= p-d)]
            if missing:
                noncluster[p] = missing
        self.assertEqual(noncluster, {97:[88]})
        # #18: 8 is practical and 7 needs three distinct divisor powers.
        divisors = [1,2,4,8]
        minimum = {}
        for k in range(1,9):
            usable = [x for x in divisors if x <= k]
            minimum[k] = min(len(v) for r in range(1,len(usable)+1)
                             for v in itertools.combinations(usable,r) if sum(v) == k)
        self.assertEqual(max(minimum.values()), 3)
        self.assertEqual(minimum[7], 3)
        # #25: tail residues versus threshold exceptions.
        self.assertEqual([k for k in range(6) if k%2 != 0 and k%3 != 1], [3,5])
        self.assertLess(1, 2)  # 1 survives the threshold before residue exclusion
        # #32: 11 is not a prime plus either shift from {1,2}.
        self.assertFalse(prime(11-1))
        self.assertFalse(prime(11-2))
        # #36: exact balanced partition minima for two small instances.
        for n, expected in [(2,1),(3,2)]:
            universe = set(range(1,2*n+1))
            maxima = []
            for a in itertools.combinations(sorted(universe),n):
                b = universe - set(a)
                counts = {}
                for x in a:
                    for y in b:
                        counts[x-y] = counts.get(x-y,0)+1
                maxima.append(max(counts.values()))
            self.assertEqual(min(maxima), expected)
        # #40: ordered sum-pair multiplicities, which differ from #14.
        ordered = {}
        for a in [1,2,4]:
            for b in [1,2,4]:
                ordered[a+b] = ordered.get(a+b,0)+1
        self.assertEqual(ordered, {2:1,3:2,4:1,5:2,6:2,8:1})
        self.assertEqual(sum(ordered.values()), 9)
        # #41: subset-only triple test misses a multiset collision.
        self.assertEqual(sum((1,1,3)), sum((1,2,2)))
        self.assertEqual(len(list(itertools.combinations([1,2,3], 3))), 1)

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
