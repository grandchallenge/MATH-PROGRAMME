#!/usr/bin/env python3
"""Exact Lean 4.33.0 source/type/axiom replay; no full graph theorem claim."""
from __future__ import annotations
import argparse, hashlib, json, os, re, subprocess, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "experiments/erdos_proof_verification/0561/Erdos561Core.lean"
EV = ROOT / "governance/erdos_proof_verification/evidence/0561"
LOG = EV / "C_LEAN_CORE_STDOUT_001.txt"
RECEIPT = EV / "C_LEAN_CORE_REPLAY_001.json"
THEOREMS = (
    "degree_minus_lower_eq_min", "tight_degree_iff", "split_budget_iff",
    "factor_bounds", "min_degree_ratio", "weighted_to_unweighted",
    "all_small_components_impossible", "strict_factor_slope",
    "large_component_impossible", "odd_odd_product_odd",
    "component_parity_flips",
)
ALLOWED = {"propext", "Quot.sound", "Classical.choice"}
NEGATIVES = {
    "invalid_min_rewrite":
        "import Init\nexample : (3:Nat)-(3-5)=max 3 5 := by decide\n",
    "missing_positive_alpha_saturation":
        "import Init\nexample : ((0:Nat)-2=0 → (0:Nat)=0+2) := by decide\n",
    "omitted_edge_to_T_parity":
        "import Init\nexample : ((1:Nat)*1+1)%2=1 := by decide\n",
    "false_strict_slope_at_equal_budgets":
        "import Init\nexample : (4:Nat)<2*2 := by decide\n",
    "wrong_large_boundary_direction":
        "import Init\nexample : (2:Nat)*(6*(8+1-2)+2) ≤ 8*(1-1) := by decide\n",
}

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def source_contract() -> str:
    s = SRC.read_text()
    if re.findall(r"^import\s+([\w.]+)\s*$", s, re.M) != ["Init"]:
        raise ValueError("import closure drift")
    if re.search(r"\b(sorry|admit|axiom|unsafe|native_decide)\b", s):
        raise ValueError("untrusted proof directive")
    for n in THEOREMS:
        if any(marker not in s for marker in (
            "theorem "+n, "#check ErdosPV0561."+n, "#print axioms "+n
        )):
            raise ValueError("missing declaration, type or axiom: "+n)
    return sha(s.encode())

def parse(out: str) -> tuple[dict,dict]:
    if "error:" in out or "sorryAx" in out:
        raise ValueError("compiler error or unresolved sorry")
    typespart = out.split("'ErdosPV0561.")[0]
    found = list(re.finditer(r"^ErdosPV0561\.(\w+)\b", typespart, flags=re.M))
    if len(found)!=len(THEOREMS) or {m[1] for m in found}!=set(THEOREMS):
        raise ValueError("wrong theorem type census")
    types = {}
    for i,m in enumerate(found):
        end = found[i+1].start() if i+1<len(found) else len(typespart)
        t = typespart[m.start():end].strip()
        if not t.startswith("ErdosPV0561."+m[1]+" "):
            raise ValueError("malformed type")
        types[m[1]]=sha(t.encode())
    pat = re.compile(r"^'ErdosPV0561\.(\w+)' (does not depend on any axioms|depends on axioms: \[([^\]]*)\])$",re.M)
    ax = {}
    for m in pat.finditer(out):
        if m[1] in ax: raise ValueError("duplicate axiom report")
        values = [] if m[2].startswith("does not") else [
            x.strip() for x in m[3].split(",") if x.strip()]
        if set(values)-ALLOWED: raise ValueError("unapproved axiom")
        ax[m[1]] = values
    if set(ax)!=set(THEOREMS): raise ValueError("incomplete axioms")
    return ax, types

def compile(binary: Path, file: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(binary),str(file)],cwd=ROOT,
        env={**os.environ,"LEAN_COLOR":"never"},
        capture_output=True,text=True,timeout=20,check=False)

