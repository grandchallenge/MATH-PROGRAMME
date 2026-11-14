#!/usr/bin/env python3
"""Source-locked Erdős #1 Lean replay contract. A replay is not certification."""
import argparse, hashlib, json, re, subprocess
from pathlib import Path

PIN = {
    "commit": "db6f9091dfaf9bac704e6b28fb3a094594869328",
    "proof": "Erdos1/Resolutions/Erdos1_219usd_38h.lean",
    "proof_git_blob": "07d2f36647a2319e65c0c8c756527460925e9075",
    "proof_sha256": "b99ae0ce768fd02ee21c05f1392e9f6ab01988fbca9d2d359a4c51fd5e345107",
    "manifest_git_blob": "8313c2070fbc6c323b32b67aca5f0751dbc24da6",
    "toolchain": "leanprover/lean4:v4.28.0",
    "mathlib_commit": "8f9d9cff6bd728b17a24e163c9402775d9e6a365",
}
THEOREMS = ("ErdosCounter.exists_binary_block_set", "Erdos1.erdos_1.disproof")
ALLOWED_AXIOMS = {"propext", "Quot.sound", "Classical.choice"}
READBACK = """import Erdos1.Resolutions.Erdos1_219usd_38h

example (d k W : ℕ) (hd : 0 < d) (hk : 0 < k)
    (a : Fin d → ℕ) (ha : ∀ i, 0 < a i)
    (hW : ∀ i, a i ≤ W) (hf : ErdosCounter.RelationFree a (2 ^ k)) :
    ∃ A : Finset ℕ, A.card = d * k ∧
      A ⊆ Finset.Icc 1 (2 ^ (k - 1) * W) ∧
      ErdosCounter.SumDistinct A :=
  ErdosCounter.exists_binary_block_set d k W hd hk a ha hW hf

example : ¬ (∃ C > (0 : ℝ), ∀ (N : ℕ) (A : Finset ℕ)
    (_ : Erdos1.IsSumDistinctSet A N), N ≠ 0 → C * 2 ^ A.card < N) :=
  Erdos1.erdos_1.disproof

#print axioms ErdosCounter.exists_binary_block_set
#print axioms Erdos1.erdos_1.disproof
"""
NEGATIVE = """import Erdos1.Resolutions.Erdos1_219usd_38h

-- Omit the bounded integer-relation-freedom hypothesis deliberately.
example (d k W : ℕ) (hd : 0 < d) (hk : 0 < k)
    (a : Fin d → ℕ) (ha : ∀ i, 0 < a i)
    (hW : ∀ i, a i ≤ W) :
    ∃ A : Finset ℕ, A.card = d * k ∧
      A ⊆ Finset.Icc 1 (2 ^ (k - 1) * W) ∧
      ErdosCounter.SumDistinct A := by
  exact ErdosCounter.exists_binary_block_set d k W hd hk a ha hW
"""

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()

def verify_source(root):
    root = Path(root).resolve()
    proof, manifest = root / PIN["proof"], root / "lake-manifest.json"
    if git(root, "rev-parse", "HEAD") != PIN["commit"]:
        raise ValueError("author commit differs from source lock")
    if sha(proof) != PIN["proof_sha256"] or git(root, "hash-object", str(proof)) != PIN["proof_git_blob"]:
        raise ValueError("author proof byte identity mismatch")
    if git(root, "hash-object", str(manifest)) != PIN["manifest_git_blob"]:
        raise ValueError("Lake manifest drift")
    if (root / "lean-toolchain").read_text().strip() != PIN["toolchain"]:
        raise ValueError("Lean toolchain drift")
    mathlib = [x for x in json.loads(manifest.read_text())["packages"] if x["name"] == "mathlib"]
    if len(mathlib) != 1 or mathlib[0]["rev"] != PIN["mathlib_commit"]:
        raise ValueError("Mathlib commit drift")
    text = proof.read_text()
    if re.search(r"\b(?:sorry|admit|axiom|unsafe)\b", text):
        raise ValueError("unsafe source proof token")
    for name in ("theorem exists_binary_block_set", "theorem no_uniform_subset_bound",
                 "theorem Erdos1.erdos_1.disproof", "def RelationFree"):
        if name not in text:
            raise ValueError("required source declaration missing: " + name)
    return {"result": "PINNED_SOURCE_MATCH", **PIN}

