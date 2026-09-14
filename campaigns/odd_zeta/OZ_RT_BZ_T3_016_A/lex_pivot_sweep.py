from __future__ import annotations

import hashlib
import json
import multiprocessing as mp
import shutil
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import affine_sweep

SOURCE_REPOSITORY = affine_sweep.SOURCE_REPOSITORY
SOURCE_COMMIT = affine_sweep.SOURCE_COMMIT
SOURCE_TREE = affine_sweep.SOURCE_TREE
SOURCE_FILES = dict(affine_sweep.SOURCE_FILES)

M_ORDER = affine_sweep.M_ORDER
E1_COLUMNS = affine_sweep.E1_COLUMNS
EXPECTED_RANK = affine_sweep.FREE_COORDINATES
STANDALONE_BLOCKS = affine_sweep.STANDALONE_BLOCKS
SECTION_MODE = "LEXICOGRAPHIC_FIRST_PIVOT"
DEFAULT_REQUEST = HERE / "LEX_PIVOT_SWEEP_REQUEST.json"


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _pivot_sha(pivots: list[int]) -> str:
    return _sha256_bytes(_canonical_json_bytes([int(x) for x in pivots]))


def load_request(path: Path | str = DEFAULT_REQUEST) -> dict:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_request(value)
    return value


def validate_request(request: dict) -> dict:
    required = {
        "schema_version",
        "request_id",
        "enabled",
        "section_mode",
        "expected_pivot_sha256",
        "source_commit",
        "source_tree",
        "prime",
        "n_start",
        "n_stop",
        "chunks",
        "workers_per_chunk",
        "fit_extra_rows",
        "fresh_rows",
        "solver_block_size",
        "reconstruction_fit_count",
        "holdout_count",
        "evidence_effect",
        "proof_effect",
        "promotion_effect",
    }
    missing = sorted(required - set(request))
    if missing:
        raise AssertionError(f"lex-pivot sweep request missing fields: {missing}")
    base = dict(request)
    affine_sweep.validate_request(base)
    if request["section_mode"] != SECTION_MODE:
        raise AssertionError("lex-pivot section mode drift")
    expected = request["expected_pivot_sha256"]
    if expected is not None:
        if not isinstance(expected, str) or len(expected) != 64:
            raise AssertionError("expected pivot digest must be a SHA-256 hex string")
        try:
            int(expected, 16)
        except ValueError as exc:
            raise AssertionError("expected pivot digest must be hexadecimal") from exc
    if request["enabled"] and expected is None:
        raise AssertionError("enabled lex-pivot sweep requires an expected pivot digest")
    request["rational_degree_test_bound"] = base["rational_degree_test_bound"]
    return request


def max_rational_degree_bound(sample_count: int) -> int:
    return affine_sweep.max_rational_degree_bound(sample_count)


def chunk_ranges(request: dict) -> list[tuple[int, int]]:
    validate_request(request)
    start = int(request["n_start"])
    stop = int(request["n_stop"])
    chunks = int(request["chunks"])
    total = stop - start + 1
    q, r = divmod(total, chunks)
    out: list[tuple[int, int]] = []
    cursor = start
    for index in range(chunks):
        size = q + (1 if index < r else 0)
        if size <= 0:
            raise AssertionError("empty lex-pivot sweep chunk")
        out.append((cursor, cursor + size - 1))
        cursor += size
    if cursor != stop + 1:
        raise AssertionError("lex-pivot chunk partition drift")
    return out


def verify_source_checkout(source: Path | str, request: dict) -> dict:
    return affine_sweep.verify_source_checkout(source, request)


def _install_source_modules(source: Path, cache_path: Path, *, prewarm: bool) -> None:
    affine_sweep._install_source_modules(source, cache_path, prewarm=prewarm)


def _worker_init(source: str, cache_path: str) -> None:
    _install_source_modules(Path(source), Path(cache_path), prewarm=False)


