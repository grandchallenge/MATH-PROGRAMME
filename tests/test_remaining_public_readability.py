"""Public narrative leads, while source and certification authorities remain intact."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'docs'

class RemainingPublicNarrativeTests(unittest.TestCase):
    def test_openmath_outcome_preserves_exact_historical_state(self):
        s=(D/'campaigns/OPENMATH_2026_STATUS.md').read_text()
        self.assertIn('## What happened?',s)
        self.assertIn('## What was learned?',s)
        self.assertIn('## Historical research record',s)
        self.assertIn('no official submissions and no official acceptances',s)
        for k in ('H1','H2','H3','H4','H5','H6','H7'):
            self.assertIn(k,s)
        for x in ('Official competition submissions: **0**',
                  'GCL-RETURN-RELAY/1',
                  'READY → LAUNCHED → RETURNED → CAPTURED → REPLAYED → ADJUDICATED → ADVANCED',
                  '**Canonical machine authority:**'):
            self.assertIn(x,s)
        self.assertLess(s.index('## What happened?'),s.index('## Event-window disposition'))

    def test_openmath_agenda_reader_entry_and_open_frontiers(self):
        s=(D/'campaigns/OPENMATH_2026_RESEARCH_AGENDA.md').read_text()
        for x in ('## What would count as progress?', '## Surviving frontiers',
                  'H7', 'GCL-ERDOS3', '324-mutant', 'SOURCE_BLOCKED',
                  'does not', 'without a gcl submission'):
            self.assertIn(x.lower(),s.lower())
        self.assertLess(s.index('## What would count as progress?'),s.index('## Surviving frontiers'))

    def test_domain_intros_before_specialist_record(self):
        files=('union_closed','navier_stokes','hodge','birch_swinnerton_dyer',
               'poincare_reconstruction','yang_mills','p_vs_np','riemann_hypothesis')
        for slug in files:
            with self.subTest(slug=slug):
                s=(D/'domains'/f'{slug}.md').read_text()
                self.assertIn('## The question in everyday language',s)
                self.assertIn('## Detailed research record',s)
                self.assertLess(s.index('## The question in everyday language'),
                                s.index('## Detailed research record'))
                self.assertIn('**What remains uncertain',s)
                self.assertTrue('## Claim boundary' in s or '## Certification boundary' in s)
                self.assertIn('Campaign ID:',s)
        uc=(D/'domains/union_closed.md').read_text()
        self.assertIn('now part of the published Documentary Library',uc)
        self.assertIn('admitted full-tier documentary',uc)
        rh=(D/'domains/riemann_hypothesis.md').read_text()
        self.assertIn('Post-merge retained-blocker disposition',rh)

    def test_proof_checker_explanation_keeps_replay_identity(self):
        s=(D/'OPENAI_TEN_PROOFS_VERIFICATION.md').read_text()
        for x in ('## What was checked?','## Ten advertised results',
                  'all ten supplied proof files','twelve principal declarations',
                  'not', 'Lean',
                  '94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6',
                  '34838818609'):
            self.assertIn(x.lower(),s.lower())
        self.assertLess(s.index('## What was checked?'),s.index('## The exact subject'))

    def test_fixture_explanation_does_not_upgrade_checks(self):
        s=(D/'FIXTURE_LEDGER.md').read_text()
        for x in ('## Why begin with small examples?', '## Ledger rule',
                  'UF-INV-001','RAD-NIL-002','LOG-GCD-001',
                  'not', '## Promotion discipline'):
            self.assertIn(x,s)
        self.assertLess(s.index('## Why begin with small examples?'),s.index('## Ledger rule'))

if __name__=='__main__':
    unittest.main()
