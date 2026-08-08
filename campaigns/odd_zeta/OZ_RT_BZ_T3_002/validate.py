#!/usr/bin/env python3
from __future__ import annotations
import hashlib, importlib.util, json, sys
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
RECORD=HERE/'OZ_RT_BZ_T3_002.json'; SCHEMA=HERE/'OZ_RT_BZ_T3_002.schema.json'; RESULT=HERE/'SEARCH_RESULT.json'

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def canonical_sha256(value):
    raw=json.dumps(value,sort_keys=True,separators=(',',':')).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()
def errors(record=None, result=None):
    record=load(RECORD) if record is None else record; result=load(RESULT) if result is None else result
    out=[f'schema{e.json_path}: {e.message}' for e in Draft202012Validator(load(SCHEMA)).iter_errors(record)]
    a=record.get('authority',{})
    expected={'programme_base_commit':'bb4bf555e4569e08818a1fb06017ad97543e884d','predecessor_merge':'b98d5ba79439e7ef7ee6493604bcfc40f9422dd8','admitted_source_head':'6cc0bf07137815ceeef0d9f340559f85352391e5','admitted_source_tree':'be780558454b704bdd016a3070d698c2e106e2b8'}
    for k,v in expected.items():
        if a.get(k)!=v: out.append(f'authority drift: {k}')
    loci=a.get('source_loci',{})
    blobs={'statement':'da46db62471fbed81d861772c1d2d03d80782e23','bridge':'002c96d28123e5949c38656f26677ae5a723ee93','finite_verifier':'be458d969e1f8c989c8007a2b181506f84fd7f48','recurrence':'9495275bc31e5a8f535c68f027f3b24d12c07ae1','weights':'b6129348c96ff061441403445ca9a278be252afd','rational_part':'a54fabc29f910eada2ecf17fbbdc99f4c22aa06b','nested_sums':'a31d36d291fcc4efc42c210f4b524f1f265cdeab','exact_evaluator':'80abbb21e4133a19d12b510c1a4d6b962e030e24'}
    for k,v in blobs.items():
        if loci.get(k,{}).get('blob')!=v: out.append(f'source blob drift: {k}')
    target=record.get('target_lock',{})
    if 'W1(k,l)+2*w5_sym(n,k,l)' not in target.get('normalized_zero_form',''): out.append('T3 representative drift')
    if target.get('finite_evidence_theorem_effect')!='NONE': out.append('finite evidence promoted')
    search=record.get('search_execution',{})
    digest=canonical_sha256(result)
    if search.get('result_sha256')!=digest: out.append('search result digest drift')
    if search.get('strongest_frontier')!={'degree':6,'equations':65,'unknowns':56,'rank':56,'nullity':0}: out.append('strongest frontier drift')
    if result.get('terminal')!='NO_CERTIFICATE_IN_BOUNDED_CLASS' or result.get('proof_effect')!='NONE': out.append('search result inflation')
    spec=importlib.util.spec_from_file_location('oz_t3_002_verify',HERE/'verify.py'); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod)
    out.extend('independent verifier: '+x for x in mod.verify(result))
    disp=record.get('disposition',{})
    if disp.get('status')!='OPEN_WITH_CHARACTERIZED_BLOCKER' or disp.get('proof_found') or disp.get('counterexample_found'): out.append('disposition inflation')
    if any(record.get('nonclaims',{}).values()): out.append('nonclaim promoted')
    return out

def main():
    e=errors()
    if e:
        print('\n'.join(e),file=sys.stderr); return 1
    print('OZ-RT-BZ-T3-002 bounded certificate search and independent verification are valid')
    return 0
if __name__=='__main__': raise SystemExit(main())
