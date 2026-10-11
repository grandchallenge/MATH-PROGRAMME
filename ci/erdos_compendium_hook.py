"""MkDocs lifecycle for source-locked Erdős reference pages.

Build-only Markdown is removed after rendering so authoritative registry and
authored editorial articles remain the only durable inputs in Git.
"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from erdos_compendium import build, clean, GENERATED  # noqa: E402


def on_pre_build(config, **kwargs):
    result = build()
    if result["problems"] != 1221 or result["pages"] < 1222:
        raise RuntimeError("Erdős site generation incomplete")
    print("ERDOS_COMPENDIUM_BUILD " + str(result))


def on_post_build(config, **kwargs):
    site = Path(config["site_dir"])
    required = [
        site / "erdos/catalogue/index.html",
        site / "erdos/problems/0001/index.html",
        site / "erdos/problems/0002/index.html",
        site / "erdos/problems/0003/index.html",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    clean()
    if missing:
        raise RuntimeError(f"Erdős rendered-site sentinel pages missing: {missing}")
