#!/usr/bin/env python3
"""Zensical-only authored-documentary asset depth correction in copied docs.

Never edits protected source Markdown; fail on uncertain source, asset or scope.
"""
from __future__ import annotations
import hashlib
from pathlib import Path
import re

DOCUMENTARIES = ('bsd','hodge','navier_stokes','p_vs_np','poincare',
                 'riemann','union_closed','yang_mills')
SOURCE_PREFIX = '../../'
TARGET_PREFIX = '../'
ASSET_FOLDERS = ('assets/','stylesheets/','javascripts/')
PATTERN = re.compile(r'(?P<prefix>\b(?:href|src)=["\'])\.\./\.\./(?P<asset>(?:assets|stylesheets|javascripts)/[^"\']+)(?P<end>["\'])')


def rewrite_temporary_docs(docs_root:Path) -> list[dict]:
    """Return exact provenance of the only allowed path changes."""
    rows=[]
    for slug in DOCUMENTARIES:
        path=docs_root/'documentaries'/f'{slug}.md'
        if not path.is_file():
            raise ValueError('missing documentary source: '+slug)
        original=path.read_text(encoding='utf-8')
        paths=[]
        def replace(match):
            name=match['asset']
            # The rewritten relative link resolves in authored `docs/` copy
            # to exactly the existing static asset that MkDocs includes.
            target=(path.parent/TARGET_PREFIX/name).resolve()
            if not target.is_relative_to(docs_root.resolve()) or not target.is_file():
                raise ValueError('unknown copied documentary asset: '+name)
            paths.append(name)
            return match['prefix']+TARGET_PREFIX+name+match['end']
        updated=PATTERN.sub(replace,original)
        if not paths or len(paths)!=len(set(paths)):
            raise ValueError('ambiguous documentary asset bindings: '+slug)
        # All and only the expected relative static references are rewritten.
        unresolved=re.findall(r'(?:href|src)=["\']\.\./\.\./(?:assets|stylesheets|javascripts)/',updated)
        if unresolved:
            raise ValueError('unconverted documentary asset reference: '+slug)
        path.write_text(updated,encoding='utf-8')
        rows.append({'slug':slug,'source_sha256':hashlib.sha256(original.encode()).hexdigest(),
                     'temporary_sha256':hashlib.sha256(updated.encode()).hexdigest(),
                     'asset_references_rebased':len(paths)})
    return rows
