#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
import struct
import subprocess
import sys
import tempfile
from array import array
from functools import lru_cache
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
ODD = HERE.parent
T3005 = ODD / "OZ_RT_BZ_T3_005"
RESULT = json.loads((HERE / "SEARCH_RESULT.json").read_text(encoding="utf-8"))
P = 1000003

sys.path.insert(0, str(T3005))
import jet_map  # type: ignore


def mon2(d: int):
    return [(i, j) for i in range(d + 1) for j in range(d + 1 - i)]


def mon3(d: int):
    return [
        (i, j, h)
        for i in range(d + 1)
        for j in range(d + 1 - i)
        for h in range(d + 1 - i - j)
    ]


@lru_cache(None)
def H(m: int, r: int) -> int:
    if m <= 0:
        return 0
    return (H(m - 1, r) + pow(m, -r, P)) % P


def ES(x: int, r: int, m: int) -> int:
    return sum((H(t, m) * pow(t, -r, P) for t in range(1, x + 1))) % P


def U(a: int, b: int, r: int, m: int) -> int:
    return sum((H(t + b, m) * pow(t, -r, P) for t in range(1, a + 1))) % P


def T(n: int, k: int, l: int) -> int:
    return (
        comb(n + k, n) * pow(comb(n, k), 2, P)
        * comb(n + l, n) * pow(comb(n, l), 2, P)
        * comb(n + k + l, n)
    ) % P


def A(n: int, x: int, r: int) -> int:
    return (H(n + x, r) - H(x, r)) % P


def B(n: int, x: int, r: int) -> int:
    return (H(n - x, r) - H(x, r)) % P


def C(n: int, k: int, l: int, r: int) -> int:
    return (H(n + k + l, r) - H(k + l, r)) % P


def L(n: int, k: int, l: int, x: int) -> int:
    return (-A(n, x, 1) - C(n, k, l, 1) - 2 * B(n, x, 1)) % P


def r11(k: int, l: int) -> int:
    return (
        (H(k + l, 1) - H(k, 1) - H(l, 1)) * (H(k, 2) + H(l, 2))
        - H(k, 3) - H(l, 3) + U(k, l, 1, 2) + U(l, k, 1, 2)
    ) % P


def r12(k: int, l: int) -> int:
    i2 = pow(2, -1, P)
    return (
        -2 * (H(k, 1) + H(l, 1) - H(k + l, 1)) * H(l, 3)
        + H(k, 2) * H(k + l, 2) - H(l, 2) * H(l, 2) * i2
        + H(k + l, 2) * H(l, 2) - 5 * i2 * H(l, 4)
        + 2 * ES(l, 1, 3) - U(k, l, 2, 2)
    ) % P


def r22(k: int, l: int) -> int:
    return (
        -2 * (H(k, 2) + H(l, 2)) * (H(k, 3) + H(l, 3))
        + 2 * H(k + l, 3) * (H(k, 2) + H(l, 2))
        + 2 * H(k + l, 2) * (H(k, 3) + H(l, 3))
        - 2 * H(k, 5) - 2 * H(l, 5)
        - 6 * ES(k, 1, 4) - 6 * ES(l, 1, 4)
        - 2 * ES(k, 2, 3) - 2 * ES(l, 2, 3)
        + 6 * U(k, l, 1, 4) + 6 * U(l, k, 1, 4)
        + 2 * U(k, l, 2, 3) + 2 * U(l, k, 2, 3)
    ) % P


def W1(n: int, k: int, l: int) -> int:
    lk, ll = L(n, k, l, k), L(n, k, l, l)
    return (r22(k, l) + lk * r12(k, l) + ll * r12(l, k) + (lk * ll - C(n, k, l, 2)) * r11(k, l)) % P


def w5(n: int, k: int, l: int) -> int:
    i2, i4 = pow(2, -1, P), pow(4, -1, P)
    alpha = (A(n, k, 1) - A(n, l, 1)) % P
    beta = (B(n, k, 1) - B(n, l, 1)) % P
    psi = (alpha * i2 + beta) % P
    cc = ((A(n, k, 2) + A(n, l, 2)) * i4 - alpha * psi * i2) % P
    return (H(n + k, 5) + (alpha - beta) * H(n + k, 4) * i2 + cc * H(n + k, 3)) % P


def F(n: int, k: int, l: int) -> int:
    return T(n, k, l) * (W1(n, k, l) + w5(n, k, l) + w5(n, l, k)) % P


def atom(name: str, n: int, k: int, l: int) -> int:
    p = name.split("_")
    if name.startswith("H_k_"): return H(k, int(p[-1]))
    if name.startswith("H_l_"): return H(l, int(p[-1]))
    if name.startswith("H_kl_"): return H(k + l, int(p[-1]))
    if name.startswith("H_nk_"): return H(n + k, int(p[-1]))
    if name.startswith("H_nl_"): return H(n + l, int(p[-1]))
    if name.startswith("A_k_"): return A(n, k, int(p[-1]))
    if name.startswith("A_l_"): return A(n, l, int(p[-1]))
    if name.startswith("B_k_"): return B(n, k, int(p[-1]))
    if name.startswith("B_l_"): return B(n, l, int(p[-1]))
    if name.startswith("C_"): return C(n, k, l, int(p[-1]))
    if name.startswith("U_k_l_"):
        r, m = map(int, p[-2:]); return U(k, l, r, m)
    if name.startswith("U_l_k_"):
        r, m = map(int, p[-2:]); return U(l, k, r, m)
    if name.startswith("ES_k_"):
        r, m = map(int, p[-2:]); return ES(k, r, m)
    if name.startswith("ES_l_"):
        r, m = map(int, p[-2:]); return ES(l, r, m)
    raise ValueError(name)


