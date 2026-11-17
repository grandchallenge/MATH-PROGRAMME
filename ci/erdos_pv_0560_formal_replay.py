#!/usr/bin/env python3
"""Bounded exact Lean 4.33.0 core replay: auxiliary Phase C proof only."""
from __future__ import annotations
import argparse, hashlib, json, os, re, subprocess, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "experiments/erdos_proof_verification/0560/Erdos560Core.lean"
EV = ROOT / "governance/erdos_proof_verification/evidence/0560"
RECEIPT = EV / "C_LEAN_CORE_REPLAY_001.json"
LOG = EV / "C_LEAN_CORE_STDOUT_001.txt"
THEOREMS = (
    "completeBetween_disjoint", "right_subset_neighbors",
    "completeBetween_symm", "completeBetween_mono", "n_le_two_pow",
    "integral_factor_cleared", "strict_gate_base", "strict_gate_step",
    "strict_gate_all", "integral_denominators_positive",
    "gap_ge_two", "t_ge_four",
)
NEGATIVES = {
    "incorrect_t_ge_2": "import Init\nexample : 2 * 18 ^ 2 < 25 ^ 2 := by decide\n",
    "incorrect_gap_a_eq_1":
        "import Init\nexample : (2-1) * 2 ^ 1 ≤ (1-1) * 2 ^ (2+1) * (2-1) ^ 1 := by decide\n",
    "overlap_without_loopless":
        "import Init\ndef S : Unit → Prop := fun _ => True\n"
        "example : ∀ (v : Unit), ¬ (S v ∧ S v) := by decide\n",
}
def hash256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def source_contract() -> str:
    source = SRC.read_text(encoding="utf-8")
    if re.findall(r"^import\s+([\w.]+)\s*$", source, re.M) != ["Init"]:
        raise ValueError("import closure drift")
    if re.search(r"\b(sorry|admit|axiom|unsafe)\b", source):
        raise ValueError("untrusted proof directive")
    for name in THEOREMS:
        if f"theorem {name}" not in source or f"#print axioms {name}" not in source:
            raise ValueError("missing governed declaration: " + name)
    return hash256(source.encode())

def parse_axioms(output: str) -> dict:
    if "error:" in output or "sorryAx" in output:
        raise ValueError("positive Lean log contains rejected proof")
    found = {}
    rx = r"'ErdosPV0560\.(\w+)' (does not depend on any axioms|depends on axioms: \[([^\]]*)\])"
    for hit in re.finditer(rx, output):
        name = hit.group(1)
        if name in found: raise ValueError("duplicate axiom output")
        ax = [] if hit.group(2).startswith("does not") else [
            t.strip() for t in hit.group(3).split(",") if t.strip()
        ]
        if set(ax) - {"propext", "Quot.sound"}:
            raise ValueError("unpermitted axiom: " + name)
        found[name] = ax
    if set(found) != set(THEOREMS):
        raise ValueError("axiom report incomplete")
    for text in ("ErdosPV0560.integral_factor_cleared (s a : Nat)",
                 "ErdosPV0560.strict_gate_all (t : Nat)",
                 "ErdosPV0560.completeBetween_disjoint {V : Type}",
                 "def ErdosPV0560.CompleteBetween"):
        if text not in output: raise ValueError("theorem type not read back: " + text)
    return {name: found[name] for name in THEOREMS}

def verify() -> dict:
    r = json.loads(RECEIPT.read_text(encoding="utf-8"))
    if (r.get("record_type") != "ERDOS_PV_0560_C_LEAN_CORE_REPLAY/1"
        or r.get("source_sha256") != source_contract()
        or r.get("assignment_id") != "ERDOS-PV-0560-C"
        or r.get("claim_sha") != "8b6a32fa6fc8fd037051835fa54542f81ecca50e"
        or r.get("predecessor_main") != "123701f543f32c7bf92197f77f39405a3702f8f4"
        or not r.get("lean_version","").startswith("Lean (version 4.33.0")
        or r.get("positive_exit_code") != 0
        or r.get("whole_size_ramsey_proved") is not False
        or r.get("formalization_work_required") is not True):
        raise ValueError("source/claim/toolchain/partial-scope drift")
    output = LOG.read_text(encoding="utf-8")
    if r["positive_stdout_sha256"] != hash256(output.encode()):
        raise ValueError("compiler stdout not pinned")
    if parse_axioms(output) != r["axioms"]:
        raise ValueError("actual kernel axiom report differs from record")
    if set(r["hostile"]) != set(NEGATIVES):
        raise ValueError("hostile census incomplete")
    for name, code in NEGATIVES.items():
        row = r["hostile"][name]
        if (row.get("source_sha256") != hash256(code.encode())
            or row.get("exit_code") == 0
            or not re.fullmatch("[a-f0-9]{64}",row.get("log_sha256",""))):
            raise ValueError("unreplayed false target: " + name)
    return r


