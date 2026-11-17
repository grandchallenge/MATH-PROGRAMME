#!/usr/bin/env python3
"""Hostile exact-head evidence for nonformal-contract / Lean replay separation."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

import formal_validation as formal
import formal_contract_dependency as guard


class ContractDependencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = formal.load_registry()

    def test_current_audited_dependency_closure_disjoint(self):
        allowed, reason = guard.contract_only_safe(formal.ROOT, self.registry)
        self.assertTrue(allowed, reason)
        paths = guard.audited_code_paths(formal.ROOT, self.registry)
        self.assertGreaterEqual(len(paths), 30)
        self.assertFalse(paths & guard.CONTRACT_FILES)
        self.assertIn('ci/formal_validation.py', paths)
        self.assertIn('campaigns/poincare_reconstruction/WP03_SURGERY_TOPOLOGY/05_ADVERSARIAL_HISTORIES/validate_histories.py', paths)

    def test_known_contract_only_does_not_start_formal_lanes(self):
        for p in sorted(guard.CONTRACT_FILES):
            with self.subTest(p=p):
                result = formal.classify_paths([p], self.registry)
                self.assertEqual(result['lanes'], [])
                self.assertEqual(result['reason'], 'nonformal_contract_only')

    def test_mixed_material_still_executes_required_lane(self):
        result = formal.classify_paths(['ci/validate_workflow_semantics.py',
            'fixtures/formal/LOG-GCD-001/lakefile.toml'], self.registry)
        self.assertEqual(result['lanes'], ['log-gcd'])

    def test_new_contract_script_and_protected_control_full_fanout(self):
        all_lanes = set(formal.lane_map(self.registry))
        for p in ('ci/validate_workflow_coverage_v999.py',
                  'ci/test_workflow_coverage_next.py',
                  'ci/formal_validation.py', 'ci/formal_contract_dependency.py',
                  'ci/test_formal_contract_dependency.py',
                  '.github/workflows/formal-validation.yml',
                  'requirements/policy.txt', 'governance/formal_validation_registry.json',
                  'governance/policy_impact_gating.json'):
            with self.subTest(p=p):
                result = formal.classify_paths([p], self.registry)
                self.assertEqual(set(result['lanes']), all_lanes)
                self.assertEqual(result['reason'], 'control_plane_full_fanout')

    def test_any_mixed_full_control_overrides_contract_exception(self):
        result = formal.classify_paths(['ci/test_workflow_coverage.py',
                                         '.github/workflows/formal-validation.yml'], self.registry)
        self.assertEqual(len(result['lanes']), len(self.registry['lanes']))

    def test_uncertain_dependency_fails_to_full_fanout(self):
        with mock.patch.object(formal, 'contract_only_safe', return_value=(False,'unknown')):
            result = formal.classify_paths(['ci/test_workflow_semantics.py'],self.registry)
        self.assertEqual(len(result['lanes']), len(self.registry['lanes']))

    def test_sentinels_manual_and_unclassified_formal_preserved(self):
        event = formal.event_plan('workflow_dispatch', {}, self.registry)
        self.assertEqual(len(event['lanes']), len(self.registry['lanes']))
        scheduled = formal.event_plan('schedule',
            {'schedule':self.registry['sentinels']['legacy_formal_cron']},self.registry)
        self.assertEqual(len(scheduled['lanes']), 3)
        with self.assertRaises(formal.FormalValidationError):
            formal.classify_paths(['fixtures/formal/CMDG-NAT-CONCORDANCE-001/NewTheorem.lean'],
                                   self.registry)

    def test_merge_queue_selection_protected(self):
        group={'merge_group':{'base_sha':'a'*40,'head_sha':'b'*40}}
        with mock.patch.object(formal,'diff_paths',return_value=['ci/test_workflow_semantics.py']):
            result=formal.event_plan('merge_group',group,self.registry)
        self.assertEqual(result['mode'],'promotion')
        self.assertEqual(result['lanes'],[])
        wf=(formal.ROOT/'.github/workflows/formal-validation.yml').read_text()
        self.assertIn('if: always()',wf)
        self.assertIn('needs: [impact, formal-lane]',wf)
        self.assertIn('name: formal-validation / formal-validation',wf)
        self.assertIn('test "$LANE_RESULT" = "skipped"',wf)

    def make_fixture(self, location: Path):
        paths=guard.audited_code_paths(formal.ROOT,self.registry)
        paths |= {guard.PC_MANIFEST,'governance/policy_shard_registry.json'}
        for relative in paths:
            source=formal.ROOT/relative
            dest=location/relative
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(source,dest)

    def test_injected_python_dependency_forces_full_fanout(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            self.make_fixture(root)
            self.assertTrue(guard.contract_only_safe(root,self.registry)[0])
            target=root/'ci/validate_cmdg_nat_concordance.py'
            target.write_text(target.read_text()+'\nimport validate_workflow_semantics\n')
            ok,reason=guard.contract_only_safe(root,self.registry)
            self.assertFalse(ok)
            self.assertIn('formal validator imports contract code',reason)

    def test_dynamic_module_import_forces_full_fanout(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            self.make_fixture(root)
            target=root/'ci/validate_cmdg_nat_concordance.py'
            target.write_text(target.read_text()+'\n__import__("unexpected")\n')
            self.assertFalse(guard.contract_only_safe(root,self.registry)[0])

    def test_unrelated_duplicate_module_name_is_not_an_execution_dependency(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            self.make_fixture(root)
            unrelated=root/'campaigns/odd_zeta/unrelated/validate.py'
            unrelated.parent.mkdir(parents=True)
            unrelated.write_text('__import__("unexpected")\n')
            self.assertTrue(guard.contract_only_safe(root,self.registry)[0])

    def test_guard_rejects_importlib_replay_target_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            self.make_fixture(root)
            p=root/'tests/test_cmdg_condensed_cm4_p3.py'
            p.write_text(p.read_text().replace(
                '"ci/validate_cmdg_condensed_cm4_p3.py"',
                '"ci/validate_workflow_semantics.py"'))
            ok,reason=guard.contract_only_safe(root,self.registry)
            self.assertFalse(ok)
            self.assertIn('dynamic validator source identity',reason)

    def test_relative_import_is_unproved_and_fails_open(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            self.make_fixture(root)
            p=root/'ci/validate_cmdg_nat_concordance.py'
            p.write_text(p.read_text()+'\nfrom . import unexpected_module\n')
            self.assertFalse(guard.contract_only_safe(root,self.registry)[0])

    def test_missing_contract_command_forces_full_fanout(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            self.make_fixture(root)
            p=root/'governance/policy_shard_registry.json'
            j=json.loads(p.read_text())
            for xs in j['shards'].values():
                if ['python3','ci/test_workflow_semantics.py'] in xs:
                    xs.remove(['python3','ci/test_workflow_semantics.py'])
            p.write_text(json.dumps(j))
            self.assertFalse(guard.contract_only_safe(root,self.registry)[0])

    def test_unknown_python_process_spawn_remains_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            self.make_fixture(root)
            # The existing separately audited CMDG validator cannot gain
            # ad hoc subprocess execution from a candidate change.
            target=root/'ci/validate_cmdg_nat_concordance.py'
            target.write_text(target.read_text()+
                              '\nimport subprocess\nsubprocess.run(["true"])\n')
            allowed,reason=guard.contract_only_safe(root,self.registry)
            self.assertFalse(allowed)
            self.assertIn('unreviewed subprocess dependency',reason)

    def test_deleted_or_renamed_formal_source_is_not_invisible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            def run(*args):
                return subprocess.check_output(['git',*args],cwd=root,text=True).strip()
            run('init','-q')
            run('config','user.email','formal-gate@example.invalid')
            run('config','user.name','Formal Gate Test')
            source=root/'fixtures/formal/LOG-GCD-001/Case.lean'
            source.parent.mkdir(parents=True)
            source.write_text('theorem example : True := trivial\n')
            run('add','.')
            run('commit','-qm','original')
            parent=run('rev-parse','HEAD')
            # A deleted formal file must remain visible to the router.
            source.unlink()
            run('add','-A')
            run('commit','-qm','delete')
            child=run('rev-parse','HEAD')
            paths=formal.diff_paths(parent,child,root)
            self.assertEqual(paths,['fixtures/formal/LOG-GCD-001/Case.lean'])
            self.assertEqual(formal.classify_paths(paths,self.registry)['lanes'],['log-gcd'])
            # A rename crossing the managed-root boundary must report both
            # the original formal source and the new destination.
            run('reset','--hard',parent)
            destination=root/'docs/Case.lean'
            destination.parent.mkdir(parents=True)
            run('mv','fixtures/formal/LOG-GCD-001/Case.lean','docs/Case.lean')
            run('commit','-qm','relocate')
            moved=run('rev-parse','HEAD')
            paths=formal.diff_paths(parent,moved,root)
            self.assertIn('fixtures/formal/LOG-GCD-001/Case.lean',paths)
            self.assertIn('docs/Case.lean',paths)
            self.assertEqual(formal.classify_paths(paths,self.registry)['lanes'],['log-gcd'])

    def test_pc_dynamic_validator_blob_mismatch_forces_full_fanout(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            self.make_fixture(root)
            p=root/guard._dynamic_pc_target(root)
            p.write_text(p.read_text()+'\n# unexpected drift\n')
            ok,reason=guard.contract_only_safe(root,self.registry)
            self.assertFalse(ok)
            self.assertIn('blob mismatch',reason)


if __name__ == '__main__':
    unittest.main()
