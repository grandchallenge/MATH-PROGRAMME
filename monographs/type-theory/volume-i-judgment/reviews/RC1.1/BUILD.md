# Optional Reproducibility Build — Volume I RC1.1

Compilation is **not required for Gate 8 mathematical review**. The supplied PDFs are the primary reading surface.

The exact admitted source archive is `assets/04_GCL_Type_Theory_Volume_I_JUDGMENT_RC1_1_Source.zip` with SHA-256 `013fd6b5f78a8bb45711bb9e167321f7ca58324b7a0ae3f0c7e594ba63a96e3b`.

The repository reviewer renderings were built with LuaLaTeX/latexmk and fixed `SOURCE_DATE_EPOCH=1788684079`. A typical rebuild is:

```bash
unzip 04_GCL_Type_Theory_Volume_I_JUDGMENT_RC1_1_Source.zip
export SOURCE_DATE_EPOCH=1788684079
export FORCE_SOURCE_DATE=1
latexmk -lualatex -interaction=nonstopmode -halt-on-error main.tex
latexmk -lualatex -interaction=nonstopmode -halt-on-error solutions_companion.tex
latexmk -lualatex -interaction=nonstopmode -halt-on-error plates_folio.tex
```

Expected page counts are `146/50/43` for manuscript/solutions/folio.

Historical Gate-7 PDF hashes and reviewer-rendering hashes are distinct identity fields. A rebuild should be judged against the exact source identity, expected page counts, and visual/content checks unless the build environment is intentionally pinned tightly enough for byte-for-byte PDF reproduction.