def _lex_shape(
    n: int,
    p: int,
    fit_rows: int,
    fresh_rows: int,
    nb: int,
    expected_pivot_sha256: str | None = None,
) -> tuple[np.ndarray, dict]:
    modules = affine_sweep._MODULES
    fastlin = modules["fastlin"]
    o_scan = modules["o_scan"]
    o_zero = modules["o_zero"]
    ordm = modules["ordm"]
    solve = modules["solve"]
    source = affine_sweep._SOURCE_ROOT
    if source is None:
        raise AssertionError("source modules not initialized")

    D = o_scan.dens(M_ORDER)["E1"]
    dk0 = sum(mu * abs(f[2]) for f, mu in D)
    dl0 = sum(mu * abs(f[3]) for f, mu in D)
    ans = solve.Ansatz(
        D,
        D,
        dk0 + 18,
        dl0 + 18,
        dk0 + 18,
        dl0 + 18,
        force_k=1,
        force_l=1,
    )
    if ans.nc != E1_COLUMNS:
        raise AssertionError(f"E1 column drift: {ans.nc}")

    lift = json.loads((source / "work" / "z5la" / "a_lift.json").read_text(encoding="utf-8"))
    avec = np.asarray([affine_sweep._peval(row, n, p) for row in lift["a"]], dtype=np.int64)

    pd = ordm.PDm("w3", p, n, M_ORDER, fit_rows + fresh_rows)
    Acol = ordm.acols(pd)
    stand = [j for j in pd.free if len(pd.B[j]) > 0]
    if len(stand) != STANDALONE_BLOCKS:
        raise AssertionError(f"standalone block count drift: {len(stand)}")
    _r0, _r1, _s0, _s1, op = o_zero.design(pd, ans)

    rhs = np.zeros((pd.npts, len(stand)), dtype=np.int64)
    avec_object = avec.astype(object)
    for column, block in enumerate(stand):
        slab = Acol[block * pd.npts : (block + 1) * pd.npts].astype(object)
        rhs[:, column] = [int(x) for x in (-(slab @ avec_object)) % p]

    fit_matrix = op[:fit_rows].astype(np.int64)
    X, rank, piv, nbad = fastlin.solve(fit_matrix, rhs[:fit_rows], p, nb=nb)
    X = np.asarray(X, dtype=np.int64) % p
    pivots = [int(x) for x in piv]
    if rank != EXPECTED_RANK or len(pivots) != EXPECTED_RANK or nbad != 0:
        raise RuntimeError(f"lex-pivot affine solve failed: rank={rank} piv={len(pivots)} nbad={nbad}")
    if pivots != sorted(pivots) or len(set(pivots)) != len(pivots):
        raise AssertionError("lex-pivot solver returned noncanonical pivot ordering")
    pivot_sha = _pivot_sha(pivots)
    if expected_pivot_sha256 is not None and pivot_sha != expected_pivot_sha256:
        raise RuntimeError(
            f"lex-pivot set drift at n={n}: {pivot_sha} != {expected_pivot_sha256}"
        )

    pivot_set = set(pivots)
    nonpivots = np.asarray([i for i in range(ans.nc) if i not in pivot_set], dtype=np.int64)
    if len(nonpivots) != E1_COLUMNS - EXPECTED_RANK:
        raise AssertionError("lex-pivot nonpivot dimension drift")
    if np.count_nonzero(X[nonpivots] % p):
        raise RuntimeError("lex-pivot canonical solution has nonzero free coordinates")

    fresh = o_zero.matmul_mod(op[fit_rows:], X.astype(np.float64), p)
    fresh = (fresh - rhs[fit_rows:]) % p
    fresh_violations = int(np.count_nonzero(fresh))
    if fresh_violations:
        raise RuntimeError(f"fresh residual violations: {fresh_violations}")

    section_i4 = np.asarray(X, dtype="<i4", order="C")
    primitive_digest = _sha256_bytes(section_i4.tobytes(order="C"))
    a0 = int(avec[0]) % p
    normalized_digest = None
    if a0:
        inv = pow(a0, p - 2, p)
        normalized = np.asarray((X.astype(object) * inv) % p, dtype="<i4", order="C")
        normalized_digest = _sha256_bytes(normalized.tobytes(order="C"))

    coordinate_map = {
        "section_mode": SECTION_MODE,
        "e1_columns": ans.nc,
        "r_columns": len(ans.mons_r),
        "s_columns": len(ans.mons_s),
        "mons_r": [[int(a), int(b)] for a, b in ans.mons_r],
        "mons_s": [[int(a), int(b)] for a, b in ans.mons_s],
        "pivot_indices": pivots,
        "pivot_sha256": pivot_sha,
        "standalone_blocks": [str(pd.B[j]) for j in stand],
    }
    record = {
        "n": n,
        "prime": p,
        "a_mod_p": [int(x) for x in avec],
        "a0_mod_p": a0,
        "rank": int(rank),
        "solver_nbad": int(nbad),
        "fit_rows": fit_rows,
        "fresh_rows": fresh_rows,
        "fresh_violations": fresh_violations,
        "pivot_sha256": pivot_sha,
        "primitive_section_sha256": primitive_digest,
        "normalized_section_sha256": normalized_digest,
    }
    return section_i4, {"record": record, "coordinate_map": coordinate_map}


def _worker(task: tuple[int, int, int, int, int, str]) -> tuple[int, np.ndarray, dict]:
    n, p, fit_rows, fresh_rows, nb, expected = task
    section, data = _lex_shape(n, p, fit_rows, fresh_rows, nb, expected)
    return n, section, data


