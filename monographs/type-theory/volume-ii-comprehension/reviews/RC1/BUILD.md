# Optional Reproducibility Build — Volume II RC1

Compilation is **not required for Gate 8 mathematical review**. The supplied PDFs are the primary reading surface.

The exact admitted source archive is `assets/04_GCL_Type_Theory_Volume_II_COMPREHENSION_RC1_Source.zip` with SHA-256 `1e1f4ae917e50514dc0a74fa706d30ad0d1c3dbf9ac2f45d7c8ad2445f3fd95a`.

The repository reviewer renderings were built with LuaLaTeX/latexmk and fixed `SOURCE_DATE_EPOCH=1788664742`. A typical rebuild is:

```bash
unzip 04_GCL_Type_Theory_Volume_II_COMPREHENSION_RC1_Source.zip
export SOURCE_DATE_EPOCH=1788664742
export FORCE_SOURCE_DATE=1
latexmk -lualatex -interaction=nonstopmode -halt-on-error main.tex
latexmk -lualatex -interaction=nonstopmode -halt-on-error solutions_companion.tex
latexmk -lualatex -interaction=nonstopmode -halt-on-error plates_folio.tex
```

Expected page counts are `96/59/43` for manuscript/solutions/folio.

Historical Gate-7 PDF hashes and reviewer-rendering hashes are distinct identity fields. A rebuild should be judged against the exact source identity, expected page counts, and visual/content checks unless the build environment is intentionally pinned tightly enough for byte-for-byte PDF reproduction.
