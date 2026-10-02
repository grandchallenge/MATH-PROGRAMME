#!/usr/bin/env python3
"""Reconstruct and verify the exact Volume III PROOF / PROGRAM RC1 source archive."""
from __future__ import annotations
import base64, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / "SOURCE_TRANSPORT_MANIFEST.json").read_text(encoding="utf-8"))
chunks = []
for part in manifest["ordered_parts"]:
    p = ROOT / part["file"]
    data = p.read_text(encoding="ascii")
    if len(data) != part["chars"]:
        raise SystemExit(f"length mismatch: {p.name}: {len(data)} != {part['chars']}")
    chunks.append(data)
encoded = "".join(chunks)
if len(encoded) != manifest["base64_length"]:
    raise SystemExit(f"base64 length mismatch: {len(encoded)}")
raw = base64.b64decode(encoded, validate=True)
if len(raw) != manifest["decoded_size"]:
    raise SystemExit(f"decoded size mismatch: {len(raw)}")
sha = hashlib.sha256(raw).hexdigest()
if sha != manifest["decoded_sha256"]:
    raise SystemExit(f"sha256 mismatch: {sha}")
out = ROOT / manifest["decoded_filename"]
out.write_bytes(raw)
print(f"verified {out.name} bytes={len(raw)} sha256={sha}")
