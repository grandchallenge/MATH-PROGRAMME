import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance/visual_pedagogy/batch1_live_switch.json"
RUNTIME = ROOT / "docs/javascripts/documentary.js"
REVIEW_REF = "https://github.com/grandchallenge/MATH-PROGRAMME/issues/429#issuecomment-5252274813"


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def test_batch1_live_switch_is_exact_and_review_bound():
    data = json.loads(RECORD.read_text(encoding="utf-8"))
    assert data["operation_id"] == "MP-DOC-VISUAL-PROPAGATION-BATCH1-LIVE-SWITCH-001"
    assert data["implementation_issue"] == 431
    assert data["review_issue"] == 429
    assert data["review_evidence"] == REVIEW_REF
    assert data["expected_plate_count"] == 6
    assert data["visual_is_evidence"] is False
    assert data["activation_mode"] == "shared_reader_exact_path_rewrite"
    assert len(data["plates"]) == 6

    runtime = RUNTIME.read_text(encoding="utf-8")
    ids = set()
    live_paths = set()
    predecessors = set()

    for plate in data["plates"]:
        ids.add(plate["plate_id"])
        live_paths.add(plate["live_path"])
        predecessors.add(plate["predecessor_path"])
        assert plate["review_outcome"] == "APPROVED"
        assert plate["live_path"] != plate["predecessor_path"]
        assert plate["source_reference"] != plate["live_reference"]

        predecessor = ROOT / plate["predecessor_path"]
        candidate = ROOT / plate["review_candidate_path"]
        live = ROOT / plate["live_path"]
        assert predecessor.is_file()
        assert candidate.is_file()
        assert live.is_file()
        assert live.read_bytes() == candidate.read_bytes()
        assert sha256(live) == plate["reviewed_digest"]

        assert runtime.count(repr(plate["source_reference"])) == 1
        assert runtime.count(repr(plate["live_reference"])) == 1

        contract_path = ROOT / "governance/visual_pedagogy/plates" / f"{plate['plate_id']}.json"
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        assert contract["independent_review"]["status"] == "reviewed"
        assert REVIEW_REF in contract["independent_review"]["evidence_refs"]
        assert contract["claim_boundary"]["visual_is_evidence"] is False
        assert contract["predecessor"] == plate["predecessor_path"]

    assert len(ids) == len(live_paths) == len(predecessors) == 6


def test_batch1_source_pages_keep_exact_rollback_references():
    data = json.loads(RECORD.read_text(encoding="utf-8"))
    docs = {
        "union_closed": (ROOT / "docs/documentaries/union_closed.md").read_text(encoding="utf-8"),
        "bsd": (ROOT / "docs/documentaries/bsd.md").read_text(encoding="utf-8"),
    }
    for plate in data["plates"]:
        assert plate["source_reference"] in docs[plate["reader"]]
        assert plate["live_reference"] not in docs[plate["reader"]]


def test_batch1_scope_does_not_activate_later_assets():
    runtime = RUNTIME.read_text(encoding="utf-8")
    assert runtime.count("dataset.visualPedagogyActivation") == 1
    assert runtime.count("visualPedagogyActivation = 'batch1'") == 1
    assert "plate_vorticity_v2" not in runtime
    assert "plate_geometry_v2" not in runtime
    assert "plate_gauge_v2" not in runtime
