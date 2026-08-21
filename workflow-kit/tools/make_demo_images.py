from __future__ import annotations

import argparse
import struct
import zlib
from pathlib import Path


def png_chunk(chunk_type: bytes, data: bytes) -> bytes:
    crc = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", crc)


def write_solid_png(path: Path, width: int, height: int, rgb: tuple[int, int, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw_rows = []
    row = bytes(rgb) * width
    for _ in range(height):
        raw_rows.append(b"\x00" + row)
    raw = b"".join(raw_rows)
    png = b"\x89PNG\r\n\x1a\n"
    png += png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += png_chunk(b"IDAT", zlib.compress(raw, level=9))
    png += png_chunk(b"IEND", b"")
    path.write_bytes(png)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create placeholder 1080x1440 PNG images for workflow testing.")
    parser.add_argument("--project", required=True, help="Project directory.")
    parser.add_argument("--id", default="demo", help="Image folder id under assets/images.")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    image_dir = project / "assets" / "images" / args.id
    colors = [(245, 245, 245), (238, 242, 255), (245, 240, 232)]
    names = ["01-cover.png", "02-detail.png", "03-workflow.png"]
    for name, color in zip(names, colors):
        write_solid_png(image_dir / name, 1080, 1440, color)
        print(f"Wrote {image_dir / name}")
    print("These are placeholder test images. Replace them before real publishing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

