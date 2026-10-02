# Optional Reproducibility Build

Mathematical review does not require compilation. This recipe exists only for reviewers who want to inspect source or reproduce the rendered representation.

## Environment used for the admitted Gate-7 freeze

- LuaHBTeX 1.17.0 (TeX Live 2023/Debian)
- makeindex 2.17 (TeX Live 2023)
- Python 3.12.3

## Build

Unpack the source archive and run:

```bash
set -euo pipefail

build_tex() {
  stem="$1"
  lualatex -interaction=nonstopmode -halt-on-error "${stem}.tex"
  if [ -s "${stem}.idx" ]; then
    makeindex "${stem}.idx"
  fi
  lualatex -interaction=nonstopmode -halt-on-error "${stem}.tex"
  lualatex -interaction=nonstopmode -halt-on-error "${stem}.tex"
}

build_tex main
build_tex solutions_companion
build_tex plates_folio

for lab in labs/*.py; do
  python "$lab"
done
```

Byte-identical PDF output is not required for Gate 8 because TeX metadata can vary by environment/time. If you rebuild, record environment details and output hashes. Compare mathematical content and rendering separately from byte identity.
