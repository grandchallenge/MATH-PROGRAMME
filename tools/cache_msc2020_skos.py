#!/usr/bin/env python3
"""Create and verify the ignored MSC2020-SKOS cache."""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

REPOSITORY = "https://github.com/TIBHannover/MSC2020_SKOS.git"
REVISION = "33972ddb6a72c3660a6e499ee5f881b57fa92d41"


def run(*args: str, cwd: Path | None = None) -> str:
    completed = subprocess.run(
        args,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / ".cache" / "msc2020-skos",
    )
    args = parser.parse_args()
    cache_dir = args.cache_dir.resolve()

    if not (cache_dir / ".git").exists():
        cache_dir.parent.mkdir(parents=True, exist_ok=True)
        run("git", "clone", "--no-checkout", REPOSITORY, str(cache_dir))

    remote = run("git", "remote", "get-url", "origin", cwd=cache_dir)
    if remote.rstrip("/") != REPOSITORY.rstrip("/"):
        raise SystemExit(f"unexpected MSC cache remote: {remote}")

    run("git", "fetch", "origin", REVISION, cwd=cache_dir)
    run("git", "checkout", "--detach", REVISION, cwd=cache_dir)
    actual = run("git", "rev-parse", "HEAD", cwd=cache_dir)
    if actual != REVISION:
        raise SystemExit(f"MSC cache revision mismatch: {actual}")

    print(f"verified MSC2020-SKOS cache at {cache_dir} ({actual})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
