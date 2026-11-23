"""Entrypoint for the news-image-20261123 entry.

Decodes the bundled base64 front-page image and writes it to
/output/entry.png, creating /output if it does not exist.

Standard library only. No network access, no randomness, no
command-line arguments: the output is byte-identical on every run.
"""

import base64
import os
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    b64_path = os.path.join(here, "entry.png.b64")
    with open(b64_path, "rb") as handle:
        payload = base64.b64decode(handle.read())
    if not payload.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("bundled image is not a PNG")
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as handle:
        handle.write(payload)
    print("wrote {} ({} bytes)".format(out_path, len(payload)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
