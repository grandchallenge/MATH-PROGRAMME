"""Build ephemeral OAI-26 reference pages; preserve source inputs only."""
import shutil
from pathlib import Path
from oai26_compendium import generate

def on_pre_build(config, **kwargs):
    evidence=generate()
    if evidence['families']!=372 or evidence['pdfs']!=719:
        raise RuntimeError('OAI26 index incomplete')
    print('OAI26_COMPENDIUM_BUILD', evidence)

def on_post_build(config, **kwargs):
    site=Path(config['site_dir'])
    missing=[str(p) for p in (site/'oai26/catalogue/index.html',site/'oai26/families/001/index.html',site/'oai26/families/377/index.html') if not p.is_file()]
    root=Path(__file__).resolve().parents[1]/'docs/oai26'
    for name in ('catalogue','families'):
        shutil.rmtree(root/name,ignore_errors=True)
    if missing: raise RuntimeError('Missing OAI26 public sentinel '+str(missing))
