#!/usr/bin/env python3
"""Fail-closed validator for CMDG-EUCLID-BRIDGE-001."""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path
from typing import Any
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
P = lambda *x: ROOT.joinpath(*x)
RECORD=P("governance","cmdg_euclid_bridge_001.json"); NODES=P("fixtures","cmdg","euclid_bridge_001","nodes.json"); EDGES=P("fixtures","cmdg","euclid_bridge_001","edges.json")
NODE_SCHEMA=P("schemas","cmdg_node.schema.json"); EDGE_SCHEMA=P("schemas","cmdg_edge.schema.json")
SOURCE=P("fixtures","formal","CMDG-NAT-CONCORDANCE-001","CMDGEuclidBridge.lean"); TOOL=P("fixtures","formal","CMDG-NAT-CONCORDANCE-001","lean-toolchain"); MAN=P("fixtures","formal","CMDG-NAT-CONCORDANCE-001","lake-manifest.json")
CLOSE=P("governance","euclid_gcd_e2e_001_closeout.json"); OCFG=P("fixtures","cmdg","extractor_001","euclid_gcd_original.json"); BCFG=P("fixtures","cmdg","extractor_001","euclid_bridge.json"); WF=P(".github","workflows","cmdg-euclid-bridge.yml")
BASE="25f5fef222433f60f28b375d6ea814b844b5b062"; CLOSE_BLOB="a5e390ee01b23862a79d53a7cac1c0d6f0930608"; MC="78b69e6a3461a83f4893d61c421b1570c08a9ba6"; MC_SRC="bf0ab5bac117490299ff5bffb8ca59263ec3f2a3"
OT="33e0c088939ad08c9f2b1befa3118a423b06ad7d"; OM="4d92c79ff638dceb6c44472e1e96bbac9cebcdfd"; BT="fd85b262bf1c734663aa8292b0101f672168788f"; BM="9e478e09f622406970dc9613f6cf323ade82f787"; ML="79d0395a1825a6264ad5d269e35e60537518955e"
ROOTS=["MathCert.NumberTheory.acceptedGCDCertificate_sound","MathCert.NumberTheory.euclidTrace252105","MathCert.NumberTheory.bezout252105","MathCert.NumberTheory.gcd252105","MathCert.NumberTheory.accepted252105","MathCert.NumberTheory.accepted252105_sound"]
BROOT="CMDG.EuclidBridge.euclid_gcd_relational_bridge"; OPS=["ZERO","SUCCESSOR","ADDITION","MULTIPLICATION","ORDER","DIVISIBILITY"]

class BridgeError(RuntimeError):
    def __init__(self, code:str, message:str): super().__init__(f"{code}: {message}"); self.code=code; self.message=message
def reject(c,m): raise BridgeError(c,m)
def load(p):
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e: reject("JSON_LOAD_FAILED",f"{p}: {e}")
def blob(p):
    b=p.read_bytes(); return hashlib.sha1(f"blob {len(b)}\0".encode()+b).hexdigest()
def schema(v,p,c):
    es=sorted(Draft202012Validator(load(p)).iter_errors(v),key=lambda e:list(e.path))
    if es: reject(c,es[0].message)

