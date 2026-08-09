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
T3002_TARGET = ODD / "OZ_RT_BZ_T3_002" / "target.py"
OUT = HERE / "SEARCH_RESULT.json"
P = 1000003

sys.path.insert(0, str(T3005))
import jet_map  # type: ignore  # protected predecessor implementation

spec = importlib.util.spec_from_file_location("t3_002_target_for_t3_006", T3002_TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load protected T3-002 target")
target002 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(target002)


def modq(x: Q) -> int:
    den = x.denominator % P
    if den == 0:
        raise AssertionError("rank-prime denominator collision")
    return (x.numerator % P) * pow(den, -1, P) % P


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
def Hm(m: int, r: int) -> int:
    if m <= 0:
        return 0
    return (Hm(m - 1, r) + pow(m, -r, P)) % P


def Tm(n: int, k: int, l: int) -> int:
    return (
        comb(n + k, n) * pow(comb(n, k), 2, P)
        * comb(n + l, n) * pow(comb(n, l), 2, P)
        * comb(n + k + l, n)
    ) % P


def ESm(x: int, r: int, m: int) -> int:
    return sum((Hm(t, m) * pow(t, -r, P) for t in range(1, x + 1))) % P


def Um(a: int, b: int, r: int, m: int) -> int:
    return sum((Hm(t + b, m) * pow(t, -r, P) for t in range(1, a + 1))) % P


def Am(n: int, x: int, r: int) -> int:
    return (Hm(n + x, r) - Hm(x, r)) % P


def Bm(n: int, x: int, r: int) -> int:
    return (Hm(n - x, r) - Hm(x, r)) % P


def Cm(n: int, k: int, l: int, r: int) -> int:
    return (Hm(n + k + l, r) - Hm(k + l, r)) % P


def atom_mod(name: str, n: int, k: int, l: int) -> int:
    p = name.split("_")
    if name.startswith("H_k_"):
        return Hm(k, int(p[-1]))
    if name.startswith("H_l_"):
        return Hm(l, int(p[-1]))
    if name.startswith("H_kl_"):
        return Hm(k + l, int(p[-1]))
    if name.startswith("H_nk_"):
        return Hm(n + k, int(p[-1]))
    if name.startswith("H_nl_"):
        return Hm(n + l, int(p[-1]))
    if name.startswith("A_k_"):
        return Am(n, k, int(p[-1]))
    if name.startswith("A_l_"):
        return Am(n, l, int(p[-1]))
    if name.startswith("B_k_"):
        return Bm(n, k, int(p[-1]))
    if name.startswith("B_l_"):
        return Bm(n, l, int(p[-1]))
    if name.startswith("C_"):
        return Cm(n, k, l, int(p[-1]))
    if name.startswith("U_k_l_"):
        r, m = map(int, p[-2:]); return Um(k, l, r, m)
    if name.startswith("U_l_k_"):
        r, m = map(int, p[-2:]); return Um(l, k, r, m)
    if name.startswith("ES_k_"):
        r, m = map(int, p[-2:]); return ESm(k, r, m)
    if name.startswith("ES_l_"):
        r, m = map(int, p[-2:]); return ESm(l, r, m)
    raise ValueError(name)


POLY = jet_map.target_polynomial()
MONOMS = sorted(POLY)


def monomial_mod(mon: tuple[str, ...], n: int, k: int, l: int) -> int:
    out = 1
    for name in mon:
        out = out * atom_mod(name, n, k, l) % P
    return out


def Fm(n: int, k: int, l: int) -> int:
    defect = 0
    for mon in MONOMS:
        defect = (defect + modq(POLY[mon]) * monomial_mod(mon, n, k, l)) % P
    return Tm(n, k, l) * defect % P


def qden(k: int, l: int) -> int:
    return (l + 1) ** 3 * (k + l + 1)


def samples(nmax: int):
    return [
        (n, k, l)
        for n in range(3, nmax + 1)
        for k in range(0, n - 1)
        for l in range(0, n)
    ]


def basis_lock() -> dict:
    if len(MONOMS) != 198:
        raise AssertionError("T3-005 monomial count drift")
    if jet_map.swap(POLY) != POLY:
        raise AssertionError("k/l target symmetry drift")
    nested = lambda x: x.startswith(("U_k_l_", "U_l_k_", "ES_k_", "ES_l_"))
    if any(sum(nested(x) for x in mon) > 1 for mon in MONOMS):
        raise AssertionError("nested-atom arity drift")
    payload = [{"atoms": list(mon), "coefficient": str(POLY[mon])} for mon in MONOMS]
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    if digest != "cbdfe5798d360cb98f2d64743907a06ddc0612f88d17ef4bcef65c81c74e1438":
        raise AssertionError("raw-jet basis digest drift")
    nested_count = sum(any(nested(x) for x in mon) for mon in MONOMS)
    atoms = {x for mon in MONOMS for x in mon}
    return {
        "source": "OZ-RT-BZ-T3-005 linear raw-jet coefficient map",
        "monomial_count": 198,
        "one_body_only_count": 198 - nested_count,
        "one_nested_atom_count": nested_count,
        "distinct_atom_count": len(atoms),
        "basis_sha256": digest,
        "k_l_swap_invariant": True,
        "max_nested_atoms_per_monomial": 1,
    }


def exact_cross_lock() -> int:
    checks = 0
    for n in range(2, 7):
        for k in range(n + 1):
            for l in range(n + 1):
                if Fm(n, k, l) != modq(target002.cell(n, k, l)):
                    raise AssertionError("T3-002/T3-005 target lock drift")
                checks += 1
    return checks


def compile_rank(tmp: Path) -> Path:
    exe = tmp / "rank_mod"
    cc = os.environ.get("CC", "cc")
    subprocess.run(
        [cc, "-O3", str(HERE / "rank_mod.c"), "-o", str(exe)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return exe


def rank_rows(rows: list[list[int]], exe: Path, tmp: Path, tag: str) -> int:
    if not rows:
        return 0
    nr, nc = len(rows), len(rows[0])
    path = tmp / f"{tag}.bin"
    with path.open("wb") as f:
        f.write(struct.pack("<II", nr, nc))
        for row in rows:
            if len(row) != nc:
                raise AssertionError("ragged rank matrix")
            a = array("I", (x % P for x in row))
            if a.itemsize != 4:
                raise AssertionError("unexpected unsigned-int width")
            a.tofile(f)
    rank = int(subprocess.check_output([str(exe), str(path)], text=True).strip())
    return rank


def scalar_rows(adeg: int, qdeg: int, nmax: int) -> list[list[int]]:
    ma, mq = mon2(adeg), mon3(qdeg)
    rows = []
    for n, k, l in samples(nmax):
        row = []
        for shift in range(3):
            f = Fm(n, k + shift, l)
            row.extend(f * pow(n, i, P) * pow(k, j, P) % P for i, j in ma)
        fc, fn = Fm(n, k, l), Fm(n, k, l + 1)
        dc, dn = qden(k, l) % P, qden(k, l + 1) % P
        if dc == 0 or dn == 0:
            raise AssertionError("certificate denominator collision")
        idc, idn = pow(dc, -1, P), pow(dn, -1, P)
        for i, j, h in mq:
            pc = pow(n, i, P) * pow(k, j, P) * pow(l, h, P) % P
            pn = pow(n, i, P) * pow(k, j, P) * pow(l + 1, h, P) % P
            row.append((fc * pc * idc - fn * pn * idn) % P)
        rows.append(row)
    return rows


def module_row(n: int, k: int, l: int, qdeg: int, reverse: bool = False) -> list[int]:
    ma, mq = mon2(2), mon3(qdeg)
    mons = list(reversed(MONOMS)) if reverse else MONOMS
    qmons = list(reversed(mq)) if reverse else mq
    row = []
    for shift in range(3):
        f = Fm(n, k + shift, l)
        row.extend(f * pow(n, i, P) * pow(k, j, P) % P for i, j in ma)
    tc, tn = Tm(n, k, l), Tm(n, k, l + 1)
    dc, dn = qden(k, l) % P, qden(k, l + 1) % P
    if dc == 0 or dn == 0:
        raise AssertionError("certificate denominator collision")
    idc, idn = pow(dc, -1, P), pow(dn, -1, P)
    for mon in mons:
        vc, vn = monomial_mod(mon, n, k, l), monomial_mod(mon, n, k, l + 1)
        for i, j, h in qmons:
            pc = pow(n, i, P) * pow(k, j, P) * pow(l, h, P) % P
            pn = pow(n, i, P) * pow(k, j, P) * pow(l + 1, h, P) % P
            row.append((tc * vc * pc * idc - tn * vn * pn * idn) % P)
    return row


def module_stage(qdeg: int, nmax: int, exe: Path, tmp: Path) -> dict:
    tel = 3 * len(mon2(2))
    cert = len(MONOMS) * len(mon3(qdeg))
    unknowns = tel + cert
    grid = samples(nmax)
    if len(grid) < unknowns:
        raise AssertionError("insufficient rank-witness rows")
    rows = [module_row(n, k, l, qdeg) for n, k, l in grid[:unknowns]]
    rank = rank_rows(rows, exe, tmp, f"module_q{qdeg}")
    return {
        "q_coefficient_degree": qdeg,
        "n_max": nmax,
        "full_grid_rows": len(grid),
        "rank_witness_rows": unknowns,
        "telescoper_unknowns": tel,
        "certificate_unknowns": cert,
        "unknowns": unknowns,
        "rank": rank,
        "nullity": unknowns - rank,
    }


def main() -> int:
    basis = basis_lock()
    cross = exact_cross_lock()
    with tempfile.TemporaryDirectory(prefix="t3_006_") as td:
        tmp = Path(td)
        exe = compile_rank(tmp)
        scalar = []
        for adeg in range(7):
            qdeg = adeg + 2
            nmax = max(8, adeg + 5)
            rows = scalar_rows(adeg, qdeg, nmax)
            unknowns = len(rows[0])
            rank = rank_rows(rows, exe, tmp, f"scalar_a{adeg}")
            scalar.append({
                "a_degree": adeg, "q_degree": qdeg, "n_max": nmax,
                "equations": len(rows), "unknowns": unknowns,
                "rank": rank, "nullity": unknowns - rank,
            })
        module = [module_stage(q, n, exe, tmp) for q, n in ((0, 10), (1, 15), (2, 19))]

    if any(x["nullity"] != 0 for x in scalar + module):
        terminal = "CANDIDATE_SPACE_REMAINS_REQUIRING_RATIONAL_RECONSTRUCTION"
    else:
        terminal = "ORDER2_COMPLETE_WEIGHT5_MODULE_BOUNDED_CLASS_EXHAUSTED"
    result = {
        "schema_version": "1.0.0",
        "operation": "OZ-RT-BZ-T3-006",
        "route": "COUPLED_WEIGHT5_RAW_JET_ORDER2_SEARCH_001",
        "prime": P,
        "target": "sum_{k,l=0}^n T(n,k,l)*(W1(k,l)+2*w5_sym(n,k,l))=0",
        "predecessor": {"issue": 341, "pull_request": 344, "merge_commit": "e99defaabbc0d971e6299360ac03084e516c31c3", "merge_tree": "041b4f7afa647fec06d3303503b53fa0fc65350d"},
        "execution_intake": {"protected_head": "d2cdd1cfb57feb648bdd624a3362dae646a8b72f", "protected_tree": "3b7cc40fbf7f82cb1c219aef6b9733429e83e54f"},
        "basis": basis,
        "exact_target_cross_checks": cross,
        "search_equation": "sum_{j=0}^2 a_j(n,k) F(n,k+j,l) = Delta_l Q(n,k,l)",
        "certificate_denominator": "(l+1)^3*(k+l+1)",
        "denominator_provenance": "exact undeformed T(n,k,l+1)/T(n,k,l) shift-ratio denominator",
        "stage_a_scalar_envelope": {"classification": "EXACT_BOUNDED_EXHAUSTION", "stages": scalar, "strongest_frontier": "ORDER2_EXTRACTED_SCALAR_ENVELOPE_ADEG_LE_6_QDEG_LE_8", "terminal": "NO_NONZERO_ORDER2_SCALAR_ENVELOPE_CERTIFICATE_IN_DECLARED_CLASS"},
        "stage_b_full_weight5_module": {"classification": "EXACT_BOUNDED_EXHAUSTION", "a_degree": 2, "certificate_basis": "all 198 locked weight-five monomials with independent polynomial coefficients", "stages": module, "producer_witness_selection": "first unknowns rows of the lexicographic exact grid", "independent_verifier_witness_selection": "last unknowns rows of the same declared exact grid with reversed basis ordering", "strongest_frontier": "COUPLED_WEIGHT5_RAW_JET_ORDER2_ADEG_LE_2_QCOEFFDEG_LE_2", "terminal": "NO_NONZERO_ORDER2_FIBRE_CERTIFICATE_IN_COMPLETE_WEIGHT5_MODULE_DECLARED_CLASS"},
        "rank_certificate": "FULL_COLUMN_RANK_MOD_P_EXHIBITS_NONZERO_MAXIMAL_MINOR_AND_IMPLIES_FULL_COLUMN_RANK_OVER_Q",
        "denominator_condition": "all exact rational matrix-entry denominators are nonzero modulo p on every declared sample",
        "mirror_status": "EXACTLY_EQUIVALENT_BY_K_L_SWAP",
        "terminal": terminal,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "next_distinct_routes": ["COUPLED_WEIGHT5_RAW_JET_ORDER3_4_SEARCH_001", "SYMMETRIC_2D_RAW_JET_DIVERGENCE_001", "T3_SEQUENCE_RECURRENCE_EXTRACTION_001"],
        "nonclaims": ["T3 is not proved", "T3 is not refuted", "bounded order-2 exhaustion is not evidence that T3 is false", "T1-top is not substituted for T3", "DEPTH and Sharp-12 are unchanged", "MATHCERT and GRAPH_CERTIFIED are unchanged"],
    }
    expected = json.loads(OUT.read_text(encoding="utf-8"))
    expected.pop("exact_target_cross_checks", None)
    actual = dict(result); actual.pop("exact_target_cross_checks", None)
    if actual != expected:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        raise AssertionError("canonical search result drift; regenerated SEARCH_RESULT.json")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