def verify() -> dict:
    r=json.loads(RECEIPT.read_text())
    if (r.get("record_type")!="ERDOS_PV_0561_C_LEAN_CORE_REPLAY/1"
        or r.get("assignment_id")!="ERDOS-PV-0561-C"
        or r.get("predecessor_protected_main")!="3fd1d27e4d0d3942d2d7fe7f0ec72409f653ad99"
        or r.get("predecessor_phase_B_admission")!="070f9a9d71b22132d48d7c1dc0c05671c11c0a90"
        or r.get("claim_sha")!="a5496eb0bdc1199ce0330de45abc26f05d90e0cd"
        or r.get("source_sha256")!=source_contract()
        or not r.get("lean_version","").startswith("Lean (version 4.33.0")
        or r.get("positive_exit_code")!=0
        or r.get("import_closure")!=["Init"]
        or r.get("scope")!="ELEVEN_KERNEL_CHECKED_ARITHMETIC_AUXILIARIES_ONLY"
        or r.get("formalization_work_required") is not True
        or any(r.get(k) is not False for k in (
          "full_factor_theorem_kernel_checked",
          "star_center_structural_hypotheses_kernel_checked",
          "full_you_theorem_1_2_kernel_checked",
          "original_erdos_561_conjecture_solved","mathcert_certified"))):
        raise ValueError("source/claim/toolchain/scope mismatch")
    out=LOG.read_text()
    if r.get("positive_stdout_sha256")!=sha(out.encode()):
        raise ValueError("Lean stdout changed")
    axioms,types=parse(out)
    if r.get("axioms")!=axioms or r.get("types_sha256")!=types:
        raise ValueError("type/axiom replay drift")
    if set(r.get("hostile",{}))!=set(NEGATIVES):
        raise ValueError("missing negatives")
    for name,src in NEGATIVES.items():
        x=r["hostile"][name]
        if (x.get("source_sha256")!=sha(src.encode())
            or not isinstance(x.get("exit_code"),int) or x["exit_code"]==0
            or not re.fullmatch("[0-9a-f]{64}",x.get("log_sha256",""))
            or "error:" not in x.get("diagnostic","")):
            raise ValueError("false target not rejected: "+name)
    return r

def execute(binary: Path) -> dict:
    source_sha=source_contract()
    binary=binary.expanduser().resolve(strict=True)
    version=subprocess.check_output(
        [str(binary),"--version"],text=True,timeout=8).strip()
    if not version.startswith("Lean (version 4.33.0"):
        raise ValueError("wrong pinned Lean")
    init=binary.parent.parent/"lib/lean/Init.olean"
    if not init.is_file(): raise ValueError("missing Init.olean")
    result=compile(binary,SRC)
    if result.returncode or result.stderr:
        raise ValueError("positive compilation: "+(result.stdout+result.stderr)[:500])
    axioms,types=parse(result.stdout)
    negatives={}
    with tempfile.TemporaryDirectory(prefix="erdos561-c-") as td:
        for name,src in NEGATIVES.items():
            target=Path(td)/(name+".lean")
            target.write_text(src)
            x=compile(binary,target)
            log=x.stdout+x.stderr
            if x.returncode==0 or "error:" not in log:
                raise ValueError("false target accepted: "+name)
            negatives[name]={
                "source_sha256":sha(src.encode()),
                "exit_code":x.returncode,
                "log_sha256":sha(log.encode()),
                "diagnostic":log[:360]}
    EV.mkdir(parents=True,exist_ok=True)
    LOG.write_text(result.stdout)
    r={
        "record_type":"ERDOS_PV_0561_C_LEAN_CORE_REPLAY/1",
        "assignment_id":"ERDOS-PV-0561-C","problem_id":561,"phase":"C",
        "predecessor_protected_main":"3fd1d27e4d0d3942d2d7fe7f0ec72409f653ad99",
        "predecessor_phase_B_admission":"070f9a9d71b22132d48d7c1dc0c05671c11c0a90",
        "claim_sha":"a5496eb0bdc1199ce0330de45abc26f05d90e0cd",
        "source_path":SRC.relative_to(ROOT).as_posix(),
        "source_sha256":source_sha,"lean_version":version,
        "lean_binary_sha256":sha(binary.read_bytes()),
        "init_olean_sha256":sha(init.read_bytes()),
        "import_closure":["Init"],
        "scope":"ELEVEN_KERNEL_CHECKED_ARITHMETIC_AUXILIARIES_ONLY",
        "positive_exit_code":result.returncode,
        "positive_stdout_sha256":sha(result.stdout.encode()),
        "types_sha256":types,"axioms":axioms,"hostile":negatives,
        "full_factor_theorem_kernel_checked":False,
        "star_center_structural_hypotheses_kernel_checked":False,
        "full_you_theorem_1_2_kernel_checked":False,
        "original_erdos_561_conjecture_solved":False,
        "formalization_work_required":True,"mathcert_certified":False,
        "execution_origin":"CHAD_LOCAL_OS_ONLY_NOT_INDEPENDENTLY_ATTESTED",
    }
    RECEIPT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    return verify()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--execute",action="store_true")
    p.add_argument("--lean-bin",
       default="/home/jim/.elan/toolchains/leanprover--lean4---v4.33.0/bin/lean")
    a=p.parse_args()
    r=execute(Path(a.lean_bin)) if a.execute else verify()
    print(json.dumps({
      "result":"PASS",
      "assignment_id":r["assignment_id"],
      "auxiliary_theorems":len(r["axioms"]),
      "hostile_rejections":len(r["hostile"]),
      "source_sha256":r["source_sha256"],
      "full_theorem":r["full_you_theorem_1_2_kernel_checked"],
    },sort_keys=True))

if __name__=="__main__":
    main()
