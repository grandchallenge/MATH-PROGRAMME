#!/usr/bin/env python3
"""Isolated, nonauthoritative Zensical migration probe for GCL compendia.

Never replace the production MkDocs workflow or write generated files to
tracked docs/. Build a temporary copy and fail if protected input is missing.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from erdos_compendium import build as build_erdos  # noqa: E402
from erdos_compendium_hook import (  # noqa: E402
    ERDOS_HOME_MARKER, ERDOS_SHOWCASE_MARKER, ERDOS_LANDING_MARKER,
    erdos_home_status, erdos_showcase_status, erdos_landing_status,
)
from oai26_compendium import build as build_oai26  # noqa: E402
from zensical_semantic_parity import (  # noqa: E402
    audit as audit_rendered_content, governed_asset_census, search_parity)
from zensical_documentary_assets import rewrite_temporary_docs  # noqa: E402

DOCS = ROOT / ".zensical-probe-docs"
CONFIG = ROOT / "zensical-probe.yml"
SITE = ROOT / ".zensical-probe-site"
BASELINE = ROOT / ".mkdocs-probe-site"
REPORT = ROOT / "zensical-parity-report.json"

SENTINELS = (
    "index.html",
    "erdos/catalogue/index.html",
    "erdos/problems/0001/index.html",
    "erdos/problems/1221/index.html",
    "oai26/catalogue/index.html",
    "oai26/families/001/index.html",
    "oai26/families/377/index.html",
    "CMDG_CM4/index.html",
)


def inject(path: Path, marker: str, value: str) -> None:
    original = path.read_text(encoding="utf-8")
    if original.count(marker) != 1:
        raise RuntimeError(f"expected one {marker} in {path}")
    path.write_text(original.replace(marker, value), encoding="utf-8")


def prepare() -> None:
    for p in (DOCS, CONFIG, SITE):
        if p.exists():
            raise RuntimeError(f"refusing to overwrite existing probe material: {p}")
    shutil.copytree(ROOT / "docs", DOCS, symlinks=False)
    documentary_assets = rewrite_temporary_docs(DOCS)
    erdos = build_erdos(output=DOCS / "erdos")
    oai = build_oai26(output_dir=DOCS / "oai26")
    if erdos["problems"] != 1221 or erdos["pages"] < 1222:
        raise RuntimeError(f"Erdős generator incomplete: {erdos}")
    if oai["families"] != 375 or oai["manuscript_paths"] != 730:
        raise RuntimeError(f"OAI26 generator incomplete: {oai}")

    inject(DOCS / "index.md", ERDOS_HOME_MARKER, erdos_home_status())
    inject(DOCS / "SHOWCASE.md", ERDOS_SHOWCASE_MARKER, erdos_showcase_status())
    inject(DOCS / "erdos" / "index.md", ERDOS_LANDING_MARKER, erdos_landing_status())

    config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
    if config.get("hooks") != ["ci/erdos_compendium_hook.py", "ci/oai26_compendium_hook.py"]:
        raise RuntimeError("hook inventory changed: do not silently drop new hooks")
    config.pop("hooks")
    # Candidate-only footer contrast repair. Never mutate authored docs or
    # production MkDocs; this is a copied, isolated renderer compatibility fix.
    override = DOCS / "stylesheets" / "zensical-contrast.css"
    override.write_text(
        "/* G1 B03: accessible footer for Zensical on dark footer surface. */\n"
        ".md-footer .md-copyright, .md-footer .md-copyright__highlight, "
        ".md-footer a[href$=\"zensical.org/\"] "
        "{ color: #f2f5fa !important; }\n"
        "@media (prefers-color-scheme: light) { "
        ".md-typeset .highlight .kd, .md-typeset .highlight .kt "
        "{ color: #214a88 !important; } }\n", encoding="utf-8")
    extra_css = config.get("extra_css", [])
    if not isinstance(extra_css, list):
        raise RuntimeError("invalid extra_css inventory")
    config["extra_css"] = [*extra_css, "stylesheets/zensical-contrast.css"]
    focus = DOCS / "javascripts" / "zensical-code-focus.js"
    focus.write_text(
        "/* Isolated renderer B03: allow keyboard focus on overflow code. */\n"
        "(() => { const apply = () => { document.querySelectorAll('pre code').forEach(e => { "
        "if (e.scrollWidth > e.clientWidth && e.clientWidth > 0) { "
        "e.tabIndex = 0; e.setAttribute('aria-label', 'Scrollable code block'); } "
        "}); }; if (document.readyState === 'loading') "
        "document.addEventListener('DOMContentLoaded', apply, {once:true}); "
        "else apply(); })();\n", encoding="utf-8")
    extra_js = config.get("extra_javascript", [])
    if not isinstance(extra_js, list):
        raise RuntimeError("invalid extra_javascript inventory")
    config["extra_javascript"] = [*extra_js, "javascripts/zensical-code-focus.js"]
    config["docs_dir"] = DOCS.name
    config["site_dir"] = SITE.name
    CONFIG.write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(json.dumps({"prepared": True, "erdos": erdos, "oai26": oai,
                      "temporary_documentary_asset_rebases": documentary_assets}, sort_keys=True))


def verify() -> None:
    if not BASELINE.is_dir() or not SITE.is_dir():
        raise RuntimeError("both baseline and candidate output directories required")
    baseline_routes = {p.relative_to(BASELINE).as_posix() for p in BASELINE.rglob("*.html")}
    candidate_routes = {p.relative_to(SITE).as_posix() for p in SITE.rglob("*.html")}
    missing = sorted(baseline_routes - candidate_routes)
    extra = sorted(candidate_routes - baseline_routes)
    missing_sentinels = [p for p in SENTINELS if not (SITE / p).is_file()]
    unexpanded = []
    for path in ("index.html", "SHOWCASE/index.html", "erdos/index.html"):
        page = SITE / path
        if page.is_file() and "GCL_ERDOS_" in page.read_text(encoding="utf-8"):
            unexpanded.append(path)
    semantic = audit_rendered_content(BASELINE, SITE, baseline_routes & candidate_routes)
    assets = governed_asset_census(BASELINE,SITE)
    search = search_parity(BASELINE,SITE,baseline_routes & candidate_routes)
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    report = {
        "record_type": "GCL_ZENSICAL_RENDERER_PROBE/2",
        "source_head": head,
        "source_locked_erdos_counts": __import__("erdos_compendium_hook").protected_erdos_counts(),
        "oai26_expected_families": 372,
        "oai26_expected_manuscript_paths": 719,
        "rendered_content_audit": semantic,
        "governed_static_asset_parity": assets,
        "search_index_audit": search,
        "candidate_generator": "zensical==0.1.1",
        "baseline_html_routes": len(baseline_routes),
        "candidate_html_routes": len(candidate_routes),
        "missing_count": len(missing),
        "extra_count": len(extra),
        "missing_routes_first_40": missing[:40],
        "extra_routes_first_40": extra[:40],
        "missing_sentinels": missing_sentinels,
        "unexpanded_status_markers": unexpanded,
        "route_parity": not missing and not extra and not missing_sentinels and not unexpanded,
        "critical_parity": not missing and not extra and not missing_sentinels and not unexpanded
            and not semantic["critical_issue_count"]
            and assets["byte_identical_on_shared_source_assets"]
            and search["search_parity_proven"],
        "production_switch_authorized": False,
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    if not report["critical_parity"]:
        raise SystemExit("Zensical critical parity FAIL; production MkDocs remains authoritative")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("prepare", "verify"))
    args = parser.parse_args()
    if args.action == "prepare":
        prepare()
    else:
        verify()
