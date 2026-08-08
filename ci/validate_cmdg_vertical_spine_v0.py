#!/usr/bin/env python3
"""Fail-closed validator for CMDG-VERTICAL-SPINE-V0-001."""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path
from typing import Any
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
P = ROOT.joinpath
RECORD=P('governance','cmdg_vertical_spine_v0_001.json'); NODES=P('fixtures','cmdg','vertical_spine_v0_001','nodes.json'); EDGES=P('fixtures','cmdg','vertical_spine_v0_001','edges.json')
NODE_SCHEMA=P('schemas','cmdg_node.schema.json'); EDGE_SCHEMA=P('schemas','cmdg_edge.schema.json')
FORMAL=P('fixtures','formal','CMDG-NAT-CONCORDANCE-001'); LEAN=FORMAL/'CMDGVerticalSpineV0.lean'; TOOLCHAIN=FORMAL/'lean-toolchain'; LAKE=FORMAL/'lake-manifest.json'
NAT_RECORD=P('governance','cmdg_nat_concordance_001.json'); EUCLID_RECORD=P('governance','cmdg_euclid_bridge_001.json')
NAT_NODES=P('fixtures','cmdg','nat_concordance_001','nodes.json'); EUCLID_NODES=P('fixtures','cmdg','euclid_bridge_001','nodes.json')
BASE='16a9e568e89cabbe989414ff8adb2599cdf24f5a'; BASE_TREE='dc464829ec5b798a922d059364dc5b40f577c12e'; LEAN_COMMIT='62eed1db4d67327ec8120be05f1a1b0847d74561'; MATHLIB='79d0395a1825a6264ad5d269e35e60537518955e'
BLOBS={'toolchain':'fd85b262bf1c734663aa8292b0101f672168788f','lake':'9e478e09f622406970dc9613f6cf323ade82f787','nat_record':'b06786dce9587149bdc6dba6bc32b037637dd379','euclid_record':'ebff50f400a68e4c45852aad45dbc1aabdee559c','nat_nodes':'955b593ae56accae2e71310c8cbc78842e0325ac','euclid_nodes':'1d58a548e549cf2751f4db32151d5c13af51ba86'}
NEW={'CMDG:V0:LEAN_SUBSTRATE','CMDG:V0:FOL_SEMANTICS','CMDG:V0:ALGEBRA_RING_INTERFACE','CMDG:V0:CATEGORY','CMDG:V0:TOPOLOGICAL_SPACES','CMDG:V0:COMPACT_HAUSDORFF','CMDG:V0:PROFINITE','CMDG:V0:GROTHENDIECK_TOPOLOGY','CMDG:V0:COHERENT_TOPOLOGY_COMPHAUS','CMDG:V0:SHEAF','CMDG:V0:CONDENSED_SET','CMDG:V0:DISCRETE_UNDERLYING_ADJUNCTION'}
SOURCES={'CMDG:V0:FOL_SEMANTICS':'Mathlib/ModelTheory/Semantics.lean','CMDG:V0:ALGEBRA_RING_INTERFACE':'Mathlib/Algebra/Category/Ring/Basic.lean','CMDG:V0:CATEGORY':'Mathlib/CategoryTheory/Category/Basic.lean','CMDG:V0:TOPOLOGICAL_SPACES':'Mathlib/Topology/Category/TopCat/Basic.lean','CMDG:V0:COMPACT_HAUSDORFF':'Mathlib/Topology/Category/CompHaus/Basic.lean','CMDG:V0:PROFINITE':'Mathlib/Topology/Category/Profinite/Basic.lean','CMDG:V0:GROTHENDIECK_TOPOLOGY':'Mathlib/CategoryTheory/Sites/Grothendieck.lean','CMDG:V0:COHERENT_TOPOLOGY_COMPHAUS':'Mathlib/Condensed/Basic.lean','CMDG:V0:SHEAF':'Mathlib/CategoryTheory/Sites/Sheaf.lean','CMDG:V0:CONDENSED_SET':'Mathlib/Condensed/Basic.lean','CMDG:V0:DISCRETE_UNDERLYING_ADJUNCTION':'Mathlib/Condensed/Discrete/Basic.lean'}
TRACES=[['CMDG:V0:DISCRETE_UNDERLYING_ADJUNCTION','CMDG:V0:CONDENSED_SET','CMDG:V0:SHEAF','CMDG:V0:GROTHENDIECK_TOPOLOGY','CMDG:V0:CATEGORY'],['CMDG:V0:CONDENSED_SET','CMDG:V0:COHERENT_TOPOLOGY_COMPHAUS','CMDG:V0:COMPACT_HAUSDORFF','CMDG:V0:TOPOLOGICAL_SPACES','CMDG:V0:CATEGORY'],['CMDG:V0:PROFINITE','CMDG:V0:COMPACT_HAUSDORFF','CMDG:V0:TOPOLOGICAL_SPACES','CMDG:V0:CATEGORY'],['CMDG:V0:ALGEBRA_RING_INTERFACE','CMDG:V0:CATEGORY']]
SEM={'CMDG:E:V0.RINGCAT.CATEGORY','CMDG:E:V0.TOPCAT.CATEGORY','CMDG:E:V0.COMPHAUS.TOPCAT','CMDG:E:V0.PROFINITE.COMPHAUS','CMDG:E:V0.COHERENT.COMPHAUS','CMDG:E:V0.COHERENT.GROTHENDIECK','CMDG:E:V0.GROTHENDIECK.CATEGORY','CMDG:E:V0.SHEAF.GROTHENDIECK','CMDG:E:V0.SHEAF.CATEGORY','CMDG:E:V0.CONDENSED.SHEAF','CMDG:E:V0.CONDENSED.COHERENT','CMDG:E:V0.DISCRETE.CONDENSED'}
CHECKS=['#check FirstOrder.Language','#check RingCat','#check CategoryTheory.Category','#check TopCat','#check CompHaus','#check Profinite','#check CategoryTheory.GrothendieckTopology','#check CategoryTheory.Sheaf','#check CategoryTheory.coherentTopology','#check Condensed','#check CondensedSet','#check Condensed.discrete','#check Condensed.underlying','#check Condensed.discreteUnderlyingAdj']

