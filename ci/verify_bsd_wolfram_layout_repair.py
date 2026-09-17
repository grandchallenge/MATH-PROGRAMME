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

EXPECTED_SEMANTIC_SHA256 = "d05088cf0f88c7e3c0960ebb99973fac19001a2bdb6abff3e92f8a4fe0bc2ec0"
EXPECTED_SEMANTIC_BYTES = 4665
EXPECTED_SEMANTIC_BLOB = "206842583d15acf91eb0e363ddb12cbf124ab0a9"
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
    if (
        len(semantic) != EXPECTED_SEMANTIC_BYTES
        or sha256(semantic) != EXPECTED_SEMANTIC_SHA256
        or git_blob(semantic) != EXPECTED_SEMANTIC_BLOB
    ):
        fail("semantic master changed during presentation-only repair")

    runtime = manifest.get("runtime_validation", {})
    if runtime.get("semantic_master_bytes") != EXPECTED_SEMANTIC_BYTES:
        fail("manifest semantic byte lock disagrees with verifier")
    if runtime.get("semantic_master_sha256") != EXPECTED_SEMANTIC_SHA256:
        fail("manifest semantic sha256 lock disagrees with verifier")
    if runtime.get("semantic_master_git_blob") != EXPECTED_SEMANTIC_BLOB:
        fail("manifest semantic git-blob lock disagrees with verifier")

    repair = manifest.get("layout_repair", {})
    if repair.get("protected_base") != "989fd25de2d65eee4da65fc7ce1b10bebc91f963":
        fail("layout repair is not bound to the protected #1003 merge")
    if repair.get("semantic_changes") is not False:
        fail("layout repair claims a semantic change")
    if repair.get("semantic_master_unchanged_sha256") != EXPECTED_SEMANTIC_SHA256:
        fail("repair semantic sha256 lock disagrees with verifier")
    if repair.get("semantic_master_unchanged_bytes") != EXPECTED_SEMANTIC_BYTES:
        fail("repair semantic byte lock disagrees with verifier")
    if repair.get("semantic_master_unchanged_git_blob") != EXPECTED_SEMANTIC_BLOB:
        fail("repair semantic git-blob lock disagrees with verifier")
    if repair.get("free_coordinate_typography_synthesis_forbidden") is not True:
        fail("free-coordinate typography synthesis is not explicitly forbidden")

    layout = LAYOUT.read_text(encoding="utf-8")
    for token in ("ContourPlot", "Grid", "Framed", "Pane", "1536", "1024"):
        if token not in layout:
            fail(f"Wolfram layout reference missing {token!r}")
    for token in ("Lₑ⁽ʳ⁾(1) / r!", "Ωₑ", "Reg(E/ℚ)", "#E(ℚ)ₜₒᵣₛ²"):
        if token not in layout:
            fail(f"Wolfram layout reference lost Plate IV typesetting token {token!r}")

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

    identity_mismatches: list[str] = []
    for plate in plates:
        path = ROOT / plate["live_path"]
        data = path.read_bytes()
        text = data.decode("utf-8")
        actual_bytes = len(data)
        actual_sha256 = sha256(data)
        actual_blob = git_blob(data)
        if (
            actual_bytes != plate["bytes"]
            or actual_sha256 != plate["sha256"]
            or actual_blob != plate["git_blob"]
        ):
            identity_mismatches.append(
                f"{plate['plate_id']}: bytes={actual_bytes} sha256={actual_sha256} git_blob={actual_blob}"
            )
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
        if plate["plate_id"] == "BSD-OVERTURE-PLATE-IV":
            for raw_token in ("L_E^", "Ω_E", "Reg(E/Q)", "#Sha(E/Q)", "_tors"):
                if raw_token in text:
                    fail(f"raw source-style math token leaked into Plate IV: {raw_token}")
            for typeset_token in ("Lₑ⁽ʳ⁾", "Ωₑ", "Reg(E/ℚ)", "#Sha(E/ℚ)", "#E(ℚ)ₜₒᵣₛ²", "ordₛ₌₁"):
                if typeset_token not in text:
                    fail(f"Plate IV lost typeset math token: {typeset_token}")
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

    print("BSD Wolfram layout repair verification: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
