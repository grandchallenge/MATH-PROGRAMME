#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import struct
import subprocess
import sys
import tempfile
from array import array
from fractions import Fraction as Q
from functools import lru_cache
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
ODD = HERE.parent
T3005 = ODD / "OZ_RT_BZ_T3_005"
T3002 = ODD / "OZ_RT_BZ_T3_002" / "target.py"
RESULT = HERE / "SEARCH_RESULT.json"
WITNESS = HERE / "Q2_RANK_WITNESS.json"
P = 1000003
BASIS_SHA = "cbdfe5798d360cb98f2d64743907a06ddc0612f88d17ef4bcef65c81c74e1438"
Q2_INDEX_SHA = "d0bb330deff059c2afdc4e1a994d7c544c42ce7ec497e1c6490ca9f2781dc57f"

sys.path.insert(0, str(T3005))
import jet_map  # type: ignore

spec = importlib.util.spec_from_file_location("t3_002_target_for_t3_008_verifier", T3002)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load protected T3-002 target")
target = importlib.util.module_from_spec(spec)
spec.loader.exec_module(target)

POLY = jet_map.target_polynomial()
MONOMS = sorted(POLY)


def canonical_sha(obj: object) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def mon3(d: int):
    return [(i, j, h) for i in range(d + 1) for j in range(d + 1 - i) for h in range(d + 1 - i - j)]


@lru_cache(None)
def Hm(m: int, r: int) -> int:
    if m <= 0:
        return 0
    return (Hm(m - 1, r) + pow(m, -r, P)) % P


@lru_cache(None)
def ESm(x: int, r: int, m: int) -> int:
    return sum((Hm(t, m) * pow(t, -r, P) for t in range(1, x + 1))) % P


@lru_cache(None)
def Um(a: int, b: int, r: int, m: int) -> int:
    return sum((Hm(t + b, m) * pow(t, -r, P) for t in range(1, a + 1))) % P


def Tm(n: int, k: int, l: int) -> int:
    return (comb(n + k, n) * pow(comb(n, k), 2, P) * comb(n + l, n) * pow(comb(n, l), 2, P) * comb(n + k + l, n)) % P


def Am(n: int, x: int, r: int) -> int:
    return (Hm(n + x, r) - Hm(x, r)) % P


def Bm(n: int, x: int, r: int) -> int:
    return (Hm(n - x, r) - Hm(x, r)) % P


def Cm(n: int, k: int, l: int, r: int) -> int:
    return (Hm(n + k + l, r) - Hm(k + l, r)) % P


def Lm(n: int, k: int, l: int, x: int) -> int:
    return (-Am(n, x, 1) - Cm(n, k, l, 1) - 2 * Bm(n, x, 1)) % P


def r11m(k: int, l: int) -> int:
    return ((Hm(k + l, 1) - Hm(k, 1) - Hm(l, 1)) * (Hm(k, 2) + Hm(l, 2)) - Hm(k, 3) - Hm(l, 3) + Um(k, l, 1, 2) + Um(l, k, 1, 2)) % P


def r12m(k: int, l: int) -> int:
    inv2 = pow(2, -1, P)
    return (-2 * (Hm(k, 1) + Hm(l, 1) - Hm(k + l, 1)) * Hm(l, 3) + Hm(k, 2) * Hm(k + l, 2) - Hm(l, 2) * Hm(l, 2) * inv2 + Hm(k + l, 2) * Hm(l, 2) - 5 * Hm(l, 4) * inv2 + 2 * ESm(l, 1, 3) - Um(k, l, 2, 2)) % P


def r22m(k: int, l: int) -> int:
    return (-2 * (Hm(k, 2) + Hm(l, 2)) * (Hm(k, 3) + Hm(l, 3)) + 2 * Hm(k + l, 3) * (Hm(k, 2) + Hm(l, 2)) + 2 * Hm(k + l, 2) * (Hm(k, 3) + Hm(l, 3)) - 2 * Hm(k, 5) - 2 * Hm(l, 5) - 6 * ESm(k, 1, 4) - 6 * ESm(l, 1, 4) - 2 * ESm(k, 2, 3) - 2 * ESm(l, 2, 3) + 6 * Um(k, l, 1, 4) + 6 * Um(l, k, 1, 4) + 2 * Um(k, l, 2, 3) + 2 * Um(l, k, 2, 3)) % P


