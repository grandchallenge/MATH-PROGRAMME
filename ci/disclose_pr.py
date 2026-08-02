#!/usr/bin/env python3
"""Render or validate the bounded GCL-DISCLOSE-PR-001 control surface."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from typing import Any
from jsonschema import Draft202012Validator
from disclose_evaluate import evaluate,load
from disclose_render import generated
ROOT=Path(__file__).resolve().parents[1]
FIXTURE=Path("disclosure/fixtures/GCL-DISCLOSE-PR-001")
SCHEMAS={"contract":"schemas/gcl_disclosure_product.schema.json","manifest":"schemas/gcl_disclosure_manifest.schema.json","reviews":"schemas/gcl_disclosure_review_evidence.schema.json","ledger":"schemas/gcl_disclosure_disposition_ledger.schema.json"}
OFFICES={"Axiomatist","Cartographer","Verifier","Adversary","Formalist","Amanuensis","Referee","Human Steward"}
DISPOSITIONS={"open_scientific_infrastructure","ordinary_publication","defensive_publication","patent_review_candidate","trade_secret","internal_method","benchmark_or_dataset_asset","commercial_implementation","no_external_release"}
def schema_errors(value:Any,schema:Any,label:str)->list[str]:return [f"{label}{e.json_path}: {e.message}" for e in sorted(Draft202012Validator(schema).iter_errors(value),key=lambda e:list(e.path))]
def validate(root:Path=ROOT)->list[str]:
    try:
        contract=load(root/"disclosure/product_contract.json");manifest=load(root/FIXTURE/"manifest.json");reviews=load(root/FIXTURE/manifest["evidence_files"]["reviews"]);ledger=load(root/"disclosure/disposition_ledger.json");recorded=load(root/"disclosure/measurement_ledger.json");schemas={k:load(root/v) for k,v in SCHEMAS.items()}
    except (OSError,json.JSONDecodeError,KeyError) as exc:return [f"disclosure load failed: {exc}"]
    errors=[]
    for label,value,key in (("contract",contract,"contract"),("manifest",manifest,"manifest"),("review evidence",reviews,"reviews"),("disposition ledger",ledger,"ledger")):errors+=schema_errors(value,schemas[key],label)
    if errors:return errors
    if set(contract["activation"]["required_conditions"])!={"external_exact_head_review","human_steward_release","protected_merge"}:errors.append("activation conditions drifted")
    if {x["office"] for x in contract["review_packet"]}!=OFFICES or any(x["may_self_authenticate"] or x["status"]!="pending_external_review" for x in contract["review_packet"]):errors.append("review packet must contain the exact non-self-authenticating eight offices")
    if any(contract["claim_boundaries"].values()):errors.append("claim-boundary promotion is prohibited")
    if set(ledger["supported_dispositions"])!=DISPOSITIONS:errors.append("disposition ledger must cover the exact nine required dispositions")
    if ledger["external_release_authorized"]:errors.append("disposition ledger cannot authorize external release")
    expected={x["finding_id"]:(x["disposition"],x["reason_code"]) for x in manifest["expected_findings"]};d=evaluate(root/FIXTURE);actual={x["finding_id"]:(x["disposition"],x["reason_code"]) for x in d["findings"]}
    if len(expected)!=len(manifest["expected_findings"]) or actual!=expected:errors.append("bounded disclosure findings do not match the protected expectation ledger")
    if d["overall_disposition"]!="FAIL":errors.append("mixed adversarial disclosure fixture must remain overall FAIL")
    if manifest["data_classification"]!="synthetic_public" or not contract["core_contract"]["synthetic_public_only"]:errors.append("Tranche 1 must remain synthetic-public only")
    b=recorded.get("bounded_classification",{});r=recorded.get("partial_evidence_recovery",{})
    if b.get("case_count")!=len(expected) or b.get("exact_match_count")!=len(expected) or b.get("false_positive_count")!=0 or b.get("false_negative_count")!=0:errors.append("measurement ledger does not match bounded disclosure characterization")
    if not recorded.get("deterministic_replay",{}).get("byte_identical") or r.get("expected_disposition")!="ABSTAIN" or not r.get("crash_free") or not r.get("implicit_clearance_forbidden"):errors.append("deterministic or partial-evidence recovery contract drifted")
    first,second=generated(root),generated(root)
    if first!=second:errors.append("deterministic replay mismatch")
    for path,text in first.items():
        if not path.is_file() or path.read_text(encoding="utf-8")!=text:errors.append(f"generated output drift {path.relative_to(root)}")
    return errors
def render(root:Path=ROOT)->int:
    for path,text in generated(root).items():path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding="utf-8");print(f"rendered {path.relative_to(root)}")
    return 0
def check(root:Path=ROOT)->int:
    errors=validate(root)
    if errors:
        for error in errors:print(error,file=sys.stderr)
        print(f"GCL-DISCLOSE-PR-001 failed with {len(errors)} error(s)",file=sys.stderr);return 1
    print("GCL-DISCLOSE-PR-001 valid: deterministic synthetic disclosure dossier, ledgers, and review packet");return 0
def main()->int:
    parser=argparse.ArgumentParser();parser.add_argument("command",choices=("render","check"));args=parser.parse_args();return render() if args.command=="render" else check()
if __name__=="__main__":raise SystemExit(main())