def validate_record(r:dict[str,Any])->None:
    if r.get("operation_id")!="CMDG-EUCLID-BRIDGE-001" or r.get("protected_baseline")!=BASE: reject("AUTHORITY_BASELINE_DRIFT",str(r.get("protected_baseline")))
    a=r["euclid_authority"]
    if a["programme_closeout_blob_sha1"]!=CLOSE_BLOB or blob(CLOSE)!=CLOSE_BLOB: reject("EUCLID_CLOSEOUT_IDENTITY_DRIFT",blob(CLOSE))
    if a["mathcert_merge_commit"]!=MC or a["mathcert_source_blob_sha1"]!=MC_SRC: reject("MATHCERT_SOURCE_IDENTITY_DRIFT",str(a))
    if a["roots"]!=ROOTS: reject("EUCLID_THEOREM_ROOT_DRIFT",str(a["roots"]))
    if r["original_proof_environment"]!={"lean_toolchain":"leanprover/lean4:v4.29.1","toolchain_blob_sha1":OT,"lake_manifest_blob_sha1":OM,"mathcert_commit":MC}: reject("ORIGINAL_ENVIRONMENT_DRIFT",str(r["original_proof_environment"]))
    b=r["bridge_proof_environment"]
    if blob(TOOL)!=BT or blob(MAN)!=BM: reject("BRIDGE_ENVIRONMENT_PIN_DRIFT","local pins changed")
    if (b["toolchain_blob_sha1"],b["lake_manifest_blob_sha1"],b["mathlib_commit"],b["root"])!=(BT,BM,ML,BROOT): reject("BRIDGE_RECORDED_PIN_DRIFT",str(b))
    s=r["semantic_scope"]
    if s["transport_route"]!=["N_DTT","N_NNO","N_ZFC"]: reject("TRANSPORT_DIRECTION_DRIFT",str(s["transport_route"]))
    if s["admitted_operation_dependencies"]!=OPS: reject("NAT_OPERATION_SCOPE_DRIFT",str(s["admitted_operation_dependencies"]))
    if s["transported_objects"]!=["RELATIONAL_GCD_SPECIFICATION","EUCLIDEAN_TRACE_252_105"]: reject("TRANSPORT_OBJECT_SCOPE_DRIFT",str(s["transported_objects"]))
    if s["gcd_function_transport"]!="NOT_ADMITTED": reject("GCD_FUNCTION_TRANSPORT_OVERCLAIM",s["gcd_function_transport"])
    if s["bezout_integer_transport"]!="OUT_OF_SCOPE_PENDING_INTEGER_CONCORDANCE": reject("INTEGER_BEZOUT_TRANSPORT_OVERCLAIM",s["bezout_integer_transport"])
    if s["zfc_scope"]!="FINITE_VON_NEUMANN_IMAGE_ONLY": reject("SYNTACTIC_ZFC_OVERCLAIM",s["zfc_scope"])
    text=SOURCE.read_text(encoding="utf-8")
    for q in ["def DTTIsGCD","def NNOIsGCD","def ZFCFiniteImageIsGCD","theorem dtt_to_nno_gcd","theorem nno_to_zfc_finite_image_gcd","theorem dtt_gcd_252_105_21","theorem dtt_trace_252_105","theorem nno_trace_252_105","theorem zfc_finite_image_trace_252_105","theorem euclid_gcd_relational_bridge"]:
        if q not in text: reject("FORMAL_BRIDGE_DECLARATION_MISSING",q)
    if re.search(r"^[ \t]*(sorry|axiom)(?:[ \t]|$)",text,re.M): reject("FORMAL_PLACEHOLDER_OR_AXIOM","sorry/axiom")
    if re.search(r"theorem\s+\w*bezout",text,re.I): reject("INTEGER_BEZOUT_SCOPE_VIOLATION","local Bezout theorem")
    if r["formal_bridge"]["root"]!=BROOT or r["formal_bridge"]["source"]!=str(SOURCE.relative_to(ROOT)): reject("FORMAL_BINDING_DRIFT",str(r["formal_bridge"]))
    nodes=load(NODES); edges=load(EDGES); seen=set()
    for n in nodes:
        schema(n,NODE_SCHEMA,"NODE_SCHEMA_VIOLATION")
        if n["node_id"] in seen: reject("DUPLICATE_NODE",n["node_id"])
        seen.add(n["node_id"])
    seen=set()
    for e in edges:
        schema(e,EDGE_SCHEMA,"EDGE_SCHEMA_VIOLATION")
        if e["edge_id"] in seen: reject("DUPLICATE_EDGE",e["edge_id"])
        seen.add(e["edge_id"])
        if e["layer"] in {"G_semantic","CROSS_LAYER"} and e["authority_state"]!="PROPOSED": reject("UNREVIEWED_SEMANTIC_AUTHORITY",e["edge_id"])
        if e["layer"] in {"G_proof","G_implementation","G_provenance"} and e["authority_state"]!="OBSERVED": reject("NONSEMANTIC_AUTHORITY_DRIFT",e["edge_id"])
        if e["relation"]=="REALIZES_AS" and any(e["realization"]["automatic_claims"].values()): reject("REALIZATION_AUTOMATIC_OVERCLAIM",e["edge_id"])
    if r["graph"]["semantic_edge_authority"]!="PROPOSED" or r["graph"]["derived_closure_authoritative"]: reject("GRAPH_BINDING_DRIFT",str(r["graph"]))
    oc=load(OCFG); bc=load(BCFG)
    if oc["project_dir"]!="external/MATHCERT" or oc["roots"]!=ROOTS: reject("ORIGINAL_EXTRACTOR_ROOT_DRIFT",str(oc["roots"]))
    if (oc["expected_toolchain_git_blob_sha1"],oc["expected_lake_manifest_git_blob_sha1"])!=(OT,OM): reject("ORIGINAL_EXTRACTOR_PIN_DRIFT","pins")
    if bc["roots"]!=[BROOT] or bc["module"]!="CMDGEuclidBridge": reject("BRIDGE_EXTRACTOR_ROOT_DRIFT",str(bc["roots"]))
    if (bc["expected_toolchain_git_blob_sha1"],bc["expected_lake_manifest_git_blob_sha1"])!=(BT,BM): reject("BRIDGE_EXTRACTOR_PIN_DRIFT","pins")
    if any(any(c["claim_boundary"].values()) for c in (oc,bc)): reject("EXTRACTOR_AUTHORITY_PROMOTION","boundary")
    wf=WF.read_text(encoding="utf-8")
    for q in (MC,MC_SRC,"euclid_gcd_original.json","euclid_bridge.json"):
        if q not in wf: reject("WORKFLOW_AUTHORITY_BINDING_MISSING",q)
    cb=r["claim_boundary"]
    for k in ["original_euclid_certification_modified","new_or_stronger_gcd_theorem_conferred","nat_gcd_function_transport_conferred","integer_bezout_transport_conferred","syntactic_zfc_realization_conferred","foundational_equivalence_conferred","dependency_minimality_claim","global_dependency_completeness_claim","graph_certified_conferred"]:
        if cb[k]: reject("PROHIBITED_AUTHORITY_PROMOTION",k)
    if not cb["independent_review_required"] or not cb["protected_admission_required"]: reject("ADMISSION_GATE_BYPASS","review/protected admission")
    if not cb["c04_c05_c06_unchanged"]: reject("UNRELATED_CORRECTION_GATE_DRIFT","C04-C06")

def main():
    try: validate_record(load(RECORD))
    except BridgeError as e: print(f"CMDG Euclid bridge validation FAILED [{e.code}]: {e.message}"); return 1
    print("CMDG Euclid bridge validation PASS"); print("scope: relational gcd + trace only; Nat.gcd-function and Int-Bezout transport excluded"); return 0
if __name__=="__main__": raise SystemExit(main())