MAP = jet_map.coefficient_map()
MONOMS = [tuple(item["atoms"]) for item in MAP["monomials"]]


def mval(mon: tuple[str, ...], n: int, k: int, l: int) -> int:
    z = 1
    for name in mon:
        z = z * atom(name, n, k, l) % P
    return z


def qden(k: int, l: int) -> int:
    return (l + 1) ** 3 * (k + l + 1)


def grid(nmax: int):
    return [(n, k, l) for n in range(3, nmax + 1) for k in range(n - 1) for l in range(n)]


def compile_rank(tmp: Path) -> Path:
    exe = tmp / "rank_verify"
    subprocess.run(
        [os.environ.get("CC", "cc"), "-O3", str(HERE / "rank_mod.c"), "-o", str(exe)],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    return exe


def rank(rows: list[list[int]], exe: Path, tmp: Path, tag: str) -> int:
    nr, nc = len(rows), len(rows[0])
    fpath = tmp / f"{tag}.bin"
    with fpath.open("wb") as f:
        f.write(struct.pack("<II", nr, nc))
        for row in rows:
            # Verifier deliberately reverses every column before elimination.
            a = array("I", (x % P for x in reversed(row)))
            if a.itemsize != 4: raise AssertionError("unexpected uint width")
            a.tofile(f)
    return int(subprocess.check_output([str(exe), str(fpath)], text=True).strip())


def scalar_row(n: int, k: int, l: int, adeg: int, qdeg: int) -> list[int]:
    row = []
    for s in range(3):
        fs = F(n, k + s, l)
        row.extend(fs * pow(n, i, P) * pow(k, j, P) % P for i, j in mon2(adeg))
    fc, fn = F(n, k, l), F(n, k, l + 1)
    dc, dn = qden(k, l) % P, qden(k, l + 1) % P
    if dc == 0 or dn == 0: raise AssertionError("denominator collision")
    for i, j, h in mon3(qdeg):
        pc = pow(n, i, P) * pow(k, j, P) * pow(l, h, P) % P
        pn = pow(n, i, P) * pow(k, j, P) * pow(l + 1, h, P) % P
        row.append((fc * pc * pow(dc, -1, P) - fn * pn * pow(dn, -1, P)) % P)
    return row


def module_row(n: int, k: int, l: int, qdeg: int) -> list[int]:
    row = []
    for s in range(3):
        fs = F(n, k + s, l)
        row.extend(fs * pow(n, i, P) * pow(k, j, P) % P for i, j in mon2(2))
    tc, tn = T(n, k, l), T(n, k, l + 1)
    dc, dn = qden(k, l) % P, qden(k, l + 1) % P
    if dc == 0 or dn == 0: raise AssertionError("denominator collision")
    idc, idn = pow(dc, -1, P), pow(dn, -1, P)
    # Independent monomial and coefficient order.
    for mon in reversed(MONOMS):
        vc, vn = mval(mon, n, k, l), mval(mon, n, k, l + 1)
        for i, j, h in reversed(mon3(qdeg)):
            pc = pow(n, i, P) * pow(k, j, P) * pow(l, h, P) % P
            pn = pow(n, i, P) * pow(k, j, P) * pow(l + 1, h, P) % P
            row.append((tc * vc * pc * idc - tn * vn * pn * idn) % P)
    return row


def main() -> int:
    if RESULT["prime"] != P or len(MONOMS) != 198:
        raise AssertionError("result/basis lock drift")
    if not MAP["all_monomials_weight_five"] or MAP["nested_atom_count_max"] != 1:
        raise AssertionError("predecessor raw-jet structure drift")
    if jet_map.swap(jet_map.target_polynomial()) != jet_map.target_polynomial():
        raise AssertionError("target symmetry drift")
    # Exact finite identity remains evidence only; it is not used to infer the theorem.
    for n in range(9):
        if sum(F(n, k, l) for k in range(n + 1) for l in range(n + 1)) % P != 0:
            raise AssertionError("finite T3 replay drift")

    with tempfile.TemporaryDirectory(prefix="t3_006_verify_") as td:
        tmp = Path(td); exe = compile_rank(tmp)
        for rec in RESULT["stage_a_scalar_envelope"]["stages"]:
            rows = [scalar_row(n, k, l, rec["a_degree"], rec["q_degree"]) for n, k, l in grid(rec["n_max"])]
            got = rank(rows, exe, tmp, f"scalar_{rec['a_degree']}")
            if got != rec["rank"] or got != rec["unknowns"]:
                raise AssertionError("independent scalar rank mismatch")
        for rec in RESULT["stage_b_full_weight5_module"]["stages"]:
            g = grid(rec["n_max"]); count = rec["unknowns"]
            rows = [module_row(n, k, l, rec["q_coefficient_degree"]) for n, k, l in g[-count:]]
            got = rank(rows, exe, tmp, f"module_{rec['q_coefficient_degree']}")
            if got != rec["rank"] or got != rec["unknowns"]:
                raise AssertionError("independent module rank mismatch")
    if RESULT["proof_effect"] != "NONE" or RESULT["promotion_effect"] != "NONE":
        raise AssertionError("claim inflation")
    if RESULT["t3_status"] != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("T3 status inflation")
    print("T3-006 independent replay: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
