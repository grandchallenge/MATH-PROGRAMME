#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

MANIFEST=Path('governance/visual_pedagogy/representation_repair_manifest.json')

def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repository-root',default='.')
    ap.add_argument('--rendered-root',required=True)
    args=ap.parse_args()
    repo=Path(args.repository_root); rendered=Path(args.rendered_root)
    manifest=json.loads((repo/MANIFEST).read_text(encoding='utf-8'))
    errors=[]
    refs=[manifest['review_entry']]
    for output in manifest['outputs']:
        refs.extend(output['derivatives'])
    for item in refs:
        rel=Path(item['path']); expected=item['sha256']
        rp=repo/rel; mp=rendered/rel
        if not rp.is_file(): errors.append(f'missing committed candidate: {rel}'); continue
        if not mp.is_file(): errors.append(f'missing rerendered candidate: {rel}'); continue
        rd=digest(rp); md=digest(mp)
        if rd != expected: errors.append(f'committed digest mismatch {rel}: {rd} != {expected}')
        if md != expected: errors.append(f'rerender digest mismatch {rel}: {md} != {expected}')
        if rp.read_bytes() != mp.read_bytes(): errors.append(f'byte mismatch between committed and rerendered {rel}')
    if errors:
        print('\n'.join(errors)); raise SystemExit(1)
    print(f'visual pedagogy representation repair: verified {len(refs)} deterministic derivatives')
if __name__=='__main__': main()
