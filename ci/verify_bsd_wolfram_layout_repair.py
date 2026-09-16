#!/usr/bin/env python3
"""Fail-closed verifier for the BSD documentary Wolfram-layout repair."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "governance/visual_pedagogy/bsd_exact_object_overhaul.json"
SEMANTIC = ROOT / "tools/bsd_wolfram_semantic_master.wl"
LAYOUT = ROOT / "tools/bsd_wolfram_layout_reference.wl"
COMPOSITOR = ROOT / "tools/compose_bsd_wolfram_plates.py"
ACTIVATION = ROOT / "docs/assets/visual_pedagogy/bsd_exact/bsd_activation.js"
SHARED_RUNTIME = ROOT / "docs/javascripts/documentary.js"

EXPECTED_SEMANTIC_SHA256 = "41b9e926d0edda8fbb65ead57d54fd0985689ca73ac1715731818843cc013936"
EXPECTED_SEMANTIC_BYTES = 4263
EXPECTED_SHARED_RUNTIME_BLOB = "b53dce8861e9eee78ced01758220b3ed3110a22f"
VIEWBOX = 'viewBox="0 0 1536 1024"'


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != "1.2.0":
        fail("unexpected BSD repair manifest schema")
    if manifest.get("state") != "WOLFRAM_LAYOUT_REPAIR_CANDIDATE":
        fail("BSD layout repair is not in the expected candidate state")
    if manifest.get("visual_is_evidence") is not False:
        fail("visual evidence boundary was promoted")

    semantic = SEMANTIC.read_bytes()
    if len(semantic) != EXPECTED_SEMANTIC_BYTES or sha256(semantic) != EXPECTED_SEMANTIC_SHA256:
        fail("semantic master changed during presentation-only repair")

    repair = manifest.get("layout_repair", {})
    if repair.get("protected_base") != "989fd25de2d65eee4da65fc7ce1b10bebc91f963":
        fail("layout repair is not bound to the protected #1003 merge")
    if repair.get("semantic_changes") is not False:
        fail("layout repair claims a semantic change")
    if repair.get("free_coordinate_typography_synthesis_forbidden") is not True:
        fail("free-coordinate typography synthesis is not explicitly forbidden")

    layout = LAYOUT.read_text(encoding="utf-8")
    for token in ("ContourPlot", "Grid", "Framed", "Pane", "1536", "1024"):
        if token not in layout:
            fail(f"Wolfram layout reference missing {token!r}")

    compositor = COMPOSITOR.read_text(encoding="utf-8")
    for forbidden in ("def mappt(", "<text x=", "polyline points=", "font-family=\"Georgia,Times New Roman,serif\""):
        if forbidden in compositor:
            fail(f"superseded free-coordinate compositor primitive returned: {forbidden}")
    if "copies the approved static SVG snapshots" not in compositor:
        fail("replay tool no longer declares snapshot-only behavior")

    shared = SHARED_RUNTIME.read_bytes()
    if git_blob(shared) != EXPECTED_SHARED_RUNTIME_BLOB:
        fail("shared documentary runtime changed; BSD repair must stay scoped")

    activation = ACTIVATION.read_text(encoding="utf-8")
    if "editorial-landscape-3x2" not in activation:
        fail("BSD activation lost landscape geometry binding")

    plates = manifest.get("plates", [])
    if len(plates) != 5:
        fail("expected exactly five governed BSD plates")

    for plate in plates:
        path = ROOT / plate["live_path"]
        data = path.read_bytes()
        text = data.decode("utf-8")
        if len(data) != plate["bytes"]:
            fail(f"byte count mismatch: {plate['plate_id']}")
        if sha256(data) != plate["sha256"]:
            fail(f"sha256 mismatch: {plate['plate_id']}")
        if git_blob(data) != plate["git_blob"]:
            fail(f"git blob mismatch: {plate['plate_id']}")
        if VIEWBOX not in text or plate.get("delivery_aspect_ratio") != "3:2":
            fail(f"landscape geometry mismatch: {plate['plate_id']}")
        if "<title" not in text or "<desc" not in text:
            fail(f"accessible SVG metadata missing: {plate['plate_id']}")
        if 'font-family="Georgia,Times New Roman,serif"' in text:
            fail(f"superseded compositor signature found: {plate['plate_id']}")
        # Reject the original bleeding mode: very long unwrapped visible text runs.
        for block in re.findall(r"<text\b[^>]*>(.*?)</text>", text, flags=re.S):
            plain = re.sub(r"<[^>]+>", "", block).strip()
            if len(plain) > 160 and "<tspan" not in block:
                fail(f"unwrapped visible text run ({len(plain)} chars): {plate['plate_id']}")
        if plate["live_reference"] not in activation:
            fail(f"activation does not bind {plate['plate_id']}")

    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "bsd-exact"
        subprocess.run(
            [sys.executable, str(COMPOSITOR), "--root", str(out), "--hashes"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        for plate in plates:
            expected = (ROOT / plate["live_path"]).read_bytes()
            reproduced = (out / Path(plate["live_path"]).name).read_bytes()
            if reproduced != expected:
                fail(f"deterministic replay mismatch: {plate['plate_id']}")

    print("BSD Wolfram layout repair verification: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
