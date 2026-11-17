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
    if n == 249 and data['stage_results']['REPLAY_EXECUTION'] == 'PASS':
        # A proved lacunary subseries cannot promote the original open series.
        root = 'experiments/erdos_proof_verification/0249/'
        receipt = 'governance/erdos_proof_verification/evidence/0249/LACUNARY_LEAN_GREEN_001.receipt.json'
        require(receipt in data['proof_receipts'],
                'Erdos249 Green requires the exact bounded lacunary receipt')
        r = load(receipt)
        hostile = r.get('hostile_full_series_target', {})
        src = root + 'Erdos249Lacunary.lean'
        fixed = {
            src: '6ec552e86902699f26472a3cddb6fdcf79e7dba1abb6ac3c3b486a2bda82cb99',
            root + 'lean-toolchain': 'bc84812c94489d1e3e191baa1dc10d5eb684382d7fe9d2a5ab085e72c1c67e47',
            root + 'lakefile.toml': '4dc46a70590893697fb3f3183000af552e29d972e1eacb6b5c7adb86a9f30525',
            root + 'lake-manifest.json': '3b9de3758005c73d884250d11611c935882adf24f02d9a35dc698a033daadde2',
            root + 'theorem_replay_stdout.log':
                '038d3d08c883f2c17394c2e39a9eaeaeda5d57970745626390528d360f9c9365',
            'governance/erdos_proof_verification/evidence/0249/LACUNARY_HOSTILE_FULL_SERIES_001.stdout.log':
                '5cc0d6ccb3b7a8ed27e283c9bc78a435984441bc0cb2faa4f810acc2e258f6ec',
        }
        for file, digest in fixed.items():
            p = (ROOT / file).resolve()
            require(p.is_relative_to(ROOT.resolve()) and p.is_file()
                    and hashlib.sha256(p.read_bytes()).hexdigest() == digest,
                    f'Erdos249 exact source/log package drift: {file}')
        t = data['toolchain_pins'] or {}
        require(
            r.get('schema') == 'GCL-ERDOS-249-LACUNARY-LEAN-REPLAY/1'
            and r.get('job') == 'ERDOS-PV-0249-LACUNARY-001'
            and r.get('problem_id') == 249
            and r.get('source_scope') == 'AUXILIARY_LACUNARY_TOTIENT_SUBSERIES_ONLY'
            and r.get('original_erdos_249_full_series_irrational_claim') is False
            and r.get('result') == 'GREEN_KERNEL_PROOF_UNADJUDICATED'
            and r.get('build_exit_code') == 0
            and r.get('independent_execution_attested') is False
            and r.get('kernel_proof_source') == src
            and r.get('source_sha256') == fixed[src]
            and r.get('lean_toolchain') == 'leanprover/lean4:v4.35.0-rc3'
            and r.get('lean_binary_commit') ==
                '470d5ce1400764999581fd26d5d72b00d990b0f4'
            and r.get('mathlib_commit') ==
                'c55e6e786f49471c72fbddbec5415808896aec1e'
            and r.get('lakefile_sha256') == fixed[root + 'lakefile.toml']
            and r.get('lake_manifest_sha256') == fixed[root + 'lake-manifest.json']
            and r.get('source_lines') == 292
            and r.get('command') == 'lake env lean Erdos249Lacunary.lean'
            and r.get('stdout_sha256') == fixed[root + 'theorem_replay_stdout.log']
            and r.get('stderr_empty') is True
            and r.get('stderr_sha256') ==
                'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
            and r.get('theorem_name') == 'Erdos249Bounded.totient_subseries_irrational'
            and r.get('theorem_type_observed') is True
            and r.get('axiom_report_observed') is True
            and r.get('axioms') == ['propext','Classical.choice','Quot.sound']
            and r.get('sorryAx_observed') is False
            and r.get('formal_derivation_complete_for_auxiliary_series') is True
            and hostile.get('expected_failure_observed') is True
            and hostile.get('exit_code') == 1
            and hostile.get('stdout_sha256') ==
                fixed['governance/erdos_proof_verification/evidence/0249/LACUNARY_HOSTILE_FULL_SERIES_001.stdout.log']
            and r.get('provider_formal_statement',{}).get('full_theorem_has_sorry') is True
            and r.get('provider_formal_statement',{}).get('full_theorem_replay_green') is False
            and r.get('adjudication_state') == 'NOT_YET_PERFORMED'
            and r.get('certification_state') == 'NOT_SUBMITTED'
            and t.get('lean') == r.get('lean_toolchain')
            and t.get('mathlib') == r.get('mathlib_commit')
            and t.get('provider_source_sha256') == r.get('source_sha256')
            and data['literature_status'] == 'OPEN'
            and data['certification_status'] == 'NOT_SUBMITTED',
            'Erdos249 Green is limited to exact pinned T, never full S'
        )
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
    if n == 249 and data['stage_results']['ADVERSARIAL_REVIEW'] == 'PASS':
        p = 'governance/erdos_proof_verification/reviews/0249_SOURCE_CRITICAL_REVIEW_001.json'
        doc = 'governance/erdos_proof_verification/reviews/0249_SOURCE_CRITICAL_REVIEW_001.md'
        require(p in data['review_receipts'] and doc in data['review_receipts'],
                'Erdos249 adversarial PASS requires exact T review receipt')
        r = load(p)
        f = (ROOT / doc).resolve()
        checks = r.get('checks', {})
        authority = r.get('authority_effects', {})
        require(f.is_relative_to(ROOT.resolve()) and f.is_file(),
                'Erdos249 source critical report unavailable')
        require(
            r.get('record_type') == 'GCL-ERDOS249-SOURCE-CRITICAL-REVIEW/1'
            and r.get('review_id') == 'ERDOS-PV-0249-R001'
            and r.get('review_scope') == 'AUXILIARY_LACUNARY_SUBSERIES_T_ONLY'
            and r.get('disposition') == 'QUALIFIED_PASS'
            and r.get('original_conjecture_status') == 'OPEN'
            and r.get('same_authenticated_agent_as_formal_author') is True
            and r.get('role_scoped_adversary_separate_pass') is True
            and r.get('independent_human_review') is False
            and r.get('independent_external_mathematical_rederivation') is False
            and r.get('review_document') == doc
            and r.get('review_document_sha256') ==
                hashlib.sha256(f.read_bytes()).hexdigest()
            and r.get('protected_proof_merge') ==
                '62ffaa1db3e2d1a5d120611e86fc189f1c24b50e'
            and r.get('source_sha256') ==
                '6ec552e86902699f26472a3cddb6fdcf79e7dba1abb6ac3c3b486a2bda82cb99'
            and r.get('stdout_sha256') ==
                '038d3d08c883f2c17394c2e39a9eaeaeda5d57970745626390528d360f9c9365'
            and checks.get('exact_exponent_gap') is True
            and checks.get('positive_tail') is True
            and checks.get('dyadic_partial_sum') is True
            and checks.get('integer_obstruction_positive_and_less_than_one') is True
            and checks.get('full_original_series_irrationality_proved') is False
            and checks.get('mathcert_certification') is False
            and authority.get('adversarial_review_scoped_T') is True
            and authority.get('internal_adjudication') is False
            and authority.get('protected_evidence_admission') is False
            and authority.get('issue_closure') is False,
            'Erdos249 adversarial pass must be exact qualified same-agent T scope'
        )
    if data['stage_results']['INTERNAL_ADJUDICATION'] == 'PASS':
        require(data['stage_results']['ADVERSARIAL_REVIEW'] == 'PASS', f'adjudication without adverse pass: {n}')
        if n == 248:
            # Internal Referee decision is a separate scoped non-author review
            # of the pinned external formalization, not a certificate.
            path = 'governance/erdos_proof_verification/adjudications/0248_REFEREE_ADJUDICATION_001.json'
            require(path in data['review_receipts'],
                    'Erdos248 adjudication PASS requires exact Referee receipt')
            r = load(path)
            doc = 'governance/erdos_proof_verification/adjudications/0248_REFEREE_ADJUDICATION_001.md'
            require(doc in data['review_receipts'],
                    'Erdos248 adjudication PASS requires full Referee report')
            report = (ROOT / doc).resolve()
            require(report.is_relative_to(ROOT.resolve()) and report.is_file(),
                    'Erdos248 Referee report unavailable')
            flags = r.get('findings', {})
            auth = r.get('authority_effects', {})
            require(
                r.get('record_type') == 'GCL-ERDOS-248-REFEREE-ADJUDICATION/1'
                and r.get('adjudication_id') == 'ERDOS-PV-0248-A001'
                and r.get('governing_issue') == 3204
                and r.get('parent_issue') == 3201
                and r.get('decision') ==
                    'ACCEPT_SCOPED_OMEGA248_FORMAL_VERIFICATION_WITHOUT_MATHCERT'
                and r.get('outcome_scope') ==
                    'EXACT_DISTINCT_PRIME_OMEGA_ERDOS248_FORMAL_STATEMENT_ONLY'
                and r.get('provider_commit') ==
                    '8822f7ddef30fadbd92e1c6ab4ed897af356af5e'
                and r.get('provider_source_sha256') ==
                    '292041372e8f0e45a2ac06fb78dafc32d79cdc4638253139ea4f495a3334a267'
                and r.get('kernel_receipt_sha256') ==
                    '708fb9a104231e8d6a07f425226808a26c4a0227239a50ea139cb2777cd78f28'
                and r.get('prior_source_critical_sha256') ==
                    'dc58e9dd9b2f069426ecfd3cfbb5c6a20094010bf4a0afa344e6aa7c1c323520'
                and r.get('adjudication_document') == doc
                and r.get('adjudication_document_sha256') ==
                    hashlib.sha256(report.read_bytes()).hexdigest()
                and r.get('reviewer_source_author') is False
                and r.get('role_pass_independent_identity') is False
                and r.get('independent_human_attestation') is False
                and flags.get('same_C_for_all_k') is True
                and flags.get('same_n_for_every_k') is True
                and flags.get('uniform_medium_and_large_thresholds') is True
                and flags.get('omega_le_Omega_direction_correct') is True
                and flags.get('published_Omega_multiplicity_formalized') is False
                and flags.get('author_leanization_map_present') is False
                and flags.get('complete_independent_analytic_reconstruction') is False
                and auth.get('internal_adjudication') is True
                and auth.get('protected_evidence_admission') is False
                and auth.get('verified_without_certification_status') is False
                and auth.get('mathcert_certification') is False
                and auth.get('issue_closure') is False,
                'Erdos248 Referee PASS requires real scoped noncertifying custody'
            )
    if n == 249 and data['stage_results']['INTERNAL_ADJUDICATION'] == 'PASS':
        p = 'governance/erdos_proof_verification/adjudications/0249_REFEREE_ADJUDICATION_001.json'
        doc = 'governance/erdos_proof_verification/adjudications/0249_REFEREE_ADJUDICATION_001.md'
        require(p in data['review_receipts'] and doc in data['review_receipts'],
                'Erdos249 adjudication PASS requires exact scoped Referee receipt')
        r = load(p)
        d = (ROOT / doc).resolve()
        require(d.is_relative_to(ROOT.resolve()) and d.is_file(),
                'Erdos249 Referee report unavailable')
        authorship = r.get('actual_review_authorship', {})
        checks = r.get('mathematical_checks', {})
        authority = r.get('authority_effects', {})
        require(
            r.get('record_type') == 'GCL-ERDOS249-REFEREE-ADJUDICATION/1'
            and r.get('decision_id') == 'ERDOS-PV-0249-A001'
            and r.get('problem_id') == 249
            and r.get('disposition') == 'ACCEPT_AUXILIARY_LACUNARY_T_IRRATIONALITY_ONLY'
            and r.get('claim_scope') == 'PROVED_AUXILIARY_T_ONLY'
            and r.get('original_full_S_status') == 'OPEN'
            and r.get('referee_document') == doc
            and r.get('referee_document_sha256') ==
                hashlib.sha256(d.read_bytes()).hexdigest()
            and r.get('source_critical_document_sha256') ==
                '334fe2621bca16973ee4a4af8b4be26725ce6753820d223a396aa3860b353887'
            and r.get('protected_green_proof_commit') ==
                '62ffaa1db3e2d1a5d120611e86fc189f1c24b50e'
            and r.get('source_sha256') ==
                '6ec552e86902699f26472a3cddb6fdcf79e7dba1abb6ac3c3b486a2bda82cb99'
            and authorship.get('same_authenticated_agent_as_formal_author') is True
            and authorship.get('logical_roles_distinct') is True
            and authorship.get('independent_human_reviewer') is False
            and authorship.get('independent_external_mathematical_rederivation') is False
            and checks.get('actual_kernel_green') is True
            and checks.get('integer_denominator_contradiction') is True
            and checks.get('original_series_claim') is False
            and authority.get('internal_adjudication_scoped_T') is True
            and authority.get('protected_evidence_admission') is False
            and authority.get('certification') is False
            and authority.get('original_conjecture_solved') is False
            and authority.get('issue_closure') is False
            and data['literature_status'] == 'OPEN'
            and data['certification_status'] == 'NOT_SUBMITTED',
            'Erdos249 internal Referee requires exact noncertifying T scope'
        )
    if data['stage_results']['PROTECTED_EVIDENCE_ADMISSION'] == 'PASS':
        require(data['stage_results']['INTERNAL_ADJUDICATION'] == 'PASS', f'admitted without adjudication: {n}')
        if n == 248:
            # Final status is permitted only after the prior Referee decision
            # exists on protected main with real merge/byte identities. The
            # current final PR remains a candidate until protected merge/readback.
            receipt = 'governance/erdos_proof_verification/admissions/0248_PROTECTED_EVIDENCE_ADMISSION_001.json'
            doc = 'governance/erdos_proof_verification/admissions/0248_PROTECTED_EVIDENCE_ADMISSION_001.md'
            require(receipt in data['review_receipts'] and doc in data['review_receipts'],
                    'Erdos248 protected PASS requires exact final custody packet')
            r = load(receipt)
            md = (ROOT / doc).resolve()
            require(md.is_relative_to(ROOT.resolve()) and md.is_file(),
                    'Erdos248 final custody document absent')
            checks = r.get('evidence_chain_status', {})
            excluded = r.get('claim_exclusions', {})
            auth = r.get('authority_effects', {})
            require(
                r.get('record_type') == 'GCL-ERDOS-248-PROTECTED-EVIDENCE-ADMISSION/1'
                and r.get('admission_id') == 'ERDOS-PV-0248-EA001'
                and r.get('governing_issue') == 3204
                and r.get('parent_issue') == 3201
                and r.get('candidate_phase') ==
                    'FINAL_EVIDENCE_ADMISSION_SUBJECT_TO_PROTECTED_MERGE_AND_READBACK'
                and r.get('outcome') == 'VERIFIED_WITHOUT_CERTIFICATION'
                and r.get('outcome_scope') ==
                    'EXACT_ERDOS248_DISTINCT_PRIME_OMEGA_KERNEL_VERIFIED_ONLY'
                and r.get('source_provider_commit') ==
                    '8822f7ddef30fadbd92e1c6ab4ed897af356af5e'
                and r.get('source_sha256') ==
                    '292041372e8f0e45a2ac06fb78dafc32d79cdc4638253139ea4f495a3334a267'
                and r.get('kernel_receipt_sha256') ==
                    '708fb9a104231e8d6a07f425226808a26c4a0227239a50ea139cb2777cd78f28'
                and r.get('source_review_sha256') ==
                    'dc58e9dd9b2f069426ecfd3cfbb5c6a20094010bf4a0afa344e6aa7c1c323520'
                and r.get('referee_adjudication_doc_sha256') ==
                    '0218423c75cb5712bdd3f9bc3031f003e398f5a966bfd82075cedcacfc753d6a'
                and r.get('referee_adjudication_json_sha256') ==
                    'ce859d609dcf89c7ae030234ea2aa3bae9e9d735fbb73a0e3f3cf7d9ee57f455'
                and r.get('protected_green_replay_merge') ==
                    'a55255f01b18139ddf045d4c82fb566c3e77f36d'
                and r.get('protected_source_review_merge') ==
                    'bb91ff9e21679e201013de3ef9bc5fba8986748d'
                and r.get('protected_referee_adjudication_merge') ==
                    '3cd3e6951c9c34d970b1e0e8ca7ae7edcb6ba871'
                and r.get('admission_document') == doc
                and r.get('admission_document_sha256') ==
                    hashlib.sha256(md.read_bytes()).hexdigest()
                and checks.get('source_lock') is True
                and checks.get('compiler_and_axiom_replay') is True
                and checks.get('non_author_critical_review') is True
                and checks.get('internal_referee_adjudication') is True
                and checks.get('all_three_predecessor_prs_protected') is True
                and checks.get('final_pr_protected_readback_required') is True
                and checks.get('certification_not_submitted') is True
                and excluded.get('published_multiplicity_Omega_formalized') is False
                and excluded.get('full_published_paper_verified') is False
                and excluded.get('author_tex_248_leanization_map_present') is False
                and excluded.get('mathcert_certified') is False
                and excluded.get('independent_human_certification') is False
                and auth.get('public_certification') is False
                and auth.get('human_independence') is False
                and auth.get('issue_auto_closure') is False
                and auth.get('issue_manual_completion_only_after_exact_merge_and_project_readback') is True
                and data['work_status'] == 'VERIFIED_WITHOUT_CERTIFICATION'
                and data['certification_status'] == 'NOT_SUBMITTED',
                'Erdos248 final protected admission requires exact noncertifying source custody'
            )
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
