#!/usr/bin/env python3
"""news-23 b153 numbers-led entry verifier + emitter (stdlib only, no PIL).

Reads the entry.png stored next to this file, verifies it is a valid
1024x1024 PNG (manual header parse via struct, chunk-walk with CRC
checks), then writes a byte-identical copy to
os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"), "entry.png").

Guards: refuses an empty MAKEFUN_OUTPUT_DIR, one inside this repo,
or one that is a file; refuses to overwrite the source image; never
writes next to main.py (the grader runs this from a read-only copy).
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "ff2b51a83b066e1b7cffaad12fabcae207ad3f1e19b834563025281574f37143"
EXPECTED_SIZE = 164720
MIN_SIZE = 10000
MAX_SIZE = 1024 * 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def check_png(data):
    """Validate PNG bytes. Returns (width, height). Raises SystemExit."""
    if len(data) < MIN_SIZE:
        fail(f"PNG too small: {len(data)} bytes (min {MIN_SIZE})")
    if len(data) > MAX_SIZE:
        fail(f"PNG too large: {len(data)} bytes (max {MAX_SIZE})")
    if data[:8] != PNG_SIGNATURE:
        fail("bad PNG signature")
    # First chunk must be IHDR, 13 bytes of data.
    # Chunk layout: 4-byte length, 4-byte type, data, 4-byte CRC.
    # CRC covers type + data, NOT the length field (length is excluded).
    (length,) = struct.unpack(">I", data[8:12])
    ctype = data[12:16]
    if ctype != b"IHDR":
        fail("first chunk is not IHDR")
    if length != 13:
        fail(f"IHDR length {length} != 13")
    ihdr = data[16:29]
    crc_stored, = struct.unpack(">I", data[29:33])
    crc_calc = zlib.crc32(b"IHDR" + ihdr) & 0xFFFFFFFF
    if crc_stored != crc_calc:
        fail("IHDR CRC mismatch")
    (w, h, depth, ctype_b, comp, filt, inter) = struct.unpack(">IIBBBBB", ihdr)
    if (w, h) != (1024, 1024):
        fail(f"bad dimensions {w}x{h} (want 1024x1024)")
    if depth != 8:
        fail(f"bad bit depth {depth} (want 8)")
    if ctype_b not in (2, 6):
        fail(f"bad colour type {ctype_b} (want 2 or 6)")
    if comp != 0 or filt != 0 or inter != 0:
        fail("compression/filter/interlace must all be 0")
    # Chunk walk: verify every CRC, require non-empty IDAT payload,
    # and require a 0-byte IEND as the final chunk with no trailing data.
    pos = 33
    idat_total = 0
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            fail("truncated chunk header")
        (clen,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        if pos + 12 + clen > len(data):
            fail(f"truncated chunk {ctype!r}")
        cdata = data[pos + 8:pos + 8 + clen]
        crc_stored, = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])
        crc_calc = zlib.crc32(ctype + cdata) & 0xFFFFFFFF
        if crc_stored != crc_calc:
            fail(f"CRC mismatch in chunk {ctype!r}")
        if ctype == b"IDAT":
            if clen == 0:
                fail("empty IDAT chunk")
            idat_total += clen
        if ctype == b"IEND":
            if clen != 0:
                fail("IEND must be 0 bytes")
            if pos + 12 != len(data):
                fail("trailing data after IEND")
            seen_iend = True
            break
        pos += 12 + clen
    if not seen_iend:
        fail("missing IEND chunk")
    if idat_total < 1000:
        fail(f"IDAT payload too small: {idat_total} bytes")
    return w, h


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir_raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir_raw:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir = os.path.abspath(out_dir_raw)
    if os.path.isfile(out_dir):
        fail(f"MAKEFUN_OUTPUT_DIR is a file: {out_dir}")
    if os.path.commonpath([out_dir, here]) == here:
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    out_path = os.path.join(out_dir, "entry.png")
    if os.path.abspath(out_path) == os.path.abspath(src):
        fail("output would overwrite the source image")
    if not os.path.isfile(src):
        fail(f"source entry.png not found: {src}")
    with open(src, "rb") as f:
        data = f.read()
    if len(data) != EXPECTED_SIZE:
        fail(f"size {len(data)} != expected {EXPECTED_SIZE}")
    sha = hashlib.sha256(data).hexdigest()
    if sha != EXPECTED_SHA256:
        fail(f"sha256 {sha} != expected {EXPECTED_SHA256}")
    check_png(data)
    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(data)
    # Re-read the output and confirm it is byte-identical.
    with open(out_path, "rb") as f:
        back = f.read()
    if back != data:
        fail("output differs from source after write")
    print(f"OK entry.png {len(data)} bytes sha256={sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
