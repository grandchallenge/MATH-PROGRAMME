#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "governance/policy_shard_registry.json"


def _stream_command(cmd: list[str], *, log_handle) -> int:
    proc = subprocess.Popen(
        cmd,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    if proc.stdout is None:
        raise RuntimeError("policy shard subprocess stdout unavailable")
    for line in proc.stdout:
        sys.stdout.write(line)
        sys.stdout.flush()
        log_handle.write(line)
        log_handle.flush()
    return proc.wait()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard", required=True)
    parser.add_argument("--log")
    args = parser.parse_args()
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        if data.get("registry_id") != "MP-POLICY-SHARDS-001":
            raise RuntimeError("policy shard registry identity drift")
        commands = data.get("shards", {}).get(args.shard)
        if not isinstance(commands, list) or not commands:
            raise RuntimeError(f"unknown or empty policy shard: {args.shard}")
        log = Path(args.log) if args.log else ROOT / f"policy-shard-{args.shard}.log"
        shard_started = time.perf_counter()
        with log.open("w", encoding="utf-8") as handle:
            for index, cmd in enumerate(commands, 1):
                if not isinstance(cmd, list) or not cmd or not all(isinstance(item, str) and item for item in cmd):
                    raise RuntimeError("invalid shard command")
                rendered = " ".join(cmd)
                prefix = f"[{args.shard} {index}/{len(commands)}] {rendered}"
                print(prefix, flush=True)
                handle.write("$ " + rendered + "\n")
                handle.flush()
                started = time.perf_counter()
                returncode = _stream_command(cmd, log_handle=handle)
                elapsed = time.perf_counter() - started
                timing = (
                    f"POLICY_SHARD_TIMING shard={args.shard} operation={index} "
                    f"seconds={elapsed:.3f} status={'PASS' if returncode == 0 else 'FAIL'}\n"
                )
                print(timing, end="", flush=True)
                handle.write(timing)
                handle.flush()
                if returncode:
                    return returncode
        total = time.perf_counter() - shard_started
        print(f"POLICY_SHARD_TIMING_TOTAL shard={args.shard} seconds={total:.3f}")
        print(f"policy shard {args.shard}: success")
        return 0
    except (OSError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"policy shard execution error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
