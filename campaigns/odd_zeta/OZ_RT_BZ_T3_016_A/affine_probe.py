from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import urllib.request
from pathlib import Path

SOURCE_REPOSITORY = "rain-1/-odd-zeta-values-moremath"
SOURCE_COMMIT = "6cc0bf07137815ceeef0d9f340559f85352391e5"
SOURCE_FILES = {
    "zla.py": ("work/z5la/zla.py", "76868d96a9ebbe41dbc72ca71e32693e4e2bd374"),
    "solve.py": ("work/z5la/solve.py", "478b15ce7584b5e8af6caaf5326d99c85a7b55bf"),
    "qrow.py": ("work/z5la/qrow.py", "91461bbd6094d01fb94d2d27cf3bc605f070eb91"),
    "ordm.py": ("work/z5la/ordm.py", "5947e3ab176a57401c8e0d4f46e3402f0f9ee08c"),
    "o_scan.py": ("work/z5la/o_scan.py", "bc6e9a59a48b15eddbab8e80ad4e5063972582d2"),
    "o_zero.py": ("work/z5la/o_zero.py", "2bfa58cb573b0d40646e85bdbed682d8344b594a"),
    "fastlin.py": ("work/z5la/fastlin.py", "22e05c965a908ffe56308630b7af498f9d7fa986"),
    "ratrec.py": ("work/z5la/ratrec.py", "0d407c2aeda2b8de4a2f570f7890f97bd267239a"),
    "Qrow_phicert.m": ("work/z5cf/Qrow_phicert.m", "5189f47a425611c44f2c0faee438b7856725236c"),
    "a_lift.json": ("work/z5la/a_lift.json", "564fc9637f31b870d85dab293d6cbb5cfe52bae0"),
}

