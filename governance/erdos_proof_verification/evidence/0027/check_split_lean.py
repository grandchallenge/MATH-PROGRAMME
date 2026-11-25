"""Replay prime-power splitting and actual CRT fibre density on pinned inputs."""
import argparse,hashlib,json,os,pathlib,re,subprocess,tempfile
E=pathlib.Path(__file__).resolve().parent
P=E.parents[3]/'experiments/erdos_proof_verification/0027'
AX={'propext','Classical.choice','Quot.sound'}
NAMES=set('smooth_power_allocation rough_power_allocation split_lcm_positive congruence_transport family_density smooth_one rough_one smooth_prime rough_prime smooth_dvd rough_dvd smooth_lcm rough_lcm lcm_split family_split smooth_mul rough_mul cross_coprime split_exists split_unique'.split())
def sha(b):return hashlib.sha256(b).hexdigest()
def checked(args,**kw):
 r=subprocess.run([str(x) for x in args],stdout=subprocess.PIPE,stderr=subprocess.PIPE,**kw)
 if r.returncode:raise RuntimeError((r.stdout+r.stderr).decode())
 return r.stdout
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--cache-root',required=True,type=pathlib.Path)
 p.add_argument('--lean',required=True,type=pathlib.Path)
 p.add_argument('--output',required=True,type=pathlib.Path)
 p.add_argument('--managed-workspace')
 a=p.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
 src=[P/n for n in ['Erdos27CRT.lean','Erdos27Weighted.lean','Erdos27Independence.lean','Erdos27Period.lean','Erdos27Split.lean']]
 if a.managed_workspace:
  w=pathlib.Path(checked(['gcl-lean-work','path',a.managed_workspace]).decode().strip())
  assert w==a.cache_root.resolve()
  for f in src+[P/'lakefile.toml',P/'lake-manifest.json',P/'lean-toolchain']:
   assert f.read_bytes()==(w/f.name).read_bytes(),f.name
  prefix=['gcl-lean-work','run',a.managed_workspace]
  v=checked(prefix+['lean','--version'],cwd=w).decode().strip()
 else:
  v=checked([a.lean,'--version'],cwd=P).decode().strip()
 assert 'version 4.33.0' in v and 'd8b18978322de05a8f3dba51ef03cf5461676c17' in v
 deps={};paths=[]
 for x in json.loads((P/'lake-manifest.json').read_text())['packages']:
  d=a.cache_root.resolve()/'.lake/packages'/x['name']
  assert checked(['git','-C',d,'rev-parse','HEAD']).decode().strip()==x['rev']
  assert not checked(['git','-C',d,'status','--porcelain','--untracked-files=no']).strip()
  deps[x['name']]=x['rev'];paths.append(str(d/'.lake/build/lib/lean'))
 if a.managed_workspace:
  checked(prefix+['lake','build','Erdos27CRT','Erdos27Weighted','Erdos27Independence','Erdos27Period'],cwd=w)
  log=checked(prefix+['lean','Erdos27Split.lean'],cwd=w)
 else:
  with tempfile.TemporaryDirectory() as t:
   env=dict(os.environ,LEAN_PATH=os.pathsep.join([t]+paths))
   for f in src[:-1]:
    checked([a.lean,'-o',pathlib.Path(t)/(f.stem+'.olean'),f],cwd=P,env=env)
   log=checked([a.lean,src[-1]],cwd=P,env=env)
 s=log.decode();reports=re.findall(r"'Erdos27Split\.(\w+)' depends on axioms: \[([^\]]*)\]",s)
 ax={n:set(x.split(', ')) for n,x in reports}
 assert len(reports)==len(NAMES) and set(ax)==NAMES and all(x<=AX for x in ax.values())
 assert not any(x in s for x in ('sorryAx','error:','warning:'))
 r={'record_type':'ERDOS_PV_0027_PRIME_SPLIT_REPLAY/1','result':'PASS','lean_version':v,'dependency_revisions':deps,'source_sha256':{f.name:sha(f.read_bytes()) for f in src},'manifest_sha256':sha((P/'lake-manifest.json').read_bytes()),'stdout_sha256':sha(log),'axioms':{n:sorted(x) for n,x in ax.items()},'scope':'existence and uniqueness of smooth rough prime-power split, LCM product, original modulus CRT fibre density','prime_power_split_in_lean':True,'actual_fibre_density_in_lean':True,'full_theorem_b_in_lean':False,'mathcert_certified':False}
 if out!=E:
  assert (E/'SPLIT_KERNEL_STDOUT_001.txt').read_bytes()==log
  assert json.loads((E/'SPLIT_KERNEL_REPLAY_001.json').read_text())==r
 (out/'SPLIT_KERNEL_STDOUT_001.txt').write_bytes(log)
 (out/'SPLIT_KERNEL_REPLAY_001.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({'result':'PASS','axiom_reports':len(ax),'source_sha256':r['source_sha256']}))
if __name__=='__main__':main()
