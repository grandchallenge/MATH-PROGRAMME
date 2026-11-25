"""Pinned supplemental weighted-correlation replay; not a full Theorem B proof."""
import argparse, hashlib, json, os, pathlib, re, subprocess, tempfile
ROOT=pathlib.Path(__file__).resolve().parents[4]
P=ROOT/'experiments/erdos_proof_verification/0027'
E=pathlib.Path(__file__).resolve().parent
EXPECTED=set('bad_mass_nonneg finite_sequence_unweighted bad_union_bound finite_step_list finite_sequence mass_mono mass_sdiff mass_union_bound finite_step weighted_recurrence weighted_nonneg weighted_le_plain unweighted_bound reject_independence_drop reject_correlation_drop reject_weight_range_drop'.split())
AX={'propext','Classical.choice','Quot.sound'}
CONTROLS={
'independence':(r'(1-(1/2:ℚ))*mass 4 ({0,1}:Finset ℕ) ≤ mass 4 (({0,1}:Finset ℕ) \ ({0,1}:Finset ℕ))','simp [mass]\n  norm_num'),
'correlation':(r'(1-(1/4:ℚ))*mass 4 ({1,3}:Finset ℕ) ≤ mass 4 (({1,3}:Finset ℕ) \ ({1}:Finset ℕ))',r'have h : (({1,3}:Finset ℕ) \ ({1}:Finset ℕ)) = {3} := by decide'+'\n  rw [h]\n  norm_num [mass]'),
'weight':('0 ≤ weightedError (fun _ => 2) (fun n => if n=0 then 1 else 0) 2','norm_num [weightedError]')}
def sha(b):return hashlib.sha256(b).hexdigest()
def run(a,**kw):return subprocess.run([str(x) for x in a],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,**kw)
def checked(a,**kw):
 r=run(a,**kw)
 if r.returncode!=0:raise RuntimeError(r.stdout.decode())
 return r.stdout
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--cache-root',required=True,type=pathlib.Path)
 p.add_argument('--lean',required=True,type=pathlib.Path)
 p.add_argument('--output',required=True,type=pathlib.Path)
 a=p.parse_args()
 cache=a.cache_root.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
 # Select the pinned toolchain in the package cwd even when using elan.
 v=checked([a.lean,'--version'],cwd=P).decode().strip()
 assert 'version 4.33.0' in v and 'd8b18978322de05a8f3dba51ef03cf5461676c17' in v
 deps={};paths=[]
 for x in json.loads((P/'lake-manifest.json').read_text())['packages']:
  d=cache/'.lake/packages'/x['name']
  assert checked(['git','-C',d,'rev-parse','HEAD']).decode().strip()==x['rev']
  assert not checked(['git','-C',d,'status','--porcelain','--untracked-files=no']).strip()
  deps[x['name']]=x['rev'];paths.append(str(d/'.lake/build/lib/lean'))
 env=dict(os.environ,LEAN_PATH=os.pathsep.join(paths))
 source=P/'Erdos27Weighted.lean'
 log=checked([a.lean,source],env=env,cwd=P)
 s=log.decode()
 reports=re.findall(r"'Erdos27Weighted\.(\w+)' depends on axioms: \[([^\]]*)\]",s)
 ax={n:set(x.split(', ')) for n,x in reports}
 assert len(reports)==len(EXPECTED) and set(ax)==EXPECTED and all(x==AX for x in ax.values())
 assert not any(x in s for x in ('sorryAx','error:','warning:'))
 neg={}
 with tempfile.TemporaryDirectory() as tmp:
  t=pathlib.Path(tmp)
  # Source is already checked by the kernel. Build a temporary import for the false statements.
  checked([a.lean,'-o',t/'Erdos27Weighted.olean',source],env=env,cwd=P)
  env['LEAN_PATH']=str(t)+os.pathsep+env['LEAN_PATH']
  for name,(target,tactic) in CONTROLS.items():
   witness=t/'Witness.lean'
   pre='import Erdos27Weighted\nopen Erdos27Weighted\n'
   witness.write_text(pre+'example : ¬ ('+target+') := by\n  '+tactic+'\n')
   checked([a.lean,witness],env=env,cwd=P)
   witness.write_text(pre+'example : '+target+' := by\n  '+tactic+'\n')
   bad=run([a.lean,witness],env=env,cwd=P)
   msg=bad.stdout.decode().replace(str(t),'<tmp>')
   assert bad.returncode!=0 and '⊢ False' in msg,msg
   neg[name]={'negation_exit':0,'false_target_exit':bad.returncode,'diagnostic':msg,'target':target}
 receipt={'record_type':'ERDOS_PV_0027_WEIGHTED_KERNEL_REPLAY/1','result':'PASS','lean_version':v,'dependency_revisions':deps,'source_sha256':sha(source.read_bytes()),'manifest_sha256':sha((P/'lake-manifest.json').read_bytes()),'stdout_sha256':sha(log),'axioms':{n:sorted(x) for n,x in ax.items()},'negative_controls':neg,'joint_independence_assumed_not_derived':True,'full_arithmetic_lemma_in_lean':False,'full_theorem_b_in_lean':False,'mathcert_certified':False}
 if out != E:
  assert (E/'WEIGHTED_KERNEL_STDOUT_001.txt').read_bytes()==log,'stored stdout differs'
  assert json.loads((E/'WEIGHTED_KERNEL_REPLAY_001.json').read_text())==receipt,'stored replay receipt differs'
 (out/'WEIGHTED_KERNEL_STDOUT_001.txt').write_bytes(log)
 (out/'WEIGHTED_KERNEL_REPLAY_001.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps({'result':'PASS','axiom_reports':len(ax),'hostile_targets':len(neg),'source_sha256':receipt['source_sha256']}))
if __name__=='__main__':main()
