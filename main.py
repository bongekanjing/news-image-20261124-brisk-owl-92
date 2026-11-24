#!/usr/bin/env python3
"""Copy the committed front page to the grader's output directory.

The page is drawn once by render/page.py (Pillow, outside the grader) and the
finished PNG is committed beside this file. The grader has no Pillow and no
network, so the entry ships the bytes and this program places them where the
grader reads them: MAKEFUN_OUTPUT_DIR, which is /output inside the sandbox.

Standard library only. Two runs write the same bytes because the input file is
never modified.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main():
    if not os.path.isfile(SOURCE):
        sys.stderr.write("entry.png is missing beside main.py\n")
        return 1

    dest_dir = output_dir()
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "entry.png")

    shutil.copyfile(SOURCE, dest)

    # Read it back and prove the bytes landed intact.
    with open(SOURCE, "rb") as fh:
        want = fh.read()
    with open(dest, "rb") as fh:
        got = fh.read()

    if got != want:
        sys.stderr.write("copy did not match: %d vs %d bytes\n"
                         % (len(want), len(got)))
        return 1
    if len(want) > 1048576:
        sys.stderr.write("entry is %d bytes, over the 1 MiB cap\n" % len(want))
        return 1

    sys.stdout.write("%s %d bytes sha256=%s\n"
                     % (dest, len(want), hashlib.sha256(want).hexdigest()[:16]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
