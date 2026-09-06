from __future__ import annotations
import base64, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / "SOURCE_TRANSPORT_MANIFEST.json").read_text())
parts = []
for rec in manifest["parts"]:
    p = ROOT / rec["file"]
    text = p.read_text()
    assert len(text) == rec["chars"], (p, len(text), rec["chars"])
    assert hashlib.sha256(text.encode()).hexdigest() == rec["sha256"], p
    parts.append(text)
b64 = "".join(parts)
assert len(b64) == manifest["base64_chars"]
data = base64.b64decode(b64, validate=True)
assert len(data) == manifest["decoded_bytes"]
digest = hashlib.sha256(data).hexdigest()
assert digest == manifest["decoded_sha256"], digest
out = ROOT / "GCL_Type_Theory_Volume_I_JUDGMENT_RC1_1_Rebuild_Source.zip"
out.write_bytes(data)
print(f"PASS bytes={len(data)} sha256={digest} output={out.name}")
