"""Recompile the CRT dependency and the joint-independence proof on pinned inputs."""
import argparse,hashlib,json,os,pathlib,re,subprocess,tempfile
E=pathlib.Path(__file__).resolve().parent
P=E.parents[3]/'experiments/erdos_proof_verification/0027'
AX={'propext','Classical.choice','Quot.sound'}
NAMES=set('count_all residue_count residue_mass congruence_family_independent left_cast right_cast_divisor count_and joint_count right_count joint_density'.split())
def sha(b):return hashlib.sha256(b).hexdigest()
def checked(args,**kw):
 r=subprocess.run([str(x) for x in args],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,**kw)
 if r.returncode:raise RuntimeError(r.stdout.decode())
 return r.stdout
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--cache-root',required=True,type=pathlib.Path)
 p.add_argument('--lean',required=True,type=pathlib.Path)
 p.add_argument('--output',required=True,type=pathlib.Path)
 a=p.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
 v=checked([a.lean,'--version'],cwd=P).decode().strip()
 assert 'version 4.33.0' in v and 'd8b18978322de05a8f3dba51ef03cf5461676c17' in v
 deps={};paths=[]
 for x in json.loads((P/'lake-manifest.json').read_text())['packages']:
  d=a.cache_root.resolve()/'.lake/packages'/x['name']
  assert checked(['git','-C',d,'rev-parse','HEAD']).decode().strip()==x['rev']
  assert not checked(['git','-C',d,'status','--porcelain','--untracked-files=no']).strip()
  deps[x['name']]=x['rev'];paths.append(str(d/'.lake/build/lib/lean'))
 sources=[P/'Erdos27CRT.lean',P/'Erdos27Independence.lean']
 with tempfile.TemporaryDirectory() as t:
  env=dict(os.environ,LEAN_PATH=os.pathsep.join([t]+paths))
  checked([a.lean,'-o',pathlib.Path(t)/'Erdos27CRT.olean',sources[0]],cwd=P,env=env)
  log=checked([a.lean,sources[1]],cwd=P,env=env)
 s=log.decode();reports=re.findall(r"'Erdos27Independence\.(\w+)' depends on axioms: \[([^\]]*)\]",s)
 ax={n:set(x.split(', ')) for n,x in reports}
 assert len(reports)==len(NAMES) and set(ax)==NAMES and all(x==AX for x in ax.values())
 assert not any(x in s for x in ('sorryAx','error:','warning:'))
 r={'record_type':'ERDOS_PV_0027_CRT_JOINT_INDEPENDENCE_REPLAY/1','result':'PASS','lean_version':v,'dependency_revisions':deps,'source_sha256':{f.name:sha(f.read_bytes()) for f in sources},'manifest_sha256':sha((P/'lake-manifest.json').read_bytes()),'stdout_sha256':sha(log),'axioms':{n:sorted(x) for n,x in ax.items()},'scope':'joint avoidance and single residue mass on coprime product period M*B with each earlier modulus dividing B','arbitrary_common_period_lift_proved':False,'full_arithmetic_lemma_in_lean':False,'full_theorem_b_in_lean':False,'mathcert_certified':False}
 if out!=E:
  assert (E/'INDEPENDENCE_KERNEL_STDOUT_001.txt').read_bytes()==log
  assert json.loads((E/'INDEPENDENCE_KERNEL_REPLAY_001.json').read_text())==r
 (out/'INDEPENDENCE_KERNEL_STDOUT_001.txt').write_bytes(log)
 (out/'INDEPENDENCE_KERNEL_REPLAY_001.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({'result':'PASS','axiom_reports':len(ax),'source_sha256':r['source_sha256']}))
if __name__=='__main__':main()