def compile_lean(binary: Path, target: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(binary), str(target)],
        cwd=ROOT, env={**os.environ, "LEAN_COLOR": "never"},
        capture_output=True, text=True, timeout=14, check=False,
    )

def execute(binary: Path) -> dict:
    source_hash = source_contract()
    binary = binary.expanduser().resolve(strict=True)
    version = subprocess.check_output([str(binary), "--version"], text=True, timeout=7).strip()
    if not version.startswith("Lean (version 4.33.0"):
        raise ValueError("unlocked toolchain")
    init_olean = binary.parent.parent / "lib/lean/Init.olean"
    if not init_olean.is_file():
        raise ValueError("Init dependency closure missing")
    positive = compile_lean(binary, SRC)
    if positive.returncode != 0 or positive.stderr:
        raise ValueError("positive kernel replay failed: " + str(positive.returncode)
                         + positive.stderr[:600])
    axioms = parse_axioms(positive.stdout)
    negatives = {}
    with tempfile.TemporaryDirectory(prefix="gcl-pv-0560-c-") as tmp:
        for name, source in NEGATIVES.items():
            target = Path(tmp) / (name + ".lean")
            target.write_text(source, encoding="utf-8")
            outcome = compile_lean(binary, target)
            log = outcome.stdout + outcome.stderr
            if outcome.returncode == 0 or "error:" not in log:
                raise ValueError("hostile target accepted: " + name)
            negatives[name] = {
                "source_sha256": hash256(source.encode()),
                "exit_code": outcome.returncode,
                "log_sha256": hash256(log.encode()),
                "diagnostic": log[:320],
            }
    EV.mkdir(parents=True, exist_ok=True)
    LOG.write_text(positive.stdout, encoding="utf-8")
    record = {
        "record_type": "ERDOS_PV_0560_C_LEAN_CORE_REPLAY/1",
        "assignment_id": "ERDOS-PV-0560-C",
        "predecessor_main": "123701f543f32c7bf92197f77f39405a3702f8f4",
        "claim_sha": "8b6a32fa6fc8fd037051835fa54542f81ecca50e",
        "source_path": SRC.relative_to(ROOT).as_posix(),
        "source_sha256": source_hash,
        "lean_version": version,
        "lean_binary_sha256": hash256(binary.read_bytes()),
        "init_olean_sha256": hash256(init_olean.read_bytes()),
        "imports": ["Init"],
        "scope": "TWELVE_KERNEL_CHECKED_AUXILIARY_DECLARATIONS_ONLY",
        "positive_exit_code": positive.returncode,
        "positive_stdout_sha256": hash256(positive.stdout.encode()),
        "axioms": axioms,
        "hostile": negatives,
        "whole_size_ramsey_proved": False,
        "formalization_work_required": True,
        "mathlib_semantic_equivalence_kernel_checked": False,
        "mathcert_certified": False,
        "execution_origin": "CHAD_LOCAL_OS_ONLY_NOT_INDEPENDENTLY_ATTESTED"
    }
    RECEIPT.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return verify()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--execute", action="store_true")
    p.add_argument("--lean-bin", default="/home/jim/.elan/toolchains/leanprover--lean4---v4.33.0/bin/lean")
    a = p.parse_args()
    r = execute(Path(a.lean_bin)) if a.execute else verify()
    print(json.dumps({"result":"PASS", "task":r["assignment_id"],
                      "auxiliary_theorems":len(THEOREMS),
                      "hostile_rejections":len(r["hostile"]),
                      "source_sha256":r["source_sha256"],
                      "full_theorem":r["whole_size_ramsey_proved"]},sort_keys=True))

if __name__=="__main__":
    main()
