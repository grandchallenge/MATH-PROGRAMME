#!/usr/bin/env python3
"""Fail-closed verifier for the BSD documentary exact-object delivery."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "governance/visual_pedagogy/bsd_exact_object_overhaul.json"
SEMANTIC = ROOT / "tools/bsd_wolfram_semantic_master.wl"
LAYOUT = ROOT / "tools/bsd_wolfram_layout_reference.wl"
COMPOSITOR = ROOT / "tools/compose_bsd_wolfram_plates.py"
ACTIVATION = ROOT / "docs/assets/visual_pedagogy/bsd_exact/bsd_activation.js"
SHARED_RUNTIME = ROOT / "docs/javascripts/documentary.js"

EXPECTED_SEMANTIC_SHA256 = "d05088cf0f88c7e3c0960ebb99973fac19001a2bdb6abff3e92f8a4fe0bc2ec0"
EXPECTED_SEMANTIC_BYTES = 4665
EXPECTED_SEMANTIC_BLOB = "206842583d15acf91eb0e363ddb12cbf124ab0a9"
EXPECTED_SHARED_RUNTIME_BLOB = "b53dce8861e9eee78ced01758220b3ed3110a22f"
EXPECTED_NATIVE_REPAIR_BASE = "050bde21b0dabb25ae4120d3e2c8d0e271a0efc2"
PLATE_IV_CACHE_TOKEN = "plate_04_strong_bsd_ledger.svg?v=bsd-math-v6-20260917"
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
    if manifest.get("state") != "NATIVE_MATH_PRESENTATION_REPAIR_CANDIDATE":
        fail("BSD native-math presentation repair is not in candidate state")
    if manifest.get("visual_is_evidence") is not False:
        fail("visual evidence boundary was promoted")

    semantic = SEMANTIC.read_bytes()
    if (len(semantic), sha256(semantic), git_blob(semantic)) != (
        EXPECTED_SEMANTIC_BYTES,
        EXPECTED_SEMANTIC_SHA256,
        EXPECTED_SEMANTIC_BLOB,
    ):
        fail("semantic master changed during presentation-only repair")

    runtime = manifest.get("runtime_validation", {})
    if runtime.get("semantic_master_bytes") != EXPECTED_SEMANTIC_BYTES:
        fail("manifest semantic byte lock disagrees with verifier")
    if runtime.get("semantic_master_sha256") != EXPECTED_SEMANTIC_SHA256:
        fail("manifest semantic sha256 lock disagrees with verifier")
    if runtime.get("semantic_master_git_blob") != EXPECTED_SEMANTIC_BLOB:
        fail("manifest semantic git-blob lock disagrees with verifier")
    if runtime.get("native_mathml_img_embedding_smoke_test_completed") is not True:
        fail("native MathML img-embedding smoke-test receipt missing")

    repair = manifest.get("native_math_presentation_repair", {})
    if repair.get("operation_id") != "BSD-DOC-NATIVE-MATH-PRESENTATION-006":
        fail("unexpected native-math repair operation")
    if repair.get("protected_base") != EXPECTED_NATIVE_REPAIR_BASE:
        fail("native-math repair is not bound to the protected #1006 merge")
    if repair.get("semantic_changes") is not False:
        fail("native-math repair claims a semantic change")
    if repair.get("semantic_master_unchanged_sha256") != EXPECTED_SEMANTIC_SHA256:
        fail("native-math semantic sha256 lock disagrees with verifier")
    if repair.get("semantic_master_unchanged_git_blob") != EXPECTED_SEMANTIC_BLOB:
        fail("native-math semantic git-blob lock disagrees with verifier")
    if repair.get("rendering_mode") != "native_mathml_in_svg_foreignObject":
        fail("native-math rendering mode changed")
    gate = repair.get("review_gate", {})
    if gate.get("required") is not True or gate.get("class") != "independent_visual_semantic_review":
        fail("independent visual-semantic review gate missing")

    layout = LAYOUT.read_text(encoding="utf-8")
    for token in ("ContourPlot", "Grid", "Framed", "Pane", "1536", "1024"):
        if token not in layout:
            fail(f"Wolfram layout reference missing {token!r}")

    compositor = COMPOSITOR.read_text(encoding="utf-8")
    for forbidden in ("def mappt(", "<text x=", "polyline points=", 'font-family="Georgia,Times New Roman,serif"'):
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
    if PLATE_IV_CACHE_TOKEN not in activation:
        fail("Plate IV activation is not cache-busted to the reviewed native-math asset")

    plates = manifest.get("plates", [])
    if len(plates) != 5:
        fail("expected exactly five governed BSD plates")

    identity_mismatches: list[str] = []
    for plate in plates:
        path = ROOT / plate["live_path"]
        data = path.read_bytes()
        text = data.decode("utf-8")
        try:
            ET.fromstring(text)
        except ET.ParseError as exc:
            fail(f"invalid SVG XML: {plate['plate_id']}: {exc}")
        actual = (len(data), sha256(data), git_blob(data))
        expected = (plate["bytes"], plate["sha256"], plate["git_blob"])
        if actual != expected:
            identity_mismatches.append(
                f"{plate['plate_id']}: bytes={actual[0]} sha256={actual[1]} git_blob={actual[2]}"
            )
        if VIEWBOX not in text or plate.get("delivery_aspect_ratio") != "3:2":
            fail(f"landscape geometry mismatch: {plate['plate_id']}")
        if "<title" not in text or "<desc" not in text:
            fail(f"accessible SVG metadata missing: {plate['plate_id']}")
        if 'font-family="Georgia,Times New Roman,serif"' in text:
            fail(f"superseded compositor signature found: {plate['plate_id']}")
        for block in re.findall(r"<text\b[^>]*>(.*?)</text>", text, flags=re.S):
            plain = re.sub(r"<[^>]+>", "", block).strip()
            if len(plain) > 160 and "<tspan" not in block:
                fail(f"unwrapped visible text run ({len(plain)} chars): {plate['plate_id']}")

        if plate["plate_id"] == "BSD-OVERTURE-PLATE-IV":
            for raw_token in ("L_E^", "Ω_E", "Reg(E/Q)", "#Sha(E/Q)", "_tors", "Lₑ", "Ωₑ", "native-svg-typeset-v4"):
                if raw_token in text:
                    fail(f"superseded or source-style math leaked into Plate IV: {raw_token}")
            required = (
                'data-bsd-math-rendering="native-mathml-v6"',
                'xmlns="http://www.w3.org/1998/Math/MathML"',
                'aria-label="Strong BSD normalized leading-term identity"',
                "<mfrac>", "<msub>", "<msubsup>", "<munder>", "<mi>ℚ</mi>",
            )
            for token in required:
                if token not in text:
                    fail(f"Plate IV lost native mathematical typesetting structure: {token}")
            if text.count("<mfrac>") < 2 or text.count("<foreignObject") < 7:
                fail("Plate IV native mathematical structure is incomplete")

        if plate["plate_id"] == "BSD-FRONTIER-PLATE-V":
            for raw_token in ("E/Q", "E(Q)", "Sha(E/Q)"):
                if raw_token in text:
                    fail(f"raw rational-field notation leaked into Plate V: {raw_token}")
            for token in ("E/ℚ", "E(ℚ)", "Sha(E/ℚ)"):
                if token not in text:
                    fail(f"Plate V lost normalized rational-field notation: {token}")

        if plate["live_reference"] not in activation:
            fail(f"activation does not bind {plate['plate_id']}")

    if identity_mismatches:
        fail("plate identity receipt mismatch:\n" + "\n".join(identity_mismatches))

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

    print("BSD native-math delivery verification: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
