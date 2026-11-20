#!/usr/bin/env python3
"""Entrypoint: copy entry.png to the output directory.

Writes entry.png beside this file to /output/entry.png, or to
$MAKEFUN_OUTPUT_DIR/entry.png when that variable is set (for local testing).
Fails loudly if entry.png is missing or is not a PNG file.
"""
import os
import shutil
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print(f"ERROR: {src} does not exist", file=sys.stderr)
        sys.exit(1)
    with open(src, "rb") as fh:
        header = fh.read(8)
    if header != PNG_SIGNATURE:
        print(f"ERROR: {src} is not a PNG file (bad 8-byte signature)",
              file=sys.stderr)
        sys.exit(1)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")


if __name__ == "__main__":
    main()
