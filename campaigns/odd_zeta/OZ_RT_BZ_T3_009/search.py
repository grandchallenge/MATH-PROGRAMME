#!/usr/bin/env python3
from __future__ import annotations

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
BASE_PATH = ODD / "OZ_RT_BZ_T3_006" / "producer.py"
RANK_C = ODD / "OZ_RT_BZ_T3_008" / "rank_mod.c"
OUT = HERE / "SEARCH_RESULT.json"
P = 1000003

spec = importlib.util.spec_from_file_location("t3_006_base_for_t3_009", BASE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load protected T3-006 basis")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
MONOMS = base.MONOMS


def a0(n): return 41218*n**3 + 198849*n**2 + 320790*n + 173057

def B8(n):
    return (3874492*n**8 + 59373972*n**7 + 394148190*n**6 + 1481084196*n**5
            + 3447878810*n**4 + 5095855458*n**3 + 4673546679*n**2
            + 2433871008*n + 551502039)

def B9(n):
    return (48802112*n**9 + 967468896*n**8 + 8488000862*n**7 + 43246197636*n**6
            + 140983768422*n**5 + 304912330849*n**4 + 437406946975*n**3
            + 401272692378*n**2 + 213593890911*n + 50257929339)

def coeffs(n):
    return ((n+1)**5*(n+2)*a0(n+1), -2*(n+2)*B8(n), -2*B9(n), 2*(n+3)**5*(2*n+5)*a0(n))


def mon3(d):
    return [(i,j,h) for i in range(d+1) for j in range(d+1-i) for h in range(d+1-i-j)]


def grid(nmax):
    return [(n,k,l) for n in range(nmax+1) for k in range(n+4) for l in range(n+4)]


def boundary(N,x): return x*(N+1-x)
def dk(k,l): return (k+1)**3*(k+l+1)
def dl(k,l): return (l+1)**3*(k+l+1)


def recurrence_cell_mod(n,k,l):
    return sum((c % P)*base.Fm(n+j,k,l) for j,c in enumerate(coeffs(n))) % P


def zero_extension_lock(nmax):
    checks = 0
    for n in range(nmax+1):
        for j in range(4):
            nj = n+j
            for k in range(n+4):
                for l in range(n+4):
                    if k > nj or l > nj:
                        if base.target002.T(nj,k,l) != 0:
                            raise AssertionError("binomial zero-extension drift")
                        checks += 1
    return checks


def matrix_row(n,k,l,degree,reverse=False):
    N=n+3
    exps=list(reversed(mon3(degree))) if reverse else mon3(degree)
    mons=list(reversed(MONOMS)) if reverse else MONOMS
    dkc, dkn = dk(k,l)%P, dk(k+1,l)%P
    dlc, dln = dl(k,l)%P, dl(k,l+1)%P
    if 0 in (dkc,dkn,dlc,dln):
        raise AssertionError("flux denominator collision")
    pk0=base.Tm(N,k,l)*(boundary(N,k)%P)*pow(dkc,-1,P)%P
    pk1=base.Tm(N,k+1,l)*(boundary(N,k+1)%P)*pow(dkn,-1,P)%P
    ql0=base.Tm(N,k,l)*(boundary(N,l)%P)*pow(dlc,-1,P)%P
    ql1=base.Tm(N,k,l+1)*(boundary(N,l+1)%P)*pow(dln,-1,P)%P
    row=[]
    for mon in mons:
        av0=pk0*base.monomial_mod(mon,N,k,l)%P
        av1=pk1*base.monomial_mod(mon,N,k+1,l)%P
        bv0=ql0*base.monomial_mod(mon,N,l,k)%P
        bv1=ql1*base.monomial_mod(mon,N,l+1,k)%P
        for i,j,h in exps:
            p0=pow(n,i,P)*pow(k,j,P)%P*pow(l,h,P)%P
            p1=pow(n,i,P)*pow(k+1,j,P)%P*pow(l,h,P)%P
            q0=pow(n,i,P)*pow(l,j,P)%P*pow(k,h,P)%P
            q1=pow(n,i,P)*pow(l+1,j,P)%P*pow(k,h,P)%P
            row.append((av0*p0-av1*p1+bv0*q0-bv1*q1)%P)
    return row


def compile_rank(tmp):
    exe=tmp/"rank_mod"
    subprocess.run([os.environ.get("CC","cc"),"-O3",str(RANK_C),"-o",str(exe)],check=True,
                   stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    return exe


def rank_rows(rows,exe,tmp,tag,target=None):
    nr=len(rows); nc0=len(rows[0]); nc=nc0+(1 if target is not None else 0)
    path=tmp/f"{tag}.bin"
    with path.open("wb") as f:
        f.write(struct.pack("<II",nr,nc))
        for i,row in enumerate(rows):
            vals=array("I",(x%P for x in row))
            if target is not None: vals.append(target[i]%P)
            vals.tofile(f)
    return int(subprocess.check_output([str(exe),str(path)],text=True).strip())


def stage(degree,nmax,exe,tmp,reverse=False):
    g=grid(nmax)
    rows=[matrix_row(n,k,l,degree,reverse=reverse) for n,k,l in g]
    rhs=[recurrence_cell_mod(n,k,l) for n,k,l in g]
    unknowns=len(MONOMS)*len(mon3(degree))
    rc=rank_rows(rows,exe,tmp,f"d{degree}_coeff_{int(reverse)}")
    ra=rank_rows(rows,exe,tmp,f"d{degree}_aug_{int(reverse)}",rhs)
    return {"coefficient_degree":degree,"n_max":nmax,"full_grid_rows":len(g),"unknowns":unknowns,
            "coefficient_rank":rc,"augmented_rank":ra}


def main():
    basis=base.basis_lock()
    if basis["basis_sha256"] != "cbdfe5798d360cb98f2d64743907a06ddc0612f88d17ef4bcef65c81c74e1438":
        raise AssertionError("protected basis drift")
    zero_extension_lock(12)
    expected=json.loads(OUT.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="t3_009_rec_") as td:
        tmp=Path(td); exe=compile_rank(tmp)
        got=[stage(0,7,exe,tmp),stage(1,12,exe,tmp)]
    for a,b in zip(got,expected["stages"]):
        for key in ("coefficient_degree","n_max","full_grid_rows","unknowns","coefficient_rank","augmented_rank"):
            if a[key] != b[key]: raise AssertionError(f"recurrence search drift: {key}")
        if a["coefficient_rank"] != a["unknowns"] or a["augmented_rank"] != a["unknowns"]+1:
            raise AssertionError("bounded recurrence class no longer exactly inconsistent")
    print(json.dumps(got,sort_keys=True,separators=(",",":")))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
