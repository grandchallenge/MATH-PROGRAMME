"""MkDocs lifecycle hooks for pinned OAI-26 source and editorial pages."""
from __future__ import annotations
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from oai26_compendium import build, clean


def on_pre_build(config, **kwargs):
    result = build()
    if result["families"] != 372 or result["manuscript_paths"] != 719:
        raise RuntimeError("OAI-26 catalogue build incomplete")
    print("OAI26_COMPENDIUM_BUILD " + str(result))


def on_post_build(config, **kwargs):
    site = Path(config["site_dir"])
    required = [
        site / "oai26/catalogue/index.html",
        site / "oai26/families/001/index.html",
        site / "oai26/families/003/index.html",
        site / "oai26/families/342/index.html",
        site / "oai26/families/377/index.html",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    clean()
    if missing:
        raise RuntimeError("OAI-26 rendered-site sentinel pages missing: " + repr(missing))