def run_chunk(
    request_path: Path | str,
    source: Path | str,
    chunk_index: int,
    output: Path | str,
) -> dict:
    request_path = Path(request_path)
    request = load_request(request_path)
    if not request["enabled"]:
        raise AssertionError("refusing to execute disabled lex-pivot sweep request")
    chunk_index = int(chunk_index)
    ranges = chunk_ranges(request)
    if not 0 <= chunk_index < len(ranges):
        raise AssertionError("chunk index outside request")
    start, stop = ranges[chunk_index]
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    source = Path(source).resolve()
    source_identity = verify_source_checkout(source, request)

    cache_path = output / "qrow_cache.pkl"
    _install_source_modules(source, cache_path, prewarm=True)

    p = int(request["prime"])
    fit_rows = EXPECTED_RANK + int(request["fit_extra_rows"])
    fresh_rows = int(request["fresh_rows"])
    nb = int(request["solver_block_size"])
    expected = str(request["expected_pivot_sha256"])
    tasks = [
        (n, p, fit_rows, fresh_rows, nb, expected)
        for n in range(start, stop + 1)
    ]
    workers = min(int(request["workers_per_chunk"]), len(tasks))
    ctx = mp.get_context("spawn")
    with ctx.Pool(
        processes=workers,
        initializer=_worker_init,
        initargs=(str(source), str(cache_path)),
    ) as pool:
        rows = list(pool.imap_unordered(_worker, tasks, chunksize=1))
    rows.sort(key=lambda item: item[0])

    expected_ns = list(range(start, stop + 1))
    if [row[0] for row in rows] != expected_ns:
        raise AssertionError("chunk n ordering/coverage drift")
    sections = np.stack([row[1] for row in rows]).astype("<i4", copy=False)
    records = [row[2]["record"] for row in rows]
    coordinate_map = rows[0][2]["coordinate_map"]
    for row in rows[1:]:
        if row[2]["coordinate_map"] != coordinate_map:
            raise AssertionError("pivot or coordinate map changed inside chunk")
    if coordinate_map["pivot_sha256"] != expected:
        raise AssertionError("chunk pivot digest differs from request")

    coordinate_bytes = _canonical_json_bytes(coordinate_map)
    coordinate_sha = _sha256_bytes(coordinate_bytes)
    np.savez_compressed(output / "sections.npz", sections=sections)
    (output / "coordinate-map.json").write_bytes(coordinate_bytes)
    shutil.copyfile(request_path, output / "request.json")
    metadata = {
        "schema_version": "1.0.0",
        "request_id": request["request_id"],
        "section_mode": SECTION_MODE,
        "chunk_index": chunk_index,
        "n_start": start,
        "n_stop": stop,
        "sample_count": len(rows),
        "source": source_identity,
        "prime": p,
        "fit_rows": fit_rows,
        "fresh_rows": fresh_rows,
        "section_coordinates": E1_COLUMNS,
        "expected_rank": EXPECTED_RANK,
        "standalone_blocks": STANDALONE_BLOCKS,
        "pivot_sha256": expected,
        "coordinate_map_sha256": coordinate_sha,
        "records": records,
        "evidence_effect": request["evidence_effect"],
        "proof_effect": request["proof_effect"],
        "promotion_effect": request["promotion_effect"],
    }
    (output / "metadata.json").write_bytes(_canonical_json_bytes(metadata))
    cache_path.unlink(missing_ok=True)
    return metadata


