#!/usr/bin/env python3
"""Static consistency checks for a GCL Type Theory volume workspace."""
from __future__ import annotations
import argparse, re, subprocess, sys
from pathlib import Path

REQUIRED=["main.tex","solutions_companion.tex","series_style.tex","series_macros.tex","VOLUME_PLAN.md","CLAIMS_LEDGER.md","THEOREM_AUDIT.md","ILLUSTRATION_REGISTER.md","BIBLIOGRAPHY_AUDIT.md","EXERCISE_AUDIT.json","PUBLICATION_AUDIT_RC1.md","plates_folio.tex"]

def fail(msg, errors): errors.append(msg)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("workspace"); ap.add_argument("--rc",action="store_true",help="apply release-candidate strictness"); ap.add_argument("--compile",action="store_true")
    a=ap.parse_args(); root=Path(a.workspace).resolve(); errors=[]; warnings=[]
    for f in REQUIRED:
        if not (root/f).exists(): fail(f"missing required file: {f}",errors)
    plates=sorted((root/"plates").glob("plate*.tex")) if (root/"plates").exists() else []
    if not plates: fail("no plate sources found",errors)
    for p in plates:
        s=p.read_text(errors="ignore")
        if "gclplate" not in s: warnings.append(f"{p.name}: missing gclplate style")
        if "\\caption{" not in s: fail(f"{p.name}: missing caption",errors)
        if "\\label{plate:" not in s: fail(f"{p.name}: missing plate label",errors)
        if "gcllabel" not in s: warnings.append(f"{p.name}: no gcllabel text shield found; inspect arrow/text intersections manually")
    if (root/"main.tex").exists():
        s=(root/"main.tex").read_text(errors="ignore")
        if "\\input{series_style.tex}" not in s: fail("main.tex does not import series_style.tex",errors)
        if "research thesis" not in s.lower(): warnings.append("main.tex does not visibly restate the research-thesis status")
    if a.rc:
        bad=re.compile(r"\b(TODO|TBD|FIXME|PLACEHOLDER)\b",re.I)
        for p in root.rglob("*"):
            if p.is_file() and p.suffix.lower() in {".tex",".md",".json",".py"}:
                try: txt=p.read_text(errors="ignore")
                except Exception: continue
                if bad.search(txt): fail(f"RC forbidden marker in {p.relative_to(root)}",errors)
    if a.compile and not errors:
        for target in ["main.tex","solutions_companion.tex","plates_folio.tex"]:
            r=subprocess.run(["lualatex","-interaction=nonstopmode","-halt-on-error",target],cwd=root,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
            if r.returncode: fail(f"compile failed: {target}",errors)
    print(f"plates={len(plates)} errors={len(errors)} warnings={len(warnings)}")
    for x in warnings: print("WARN:",x)
    for x in errors: print("ERROR:",x)
    sys.exit(1 if errors else 0)
if __name__=="__main__": main()