def W1m(n: int, k: int, l: int) -> int:
    lk = Lm(n, k, l, k)
    ll = Lm(n, k, l, l)
    return (r22m(k, l) + lk * r12m(k, l) + ll * r12m(l, k) + (lk * ll - Cm(n, k, l, 2)) * r11m(k, l)) % P


def w5m(n: int, k: int, l: int) -> int:
    inv2 = pow(2, -1, P)
    inv4 = pow(4, -1, P)
    alpha = (Am(n, k, 1) - Am(n, l, 1)) % P
    beta = (Bm(n, k, 1) - Bm(n, l, 1)) % P
    psi = (alpha * inv2 + beta) % P
    cc = ((Am(n, k, 2) + Am(n, l, 2)) * inv4 - alpha * psi * inv2) % P
    return (Hm(n + k, 5) + (alpha - beta) * Hm(n + k, 4) * inv2 + cc * Hm(n + k, 3)) % P


def source_cell_mod(n: int, k: int, l: int) -> int:
    w5sym = (w5m(n, k, l) + w5m(n, l, k)) * pow(2, -1, P) % P
    return Tm(n, k, l) * (W1m(n, k, l) + 2 * w5sym) % P


def atom_mod(name: str, n: int, k: int, l: int) -> int:
    p = name.split("_")
    if name.startswith("H_k_"): return Hm(k, int(p[-1]))
    if name.startswith("H_l_"): return Hm(l, int(p[-1]))
    if name.startswith("H_kl_"): return Hm(k + l, int(p[-1]))
    if name.startswith("H_nk_"): return Hm(n + k, int(p[-1]))
    if name.startswith("H_nl_"): return Hm(n + l, int(p[-1]))
    if name.startswith("A_k_"): return Am(n, k, int(p[-1]))
    if name.startswith("A_l_"): return Am(n, l, int(p[-1]))
    if name.startswith("B_k_"): return Bm(n, k, int(p[-1]))
    if name.startswith("B_l_"): return Bm(n, l, int(p[-1]))
    if name.startswith("C_"): return Cm(n, k, l, int(p[-1]))
    if name.startswith("U_k_l_"):
        r, m = map(int, p[-2:]); return Um(k, l, r, m)
    if name.startswith("U_l_k_"):
        r, m = map(int, p[-2:]); return Um(l, k, r, m)
    if name.startswith("ES_k_"):
        r, m = map(int, p[-2:]); return ESm(k, r, m)
    if name.startswith("ES_l_"):
        r, m = map(int, p[-2:]); return ESm(l, r, m)
    raise ValueError(name)


def monomial_mod(mon: tuple[str, ...], n: int, k: int, l: int) -> int:
    z = 1
    for name in mon:
        z = z * atom_mod(name, n, k, l) % P
    return z


def boundary(n: int, x: int) -> int:
    return x * (n + 1 - x)


def d_k(k: int, l: int) -> int:
    return (k + 1) ** 3 * (k + l + 1)


def d_l(k: int, l: int) -> int:
    return (l + 1) ** 3 * (k + l + 1)


def grid(nmax: int):
    return [(n, k, l) for n in range(2, nmax + 1) for k in range(n + 1) for l in range(n + 1)]


def matrix_row(n: int, k: int, l: int, qdeg: int) -> list[int]:
    mons = list(reversed(MONOMS))
    exps = list(reversed(mon3(qdeg)))
    den = (d_k(k, l), d_k(k + 1, l), d_l(k, l), d_l(k, l + 1))
    if any(x % P == 0 for x in den):
        raise AssertionError("verifier flux denominator collision")
    pk0 = Tm(n, k, l) * boundary(n, k) * pow(den[0], -1, P) % P
    pk1 = Tm(n, k + 1, l) * boundary(n, k + 1) * pow(den[1], -1, P) % P
    ql0 = Tm(n, k, l) * boundary(n, l) * pow(den[2], -1, P) % P
    ql1 = Tm(n, k, l + 1) * boundary(n, l + 1) * pow(den[3], -1, P) % P
    poly = []
    for i, j, h in exps:
        ni = pow(n, i, P)
        poly.append((ni * pow(k, j, P) % P * pow(l, h, P) % P, ni * pow(k + 1, j, P) % P * pow(l, h, P) % P, ni * pow(l, j, P) % P * pow(k, h, P) % P, ni * pow(l + 1, j, P) % P * pow(k, h, P) % P))
    row: list[int] = []
    for mon in mons:
        a0 = pk0 * monomial_mod(mon, n, k, l) % P
        a1 = pk1 * monomial_mod(mon, n, k + 1, l) % P
        b0 = ql0 * monomial_mod(mon, n, l, k) % P
        b1 = ql1 * monomial_mod(mon, n, l + 1, k) % P
        for p0, p1, q0, q1 in poly:
            row.append((a0 * p0 - a1 * p1 + b0 * q0 - b1 * q1) % P)
    return row


