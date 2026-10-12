#!/usr/bin/env python3
"""Credential-free Colab Lean proof check. All mathematical authority stays outside Colab."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request

TOOLCHAIN = "leanprover/lean4:v4.29.1"
ELAN_RELEASE = "v4.2.4"
ELAN_URL = ("https://github.com/leanprover/elan/releases/download/v4.2.4/"
            "elan-x86_64-unknown-linux-gnu.tar.gz")
ELAN_ARCHIVE_SHA256 = "42b94d4244e8353142c456ec0e4ca6528fd898a6c604d4059f494e706e431f63"
MAX_ARCHIVE_BYTES = 8_000_000

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def provision_elan():
    """Install exact GitHub-release asset, if missing. No model, host token, or sudo."""
    existing = shutil.which("elan")
    if existing:
        return existing, "preinstalled_version_checked", None
    if sys.platform != "linux" or platform.machine().lower() not in ("x86_64", "amd64"):
        raise RuntimeError("Pinned elan installer only supports x86_64 Linux")
    req = urllib.request.Request(ELAN_URL, headers={"User-Agent": "gcl-lean-compute/1"})
    with urllib.request.urlopen(req, timeout=40) as response:
        blob = response.read(MAX_ARCHIVE_BYTES + 1)
    if len(blob) > MAX_ARCHIVE_BYTES or hashlib.sha256(blob).hexdigest() != ELAN_ARCHIVE_SHA256:
        raise RuntimeError("Pinned elan release archive SHA256 mismatch or oversized")
    with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as archive:
        members = archive.getmembers()
        if len(members) != 1 or members[0].name != "elan-init" or not members[0].isfile():
            raise RuntimeError("Unexpected pinned elan archive contents")
        data = archive.extractfile(members[0]).read()
    with tempfile.TemporaryDirectory(prefix="gcl-lean-bootstrap-") as td:
        installer = Path(td) / "elan-init"
        installer.write_bytes(data)
        installer.chmod(0o700)
        installed = subprocess.run(
            [str(installer), "-y", "--no-modify-path", "--default-toolchain", TOOLCHAIN],
            capture_output=True, text=True, timeout=155, check=False)
        if installed.returncode != 0:
            raise RuntimeError("Pinned elan installer failed with exit " + str(installed.returncode))
    elan = Path.home() / ".elan" / "bin" / "elan"
    if not elan.is_file():
        raise RuntimeError("Pinned elan installer did not install executable")
    return str(elan), "installed_pinned_release", ELAN_ARCHIVE_SHA256

def execute(source, receipt, *, timeout=180):
    source, receipt = Path(source), Path(receipt)
    started = time.monotonic()
    data = {"schema":"GCL-ERDOS-41-LEAN-COMPUTE/1",
            "source_sha256":sha(source), "toolchain":TOOLCHAIN,
            "elan_release":ELAN_RELEASE, "status":"RED",
            "authority_effects":{"certification":False,"publication":False,"solve_dispatch":False}}
    try:
        elan, mode, archive_hash = provision_elan()
        data.update({"elan_provisioning":mode,"elan_archive_sha256":archive_hash})
        version = subprocess.run([elan,"run",TOOLCHAIN,"lean","--version"],
                                 capture_output=True,text=True,timeout=60)
        if version.returncode or not re.match(r"^Lean \(version 4\.29\.1(?:,|\))",version.stdout.strip()):
            raise RuntimeError("Unexpected Lean version or toolchain unavailable")
        data["lean_version"] = version.stdout.strip()
        result = subprocess.run([elan,"run",TOOLCHAIN,"lean",str(source)],
                                capture_output=True,text=True,timeout=timeout)
        data.update({"exit_code":result.returncode,
                     "stdout_sha256":hashlib.sha256(result.stdout.encode()).hexdigest(),
                     "stderr_sha256":hashlib.sha256(result.stderr.encode()).hexdigest(),
                     "stdout":result.stdout[:8000],"stderr":result.stderr[:8000]})
        data["status"] = "GREEN_LEAN_CHECKED_UNADJUDICATED" if result.returncode == 0 else "RED_LEAN"
    except Exception as error:
        data["error"] = type(error).__name__ + ": " + str(error)[:250]
    data["elapsed_seconds"] = round(time.monotonic() - started, 3)
    receipt.write_text(json.dumps(data,sort_keys=True,indent=2)+"\n")
    return 0 if data["status"] == "GREEN_LEAN_CHECKED_UNADJUDICATED" else 1

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source",default="/content/Erdos41Finite.lean")
    p.add_argument("--receipt",default="/content/erdos41_lean_receipt.json")
    p.add_argument("--timeout",type=int,default=180)
    a=p.parse_args()
    if not 30 <= a.timeout <= 600:
        p.error("timeout outside bounded envelope")
    sys.exit(execute(a.source,a.receipt,timeout=a.timeout))
