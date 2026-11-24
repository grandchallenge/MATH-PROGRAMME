"""Shared correspondence and separate public evidence-update regression checks."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import erdos_compendium as comp
from erdos_compendium_crossrepo_reconciliation import reconcile_shared_paths

ROOT=comp.ROOT
DIR=ROOT/'governance/erdos_compendium/crossrepo'
class EvidenceUpdateTests(unittest.TestCase):
    def setUp(self):
        self.raw=(DIR/'RECONCILIATION_20261124.json').read_bytes()
        self.base=json.loads(self.raw)
        self.mapping=json.loads((DIR/'SHARED_ARTIFACTS_20261124.json').read_bytes())
        self.trees={r:{} for r in ('MATH-PROGRAMME','MATHSOLVE','MATHCERT')}
        self.trees['MATHSOLVE']={r['path']:r['blob'] for r in self.mapping['entries']}
    def test_all_27_and_three_recovered_ids(self):
        r=reconcile_shared_paths(self.trees,self.base,self.raw,self.mapping)
        self.assertEqual(r['mapped_paths_current'],27)
        self.assertTrue({7,9,10}<=set(r['mapped_problem_ids']))
        self.assertEqual(r['unresolved_current_paths']['MATHSOLVE'],[])
        self.assertFalse(r['theorem_authority'])
    def test_stale_mapping_and_new_path_stay_unresolved(self):
        path=self.mapping['entries'][0]['path']; self.trees['MATHSOLVE'][path]='a'*40
        self.trees['MATHSOLVE']['research/erdos-shared-new.md']='b'*40
        r=reconcile_shared_paths(self.trees,self.base,self.raw,self.mapping)
        self.assertEqual(r['mapped_paths_current'],26)
        self.assertEqual(r['stale_or_missing_paths'],[path])
        self.assertEqual(len(r['unresolved_current_paths']['MATHSOLVE']),2)
    def test_forged_authority_and_missing_path_rejected(self):
        for change in ('promotion','missing','blob'):
            d=copy.deepcopy(self.mapping)
            if change=='promotion': d['entries'][0]['theorem_promotion']=True
            elif change=='missing': d['entries'].pop()
            else: d['entries'][0]['blob']='a'*40
            with self.assertRaises(ValueError): reconcile_shared_paths(self.trees,self.base,self.raw,d)
    def test_eight_addenda_keep_admission_and_original_manuscript(self):
        rows,heads=comp.load_evidence_addenda(DIR)
        self.assertEqual(set(rows),{2,3,14,248,249,560,561,602})
        with tempfile.TemporaryDirectory() as d:
            out=Path(d); counts=comp.build(output=out)
            self.assertEqual(counts['reviewed'],len(comp.load_batch_admissions()))
            for n,r in rows.items():
                page=(out/'problems'/f'{n:04d}.md').read_text()
                self.assertIn('## Evidence update — 24 November 2026',page)
                self.assertIn(r['text'],page)
                original=comp.manuscript(n)
                if original: self.assertIn(original,page)
                for a in r['anchors']: self.assertIn(heads[a['repository']],page)
            self.assertNotIn('## Evidence update — 24 November 2026',(out/'problems/0001.md').read_text())
    def test_changed_manuscript_does_not_inherit_old_update(self):
        rows,heads=comp.load_evidence_addenda(DIR)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'0249.md';p.write_text('changed')
            self.assertEqual(comp.evidence_addendum(rows[249],heads,p),'')
    def test_addendum_claim_promotion_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'RECONCILIATION_20261124.json').write_bytes(self.raw)
            doc=json.loads((DIR/'PUBLIC_EVIDENCE_UPDATES_20261124.json').read_bytes())
            doc['entries'][0]['certification']=True
            (p/'PUBLIC_EVIDENCE_UPDATES_20261124.json').write_text(json.dumps(doc))
            with self.assertRaises(ValueError):comp.load_evidence_addenda(p)
if __name__=='__main__':unittest.main()
