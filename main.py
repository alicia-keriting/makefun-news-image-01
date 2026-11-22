#!/usr/bin/env python3
"""Entry for make.fun competition news-image-20261122.

The image is already made: entry.png sits beside this file. The program writes
it to the competition's output directory byte for byte, and prints one line of
proof (the byte count and the sha256 of what it wrote).

Python 3.13, standard library only, no network. It reads nothing but
entry.png next to this file. Deterministic by construction: the output bytes
are the image's own bytes, written straight out, with no timestamp, no
temporary file and nothing random, so two runs write identical bytes.

    python3 main.py                      # writes /output/entry.png
    MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
"""

import hashlib
import os
import sys
from pathlib import Path

IMAGE = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"
CHUNK = 1 << 16  # 64 KiB: copy in bounded memory, hash as it goes


def main() -> int:
    source = Path(__file__).resolve().parent / IMAGE
    out_env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    out_dir = Path(out_env) if out_env else Path(DEFAULT_OUTPUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / IMAGE

    digest = hashlib.sha256()
    total = 0
    with source.open("rb") as src, target.open("wb") as dst:
        while True:
            chunk = src.read(CHUNK)
            if not chunk:
                break
            dst.write(chunk)
            digest.update(chunk)
            total += len(chunk)

    print(f"{target}: {total} bytes, sha256 {digest.hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