DRIVER = r'''
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(sys.argv[1])
N = int(sys.argv[2])
P = int(sys.argv[3])
NFRESH = int(sys.argv[4])

sys.path.insert(0, str(ROOT))
import qrow
qrow.SRC = str(ROOT / "Qrow_phicert.m")
qrow.CACHE = str(ROOT / "qrow_cache.pkl")
import fastlin
import o_scan
import o_zero
import ordm
import solve

M_ORDER = 7
RANK_ROWS = 1048
D = o_scan.dens(M_ORDER)["E1"]
dk0 = sum(mu * abs(f[2]) for f, mu in D)
dl0 = sum(mu * abs(f[3]) for f, mu in D)
ans = solve.Ansatz(D, D, dk0 + 18, dl0 + 18, dk0 + 18, dl0 + 18,
                   force_k=1, force_l=1)
assert ans.nc == 1624

# Natural curl coordinates: the 24x24 low-r rectangle. The exact campaign
# proof identifies the full homogeneous kernel with the discrete-curl image;
# at generic n these 576 coordinates form an invertible curl minor.
gauge = [i for i, mon in enumerate(ans.mons_r)
         if 2 <= mon[0] <= 25 and 0 <= mon[1] <= 23]
assert len(gauge) == 576

lift = json.loads((ROOT / "a_lift.json").read_text())
def peval(coeffs, x, p):
    value = 0
    for coefficient in reversed(coeffs):
        value = (value * x + int(coefficient)) % p
    return value

avec = np.asarray([peval(row, N, P) for row in lift["a"]], dtype=np.int64)
if int(avec[0]) % P == 0:
    raise RuntimeError("a_0 specialization vanishes modulo probe prime")
avec = avec * pow(int(avec[0]), P - 2, P) % P

pd = ordm.PDm("w3", P, N, M_ORDER, RANK_ROWS + NFRESH)
Acol = ordm.acols(pd)
stand = [j for j in pd.free if len(pd.B[j]) > 0]
assert len(stand) == 7
R0, R1, S0, S1, op = o_zero.design(pd, ans)

rhs = np.zeros((pd.npts, len(stand)), dtype=np.int64)
for column, block in enumerate(stand):
    slab = Acol[block * pd.npts:(block + 1) * pd.npts].astype(object)
    rhs[:, column] = [int(x) for x in (-(slab @ avec.astype(object))) % P]

constraints = np.zeros((len(gauge), ans.nc), dtype=np.int64)
for row, column in enumerate(gauge):
    constraints[row, column] = 1
G = np.concatenate([op[:RANK_ROWS].astype(np.int64), constraints], axis=0)
B = np.concatenate([rhs[:RANK_ROWS], np.zeros((len(gauge), len(stand)), dtype=np.int64)], axis=0)
X, rank, piv, nbad = fastlin.solve(G, B, P, nb=64)

if rank != ans.nc or nbad != 0:
    raise RuntimeError(f"potential gauge solve failed: rank={rank} nbad={nbad}")
if np.count_nonzero(X[np.asarray(gauge), :] % P):
    raise RuntimeError("potential gauge constraints not satisfied")

fresh = o_zero.matmul_mod(op[RANK_ROWS:], X.astype(np.float64), P)
fresh = (fresh - rhs[RANK_ROWS:]) % P
fresh_violations = int(np.count_nonzero(fresh))
if fresh_violations:
    raise RuntimeError(f"fresh residual violations: {fresh_violations}")

# Digest the canonical fixed-(n,p) seven-block section. This is diagnostic
# identity, not theorem authority.
xd = np.asarray(X, dtype="<i8", order="C")
digest = hashlib.sha256(xd.tobytes(order="C")).hexdigest()
nonzero = [int(np.count_nonzero(X[:, j] % P)) for j in range(X.shape[1])]
max_centered = 0
for value in X.ravel():
    v = int(value) % P
    v = min(v, P - v)
    max_centered = max(max_centered, v)

print(json.dumps({
    "n": N,
    "prime": P,
    "a_normalized": [int(x) for x in avec],
    "standalone_blocks": [str(pd.B[j]) for j in stand],
    "e1_columns": ans.nc,
    "rank_rows": RANK_ROWS,
    "gauge_coordinates": len(gauge),
    "augmented_rank": int(rank),
    "solver_nbad": int(nbad),
    "fresh_points": NFRESH,
    "fresh_violations": fresh_violations,
    "gauge_violations": int(np.count_nonzero(X[np.asarray(gauge), :] % P)),
    "section_sha256": digest,
    "section_nonzero_coefficients_by_block": nonzero,
    "max_centered_residue": max_centered,
}, sort_keys=True))
'''


def _blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def _fetch_locked(root: Path) -> None:
    for local_name, (remote_path, expected_sha) in SOURCE_FILES.items():
        url = f"https://raw.githubusercontent.com/{SOURCE_REPOSITORY}/{SOURCE_COMMIT}/{remote_path}"
        with urllib.request.urlopen(url, timeout=90) as response:
            data = response.read()
        got = _blob_sha1(data)
        if got != expected_sha:
            raise AssertionError(f"source lock drift for {remote_path}: {got} != {expected_sha}")
        (root / local_name).write_bytes(data)


def probe(n: int, prime: int = 4194301, fresh_points: int = 48) -> dict:
    with tempfile.TemporaryDirectory(prefix="oz-t3-016-affine-") as tmp:
        root = Path(tmp)
        _fetch_locked(root)
        driver = root / "driver.py"
        driver.write_text(textwrap.dedent(DRIVER), encoding="utf-8")
        env = dict(os.environ)
        env.setdefault("OMP_NUM_THREADS", "1")
        env.setdefault("OPENBLAS_NUM_THREADS", "1")
        env.setdefault("MKL_NUM_THREADS", "1")
        completed = subprocess.run(
            [sys.executable, str(driver), str(root), str(n), str(prime), str(fresh_points)],
            check=True,
            capture_output=True,
            text=True,
            env=env,
            timeout=900,
        )
        lines = [line for line in completed.stdout.splitlines() if line.strip()]
        if not lines:
            raise RuntimeError("affine probe produced no output")
        return json.loads(lines[-1])