def prepare(root):
    p = Path(root)
    result = verify_source(p)
    (p / "GCLReadback.lean").write_text(READBACK)
    (p / "GCLNegative.lean").write_text(NEGATIVE)
    return {**result, "readback_sha256": sha(p / "GCLReadback.lean"),
            "negative_sha256": sha(p / "GCLNegative.lean")}

def parse_axioms(log):
    if "sorryAx" in log or re.search(r"\bsorry\b", log):
        raise ValueError("untrusted sorry axiom marker")
    out = {}
    for theorem in THEOREMS:
        found = re.search(r"(?m)^" + re.escape(theorem) +
                          r" depends on axioms:\s*\[([^\]]*)\]", log)
        if found:
            values = [v.strip() for v in found.group(1).split(",") if v.strip()]
        elif re.search(r"(?m)^" + re.escape(theorem) + r" does not depend on any axioms", log):
            values = []
        else:
            raise ValueError("missing kernel axiom report: " + theorem)
        if not set(values) <= ALLOWED_AXIOMS:
            raise ValueError("unexpected axioms: " + repr(values))
        out[theorem] = values
    return out

def adjudicate(root, build_log, readback_log, negative_log, build_exit, readback_exit, negative_exit):
    source = verify_source(root)
    logs = {"build": Path(build_log), "readback": Path(readback_log), "negative": Path(negative_log)}
    receipt = {
        "record_type": "ERDOS_PV_0001_LEAN_REPLAY/1", "task_id": "ERDOS-PV-0001-C",
        "source": source, "build_exit": build_exit, "readback_exit": readback_exit,
        "negative_exit": negative_exit, "log_sha256": {n: sha(p) for n, p in logs.items()},
        "authority": "UNADJUDICATED_COMPUTATIONAL_EVIDENCE_ONLY",
        "independent_referee": False, "mathcert": False,
    }
    try:
        if build_exit != 0 or readback_exit != 0 or negative_exit == 0:
            raise ValueError("kernel build/readback/negative exit mismatch")
        if "error:" not in logs["negative"].read_text():
            raise ValueError("negative test did not produce an error")
        receipt["axioms"] = parse_axioms(logs["readback"].read_text())
        receipt["result"] = "LEAN_KERNEL_REPLAY_PASS_UNADJUDICATED"
    except ValueError as exc:
        receipt["result"], receipt["reason"] = "REPLAY_FAILED_OR_UNVERIFIED", str(exc)
    return receipt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=("prepare", "verify", "adjudicate"))
    ap.add_argument("--source-dir", type=Path, required=True)
    for name in ("build-log", "type-log", "bad-log", "receipt"):
        ap.add_argument("--" + name, type=Path)
    for name in ("build-exit", "type-exit", "bad-exit"):
        ap.add_argument("--" + name, type=int)
    args = ap.parse_args()
    if args.action == "prepare":
        out = prepare(args.source_dir)
    elif args.action == "verify":
        out = verify_source(args.source_dir)
    else:
        vals = (args.build_log, args.type_log, args.bad_log, args.receipt,
                args.build_exit, args.type_exit, args.bad_exit)
        if any(v is None for v in vals):
            ap.error("adjudicate requires all log, status and receipt arguments")
        out = adjudicate(args.source_dir, args.build_log, args.type_log, args.bad_log,
                         args.build_exit, args.type_exit, args.bad_exit)
        args.receipt.write_text(json.dumps(out, sort_keys=True, indent=2) + "\n")
    print(json.dumps(out, sort_keys=True))
    if out["result"] == "REPLAY_FAILED_OR_UNVERIFIED":
        raise SystemExit(2)

if __name__ == "__main__":
    main()