def compile_rank(tmp: Path) -> Path:
    exe = tmp / "rank_mod"
    subprocess.run([os.environ.get("CC", "cc"), "-O3", str(HERE / "rank_mod.c"), "-o", str(exe)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return exe


def rank_rows(rows: list[list[int]], target_values: list[int] | None, exe: Path, tmp: Path, tag: str) -> int:
    nr = len(rows)
    nc0 = len(rows[0])
    nc = nc0 + (1 if target_values is not None else 0)
    path = tmp / f"{tag}.bin"
    with path.open("wb") as f:
        f.write(struct.pack("<II", nr, nc))
        for i, row in enumerate(rows):
            a = array("I", (x % P for x in row))
            if target_values is not None:
                a.append(target_values[i] % P)
            a.tofile(f)
    return int(subprocess.check_output([str(exe), str(path)], text=True).strip())


def basis_lock() -> None:
    if len(MONOMS) != 198:
        raise AssertionError("verifier basis cardinality drift")
    payload = [{"atoms": list(mon), "coefficient": str(POLY[mon])} for mon in MONOMS]
    if canonical_sha(payload) != BASIS_SHA:
        raise AssertionError("verifier basis digest drift")
    if jet_map.swap(POLY) != POLY:
        raise AssertionError("verifier target swap drift")


def main() -> int:
    basis_lock()
    for n in range(0, 9):
        if target.t3_sum(n) != 0:
            raise AssertionError(f"finite T3 replay failed at n={n}")
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    witness = json.loads(WITNESS.read_text(encoding="utf-8"))
    ids = witness["coefficient_row_indices"]
    if canonical_sha(ids) != Q2_INDEX_SHA:
        raise AssertionError("verifier degree-2 witness digest drift")
    with tempfile.TemporaryDirectory(prefix="t3_008_verify_") as td:
        tmp = Path(td)
        exe = compile_rank(tmp)
        observed = []
        for qdeg, nmax, expected_unknowns in ((0, 20, 198), (1, 20, 792)):
            g = list(reversed(grid(nmax)))
            rows = [matrix_row(n, k, l, qdeg) for n, k, l in g]
            tv = [source_cell_mod(n, k, l) for n, k, l in g]
            rc = rank_rows(rows, None, exe, tmp, f"q{qdeg}_coeff_reverse")
            ra = rank_rows(rows, tv, exe, tmp, f"q{qdeg}_aug_reverse")
            if (rc, ra) != (expected_unknowns, expected_unknowns + 1):
                raise AssertionError(f"verifier degree-{qdeg} rank drift: {(rc, ra)}")
            observed.append((rc, ra))
        g22 = grid(22)
        coeff_points = list(reversed([g22[i] for i in ids]))
        coeff_rows = [matrix_row(n, k, l, 2) for n, k, l in coeff_points]
        rc2 = rank_rows(coeff_rows, None, exe, tmp, "q2_coeff_reverse")
        extra = tuple(witness["augmented_extra_row_point"])
        aug_points = [extra] + coeff_points
        aug_rows = [matrix_row(n, k, l, 2) for n, k, l in aug_points]
        aug_tv = [source_cell_mod(n, k, l) for n, k, l in aug_points]
        ra2 = rank_rows(aug_rows, aug_tv, exe, tmp, "q2_aug_reverse")
        if (rc2, ra2) != (1980, 1981):
            raise AssertionError(f"verifier degree-2 rank drift: {(rc2, ra2)}")
        observed.append((rc2, ra2))
    expected = [(s["coefficient_rank"], s["augmented_rank"]) for s in result["stages"]]
    if observed != expected:
        raise AssertionError(f"verifier/result rank mismatch: {observed} != {expected}")
    if result["terminal"] != "SYMMETRIC_2D_WEIGHT5_DIVERGENCE_BOUNDED_CLASS_EXHAUSTED":
        raise AssertionError("terminal drift")
    if result["proof_effect"] != "NONE" or result["promotion_effect"] != "NONE":
        raise AssertionError("claim inflation")
    print("T3-008 independent symmetric-2D affine-rank replay: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
