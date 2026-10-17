#!/usr/bin/env python3
"""Bounded real page/source content assertions, not full publication parity."""
import base64,datetime,hashlib,html.parser,json,subprocess
from pathlib import Path
ROOT=Path(__file__).parent
EXCERPTS=[
 'A result belongs here only when the public record states what crossed the boundary and what did not.',
 'Every registered problem has a navigable catalogue entry',
 'The restricted result therefore does not qualify the original five-claim route by implication.',
 'The verification does not claim line-by-line semantic equivalence with every prose statement in the source exposition.',
 'documented mathematical exposition']
class Collector(html.parser.HTMLParser):
 def __init__(self):super().__init__();self.data=[]
 def handle_data(self,s):self.data.append(s)
def gh(url):
 p=subprocess.run(['gh','api',url],capture_output=True,text=True,check=True,timeout=25)
 return json.loads(p.stdout)
def public(url):return subprocess.check_output(['curl','-fsSL','--max-time','20',url],timeout=25)
def digest(data):return hashlib.sha256(data).hexdigest()
def main():
 prior=(ROOT/'ESTATE_ADVERSE_DEPLOYMENTS_20261017.json').read_bytes()
 a=json.loads(prior);rows={x['repository']:x for x in a['pages_deployments']}
 assert len(rows)==2
 mat=rows['grandchallenge/MATH-PROGRAMME'];ae=rows['grandchallenge/AETHER']
 item=gh('repos/grandchallenge/MATH-PROGRAMME/contents/docs/SHOWCASE.md?ref='+mat['protected_source_sha'])
 raw=base64.b64decode(item['content']);source=raw.decode()
 assert item['sha']==hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
 html=public('https://grandchallenge.github.io/MATH-PROGRAMME/SHOWCASE/')
 parser=Collector();parser.feed(html.decode())
 visible=' '.join(' '.join(parser.data).split())
 matching=[x for x in EXCERPTS if x in source and x in visible]
 if len(matching)!=len(EXCERPTS):raise ValueError('protected source does not match sampled public text')
 manifest=public('https://grandchallenge.github.io/AETHER/source-version.json')
 ident=json.loads(manifest)
 if not (ident.get('schema_version')=='aether-pages-source-v1'
         and ident.get('source_ref')=='refs/heads/main'
         and ident.get('source_sha')==ae['protected_source_sha']):
  raise ValueError('AETHER live Pages source-version marker mismatch')
 doc={'record_type':'GCL_PAAR_001_PUBLIC_CONTENT_SPECIMEN/1',
  'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'source_deployment_evidence_sha256':digest(prior),
  'showcase':{'source_commit_sha':mat['protected_source_sha'],
    'source_git_blob_sha':item['sha'],'rendered_url':'https://grandchallenge.github.io/MATH-PROGRAMME/SHOWCASE/',
    'live_html_sha256':digest(html),'matching_excerpts':matching,'matched':len(matching),
    'full_document_equivalence_verified':False},
  'aether':{'source_commit_sha':ae['protected_source_sha'],
    'live_version_url':'https://grandchallenge.github.io/AETHER/source-version.json',
    'live_manifest_sha256':digest(manifest),'source_marker_verified':True,
    'full_document_equivalence_verified':False},
  'all_publications_certified':False,'scientific_certification':False,
  'gcl_wide_assurance_certified':False}
 path=ROOT/'ESTATE_PUBLIC_CONTENT_SPECIMEN_20261017.json'
 path.write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'result':'PASS_BOUNDED_PUBLIC_CONTENT_AND_VERSION_SPECIMENS',
  'showcase_matching_excerpts':len(matching),'aether_source_commit_matched':True,
  'full_parity_certified':False,'sha256':digest(path.read_bytes())},sort_keys=True))
if __name__=='__main__':main()
