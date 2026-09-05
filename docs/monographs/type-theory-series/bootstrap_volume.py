#!/usr/bin/env python3
"""Instantiate a new GCL Type Theory monograph workspace from the series contract."""
from __future__ import annotations
import argparse, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = json.loads((ROOT / "SERIES_MANIFEST.json").read_text())

def volume_record(key: str):
    key=key.lower()
    for v in MANIFEST["volumes"]:
        if v["number"].lower()==key or v["slug"].lower()==key or v["title"].lower()==key:
            return v
    raise SystemExit(f"Unknown volume {key!r}. Use I–X or a manifest slug.")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("volume", help="II–X or manifest slug")
    ap.add_argument("out", help="output directory")
    args=ap.parse_args()
    v=volume_record(args.volume)
    out=Path(args.out).resolve()
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"Refusing non-empty output directory: {out}")
    out.mkdir(parents=True, exist_ok=True)
    (out/"plates").mkdir(); (out/"labs").mkdir(); (out/"evidence").mkdir()
    shutil.copy(ROOT/"templates"/"series_style.tex", out/"series_style.tex")
    shutil.copy(ROOT/"templates"/"series_macros.tex", out/"series_macros.tex")
    shutil.copy(ROOT/"templates"/"plate_template.tex", out/"plates"/"plate01.tex")
    plan=f'''# Volume {v["number"]} — {v["title"]}: {v["subtitle"]}\n\n## Governing question\n\n{v["governing_question"]}\n\n## Formal scope\n\n{v.get("formal_core","Define before drafting.")}\n\n## Inherited machinery\n\n- [ ] List exact concepts/results inherited from previous volumes.\n- [ ] State which are reintroduced for self-containment.\n\n## Semantics in scope\n\n- [ ] Operational relation(s).\n- [ ] Equational/definitional equality.\n- [ ] Model/denotational semantics if used.\n\n## Intended metatheory\n\n| Result | Prove / cite / assume / postpone | Exact calculus | Evidence |\n|---|---|---|---|\n| | | | |\n\n## Central distinctions not to collapse\n\n- [ ] Add volume-specific distinctions.\n\n## Chapter and laboratory map\n\nTarget: 12–15 teaching chapters, default 14. One lab per teaching chapter unless justified.\n\n## Initial plate register\n\nDefault target 42, acceptable 36–48 without padding.\n\n## Exercise ecology\n\nDefault 12/chapter: 3 Checkpoint, 3 Core, 2 Synthesis, 2 Proof Workshop, 1 Design Clinic, 1 Challenge.\n\n## Bibliography / attribution plan\n\n- [ ] Primary sources.\n- [ ] Modern expository references.\n- [ ] Historical/date claims needing verification.\n\n## Pressure points against the series thesis\n\n- [ ] What could this volume show type theory cannot express or unify cleanly?\n\n## Next-volume threshold\n\n{v.get("next_threshold", "Define the forced transition.")}\n\n## Smallest safe executable tranche\n\nDefine Chapters 1–2 + lab(s) + first 4–6 plates + exercises before broad expansion.\n'''
    (out/"VOLUME_PLAN.md").write_text(plan)
    (out/"CLAIMS_LEDGER.md").write_text("# Claims Ledger\n\n| ID | Claim | Status (theorem / cited / computed / analogy / conjecture) | Scope | Evidence/source |\n|---|---|---|---|---|\n")
    (out/"THEOREM_AUDIT.md").write_text("# Theorem Audit\n\n| Result | Statement scope | Dependencies | Critical cases | Proof status |\n|---|---|---|---|---|\n")
    (out/"ILLUSTRATION_REGISTER.md").write_text("# Illustration Register\n\n## Plate 1 — [PLANNED] TITLE\n\n**Pedagogical burden:**\n\n**Composition:**\n\n**Analogy/scope limit:**\n")
    (out/"BIBLIOGRAPHY_PLAN.md").write_text("# Bibliography Plan\n\n## Primary sources\n\n## Modern references\n\n## Historical claims requiring verification\n")
    (out/"BIBLIOGRAPHY_AUDIT.md").write_text("# Bibliography Audit\n\n| Claim/name | Source | Primary? | Verified metadata | Notes |\n|---|---|---|---|---|\n")
    (out/"PUBLICATION_AUDIT_RC1.md").write_text("# Publication Audit RC1\n\nComplete at publication stage.\n")
    (out/"EXERCISE_AUDIT.json").write_text(json.dumps({"volume":v["number"],"chapters":[],"complete":False},indent=2)+"\n")
    main_tex=rf'''\documentclass[11pt,openany]{{book}}
\input{{series_style.tex}}
\input{{series_macros.tex}}
\hypersetup{{colorlinks=true,linkcolor=GCLBlue,urlcolor=GCLBlue,citecolor=GCLGreen,
  pdftitle={{{v['title']}: {v['subtitle']}}},pdfauthor={{Grand Challenge Labs}}}}
\begin{{document}}
\frontmatter
\begin{{titlepage}}
\pagecolor{{GCLPale!35}}\color{{GCLInk}}\centering
\vspace*{{1.2cm}}
{{\small\sffamily GRAND CHALLENGE MONOGRAPH COLLECTION\par}}
\vspace{{1.1cm}}{{\Huge\bfseries TYPE THEORY\par}}
\vspace{{0.25cm}}{{\Large The Grand Unified Theory of Computation\par}}
\vspace{{1cm}}{{\color{{GCLWarm}}\rule{{0.76\textwidth}}{{1.1pt}}\par}}
\vspace{{0.8cm}}{{\fontsize{{31}}{{35}}\selectfont\bfseries {v['title']}\par}}
\vspace{{0.25cm}}{{\LARGE {v['subtitle']}\par}}
\vspace{{0.25cm}}{{\large Volume {v['number']}\par}}
\vfill {{\large Grand Challenge Labs\par}}
\end{{titlepage}}
\nopagecolor\color{{GCLInk}}
\chapter*{{Scope and series thesis}}
The phrase ``grand unified theory'' names a research thesis, not an established theorem. This volume asks: {v['governing_question']}
\tableofcontents
\mainmatter
\chapter{{Chapter title}}
State the problem before the notation.\n
\input{{plates/plate01.tex}}
\backmatter
\chapter*{{Transition}}
{v.get('next_threshold','State the threshold into the next volume.')}
\printindex
\end{{document}}
'''
    (out/"main.tex").write_text(main_tex)
    (out/"solutions_companion.tex").write_text(r'''\documentclass[11pt,openany]{book}
\input{series_style.tex}
\input{series_macros.tex}
\begin{document}
\frontmatter\chapter*{Instructor and Self-Study Solutions Companion}\mainmatter
\chapter{Solutions}\textit{Populate every exercise with a solution or explicit rubric.}
\end{document}
''')
    (out/"plates_folio.tex").write_text(r'''\documentclass[11pt]{article}
\input{series_style.tex}
\begin{document}
\input{plates/plate01.tex}
\end{document}
''')
    (out/"README.md").write_text(f"# Volume {v['number']}: {v['title']} — {v['subtitle']}\n\nStart with `VOLUME_PLAN.md`. Build with LuaLaTeX. Run the series validator before release.\n")
    print(out)

if __name__ == "__main__": main()
