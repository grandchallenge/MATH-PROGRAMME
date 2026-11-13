#!/usr/bin/env python3
"""Fail-closed structural/claim-boundary checks for source-locked Erdős verification."""
from __future__ import annotations
import json
from pathlib import Path
import re
import sys
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = 'governance/erdos_proof_verification/registry.json'
SCHEMA = 'schemas/erdos_proof_verification_manifest.schema.json'
STAGES = ['SOURCE_LOCK','STATEMENT_EQUIVALENCE','REPLAY_PREPARATION','REPLAY_EXECUTION','ADVERSARIAL_REVIEW','INTERNAL_ADJUDICATION','PROTECTED_EVIDENCE_ADMISSION']


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load(path: str, root: Path = ROOT) -> dict:
    p = (root / path).resolve()
    require(p.is_relative_to(root.resolve()) and p.is_file(), f'missing/escaped: {path}')
    return json.loads(p.read_text(encoding='utf-8'))


def validate_manifest(data: dict, schema: dict) -> None:
    jsonschema.Draft202012Validator(schema).validate(data)
    n = data['problem_id']
    require(data['manifest_id'] == f'ERDOS-PV-{n:04}-S01', f'identity mismatch: {n}')
    require(data['governing_issue'] == 3201, f'wrong parent: {n}')
    require(data['source_audit_issue'] != data['verification_issue'], f'self-loop: {n}')
    require(data['verification_issue'] != data['governing_issue'], f'parent-self-loop: {n}')
    s = data['source_locks']
    require(s['catalogue_entry'] == str(n), f'catalogue entry mismatch: {n}')
    require(s['formal_path'].endswith(f'/{n}.lean'), f'formal file mismatch: {n}')
    require(s['source_return_comment'].startswith(f'https://github.com/grandchallenge/MATH-PROGRAMME/issues/{data["source_audit_issue"]}#issuecomment-'), f'bad return link: {n}')
    require(data['work_status'] != 'QUEUED_UNEXECUTED' or (all(x == 'PENDING' for x in data['stage_results'].values()) and not data['proof_receipts'] and not data['review_receipts']), f'unexecuted receipt contradiction: {n}')
    if data['stage_results']['REPLAY_EXECUTION'] == 'PASS':
        require(data['proof_receipts'] and data['toolchain_pins'], f'replay PASS missing receipt or toolchain: {n}')
        require(data['stage_results']['STATEMENT_EQUIVALENCE'] == 'PASS', f'replay PASS lacks semantic review: {n}')
    if data['stage_results']['ADVERSARIAL_REVIEW'] == 'PASS':
        require(data['review_receipts'], f'review PASS missing independent receipt: {n}')
    if data['stage_results']['INTERNAL_ADJUDICATION'] == 'PASS':
        require(data['stage_results']['ADVERSARIAL_REVIEW'] == 'PASS', f'adjudication without adverse pass: {n}')
    if data['stage_results']['PROTECTED_EVIDENCE_ADMISSION'] == 'PASS':
        require(data['stage_results']['INTERNAL_ADJUDICATION'] == 'PASS', f'admitted without adjudication: {n}')
    if data['work_status'] in ('VERIFIED_WITHOUT_CERTIFICATION','SUBMITTED_TO_MATHCERT'):
        require(data['stage_results']['PROTECTED_EVIDENCE_ADMISSION'] == 'PASS', f'verified absent protected evidence: {n}')
    if data['certification_status'] != 'NOT_SUBMITTED':
        require(data['stage_results']['PROTECTED_EVIDENCE_ADMISSION'] == 'PASS' and data['work_status'] == 'SUBMITTED_TO_MATHCERT', f'MATHCERT status without handoff: {n}')
    if data['literature_status'] == 'OPEN':
        require('IRRATIONALITY' in data['verification_kind'] or 'NORMALIZATION' in data['verification_kind'], f'open result improperly scoped: {n}')
    if s['external_formal_commit'] is None:
        require(s['external_formal_path'] is None, f'unpinned external path: {n}')
    else:
        require(bool(s['external_formal_path']), f'missing external path: {n}')


def validate_registry(root: Path = ROOT) -> dict:
    registry = load(REGISTRY, root)
    require(registry['record_type'] == 'ERDOS_PROOF_VERIFICATION_REGISTRY/1', 'bad registry kind')
    require(registry['governing_issue'] == 3201, 'wrong governing issue')
    require(registry['project_number'] == 2, 'wrong project')
    require(registry['manifest_schema'] == SCHEMA, 'wrong schema path')
    require(registry['status'] == 'PILOT_REGISTERED_GLOBAL_TRIAGE_INCOMPLETE' or registry['source_population']['global_inventory_complete'], 'false global coverage claim')
    paths=registry['manifests'];require(len(paths)==len(set(paths)) and paths, 'manifest duplication/empty')
    schema=load(SCHEMA,root)
    jsonschema.Draft202012Validator.check_schema(schema)
    problems=set();issues=set();items=set()
    for path in paths:
        require(re.fullmatch(r'governance/erdos_proof_verification/manifests/[0-9]{4}.json',path) is not None, f'unsafe manifest path: {path}')
        data=load(path,root);validate_manifest(data,schema)
        n=data['problem_id'];require(path.endswith(f'/{n:04}.json'), f'path mismatch: {n}')
        require(n not in problems and data['verification_issue'] not in issues and data['project_item_id'] not in items, f'duplicate work: {n}')
        problems.add(n);issues.add(data['verification_issue']);items.add(data['project_item_id'])
    assert len(problems)==len(paths)
    return {'manifest_count':len(paths),'problem_ids':sorted(problems),'statuses':{str(n):load(f'governance/erdos_proof_verification/manifests/{n:04}.json',root)['work_status'] for n in problems},'global_triage':registry['source_population']['current_global_triage']}


if __name__=='__main__':
    try: print(json.dumps({'result':'PASS',**validate_registry()},sort_keys=True))
    except Exception as e:
        print(f'ERDOS_PROOF_VERIFICATION_FAIL: {type(e).__name__}: {e}',file=sys.stderr)
        sys.exit(1)