def verify_chunk(
    request_path: Path | str,
    chunk_index: int,
    output: Path | str,
) -> dict:
    request = load_request(request_path)
    output = Path(output)
    metadata = json.loads((output / "metadata.json").read_text(encoding="utf-8"))
    coordinate_bytes = (output / "coordinate-map.json").read_bytes()
    coordinate_map = json.loads(coordinate_bytes)
    if _sha256_bytes(_canonical_json_bytes(coordinate_map)) != metadata["coordinate_map_sha256"]:
        raise AssertionError("coordinate map digest mismatch")
    if metadata["request_id"] != request["request_id"]:
        raise AssertionError("artifact request identity mismatch")
    if metadata["section_mode"] != SECTION_MODE or coordinate_map["section_mode"] != SECTION_MODE:
        raise AssertionError("artifact section mode mismatch")
    if int(metadata["chunk_index"]) != int(chunk_index):
        raise AssertionError("artifact chunk identity mismatch")
    start, stop = chunk_ranges(request)[int(chunk_index)]
    if [metadata["n_start"], metadata["n_stop"]] != [start, stop]:
        raise AssertionError("artifact n-range mismatch")
    expected_pivot_sha = str(request["expected_pivot_sha256"])
    if metadata["pivot_sha256"] != expected_pivot_sha:
        raise AssertionError("artifact pivot digest mismatch")
    pivots = [int(x) for x in coordinate_map["pivot_indices"]]
    if len(pivots) != EXPECTED_RANK or _pivot_sha(pivots) != expected_pivot_sha:
        raise AssertionError("artifact pivot set mismatch")
    pivot_set = set(pivots)
    nonpivots = np.asarray([i for i in range(E1_COLUMNS) if i not in pivot_set], dtype=np.int64)
    if len(nonpivots) != E1_COLUMNS - EXPECTED_RANK:
        raise AssertionError("artifact nonpivot dimension mismatch")

    with np.load(output / "sections.npz", allow_pickle=False) as archive:
        sections = np.asarray(archive["sections"])
    expected_shape = (stop - start + 1, E1_COLUMNS, STANDALONE_BLOCKS)
    if sections.shape != expected_shape or sections.dtype != np.dtype("<i4"):
        raise AssertionError(f"section array drift: {sections.shape} {sections.dtype}")
    records = metadata["records"]
    if len(records) != sections.shape[0]:
        raise AssertionError("record count drift")
    p = int(request["prime"])
    for index, record in enumerate(records):
        n = start + index
        if int(record["n"]) != n:
            raise AssertionError("record n ordering drift")
        if int(record["rank"]) != EXPECTED_RANK:
            raise AssertionError("rank failure in preserved artifact")
        if int(record["solver_nbad"]) != 0 or int(record["fresh_violations"]) != 0:
            raise AssertionError("failed solve preserved as evidence")
        if record["pivot_sha256"] != expected_pivot_sha:
            raise AssertionError(f"pivot drift preserved at n={n}")
        section = np.asarray(sections[index], dtype="<i4", order="C")
        if np.count_nonzero(section[nonpivots] % p):
            raise AssertionError(f"nonpivot coordinate violation at n={n}")
        if _sha256_bytes(section.tobytes(order="C")) != record["primitive_section_sha256"]:
            raise AssertionError(f"primitive section digest mismatch at n={n}")
        a0 = int(record["a0_mod_p"]) % p
        normalized_digest = record["normalized_section_sha256"]
        if a0:
            inv = pow(a0, p - 2, p)
            normalized = np.asarray((section.astype(object) * inv) % p, dtype="<i4", order="C")
            if _sha256_bytes(normalized.tobytes(order="C")) != normalized_digest:
                raise AssertionError(f"normalized section digest mismatch at n={n}")
        elif normalized_digest is not None:
            raise AssertionError("normalized digest present at singular a0 fiber")
    return {
        "request_id": request["request_id"],
        "chunk_index": int(chunk_index),
        "n_start": start,
        "n_stop": stop,
        "samples_verified": len(records),
        "pivot_sha256": expected_pivot_sha,
        "coordinate_map_sha256": metadata["coordinate_map_sha256"],
        "proof_effect": metadata["proof_effect"],
        "promotion_effect": metadata["promotion_effect"],
    }


def verify_sweep(request_path: Path | str, outputs: list[Path | str]) -> dict:
    request = load_request(request_path)
    if len(outputs) != int(request["chunks"]):
        raise AssertionError("full-sweep verification requires every chunk")
    expected_pivot_sha = str(request["expected_pivot_sha256"])
    coordinate_map_sha = None
    verified = 0
    next_n = int(request["n_start"])
    for chunk_index, output in enumerate(outputs):
        result = verify_chunk(request_path, chunk_index, output)
        if result["n_start"] != next_n:
            raise AssertionError("full-sweep coverage gap or overlap")
        next_n = result["n_stop"] + 1
        verified += int(result["samples_verified"])
        if result["pivot_sha256"] != expected_pivot_sha:
            raise AssertionError("full-sweep pivot drift")
        if coordinate_map_sha is None:
            coordinate_map_sha = result["coordinate_map_sha256"]
        elif result["coordinate_map_sha256"] != coordinate_map_sha:
            raise AssertionError("full-sweep coordinate map drift")
    if next_n != int(request["n_stop"]) + 1:
        raise AssertionError("full-sweep terminal coverage drift")
    total = int(request["n_stop"]) - int(request["n_start"]) + 1
    if verified != total:
        raise AssertionError("full-sweep sample count drift")
    return {
        "request_id": request["request_id"],
        "samples_verified": verified,
        "n_start": int(request["n_start"]),
        "n_stop": int(request["n_stop"]),
        "pivot_sha256": expected_pivot_sha,
        "coordinate_map_sha256": coordinate_map_sha,
        "rational_degree_test_bound": request["rational_degree_test_bound"],
        "proof_effect": request["proof_effect"],
        "promotion_effect": request["promotion_effect"],
    }
