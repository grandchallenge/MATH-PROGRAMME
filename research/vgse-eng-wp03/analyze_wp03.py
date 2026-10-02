#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from wp03_core import OUTPUT
from wp03_build import build_results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    generated = build_results()
    if args.check:
        retained = json.loads(OUTPUT.read_text(encoding="utf-8"))
        if retained != generated:
            raise AssertionError("RESULTS.json does not match deterministic replay")
        print("VGSE-ENG-WP03 deterministic replay: PASS")
        return 0
    OUTPUT.write_text(json.dumps(generated, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(generated, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
