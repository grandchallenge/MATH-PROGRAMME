#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import struct
import subprocess
import tempfile
from array import array
from pathlib import Path

HERE = Path(__file__).resolve().parent
ODD = HERE.parent
T3006_VERIFY = ODD / "OZ_RT_BZ_T3_006" / "verify.py"
RESULT = json.loads((HERE / "SEARCH_RESULT.json").read_text(encoding="utf-8"))
P = 1000003

spec = importlib.util.spec_from_file_location("t3_006_verify_for_t3_007", T3006_VERIFY)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load protected T3-006 independent verifier")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

MONOMS = base.MONOMS
mon2 = base.mon2
mon3 = base.mon3


def grid(order: int, nmax: int):
    return [
        (n, k, l)
        for n in range(order + 1, nmax + 1)
        for k in range(n - order + 1)
        for l in range(n)
    ]


def compile_rank(tmp: Path) -> Path:
    exe = tmp / "rank_verify"
    subprocess.run(
        [os.environ.get("CC", "cc"), "-O3", str(HERE / "rank_mod.c"), "-o", str(exe)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return exe


def rank(rows: list[list[int]], exe: Path, tmp: Path, tag: str) -> int:
    nr, nc = len(rows), len(rows[0])
    fpath = tmp / f"{tag}.bin"
    with fpath.open("wb") as f:
        f.write(struct.pack("<II", nr, nc))
        for row in rows:
            a = array("I", (x % P for x in reversed(row)))
            if a.itemsize != 4:
                raise AssertionError("unexpected uint width")
            a.tofile(f)
    return int(subprocess.check_output([str(exe), str(fpath)], text=True).strip())


def module_row(order: int, n: int, k: int, l: int, qdeg: int) -> list[int]:
    row: list[int] = []
    for shift in range(order + 1):
        fs = base.F(n, k + shift, l)
        row.extend(fs * pow(n, i, P) * pow(k, j, P) % P for i, j in mon2(2))
    tc, tn = base.T(n, k, l), base.T(n, k, l + 1)
    dc, dn = base.qden(k, l) % P, base.qden(k, l + 1) % P
    if dc == 0 or dn == 0:
        raise AssertionError("denominator collision")
    idc, idn = pow(dc, -1, P), pow(dn, -1, P)
    for mon in reversed(MONOMS):
        vc, vn = base.mval(mon, n, k, l), base.mval(mon, n, k, l + 1)
        for i, j, h in reversed(mon3(qdeg)):
            pc = pow(n, i, P) * pow(k, j, P) * pow(l, h, P) % P
            pn = pow(n, i, P) * pow(k, j, P) * pow(l + 1, h, P) % P
            row.append((tc * vc * pc * idc - tn * vn * pn * idn) % P)
    return row


def main() -> int:
    if RESULT["prime"] != P or len(MONOMS) != 198:
        raise AssertionError("result/basis lock drift")
    if not base.MAP["all_monomials_weight_five"] or base.MAP["nested_atom_count_max"] != 1:
        raise AssertionError("predecessor raw-jet structure drift")
    if base.jet_map.swap(base.jet_map.target_polynomial()) != base.jet_map.target_polynomial():
        raise AssertionError("target symmetry drift")

    multipliers = [int(x["raw_derivative_multiplier"]) for x in base.MAP["monomials"]]
    mdigest = hashlib.sha256(json.dumps(multipliers, separators=(",", ":")).encode("utf-8")).hexdigest()
    norm = RESULT["coordinate_normalization"]
    if len(multipliers) != 198 or not all(x != 0 and x % P != 0 for x in multipliers):
        raise AssertionError("raw-derivative normalization drift")
    if mdigest != norm["multiplier_vector_sha256"]:
        raise AssertionError("raw-derivative normalization digest drift")

    for n in range(9):
        if sum(base.F(n, k, l) for k in range(n + 1) for l in range(n + 1)) % P != 0:
            raise AssertionError("finite T3 replay drift")

    with tempfile.TemporaryDirectory(prefix="t3_007_verify_") as td:
        tmp = Path(td)
        exe = compile_rank(tmp)
        for key in ("order3_full_weight5_module", "order4_full_weight5_module"):
            for rec in RESULT[key]["stages"]:
                g = grid(rec["order"], rec["n_max"])
                count = rec["unknowns"]
                rows = [
                    module_row(rec["order"], n, k, l, rec["q_coefficient_degree"])
                    for n, k, l in g[-count:]
                ]
                got = rank(rows, exe, tmp, f"o{rec['order']}_q{rec['q_coefficient_degree']}")
                if got != rec["rank"] or got != rec["unknowns"]:
                    raise AssertionError("independent module rank mismatch")

    if RESULT["terminal"] != "ORDER3_4_COMPLETE_WEIGHT5_MODULE_BOUNDED_CLASS_EXHAUSTED":
        raise AssertionError("terminal search classification drift")
    if RESULT["proof_effect"] != "NONE" or RESULT["promotion_effect"] != "NONE":
        raise AssertionError("claim inflation")
    if RESULT["t3_status"] != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("T3 status inflation")
    print("T3-007 independent order-3/4 replay: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
