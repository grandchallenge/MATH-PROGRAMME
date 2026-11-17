#!/usr/bin/env python3
"""Fail-closed structural/claim-boundary checks for source-locked Erdős verification."""
from __future__ import annotations
import json
import hashlib
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
        if n == 248:
            # This lane has a machine-readable exact-worker receipt. A preserved
            # RED failure is evidence of execution, not evidence of proof replay.
            receipts = []
            for path in data['proof_receipts']:
                if isinstance(path, str) and path.endswith('.receipt.json'):
                    receipts.append(load(path))
            require(any(
                r.get('schema') == 'GCL-ERDOS-248-LEAN-REPLAY/1'
                and r.get('job') == 'ERDOS-0248-LEAN-REPLAY-001'
                and r.get('status') == 'GREEN_KERNEL_REPLAY_UNADJUDICATED'
                and r.get('full_kernel_replay') is True
                and r.get('axioms_observed') is True
                and r.get('theorem_type_observed') is True
                and r.get('source_mode') == 'PINNED_PROVIDER_WITH_DECLARED_COMPATIBILITY_PATCHES'
                and r.get('source_sha256') ==
                    '292041372e8f0e45a2ac06fb78dafc32d79cdc4638253139ea4f495a3334a267'
                and r.get('external_commit') ==
                    '8822f7ddef30fadbd92e1c6ab4ed897af356af5e'
                and r.get('mathlib_commit') ==
                    'db584cd6d46c92f209a44c0f1c829460d327499d'
                for r in receipts
            ), 'Erdos248 replay PASS requires a real pinned GREEN kernel/axiom receipt')
    if data['stage_results']['ADVERSARIAL_REVIEW'] == 'PASS':
        require(data['review_receipts'], f'review PASS missing independent receipt: {n}')
        if n == 248:
            # A generic label or earlier RED receipt is insufficient. The source
            # critical role pass expressly EXCLUDES the paper's stronger Omega
            # theorem and never represents a human-independent certification.
            path = 'governance/erdos_proof_verification/reviews/0248_SOURCE_CRITICAL_REVIEW_001.json'
            require(path in data['review_receipts'],
                    'Erdos248 adversarial PASS requires exact qualified review receipt')
            r = load(path)
            expected_md = 'governance/erdos_proof_verification/reviews/0248_SOURCE_CRITICAL_REVIEW_001.md'
            p = (ROOT / expected_md).resolve()
            require(p.is_relative_to(ROOT.resolve()) and p.is_file(),
                    'missing exact Erdos248 source-critical review document')
            actual_md_hash = hashlib.sha256(p.read_bytes()).hexdigest()
            flags = r.get('checks', {})
            authority = r.get('authority_effects', {})
            require(
                r.get('record_type') == 'GCL-ERDOS-248-SOURCE-CRITICAL-REVIEW/1'
                and r.get('review_id') == 'ERDOS-PV-0248-R001'
                and r.get('review_scope') == 'FORMAL_ERDOS_248_DISTINCT_PRIME_OMEGA_ONLY'
                and r.get('disposition') == 'QUALIFIED_PASS'
                and r.get('provider_commit') == '8822f7ddef30fadbd92e1c6ab4ed897af356af5e'
                and r.get('source_sha256') ==
                    '292041372e8f0e45a2ac06fb78dafc32d79cdc4638253139ea4f495a3334a267'
                and r.get('kernel_receipt_sha256') ==
                    '708fb9a104231e8d6a07f425226808a26c4a0227239a50ea139cb2777cd78f28'
                and r.get('module_bundle_sha256') ==
                    '7a4e16be1ef119996a7e3ee773a6a9abb0e6c041791565e679cab8cf1c28f815'
                and r.get('review_document') == expected_md
                and r.get('review_document_sha256') == actual_md_hash
                and r.get('independent_human_attestation') is False
                and flags.get('one_C_outside_all_k') is True
                and flags.get('one_n_for_every_k') is True
                and flags.get('uniform_T_independent_of_K_and_k') is True
                and flags.get('omega_le_Omega_elementary_bridge') is True
                and flags.get('full_paper_Omega_proved_in_lean') is False
                and flags.get('original_author_leanization_map_present') is False
                and flags.get('independent_analytic_rederivation_complete') is False
                and authority.get('adversarial_review_pass_for_scoped_formal_statement') is True
                and authority.get('internal_adjudication') is False
                and authority.get('mathematical_certification') is False
                and authority.get('issue_closure') is False,
                'Erdos248 adversarial PASS requires exact qualified scope and no certification'
            )
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
    if n in (566, 567):
        # The frozen FC-GDM-85F86371 provider misidentified vertex-Ramsey
        # size-linearity as edge-minimal sizeRamsey. Preserve the historical
        # immutable lock; require exact corrected, per-problem external source.
        legacy = {
            566: '0db66813b8f17be6819c53afca9cd3f853426a53',
            567: 'f2e29d94a0391f71f78d4b32168ce5e627e28b27',
        }
        require(
            s['formal_repository'] == 'google-deepmind/formal-conjectures'
            and s['formal_commit'] == '85f863718beeec7b58a3a1926ee92e3472bc2020'
            and s['formal_blob'] == legacy[n]
            and s['external_formal_commit'] == '6751c0f043985ac6647db28a45a63afdf21acffe'
            and s['external_formal_path'] == f'FormalConjectures/ErdosProblems/{n}.lean',
            f'problem {n}: stale sizeRamsey formal theorem cannot enter replay; '
            'require corrected graphRamsey source lock')


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
