"""Replay the pinned CRT proof and genuinely false altered targets."""
import argparse, hashlib, json, os, pathlib, re, subprocess, tempfile
P = pathlib.Path(__file__).resolve().parents[1]/'experiments/erdos_proof_verification/0027'
def sha(b): return hashlib.sha256(b).hexdigest()
def run(args, **kw): return subprocess.run([str(x) for x in args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kw)
def checked(args):
 r=run(args); assert r.returncode==0, r.stdout.decode(); return r.stdout.decode().strip()

def validate_axioms(s):
 expected={'covering_density','count_fibres','crt_count_fibres','congruence_split','avoid_iff','covering_count'}
 reports=re.findall(r"'Erdos27CRT\.(\w+)' depends on axioms: \[([^\]]*)\]",s)
 ax={n:set(x.split(', ')) for n,x in reports}
 if len(reports)!=len(expected) or set(ax)!=expected or any(x!={'propext','Classical.choice','Quot.sound'} for x in ax.values()) or 'sorryAx' in s:
  raise ValueError("incomplete, duplicate or forbidden axiom report")
 return ax

def printed_types(s):
 start=s.index('theorem Erdos27CRT.covering_count')
 types=s[start:s.index(' :=\n',start)]
 density=s[s.index('Erdos27CRT.covering_density.{'):].strip()
 if not density or not types: raise ValueError("missing printed theorem type")
 return types,density

def main():
 p = argparse.ArgumentParser()
 p.add_argument('--cache-root', required=True, type=pathlib.Path)
 p.add_argument('--lean', required=True, type=pathlib.Path)
 p.add_argument('--output', required=True, type=pathlib.Path)
 a = p.parse_args()
 a.output.mkdir(parents=True, exist_ok=True)
 v=checked([a.lean,'--version'])
 assert 'version 4.33.0' in v and 'd8b18978322de05a8f3dba51ef03cf5461676c17' in v, v
 deps={}
 paths=[]
 for x in json.loads((P/'lake-manifest.json').read_text())['packages']:
  d=a.cache_root/'.lake/packages'/x['name']
  assert checked(['git','-C',d,'rev-parse','HEAD'])==x['rev']
  assert not checked(['git','-C',d,'status','--porcelain','--untracked-files=no'])
  deps[x['name']]=x['rev']
  paths.append(str(d/'.lake/build/lib/lean'))
 env=dict(os.environ,LEAN_PATH=os.pathsep.join(paths))
 r=run([a.lean,P/'Erdos27CRT.lean'],env=env)
 assert r.returncode==0,r.stdout.decode()
 s=r.stdout.decode()
 ax=validate_axioms(s)
 log=(v+'\n').encode()+r.stdout
 (a.output/'C_LEAN_CRT_STDOUT_001.txt').write_bytes(log)
 types,density=printed_types(s)
 targets={
  'noncoprime_split':'(((2 : ZMod 4) = 0) ↔ (((2 : ZMod 2) = 0) ∧ ((2 : ZMod 2) = 0)))',
  'drop_smooth_condition':'(((1 : ZMod 2) ≠ 0) ↔ ((1 : ZMod 1) ≠ 0))',
  'drop_rough_condition':'(((2 : ZMod 6) ≠ 0) ↔ ((2 : ZMod 2) ≠ 0))'}
 neg={}
 with tempfile.TemporaryDirectory() as tmp:
  for name,target in targets.items():
   f=pathlib.Path(tmp)/'Witness.lean'
   f.write_text('import Mathlib.Data.ZMod.Basic\nexample : ¬ '+target+' := by decide\n')
   witness=run([a.lean,f],env=env); assert witness.returncode==0,witness.stdout.decode()
   f.write_text('import Mathlib.Data.ZMod.Basic\nexample : '+target+' := by decide\n')
   bad=run([a.lean,f],env=env)
   assert bad.returncode!=0 and b'decide' in bad.stdout and b'false' in bad.stdout,bad.stdout.decode()
   # Normalize the temporary directory only, so replay receipts are portable.
   msg=bad.stdout.decode().replace(str(tmp),'<tmp>')
   neg[name]={'target':target,'negation_exit':witness.returncode,'false_target_exit':bad.returncode,'diagnostic':msg}
 receipt={'record_type':'ERDOS_PV_0027_C_LEAN_CRT_REPLAY/1','result':'PASS','lean_version':v,'dependency_revisions':deps,
  'tracked_dependency_worktrees_clean':True,'positive_exit':r.returncode,
  'source_sha256':sha((P/'Erdos27CRT.lean').read_bytes()),'manifest_sha256':sha((P/'lake-manifest.json').read_bytes()),
  'toolchain_sha256':sha((P/'lean-toolchain').read_bytes()),'stdout_sha256':sha(log),
  'covering_count_printed_type_sha256':sha(types.encode()),'covering_density_printed_type_sha256':sha(density.encode()),
  'axioms':{n:sorted(x) for n,x in ax.items()},'negative_controls':neg,'full_problem_proof_or_mathcert':False}
 (a.output/'C_LEAN_CRT_REPLAY_001.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt,indent=2))

if __name__=='__main__':
 main()