class V0Error(RuntimeError):
    def __init__(self, code:str, msg:str): super().__init__(f'{code}: {msg}'); self.code=code; self.message=msg
def reject(code:str,msg:Any): raise V0Error(code,str(msg))
def load(path:Path):
    try: return json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc: reject('JSON_LOAD_FAILED',f'{path}: {exc}')
def blob(path:Path):
    data=path.read_bytes(); return hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
def schema(value:Any,path:Path,code:str):
    errs=sorted(Draft202012Validator(load(path)).iter_errors(value),key=lambda e:list(e.path))
    if errs: reject(code,errs[0].message)

def validate_payload(record:dict[str,Any], nodes:list[dict[str,Any]], edges:list[dict[str,Any]], lean_text:str)->None:
    if record.get('schema_version')!='1.0.0' or record.get('operation_id')!='CMDG-VERTICAL-SPINE-V0-001': reject('OPERATION_IDENTITY_DRIFT',record.get('operation_id'))
    if (record.get('protected_baseline'),record.get('protected_baseline_tree'))!=(BASE,BASE_TREE): reject('AUTHORITY_BASELINE_DRIFT','baseline/tree')
    if record.get('predecessor_disposition')!='CMDG_EUCLID_BRIDGE_001_PROTECTED_CLOSED': reject('PREDECESSOR_DISPOSITION_DRIFT',record.get('predecessor_disposition'))
    env=record.get('environment',{}); expected={'lean_toolchain':'leanprover/lean4:v4.33.0-rc1','lean_commit':LEAN_COMMIT,'toolchain_blob_sha1':BLOBS['toolchain'],'lake_manifest_blob_sha1':BLOBS['lake'],'mathlib_repository':'leanprover-community/mathlib4','mathlib_commit':MATHLIB}
    if env!=expected: reject('PROOF_ENVIRONMENT_DRIFT',env)
    reuse={x.get('node_id'):x for x in record.get('protected_reuse',[])}
    if set(reuse)!={'CMDG:NAT:N_DTT','CMDG:EUCLID:GCD:E2E001'}: reject('PROTECTED_REUSE_SET_DRIFT',sorted(reuse))
    n=reuse['CMDG:NAT:N_DTT']; e=reuse['CMDG:EUCLID:GCD:E2E001']
    if (n.get('artifact_blob_sha1'),n.get('node_fixture_blob_sha1'))!=(BLOBS['nat_record'],BLOBS['nat_nodes']): reject('NAT_REUSE_IDENTITY_DRIFT',n)
    if (e.get('artifact_blob_sha1'),e.get('node_fixture_blob_sha1'))!=(BLOBS['euclid_record'],BLOBS['euclid_nodes']): reject('EUCLID_REUSE_IDENTITY_DRIFT',e)
    if any(x.get('authority')!='PROTECTED_REUSE_NO_REDEFINITION' for x in reuse.values()): reject('PROTECTED_AUTHORITY_REDEFINITION','protected anchors')
    ids=set()
    for node in nodes:
        schema(node,NODE_SCHEMA,'NODE_SCHEMA_VIOLATION'); nid=node['node_id']
        if nid in ids: reject('DUPLICATE_NODE',nid)
        ids.add(nid)
    if ids!=NEW: reject('V0_NODE_SET_DRIFT',sorted(ids^NEW))
    modes={x['node_id']:x.get('engagement_mode') for x in nodes}
    if any(v not in {'REUSED','RECONSTRUCTED','CONCORDANT'} for v in modes.values()): reject('UNCLASSIFIED_REUSE_MODE',modes)
    if modes['CMDG:V0:CONDENSED_SET']!='CONCORDANT' or modes['CMDG:V0:DISCRETE_UNDERLYING_ADJUNCTION']!='CONCORDANT': reject('CONDENSED_CONCORDANCE_OVERCLAIM',modes)
    if any(modes[x]!='REUSED' for x in NEW-{'CMDG:V0:CONDENSED_SET','CMDG:V0:DISCRETE_UNDERLYING_ADJUNCTION'}): reject('REUSE_CLASSIFICATION_DRIFT',modes)
    if {x.get('node_id'):x.get('path') for x in record.get('source_catalog',[])}!=SOURCES: reject('SOURCE_CATALOG_DRIFT','catalog')
    route=record.get('route',{}); ordered=route.get('ordered_nodes',[])
    if not ordered or ordered[0]!='CMDG:V0:LEAN_SUBSTRATE' or ordered[-1]!='CMDG:V0:DISCRETE_UNDERLYING_ADJUNCTION': reject('BROKEN_V0_ROUTE',ordered)
    if route.get('start_node')!=ordered[0] or route.get('terminal_node')!=ordered[-1]: reject('V0_ENDPOINT_DRIFT','endpoints')
    if route.get('ordering_authoritative') is not False: reject('ROUTE_ORDER_AUTHORITY_OVERCLAIM','ordering')
    if len(ordered)!=len(set(ordered)): reject('DUPLICATE_ROUTE_NODE',ordered)
    if set(ordered)!=(NEW|{'CMDG:NAT:N_DTT'}): reject('ROUTE_NODE_COVERAGE_DRIFT',sorted(set(ordered)^(NEW|{'CMDG:NAT:N_DTT'})))
    if route.get('dependency_backtraces')!=TRACES: reject('DEPENDENCY_BACKTRACE_DRIFT',route.get('dependency_backtraces'))
    emap={}
    for edge in edges:
        schema(edge,EDGE_SCHEMA,'EDGE_SCHEMA_VIOLATION'); eid=edge['edge_id']
        if eid in emap: reject('DUPLICATE_EDGE',eid)
        emap[eid]=edge
        if edge['layer']=='G_semantic':
            if edge['authority_state']!='PROPOSED': reject('UNREVIEWED_SEMANTIC_AUTHORITY',eid)
            if edge.get('proposal_origin',{}).get('origin')!='HUMAN': reject('TOOL_ORIGIN_SEMANTIC_AUTHORITY',eid)
            if edge['relation']=='EQUIVALENT_TO': reject('UNCERTIFIED_EQUIVALENCE_IN_V0',eid)
            if edge['relation']=='REALIZES_AS': reject('FOUNDATIONAL_REALIZATION_PROMOTION',eid)
        elif edge['authority_state']!='OBSERVED': reject('NONSEMANTIC_AUTHORITY_DRIFT',eid)
        if edge['authority_state']=='DERIVED': reject('DERIVED_EDGE_AS_DIRECT_AUTHORITY',eid)
    semantic={x['edge_id'] for x in edges if x['layer']=='G_semantic'}
    if semantic!=SEM: reject('SEMANTIC_EDGE_SET_DRIFT',sorted(semantic^SEM))
    if not {'G_semantic','G_proof','G_implementation','G_provenance'}<={x['layer'] for x in edges}: reject('GRAPH_LAYER_COVERAGE_INCOMPLETE','layers')
    pairs={(x['source']['identity'],x['target']['identity']) for x in edges if x['layer']=='G_semantic'}
    for trace in TRACES:
        for pair in zip(trace,trace[1:]):
            if pair not in pairs: reject('BROKEN_SEMANTIC_BACKTRACE',f'{pair[0]} -> {pair[1]}')
    trust=record.get('trust_boundary',{})
    if trust.get('policy')!='PINNED_EXTERNAL_SOURCE_REUSE' or trust.get('all_reused_nodes_declared') is not True: reject('TRUST_BOUNDARY_INCOMPLETE',trust)
    if trust.get('unclassified_external_nodes_allowed') is not False: reject('UNCLASSIFIED_EXTERNAL_TRUST_ALLOWED',trust)
    if trust.get('semantic_reconciler_may_confer_authority') is not False: reject('SEMANTIC_RECONCILER_AUTHORITY_PROMOTION',trust)
    c04=record.get('condensed_target_profile',{})
    if c04.get('formal_target')!='CondensedSet.{u} := Sheaf (coherentTopology CompHaus.{u}) (Type (u + 1))': reject('CONDENSED_TARGET_IDENTITY_DRIFT',c04.get('formal_target'))
    if c04.get('formal_target_revision')!=MATHLIB: reject('CONDENSED_TARGET_PIN_DRIFT',c04.get('formal_target_revision'))
    if c04.get('formal_cardinality_policy')!='NO_CARDINALITY_BOUND': reject('CONDENSED_CARDINALITY_PROFILE_MISSING',c04.get('formal_cardinality_policy'))
    if c04.get('formal_source_characterization')!='CLOSER_TO_PYKNOTIC_OBJECTS': reject('PYKNOTIC_BOUNDARY_MISSING',c04.get('formal_source_characterization'))
    if c04.get('concordance_status')!='PARTIAL_INTERFACE_ONLY': reject('CONDENSED_FULL_CONCORDANCE_OVERCLAIM',c04.get('concordance_status'))
    if c04.get('cm_scope')!='CM0_CM1_INTERFACE_ONLY': reject('CONDENSED_CM_SCOPE_OVERCLAIM',c04.get('cm_scope'))
    if c04.get('c04_status')!='ADVANCED_FOR_V0_TERMINAL_PROFILE_NOT_GLOBALLY_DISCHARGED': reject('C04_STATUS_OVERCLAIM',c04.get('c04_status'))
    if c04.get('terminal_interface')!={'discrete':'Condensed.discrete','underlying':'Condensed.underlying','adjunction':'Condensed.discreteUnderlyingAdj','module':'Mathlib/Condensed/Discrete/Basic.lean'}: reject('TERMINAL_INTERFACE_DRIFT',c04.get('terminal_interface'))
    graph=record.get('graph',{})
    if graph.get('semantic_edge_authority')!='PROPOSED_PENDING_INDEPENDENT_EXACT_HEAD_REVIEW_AND_PROTECTED_ADMISSION': reject('SEMANTIC_AUTHORITY_STATE_DRIFT',graph)
    if graph.get('derived_closure_authoritative') is not False or graph.get('graph_certified') is not False: reject('GRAPH_AUTHORITY_OVERCLAIM',graph)
    cb=record.get('claim_boundary',{})
    for key in ['v0_unique_or_minimal','foundational_equivalence_conferred','syntactic_zfc_realization_conferred','all_domains_fully_formalized','condensed_full_concordance_conferred','cm2_or_stronger_conferred','global_dependency_completeness_claim','graph_certified_conferred','c05_discharged','c06_discharged']:
        if cb.get(key) is not False: reject('PROHIBITED_AUTHORITY_PROMOTION',key)
    if cb.get('independent_review_required') is not True or cb.get('protected_admission_required') is not True: reject('ADMISSION_GATE_BYPASS',cb)
    if record.get('candidate_disposition')!='V0_CANDIDATE_PENDING_INDEPENDENT_REVIEW': reject('CANDIDATE_DISPOSITION_DRIFT',record.get('candidate_disposition'))
    if re.search(r'^[ \t]*(sorry|axiom)(?:[ \t]|$)',lean_text,re.M): reject('FORMAL_INTERFACE_PLACEHOLDER_OR_AXIOM','sorry/axiom')
    for check in CHECKS:
        if check not in lean_text: reject('FORMAL_INTERFACE_CHECK_MISSING',check)

def validate_repository()->None:
    if (blob(TOOLCHAIN),blob(LAKE))!=(BLOBS['toolchain'],BLOBS['lake']): reject('PINNED_FORMAL_ENVIRONMENT_DRIFT','toolchain/lake')
    if (blob(NAT_RECORD),blob(EUCLID_RECORD))!=(BLOBS['nat_record'],BLOBS['euclid_record']): reject('PROTECTED_REGRESSION_RECORD_DRIFT','records')
    if (blob(NAT_NODES),blob(EUCLID_NODES))!=(BLOBS['nat_nodes'],BLOBS['euclid_nodes']): reject('PROTECTED_REGRESSION_NODE_DRIFT','nodes')
    validate_payload(load(RECORD),load(NODES),load(EDGES),LEAN.read_text(encoding='utf-8'))

def main()->int:
    try: validate_repository()
    except V0Error as exc:
        print(f'CMDG V0 validation FAILED [{exc.code}]: {exc.message}'); return 1
    print('CMDG V0 validation PASS')
    print('scope: demonstration/certified spine candidate; C04 bounded; C05/C06 and GRAPH_CERTIFIED remain open')
    return 0
if __name__=='__main__': raise SystemExit(main())
