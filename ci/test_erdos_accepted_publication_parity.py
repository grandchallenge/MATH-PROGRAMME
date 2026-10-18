import hashlib
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
from erdos_accepted_publication_parity import compare_accepted_article, HEADINGS
import markdown

BASE='b'*40
URL='https://grandchallenge.github.io/MATH-PROGRAMME/erdos/problems/0099/'
SOURCE='\n\n'.join('## '+h+'\n\nThis section '+str(i)+' states $n\\ge2$ and retains its source meaning.' for i,h in enumerate(HEADINGS)).strip()
ROW={'source_sha256':hashlib.sha256(SOURCE.encode()).hexdigest()}

def page(source=SOURCE,status='Reviewed explanatory article — evidence qualified'):
    return ('<html><body><main><h1>Erdős Problem #99</h1><p>'+status+'</p>'+markdown.markdown(source,extensions=['pymdownx.arithmatex','extra'])+'</main></body></html>').encode()

class AcceptedParityTests(unittest.TestCase):
    def run_case(self,html=None,**change):
        args=dict(problem_id=99,source=SOURCE,admission=ROW,public_html=page() if html is None else html,public_url=URL,source_commit=BASE,deploy_commit=BASE)
        args.update(change)
        return compare_accepted_article(**args)
    def test_all_sections_and_math(self):
        x=self.run_case();self.assertEqual((x['verified_editorial_sections'],x['verified_math_expressions']),(6,6));self.assertFalse(x['mathematical_theorem_certification'])
    def reject(self,*a,**kw):
        with self.assertRaises(ValueError):self.run_case(*a,**kw)
    def test_source_modified(self):self.reject(source=SOURCE+' corrupted')
    def test_deployment_stale(self):self.reject(deploy_commit='a'*40)
    def test_wrong_url(self):self.reject(public_url=URL.replace('0099','0100'))
    def test_unaccepted_draft(self):self.reject(html=page(status='UNACCEPTED DRAFT'))
    def test_uncertified_status_changed(self):self.reject(html=page(status='NOT received separate GCL editorial acceptance'))
    def test_display_math_enters_source_fidelity_and_render_count(self):
        # A top-level <div class="arithmatex"> must never be silently skipped.
        revised=SOURCE.replace('This section 1', 'Display equation:\n\n$$\na^2+b^2=c^2\n$$\n\nThis section 1',1)
        admission={'source_sha256':hashlib.sha256(revised.encode()).hexdigest()}
        good=self.run_case(source=revised,admission=admission,html=page(source=revised))
        self.assertEqual(good['verified_math_expressions'],7)
        changed=revised.replace('a^2+b^2=c^2','a^2+b^2=c^3')
        self.reject(source=revised,admission=admission,html=page(source=changed))
        missing=revised.replace('$$\na^2+b^2=c^2\n$$','')
        self.reject(source=revised,admission=admission,html=page(source=missing))
    def test_math_changed(self):self.reject(html=page(source=SOURCE.replace('n\\ge2','n\\ge3',1)))
    def test_math_removed(self):self.reject(html=page(source=SOURCE.replace('$n\\ge2$', 'n is at least 2',1)))
    def test_prose_changed(self):self.reject(html=page(source=SOURCE.replace('retains its source meaning','alters its meaning',1)))
    def test_missing_headings(self):self.reject(html=page(source=SOURCE.replace('## What remains','## Replaced heading')))
    def test_broken_url(self):self.reject(public_url='https://invalid.example/99')
    def test_no_page(self):self.reject(html=b'404')

if __name__=='__main__':unittest.main()
