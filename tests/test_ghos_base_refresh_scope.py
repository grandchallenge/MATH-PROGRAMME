import pathlib, subprocess, tempfile, unittest
from unittest import mock
from ci.ghos_base_refresh_scope import CONTROL_INPUTS,classify

def git(root,*args):return subprocess.check_output(['git',*args],cwd=root,text=True).strip()
class RefreshProofTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=pathlib.Path(self.tmp.name)
  git(self.root,'init','-q','-b','main');git(self.root,'remote','add','origin',str(self.root));git(self.root,'config','user.email','audit@example.invalid');git(self.root,'config','user.name','Audit')
  for name in CONTROL_INPUTS:
   p=self.root/name
   if name in ('.github/workflows','.ghos-routing'):
    p.mkdir(parents=True);p=p/'control.txt'
   else:p.parent.mkdir(parents=True,exist_ok=True)
   p.write_text('protected bytes\n')
  self.commit('baseline');self.base=git(self.root,'rev-parse','HEAD')
 def tearDown(self):self.tmp.cleanup()
 def commit(self,subject):git(self.root,'add','-A');git(self.root,'commit','-qm',subject)
 def current(self):return git(self.root,'rev-parse','HEAD')
 def test_disjoint_math_change_skips(self):
  p=self.root/'fixtures/formal/New.lean';p.parent.mkdir(parents=True);p.write_text('math\n');self.commit('math')
  r=classify(self.root,self.base,self.current(),self.current())
  self.assertEqual((r['refresh'],r['reason']),(False,'CONTROL_INPUT_BYTES_IDENTICAL'))
 def test_each_material_control_change_requires_refresh(self):
  for name in CONTROL_INPUTS:
   with self.subTest(name=name):
    git(self.root,'reset','--hard',self.base)
    p=self.root/name
    if p.is_dir():p=p/'new-file.txt'
    p.write_text('different input\n');self.commit(name)
    self.assertTrue(classify(self.root,self.base,self.current(),self.current())['refresh'])
 def test_unknown_or_superseded_fails_open(self):
  p=self.root/'misc';p.write_text('change');self.commit('change');head=self.current()
  for old,new,current in [('0'*40,head,head),('x',head,head),(self.base,head,'f'*40),(self.base,'a'*40,'a'*40),(head,head,head)]:
   self.assertTrue(classify(self.root,old,new,current)['refresh'])
 def test_old_push_fails_open_when_protected_main_advanced(self):
  p=self.root/'math.txt';p.write_text('first math');self.commit('first push')
  older=self.current()
  p.write_text('later math');self.commit('second push')
  # The first event checkout can still be checked out in a separate job,
  # but the authoritative remote must now identify the second push.
  with mock.patch('ci.ghos_base_refresh_scope.git') as fake:
   from ci.ghos_base_refresh_scope import git as normal
   def same_except_remote(root,*args):
    if args[0]=='ls-remote':return self.current()+'\trefs/heads/main'
    if args[:2]==('rev-parse','HEAD'):return older
    return normal(root,*args)
   fake.side_effect=same_except_remote
   self.assertTrue(classify(self.root,self.base,older,older)['refresh'])
 def test_deleted_input_fails_open(self):
  (self.root/'requirements/policy.txt').unlink();self.commit('deletion')
  self.assertTrue(classify(self.root,self.base,self.current(),self.current())['refresh'])
 def test_unchanged_symlink_with_external_target_must_not_skip(self):
  target=self.root/'elsewhere.yml';target.write_text('initial')
  link=self.root/'.github/workflows/link.yml';link.symlink_to('../../elsewhere.yml')
  self.commit('baseline symlink')
  before=self.current()
  (self.root/'other.txt').write_text('unrelated source')
  self.commit('unrelated change')
  self.assertTrue(classify(self.root,before,self.current(),self.current())['refresh'])
 def test_new_gate_script_change_is_control_input(self):
  self.assertIn('ci/ghos_base_refresh_scope.py',CONTROL_INPUTS)
  self.assertIn('tests/test_ghos_base_refresh_scope.py',CONTROL_INPUTS)
 def test_nonancestor_fails_open(self):
  (self.root/'a').write_text('one');self.commit('main child');a=self.current()
  git(self.root,'checkout','-qb','fork',self.base)
  (self.root/'b').write_text('two');self.commit('other child')
  self.assertTrue(classify(self.root,a,self.current(),self.current())['refresh'])
if __name__=='__main__':unittest.main()
